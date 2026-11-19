# kb (pi-dashboard-kb): issues for the kb developers

Found while a build agent used this catalog as its kb (webshop build test, R16–R19). Each item reproduced on 2026-11-19 against this repo's index. Analysis: [research log](../research/README.md#2026-11-19-kb-use-in-the-webshop-run-r18r19).

| # | Issue | Effect |
|---|---|---|
| 1 | `kb_search` reports a sibling heading as `parent` | agents build a wrong section path |
| 2 | `kb_get` with a wrong section says the file is not found | agents conclude the file is missing |
| 3 | The frontmatter `meta` chunk wins and hides the body sections | agents cannot reach the sections and read the file from disk |

## 1. Sibling heading reported as `parent`

- **Reproduction:** `kb_search("Dashboard Page DASHBOARD_PAGE_INTERFACE_KEY", format: "json")` on `catalog/agent-docs/frontend/extension-points.md`.
- **Behaviour:** the hit has `headingPath: "Frontend Extension Points > Dashboard Page"` and `parent: {"headingPath": "Frontend Extension Points > Extra Routes"}`. In the file, `# Frontend Extension Points` (line 9) contains `## Extra Routes` (line 13) and `## Dashboard Page` (line 41): siblings. The condensed output prints the same wrong parent on its `⤷` line.
- **Expected:** `parent` is the enclosing heading (`Frontend Extension Points`), or the field is named for what it is (for example the first section of the file).
- **Seen in the build:** the agent called `kb_get(path, "Frontend Extension Points > Extra Routes > Dashboard Page")` (webshop session `reports/research/webshop-run/2026-11-11T14-06-20-342Z_01a1caee-….jsonl.gz`, line 10309).

## 2. Wrong section reported as a missing file

- **Reproduction:** `kb_get("agent-docs/frontend/extension-points.md", "Frontend Extension Points > Extra Routes > Dashboard Page")`.
- **Behaviour:** `(not found: agent-docs/frontend/extension-points.md)`. The file is indexed; only the section path is wrong.
- **Expected:** `section not found: <section>` followed by the file's section list (heading paths), so the caller can retry.

## 3. Frontmatter chunk wins and hides the body

- **Reproduction:** `kb_search("gdpr placeholder user on delete", format: "json")`.
- **Behaviour:** the top hit is `chunkId "b5baf5fc:meta"` with `headingPath` = the document title and `suppressedSections: 4`. `kb_get(path, "<title>")` returns the description followed by the raw keyword list. `kb_get(path)` returns the intro paragraph and `(+7 more sections in this file — pass section to fetch one)` without naming the sections.
- **Expected:** the meta chunk does not suppress body sections that match (or the hit carries the best body section's `headingPath`); a path-only `kb_get` lists the section heading paths.
- **Seen in the build:** reported in every round since R16 (webshop GAPS R16-10, R16U-1, R17-1, R18-1); the agent reads best practices and blueprints from disk instead.
