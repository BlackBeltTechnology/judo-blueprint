#!/usr/bin/env python3
"""
SubagentStop Hook Template - Cleanup and Continuation Script

This script runs when a subagent finishes. Use for cleanup, validation,
or deciding whether the subagent should continue working.

USAGE IN FRONTMATTER (Note: Stop in frontmatter becomes SubagentStop):
---
hooks:
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/subagent-stop-cleanup.py"
---

EXIT CODES:
  0 - Success (JSON output processed)
  2 - Blocking: Prevent subagent from stopping (continue working)
  Other - Non-blocking error

DECISION CONTROL:
  - Return decision: "block" to prevent stopping
  - Return decision: "allow" or exit 0 without decision to allow stopping
"""

import sys
import json
import os
from pathlib import Path
from typing import Any

# MODIFY: Configure cleanup and continuation logic
CHECK_TASK_COMPLETION = True
CLEANUP_TEMP_FILES = False
VALIDATE_OUTPUT = True


def read_hook_input() -> dict:
    """Read JSON input from stdin."""
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Failed to parse hook input: {e}", file=sys.stderr)
        sys.exit(1)


def check_tasks_complete(session_id: str) -> tuple[bool, str | None]:
    """
    Check if all tasks are complete.

    MODIFY: Add your task completion logic.
    Uses ~/.claude/tasks/{session}/*.json for task state.

    Returns:
        tuple: (all_complete, incomplete_task_description)
    """
    if not CHECK_TASK_COMPLETION:
        return True, None

    # MODIFY: Path discovery - use Explore agent to find exact paths
    # Path discovered via Explore: ~/.claude/tasks/{session}/
    tasks_dir = Path.home() / ".claude" / "tasks" / session_id

    if not tasks_dir.exists():
        return True, None  # No tasks tracked

    incomplete_tasks = []
    for task_file in tasks_dir.glob("*.json"):
        if task_file.name.startswith("."):
            continue
        try:
            with open(task_file) as f:
                task = json.load(f)
            if task.get("status") != "completed":
                incomplete_tasks.append(task.get("subject", task_file.name))
        except (json.JSONDecodeError, IOError):
            continue

    if incomplete_tasks:
        return False, f"Incomplete tasks: {', '.join(incomplete_tasks[:3])}"

    return True, None


def validate_subagent_output(agent_transcript_path: str) -> tuple[bool, str | None]:
    """
    Validate subagent output quality.

    MODIFY: Add your validation logic.

    Returns:
        tuple: (is_valid, issue_description)
    """
    if not VALIDATE_OUTPUT:
        return True, None

    if not agent_transcript_path or not Path(agent_transcript_path).exists():
        return True, None

    # MODIFY: Read and validate transcript
    try:
        with open(agent_transcript_path) as f:
            # Transcript is JSONL format
            lines = f.readlines()

        # MODIFY: Add your validation criteria
        # Example: Check if agent produced meaningful output
        if len(lines) < 3:
            return False, "Subagent produced minimal output - may need to continue"

        # Example: Check for error patterns in last messages
        for line in lines[-5:]:
            try:
                msg = json.loads(line)
                content = str(msg.get("content", ""))
                if "error" in content.lower() and "fixed" not in content.lower():
                    return False, "Subagent may have unresolved errors"
            except json.JSONDecodeError:
                continue

    except IOError as e:
        # Can't read transcript, allow stopping
        return True, None

    return True, None


def cleanup_temp_files(session_id: str, cwd: str) -> None:
    """
    Clean up temporary files created during subagent run.

    MODIFY: Add your cleanup patterns.
    """
    if not CLEANUP_TEMP_FILES:
        return

    # MODIFY: Patterns to clean up
    cleanup_patterns = [
        "*.tmp",
        ".cache/*",
        "__pycache__/*",
    ]

    project_dir = Path(cwd)
    for pattern in cleanup_patterns:
        for file_path in project_dir.glob(pattern):
            try:
                if file_path.is_file():
                    file_path.unlink()
                elif file_path.is_dir():
                    import shutil
                    shutil.rmtree(file_path)
            except OSError:
                pass  # Ignore cleanup errors


def output_decision(decision: str, reason: str | None = None) -> None:
    """Output the hook decision as JSON."""
    output = {
        "decision": decision,
    }
    if reason:
        output["reason"] = reason

    print(json.dumps(output))


def output_block_via_exit(message: str) -> None:
    """Block subagent from stopping using exit code 2."""
    print(message, file=sys.stderr)
    sys.exit(2)


def main():
    # Read hook input
    hook_input = read_hook_input()

    # Extract fields specific to SubagentStop
    agent_id = hook_input.get("agent_id", "")
    agent_type = hook_input.get("agent_type", "")
    agent_transcript_path = hook_input.get("agent_transcript_path", "")
    stop_hook_active = hook_input.get("stop_hook_active", False)
    session_id = hook_input.get("session_id", "")
    cwd = hook_input.get("cwd", "")

    # Avoid infinite loops - if stop hook already active, allow stopping
    if stop_hook_active:
        output_decision("allow", "Stop hook already active")
        return

    # MODIFY: Add agent-type-specific handling
    # Example: Only validate certain agent types
    validate_agents = ["gsd-executor", "gsd-planner", "Explore"]
    should_validate = agent_type in validate_agents

    # Check task completion
    tasks_complete, incomplete_msg = check_tasks_complete(session_id)
    if not tasks_complete:
        # Block stopping - tasks not done
        output_decision("block", incomplete_msg)
        return

    # Validate output quality
    if should_validate:
        output_valid, issue_msg = validate_subagent_output(agent_transcript_path)
        if not output_valid:
            output_decision("block", issue_msg)
            return

    # Cleanup
    cleanup_temp_files(session_id, cwd)

    # Allow stopping
    output_decision("allow")


if __name__ == "__main__":
    main()
