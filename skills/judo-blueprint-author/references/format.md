---
title: Catalog entry format
description: The exact shape of model blueprints and best practices in catalog/, the frontmatter keys, sections, fragment rules and what is forbidden.
---

# Catalog entry format

The catalog holds **knowledge only: descriptions and Mermaid**. Never GraphQL,
never CLI commands, never `judo.sh` commands, never recipes or step lists for
building model elements. Generic Java / TypeScript / JSX samples in layer
guidance are fine.

## Frontmatter (all entries)

kb parses frontmatter. Use single-line scalars and flow lists only: no `|` or
`>` block scalars, no multi-line lists.

```yaml
---
id: audit-log-entity
title: Audit Log Entity
description: One sentence that says what the entry is and when it applies (used by kb and AGENTS.md rows).
aliases: [audit trail, event log]
keywords: [audit, timestamp, immutable, history]
tags: [domain:model, layer:backend, project:mlszksz-platform, status:single-project]
category: entity
status: single-project
projects: [mlszksz-platform]
evidence: [mlszksz-platform:model/mlszksz.model]
alternatives: [audit-event-trail]
fragment: audit-log-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-09
---
```

- `status` is derived from the number of distinct `projects`: 1 → `single-project`,
  2–3 → `emerging`, 4+ → `established`. The `status:` tag must match.
- `score`, `usage_count`, `alternative_count` are **forbidden**.
- `alternatives` holds entry ids (each must exist in the catalog).
- `fragment`: the fragment id (= entry id) when the entry has a model shape;
  otherwise `none: <reason>` (`none: backend-only`, `none: frontend-only`,
  `none: infrastructure`). `pending` is only allowed together with
  `format: legacy`.
- `diagram` (optional): CLI render options, `kinds` from
  `entity, enum, transfer, actor, operation`, `members` from `types|names|none`.
- `tags`: `domain:<model|backend|frontend|...>`, `layer:<model|backend|frontend>`
  (one per layer file present), `project:<p>` per project, `status:<s>`.
- Dates are `YYYY-MM-DD`.

## Model blueprint: `catalog/model-blueprints/<id>/`

| File | Content |
|---|---|
| `BLUEPRINT.md` | frontmatter + abstract sections, in this order: `## Intent`, `## Structure`, `## Constraints`, `## Variations`, `## When to use`, `## When to avoid`, `## Related` |
| `model.md` | model-layer description: elements, attributes, relation kinds, cardinalities, transfer objects, access, UI pages the shape implies; plus the generated structure diagram |
| `backend.md` | backend layer guidance (custom operations, interceptors, services). Generic Java allowed |
| `frontend.md` | frontend layer guidance (generated pages to keep/hide/customize, hooks). Generic TS/TSX allowed |

Headings are descriptive: `## Intent`, then sub-headings that name the entry,
e.g. `### Audit log is append-only`. No section body longer than 4000
characters without a sub-heading (kb chunk size).

`Structure` describes the shape in prose: element names, attribute types,
relation kinds (composition / aggregation / association), cardinalities,
enumerations. It names **no tool**.

`model.md` starts with `## Model shape` (prose) and ends with
`## Structure diagram` holding the generated block (see below). Model-layer
guidance that belongs to the shape (derived members, access, transfer
objects, generated UI pages: which View/Form/Table pages to keep, hide or
customize) goes in between.

## Best practice: `catalog/best-practices/<domain>/<id>.md`

One file. `domain` is the folder (`model`, `backend`, `frontend`) and must
match the `domain:` tag. Sections in this order:
`## Intent`, `## Practice`, `## Rationale`, `## Example`, `## When to avoid`,
`## Related`.

A best practice with a model shape gets a fragment and a generated block
inside `## Example` (or a final `## Structure diagram`). Backend/frontend-only
practices declare `fragment: none: backend-only` / `none: frontend-only`.

## Related and links

`## Related` lists entries as `[[id]]` wikilinks with a short reason:
`- [[derived-attribute-flattening]] — compute on read instead`. Every id
must exist. Links into agent-docs use relative markdown links.

## Generated structure diagram (fragments)

```
<!-- mermaid:generated fragment=<id> cli=<version> -->
```mermaid
classDiagram
...
```
<!-- /mermaid:generated -->
```

- Never write or edit this block by hand. It is produced by
  `skills/judo-model-mermaid/scripts/render <id>` from `fragments/<id>.model`.
- `skills/judo-model-mermaid/scripts/check <id>` must pass
  (`validate --strict`, render equals block, no leaked classes).

## Fragments: `fragments/<id>.model`

A fragment is the Sandbox model (`tests/fixtures/Sandbox.model`) plus one
package `Sandbox::bp::<pkg>` where `<pkg>` = id with `-` → `_`. It holds the
entry's shape with **neutral names** (`Order`, `OrderLine`, `AuditLog`,
`Status`), never client domain names.

Build it only with the JUDO CLI in a scratch copy, then `save`:
see [fragments.md](../../judo-model-mermaid/references/fragments.md).
Never edit a `.model` file by hand, never commit the commands you used.

## Forbidden content (entry-lint rejects)

- ```` ```graphql ```` fences, `mutation {`, `query {` GraphQL blocks
- CLI invocations: `java -jar`, `judo-cli`, `judo_cli`, `create -t`, `--ns `,
  `mermaid model`, `validate --strict`, `./judo.sh`, `judo.sh build|start|generate`
- Handlebars outside code fences (`{{ … }}`); JSX like `sx={{ … }}` inside
  `tsx`/`jsx`/`ts` fences is fine
- `score:` / `usage_count:` / `alternative_count:` in frontmatter
- block scalars in frontmatter
- harness wording: `.claude/`, `SKILL.md`, `subagent`, `judospec`
- real user names, home paths (`/Users/…`), e-mails, secrets
