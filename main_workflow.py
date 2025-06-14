import time # To add slight delays for readability if needed, and for unique filenames if agents run too fast.
import subprocess
import sys
import random

# --- ReportLab Imports with Installation Attempt ---
REPORTLAB_AVAILABLE = False
try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    print("ReportLab not found. Attempting to install...")
    try:
        # Using sys.executable to ensure using the correct pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
        print("ReportLab installation attempted. Re-importing...")
        # Attempt to import again after installation
        # Forcing a re-check or re-import can be tricky.
        # Python's import system caches, and sys.path might not be updated immediately
        # for the current running process. This re-import might still fail here.
        import site # Try to refresh sys.path
        from importlib import reload
        reload(site)
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        REPORTLAB_AVAILABLE = True
        print("ReportLab imported successfully after installation attempt.")
    except Exception as e:
        print(f"Could not install or import ReportLab after attempt: {e}. PDF generation will be skipped.")
        # Define dummy classes if import still fails, so the rest of the script can be parsed
        class SimpleDocTemplate:
            def __init__(self, filename): self.filename = filename
            def build(self, story): print(f"Dummy PDF Build for {self.filename} with story: {len(story)} elements")
        class Paragraph:
            def __init__(self, text, style): self.text = text; self.style = style
        class Spacer:
            def __init__(self, width, height): self.width = width; self.height = height
        def getSampleStyleSheet(): return {'h1': type('Style', (), {'alignment':0, 'fontSize':18, 'spaceAfter':1}), 'h3': type('Style', (), {'fontSize':12, 'spaceBefore':1, 'spaceAfter':1}), 'Normal': type('Style', (), {'fontSize':10, 'leftIndent':0, 'spaceAfter':1, 'leading':12})}
        inch = 72.0 # default value
        TA_CENTER, TA_LEFT = 0, 2 # dummy alignment values
        print("Defined dummy ReportLab components to allow script to proceed without PDF functionality.")

from poet_agents.poetry_agent import PoetryAgent
from poet_agents.style_guide import frederick_turner_style

def print_formatted_poem(agent_name: str, poem_text: str, title: str = "Generated Poem"):
    """Helper function to print poems with a standard format."""
    print(f"\n--- {agent_name}'s {title} ---")
    # print(f"{agent_name.upper()}:") # Alternative simpler header
    for line in poem_text.split('\n'):
        print(f"  {line}")
    print("-----------------------------------")

ALPHA_INITIAL_PROMPTS_LIST = [
    "themes of cosmic wonder and stellar destiny",
    "the silent wisdom of ancient mountains and hidden valleys",
    "a quest for the ephemeral city of echoes and lost dreams",
    "the rhythmic dance of ocean tides under a cryptic moon",
    "secrets whispered by the winds on a desolate plain"
]

def create_conversation_pdf(title_prompt: str, conversation_data: list, filename: str):
    if not REPORTLAB_AVAILABLE:
        print("ReportLab is not available or failed to import. Skipping PDF generation.")
        return

    print(f"\nGenerating PDF: {filename}...")
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    # Title Style
    title_style = styles['h1']
    title_style.alignment = TA_CENTER
    title_style.fontSize = 18
    title_style.spaceAfter = 0.5 * inch

    # Agent Name Style
    agent_name_style = styles['h3']
    agent_name_style.fontSize = 12
    agent_name_style.spaceBefore = 0.2 * inch
    agent_name_style.spaceAfter = 0.1 * inch

    # Poem Style
    poem_style = styles['Normal']
    poem_style.fontSize = 10
    poem_style.leftIndent = 0.2 * inch # Indent poem lines
    poem_style.spaceAfter = 0.1 * inch
    poem_style.leading = 12 # Line spacing for poems

    # Add Title
    story.append(Paragraph(title_prompt.title(), title_style)) # .title() for title case

    # Add Conversation
    for entry in conversation_data:
        agent_name = entry['agent'].upper()
        poem_text = entry['poem'].replace('\n', '<br/>\n') # Preserve line breaks in PDF

        story.append(Paragraph(f"{agent_name}:", agent_name_style))
        story.append(Paragraph(poem_text, poem_style))
        story.append(Spacer(1, 0.1 * inch)) # Small spacer after each poem block

    try:
        doc.build(story)
        print(f"PDF '{filename}' generated successfully.")
    except Exception as e:
        print(f"Error generating PDF: {e}")

def run_workflow():
    print("Initializing Agents...")
    agent_alpha = PoetryAgent(agent_name="alpha")
    agent_beta = PoetryAgent(agent_name="beta")
    conversation_log = []
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
    alpha_initial_prompt_text = random.choice(ALPHA_INITIAL_PROMPTS_LIST) # Select random initial prompt
    # alpha_initial_prompt_text = "themes of cosmic wonder and stellar destiny" # Ensure this is commented out or deleted
    print(f"Alpha's initial prompt for first poem: '{alpha_initial_prompt_text}'")

    # Alpha's first poem has no prior reference.
    alpha_poem_1 = agent_alpha.generate_poetry(
        prompt_data={'prompt': alpha_initial_prompt_text, 'reference': None},
        style_guide=frederick_turner_style
    )
    conversation_log.append({'agent': agent_alpha.agent_name, 'poem': alpha_poem_1})
    print_formatted_poem(agent_alpha.agent_name, alpha_poem_1, "First Poem (to Beta)")

    print(f"\nAlpha ({agent_alpha.agent_name}) sending its first poem to Beta ({agent_beta.agent_name})...")
    agent_alpha.send_message(recipient_id=agent_beta.agent_name, message_type="initial_poem", payload=alpha_poem_1)

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
            # The method itself prints the derived theme, reference, and the new prompt.
            interpretation_data_for_beta = agent_beta.interpret_poetry(beta_received_message['payload'])
            # Example of what interpret_poetry prints: "[beta] Interpreted keywords: 'kw1', 'kw2'. Ref: 'ref phrase'. New prompt: 'new creative prompt'"

            print(f"\nBeta ({agent_beta.agent_name}) generating its first response poem based on interpretation (Prompt: '{interpretation_data_for_beta['prompt']}', Ref: '{interpretation_data_for_beta['reference']}')...")
            beta_response_poem_1 = agent_beta.generate_poetry(
                prompt_data=interpretation_data_for_beta, # Pass the whole dictionary
                style_guide=frederick_turner_style
            )
            conversation_log.append({'agent': agent_beta.agent_name, 'poem': beta_response_poem_1})
            print_formatted_poem(agent_beta.agent_name, beta_response_poem_1, "First Response Poem (to Alpha)")

            print(f"\nBeta ({agent_beta.agent_name}) sending its first response poem to Alpha ({agent_alpha.agent_name})...")
            agent_beta.send_message(recipient_id=agent_alpha.agent_name, message_type="response_poem", payload=beta_response_poem_1)
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
            # The method itself prints the derived theme, reference, and the new prompt.
            interpretation_data_for_alpha = agent_alpha.interpret_poetry(alpha_received_message['payload'])

            print(f"\nAlpha ({agent_alpha.agent_name}) generating its second poem based on interpretation (Prompt: '{interpretation_data_for_alpha['prompt']}', Ref: '{interpretation_data_for_alpha['reference']}')...")
            alpha_poem_2 = agent_alpha.generate_poetry(
                prompt_data=interpretation_data_for_alpha, # Pass the whole dictionary
                style_guide=frederick_turner_style
            )
            conversation_log.append({'agent': agent_alpha.agent_name, 'poem': alpha_poem_2})
            print_formatted_poem(agent_alpha.agent_name, alpha_poem_2, "Second Poem (to Beta)")

            print(f"\nAlpha ({agent_alpha.agent_name}) sending its second poem to Beta ({agent_beta.agent_name})...")
            agent_alpha.send_message(recipient_id=agent_beta.agent_name, message_type="second_poem", payload=alpha_poem_2)

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
                    interpretation_data_for_beta_2 = agent_beta.interpret_poetry(beta_received_second_message['payload'])

                    print(f"\nBeta ({agent_beta.agent_name}) generating its second poem based on interpretation (Prompt: '{interpretation_data_for_beta_2['prompt']}', Ref: '{interpretation_data_for_beta_2['reference']}')...")
                    beta_poem_2 = agent_beta.generate_poetry(
                        prompt_data=interpretation_data_for_beta_2, # Pass the whole dictionary
                        style_guide=frederick_turner_style
                    )
                    conversation_log.append({'agent': agent_beta.agent_name, 'poem': beta_poem_2})
                    print_formatted_poem(agent_beta.agent_name, beta_poem_2, "Second Response Poem (Final)")
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

    # Generate the PDF with the conversation
    # Note: 'alpha_initial_prompt' was renamed to 'alpha_initial_prompt_text' for clarity,
    # as it's just the text string used for the PDF title and Alpha's first actual prompt.
    if conversation_log and 'alpha_initial_prompt_text' in locals() and alpha_initial_prompt_text:
        output_pdf_filename = "poetic_exchange.pdf"
        create_conversation_pdf(
            title_prompt=alpha_initial_prompt_text,
            conversation_data=conversation_log,
            filename=output_pdf_filename
        )
    else:
        print("\nSkipping PDF generation as conversation data or initial prompt was missing.")

    print("\nEnd of poetic exchange simulation.")

if __name__ == "__main__":
    run_workflow()
