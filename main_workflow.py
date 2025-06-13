import time # To add slight delays for readability if needed, and for unique filenames if agents run too fast.
from poet_agents.poetry_agent import PoetryAgent
from poet_agents.style_guide import frederick_turner_style

def print_formatted_poem(agent_name: str, poem_text: str, title: str = "Generated Poem"):
    """Helper function to print poems with a standard format."""
    print(f"\n--- {agent_name}'s {title} ---")
    # print(f"{agent_name.upper()}:") # Alternative simpler header
    for line in poem_text.split('\n'):
        print(f"  {line}")
    print("-----------------------------------")

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
    print(f"\n--- Agent Alpha's First Turn ---")
    print(f"Alpha's initial prompt for first poem: '{initial_prompt}'")

    alpha_poem = agent_alpha.generate_poetry(initial_prompt, frederick_turner_style)
    print_formatted_poem(agent_alpha.agent_name, alpha_poem, "First Poem (to Beta)")

    print(f"\nAlpha ({agent_alpha.agent_name}) sending its first poem to Beta ({agent_beta.agent_name})...")
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
            print(f"\nBeta ({agent_beta.agent_name}) interpreting Alpha's poem to derive a new prompt...")
            # interpret_poetry now directly returns a creative prompt.
            # The method itself prints the derived theme and the new prompt.
            creative_prompt_for_beta = agent_beta.interpret_poetry(beta_received_message['payload'])
            # The interpret_poetry method already prints: "[beta] Interpreted theme: '...'. New creative prompt: '...'"

            print(f"\nBeta ({agent_beta.agent_name}) generating its first response poem based on derived prompt: '{creative_prompt_for_beta}'...")
            beta_response_poem = agent_beta.generate_poetry(
                input_prompt=creative_prompt_for_beta, # Use the dynamic prompt from interpret_poetry
                style_guide=frederick_turner_style
            )
            print_formatted_poem(agent_beta.agent_name, beta_response_poem, "First Response Poem (to Alpha)")

            print(f"\nBeta ({agent_beta.agent_name}) sending its first response poem to Alpha ({agent_alpha.agent_name})...")
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
            print(f"\nAlpha ({agent_alpha.agent_name}) interpreting Beta's response poem to derive a new prompt...")
            # interpret_poetry now directly returns a creative prompt.
            # The method itself prints the derived theme and the new prompt.
            creative_prompt_for_alpha_next_turn = agent_alpha.interpret_poetry(alpha_received_message['payload'])

            print(f"\nAlpha ({agent_alpha.agent_name}) has derived a new prompt for its second poem: '{creative_prompt_for_alpha_next_turn}'")

            print(f"\nAlpha ({agent_alpha.agent_name}) generating its second poem based on prompt: '{creative_prompt_for_alpha_next_turn}'...")
            alpha_second_poem = agent_alpha.generate_poetry(
                input_prompt=creative_prompt_for_alpha_next_turn,
                style_guide=frederick_turner_style
            )
            print_formatted_poem(agent_alpha.agent_name, alpha_second_poem, "Second Poem (to Beta)")

            print(f"\nAlpha ({agent_alpha.agent_name}) sending its second poem to Beta ({agent_beta.agent_name})...")
            agent_alpha.send_message(recipient_id=agent_beta.agent_name, message_type="second_poem", payload=alpha_second_poem)

            # Adding a small delay
            time.sleep(0.1)

            # 4. Agent Beta's Second Response Turn
            print("\n--- Agent Beta's Second Response Turn ---")
            print(f"Beta ({agent_beta.agent_name}) attempting to receive Alpha's second poem...")
            beta_received_second_message = agent_beta.receive_message()

            if beta_received_second_message:
                print("\nBeta received Alpha's second poem:")
                print("------------------------------------")
                print(f"From: {beta_received_second_message['sender_id']}")
                print(f"Type: {beta_received_second_message['message_type']}")
                print("Payload (Second Poem from Alpha):")
                print(beta_received_second_message['payload'])
                print("------------------------------------")

                if beta_received_second_message['message_type'] == "second_poem":
                    print(f"\nBeta ({agent_beta.agent_name}) interpreting Alpha's second poem to derive a new prompt...")
                    creative_prompt_for_beta_second_turn = agent_beta.interpret_poetry(beta_received_second_message['payload'])

                    print(f"\nBeta ({agent_beta.agent_name}) generating its second poem based on prompt: '{creative_prompt_for_beta_second_turn}'...")
                    beta_second_poem = agent_beta.generate_poetry(
                        input_prompt=creative_prompt_for_beta_second_turn,
                        style_guide=frederick_turner_style
                    )
                    print_formatted_poem(agent_beta.agent_name, beta_second_poem, "Second Response Poem (Final)")
                    # Workflow ends with Beta's second poem generation for now.
                else:
                    print(f"Beta received unexpected message type: {beta_received_second_message['message_type']}")
            else:
                print(f"Beta ({agent_beta.agent_name}) received no second message from Alpha.")
        else:
            print(f"Alpha received unexpected message type: {alpha_received_message['message_type']}")
    else:
        print(f"Alpha ({agent_alpha.agent_name}) received no response message from Beta.")

    print("\n--- [END WORKFLOW] ---")

if __name__ == "__main__":
    run_workflow()
