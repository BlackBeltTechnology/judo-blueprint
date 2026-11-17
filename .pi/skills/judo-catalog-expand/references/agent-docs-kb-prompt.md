# Agent-docs kb pass: one edit pass per file

Work in the judo-blueprint repository root. Read AGENTS.md and `skills/judo-blueprint-author/references/format.md`, sections "Agent-doc" and "Companion": that is the contract you implement.

Your files: the list in `<SCOPE_FILE>`. Edit ONLY those files and create their companions. Touch each file once and do all steps in that pass.

## Steps per file

1. **Frontmatter.** Keep `title`; rewrite `description` as one sentence naming the platform area and the questions the doc answers. Add:
   - `aliases`: 3 to 8 phrases a developer would type to find this doc (plain words, no identifiers);
   - `keywords`: 5 to 15 identifiers that really occur in the doc (class, annotation, method, config key, CLI command, file name);
   - `tags`: `[domain:<area>, layer:<layer>, status:platform]`. Area by folder: `model/` model, `backend/` backend, `frontend/` frontend, `deployment/` deployment, `integration-testing/` and `e2e-testing/` testing. Layer: model, backend, frontend, infrastructure (deployment) or test (testing). A root README may carry several domain and layer tags.
   - Remove harness keys (`name`, `agent`, `model`, `context`, `disable-model-invocation`, `user-invocable`, `allowed-tools`).
   Single-line flow lists only, no `|` or `>` block scalars.
2. **Headings.** Rename every generic `##`/`###` (Overview, Introduction, Summary, Example(s), Usage, Notes, Details, Configuration, Key Concepts, Best Practices, Troubleshooting, Common Patterns, Patterns, Reference, Quick Reference, Setup, General, FAQ) to a heading that names its subject, e.g. `## Interceptor overview` -> `## How operation interceptors run`. Remove table-of-contents sections. Update `#anchor` links inside your files to the new anchors, and log every rename (other files' links are fixed by the parent).
3. **Companion** when the file has over 300 lines or over 15000 bytes: write `<name>.agent.md` next to it exactly per format.md: first line `# <name>.md — index`, then `Pull-only condensed map. Source: <repo path>.`, then one `##` per `##` of the source with the identical heading text (after your renames), each with terse bullets: rules, identifiers, gotchas. Nothing that is not in the source. At most 250 lines. No frontmatter.
4. Do not change platform facts, examples or meaning. No project names or client business words.
5. `skills/judo-blueprint-author/scripts/entry-lint <your files>` must pass. kb_search / kb_get for questions (never the `kb` CLI). No git, no check-all, no dox-agents.

## Log

`<WORK>/agentdocs-<SCOPE>.jsonl`, one line per file: `{"file":"...","renamed":[{"old":"Overview","new":"...","anchor_old":"overview","anchor_new":"..."}],"removed_toc":true|false,"companion":"<path or null>"}`

Final answer: three lines only: files done, companions written, anything not done.
