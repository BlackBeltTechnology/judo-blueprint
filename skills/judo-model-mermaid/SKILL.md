---
name: judo-model-mermaid
description: Draw a Mermaid diagram of a scope of a real JUDO model with the JUDO model CLI, read-only. Use when writing or updating the structure diagram of a catalog entry from a project's model, or to get an overview of your own model before analysis.
---

# judo-model-mermaid

Catalog diagrams are plain ```mermaid blocks. The catalog stores no model files: a diagram is text, so it stays valid when the ESM metamodel changes.

## Script

| Script | Does |
|---|---|
| `scripts/render --model <path> --scope <fqn> [--depth N] [--kinds k,..] [--members m]` | Prints the Mermaid diagram of that scope of the model. The model is not changed. |

It needs the JUDO CLI jar: `$JUDO_CLI_JAR`, else `target/judo-cli.jar` (`./mvnw validate -P download-model-cli`).

## Writing an entry's structure diagram

1. Render the pattern's scope from the real project model the entry's evidence points at.
2. Paste the output under `## Structure diagram` in `model.md` (blueprints) or the entry file (best practices).
3. Replace project and client names with neutral ones, and drop classes that are not part of the pattern.
4. Hand-written diagrams are fine when no model is at hand; keep them consistent with the entry's prose.
