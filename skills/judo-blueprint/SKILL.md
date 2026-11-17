---
name: judo-blueprint
description: Find and apply JUDO catalog knowledge (model blueprints, best practices, agent-docs) through the kb. Use when designing or changing a JUDO model, backend, or frontend and you need a proven pattern, a platform rule, or a model shape to copy. Also sets up the catalog as a pinned kb source in a consuming project, or a project contribution branch (`project/<id>`) that the project grows and the maintainer merges.
---

# judo-blueprint

The JUDO catalog is indexed by the kb (`kb_search`, `kb_get`). It has three parts under `catalog/`:

| Part | Holds | Trust |
|---|---|---|
| `agent-docs/` | Platform behaviour and rules, by area (model, backend, frontend, deployment, testing) | Source of truth for platform facts |
| `model-blueprints/<id>/` | Reusable domain shapes: `BLUEPRINT.md` plus `model.md` (shape and generated diagram), `backend.md`, `frontend.md` | Project-proven patterns |
| `best-practices/<domain>/<id>.md` | Single practices for model, backend and frontend | Project-proven practices |

## Use it

1. **Search first.** Run `kb_search` with the domain words of the task ("approval workflow", "soft delete", "range interceptor"). Entry aliases are tuned for this. See [references/search.md](references/search.md).
2. **Read the entry.** Blueprint and best-practice files are short (median 64 lines, 95% under 100): read the whole file once kb_search has found it (`catalog/<path>`, or the `read` tool). For long agent-docs, read the `.agent.md` companion, then `kb_get` one section. A path-only `kb_get` returns only the first section, and `section` needs the full `headingPath` from `kb_search` with `format: "json"`; a short name such as `Practice` returns "not found".
3. **Check the platform rule** the entry links to in `agent-docs/`. When an entry and the agent-docs disagree, the agent-docs win.
4. **Apply** with the steps in [references/apply.md](references/apply.md): adapt names, build the model shape with the JUDO model CLI, and keep labelled *project practice* separate from platform behaviour.

## Set up in a consuming project

```bash
skills/judo-blueprint/scripts/pin-source v1.0.0 --project /path/to/project
```

This adds a pinned kb git source with `subdir: catalog` to the project's `.pi/dashboard/knowledge_base.json`, then you reload the kb. Consumers pin a tag or SHA. The script only edits the local file.

## Contribute from your project

The catalog grows from the projects that use it. A contributing project works on its own branch of this repository, `project/<project-id>`, branched from `develop`, and points its kb at that branch:

```bash
skills/judo-blueprint/scripts/pin-source --branch project/<project-id> --project /path/to/project
```

When the catalog lacks something, add it in the branch (facts with evidence, new entries via `judo-blueprint-author`, your evidence on existing entries, a different method as a variation), run `check-all`, push, and re-index the project's kb (`kb index` or `/reload`). The maintainer merges what meets the merge criteria into `develop`. Full guide: [references/contribute.md](references/contribute.md); criteria: [merge-criteria.md](../judo-catalog-maintain/references/merge-criteria.md).
