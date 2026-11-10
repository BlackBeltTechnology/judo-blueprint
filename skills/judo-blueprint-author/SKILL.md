---
name: judo-blueprint-author
description: Write or update ONE judo-blueprint catalog entry (model blueprint or best practice) in the kb format, including its CLI-built fragment and generated Mermaid diagram. Use when creating a new entry or rewriting a legacy one.
---

# judo-blueprint-author

One job: produce one catalog entry that passes `entry-lint` and, for model
shapes, `judo-model-mermaid/scripts/check`.

Paths below are relative to the judo-blueprint repository root (the folder
holding `catalog/`, `skills/`, `fragments/`).

## Read first

- [references/format.md](references/format.md): the exact entry shape (frontmatter,
  sections, forbidden content).
- [../judo-model-mermaid/references/fragments.md](../judo-model-mermaid/references/fragments.md):
  how to build a fragment with the CLI.
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
   `openspec/changes/restructure-blueprints-for-kb/judo-doc-problems.md`.
   Never copy a platform claim the docs mark as wrong.
3. **Write the text** in the format: abstract sections, layer files, neutral
   wording, wikilinks in `## Related`.
4. **Fragment** (model shapes only): scratch dir, copy
   `tests/fixtures/Sandbox.model`, build `Sandbox::bp::<pkg>` with CLI
   commands, `validate --strict`, `save`, copy to `fragments/<id>.model`,
   then stop the CLI server for that model
   (`java -jar target/judo-cli.jar -m <scratch>/Sandbox.model server stop`).
5. **Render and check:** `skills/judo-model-mermaid/scripts/render <id>` then
   `skills/judo-model-mermaid/scripts/check <id>`.
6. **Lint:** `skills/judo-blueprint-author/scripts/entry-lint <entry path>`.
   `entry-lint` rejects `format: legacy` and `fragment: pending`; every entry must pass all rules.

## Rules

- Never edit a `.model` file or a generated Mermaid block by hand.
- Never put CLI commands, GraphQL or `judo.sh` commands in `catalog/`.
- Neutral element names in fragments. Project names only in `projects:`,
  `evidence:` and `project:` tags.
- Do not run git commands that change history (commit, reset, checkout).
