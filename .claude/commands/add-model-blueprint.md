---
name: "add-model-blueprint"
description: "Add a single model blueprint by describing it and linking to a GitHub project where it occurs"
argument-hint: "<description> <github-url>"
user-invocable: true
allowed-tools:
  - Task(judo-model-blueprint-analyzer, judo-backend-blueprint-analyzer, judo-frontend-blueprint-analyzer)
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

Add a single blueprint to the catalog by describing the structural fragment or implementation pattern and linking to a GitHub project or file where it occurs. The command clones the project and:

- **For model fragments**: Uses CLI queries to survey the model and identify the described fragment, then generates detection queries and creation mutations. Optionally runs backend/frontend analysis too.
- **For implementation-only patterns**: Skips the model analyzer entirely and runs backend/frontend analyzers in discovery mode to catalog the described custom implementation pattern (e.g., external service integrations, custom hook systems, cross-cutting interceptors).

## Command-Specific Task Initialization

Create the following tasks before starting work:

1. **Task: Parse input and clone project**
   - `subject`: "Parse input and clone project"
   - `description`: "Extract the blueprint description and GitHub URL from arguments. Clone the project to /tmp. Determine if this is a model fragment or implementation-only pattern."
   - `activeForm`: "Parsing input and cloning project"

2. **Task: Find model file and determine mode**
   - `subject`: "Find model file and determine mode"
   - `description`: "Locate the .model file in the cloned project. Determine if this is model-based or implementation-only. If no model file or user describes a custom implementation pattern, use impl-only mode."
   - `activeForm`: "Determining analysis mode"

3. **Task: Collect blueprint**
   - `subject`: "Collect blueprint"
   - `description`: "For model fragments: launch model blueprint analyzer. For impl-only: launch backend/frontend analyzers in discovery mode."
   - `activeForm`: "Collecting blueprint"

4. **Task: Validate blueprint mutations (model-based only)**
   - `subject`: "Validate blueprint mutations"
   - `description`: "Run test-blueprint-mutations.sh --blueprint <id> to validate the new blueprint's mutations against Sandbox. Skip for impl-only blueprints."
   - `activeForm`: "Validating mutations"

5. **Task: Cleanup and report**
   - `subject`: "Cleanup and report"
   - `description`: "Remove cloned repo, display summary of blueprint collected including mutations generated."
   - `activeForm`: "Cleaning up"

---

## Usage

**Syntax:**
```
/add-model-blueprint <description> <github-url>
```

**Arguments:**
| Argument | Description |
|----------|-------------|
| `description` | A natural language description of the model structural fragment to look for |
| `github-url` | A GitHub URL — can be a repo URL, a file URL, or a directory URL |

**URL formats accepted:**
- Repo: `https://github.com/org/repo`
- File: `https://github.com/org/repo/blob/main/model/Project.model`
- Directory: `https://github.com/org/repo/tree/main/model`

**Examples:**
```
# Model-based blueprints (entity/enum/TO fragments)
/add-model-blueprint "Audit log entity with timestamp, action type enum, and user relation" https://github.com/org/project
/add-model-blueprint "Address entity cluster with street, city, postal code, country fields" https://github.com/org/project/blob/main/model/Project.model
/add-model-blueprint "Status enum with ACTIVE/INACTIVE/DELETED members and toggleActive operation" https://github.com/org/project

# Implementation-only blueprints (custom code patterns without model counterpart)
/add-model-blueprint "Keycloak realm integration with RealmManager OSGi service" https://github.com/org/project
/add-model-blueprint "Multi-tenancy context filtering via X-Judo-RequestParameters header" https://github.com/org/project
/add-model-blueprint "Custom dashboard component replacement with Pandino hook" https://github.com/org/project
/add-model-blueprint "Bulk JSON import/export custom operation pattern" https://github.com/org/project
```

---

## Orchestrator Instructions

When this command is invoked, follow these steps:

### Step 1: Parse Input and Clone Project

#### 1a. Parse Arguments

Extract the two parts from the command arguments:
- **Description**: The natural language text describing the model structural fragment
- **GitHub URL**: The URL pointing to the project, file, or directory

If the arguments are ambiguous, ask the user to clarify which part is the description and which is the URL.

If either is missing, ask the user:
- Missing description → "What model structural fragment should I look for?"
- Missing URL → "Which GitHub project contains this fragment?"

#### 1b. Parse the GitHub URL

Extract from the URL:
- **Owner/Repo**: e.g., `org/project`
- **Branch** (if present): e.g., `main`
- **File path** (if present): e.g., `model/Project.model`

Use this regex-style breakdown:
```
https://github.com/{owner}/{repo}[/blob|tree/{branch}/{path}]
```

#### 1c. Clone the Project

```bash
mkdir -p /tmp/judo-projects/
```

Clone the repo (shallow, full — backend/frontend code may be needed):
```bash
git clone --depth 1 https://github.com/{owner}/{repo}.git /tmp/judo-projects/{repo}/
```

If the clone fails (private repo, network), inform the user and stop.

### Step 2: Find Model File and Determine Mode

#### 2a. Find the Model File

```bash
find /tmp/judo-projects/{repo}/ -name "*.model" -type f 2>/dev/null | grep -v '\-esm\.model$' | head -5
```

Store the model file path. If the URL pointed to a specific `.model` file, use that directly.

#### 2b. Determine Analysis Mode

Decide between **model mode** and **impl-only mode** based on:

1. **User's description mentions custom implementation** — keywords like "custom operation", "interceptor", "hook", "Pandino", "OSGi service", "Keycloak", "integration module", "custom component", "axios interceptor", "theme", "multi-tenancy", "external API" → use **impl-only mode**
2. **No `.model` file found** → use **impl-only mode**
3. **`.model` file exists AND user describes a model fragment** (entity, enum, TO, operation) → use **model mode**

If ambiguous, ask the user:
**"This could be a model-level fragment or an implementation-only pattern. Should I search the model (entities/enums) or scan backend/frontend custom code?"**

#### 2c. Verify CLI Access (model mode only)

If in model mode, run a quick packages query to verify the model file is accessible:
```bash
java -jar $CLAUDE_PROJECT_DIR/.claude/judo-cli.jar -m <model-path> graphql -q 'esm { packages(limit: 5) { items { fqn name } totalCount } }' 2>/dev/null
```

If the CLI fails, fall back to **impl-only mode** and inform the user.

### Step 3: Collect Blueprint

#### Model Mode (model fragment described, .model file found)

##### 3a. Prepare Focused Prompt

Build a targeted prompt for the model blueprint analyzer agent that includes:
- The user's **description** of the structural fragment to look for
- The **project path** on disk
- The **model file path**
- The **specific file/directory** from the URL (if applicable) — so the agent starts there
- **Explicit instruction** to use CLI queries to survey relevant entities/enums/transfers and generate appropriate creation mutations

##### 3b. Launch the Model Blueprint Analyzer Agent

Launch the agent using the Task tool:

- `subagent_type`: `judo-model-blueprint-analyzer`
- `description`: "Add blueprint: {short-description}"
- `prompt`: Build as follows:

```
Analyze project **{repo}** to find and document this specific model structural fragment as a blueprint:

> {user's description}

Project path: `/tmp/judo-projects/{repo}/`
Model file: `{model-path}`
{If specific file: "The user pointed to this file: `{file-path}`"}

**Critical: Use CLI queries to determine the correct mutations.**

Follow this process:
1. Read existing model blueprints from model-blueprints/ first — check if this fragment already exists (use `query-catalog.py list --type blueprint`)
2. Use CLI queries to survey the model:
   - Query entity types to find the described structural pattern
   - Query enumeration types if the fragment involves enums
   - Query transfer object types if the fragment involves TOs
   - Query relations to understand how entities connect
3. From the query results, identify the exact attributes, relations, operations, and enums that make up this fragment
4. Write detection queries that match this fragment's characteristic shape
5. Generate creation mutations using the discovered attribute names, relation kinds, cardinalities, and enum members as the template
6. Create or update the blueprint directory in model-blueprints/<id>/ with:
   - BLUEPRINT.md: frontmatter + description + Model Definition link to model.md
   - model.md: detection query + creation mutations + concrete example from this project

The mutations should use `{{PLACEHOLDER}}` template variables for namespace and entity names while preserving the discovered structural details (attribute names, relation kinds, cardinalities, enum member names). Report what you found including the blueprint ID.
```

##### 3c. Wait for Agent

Wait for the agent to complete using TaskOutput with `block: true`.

---

#### Implementation-Only Mode (custom implementation pattern, no model counterpart)

##### 3a-impl. Launch Backend and/or Frontend Analyzers

Based on the user's description, determine whether to launch backend, frontend, or both agents:
- **Backend keywords**: custom operation, interceptor, OSGi, service layer, DAO, Java, Keycloak, external API, integration module → launch backend agent
- **Frontend keywords**: hook, Pandino, component, theme, layout, i18n, axios, custom component, dashboard → launch frontend agent
- **Both or ambiguous** → launch both

Launch the appropriate agent(s) using the Task tool with `run_in_background: false`:

**Backend agent (if applicable):**
- `subagent_type`: `judo-backend-blueprint-analyzer`
- `description`: "Discover impl blueprint: {short-description}"
- `prompt`:
```
Analyze project **{repo}** to find and document this specific implementation pattern as a blueprint:

> {user's description}

Project path: `/tmp/judo-projects/{repo}/`
Model file: none (this is an implementation-only pattern)
Blueprint IDs to analyze: none

**Run Phase 0 (Discovery Scan) with a SPECIFIC FOCUS on the described pattern.** Search the project's backend code for the described custom implementation. Create a new impl-only blueprint (with `impl_only: true` in BLUEPRINT.md frontmatter) for the discovered pattern. Do NOT create model.md.

{If specific file: "The user pointed to this file: `{file-path}` — start your search there."}

Report what you found including the new blueprint ID.
```

**Frontend agent (if applicable):**
- `subagent_type`: `judo-frontend-blueprint-analyzer`
- `description`: "Discover impl blueprint: {short-description}"
- `prompt`:
```
Analyze project **{repo}** to find and document this specific implementation pattern as a blueprint:

> {user's description}

Project path: `/tmp/judo-projects/{repo}/`
Model file: none (this is an implementation-only pattern)
Blueprint IDs to analyze: none

**Run Phase 0 (Discovery Scan) with a SPECIFIC FOCUS on the described pattern.** Search the project's frontend code for the described custom implementation. Create a new impl-only blueprint (with `impl_only: true` in BLUEPRINT.md frontmatter) for the discovered pattern. Do NOT create model.md.

{If specific file: "The user pointed to this file: `{file-path}` — start your search there."}

Report what you found including the new blueprint ID.
```

##### 3b-impl. Wait for Agent(s)

Wait for the agent(s) to complete.

### Step 4: Validate Blueprint Mutations (Model Mode Only)

**Skip this step entirely for implementation-only blueprints** — they have no model.md and no mutations to validate.

For model-based blueprints, validate the newly created/updated blueprint's mutations against the Sandbox model:

```bash
$CLAUDE_PROJECT_DIR/tests/test-blueprint-mutations.sh --blueprint <new-blueprint-id>
```

- If the test **passes**: proceed to cleanup
- If the test **fails**: report the errors to the user with the specific mutation failures. Suggest fixes based on common issues (unquoted enum values, missing binding fields, wrong creation order). Do NOT auto-fix — the agent or user should fix the blueprint mutations.

### Step 5: Cleanup and Report

#### 5a. Ask About Backend/Frontend Analysis (Model Mode Only)

**Skip this step for implementation-only blueprints** — the backend/frontend agents already ran in Step 3.

For model-based blueprints, after the model blueprint is created, ask the user:

**"Also run backend/frontend analysis for this project on the new blueprint?"**

If yes:
- Launch both `judo-backend-blueprint-analyzer` and `judo-frontend-blueprint-analyzer` with `run_in_background: true`
- Provide the blueprint ID and project path
- **Include discovery mode instructions** in the prompt so agents also scan for impl-only patterns
- Wait for both to complete
- Report what was found

#### 5b. Cleanup

Remove the cloned project:
```bash
rm -rf /tmp/judo-projects/{repo}/
```

#### 5c. Report

Display a summary to the user:
- Fragment/pattern description
- Source project
- Blueprint directory created or updated (`model-blueprints/<id>/`)
- **Blueprint type**: model-based or implementation-only
- Files created: BLUEPRINT.md, and optionally model.md, backend.md, frontend.md
- Key mutations generated (model-based only — list the mutation types used)
- Suggestion: "Run `/collect-model-blueprints` to discover this fragment across all other projects and update its usage count"

---

## Notes

- This command is the **single-fragment complement** to `/collect-model-blueprints` (which batch-processes all projects)
- **Two modes**: model mode (uses `judo-model-blueprint-analyzer`) and impl-only mode (uses `judo-backend-blueprint-analyzer` / `judo-frontend-blueprint-analyzer` directly)
- For model-based blueprints: the agent uses **CLI queries** to discover the fragment's exact shape and generate matching mutations — it does NOT guess mutations from the description alone
- For impl-only blueprints: the backend/frontend agents scan custom code and create blueprints with `impl_only: true` — no model.md, no mutations
- The same blueprint directory format and catalog conventions are used as in `/collect-model-blueprints` — all blueprints are fully compatible
- Blueprints are stored as directories: `model-blueprints/<id>/` with `BLUEPRINT.md`, optionally `model.md`, `backend.md`, `frontend.md`
- Cloned repos go to `/tmp/judo-projects/` and are cleaned up after the agent finishes
- No changes are made to `model-blueprints/PROGRESS.md` — this command is for ad-hoc additions, not tracked batch runs
- If the described fragment already exists as a blueprint, the agent updates usage count and adds the new project as an example
