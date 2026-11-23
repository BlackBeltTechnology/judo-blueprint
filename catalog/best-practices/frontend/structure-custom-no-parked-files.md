---
id: structure-custom-no-parked-files
title: No Parked or Disabled Files in src/custom
description: Delete hook files you no longer use instead of renaming them to .notused or .old inside src/custom, and keep notes and prototypes out of the source folders, so that every committed file under src/custom is live code.
aliases: [parked hook files, disabled hook files, notused files, dead custom code]
keywords: [src/custom, .notused, .old, .default, dead code, implementation note, preview, prototype, version control]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: structure
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks"]
alternatives: []
related: [hook-scaffold-default-pattern, custom-component-directory, application-customizer-hub, structure-generator-ignore-scope]
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

A reader of `src/custom/` should be able to trust that every committed file there is active. Parked copies with ad-hoc suffixes break that trust and sit next to the generator's own `.default` scaffolds, which look similar but mean something else.

## Practice

### Platform base

- The generator emits hook scaffolds as `X.default` under `src/custom/hooks/...`; you activate one by copying it to `X`. The `.default` file is regenerated on every build as a reference and is gitignored ([.default scaffolds](../../agent-docs/frontend/development-workflow.md), [hook files and the custom folder](../../agent-docs/frontend/extension-points.md)).
- A hook takes effect only when it is registered from the application customizer ([[application-customizer-hub]]).

### Practice notes: deactivate in the customizer, delete the file

- To switch a hook off, remove its registration call from the customizer. If it stays off, delete the hook file; the version history keeps it.
- Never rename a hook to `X.ts.notused`, `X.tsx.old` or similar. Such files are committed (the frontend `.gitignore` ignores only the `.default` scaffolds), are not type-checked, and rot silently while the generated types change.
- Never commit an edited copy under the `.default` name: that suffix belongs to the generator.
- Keep design notes out of the hook folders. One module-level `README` or `AGENTS.md` that lists the hand-written files is easier to keep current than notes scattered between hook files.
- Keep throw-away UI prototypes (a standalone HTML page plus component used to preview a widget) in a folder outside `src/`, or delete them after the feature lands.

## Rationale

`.default` is a generator convention with a precise meaning: "reference, not active". Ad-hoc suffixes imitate it without the guarantees: they are tracked, never regenerated and never compiled. After a model change, nothing tells you that a parked file no longer matches the generated API, so reviving it later costs more than rewriting it from the fresh `.default`.

## Example

- One frontend had several `.notused` hook files in `hooks/dialogs/` and `hooks/pages/`, one `.tsx.old` custom implementation in `hooks/custom-implementations/`, and an `IMPLEMENTATION_NOTE.md` in `hooks/containers/` that describes a placeholder hook waiting for a model change.
- One frontend had a `preview/` folder at the module root that holds a standalone prototype page, its component and a rendered PNG.
- Positive case: `src/AGENTS.md` lists only the hand-written files of the module, one row each, with the change that introduced it.

## When to avoid

- A hook is disabled only for one short-lived branch: removing the registration is enough; delete the file before merging if it stays unused.

## Related

- [[hook-scaffold-default-pattern]] — the generator's `.default` convention
- [[custom-component-directory]] — what belongs in `src/custom/`
- [[application-customizer-hub]] — where hooks are switched on and off
- [[structure-generator-ignore-scope]] — the other file that tends to collect stale entries
