---
name: "add-best-practice"
description: "Add a single best practice by describing it and linking to a GitHub project or file where it occurs"
argument-hint: "<description> <github-url>"
user-invocable: true
allowed-tools:
  - Task(judo-model-analyzer, judo-backend-analyzer, judo-frontend-analyzer)
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
---

Add a single best practice to the catalog by describing the pattern and linking to a GitHub project or file where it occurs. The command auto-detects the domain (model/backend/frontend) from the URL, confirms with the user, then launches the appropriate domain-specific analyzer agent.

## Command-Specific Task Initialization

Create the following tasks before starting work:

1. **Task: Parse input and resolve source**
   - `subject`: "Parse input and resolve source"
   - `description`: "Extract the best-practice description and GitHub URL from arguments. Clone the project to /tmp if needed."
   - `activeForm`: "Parsing input and resolving source"

2. **Task: Detect and confirm domain**
   - `subject`: "Detect and confirm domain"
   - `description`: "Auto-detect the domain (model/backend/frontend) from the file path or URL, then confirm with the user."
   - `activeForm`: "Detecting domain"

3. **Task: Collect best practice**
   - `subject`: "Collect best practice"
   - `description`: "Launch the domain-specific analyzer agent with focused instructions to find and document the described pattern."
   - `activeForm`: "Collecting best practice"

4. **Task: Cleanup and report**
   - `subject`: "Cleanup and report"
   - `description`: "Remove cloned repo if applicable, display summary of what was collected."
   - `activeForm`: "Cleaning up"

---

## Usage

**Syntax:**
```
/add-best-practice <description> <github-url>
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `description` | A natural language description of the best practice to look for |
| `github-url` | A GitHub URL — can be a repo URL, a file URL, or a directory URL |

**URL formats accepted:**
- Repo: `https://github.com/org/repo`
- File: `https://github.com/org/repo/blob/main/path/to/File.java`
- Directory: `https://github.com/org/repo/tree/main/path/to/dir`

**Examples:**
```
/add-best-practice "Toggle boolean operation pattern" https://github.com/org/project/blob/main/custom/ToggleActiveCustomImpl.java
/add-best-practice "Custom landing page with authentication" https://github.com/org/project/tree/main/frontend-react/src/custom
/add-best-practice "Singleton entity for global settings" https://github.com/org/project
```

---

## Orchestrator Instructions

When this command is invoked, follow these steps:

### Step 1: Parse Input and Resolve Source

#### 1a. Parse Arguments

Extract the two parts from the command arguments:
- **Description**: The natural language text describing the best practice
- **GitHub URL**: The URL pointing to the project, file, or directory

If the arguments are ambiguous, ask the user to clarify which part is the description and which is the URL.

If either is missing, ask the user:
- Missing description → "What best practice should I look for?"
- Missing URL → "Which GitHub project or file contains this pattern?"

#### 1b. Parse the GitHub URL

Extract from the URL:
- **Owner/Repo**: e.g., `org/project`
- **Branch** (if present): e.g., `main`
- **File path** (if present): e.g., `custom/ToggleActiveCustomImpl.java`

Use this regex-style breakdown:
```
https://github.com/{owner}/{repo}[/blob|tree/{branch}/{path}]
```

#### 1c. Clone the Project

```bash
mkdir -p /tmp/judo-projects/
```

Clone the repo (shallow, fast):
```bash
git clone --depth 1 https://github.com/{owner}/{repo}.git /tmp/judo-projects/{repo}/
```

If the clone fails (private repo, network), inform the user and stop.

#### 1d. Find the Model File

```bash
find /tmp/judo-projects/{repo}/ -name "*.model" -type f 2>/dev/null | head -1
```

Store the model file path for the agent prompt. If no `.model` file exists, note this — agents handle it gracefully.

### Step 2: Detect and Confirm Domain

#### 2a. Auto-Detect Domain

Use the file path from the URL (or scan the project) to infer the domain:

| Signal | Domain |
|--------|--------|
| Path contains `*.model`, `*.jsl`, `*.esm`, or points to `model/` directory | **model** |
| Path contains `*.java`, points to `custom/` with Java files, `interceptor`, `backend` in path | **backend** |
| Path contains `*.tsx`, `*.ts`, `*.jsx`, `*.css`, `theme/`, `layout/`, `frontend` in path, `*.dart` | **frontend** |

If the URL points to a **repo root** (no file path), scan the project to see what's available:
```bash
# Check what domains exist
ls /tmp/judo-projects/{repo}/model/*.model 2>/dev/null && echo "MODEL_EXISTS"
find /tmp/judo-projects/{repo} -path "*/custom/*.java" -type f 2>/dev/null | head -1 && echo "BACKEND_EXISTS"
find /tmp/judo-projects/{repo} -path "*/frontend*" -type d 2>/dev/null | head -1 && echo "FRONTEND_EXISTS"
```

If detection is ambiguous or the URL points to the repo root, default to asking.

#### 2b. Confirm with User

Present the detected domain for confirmation using AskUserQuestion:

"I detected this as a **{domain}** pattern. Is that correct?"

Options:
1. **model** — Entity/transfer/enum patterns in the .model layer
2. **backend** — Java implementation patterns (operations, interceptors, services)
3. **frontend** — React/Flutter UI patterns (hooks, themes, components)

### Step 3: Collect Best Practice

#### 3a. Prepare Focused Prompt

Build a targeted prompt for the analyzer agent that includes:
- The user's **description** of the pattern to look for
- The **project path** on disk
- The **model file path** (if found)
- The **specific file/directory** from the URL (if applicable) — so the agent starts there

#### 3b. Launch the Analyzer Agent

Based on the confirmed domain, launch ONE agent using the Task tool:

**For model domain:**
- `subagent_type`: `judo-model-analyzer`
- `description`: "Add best practice: {short-description}"
- `prompt`: Build as follows:

```
Analyze project **{repo}** to find and document this specific best practice:

> {user's description}

Project path: `/tmp/judo-projects/{repo}/`
Model file: `{model-path}`
{If specific file: "Start by examining this file: `{file-path}`"}

Read existing best practices from best-practices/model/ first. Then analyze the project source focusing on the described pattern. Create or update the best practice in best-practices/model/. Keep examples concise (3-5 lines). Report what you found.
```

**For backend domain:**
- `subagent_type`: `judo-backend-analyzer`
- `description`: "Add best practice: {short-description}"
- `prompt`: Build as follows:

```
Analyze project **{repo}** to find and document this specific best practice:

> {user's description}

Project path: `/tmp/judo-projects/{repo}/`
Model file: `{model-path}`
{If specific file: "Start by examining this file: `{file-path}`"}

Read existing best practices from best-practices/backend/ first. Then scan the project focusing on the described pattern. Create or update the best practice in best-practices/backend/. Keep examples concise (3-5 lines). Report what you found.
```

**For frontend domain:**
- `subagent_type`: `judo-frontend-analyzer`
- `description`: "Add best practice: {short-description}"
- `prompt`: Build as follows:

```
Analyze project **{repo}** to find and document this specific best practice:

> {user's description}

Project path: `/tmp/judo-projects/{repo}/`
Model file: `{model-path}`
{If specific file: "Start by examining this file: `{file-path}`"}

Read existing best practices from best-practices/frontend/ first. Then scan the project focusing on the described pattern. Create or update the best practice in best-practices/frontend/. Keep examples concise (3-5 lines). Report what you found.
```

#### 3c. Wait for Agent

Wait for the agent to complete using TaskOutput with `block: true`.

### Step 4: Cleanup and Report

#### 4a. Cleanup

Remove the cloned project:
```bash
rm -rf /tmp/judo-projects/{repo}/
```

#### 4b. Report

Display a summary to the user:
- Pattern description
- Domain (model/backend/frontend)
- Source project
- Best-practice file(s) created or updated
- Suggestion: "Run `/collect-best-practices` to re-score all patterns" if scoring is desired

---

## Notes

- This command is the **single-pattern complement** to `/collect-best-practices` (which batch-processes all projects)
- Only ONE analyzer agent is launched per invocation (not all three)
- The agent receives a **focused prompt** with the user's description, so it knows exactly what to look for
- If a specific file URL is given, the agent starts by examining that file
- The same analyzer agents and best-practice file format are used as in `/collect-best-practices` — patterns are fully compatible
- Cloned repos go to `/tmp/judo-projects/` and are cleaned up after the agent finishes
- No changes are made to `best-practices/PROGRESS.md` — this command is for ad-hoc additions, not tracked batch runs
