# JUDO Blueprint

The JUDO catalog: platform documentation, model blueprints and best practices for JUDO applications. It is built to be searched by the pi kb (`kb_search`, `kb_get`) and comes with pi skills that use, diagram and author it.

## What's inside

```
catalog/                     the kb source (consumers index only this folder)
  agent-docs/                platform behaviour and rules, by area (83 docs)
    model/ backend/ frontend/ deployment/ integration-testing/ e2e-testing/
  model-blueprints/<id>/     103 reusable domain shapes
    BLUEPRINT.md             intent, structure, constraints, variations, when to use/avoid
    model.md                 model shape + generated Mermaid diagram
    backend.md frontend.md   layer guidance (project code is labelled as such)
  best-practices/<domain>/   207 single practices (model 71, backend 74, frontend 62)
fragments/<id>.model         144 validated fragment models behind the diagrams
skills/                      pi skills (see below)
PROJECTS.md                  projects the patterns were taken from
openspec/                    change proposals and specs for this repository
```

Every directory under `catalog/` has a generated `AGENTS.md` index (`| File | Purpose |`) for the kb.

## Use it in a project

1. Install the skills: `pi install` this package at a release tag.
2. Add the catalog as a pinned kb source:

   ```bash
   skills/judo-blueprint/scripts/pin-source <tag> --project /path/to/project
   ```

   This writes a `git` source with `pin: <tag>` and `subdir: catalog` into the project's `.pi/dashboard/knowledge_base.json`. Reload the kb afterwards. Pin a tag or SHA, never a branch.
3. Ask with domain words; the `judo-blueprint` skill explains search and apply.

## Skills

| Skill | For |
|---|---|
| `judo-blueprint` | Consumers: search the catalog, apply a blueprint or practice, pin the kb source |
| `judo-model-mermaid` | Render and check entry diagrams from `fragments/` |
| `judo-blueprint-author` | Write or update entries (format, `entry-lint`, `spec-check`, `claim-check`, `dox-agents`) |
| `judo-catalog-maintain` | `check-all`: every catalog gate in one run |
| `judo-session-distill` | Planned: turn development sessions into catalog candidates (not implemented yet) |

## Checks

```bash
./mvnw validate -P download-model-cli                 # pinned JUDO CLI → target/judo-cli.jar (never tracked)
skills/judo-catalog-maintain/scripts/check-all        # all gates; --no-sandbox skips the CLI-based fragment check
```

`check-all` runs `entry-lint`, `spec-check`, `claim-check`, the `AGENTS.md` freshness check, `kb dox lint`, no tracked jars, no legacy entries, and `check --all` on the fragments. CI runs the same in two jobs (lint, sandbox).

## Rules for contributors

- Platform facts come from `catalog/agent-docs`. A catalog entry never contradicts them; when the docs are silent, the entry says *verify* instead of guessing.
- Project code in entries is labelled as example project code, with neutral names.
- Diagrams are generated. Change the fragment, then `render`.
- The old `.claude/` agents, commands and scoring scripts are retired. They remain readable at the local tag `archive/pre-kb-restructure`.
