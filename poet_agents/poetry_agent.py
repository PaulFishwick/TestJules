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
        This is currently a stub and will be expanded later.
        """
        lines = poetry.split('\n')
        num_lines = len(lines)

        # Attempt to extract a theme (very basic: first non-empty line's first word, or a default)
        theme = "an unknown essence"
        for line in lines:
            if line.strip():
                # Let's try to get a more meaningful word if possible, not just "A" or "Hark"
                words = line.strip().split()
                if len(words) > 2 and words[0].lower() in ["a", "an", "the", "hark", "o", "in", "with", "thus"]:
                    theme = words[1] if len(words) > 1 else words[0]
                elif words:
                    theme = words[0]
                break

        related_theme_map = {
            "sunrise": "the dawn of new beginnings",
            "moon": "the mysteries of the night",
            "love": "the depths of human connection",
            "war": "the resilience of the human spirit",
            "dream": "the landscapes of the mind"
        }
        related_theme = related_theme_map.get(theme.lower().rstrip(",.?!"), "its profound meanings")


        interpretation = (
            f"{self.agent_name} has received your poem of {num_lines} lines. "
            f"It seems to speak of '{theme}'. "
            f"I shall now ponder on {related_theme}."
        )
        return interpretation

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
    prompt = "the silent wisdom of ancient stones"
    poem_content = agent_one.generate_poetry(prompt, frederick_turner_style)
    print("\nGenerated Poem:\n")
    print(poem_content)

    # Agent One sends the poem to Agent Two
    print(f"\n--- {agent_one.agent_name} sending poem to {agent_two.agent_name} ---")
    agent_one.send_message(recipient_id=agent_two.agent_name, message_type="poetry_submission", payload=poem_content)

    # Agent Two attempts to receive the message
    print(f"\n--- {agent_two.agent_name} attempting to receive message ---")
    received_message_by_two = agent_two.receive_message()

    if received_message_by_two:
        print(f"\n--- {agent_two.agent_name} processes the received poem ---")
        if received_message_by_two["message_type"] == "poetry_submission":
            interpretation = agent_two.interpret_poetry(received_message_by_two["payload"])
            print(interpretation)

            # Agent Two sends back an interpretation
            print(f"\n--- {agent_two.agent_name} sending interpretation to {agent_one.agent_name} ---")
            agent_two.send_message(recipient_id=agent_one.agent_name, message_type="poetry_response", payload=interpretation)

            # Agent One attempts to receive the interpretation
            print(f"\n--- {agent_one.agent_name} attempting to receive interpretation ---")
            interpretation_message = agent_one.receive_message()
            if interpretation_message:
                print(f"\n--- {agent_one.agent_name} received interpretation: ---")
                print(f"From: {interpretation_message['sender_id']}")
                print(f"Type: {interpretation_message['message_type']}")
                print(f"Content: {interpretation_message['payload']}")
            else:
                print(f"{agent_one.agent_name} found no message.")
        else:
            print(f"{agent_two.agent_name} received an unexpected message type: {received_message_by_two['message_type']}")
    else:
        print(f"{agent_two.agent_name} found no message.")

    # Test case: Attempt to receive when no message is present for agent_one
    print(f"\n--- {agent_one.agent_name} attempting to receive message (expecting none) ---")
    no_message = agent_one.receive_message()
    if not no_message:
        print(f"{agent_one.agent_name} correctly found no new message.")
    else:
        print(f"{agent_one.agent_name} unexpectedly found a message: {no_message}")
