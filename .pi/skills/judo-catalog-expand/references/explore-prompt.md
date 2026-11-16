# Project compliance explore

Work in the judo-blueprint repository root (read AGENTS.md). You audit ONE swept JUDO project (read-only snapshot under target/sweep/<project>/<sha>/src) against the catalog: does the project's structure and code follow, deviate from, or contradict what the catalog's best practices and model blueprints say, especially the entries that cite this project (`project:<project>` tag or `projects:`/`evidence:`)?

## Steps
1. Map the project: root layout, application/ modules, frontend-react actor modules and src/custom, model location, tests, openspec/docs. Note size (files per area).
2. List catalog entries that cite this project: `grep -rl '"project:<project>"' catalog` (frontmatter tags). For each, kb_get the entry and check the project actually does what the entry claims (file/class exists, pattern is as described, evidence path still valid at this SHA).
3. Structure compliance: check against `catalog/best-practices/*/structure-*.md` and `catalog/best-practices/project/` (new structure entries), `agent-docs/deployment`, `agent-docs/frontend/development-workflow.md` (generated vs custom, .generator-ignore, src/custom), and backend module/interceptor/custom-operation guides.
4. Code compliance: sample the custom backend code (custom operations, interceptors, services, DAO use) and frontend custom code (hooks, components, application-customizer) against the relevant best practices. Look for patched generated files, .generator-ignore entries, anti-patterns the catalog warns against, and good patterns the catalog does NOT have yet.
5. kb_search + kb_get FIRST for every question (never the `kb` CLI). Grep catalog/ only as fallback.

## Output
Write two files (edit nothing else, no state-changing git):
- <WORK>/<project>.jsonl, one object per finding:
  {"id":"<project>-NN","area":"structure|backend|frontend|model|test|docs","finding":"plain 1-2 sentences","kind":"complies|deviates|contradicts-catalog|catalog-claim-wrong|missing-in-catalog|anti-pattern","catalog_entry":"catalog/... or null","project_evidence":["src/rel/path:line", ...],"severity":"high|medium|low","proposed":"modify-catalog|add-catalog|fix-in-project|none","note":"what should change, one line"}
  Every finding needs at least one project_evidence path that exists (relative to the snapshot src/). `catalog-claim-wrong` = a catalog entry cites this project for something the project does not do.
- <WORK>/<project>.md: a short report: project map (a Mermaid or fenced tree), table of catalog entries citing it with verdict (holds / partly / wrong), top deviations, missing-in-catalog patterns, and recommendations.
Plain language, no em dashes. Aim for depth over breadth: 30 to 80 findings.
Final answer: three lines only (counts per type and kind; the 3 most important items; anything not done). Detail goes in your output file.
