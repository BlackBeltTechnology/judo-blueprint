---
name: docwriter
description: Generate Claude Code artifacts (skills, commands, subagents) from natural language descriptions. Creates properly structured files with frontmatter, hooks, and required sections.
argument-hint: "[description of what to create]"
user-invocable: true
disable-model-invocation: false
hooks:
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "python3 \"$CLAUDE_PROJECT_DIR/.claude/skills/docwriter/validator.py\""
---

# Docwriter

Generate Claude Code artifacts from natural language descriptions.

**Templates and References loaded automatically:**
- @command-template.md
- @agent-template.md
- @.claude/skills/docwriter/hooks-reference.md
- @.claude/skills/docwriter/claude-meta.md

## Quick Reference: ~/.claude Paths

| Path | Contains | Use For |
|------|----------|---------|
| `~/.claude/projects/{project}/{session}.jsonl` | Conversation transcript | Reading history |
| `~/.claude/tasks/{session}/*.json` | Task state | Checking/updating tasks |
| `~/.claude/file-history/{session}/` | File versions | Rollback, comparison |
| `~/.claude/debug/{session}.txt` | Debug logs | Troubleshooting |
| `~/.claude/todos/` | Agent task assignments | Cross-agent coordination |

**Note:** Use the `transcript_path` field from hook input JSON for direct transcript access.

## Workflow

### Step 1: Determine Artifact Type

Use the **AskUserQuestion** tool to ask what type of artifact to create:

**Question:** "What type of Claude Code artifact do you want to create?"

**Options:**
1. **Skill** - A standalone capability with its own directory (e.g., `docwriter/SKILL.md.hbs`). Skills do NOT use Task Management Protocol.
2. **Command** - An orchestrator that manages multi-step workflows (e.g., `opsx/new.md.hbs`). Commands MUST include Task Management Protocol.
3. **Subagent** - A specialized agent for focused tasks (e.g., `backend-researcher.md.hbs`). Subagents include hook configurations.

### Step 2: Gather Details Based on Type

#### For Skills:
- Ask for skill name (kebab-case)
- Ask for description of what the skill does
- Ask if it needs execution context isolation (`context: fork` + `agent` field)
- Ask if it needs a model override (`model: sonnet|opus|haiku|inherit`)
- File will be created at: `.claude/skills/<name>/SKILL.md.hbs`

#### For Commands:
- Ask for command path (e.g., `judospec/research` or `mycommand`)
- Ask for description of what the command does
- Note: Commands use the same skill system; `.claude/commands/<path>.md.hbs` still works
- File will be created at: `.claude/commands/<path>.md.hbs`

#### For Subagents:
- Ask for agent name (kebab-case)
- Ask for detailed description (full sentence/paragraph)
- Ask about tool restrictions (`tools` allowlist and/or `disallowedTools` denylist)
- Ask about isolation needs (`isolation: worktree`, `background: true`)
- Ask about persistent memory (`memory: user|project|local`)
- Ask about max turns (`maxTurns`, default 50)
- File will be created at: `.claude/agents/<name>.md.hbs`

### Step 2.5: Configure Hooks (Hook Wizard)

Use the **AskUserQuestion** tool:

**Question:** "Does this [artifact type] need hooks?"

**Options:**
1. **Yes** - Configure hooks for this artifact
2. **No** - Skip hook configuration

#### If Yes: Select Lifecycle Groups

**Question:** "Which lifecycle phases need hooks?"

**Options (multi-select):**
1. **Tool Lifecycle** - React to tool calls (PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest)
2. **Agent Lifecycle** - React to subagents and stopping (SubagentStart, SubagentStop, Stop, Notification, TeammateIdle, TaskCompleted)
3. **Session Lifecycle** - React to session events (SessionStart, SessionEnd) - *Note: Requires settings.json, not frontmatter*
4. **Prompt Lifecycle** - React to prompts (UserPromptSubmit, PreCompact) - *Note: Requires settings.json, not frontmatter*
5. **Config Lifecycle** - React to settings/skills changes (ConfigChange) - *Note: Requires settings.json*
6. **Worktree Lifecycle** - React to git worktree operations (WorktreeCreate, WorktreeRemove) - *Note: Requires settings.json*

#### For Each Selected Group: Select Events

**Tool Lifecycle Events:**
| Event | Fires When | Can Block? | Matcher |
|-------|------------|------------|---------|
| PreToolUse | Before tool executes | Yes | tool_name |
| PostToolUse | After tool succeeds | No | tool_name |
| PostToolUseFailure | After tool fails | No | tool_name |
| PermissionRequest | Permission dialog appears | Yes | tool_name |

**Agent Lifecycle Events:**
| Event | Fires When | Can Block? | Matcher |
|-------|------------|------------|---------|
| SubagentStart | Subagent spawned | No | agent_type |
| SubagentStop | Subagent finishes | Yes | agent_type |
| Stop | Claude finishes responding | Yes | No matcher |
| Notification | Notification sent | No | notification_type |
| TeammateIdle | Agent team teammate going idle | No | No matcher |
| TaskCompleted | Task marked complete | No | No matcher |

*Note: `Stop` in subagent frontmatter becomes `SubagentStop` event.*

**Config Lifecycle Events:**
| Event | Fires When | Can Block? | Matcher |
|-------|------------|------------|---------|
| ConfigChange | Config file changed | No | config_type: user_settings, project_settings, local_settings, policy_settings, skills |

**Worktree Lifecycle Events:**
| Event | Fires When | Can Block? | Matcher |
|-------|------------|------------|---------|
| WorktreeCreate | Git worktree being created | No | No matcher (prints path to stdout) |
| WorktreeRemove | Git worktree being removed | No | No matcher |

#### For Each Selected Event: Gather Details

**Question:** "Configure [Event] hook:"

1. **Matcher pattern** (if applicable): Regex to filter when hook fires
   - Tool events: Match tool name (e.g., `"Bash"`, `"Edit|Write"`, `"mcp__.*"`)
   - Agent events: Match agent type (e.g., `"Explore"`, `"gsd-.*"`)

2. **Handler type:**
   - **command** - Shell script (deterministic validation)
   - **http** - POST to URL (webhook integration, external services)
   - **prompt** - Single LLM evaluation
   - **agent** - Multi-turn LLM with tool access

3. **Script/prompt/URL details:**
   - For command: Script path (use `$CLAUDE_PROJECT_DIR/.claude/hooks/<name>.py`)
   - For http: URL endpoint, optional headers and `allowedEnvVars` for env var substitution in headers
   - For prompt/agent: Prompt text (use `$ARGUMENTS` for hook input)

4. **Options:**
   - `async: true` - Run in background (command only, cannot block)
   - `timeout` - Custom timeout in seconds
   - `statusMessage` - Custom spinner text while hook runs
   - `once: true` - Run only once per session then is removed (skills only, not agents)

#### Explore Integration for ~/.claude Data

**If user's hook description mentions:** session, transcript, task, history, metadata, conversation

**Then spawn Explore subagent:**
```
Explore ~/.claude to find paths for [user's data need].
Return the exact path pattern and example content structure.
Key starting points:
- ~/.claude/projects/ for sessions and transcripts
- ~/.claude/tasks/ for task state
- ~/.claude/file-history/ for file versions
```

Use discovered paths in the generated hook script with comment:
```python
# Path discovered via Explore: ~/.claude/tasks/{session}/
```

#### Validate Hook Placement

**Frontmatter-valid hooks (Tool + Agent lifecycle):**
- PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest
- SubagentStart, SubagentStop, Stop, Notification

**Settings.json-only hooks (Session + Prompt + Config + Worktree lifecycle):**
- SessionStart, SessionEnd, UserPromptSubmit, PreCompact
- TeammateIdle, TaskCompleted, ConfigChange, WorktreeCreate, WorktreeRemove

If user selects a settings.json-only hook, warn:
> "This hook event must be placed in `.claude/settings.json`, not in artifact frontmatter. Would you like me to show the settings.json format instead?"

### Step 3: Get Natural Language Description

Prompt: "Describe what this [skill/command/agent] should do. Be specific about its purpose, workflow steps, and any constraints."

### Step 4: Generate the Artifact

Based on the artifact type and description, generate the file:

**For Skills:**
- Create YAML frontmatter with name, description, user-invocable
- Optionally add: `context: fork`, `agent`, `model`, `allowed-tools`
- Include configured hooks from Step 2.5
- Support `$ARGUMENTS` and `$ARGUMENTS[N]` substitution in content
- Create content sections appropriate to the skill's purpose
- Do NOT include Task Management Protocol

**For Commands:**
- Create YAML frontmatter (see @command-template.md)
- Include configured hooks from Step 2.5
- Include `@.claude/rules/xml-rule.md.hbs` reference
- Include complete Task Management Protocol section with tasks derived from steps
- Include Usage section
- Include Orchestrator Instructions with numbered Steps
- Each Step should have a corresponding task in the Initialization Requirement

**For Subagents:**
- Create YAML frontmatter with detailed description (see @agent-template.md)
- Include `tools`/`disallowedTools` for tool access control
- Optionally add: `maxTurns`, `memory`, `isolation`, `background`, `mcpServers`, `skills`
- Include configured hooks from Step 2.5 (Stop becomes SubagentStop)
- Include `@.claude/rules/xml-rule.md.hbs` reference
- Include: Your Domain, Output File, Research Process, Output Format, Constraints sections

**Hook Frontmatter Format:**
```yaml
hooks:
  PreToolUse:
    - matcher: "Bash"  # Regex pattern
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py"
          statusMessage: "Validating..."
          once: true  # Run only once per session (skills only)
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/process.py"
          async: true
        - type: http
          url: "http://localhost:8080/hooks/post-write"
          headers:
            Authorization: "Bearer $API_TOKEN"
          allowedEnvVars: ["API_TOKEN"]
          timeout: 30
  Stop:  # Becomes SubagentStop for subagents
    - hooks:
        - type: prompt
          prompt: "Evaluate if all tasks are complete. $ARGUMENTS"
          model: haiku
          timeout: 30
```

**Important:**
- All generated files use `.md.hbs` extension
- Use `{{model.name}}` where the project name is needed
- All file references use `@.claude/...` format (never absolute paths)
- Hook scripts should be placed in `.claude/hooks/` directory
- Reference @hooks-reference.md for detailed hook schemas

### Step 5: Generate Hook Scripts (if configured)

For each hook configured in Step 2.5, generate the corresponding script:

**Use templates from:** `.claude/skills/docwriter/templates/`
- `pretooluse-validator.py` - For PreToolUse permission decisions
- `posttooluse-processor.py` - For PostToolUse result processing
- `subagent-stop-cleanup.py` - For SubagentStop/Stop cleanup
- `bash-hook-template.sh` - For Bash-based hooks

**Customize each script:**
1. Copy the appropriate template to `.claude/hooks/<artifact-name>-<event>.py`
2. Modify the `# MODIFY:` sections based on user requirements
3. If hook needs `~/.claude` data, add paths discovered via Explore

### Step 6: Prompt for Additional Artifacts

After creating the primary artifact, ask: "Do you also need any of these?"

**Options (multi-select):**
1. **Rule** - A mixin for common instructions (like `xml-rule.md.hbs`)
2. **Script** - A helper script (like `validator.py`)
3. **None** - Skip additional artifacts

#### If Rule selected:
- Ask for rule name (kebab-case)
- Ask for rule purpose/description
- Create at `.claude/rules/<name>.md.hbs`
- Suggest adding `@.claude/rules/<name>.md.hbs` to the primary artifact

#### If Script selected:
- Ask for script name and purpose
- Ask for language (Python default, shell option)
- Create at `.claude/scripts/<name>.py` (or `.sh`)
- Include argparse boilerplate for Python scripts
- Make script executable
- Provide invocation pattern: `$CLAUDE_PROJECT_DIR/.claude/scripts/<name>`

### Step 7: Check for Template Updates

If the generated artifact introduces a pattern not in the current templates:
- Ask: "This introduces a new pattern. Would you like to update the template?"
- If yes, update the appropriate template file (command-template.md or agent-template.md)
- Preserve existing sections when updating

## Output Summary

After generation, summarize:
- File(s) created with paths
- Key sections included
- Hook configuration (events, matchers, handlers)
- Any additional artifacts created (scripts, rules)
- How to invoke (for skills/commands)

## Notes

- Commands ALWAYS need Task Management Protocol (validated by hook)
- Skills NEVER need Task Management Protocol
- Subagents need detailed descriptions in frontmatter
- Use `{{model.name}}` for project-specific references
- Never use absolute paths - always use `@.claude/...` syntax
- **Hook Lifecycle Scoping:** Frontmatter hooks only fire while the component is active
- **Stop → SubagentStop:** Stop hooks in subagent frontmatter become SubagentStop events
- **Two Data Sources:** Hooks can access stdin JSON (immediate context) AND `~/.claude` filesystem (persistent state)
- **Explore for Discovery:** When hooks need `~/.claude` data, spawn Explore to find exact paths
