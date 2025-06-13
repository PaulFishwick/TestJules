# A2A Poetic Agents Simulation

## Overview

This project simulates a system where two AI agents can communicate by exchanging poetry written in the style of the poet Frederick Turner. The communication itself is a simulation of Google's Agent-to-Agent (A2A) protocol, currently implemented using file-based message passing (JSON files).

The primary goal of this foundational codebase is to establish the core components, agent logic stubs, and interaction workflow. A key objective is for the agents to engage in creative interpretation of received poetry, allowing them to generate distinct and original responses rather than mere echoes, fostering a more dynamic and engaging poetic dialogue. This can be expanded upon in the future with real Large Language Model (LLM) integration for poetry generation and the official Google A2A SDK for communication.

## Agent Personas and Unique Poetic Voices

To enhance the distinctiveness of the interacting agents, this simulation now implements basic "Agent Personas":

-   **Agent Alpha ("The Orator"):** Alpha's poetic style is characterized by a more formal, structured, and declarative voice. Its expressions often aim for clarity and reasoned discourse.
-   **Agent Beta ("The Dreamer"):** Beta's style is more lyrical, questioning, and tends towards abstract imagery and whimsical reflections.

This distinction is primarily achieved within the `PoetryAgent`'s `generate_poetry` method. Each agent persona (specifically "alpha" and "beta" by name) is assigned a unique set of internal poem templates. These template sets for Alpha and Beta are designed to have no overlapping boilerplate phrases or sentence structures, ensuring that their generated poetry is stylistically unique and their "voices" remain clearly distinguishable throughout the conversation. Agents with other names will default to Alpha's templates.

A key feature enhancing the dialogue is the agents' ability to create direct conversational threads. When responding, an agent's `interpret_poetry` method extracts a salient short phrase from the received poem. This `reference_phrase` is then prominently woven into the responding agent's poem via its persona-specific templates in `generate_poetry` (passed as part of a data dictionary). This mechanism ensures that the agents explicitly acknowledge and build upon specific words of the previous speaker, resulting in a demonstrably more cohesive, engaging, and thematically linked exchange.

## Directory Structure

```
.
├── poet_agents/
│   ├── __init__.py
│   ├── message_structure.py
│   ├── poetry_agent.py
│   └── style_guide.py
├── main_workflow.py
└── README.md
```

- **`poet_agents/`**: This directory is a Python package containing all the core logic for the poetry agents.
- **`main_workflow.py`**: The main script to run the two-agent interaction simulation.
- **`README.md`**: This file.

## Key Files

### `poet_agents/__init__.py`
- An empty file that makes the `poet_agents` directory a Python package, allowing for modular imports.

### `poet_agents/style_guide.py`
- Defines a Python dictionary `frederick_turner_style`.
- This dictionary encapsulates the key characteristics of Frederick Turner's poetry (e.g., preference for narrative, metrical forms, specific language use, imagery).
- It serves as a "style guide" or rule set for the poetry generation logic in `PoetryAgent`.

### `poet_agents/poetry_agent.py`
- Contains the `PoetryAgent` class, which represents an individual AI agent.
- **Key Methods:**
    - `__init__(self, agent_name)`: Initializes the agent with a name, a counter for poem generation, and assigns persona-specific poem templates (for "alpha" or "beta") or default templates.
    - `generate_poetry(self, input_prompt, style_guide)`: (Stub enhanced for creativity & variety) Generates a piece of poetry based on an input prompt and the `style_guide`. It utilizes the agent's assigned persona-specific (or default) set of distinct poem templates and attempts to weave keywords from the prompt into the chosen structure. A counter mechanism ensures the same agent cycles through different templates on successive generations, further diversifying the poetic output. It also stores the prompt it just used.
    - `interpret_poetry(self, poetry)`: (Stub enhanced for deeper interpretation & varied prompting) Processes received poetry to extract key themes/words, focusing on the core content rather than just opening lines. It then uses diverse templates to formulate a new creative prompt string designed to guide the agent in generating an original and thematically relevant response. Includes a simple check to prevent the agent from re-using its own immediately preceding generation prompt.
    - `send_message(self, recipient_id, message_type, payload)`: Constructs a message (dictionary) and saves it as a JSON file (e.g., `message_to_beta.json`), simulating sending a message via A2A.
    - `receive_message(self)`: Checks for an incoming message file (e.g., `message_to_alpha.json`), reads it, and deletes it. Simulates receiving an A2A message.

### `poet_agents/message_structure.py`
- This file provides a commented example and description of the Python dictionary structure used for messages exchanged between agents.
- Messages include fields like `sender_id`, `recipient_id`, `message_type`, `payload` (the poetry), and `timestamp`.
- This structure would typically be serialized to JSON in a real A2A scenario.

### `main_workflow.py`
- This script orchestrates a simple interaction between two `PoetryAgent` instances (e.g., "alpha" and "beta").
- **Workflow:**
    1. Agent Alpha generates and "sends" an initial poem to Agent Beta.
    2. Agent Beta "receives" this poem, "interprets" it (deriving a new creative prompt), generates a response poem based on this new prompt, and "sends" it back to Alpha.
    3. Agent Alpha "receives" Beta's response, "interprets" it (deriving another new creative prompt), generates its second poem, and "sends" it to Beta.
    4. Agent Beta "receives" Alpha's second poem, "interprets" it, and generates its second response poem.
- The script simulates a **two-round poetic exchange**.
- It uses `print()` statements to show the progression of the interaction, including message details and derived prompts.
- It demonstrates how agents use dynamically generated creative prompts from `interpret_poetry` to craft their responses, fostering a more varied exchange.

## How to Run

1.  Ensure you have Python 3 installed.
2.  Navigate to the root directory of the project in your terminal.
3.  Run the simulation using the command:
    ```bash
    python main_workflow.py
    ```
4.  Observe the console output. It will show:
    - The full two-round poetic exchange (four poems in total).
    - Each poem clearly attributed to its generating agent (e.g., "--- alpha's First Poem (to Beta) ---") and with indented lines.
    - Notifications of messages being "sent" and "received" (as JSON files).
    - The derived creative prompts that guide each agent's response.
    - The creation and deletion of temporary JSON files (e.g., `message_to_alpha.json`, `message_to_beta.json`) in the root directory, which represent the messages.

## Output Artifacts

Upon successful completion, the `main_workflow.py` script generates a PDF file named `poetic_exchange.pdf` in the root directory of the project.

This PDF includes:
- A bold-faced title, taken from Agent Alpha's initial poetic prompt.
- The complete four-poem conversation between Agent Alpha and Agent Beta, with each agent's contribution clearly attributed.

This feature uses the [ReportLab](https://www.reportlab.com/opensource/) Python library for PDF generation. If ReportLab is not found in your Python environment, the script will attempt to install it automatically.

## Current Status & Future Work

- **Simulated Components:**
    - **Poetry Generation:** The current poetry generation is a basic stub. It does not involve any actual AI or LLM.
    - **A2A Communication:** The A2A protocol is simulated using local file system operations (reading/writing JSON files).
- **Potential Future Enhancements:**
    - Integrate a pre-trained Large Language Model (LLM) for sophisticated poetry generation in Frederick Turner's style. This would involve replacing the stub `generate_poetry` method with calls to an LLM API or library, guided by the `style_guide.py`.
    - Implement communication using the official Google A2A SDK, replacing the file-based `send_message` and `receive_message` methods.
    - Develop more complex agent interaction logic, such as multi-turn conversations or feedback mechanisms.
    - Add comprehensive unit tests.
