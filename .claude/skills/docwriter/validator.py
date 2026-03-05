#!/usr/bin/env python3
"""
Validator hook script for docwriter skill.
Validates that command files in .claude/commands/ have required structure.
Also validates Python hook scripts and hook frontmatter in .md files.

Triggered via PostToolUse hook on Write tool.

Exit codes:
  0 - Allow (validation passed or file not applicable)
  2 - Block (validation failed, error message on stderr)
"""

import json
import sys
import re
import fnmatch
import ast


def parse_hook_input():
    """Parse JSON input from stdin. Returns file_path or None on error."""
    try:
        data = json.load(sys.stdin)
        # Hook input structure: { "tool_input": { "file_path": "..." } }
        return data.get("tool_input", {}).get("file_path")
    except (json.JSONDecodeError, AttributeError):
        return None


def matches_command_pattern(file_path):
    """Check if file path matches .claude/commands/**/*.md.hbs pattern."""
    if not file_path:
        return False
    # Normalize path separators
    normalized = file_path.replace("\\", "/")
    # Check for .claude/commands/ anywhere in path with .md.hbs extension
    return ".claude/commands/" in normalized and normalized.endswith(".md.hbs")


def matches_python_pattern(file_path):
    """Check if file path is a Python file."""
    if not file_path:
        return False
    return file_path.endswith(".py")


def matches_hook_md_pattern(file_path):
    """Check if file path is a markdown file that might contain hooks."""
    if not file_path:
        return False
    # Normalize path separators
    normalized = file_path.replace("\\", "/")
    # Check for .md files in .claude/ directory (skills, hooks, etc.)
    return ".claude/" in normalized and normalized.endswith(".md")


def read_file_content(file_path):
    """Read file content. Returns None on error."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except (IOError, OSError):
        return None


# =============================================================================
# Python Hook Script Validation
# =============================================================================

def validate_python_syntax(content, file_path):
    """Validate Python syntax using AST parsing. Returns list of errors."""
    errors = []
    try:
        ast.parse(content)
    except SyntaxError as e:
        errors.append(f"Python syntax error at line {e.lineno}: {e.msg}")
    return errors


def check_python_imports(tree):
    """Check for required imports in AST. Returns list of errors."""
    errors = []
    required_imports = {"sys", "json"}
    found_imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found_imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found_imports.add(node.module.split('.')[0])

    missing = required_imports - found_imports
    if missing:
        errors.append(f"Missing required imports: {', '.join(sorted(missing))}")

    return errors


def check_stdin_read_pattern(tree):
    """Check for stdin read pattern (json.load(sys.stdin) or similar). Returns list of errors."""
    errors = []
    found_stdin_read = False

    for node in ast.walk(tree):
        # Look for json.load(sys.stdin)
        if isinstance(node, ast.Call):
            # Check for json.load
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "load":
                    # Check if first arg is sys.stdin
                    if node.args:
                        arg = node.args[0]
                        if isinstance(arg, ast.Attribute):
                            if arg.attr == "stdin":
                                found_stdin_read = True
                                break
            # Also check for sys.stdin.read() pattern
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "read":
                    if isinstance(node.func.value, ast.Attribute):
                        if node.func.value.attr == "stdin":
                            found_stdin_read = True
                            break

    if not found_stdin_read:
        errors.append("Missing stdin read pattern: hook scripts should read input via json.load(sys.stdin) or sys.stdin.read()")

    return errors


def check_json_output_pattern(tree):
    """Check for JSON output pattern (json.dumps or print with json). Returns list of errors."""
    errors = []
    found_json_output = False

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # Check for json.dumps
            if isinstance(node.func, ast.Attribute):
                if node.func.attr == "dumps":
                    found_json_output = True
                    break
            # Check for print() call (common for output)
            if isinstance(node.func, ast.Name):
                if node.func.id == "print":
                    found_json_output = True
                    break

    if not found_json_output:
        errors.append("Missing JSON output pattern: hook scripts should output via json.dumps() or print()")

    return errors


def validate_python_hook_script(file_path):
    """Run all Python hook script validations. Returns list of errors."""
    content = read_file_content(file_path)
    if content is None:
        return []

    errors = []

    # First check syntax
    syntax_errors = validate_python_syntax(content, file_path)
    if syntax_errors:
        return syntax_errors  # Can't do AST analysis if syntax is invalid

    # Parse AST for structure checks
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return errors  # Already caught above

    # Check required imports
    errors.extend(check_python_imports(tree))

    # Check stdin read pattern
    errors.extend(check_stdin_read_pattern(tree))

    # Check JSON output pattern
    errors.extend(check_json_output_pattern(tree))

    return errors


# =============================================================================
# Hook Frontmatter YAML Validation
# =============================================================================

# Valid hook event names per Claude Code specification (2026)
VALID_HOOK_EVENTS = {
    "PreToolUse",
    "PostToolUse",
    "PostToolUseFailure",
    "PermissionRequest",
    "SubagentStart",
    "SubagentStop",
    "Stop",
    "Notification",
    "TeammateIdle",
    "TaskCompleted",
    "ConfigChange",
    "WorktreeCreate",
    "WorktreeRemove",
    "SessionStart",
    "SessionEnd",
    "UserPromptSubmit",
    "PreCompact",
}


def extract_hooks_from_frontmatter(frontmatter):
    """Extract hooks section from frontmatter. Returns (hooks_str, found)."""
    if not frontmatter:
        return None, False

    # Look for hooks: section
    hooks_match = re.search(r'^hooks:\s*\n((?:[ \t]+.+\n?)*)', frontmatter, re.MULTILINE)
    if not hooks_match:
        return None, False

    return hooks_match.group(0), True


def validate_hook_entry(hook_text, line_offset=0):
    """Validate a single hook entry. Returns list of errors."""
    errors = []

    # Extract event type (e.g., "- type: PostToolUse")
    type_match = re.search(r'type:\s*(\S+)', hook_text)
    if not type_match:
        errors.append("Hook entry missing required 'type' field")
    else:
        event_type = type_match.group(1)
        if event_type not in VALID_HOOK_EVENTS:
            errors.append(f"Invalid hook event type '{event_type}'. Valid types: {', '.join(sorted(VALID_HOOK_EVENTS))}")

    # Check for command, prompt, or url (at least one required)
    has_command = "command:" in hook_text
    has_prompt = "prompt:" in hook_text
    has_url = "url:" in hook_text

    if not has_command and not has_prompt and not has_url:
        errors.append("Hook entry must have 'command', 'prompt', or 'url' field")

    # Validate matcher is a string if present
    matcher_match = re.search(r'matcher:\s*(.+)', hook_text)
    if matcher_match:
        matcher_value = matcher_match.group(1).strip()
        # Check if it looks like a non-string (e.g., array, number, etc.)
        if matcher_value.startswith('[') or matcher_value.startswith('{'):
            errors.append("Hook 'matcher' field must be a string, not an array or object")

    return errors


def validate_hooks_in_frontmatter(frontmatter):
    """Validate hooks section in frontmatter. Returns list of errors."""
    errors = []

    hooks_str, found = extract_hooks_from_frontmatter(frontmatter)
    if not found:
        return []  # No hooks section, that's OK

    # Split into individual hook entries (each starts with "- ")
    # Simple regex to find hook entries
    hook_entries = re.findall(r'- type:.*?(?=\n- type:|\n[^\s-]|\Z)', hooks_str, re.DOTALL)

    if not hook_entries:
        # Check if hooks section exists but has no entries
        if "hooks:" in frontmatter:
            return []  # Empty hooks section is valid

    for i, entry in enumerate(hook_entries):
        entry_errors = validate_hook_entry(entry)
        for error in entry_errors:
            errors.append(f"Hook entry {i + 1}: {error}")

    return errors


def validate_hook_md_file(file_path):
    """Validate hooks in a markdown file's frontmatter. Returns list of errors."""
    content = read_file_content(file_path)
    if content is None:
        return []

    frontmatter, has_frontmatter = extract_frontmatter(content)
    if not has_frontmatter:
        return []  # No frontmatter, no hooks to validate

    return validate_hooks_in_frontmatter(frontmatter)


def extract_frontmatter(content):
    """Extract YAML frontmatter from content. Returns (frontmatter_str, has_frontmatter)."""
    if not content.startswith("---"):
        return None, False

    # Find the closing ---
    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        return None, False

    frontmatter = content[3:3 + end_match.start()]
    return frontmatter, True


def validate_frontmatter(frontmatter):
    """Validate required frontmatter fields. Returns list of errors."""
    errors = []

    if frontmatter is None:
        errors.append("Missing YAML frontmatter (must start with ---)")
        return errors

    # Check for required fields (simple string matching, not full YAML parsing)
    if "description:" not in frontmatter:
        errors.append("Missing required frontmatter field: description")

    if "user-invocable:" not in frontmatter:
        errors.append("Missing required frontmatter field: user-invocable")

    return errors


def validate_task_protocol(content):
    """Validate Task Management Protocol section. Returns list of errors."""
    errors = []

    # Check main section
    if "## Task Management Protocol" not in content:
        errors.append("Missing required section: ## Task Management Protocol")
        return errors  # Can't check subsections if main section missing

    # Check subsections
    if "### Initialization Requirement" not in content:
        errors.append("Missing required subsection: ### Initialization Requirement")

    if "### State Management Rules" not in content:
        errors.append("Missing required subsection: ### State Management Rules")

    if "### Completion Requirement" not in content:
        errors.append("Missing required subsection: ### Completion Requirement")

    return errors


def validate_orchestrator_instructions(content):
    """Validate Orchestrator Instructions section. Returns list of errors."""
    errors = []

    # Check main section
    if "## Orchestrator Instructions" not in content:
        errors.append("Missing required section: ## Orchestrator Instructions")
        return errors

    # Check for at least one Step
    if "### Step" not in content:
        errors.append("Orchestrator Instructions must have at least one ### Step subsection")

    return errors


def validate_no_absolute_paths(content):
    """Check for absolute paths that should use @ syntax. Returns list of errors."""
    errors = []

    # Patterns that indicate absolute paths
    absolute_patterns = [
        (r'/home/[^\s\'"]+', "Absolute path starting with /home/"),
        (r'/Users/[^\s\'"]+', "Absolute path starting with /Users/"),
    ]

    lines = content.split('\n')
    for line_num, line in enumerate(lines, 1):
        # Skip lines that are in code blocks showing examples
        # (simple heuristic: if line contains "SHALL" or is describing a pattern)
        if "SHALL" in line:
            continue

        for pattern, desc in absolute_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                # Ignore if it's in a "rejected" example context
                if "✗" in line or "rejected" in line.lower():
                    continue
                errors.append(f"Line {line_num}: {desc} found: {match[:50]}... (use @.claude/... syntax instead)")

    return errors


def validate_command_file(file_path):
    """Run all validations on a command file. Returns list of errors."""
    content = read_file_content(file_path)
    if content is None:
        # Can't read file, allow it (might be deleted or permission issue)
        return []

    errors = []

    # Extract and validate frontmatter
    frontmatter, has_frontmatter = extract_frontmatter(content)
    if not has_frontmatter:
        errors.append("Missing YAML frontmatter (file must start with ---)")
    else:
        errors.extend(validate_frontmatter(frontmatter))

    # Validate Task Management Protocol
    errors.extend(validate_task_protocol(content))

    # Validate Orchestrator Instructions
    errors.extend(validate_orchestrator_instructions(content))

    # Validate no absolute paths
    errors.extend(validate_no_absolute_paths(content))

    return errors


def format_error_message(file_path, errors, help_text=None):
    """Format validation errors into a readable message."""
    msg = f"Validation failed for {file_path}:\n"
    for error in errors:
        msg += f"  - {error}\n"
    if help_text:
        msg += f"\n{help_text}"
    return msg


def format_command_error_message(file_path, errors):
    """Format command file validation errors."""
    return format_error_message(
        file_path, errors,
        "Fix these issues and try again. See @command-template.md for the required structure."
    )


def format_python_error_message(file_path, errors):
    """Format Python hook script validation errors."""
    return format_error_message(
        file_path, errors,
        "Python hook scripts must:\n"
        "  - Import sys and json\n"
        "  - Read input via json.load(sys.stdin)\n"
        "  - Output via json.dumps() or print()"
    )


def format_hook_error_message(file_path, errors):
    """Format hook frontmatter validation errors."""
    return format_error_message(
        file_path, errors,
        "Hook entries must have:\n"
        "  - type: (valid event name)\n"
        "  - command:, prompt:, or url: (at least one)\n"
        f"Valid event types: {', '.join(sorted(VALID_HOOK_EVENTS))}"
    )


def main():
    # Parse input
    file_path = parse_hook_input()

    if file_path is None:
        # JSON parse error - allow to avoid blocking on malformed input
        sys.exit(0)

    # Check if this is a command file
    if matches_command_pattern(file_path):
        errors = validate_command_file(file_path)
        if errors:
            print(format_command_error_message(file_path, errors), file=sys.stderr)
            sys.exit(2)
        sys.exit(0)

    # Check if this is a Python file
    if matches_python_pattern(file_path):
        errors = validate_python_hook_script(file_path)
        if errors:
            print(format_python_error_message(file_path, errors), file=sys.stderr)
            sys.exit(2)
        sys.exit(0)

    # Check if this is a markdown file with potential hooks
    if matches_hook_md_pattern(file_path):
        errors = validate_hook_md_file(file_path)
        if errors:
            print(format_hook_error_message(file_path, errors), file=sys.stderr)
            sys.exit(2)
        sys.exit(0)

    # Not a file type we validate - allow
    sys.exit(0)


if __name__ == "__main__":
    main()
