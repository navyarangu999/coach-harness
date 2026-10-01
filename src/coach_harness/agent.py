"""The agent loop: give it a task, and it uses tools until the task is done."""
import json
import sys

import anthropic
from dotenv import load_dotenv

from . import tools

load_dotenv()
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from .env

MODEL = "claude-sonnet-5"
MAX_STEPS = 15

SYSTEM = (
    "You are a coding agent working in the current directory. "
    "Inspect files before editing them, run commands to verify your work, "
    "and stop once the task is done."
)

# Describe each tool so the model knows what it can call and what to pass.
TOOL_SCHEMAS = [
    {
        "name": "read_file",
        "description": "Read a UTF-8 text file and return its contents.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
    {
        "name": "write_file",
        "description": "Create or overwrite a file with the given content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["path", "content"],
        },
    },
    {
        "name": "edit_file",
        "description": (
            "Replace one exact, unique occurrence of old_text with new_text "
            "in a file. Preferred over write_file for changing existing files."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old_text": {"type": "string"},
                "new_text": {"type": "string"},
            },
            "required": ["path", "old_text", "new_text"],
        },
    },
    {
        "name": "run_shell",
        "description": "Run a shell command and return its output.",
        "input_schema": {
            "type": "object",
            "properties": {"command": {"type": "string"}},
            "required": ["command"],
        },
    },
]

# Map tool names to the actual Python functions.
TOOL_FUNCTIONS = {
    "read_file": tools.read_file,
    "write_file": tools.write_file,
    "edit_file": tools.edit_file,
    "run_shell": tools.run_shell,
}


def run_agent(task: str) -> None:
    messages = [{"role": "user", "content": task}]

    for step in range(1, MAX_STEPS + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM,
            tools=TOOL_SCHEMAS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        # If the model didn't ask for a tool, it's finished: print and stop.
        if response.stop_reason != "tool_use":
            for block in response.content:
                if block.type == "text":
                    print("\n" + block.text)
            return

        # Otherwise, run each tool it asked for and feed the results back.
        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            print(f"[step {step}] {block.name} {json.dumps(block.input)}")

            func = TOOL_FUNCTIONS[block.name]
            try:
                output = func(**block.input)
            except Exception as e:
                output = f"ERROR: {e}"

            results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": output[:8000],  # crude truncation for now
            })
        messages.append({"role": "user", "content": results})

    print("Stopped: hit the step limit.")


if __name__ == "__main__":
    run_agent(" ".join(sys.argv[1:]))