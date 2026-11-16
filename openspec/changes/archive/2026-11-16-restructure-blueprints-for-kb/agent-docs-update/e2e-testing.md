# agent-docs/e2e-testing: sweep inventory (9 items)

Each item: id, kind, target, source, status, claim, fact, evidence.

## E2-001 [missing-how-to] E2E/integration suite multi-JVM heap: silent green with classes never run
- target: agent-docs/(general) | src: gap-mining | status: mined
- fact: The JUDO test suite forks several JVMs (each with its own heap, set in test/pom.xml); when a JVM OOMs halfway, every class still queued on that JVM never runs, yet surefire can still report '524 tests, 0 failures' — a misleading green. To get trustworthy results, raise the per-JVM heap (e.g. 4 GB), avoid running scenarios in parallel on a local machine, and/or run class-by-class; do not trust the aggregate pass count without confirming all test classes actually ran.
- evidence: ['rackinspect 2026-10-04T16-10-56 : "Memory builds up from class to class, and each JVM crashed with "Java heap space" after about 25 classes... So "524 tests, 0 failures" looked green, but 196 of 294 test classes never ran and the build still exited 1."', 'rackinspect 2026-10-04T16-10-56 : "we should run the test senarios after each other and not parallel on local machine toavoid the not enough r

## E2-002 [wrong-fact] e2e: TableHelper.getRowCheckbox, data-id, retries, baseURL
- target: agent-docs/e2e-testing | src: session:jb-007.json | status: reported-unvalidated
- claim: model-screen-layout uses tableHelper.getRowCheckbox; VisualElementIds example uses [data-id=...]; troubleshooting suggests retries: process.env.CI ? 4 : 0; README app URL includes ${ModelName}.
- fact: TableHelper has no getRowCheckbox; React template emits data-testid; generated playwright config already sets retries: 4; generated baseURL uses only the actor name (medium confidence).
- evidence: judo-ui-e2e-template@2b3e9b3 (E2E-001..004)

## E2-003 [wrong-fact] ## Running tests (APP_URL section)
- target: agent-docs/e2e-testing/README.md | src: agent-docs-review:e2e-testing.json | status: reported
- claim: App URL pattern is ${APP_URL}/${ModelName}/${ActorName}
- evidence: judo-ui-e2e-template@2b3e9b3:judo-ui-playwright-e2e-template/src/main/resources/actor/playwright/playwright.config.ts.hbs:35

## E2-004 [wrong-fact] ### Usage (VisualElementIds)
- target: agent-docs/e2e-testing/helpers-reference.md | src: agent-docs-review:e2e-testing.json | status: reported
- claim: await page.locator(`[data-id="${EntityNameForm.fieldName.id}"]`).fill('Value')
- evidence: judo-ui-react-template@ad0848bc:judo-ui-react/src/main/resources/actor/src/pages/index.tsx.hbs:397

## E2-005 [wrong-fact] ## VisualElementIds
- target: agent-docs/e2e-testing/helpers-reference.md | src: agent-docs-review:e2e-testing.json | status: reported
- claim: Generated file helpers/visualElementIds/VisualElementIds.ts exports PageContainer constants with id/label nodes
- evidence: judo-ui-e2e-template@2b3e9b3:judo-ui-playwright-e2e-template/src/main/resources/actor/playwright/helpers/visualElementIds/VisualElementIds.hbs:1

## E2-006 [bug] judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/e2e-testing/model-screen-layout.md.hbs:394
- target: agent-docs/e2e-testing/model-screen-layout.md | src: judo-ng-read | status: validated
- claim: The ```typescript fence that opens the Tab Bar example is never closed; the file has 93 fence markers (odd count), so the 'Relation Types' s
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template@6273a87:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/e2e-testing/model-screen-layout.md.hbs:394

## E2-007 [wrong-fact] ### Testing Association Tables
- target: agent-docs/e2e-testing/model-screen-layout.md | src: agent-docs-review:e2e-testing.json | status: reported
- claim: tableHelper.getRowCheckbox(selectorTable, n).click() selects table rows
- evidence: judo-ui-e2e-template@2b3e9b3:judo-ui-playwright-e2e-template/src/main/resources/actor/playwright/helpers/TableHelper.ts.hbs:3

## E2-008 [wrong-fact] #### Tests work locally but fail in CI
- target: agent-docs/e2e-testing/troubleshooting.md | src: agent-docs-review:e2e-testing.json | status: reported
- claim: Add retries in config: retries: process.env.CI ? 4 : 0
- evidence: judo-ui-e2e-template@2b3e9b3:judo-ui-playwright-e2e-template/src/main/resources/actor/playwright/playwright.config.ts.hbs:15

## E2-009 [wrong-fact] judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/e2e-testing/writing-tests.md.hbs:191
- target: agent-docs/e2e-testing/writing-tests.md | src: judo-ng-read | status: validated
- claim: Comment says getRow(page, 1) is 'Get specific row (1-indexed)'.
- fact: helpers-reference.md.hbs documents getRow as 0-indexed where 0 is the header row (and troubleshooting.md.hbs:112 says row 0 is the header); 
- evidence: template/judo-esm-fullstack-project-template:judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/e2e-testing/writing-tests.md.hbs:191

