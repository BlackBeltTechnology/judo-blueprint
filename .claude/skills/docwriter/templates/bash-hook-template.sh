#!/bin/bash
#
# Bash Hook Template - Shell Script for Hook Processing
#
# This template shows how to write hooks in Bash using jq for JSON processing.
# Bash hooks are useful for simple validations or when Python isn't available.
#
# USAGE IN FRONTMATTER:
# ---
# hooks:
#   PreToolUse:
#     - matcher: "Bash"
#       hooks:
#         - type: command
#           command: "$CLAUDE_PROJECT_DIR/.claude/hooks/bash-hook-template.sh"
# ---
#
# EXIT CODES:
#   0 - Success (JSON output processed)
#   2 - Blocking error (stderr shown to Claude)
#   Other - Non-blocking error (stderr in verbose mode)
#
# DEPENDENCIES: jq (JSON processor)
#

set -euo pipefail

# MODIFY: Configuration
BLOCK_DANGEROUS_COMMANDS=true
LOG_ENABLED=false
LOG_FILE="/tmp/claude-hook.log"

# Read JSON input from stdin
INPUT=$(cat)

# Extract common fields using jq
HOOK_EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')

# MODIFY: Add logging if needed
log_message() {
    if [ "$LOG_ENABLED" = true ]; then
        echo "$(date -Iseconds) [$HOOK_EVENT] $1" >> "$LOG_FILE"
    fi
}

# Output JSON decision for PreToolUse
output_pretooluse_decision() {
    local decision="$1"
    local reason="${2:-}"

    if [ -n "$reason" ]; then
        jq -n \
            --arg decision "$decision" \
            --arg reason "$reason" \
            '{
                hookSpecificOutput: {
                    hookEventName: "PreToolUse",
                    permissionDecision: $decision,
                    permissionDecisionReason: $reason
                }
            }'
    else
        jq -n \
            --arg decision "$decision" \
            '{
                hookSpecificOutput: {
                    hookEventName: "PreToolUse",
                    permissionDecision: $decision
                }
            }'
    fi
}

# Output JSON for PostToolUse context
output_posttooluse_context() {
    local context="$1"

    jq -n \
        --arg context "$context" \
        '{
            hookSpecificOutput: {
                hookEventName: "PostToolUse",
                additionalContext: $context
            }
        }'
}

# Output top-level decision (for Stop, SubagentStop, etc.)
output_decision() {
    local decision="$1"
    local reason="${2:-}"

    if [ -n "$reason" ]; then
        jq -n \
            --arg decision "$decision" \
            --arg reason "$reason" \
            '{decision: $decision, reason: $reason}'
    else
        jq -n \
            --arg decision "$decision" \
            '{decision: $decision}'
    fi
}

# Output blocking error (exit 2)
output_blocking_error() {
    echo "$1" >&2
    exit 2
}

# MODIFY: Add your validation functions here

validate_bash_command() {
    local command="$1"

    # MODIFY: Patterns to block
    local blocked_patterns=(
        'rm -rf /'
        'rm -rf *'
        'chmod 777'
        '> /dev/sda'
        'mkfs'
        'dd if='
    )

    for pattern in "${blocked_patterns[@]}"; do
        if [[ "$command" == *"$pattern"* ]]; then
            output_pretooluse_decision "deny" "Blocked dangerous pattern: $pattern"
            exit 0
        fi
    done

    # MODIFY: Patterns to auto-allow
    if [[ "$command" =~ ^(ls|cat|git\ status|git\ diff|npm\ test) ]]; then
        output_pretooluse_decision "allow"
        exit 0
    fi

    # Default: ask for permission
    output_pretooluse_decision "ask"
}

validate_write_operation() {
    local file_path="$1"

    # MODIFY: Protected paths
    local protected_paths=(
        "/etc/"
        "/usr/"
        "/var/"
        "$HOME/.ssh/"
        "$HOME/.aws/"
    )

    for path in "${protected_paths[@]}"; do
        if [[ "$file_path" == "$path"* ]]; then
            output_pretooluse_decision "deny" "Cannot write to protected path: $path"
            exit 0
        fi
    done

    output_pretooluse_decision "allow"
}

# Main routing logic
case "$HOOK_EVENT" in
    "PreToolUse")
        log_message "PreToolUse: $TOOL_NAME"

        case "$TOOL_NAME" in
            "Bash")
                COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
                if [ "$BLOCK_DANGEROUS_COMMANDS" = true ]; then
                    validate_bash_command "$COMMAND"
                else
                    output_pretooluse_decision "allow"
                fi
                ;;
            "Write")
                FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
                validate_write_operation "$FILE_PATH"
                ;;
            "Edit")
                FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
                validate_write_operation "$FILE_PATH"
                ;;
            *)
                # MODIFY: Default behavior for other tools
                output_pretooluse_decision "allow"
                ;;
        esac
        ;;

    "PostToolUse")
        log_message "PostToolUse: $TOOL_NAME"

        # MODIFY: Add post-tool processing
        case "$TOOL_NAME" in
            "Write"|"Edit")
                FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

                # Example: Notify about Python file changes
                if [[ "$FILE_PATH" == *.py ]]; then
                    # Check syntax (optional)
                    if command -v python3 &> /dev/null; then
                        if ! python3 -m py_compile "$FILE_PATH" 2>/dev/null; then
                            output_posttooluse_context "Warning: Python syntax error in $FILE_PATH"
                            exit 0
                        fi
                    fi
                fi
                ;;
        esac
        # No output needed for most PostToolUse
        ;;

    "Stop"|"SubagentStop")
        log_message "Stop hook triggered"

        # MODIFY: Add stop validation logic
        # Example: Check if there are uncommitted changes
        if command -v git &> /dev/null && [ -d ".git" ]; then
            if ! git diff --quiet 2>/dev/null; then
                # Has uncommitted changes - warn but don't block
                output_decision "allow"
            else
                output_decision "allow"
            fi
        else
            output_decision "allow"
        fi
        ;;

    "SessionStart")
        log_message "Session started"
        # MODIFY: Add session initialization
        # Note: Can write to $CLAUDE_ENV_FILE to set environment variables
        ;;

    "SessionEnd")
        log_message "Session ended"
        # MODIFY: Add cleanup logic
        ;;

    *)
        log_message "Unknown event: $HOOK_EVENT"
        # Unknown event - allow by default
        ;;
esac

exit 0
