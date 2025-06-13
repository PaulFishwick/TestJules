# Agent-to-Agent (A2A) Message Structure Definition
#
# This file defines the structure for messages exchanged between poetry agents.
# The structure is designed to be simple and clear, facilitating simulated communication.
# In a real-world scenario, these messages would likely be serialized (e.g., to JSON)
# and transmitted over a network or messaging queue.

# Example A2A Message Structure (Simulated)
# This dictionary represents the structure of a message exchanged between agents.
# It would typically be serialized to JSON for actual A2A communication.

example_message = {
    "sender_id": "agent_alpha_poet_001",
    "recipient_id": "agent_beta_critic_002",
    "message_type": "poetry_submission",  # Examples: "poetry_submission", "poetry_interpretation_request", "poetry_response", "feedback_on_interpretation", "style_critique_request", "style_critique_response", "initial_prompt"
    "payload": "Hark, a verse I weave for thee,\nOf mountains grand and oceans free.\nWith iambic grace and words so bright,\nI share this poem, my soul's own light.",
    "timestamp": "2023-10-27T10:00:00Z"
}

# Field Descriptions:
#
# sender_id (str):
#   A unique identifier for the agent sending the message.
#   Example: "agent_alpha_poet_001", "frederick_turner_ai_v1"
#
# recipient_id (str):
#   A unique identifier for the agent intended to receive the message.
#   Example: "agent_beta_critic_002", "poetry_evaluator_module"
#
# message_type (str):
#   Indicates the nature or intent of the message. This helps the receiving
#   agent understand how to process the payload.
#   Possible values include, but are not limited to:
#     - "poetry_submission": When an agent sends a newly generated poem.
#     - "poetry_interpretation_request": When an agent requests an interpretation of a poem.
#     - "poetry_response": When an agent sends its interpretation or thoughts on a poem.
#     - "feedback_on_interpretation": For providing feedback on an interpretation received.
#     - "style_critique_request": Requesting a critique based on a specific style guide.
#     - "style_critique_response": The actual critique.
#     - "initial_prompt": To provide an initial creative spark or instruction.
#
# payload (str):
#   The main content of the message. The format of the payload is often
#   dependent on the `message_type`. For poetry-related messages, this will
#   typically be the poem text itself, or an interpretation string.
#   For other message types, it could be a prompt, feedback, or other relevant data.
#
# timestamp (str):
#   The time at which the message was created, represented in ISO 8601 format.
#   This helps in ordering messages, logging, and debugging.
#   Example: "2023-10-27T10:00:00Z"

# Note: For more complex scenarios, the payload could be a dictionary itself,
# containing multiple pieces of information. However, for this project,
# a string payload for poetry or interpretation text is sufficient for now.

if __name__ == '__main__':
    print("This file defines the A2A message structure.")
    print("Example Message:")
    import json
    print(json.dumps(example_message, indent=4))

    # Example of how a message might be constructed:
    import datetime
    new_message = {
        "sender_id": "agent_turner_ai",
        "recipient_id": "agent_critic_bot",
        "message_type": "poetry_submission",
        "payload": "The wind whispers secrets through the ancient trees,\nA timeless story on the gentle breeze.",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z" # Adding 'Z' for UTC
    }
    print("\nNewly Constructed Message Example:")
    print(json.dumps(new_message, indent=4))
