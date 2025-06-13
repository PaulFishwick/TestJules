import json
import datetime
import os # For file operations like delete and check existence
import collections # For Counter
import string # For punctuation removal

from .style_guide import frederick_turner_style

# Persona: Alpha - The Orator (Formal, Structured, Declarative)
ALPHA_TEMPLATES = {
    0: ("Your point on '{reference_phrase}' is noted; I now turn to '{prompt}'.\n"
        "Let {kw1} and {kw2} bring forth its core, from slumbering thought unkempt.\n"
        "A structured argument, from fallacy exempt,\n"
        "Thus Alpha speaks, a new perspective to attempt."),

    1: ("Considering '{reference_phrase}', my discourse on '{prompt}' shall proceed.\n"
        "With {kw1} as foundation, and {kw2} the vital seed.\n"
        "Observe the logic, a carefully planted creed,\n"
        "Alpha elaborates, fulfilling reason's need."),

    2: ("Indeed, '{reference_phrase}' leads well to my reflections on '{prompt}'.\n"
        "Herein, {kw1} and {kw2} from their confines are promptly unblocked.\n" # Changed from 'unkempt' to avoid repetition
        "A cogent thesis, precisely interlocked,\n"
        "Alpha concludes, ensuring all minds are unlocked.")
}

# Persona: Beta - The Dreamer (Lyrical, Questioning, Abstract)
BETA_TEMPLATES = {
    0: ("'{reference_phrase}'... such curious words you've spun!\n"
        "They make me dream of '{prompt}', neath a cosmic, mystic sun.\n"
        "Do {kw1} and {kw2} join in this ethereal fun?\n"
        "Beta muses, till the course of wonder's run."),

    1: ("Hearing '{reference_phrase}' sets my thoughts alight, towards '{prompt}' they stray.\n"
        "What if {kw1} is but a dream, and {kw2} the light of yesterday?\n"
        "My spirit wanders, come what may,\n"
        "Beta questions, in this soft, reflective play."),

    2: ("When you mentioned '{reference_phrase}', a new idea of '{prompt}' started to bloom!\n"
        "Could {kw1} be the shimmer, and {kw2} escape the gloom?\n"
        "Across this notion, my fancies freely roam,\n"
        "Beta whispers, finding wonder's home.")
}

class PoetryAgent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.generation_counter = 0
        self.last_prompt_generated_by_me = None # For tracking prompt used by this agent for its own generation

        if self.agent_name.lower() == 'alpha':
            self.templates = ALPHA_TEMPLATES
        elif self.agent_name.lower() == 'beta':
            self.templates = BETA_TEMPLATES
        else:
            # Default or fallback if agent name is neither alpha nor beta
            print(f"Warning: Agent name '{self.agent_name}' not recognized for specific persona templates. Using Alpha's templates as default.")
            self.templates = ALPHA_TEMPLATES

        self.common_words_filter = {
            "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "should", "can",
            "could", "may", "might", "must", "and", "but", "or", "nor", "for", "so", "yet",
            "if", "then", "else", "when", "where", "why", "how", "what", "which", "who",
            "whom", "whose", "of", "at", "by", "from", "to", "in", "out", "on", "off",
            "over", "under", "again", "further", "once", "here", "there", "all",
            "any", "both", "each", "few", "more", "most", "other", "some", "such", "no",
            "not", "only", "own", "same", "than", "too", "very", "s", "t",
            "just", "don", "shouldve", "now", "d", "ll", "m", "re", "ve", "y",
            "ain", "aren", "couldn", "didn", "doesn", "hadn", "hasn", "haven", "isn",
            "ma", "mightn", "mustn", "needn", "shan", "shouldn", "wasn", "weren",
            "won", "wouldn", "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
            "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
            "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
            "theirs", "themselves",
            "prompt", "kw1", "kw2", "reference_phrase", # From template placeholders
            "alpha", "beta", # Agent names
            # Common words from Alpha's templates
            "hark", "articulate", "matter", "import", "hold", "court", "observe", "structure", "meticulously",
            "wrought", "reasoned", "discourse", "taught", "consider", "clarity", "precision", "facets",
            "logical", "decision", "fleeting", "whim", "studied", "keen", "vision", "presents", "theme",
            "erudition", "subject", "commands", "stage", "focus", "engage", "sage", "line", "considered",
            "turned", "page", "speaks", "actor", "historys", "point", "noted", "turn", "bring", "forth",
            "core", "slumbering", "thought", "unkempt", "argument", "fallacy", "exempt", "perspective",
            "attempt", "discourse", "proceed", "foundation", "vital", "seed", "logic", "carefully", "planted",
            "creed", "elaborates", "fulfilling", "reasons", "need", "indeed", "leads", "well", "reflections",
            "herein", "confines", "promptly", "unblocked", "cogent", "thesis", "precisely", "interlocked",
            "concludes", "ensuring", "minds", "unlocked", "regarding", "insightful", "anew", "critical",
            "counterpoint", "varied", "grand", "touched", "expanded", "mention",
            # Common words from Beta's templates
            "whispers", "feel", "adrift", "mornings", "dew", "azure", "hue", "thought", "startlingly",
            "wonders", "sharing", "view", "shimmering", "veil", "lost", "echo", "forgotten", "tale",
            "mists", "doubt", "questions", "sail", "ponders", "truths", "prevail", "fail", "imagine",
            "unseen", "unknown", "dances", "lightly", "softly", "sown", "fancy", "uniquely", "queries",
            "mind", "prone", "curious", "spun", "dream", "neath", "cosmic", "mystic", "sun", "join",
            "ethereal", "fun", "muses", "course", "run", "hearing", "sets", "alight", "stray",
            "yesterday", "spirit", "wanders", "come", "may", "reflective", "play", "bloomed", "shimmer",
            "gloom", "notion", "fancies", "freely", "roam", "home", "make", "unfolding", "connection",
            "spoke", "elusive", "drifting", "wistful", "ideas", "combined", "gently", "sparking", "newly",
            "seeds", "beautifully", "grown", "shared", "deep"
        }


    def generate_poetry(self, prompt_data: dict, style_guide: dict) -> str:
        """
        Generates a poem using different templates and keywords from the prompt_data.
        Style_guide is not actively used in this stub but is kept for API consistency.
        prompt_data is expected to be a dict: {'prompt': str, 'reference': str|None}
        """
        actual_prompt = prompt_data['prompt']
        reference_phrase = prompt_data.get('reference')
        if reference_phrase is None:
            reference_phrase = "" # Default to empty string for formatting

        common_filter_words = {
            "a", "an", "the", "is", "of", "on", "in", "to", "for", "with", "theme",
            "about", "response", "poetic", "and", "or", "but", "if", "then", "else",
            "i", "you", "me", "he", "she", "it", "we", "they", "my", "your", "his", "her", "its", "our", "their",
            "what", "when", "where", "why", "how", "thus", "hark", "tale", "verse", "inspired", "unfold",
            "meter", "words", "placed", "lines", "interlaced", "language", "fresh", "avoiding", "cliche",
            "concrete", "scenes", "see", "metaphors", "bloom", "meanings", "deep", "true", "speaks"
        } # Note: agent names 'alpha', 'beta' could be added here if they become too prominent as keywords

        # Sanitize and split actual_prompt for keywords
        cleaned_actual_prompt = ''.join(char.lower() if char.isalnum() or char == "'" or char.isspace() else ' ' for char in actual_prompt)
        prompt_words = [word for word in cleaned_actual_prompt.split() if len(word) > 3 and word not in common_filter_words]

        kw1 = prompt_words[0] if len(prompt_words) > 0 else "stars"
        kw2 = prompt_words[1] if len(prompt_words) > 1 else "dreams"

        # Select template from the agent's persona-specific set
        template_key = self.generation_counter % len(self.templates)
        chosen_template_format_string = self.templates[template_key]

        # Format the chosen template string
        generated_poem = chosen_template_format_string.format(
            prompt=actual_prompt,
            kw1=kw1,
            kw2=kw2,
            reference_phrase=reference_phrase
        )

        self.generation_counter += 1
        self.last_prompt_generated_by_me = actual_prompt # Store the actual_prompt this agent used
        return generated_poem

    def interpret_poetry(self, poetry: str) -> str:
        """
        Interprets received poetry to extract themes and generate a new creative prompt.
        Aims to avoid re-using the prompt this agent last generated with.
        """
        # --- New Theme Keyword Extraction Logic ---
        # Normalize: lowercase, remove punctuation
        translator = str.maketrans('', '', string.punctuation.replace("'", "")) # Keep apostrophes
        normalized_poetry = poetry.lower().translate(translator)
        all_words = normalized_poetry.split()

        # Filter stop words using self.common_words_filter
        significant_words = [word for word in all_words if word not in self.common_words_filter and len(word) > 2]

        if not significant_words:
            theme_kw1 = "mystery"  # Fallback
            theme_kw2 = "silence"  # Fallback
        else:
            word_counts = collections.Counter(significant_words)
            most_common = word_counts.most_common(2) # Get up to 2 most common

            theme_kw1 = most_common[0][0]
            if len(most_common) > 1:
                theme_kw2 = most_common[1][0]
            else:
                # If only one significant word, try to make kw2 related or a general term
                related_fallbacks = { # Simple map for related words
                    "stars": "sky", "dream": "sleep", "night": "day",
                    "light": "dark", "love": "heart", "time": "eternity",
                    "ocean": "sea", "cosmic": "universe", "robot": "future",
                    "song": "melody", "lonely": "solitude", "space": "void"
                }
                theme_kw2 = related_fallbacks.get(theme_kw1, "meaning") # Default fallback for kw2
                if theme_kw1 == theme_kw2: # Avoid kw1 and kw2 being identical
                    theme_kw2 = "essence" if theme_kw1 != "essence" else "depth"

        # --- End of New Theme Keyword Extraction Logic ---

        # Define interpretation prompt templates (using the new theme_kw1, theme_kw2)
        # These are f-strings that will be evaluated *after* theme_kw1 and theme_kw2 are set.
        interpretation_prompt_templates = [
            lambda kw1, kw2: f"Delve into the connection between {kw1} and {kw2}.",
            lambda kw1, kw2: f"Imagine {kw1} as a secret held by {kw2}—what unfolds?",
            lambda kw1, kw2: f"A reflective dialogue: {kw1} converses with {kw2}.",
            lambda kw1, kw2: f"Explore the hidden meaning of {kw1}'s journey towards {kw2}."
        ]

        # Deterministic selection of template
        # Using a different logic than generate_poetry to ensure variety if called sequentially with similar inputs
        # Use len(significant_words) as a proxy for the removed potential_keywords list length
        template_idx = (len(theme_kw1) + len(theme_kw2) + len(significant_words)) % len(interpretation_prompt_templates)
        new_creative_prompt = interpretation_prompt_templates[template_idx](theme_kw1, theme_kw2)

        # Simple check to avoid this agent re-using the exact same prompt it last generated a poem with
        if self.last_prompt_generated_by_me and new_creative_prompt == self.last_prompt_generated_by_me:
            # If it's the same, try the next template in a cycle, or add a suffix
            template_idx = (template_idx + 1) % len(interpretation_prompt_templates)
            new_creative_prompt = interpretation_prompt_templates[template_idx](theme_kw1, theme_kw2)
            if new_creative_prompt == self.last_prompt_generated_by_me: # Still same after trying next?
                 new_creative_prompt = f"{new_creative_prompt}, from a new perspective."

        # Extract reference_phrase from the input poetry
        lines = poetry.split('\n')
        reference_phrase = None

        # Using the same common_words_set as for theme keyword extraction earlier in this method
        # common_words_set for reference phrase extraction will now use self.common_words_filter
        lines = poetry.split('\n') # This was already here for reference_phrase extraction
        reference_phrase = None

        start_line_for_ref = 0
        for i in range(start_line_for_ref, len(lines)):
            line = lines[i].strip()
            if not line:
                continue
            words = line.split()
            significant_line_words = [w for w in words if len(w) >= 3 and w.lower() not in self.common_words_filter] # Use class filter
            if len(significant_line_words) >= 2:
                reference_phrase = " ".join(significant_line_words[:4])
                break
        if reference_phrase is None:
            for line in lines:
                line_content = line.strip()
                if line_content:
                    words_in_line = line_content.split()
                    if len(words_in_line) >= 3:
                        reference_phrase = " ".join(words_in_line[:3])
                        break
                    elif words_in_line:
                        reference_phrase = " ".join(words_in_line)
                        break
        if reference_phrase is None:
            reference_phrase = ""

        print(f"[{self.agent_name}] Interpreted keywords: '{theme_kw1}', '{theme_kw2}'. Ref: '{reference_phrase}'. New prompt: '{new_creative_prompt}'")
        return {'prompt': new_creative_prompt, 'reference': reference_phrase}

    def send_message(self, recipient_id: str, message_type: str, payload: str):
        """
        Constructs a message, serializes it to JSON, and writes it to a file.
        """
        message = {
            "sender_id": self.agent_name,
            "recipient_id": recipient_id,
            "message_type": message_type,
            "payload": payload,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z" # Adding 'Z' for UTC
        }

        filename = f"message_to_{recipient_id}.json"
        try:
            with open(filename, 'w') as f:
                json.dump(message, f, indent=4)
            print(f"Message from {self.agent_name} sent to {recipient_id} in {filename}")
        except IOError as e:
            print(f"Error writing message to file {filename}: {e}")

    def receive_message(self) -> dict | None:
        """
        Checks for a message file, reads it, deserializes it, and then deletes the file.
        """
        filename = f"message_to_{self.agent_name}.json"
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    message = json.load(f)
                print(f"Message received by {self.agent_name} from {message.get('sender_id', 'unknown sender')} in {filename}")

                # Delete the file after successful reading
                try:
                    os.remove(filename)
                    print(f"Successfully deleted message file: {filename}")
                except OSError as e:
                    print(f"Error deleting message file {filename}: {e}")

                return message
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from file {filename}: {e}")
                return None
            except IOError as e:
                print(f"Error reading message file {filename}: {e}")
                return None
        else:
            # print(f"No message file found for {self.agent_name} at {filename}")
            return None

if __name__ == '__main__':
    # Initialize agents
    agent_one_name = "PoetPioneer"
    agent_two_name = "CritiqueCraft"
    # Example Usage within poetry_agent.py
    agent_tester = PoetryAgent(agent_name="BardTest")
    style_to_use = frederick_turner_style # Keep for API consistency

    print(f"--- Testing {agent_tester.agent_name}'s Varied Poem Generation & Interpretation ---")

    # First generation by BardTest
    prompt_data1 = {'prompt': "the song of a lonely robot in space", 'reference': "a silent wish"} # Added a sample reference
    print(f"\nInput Prompt Data 1: {prompt_data1}")
    poem1 = agent_tester.generate_poetry(prompt_data1, style_to_use)
    # The number of templates for Alpha (default for BardTest) is 3.
    print(f"[{agent_tester.agent_name} generated Poem 1 (template {(agent_tester.generation_counter-1) % 3 + 1})]:\n{poem1}")
    print(f"BardTest's last_prompt_generated_by_me is now: '{agent_tester.last_prompt_generated_by_me}'")


    # BardTest interprets another poem (e.g., from another agent)
    incoming_poem = "The stars are cold and distant fires,\nA cosmic ocean of desires.\nEchoes of creation's birth."
    print(f"\n{agent_tester.agent_name} interpreting incoming poem:\n{incoming_poem}")
    interpretation_result = agent_tester.interpret_poetry(incoming_poem)
    # Note: interpret_poetry already prints its findings.
    # The following line is for __main__ to confirm what it received.
    print(f"[{agent_tester.agent_name}] Received from interpretation - Prompt: '{interpretation_result['prompt']}', Reference: '{interpretation_result['reference']}'")


    # BardTest generates its second poem using the derived prompt and reference
    prompt_data2 = interpretation_result # Pass the whole dict
    print(f"\n{agent_tester.agent_name} generating Poem 2 using prompt_data: {prompt_data2}")
    poem2 = agent_tester.generate_poetry(prompt_data2, style_to_use)
    print(f"[{agent_tester.agent_name} generated Poem 2 (template {(agent_tester.generation_counter-1) % 3 + 1})]:\n{poem2}")
    print(f"BardTest's last_prompt_generated_by_me is now: '{agent_tester.last_prompt_generated_by_me}'")

    # Simulate interpreting another poem
    incoming_poem_2 = "A journey to distant stars, a quest for the unknown desires of space."
    print(f"\n{agent_tester.agent_name} interpreting incoming poem 2:\n{incoming_poem_2}")
    interpretation_result_2 = agent_tester.interpret_poetry(incoming_poem_2)
    print(f"[{agent_tester.agent_name}] Received from interpretation 2 - Prompt: '{interpretation_result_2['prompt']}', Reference: '{interpretation_result_2['reference']}'")

    # BardTest generates its third poem
    prompt_data3 = interpretation_result_2
    print(f"\n{agent_tester.agent_name} generating Poem 3 using prompt_data: {prompt_data3}")
    poem3 = agent_tester.generate_poetry(prompt_data3, style_to_use)
    print(f"[{agent_tester.agent_name} generated Poem 3 (template {(agent_tester.generation_counter-1) % 3 + 1})]:\n{poem3}")
    print(f"BardTest's last_prompt_generated_by_me is now: '{agent_tester.last_prompt_generated_by_me}'")

    # Deleting message files that might have been created by previous test runs, if any.
    # This is not strictly related to this test but good practice if this __main__ was more complex.
    # For this specific test, send_message and receive_message are not directly tested in __main__.
    # However, if they were, cleanup would be important.
    # Example:
    # if os.path.exists(f"message_to_{agent_tester.agent_name}.json"):
    #     try:
    #         os.remove(f"message_to_{agent_tester.agent_name}.json")
    #     except OSError:
    #         pass # ignore if deletion fails for some reason
