---
title: Building a catalog fragment with the JUDO CLI
description: How to build fragments/<id>.model in a scratch Sandbox copy with the JUDO model CLI, save it and render the entry diagram.
---

# Building a fragment

A fragment is model data written by the JUDO CLI. The commands you run are
never stored in the repository; only the saved `.model` file is.

## Rules

- Start from a fresh copy of `tests/fixtures/Sandbox.model` in a scratch
  directory (never inside `catalog/`). The model is named `Sandbox`; its
  primitive types live in `Sandbox::types` (`String`, `Integer`, `Decimal`,
  `Boolean`, `Date`, `Timestamp`, `Time`, `Text`, …: list them with
  `query esm Primitive --select name`).
- Create package `bp` in `Sandbox`, then `Sandbox::bp::<pkg>` (`<pkg>` = entry
  id with `-` replaced by `_`). Put every element of the shape inside it.
- Neutral names only (`Order`, `OrderLine`, `Customer`, `Status`).
- Use the CLI's own help, never a copied command list:
  - `<cli> --help`, `<cli> <command> --help`
  - `<cli> create -t <Type> --schema` lists the fields of an element type
    and the valid values; every error prints a `fix` line with the next command
  - the CLI's `judo-cli` skill docs in the judo-model-cli repository
- When the shape is complete: `validate --strict` must pass, then `save`.
- Copy the saved model to `fragments/<id>.model`, then run
  `skills/judo-model-mermaid/scripts/render <id>` and
  `skills/judo-model-mermaid/scripts/check <id>`.

`<cli>` is `java -jar $JUDO_CLI_JAR -m Sandbox.model` (or
`<repo>/target/judo-cli.jar`; download it with
`./mvnw -q validate -P download-model-cli`). Run each scratch Sandbox in its
own directory: the CLI keeps one server session per model file.

## Diagram options

`render` draws `mermaid model --scope Sandbox::bp::<pkg> --split none` plus the
entry's `diagram:` frontmatter (`kinds`, `members`). Defaults: kinds
`entity,enum`, members `types`. Add `transfer`, `actor` or `operation` to
`kinds` when the transfer objects, actors or operations are part of the shape.

## Common element types

`Package`, `EntityType`, `DataMember` (attribute; `memberType`
STORED/DERIVED/MAPPED/TRANSIENT), `OneWayRelationMember`,
`TwoWayRelationMember`, `EnumerationType`, `EnumerationMember`,
`TransferObjectType`, `Operation`, `ActorType`, `Access`. Get the exact fields
with `--schema` before creating.
