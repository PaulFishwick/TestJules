import json
import datetime
import os
import collections
import string
import subprocess
import sys
import random
from typing import Union, Dict

from .style_guide import frederick_turner_style

PRONOUNCING_AVAILABLE = False
try:
    import pronouncing
    PRONOUNCING_AVAILABLE = True
    print("Pronouncing library imported successfully.")
except ImportError:
    print("Pronouncing library not found. Attempting to install...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pronouncing"])
        print("Pronouncing library installation attempted. Re-importing...")
        import site
        from importlib import reload
        reload(site)
        import pronouncing
        PRONOUNCING_AVAILABLE = True
        print("Pronouncing library imported successfully after installation attempt.")
    except Exception as e:
        print(f"Could not install or import Pronouncing library after attempt: {e}. Dynamic rhyming/syllable counting will be disabled.")

class PoetryAgent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.generation_counter = 0
        self.last_prompt_generated_by_me = None
        self.templates = {}

        self.common_words_filter = {
            "a", "an", "the", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
            "do", "does", "did", "will", "would", "should", "can", "could", "may", "might", "must",
            "and", "but", "or", "nor", "for", "so", "yet", "if", "then", "else", "when", "where",
            "why", "how", "what", "which", "who", "whom", "whose", "of", "at", "by", "from", "to",
            "in", "out", "on", "off", "over", "under", "again", "further", "once", "here", "there",
            "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no",
            "not", "only", "own", "same", "than", "too", "very", "s", "t", "just", "don",
            "shouldve", "now", "d", "ll", "m", "o", "re", "ve", "y", "ain", "aren", "couldn",
            "didn", "doesn", "hadn", "hasn", "haven", "isn", "ma", "mightn", "mustn", "needn",
            "shan", "shouldn", "wasn", "weren", "won", "wouldn", "i", "me", "my", "myself",
            "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves",
            "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
            "they", "them", "their", "theirs", "themselves", "prompt", "kw1", "kw2",
            "reference_phrase", "alpha", "beta","noted", "turn", "core", "argument", "attempt",
            "proceed", "foundation", "seed", "logic", "creed", "elaborates", "need", "leads",
            "reflections", "confines", "unblocked", "thesis", "interlocked", "concludes", "unlock",
            "spun", "dream", "sun", "fun", "muses", "run", "alight", "stray", "yesterday", "spirit",
            "wanders", "play", "bloomed", "shimmer", "gloom", "fancies", "roam", "home"
        }

    def _count_syllables_for_word(self, word: str) -> int:
        if not word: return 0
        if not PRONOUNCING_AVAILABLE:
            num_vowels = sum(1 for char_in_word in word.lower() if char_in_word in "aeiou")
            syl_count = max(1, num_vowels) if num_vowels > 0 else (1 if len(word) > 0 else 0)
            print(f"    [Syllable Fallback - No Pronouncing] Word '{word}': Approx syllables: {syl_count}")
            return syl_count
        try:
            word_lower = word.lower()
            cleaned_word = word_lower.strip(string.punctuation)
            if not cleaned_word: return 0

            counts = pronouncing.syllable_count(cleaned_word)
            if counts > 0:
                # print(f"    [Syllable CMUdict] Word '{cleaned_word}': Syllables: {counts}")
                return counts

            print(f"    [Syllable Fallback] Word '{cleaned_word}' not in CMUdict. Using vowel group count.")
            num_vowels = 0
            last_char_was_vowel = False
            for char_val in cleaned_word:
                is_vowel = char_val in "aeiouy"
                if is_vowel and not last_char_was_vowel: num_vowels += 1
                last_char_was_vowel = is_vowel

            if len(cleaned_word) > 2 and cleaned_word.endswith("e") and not cleaned_word.endswith("le") and num_vowels > 1:
                if cleaned_word[-2] not in "aeiouy":
                     if not (cleaned_word.endswith("es") and len(cleaned_word) > 3 and cleaned_word[-3] not in "aeiouy"):
                        if not (cleaned_word.endswith("le") and len(cleaned_word) > 2 and cleaned_word[-3] not in "aeiouy"):
                            num_vowels -=1

            final_syl_count = max(1, num_vowels) if cleaned_word else 0
            print(f"    [Syllable Fallback] Approx syllables for '{cleaned_word}': {final_syl_count}")
            return final_syl_count
        except Exception as e:
            print(f"    [Syllable Error] Error counting syllables for '{word}': {e}. Defaulting to 1.")
            return 1

    def _count_syllables_in_line(self, line_words: list) -> int:
        if not line_words: return 0
        total_syllables = 0
        for word in line_words:
            syl = self._count_syllables_for_word(word)
            total_syllables += syl
        print(f"    [Line Syllable Count] For line: '{' '.join(line_words)}', CALC SYL: {total_syllables}")
        return total_syllables

    def _generate_haiku_line(self, theme_prompt: str, kw1: str, kw2: str, target_syl: int, line_number: int) -> str:
        if not PRONOUNCING_AVAILABLE:
            return "(Syllable counting unavailable)"

        line_attempts = 0
        max_attempts = 30

        alpha_1syl_words = ["wise", "deep", "clear", "true", "strong", "form", "thus", "one", "all", "past", "vast", "still", "mark", "fact"]
        alpha_2syl_words = ["reason", "logic", "future", "structure", "order", "wisdom", "pattern", "essence", "concept"]
        beta_1syl_words = ["soft", "light", "hush", "mist", "far", "dim", "soul", "dream", "now", "deep", "calm", "sky", "moon", "star"]
        beta_2syl_words = ["hidden", "secret", "spirit", "wonder", "magic", "echo", "flowing", "drifting", "fading"]

        persona_1syl = alpha_1syl_words if self.agent_name.lower() == 'alpha' else beta_1syl_words
        persona_2syl = alpha_2syl_words if self.agent_name.lower() == 'alpha' else beta_2syl_words
        # persona_3syl not used in this simplified adjustment logic but kept for potential future

        safe_kw1 = kw1 if kw1 else "theme"
        safe_kw2 = kw2 if kw2 else "idea"

        patterns = []
        if self.agent_name.lower() == 'alpha':
            patterns = [[safe_kw1, random.choice(persona_1syl), safe_kw2], [random.choice(persona_2syl), safe_kw1], [safe_kw1, "is", safe_kw2]]
        else: # Beta
            patterns = [[random.choice(persona_1syl), safe_kw1, safe_kw2], [safe_kw1, "like", random.choice(beta_2syl_words)], ["Ah,", safe_kw1]]

        current_line_words = [str(w) for w in random.choice(patterns) if w is not None and str(w).strip()]
        if not current_line_words: current_line_words = [safe_kw1]

        best_attempt_words = list(current_line_words)
        best_attempt_syllables = self._count_syllables_in_line(best_attempt_words)

        while line_attempts < max_attempts:
            line_attempts += 1
            current_line_words = [str(w) for w in current_line_words if w and str(w).strip()]
            if not current_line_words: current_line_words = [random.choice(persona_1syl)] if persona_1syl else [safe_kw1]

            current_syllables = self._count_syllables_in_line(current_line_words)

            print(f"    Haiku Line Gen Attempt {line_attempts}: '{' '.join(current_line_words)}' - Calculated Syllables: {current_syllables} (Target: {target_syl})")

            if current_syllables == target_syl:
                final_line_str = " ".join(current_line_words)
                if self.agent_name.lower() == 'alpha': final_line_str = final_line_str.capitalize() + "."
                else: final_line_str = final_line_str.capitalize() + random.choice(["...", ".", "!"])
                print(f"[{self.agent_name}] Line {line_number} ({target_syl} syl): SUCCEEDED. Line: '{final_line_str}' (Syllables: {current_syllables})")
                return final_line_str

            if abs(current_syllables - target_syl) < abs(best_attempt_syllables - target_syl):
                best_attempt_words = list(current_line_words); best_attempt_syllables = current_syllables
            elif abs(current_syllables - target_syl) == abs(best_attempt_syllables - target_syl) and current_syllables > best_attempt_syllables :
                best_attempt_words = list(current_line_words); best_attempt_syllables = current_syllables

            diff = target_syl - current_syllables
            if diff > 0:
                word_to_add = None
                if diff >= 2 and persona_2syl: word_to_add = random.choice(persona_2syl)
                elif persona_1syl: word_to_add = random.choice(persona_1syl)
                if word_to_add: current_line_words.append(word_to_add)
                else: current_line_words.append(random.choice(["on", "is"]))
            elif diff < 0:
                if len(current_line_words) > 1:
                    if current_line_words[-1] not in [safe_kw1, safe_kw2] or len(current_line_words) > 2 : current_line_words.pop()
                    else: current_line_words.pop(0)
                elif len(current_line_words) == 1: current_line_words = [random.choice(persona_1syl)] if persona_1syl else ["go"]

        final_line_str = " ".join(best_attempt_words)
        final_syllables = best_attempt_syllables
        if final_syllables != target_syl : # Recalculate if loop ended by max_attempts
             final_syllables = self._count_syllables_in_line(best_attempt_words)

        print(f"[{self.agent_name}] Line {line_number} ({target_syl} syl): FAILED. Best attempt: '{final_line_str}' (Syllables: {final_syllables})")
        return f"({final_line_str} - {target_syl} syl target not met; got {final_syllables})"

    def generate_poetry(self, prompt_data_or_text: Union[str, Dict], session_form_rules: dict) -> str:
        if isinstance(prompt_data_or_text, dict):
            actual_prompt = prompt_data_or_text.get('prompt', "a silent pond")
        else:
            actual_prompt = prompt_data_or_text

        self.last_prompt_generated_by_me = actual_prompt

        cleaned_actual_prompt = ''.join(char.lower() if char.isalnum() or char == "'" or char.isspace() else ' ' for char in actual_prompt)
        prompt_words = [word for word in cleaned_actual_prompt.split() if len(word) > 3 and word not in self.common_words_filter]
        kw1 = prompt_words[0] if len(prompt_words) > 0 else "frog"
        kw2 = prompt_words[1] if len(prompt_words) > 1 else "water"

        form_name = session_form_rules.get('name', "Unknown Form")
        target_line_count = session_form_rules.get('line_count', 3)
        target_syllables_list = session_form_rules.get('syllables', [5, 7, 5])

        print(f"[{self.agent_name}] Generating for form: '{form_name}'. Target lines: {target_line_count}, Syllables: {target_syllables_list} for prompt: '{actual_prompt}'")

        poem_lines = []
        if form_name == "Haiku (3 lines, 5-7-5 syllables)" and PRONOUNCING_AVAILABLE:
            for i in range(target_line_count):
                target_syl = target_syllables_list[i] if i < len(target_syllables_list) else 0
                line_text = self._generate_haiku_line(actual_prompt, kw1, kw2, target_syl, line_number=(i+1))
                poem_lines.append(line_text)
            generated_poem = "\n".join(poem_lines)
        else:
            print(f"[{self.agent_name}] Warning: Form '{form_name}' not Haiku or pronouncing unavailable. Generating basic fallback.")
            poem_lines.append(f"Prompt: {actual_prompt} ({kw1}, {kw2})")
            poem_lines.append("Form rules not for Haiku / Or pronouncing lib missing.")
            poem_lines.append("A simple verse instead.")
            current_len = len(poem_lines)
            if current_len > target_line_count:
                poem_lines = poem_lines[:target_line_count]
            elif current_len < target_line_count:
                padding_needed = target_line_count - current_len
                for _ in range(padding_needed): poem_lines.append("Line added for count.")
            generated_poem = "\n".join(poem_lines)

        return generated_poem

    def interpret_poetry(self, poetry: str) -> dict:
        translator = str.maketrans('', '', string.punctuation.replace("'", ""))
        normalized_poetry = poetry.lower().translate(translator)
        all_words = normalized_poetry.split()
        significant_words = [word for word in all_words if word not in self.common_words_filter and len(word) > 2]

        if not significant_words:
            theme_kw1 = "mystery"
            theme_kw2 = "silence"
        else:
            word_counts = collections.Counter(significant_words)
            most_common = word_counts.most_common(2)
            theme_kw1 = most_common[0][0]
            if len(most_common) > 1:
                theme_kw2 = most_common[1][0]
            else:
                related_fallbacks = {
                    "stars": "sky", "dream": "sleep", "night": "day", "light": "dark",
                    "love": "heart", "time": "eternity", "ocean": "sea", "cosmic": "universe",
                    "robot": "future", "song": "melody", "lonely": "solitude", "space": "void"
                }
                theme_kw2 = related_fallbacks.get(theme_kw1, "meaning")
                if theme_kw1 == theme_kw2:
                    theme_kw2 = "essence" if theme_kw1 != "essence" else "depth"

        interpretation_prompt_templates = [
            lambda kw1, kw2: f"Delve into the connection between {kw1} and {kw2}.",
            lambda kw1, kw2: f"Imagine {kw1} as a secret held by {kw2}—what unfolds?",
            lambda kw1, kw2: f"A reflective dialogue: {kw1} converses with {kw2}.",
            lambda kw1, kw2: f"Explore the hidden meaning of {kw1}'s journey towards {kw2}."
        ]
        template_idx = (len(theme_kw1) + len(theme_kw2) + len(significant_words)) % len(interpretation_prompt_templates)
        new_creative_prompt = interpretation_prompt_templates[template_idx](theme_kw1, theme_kw2)

        if self.last_prompt_generated_by_me and new_creative_prompt == self.last_prompt_generated_by_me:
            template_idx = (template_idx + 1) % len(interpretation_prompt_templates)
            new_creative_prompt = interpretation_prompt_templates[template_idx](theme_kw1, theme_kw2)
            if new_creative_prompt == self.last_prompt_generated_by_me:
                 new_creative_prompt = f"{new_creative_prompt}, from a new perspective."

        lines = poetry.split('\n')
        reference_phrase = None
        start_line_for_ref = 0
        for i in range(start_line_for_ref, len(lines)):
            line = lines[i].strip()
            if not line: continue
            words = line.split()
            significant_line_words = [w for w in words if len(w) >= 3 and w.lower() not in self.common_words_filter]
            if len(significant_line_words) >= 2:
                reference_phrase = " ".join(significant_line_words[:4])
                break
        if reference_phrase is None:
            for line in lines:
                line_content = line.strip()
                if line_content:
                    words_in_line = line_content.split()
                    if len(words_in_line) >= 3: reference_phrase = " ".join(words_in_line[:3]); break
                    elif words_in_line: reference_phrase = " ".join(words_in_line); break
        if reference_phrase is None: reference_phrase = ""

        print(f"[{self.agent_name}] Interpreted keywords: '{theme_kw1}', '{theme_kw2}'. Ref: '{reference_phrase}'. New prompt: '{new_creative_prompt}'")
        return {'prompt': new_creative_prompt, 'reference': reference_phrase}

    def send_message(self, recipient_id: str, message_type: str, payload: str):
        message = {
            "sender_id": self.agent_name, "recipient_id": recipient_id,
            "message_type": message_type, "payload": payload,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }
        filename = f"message_to_{recipient_id}.json"
        try:
            with open(filename, 'w') as f: json.dump(message, f, indent=4)
            print(f"Message from {self.agent_name} sent to {recipient_id} in {filename}")
        except IOError as e: print(f"Error writing message to file {filename}: {e}")

    def receive_message(self) -> dict | None:
        filename = f"message_to_{self.agent_name}.json"
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f: message = json.load(f)
                print(f"Message received by {self.agent_name} from {message.get('sender_id', 'unknown sender')} in {filename}")
                try: os.remove(filename); print(f"Successfully deleted message file: {filename}")
                except OSError as e: print(f"Error deleting message file {filename}: {e}")
                return message
            except json.JSONDecodeError as e: print(f"Error decoding JSON from file {filename}: {e}"); return None
            except IOError as e: print(f"Error reading message file {filename}: {e}"); return None
        return None

if __name__ == '__main__':
    agent_tester = PoetryAgent(agent_name="BardTest")
    print(f"--- Testing {agent_tester.agent_name}'s Haiku Generation & Interpretation ---")
    haiku_rules = {"name": "Haiku (3 lines, 5-7-5 syllables)", "line_count": 3, "syllables": [5, 7, 5], "rhyme_scheme": None}

    print(f"\n--- Test 1: Haiku Generation ---")
    prompt_data1_text = "green frog leaps in pond"
    print(f"Input Prompt Text 1: '{prompt_data1_text}'")
    poem1 = agent_tester.generate_poetry(prompt_data1_text, haiku_rules)
    print(f"[{agent_tester.agent_name} generated Poem 1 (Haiku)]:\n{poem1}")
    print(f"BardTest's last_prompt_generated_by_me is now: '{agent_tester.last_prompt_generated_by_me}'")

    incoming_poem = "Old pond, still and deep,\nA frog jumps, water's sound clear,\nSilence fills the air."
    print(f"\n{agent_tester.agent_name} interpreting incoming Haiku:\n{incoming_poem}")
    interpretation_result = agent_tester.interpret_poetry(incoming_poem)
    print(f"[{agent_tester.agent_name}] Received from interpretation - Prompt: '{interpretation_result['prompt']}', Reference: '{interpretation_result['reference']}'")

    print(f"\n--- Test 2: Haiku Generation from Interpretation ---")
    prompt_data2 = interpretation_result
    print(f"{agent_tester.agent_name} generating Poem 2 using prompt_data: {prompt_data2}")
    poem2 = agent_tester.generate_poetry(prompt_data2, haiku_rules)
    print(f"[{agent_tester.agent_name} generated Poem 2 (Haiku)]:\n{poem2}")
    print(f"BardTest's last_prompt_generated_by_me is now: '{agent_tester.last_prompt_generated_by_me}'")

    print(f"\n--- Test 3: Challenging Haiku Prompt ---")
    prompt_data3_text = "ephemeral cherry blossoms quickly fade"
    prompt_data3 = {'prompt': prompt_data3_text, 'reference': "spring's gentle touch"}
    print(f"{agent_tester.agent_name} generating Poem 3 using prompt_data: {prompt_data3}")
    poem3 = agent_tester.generate_poetry(prompt_data3, haiku_rules)
    print(f"[{agent_tester.agent_name} generated Poem 3 (Haiku)]:\n{poem3}")
    print(f"BardTest's last_prompt_generated_by_me is now: '{agent_tester.last_prompt_generated_by_me}'")
