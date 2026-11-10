---
name: judo-blueprint
description: Find and apply JUDO catalog knowledge (model blueprints, best practices, agent-docs) through the kb. Use when designing or changing a JUDO model, backend, or frontend and you need a proven pattern, a platform rule, or a model shape to copy. Also sets up the catalog as a pinned kb source in a consuming project.
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
2. **Read the entry.** `kb_get <path>` gives the first section and a count of the rest. Pass `section` with the full heading path from `kb_search` JSON output to read one section.
3. **Check the platform rule** the entry links to in `agent-docs/`. When an entry and the agent-docs disagree, the agent-docs win.
4. **Apply** with the steps in [references/apply.md](references/apply.md): adapt names, build the model shape with the JUDO model CLI, and keep labelled *project practice* separate from platform behaviour.

## Set up in a consuming project

```bash
skills/judo-blueprint/scripts/pin-source v1.0.0 --project /path/to/project
```

This adds a pinned kb git source with `subdir: catalog` to the project's `.pi/dashboard/knowledge_base.json`, then you reload the kb. Pin a tag or SHA, never a branch. The script only edits the local file.
