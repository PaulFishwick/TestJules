import json
import datetime
import os # For file operations like delete and check existence
from .style_guide import frederick_turner_style

# Persona: Alpha - The Orator (Formal, Structured, Declarative)
ALPHA_TEMPLATES = {
    0: ("Hark, I shall articulate on '{prompt}', a matter of import,\n"
        "Where {kw1} and {kw2} hold their court.\n"
        "Observe the structure, meticulously wrought,\n"
        "A reasoned discourse, by Alpha taught."),

    1: ("Let us consider '{prompt}', with clarity and precision,\n"
        "Its facets ({kw1}, {kw2}) shaped by logical decision.\n"
        "No fleeting whim, but studied, keen vision,\n"
        "Alpha presents this theme for your erudition."),

    2: ("The subject '{prompt}' now commands the stage,\n"
        "With {kw1} as a focus, and {kw2} to engage the sage.\n"
        "Each line considered, turned upon the page,\n"
        "So speaks Alpha, actor on history's stage.")
}

# Persona: Beta - The Dreamer (Lyrical, Questioning, Abstract)
BETA_TEMPLATES = {
    0: ("Whispers of '{prompt}', do you feel them too?\n"
        "Like {kw1} adrift in morning's dew, or {kw2} of azure hue.\n"
        "A fleeting thought, what if it's new?\n"
        "Beta wonders, sharing this view with you."),

    1: ("What if '{prompt}' is but a shimmering veil?\n"
        "And {kw1} a lost echo, {kw2} a forgotten tale.\n"
        "Through mists of doubt, my questions sail,\n"
        "Beta ponders, where truths prevail or fail."),

    2: ("Imagine '{prompt}', a world unseen, unknown,\n"
        "Where {kw1} dances lightly, and {kw2} is softly sown.\n"
        "Is this a fancy, uniquely my own?\n"
        "Beta queries, from a mind to wonder prone.")
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


    def generate_poetry(self, input_prompt: str, style_guide: dict) -> str:
        """
        Generates a poem using different templates and keywords from the prompt.
        Style_guide is not actively used in this stub but is kept for API consistency.
        """
        common_filter_words = {
            "a", "an", "the", "is", "of", "on", "in", "to", "for", "with", "theme",
            "about", "response", "poetic", "and", "or", "but", "if", "then", "else",
            "i", "you", "me", "he", "she", "it", "we", "they", "my", "your", "his", "her", "its", "our", "their",
            "what", "when", "where", "why", "how", "thus", "hark", "tale", "verse", "inspired", "unfold",
            "meter", "words", "placed", "lines", "interlaced", "language", "fresh", "avoiding", "cliche",
            "concrete", "scenes", "see", "metaphors", "bloom", "meanings", "deep", "true", "speaks"
        } # Note: agent names 'alpha', 'beta' could be added here if they become too prominent as keywords

        # Sanitize and split prompt for keywords
        cleaned_prompt = ''.join(char.lower() if char.isalnum() or char == "'" or char.isspace() else ' ' for char in input_prompt)
        prompt_words = [word for word in cleaned_prompt.split() if len(word) > 3 and word not in common_filter_words]

        kw1 = prompt_words[0] if len(prompt_words) > 0 else "stars"
        kw2 = prompt_words[1] if len(prompt_words) > 1 else "dreams"
        # kw3 removed as new persona templates only use two keywords.

        # Select template from the agent's persona-specific set
        template_key = self.generation_counter % len(self.templates)
        chosen_template_format_string = self.templates[template_key]

        # Format the chosen template string
        generated_poem = chosen_template_format_string.format(
            prompt=input_prompt,
            kw1=kw1,
            kw2=kw2
            # self.agent_name is part of the template literal, not a format placeholder
        )

        self.generation_counter += 1
        self.last_prompt_generated_by_me = input_prompt # Store the prompt this agent used
        return generated_poem

    def interpret_poetry(self, poetry: str) -> str:
        """
        Interprets received poetry to extract themes and generate a new creative prompt.
        Aims to avoid re-using the prompt this agent last generated with.
        """
        lines = poetry.split('\n')
        # Focus on words from the second half of the poem for theme extraction
        # or all lines if poem is short
        start_index_for_theme_lines = len(lines) // 2 if len(lines) > 1 else 0
        target_lines_text = " ".join(lines[start_index_for_theme_lines:])

        # Common words set for filtering - should be consistent or expanded from generate_poetry
        common_words_set = {
            "the", "a", "an", "is", "of", "and", "to", "in", "it", "that", "this", "i", "you", "he", "she", "was",
            "for", "on", "are", "with", "as", "my", "thus", "hark", "verse", "inspired", "tale", "unfold", "meter",
            "words", "placed", "lines", "interlaced", "language", "fresh", "avoiding", "cliche", "concrete", "scenes",
            "see", "metaphors", "bloom", "meanings", "deep", "true", "speaks", "poet", "upon", "theme", "thoughts",
            "flight", "bright", "night", "might", "where", "weaves", "patterns", "dark", "light", "say", "challenge",
            "embrace", "let", "dance", "space", "no", "simple", "rhyme", "grace", "unfolds", "pace", "thoughtful",
            "trace", "core", "explore", "whispers", "secrets", "calls", "more", "through", "veils", "view", "offered",
            "before", "opening", "new", "door", "consider", "notion", "vast", "wide", "compass", "guide", "long",
            "river", "fancies", "gently", "glide", "crafted", "naught", "hide"
        }

        # Sanitize and split for keywords
        cleaned_target_text = ''.join(char.lower() if char.isalnum() or char == "'" or char.isspace() else ' ' for char in target_lines_text)
        potential_keywords = [word for word in cleaned_target_text.split() if len(word) > 3 and word not in common_words_set]

        theme_kw1 = potential_keywords[0] if len(potential_keywords) > 0 else "mystery"
        theme_kw2 = potential_keywords[1] if len(potential_keywords) > 1 else "echoes"

        # Define interpretation prompt templates
        # These are f-strings that will be evaluated *after* theme_kw1 and theme_kw2 are set.
        interpretation_prompt_templates = [
            lambda kw1, kw2: f"Delve into the connection between {kw1} and {kw2}.",
            lambda kw1, kw2: f"Imagine {kw1} as a secret held by {kw2}—what unfolds?",
            lambda kw1, kw2: f"A reflective dialogue: {kw1} converses with {kw2}.",
            lambda kw1, kw2: f"Explore the hidden meaning of {kw1}'s journey towards {kw2}."
        ]

        # Deterministic selection of template
        # Using a different logic than generate_poetry to ensure variety if called sequentially with similar inputs
        template_idx = (len(theme_kw1) + len(theme_kw2) + len(potential_keywords)) % len(interpretation_prompt_templates)
        new_creative_prompt = interpretation_prompt_templates[template_idx](theme_kw1, theme_kw2)

        # Simple check to avoid this agent re-using the exact same prompt it last generated a poem with
        if self.last_prompt_generated_by_me and new_creative_prompt == self.last_prompt_generated_by_me:
            # If it's the same, try the next template in a cycle, or add a suffix
            template_idx = (template_idx + 1) % len(interpretation_prompt_templates)
            new_creative_prompt = interpretation_prompt_templates[template_idx](theme_kw1, theme_kw2)
            if new_creative_prompt == self.last_prompt_generated_by_me: # Still same after trying next?
                 new_creative_prompt = f"{new_creative_prompt}, from a new perspective."

        print(f"[{self.agent_name}] Interpreted keywords: '{theme_kw1}', '{theme_kw2}'. New creative prompt: '{new_creative_prompt}'")
        return new_creative_prompt

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
    prompt1 = "the song of a lonely robot in space"
    print(f"\nInput Prompt 1: '{prompt1}'")
    poem1 = agent_tester.generate_poetry(prompt1, style_to_use)
    print(f"[{agent_tester.agent_name} generated Poem 1 (template {(agent_tester.generation_counter-1) % 4 + 1})]:\n{poem1}")
    print(f"BardTest's last_prompt_generated_by_me is now: '{agent_tester.last_prompt_generated_by_me}'")


    # BardTest interprets another poem (e.g., from another agent)
    incoming_poem = "The stars are cold and distant fires,\nA cosmic ocean of desires.\nEchoes of creation's birth."
    print(f"\n{agent_tester.agent_name} interpreting incoming poem:\n{incoming_poem}")
    derived_prompt_for_next_poem = agent_tester.interpret_poetry(incoming_poem)
    # The interpret_poetry method prints the new prompt.

    # BardTest generates its second poem using the derived prompt
    print(f"\n{agent_tester.agent_name} generating Poem 2 using derived prompt: '{derived_prompt_for_next_poem}'")
    poem2 = agent_tester.generate_poetry(derived_prompt_for_next_poem, style_to_use)
    print(f"[{agent_tester.agent_name} generated Poem 2 (template {(agent_tester.generation_counter-1) % 4 + 1})]:\n{poem2}")
    print(f"BardTest's last_prompt_generated_by_me is now: '{agent_tester.last_prompt_generated_by_me}'")

    # Simulate interpreting another poem, potentially leading to a prompt similar to the one BardTest just used
    incoming_poem_2 = "A journey to distant stars, a quest for the unknown desires of space."
    print(f"\n{agent_tester.agent_name} interpreting incoming poem 2:\n{incoming_poem_2}")
    derived_prompt_for_next_poem_2 = agent_tester.interpret_poetry(incoming_poem_2)

    # BardTest generates its third poem
    print(f"\n{agent_tester.agent_name} generating Poem 3 using derived prompt: '{derived_prompt_for_next_poem_2}'")
    poem3 = agent_tester.generate_poetry(derived_prompt_for_next_poem_2, style_to_use)
    print(f"[{agent_tester.agent_name} generated Poem 3 (template {(agent_tester.generation_counter-1) % 4 + 1})]:\n{poem3}")
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
