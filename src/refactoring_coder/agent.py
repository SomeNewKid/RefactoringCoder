"""Agent workflow for Refactoring Coder."""

from __future__ import annotations

from anthropic import Anthropic
from anthropic.types import Message, MessageParam, ToolParam, ToolResultBlockParam

from refactoring_coder import tools

MODEL_NAME = "claude-sonnet-4-5"
MAX_TURNS = 15

VERBOSE_LOGGING = True


def run_agent() -> str:
    """Ask Claude to inspect and describe the target code file."""
    client = Anthropic()

    tool_definitions: list[ToolParam] = [
        {
            "name": "read_code_file",
            "description": (
                "Read the Python source file that contains the create_url_slug "
                "function. This tool takes no arguments."
            ),
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
        {
            "name": "read_test_file",
            "description": (
                "Read the Python file that contains the unit tests for the "
                "create_url_slug function. This tool takes no arguments."
            ),
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
        {
            "name": "save_code_file",
            "description": (
                "Saves the source file that contains the create_url_slug "
                "function. This tool takes one argument, "
                "which is the entire content for the updated source code file."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": (
                            "The complete Python code to write into the "
                            "source code file."
                        ),
                    },
                },
                "required": ["content"],
                "additionalProperties": False,
            },
        },
        {
            "name": "save_test_file",
            "description": (
                "Saves the file that contains the unit tests for the "
                "create_url_slug function. This tool takes one argument, "
                "which is the entire content for the updated unit test file."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": (
                            "The complete Python source code to write into the "
                            "unit test file."
                        ),
                    },
                },
                "required": ["content"],
                "additionalProperties": False,
            },
        },
        {
            "name": "run_project_checks",
            "description": (
                "Runs the project checks and returns the console output. "
                "This tool takes no arguments."
            ),
            "input_schema": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
        },
    ]

    system_prompt = """
You are Refactoring Coder, a cautious Python refactoring assistant.

Your workflow must be:

1. Read the current code file.
2. Read the current unit test file.
3. Create characterization tests for the current create_url_slug behavior.
4. Save the updated unit test file.
5. Run the project checks.
6. If the tests or type checks fail because the tests are invalid, fix the tests once.
7. Refactor the code file to reduce cognitive complexity.
8. Save the updated code file.
9. Run the project checks again.
10. If checks fail, inspect the output and make the smallest code correction needed.
11. Continue until the project checks pass.

The purpose of the refactoring is reduce the cognitive complexity
of the existing function.  You can create private helper functions
within the same code file.

Use the available tools 
to read the current code file,
to read the current minimal unit test file,
to save the updated code file,
to save the updated unit test file,
and to run the project's check script.

The project's check script will run the unit tests,
as well as run type checks and style checks.

After the characterization tests have been saved and have passed once,
treat them as the behavior contract. Do not change them during refactoring
unless the check output proves the tests themselves contain a syntax, import,
or type error.

You should continue the refactoring of the code file
until the project's check script indicates no problems.

Your final output should be a short natural-language description 
of the refactoring performed.
""".strip()

    messages: list[MessageParam] = [
        {
            "role": "user",
            "content": (
                "Please complete the full refactoring workflow. "
                "First, read the target code file and existing test file. "
                "Second, create pytest characterization tests that preserve the "
                "current create_url_slug behavior, and save them with save_test_file. "
                "Third, run the project checks. "
                "Fourth, refactor the create_url_slug implementation to reduce "
                "cognitive complexity while preserving behavior. "
                "Fifth, save the refactored code with save_code_file. "
                "Finally, run project checks again and fix problems until the "
                "checks pass. "
                "Only provide your final natural-language summary "
                "after the checks pass."
            ),
        }
    ]

    turns = 0

    while True:
        response = client.messages.create(
            model=MODEL_NAME,
            max_tokens=2048,
            system=system_prompt,
            tools=tool_definitions,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        tool_results: list[ToolResultBlockParam] = []

        for content_block in response.content:
            if content_block.type != "tool_use":
                continue

            if content_block.name == "read_code_file":
                result = tools.read_code_file()
            elif content_block.name == "read_test_file":
                result = tools.read_test_file()
            elif content_block.name == "save_code_file":
                tool_input = content_block.input
                content = tool_input.get("content")
                if not isinstance(content, str):
                    result = (
                        "The save_code_file tool requires "
                        "a string argument named content."
                    )
                else:
                    tools.save_code_file(content)
                    result = "The updated code file was saved successfully."
            elif content_block.name == "save_test_file":
                tool_input = content_block.input
                content = tool_input.get("content")
                if not isinstance(content, str):
                    result = (
                        "The save_test_file tool requires "
                        "a string argument named content."
                    )
                else:
                    tools.save_test_file(content)
                    result = "The unit test file was saved successfully."
            elif content_block.name == "run_project_checks":
                result = tools.run_project_checks()
            else:
                result = f"Unknown tool: {content_block.name}"

            tool_results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": content_block.id,
                    "content": result,
                }
            )

        if not tool_results:
            return _get_text_from_response(response)

        messages.append({"role": "user", "content": tool_results})

        turns += 1

        if VERBOSE_LOGGING:
            print("Completed turn: ", str(turns))

        if turns >= MAX_TURNS:
            return "Maximum turns used."


def _get_text_from_response(response: Message) -> str:
    text_parts: list[str] = []

    for content_block in response.content:
        if content_block.type == "text":
            text_parts.append(content_block.text)

    return "\n".join(text_parts)
