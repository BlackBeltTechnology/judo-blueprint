# Catalog pass: one edit pass per file

Work in the judo-blueprint repository root. Read AGENTS.md, `skills/judo-blueprint-author/references/format.md`.

Your files: the list in `<SCOPE_FILE>` (one path per line). Edit ONLY these files. Touch each file ONCE and apply every enabled step below in that single pass.

## Steps (the task says which are enabled)

**E. Evidence** (projects `<PROJECTS>`, snapshots `target/sweep/<project>/<sha>/src`, which is the repository root: paths never start with `src/`). For each `<project>:unrecorded`: find the claimed class, operation, hook or file in the snapshot; record 1 to 3 real paths `<project>:<path>`; fix a body fact the code contradicts. Not found: remove the project from `projects:`, `evidence:` and its `project:` tag and recompute `status` (1 single-project, 2-3 emerging, 4+ established); if that leaves zero projects, keep `unrecorded` and log `orphan`. Also apply the compliance findings in `<WORK>/<project>.jsonl` whose `catalog_entry` is one of your files.

**N. Neutral wording.** The body (everything outside frontmatter and generated Mermaid blocks) names no project and uses no client business words. "RackInspect keeps X" -> "One project keeps X" or just the practice. Domain names -> neutral names (Order, Product, Item, Account, Document, WorkOrder). Keep platform and integrated-product names (JUDO, Karaf, Keycloak, Vite, Playwright, Firebase). Never touch `projects:`, `evidence:`, `project:` tags. Keep every rule, caveat and *verify*.

**G. Generic names** (map in the task). Id rename: folder or file, `id:`, title, description; old id and old domain words into `aliases:`. Diagram classes: rename them in the entry's ```mermaid block to the generic names. Do NOT edit `[[links]]` in other files; the parent runs `rename-ids`.

## Rules

- `kb_search` / `kb_get` for catalog questions, never the `kb` CLI. No state-changing git. Plain language, no em dashes.
- Run `skills/judo-blueprint-author/scripts/entry-lint <your files>` before you finish; it must pass.
- Do not run `check-all` or `dox-agents`.

## Log

`<WORK>/pass-<SCOPE>.jsonl`, one line per changed file:
`{"file":"...","evidence":[{"project":"...","result":"found|partly|removed|orphan","paths":[...]}],"neutral":["terms removed"],"renames":[{"type":"id|class","old":"...","new":"..."}],"note":"anything kept on purpose"}`

Final answer: three lines only: counts per step, orphans and removed citations, anything you could not do.
