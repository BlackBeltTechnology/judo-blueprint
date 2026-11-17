---
title: Catalog entry format
description: The exact shape of model blueprints and best practices in catalog/, the frontmatter keys, sections, structure diagrams and what is forbidden.
---

# Catalog file format

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
first_seen: 2026-03-05
last_updated: 2026-11-09
---
```

- `status` is derived from the number of distinct `projects`: 1 → `single-project`,
  2–3 → `emerging`, 4+ → `established`. The `status:` tag must match.
- `score`, `usage_count`, `alternative_count` are **forbidden**.
- `alternatives` holds entry ids (each must exist in the catalog).
- `fragment` and `diagram` are retired: there are no fragment models (`entry-lint` rejects them).
- `tags`: `domain:<model|backend|frontend|project|...>` (`project` = repository-level layout), `layer:<model|backend|frontend>`
  (one per layer file present), `project:<p>` per project, `status:<s>`.
- Dates are `YYYY-MM-DD`.

## Model blueprint: `catalog/model-blueprints/<id>/`

| File | Content |
|---|---|
| `BLUEPRINT.md` | frontmatter + abstract sections, in this order: `## Intent`, `## Structure`, `## Constraints`, `## Variations`, `## When to use`, `## When to avoid`, `## Related` |
| `model.md` | model-layer description: elements, attributes, relation kinds, cardinalities, transfer objects, access, UI pages the shape implies; plus the structure diagram (plain Mermaid) |
| `backend.md` | backend layer guidance (custom operations, interceptors, services). Generic Java allowed |
| `frontend.md` | frontend layer guidance (generated pages to keep/hide/customize, hooks). Generic TS/TSX allowed |

Headings are descriptive: `## Intent`, then sub-headings that name the entry,
e.g. `### Audit log is append-only`. No section body longer than 4000
characters without a sub-heading (kb chunk size).

`Structure` describes the shape in prose: element names, attribute types,
relation kinds (composition / aggregation / association), cardinalities,
enumerations. It names **no tool**.

`model.md` starts with `## Model shape` (prose) and ends with
`## Structure diagram` holding a Mermaid block (see below). Model-layer
guidance that belongs to the shape (derived members, access, transfer
objects, generated UI pages: which View/Form/Table pages to keep, hide or
customize) goes in between.

## Best practice: `catalog/best-practices/<domain>/<id>.md`

One file. `domain` is the folder (`model`, `backend`, `frontend`, `project`) and must
match the `domain:` tag. Sections in this order:
`## Intent`, `## Practice`, `## Rationale`, `## Example`, `## When to avoid`,
`## Related`.

A best practice with a model shape gets a Mermaid structure diagram
inside `## Example` (or a final `## Structure diagram`).

## Agent-doc: `catalog/agent-docs/<area>/<name>.md`

Platform documentation, the source of truth for platform facts. Same kb contract as entries, without the entry-only keys.

```yaml
---
title: Operation Call Interceptors
description: One sentence naming the platform area and the questions the doc answers (used by kb and the AGENTS.md row).
aliases: [interceptor order, preCall postCall]         # phrases developers type
keywords: [OperationCallInterceptor, preCall, postCall] # identifiers in the doc: classes, annotations, keys, commands
tags: [domain:backend, layer:backend, status:platform]
---
```

- `domain:` is the area: `model`, `backend`, `frontend`, `deployment`, `testing` (integration and e2e). `layer:` is `model`, `backend`, `frontend`, `infrastructure` or `test`. `status:platform` marks a platform fact; no `project:` tags.
- New headings name their subject (`## Interceptor ordering`, not `## Overview`): kb returns the heading path as the hit. Existing headings and text are kept as written; format work only adds frontmatter, companions and sub-headings.
- No section body over 4000 characters without a sub-heading (kb chunk size).

## Companion: `<name>.agent.md` for large files

kb's contract (`kb dox lint`): any markdown file over **300 lines or 15000 bytes** has a companion next to it, `<name>.agent.md`, a pull-only condensed map that an agent reads before pulling one section with `kb_get`. It applies to agent-docs, entries and layer files alike.

```markdown
# interceptors.md — index

Pull-only condensed map. Source: catalog/agent-docs/backend/interceptors.md.

## Interceptor ordering
- preCall runs in registration order; postCall in reverse. `@Component(property = "operation=…")`.
```

- First line `# <name>.md — index`, then the `Source: <repo path>` line. No frontmatter.
- One `##` per `##` of the source, with the same heading text, so every section is reachable; terse bullets with the rules, identifiers and gotchas of that section. Nothing that is not in the source.
- At most 250 lines. Rewrite the companion whenever the source's `##` headings change (`entry-lint` checks coverage).
- The directory `AGENTS.md` lists the companion as "condensed map of `<name>.md`".

## Related and links

`## Related` lists entries as `[[id]]` wikilinks with a short reason:
`- [[derived-attribute-flattening]] — compute on read instead`. Every id
must exist. Links into agent-docs use relative markdown links.

## Structure diagram

A plain Mermaid block under `## Structure diagram`:

```
## Structure diagram

```mermaid
classDiagram
...
```
```

- The catalog stores only the Mermaid text, never a model file, so diagrams survive ESM metamodel changes.
- Draw it from the real project model the evidence points at with
  `skills/judo-model-mermaid/scripts/render --model <path> --scope <fqn>`, or by hand when no model is at hand.
- Use neutral names (`Order`, `OrderLine`, `AuditLog`, `Status`), never project or client domain names. Keep it consistent with `## Model shape`.
- `spec-check` checks that every mermaid block starts with a known diagram type and is balanced.

## Forbidden content (entry-lint rejects)

- Project names (from `.pi/skills/judo-catalog-maintain/references/PROJECTS.md`) anywhere in the body: they belong only in
  `projects:`, `evidence:` and `project:` tags. Write the body neutrally
  ("one project", neutral names like `Order`, `Product`), with no client-domain terms.

- ```` ```graphql ```` fences, `mutation {`, `query {` GraphQL blocks
- CLI invocations: `java -jar`, `judo-cli`, `judo_cli`, `create -t`, `--ns `,
  `mermaid model`, `validate --strict`, `./judo.sh`, `judo.sh build|start|generate`
- Handlebars outside code fences (`{{ … }}`); JSX like `sx={{ … }}` inside
  `tsx`/`jsx`/`ts` fences is fine
- `score:` / `usage_count:` / `alternative_count:` in frontmatter
- block scalars in frontmatter
- harness wording: `.claude/`, `SKILL.md`, `subagent`, `judospec`
- real user names, home paths (`/Users/…`), e-mails, secrets
