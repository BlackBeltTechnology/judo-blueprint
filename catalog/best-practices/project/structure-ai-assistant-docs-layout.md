---
id: structure-ai-assistant-docs-layout
title: AI Assistant Docs and Specs Layout
description: "One root AGENTS.md as the assistant entry point with tool-specific files only pointing to it, generated agent-docs left untouched, project facts in project-owned docs, and specs with their change history in one spec folder."
aliases: [AGENTS.md layout, CLAUDE.md pointer, agent docs location, spec folder, project brief]
keywords: [AGENTS.md, CLAUDE.md, agent-docs, openspec, specs, changes, archive, project brief, per-directory AGENTS.md, ADR]
tags: ["domain:project", "layer:backend", "project:rackinspect", "project:park-here", "project:mlszksz-platform", "status:emerging"]
category: structure
status: emerging
projects: [rackinspect, park-here, mlszksz-platform]
evidence: ["rackinspect:AGENTS.md", "rackinspect:CLAUDE.md", "rackinspect:openspec/", "park-here:src/AGENTS.md", "park-here:src/openspec/", "mlszksz-platform:CLAUDE.md", "mlszksz-platform:openspec/"]
alternatives: []
fragment: "none: infrastructure"
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

AI assistants need one place to start, one source for platform facts, one place for project facts and one place for specs. Projects that scatter these across several entry files, forked doc trees and parallel spec systems end up with stale and contradictory instructions.

## Practice

### Platform base

The project template generates `AGENTS.md` at the root and the platform agent-docs from Handlebars templates ([creating a new project](../../agent-docs/deployment/build-process.md#creating-a-new-project-from-the-esm-fullstack-template), [agent-docs placeholders](../../agent-docs/deployment/build-process.md#template-agent-docs-placeholders)). The agent-docs are organised by domain (`backend/`, `frontend/`, `model/`, `domain/`, `deployment/`, `integration-testing/`, `e2e-testing/`) ([technical documentation](../../agent-docs/README.md)). Whether a template update or regeneration overwrites a hand-edited root `AGENTS.md` or agent-docs file: *verify*.

### One entry point, pointers for each tool

- `AGENTS.md` at the root is the single entry point: project identity (app name, model path, Java package), hard rules, where things live, and pointers. No per-file index in the root file.
- A tool that reads its own file name gets a one-line pointer, not a copy. A `CLAUDE.md` that contains only an include of `./AGENTS.md` is enough.
- Optional: a short project brief (what the app is, stack, repository map, critical rules) for session bootstrap. Keep it small and dated; it goes stale fastest.
- Large projects add `AGENTS.md` per directory as the per-file record (purpose of each file), and a sidecar `AGENTS.md` next to a file that needs a warning (for example a locally modified IDE project file).

### Platform docs vs project docs

- Treat the generated agent-docs as platform-owned. Do not add project facts to them: One project committed an ADR and a tooling note into `agent-docs/model/` while the rest of the folder was ignored, so the folder became half generated, half project.
- Project knowledge goes to `docs/` (ADRs in `docs/adr/`, plans in `docs/planning/`) or to the spec folder. If the team maintains an improved copy of the platform docs, name one copy the source of truth in `AGENTS.md` and ignore or delete the other.

### One spec folder with history

- Keep specs and change proposals in one folder, for example `openspec/` with `specs/` (current behaviour by capability), `changes/` (open proposals) and `changes/archive/` (done).
- Put authoring rules for specs and tasks in the tool's config file (for example, `openspec/config.yaml` can require one test task per spec scenario).
- Replace boilerplate in the spec tool's project file: a copied `openspec/project.md` can still name a different project.
- When a spec system is retired, keep its folder read-only for history and say so in `AGENTS.md`; do not run two systems at once.

## Rationale

- One entry file means one place to update rules; pointer files cannot drift.
- Separating generated platform docs from project docs keeps template updates safe and shows which statements are platform facts.
- Archived changes give the fastest route to why the model and code look the way they do.
- Cost: the root `AGENTS.md` needs a size budget and regular pruning, and a project brief needs a refresh date.

## Example

- One project: root `AGENTS.md` (entry point, critical rules, pointer to the per-directory doc tree), `CLAUDE.md` as a one-line include, `PROJECT_BRIEF.md`, `openspec/` with many specs and archived changes, the retired spec system's folder kept as history only.
- Another project: root `AGENTS.md` as a universal entry point, generated `agent-docs/` not ignored, `openspec/` with `changes/`, `specs/` and `notes/`.
- A project whose entry point lives in `CLAUDE.md` (no `AGENTS.md`), generated agent-docs listed in `.gitignore`, `openspec/` with `CHANGELOG`, `archive/`, `changes/` and `specs/`.

## When to avoid

- A small project without AI-assisted work needs only the generated `AGENTS.md` and `README.adoc`; skip the brief and the per-directory tree.

## Related

- [[structure-repository-root-layout]] — the rest of the root layout
- [[generator-ignore-config-protection]] — protecting hand-edited generated files
