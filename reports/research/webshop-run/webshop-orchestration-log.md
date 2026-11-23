# Webshop build: orchestration log

- **Build session:** `01a1caee`, model anthropic/claude-sonnet-5-5, folder `~/Projects/webshop-test`.
- **Acceptance list:** `FUNCTIONS.md`.

The orchestrator works in rounds:
1. Send one feature batch with "stop after X".
2. Wait for the build session to go idle.
3. Run the quality check (`target/webshop-round.sh qc`), look at the screenshots, and log the result here.
4. Send the next follow-up, with corrections on how to work.

Each issue the builder faces is logged with **why** it happened:
- **catalog gap:** the catalog is missing knowledge or has it wrong;
- **tool:** a problem in the browser or CLI tooling;
- **builder:** a working-method mistake by the build session;
- **platform:** a JUDO platform bug.

## Round 0: Level 0 S01–S06 (before orchestration)

- **Result:** S01–S06 reported done. 16 gaps logged in `GAPS.md`.

| Issue | Why | Kind |
|---|---|---|
| Price formatting done by patching a generated 490-line table component, added to `.generator-ignore` | The documented `TABLE_COLUMN_CUSTOMIZER_HOOK` is not consulted by this template version's table; the doc example signature differs from the shipped type | catalog gap, plus builder (should have asked) |
| No reproducible first login user; seed script uses psql and the Keycloak admin API | No catalog recipe for the first user of a minimal app; the actor/principal guidance is contradictory | catalog gap |
| Project creation needed plugin coordinates taken from `~/.m2` | build-process.md lacks the plugin groupId, version and `-Dversion` | catalog gap |
| Wrong app and Keycloak URLs (`/apps/`, port 8080, no `/auth`) | local-development.md is out of date | catalog gap |
| 95 fixed browser waits (~26 min); clicks ignored after restart; navigation forced with DOM `eval` clicks | Snapshot-ref clicks went stale on a re-rendering page; the builder assumed the app was slow (the server answers in ms) | tool, plus builder |
| Only 14 of ~460 calls were kb calls in the first hour | No kb-first rule in the first prompt | builder (fixed by the user's steering) |
| S03 checked with curl, not the UI | Headless `fill` did not update the React state of the numeric field | tool |
| `kb_get` returns "not found" for paths that `kb_search` lists | kb path resolution | tool |

## Round 1: price display (S04 redo + S09)

- **QC (16:39):**
  - S04 patch reverted.
  - Shared `Price.tsx` added, used in the form and details view through `customImplementation=true` field scaffolds.
  - Table column skipped.
  - kb share 28/201 (was 14/460). No DOM/eval clicks, no curl. Fixed waits 1.7 min (was 26).
  - No screenshots: the browser checks were not done.
- **Verdict:** method much better. Feature unverified. The table column is still `79.90` without a currency.

| Issue | Why | Kind |
|---|---|---|
| Table column hook unusable: with `customImplementation=true` on the column, the generated table does not compile (`useTrackService` not imported, filter string missing `)`) | Template bug. `table-hooks.md` never says the column needs `customImplementation=true` | platform + catalog gap |
| Doc hook signature `(original) => …` vs shipped `() => (original) => GridColDef` | Docs out of date | catalog gap |
| No "view field hook"; only a model-level `customImplementation` on the DataField works | `ui-hooks.md` covers only the AppBar, hero, logo, footer and menu | catalog gap |
| Registering custom implementations means editing `src/custom/application-customizer.tsx`, which needs a `.generator-ignore` entry | That file is generated once as a scaffold; the catalog doesn't say it is meant to be owned | catalog gap (accepted exception) |
| `./judo.sh generate` deletes `target/judo-cli.jar`; the catalog says `./mvnw`, but the project has no mvnw | Docs out of date | catalog gap |
| Model change silently not applied while the CLI jar was missing | Builder ran the CLI without checking the jar | builder |
| **Menu click does nothing**, so nothing could be checked | **Orchestrator test:** the agent-browser tool delivers no click events to the page at all (a capture listener sees zero clicks for ref, text and raw mouse clicks). `set viewport` lags, and `open` sometimes leaves the tab on `about:blank`. The app's handlers are fine (`setTimeout(0)` fires in 0 ms; the link has a correct hash href) | **tool** |

- **Follow-up R2:** move all browser checks to Playwright E2E tests, as the catalog prescribes (`agent-docs/e2e-testing`). Then check S04/S09 for real.

## Round 2: Playwright E2E checks + verify S04/S09

- **QC (17:20; session resumed once after a user stop, before its report):**
  - 4 Playwright tests pass. 15 screenshots in `checks/S04`, `checks/S09`.
  - No generated files patched, no `.generator-ignore` additions.
  - kb share 18/104. No DOM clicks, no curl.
- **Orchestrator looked at the screenshots:**
  - The list at 1440 shows `79.90 / 12.00 / 129.50 EUR`. Correct.
  - Details at 375 shows `79.90 EUR`, but the **Price field is above Name**, and the description test data is "a / b".
  - Titles are still "ProductInfo Table" / "ProductInfo View / Edit".
  - The phone bottom bar shows "ProductInfo" and "Other".
- **Verdict:** S04 and S09 pass. The frontend still looks like a raw generated back office (that is S07, S10, S11).

| Issue | Why | Kind |
|---|---|---|
| `playwright install chromium` hangs at extraction and leaves a broken binary | Unknown; the kb has nothing on browser install | tool/environment |
| E2E docs show glyph button names (`'󰆓 Update'`, `'󰵲 Galaxies'`); real names are `Update`, `Back`, `Cancel`; create is a dialog | Docs out of date with the template | catalog gap |
| `getByLabel('Price')` ambiguous (column-menu button); `getByRole('textbox',{name})` works | Not documented | catalog gap |
| Custom `PriceField` was read-only on the view page | Generated view starts `editMode=false` and switches on first change; undocumented. Builder used `readOnly = !editMode` | builder + catalog gap |
| Test clicked `Save`, the button is `Update` | Builder took the name from the VisualElementIds file | builder |
| E2E generation needs `generate` **and** `build`; the flag already exists in `generator-parameter.properties` | README only says "build" | catalog gap |
| Price column is now a derived String (`price!round(2)!asString() + " EUR"`): sorts alphabetically; currency duplicated in model and `Price.tsx` | Column hook is broken (R1), so this is the only documented route | platform (consequence of R1) |
| `kb_get` returns only the first section of long files | kb tool behaviour | tool |
| Field order on the view: Price before Name | Builder never set the layout order | builder |

## Round 3: branding + labels (S07, S11 labels)

- **QC (18:40):** 10 tests pass, 2 fail (field order).
  - Branding is in the model: title, palette, logo. A logo props hook gives the collapsed icon.
  - Labels: Products / Product / Profile. The phone bar shows "Products" and "More" (via an i18n fragment override).
  - Descriptions are seeded through the UI.
  - No new `.generator-ignore` entries. kb share 17/139.
- **Orchestrator looked at the screenshots:**
  - The green palette, logo and labels are correct.
  - The details page at 375 still shows Price first.
  - Home is still a bare "Hello!" page.
- **Verdict:** S07 passes. S11 labels pass. Field order fails.

| Issue | Why | Kind |
|---|---|---|
| **Price always rendered before Name/Description** despite the model order and `row` | **Orchestrator root cause:** esm2ui `dataField.etl` has one ETL rule per widget type, and they run in declaration order. `NumericTypeVisualInput` (l.180) runs before `StringTypeTextInput` (l.215), and each rule appends to `uiContainer().children`. So the container order is grouped by widget type; `row` is copied but not used for ordering | **platform bug** |
| The builder spent most of the round on `move`/delete/re-add/`fill` attempts | No catalog note on field order; the transformation behaviour is undocumented; the builder kept trying blind instead of stopping to ask | catalog gap + builder |
| `judo move` reports "reordered description" whatever is moved; `graphql ui`/`query ui` read a stale model | CLI bugs | tool |
| i18n override path in the practice note is wrong (real: `application/frontend-react/generator-overrides/`); the fragment needs a trailing comma; a wrong path only gives a WARNING | Docs out of date | catalog gap |
| "Other" phone-bar item cannot be removed, only renamed | Not supported in a documented way | catalog gap |
| Logo SVG without width/height collapses to 0 height | Not documented | catalog gap |
| Delete/re-add lost the custom price field and the multi-line flag; `fill` added stray `priceLabel` fields | Builder side effects of blind attempts | builder |
| `generate` deletes `target/judo-cli.jar` (3rd time) | Repeats R1 | catalog gap |

- **Follow-up R4:** apply the field-order workaround (one Group per field), then stop. Next: S08 card grid as the home page.

## Round 4: field order workaround (one Group per field)

- **QC (18:45):** the workaround had no effect. 10/12 tests pass. Short round, 7 tool calls; the builder stopped as told.
- **Orchestrator root cause (corrects my R3 diagnosis):**
  - The UI model (`webshop-ui.model`) already has `priceGroup, nameGroup, descriptionGroup` while the ESM model has name, price, description.
  - `esmToUi.etl` *does* sort container children by ESM position (pre block l.~77 fills `__pos`; post block l.114 `sortBy(__pos)`).
  - Element rules look the position up with `__pos.get(component) ?: 0` (`operations/ui/visualElement.eol:5`). For these fields the lookup misses, so every element gets 0, and the stable sort keeps rule-firing order. Number widgets come first.
  - Groups are created lazily from their first child's rule (`s.eContainer.uiContainer()`), so groups inherit the same order.
- **Verdict:** platform bug, no model-level workaround. Handle the order at the UI layer (custom layout in S10). The field-order tests are marked expected-to-fail with the bug reference.

| Issue | Why | Kind |
|---|---|---|
| Groups keep the price-first order | Position lookup falls back to 0; lazy group creation follows field rule order | platform bug |
| My R3 diagnosis ("no sort exists") was incomplete | I read only the rule order, not the post block | orchestrator |

## Round 5: S08 card grid home + S10 details layout

- **QC (18:56):** 17 passed, 1 skipped (empty state).
  - Custom components only in `src/custom`. No generated file patched, no `.generator-ignore` additions.
  - **kb share 1/31: regression.** The builder mostly read generated code.
- **Orchestrator looked at the screenshots:**
  - The grid looks finished: 3 columns at 1440, 1 at 375, brand colours, `79.90 EUR`, first description line.
  - The details page has a large name, the price badge and the description, in the right order. It still looks a bit form-like (field labels, underline on the name).
- **Verdict:** S08 and S10 pass. **Level 0 complete**, apart from the documented gaps. Stop for the user's review, as FUNCTIONS.md requires.

| Issue | Why | Kind |
|---|---|---|
| Home page seam (`ComponentProxy` with key `DashboardPage`, "Hello!" fallback) not in the kb | The catalog only describes the no-layout dashboard and Extra Routes | catalog gap |
| No hook for a whole view layout; `ui:Placeholder` + `customImplementation` renders nothing | Undocumented and unsupported | catalog gap / platform |
| The view loads only attributes that have a field, so the layout needs 3 custom field registrations (2 render nothing) | Query mask follows the view fields | platform behaviour, undocumented |
| Create dialog still shows Price first (test marked `test.fail`) | R4 platform bug | platform bug |
| Empty state not testable | No documented way to get an empty data set | catalog gap |
| No product images (placeholder art) | The Level 0 model has no image attribute; images are F09 | by design |
| kb used once in 31 calls | Builder slipped back to reading generated code | builder |
| `sed -i` on macOS, TS errors found only at build | Builder | builder |

## Round 6: Level 1, F01–F08

- **QC (20:04):** 29 passed, 1 skipped; F07 category filter `test.fail()`. No generated-file patches. kb 10/110 (still low).
- **Orchestrator looked at the screenshots:** the category view shows a "Products" *button*, not an embedded table (F08 asks for an embedded table).
- **Verdict:** F01–F06 pass. F07 partial (no category filter until F12). F08 partial (button, not table).

| Issue | Why | Kind |
|---|---|---|
| Adding columns broke the dev DB (`column c_sku does not exist`); `schema-upgrade` uses a wrong `-f ${SCHEMA_DIR}/schema` path and hung with `-o schema_dir=application`; DB and Keycloak volumes wiped | schema-evolution.md says a dev DB needs no manual step; the script default path is wrong | platform + catalog gap |
| To-one association renders as a plain button; AGGREGATION gives the autocomplete; docs list `button`/`tag` representations the CLI rejects | Docs vs CLI mismatch | catalog gap |
| Relation can't be a table column/filter | Codegen limit (needs a derived attribute, F12) | platform |
| Two price columns (formatted string + numeric) for sort | Column hook bug (R1) | platform |
| Category view: button instead of an embedded table | Probably a non-eager relation (embedded tables need `isEager`, per the developer answers); the builder didn't check | builder / catalog gap |
| Generated text fields commit with a debounce; `fill()` too fast | Undocumented | catalog gap |
| Builder test mistakes (sidebar click, stale temp data, header row parsed as price) | Builder | builder |

## Round 7: Level 2, F09–F16 (+ F07/F08 follow-ups)

- **QC (21:27):**
  - Admin 30 passed, customer 15 passed and 1 skipped (two suites now).
  - `.generator-ignore` gained the customizer entry in the two new actor modules (the accepted R1 exception).
  - kb 14/198 (low).
- **Orchestrator looked at the screenshots:**
  - Customer grid with images, category chips and SKUs looks good.
  - **Regression:** the customer side drawer is squashed. Menu labels are cut to "Pr…", "My…", and the logo is tiny.
- **Verdict:** F09–F16 pass functionally. F07 and F08 are now fixed. Two quality defects to fix: the drawer, and the customer API leaking `stock`/`active` through the shared TO.

| Issue | Why | Kind |
|---|---|---|
| No `isEager`; embedded table needs `representationComponent=table` (CLI default on views is `button`, kb says `table`) | Docs vs CLI | catalog gap |
| First-login entity row needs a hand-written Java interceptor | Runtime doesn't provision | platform (documented) |
| Interceptor `client` arg holds `webshop.Customer` with dots; switched to the token `azp` | Undocumented | catalog gap + builder |
| Self sign-up not modelled; seed script PUTs the realm | No model setting | catalog gap |
| Actor split leaves stale `webshop__shop` modules; no shared home for custom code (Price.tsx duplicated) | Undocumented | catalog gap |
| Customer API returns admin fields (`stock`, `active`) — hidden in the UI only | Builder reused one TO for both actors | builder (security) |
| Bidirectional composition rejected; derived `!any().addresses` returned 2 of 6 | Validator rule undocumented; derived bug unexplained | catalog gap / platform? |
| Field-order bug also hits the admin details page, the variant dialog and the customer Unit field | R3-1 | platform |
| Embedded dialog button "Ok", composition children saved by the page Update, default labels like "Sku" | Undocumented | catalog gap |
| Admin product table too wide at 1440 (8 columns) | Builder UX choice | builder |
| Drawer squashed on the customer front | Regression, not noticed by the builder | builder |

## Round 8: fixes + Level 3, F17–F24

- **QC (23:25):** admin 30 passed, customer 27 passed and 1 skipped. No generated-file patches. kb 6/161 (very low).
- **Orchestrator looked at the cart screenshot:** clean table, Price component, total row, Check out.
  - The profile name in the drawer shows a random username ("f1917…").
  - The menu order is wrong (Cart in 4th place).
- **Verdict:** F17–F24 pass. The drawer, data-leak and admin-table fixes are done.

| Issue | Why | Kind |
|---|---|---|
| Generated drawer persists "mini" in browser storage and recomputes only on tier crossing; earlier squashed screenshot was mid-animation | Undocumented platform behaviour + builder screenshot helper | platform + builder |
| Operation with output **and** input dialog breaks the frontend build (duplicate import, Biome) | Generator bug | platform |
| Generated fault dialog prints the error code letter by letter (uses the first key of the 422 body) | Generator bug; fixed via the documented error handler interceptor | platform |
| OperationForm directly in a view fails the transformation (must be in an ActionGroup); docs say it works | Docs wrong | catalog gap |
| Menu order not taken from the model | Platform | platform |
| `postCallAccessNavigation` cannot be cleared; `move --index` has no effect | CLI | tool |
| Sequence numbers can gap; the registry blueprint was not built | Builder chose the simpler route | builder (accepted) |
| kb used 6 times in 161 calls; DAO names taken from the generated SDK | Builder habit; `data-access-guide.md` not read | builder |

## Round 9: fixes + Level 4, F25–F32

- **QC (00:31):** admin 30 passed, customer 33 passed and 1 skipped (one flake re-run). kb 19/168 (better).
  - The `.gitignore` diff is only new generated container entries.
- **Orchestrator looked at the screenshots:** the order view has the 4 history rows, but they are **not sorted by time** (Delivered first, "Order placed" second). The admin can see an editable date picker on "Ordered".
- **Verdict:** F25–F31 pass. F32 partial (the 30-day boundary is untested).

| Issue | Why | Kind |
|---|---|---|
| F31 "post-call interceptor" impossible for custom transitions | Interceptors skip custom operations (confirmed earlier in code) | FUNCTIONS.md/catalog mismatch (catalog correct) |
| F32 range interceptor only fires on reference ranges; used a derived access with `now()!plusDays(-30)` | FUNCTIONS.md assumption wrong | FUNCTIONS.md |
| F32 boundary untestable: no documented way to seed an old order | No seed/initializer trigger documented | catalog gap |
| F29: catalog says refuse with a fault; FUNCTIONS says deactivate | Spec mismatch | FUNCTIONS.md vs catalog |
| Deleting operation: generated post-call refreshes the deleted record (404), output never shown | Generator bug | platform |
| DB not migrated again; `schema-upgrade` fails (Maven error); wiped again | R6-1 | platform + catalog gap |
| "Manual changes" error after generate with no real changes; `build -i` needed | Unknown | platform |
| Tool output diversion re-ran a script, duplicating model elements | context-mode wrapper | tool |
| Optional 0..1 relation query returns `Optional<T>`; `createX` only with `createable=true` | Partly documented | catalog gap |
| History rows unsorted; Ordered field editable-looking | Builder didn't set a default sort / read-only | builder |

## Round 10: fixes + Level 5, F33–F40

- **QC (02:07):** admin 31 passed, customer 39 passed and 1 skipped (3 failures from a test-edit slip, fixed; level4 re-run alone 7/7). kb 8/116 (low).
- **Orchestrator looked at the screenshots:** the Hungarian cart is fully translated, with `79,90 EUR`, net/VAT/shipping/total rows. The language switch sits under the logo. The invoice PDF opens inline.
- **Verdict:** F33–F40 pass, with caveats: the F36/F37 clock is not settable from tests, and Hungarian is partial.

| Issue | Why | Kind |
|---|---|---|
| No runnable Markdown→PDF recipe (DOCX deprecated); builder wrote a mini renderer with runtime PDFBox | Catalog has Handlebars + preview but no PDF step | catalog gap |
| Business clock is an env var read at startup; tests can't set the date | Practice design | catalog gap |
| Sale-price window uses `Date!now()` in the model, not the business clock | Model expressions can't call the Java clock | platform limit |
| `schema-upgrade` fails because `SCHEMA_DIR` is empty in the generated `judo.sh`; 3rd DB wipe | R6-1 | platform |
| Singleton has no startup seed; row entered via UI, second row not prevented | No init hook documented | catalog gap |
| Generator produces only `system_hu-HU.json`; app labels need a script-made file; model-built text and Java faults stay English; language lost on full reload | i18n gaps | catalog gap / platform |
| Custom cart component not refreshed after an operation (window-event workaround) | Platform | platform |
| `hiddenBy` on a custom-implemented field never gets its value | Platform | platform |
| Same timestamp shown in two zones (02:03 vs 03:03) | Known time-zone bug (developer K17) | platform |
| `XMI ID COLLISION` errors in the admin build (ignored) | Unknown | platform? |

## Round 11: Level 6a, F41–F47 (+ R10 time zone and field order)

- **QC (04:11):**
  - Admin 30/31 and customer 47/49 in the full runs. The 2 flakes were fixed and re-run per file, but the full suite was not repeated.
  - kb 15/269 (low).
  - The builder deleted leftover test products **with SQL** (cleanup only).
- **Orchestrator looked at the screenshots:** the inbox has the unread badge.
  - The breadcrumb says "Home / Products" on the Notifications page (wrong).
  - The bell sits on a grey ellipse under the language switch (clumsy header).
- **Verdict:** F41–F44, F46 and F47 pass. F44's "filtered" export has its own form.

| Issue | Why | Kind |
|---|---|---|
| DB migration failed again (4th wipe) | R6-1 | platform |
| Post-call interceptor on refresh "marked read" but the row stayed unread; async never ran | Unknown | platform / catalog gap |
| Static operation with input as a table action breaks the UI generator | Generator bug | platform |
| Custom operation can't see the table's filter | By design; FUNCTIONS assumption | catalog gap |
| Optional inputs arrive as `null` despite an `Optional` getter type | Matches the developer's "Optional can be null" (K14) | platform (documented by developer) |
| Date fields drop keys in the first second; upload button only by title | Undocumented | catalog gap |
| CLI: partner relation default name/cardinality wrong; `MenuItemAccess` label ignored; mapped TO gets all attributes | CLI | tool |
| Invited admin can't log in (no password, no mail locally); no unique e-mail constraint | Local env + builder | environment + builder |
| Wishlist price column is a derived string, not the Price component | Builder shortcut | builder |
| Wrong breadcrumb on Notifications; bell layout | Builder UX | builder |

## Round 12: Level 6b, F45, F48–F54 (+ UI fixes)

- **QC (08:30):** one full run of both suites green: admin 35, customer 54 + 1 skipped. CI checkout passes headless. 8 integration tests pass. kb 18/365 (very low share, many test iterations).
- **Verdict:** all pass. **F52 is the first model change without a DB wipe** (two real migrations with backfill).
  - F51 kept in the model (documented decision).
  - F50 audit covers built-in edits plus the bulk price change only.

| Issue | Why | Kind |
|---|---|---|
| `schema-upgrade` looks for `<root>/schema`; `schema_dir=application` works but is undocumented; `apply` leaves no room for the backfill → used `judo-rdbms-schema:generate` with the old model + hand-written changeset + `:execute` | Script default + docs | platform + catalog gap (**root cause of the R6–R11 wipes**) |
| Generated table column hooks never applied; `DataColumn.customImplementation` doesn't compile; `TransferObjectTable.customImplementation` does nothing | R1 again | platform |
| Java clock in JVM zone (CET) vs model clock in platform zone (UTC) broke the return window | Builder (R11 claim was wrong); catalog says one clock | builder |
| Generated `integration-test/pom.xml` has an empty `i18n-api` version → hand-written test module | Template bug | platform |
| Top-N: `!sort()!heads(5)` fails in asm2query; `!heads(sel,5)` returns 1 row; sort by derived aggregate → broken SQL | JQL/query bugs | platform |
| Row actions: CLI offers no `hiddenBy`/`enabledBy` though the docs list them | CLI vs docs | tool + catalog gap |
| `fill` adds menu items labelled with TO names; duplicate `MenuItemAccess` fails silently | CLI | tool |
| Enum labels can't be set in the model → derived label strings | Platform limit | platform |
| Kept DB means test data hygiene; SQL used once for restock/cleanup | Test design | builder |

## Round 13: Level 7, F55–F61 (B2B)
- **Built:** companies + members (inside the Customer actor, decision in TRACE.md), invitation key, company prices and tiers, credit limit + approval, quotes, PO number. Migration without wipe (F52 route). Commits 37610d9, 8fd2635.
- **Tests:** Level 7 spec 7/7, backend IT 8/8. Full suites at 3 workers: 9 customer + 3 admin failures from shared cart/stock (own mistake, test isolation); serial reruns green. New rule: round = new spec + `@smoke`, full suites serial at the end. User stopped one over-long E2E run.
- **QC (my own look):** report claims screenshots at 375/768/1440 for F55–F61, but only 2 exist (`checks/F55/...-1440.png`, `checks/F60/...-1440.png`) → builder over-reports (own mistake). Admin quote page: `Requested` date and `Order` are editable-looking fields (should be read-only); field order wrong again (platform sort bug). Order page shows the company and PO fields fine.
- **kb share:** 7/298 tool calls. Still too low despite the rule (builder).
- **Generated files patched:** none.

## Round 14: Level 8 paused (WIP)
- Stopped twice by the user for review. Commits d07ed07, 51df7b9 are WIP; F62–F70 not finished. The user asked to stop features and do a UI overhaul first.

## Round 15: UI overhaul (sent)
- Goal: real-webshop look (storefront, header with cart counter, category listing, product page, step checkout, account area). Builder must first kb_get the live-iteration docs (frontend/development-workflow.md, deployment/local-development.md) and use dev server + HMR instead of full rebuilds. Stops after for user review.
- **Result:** storefront overhaul done (top bar via `menuOrientation=HORIZONTAL`, grouped menu, hero/categories/search, cart counter, step checkout inside the cart page) and Level 8 finished (F62–F70). Commit e35dddd. Iterated with the Vite dev server against the running backend. `@smoke` 7/7, Level 8 spec 6/6 serial; one admin-restock run incomplete. 21 screenshots in `checks/UI15`.

| Issue | Why | Kind |
|---|---|---|
| `textWidget=TEXT` drops the field label (tried on 158 fields, reverted) | Docs said only "read-only"; it renders `ui:Formatted` without label | catalog gap (fixed since: widgets.md) |
| Users keep the old vertical drawer after the menu switch | Layout stored in localStorage `<model>-config` | catalog gap (fixed since: ui-hooks.md) |
| Step checkout is custom inside the cart page; generated checkout dialog stays | Hiding a generated action needs a `hiddenBy` flag; extra routes need `.generator-ignore` | builder decision, documented |
| `ACCESS_TOKEN_EXPIRED` in long E2E tests | Token renewal in e2e undocumented | catalog gap (fixed since: e2e troubleshooting.md) |

## Catalog update before Round 16
- agent-docs got 277 verified corrections and additions (commit 272b6fc on judo-blueprint `feature/remove-fragments`), incl. the R0–R15 build gaps (URLs, schema migration without wipe, CLI jar after generate, fill, table hooks, E2E names, i18n). The builder's kb reads the catalog folder directly, so it sees the new text after reindex.

## R16 Review (catalog compliance, no code changes) — %d %b %H:%M
- 23 webshop issues (2 bug, 10 risk, 7 deviation, 4 style), 10 catalog issues; REVIEW-R16.md in webshop root, uncommitted.
- kb share 42/106; 9/21 kb_get misses: breadcrumbs built from the condensed parent line (kb output issue; skill note added).
- Session discarded leftover unsaved CLI model edits from the aborted R16 build.
