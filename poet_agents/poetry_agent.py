import json
import datetime
import os # For file operations like delete and check existence
from .style_guide import frederick_turner_style

class PoetryAgent:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name

    def generate_poetry(self, input_prompt: str, style_guide: dict) -> str:
        """
        Generates a poem based on the input prompt and style guide.
        This is currently a stub and will be expanded later.
        """
        poem_lines = []

        # Acknowledge the input prompt
        poem_lines.append(f"A verse inspired by: '{input_prompt}'.")

        # Incorporate genre preference
        genre = style_guide.get("genre_preference", "verse")
        if genre == "narrative_epic":
            poem_lines.append(f"Hark, a tale of {input_prompt} I shall unfold,")
        else:
            poem_lines.append(f"A {genre} I shall now compose,")

        # Incorporate metrical forms preference (basic)
        metrical_forms = style_guide.get("metrical_forms", {})
        if metrical_forms.get("preference") == "strict":
            poem_lines.append("With structured meter, words precisely placed,")
            common_meter = metrical_forms.get("common_meters", ["iambic_pentameter"])[0]
            poem_lines.append(f"In {common_meter}, my lines are interlaced.")
        else:
            poem_lines.append("In flowing lines, the story will take flight,")

        # Incorporate language rules (freshness)
        language_rules = style_guide.get("language_rules", {})
        if language_rules.get("freshness_of_language"):
            poem_lines.append("With language fresh, avoiding the cliche,")

        # Incorporate imagery focus (concrete words)
        imagery_focus = style_guide.get("imagery_focus", {})
        if imagery_focus.get("use_concrete_words"):
            poem_lines.append("Using words concrete, for scenes you can see.")

        # Incorporate figurative language (metaphor)
        figurative_language = style_guide.get("figurative_language", {})
        if figurative_language.get("metaphor_usage") == "frequent_for_deeper_meaning":
            poem_lines.append("Metaphors will bloom, for meanings deep and true.")

        poem_lines.append(f"Thus speaks {self.agent_name}, the poet for you.")

        return "\n".join(poem_lines)

    def interpret_poetry(self, poetry: str) -> str:
        """
        Provides a basic interpretation of the given poetry.
        This is currently a stub and will be expanded. Its goal is to return a new creative prompt.
        """
        # Sanitize poetry by removing punctuation and making it lowercase
        # Keep apostrophes for words like "dream's" but remove other punctuation
        cleaned_poetry = ''.join(char.lower() if char.isalnum() or char == "'" or char.isspace() else ' ' for char in poetry)
        words = cleaned_poetry.split()

        common_words = {
            "the", "a", "an", "is", "of", "and", "to", "in", "it", "that", "this", "i", "you", "he", "she", "was",
            "for", "on", "are", "with", "as", "my", "thus", "hark", "verse", "inspired", "tale", "unfold", "meter",
            "words", "placed", "lines", "interlaced", "language", "fresh", "avoiding", "cliche", "concrete", "scenes",
            "see", "metaphors", "bloom", "meanings", "deep", "true", "speaks", "poet"
        }

        # Filter out common words and words shorter than 4 characters
        significant_words = [word for word in words if word.isalpha() and word not in common_words and len(word) > 3]

        if not significant_words:
            # Fallback if no significant words are found
            extracted_theme = "silence"
            prompt_starters = [
                "a poem born from quiet contemplation",
                "the echo of unspoken thoughts",
                "whispers from a tranquil void",
                "meditations on the unseen"
            ]
            # Deterministic choice for fallback to ensure reproducibility
            new_prompt = prompt_starters[len(poetry) % len(prompt_starters)]
        else:
            # Deterministically pick the last significant word as the theme
            extracted_theme = significant_words[-1]

            # Formulate a new prompt based on this theme
            prompt_starters = [
                f"dreams inspired by {extracted_theme}",
                f"secrets of the {extracted_theme}",
                f"a new song about the journey of {extracted_theme}",
                f"the mystery of {extracted_theme}'s heart",
                f"exploring the shadows of {extracted_theme}",
                f"what if {extracted_theme} could speak?",
                f"the world within a {extracted_theme}"
            ]
            # Deterministic choice for the prompt starter (e.g., based on length of theme or number of significant words)
            new_prompt = prompt_starters[len(extracted_theme) % len(prompt_starters)]

        print(f"[{self.agent_name}] Interpreted theme: '{extracted_theme}'. New creative prompt: '{new_prompt}'")
        return new_prompt

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
    agent_one = PoetryAgent(agent_name=agent_one_name)
    agent_two = PoetryAgent(agent_name=agent_two_name)

    print(f"\n--- {agent_one.agent_name} generating a poem ---")
    initial_prompt = "the silent wisdom of ancient stones"
    poem_content = agent_one.generate_poetry(initial_prompt, frederick_turner_style)
    print("\nGenerated Poem by {}:\n{}".format(agent_one.agent_name, poem_content))

    # Demonstrate new interpret_poetry functionality (Agent One interprets its own poem for a new prompt)
    print(f"\n--- {agent_one.agent_name} interpreting its own poem to generate a new prompt ---")
    new_prompt_from_interpretation = agent_one.interpret_poetry(poem_content)
    print(f"[{agent_one.agent_name}] New prompt derived: '{new_prompt_from_interpretation}'")

    # Agent One generates another poem based on this new prompt
    print(f"\n--- {agent_one.agent_name} generating a second poem based on the derived prompt ---")
    second_poem_content = agent_one.generate_poetry(new_prompt_from_interpretation, frederick_turner_style)
    print("\nGenerated Second Poem by {}:\n{}".format(agent_one.agent_name, second_poem_content))


    # Simulate Sending and Receiving for a full cycle using the new interpret_poetry
    print(f"\n\n--- SIMULATING MESSAGE EXCHANGE WITH NEW INTERPRETATION LOGIC ---")
    # Agent One sends the *first* poem to Agent Two
    print(f"\n--- {agent_one.agent_name} sending original poem to {agent_two.agent_name} ---")
    agent_one.send_message(recipient_id=agent_two.agent_name, message_type="poetry_submission", payload=poem_content)

    # Agent Two attempts to receive the message
    print(f"\n--- {agent_two.agent_name} attempting to receive message ---")
    received_message_by_two = agent_two.receive_message()

    if received_message_by_two:
        print(f"\n--- {agent_two.agent_name} processes the received poem from {received_message_by_two.get('sender_id')} ---")
        if received_message_by_two["message_type"] == "poetry_submission":
            # Agent Two interprets the received poem to get a NEW PROMPT
            print(f"\n--- {agent_two.agent_name} interpreting poem to generate a response prompt ---")
            prompt_for_response_poem = agent_two.interpret_poetry(received_message_by_two["payload"])

            # Agent Two generates a response poem using this new prompt
            print(f"\n--- {agent_two.agent_name} generating response poem based on: '{prompt_for_response_poem}' ---")
            response_poem_content = agent_two.generate_poetry(prompt_for_response_poem, frederick_turner_style)
            print("\nGenerated Response Poem by {}:\n{}".format(agent_two.agent_name, response_poem_content))

            # Agent Two sends back the response poem
            print(f"\n--- {agent_two.agent_name} sending response poem to {agent_one.agent_name} ---")
            agent_two.send_message(recipient_id=agent_one.agent_name, message_type="poetry_response", payload=response_poem_content)

            # Agent One attempts to receive the response
            print(f"\n--- {agent_one.agent_name} attempting to receive response ---")
            response_message = agent_one.receive_message()
            if response_message:
                print(f"\n--- {agent_one.agent_name} received response from {response_message.get('sender_id')}: ---")
                print(f"Type: {response_message['message_type']}")
                # Agent One now interprets this response poem to get another new prompt
                print(f"\n--- {agent_one.agent_name} interpreting response poem for a new creative direction ---")
                final_prompt_idea = agent_one.interpret_poetry(response_message['payload'])
                print(f"[{agent_one.agent_name}] Final prompt idea from Beta's response: '{final_prompt_idea}'")
            else:
                print(f"{agent_one.agent_name} found no response message.")
        else:
            print(f"{agent_two.agent_name} received an unexpected message type: {received_message_by_two['message_type']}")
    else:
        print(f"{agent_two.agent_name} found no message from {agent_one_name}.")

    # Test case: Attempt to receive when no message is present for agent_one
    print(f"\n--- {agent_one.agent_name} attempting to receive message (expecting none) ---")
    no_message = agent_one.receive_message()
    if not no_message:
        print(f"{agent_one.agent_name} correctly found no new message.")
    else:
        print(f"{agent_one.agent_name} unexpectedly found a message: {no_message}")
