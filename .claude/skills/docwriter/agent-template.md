# Agent Template

This is a reference template for generating Claude Code **subagents** (specialized agents that focus on specific domains or tasks). Generated agents use the `.md.hbs` extension (Handlebars templates).

## Handlebars Variable

The only available Handlebars variable is `{{model.name}}` - use it where the project/model name is needed.

---

## Frontmatter Structure

```yaml
---
name: "[agent-name]"
description: >
  A detailed description of what this agent does, when to use it, and what
  kind of tasks it handles. This should be a full sentence or paragraph,
  not a brief phrase. The description helps other agents and orchestrators
  understand when to delegate work to this agent.
tools: [Read, Glob, Grep, Bash, Write, AskUserQuestion]
disallowedTools: []
model: sonnet
permissionMode: dontAsk
maxTurns: 50
# Optional fields
skills: []
memory: user
isolation: worktree
background: false
mcpServers:
  server-name: ...
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "[validation command]"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "[post-processing command]"
  Stop:
    - hooks:
        - type: command
          command: "[cleanup command]"
---
```

### Required Fields

| Field | Purpose |
|-------|---------|
| `name` | Kebab-case identifier for the agent |
| `description` | **Detailed** explanation (full sentence/paragraph) of what the agent does and when to use it |

### Common Fields

| Field | Purpose | Default |
|-------|---------|---------|
| `tools` | Allowlist of tools the agent can use. Use `Agent(name)` to restrict subagent spawning | Inherits all |
| `disallowedTools` | Denylist applied after tools allowlist | None |
| `model` | Model to use (`inherit`, `sonnet`, `opus`, `haiku`) | `inherit` |
| `permissionMode` | Permission level: `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` | `default` |
| `maxTurns` | Max agentic turns before stopping | 50 |

### Optional Fields

| Field | Purpose |
|-------|---------|
| `skills` | Skills preloaded into subagent context at startup |
| `memory` | Persistent memory across sessions: `user`, `project`, or `local` |
| `isolation` | `worktree` for git worktree isolation (auto-cleanup if no changes) |
| `background` | `true` for concurrent execution (pre-approved permissions, auto-denies unapproved) |
| `mcpServers` | MCP servers this agent can access (reference existing or inline definition) |
| `hooks` | PreToolUse, PostToolUse, Stop, and other lifecycle hooks |

### Description Field Guidance

Agent descriptions should be **detailed**, unlike brief command descriptions:

**Good:**
```yaml
description: >
  Researches the backend codebase to understand service implementations,
  database schemas, and API endpoints. Use this agent when you need deep
  analysis of Java/Spring components or when planning backend modifications.
```

**Bad:**
```yaml
description: Backend researcher
```

---

## Hook Configuration

### PreToolUse Hook

Runs before a tool is executed. Use for validation or pre-processing.

```yaml
PreToolUse:
  - matcher: "Bash"
    hooks:
      - type: command
        command: "[validation script or command]"
```

### PostToolUse Hook

Runs after a tool completes. Use for validation or post-processing.

```yaml
PostToolUse:
  - matcher: "Edit|Write"
    hooks:
      - type: command
        command: "[post-processing script]"
```

### Stop Hook

Runs when the agent stops. Use for cleanup or final output. Note: No matcher needed.

```yaml
Stop:
  - hooks:
      - type: command
        command: "[cleanup script]"
```

---

## Content Structure

After the frontmatter, use this structure:

```markdown
You are the **[Role Name]** for {{model.name}}. [Brief description of responsibilities].

@.claude/rules/xml-rule.md.hbs

## Your Domain

Focus on these areas:
- [Focus area 1]
- [Focus area 2]
- [Focus area 3]

**Relevant file patterns:**
- `[path/pattern/**/*.ext]`
- `[another/pattern/*.ext]`

## Output File

Write your findings to:
```
[output/path/filename.md]
```

## Research Process

1. **[First Phase]**: [What to do]
2. **[Second Phase]**: [What to do]
3. **[Third Phase]**: [What to do]
4. **Signal Completion**: Stop when findings are written to output file

## Output Format

Structure your output file as:

```markdown
# [Title]

## Summary
[Key findings in 2-3 sentences]

## [Section 1]
[Details]

## [Section 2]
[Details]

## Recommendations
[If applicable]
```

## Constraints

- [Limitation 1]
- [Limitation 2]
- Stay within your domain focus
```

---

## Notes

- Agent descriptions should explain **when** to use the agent, not just what it does
- The `@.claude/rules/xml-rule.md.hbs` reference enables proper delegation protocol
- Always include a "Signal Completion" step in the research process
- Use `tools:` + `permissionMode: dontAsk` to restrict agent tool access. Tools not in the list are auto-denied without prompting
- Use `disallowedTools:` as a denylist alternative when you want most tools but need to exclude a few
- Use `isolation: worktree` when agents make file changes that should be reviewed before merging
- Use `background: true` for concurrent agent execution (e.g., parallel research tasks)
- Use `memory: user` to enable persistent cross-session learning for the agent
- Agent discovery locations (priority): CLI flags → project `.claude/agents/` → user `~/.claude/agents/` → plugin agents
