# kb (pi-dashboard-kb): observations for the kb developers (2 bugs, the rest design limits)

Found while a build agent used this catalog as its kb (webshop build test, R16–R19). Items 1–5 reproduced on 2026-11-19 against this repo's index; item 6 not reproduced on that date. `session L<n>` = `reports/research/webshop-run/2026-11-11T14-06-20-342Z_01a1caee-58b6-724e-ae62-d32987dbcd2d.jsonl.gz`. Analysis: [research log](../research/README.md#2026-11-19-kb-use-in-the-webshop-run-r18r19).

**Classification (2026-11-20, against the kb specs in pi-agent-dashboard `openspec/specs/`):** only 1 and 2b are bugs. 2a and 3 come from two specified rules interacting; fixing them means amending a spec requirement first. 4 works as specified. 5a is a setting, 5b a limit of keyword search, 6 is unconfirmed. The kb maintainer fixes 1 and 2b.

| # | Issue | Verdict | What decides it | Effect |
|---|---|---|---|---|
| 1 | `kb_search` reports a sibling heading as `parent` | **Bug** | kb-markdown-chunking "Breadcrumb and Parent Linkage" requires the enclosing heading; chunks even name themselves as parent (`:1` → `:1`) | agents build a wrong section path |
| 2b | `kb_get` with a wrong section says the file is not found | **Bug** (misleading message) | no spec; `resolveFetch` returns the same result for "no such file" and "no such section" | agents conclude the file is missing |
| 2a | Section `Practice` cannot be fetched | Specified, side effect; needs a spec decision | "Empty sections dropped" plus the merge of sections under 100 characters; nobody specified that the dropped heading names then fail to fetch | a heading seen in the file returns not found |
| 3 | The frontmatter `meta` chunk wins and hides the body sections | Specified (design gap); needs a spec decision | one hit per file keeps the best-scoring chunk, and the meta chunk is a specified part of the index; the count-only path fetch is deliberate (design D7, per the kb maintainer); listing section names would be an enhancement | agents cannot reach the sections and read the file from disk |
| 4 | The read-discipline guard fires on build, log and test work | Specified; spec change, not a fix | kb-read-discipline "Piped search counts": `npm test \| grep FAIL` counts by design; `kb_guard_pause` is the intended exit. A change would stop counting a grep that only filters the previous command's output | nudges that no kb entry can answer |
| 5a | AGENTS.md rows take about half the results | Feature, adjustable here | the AGENTS.md lane quota is specified with its measured reason ("which file" recall 0.500 → 0.317 without it); `ranking.laneQuota` (default 0.5) can be lowered in this repo's kb config without code changes | answer sections are pushed down |
| 5b | `Index` and `Routing` sections rank 12th and 15th | Limit of keyword search | the query words are not in the heading; meaning-based matching is the open add-kb-semantic-annotation-plane change | agents conclude that the fact is not documented |
| 6 | The index-refresh warning stays on every search | Unknown | not reproduced 2026-11-19 | hits look stale |

Next step on this side: A/B-test a lower `ranking.laneQuota` with the harness in [`../research/runs/kbab/`](../research/runs/kbab/), every variant interleaved with a same-time baseline.

## 1. Sibling heading reported as `parent`

- **Reproduction:** `kb_search("Dashboard Page DASHBOARD_PAGE_INTERFACE_KEY", format: "json")` on `catalog/agent-docs/frontend/extension-points.md`.
- **Behaviour:** the hit has `headingPath: "Frontend Extension Points > Dashboard Page"` and `parent: {"headingPath": "Frontend Extension Points > Extra Routes"}`. In the file, `# Frontend Extension Points` (line 9) contains `## Extra Routes` (line 13) and `## Dashboard Page` (line 41): siblings. The condensed output prints the same wrong parent on its `⤷` line.
- **Expected:** `parent` is the enclosing heading (`Frontend Extension Points`), or the field is named for what it is (for example the first section of the file).
- **Seen in the build:** the agent called `kb_get(path, "Frontend Extension Points > Extra Routes > Dashboard Page")` (session L10309).
- **Re-run 2026-11-19:** reproduced. `kb_search` returned `parent: "Frontend Extension Points > Extra Routes"` for the `Dashboard Page` hit.
- **Also seen:** R16: `6. Test Isolation` is reported under its sibling `5. Logging and Debugging` (session L6338–L6342). Session L10306 and L10309 show the same wrong breadcrumb.

## 2. Wrong section reported as a missing file

- **Reproduction:** `kb_get("agent-docs/frontend/extension-points.md", "Frontend Extension Points > Extra Routes > Dashboard Page")`.
- **Behaviour:** `(not found: agent-docs/frontend/extension-points.md)`. The file is indexed; only the section path is wrong.
- **Expected:** `section not found: <section>` followed by the file's section list (heading paths), so the caller can retry.
- **Re-run 2026-11-19:** reproduced. `kb_get("catalog/agent-docs/frontend/extension-points.md", "Frontend Extension Points > Extra Routes > Dashboard Page")` and `kb_get("catalog/best-practices/frontend/i18n-generator-override-extra-fragment.md", "Practice")` both return `(not found: …)` for files that `kb_search` returns.
- **Also seen:** the `Practice` section name fails on other best-practice files (session L6246, L6265, L6487, L6593, L7050); a breadcrumb that makes a sibling a child fails the same way (session L6329, L6337). A bare path without the `catalog/` prefix also returns not found (session L7604; not re-run). A transient case that resolved later (session L6097) was not re-run.

## 3. Frontmatter chunk wins and hides the body

- **Reproduction:** `kb_search("gdpr placeholder user on delete", format: "json")`.
- **Behaviour:** the top hit is `chunkId "b5baf5fc:meta"` with `headingPath` = the document title and `suppressedSections: 4`. `kb_get(path, "<title>")` returns the description followed by the raw keyword list. `kb_get(path)` returns the intro paragraph and `(+7 more sections in this file — pass section to fetch one)` without naming the sections.
- **Expected:** the meta chunk does not suppress body sections that match (or the hit carries the best body section's `headingPath`); a path-only `kb_get` lists the section heading paths.
- **Seen in the build:** reported in every round since R16 (webshop GAPS R16-10, R16U-1, R17-1, R18-1); the agent reads best practices and blueprints from disk instead. Sessions: L6439, L6480–L6489, L6482, L7050, L7056, L7206–L7212, L8563, L8637–L8638, L8956, L9200, L9311–L9313, L9874–L9878, L9895.
- **Re-run 2026-11-19:** reproduced. `kb_get("catalog/best-practices/backend/quartz-scheduled-job.md")` returns the intro and `(+7 more sections …)` with no names. `kb_search("gdpr placeholder user on delete")` ranks the `:meta` chunk first with `suppressedSections: 4`.

## 4. The read-discipline guard fires on build, log and test work

- **Behaviour:** the guard prints `[kb] 3 consecutive searches without consulting the knowledge base` and `[kb] Repeated source searching, still no kb consult` after shell, grep, log, build and test commands. In one chunk it fired about forty times; in another more than twenty. No kb entry could answer most of those commands, and the notices did not lead to a `kb_search`.
- **Expected:** the guard does not count build, log and test output, or counts only searches that a `kb_search` would have answered. `kb_guard_pause` exists, but the agent gets no signal that it applies to such work.
- **Workaround:** `kb_guard_pause` for bulk triage work.
- **Re-run 2026-11-19:** reproduced. A shell call in this pass that read a session transcript returned `[kb] Repeated source searching, still no kb consult`.
- **Seen in the build:** R16 and R16U (session L6112, L6145, L6283, L6554, L6568, L6621, L6694, L6718, L6799, L7064, L7070, L7095, L7189, L8408, L8428, L8962); R17 (session L9112, L9118, L9286); R18 (session L9304, L9331, L9553); R19 (session L10176, L10226, L10516).

## 5. `kb_search` ranking misses sections that answer the question

- **Behaviour:** a query returns blueprint meta chunks and best-practice pages, but not the `agent-docs` section that holds the answer. The agent then concludes that the fact is not documented and looks elsewhere.
- **Expected:** the section ranks in the top hits for its own question.
- **Workaround:** `kb_get` with the known path, or a read of the catalog file.
- **Re-run 2026-11-19:** reproduced for all three queries.
  - `email service handlebars templates send email`: the `## Email Service` section of `agent-docs/backend/platform-behavior-reference.agent.md` (line 145) is not in the top 5; the hits are a blueprint, best-practice pages and an unrelated email page.
  - `declare database index on entity attribute`: `agent-docs/deployment/generator-plugins.md` `### Indexes` is not in the top 5; the hits are local-development, schema-evolution and interceptors.
  - `root URL redirect default landing page change`: the `Routing` section of `agent-docs/frontend/README.md` is not in the top 5; the hits are role-landing and action-hook pages.
- **Seen in the build:** R17 (session L8681, L8715); R18 (session L9855); R19 (session L10533, L10537).

## 6. The index-refresh warning stays on every search

- **Behaviour:** in the R16 re-check every `kb_search` returned `(index refresh still running, results may be stale)`. There is no status call and no wait option. The hits were usable, but the warning stayed on every call.
- **Expected:** a status call or a wait option; the warning only while hits are actually stale.
- **Re-run 2026-11-19:** not reproduced. The five `kb_search` calls in this pass carried no warning.
- **Seen in the build:** R16 (session L6404, L6415).
