# Claude Code Metadata Directory Structure

This document describes the metadata stored in `~/.claude` for Claude Code sessions, subagents, and related data.

## Directory Overview

| Directory | Purpose | Session/Subagent Metadata |
|-----------|---------|---------------------------|
| `agents/` | GSD subagent specifications | Subagent definitions |
| `cache/` | Cached data (changelog, updates) | - |
| `commands/` | GSD command workflows | Command orchestration specs |
| `debug/` | Debug logs per session | Session debug traces |
| `file-history/` | File version tracking | Per-session file snapshots |
| `get-shit-done/` | GSD framework templates | Workflow templates |
| `hooks/` | Session lifecycle hooks | Session start/status hooks |
| `paste-cache/` | Clipboard content cache | - |
| `plans/` | Active/archived plans | - |
| `plugins/` | Plugin registry | - |
| `projects/` | Project session storage | **Primary session/subagent data** |
| `session-env/` | Session environment placeholders | Session UUIDs |
| `shell-snapshots/` | Shell state snapshots | Session shell environments |
| `skills/` | Custom skill definitions | - |
| `statsig/` | Feature flags/analytics | - |
| `tasks/` | Task management system | Task state per session |
| `telemetry/` | Failed telemetry events | - |
| `todos/` | Todo items per agent | Agent task assignments |

---

## Session Metadata

### Primary Session Storage: `projects/`

**Location:** `~/.claude/projects/{encoded-path}/`

Each project directory contains:

1. **`sessions-index.json`** - Index of all sessions
   ```json
   {
     "version": 1,
     "sessions": [{
       "sessionId": "UUID",
       "fullPath": "path/to/session.jsonl",
       "firstPrompt": "initial user message",
       "summary": "session summary",
       "messageCount": 42,
       "created": "ISO timestamp",
       "modified": "ISO timestamp",
       "gitBranch": "branch-name",
       "projectPath": "/absolute/path",
       "isSidechain": false
     }]
   }
   ```

2. **`{session-uuid}.jsonl`** - Session conversation history (JSONL format)
   - Each line is a message with: `type`, `role`, `content`, `timestamp`, `uuid`, `sessionId`, `cwd`, `gitBranch`
   - Message types: `user`, `assistant`, `progress`, `file-history-snapshot`

3. **`{session-uuid}/`** - Multi-agent session directory
   - `subagents/agent-{id}.jsonl` - Subagent conversation logs
   - `tool-results/toolu_{id}.txt` - Tool execution outputs

### Session Environment: `session-env/`

**Location:** `~/.claude/session-env/{session-uuid}/`

- Empty placeholder directories for each session UUID
- Links to data in `debug/`, `shell-snapshots/`, and `history.jsonl`

### Session Debug Logs: `debug/`

**Location:** `~/.claude/debug/{session-uuid}.txt`

- Detailed debug output per session
- Contains: startup logs, API auth, tool execution, LSP manager, errors
- `latest` symlink points to current session log

### Shell Snapshots: `shell-snapshots/`

**Location:** `~/.claude/shell-snapshots/snapshot-bash-{timestamp}-{id}.sh`

- Bash environment snapshots at session start
- Contains: functions, shell options, aliases, PATH, environment variables

### History Log: `history.jsonl`

**Location:** `~/.claude/history.jsonl`

- JSONL file with all session history entries
- Fields: `display`, `pastedContents`, `timestamp`, `project`, `sessionId`

---

## Subagent Metadata

### Agent Specifications: `agents/`

**Location:** `~/.claude/agents/{agent-name}.md`

YAML frontmatter + Markdown specification files:

```yaml
---
name: gsd-planner
description: Creates executable phase plans
tools: [Read, Write, Edit, Bash, Grep, Glob]
color: green
model: sonnet
---
```

**Available GSD Agents:**
| Agent | Purpose |
|-------|---------|
| `gsd-planner` | Creates phase plans with task breakdown |
| `gsd-executor` | Executes plans with atomic commits |
| `gsd-debugger` | Scientific debugging with state management |
| `gsd-verifier` | Goal-backward verification |
| `gsd-plan-checker` | Pre-execution plan quality gate |
| `gsd-codebase-mapper` | Documents codebase patterns |
| `gsd-phase-researcher` | Pre-planning phase research |
| `gsd-project-researcher` | Domain/ecosystem research |
| `gsd-roadmapper` | Creates project roadmaps |
| `gsd-research-synthesizer` | Synthesizes parallel research |
| `gsd-integration-checker` | Cross-phase integration verification |
| `doc-structure-explorer` | Documentation structure mapping |

### Subagent Conversation Logs

**Location:** `~/.claude/projects/{project}/subagents/agent-{id}.jsonl`

- JSONL format with `agentId` field
- Full conversation history for each spawned agent
- Linked to parent session via `parentUuid`

### Task Assignments: `todos/`

**Location:** `~/.claude/todos/{task-uuid}-agent-{agent-uuid}.json`

```json
[{
  "content": "Task description",
  "status": "pending|in_progress|completed",
  "activeForm": "Present continuous form for display"
}]
```

### Task Management: `tasks/`

**Location:** `~/.claude/tasks/{session-uuid}/{task-id}.json`

```json
{
  "id": "1",
  "subject": "Task title",
  "description": "Detailed description",
  "activeForm": "Running the task",
  "status": "pending|in_progress|completed",
  "blocks": ["2", "3"],
  "blockedBy": ["0"],
  "metadata": { "phase": 1 }
}
```

Supporting files:
- `.lock` - Concurrency control
- `.highwatermark` - Highest task ID assigned

---

## File Tracking

### File History: `file-history/`

**Location:** `~/.claude/file-history/{session-uuid}/{file-hash}@v{version}`

- Full file content at each version (not diffs)
- Version numbers increment per edit (v1, v2, v3...)
- Enables reverting to previous file states

---

## Configuration Files

### Settings: `settings.json`

```json
{
  "permissions": {
    "allow": ["Bash(pattern:*)"],
    "deny": ["Bash(git commit:*)"]
  },
  "hooks": {
    "SessionStart": [{ "type": "command", "command": "..." }]
  },
  "statusLine": { "type": "command", "command": "..." }
}
```

### Hooks: `hooks/`

- `gsd-check-update.js` - SessionStart hook for update checks
- `gsd-statusline.js` - Status line rendering with task display

---

## GSD Framework: `get-shit-done/`

### Templates (`templates/`)
- `PROJECT.md`, `ROADMAP.md`, `STATE.md` - Planning documents
- `phase-prompt.md`, `summary.md` - Execution documents
- `codebase/*.md` - Architecture/stack documentation templates

### References (`references/`)
- `planning-config.md`, `model-profiles.md` - Configuration guides
- `checkpoints.md`, `verification-patterns.md` - Quality assurance

### Workflows (`workflows/`)
- `execute-phase.md`, `execute-plan.md` - Execution orchestration
- `verify-phase.md`, `verify-work.md` - Verification workflows
- `resume-project.md`, `transition.md` - Session continuity

---

## Cache & Analytics

### Cache: `cache/`
- `changelog.md` - Claude Code release notes
- `gsd-update-check.json` - GSD version check results

### Paste Cache: `paste-cache/`
- `{hash}.txt` - Cached clipboard content by content hash

### Statsig: `statsig/`
- Feature flag evaluations and session IDs

### Telemetry: `telemetry/`
- Failed telemetry events (retry queue)

---

## Key Relationships

```
Session Flow:
┌─────────────────────────────────────────────────────────┐
│ session-env/{uuid}/  ←──────────────────────────────┐   │
│         │                                           │   │
│         ▼                                           │   │
│ projects/{project}/{uuid}.jsonl ◄─── Main session   │   │
│         │                                           │   │
│         ├── {uuid}/subagents/agent-{id}.jsonl       │   │
│         │         └── Subagent conversations        │   │
│         │                                           │   │
│         └── {uuid}/tool-results/toolu_{id}.txt      │   │
│                   └── Tool execution outputs        │   │
│                                                     │   │
│ debug/{uuid}.txt ◄─── Debug logs ───────────────────┤   │
│                                                     │   │
│ shell-snapshots/snapshot-bash-{ts}-{id}.sh          │   │
│         └── Shell environment at session start      │   │
│                                                     │   │
│ file-history/{uuid}/{hash}@v{n}                     │   │
│         └── File versions edited in session         │   │
│                                                     │   │
│ tasks/{uuid}/{id}.json                              │   │
│         └── Task state for session                  │   │
│                                                     │   │
│ todos/{task-uuid}-agent-{agent-uuid}.json           │   │
│         └── Agent task assignments                  │   │
└─────────────────────────────────────────────────────┘

Agent Specification:
┌─────────────────────────────────────────────────────────┐
│ agents/{name}.md ◄─── Agent definition                  │
│         │                                               │
│         ▼                                               │
│ commands/gsd/{cmd}.md ◄─── Command orchestration        │
│         │                                               │
│         ▼                                               │
│ get-shit-done/workflows/{workflow}.md                   │
│         │                                               │
│         ▼                                               │
│ get-shit-done/templates/{template}.md                   │
└─────────────────────────────────────────────────────────┘
```

---

## Size Summary

| Directory | Size | Files |
|-----------|------|-------|
| `projects/` | ~500 MB | Sessions + subagents |
| `debug/` | ~196 MB | 1,194 log files |
| `file-history/` | ~31 MB | 2,212 file versions |
| `history.jsonl` | ~665 KB | Command history |
| `todos/` | ~2.1 MB | 499 task files |
| `tasks/` | Variable | 69 task JSON files |
| `agents/` | ~260 KB | 12 agent specs |
| `get-shit-done/` | ~350 KB | Framework files |
