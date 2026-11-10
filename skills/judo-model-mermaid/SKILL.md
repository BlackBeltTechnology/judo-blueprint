---
name: judo-model-mermaid
description: Render and check the Mermaid structure diagrams of JUDO catalog entries from their fragment models (fragments/<id>.model). Use when building or changing a blueprint's model shape, or when a diagram looks out of date.
---

# judo-model-mermaid

Every catalog entry with a model shape has a fragment: `fragments/<id>.model`, a small JUDO model built with the JUDO model CLI and validated with `validate --strict`. The entry's `model.md` holds a generated Mermaid diagram of that fragment between generated-block markers. Never edit inside the markers by hand.

## Scripts

| Script | Does |
|---|---|
| `scripts/render <id>` / `--all` | Writes the diagram of `fragments/<id>.model` into the entry. `--stdout` prints it instead. |
| `scripts/check <id>` / `--all` | Fails unless the fragment passes `validate --strict` and the diagram in the entry equals a fresh render. Also fails when an entry declares `fragment: <id>` with no fragment file. |

Both need the JUDO CLI jar: `$JUDO_CLI_JAR`, else `target/judo-cli.jar` (`./mvnw validate -P download-model-cli`).

## Building a fragment

See [references/fragments.md](references/fragments.md): a fresh `tests/fixtures/Sandbox.model` copy in a scratch directory, package `Sandbox::bp::<id_with_underscores>`, neutral names, `validate --strict`, `save`, copy to `fragments/<id>.model`, then `render` and `check`.
