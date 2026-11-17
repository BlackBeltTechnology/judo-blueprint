---
name: judo-blueprint-author
description: Write or update ONE judo-blueprint catalog entry (model blueprint or best practice) in the kb format, including its Mermaid structure diagram. Use when creating a new entry or rewriting a legacy one.
---

# judo-blueprint-author

One job: produce one catalog entry that passes `entry-lint` and `spec-check`.

Paths below are relative to the judo-blueprint repository root (the folder
holding `catalog/` and `skills/`).

## Read first

- [references/format.md](references/format.md): the exact entry shape (frontmatter,
  sections, forbidden content).
- [../judo-model-mermaid/SKILL.md](../judo-model-mermaid/SKILL.md):
  how to draw the structure diagram from a real model.
- Layer guidance: [references/model.md](references/model.md),
  [references/backend.md](references/backend.md), [references/frontend.md](references/frontend.md).

## Flow

1. **Inputs.** The current entry (legacy or new) plus, for legacy entries,
   the pre-restructure version:
   `git show archive/pre-kb-restructure:model-blueprints/<id>/model.md`
   (or `best-practices/<domain>/<id>.md`). It contains the old GraphQL
   that describes the shape; use it only as input.
2. **Search before writing.** Use the `kb_search` / `kb_get` tools (never the
   `kb` CLI from an agent: parallel CLI processes lock the index) for the
   topic: related entries, agent-docs facts, and known problems in
   `openspec/changes/archive/2026-11-16-restructure-blueprints-for-kb/judo-doc-problems.md`.
   Never copy a platform claim the docs mark as wrong.
3. **Write the text** in the format: abstract sections, layer files, neutral
   wording, wikilinks in `## Related`.
4. **Structure diagram** (model shapes only): render the pattern's scope from
   the real project model with `skills/judo-model-mermaid/scripts/render --model <path> --scope <fqn>`
   (or write it by hand), paste it as a plain ```mermaid block under
   `## Structure diagram`, and generalise the names.
5. **Lint:** `skills/judo-blueprint-author/scripts/entry-lint <entry path>` and
   `skills/judo-blueprint-author/scripts/spec-check <entry path>`.
   `entry-lint` rejects `format: legacy` and the retired `fragment:`/`diagram:` keys.

## Rules

- Never commit model files (`.model`) to this repo.
- Never put CLI commands, GraphQL or `judo.sh` commands in `catalog/`.
- Neutral element names in diagrams. Project names only in `projects:`,
  `evidence:` and `project:` tags.
- Do not run git commands that change history (commit, reset, checkout).
