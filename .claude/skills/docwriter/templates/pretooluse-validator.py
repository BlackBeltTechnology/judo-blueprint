#!/usr/bin/env python3
"""
PreToolUse Hook Template - Permission Decision Script

This script validates tool calls before execution and returns allow/deny/ask decisions.

USAGE IN FRONTMATTER:
---
hooks:
  PreToolUse:
    - matcher: "Bash"  # MODIFY: Change matcher pattern
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/pretooluse-validator.py"
---

EXIT CODES:
  0 - Success (JSON output processed)
  2 - Blocking error (stderr shown to Claude, action blocked)
  Other - Non-blocking error (stderr in verbose mode)
"""

import sys
import json
import os
import re

# MODIFY: Add your validation patterns here
BLOCKED_PATTERNS = [
    r'rm\s+-rf\s+/',           # Block recursive delete from root
    r'rm\s+-rf\s+\*',          # Block wildcard recursive delete
    r'chmod\s+777',            # Block overly permissive chmod
    r'curl.*\|\s*bash',        # Block pipe to bash
    r'wget.*\|\s*bash',        # Block pipe to bash
]

ALLOWED_PATTERNS = [
    r'^npm\s+(test|run|install)',  # Allow npm commands
    r'^git\s+(status|diff|log)',   # Allow read-only git
    r'^ls\s',                       # Allow ls
    r'^cat\s',                      # Allow cat
]

# MODIFY: Add directories that should never be modified
PROTECTED_PATHS = [
    '/etc/',
    '/usr/',
    '/var/',
    os.path.expanduser('~/.ssh/'),
    os.path.expanduser('~/.aws/'),
]


def read_hook_input() -> dict:
    """Read JSON input from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Failed to parse hook input: {e}", file=sys.stderr)
        sys.exit(1)


def validate_bash_command(command: str) -> tuple[str, str | None]:
    """
    Validate a Bash command.

    Returns:
        tuple: (decision, reason)
        - decision: "allow", "deny", or "ask"
        - reason: explanation string or None
    """
    # MODIFY: Add your validation logic here

    # Check blocked patterns
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return "deny", f"Command matches blocked pattern: {pattern}"

    # Check protected paths
    for path in PROTECTED_PATHS:
        if path in command:
            return "ask", f"Command may affect protected path: {path}"

    # Check allowed patterns (auto-approve)
    for pattern in ALLOWED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return "allow", None

    # Default: ask for permission
    return "ask", None


def validate_write_operation(file_path: str, content: str) -> tuple[str, str | None]:
    """
    Validate a Write operation.

    Returns:
        tuple: (decision, reason)
    """
    # MODIFY: Add your file write validation logic here

    # Check protected paths
    for path in PROTECTED_PATHS:
        if file_path.startswith(path):
            return "deny", f"Cannot write to protected path: {path}"

    # Check for sensitive file patterns
    sensitive_patterns = ['.env', 'credentials', 'secrets', '.pem', '.key']
    for pattern in sensitive_patterns:
        if pattern in file_path.lower():
            return "ask", f"Writing to potentially sensitive file: {file_path}"

    return "allow", None


def validate_edit_operation(file_path: str, old_string: str, new_string: str) -> tuple[str, str | None]:
    """
    Validate an Edit operation.

    Returns:
        tuple: (decision, reason)
    """
    # MODIFY: Add your edit validation logic here

    # Check protected paths
    for path in PROTECTED_PATHS:
        if file_path.startswith(path):
            return "deny", f"Cannot edit protected path: {path}"

    return "allow", None


def output_decision(decision: str, reason: str | None = None,
                   updated_input: dict | None = None,
                   additional_context: str | None = None) -> None:
    """Output the hook decision as JSON."""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
        }
    }

    if reason:
        output["hookSpecificOutput"]["permissionDecisionReason"] = reason

    if updated_input:
        # MODIFY: Use this to modify tool input before execution
        output["hookSpecificOutput"]["updatedInput"] = updated_input

    if additional_context:
        # MODIFY: Add context that Claude will see
        output["hookSpecificOutput"]["additionalContext"] = additional_context

    print(json.dumps(output))


def output_blocking_error(message: str) -> None:
    """Output a blocking error (exit code 2)."""
    print(message, file=sys.stderr)
    sys.exit(2)


def main():
    # Read hook input
    hook_input = read_hook_input()

    # Extract common fields
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})
    session_id = hook_input.get("session_id", "")
    cwd = hook_input.get("cwd", "")

    # MODIFY: Add logging if needed
    # print(f"PreToolUse: {tool_name} in {cwd}", file=sys.stderr)

    # Route to appropriate validator based on tool
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        decision, reason = validate_bash_command(command)
        output_decision(decision, reason)

    elif tool_name == "Write":
        file_path = tool_input.get("file_path", "")
        content = tool_input.get("content", "")
        decision, reason = validate_write_operation(file_path, content)
        output_decision(decision, reason)

    elif tool_name == "Edit":
        file_path = tool_input.get("file_path", "")
        old_string = tool_input.get("old_string", "")
        new_string = tool_input.get("new_string", "")
        decision, reason = validate_edit_operation(file_path, old_string, new_string)
        output_decision(decision, reason)

    else:
        # MODIFY: Handle other tools or allow by default
        output_decision("allow")


if __name__ == "__main__":
    main()
