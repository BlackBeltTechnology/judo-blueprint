## Why

Each catalog diagram was backed by a hand-built JUDO model, `fragments/<id>.model` (156 ESM XMI files). They are pinned to one ESM `metaVersion`, so every metamodel change breaks or forces a rewrite of all of them. They are invented models, so validating them proves nothing about real projects. The fragment gate starts one JVM per file and takes 10+ minutes. The original ask was descriptions plus Mermaid only.

## What Changes

- **BREAKING** Remove `fragments/`, the `fragment:` and `diagram:` frontmatter keys and the `<!-- mermaid:generated -->` markers. The existing Mermaid text stays unchanged as a plain ```mermaid block.
- Remove `judo-model-mermaid/scripts/check`, the fragment mode of `render`, the `fragments` gate of `check-all` (`--no-sandbox` goes away) and the CI sandbox job.
- `render --model <path> --scope <fqn>` stays: authors draw a diagram from the real project model and paste the Mermaid text, generalised.
- `entry-lint` rejects the retired keys; `spec-check` keeps checking Mermaid syntax.
- `tests/fixtures/Sandbox.model` stays as a scratch base for checking CLI claims; it is not catalog content.

## Capabilities

### New Capabilities

### Modified Capabilities
- `blueprint-sandbox-validation`: fragment requirements removed; only the pinned, untracked CLI remains.
- `blueprint-format`: structure diagrams are plain Mermaid; no fragment keys.
- `catalog-release-versioning`: release gates and notes no longer name Sandbox validation.
- `catalog-contribution-branches`: merge criteria no longer require CLI-built fragments.
- `catalog-kb-indexing`: `fragments/` no longer listed as non-catalog content.
- `catalog-collection-agents`: fragment authoring requirements removed; Mermaid rendering is for real models only.

## Impact

Catalog frontmatter of 360 entries and 157 diagram markers; `skills/judo-model-mermaid`, `skills/judo-blueprint-author`, `skills/judo-catalog-maintain`, `.pi/skills/judo-catalog-expand`, `.pi/agents/judo-sweep-author.md`, CI workflow, README, AGENTS.md.
