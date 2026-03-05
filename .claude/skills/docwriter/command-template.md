# Command Template

This is a reference template for generating Claude Code **commands** (orchestrator skills that manage multi-step workflows). Generated commands use the `.md.hbs` extension (Handlebars templates).

> **Note:** Commands are now part of the unified skill system. Old `.claude/commands/` paths still work alongside `.claude/skills/<name>/SKILL.md`. Both use the same frontmatter schema.

## Handlebars Variable

The only available Handlebars variable is `{{model.name}}` - use it where the project/model name is needed.

---

## Frontmatter Structure

```yaml
---
name: "[Command Name]"
description: Brief description of what this command does
argument-hint: "[optional-arg]"
disable-model-invocation: true
user-invocable: true
allowed-tools:
  - Task(worker-agent-name)
  - Bash
  - Read
  - AskUserQuestion
# Optional: execution context
context: fork
agent: general-purpose
model: sonnet
# Optional: hooks for subagent management
hooks:
  SubagentStop:
    - matcher: "[agent-name-pattern]"
      hooks:
        - type: command
          command: "echo 'subagent stopped'"
---
```

### Required Fields

| Field | Purpose |
|-------|---------|
| `description` | Brief explanation shown in skill listings. Claude uses this for auto-invocation |
| `user-invocable` | Must be `true` for slash commands |

### Optional Fields

| Field | Purpose |
|-------|---------|
| `argument-hint` | Placeholder text for the command argument |
| `disable-model-invocation` | Set `true` to prevent model from auto-invoking |
| `allowed-tools` | Explicit list of tools this command can use. Use `Task(agent-name, ...)` for agent spawning filters |
| `context` | `fork` to run in isolated subagent context |
| `agent` | Which subagent type to use: `Explore`, `Plan`, `general-purpose`, or custom agent name |
| `model` | Model override: `inherit`, `sonnet`, `opus`, `haiku` |
| `hooks` | Configure lifecycle hooks (SubagentStop, PreToolUse, PostToolUse, etc.) |

---

## Content Structure

After the frontmatter, use this structure:

```markdown
Brief description of what this command does.

## Shared Rule References

Include these @ references based on command type (see Notes for guidance):

@.claude/rules/xml-rule.md
@.claude/rules/task-protocol.md
@.claude/rules/arg-resolution.md    (if command resolves change IDs)
@.claude/rules/templating-rule.md    (if command writes template-generated files)

For commands that validate prerequisite files, use the validation script instead of a rule reference:

```bash
PREREQ=$(python3 .claude/scripts/template_manager.py --command <command-name> --change-id "<change-id>")
```

Parse JSON: `"status": "pass"` → proceed, `"status": "fail"` → display `first_missing.error_message` and STOP.

### Command-Specific Task Initialization

Create the following tasks before starting work:

1. **Task: [First Step Name]**
   - `subject`: "[First Step Name]"
   - `description`: "[What this step accomplishes]"
   - `activeForm`: "[Present continuous form, e.g., 'Parsing input']"

2. **Task: [Second Step Name]**
   - `subject`: "[Second Step Name]"
   - `description`: "[What this step accomplishes]"
   - `activeForm`: "[Present continuous form]"

3. **Task: [Third Step Name]**
   - `subject`: "[Third Step Name]"
   - `description`: "[What this step accomplishes]"
   - `activeForm`: "[Present continuous form]"

---

## Usage

**Syntax:**
```
/<command-path> [argument]
```

**Flags:**
| Flag | Description |
|------|-------------|
| `--flag-name` | What this flag does |

**Examples:**
```
/<command-path> example-arg
/<command-path> --flag-name value
```

---

## Orchestrator Instructions

When this skill is invoked, follow these steps:

### Step 1: [First Step Name]

[Detailed instructions for what to do in this step]

- Key action 1
- Key action 2
- What to do with the results

### Step 2: [Second Step Name]

[Detailed instructions for what to do in this step]

- Key action 1
- Key action 2
- What to do with the results

### Step 3: [Third Step Name]

[Detailed instructions for what to do in this step]

- Key action 1
- Key action 2
- What to do with the results

---

## Notes

- The task list in "Command-Specific Task Initialization" should correspond to the Steps in "Orchestrator Instructions"
- Each Step should have a matching task with the same name
- The `activeForm` should be present-continuous (e.g., "Processing" not "Process")
- **Shared rule references** -- include based on command type:
  - `@.claude/rules/xml-rule.md` -- all commands that dispatch agents via Task tool
  - `@.claude/rules/task-protocol.md` -- all commands that use TaskCreate/TaskUpdate/TaskList
  - `@.claude/rules/arg-resolution.md` -- commands that resolve a change ID from arguments (e.g., apply, research, proposal, archive). Omit for commands with unique resolution flows (e.g., resume uses dashboard-first menu).
  - `template_manager.py` script -- commands that validate prerequisite files (e.g., apply validates tasks.md, proposal validates research.md, archive validates summary). Use the script call pattern instead of a rule reference.
  - `@.claude/rules/templating-rule.md` -- commands whose agents write into template-generated files (e.g., research agents fill research templates)
- Do NOT use `.hbs` suffix in `@` references -- the generated file path has no `.hbs` extension
```
