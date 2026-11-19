# Webshop build session: validated gap analysis

Source: pi session `01a1caee` (webshop build in `~/Projects/webshop-test`, 2026-11-11 14:06 to 2026-11-12, Rounds 0 to 15), mined by 10 parallel miners, validated by 9 validators, then checked mechanically (session line, file, commit and catalog-path existence). Raw data: `target/gap-analysis/validated/*.jsonl`.

**How to confirm:** tick `Issue` if you agree it is real, then tick ONE action: `add` (new catalog entry), `modify` (change an existing catalog file), `one-off` (no catalog change), `ticket` (judo-ng platform issue), `tool` (CLI/skill/tool fix), or `drop`. The pre-ticked suggestion is shown as **Proposed**.

## Summary

- **Mined:** 426 claims (issues, platform claims, GAPS.md items); 152 merged as duplicates, leaving **277 distinct items**.
- **Validator verdicts (distinct):** confirmed 186, partly 71, refuted 10, unverifiable 10.
- **Proposed actions (excluding refuted):** modify-catalog 129, one-off 60, no-action 37, platform-ticket 27, tool-fix 8, add-catalog 6.
- **Mechanical checks:** every distinct item cites a session line or a GAPS.md entry; 8 had a weak keyword match on the cited line and were spot-checked by hand (the events are real, a few line numbers are off by up to ~50 lines). 32 items proposed `add` for a file that already exists; they are relabelled `modify` (add a section).
- **Validation depth caveat:** validators replayed session lines only on samples; CLI claims could not be checked against source (no CLI source in `target/judo-ng-read`). Treat `partly`/`unverifiable` as needing your call.

## What the session built

| Commit | Round / content |
|---|---|
| `65b7478` | chore: acceptance list (FUNCTIONS.md) and kb setup |
| `5f2e8d9` | S01: project scaffold from ESM fullstack template (create-judo-project), CLI jar |
| `b1c6f91` | S01: shop frame model (Shop actor, Product, ProductInfo), build + login to home verified; dbtype=postgresql, keycloak_port=8280 |
| `e3ce424` | S04: price column shows 2 decimals (patched generated table component, listed in module .generator-ignore) |
| `ce23ca9` | Level 0 done: TRACE.md, GAPS.md |
| `56f6695` | Level 0 follow-up: seed script for dev user, Back verified, GAPS/TRACE updated |
| `4c8fe35` | FUNCTIONS.md: frontend quality bar and Level 0 custom components (S07–S11) |
| `fcc7cc4` | Round 1: price display via customImplementation (form, view), S04 patch reverted, table column skipped (generator bug), gaps logged |
| `b69df6a` | Round 2: E2E module + Playwright tests for S04/S09, price label via derived attribute, PriceField edit fix, screenshots |
| `612e64c` | Round 3: Trail Shop branding, labels, bottom bar, seed descriptions test, new E2E tests; field order open (R3-1) |
| `2861a02` | Round 4: Group workaround for field order tried (no effect), GAPS R3-1 rewritten as platform bug |
| `b7cfad3` | Round 5: catalog card grid home (S08), custom product details layout (S10), groups removed, field-order test marked fail, new tests |
| `4561e67` | FUNCTIONS.md: build all levels without a review stop |
| `836c3d6` | Round 6: Level 1 (F01-F08): Category, SKU, Unit enum, bidirectional relation, admin tables/filters, seed + E2E tests |
| `30914f0` | Round 7: Level 2 (F09-F16): images, variants, derived stock status and category, actors Admin and Customer, JIT customer rows, active filter, own addresses; F08 inline table; F07 category filter |
| `a926eee` | Round 8: drawer fix, ShopProductInfo (no admin data for customers), admin table at 1440, Level 3 (F17-F24): cart, checkout, orders, stock transaction, order numbers |
| `66ec7a7` | Round 9: profile name + menu order hooks, Level 4 (F25-F32): order state machine, history, cancel with stock, active switch, delete-or-deactivate, 30 day order list |
| `5131c2b` | Round 10: history order + read-only ordered, Level 5 (F33-F40): settings, VAT, shipping, coupons, sale price, low stock, invoice PDF, Hungarian UI |
| `f0e9a72` | Round 11: Ordered time zone + field order, Level 6a (F41-F47): wishlist, reviews, rating, CSV export/import, notifications, invite admin |
| `659e439` | Round 12: header/breadcrumb/wishlist price fixes, Level 6b (F45, F48-F54): bulk price change, dashboard, returns, audit log, branding decision, migration with data (2x), integration tests, CI checkout |
| `37610d9` | Round 13: Level 7 B2B (F55-F61), migration without wipe |
| `8fd2635` | Round 13: smoke tags, F49 order lookup by filter, GAPS R13, report |
| `d07ed07` | R14 WIP: Level 8 model, services, migration (data kept) |
| `51df7b9` | R14 WIP: Level 8 services, ITs, spec, UI labels, ownership interceptor |
| `2cadb05` | R14 WIP: paused for UI overhaul |
| `e35dddd` | Round 15: storefront UI overhaul (top bar, grouped menu, hero/categories/search, cart counter, checkout steps), Level 8 finished (F62-F70), specs updated |

Per function (from the miners' `built` records):

| Round | Functions | What | Catalog used |
|---|---|---|---|
| R0 | S01 | Project scaffolded from the ESM fullstack template, CLI jar obtained, shop frame model built, app built and started, login to the shop home page verified in the | `build-process.md`, `local-development.md`, `judo-cli.md` |
| R0 | S02 | Product entity with name (String), description (LongText) and price (Price, NumericType scale 2). Product form shows Price, Name and Description. | `type.md`, `judo-cli.md`, `ui-authoring-guide.md` |
| R0 | S03 | ProductInfo transfer object on the Shop access (createable, updateable). Create and update checked by REST: Running shoe 89.90 changed to 79.90, plus Trail back | `accesspoint.md`, `entity-crud-at-service-layer.md`, `advanced-modeling-patterns.md` |
| R0 | S04 | Product list (table) shows name and price. Price column shows two decimals after the generated table was patched and rebuilt. | `tables-navigation.md`, `table-hooks.md` |
| R0 | S05 | Product view and edit page shows name, price and multi-line description. Back verified only after in-app navigation (list, row, view, Back). | `breadcrumb-navigation-context.md`, `navigation-and-access.md`, `writing-tests.md` |
| R0 | S06 | Data persisted across ./judo.sh stop and start: products still listed after restart (Running shoe 79.9, Wool socks, Trail backpack). | `local-development.md`, `build-process.md` |
| R1 | S04, S09 | Reverted the S04 patch (generated table component and .gitignore/.generator-ignore restored from b1c6f91) and regenerated through the frontend build. | `build-process.md` |
| R1 | S09 | Shared price component src/custom/components/Price.tsx (formatPrice to 2 decimals plus EUR, read-only Price, editable PriceField); form and view price fields on | `advanced-patterns.md`, `custom-visual-element-override.md`, `extension-points.md` |
| R2 | S04, S09 | Table price column shows 'NN.NN EUR' through a derived String attribute priceLabel on ProductInfo (getter self.price!round(2)!asString() + ' EUR'); the plain pr | `literal-derived-attribute.md`, `model-development.md` |
| R2 | S04, S09 | E2E module enabled (generateE2eModule=true) and Playwright suite tests/price-display.spec.ts (list, details, edit with restore, create form with Back), run with | `README.md`, `writing-tests.md`, `helpers-reference.md` |
| R3 | S07 | Trail Shop look set in the model: ActorType Shop applicationTitle 'Trail Shop', applicationLogo trail-shop-logo.svg (SVG in public/), seven colour attributes; s | `theming.md`, `ui-hooks.md`, `custom-public-assets.md` |
| R3 | S11 | Labels: menu item Products, list page Products, details and create Product, ShopUserInfo table Profile (model labels), and the phone bottom bar 'More' through t | `i18n.md`, `i18n-generator-override-extra-fragment.md`, `judo-cli.md` |
| R3 | S02, S03 | Real 2 to 3 line descriptions for the 3 products entered through the UI in a Playwright seed test (a-seed-descriptions.spec.ts), no SQL. | `writing-tests.md` |
| R5 | S08 | Catalog card grid as the shop home (CatalogHome): image placeholder, name, shared Price, first line of the description; 1/2/3-4 columns at 375/768/1440; loading | `extension-points.md`, `data-hooks.md`, `navigation-and-access.md` |
| R5 | S10, S11 | Product details layout (ProductDetailsLayout): large name, price badge via shared PriceField, full description, in that order; edit still works through storeDif | `advanced-patterns.md`, `custom-visual-element-override.md` |
| R6 | F01 | Category entity, CategoryInfo transfer object, categories access (create, update, delete), Categories menu, generated table, form and view; commit 836c3d6. | `structure.md`, `accesspoint.md`, `judo-cli.md` |
| R6 | F02 | sku (SKU type with regExp and maxLength 20), unit (Unit enumeration PIECE/KG/LITRE), and a category relation on Product; shown in product form, view and table;  | `type.md`, `ui-authoring-guide.md`, `widgets.md` |
| R6 | F03 | name and sku and unit required (required=true); save without SKU shows Missing required attribute. | `structure.md` |
| R6 | F04 | sku as identifier attribute on Product; duplicate SKU rejected in create dialog, dialog stays open with error. | `structure.md`, `AGENTS.md` |
| R6 | F05 | SKU type regExp ^[A-Z]{2}-[0-9]{4}$ and maxLength 20; ab1234 rejected. | `type.md` |
| R6 | F06 | Unit enumeration with PIECE, KG, LITRE; form dropdown shows 3 options. | `type.md` |
| R6 | F07 | Product table with Name, SKU, Unit, Price and Price (number) columns, filters Name, SKU, Unit, Price (number), numeric sort and paging tests. | `tables-navigation.md`, `ui-authoring-guide.md` |
| R6 | F08 | Product.category and Category.products as a two-way relation (ASSOCIATION both ends); category view lists its products, product links back to category. | `bidirectional-relation.md`, `structure.md` |
| R7 | F09 | Product image: ProductImage BinaryType (PNG, JPEG, 2 MB) on Product.image; seed uploads a PNG per product; customer grid and details show it; admin shows the fi | `type.md`, `filestore-mediated-file-transfer.md`, `binary-blob-url-hook.md` |
| R7 | F10 | Variant composed in Product (label, SKU, stock), inline table on the admin product view, stored with Update; customer front hides the variants table; commit 309 | `composition-ownership.md`, `ui-authoring-guide.md` |
| R7 | F11 | stockStatus DERIVED string (Out of stock, Low, In stock) from stock; shown in admin table and both details pages; nothing stored; commit 30914f0. | `model-development.md`, `conditional-visibility-getter.md` |
| R7 | F12 | ProductInfo.categoryName DERIVED from self.category.name; labelled Category; column and filter in the admin table; test.fail() removed; commit 30914f0. | `derived-attribute-flattening.md` |
| R7 | F13 | Customer sign-up through Keycloak registration page, CustomerProvisioningInterceptor creates the CustomerAccount on first customer login, seed script for keyclo | `keycloak-jit-user-provisioning.md`, `authentication-guide.md`, `managed-actor-admin-pattern.md` |
| R7 | F14 | Two actors: Admin (back office, /webshop/Admin) and Customer (shop front, /webshop/Customer) with their own principals, claims, accesses, menus and generated mo | `BLUEPRINT.md`, `dual-actor-frontend-architecture.md` |
| R7 | F15 | Customer products access filtered to active products (Product!filter(p \| p.active)); admin access unfiltered; commit 30914f0. | `derived-access-filtering.md` |
| R7 | F16 | Customer profile singleton by email from token; own addresses via container back-reference getter; customer 1 and 2 never see each other's addresses; commit 309 | `container-back-reference.md`, `derived-access-filtering.md` |
| R7 | F08 | Footwear category page lists its products in an inline table (representationComponent table on CategoryInfo View_Edit), no Products button; commit 30914f0. | `ui-authoring-guide.md` |
| R8 | F17 | Add to cart on product cards and details page, via bound custom operation addToCart (Java, customer found by ACTOR email, DAO access); button disabled when out  | `custom-operations.md`, `data-access-guide.md` |
| R8 | F18 | Adding the same product again increases the quantity of the existing cart line; the operation re-fetches the entity. | `entity-re-fetch-pattern.md` |
| R8 | F19 | Cart line total (quantity times price), cart total and line count derived in the model; empty cart shows 0.00 EUR; cart page in the Customer menu uses the share | `null-safe-collection-aggregation.md` |
| R8 | F20 | Quantity above stock throws the modeled ShopFault from addToCart; the UI shows a readable snackbar with the stock count and what is already in the cart; nothing | `error-handling-guide.md`, `error-handling.md` |
| R8 | F21 | Checkout asks for a shipping address (CheckoutInput transfer object), creates the order from the cart, empties the cart and opens the new order via the dialog a | `operation-output-with-behaviors.md`, `operation-return-type-navigation.md`, `action-hooks.md` |
| R8 | F22 | Order lines copy product name and unit price at order time (snapshot fields on SalesOrderLine and OrderLineInfo); later price changes do not affect the order li | `quote-lines-with-price-modifiers` |
| R8 | F23 | Checkout decrements stock per line inside the one operation transaction; a test proves the rollback (stock restored, cart kept, no order) when a later line fail | `platform-behavior-reference.md`, `custom-operations.md` |
| R8 | F24 | Order numbers WS-year-six digits from the SalesOrder platform sequence (VariableResolver SEQUENCE); test checks consecutive numbers. Admin gets a read-only Orde | `sequence-based-identifier.md`, `platform-behavior-reference.md` |
| R9 | F25 | F25 order status NEW to PAID to SHIPPED to DELIVERED or CANCELLED: OrderStatus enum and one custom operation per transition on AdminOrderInfo (Pay, Ship, Delive | `enum-state-machine.md`, `custom-operations.md` |
| R9 | F26 | F26 only valid transitions are offered: derived hide booleans feed hiddenBy on each action; invalid moves refused with INVALID_TRANSITION fault. | `enum-state-machine.md`, `operation.md` |
| R9 | F27 | F27 customer cancels an own NEW order; ownership and state checked in Java; cancelling returns the stock. Admin can also cancel PAID orders. | `role-guarded-write.md` |
| R9 | F28 | F28 product active switch (toggleActive operation); deactivated products are hidden from the shop. | `BLUEPRINT.md`, `soft-delete-active-flag.md` |
| R9 | F29 | F29 delete of a product with orders deactivates it and shows a message; without orders it is deleted; generic delete switched off; cart lines of a deleted produ | `guarded-delete-with-deactivate-fallback.md` |
| R9 | F30 | F30 tracking number is required only in the ship dialog and checked again in Java; it is shown on the order only for SHIPPED and DELIVERED. | `conditional-field-validation-hook.md` |
| R9 | F31 | F31 order status history: each transition writes a history row (who, what, when) in the same transaction; admin order view lists the rows. | `BLUEPRINT.md`, `interceptors.md` |
| R9 | F32 | F32 Orders (30 days) is a derived access (orderedAt later than now minus 30 days); All orders keeps older orders reachable. Cut-off itself untested. | `derived-access-filtering.md`, `model-development.md` |
| R9 |  | Round 9 fixes: drawer profile name (CustomHeroPropsHook), menu order by title (MenuItemsCustomizerHook), and DAO docs read before the Java. | `ui-hooks.md`, `data-access-guide.md` |
| R10 | F31 | F31 history sorted oldest first and Ordered shown read-only as derived text (orderedAtLabel) on both order views. | `tables-navigation.md`, `ui.md` |
| R10 | F33 | F33 shop configuration singleton (ShopConfig): shop name, free-shipping threshold, shipping fee, low-stock threshold, default VAT; admin menu Shop settings. | `BLUEPRINT.md`, `singleton-entity.md` |
| R10 | F34 | F34 VAT rate per category; cart and order show goods, discount, net, VAT, shipping and total; order keeps per-line VAT. | `aggregated-stored-field.md`, `null-safe-collection-aggregation.md` |
| R10 | F35 | F35 flat shipping fee below the free-shipping threshold read from the singleton in a derived expression; free at or above it. | `BLUEPRINT.md` |
| R10 | F36 | F36 coupons: admin Coupons menu; customer applies or removes a code in the cart; five distinct refusal messages; re-checked and counted at checkout. | `injectable-business-clock.md`, `error-handling-guide.md` |
| R10 | F37 | F37 sale price with a date window on the product; cards show sale price, struck-through regular price and a Sale chip; cart and order use the sale price only in | `injectable-business-clock.md`, `model-development.md` |
| R10 | F38 | F38 low-stock list for the admin: derived access filtered by stock below the settings threshold; changing the threshold changes the list. | `derived-access-filtering.md` |
| R10 | F39 | F39 invoice PDF on paid, shipped and delivered orders for customer and admin; PDF opens inline in a dialog; test checks the PDF content. | `handlebars-email-template.md`, `filestore-mediated-file-transfer.md`, `pdf-preview-inline-display.md` |
| R10 | F40 | F40 English and Hungarian switch in the header of both actors; shared Price component formats with Intl (79,90 EUR in Hungarian); menus, buttons and cart labels | `i18n.md`, `ui-hooks.md` |
| R11 | F41 | Wishlist: many-to-many Customer.wishlist and Product.wishedBy, add from product page, My wishlist with Move to cart and Remove. | `bidirectional-relation.md` |
| R11 | F42 | Review entity owned by Product; write action hidden for non-buyers and after the first review; operation rechecks buyer and 1-5 range. | `role-guarded-write.md` |
| R11 | F43 | Derived averageRating, reviewCount and ratingLabel on Product, shown on product page, shop cards and admin table; no reviews shows nothing. | `null-safe-collection-aggregation.md` |
| R11 | F44 | Orders CSV export (filters status and ordered from/until) and products CSV import (all rows checked first), each as a custom operation with a file. | `bulk-csv-import-export.md`, `filestore-mediated-file-transfer.md` |
| R11 | F46 | Notification entity, written inside Ship order; header bell with unread count; inbox sorted newest first; markRead custom operation marks read. | `notification-entity-pattern.md`, `read-tracking-postcall-interceptor.md` |
| R11 | F47 | Admins page with Invite admin; e-mail trimmed, lower-cased and validated; duplicate invite answers already an admin. | `managed-actor-admin-pattern.md`, `email-normalization-at-invite.md` |
| R12 | F52 | Migration with data: weight (backfilled 500) and ShopConfig.returnWindowDays (backfilled 14) in migration 1, then a second migration adding stored soldUnits wit | `schema-evolution.md`, `migration-backfill-default-where-null.md` |
| R12 | F45 | Bulk price change: a Change prices row action on each category (instance operation with a percent input), one transaction, 2-decimal rounding, rejects 0, -100 o | `custom-operations.md`, `backend.md`, `action-hooks.md` |
| R12 | F48 | Admin dashboard: DashboardInfo over the settings row with orders today, revenue today (cancelled excluded, shared price format), and top 5 best sellers by store | `aggregated-stored-field.md`, `model-screen-layout.md`, `custom-visual-element-override.md` |
| R12 | F49 | Returns: ReturnRequest owned by the order line (REQUESTED to APPROVED or REJECTED), window from delivery plus ShopConfig.returnWindowDays (default 14), approval | `enum-state-machine.md`, `composition-ownership.md`, `role-guarded-write.md` |
| R12 | F41 | Wishlist page uses the shared Price component ('12,00 EUR' in Hungarian), with loading, empty and error states, Move to cart and Remove through the generated se | `custom-visual-element-override.md` |
| R12 | F40, F46 | Notifications header: the bell navigates with clearNavigate so the breadcrumb reads Home, and AppBarExtras wraps the language switch and the bell in one flex ro | `breadcrumb-navigation-context.md`, `ui-hooks.md` |
| R12 | F50 | Audit log: one row per changed product field (who, what, old and new value), read-only audit page; unchanged fields create no row; bulk price change rows appear | `backend.md`, `interceptors.md` |
| R12 | F53 | Order lifecycle integration tests in a hand-written module application/order-tests: 8 tests (new to paid to shipped to delivered with history, refused steps cha | `getting-started.md`, `advanced-patterns.md`, `backend.md` |
| R12 | F54 | Checkout E2E test (two products, address required, order shows cart total) in CI mode: playwright.ci.config.ts with retries and workers from the catalog, headle | `troubleshooting.md`, `README.md` |
| R13 | F55 | Companies, members, invitations with key, join by key, company admin invite and role change; the level 7 test for F55 passed. | `BLUEPRINT.md`, `BLUEPRINT.md`, `BLUEPRINT.md` |
| R13 | F56 | Company price list with Product.companyPrices; the shared Price component shows the company price, a company without a list sees the list price; the level 7 tes | `derived-access-filtering.md`, `BLUEPRINT.md` |
| R13 | F57 | Quantity price tiers (Product.tiers, PriceTierInfo) with unit price switching at 10 and 50; the level 7 test passed. | `BLUEPRINT.md` |
| R13 | F58 | Checkout branches to PENDING_APPROVAL when the order exceeds the remaining credit; the test passed in the level 7 run with six passing. | `approval-workflow-pattern.md`, `null-safe-collection-aggregation.md` |
| R13 | F59 | Approve and reject operations via ApprovalService; negative test (buyer cannot approve own order) passed in the level 7 run. | `approval-workflow-pattern.md` |
| R13 | F60 | Quote and QuoteLine with request a quote from the cart, admin discount and offer, convert to order; the quote test passed after many test fixes. | `BLUEPRINT.md` |
| R13 | F61 | Purchase order number on SalesOrder and checkout input, required when the company sets poRequired; column added by migration. No separate test result seen in th | `schema-evolution.md` |
| R13 | F55 | Companies and members inside the Customer actor, invitation with a key shown in the open-invitations table (no mail server); Level 7 spec passes. | `user-with-organization-and-role`, `organization-entity`, `BLUEPRINT.md` |
| R13 | F56, F57 | Company prices and quantity tiers shown through the shared Price component in cards, cart and order; Level 7 spec passes. | `quote-lines-with-price-modifiers`, `BLUEPRINT.md` |
| R13 | F58, F59 | Credit limit and approval workflow: over-limit orders await approval; buyer has no Approve button; approver cannot approve own order. | `approval-workflow-pattern.md`, `role-guarded-write.md` |
| R13 | F60 | Quotes: buyer requests, admin discounts and offers, buyer converts once at quoted prices. Requested and Order made read-only in round 14 (see issue c09-09). | `quote-lines-with-price-modifiers`, `enum-state-machine.md` |
| R13 | F61 | Purchase-order number on company orders; the rule is enforced in the checkout operation (PO required blocks checkout). | `sequence-based-identifier.md` |
| R13 | F49 | F49 test fixed: admin order lookup by number filter instead of first page (test only, no product change). |  |
| R14 | F62 | Seller role: apply, admin approve or reject, seller products with publish and unpublish, ownership guard; F62 test passes after the assertion change. | `BLUEPRINT.md`, `derived-access-filtering.md`, `interceptors.md` |
| R14 | F63, F64, F66 | One checkout from three sellers creates one order and three sub-orders in one transaction; order status derived from sub-orders; seller ledger entries. Five int | `composition-ownership.md`, `BLUEPRINT.md`, `enum-state-machine.md` |
| R14 | F65 | Commission per category (CategoryInfo.commissionPercent), per-line commission rounded half up in the Money helper; seller payout equals sub-order total minus co | `BLUEPRINT.md`, `type-system-guide.md` |
| R14 | F67 | Partial refund of one sub-order line: stock returned, REFUND ledger entry and proportional commission reversal; browser test passes in the last run. | `custom-operations.md` |
| R14 | F68 | Currency switch (EUR, USD, HUF) in the header; prices converted by the shared Price component from the newest rate; missing rate shows a notice. Admin can enter | `BLUEPRINT.md` |
| R14 | F69 | Gift cards bought by the customer, code shown once, partial redemption over two orders, balance never below zero; buyGiftCard is a void operation. Browser test  | `platform-behavior-reference.md` |
| R14 | F70 | Loyalty points earned on DELIVERED (400 points per 1000 EUR), spent at checkout (10 points equal 1.00 EUR); browser test FAILS at the end of the chunk (amount d | `BLUEPRINT.md` |
| R15 | F40 | Language switch kept in the header through the AppBarExtras wrapper (EN/HU). | `ui-hooks.md`, `i18n.md` |
| R15 | F46 | Notification bell kept in the header with the unread count from the profile. | `ui-hooks.md` |
| R15 |  | Storefront overhaul: top bar with cart counter and search box, grouped menu, home hero and category chips with sort, card grid, category filter, four-step check | `accesspoint.md`, `ui-hooks.md`, `extension-points.md` |
| R15 | F62, F63, F64, F65, F66 | Level 8 marketplace spec F62 and F63-F66 pass (6 tests in level8 pass after helper and fixture fixes). | `e2e-testing` |
| R15 | F69, F70 | Level 8 gift card (F69) and loyalty points (F70) tests pass on run-local products. | `e2e-testing` |
| R15 | F21, F22, F24, F59 | Smoke suite (--grep @smoke) passes 7 of 7 after helper and fixture fixes (showAllRows, F59 orders 30 units). | `e2e-testing` |

Key design decisions:

- **R0 S01:** Ran create-judo-project in /tmp/gen and copied the output into ~/Projects/webshop-test. *Why:* The target folder already held FUNCTIONS.md and git history. The catalog does not say whether create-judo-project may run in a non-empty repo or which folder to use.
- **R0 S04:** Patched one generated table component to use min and max fraction digits of 2, and listed the file in the frontend module .generator-ignore. *Why:* No model-level or documented hook produced 2 decimals, and the builder judged a one-file patch the quickest path to S04.
- **R0 S03:** Modelled the shop login as EntityType ShopUser (username is identifier), a ShopUserInfo transfer object mapped to it, and ActorType Shop with principal ShopUserInfo and managed=false. *Why:* Managed auto-insert is not implemented in this runtime (advanced-modeling-patterns), so the principal row must come from elsewhere.
- **R0 S02:** Price is a NumericType with precision 12 and scale 2. LongText is a StringType with maxLength 4000. Product has name, description and price members. *Why:* Price needs two decimals; the predefined Text type is too short for a description.
- **R0 S01:** Set dbtype=postgresql and keycloak_port=8280 in judo.properties, and committed them. *Why:* Local-development says the default is PostgreSQL in Docker, and port 8080 was taken.
- **R0 S01:** Wrote scripts/seed-dev-user.sh (idempotent Keycloak user shop/shop plus the ShopUser row) instead of building a JIT AuthenticationInterceptor, because the interceptor adds backend code beyond Level 0. *Why:* Level 0 scope. The JIT best practice explains the interceptor, but the builder judged it out of scope.
- **R0 S03:** Checked S03 create and update with curl REST calls rather than the browser form. *Why:* Browser form did not commit numeric input (see c01-23). The later user rule asked for checks only at the end.
- **R1 S09:** For the shared price component the only registration point the kb documents is the generated src/custom/application-customizer.tsx. The builder asked the user before editing that generated file and adding it to .generator-ignore, which the quality bar forbids without asking. The user approved. *Why:* The quality bar forbids editing generated files; the kb documents no other registration place for custom visual elements.
- **R1 S09:** Built a shared price component in src/custom/components/Price.tsx (formatPrice gives two decimals plus EUR, e.g. 79.90 EUR). Registered it for the form and the view through application-customizer.tsx, which was added to .generator-ignore. The table column was skipped, logged in GAPS R1-1, and kept on customImplementation=false. *Why:* Table column hook could not be used (generator bug, see c02-04 and c02-09). Form and view could use the model flag plus CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY.
- **R2 S04, S09:** Orchestrator directed that every browser check be a Playwright E2E test (login, menu, list, details, edit, back), with screenshots at 375, 768 and 1440 px. Table currency stays a logged gap unless a documented non-generated route appears. *Why:* Browser tool click delivery failed; E2E is the JUDO check method in agent-docs/e2e-testing.
- **R2 S04:** For the table price column, the builder chose a derived String attribute priceLabel on ProductInfo, getter self.price!round(2)!asString() + ' EUR', added as a DataColumn with fill --pages table, and removed the plain price column from the table. This puts the currency into the list without patching a generated file. *Why:* Column hook could not be used (c02-04). Kb search for a non-generated route led to derived attributes (literal-derived-attribute.md and the JQL function list in model-development.md).
- **R3 S07, S11:** Shop look is set in the model, not in patched files: ActorType Shop gets applicationTitle 'Trail Shop', applicationLogo trail-shop-logo.svg (SVG placed in public/) and the seven colour attributes (primaryColor, secondaryColor, backgroundColor and others). Labels are set on the model elements: menu item Products, page containers Products and Product, Profile for ShopUserInfo. *Why:* kb says ActorType colour attributes and applicationLogo are the model route for brand palette and logo (theming.md, custom-public-assets.md), and the generated palette and logo follow from them.
- **R3 S07:** Small logo for the collapsed drawer is a CustomLogoPropsHook registered in src/custom/hooks/registerShopLogoHook.ts through application-customizer.tsx (already generator-ignored). The wide logo and title come from the model (applicationLogo, applicationTitle). *Why:* ui-hooks.md documents the logo customization hook; the generated useLogoProps.ts does not expose the icon otherwise.
- **R5 S11:** Orchestrator decided the two field-order tests stay in the suite but are marked test.fail() with a comment naming the platform bug, so the suite is green with a known failure. Wrapper groups from Round 4 are removed again. *Why:* Field order cannot be fixed by the model until the platform bug is fixed; the tests should document the gap, not block the suite.
- **R5 S10, S11:** Builder marked only the create-form field-order test with test.fail(), not both as the orchestrator asked, because the details order test passed once the custom layout was in place. test.fail() on a passing test would have turned the suite red. *Why:* Deviation from the round text, justified by the test result; disclosed in the report.
- **R5 S08, S10:** Home is a card grid (CatalogHome) registered on the DashboardPage seam. It feeds ShopServiceForProductsImpl.list with the generated query customizer and navigates through routeToShopProductsAccessViewPage. The details layout (ProductDetailsLayout) uses the shared PriceField and a multi-line description, through a custom implementation on the name field. *Why:* No documented hook for a whole view or a home replacement; generated services and navigation are the documented way to fetch data and move between pages.
- **R6 F07:** Category shown on the catalog card through a nested mask {name,price,description,sku,category{name}} in the list call, with a Chip for the category and a caption for the SKU. *Why:* A nested mask returns the related category name in one list call; no extra request per card.
- **R6 F01, F02:** Seed data built through the UI helpers (fillEnumCombobox, fillSingleRelationElement) in helpers-shop.ts: 3 categories and 8 products via real user actions. *Why:* Checks and seeding must use real user actions only; the e2e helpers encode the Playwright patterns.
- **R7 F08:** Category Products shown as an inline to-many table on CategoryInfo View_Edit (representationComponent=table, with name, sku, priceLabel, unit columns) instead of the Products button, as the Round 7 correction asks. *Why:* FUNCTIONS.md asks for an embedded table; a to-many relation on a view renders as an embedded table in the catalog pattern.
- **R7 F09:** Product image modelled as a BinaryType ProductImage (mime types image/png and image/jpeg, max 2 MB) on a STORED Product.image member. *Why:* Binary types need a MIME list and a size limit; the attachment blueprint says a binary field on a create-capable transfer gets a generated upload operation.
- **R7 F13, F14:** Rename the actor Shop to Customer and the entity ShopUser to CustomerAccount with email as the claim attribute, keeping the mapped principal transfer object; the Admin actor is the second actor. *Why:* Actor split needs distinct actors with their own principals and accesses; rename keeps the existing wiring.
- **R7 F11, F12:** Stock status is a DERIVED string with a ternary getter (stock <= 0 gives Out of stock, below 5 gives Low, else In stock); category name is a DERIVED flattening self.category.name. *Why:* Derived attributes compute from the model without storing; ternary getters are typed switch expressions in JQL.
- **R7 F14:** Admin actor added as a second actor with its own principal AdminAccountInfo (managed=false), branding copied from the shop, an EMAIL claim, products and categories accesses, and two menu entries. *Why:* Each actor needs its own principal, claim and accesses; the Admin keeps the back office and the Customer keeps the shop.
- **R7 F13:** Customer account created on first login by a custom AuthenticationInterceptor (CustomerProvisioningInterceptor) in the interceptors module; admin accounts are seeded on purpose, not created on login. *Why:* Runtime does not auto-insert the managed principal row, so a first-login interceptor is the documented route; interceptors module is custom code, not a generated file.
- **R7 F13, F14:** Seed script creates Keycloak users admin, customer1 and customer2, switches realm self sign-up on through the admin API, and seeds one AdminAccount row; customer rows are left to the first-login interceptor. *Why:* Keycloak users and database rows are two stores; sign-up needs a realm setting the model cannot express.
- **R7 F14, F15:** Level 0 webshop__shop frontend and e2e modules were removed from git and disk; their code was split into webshop__customer (shop front) and webshop__admin (back office) modules, with duplicated Price, CatalogHome and hook files. *Why:* The Customer actor takes over the shop front, the Admin takes the CRUD screens, and each actor has its own generated module.
- **R7 F09:** Product images: the seed uploads a generated PNG per product through the file chooser; the customer card grid and details page show the real image (placeholder only without one); the admin view shows the file name. *Why:* Binary upload through the generated create dialog is the documented route; display in the customer front needs the token download.
- **R7 F16:** Customer profile is a singleton CustomerAccount found by its email from the login token; addresses are a composition of CustomerAccount, listed by a container back-reference getter, so one customer sees only their own rows. *Why:* Ownership must be enforced in the model; the back-reference pattern avoids a stored foreign key.
- **R7 F15:** Customer products access filtered with Product!filter(p \| p.active) so inactive products are missing from the shop; the admin access stays unfiltered. *Why:* Visibility must be enforced in the access getter, not in the frontend.
- **R8 F21:** Checkout is a void operation. The new order opens through the generated dialog actions hook (postCheckoutForCartInfoAction, generateActionsHook=true), which lists the newest order and navigates to it. *Why:* Only route left after the duplicate-import generator bug (c04-13); it costs one extra list call and deviates from FUNCTIONS F21 (operation returns the created order).
- **R8 F20:** Stock overflow is a modeled fault (ShopFault with message) declared on addToCart; the UI reads the message through a custom error interceptor and shows it as a snackbar. *Why:* Modeled faults are the documented business-error route (error-handling-guide); the generated dialog cannot show the message (c04-15).
- **R8 F24:** Order numbers come from the platform SEQUENCE variable (WS-year-six digits), not from the gap-free document-registry-sequence blueprint; a refused checkout does not use a number, but a number can gap after a rollback or crash. *Why:* The blueprint needs a lock and a registry entity; the platform sequence is simpler and the builder accepted gaps as documented in platform-behavior-reference.
- **R8 F19:** The cart page is a custom component (Cart.tsx) that replaces the generated lines table and shows unit price, line total and total with the shared Price component; values come from the model's derived members (CartLine.lineTotal, CartInfo.total). *Why:* The generated lines table shows raw numbers (R1-1), and the Price component is the frontend quality bar from FUNCTIONS.md.
- **R9 F31:** History rows are written by OrderLifecycle.transition (actor = ACTOR e-mail, what = status change, when = now) in the same transaction; a refused transition writes nothing; checkout writes Order placed. *Why:* Custom operations never reach interceptors, and the audit blueprint says the operation itself must write the row.
- **R9 F26, F30:** Transition buttons are hidden with hiddenBy on derived booleans on the order (payHidden, shipHidden and so on); the tracking number is an input of the ship operation and is hidden on the order unless SHIPPED or DELIVERED; the server also refuses invalid moves. *Why:* Derived booleans give valid buttons without a frontend hook; the server check protects against stale UI.
- **R9 F25, F27:** Two order transfer objects: AdminOrderInfo (all transitions, tracking, history, customer e-mail) for the admin and OrderInfo (cancel on NEW only) for the customer. *Why:* Customer must never see admin buttons; same idea as the product split in R8.
- **R10 F36:** Coupon codes are stored on the cart as code plus percent (no relation), revalidated at checkout (clock, usage, minimum), and a use is counted in the checkout transaction; five distinct refusal codes. *Why:* Checkout must not accept a coupon that expired or was used up after it was applied; no relation keeps the cart simple.
- **R10 F36, F37:** BusinessClock class reads WEBSHOP_BUSINESS_DATE (env or system property) once at class load; checkout, order date and history use it; model expressions keep the platform clock. *Why:* Catalog pattern for one clock in Java; browser tests cannot change it, so tests use real dates.
- **R10 F39:** Least-bad invoice route: Handlebars Markdown template, own Markdown-to-PDF renderer on PDFBox, FileStoreService put, FileType output, inline PDF dialog; DOCX pipeline not used. *Why:* Project lead says DOCX/XDocReport is deprecated; kb has no runnable Markdown to PDF recipe.
- **R10 F40:** Hungarian application file is built by scripts/make-hu-translations.py as a new file (not a generated file), so no .generator-ignore entry; the script keeps every generated key and falls back to English. *Why:* Generator emits only en-US for this model; a new file with a new name needs no ignore entry.
- **R10 F34:** Product prices are gross (VAT included): VAT = gross x rate / (100 + rate), net = goods minus discount minus VAT; VAT rate per category with a default. *Why:* Shop prices shown to customers include VAT; net and VAT are derived from gross.
- **R10 F33:** Shop settings are one ShopConfig row entered through the admin UI by a seed test (no startup initializer), with create and update but no delete. *Why:* No documented startup trigger for an initializer (see c05-60).
- **R11 F46:** Notification read state is set by a custom operation markRead on NotificationInfo, called from the documented post-refresh page hook; the interceptor was removed. *Why:* Interceptor write was not persisted (c06-13); custom operations are not intercepted, so the operation is explicit.
- **R11 :** 'Ordered' is the real timestamp shown by a read-only custom LocalTimestamp component in the browser zone (customer and admin), formatted without 12-hour clock; the test checks it equals the 'Order placed' history row. *Why:* Browser zone display matches the generated history column; no model change needed.
- **R11 F44:** CSV export and import are custom operations that exchange the file through the file store; a small Csv helper quotes fields on write and parses on read; import checks all rows before creating any. *Why:* Matches the catalog bulk-csv pattern (file store, rows validated first).
- **R11 F47:** Invite admin is a custom operation that normalizes the e-mail (trim and lower case) and writes through the principal TO's DAO, so the managed realm sync applies; the TO keeps its own admin projection. *Why:* Managed-actor pattern: the sync is bound to the principal TO's DAO, not to the entity.
- **R12 F52:** F52 migration without a wipe: copy the pre-change RDBMS model and pg_dump first, generate the migration with the old model as base, hand-write the weight and returnWindowDays backfill in changeset 06, then execute. Products, settings and orders survived. *Why:* schema-upgrade cannot host the backfill, and the user asked for a documented route with no wipe.
- **R12 F45:** Bulk price change is an instance row action on the category table, not a static collection operation. *Why:* Static collection operations on shared tables hit a generator bug seen in R11 (R11-7c).
- **R12 F48:** soldUnits is a STORED aggregate kept by checkout, cancel and return approval, instead of a derived sum, so the dashboard can sort it. *Why:* Derived aggregates cannot be sorted (see platform-bug on F48 SQL). The catalog recommends stored aggregates.
- **R12 F49:** The Request return button exists only inside the window because a row action cannot be hidden per row (CLI rejects hiddenBy), so returnable lines get their own page. *Why:* The row action visibility property is not settable from the CLI (see cli-tool item on hiddenBy).
- **R12 F41:** Wishlist is a view page of a new TransferObjectType WishlistInfo (access Customer.myWishlist, 0..1) whose items element is a custom implementation, following the cart pattern. The generated wishlist access is kept for move and remove. *Why:* Column hooks and column customImplementation do not work (see the two platform-bug items).
- **R12 F51:** Shop branding (logo, title, primary colour) stays in the model. It is not read from the configuration singleton. A test checks logo and colour on five pages per app. *Why:* Theme colours are ActorType attributes and the logo and title are model elements, all applied at build time; editing palette.ts would need a .generator-ignore entry, which is forbidden.
- **R12 F50, F45:** Admin product edits are audited by a post-call interceptor on the built-in update, one AuditEntry per changed field in the same transaction; the bulk price change writes its own rows through an AuditLog service. *Why:* Built-in update is intercepted and custom operations are not, as the catalog says.
- **R12 F53:** Use a hand-written module (application/order-tests) with the generated pom copied and its i18n-api version filled in, instead of the generated integration-test module. *Why:* The generated module cannot be read by Maven (empty i18n-api version), and the root fragment override did not win.
- **R12 F46, F49:** Menu order of both apps is set by the documented menu customizer hook (customer registerShellHooks MENU_ORDER, admin registerMenuOrder by title), not by model order. *Why:* Model creation order put Returns to review first and Dashboard last; the hook is the documented route.
- **R12 F45, F44:** Add-to-message snackbar for operation replies: a documented post-operation hook shows output.message in the snackbar and then calls onSubmit, instead of the generated second dialog. *Why:* Operations answer with a short ShopMessage; the generated flow opens a second dialog showing it.
- **R13 F55:** Company members are CustomerAccount rows inside the existing Customer actor (company relation, companyRole BUYER or APPROVER, companyAdmin flag). No third actor. *Why:* One user has one organization and a small fixed role set, which is the user-with-organization-and-role case. A third actor would add a Keycloak client and a frontend module. B2C must keep working.
- **R13 F52, F55, F61:** Model changes went through the F52 migration route: pg_dump before the step, a base model from before the round, a generated migration, a hand-written backfill setting companyAdmin false on existing customers, then execute. No database wipe; 251 customer rows kept. *Why:* Orchestrator rule for every model change after round 12; a required new flag needs a backfill.
- **R13 :** User rule for all later rounds: a round runs its new spec plus --grep @smoke, serially, under about 10 minutes; both full suites run once at the very end. *Why:* Full-suite runs per round were too slow for the build loop.
- **R14 F62:** A seller is a role of the existing customer account (one actor, one login, one cart), not a third actor. An optional Seller row holds status PENDING, APPROVED or REJECTED; the admin approves. This deviates from the FUNCTIONS row, which asks for a third actor. *Why:* Catalog: multi-actor blueprint 'When to use' (a self-service actor sees only its own records) and 'When to avoid' (a difference that is only permission needs no copy per role); a real third actor costs a Keycloak client, acceptableClients entry, frontend module, e2e project and sign-up flow (authentication-guide).
- **R14 F62:** Ownership is enforced by SellerOwnershipInterceptor on refresh and update of the exposed transfer objects, plus ownership checks inside the custom operations. *Why:* Documented route: interceptors see refresh and update; InterceptorCallBusinessException refuses the call. Access filters alone do not stop a direct identifier.
- **R14 F65:** All money arithmetic goes through one Money helper: BigDecimal.valueOf of the stored double, scale 2, HALF_UP per line. Commission and payout are computed per line; hand calculations to the cent are written in the spec. *Why:* Price is stored as a decimal with scale 2; the generated SDK exposes money as Double, so rounding must be explicit.
- **R14 F68:** Base currency stays EUR everywhere; USD and HUF are display conversions from the exchange rate table (newest valid rate on or before today), with a notice when no rate exists. HUF is not stored, which deviates from the FUNCTIONS row. *Why:* Storing HUF would change every price, label and invoice; ExchangeRate rows are units per 1 EUR.
- **R14 F62, F63, F64, F65, F66, F67, F68, F69, F70:** Level 8 model change without a wipe: old model and pg_dump kept, schema generated with judo-rdbms-schema:generate against the base model, backfill for new required attributes written by hand in changeset 06 (Category.commissionPercent 10, line commission 0, refunded 0, gift card and points amount 0). Existing rows kept (10, 242 and 225 rows checked). *Why:* schema-upgrade (apply) gives no moment to write the backfill; generator adds new columns as nullable, so existing rows need explicit defaults.
- **R14 F69:** Gift card balance update carries the version of the row read, so two concurrent redemptions cannot both pass; the integration test shows a stale writer is refused. *Why:* Platform optimistic locking checks __version only when present in the payload.
- **R15 :** Round 15 starts by committing the uncommitted Level 8 work as 'R14 WIP: paused for UI overhaul' (2cadb05) and does not continue F62-F70 until the UI work is done. *Why:* Orchestrator instruction to stop feature work and make the UI overhaul the only goal.
- **R15 :** Admin stays the JUDO default. Customer look changes go through view changes of the transfer objects (UI model) and src/custom hooks; no admin tidying except the Quote fix. *Why:* Owner decision given mid-round ('admin can stay judo default use view changes to the view model of TOs').
- **R15 :** Live iteration loop: Vite dev server on port 5173 against the running Karaf backend on 8181 (VITE_API_DEFAULT_BASE_URL), edit src/custom with HMR, and batch UI-model changes into one generate-root plus 'build -f -i' (about 38 s) instead of full root builds. *Why:* Round brief requires fast iteration; the kb docs on the dev server, env variables and reckless/frontend-only builds were read first.
- **R15 :** Customer layout becomes a top bar by setting menuOrientation=HORIZONTAL on webshop::Customer in the model (CLI update), not by a template override. *Why:* accesspoint.md documents menuOrientation on the actor (VERTICAL or HORIZONTAL); this is the documented model route.
- **R15 :** Header extras (search box, language switch, currency switch, cart counter, notification bell, drawer expander) share the one AppBarExtraComponents slot through a single wrapper component AppBarExtras, with spaceRequired tuned to 4. *Why:* The generated header accepts exactly one AppBarExtra component (ui-hooks.md 'AppBar Extra Components').
- **R15 :** Storefront menu is regrouped by a MenuItemsCustomizerHook in registerShellHooks.ts (sorted by title, fixed order) so the drawer shows Products, Cart, My account, Company and Sell groups. *Why:* ui-hooks.md 'Menu Manipulation' documents the customizer hook; generated item ids are model ids so titles are used for ordering.
- **R15 :** Checkout becomes a four-step flow (address, delivery, payment, review) plus a confirmation page, built as a custom component (CheckoutFlow.tsx) on the cart page instead of a model Stepper; the new order is opened after the generated checkout operation succeeds. *Why:* Stepper in the UI mapping docs is described for forms; the operation flow is a custom implementation (custom-visual-element-override.md). registerCheckoutHook navigates to the newest order.
- **R15 :** No .generator-ignore entry and no extra route for a /checkout URL; the checkout flow is reached from the cart page only. *Why:* Standing rule forbids .generator-ignore entries; extension-points.md documents extra routes only through src/extra-routes.tsx, which needs an ignore entry to survive regeneration.
- **R15 F62, F63, F69, F70:** Level 8 specs buy a product created in the same run (shops[0].product) instead of the shared seed products Trail shoe and Trail mix, so repeated runs do not depend on seed stock. *Why:* Repeated runs had used up the seed stock; the old tests depended on it.

## A0. GAPS.md details lost in merging (added after the reconciler report)

The reconciler merged these GAPS.md items into claims that cover only part of them. The missing part is listed here so it is not lost.

#### G268 `gaps:L8` R0 S01: a login-capable actor needs a MAPPED principal; the catalog has no recipe for a working first user
- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify → `catalog/agent-docs/model/esm_metamodel/accesspoint.md` (or `deployment/local-development.md`): a minimal first-user recipe (mapped principal + Keycloak user + entity row). Merged into `c01-09`, which only covers `managed=true`.

#### G269 `gaps:R3-5` R3 S07: the logo file needs explicit `width`/`height`, or the generated `<img>` renders it wrongly
- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify → `catalog/agent-docs/frontend/theming.md`: add the SVG size requirement next to `applicationLogo`. Merged into `c02-37`, which lacks this detail.

#### G270 `gaps:R7-6` R7 F14: actor split duplicates custom code across actor frontends; no documented shared place
- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** add (open question): a best practice for custom code shared by actor frontends. It is marked *verify* in `catalog/best-practices/frontend/structure-cross-actor-shared-overrides.md`, and needs a JUDO developer answer. Merged into `c03-60`, which covers only the stale-directory removal.

#### G271 `gaps:R7-10` R7 F14: the field-order bug also hits details pages and dialogs, not only the create form
- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket (ETL esm2ui ordering, see `c02-40`): extend the ticket scope to details pages (Price above Name), the Variant dialog and the customer details page.

## A. Catalog changes (grouped by file)

### `catalog/agent-docs/model/judo-cli.md` (23)

#### G001 `c01-05` R0 S01: The CLI doc says the judo-cli.jar is downloaded by ./judo.sh build. In this generated project, generate-root did not create target/judo-cli.jar. Running mvn -DgenerateRoot validate did.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. judo-cli.md line 15 says ./judo.sh build downloads the jar; the root pom has a generateRoot profile (dependency:copy at validate) that does it. Add: if target/judo-cli.jar is missing run `mvn -DgenerateRoot validate` (the project has no mvnw).
- **Why:** The catalog describes the download as part of judo.sh build. The generated root pom has its own download-cli profile that runs on generateRoot, so the catalog is incomplete for the new-project case. **Workaround:** Ran mvn -B -DgenerateRoot validate, which copied target/judo-cli.jar.
- **Validation:** confirmed; kind catalog-wrong; catalog wrong. Evidence: `session:L32`, `session:L75`, `session:L76`, `session:L77`. Merged: c02-02, g-L2, g-R1-4

#### G002 `c01-07` R0 S02, S03: Mapping a TransferObjectType to an entity made the CLI auto-create members, forms, tables and views. The builder's hand-added DataMembers then failed validate --strict with binding and uniqueness erro

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. judo-cli.md `create` says it cascades view/form/table pages, but not that a TransferObjectType with a mapping gets its mapped members too. Add: do not hand-add members for a mapped TO; they exist, duplicates give BindingIsNotMappedByOtherMappedAttribute and NamedElementIsUniqueInItsContainer.
- **Why:** The catalog does not say that a mapped TransferObjectType creates its members and UI scaffolds, so the builder assumed it had to create them. **Workaround:** Discarded the unsaved edits and rebuilt the model without the hand-added MAPPED members.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L121`, `session:L122`, `session:L124`, `session:L125`. Merged: c03-47

#### G003 `c01-42` R0 S01: validate --strict failed with ExposedTransferObjectTableHasColumns (no columns on the viewable table). The fix was the fill command, which the builder found by trial.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. `fill <toFqn>` is in the command table (line 79) but not tied to the validator error ExposedTransferObjectTableHasColumns. Add: run fill (or add DataColumns) to clear it. Note R6 GAPS: fill also adds unwanted label fields and menu items.
- **Why:** The accesspoint doc states the rule, but the fill command is not in the judo-cli reference (openspec sweep item MO-172 lists it as missing). **Workaround:** fill webshop::ProductInfo --pages view,form,table.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L137`, `session:L138`, `session:L139`, `session:L140`. Merged: c03-06, g-L11

#### G004 `c01-43` R0 S01, S03: Tried create -t MenuItemAccess, which the CLI rejects because MenuItemAccess is created automatically for an actor's access.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. accesspoint.md has the Access to MenuItemAccess pairing rule but judo-cli.md does not say create -t MenuItemAccess is refused; add: create MenuItemAccess via the Access/actor menu flow (verify exact command).
- **Why:** Builder tried the create command on an auto-generated element. **Workaround:** Used create -t Access on the actor and let the CLI create the menu access.
- **Validation:** confirmed; kind builder-mistake; catalog partly-covered. Evidence: `session:L135`, `session:L136`

#### G005 `c02-03` R1 S09: ./judo.sh generate runs a clean that deletes target/judo-cli.jar. Every model edit made through the CLI jar after a generate fails with 'Unable to access jarfile'.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Not covered. Add: ./judo.sh generate cleans target and deletes judo-cli.jar; re-fetch it with `mvn -DgenerateRoot validate` before the next CLI call (or copy it outside target).
- **Why:** Generate wipes the target folder, and the jar lives there. The required order (fetch jar, change model, save, then generate and build) is not documented as a single sequence. **Workaround:** Re-fetched the jar before each model change and ran generate and build after the model was saved.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L1479`, `session:L1480`, `session:L1554`, `session:L1555`

#### G006 `c02-25` R2 S04: judo fill --pages table added unrequested DataColumns (description and priceLabel) and changed dataFeature on them. The builder had to delete the description column by hand.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Catalog says fill "creates and populates view/form/table from its members" but not that it adds a DataColumn for every transfer object member. Add: run fill --dry-run first; fill adds a column per member, delete unwanted DataColumns afterwards.
- **Why:** fill creates a column for every transfer object member, so the dry-run output had to be read before the real run. **Workaround:** Ran fill --dry-run first, then fill, then judo delete on the unwanted columns; the price column was removed on purpose.
- **Validation:** confirmed; kind cli-tool; catalog partly-covered. Evidence: `session:L1310`, `session:L1311`, `session:L1312`, `session:L1313`

#### G007 `c02-34` R3 S11: Model CLI element names and paths were guessed repeatedly: query ui MenuItem, Access, PageDefinition title, GraphQL menuItems and _type fields, and FQNs with the id: prefix all failed with 'does not e

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Catalog has the UI FQN rules and query syntax but no list of working type and field names for menus, accesses and pages. Add a short table of valid query esm types/fields for Access, MenuItemAccess, ActorType and page definitions, and note that FQNs must not carry the id: prefix unless using id:<xmi:id> form.
- **Why:** The CLI and GraphQL type and field names differ between query, create and graphql, and the catalog does not list the working names for the navigation and page elements. **Workaround:** Read the GraphQL schema with graphql queries, then used FQNs from the query output (e.g. webshop::Shop::Menu for the menu label, ProductInfo_Table label via webshop::ProductInfo::ProductInfo_Table).
- **Validation:** partly; kind cli-tool; catalog partly-covered. Evidence: `session:L1302`, `session:L1303`, `session:L1306`, `session:L1308`. Merged: c06-04, c08-03, c09-10

#### G008 `c02-39` R3 S11: judo move --dry-run printed the reordered element as 'changed ... description (in components)' rather than the element being moved, so the dry-run output was misread while reordering the form fields. 

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Not in catalog. Add: move --dry-run reports the sibling that shifted, not the moved element; check the order with a query and use discard --force to clear a wrong reorder.
- **Why:** The dry-run summary names the sibling that shifts, not the moved element, and the status output lists unsaved reorders by sibling. **Workaround:** Used move --json and graphql to confirm the child order, then discard --force and re-applied the move.
- **Validation:** partly; kind cli-tool; catalog missing. Evidence: `session:L1527`, `session:L1528`, `session:L1529`, `session:L1530`

#### G009 `c03-02` R6 F02: CLI query of TwoWayRelationMember failed: asking for field partner without a sub-selection returns SubselectionRequired.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Catalog query section gives no select syntax for reference fields. Add: a reference field needs a sub-selection, e.g. --select "partner{name}"; one-line example.
- **Why:** The query select syntax needs a nested selection for ref fields; builder did not know the syntax. **Workaround:** Builder queried fqn and primary only and used validate output instead.
- **Validation:** confirmed; kind cli-tool; catalog missing. Evidence: `session:L1773`, `session:L1774`, `session:L2038`. Merged: c05-19

#### G010 `c03-44` R7 F13: Renaming the username member to email with a new type left the mapped member on the actor info transfer object with the old type; validate warned the data type must match its binding.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. judo-cli.md covers rename keeping identity but not that a type change must also be applied to the mapped member on transfer objects. Add that line.
- **Why:** A rename plus type change must be applied to the mapped member too; the builder changed only the entity side first. **Workaround:** Renamed the mapped member in the same script step.
- **Validation:** confirmed; kind builder-mistake; catalog missing. Evidence: `session:L2059`, `session:L2060`

#### G011 `c04-17` R8 : After generate or build, target/judo-cli.jar disappeared, so every CLI call failed with 'Unable to access jarfile' until generate-root was run again.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. judo-cli.md line 15 says ./judo.sh build downloads target/judo-cli.jar; GAPS S01-2 shows neither build nor generate-root created it first time, and the session shows it missing after generate/build until generate-root ran again. State: restore with ./judo.sh generate-root (or mvn -DgenerateRoot validate) and check the jar exists before CLI calls.
- **Why:** generate and build do not recreate the CLI jar; only generate-root (or the validate goal) copies it. Known from earlier rounds (R7-7, S01). **Workaround:** Helper script .scratch/ensure-cli.sh runs generate-root when the jar is missing; used before every CLI step.
- **Validation:** confirmed; kind catalog-gap; catalog wrong. Evidence: `session:L2483`, `session:L2484`, `session:L2491`, `gaps:R8-12`. Merged: c07-44, g-R7-7

#### G012 `c04-07` R8 : The CLI query for DataColumn and DataFilter returned nothing until 'fill' had been run on the transfer object, so the builder first thought the table columns did not exist.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Catalog says DataColumn/DataFilter have no name and fill creates them, but not that they do not exist before fill. Add: query DataColumn/DataFilter returns nothing until fill has run on the transfer object.
- **Why:** Column and filter elements are created by fill, not by create; the query output gives no hint of that. **Workaround:** Ran fill on the transfer object, then queried again.
- **Validation:** confirmed; kind cli-tool; catalog partly-covered. Evidence: `session:L2390`, `session:L2392`

#### G013 `c04-12` R8 F21: postCallAccessNavigation cannot be cleared once set, and move --index had no effect on the position of the action group; move --after did reorder the menu entries.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Not in catalog; evidence is session-only. Add as verify: postCallAccessNavigation cannot be unset once set; move --index is ignored for action groups, use --before/--after.
- **Why:** CLI behaviour: unset is refused for this attribute and move with an index is ignored for these elements. **Workaround:** Left postCallAccessNavigation set (the clear attempt was refused, session:L2481); used move --after for menu order, since move --index had no effect.
- **Validation:** partly; kind cli-tool; catalog missing. Evidence: `session:L2481`, `session:L2544`, `session:L2547`, `session:L2572`

#### G014 `c05-20` R9 F32: create -t Access also creates a MenuItemAccess named Menu_n labelled with the target type name (AdminOrderInfo), so duplicate menu entries and not-unique errors followed; deleting an access referenced

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Not covered. Add: create -t Access also creates a MenuItemAccess named Menu_n labelled with the type name; rename or reuse it, and delete of an access referenced by a menu needs --cascade.
- **Why:** Side effects of Access creation are not documented for the CLI. **Workaround:** Deleted the duplicate access and menu, re-created one access, relabelled the menu.
- **Validation:** confirmed; kind cli-tool; catalog missing. Evidence: `session:L2816`, `session:L2818`, `session:L2819`, `session:L2820`. Merged: c07-41, c09-16

#### G015 `c06-05` R11 F44: create -t MimeType with -n failed ('name' not defined for MimeTypeCreateInput), and the --brief 'valid' output printed Java object strings (MimeTypeImpl@hash) instead of names.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Catalog notes name-less reference UI elements but not MimeType. Add MimeType (name derives from type/subType) to the no-name list; the MimeTypeImpl@hash print is a CLI bug.
- **Why:** CLI create for MimeType takes no name; the list of valid values is not rendered. **Workaround:** Created the MimeType with --ns only and kept the default name.
- **Validation:** partly; kind cli-tool; catalog missing. Evidence: `session:L3389`, `session:L3390`, `session:L3391`. Merged: g-R10-16

#### G016 `c06-08` R11 F44: Table operation names are not the short names the builder used (exportOrders vs exportOrdersTableOperation::exportOrders), and ui query has no TableOperation type, so updates failed with 'element not 

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Not in catalog. Add: table operations use FQN <table>::<opName>TableOperation::<opName> style names; query esm for them, since ui has no TableOperation type (verify).
- **Why:** Operation element naming of table actions is not obvious from the CLI output. **Workaround:** Listed the table operations with query esm TableOperation and used the full names.
- **Validation:** partly; kind cli-tool; catalog missing. Evidence: `session:L3406`, `session:L3414`, `session:L3448`

#### G017 `c06-09` R11 F44: validate --strict reported errors after a delete with --no-check, but the same command still ran save, so an invalid model was written to disk.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Catalog rule 6 says never save blindly and --no-check needs validate at the end, but not that chaining with && continues after validate reports errors. Add: gate save on the validate exit code (1 or 2).
- **Why:** save does not stop when validation fails in the same command chain; the builder chained them. **Workaround:** Re-ran delete --cascade and validation until clean.
- **Validation:** partly; kind cli-tool; catalog partly-covered. Evidence: `session:L3445`, `session:L3446`

#### G018 `c07-40` R12 F52, F53: judo-cli query esm with --where fqn=... returns nothing, and --select dataType{name} or dataType.name is rejected (scalar fields only), so the builder decompiled and grepped generated code to learn na

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Catalog lists --where operators but not that fqn is not a filterable field, nor that --select takes scalars or Name{sub} only. Add: filter by name.contains, not fqn.
- **Why:** CLI query selection rules are not what the builder expected; the catalog page on the CLI was not consulted for query syntax first. **Workaround:** Used name filters and grep over generated sources.
- **Validation:** confirmed; kind cli-tool; catalog partly-covered. Evidence: `session:L3831`, `session:L3833`, `session:L3834`, `session:L3836`. Merged: c09-11

#### G019 `c08-04` R13 F58, F60: judo query ui MenuItemAccess failed because MenuItemAccess is an esm type, not a ui type; the builder had to fall back to query esm for menu items.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Add: MenuItemAccess and Access are esm types; query esm, not query ui, to list menu items.
- **Why:** Type names for query ui and query esm differ and the CLI error lists valid types without saying which lane holds menus. **Workaround:** Used query esm MenuItemAccess for the menu list.
- **Validation:** confirmed; kind cli-tool; catalog missing. Evidence: `session:L4606`, `session:L4609`

#### G020 `c09-27` R14 F68: Admin Exchange rates had no Create button: create -t Access without flags made the access not createable, while the companies access was. The F68 test then timed out waiting for the rate save.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. No mention that create -t Access defaults createable=false (grep found only the property list in ui-authoring-guide). Add: set createable, updateable, deleteable explicitly when creating an Access.
- **Why:** Builder did not set createable, updateable and deleteable on the new access; the command default differs by access. **Workaround:** Set the three flags on Admin.exchangeRates by hand and rebuilt.
- **Validation:** confirmed; kind builder-mistake; catalog missing. Evidence: `session:L5420`, `session:L5423`, `session:L5425`, `session:L5531`

#### G021 `c09-12` R14 F62, F63, F67: update --add feature failed for actions containers that do not exist yet ('Container not found', 'element not found'); fill reported 'unchanged'; a row action on a relation table was refused ('refund 

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Not documented. Add order: create the actions container first, then update --add feature; row actions on relation tables must be added to the relation table, not placed anywhere (verify).
- **Why:** CLI order of creating the actions group and row actions is not documented; error text does not say what to run first. **Workaround:** Used the generated refund table operation that already exists on the lines table; the test then opens the action group menu to click it.
- **Validation:** partly; kind cli-tool; catalog missing. Evidence: `session:L5222`, `session:L5224`, `session:L5226`, `session:L5228`

#### G022 `c10-18` R15 : judo query on StringType with --select textWidget fails ('not a field'); textWidget lives on DataField, and the error lists valid fields without saying which type owns the attribute.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Catalog ui-behaviour.md maps widgets but the CLI error does not name the owner type. Add a hint: textWidget lives on DataField, not on the data type.
- **Why:** Attribute is on DataField, not on the data type; the CLI does not point to the owning type. **Workaround:** Queried DataField instead.
- **Validation:** partly; kind cli-tool; catalog partly-covered. Evidence: `session:L5738`, `session:L5739`, `session:L5740`, `session:L5743`

#### G023 `c10-19` R15 : A batch of 178 judo update attribute changes produced 20 errors: 'element not found' for view fields that do not exist (email, ratingLabel, soldBy, remainingCreditLabel) and textWidget refused on a un

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/judo-cli.md`. Add: use update --schema or query the view DataFields before a bulk update; view members that are not on the TO (derived labels) do not exist.
- **Why:** Builder guessed the view attribute names from the TO fields; the CLI gives no per-view attribute list. **Workaround:** Accepted the 158 ok changes and skipped the 20 bad ones.
- **Validation:** partly; kind cli-tool; catalog missing. Evidence: `session:L5744`, `session:L5746`, `session:L5753`

### `catalog/agent-docs/model/ui-authoring-guide.md` (12)

#### G024 `c02-41` R3 S11: The kb has no section that says where the generated order of form and view fields comes from. The builder had to read the esm2ui transformation jar to learn it.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/ui-authoring-guide.md`. No section on field order. Add: generated form/view field order follows the order of the container components in the ESM; reorder with `move --index`, not by delete and re-add (that loses customImplementation and widgets, GAPS R3-6).
- **Why:** Catalog gap: the order rule (position from the container components in the ESM model) is not in the kb; the 'move' section of judo-cli.md does not say it affects generated field order. **Workaround:** Read the tatami esm2ui ETL (esmToUi.etl) from the local jar.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L1573`, `session:L1575`, `session:L1596`, `session:L1597`

#### G025 `c03-17` R6 F07, F02: Builder tried representationComponent link, autocomplete and tag on the category relation; the CLI accepted only table (then button after relationKind changed). The catalog lists table, button and tag

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/ui-authoring-guide.md`. Shape table (line 257) lists to-one options table, button, tag, which matches the builder's note; the CLI behaviour (options depend on relationKind, e.g. table before kind change) is not stated. Add a line on that.
- **Why:** Allowed representationComponent values depend on relationKind as enforced by the CLI, which the catalog's shape table does not state clearly; the builder guessed values before reading the catalog. **Workaround:** Set relationKind to AGGREGATION on ProductInfo.category, then set representationComponent to table on Form and View_Edit.
- **Validation:** partly; kind catalog-wrong; catalog partly-covered. Evidence: `session:L1919`, `session:L1920`, `session:L1921`, `session:L1923`

#### G026 `c03-07` R6 F07: update --feature name failed on CategoryInfo and ProductInfo: name is not a placeable feature on the table or view element because the feature is on the nested relation.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/ui-authoring-guide.md`. Guide does not say a name feature on a nested relation table is added on the nested element, not the table/view. Add one CLI example of update --add feature on a relation table element (verify).
- **Why:** Builder targeted the wrong element; the feature belongs to the nested category or products relation. **Workaround:** Targeted the nested element instead (CategoryInfo_View_Edit products column).
- **Validation:** confirmed; kind builder-mistake; catalog partly-covered. Evidence: `session:L1793`

#### G027 `c03-36` R7 F08: kb_search for eager or isEager and embedded tables on views returned generic embedded-table sections; the view-table example (TabularReferenceField with representationComponent=table) was only found b

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/ui-authoring-guide.md`. kb has no isEager entry (grep only finds jsl eager note and sessionStorage). Add a view-table example with TabularReferenceField representationComponent=table and say whether an eager attribute exists (verify against esm.ecore).
- **Why:** The orchestrator's term isEager is not a catalog concept; the catalog answer is the to-many TabularReferenceField on the view, which the search did not rank first. **Workaround:** Read the catalog by grep, then used a to-many TabularReferenceField with representationComponent table on the view.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L1961`, `session:L1963`, `session:L1966`, `session:L1967`

#### G028 `c03-37` R7 F08: Builder noted that the CLI lists table, button, tag and card as valid representationComponent values for a to-many relation, while the catalog shape table lists table, card and tag only.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/ui-authoring-guide.md`. Shape table (line 257) lists table, card, tag for to-many; builder reports the CLI also accepts button. Verify with `create --schema` and align the table.
- **Why:** Possible mismatch between the catalog shape table and the CLI schema for to-many relations.
- **Validation:** partly; kind catalog-wrong; catalog partly-covered. Evidence: `session:L1972`, `session:L1966`, `session:L2297`

#### G029 `c03-71` R7 F10, F16: Variants and addresses inside a product or profile view are saved only with the page Update button; the tests failed until they clicked Update.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/ui-authoring-guide.md`. No statement found. Add: composed child rows edited in a view are saved only by the page Update button; tests must click it.
- **Why:** Composed child rows belong to the parent view and are stored with the parent save; the catalog does not say so next to the inline table pattern. **Workaround:** Tests click Update (saveView, saveProfile) after adding the child rows.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L2275`, `session:L2281`, `session:L2287`

#### G030 `c04-11` R8 F17, F21: An OperationForm placed directly in a view fails UI validation (ActionContainerSameWithActionDefinition, NamedElementHaveToBeInApplication); the operation must sit in an ActionGroup, and the catalog s

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/ui-authoring-guide.md`. ui-authoring-guide lines 131 and 190 say OperationForm can sit directly in a View/Form; the session shows the transformation rejects it and needs an ActionGroup. Already listed as open in judo-doc-problems (ActionGroup-wrapped OperationForms). Change the text: operation buttons go inside a ui:ActionGroup.
- **Why:** The catalog section on operation wiring says OperationForm inside View or Form works; the transformation rejects it. The openspec sweep already lists ActionGroup-wrapped OperationForms as an open item (FR-033). Even inside an ActionGroup, the validator still reported action container errors after the wrap (session:L2494). **Workaround:** Moved both operations into an ActionGroup named actions, set label Actions and featuredActions=1; for checkout the action container errors cleared only after it became void with generateActionsHook=true (validation passed, session:L2522).
- **Validation:** confirmed; kind catalog-wrong; catalog wrong. Evidence: `session:L2445`, `session:L2447`, `session:L2457`, `session:L2493`

#### G031 `c05-21` R9 F25, F27: create -t ActionGroup without a parent was refused (Cannot create ActionGroup in Model); the group must be created with --ns of the view, then operations are relocated into it.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/ui-authoring-guide.md`. No CLI recipe for creating an ActionGroup (create -t ActionGroup needs --ns of the view; operations are then moved in). Add it next to the ActionGroup row at line 191.
- **Why:** The ui-authoring-guide says an OperationForm inside a view works, but gives no CLI recipe for the ActionGroup. **Workaround:** create -t ActionGroup -n actions --ns <view>, then relocate each operation into it.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L2839`, `session:L2840`, `session:L2841`. Merged: c08-05. add→modify (target file exists; add a section)

#### G032 `c05-54` R10 F36, F39: Invoice and coupon actions were placed directly into the view again (OperationForm outside an ActionGroup), giving ActionContainerSameWithActionDefinition and NamedElementHaveToBeInApplication errors.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/ui-authoring-guide.md`. Line 302 only says OperationForm inside ActionGroup is for grouping; no sentence says direct placement fails validation. Add the rule: operations must be inside an ActionGroup (error ActionContainerSameWithActionDefinition). Repeated mistake, so a catalog entry would have helped.
- **Why:** Builder repeated the R8-7 mistake; the lesson was not applied. **Workaround:** Deleted the actions, moved them into an ActionGroup with relocate, validate passed.
- **Validation:** confirmed; kind builder-mistake; catalog partly-covered. Evidence: `session:L3072`, `session:L3074`, `session:L3076`, `session:L3077`

#### G033 `c06-17` R11 : 'Ordered' is a custom field and the generator draws custom fields after the generated ones, so after the move it sits just above the buttons; field order in the order view is not fully controllable.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `agent-docs/model/ui-authoring-guide.md`. Custom field after generated ones is the same field-order problem as the esmToUi position lookup (other batch). Note in the guide that generated field order is not fully controllable, and that move only works partly.
- **Why:** Custom fields are placed after generated fields; the field-order platform bug may apply. **Workaround:** Used the CLI move command to reorder the generated fields; left Ordered last.
- **Validation:** partly; kind platform-limit; catalog missing. Evidence: `session:L3417`, `session:L3420`, `session:L3742`

#### G034 `c09-44` R14 F60, F63, F67: Relation tables inside a view show raw member names (TotalLabel, SellerName) unless every column of that table gets its own label and order; row actions sit behind the generated action group drop-down

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/ui-authoring-guide.md`. Builder reports relation tables in a view need labels and order per column; no catalog text on this. Single observation, add with verify.
- **Why:** Labels set on the target transfer object do not reach a relation table in a view; not documented as far as checked. **Workaround:** Each relation column labelled and moved to an index via a script (cols function).
- **Validation:** partly; kind catalog-gap; catalog missing. Evidence: `session:L5417`, `session:L5418`, `session:L5531`

#### G035 `c10-13` R15 : No documented way to hide the generated 'Check out' dialog action on the cart page, so the old and new checkout both exist.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/ui-authoring-guide.md`. hiddenBy exists (ui-behaviour.md line 44, ui-authoring-guide line 275) but there is no recipe for hiding a generated action; add one: put a boolean on the owner transfer object and set hiddenBy on the action.
- **Why:** Hiding a generated action needs a hiddenBy boolean in the model; the builder left the model change for the owner. **Workaround:** Left the generated checkout dialog in place; documented in GAPS R15-3.
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L5867`, `session:L6092`

### `catalog/agent-docs/e2e-testing/troubleshooting.md` (11)

#### G036 `c02-28` R2 S09: E2E selectors did not match the generated UI: getByLabel('Price') matched both the column menu button and the input, getByLabel('Name') matched more than one element, and 'Save' was used for the view 

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/troubleshooting.md`. Session shows the guessed selectors failing. troubleshooting.md "Element not found" only shows getByLabel/dialog scoping and the "Update after" flag exists in writing-tests.md. Add: the generated pages have several elements with the same label (column menu button plus input), so use getByRole("textbox",{name}) or the helper field names; the view save button is "Update".
- **Why:** Builder guessed names; the catalog examples use icon-prefixed names and label-only lookups that are ambiguous on the list and form pages. **Workaround:** Changed the selectors to Update and to getByRole('textbox', { name }) with the helper names.
- **Validation:** confirmed; kind test-design; catalog partly-covered. Evidence: `session:L1329`, `session:L1353`, `session:L1371`, `session:L1372`. Merged: c03-15, c03-65, c03-67, c03-70, c04-21, c04-22, c05-13, c06-20

#### G037 `c03-20` R6 F01: Create-rename-delete test failed on a strict-mode violation: two grid cells named Temp Shoes from earlier failed runs.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/troubleshooting.md`. The E2E database and Keycloak users persist between runs, so failed or repeated runs leave rows that break counts, strict locators and paging. Add a "Test data accumulates" section: use unique stamped names, clean up leftovers in the seed or an afterAll, filter by own stamp, never assert absolute counts.
- **Why:** The test used a fixed name and was not idempotent; leftovers from previous runs stayed in the database. **Workaround:** Made the name unique with Date.now() and added a cleanup of leftover Temp categories in the seed.
- **Validation:** confirmed; kind test-design; catalog missing. Evidence: `session:L1943`, `session:L1946`. Merged: c03-22, c03-69, c03-78, c04-23, c05-12, c05-56, c07-47, c08-23. add→modify (target file exists; add a section)

#### G038 `g-R6-6` R6 F01, F02: Generated text fields (DebouncedTextField) store the value after a delay, so fill() or typing then clicking Create gives "Missing required attribute"; tests must type with key presses, blur and wait ~

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/troubleshooting.md`. Session L1893 shows DebouncedTextField with onDebouncedChange in the generated code; no debounce text in e2e-testing docs (only unrelated hits in frontend/advanced-patterns.md), and writing-tests.md still shows glyph button names. Add: generated text inputs commit after a debounce; type with pressSequentially, blur, wait for the Update/Create button before clicking.
- **Why:** writing-tests.md helpers (fillPrimitiveField) do not mention the debounce. **Workaround:** Real key presses, blur, wait 700 ms; regex button names.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L1893`, `gaps:R6-6`. add→modify (target file exists; add a section)

#### G039 `g-R7-12` R7 F09: Admin product table has 8 columns; at 1440 px the last ones are off screen and the grid renders only visible columns, so tests reading them need a wider window.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/troubleshooting.md`. Grep over e2e-testing finds nothing on column or row virtualization. Same root as R12-14. Add: DataGrid renders only visible columns and the first page of rows; set wide viewport or scroll the grid horizontally, and filter before looking for a row.
- **Why:** MUI DataGrid column virtualization. **Workaround:** Tests use 1920 px window (later column widths in R8-3).
- **Validation:** partly; kind platform-limit; catalog missing. Evidence: `gaps:R7-12`. Merged: g-R12-14. add→modify (target file exists; add a section)

#### G040 `c05-15` R9 : Customer spec imported helpers from the admin Playwright package, which loaded a second copy of @playwright/test; Playwright then reported No tests found.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/troubleshooting.md`. Session L2912 shows "Requiring @playwright/test second time ... No tests found" and GAPS R9-15 confirms. Add: do not import helpers across the generated Playwright projects (each has its own node_modules); copy or share via a single package.
- **Why:** Shared helpers across actor packages are not documented as a supported pattern in the e2e docs. **Workaround:** Copied the needed helper functions into the customer spec.
- **Validation:** confirmed; kind test-design; catalog missing. Evidence: `session:L2905`, `session:L2912`, `session:L2913`. add→modify (target file exists; add a section)

#### G041 `c06-10` R11 F44: The generated file upload button in the admin import dialog has only a title ('Upload file') and wraps a hidden file input, so getByRole('button', name) cannot find it in Playwright; getByTitle works.

- [ ] **Issue**  Action: [x] add [ ] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** add-catalog → `agent-docs/e2e-testing/troubleshooting.md`. GAPS R11-7(d): the file field is a hidden input in an icon button with title only. Add: use getByTitle('Upload file') plus the file chooser event, not getByRole button name. Generator design, not a bug.
- **Why:** Generated BinaryInput widget gives the upload control no accessible name. **Workaround:** Test uses getByTitle('Upload file') and the file chooser event.
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L3612`, `session:L3620`, `session:L3623`, `session:L3627`

#### G042 `c06-11` R11 F44: In the generated export dialog, keys typed into the date range fields in one burst were lost, and typing into the second date field reset the first in form state (the request sent only toDate or only 

- [ ] **Issue**  Action: [x] add [ ] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** add-catalog → `agent-docs/e2e-testing/troubleshooting.md`. Reproduced in GAPS R11-7(d) but root cause (frontend form state vs Playwright timing) not established. Add a short tip: type dates in segments and wait for the template request.
- **Why:** Builder's diagnosis: generated date widget loses input when typed fast and the second field resets the first. **Workaround:** Test types the date in segments with a pause, waits for the template request, and waits 1.5 s before typing; the until filter was dropped from the test.
- **Validation:** partly; kind platform-bug; catalog missing. Evidence: `session:L3661`, `session:L3662`, `session:L3664`, `session:L3688`

#### G043 `c08-24` R13 F55, F56, F57, F58, F59: Full customer suite ran with parallel workers: customers shared one cart and one seeded stock, so stock reached zero and tests interfered. Builder reset stock with a direct SQL UPDATE.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/troubleshooting.md`. Session L4980 and L5044 show parallel workers sharing one cart and seeded stock. troubleshooting.md "Speed Up Tests" recommends fullyParallel without this warning. Add: with shared seeded data run serial (workers 1) or give each test its own buyer and products; reset stock by SQL only as last resort.
- **Why:** Test isolation: shared fixtures and parallel workers. Not a code bug. **Workaround:** Direct SQL reset of stock; new rule: run new spec with --grep @smoke, full suites once, serial.
- **Validation:** confirmed; kind test-design; catalog missing. Evidence: `session:L4980`, `session:L4983`. Merged: c09-04, c09-31, c09-33, c09-36, c10-26. add→modify (target file exists; add a section)

#### G044 `c09-02` R13 F55, F56, F57, F58, F59, F60, F61: The full customer E2E suite took 10.6 minutes at 3 workers and the admin suite 2.8 minutes. The user stopped a run as too long and asked for about 5 minutes.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/troubleshooting.md`. Suite took 10.6 min at 3 workers; user asked for ~5 min. "Speed Up Tests" exists but lacks the smoke-subset advice. Add: tag a small @smoke set, run new specs plus --grep @smoke per round, full suites once at the end. The time target is a user rule, so keep it as a suggestion.
- **Why:** Every round ran both full suites; no smoke subset existed. **Workaround:** Tagged a small @smoke set; each round runs only its new spec plus --grep @smoke; full suites run once at the end of the build.
- **Validation:** confirmed; kind test-design; catalog partly-covered. Evidence: `session:L5020`, `session:L5022`, `session:L5042`, `session:L5044`

#### G045 `c08-21` R13 F59, F60: Generated action group shows the first three actions; Request a quote sits under the Actions menu in the cart, so the test must open the menu.

- [ ] **Issue**  Action: [x] add [ ] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** add-catalog → `agent-docs/e2e-testing/troubleshooting.md`. Generated action groups show three actions, the rest go under an Actions menu; tests must open the menu first.
- **Why:** Platform behaviour of the generated action group (featured actions), not a bug. **Workaround:** Test opens Actions and clicks the menu item. Not hidden or patched.
- **Validation:** confirmed; kind platform-limit; catalog missing. Evidence: `session:L4939`, `session:L4944`

#### G046 `c10-16` R15 : A long single test (several minutes with 3-width screenshots) hit ACCESS_TOKEN_EXPIRED; the overhaul spec was split into two tests with a login each.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/troubleshooting.md`. Only error-handling-guide lists ACCESS_TOKEN_EXPIRED; no e2e guidance. Add: keep tests shorter than the token lifetime or log in per test.
- **Why:** Access token lifetime is shorter than the test; kb search for token renewal in e2e found only error codes, no renewal guidance. **Workaround:** Split the spec into two short tests.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L5919`, `session:L5920`, `session:L5921`, `session:L5923`. add→modify (target file exists; add a section)

### `catalog/agent-docs/deployment/local-development.md` (7)

#### G047 `c01-11` R0 S01: No documented recipe for the first login user of a local dev app: no test user, no seed data and no credentials are given for the generated Keycloak realm.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/local-development.md`. No login step for a fresh local app. Add a short recipe: create a user in the app realm (Keycloak admin under /auth), and the matching principal row or rely on JIT provisioning (link keycloak-jit-user-provisioning.md).
- **Why:** Grep of agent-docs found only integration-test users and the test realm file. The local-development doc has no login step. The builder had to create a Keycloak user and a DB row by hand. **Workaround:** Created Keycloak user shop/shop through the admin REST API and inserted a t_webshop_shop_user row with psql. Wrapped in scripts/seed-dev-user.sh.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L112`, `session:L131`, `session:L165`, `session:L173`. add→modify (target file exists; add a section)

#### G048 `c01-13` R0 S01: local-development.md gives the app URL as http://localhost:8181/apps/. The app is at /webshop/Shop/, and /apps/ only lists bundles.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/local-development.md`. Line 40 (and deployment/README.md line 160) give /apps/. GAPS R0-7 shows the app is at /<model>/<Actor>/ (here /webshop/Shop/); /apps/ is only a bundle list. Fix both files.
- **Why:** Doc is out of date for the generated app path. **Workaround:** Used http://localhost:8181/webshop/Shop/ (from the Karaf start log).
- **Validation:** confirmed; kind catalog-wrong; catalog wrong. Evidence: `session:L28`, `session:L176`, `session:L179`, `gaps:R0-7`. Merged: g-L7

#### G049 `c01-14` R0 S01: Keycloak on the local port is served under /auth (Keycloak 23 with a relative path). Root and /realms return 404, and the catalog gives http://localhost:8080 with no path.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/local-development.md`. judo.sh line 492 starts Keycloak with --http-relative-path /auth, so the console is http://localhost:8080/auth. Doc line 41 omits the path.
- **Why:** judo.sh starts Keycloak with --http-relative-path /auth, which the local-development doc does not mention. **Workaround:** Used http://localhost:8280/auth for admin and realm calls.
- **Validation:** confirmed; kind catalog-wrong; catalog wrong. Evidence: `session:L28`, `session:L161`, `session:L162`, `session:L164`

#### G050 `c01-16` R0 S01: The generated judo.properties sets dbtype=hsqldb, but local-development.md says the default run uses PostgreSQL in Docker.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/local-development.md`. Fresh template judo.properties has dbtype=hsqldb (git history of webshop-test shows the builder changed it to postgresql); doc lines 35-36 and 203 say PostgreSQL is the default. Fix: default is hsqldb, PostgreSQL is opt-in via dbtype=postgresql.
- **Why:** Doc and generated default disagree. **Workaround:** Changed dbtype to postgresql in judo.properties.
- **Validation:** confirmed; kind catalog-wrong; catalog wrong. Evidence: `session:L59`, `session:L128`, `session:L147`, `gaps:R0-5`. Merged: g-L5

#### G051 `g-L6` R0 S01: Local Keycloak runs with --http-relative-path /auth, so with keycloak_port=8280 the URL is http://localhost:8280/auth/...; the docs say http://localhost:8080 and do not say changing the port needs onl

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/local-development.md`. Session L164 shows the start script uses --http-relative-path /auth; local-development.md lines 36-41, 279 give http://localhost:8080 with no /auth and no relative-path hit anywhere in agent-docs/deployment. Add: Keycloak base URL is http://localhost:<keycloak_port>/auth (set keycloak_port in judo.properties).
- **Why:** local-development.md gives Keycloak URLs without the /auth path. **Workaround:** Set keycloak_port=8280 in judo.properties and used /auth URLs.
- **Validation:** confirmed; kind catalog-gap; catalog wrong. Evidence: `session:L164`, `gaps:L0-6`

#### G052 `c02-38` R3 S07, S11: Round 3 test run failed 10 tests with ERR_CONNECTION_REFUSED because Docker was not running. judo.sh start printed 'Cannot connect to the Docker daemon' and the builder's wait loop ended before the ap

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/local-development.md`. grep found no mention of the Docker daemon being required or checked. Add: run docker info before judo.sh start; start returns before failure shows, so wait for the app URL before tests.
- **Why:** Docker Desktop was stopped; the builder did not check the Docker daemon before starting the stack. **Workaround:** Started Docker, stopped and restarted the stack, waited for HTTP 200, then reran the tests.
- **Validation:** confirmed; kind builder-mistake; catalog missing. Evidence: `session:L1510`, `session:L1512`, `session:L1513`, `session:L1514`

#### G053 `c03-63` R7 F01: judo-cli.jar was missing from target/ after generate and build steps, so CLI calls failed with Unable to access jarfile; the builder had to run generate-root to restore it.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/local-development.md`. Not covered anywhere (checked judo-cli.md Version and jar pitfalls and deployment docs). Add: generate (maven clean) deletes target/judo-cli.jar; run ./judo.sh generate-root to restore it before CLI calls.
- **Why:** Cause not stated in the session; the target folder was gone after a build step. **Workaround:** Ran ./judo.sh generate-root before each CLI session that followed a generate.
- **Validation:** confirmed; kind cli-tool; catalog missing. Evidence: `session:L2251`, `session:L2252`, `session:L2253`, `session:L2254`. Merged: c06-06

### `catalog/agent-docs/frontend/hooks/ui-hooks.md` (6)

#### G054 `c02-18` R1 S09: Builder states the catalog has no hook for a view or field display; ui-hooks.md covers only AppBar, hero, logo, footer and menu. The only route it found is a model-level custom implementation on the f

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/hooks/ui-hooks.md`. ui-hooks.md has no field or value hook; advanced-patterns.md line 1519 does describe model-level customImplementation on an element. Add a pointer in ui-hooks.md: for field display use customImplementation on the DataField, with the key/scaffold names and the note that the field must stay in the mask.
- **Why:** ui-hooks.md scope does not list field or detail display hooks, so a price display on a plain DataField has no documented hook. **Workaround:** Used the model customImplementation flag on the form and view price fields.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L916`, `session:L1206`

#### G055 `c05-02` R9 : The documented menu reorder example sorts by item ids such as dashboard, but generated menu ids are long model ids, so the example cannot be used as written.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/hooks/ui-hooks.md`. The Reordering Menu Items example (line 340) orders by ids like dashboard and entities; generated menu item ids are long model ids. Change the example to match on a suffix or the real id format.
- **Why:** The catalog example does not show the real id format of generated menu items. **Workaround:** Sorted the menu by item title (Products, Cart, My orders, My profile, My addresses) in registerShellHooks.ts; test checks the five labels.
- **Validation:** confirmed; kind catalog-gap; catalog wrong. Evidence: `session:L2698`, `session:L2699`, `session:L2713`, `session:L2714`

#### G056 `g-R10-13` R10 F40: The generated header puts AppBar extra components at the top left of the drawer under the logo; no documented slot for the top right, where a language switch is expected.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/hooks/ui-hooks.md`. Session L916 shows the AppBarExtraComponents hook doc; ui-hooks.md has no placement statement. Add: extras render in the drawer under the logo (column layout), wrap in a flex Box, and there is no top-right slot.
- **Why:** ui-hooks.md describes the extra component but not its position. **Workaround:** Left in place.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L916`, `gaps:R10-13`

#### G057 `c06-19` R11 F43, F41: Customer view fields that the page must load but not show (effectivePrice, onSale, ratingLabel, image, sale fields) were hidden with customImplementation=true and render-nothing components, because no

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `agent-docs/frontend/hooks/ui-hooks.md`. GAPS R1-2: there is no view-field hook; ui-hooks.md covers AppBar, hero, logo, footer, menu only. Add: for load-but-hide fields, set customImplementation=true on the DataField (not DataColumn, see c07-17) and render nothing.
- **Why:** ui-hooks.md covers AppBar, hero, logo, footer and menu only; the only mechanism is a model-level custom implementation (already logged as a gap). **Workaround:** Layout-only components render the values in ProductDetailsLayout and CatalogHome.
- **Validation:** confirmed; kind platform-limit; catalog partly-covered. Evidence: `session:L3566`, `session:L3567`, `session:L3569`, `session:L3570`

#### G058 `c07-22` R12 F40: In the drawer, the generated layout stacks the AppBar extra components as a column, so the bell button stretched over the full drawer width and showed as a grey ellipse.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `agent-docs/frontend/hooks/ui-hooks.md`. ui-hooks.md has an AppBarExtras example but no note on layout. Add: in the drawer the extras stack as a column, wrap the content in one flex Box. Low value, evidence only the session.
- **Why:** Generated layout of AppBar extra components has no documented row layout; the builder fixed it by wrapping them in one Box. **Workaround:** One flex Box wrapper inside AppBarExtras.
- **Validation:** partly; kind platform-limit; catalog partly-covered. Evidence: `session:L3790`, `session:L3796`

#### G059 `c10-32` R15 : Custom menu groups were first typed 'collapse' and then changed to 'group' after the drawer rendered wrong.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/hooks/ui-hooks.md`. Chunk gives no reason; ui-hooks.md should list valid menu item types (group vs collapse) and which suits horizontal vs drawer menus (verify).
- **Why:** Not stated in the chunk; the group type fits top-level menu groups in the horizontal bar. **Workaround:** sed change of the type to 'group'.
- **Validation:** unverifiable; kind builder-mistake; catalog partly-covered. Evidence: `session:L5807`, `session:L5808`, `session:L5809`, `session:L5814`

### `catalog/agent-docs/e2e-testing/writing-tests.md` (6)

#### G060 `c02-45` R3 S02, S03: Seeding the description through the UI with Playwright fill() did not store the value; the save response timed out. Switching to pressSequentially with a delay and a blur made the test pass.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/writing-tests.md`. Session and GAPS R3-6e confirm fill() did not mark the form changed so no Update button appeared; the textarea had also lost its TextArea widget in that round, so this may be tied to the builder's own model edit. If kept: for text areas type with pressSequentially then click another field to blur so the change registers.
- **Why:** fill() sets the value in one step, which the React text area did not register as edits before save; the builder found it by trial. **Workaround:** a-seed-descriptions.spec.ts uses fill('') then pressSequentially(text) and clicks the Name field to blur.
- **Validation:** partly; kind test-design; catalog missing. Evidence: `session:L1652`, `session:L1656`, `session:L1657`, `session:L1660`. add→modify (target file exists; add a section)

#### G061 `c03-14` R6 F01, F03: Playwright fill() on the generated text field did not store the value; the create dialog stayed open and Create was never accepted. Stored data then failed with MISSING_REQUIRED_ATTRIBUTE on categorie

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/writing-tests.md`. Catalog uses .fill() in examples and never warns. Only the session shows the failure, and the cause (blur versus key events) is the miner's guess. Test first before adding a note.
- **Why:** Generated inputs store the value on blur or on real key events, not on programmatic fill(). **Workaround:** Used pressSequentially with a blur after each field.
- **Validation:** unverifiable; kind catalog-gap; catalog missing. Evidence: `session:L1871`, `session:L1875`, `session:L1878`, `session:L1882`. add→modify (target file exists; add a section)

#### G062 `c03-16` R6 F01: Seed test looked for catalog-grid and then for a generic no-rows text; both locators were guessed, and the test failed on each before it matched the real markup.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/writing-tests.md`. Builder guessed locators; writing-tests.md exists but the builder skipped it. Add a short "no rows / table container locators" line if missing; mostly a kb-first lapse.
- **Why:** The builder guessed selectors instead of reading the e2e locator conventions. **Workaround:** Replaced locators with or() alternatives and the table row locator.
- **Validation:** confirmed; kind builder-mistake; catalog partly-covered. Evidence: `session:L1823`, `session:L1825`, `session:L1866`, `session:L1870`

#### G063 `c03-19` R6 F01, F02, F07: Seed helper passed the dialog as the locator for the Unit and Category pickers; their option popups render outside the dialog, so the option click timed out, and the relation waited on a range respons

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/writing-tests.md`. grep for popup/portal/listbox in writing-tests.md found nothing. Add: picker option popups render outside the dialog, locate options on the page, not inside the dialog.
- **Why:** The popup rendered outside the dialog scope; the builder scoped the locator to the dialog. **Workaround:** Opened the combobox in the dialog and clicked the option from the page scope; used pressSequentially for the category.
- **Validation:** confirmed; kind builder-mistake; catalog missing. Evidence: `session:L1899`, `session:L1900`, `session:L1901`, `session:L1905`

#### G064 `c03-62` R7 F09: Seed upload through the generated binary input: setInputFiles set the file name in the textbox, but the test looked for an img inside the dialog and timed out.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/writing-tests.md`. Session shows the generated binary input puts the file name in a textbox after setInputFiles and renders no img. Add: for BinaryType fields upload with setInputFiles on the file input and assert the textbox value (the file name), not an image.
- **Why:** The generated BinaryTypeInput shows the file name in a text field, not an image; the test expectation was wrong for the generated widget. **Workaround:** Asserted the textbox value img-SKU.png after upload.
- **Validation:** confirmed; kind test-design; catalog missing. Evidence: `session:L2236`, `session:L2239`, `session:L2240`, `session:L2241`. add→modify (target file exists; add a section)

#### G065 `g-R7-11` R7 F10, F16: Embedded relation dialogs: submit button is "Ok" (later "Submit"), title and labels come from the transfer object form, composition children are saved with the page Update button, delete is hidden whi

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/writing-tests.md`. Session L2248 mentions the F10 submit button "Ok"; writing-tests.md "Dialog Handling" (line 502) shows Yes/No and acceptChangesOnDialogElement only, nothing on composition children saved via Update. Add a short "relation dialogs" subsection: Ok/Submit button, composition children persist on page Update.
- **Why:** e2e docs only show confirm Yes/No and a generic acceptChangesOnDialogElement. **Workaround:** Test code adapted to the real names.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L2248`, `gaps:R7-11`

### `catalog/agent-docs/deployment/build-process.md` (5)

#### G066 `c01-04` R0 S01: The catalog gives the create-judo-project goal and its parameters but not the plugin groupId or version. The builder took version 1.0.0.20260311 from ~/.m2, which then pulled template 1.0.0.20261109 f

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/build-process.md`. build-process.md line 359 names the goal and parameters but not the plugin groupId or that -Dversion must be the intended judo version; add: use the groupId/version of the plugin from the target judo-versions, since the plugin version selects the template version. Version detail from the session not re-checked.
- **Why:** Build-process section lists parameters only. Plugin coordinates and a version pin are not documented, so the builder guessed from the local Maven cache. **Workaround:** Used the locally cached plugin version found under ~/.m2/repository/hu/blackbelt/judo.
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L24`, `session:L38`, `session:L39`, `session:L44`. Merged: g-L1

#### G067 `c01-02` R0 S01: generate-root stopped with 'manual changes in generated files' on .gitignore after the generated project was copied into the existing repo.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/build-process.md`. Checked build-process.md and generator-plugins.md: synchronizeGitignore is described but not how to adopt generator output into a repo with its own .gitignore. Add: copy only generated files, keep the managed JUDO GENERATOR BLOCK in .gitignore, never overwrite the tracked file wholesale.
- **Why:** The builder copied the generator output over the repo's tracked .gitignore, so the generator saw a hand edit. The catalog does not say how to adopt generated files into a repo that already has its own .gitignore. **Workaround:** Restored the generated .gitignore, added .pi/dashboard/kb/ to .git/info/exclude, reran generate-root (exit 0).
- **Validation:** confirmed; kind builder-mistake; catalog missing. Evidence: `session:L60`, `session:L72`, `session:L73`, `gaps:R0-4`. Merged: g-L4. add→modify (target file exists; add a section)

#### G068 `c04-04` R8 F09, F17: Renaming the customer product transfer object forced hand edits of custom frontend files (renamed custom-implementation file, new constants, container and type paths) and deletion of stale generated c

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/build-process.md`. Builder found Frontend Build Recovery in build-process.md. Missing: renaming a TO renames custom-implementation files and constants. Add one line: "After renaming a TO, rename custom files/constants and delete stale generated pages/dialogs/containers/services before regenerating."
- **Why:** Custom frontend file names and constants are derived from the transfer object name; stale generated containers stay behind after a model change. The builder found the recovery steps in build-process.md. **Workaround:** git mv of the custom file, search-and-replace of names and paths, removal of generated pages, dialogs, containers and services folders, then regenerate.
- **Validation:** confirmed; kind platform-limit; catalog partly-covered. Evidence: `session:L2436`, `session:L2437`, `session:L2480`, `session:L2666`

#### G069 `c05-44` R10 F39: Platform-provided libraries (PDFBox, Handlebars, FileStoreService) do not compile in the app module until the app pom declares them; the first build failed with unresolved imports.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/build-process.md`. build-process worked example (line 125) adds a runtime dependency but does not say platform-provided libraries (PDFBox, Handlebars, FileStoreService) still need compile-time dependencies in the app pom. Add that line.
- **Why:** Catalog does not say that runtime-provided libraries still need a compile-time dependency in the app module. **Workaround:** Added pom.xml.extra-dependencies.fragment.hbs (documented fragment slot), then build -i succeeded.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L3004`, `session:L3005`, `session:L3093`, `session:L3096`. add→modify (target file exists; add a section)

#### G070 `c07-02` R12 F52: schema-upgrade runs apply (generate and execute in one step), so there is no moment to insert the hand-written backfill changeset that the catalog recommends. The catalog's schema-upgrade row does not

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/build-process.md`. build-process line 283 says schema-upgrade generates and applies in one step but does not warn that the hand-written backfill cannot be inserted. Add: for backfill use generate then judo-rdbms-schema:execute separately (route in GAPS R12-1).
- **Why:** The command table describes schema-upgrade as generate-and-apply; the backfill route needs generate, edit, then execute as separate steps. **Workaround:** Used judo-rdbms-schema:generate with the old model file, wrote 06_updateDataAfterIncremental by hand, then :execute.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L3759`, `session:L3753`, `session:L4017`, `session:L4025`

### `catalog/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md` (5)

#### G071 `c01-18` R0 S04: No model-level way to show a price with two decimals in the generated table. The table shows 89.9 and 129.5.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md`. formatValue is listed as 'format numeric values' only. GAPS item 32: generated column uses Intl.NumberFormat and ignores attribute scale. Add: scale/fraction digits are not honoured; use a derived string attribute or a custom column. Also a possible platform issue.
- **Why:** The generated table valueFormatter uses Intl.NumberFormat with defaults. formatValue exists in the model but the table column does not set fraction digits. **Workaround:** Patched the generated table component (see c01-21).
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L390`, `session:L391`, `session:L393`, `session:L398`

#### G072 `c01-40` R0 S05: The generated table does not open the view page on a row click in a way the builder could find. The only row-click doc was the e2e test helper, and the embedded table row view button applies to refere

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md`. Only README.md line 212 mentions 'row click or view button'; no section says how a TransferObjectTable opens its view page (row click default versus a rowOperation). Add that behaviour once, checked against generated code.
- **Why:** The catalog has no section on how a TransferObjectTable opens its view page (rowOperations versus row click). **Workaround:** Used a DOM eval to click the grid cell, which opened the view page.
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L738`, `session:L740`, `session:L759`, `session:L761`

#### G073 `c02-31` R2 S11: Titles and menus still show internal names: 'ProductInfo Table', 'ProductInfo View / Edit', and the phone bottom bar shows 'ProductInfo' and 'Other'. Orchestrator requires user-facing labels 'Products

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md`. Docs say labels are i18n keys, but not that default titles come from the transfer object name (e.g. 'ProductInfo Table'). Add: set label on the table/view/menu item or add i18n keys; relates to c02-35/c03-23.
- **Why:** Model labels still carry the entity name; the builder had not set labels or i18n for the pages, menu and bottom bar. **Workaround:** Round 3 task: fix labels via model label and/or i18n, as the kb documents.
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L1407`, `session:L1410`. Merged: c03-23, g-R3-4, g-R6-7, g-R7-13

#### G074 `c04-06` R8 : The numeric price column cannot be shown formatted or sorted another documented way, so the admin table shows 79.9 and the builder only renamed the header to 'Price (EUR)' to fit it.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md`. DataColumn formatValue is listed (line 38) but not what it does; GAPS R12-3 shows generated numeric columns only get a localized number, no currency. Say formatValue is locale number formatting only; for a currency use a unit in the label or a custom visual element with the shared Price component.
- **Why:** The DataColumn schema has formatValue and sort settings, but the builder found no documented way to format a numeric column value (R1-1 and R6-4 remain open). **Workaround:** Kept the numeric column with a shorter label and a width; formatting left open.
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L2360`, `session:L2361`, `session:L2397`, `gaps:R8-3`. Merged: c07-15

#### G075 `c07-14` R12 F45: The label of a row action must be set on the operation form element (TableOperation::<op>::<op>), not on the TableOperation. Setting label on the TableOperation or on a guessed element name failed wit

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md`. Element naming for row action labels is not shown; label belongs on the operation form element TableOperation::<op>::<op>. Add one example with the CLI update command.
- **Why:** Element naming and the label location for row actions are not shown in the catalog. **Workaround:** Set label on ...::changePricesTableOperation::changePrices and ...::requestReturnTableOperation::requestReturn.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L3955`, `session:L4261`, `session:L4262`, `session:L4266`. add→modify (target file exists; add a section)

### `catalog/agent-docs/frontend/i18n.md` (4)

#### G076 `c02-35` R3 S11: Phone bottom bar 'Other' label comes from the i18n key menuTree.other with default 'Other' in the generated BottomMenu. The kb has no section on it, so the builder read the generated source to find it

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/i18n.md`. i18n.md lists menuTree.[MenuLabel] keys (line 66) but not the generated menuTree.other default used by the phone bottom bar. Add that key to the table.
- **Why:** Bottom-bar overflow label is a hard-coded i18n default that the catalog does not document. **Workaround:** Round 3: add an i18n override for menuTree.other via a generator override fragment (see c02-43).
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L1433`, `session:L1434`, `session:L1447`, `session:L1449`. Merged: g-R3-3

#### G077 `c05-46` R10 F40: application_hu-HU.json is not generated: the generator emits only application_en-US.json for this one-language model, while the i18n doc says every application_<locale>.json, including hu-HU, is gener

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/i18n.md`. i18n.md lines 18-23 and 108 say application_hu-HU.json is generated; the generator emits only locales that exist in the model (one-language model gives en-US only). Add: other locale files are written by hand or by a project script and need each new key added.
- **Why:** Catalog statement is wrong for a model with one language. **Workaround:** scripts/make-hu-translations.py builds the Hungarian file from the generated English file (about 190 labels translated; the rest English).
- **Validation:** confirmed; kind catalog-wrong; catalog wrong. Evidence: `session:L3136`, `session:L3137`, `session:L3138`, `session:L3139`. Merged: c07-46, g-R12-15

#### G078 `c05-47` R10 F40: The generated locale map in l10n-context.tsx allows only en-US, and no date-fns locale exists for Hungarian, so the language switch needs a cast and date pickers stay English.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/i18n.md`. Adding New Languages does not mention the generated locale map in l10n-context.tsx (en-US only) or the date-fns locale (only line 487 shows hu). Add both steps.
- **Why:** i18n Adding New Languages steps copy JSON files and update the selector but do not mention the locales map. **Workaround:** Language switch uses the documented L10N setLocale with a cast; date formatting left English.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L3037`, `session:L3038`, `session:L3040`. add→modify (target file exists; add a section)

#### G079 `c05-49` R10 F40: Model-built label strings (for example the order total label and line labels) stay in English with EUR format in Hungarian, because model expressions cannot pick the UI language.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/i18n.md`. Model expressions have no UI language; derived strings stay in one language. Catalog should state "format display strings in the frontend, not in derived model strings". This is a design limit, not a ticket.
- **Why:** Derived string members are fixed text; the Price component is the only locale-aware formatter. **Workaround:** Left as is; logged. Customer cart and shop use the Price component.
- **Validation:** confirmed; kind platform-limit; catalog missing. Evidence: `session:L3199`, `session:L3224`

### `catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md` (4)

#### G080 `c02-48` R5 S10: A custom view layout cannot be made from a placeholder: a ui:Placeholder marked customImplementation generates no scaffold and renders nothing. The builder then removed the price and description field

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md`. widgets.md line 312 only says 'marked for custom implementation'. GAPS R5-2: a Placeholder with customImplementation generates no scaffold and renders nothing; customImplementation on a DataField works. Add that.
- **Why:** Catalog gives no documented hook for replacing a whole view; the placeholder route does not render, and the field-based data load is not documented. **Workaround:** Kept all three view fields as custom implementations; only the name component renders the full layout, the price and description components render nothing.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L1709`, `session:L1711`, `session:L1715`, `session:L1719`

#### G081 `c03-18` R6 F02: Relation widget on the product form rendered as a link button; the builder wanted a dropdown picker for the category and found that a dropdown is a separate widget (isTypeAheadField/autocompleteRows),

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md`. autocompleteRows is documented (line 110, 129) but nothing says a dropdown picker is not a representationComponent value. Add to the to-one relation row of ui-authoring-guide.md: for a picker use button plus autocompleteRows; isTypeAheadField is only for strings.
- **Why:** The mapping of to-one relation to widget is split across attributes and the catalog pages disagree on which values apply. **Workaround:** Kept the table representation and used the existing relation selector in the form.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L1916`, `session:L1918`, `session:L1921`, `session:L1922`

#### G082 `c05-41` R10 F31: The Ordered field on the admin order view showed a date picker icon although it should be read-only; a derived boolean in enabledBy greyed it out but left the picker.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md`. textWidget TEXT is the only read-only switch (string fields only, line 45). Nothing for date, number or enum fields. Add the options: show a derived (non-editable) member instead of the mapped one, or use enabledBy and accept the picker.
- **Why:** The kb has no read-only switch for a mapped timestamp field; isReadOnly exists only for derived members. **Workaround:** Derived string orderedAtLabel replaces the field on both order views (sorting keeps the real timestamp); test checks a text box with no date group or picker button.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L3009`, `session:L3010`, `session:L3011`, `session:L3012`. Merged: c09-09. add→modify (target file exists; add a section)

#### G083 `c10-11` R15 : Setting textWidget=TEXT on read-only string fields removed their labels in the generated order view (values with an icon, no label). The change was reverted to INPUT; the 'read-only shows as text' req

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/esm-to-ui-mappings/widgets.md`. widgets.md line 45 says TEXT=read-only but not that the label is dropped in the generated view. Add that effect; possible generator bug worth a ticket.
- **Why:** The kb says TEXT means read-only but says nothing about labels; the generated theme styles read-only inputs but the builder found no documented labelled-text route. **Workaround:** Reverted all 158 fields to INPUT via .scratch/r15-model.py; relied on the generated theme read-only styling.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L5735`, `session:L5937`, `session:L5938`, `session:L5940`

### `catalog/agent-docs/model/model-development.md` (4)

#### G084 `c03-05` R6 F01, F02: judo create -t MenuItemAccess is refused: the menu item access is created automatically with the actor access.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/model-development.md`. Step 8 (line 56) says a MenuItemAccess must be added by hand. With the CLI, `create -t MenuItemAccess` is refused because the item is created with the actor access (and by fill). Say so; GAPS R12-12 notes a silent failure when naming collides.
- **Why:** Menu item accesses are generated by the Designer cascade, not by a direct create command. **Workaround:** Used create -t Access on the actor and let the cascade create the menu item.
- **Validation:** confirmed; kind catalog-gap; catalog wrong. Evidence: `session:L1788`, `session:L1789`, `session:L2104`

#### G085 `c04-08` R8 F22, F21: Creating a transfer object with a mapping auto-creates the mapped members (lineTotal, total and so on), so hand-made derived members with the same names gave 'not unique' and binding errors on validat

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/model-development.md`. Nothing in the catalog says a transfer object with a mapping auto-creates the mapped members, so a hand-made derived member of the same name is "not unique" (repeat of R7-14). Add one sentence: reuse the generated member, name derived members differently.
- **Why:** Behaviour of mapped transfer objects not described where the builder looked; the same lesson was learned in R7 (R7-14) and repeated. **Workaround:** Deleted the duplicated hand-made members and kept the auto-created ones; validation passed.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L2384`, `session:L2385`, `session:L2408`, `session:L2410`. Merged: g-L10, g-R7-14. add→modify (target file exists; add a section)

#### G086 `c06-01` R11 F41: A derived flag written as a JQL negation on a boolean (filter with !n.read) failed to parse; the builder then used n.read == false.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/model-development.md`. Catalog line 506 shows the !isUndefined escape hatch but I found no JQL negation example for boolean filters. Add: use `n.read == false`, `!n.read` does not parse; the not keyword form (verify).
- **Why:** Builder used a negation form without checking the kb first; the catalog documents the 'not' keyword in model-development.md. **Workaround:** Rewrote the expression as n.read == false.
- **Validation:** confirmed; kind builder-mistake; catalog partly-covered. Evidence: `session:L3382`, `session:L3383`

#### G087 `c07-09` R12 F48: The top-N expression form is unclear: !sort(...)!heads(5) fails in asm2query with 'Missing variable name', and !heads(p \| ..., 5) validates but returns only one row at runtime. The catalog lists !hea

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/model-development.md`. model-development line 332 lists !heads(n) with no top-N example; judo-doc-problems already notes heads is under-documented. Add a validated top-N form and its runtime result once checked (verify).
- **Why:** The catalog documents heads and sort separately; the lambda form and its runtime behaviour are not shown. **Workaround:** Used filter then sort with DESC and let the table page show 5 rows.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L3941`, `session:L3945`, `session:L3947`, `session:L3950`. add→modify (target file exists; add a section)

### `catalog/agent-docs/model/esm_metamodel/accesspoint.md` (3)

#### G088 `c03-49` R7 F14: Creating an actor with a principal auto-creates a Claim per attribute (for example Customer email USERNAME and EMAIL); the builder removed the USERNAME claim so only EMAIL remains.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/esm_metamodel/accesspoint.md`. accesspoint.md describes Claim but not that creating an actor with a principal auto-creates one claim per attribute (EMAIL and USERNAME). Add: keep only the claims the IdP token carries.
- **Why:** The principal and claim cascade in the CLI creates claims by default; the catalog does not say which claim to keep. **Workaround:** Deleted the USERNAME claim on Customer.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L2104`, `session:L2107`, `session:L2108`

#### G089 `c03-43` R7 F13: graphql and CLI queries used Claim name or a claim fqn that does not exist (Customer username USERNAME, Claim name field); the query or update failed.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/esm_metamodel/accesspoint.md`. accesspoint.md lists claims and the JQL key being the DataMember name, but not the CLI route to set or query a Claim. Add one CLI example (verify).
- **Why:** Builder assumed the Claim type has a name field; the schema does not expose it under that name. **Workaround:** Queried Claim fqn only.
- **Validation:** confirmed; kind builder-mistake; catalog partly-covered. Evidence: `session:L2021`, `session:L2022`, `session:L2105`

#### G090 `c10-12` R15 : Customers with a saved browser config keep the old vertical drawer because the layout is stored in localStorage under 'webshop-config', which overrides the new model default.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/model/esm_metamodel/accesspoint.md`. No page says generated client layout config in localStorage overrides a changed model default. Add: users with stored config keep the old layout until it is cleared.
- **Why:** Stored client config wins over the generated default layout; the builder found it by testing and cleared localStorage in the browser. **Workaround:** Cleared the localStorage key in the test browser; real users are not migrated.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L5773`, `session:L5776`, `session:L5778`, `session:L6092`. add→modify (target file exists; add a section)

### `catalog/agent-docs/deployment/schema-evolution.md` (3)

#### G091 `c05-16` R9 F25, F26, F27, F31: Existing Postgres volume was not migrated after the model added SalesOrderLine.product: queries failed with column c_product_id does not exist. ./judo.sh schema-upgrade then failed (SCHEMA_DIR empty, 

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/schema-evolution.md` (also: platform-ticket: judo.sh template default SCHEMA_DIR). judo-ng judo.sh line 991: SCHEMA_DIR=${schema_dir:-$MODEL_DIR}, so the schema POM path is wrong unless schema_dir=application is set; this is a template default and the catalog has no mention of schema_dir. Catalog also claims no step is needed for a dev database, which fails for a persistent volume (L2921).
- **Why:** Generated judo.sh schema-upgrade path bug; the catalog says a development database needs no step, which does not hold for an existing volume with data. **Workaround:** Wipe containers and volumes, restart, scripts/seed-dev-user.sh, seed tests (repeated in R10 with the same failure).
- **Validation:** confirmed; kind platform-bug; catalog wrong. Evidence: `session:L2921`, `session:L2922`, `session:L2924`, `session:L2930`. Merged: g-R9-12, g-R10-3, c07-01

#### G092 `c07-01` R12 F52: ./judo.sh schema-upgrade fails with ProjectBuildingException because SCHEMA_DIR defaults to the model directory (project root), so the schema POM path is <root>/schema. Setting schema_dir=application 

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/schema-evolution.md`. Confirmed from judo.sh (GAPS R12-1): SCHEMA_DIR defaults to the model dir; schema_dir env var or judo.properties line fixes layouts where schema lives under application/. grep over the catalog finds no schema_dir. Add it to the schema-upgrade row.
- **Why:** judo.sh derives SCHEMA_DIR from model_dir; in this layout the schema module lives under application/, and the catalog does not document schema_dir. **Workaround:** Ran schema_dir=application ./judo.sh schema-upgrade, and later the generate/execute route (see c07 F52 decision).
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L3752`, `session:L3753`, `session:L3755`, `session:L4029`. add→modify (target file exists; add a section)

#### G093 `c09-13` R14 : judo-cli generate printed the line 'ERROR DATABASE HAVE TO BE UPDATED!' and then BUILD SUCCESS, so the level of the message is misleading.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/schema-evolution.md`. Message appears in the session; level is misleading but build succeeded. Add to schema-evolution.md: "ERROR DATABASE HAVE TO BE UPDATED!" during generate is a notice, not a build failure; it means a migration step is needed.
- **Why:** Log level of the migration check does not match its meaning. **Workaround:** Read the message as informational and continued with the migration route.
- **Validation:** partly; kind cli-tool; catalog partly-covered. Evidence: `session:L5336`

### `catalog/agent-docs/frontend/hooks/action-hooks.md` (3)

#### G094 `c05-50` R10 F36: After Apply coupon or Remove coupon the generated cart page does not give the custom cart summary component new data, so the total stayed stale.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/hooks/action-hooks.md`. Custom visual components are not refreshed after operations; window event workaround is the builder pattern. Add the recipe; not enough to call it a bug.
- **Why:** Post-operation flow does not refresh custom visual components. **Workaround:** Post-operation hooks dispatch a window event; the cart component listens and reloads; cart component also reloads on new signed identifier.
- **Validation:** partly; kind platform-limit; catalog missing. Evidence: `session:L3130`, `session:L3193`, `session:L3195`, `session:L3197`

#### G095 `g-R10-11` R10 F39: The post-operation hook is registered per page key; the order view exists as three pages (two admin, one shop), so three registrations are needed; without a hook the output dialog shows only a downloa

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/hooks/action-hooks.md`. action-hooks.md documents the post<Operation>For<Page>Action naming, which implies per page. Add one line: the same operation shown on N pages needs N hook registrations.
- **Why:** Hooks are keyed by generated page/operation name. **Workaround:** Registered the hook for each page.
- **Validation:** partly; kind none; catalog partly-covered. Evidence: `gaps:R10-11`

#### G096 `c08-20` R13 F55: After the buyer joins with the key, the My company menu does not appear until the shell starts again.

- [ ] **Issue**  Action: [x] add [ ] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** add-catalog → `agent-docs/frontend/hooks/action-hooks.md`. Menu is built at shell start; after an operation changes the actor access, reload with window.location.assign. Session only, low evidence.
- **Why:** Builder comment says menu entries are decided from the principal read at shell start, so a page change does not refresh them. **Workaround:** Post-join hook calls window.location.assign on the start URL to reload the shell.
- **Validation:** partly; kind platform-limit; catalog missing. Evidence: `session:L4868`, `session:L4879`, `session:L4889`

### `catalog/agent-docs/frontend/README.md` (2)

#### G097 `c01-36` R0 S05: The frontend uses a hash router. Pages open at /webshop/Shop/#/Shop/Products/..., so direct paths without the hash return 404. The catalog does not mention this.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/README.md`. No mention of hash routing in the catalog (grep found no hash router text). Add: routes are hash based, URLs look like /<model>/<Actor>/#/<route>, direct paths without # return 404; Playwright goto must use the hash URL.
- **Why:** Frontend docs do not describe the router type or the URL shape. **Workaround:** Used hash URLs (for example #/Shop/Products/AccessTablePage).
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L651`, `session:L652`, `session:L684`, `session:L686`. add→modify (target file exists; add a section)

#### G098 `c03-51` R7 F09, F14: After generate alone the new webshop__customer and webshop__admin modules had no src/custom folder; it appeared only after the build. The catalog does not say when src/custom is created.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/README.md`. README lines 27-28 say scaffolds are generated under src/custom but not when. Session says it appears after the build, not generate; add this if confirmed (verify).
- **Why:** Generation creates the module shell; the custom folder and hook scaffolds come from the build step, which the catalog does not state. **Workaround:** Read the generated tree; no custom code moved yet; decision deferred to the frontend step.
- **Validation:** partly; kind catalog-gap; catalog missing. Evidence: `session:L2113`, `session:L2117`, `session:L2118`, `session:L2121`

### `catalog/agent-docs/backend/authentication-guide.md` (2)

#### G099 `c03-75` R7 F13, F16: Interceptor provisioned a CustomerAccount row for admin@example.com because the admin user also logs in through the customer client; the decision was made on the client argument and the token azp had 

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/backend/authentication-guide.md`. Signature with `client` is shown (lines 30-31) and the azp claim is explained at line 228, but not what the client argument holds. Add: for dual-actor realms decide on the token azp, not the client argument.
- **Why:** The client argument passed to AuthenticationInterceptor is not the client id the builder expected; the catalog does not say what it contains. **Workaround:** Read the azp claim, logged the origin, and returned early for non-customer clients; a stray admin row was then removed.
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L2314`, `session:L2323`, `session:L2326`, `session:L2327`

#### G100 `c03-76` R7 F14: A customer who opens the back office URL gets a User not found page instead of an access message.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/backend/authentication-guide.md`. No description of the wrong-actor outcome; it is plausible platform behaviour (User not found), the access message would be a custom page. Add a short note of the observed behaviour.
- **Why:** The expected error for a wrong actor is not described in the catalog as far as the builder reported. **Workaround:** Reported as a known behaviour in the round report; no test change.
- **Validation:** partly; kind catalog-gap; catalog missing. Evidence: `session:L2347`

### `catalog/agent-docs/backend/custom-operations.md` (2)

#### G101 `c04-25` R8 F23: No catalog text found by the builder on whether a custom operation rolls back on error; the builder proved it with a test instead (stock of the first line restored when the second line throws a ShopFa

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/backend/custom-operations.md`. custom-operations.md only has test transaction modes (AUTO_ROLLBACK); no runtime rule. Builder proved by test that an exception in a custom operation rolls back all its writes. Add that line (mark verify against the dispatcher).
- **Why:** The backend docs cover rollback for interceptors and for integration test modes (AUTO_ROLLBACK) but not the runtime rule for custom operations; the builder's kb search for the rule found nothing. **Workaround:** Integration-style Playwright test proves the rollback of stock, cart and order.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L2380`, `session:L2381`, `session:L2537`, `session:L2539`. add→modify (target file exists; add a section)

#### G102 `c06-12` R11 F44: The CSV export custom operation threw a NullPointerException on input.getFromDate().orElse(...) when the user left the date empty, because the optional input getter returned null, not Optional.empty.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/backend/custom-operations.md`. custom-operations.md does not say that optional input getters can return null instead of Optional.empty (sweep item BA-042). Add: null-check optional input getters (verify).
- **Why:** Custom operation input getters for optional attributes can return null; the agent-docs custom-operations page does not say this where the builder looked, and the sweep inventory (BA-042) already flagged it. **Workaround:** Null-guarded the getters and the status filter in ExportOrdersCustomImplementation.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L3646`, `session:L3647`. add→modify (target file exists; add a section)

### `catalog/best-practices/backend/relation-based-entity-creation.md` (2)

#### G103 `c05-05` R9 F31: The per-relation createHistory method did not exist until the relation had createable=true, which the builder only found after a failed build.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/backend/relation-based-entity-creation.md`. The page says the create method exists only if the relation allows creation but never names the createable=true attribute. Add: set createable=true on the relation or createX is not generated.
- **Why:** relation-based-entity-creation.md states the createable rule in one sentence that the builder missed on first read. **Workaround:** Set createable=true on SalesOrder.history in the model, then the generated create method appeared.
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L2788`, `session:L2872`, `session:L2874`, `session:L2875`

#### G104 `c09-18` R14 F69, F70: DAO create on a non-composition two-way relation (customerAccountDao.createPointEntries, createGiftCards) failed with MISSING_REQUIRED_RELATION; only the child DAO create with the back reference works

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/backend/relation-based-entity-creation.md`. Page recommends parent-DAO create for containment only; builder shows non-composition two-way relations fail with MISSING_REQUIRED_RELATION through the parent DAO. Add: for plain two-way relations create through the child DAO with the back reference.
- **Why:** The kb covers creation through composition parents only; the builder found no note for plain two-way relations. **Workaround:** pointsEntryDao.create(builder.withCustomer(customer)) and giftCardDao.create(builder.withBuyer(buyer)).
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L5371`, `session:L5531`

### `catalog/best-practices/backend/init-data-seeding.md` (2)

#### G105 `c05-08` R9 F32: No documented way to backdate or seed an old order in a running-app Playwright test, so the 30-day cut-off itself is untested.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/backend/init-data-seeding.md`. No page covers seeding or backdating rows for a running-app Playwright test (init-data-seeding and runtime-fixture pages cover Java tests only). Add the route used (SQL via psql or a test-only operation).
- **Why:** Order timestamps are set only by checkout; the initializer has no documented trigger; the kb fixture examples are for Java integration tests, not the running app. **Workaround:** Test checks that today's order is in the 30-day list and in All orders; the cut-off is left untested and logged.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L2748`, `session:L2749`, `session:L2773`, `session:L2776`. add→modify (target file exists; add a section)

#### G106 `c05-60` R10 F33: The shop settings singleton has no startup seed: the model blueprint says the row is seeded by an initializer, but no startup trigger is documented, so the admin enters it once through the UI and a se

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/backend/init-data-seeding.md`. The initializer blueprint says the project calls init from a startup or deployment routine but gives no concrete trigger and no singleton duplicate guard. Add: the platform does not auto-run init (verify); call it from a deployment script and guard with a count check.
- **Why:** Catalog gives no trigger for init operations and no rule for singleton duplicates in the running app. **Workaround:** Seed test creates the settings row through the admin UI if none exists.
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L3015`, `session:L3016`, `session:L3018`, `session:L3019`

### `catalog/best-practices/model/standard-type-library.md` (1)

#### G107 `c01-17` R0 S02: The predefined Text type is limited to 250 characters, which is too short for a product description. The catalog does not say so and does not name a long-text type.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/model/standard-type-library.md`. Catalog says Text limits vary (250 to 4000) and tells to pick one, but a model built from scratch has the 250 default. Add one line: for descriptions define a longer Text type (e.g. 2000) in the model; do not use the 250 one.
- **Why:** Type doc lists StringType widget properties but not the Text length limit. **Workaround:** Added StringType LongText with maxLength 4000 in webshop::types.
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L102`, `session:L104`, `session:L119`, `gaps:R0-9`. Merged: g-L9

### `catalog/agent-docs/frontend/hooks/table-hooks.md` (1)

#### G108 `c01-19` R0 S04: The table column customizer example in table-hooks.md uses a (original) => ... signature and registration that do not match the shipped type, which is () => ColumnCustomizer.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/hooks/table-hooks.md`. Example uses (original) => ({...}); shipped type in utilities/table.ts is ColumnCustomizerHook<T> = () => ColumnCustomizer<T>, ColumnCustomizer = (original) => GridColDef. Fix the example. Also GAPS R12-3: generated tables import the key but never consume it (platform bug, see c02-14).
- **Why:** Docs out of date against utilities/table.ts in the generated app. **Workaround:** Not used. Builder edited generated code instead.
- **Validation:** confirmed; kind catalog-wrong; catalog wrong. Evidence: `session:L402`, `session:L403`, `session:L414`, `gaps:R0-12`. Merged: c02-14, c02-17

### `catalog/best-practices/frontend/i18n-generator-override-extra-fragment.md` (1)

#### G109 `c02-36` R3 S11: Path and format of an i18n extra fragment for application_default.json were not in the kb. The builder first wrote the fragment under ui-react/actor/public/i18n with an unbraced JSON line, then found 

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/frontend/i18n-generator-override-extra-fragment.md`. Page line 34 gives `ui-react/actor/public/i18n/` under the override directory and the no-braces rule, but calls it unverified; the builder confirmed from the template jar that the file is actor/public/i18n/application_default_extra.fragment.hbs relative to generator-overrides. Make the root explicit (generator-overrides/ui-react/...) and mark as verified.
- **Why:** Best-practice page i18n-generator-override-extra-fragment.md says the path is project practice and not covered by agent-docs; the kb search did not return the template path. **Workaround:** Moved the fragment to application/frontend-react/generator-overrides/ui-react/actor/public/i18n/application_default_extra.fragment.hbs (override dir from the frontend pom), removed the wrong folders and rebuilt; menuTree.other became 'More' in application_en-US.json.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L1477`, `session:L1483`, `session:L1484`, `session:L1485`. Merged: g-R3-2

### `catalog/agent-docs/frontend/hooks/README.md` (1)

#### G110 `c02-49` R5 S10: After the view fields were removed, regeneration dropped the view's .default scaffold, but the builder's copied register file stayed in src/custom. The frontend build then failed (TS2305 missing expor

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/hooks/README.md`. Not covered. Add: a hand-copied scaffold is never removed when its element disappears; delete the copied register file when the model element is removed, or the frontend build fails (TS2305).
- **Why:** A hand-copied scaffold is not removed by generate; the catalog does not say what happens to a copied scaffold when its element disappears. **Workaround:** Rewrote the register file by hand for the remaining custom elements and rebuilt.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L1711`, `session:L1712`, `session:L1713`, `session:L1714`

### `catalog/agent-docs/frontend/extension-points.md` (1)

#### G111 `c02-52` R5 S08: The generated dashboard page already renders a ComponentProxy for the custom visual element key DashboardPage, with a Hello! fallback. A service registered under that key replaces the home page. The k

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/extension-points.md`. Seam not documented: generated DashboardPage renders a ComponentProxy for the key DashboardPage with a Hello! fallback (GAPS R5-1). Add a row: register a CUSTOM_VISUAL_ELEMENT service with component='DashboardPage' to replace the home page.
- **Why:** Catalog only covers a dashboard without layout (component-proxy-placeholder-page.md, project practice) and Extra Routes; the generated seam for the dashboard is not documented. **Workaround:** Registered CatalogHome via src/custom/hooks/registerCatalogHome.tsx from application-customizer.tsx (already generator-ignored); no generated file touched.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L1692`, `session:L1694`, `session:L1697`, `session:L1700`

### `catalog/best-practices/backend/multi-tenant-keycloak-realm.md` (1)

#### G112 `c03-56` R7 F13: The model has no setting for Keycloak self sign-up (registrationAllowed); the generated realm JSON leaves it unset, so the builder had to set it through the Keycloak admin API.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/backend/multi-tenant-keycloak-realm.md`. The practice shows createRealm(name, registrationAllowed) in code but not that the generated realm JSON leaves self sign-up off with no model setting. Add: for the generated realm enable registration through the Keycloak admin API or a realm-json override.
- **Why:** The platform's generated realm does not expose a self sign-up switch in the documented model settings; catalog does not cover it. **Workaround:** Logged as GAPS R7-3; the seed script switches self sign-up on through the Keycloak admin API.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L2135`, `session:L2137`, `session:L2138`, `session:L2139`. Merged: g-R7-4

### `catalog/best-practices/frontend/dual-actor-frontend-architecture.md` (1)

#### G113 `c03-57` R7 F14: Generated actor modules (webshop__admin, webshop__customer) each get their own e2e module; the Level 0 Playwright tests had to be split across them by hand (git mv).

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/frontend/dual-actor-frontend-architecture.md`. Page covers per-actor frontend modules but not per-actor e2e modules. Add: each actor also gets its own e2e module; split tests per actor. Also stale webshop__shop dirs remain after the actor split (GAPS R7-6).
- **Why:** Each actor has its own generated e2e and frontend module; the catalog does not say how existing tests move between them. **Workaround:** Moved helpers and specs to the matching module, changed the base URL to Admin or Customer, and added actor-specific login helpers.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L2153`, `session:L2154`, `session:L2156`, `session:L2157`

### `catalog/agent-docs/backend/data-access-guide.md` (1)

#### G114 `c05-04` R9 F29: A 0..1 relation query returns Optional<Product>, while a 1..1 relation query returns the entity; the first build failed with a type mismatch because the builder assumed Optional.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/backend/data-access-guide.md`. data-access-guide (lines 289-304) says single-valued relation queries return the entity directly; the generated SDK returns Optional<T> for 0..1 (SalesOrderLineDao shows Optional types). Split the rule: 0..1 returns Optional, 1..1 returns the entity.
- **Why:** The kb says single-valued relation queries return the entity but does not separate optional (0..1) from mandatory (1..1) relations. **Workaround:** Used the entity directly for the 1..1 cart line product relation (RemoveProductCustomImplementation.java).
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L2788`, `session:L2870`, `session:L2871`, `session:L2883`

### `catalog/best-practices/backend/markdown-handlebars-pdf-report.md` (1)

#### G115 `c05-42` R10 F39: No runnable recipe in the kb for a Markdown Handlebars template rendered to PDF; the only document pipeline in the kb is the DOCX XDocReport one.

- [ ] **Issue**  Action: [x] add [ ] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** add-catalog → `catalog/best-practices/backend/markdown-handlebars-pdf-report.md`. No recipe for Markdown plus Handlebars rendered to PDF; judo-doc-problems already records a project that migrated to it (entry about replacing the XDocReport leg). Write the pipeline page.
- **Why:** Catalog covers Handlebars email rendering, file store transfer and inline preview, but no Markdown to PDF step. **Workaround:** invoice.md.hbs rendered with Handlebars 4.2.0 (already in runtime), turned into PDF by a small Markdown renderer on PDFBox 2.0.13 (already in runtime), stored via FileStoreService, returned as FileType.
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L2992`, `session:L2994`, `session:L2996`, `session:L2998`

### `catalog/model-blueprints/xdocreport-document-generation-pipeline/BLUEPRINT.md` (1)

#### G116 `c05-43` R10 F39: The XDocReport DOCX pipeline blueprint is still presented as a current pattern with no deprecation note, although the project lead says the pipeline is deprecated.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/model-blueprints/xdocreport-document-generation-pipeline/BLUEPRINT.md`. Blueprint has no deprecation note. judo-doc-problems describes XDocReport as the legacy leg replaced by Markdown plus Handlebars, which supports the claim (the lead statement itself is unverifiable). Add a legacy note linking the replacement.
- **Why:** Blueprint status fields say single-project and do not mark deprecation. **Workaround:** Not used; a Markdown route was built instead.
- **Validation:** partly; kind catalog-wrong; catalog wrong. Evidence: `session:L2991`, `session:L2998`, `session:L2999`

### `catalog/agent-docs/backend/platform-behavior-reference.md` (1)

#### G117 `c06-15` R11 : The 'Ordered' text and history times differed by two hours: the model-built string orderedAtLabel used the platform zone (UTC), while the generated history column rendered in the browser zone (CET).

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/backend/platform-behavior-reference.md`. Time and Time Zones section (line 94) already says model expressions follow defaultZoneId, not the JVM. Add the contrast: generated UI columns render in the browser zone, so model-built strings differ by the zone offset.
- **Why:** Model expressions follow the platform defaultZoneId, the UI follows the browser; the catalog says so but gives no model-side way to show the browser zone. Container is UTC, host CET; default zone already UTC so storage needed no change. **Workaround:** Removed the derived string; see c06-16.
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L3236`, `session:L3238`, `session:L3320`, `session:L3321`

### `catalog/agent-docs/frontend/theming.md` (1)

#### G118 `c07-24` R12 F51: Builder claims there is no documented way to read brand values from a runtime settings row; palette and logo are fixed at start-up.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/theming.md`. theming.md line 101 says brand colours belong on ActorType attributes, which implies fixed at generation, but never states runtime branding is not supported. Add one line stating that.
- **Why:** Builder's reading of theming.md, which says brand colours belong to model attributes; the catalog does not state whether runtime branding is possible. **Workaround:** Decision recorded (see F51 decision).
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L3900`, `gaps:R12-8`

### `catalog/agent-docs/backend/interceptors.md` (1)

#### G119 `c07-29` R12 F50: The builder could not find how to read old and new values in the update interceptor and decompiled the dispatcher jar with javap to learn UpdateInstanceCallPayload, without a kb search.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/backend/interceptors.md`. interceptors.md already shows UpdateInstanceCallPayload (getInstance, getInput) but no example of reading old versus new values. Builder skipped kb search first. Add a short old/new comparison example (verify what the payload exposes).
- **Why:** Interceptor payload access is not clear from the interceptor page as the builder read it (unverified); the kb was not searched first. **Workaround:** Used getInput() and getInstance() from the decompiled class.
- **Validation:** partly; kind catalog-gap; catalog partly-covered. Evidence: `session:L3889`, `session:L3892`, `session:L3893`

### `catalog/agent-docs/integration-testing/getting-started.md` (1)

#### G120 `c07-33` R12 F53: The documented command 'mvn clean test -pl application/integration-test' fails from the project root with 'Could not find the selected project in the reactor', because the module is not in the root re

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/integration-testing/getting-started.md`. getting-started lines 574-610 and osgi-ds-descriptor-tests line 75 both give mvn -pl application/integration-test from the root; the session and GAPS R12-5 show this fails because the module is not in the reactor. Change to run mvn from the module directory.
- **Why:** Catalog command does not match the reactor layout described on the osgi page. **Workaround:** Ran mvn test from the module directory (later the order-tests module).
- **Validation:** confirmed; kind catalog-wrong; catalog wrong. Evidence: `session:L4180`, `session:L4181`, `session:L4182`, `session:L4183`

### `catalog/agent-docs/integration-testing/best-practices.md` (1)

#### G121 `c07-34` R12 F53: The testkit has no generated DAO module: the best-practices example uses a project AppDaoModules class that does not exist in the generated project, so the test failed with 'No implementation for Shop

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/integration-testing/best-practices.md`. best-practices.md line 310 uses AppDaoModules, a class that does not exist in a generated project. Show a small project module with one @Provides per DAO or mark the class as an example to write.
- **Why:** Catalog example assumes a project DAO module; the generated project does not provide one and the page does not say how to make one. **Workaround:** Hand-written WebshopDaoModule over ReferenceInjector.
- **Validation:** confirmed; kind catalog-gap; catalog wrong. Evidence: `session:L4207`, `session:L4208`, `session:L4209`, `session:L4212`

### `catalog/best-practices/model/derived-access-filtering.md` (1)

#### G122 `c09-19` R14 F62: A seller who opened the direct page address of another seller's product got the product, its status and an Unpublish button. The access filter hid it from lists only.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/model/derived-access-filtering.md`. derived-access-filtering.md says visibility is enforced by the model but does not say a direct GET/update by identifier bypasses list filters. Add a security warning and a write-guard interceptor pointer (verify with the dispatcher).
- **Why:** Derived access filters restrict the generated list queries; a direct identifier GET or update is not filtered. Signed identifiers are not bound to a user. **Workaround:** SellerOwnershipInterceptor on refresh and update, plus ownership checks inside the custom operations; the page shows a refusal toast and an empty form.
- **Validation:** confirmed; kind catalog-wrong; catalog missing. Evidence: `session:L5479`, `session:L5480`, `session:L5488`, `session:L5490`

### `catalog/agent-docs/frontend/advanced-patterns.md` (1)

#### G123 `c09-28` R14 F68: Rates were returned, but the customer currency switch treated the rate as absent: validOn arrives as a Date object in the generated service, so the string comparison of the day failed.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/advanced-patterns.md`. Catalog never says generated services deserialize date fields to Date objects (so string compare fails). Based on the builder's reading of generated code only; add with verify.
- **Why:** Builder's reading of the generated serializer: dates are turned into Date objects; not documented in the catalog as far as checked. **Workaround:** Compare calendar days built from the Date object in CurrencySwitch.tsx.
- **Validation:** partly; kind catalog-gap; catalog missing. Evidence: `session:L5466`, `session:L5472`, `session:L5475`. add→modify (target file exists; add a section)

### `catalog/agent-docs/backend/type-system-guide.md` (1)

#### G124 `c09-45` R14 F65: Builder states the generated SDK exposes Price and decimal values as java.lang.Double (for example SubOrder.getTotal returns Optional<Double>), so money must be rounded explicitly in Java.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/backend/type-system-guide.md`. Generated SDK shows Optional<Double> for decimal and Price values (SalesOrderLineDao in session L4000). type-system-guide does not state it; judo-doc-problems already has a numeric-mapping entry. Add: round money explicitly.
- **Why:** Observed in generated sources; the builder did not find this stated in the type-system guide. **Workaround:** Money helper (see decision on F65).
- **Validation:** confirmed; kind catalog-gap; catalog missing. Evidence: `session:L5294`, `session:L5157`

### `catalog/best-practices/frontend/multi-step-operation-flow.md` (1)

#### G125 `c10-15` R15 : The kb gives the Stepper widget (a form layout) as the step-flow answer; no catalog entry covers a multi-step operation flow like checkout.

- [ ] **Issue**  Action: [x] add [ ] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** add-catalog → `catalog/best-practices/frontend/multi-step-operation-flow.md`. Stepper is documented as a form layout only; no pattern for a multi-step operation flow like checkout. Add a pattern page (custom visual element inside the cart page).
- **Why:** kb_search for 'multi-step wizard stepper checkout flow' matched form widgets only. **Workaround:** Built a custom component instead of a model Stepper.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L5870`, `session:L5871`

### `catalog/agent-docs/e2e-testing/README.md` (1)

#### G126 `c10-21` R15 : The Playwright e2e suite runs against the packaged app on port 8181, so the fast Vite loop does not cover it. Each e2e verification needed a full judo.sh build (about 4.5 min per run).

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/README.md`. e2e README line 24 already says tests run against the backend-served frontend, not the dev server. Add the cost: every e2e check needs a full judo.sh build (about 4.5 minutes).
- **Why:** No documented way found to point the e2e suite at the dev server; the kb guidance covered only the dev server for manual checks. **Workaround:** Ran the full build script in the background (.scratch/r14-rebuild.sh) before each e2e run.
- **Validation:** partly; kind catalog-gap; catalog covered. Evidence: `session:L5894`, `session:L5960`, `session:L5963`, `session:L6082`

### `catalog/agent-docs/frontend/development-workflow.md` (1)

#### G127 `c02-01` R1 S04, S09: Builder assumed ./judo.sh generate would regenerate the frontend table component after reverting the S04 patch. It did not; the frontend build (judo.sh build -f -i) was needed.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/development-workflow.md`. Workflow page covers prune and dev server but not that generate does not regenerate frontend sources; add: frontend files are regenerated by judo.sh build -f -i.
- **Why:** Builder assumed the generate step covers frontend files; it only writes the scaffolds and model-derived sources. **Workaround:** Ran ./judo.sh build -f -i, after which the table component was regenerated.
- **Validation:** confirmed; kind builder-mistake; catalog partly-covered. Evidence: `session:L929`, `session:L930`, `session:L931`. Merged: g-R1-5

### `catalog/best-practices/model/actor-based-transfer-projection.md` (1)

#### G128 `c04-03` R8 F17, F21, F22, F24: The customer API returned stock, active and variants on the product list and details (data leak), because the customer used the admin-facing product transfer object.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/model/actor-based-transfer-projection.md`. Page exists; add a warning: never expose an admin mapped transfer object (stock, active) through a customer access; define a separate projection per actor. A rule in the builder prompt would also catch it.
- **Why:** Own design mistake from earlier rounds: the customer product access pointed at the mapped ProductInfo, which carries admin-only fields. **Workaround:** New mapped transfer object ShopProductInfo without stock, active and variants; Customer.products points at it; ProductInfo stays admin only; test watches server answers for a browsing customer.
- **Validation:** confirmed; kind builder-mistake; catalog partly-covered. Evidence: `session:L2348`, `session:L2384`, `session:L2386`, `session:L2574`. Merged: g-R7-8. add→modify (target file exists; add a section)

### `catalog/agent-docs/e2e-testing/helpers-reference.md` (1)

#### G129 `c05-57` R10 F36, F39: Test helper problems: the PDF text check failed because parentheses are escaped in the content stream; the generated date field is a group of spin-button segments, not a text box; a debug spec was use

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/e2e-testing/helpers-reference.md`. Session L3175 shows the PDF content stream escapes parentheses; GAPS confirms date fields render as spin-button segments. Add: date inputs are segmented (click the month segment and type digits); PDF text is in the content stream so escape parentheses in regexes. The debug-spec part is general practice.
- **Why:** Test-level assumptions about PDF text and the generated date widget, not documented in writing-tests.md. **Workaround:** Regex escapes the parentheses; typeDate clicks the Month segment and types digits; debug spec removed after use.
- **Validation:** confirmed; kind test-design; catalog missing. Evidence: `session:L3174`, `session:L3175`, `session:L3177`, `session:L3183`. add→modify (target file exists; add a section)

### `catalog/agent-docs/frontend/esm-to-ui-mappings/README.md` (1)

#### G130 `c03-66` R7 F09: Admin product view cannot show the stored image: the generated binary field is an upload control that shows the file name, so the image test on the admin view was changed to check the file name.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/frontend/esm-to-ui-mappings/README.md (binary field)`. The generated admin binary field is an upload control showing the file name; this is design behaviour, not a bug. Catalog should say that an image preview needs a custom visual element (see binary-blob-url-hook.md).
- **Why:** The generated admin binary widget is an upload field; a picture view needs a custom display, which the customer front provides. **Workaround:** Admin test asserts the file name; the customer front shows the image through the generated ImageDisplay path.
- **Validation:** partly; kind platform-limit; catalog missing. Evidence: `session:L2244`, `session:L2283`, `session:L2285`, `session:L2347`

### `catalog/model-blueprints/invitation-with-key-based-acceptance/BLUEPRINT.md` (1)

#### G131 `c08-12` R13 F55: Invitation key blueprint assumes an anonymous actor, so the invitee cannot accept the key without a Keycloak account. The builder adds sign-up first, then key entry, and shows the key in the admin tab

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/model-blueprints/invitation-with-key-based-acceptance/BLUEPRINT.md`. The blueprint already uses an anonymous actor (BLUEPRINT.md:20), so the builder chose sign-up first by project design. Add a variant: when the invitee must become a Keycloak user, sign up first, then enter the key.
- **Why:** Chunk does not show why anonymous acceptance was not used. GAPS R13-3 records the decision as platform limit with no mail server. **Workaround:** Key shown in the open-invitations table and logged; invitee signs up, then enters key on Join a company; acceptance checks key, expiry and e-mail and deletes the invitation in one transaction.
- **Validation:** partly; kind platform-limit; catalog partly-covered. Evidence: `session:L4481`, `session:L4537`, `session:L4541`, `session:L4879`

### `catalog/model-blueprints/osgi-scheduled-background-jobs/BLUEPRINT.md` (1)

#### G132 `c09-42` R14 F70: Loyalty points expire only by a call from an admin dashboard action or at checkout; there is no scheduled expiry job.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/model-blueprints/osgi-scheduled-background-jobs/BLUEPRINT.md`. The blueprint needs a scheduler module; GAPS R14-9 says the generated runtime has none. Add the fallback: call the expiry service from an admin action and at checkout.
- **Why:** osgi-scheduled-background-jobs needs a scheduler module the generated runtime does not have, and a job has no request transaction. **Workaround:** LoyaltyService.expireAll(now) called from the admin action and at each checkout.
- **Validation:** confirmed; kind platform-limit; catalog partly-covered. Evidence: `session:L5134`, `session:L5138`, `session:L5531`

### `catalog/agent-docs/deployment/osgi-runtime-services.md` (1)

#### G133 `c05-45` R10 F39: The Karaf runtime already contains PDFBox 2.0.13 and Handlebars 4.2.0 (karaf-offline assembly and karaf features), so no new bundle is needed for an invoice renderer.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/agent-docs/deployment/osgi-runtime-services.md`. Catalog says extra bundles (PDFBox, Handlebars) are added to the Karaf feature (best-practices osgi-karaf-bundle-architecture.md line 41), which is the opposite of the builder's finding that PDFBox 2.0.13 and Handlebars 4.2.0 already ship in the runtime. Not re-checked in the runtime assembly; mark verify. Add: 'Libraries already in the runtime (verify versions): PDFBox 2.0.13, Handlebars 4.2.0' and reconcile line 41.
- **Why:** Found by searching the built runtime; the catalog has no list of runtime-provided libraries.
- **Validation:** partly; kind none; catalog partly-covered. Evidence: `session:L3004`, `session:L3005`, `session:L3008`

### `catalog/best-practices/model/bidirectional-relation.md` (1)

#### G134 `g-R11-4` R11 F41: create TwoWayRelationMember makes the partner named after the type (customerAccount) with cardinality 0..1; a JQL over it fails with "ObjectFilterExpression cannot be cast to CollectionExpression" unt

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/model/bidirectional-relation.md`. Session L3303 starts the wishlist design; catalog has TwoWayRelationMember only as metamodel mapping (ui-authoring-guide.md line 136), no CLI default note. Add: after create TwoWayRelationMember, rename the partner and set its cardinality to 0..* for many-to-many. Not independently re-run.
- **Why:** CLI create defaults for the opposite end. **Workaround:** Renamed partner to wishedBy and set 0..*.
- **Validation:** partly; kind cli-tool; catalog missing. Evidence: `session:L3303`, `gaps:R11-4`. add→modify (target file exists; add a section)

### `catalog/best-practices/model/null-safe-collection-aggregation.md` (1)

#### G135 `g-R11-6` R11 F43: The kb says it does not document what !avg does on an empty collection; it ran without error and returned an empty value.

- [ ] **Issue**  Action: [ ] add [x] modify [ ] one-off [ ] ticket [ ] tool [ ] drop
- **Proposed:** modify-catalog → `catalog/best-practices/model/null-safe-collection-aggregation.md`. The file (line 26) says empty-collection behaviour is not documented and tells to use a ternary guard. Add the observed fact (verify): !avg over an empty collection returns undefined with no error; compare !count() first for labels.
- **Why:** Platform behaviour undocumented in catalog. **Workaround:** No guard on !avg; ratingLabel guards on count.
- **Validation:** confirmed; kind catalog-gap; catalog partly-covered. Evidence: `session:L3362`, `gaps:R11-6`

## B. Platform tickets (judo-ng)

#### G136 `c01-20` R0 S04: After the generated table was patched and listed in .generator-ignore, ./judo.sh build -f failed with 'manual changes' on many generated frontend files (App.tsx, auth files, components). Only build -f

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-tatami / generator checksum + Biome reformat` (also: modify-catalog: catalog/agent-docs/deployment/build-process.md or frontend/build-and-deployment.md: "A second build can fail with manual changes on untouched files (Biome reformats after checksum capture); use build -i; .generator-ignore does not cover these."). Catalog documents -i (build-process.md:221) and .generator-ignore (custom-public-assets.md:28) but nothing on the false positive where the frontend build reformats generated files after checksum capture, which is what hit App.tsx and auth files; judo-doc-problems.md already lists this. Session L423-427 is the symptom, not a root cause in judo-ng.
- **Why:** Generator checksum check is not satisfied by the module .generator-ignore entry, so every changed or unlisted generated file blocks the frontend build. -i disables the check and refreshes checksums, which also hides real manual edits. **Workaround:** Ran ./judo.sh build -f -i, later ./judo.sh build -M -B -i.
- **Validation:** partly; kind platform-limit; catalog partly-covered. Evidence: `session:L423`, `session:L426`, `session:L427`, `session:L539`. Merged: c05-17, g-L13

#### G137 `c01-34` R0 S05, S06: After a frontend-only rebuild, Karaf still served the old frontend bundle from application/.karaf/system. The builder had to delete application/.karaf and restart.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo.sh (karaf start / application/.karaf/system refresh)` (also: modify-catalog: catalog/agent-docs/frontend/development-workflow.md: "After a frontend-only rebuild, stop, rm -rf application/.karaf and start if the old bundle is still served."). Session L557-569 shows the old asset index served until application/.karaf was removed and the cause is the Karaf system repo caching the SNAPSHOT jar; judo.sh uses KARAF_DIR=${APP_DIR}/.karaf (L925). Likely stale-SNAPSHOT behaviour rather than a distinct bug; cause not proven.
- **Why:** Unpacked Karaf assembly was not refreshed by build -f; the old jar stayed in .karaf/system. **Workaround:** rm -rf application/.karaf, then build -i and start.
- **Validation:** partly; kind platform-bug; catalog missing. Evidence: `session:L557`, `session:L560`, `session:L566`, `session:L569`

#### G138 `c01-37` R0 S03: Karaf startup prints 'Visit http://localhost:8181/api-spec/webshop', but that URL returns 404.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng runtime__judo-services/judo-services-healthcheck-osgi ApplicationListener.java:224` (also: modify-catalog: catalog/agent-docs/deployment/osgi-runtime-services.md: note that /api-spec/<model> returned 404 in the webshop run (verify), use generated frontend REST paths.). Banner prints http://localhost:8181/api-spec/webshop (ApplicationListener.java:224) and session L476-477 shows 404 for that exact URL. Catalog deployment/README.md:161 and osgi-runtime-services.md:103 promise the same URL; trailing slash or later servlet registration not tested.
- **Why:** Startup log link does not match the served API spec path (the REST root is under /api/). **Workaround:** Used REST paths from the generated frontend services.
- **Validation:** partly; kind platform-bug; catalog partly-covered. Evidence: `session:L158`, `session:L476`, `session:L477`

#### G139 `c01-44` R0 S01: Build log showed ERROR lines for com.sun:tools systemPath ${tools.jar} but BUILD SUCCESS was reported.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng project template pom (tools.jar systemPath)` (also: modify-catalog: catalog/agent-docs/deployment/build-process.md: "com.sun:tools systemPath errors in the Maven log are harmless when BUILD SUCCESS is printed."). Log lines at L155-156 show the systemPath ${tools.jar} ERROR next to BUILD SUCCESS; I found no tools.jar reference in the judo-ng XML I searched, so the source is a dependency pom (not located). Cosmetic noise.
- **Why:** Generated pom uses a relative system path for tools.jar. Noise, not a failure.
- **Validation:** partly; kind platform-bug; catalog missing. Evidence: `session:L156`, `session:L155`. Merged: c03-08

#### G140 `c01-33` R0 S01, S06: judo.sh stop did not stop the foreground judo.sh start process or Karaf. The builder killed the leftover processes by PID.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo.sh stop (Karaf process handling)`. local-development.md "Stopping Services" only says run ./judo.sh stop and does not say it leaves a foreground start/Karaf JVM running. Add one line: if start was run under nohup, kill the Karaf PID after stop (verify against judo.sh source).
- **Why:** Start was run under nohup and stop only tears down the Docker services and not the Karaf child. **Workaround:** pkill on judo.sh start and console.out, then restart.
- **Validation:** partly; kind cli-tool; catalog missing. Evidence: `session:L494`, `session:L495`, `session:L497`, `session:L498`

#### G141 `c02-04` R1 S09: Setting customImplementation=true on the ProductInfo_Table price element makes the generated table component use useTrackService without importing it. The frontend build fails with TS2304 'Cannot find

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ui-react-template table/index.tsx.hbs (useTrackService import)` (also: modify-catalog: catalog/agent-docs/frontend/hooks/table-hooks.md: do not set customImplementation=true on table columns; use ColumnCustomizerHook.). Session L962-970 shows TS2304 after customImplementation=true on a table column. In judo-ng the template line 190 of containers/components/table/index.tsx.hbs calls useTrackService; the import condition for that file was not checked, so the bug is plausible but not pinned.
- **Why:** Generator bug in the table component template for custom-implementation columns. The build recovery section (delete generated src folders and rebuild) did not fix it. **Workaround:** Set customImplementation=false on the table price element, regenerated, and built. The price column is handled by the column customizer hook instead.
- **Validation:** partly; kind platform-bug; catalog missing. Evidence: `session:L962`, `session:L968`, `session:L969`, `session:L970`

#### G142 `c02-09` R1 S09: The generated table component builds the column customizer lookup filter with a missing closing parenthesis after (column=price), so the OSGi filter is invalid.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng template__judo-ui-react-template/.../containers/components/table/index.tsx.hbs:190` (also: modify-catalog: catalog/agent-docs/frontend/hooks/table-hooks.md: warn that ColumnCustomizerHook lookup is broken in the generated table template (version-specific, verify).). The filter string "(&(${OBJECTCLASS}=...)(component=...)(column=name)" opens "(&" and never closes it, so the OSGi filter is invalid. Real defect, reproducible by reading the template.
- **Why:** Generator bug in the table component template for customizer lookups; found when customImplementation was enabled on the table column. **Workaround:** Not patched (generated file). Table column left generated; logged in GAPS R1-1.
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L973`, `session:L995`

#### G143 `c02-40` R3 S11: Field reorder did not reach the generated form and view. After move, relocate and row changes, the saved model showed Name, Price, Description, but the generated TSX and the generated UI model still l

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng runtime__judo-tatami-client/judo-tatami-esm2ui/.../operations/ui/visualElement.eol:5` (also: modify-catalog: catalog/agent-docs/frontend/esm-to-ui-mappings/README.md: "Generated field order follows widget rule order, not model order; number fields appear before text fields; do not rely on move/relocate."). Field order bug is the same root cause as c02-46: __pos.put(self, __pos.get(component) ?: 0) at visualElement.eol:5. Model order is ignored for generated forms and views. Merged with the other field order claims.
- **Why:** Root cause given by the orchestrator in Round 4: the esm2ui ETL emits widgets per type in rule order, so number widgets come before text widgets; model order and row are ignored (see c02-55). **Workaround:** Pending; the builder tried delete and re-fill and update --add feature, see c02-49.
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L1407`, `session:L1533`, `session:L1534`, `session:L1539`. Merged: c02-43, c02-46, c03-64, c05-52, g-R7-10, g-R11-3

#### G144 `c03-13` R6 F02: ./judo.sh schema-upgrade failed with Non-readable POM for the schema directory; with -o schema_dir=application it ran for 900 seconds and timed out.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo.sh schema-upgrade default schema_dir`. build-process.md lists schema-upgrade as persistent PostgreSQL only; schema-evolution.md says it is not needed for dev DBs. Failure is expected when no persistent DB; the 900 s hang is unexplained. Add the schema_dir option and precondition to build-process.md; ticket the Non-readable POM default only if reproduced.
- **Why:** The schema-upgrade step expects a schema module directory and a running persistent DB; the default layout did not match this project and the run hung. **Workaround:** Killed the run and reset the database volumes instead of upgrading.
- **Validation:** partly; kind cli-tool; catalog partly-covered. Evidence: `session:L1843`, `session:L1844`, `session:L1855`, `session:L1859`

#### G145 `c04-02` R8 F09: The generated layout stores the mini drawer state in browser storage (webshop-config) and recomputes it only when the window crosses a size tier, so a browser that was once small opens collapsed on a 

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng frontend generator (layout/Drawer)`. Catalog has nothing on drawer state; the behaviour (drawer state persisted in browser storage under webshop-config, recomputed only on tier change) is reported from GAPS R8-1 and not re-run. Ticket for the generator; optionally a note in ui-hooks.md.
- **Why:** Behaviour not described in the catalog; the builder searched the kb twice and found nothing on drawer state. **Workaround:** Render-nothing DrawerExpander registered as the documented AppBar extra component opens the drawer at lg and xl widths on load and on size change, in both actors.
- **Validation:** partly; kind catalog-gap; catalog missing. Evidence: `session:L2582`, `session:L2585`, `session:L2588`, `session:L2614`

#### G146 `c04-13` R8 F21: An operation with an output and an input dialog makes the generated dialog file import the output type twice (import type { OrderInfo, OrderInfo, ... }); Biome rejects it as a parse error and the fron

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ui-react-template dialog template (operation input+output imports)` (also: modify-catalog: catalog/best-practices/model/operation-return-type-navigation.md: warn that an operation with both an input and an output of the same TO breaks the frontend build (verify version).). Session L2475 shows `import type { OrderInfo, OrderInfo, OrderInfoStored, OrderInfoStored }` and Biome parse error "second declaration of OrderInfo". Reproducible build error; template file not pinned in judo-ng.
- **Why:** Generator bug. Tried mapped output, output with a relation to the same type, and output with one primitive: all failed the same way. The catalog's operation-return-type-navigation pattern (return the destination type from the operation output) is therefore blocked. **Workaround:** Made checkout a void operation; the new order is opened through the generated dialog actions hook (see c04-14).
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L2471`, `session:L2475`, `session:L2479`, `session:L2487`

#### G147 `c04-15` R8 F20: A business fault shows in the generated fault dialog as the error code letter by letter (0: N, 1: O, 2: T ...), not as a readable message.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo generated error-handling.ts (useErrorHandler 422)` (also: modify-catalog: catalog/agent-docs/backend/error-handling-guide.md and frontend/error-handling.md: show the actual 422 body (first key) and recommend the error handler interceptor.). Catalog frontend/error-handling.md already states the handler uses Object.keys(data)[0]; the symptom (letters) fits a body whose first key is `code`. So catalog is incomplete on the body shape, not simply wrong. Session L2372-2373.
- **Why:** The generated 422 handler opens the dialog from the first key of the response body; the body starts with 'code', not the fault. The catalog describes the body with the fault key first, which is wrong for this version. **Workaround:** Error handler interceptor shows the fault's message as a snackbar (documented route in the frontend error-handling page).
- **Validation:** partly; kind platform-bug; catalog wrong. Evidence: `session:L2372`, `session:L2373`, `session:L2512`, `session:L2558`

#### G148 `c05-10` R9 F29: After a successful removeProduct, the generated page says the operation succeeded, refreshes the deleted product (404 BOUND_OPERATION_INSTANCE_NOT_FOUND) and never opens the output dialog.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ui-react-template page actions after delete operation` (also: modify-catalog: catalog/agent-docs/frontend/hooks/action-hooks.md: for instance operations that delete the instance, add a post-action hook that navigates back.). Generated flow refreshes the deleted instance (BOUND_OPERATION_INSTANCE_NOT_FOUND). Plausible and documented hook workaround exists; template not pinned in judo-ng.
- **Why:** Generated post-operation flow refreshes the bound instance after an operation that deletes it. **Workaround:** Page actions hook registerProductRemovedHook.ts (documented postRemoveProductForProductInfoAction): shows the returned message and goes back to the product list.
- **Validation:** partly; kind platform-bug; catalog missing. Evidence: `session:L2954`, `session:L2962`, `session:L2964`, `session:L2969`

#### G149 `c06-02` R11 F41: Transform failed on a derived attribute that filters over a two-way collection (Product.wishedBy): 'Feature wishedBy not found', then an ObjectFilterExpression cannot be cast to CollectionExpression e

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-meta-expression-asm (asm2expression)` (also: modify-catalog: catalog/best-practices/model/bidirectional-relation.md: filtering the reverse side of a two-way relation needs upper cardinality set to * before using it in a derived filter (verify).). Session L3376-3381 reproduces two errors: "Feature wishedBy not found" and ObjectFilterExpression cannot be cast to CollectionExpression, resolved only by changing cardinality to 0..*. Exact source cast not located in judo-ng; first error is probably a transient state during rename.
- **Why:** Not explained in the chunk; occurred when a derived flag filtered the reverse side of a many-to-many two-way relation. **Workaround:** Set wishedBy cardinality to 0..* and re-created the derived flag with a different expression; some derived flags were removed and rebuilt.
- **Validation:** partly; kind platform-bug; catalog missing. Evidence: `session:L3376`, `session:L3378`, `session:L3380`, `session:L3381`

#### G150 `c06-07` R11 F44: After a table operation was added to ProductInfo_Table, the build failed with XMI ID collisions on admin tabular reference actions and a UI generator NullPointerException (ActionDefinition.getIsExport

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng template__judo-ui-react-template pages/index.tsx.hbs (ActionDefinition.isExportAction null)` (also: agent-docs/model/esm_metamodel/operation.md). Session error L3434-3452 and GAPS R11-7(c) reproduce it: a static table operation with input on a TO that is also shown on a relation table page crashes the UI generator. Catalog should say: put such an operation on its own TO and page.
- **Why:** Not explained in the chunk; the NPE was in a generated page of a different entity than the one changed. **Workaround:** Deleted the ProductInfo table operation (delete --cascade) and created the import operation on a new ImportedProductInfo transfer object with a Products table operation.
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L3434`, `session:L3438`, `session:L3442`, `session:L3449`. Merged: c08-07

#### G151 `c06-23` R11 F41, F42, F43, F44, F46, F47: Database not migrated for the new tables and columns; ./judo.sh schema-upgrade fails with a Maven ProjectBuildingException, so the containers and volumes were wiped and all earlier data is gone.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo.sh line 991 (SCHEMA_DIR defaults to MODEL_DIR)` (also: agent-docs/deployment/schema-evolution.md). Reproducible: judo.sh:991 defaults SCHEMA_DIR to the project root, but schema and model sit under application/ (GAPS R12-1). schema-evolution.md names schema-upgrade but never schema_dir (no catalog hit). Add: run schema_dir=application ./judo.sh schema-upgrade; wipe is not needed.
- **Why:** Known platform issue (R6-1, R10-3); the schema-evolution route in the kb does not work on this project. **Workaround:** Wiped containers and volumes, restarted, reran seed-dev-user.sh.
- **Validation:** confirmed; kind platform-bug; catalog partly-covered. Evidence: `session:L3708`, `session:L3710`, `session:L3711`, `session:L3712`

#### G152 `g-R11-7` R11 F44: A static operation with an input as table action of a table shared with a relation page makes the UI generator fail (ActionDefinition.getIsExportAction() is null); plus traps: optional inputs arrive a

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng UI generator (pages/index.tsx.hbs)`. Session L3438 shows the NullPointerException on getIsExportAction; grep of catalog finds no mention. Not checked in judo-ng source. Add a verify note to bulk-csv-import-export.md: do not place a static operation on a table that is also a relation table.
- **Why:** Generator NPE for table actions on tables reused in a relation table page. **Workaround:** Import on its own page; export on a table with no conflict.
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L3438`, `gaps:R11-7`

#### G153 `c07-08` R12 F48: Sorting by a derived aggregate gives a generated-SQL error (missing FROM-clause entry), and a nested filter or filter plus sort over the same type gives 'table name _iterator_N specified more than onc

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng JQL to SQL generator (asm2query/rdbms)` (also: best-practices/model/aggregated-stored-field.md). Reproducible session errors (GAPS R12-10): sort by derived aggregate gives missing FROM entry; nested same-type filter gives _iterator_N twice. No judo-ng line checked. aggregated-stored-field.md gives the stored-aggregate route but not the two failure modes; add them.
- **Why:** Platform JQL-to-SQL generator bug for these expression shapes. **Workaround:** Made soldUnits a stored aggregate, maintained by checkout, cancel and return approval, and sorted on it with one selector.
- **Validation:** confirmed; kind platform-bug; catalog partly-covered. Evidence: `session:L4361`, `session:L4392`, `session:L4393`, `session:L4395`

#### G154 `c07-16` R12 F41: The table column customizer hook key is imported by the generated tables but nothing consumes it, so a hook registered for a column never applies. The catalog's Custom Columns section presents it as w

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/src/containers/components/table/index.tsx.hbs:190` (also: agent-docs/frontend/hooks/table-hooks.md). The hook IS consumed (line 208), but the OSGi filter on line 190 lacks a closing parenthesis, so it never matches. The miner stated the wrong cause. table-hooks.md "Custom Columns" presents the hook as working: mark it as not working in current generator or point to the custom component route.
- **Why:** Grep over the generated frontend found no consumer of TABLE_COLUMN_CUSTOMIZER_HOOK_INTERFACE_KEY; the platform does not wire it. **Workaround:** Not used; wishlist moved to a custom component.
- **Validation:** partly; kind platform-bug; catalog wrong. Evidence: `session:L3820`, `session:L3821`, `session:L4043`, `session:L4044`

#### G155 `c07-17` R12 F41: Setting DataColumn.customImplementation=true makes the generated table use useTrackService without importing it, so pnpm build fails with TS2304 in every such table. The builder also reports that Tran

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/src/containers/components/table/index.tsx.hbs:94 vs :190` (also: agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md). useTrackService is imported at :94 only inside the useTableRowHighlighting block, but :190 uses it for every customizable column, giving TS2304. TransferObjectTable.customImplementation being a no-op is only from the session. Add a warning in tables-navigation.md: DataColumn.customImplementation breaks the build.
- **Why:** Generator emits a call to a hook it does not import; the table-level flag has no effect in the generated code. **Workaround:** Reverted customImplementation on the columns, set it only on the table, then used a custom view page.
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L4063`, `session:L4068`, `session:L4070`, `session:L4073`

#### G156 `c07-32` R12 F53: The generated application/integration-test/pom.xml declares hu.blackbelt.osgi.i18n:i18n-api with an empty version element, so Maven cannot read the project ('dependencies.dependency.version ... is mis

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng template__judo-esm-fullstack-project-template integration-test/pom.xml.hbs:226 ({{ osgiI18nApiVersion }})` (also: agent-docs/integration-testing/getting-started.md). The template uses osgiI18nApiVersion; no other file in the judo-ng clones defines it, so the version renders empty (session error L4179-4187 matches). getting-started.md does not warn. Add: copy the generated module and fill in the i18n-api version.
- **Why:** Template or generator bug in the integration-test pom fragment; the empty element is not filled from a property. **Workaround:** Hand-written order-tests module with the version filled in.
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L4179`, `session:L4184`, `session:L4185`, `session:L4186`

#### G157 `c07-38` R12 F54: The generated playwright.config.ts sets retries: 4 unconditionally (the template comment says retry on CI only). The catalog's troubleshooting page documents the fix as retries: process.env.CI ? 4 : 0

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng template__judo-ui-e2e-template playwright.config.ts.hbs:15`. Template line 15 has retries: 4 unconditionally; the judo-ng AGENTS.md says so too. troubleshooting.md:320 already documents the fix, so no catalog change.
- **Why:** Generator template ignores the CI condition; catalog already describes the fix. **Workaround:** Separate playwright.ci.config.ts and playwright.local.config.ts (not generated).
- **Validation:** confirmed; kind platform-bug; catalog covered. Evidence: `session:L4128`, `session:L4131`, `session:L4132`

#### G158 `c07-49` R12 : Frontend build logs show 'XMI ID COLLISION DETECTED' errors for the admin and customer models, but the build still succeeded. The builder did not investigate them.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng runtime__judo-tatami (zeta XMI ids)` (also: agent-docs/deployment/build-process.md). Same log lines in several builds (L3985, L4066); judo-tatami archived a fix for zeta ESM-to-PSM ID collisions on 2026-03-20 but the admin tabular reference actions still collide. Harmless to the build, so add a one-line note to build-process.md.
- **Why:** Generator reassigns the same XMI ids to Action objects; cause not checked.
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L3985`, `session:L4066`. Merged: c09-15, c10-17

#### G159 `c07-13` R12 F45, F49: The CLI rejects hiddenBy and enabledBy on a TableOperation ('not defined for input object type TableOperationUpdateInput'), although tables-navigation.md lists both properties for ui:TableOperation.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-cli update: TableOperationUpdateInput (hiddenBy, enabledBy)`. Session L3959-3965 shows the CLI rejects hiddenBy and enabledBy on TableOperation, while tables-navigation.md lines 121-122 list them. Either CLI input type lacks them or doc is wrong; add a verify note in tables-navigation.md and ticket the CLI. CLI source not present under judo-ng-read.
- **Why:** The CLI input type does not match the documented property list. **Workaround:** Per-row hiding moved to a separate page (see decision on F49).
- **Validation:** confirmed; kind cli-tool; catalog wrong. Evidence: `session:L3959`, `session:L3964`, `session:L3968`, `session:L3969`

#### G160 `c08-06` R13 F55: Generated customer frontend fails Biome with a duplicate import: ShopMessage and ShopMessageStored are imported twice when an operation returns a mapped type.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng template__judo-ui-react-template containers/dialog.tsx.hbs:39-52` (also: best-practices/model/operation-output-with-behaviors.md). Reproducible in the session (L4690-4691) and GAPS R8-5: the dialog imports the output type twice and Biome rejects it. Catalog operation-output pages have no warning. Add: an operation with output plus input dialog breaks the frontend build, use a void operation and a post-operation hook.
- **Why:** Generator emits duplicate imports for a mapped operation output (already recorded as GAPS R8-5, referenced in the checkout hook comment). **Workaround:** Builder removed the output parameter from the invite operations (-u output), so the generator stopped emitting the import.
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L4550`, `session:L4690`, `session:L4691`. Merged: c09-14

#### G161 `c08-08` R13 F55, F56, F57: Frontend Maven step fails at pnpm install with ERR_PNPM_IGNORED_BUILDS (core-js-pure, esbuild), so the format step fails and the build stops; the same message is in an earlier build log.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng template__judo-ui-react-template (pnpm build-script approval)` (also: agent-docs/deployment/build-process.md). Session shows ERR_PNPM_IGNORED_BUILDS for core-js-pure and esbuild (L4684-4689); no judo-ng setting for allowed builds found. Add to build-process.md: if pnpm install fails with this, run biome directly or approve the builds.
- **Why:** pnpm blocks dependency build scripts that are not approved; the generated build does not approve them. **Workaround:** Builder ran npx biome directly instead of pnpm run format.
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L4684`, `session:L4685`, `session:L4686`, `session:L4689`

#### G162 `c08-18` R13 F55, F56, F58: After the build, app start logged NoClassDefFoundError for hu/blackbelt/epsilon/runtime/execution/contexts/EolExecutionContext and Could not find compatible schema model; the same error appears in the

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [x] ticket [ ] tool [ ] drop
- **Proposed:** platform-ticket → `judo-ng tools__epsilon-runtime / karaf features (EolExecutionContext)` (also: agent-docs/backend/debugging-and-monitoring-guide.md). Start logs show the NoClassDefFoundError three times (L4794-4796) while the app answers HTTP 200; the "no compatible schema model" line is unexplained. Treat as startup noise, note in debugging guide.
- **Why:** Not resolved in this chunk. Looks like a platform runtime or classpath issue, not a model error. **Workaround:** Builder kept going; the app answered HTTP 200 on the admin URL.
- **Validation:** confirmed; kind platform-bug; catalog missing. Evidence: `session:L4794`, `session:L4795`, `session:L4796`

## C. Tool / CLI / skill fixes

#### G163 `c01-22` R0 S05: Browser automation clicks and fills often did not reach the page. The builder then blamed slow app response and used many fixed waits and DOM eval clicks to move around.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [ ] ticket [x] tool [ ] drop
- **Proposed:** tool-fix → `agent-browser click and fill reliability`. Several independent claims (c02-20 and the Playwright fallback) show the browser tool delivered no click events; tool problem, not catalog. Catalog e2e-testing pages do not need a change.
- **Why:** Agent-browser tool problem. Refs went stale on re-render, text selectors failed, and clicks sent no events in several cases. Not an app latency issue. **Workaround:** Fixed waits (10 to 40 s), DOM eval clicks, direct location.hash changes, REST curl for data checks.
- **Validation:** confirmed; kind agent-tool; catalog n/a. Evidence: `session:L232`, `session:L252`, `session:L455`, `session:L815`. Merged: c01-23, c02-10, c02-11, c02-20, c08-28, g-L15

#### G164 `c01-25` R0 S01, S05: kb_get returned 'not found' for paths that kb_search had just listed, so the builder could not read those docs.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [ ] ticket [x] tool [ ] drop
- **Proposed:** tool-fix → `kb_get path resolution`. kb_get not-found right after kb_search is repeated in 8 claims, but the file paths exist; likely the builder passed catalog/ prefixed or guessed section names, or the index was refreshing. Fix: kb_get should accept catalog/ prefix and list valid sections on a miss.
- **Why:** Path resolution in the kb tool fails for some listed sections; index refresh was still running at the time. **Workaround:** Read search snippets, or grepped the catalog directly.
- **Validation:** partly; kind cli-tool; catalog n/a. Evidence: `session:L725`, `session:L729`, `session:L751`, `session:L752`. Merged: c02-54, c03-24, c03-35, c06-30, c07-50, c09-22, c09-23

#### G165 `c01-26` R0 S01: The kb read guard fired about 25 times with 'consecutive searches without consulting the knowledge base' while the builder read catalog files with bash and read.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [ ] ticket [x] tool [ ] drop
- **Proposed:** tool-fix → `kb read-discipline guard`. Guard text is visible in the session dump (e.g. L3959, "Repeated source searching, still no kb consult") firing on bash/source reads of the catalog. Guard should not count reads of catalog files or kb-driven reads.
- **Why:** Guard counts source reads as searches. It nagged on every bash call that touched the catalog. **Workaround:** Ignored; some turns then used kb_search.
- **Validation:** confirmed; kind agent-tool; catalog n/a. Evidence: `session:L31`, `session:L76`, `session:L416`, `session:L428`. Merged: c02-07

#### G166 `c01-27` R0 S01: Context-mode replaced long bash output with a search summary, so Maven and log output could not be read directly. The builder had to write output to files and read them.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [ ] ticket [x] tool [ ] drop
- **Proposed:** tool-fix → `context-mode bash output handling`. The wrapper replaced long output with a "searches the whole output" stub, visible in this validation too. Raise the threshold or let the caller opt out for build/log output.
- **Why:** Output summarising in ctx_search hid the lines the builder needed for the first Maven run. **Workaround:** Redirected output to /tmp/wsout files and read them with read.
- **Validation:** confirmed; kind agent-tool; catalog n/a. Evidence: `session:L45`, `session:L46`, `session:L48`, `session:L851`. Merged: c05-23, c06-29, c09-08

#### G167 `c01-32` R0 S01: Paths under /tmp failed in the read tool (ENOENT) because the path resolves to /private/tmp on macOS.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [ ] ticket [x] tool [ ] drop
- **Proposed:** tool-fix → `read tool path normalisation`. On macOS /tmp is /private/tmp; the read tool failed on /tmp paths (reproduced here: /tmp/ev.txt not found, /private/tmp/ev.txt works). Tool should resolve the symlink.
- **Why:** Tool path handling for the macOS /tmp symlink. **Workaround:** Read the /private/tmp path or used bash cat.
- **Validation:** confirmed; kind agent-tool; catalog n/a. Evidence: `session:L57`, `session:L58`, `session:L116`

#### G168 `c03-01` R6 F01, F02: Builder ran many repeated source searches (ls/grep/sed on catalog and CLI output) without calling kb_search; the guard warned seven times.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [ ] ticket [x] tool [ ] drop
- **Proposed:** tool-fix → `builder prompt + kb guard (enforce kb_search before grep)`. Standing kb-first rule existed and was ignored; guard warnings did not change behaviour. Fix is enforcement (block grep/read of catalog until kb_search has run), not a new catalog entry.
- **Why:** Builder defaulted to reading CLI output and source instead of kb-first discipline required by the standing rules. **Workaround:** Builder continued; later kb_search calls were made.
- **Validation:** confirmed; kind builder-mistake; catalog n/a. Evidence: `session:L1761`, `session:L1769`, `session:L1775`, `session:L1781`. Merged: c01-12, c03-54, c04-18, c05-03, c05-59, c06-27, c07-51, c08-01

#### G169 `c03-52` R7 F14: ctx_execute ran with /bin/sh and failed on bash process substitution syntax.

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [ ] ticket [x] tool [ ] drop
- **Proposed:** tool-fix → `ctx_execute shell`. ctx_execute shell runs /bin/sh; bash process substitution fails. Document or run bash.
- **Why:** The shell used for the sandbox does not support process substitution. **Workaround:** Re-ran the command without process substitution.
- **Validation:** confirmed; kind agent-tool; catalog n/a. Evidence: `session:L2115`, `session:L2116`

#### G170 `c06-03` R11 F41, F42, F43, F46, F47: validate reported 46 'Named element X is not unique in its container' errors after the model edit script ran twice on top of partly applied changes; discard refused without --force and the validate ou

- [ ] **Issue**  Action: [ ] add [ ] modify [ ] one-off [ ] ticket [x] tool [ ] drop
- **Proposed:** tool-fix → `judo-cli discard and validate output`. Catalog documents discard --force and re-run duplication (judo-cli.md l.119). The error text for refused discard and the EVL path dump are not actionable; improve CLI messages.
- **Why:** Non-idempotent create script re-run after a failed run without discarding; CLI discard requires --force and the error text is not actionable. **Workaround:** discard --force, then re-ran the script from a clean model.
- **Validation:** confirmed; kind builder-mistake; catalog covered. Evidence: `session:L3372`, `session:L3373`, `session:L3374`, `session:L3376`. Merged: c05-18

## D. One-off (no catalog change proposed)

| # | Issue | Action | ID | Round | What | Note |
|---|---|---|---|---|---|---|
| G171 | [ ] | one-off / [ ] escalate | `c01-06` | R0 | Guessed the ESM type name Namespace in a query and got an error. | confirmed; Guessed type name; trivial. A skill rule "list metamodel types first" would be marginal. |
| G172 | [ ] | one-off / [ ] escalate | `c01-08` | R0 | ActorType create warned that realm does not apply, because the actor was effectively anonymous. | confirmed; accesspoint.md already says realm applies only when the actor is not anonymous; builder warning was correct behaviour. |
| G173 | [ ] | one-off / [ ] escalate | `c01-24` | R0 | Said the app was slow to respond (15 to 40 s per click). The orchestrator later showed the server answers in milliseconds. | confirmed; Misdiagnosis from flaky browser clicks, later corrected by orchestrator; no catalog topic. |
| G174 | [ ] | one-off / [ ] escalate | `c01-31` | R0 | Shell commands used on macOS: GNU 'timeout' is not installed, and a find / scan timed out after 60 s. | confirmed; macOS shell habits (GNU timeout, whole-disk find). A one-line builder prompt note about the host OS would prevent it; repeated in c02-23, c09-01, c10-20, c05-22. |
| G175 | [ ] | one-off / [ ] escalate | `c01-41` | R0 | Clicked Back on a view page opened directly by URL. Back did nothing, because the breadcrumb stack was empty. | confirmed; breadcrumb-navigation-context.md covers in-app-only breadcrumb stack; expectation error. |
| G176 | [ ] | one-off / [ ] escalate | `c01-01` | R0 | judo.sh generate-root failed with a Maven daemon connect timeout because the mvnd registry file was corrupt. | confirmed; Session L66-69 shows the mvnd registry.bin error; it is a corrupt local file, not a platform defect. At most one troubleshooting line (kill mvnd, delete ~/.m2/mvnd/registry/*/registry.bin) in catalog/ |
| G177 | [ ] | one-off / [ ] escalate | `c01-35` | R0 | Karaf log after a restart showed NoClassDefFoundError for EolExecutionContext in the RDBMS OSGi bundle. | unverifiable; One NoClassDefFoundError line at L621 (EolExecutionContext not found by rdbms bundle) at a restart; no reproduction, no recurrence, and the app started. Possibly an OSGi start-order race. Not enough f |
| G178 | [ ] | one-off / [ ] escalate | `c01-28` | R0 | kb_search results were fragmented and marked stale while the index was still refreshing. | partly; Transient index refresh at session start; no lasting fault shown. A kb_search status line "index refreshing" would help but is minor. |
| G179 | [ ] | one-off / [ ] escalate | `c01-29` | R0 | Builder read the catalog through bash grep, sed and read for most of the first hour, instead of kb_search and kb_get. This is why the kb call share was low. | confirmed; Orchestrator log R0 confirms 14 of ~460 calls were kb calls and no kb-first rule was in the first prompt; fixed by user steering. Process fix: put the kb-first rule in the build prompt template. |
| G180 | [ ] | one-off / [ ] escalate | `c01-30` | R0 | Builder ran validate, curl, log reads and browser checks between build steps. The user then said to check only at the end and to use kb for every question. | confirmed; Log R0 confirms the check-as-you-go habit and the user rule to check only at the end. Run-specific prompt issue, nothing for the catalog. |
| G181 | [ ] | one-off / [ ] escalate | `c02-12` | R1 | Builder used fixed waits (wait 4000, 5000, 6000 ms) while checking in the browser, against the round rule to wait for an element or URL. | confirmed; Builder ignored the round rule (no fixed waits); process slip, not a catalog topic. |
| G182 | [ ] | one-off / [ ] escalate | `c02-15` | R1 | Login attempts failed because the builder typed the password into the wrong field and used the wrong input commands (quoted text, keyboard inserttext mixed with type). The builder  | confirmed; Browser typing mix-up. |
| G183 | [ ] | one-off / [ ] escalate | `c02-16` | R1 | Builder used eval to read document.activeElement while checking focus, which is outside the check rules. It said so in its notes. | confirmed; Read-only eval use; minor rule bend declared by the builder. |
| G184 | [ ] | one-off / [ ] escalate | `c02-19` | R1 | Round 1 screenshots at 375, 768 and 1440 px all failed because checks/S04 did not exist. The builder then deleted the screenshots and wrote a README saying the round's checks were  | confirmed; Builder did not mkdir output folders; the mission script could create them (minor skill tweak) but one-off. |
| G185 | [ ] | one-off / [ ] escalate | `c02-08` | R1 | Builder used ask_user to ask permission for the application-customizer.tsx exception. The orchestrator corrected it: never use ask_user, write everything to the common channel. | confirmed; Run rule: questions go to the common channel, not ask_user. Log R1 lists the customizer exception as accepted. Prompt-template item only. |
| G186 | [ ] | one-off / [ ] escalate | `c02-27` | R2 | Edit-form fill on the price input failed with 'element is not editable'. The cause was the builder's own PriceField, which set readOnly = !editMode while the view page starts with  | confirmed; Builder own PriceField readOnly logic; model-screen-layout.md does not apply. |
| G187 | [ ] | one-off / [ ] escalate | `c02-29` | R2 | Round 2 report says there were several test runs and fixes in the end phase, although the round rule was to run the tests once at the end. | confirmed; Round rule (one test run at end) not followed. |
| G188 | [ ] | one-off / [ ] escalate | `c02-30` | R2 | Orchestrator found the product descriptions are placeholder text 'a / b'. Real descriptions of 2 to 3 lines are required for the 3 products, entered through the UI in a test, not t | confirmed; Seed data quality; project instruction, not platform. |
| G189 | [ ] | one-off / [ ] escalate | `c02-32` | R2 | Builder removed .git/index.lock by hand after a git add failed, after checking pgrep. A lock file can belong to a running git process. | confirmed; Removed a stale git lock after pgrep check; acceptable but risky; no catalog topic. |
| G190 | [ ] | one-off / [ ] escalate | `c02-33` | R2 | Session stopped just before the Round 2 report; the orchestrator resumed it and asked for the report again. | confirmed; Log R2 notes the session was resumed once after a user stop. No platform or catalog content. |
| G191 | [ ] | one-off / [ ] escalate | `c02-42` | R3 | Frontend build failed once (pnpm run build error) after the fields were deleted and the priceLabel removed. The next build passed after a regenerate, with no change in the cause sh | unverifiable; One failed build then a pass after regenerate with no cause visible; typical stale generated state. Nothing actionable. |
| G192 | [ ] | one-off / [ ] escalate | `c02-53` | R5 | No documented empty-data route for the product grid, so the empty-state Playwright check could not be run as a real user action. The test is skipped and logged. | partly; Needs test data control, which is project specific (own test realm/DB). Low value as catalog text; at most one line: for empty-state checks use a fresh user or a filter that matches nothing. |
| G193 | [ ] | one-off / [ ] escalate | `c02-50` | R5 | TypeScript build error in the new CatalogHome.tsx: a helper typed (text?: string) was called with a string or null value, failing TS2345 and the build once. | confirmed; Own TypeScript typing slip. |
| G194 | [ ] | one-off / [ ] escalate | `c03-09` | R6 | Builder ran a bare tsc command that is not the project compiler; the tool printed a wrong-command banner. | confirmed; Bare tsc instead of the project compiler. |
| G195 | [ ] | one-off / [ ] escalate | `c03-34` | R6 | Builder built the category view with a Products button that opens a list instead of an embedded table on the view, which FUNCTIONS.md asks for. | confirmed; ui-authoring-guide and model-development list representationComponent table\|button; builder picked button against FUNCTIONS.md. Catalog gives the options; selection error. |
| G196 | [ ] | one-off / [ ] escalate | `c03-61` | R7 | Builder added src/custom/application-customizer.tsx to .generator-ignore in the admin and customer frontend modules, against the standing rule that .generator-ignore entries are ne | confirmed; frontend/README.md already says the four generator-written src/custom files need a .generator-ignore entry if hand-edited. Builder deviated from the project rule, but the catalog supports it; project  |
| G197 | [ ] | one-off / [ ] escalate | `c03-79` | R7 | Whole Playwright suite was not run as one command: the admin and customer modules ran separately, and the last customer test edit was not followed by an admin re-run. | confirmed; Log R13 records the same test-isolation lesson: new rule is per-round spec plus @smoke, full suites serial at the end. Builder habit after the module split. |
| G198 | [ ] | one-off / [ ] escalate | `c04-20` | R8 | A reload added to the screenshot helper (to lay out the drawer) closed open dialogs, so six admin tests failed until the reload was removed. | confirmed; Own test helper bug. |
| G199 | [ ] | one-off / [ ] escalate | `c04-01` | R8 | The customer drawer looked squashed in the F09 1440 screenshot: labels cut to 'Pr...' and 'My...' and a tiny logo. | partly; Layout settle problem for a 1440 screenshot of the drawer in this app; the settleLayout helper is project code. |
| G200 | [ ] | one-off / [ ] escalate | `c04-10` | R8 | Running pnpm format by hand failed because the lockfile entries were newer than the minimumReleaseAge policy. | partly; pnpm minimumReleaseAge vs lockfile is a local pnpm policy conflict (L2468-2471), not JUDO behaviour. One-off. |
| G201 | [ ] | one-off / [ ] escalate | `c05-11` | R9 | F29 test created a product with SKU T-514769, which breaks the model pattern for SKU, so the create failed and the test failed. | confirmed; Test data broke the model's own SKU pattern (GAPS R9-15); builder error, not a catalog gap. |
| G202 | [ ] | one-off / [ ] escalate | `c05-14` | R9 | no-admin-data customer test failed: it read response bodies asynchronously and asserted before they were collected (expected 2, got 1). | confirmed; Plain Playwright timing: asserting before async response bodies were collected. expect.poll is general Playwright knowledge. |
| G203 | [ ] | one-off / [ ] escalate | `c05-40` | R10 | Order history on the admin view was not sorted by time (Shipped to Delivered listed before Order placed). | confirmed; tables-navigation.md documents ui:DataColumn defaultSort; builder omitted it. |
| G204 | [ ] | one-off / [ ] escalate | `c05-55` | R10 | F29 test failed with ReferenceError: reactivate is not defined after a cleanup block was pasted into the wrong test. | confirmed; Test paste slip. |
| G205 | [ ] | one-off / [ ] escalate | `c05-58` | R10 | Full customer Playwright suite was not run again after the final test fix; the report says so. The standing rule asks for the whole suite once at the end. | confirmed; Builder skipped final full-suite run; process. |
| G206 | [ ] | one-off / [ ] escalate | `c05-51` | R10 | Admin build log shows XMI ID COLLISION DETECTED errors (ten lines) for the e2e and frontend model; the build still succeeds. | partly; XMI ID COLLISION lines at L3145-3147 with BUILD success. I found no such string in judo-ng java/etl, so the source was not located. Cosmetic. |
| G207 | [ ] | one-off / [ ] escalate | `c06-13` | R11 | Builder claimed a write made in a postCall interceptor on the notification refresh was not kept: the log said 'marked as read' but the database kept c_read = f. | unverifiable; Builder never isolated the cause of the dropped postCall write; read-tracking-postcall-interceptor.md describes the transaction rule correctly. No catalog statement to fix without a reproduction. |
| G208 | [ ] | one-off / [ ] escalate | `c06-22` | R11 | CSV import test used SKUs like IMP-A-<timestamp>, which fail the Product SKU pattern ^[A-Z]{2}-[0-9]{4}$; the import of the bad row caused a PATTERN_VALIDATION_FAILED error. | confirmed; Test data ignoring the model SKU pattern; same as c09-25. |
| G209 | [ ] | one-off / [ ] escalate | `c06-21` | R11 | Admin test for the unit dropdown flaked: Escape sometimes closes the whole dialog, so the later Back click timed out. | confirmed; Escape closing the whole dialog is a flaky UI interaction seen once; tolerated in the test. |
| G210 | [ ] | one-off / [ ] escalate | `c07-21` | R12 | The notifications bell used navigate, which pushes the current page into the breadcrumb, so the page showed 'Home / Products' instead of 'Home'. The sidebar already used clearNavig | confirmed; breadcrumb page and navigation-and-access.md document clearNavigate; builder chose navigate. |
| G211 | [ ] | one-off / [ ] escalate | `c07-25` | R12 | BusinessClock used the JVM zone (CET) while model Timestamp!now() uses the platform zone (UTC), so the return window was an hour off (a 0-day window stayed open). The catalog page  | confirmed; platform-behavior-reference.md l.98 states Timestamp!now() follows defaultZoneId (UTC) not the JVM zone; builder skipped it. |
| G212 | [ ] | one-off / [ ] escalate | `c07-35` | R12 | The new tests found the builder's own mistakes in ReturnService: an Optional passed to %f, an Optional in the history text, a getProductName call on the wrong object, and a guessed | confirmed; Guessed generated API names; testkit pages exist. Mixed own mistakes. |
| G213 | [ ] | one-off / [ ] escalate | `c08-02` | R13 | CompanyService and ApprovalService did not compile: getCompanyRole, getCompanyAdmin and getPoRequired return plain values, but the builder called orElse on them, then patched with  | confirmed; data-access-guide l.499 says required attributes give plain getters, optional ones Optional; builder assumed Optional everywhere. |
| G214 | [ ] | one-off / [ ] escalate | `c08-09` | R13 | Builder ran biome format and check with --write on the generated customer frontend source, which is generated code. | confirmed; Formatter run on generated frontend code, against the standing rule; frontend README checksum protection already warns. |
| G215 | [ ] | one-off / [ ] escalate | `c08-11` | R13 | discard --force threw away unsaved model edits from a fill run after an error, and the builder had to rebuild those edits. | confirmed; judo-cli.md says unsaved edits are lost on discard; builder should save before risky steps. Possibly a small line "save after each successful step". |
| G216 | [ ] | one-off / [ ] escalate | `c08-26` | R13 | A sed -i edit to level7.spec.ts replaced a line with the placeholder XX, causing a ReferenceError until fixed. | confirmed; Unsafe sed on a spec file. |
| G217 | [ ] | one-off / [ ] escalate | `c08-27` | R13 | Several bash commands ran in the same parallel batch as a read of their output, so the read ran first and returned ENOENT. | confirmed; Parallel tool-call ordering mistake by the builder. |
| G218 | [ ] | one-off / [ ] escalate | `c09-06` | R13 | The Round 13 report stated that screenshots at 375, 768 and 1440 px existed for F55 to F61, but the builder had viewed only two and had not run ls first. The user found only 2 file | confirmed; Report claimed screenshots without ls; process rule (verify before reporting). |
| G219 | [ ] | one-off / [ ] escalate | `c08-22` | R13 | Quote lines and company price rows open on their own nested page. Invite a member is enabled only after the company prices are stored with Update. | partly; Nested pages and Update before dependent actions are normal generated behaviour for this model; no catalog gap. |
| G220 | [ ] | one-off / [ ] escalate | `c08-25` | R13 | Final full customer suite run was aborted by the tool (Command aborted), so the round's full-suite result is not in this chunk. | unverifiable; Log R13 says the user stopped one over-long E2E run and the full suites at 3 workers failed from shared cart/stock; this abort is consistent with that. Cause not provable from the chunk. |
| G221 | [ ] | one-off / [ ] escalate | `c09-20` | R14 | The F62 test failed because the other seller's page showed 2 Publish or Unpublish buttons where the test expected 0. The builder changed the assertion to check that the form is emp | confirmed; Assertion weakened instead of finding cause; process. |
| G222 | [ ] | one-off / [ ] escalate | `c09-24` | R14 | Integration test imported TransactionHandling from the wrong package and failed to compile. The kb answer (Anti-Pattern 4) was found only after the failure. | confirmed; integration-testing/best-practices.md covers TransactionHandling (Anti-Pattern 4); custom-operations.md also uses it. Import package is not shown at point of use: could add the full import line. |
| G223 | [ ] | one-off / [ ] escalate | `c09-32` | R14 | Checkout from three sellers returned no order. Karaf log: 'There is illegal state, no records updated' from ProductDaoImpl.update, called in CheckoutCustomImplementation.accept (st | partly; platform-behavior-reference.md l.25 already explains "illegal state, no records updated" as a stale VERSION on update; cause in this build was never confirmed in the chunk, so the root is unproven. If |
| G224 | [ ] | one-off / [ ] escalate | `c09-26` | R14 | In the generated checkout dialog, typing the address sometimes sent stray digits to the loyalty points field, and the field's role made fill fail. | partly; Flaky typing into a debounced field; root cause not shown. No catalog change. |
| G225 | [ ] | one-off / [ ] escalate | `c09-35` | R14 | Each rebuild cycle (generate, build, start, health check) took about 3 to 5 minutes with fixed sleeps of 200 to 280 seconds; the builder used full rebuilds for every UI change. | confirmed; Log R15 shows the orchestrator sent the live-iteration docs next round. development-workflow.md has an HMR section (line 96), so the content exists; the builder was not told to use it. Put 'use dev se |
| G226 | [ ] | one-off / [ ] escalate | `c10-29` | R15 | The orchestrator asked for the admin Quote page 'Requested' and 'Order' fields to be read-only; no change for this is seen in the chunk and the final report does not mention it. | unverifiable; Not verifiable from the chunk; request dropped or finished later. The catalog gap for read-only date/number fields is covered by claim c09-09 in another batch. |
| G227 | [ ] | one-off / [ ] escalate | `c10-25` | R15 | Moving the customer menu into drop-down groups broke older specs that expected flat menu entries; clickMenu and menuCount helpers were added, and menu lookups needed retries becaus | confirmed; Menu regrouping in this app broke the app's own specs; MENU_GROUPS and clickMenu are project helpers. The generated menu structure is not a catalog gap. |
| G228 | [ ] | one-off / [ ] escalate | `c10-27` | R15 | The F70 refusal check expected 'You have 82 loyalty points', but the checkout was refused by the order-value rule (TOO_MANY_POINTS from CheckoutCustomImplementation.java) because t | confirmed; Test expectation did not match the app's own TOO_MANY_POINTS rule in CheckoutCustomImplementation; app specific. |
| G229 | [ ] | one-off / [ ] escalate | `c10-28` | R15 | The F70 expiry check looked for a toast 'loyalty points expired'; the admin operation shows the message in a dialog text box. | confirmed; Admin operation message is shown in a dialog, not a toast; builder guess about this app. |
| G230 | [ ] | one-off / [ ] escalate | `c10-30` | R15 | Standalone Playwright scripts with 'import playwright' failed (module not found, browser not installed); probes had to run through the project's 'npx playwright test' runner. | confirmed; Standalone Playwright scripts need the project install; use npx playwright test. Environment. |

## E. No action proposed (already covered, or not a gap)

| # | Issue | ID | What | Validator note |
|---|---|---|---|---|
| G231 | [ ] reopen | `c01-09` | managed=true on an actor principal is meant to insert the principal row at first login, but the runtime does not do this. An AuthenticationInterceptor is needed. | confirmed; Catalog already states the runtime gap at lines 55 and 76 (DefaultActorResolver only looks up, managed insert not implemented) and has keycloak-jit-user-provisioning. Nothing to add. |
| G232 | [ ] reopen | `c01-10` | A Keycloak user and the application's actor row are two separate stores. The runtime needs both before it can resolve the actor. | confirmed; Keycloak user vs entity-store row is documented (also judo-doc-problems.md record on managed user sync). Nothing to add. |
| G233 | [ ] reopen | `c01-15` | Port 8080 was already in use by another project's container, so Keycloak failed to take the default port. | confirmed; Port conflict was a local environment clash. build-process.md line 300 lists keycloak_port as a port override, and local-development.md covers start options. |
| G234 | [ ] reopen | `c01-39` | A stale view-page identifier from before a restart gave INVALID_IDENTIFIER (400) in the browser, and the console showed Axios errors. | confirmed; Signed identifiers section and error-handling-guide.md (INVALID_IDENTIFIER) cover the stale-identifier error after restart. Builder hit it as an environment effect, not a gap. |
| G235 | [ ] reopen | `g-L16` | Builder did not open structure.md and model-screen-layout.md, and read ui-authoring-guide.md only to section 6. | confirmed; GAPS item 16 says this explicitly; it records unread docs, not a missing or wrong entry. Retrieval note only: both files exist in the catalog. |
| G236 | [ ] reopen | `c02-06` | Builder read that a custom visual element is a model-flagged extension point: set customImplementation on the element, then register an FC under CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY | confirmed; Claim is a restatement of what the kb says (customImplementation plus CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY); the catalog paths exist. The real problems (table hook, view layout) are in other claims. |
| G237 | [ ] reopen | `c02-21` | Builder first concluded the generated project had no application/e2e module. The catalog switch exists: README 'Prerequisites > Enable E2E Generation' says set generateE2eModule=tr | partly; README lines 51-57 document generateE2eModule=true under Prerequisites. Retrieval problem: first kb search missed it; the builder found it after. The log R2 also says docs say only 'build' while generate and build are bo |
| G238 | [ ] reopen | `g-R3-6` | Own mistakes: deleting and re-adding fields lost customImplementation and the TextArea widget (textMultiLine=true restores it; textWidget=TEXT gives read-only text), fill re-added  | confirmed; textMultiLine is in widgets.md, tables-navigation.md and ui-behaviour.md, so the widget fix was findable. The fill/pressSequentially point is covered by the debounce item (R6-6). |
| G239 | [ ] reopen | `g-R5-5` | Own mistakes: macOS sed -i needs -i '' (first edit failed silently), type errors found only by the build, view fields removed too early (empty values). | confirmed; Builder process notes. Mac sed is an agent habit; the field-removal consequence is already in R5-2 (view mask loads only attributes that have a field). |
| G240 | [ ] reopen | `g-R5-6` | Catalog cards show a generated placeholder (gradient/mountain SVG) because the model had no image attribute. | confirmed; Design note of the round; c03-68 records the later real image upload. Image widget shapes (BinaryInput shows file name, ImageDisplay) are tracked under R7-16 (c03-54). |
| G241 | [ ] reopen | `c03-21` | Sort-by-price test read prices from all table rows, including the 0 row and a non-selected row, so the expected order was wrong. | partly; helpers-reference.md line 132 already documents the data-row selector that uses aria-selected; builder read raw rows. Retrieval/own-code issue, not a catalog gap. |
| G242 | [ ] reopen | `c03-45` | The Round 7 model script applied many CLI edits in one run with no check between steps; a partial run left unsaved edits, so the builder discarded them and reran the script. | confirmed; judo-cli.md "Known limitations" already says a failed script leaves earlier edits in memory and to discard --force before retrying, and documents --no-check. Builder did not apply it; retrieval problem only. |
| G243 | [ ] reopen | `c03-38` | Builder checked the catalog for how users get created and found a managed-actor admin pattern and a multi-actor projection blueprint; no documented first-login user creation withou | partly; Builder's finding is correct and the catalog already says auto-insert does not happen (authentication-guide.md line 84) and points to an AuthenticationInterceptor. Log R7 calls the interceptor 'platform (documented)'. No |
| G244 | [ ] reopen | `g-R7-15` | Negative proof for customer isolation is UI level only because rules forbid deep links; the test shows each customer sees only own addresses. | partly; Test limit as written. The real platform finding (signed identifier works for any caller, access filter covers lists only) is R14-7 and belongs to derived-access-filtering.md, not to this item. |
| G245 | [ ] reopen | `c04-09` | Validator warnings appeared after the Customer product access changed: 'Columns are not defined for the viewable table' and 'Principal of actor Customer should not have relations a | unverifiable; Only warnings noted in CLI output, no failed behaviour and no claim about the catalog; nothing to validate. |
| G246 | [ ] reopen | `c04-24` | Menu order is not taken from the model: the drawer shows Products, My orders, My addresses, Cart, My profile although the model lists Cart second; move commands had no effect on th | confirmed; Menu order not following model matches ui-hooks.md Reordering Menu Items (hook is the route) and the field-order family. Already documented. |
| G247 | [ ] reopen | `c05-25` | History rows show the login e-mail as the actor, not a person's name. | partly; True that the ACTOR variable gives the login e-mail (platform-behavior-reference lists variables); no failure and no catalog claim being wrong. Showing a name needs a lookup in the model, a design choice. |
| G248 | [ ] reopen | `c05-01` | The customer drawer profile showed the generated login name instead of the customer's name. | confirmed; ui-hooks.md line 243 documents CustomHeroPropsHook. Possible small add: say the default uses preferredUsername, which is a generated login for sign-ups. Low value. |
| G249 | [ ] reopen | `c05-06` | FUNCTIONS.md specifies the order status history as a post-call interceptor, which cannot fire for custom transition operations. | confirmed; interceptors.md says interceptors run for built-in CRUD only, never custom operations. The error was in FUNCTIONS.md (log R9: catalog correct). Fix FUNCTIONS.md, not the catalog. |
| G250 | [ ] reopen | `c05-07` | FUNCTIONS.md specifies a range interceptor for the default 30-day order filter, but range interceptors fire only on reference range operations, not on list calls. | confirmed; Catalog says range interceptors fire on reference ranges only; FUNCTIONS.md assumption was wrong (log R9). Derived access with now()!plusDays(-30) is covered by derived-access-filtering. |
| G251 | [ ] reopen | `c05-09` | FUNCTIONS.md says delete deactivates a product that has orders; the catalog pattern refuses the delete with a fault and leaves deactivation to the user. | confirmed; Spec vs pattern mismatch in FUNCTIONS.md (log R9). The practice name already covers a deactivate fallback; builder followed the spec. Fix FUNCTIONS.md wording. |
| G252 | [ ] reopen | `g-R9-11` | Admin frontend had no business-fault handler; the customer error interceptor from R8-6 was copied to the admin. | confirmed; Own omission; error-handling.md "Customizing the 422 Handling" is the documented route (session L2373 shows it was read). The duplication across actors is the R7-6 shared-code gap. |
| G253 | [ ] reopen | `c05-48` | The header tracks only one AppBarExtraComponents service, while ui-hooks.md shows several AppBar components; the drawer fix and the language switch had to be merged into one compon | partly; ui-hooks.md line 46 now says the AppBar accepts exactly one extra component and a Multiple AppBar Components section (line 214) shows merging into one. Already fixed; builder read an older or skipped text. |
| G254 | [ ] reopen | `c05-53` | The same timestamp is shown in two time zones: Ordered reads 02:03 while history rows of the same order read 03:03. | confirmed; Known: platform-behavior-reference has a Time and Time Zones section, audit-event-trail.md:29 and judo-doc-problems.md already record the UTC vs browser zone split. The builder consulted it (L3236-3238). Not a new ticket |
| G255 | [ ] reopen | `c05-61` | Browser tests cannot set the business clock: WEBSHOP_BUSINESS_DATE is read once at class load, so it needs an application restart. | confirmed; The clock pattern is in the catalog; a static final read at class load needs restart is a project design choice. Note a one-liner in that page is optional. |
| G256 | [ ] reopen | `c05-62` | Sale price window uses Date!now() in the model, so it follows the platform clock, not the business clock used by custom Java. | confirmed; Builder says the catalog states model expressions cannot call the Java clock; platform-behavior-reference covers Timestamp!now(). |
| G257 | [ ] reopen | `c06-18` | A derived effectivePrice Price value on WishlistItemInfo was replaced by a derived string priceLabel with ' EUR' appended; the reason for the change is not stated in the chunk. | unverifiable; Chunk gives no reason; a design choice by the builder (price label string), not a platform fact. |
| G258 | [ ] reopen | `c07-36` | One integration test failed with 'Outdated instance to update' (IllegalArgumentException in the update DAO processor) after the test changed the product's stock with a stale instan | confirmed; Real error in session L4215 (UpdatePayloadDaoProcessor). platform-behavior-reference.md lines 24-26 document the __version check and the "Outdated instance to update" message; the test used a stale instance. Not a test-d |
| G259 | [ ] reopen | `c07-39` | 'playwright install chromium' hangs during extraction on this machine, so the local config uses the installed Google Chrome channel. | unverifiable; Machine-local Playwright browser download hang (GAPS R2-2); environment, not catalog. |
| G260 | [ ] reopen | `c07-43` | Enumeration members have no label field (EnumerationMemberUpdateInput has only name, documentation, ordinal), so UI status text must come from a derived string member. | partly; Enum members really have no label input (L4452), but the generated UI translates enum members by key (i18n.md:45 enumerations.X.Y), so a derived label is only needed for custom text. Retrieval issue, no change. |
| G261 | [ ] reopen | `c07-45` | Each model change cost a stop, generate, build and start cycle of about 3 to 5 minutes (fixed sleeps of 125 to 150 seconds), and the full Playwright runs took about 8 minutes (admi | confirmed; Cycle times of 3-5 minutes are already listed in build-process.md. |
| G262 | [ ] reopen | `c07-26` | Timestamp!now() in model expressions follows the platform defaultZoneId (UTC here), while LocalDateTime.now() in custom Java follows the JVM zone; the builder confirmed this agains | confirmed; 'Time and Time Zones' section says exactly this (lines 98-99). Log R12 says the earlier R11 claim of a platform bug was a builder mistake; the catalog was right. |
| G263 | [ ] reopen | `c08-10` | Running mvn compile in application/app failed in the PSM generator with: there are manual changes in the generated files, discard them or add them to .generator-ignore. | confirmed; Running mvn directly in application/app hits the generator checksum guard; judo.sh generate-root and build -i is the documented route. |
| G264 | [ ] reopen | `c08-17` | Builder states that the generator adds every new column as a plain nullable column, so an existing row gets NULL and a required flag needs a backfill. | confirmed; Practice exists and the builder applied it (F52 first migration without wipe, log R12). The wipes in R6-R11 came from the schema-upgrade path problem, tracked in other claims. |
| G265 | [ ] reopen | `c09-17` | The test expected the e-mail as typed, but Keycloak stored and returned it lower-cased. | confirmed; The catalog already says Keycloak usernames are lowercase; only the test helper lowercases, a test-side detail. |
| G266 | [ ] reopen | `c10-14` | A custom page route for checkout needs src/extra-routes.tsx, which needs a .generator-ignore entry, which the standing rules forbid. So the step flow cannot have its own URL. | partly; The catalog already says to protect extra-routes.tsx in .generator-ignore; the conflict is the builder's own standing rule, not the platform. |
| G267 | [ ] reopen | `c10-31` | Vite could not Fast Refresh a component file that also exports a non-component (renderNothing), so the page reloaded fully on each edit. | confirmed; Standard Vite Fast Refresh rule (component files export only components); trivial. |

## F. Refuted claims (builder said X; validation found otherwise)

| ID | Claim | Finding |
|---|---|---|
| `c01-38` | The REST contract for updates and lists is not documented: the paths under /api/webshop/Shop/Shop/..., the X-Judo-SignedIdentifier and X-Judo-Mask headers, and the ~list and ~update verbs. | The REST contract is documented: X-Judo-SignedIdentifier, X-Judo-Mask, and ~list/~update/~create verbs are in platform-behavior-reference.md lines 14, 46, 68. Real issue: the builder did not find it (retrieval problem, backend/README.md does not point to it). |
| `c03-03` | Validator error AllRequiredFeaturesHaveBindingIfCreatable: a transfer object used by a create operation excludes required features (ProductInfo lacked sku and unit). | Rule AllRequiredFeaturesHaveBindingIfCreatable is at line 60 and in best-practices/model/relation-driven-crud-with-custom-input.md line 47. Builder hit the error before reading; retrieval problem, not a content gap. |
| `c03-04` | Validator error AggregationOnBothSidesAreNotAllowed (circular aggregation) on the mapped one-way relations ProductInfo.category and CategoryInfo.products, which the CLI created with relationKind AGGRE | Line 211 documents AggregationOnBothSidesAreNotAllowed. Only the CLI default (relationKind AGGREGATION on mapped one-way relations) could be added as a one-line note in judo-cli.md. |
| `c03-12` | Seed test failed with a 500: column t02.c_sku does not exist in the persistent PostgreSQL database after SKU was added to the model. | Line 79 says a persistent database that already holds data needs `./judo.sh schema-upgrade`. The builder missed it; a pointer from local-development.md would help but content exists. |
| `c03-39` | Builder noted that an image stored as a binary attribute cannot be used as a plain img src, because the download needs the token header; the catalog says to use a binary-to-object-URL hook. | The page already states a plain src link cannot work because download needs the token header, and gives the hook. Builder reading was correct; not a gap. |
| `c03-81` | Category filter test on the product table was marked test.fail() in Round 6 because a relation cannot be a top-level table column or filter without a derived attribute. | Claim is a non-gap: tables-navigation.md line 183 and best-practices/model/derived-attribute-flattening.md already give the route; the miner proposed none. |
| `c04-05` | Admin product table columns needed fixed widths at 1440 px, but the builder did not know the unit or value format of DataColumn.width and set plain integers (170, 120, 100 and so on). | tables-navigation.md line 30 says fixed pixel width and the example at line 56 uses width="200", so plain integers are right. The builder did use the correct format. |
| `c04-19` | The builder said the kb had no entry for the generated DAO method names, error handler and customization constants; the DAO names were read from the generated SDK instead. | data-access-guide.md covers DAO query/create methods and the builder read it at L2364; the kb-first search was not run for these names. Retrieval problem, not a catalog gap. |
| `c08-16` | Generated after-changeset for the new columns and tables contained an unresolved context variable, so the builder rewrote the file by hand and replaced the variable with sed. | The ${CTXV} placeholder came from the builder's own heredoc (session L4783); the generator wrote the file empty. Builder mistake, replaced with sed. No catalog change. |
| `c03-73` | Customer addresses list via CustomerAccount!filter(...)!any().addresses showed only 2 of 6 stored addresses. | `CustomerAccount!filter(...)!any().addresses` returns the addresses of ONE account by definition, so 2 of 6 (other addresses belong to other customers) is expected, not a platform bug. The back-reference form is the correct pattern and is covered. Evidence L23 |
