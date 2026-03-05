#!/usr/bin/env python3
"""
PostToolUse Hook Template - Result Processing Script

This script processes tool results after successful execution.
Use for logging, validation, running follow-up actions, or injecting context.

USAGE IN FRONTMATTER:
---
hooks:
  PostToolUse:
    - matcher: "Write"  # MODIFY: Change matcher pattern
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/posttooluse-processor.py"
          async: true  # MODIFY: Set to true for non-blocking (e.g., tests)
---

EXIT CODES:
  0 - Success (JSON output processed)
  2 - Show error to Claude (cannot block - tool already executed)
  Other - Non-blocking error (stderr in verbose mode)

NOTE: PostToolUse cannot block actions (tool already ran).
Use for logging, validation feedback, or triggering follow-up work.
"""

import sys
import json
import os
import subprocess
from pathlib import Path
from typing import Any

# MODIFY: Configure what to process
TRACK_FILE_CHANGES = True
RUN_TESTS_ON_CHANGE = False  # Set True and use async: true
LOG_TO_FILE = False
LOG_FILE_PATH = "/tmp/claude-tool-log.jsonl"


def read_hook_input() -> dict:
    """Read JSON input from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Failed to parse hook input: {e}", file=sys.stderr)
        sys.exit(1)


def log_tool_use(hook_input: dict) -> None:
    """Log tool usage to file."""
    if not LOG_TO_FILE:
        return

    log_entry = {
        "timestamp": __import__("datetime").datetime.now().isoformat(),
        "session_id": hook_input.get("session_id"),
        "tool_name": hook_input.get("tool_name"),
        "tool_input": hook_input.get("tool_input"),
        "cwd": hook_input.get("cwd"),
    }

    with open(LOG_FILE_PATH, "a") as f:
        f.write(json.dumps(log_entry) + "\n")


def process_write_result(tool_input: dict, tool_response: Any) -> dict | None:
    """
    Process Write tool result.

    MODIFY: Add your post-write validation logic here.

    Returns:
        dict with additionalContext if needed, None otherwise
    """
    file_path = tool_input.get("file_path", "")

    # MODIFY: Add file-specific processing
    if file_path.endswith(".py"):
        # Example: Check Python syntax
        try:
            import ast
            with open(file_path, "r") as f:
                ast.parse(f.read())
        except SyntaxError as e:
            return {
                "additionalContext": f"Warning: Python syntax error in {file_path}: {e}"
            }

    if file_path.endswith(".json"):
        # Example: Validate JSON
        try:
            with open(file_path, "r") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            return {
                "additionalContext": f"Warning: Invalid JSON in {file_path}: {e}"
            }

    return None


def process_edit_result(tool_input: dict, tool_response: Any) -> dict | None:
    """
    Process Edit tool result.

    MODIFY: Add your post-edit validation logic here.
    """
    file_path = tool_input.get("file_path", "")

    # MODIFY: Add validation after edit
    return None


def process_bash_result(tool_input: dict, tool_response: Any) -> dict | None:
    """
    Process Bash tool result.

    MODIFY: Add your post-command processing here.
    """
    command = tool_input.get("command", "")

    # MODIFY: Check for specific command patterns and add context
    if "git commit" in command:
        return {
            "additionalContext": "Commit created. Consider running tests before pushing."
        }

    return None


def run_tests_if_needed(file_path: str) -> dict | None:
    """
    Run tests if a source file was changed.

    MODIFY: Configure your test command and patterns.
    """
    if not RUN_TESTS_ON_CHANGE:
        return None

    # MODIFY: Patterns that trigger tests
    test_triggers = [".py", ".ts", ".js", ".tsx", ".jsx"]

    if not any(file_path.endswith(ext) for ext in test_triggers):
        return None

    # MODIFY: Your test command
    test_command = "npm test"  # or "pytest", "cargo test", etc.

    try:
        result = subprocess.run(
            test_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=os.environ.get("CLAUDE_PROJECT_DIR", ".")
        )

        if result.returncode == 0:
            return {
                "additionalContext": f"Tests passed after editing {file_path}"
            }
        else:
            return {
                "additionalContext": f"Tests FAILED after editing {file_path}:\n{result.stdout}\n{result.stderr}"
            }
    except subprocess.TimeoutExpired:
        return {
            "additionalContext": f"Test timeout after editing {file_path}"
        }
    except Exception as e:
        return {
            "additionalContext": f"Could not run tests: {e}"
        }


def output_response(additional_context: str | None = None,
                    decision: str | None = None,
                    reason: str | None = None,
                    system_message: str | None = None) -> None:
    """Output the hook response as JSON."""
    output = {}

    if additional_context:
        output["hookSpecificOutput"] = {
            "hookEventName": "PostToolUse",
            "additionalContext": additional_context
        }

    # NOTE: decision/reason for PostToolUse is informational only (cannot block)
    if decision:
        output["decision"] = decision
        if reason:
            output["reason"] = reason

    if system_message:
        output["systemMessage"] = system_message

    if output:
        print(json.dumps(output))


def main():
    # Read hook input
    hook_input = read_hook_input()

    # Extract fields
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})
    tool_response = hook_input.get("tool_response")
    session_id = hook_input.get("session_id", "")
    cwd = hook_input.get("cwd", "")

    # Log if enabled
    log_tool_use(hook_input)

    # Process based on tool type
    result = None

    if tool_name == "Write":
        result = process_write_result(tool_input, tool_response)

        # Run tests if configured
        file_path = tool_input.get("file_path", "")
        test_result = run_tests_if_needed(file_path)
        if test_result and result:
            result["additionalContext"] += "\n" + test_result["additionalContext"]
        elif test_result:
            result = test_result

    elif tool_name == "Edit":
        result = process_edit_result(tool_input, tool_response)

        # Run tests if configured
        file_path = tool_input.get("file_path", "")
        test_result = run_tests_if_needed(file_path)
        if test_result and result:
            result["additionalContext"] += "\n" + test_result["additionalContext"]
        elif test_result:
            result = test_result

    elif tool_name == "Bash":
        result = process_bash_result(tool_input, tool_response)

    # Output response
    if result:
        output_response(additional_context=result.get("additionalContext"))
    else:
        # No output needed - tool use logged but no context to add
        pass


if __name__ == "__main__":
    main()
