# Build test: prove the catalog by building an application with it

A builder session (a separate pi session) builds a real JUDO application from an acceptance list, using only this catalog as knowledge. The orchestrator (you) prompts it round by round, checks quality and logs every issue. The session log and the app's `GAPS.md` are then mined (see SKILL.md, workflow 1).

## Setup

- An empty app folder (`<APP_DIR>`) with `FUNCTIONS.md`: functions grouped in levels (`S01`… for the base, `F01`… for features), each with a browser-checkable acceptance line, plus a "frontend quality bar" section (human labels, shared components, theme, loading, empty and error states).
- The app's `.pi/dashboard/knowledge_base.json` has this catalog as its source, so the builder's `kb_search` hits the catalog.
- Spawn the builder session through the dashboard. Keep its id; give it the task in `dashboard-bus.ts spawn … --prompt`, and send every later command with `DASHBOARD_BUS=<dashboard-bus.ts> npx tsx .pi/skills/judo-catalog-expand/scripts/session-steer.mts <id> "<text>"` (or `@file`): always steer delivery, never `dashboard-bus.ts prompt` (followUp), wait with `dashboard-bus.ts until <id> idle`, stop it with `dashboard-bus.ts abort <id>` (the pi-dashboard skill's scripts).

## Standing rules to put in every round prompt

- `kb_search` + `kb_get` FIRST for every question and every problem, before reading generated code. Log every "kb had no answer" in `GAPS.md`.
- Never patch generated files, never add `.generator-ignore` entries. If no documented way exists, log it and use the least-bad documented route.
- Checks are Playwright tests with real user actions; screenshots at 375, 768 and 1440 px into `checks/<ID>/`. No checks while working; run them once at the end of the round.
- Run the new level's spec plus `--grep @smoke`, serially. Full suites only at the end (shared cart and stock make parallel workers interfere).
- Model changes go through the documented schema-migration route; no database wipes once data exists.
- If a function is blocked by a platform bug after one kb-guided try: log it, mark its test `test.fail()` with the reason, move on.
- Every function traces to catalog paths in `TRACE.md`. Commit locally at the end of the round, never push.
- Report per function ID; every issue with what, why and kind (catalog gap, catalog wrong, platform, CLI tool, agent tool, own mistake); test results; screenshot paths verified with `ls`. Then stop and wait.

## Your quality check after each round

- Read the round report, `git log`, the changed files outside `src/custom` (possible patched generated files) and the kb share of tool calls (kb calls / all calls).
- Open some screenshots yourself; do not trust "passes" alone. Builders over-report screenshots: `ls checks/<ID>`.
- Log the round in an orchestration log: built, QC findings, issue kinds, kb share, patched files.
- Next round prompt starts with the fixes you found, then the next level.

## Lessons from the first run (webshop, 15 rounds)

- Browser automation tools may silently drop clicks. Verify with an event listener before blaming the app; move checks to Playwright.
- The builder's kb use falls off under pressure (7 kb calls in 298 tool calls). Repeat the rule in every prompt and measure it.
- Long E2E runs block the session; the user will stop them. Smoke-tag a small set and run full suites rarely.
- For UI overhauls, make the builder read the live-iteration docs first (`agent-docs/frontend/development-workflow.md`, `agent-docs/deployment/local-development.md`) and use the Vite dev server with HMR instead of full rebuilds.
