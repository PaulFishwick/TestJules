import time # To add slight delays for readability if needed, and for unique filenames if agents run too fast.
from poet_agents.poetry_agent import PoetryAgent
from poet_agents.style_guide import frederick_turner_style

def run_workflow():
    print("Initializing Agents...")
    agent_alpha = PoetryAgent(agent_name="alpha")
    agent_beta = PoetryAgent(agent_name="beta")
    print(f"Agent Alpha: {agent_alpha.agent_name}")
    print(f"Agent Beta: {agent_beta.agent_name}")

    # Clean up any previous message files to ensure a clean run
    # This is important because agent names are fixed in this script
    try:
        import os
        if os.path.exists(f"message_to_{agent_alpha.agent_name}.json"):
            os.remove(f"message_to_{agent_alpha.agent_name}.json")
            print(f"Cleaned up old message file for {agent_alpha.agent_name}")
        if os.path.exists(f"message_to_{agent_beta.agent_name}.json"):
            os.remove(f"message_to_{agent_beta.agent_name}.json")
            print(f"Cleaned up old message file for {agent_beta.agent_name}")
    except Exception as e:
        print(f"Error during cleanup: {e}")

    print("\n--- [BEGIN WORKFLOW] ---")

    # 1. Agent Alpha's First Turn
    print("\n--- Agent Alpha's First Turn ---")
    initial_prompt = "the dawn of creativity"
    print(f"Alpha's initial prompt: '{initial_prompt}'")

    alpha_poem = agent_alpha.generate_poetry(initial_prompt, frederick_turner_style)
    print("\nAlpha generated poetry:")
    print("-------------------------")
    print(alpha_poem)
    print("-------------------------")

    print(f"\nAlpha sending poem to Beta ({agent_beta.agent_name})...")
    agent_alpha.send_message(recipient_id=agent_beta.agent_name, message_type="initial_poem", payload=alpha_poem)

    # Adding a small delay to simulate message transfer and allow file system to catch up if necessary
    time.sleep(0.1)

    # 2. Agent Beta's Turn
    print("\n--- Agent Beta's Turn ---")
    print(f"Beta ({agent_beta.agent_name}) attempting to receive message...")
    beta_received_message = agent_beta.receive_message()

    if beta_received_message:
        print("\nBeta received a message:")
        print("--------------------------")
        print(f"From: {beta_received_message['sender_id']}")
        print(f"Type: {beta_received_message['message_type']}")
        print("Payload (Poem from Alpha):")
        print(beta_received_message['payload'])
        print("--------------------------")

        if beta_received_message['message_type'] == "initial_poem":
            print("\nBeta interpreting Alpha's poem...")
            beta_interpretation = agent_beta.interpret_poetry(beta_received_message['payload'])
            print("Beta's interpretation:")
            print("----------------------")
            print(beta_interpretation)
            print("----------------------")

            # Safely extract theme from beta_interpretation string
            # Format: "{agent_name} has received your poem of {num_lines} lines. It seems to speak of '{theme}'. I shall now ponder on {related_theme}."
            try:
                theme_part = beta_interpretation.split("It seems to speak of '")[1]
                extracted_theme = theme_part.split("'")[0]
            except IndexError:
                extracted_theme = "the received verse" # Fallback theme

            response_prompt = f"a poetic response to the theme of '{extracted_theme}'"
            print(f"\nBeta's prompt for response poem: '{response_prompt}'")

            beta_response_poem = agent_beta.generate_poetry(response_prompt, frederick_turner_style)
            print("\nBeta generated response poetry:")
            print("-------------------------------")
            print(beta_response_poem)
            print("-------------------------------")

            print(f"\nBeta sending response poem to Alpha ({agent_alpha.agent_name})...")
            agent_beta.send_message(recipient_id=agent_alpha.agent_name, message_type="response_poem", payload=beta_response_poem)
        else:
            print(f"Beta received unexpected message type: {beta_received_message['message_type']}")
    else:
        print("Beta received no message.")

    # Adding a small delay
    time.sleep(0.1)

    # 3. Agent Alpha's Second Turn
    print("\n--- Agent Alpha's Second Turn ---")
    print(f"Alpha ({agent_alpha.agent_name}) attempting to receive message...")
    alpha_received_message = agent_alpha.receive_message()

    if alpha_received_message:
        print("\nAlpha received a message:")
        print("---------------------------")
        print(f"From: {alpha_received_message['sender_id']}")
        print(f"Type: {alpha_received_message['message_type']}")
        print("Payload (Poem from Beta):")
        print(alpha_received_message['payload'])
        print("---------------------------")

        if alpha_received_message['message_type'] == "response_poem":
            print("\nAlpha interpreting Beta's response poem...")
            alpha_interpretation_of_response = agent_alpha.interpret_poetry(alpha_received_message['payload'])
            print("Alpha's interpretation of Beta's response:")
            print("------------------------------------------")
            print(alpha_interpretation_of_response)
            print("------------------------------------------")
        else:
            print(f"Alpha received unexpected message type: {alpha_received_message['message_type']}")
    else:
        print("Alpha received no message.")

    print("\n--- [END WORKFLOW] ---")

if __name__ == "__main__":
    run_workflow()
