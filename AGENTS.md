# judo-blueprint

## Project Overview

The JUDO catalog (platform agent-docs, model blueprints, best practices) as a kb source, plus pi skills to use, diagram and author it. Consumers index only `catalog/`.

## Repo map

| Path | What |
|---|---|
| `catalog/agent-docs/` | Platform behaviour and rules. Source of truth for platform facts |
| `catalog/model-blueprints/<id>/` | `BLUEPRINT.md`, `model.md` (Mermaid diagram), `backend.md`, `frontend.md` |
| `catalog/best-practices/<domain>/<id>.md` | Practices for model, backend, frontend, project (repository layout) |
| `skills/` | `judo-blueprint`, `judo-model-mermaid`, `judo-blueprint-author`, `judo-catalog-maintain`, `judo-session-distill`, shared `_lib` |
| `openspec/specs/` | Main specs (8 capabilities) |
| `openspec/changes/archive/2026-11-16-restructure-blueprints-for-kb/` | The archived restructure change: proposal, design, `tasks.md` (follow-ups at the end), sweep and gap records |
| `.pi/skills/judo-catalog-expand/` | Maintainer workflows that grow the catalog with background agents (gap analysis, compliance, evidence, generic wording); not indexed by kb |
| `.pi/skills/judo-catalog-maintain/references/PROJECTS.md` | Registry of source projects (swept SHA, weight); maintenance data, not indexed by kb |
| `target/` | Ignored: CLI jar, scratch models, batch work folders, read-only judo-ng clones |

## Gates

Run `skills/judo-catalog-maintain/scripts/check-all` before committing catalog changes. It must pass. After adding or renaming catalog files, run `skills/judo-blueprint-author/scripts/dox-agents` to regenerate the `AGENTS.md` indexes.

## Hard rules

- **Origin is read-only in this maintainer clone.** Never push, merge, tag or release on `origin` from here; a local `pre-push` hook enforces it. Contributors push only their own `project/<project-id>` branch (see `skills/judo-blueprint/references/contribute.md`); `develop`, `master` and tags are changed only by the maintainer, after `branch-review` and the merge criteria.
- **judo-ng is read-only.** The clones under `target/` are references; fixes go only into local docs in this repo.
- No model files in this repo: diagrams are plain Mermaid (`judo-model-mermaid` renders them from real models).
- Platform claims must be backed by `catalog/agent-docs`; otherwise write *verify*.

## Writing Instructions

- Lead with the answer, then the detail. One idea per section, descriptive headings.
- Plain, direct language. Present tense, active voice. Consistent terms.
- Concrete examples, commands and paths over abstraction. Code samples minimal and runnable.
- Surgical edits: change only what the request needs; note adjacent issues instead of rewriting them.
- Read the edited section end to end and check every link, path and command you touched.

## Diagrams

Use Mermaid (```mermaid blocks) for diagrams, not ASCII art.
