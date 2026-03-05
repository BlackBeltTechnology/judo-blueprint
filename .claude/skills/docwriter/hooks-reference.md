# Hooks Reference for Docwriter

This distilled reference provides all hook knowledge needed to generate Claude Code artifacts with hooks.

## Hook Event Summary (17 Events)

| Event | Lifecycle | Fires When | Matcher Target | Blockable |
|-------|-----------|------------|----------------|-----------|
| **SessionStart** | Session | Session starts/resumes | `source`: startup, resume, clear, compact | No |
| **SessionEnd** | Session | Session terminates | `reason`: clear, logout, prompt_input_exit, bypass_permissions_disabled, other | No |
| **UserPromptSubmit** | Prompt | User submits prompt | No matcher (always fires) | Yes |
| **PreCompact** | Prompt | Before context compaction | `trigger`: manual, auto | No |
| **PreToolUse** | Tool | Before tool executes | `tool_name`: Bash, Edit, Write, etc. | Yes |
| **PermissionRequest** | Tool | Permission dialog appears | `tool_name` | Yes |
| **PostToolUse** | Tool | After tool succeeds | `tool_name` | No |
| **PostToolUseFailure** | Tool | After tool fails | `tool_name` | No |
| **SubagentStart** | Agent | Subagent spawned | `agent_type`: Explore, Plan, custom | No |
| **SubagentStop** | Agent | Subagent finishes | `agent_type` | Yes |
| **Stop** | Agent | Claude finishes responding | No matcher (always fires) | Yes |
| **Notification** | Agent | Notification sent | `notification_type` | No |
| **TeammateIdle** | Agent | Agent team teammate going idle | No matcher (always fires) | No |
| **TaskCompleted** | Agent | Task marked complete | No matcher (always fires) | No |
| **ConfigChange** | Config | Config file changed | `config_type`: user_settings, project_settings, local_settings, policy_settings, skills | No |
| **WorktreeCreate** | Worktree | Git worktree being created | No matcher (prints path to stdout) | No |
| **WorktreeRemove** | Worktree | Git worktree being removed | No matcher | No |

## Lifecycle Groups

### Session Lifecycle
- `SessionStart` - Load context, set environment variables via `CLAUDE_ENV_FILE`
- `SessionEnd` - Cleanup tasks

### Prompt Lifecycle
- `UserPromptSubmit` - Validate/enrich prompts before processing
- `PreCompact` - React before context compaction

### Tool Lifecycle (Most common for frontmatter)
- `PreToolUse` - Block/allow/modify tool calls
- `PermissionRequest` - Auto-approve permissions
- `PostToolUse` - Log/validate after success
- `PostToolUseFailure` - Handle errors, provide context

### Agent Lifecycle
- `SubagentStart` - Inject context into subagent
- `SubagentStop` - Evaluate if subagent should continue (Stop in frontmatter → SubagentStop)
- `Stop` - Block Claude from stopping, continue working
- `Notification` - React to notifications
- `TeammateIdle` - React when agent team teammate goes idle
- `TaskCompleted` - React when a task is marked complete

### Config Lifecycle
- `ConfigChange` - React to settings/skills file changes

### Worktree Lifecycle
- `WorktreeCreate` - React when git worktree is created
- `WorktreeRemove` - React when git worktree is removed

## Common Input Fields (All Events)

All hooks receive via stdin:
```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/transcript.jsonl",
  "cwd": "/current/working/dir",
  "permission_mode": "default|plan|acceptEdits|dontAsk|bypassPermissions",
  "hook_event_name": "EventName"
}
```

## Event-Specific Input Fields

| Event | Additional Fields |
|-------|-------------------|
| SessionStart | `source`, `model`, `agent_type?` |
| UserPromptSubmit | `prompt` |
| PreToolUse | `tool_name`, `tool_input`, `tool_use_id` |
| PermissionRequest | `tool_name`, `tool_input`, `permission_suggestions?` |
| PostToolUse | `tool_name`, `tool_input`, `tool_response`, `tool_use_id` |
| PostToolUseFailure | `tool_name`, `tool_input`, `tool_use_id`, `error`, `is_interrupt?` |
| Notification | `message`, `title?`, `notification_type` |
| SubagentStart | `agent_id`, `agent_type` |
| SubagentStop | `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` |
| Stop | `stop_hook_active` |
| TeammateIdle | (no additional fields documented) |
| TaskCompleted | (no additional fields documented) |
| ConfigChange | `config_type` |
| WorktreeCreate | (no additional fields documented) |
| WorktreeRemove | (no additional fields documented) |
| PreCompact | `trigger`, `custom_instructions` |
| SessionEnd | `reason` |

### Tool Input Schemas (PreToolUse/PostToolUse)

**File Operations:**
- **Read**: `{ "file_path": "/path", "offset": 10, "limit": 50 }`
- **Write**: `{ "file_path": "/path", "content": "..." }`
- **Edit**: `{ "file_path": "/path", "old_string": "...", "new_string": "...", "replace_all": false }`
- **Glob**: `{ "pattern": "**/*.ts", "path": "/dir" }`
- **Grep**: `{ "pattern": "TODO.*", "path": "/path", "glob": "*.ts", "output_mode": "content" }`
- **NotebookEdit**: `{ "notebook_path": "/path.ipynb", "new_source": "...", "cell_id": "...", "cell_type": "code|markdown", "edit_mode": "replace|insert|delete" }`

**Execution:**
- **Bash**: `{ "command": "...", "description": "...", "timeout": 120000, "run_in_background": false }`
- **Task**: `{ "prompt": "...", "description": "...", "subagent_type": "Explore", "model": "sonnet" }`
- **Skill**: `{ "skill": "skill-name", "args": "optional arguments" }`

**Web:**
- **WebSearch**: `{ "query": "search terms", "allowed_domains": ["..."], "blocked_domains": ["..."] }`
- **WebFetch**: `{ "url": "https://...", "prompt": "what to extract" }`

**Task Management:**
- **TaskCreate**: `{ "subject": "Task title", "description": "Details", "activeForm": "Running task" }`
- **TaskUpdate**: `{ "taskId": "1", "status": "in_progress|completed|pending|deleted", "subject": "...", "addBlockedBy": ["2"] }`
- **TaskGet**: `{ "taskId": "1" }`
- **TaskList**: `{}` (no parameters)

**User Interaction:**
- **AskUserQuestion**: `{ "questions": [{ "question": "...", "header": "Label", "options": [{"label": "...", "description": "..."}], "multiSelect": false }] }`

## Exit Code Behavior

| Exit Code | Meaning | Effect |
|-----------|---------|--------|
| **0** | Success | JSON output processed, action proceeds |
| **2** | Blocking error | Block action, stderr shown to Claude |
| **Other** | Non-blocking | stderr in verbose mode, continue |

**Exit 2 Blocks**: PreToolUse, PermissionRequest, UserPromptSubmit, Stop, SubagentStop
**Exit 2 Cannot Block**: PostToolUse, PostToolUseFailure, Notification, SubagentStart, SessionStart, SessionEnd, PreCompact

## Output Patterns

### Universal Fields (All Hooks)
```json
{
  "continue": true,              // false stops Claude entirely
  "stopReason": "message",       // shown when continue=false
  "suppressOutput": false,       // hide from verbose mode
  "systemMessage": "warning"     // user warning message
}
```

### PreToolUse Decision
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow|deny|ask",
    "permissionDecisionReason": "explanation",
    "updatedInput": { "command": "modified command" },
    "additionalContext": "context for Claude"
  }
}
```

### PermissionRequest Decision
```json
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow|deny",
      "updatedInput": { "field": "value" },
      "message": "why denied",
      "interrupt": false
    }
  }
}
```

### Top-Level Decision (PostToolUse, PostToolUseFailure, UserPromptSubmit, Stop, SubagentStop)
```json
{
  "decision": "block",
  "reason": "explanation shown to Claude"
}
```

### Context Injection (SessionStart, UserPromptSubmit, SubagentStart, Notification, PostToolUse)
```json
{
  "hookSpecificOutput": {
    "hookEventName": "EventName",
    "additionalContext": "text added to Claude's context"
  }
}
```

## Hook Handler Types

| Type | Required Field | Default Timeout | Use For |
|------|----------------|-----------------|---------|
| **command** | `command` | 600s | Shell scripts, deterministic validation |
| **http** | `url` | 30s | Webhook integrations, external services |
| **prompt** | `prompt` | 30s | Single LLM evaluation |
| **agent** | `prompt` | 60s | Multi-turn LLM with tool access |

### Command Hook
```yaml
- type: command
  command: "$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py"
  timeout: 60
  async: false
  statusMessage: "Validating..."
  once: true  # Run only once per session (skills only)
```

### HTTP Hook
```yaml
- type: http
  url: "http://localhost:8080/hooks/pre-tool"
  headers:
    Authorization: "Bearer $MY_TOKEN"
  allowedEnvVars: ["MY_TOKEN"]
  timeout: 30
  statusMessage: "Calling webhook..."
```

### Prompt Hook
```yaml
- type: prompt
  prompt: "Evaluate if this action is safe. Context: $ARGUMENTS"
  model: haiku
  timeout: 30
```

### Agent Hook
```yaml
- type: agent
  prompt: "Verify tests pass after this change. $ARGUMENTS"
  model: sonnet
  timeout: 120
```

## Frontmatter vs Settings Placement

| Location | Scope | When to Use |
|----------|-------|-------------|
| Skill/Agent frontmatter | While component active | Component-specific hooks |
| `.claude/settings.json` | Project-wide | Team automation (commit to repo) |
| `.claude/settings.local.json` | Project-wide, local | Local overrides (.gitignored) |
| `~/.claude/settings.json` | All projects | Personal preferences |

### Frontmatter Hook Placement Rules

**Valid in Frontmatter (Tool + Agent Lifecycle)**:
- PreToolUse, PostToolUse, PostToolUseFailure, PermissionRequest
- SubagentStart, SubagentStop, Stop (becomes SubagentStop for subagents), Notification

**NOT Valid in Frontmatter (use settings.json)**:
- SessionStart, SessionEnd (session-level, not component-level)
- UserPromptSubmit, PreCompact (prompt-level)
- TeammateIdle, TaskCompleted, ConfigChange, WorktreeCreate, WorktreeRemove (system-level)

### Frontmatter YAML Structure
```yaml
---
name: artifact-name
description: Description
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/script.py"
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/validate.py"
  Stop:
    - hooks:
        - type: command
          command: "$CLAUDE_PROJECT_DIR/.claude/hooks/cleanup.py"
---
```

## Environment Variables

| Variable | Available In | Description |
|----------|--------------|-------------|
| `$CLAUDE_PROJECT_DIR` | All hooks | Project root directory |
| `$CLAUDE_PLUGIN_ROOT` | Plugin hooks | Plugin root directory |
| `$CLAUDE_ENV_FILE` | SessionStart hooks only | File to write export statements |
| `$ARGUMENTS` | Prompt/Agent hooks | Hook input JSON |
| `$CLAUDE_CODE_REMOTE` | All hooks | "true" if remote environment |
| `$CLAUDECODE` | Bash tool, All hooks | Always "1" when running in Claude Code |
| `$CLAUDE_CODE_ENTRYPOINT` | Bash tool, All hooks | "cli" or "ide" |

**Important:** `CLAUDE_ENV_FILE` is only available to **hooks**, not to the Bash tool. Child processes spawned by Claude cannot modify the parent session's environment. Use `CLAUDE_ENV_FILE` in SessionStart hooks to persist environment variables for the session.

## Matcher Patterns

- **Exact match**: `"Bash"`, `"Write"`
- **Regex OR**: `"Edit|Write"`, `"Bash|Task"`
- **MCP tools**: `"mcp__memory__.*"`, `"mcp__.*__write.*"`
- **Match all**: `"*"` or omit matcher
- **No matcher support**: UserPromptSubmit, Stop (always fire)

## Quick Decision Matrix

| I want to... | Use Event | Handler Type |
|--------------|-----------|--------------|
| Block dangerous commands | PreToolUse | command |
| Auto-approve permissions | PermissionRequest | command |
| Validate after file write | PostToolUse | command |
| Run tests after changes | PostToolUse | command (async) |
| Evaluate code quality | Stop | prompt/agent |
| Inject context on start | SessionStart | command |
| Cleanup on subagent finish | Stop (→SubagentStop) | command |
| Log tool usage | PostToolUse | command (async) |
| Notify external service | PostToolUse | http |
| React to config changes | ConfigChange | command |
| Track task completion | TaskCompleted | command |
| Worktree setup/teardown | WorktreeCreate/Remove | command |

## Hook Data Sources

Hooks have access to two complementary data sources for making decisions and gathering context.

### Two Data Sources

| Source | Type | Best For |
|--------|------|----------|
| **Hook Input JSON (stdin)** | Real-time event context | Current event details, immediate decisions |
| **~/.claude filesystem** | Persistent session metadata | Historical context, cross-referencing, state |

### Hook Input JSON (stdin)

Every hook receives JSON via stdin containing event context.

**Common Fields (all events)**:
```json
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/myproject/abc123.jsonl",
  "cwd": "/path/to/project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse"
}
```

**Event-Specific Fields**:

**PreToolUse** - Tool about to execute:
```json
{
  "tool_name": "Bash",
  "tool_input": { "command": "npm test", "description": "Run tests" },
  "tool_use_id": "toolu_abc123"
}
```

**PostToolUse** - Tool completed successfully:
```json
{
  "tool_name": "Write",
  "tool_input": { "file_path": "/src/app.ts", "content": "..." },
  "tool_response": { "success": true },
  "tool_use_id": "toolu_def456"
}
```

**UserPromptSubmit** - User submitted prompt:
```json
{
  "prompt": "Fix the authentication bug"
}
```

**SubagentStop** - Subagent finished:
```json
{
  "agent_id": "agent_xyz",
  "agent_type": "Explore",
  "agent_transcript_path": "/home/user/.claude/projects/myproject/agent_xyz.jsonl",
  "stop_hook_active": true
}
```

### ~/.claude Filesystem Paths

The `~/.claude` directory contains persistent session data hooks can read.

| Path | Contents | Use Case |
|------|----------|----------|
| `~/.claude/projects/{project}/{session}.jsonl` | Conversation transcript | Review conversation history, find past decisions |
| `~/.claude/projects/{project}/{session}/subagents/agent-{id}.jsonl` | Subagent tool call logs | Trace subagent execution, audit tool usage |
| `~/.claude/projects/{project}/sessions-index.json` | Session metadata index | Find sessions by summary, branch, timestamp |
| `~/.claude/tasks/{session}/*.json` | Task state and dependencies | Task management, dependency tracking |
| `~/.claude/file-history/{session}/{hash}@v{n}` | File version snapshots | Compare file versions, track changes |
| `~/.claude/debug/{session}.txt` | Debug logs | Troubleshooting, verbose logging |
| `~/.claude/history.jsonl` | Global command history | All CLI commands across all sessions |
| `~/.claude/todos/` | Agent task assignments | Cross-agent coordination |

**Note:** `{project}` is the encoded project path (e.g., `-home-user-myproject` for `/home/user/myproject`).

**Transcript Format** (JSONL - one JSON object per line):

Each line has a `type` field and nested `message` object:

```json
// User message
{
  "type": "user",
  "uuid": "a838b7cb-...",
  "timestamp": "2026-02-04T20:23:27.468Z",
  "message": {
    "role": "user",
    "content": "Fix the auth bug"
  }
}

// Assistant message with tool_use
{
  "type": "assistant",
  "uuid": "b207a6a8-...",
  "timestamp": "2026-02-04T20:23:34.185Z",
  "message": {
    "role": "assistant",
    "model": "claude-opus-4-5-20251101",
    "content": [
      {
        "type": "tool_use",
        "id": "toolu_01LAeePjLu84JuWEERGfm5NP",
        "name": "Bash",
        "input": { "command": "npm test", "description": "Run tests" }
      }
    ]
  }
}

// Tool result
{
  "type": "user",
  "uuid": "8cd067d9-...",
  "timestamp": "2026-02-04T20:23:35.213Z",
  "message": {
    "role": "user",
    "content": [
      {
        "type": "tool_result",
        "tool_use_id": "toolu_01LAeePjLu84JuWEERGfm5NP",
        "content": "All tests passed",
        "is_error": false
      }
    ]
  },
  "toolUseResult": {
    "stdout": "All tests passed",
    "stderr": "",
    "interrupted": false
  }
}
```

**Subagent Log Format** (`agent-{id}.jsonl`):
```json
{
  "agentId": "a33b7f7",
  "isSidechain": true,
  "sessionId": "0994e21d-...",
  "type": "assistant",
  "message": {
    "role": "assistant",
    "content": [
      {
        "type": "tool_use",
        "id": "toolu_012Xoh88WjNgjAHLXZwp3tv9",
        "name": "Bash",
        "input": { "command": "ls -la", "description": "List files" }
      }
    ]
  },
  "timestamp": "2026-01-12T15:08:09.100Z"
}
```

### Decision Guide: stdin vs Filesystem

| Need | Use | Why |
|------|-----|-----|
| Current event context | stdin | Direct access to tool_name, tool_input, etc. |
| Tool inputs/outputs for this call | stdin | Available in PreToolUse/PostToolUse |
| Making immediate allow/deny decision | stdin | All needed context in event payload |
| Conversation history | filesystem | Read transcript JSONL |
| Cross-referencing past decisions | filesystem | Search transcript for patterns |
| Persistent state across hooks | filesystem | Read/write to known paths |
| Task management | filesystem | Read `~/.claude/tasks/{session}/*.json` |
| File change history | filesystem | Compare versions in file-history |

### transcript_path Shortcut

The `transcript_path` field in hook input provides direct path to the current session transcript:

```python
#!/usr/bin/env python3
import json
import sys

hook_input = json.load(sys.stdin)
transcript_path = hook_input["transcript_path"]

# Read conversation history
with open(transcript_path, "r") as f:
    for line in f:
        entry = json.loads(line)
        # Process transcript entries...
```

This eliminates the need to construct paths manually - the exact location is provided in every hook invocation.
