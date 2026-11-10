# Pass B v2: agent-docs gaps reported by the catalog rewrite

The 35 Pass B v2 batches (310 catalog entries) each reported places where the corrected agent-docs did not support a claim. This file collects those reports. Duplicates are merged. Every "missing" item was checked with grep against `catalog/agent-docs/` (excluding `AGENTS.md`). Items that turned out to be documented are listed in section F.

Batch ids in brackets: `bp` = model blueprints, `pm`/`pb`/`pf` = model/backend/frontend practices. The per-entry records are in `target/passb2/applied/<batch>.json`. Where an entry had to hedge because of a gap, it says "project practice" or "verify in your version".

## A. Contradictions: the docs say something the CLI or runtime rejects

**Status: all 9 applied.** A1, A2, A5 and A6 were reproduced in a fresh Sandbox with `judo-cli` (`'AGGREGATION' is not valid`, `Access target have to be mapped`, `Unknown symbol: self`, `Unknown function: isempty`). The catalog is re-checked by `skills/judo-blueprint-author/scripts/claim-check`.

| # | Gap | Evidence | Reported by | Where to fix |
|---|---|---|---|---|
| A1 | `AGGREGATION` is listed as an entity `relationKind` with no caveat (`structure.md` lines 87 and 204; `advanced-modeling-patterns.md` says one-way AGGREGATION is fine). The CLI rejects it: only `ASSOCIATION` and `COMPOSITION` are accepted, even though `--schema` lists it. | CLI error `relationKind: 'AGGREGATION' is not valid` | bp03, bp10, bp15, pm05 | `model/esm_metamodel/structure.md`, `model/advanced-modeling-patterns.md` |
| A2 | Dashboard panel as an **unmapped** transfer object. `validate --strict` rejects an access to it: "Access target have to be mapped". | Sandbox build | pm05 | `model/advanced-modeling-patterns.md` |
| A3 | `theming.md` "Customizing Theme" still says to edit `src/theme/palette.ts` and add it to `.generator-ignore`. The overview of the same file says the palette is model-driven on the actor. | `frontend/theming.md` lines 14, 23, 107 | pf04 | `frontend/theming.md` |
| A4 | Use of `self` is inconsistent. `architectural-patterns.md` says `self` is not in scope in actor access getters, but `advanced-modeling-patterns.md` uses `self` in a derived attribute on the principal transfer object. These are two different contexts, but neither doc says so. | Doc comparison | pm02, pm05 | `backend/architectural-patterns.md`, `model/advanced-modeling-patterns.md` |
| A5 | JCL operation bodies need `this`. `self` fails the build with "Unknown symbol: self", and no doc says this. | Sandbox build | pm01 | `model/model-development.md` (JCL) |
| A6 | `!isEmpty()` fails as an "Unknown function". Only `!empty()` exists (in `model-development.md`), and there is no JQL collection-function table. | Sandbox build | pm01 | JQL function reference (also in knowledge-gaps-report §1) |
| A7 | `downloadFile` with `inline`: `platform-behavior-reference` says it renders in a dialog frame, but rackinspect opens a new tab. Which one applies is version-dependent and not stated. | Project vs doc | bp08, pf05 | `backend/platform-behavior-reference.md` |
| A8 | Transfer object inheritance is documented as "not supported", but the CLI schema for `TransferObjectType` has `superTypes`. | CLI `--schema` | pm07 | `model/esm_metamodel/structure.md` |
| A9 | `Long` precision is 15 in the JSL built-in library and 18 in the projects' type libraries. | Source comparison | pm06 | `model/` types |

## B. Missing platform knowledge (confirmed absent from agent-docs)

### Backend runtime

| # | Topic | What developers need | Reported by |
|---|---|---|---|
| B1 | **Custom operation transaction scope** | Whether a custom operation's DAO writes share one transaction, whether they roll back when it throws, partial commits, and what a swallowed DAO error does to the transaction. Only `@JudoTest` transaction modes and interceptor transactions are documented. | bp01, bp02, bp05, bp08, bp12, pb06, pb07 (most-reported gap) |
| B2 | **FileStore Java API** | `FileStoreService` put/get, the generated `FileType` (id, fileName, mimeType) from Java, and `JUDO_PLATFORM_FILESTORE=rdbms`. Only the upload-token REST flow is documented. | bp01, bp05, bp10, pb01, pb03, pb07 |
| B3 | **INITIALIZER operation lifecycle** | Who calls an initializer operation, when (startup or deploy), under which security context, and with which transaction. Docs only say "static, no input". | bp07, pm04, pm06, pb02, pb03 |
| B4 | **Scheduled jobs** | Quartz / OSGi scheduler. What transaction, principal and `ACTOR` variable context a scheduler thread gets. | bp06, bp10, pb05, pb06 |
| B5 | **Email service** | `EmailService` / `EmailMessage` / `BinaryAttachment` API, Handlebars templates, and how the app's mail path uses the SMTP variables. | bp10, pb02, pb03 |
| B6 | **DAO API surface** | Paged `selectList(offset, limit)` / slices, `TimeFilter`, `findAllById` vs `getById`, signatures of the per-relation `create<Rel>` / `add<Rel>` methods, and actor-level DAO packages. | pb01, pb02, pb05, pb06, bp07, bp12 |
| B7 | **DAO and interceptors** | Whether a DAO call from Java service code (for example creating a child) triggers built-in-operation interceptors. | pb05, pb07 |
| B8 | **Unmasked update** | What `update` without a mask does with fields that were not loaded. | pb05 |
| B9 | **Identifier uniqueness** | Whether the `identifier` flag is enforced as unique, for one or several attributes. Docs only say "natural key". Uniqueness appears only as a hand-written validation pattern. | bp01, pm02, pm06, pb07 |
| B10 | **Faults from JCL / script operations** | Whether a script operation can raise a modeled fault or call an OSGi service. | pm04, pb06 |
| B11 | **List-call interceptor payload** | `ListCall.ListCallPayload` and `getQueryCustomizer().getFilter()`. The range payload is partly covered in `interceptors.md`, but there is no worked `_getRangeReference` example that keeps the filter and orderBy and adds constraints. | pb04, bp15 |
| B12 | **Unauthenticated operations** | How to expose an operation without login. The model-level `anonymous` actor flag is documented only in e2e-testing. | bp08, pb05, pb07 |
| B13 | **`isActiveExpression`** | How the runtime evaluates it, and how it interacts with actor resolution by `azp`. There is no sample with a boolean role flag as the guard. | bp14, pm04 |
| B14 | **Authentication interceptor scope** | `AuthenticationInterceptor` runs on authentication events, not operations. This is stated nowhere. | bp14 |
| B15 | **`VariableResolver` target filter** | Whether a `judo.model.name` target filter is needed. | pb06 |
| B16 | **Mapped claim attributes** | A claim attribute on a mapped principal must map to an identifier or derived attribute, and the `required` flags must match. Only partly stated. | pm01, pm05 |
| B17 | **Enum ordinals** | How the runtime rejects an out-of-range ordinal, whether JQL can compare ordinals, and `getByOrdinal` (only one known-issue mention). | bp05, bp08, bp11 |
| B18 | **Generated `BusinessErrorException`** | That it is generated per project from a modeled fault. Several entries had to explain this from scratch. | bp10, pb07 |

### Model

| # | Topic | What is missing | Reported by |
|---|---|---|---|
| B19 | `self!container(X)` as a derived back-reference relation | `!container(type)` is defined, but its use as a relation getter is shown only in a best practice. | bp14, pm02 |
| B20 | Range expressions on entity relations | Only input-parameter range attributes are documented. A `rangeExpression` needs `rangeType=DERIVED`. It is unknown whether `self` is allowed in a range expression and whether the server enforces a derived range. | pm05, pm06, pm07 |
| B21 | CRUD flags on a whole entity or transfer object | What a false `createable`/`updateable`/`deleteable` on a whole entity does to generated pages and REST endpoints. Only relation-level flags are documented. | bp09, pm03 (also MO-148) |
| B22 | Enum default literal | `Type#VALUE` syntax in `defaultExpression` | pm03 |
| B23 | Fault parameters | A fault parameter must be unmapped. The `Parameter` section does not cover faults. | pm03 |
| B24 | `immutable` | Whether it can be set on entities. It appears only in the signed-identifier section. | pm06 |
| B25 | `mutable` on transient references | What it does to a transient reference read from an operation input. | pm07 |
| B26 | Static operations on an unmapped TO via an actor | Only the `StaticOperations` container TO is described. | bp03 |
| B27 | Group roles | No example of unioning group roles into `effectiveRoles`. | bp14 |
| B28 | Derived attribute in tables | Whether a derived attribute can be sorted or filtered in generated tables. | pm02 |
| B29 | `!sum` on null or empty collections | Result is not stated. | pm05 |
| B30 | Deleting the target of an association | Only composition cascade is documented. What happens to an association (and a "primary" reference) when its target is deleted is not. | bp06, pm05 |
| B31 | `type.md` standard limits | The `Text`, `Phone`, `URL` and `Email` limits are not listed. | bp13 |
| B32 | UI model custom-implementation marker | How the UI model marks an element as a custom implementation. Only the `customImplementation` flag on a Placeholder is mentioned. | bp09 |

### Frontend

| # | Topic | What is missing | Reported by |
|---|---|---|---|
| B33 | Event bus | The publish/subscribe API and its event key format. | pf02 |
| B34 | Page hooks | `getMask()` page-hook handler and `_mask` syntax, the page data-mask hook (`...RelationViewPageActionsHook`), `queryCustomizer` on pages, and `postGetTemplateAction` / `storeDiff` after a template. | bp04, pf03, pf04 |
| B35 | Hook naming | The `isFieldRequired` handler vs the documented `is<Field>Required`, the range-override hook member name, and the cards-configuration hook return shape and key (one sentence today). | pf01, pf02, bp03 |
| B36 | Generated page files | Contents of `context.tsx` (ViewModel), `customization.ts`, `types.ts`, and `src/config/layout.ts`. | pf03, pf06 |
| B37 | Generator override fragments | Frontend `package.json.dependencies.extra.fragment.hbs` and `application_default_extra.fragment.hbs` (i18n). `build-process.md` lists only pom and Karaf fragments. Also the Handlebars helper `elementHasAnnotation`, the `operation.output.target` context, how a literal `{{…}}` survives rendering, and the `operation-primary-output-handler` / `@redirect` mechanism. | pf03, pf04, pf05, bp15 |
| B38 | Layout replacement | Whether a container layout can be replaced by any route other than a custom implementation element. `data-name` selectors on generated sections. | bp04 |
| B39 | Error codes | `INVALID_CODE`, `IDENTIFIER_ATTRIBUTE_UNIQUENESS_VIOLATION`, `getErrorCodeLiteralByOrdinal`. | pf02 |
| B40 | Aggregation actions | Frontend service-method signatures for add, remove, clear and set, and the range-dialog call. | pf04 |
| B41 | Widgets and rows | Whether the boolean combo can show "unknown", hiding a row action per row, a count-only list-call recipe (`__countRecords` / `X-Judo-Count` are named but no recipe exists), the old `/{model}/{actor}` context path, and signed-identifier route parameters. | pf01, pf02, pf06, bp11 |
| B42 | Operation outputs | The output `behaviours` list (REFRESH/UPDATE/DELETE), `OPERATION_OUTPUT_UPDATE` page type, and the order of generated input and output pages. | pm05, pf01 |
| B43 | `confirmationCondition` | It has no ui-authoring-guide section, only a one-line invariant. | pm07 |
| B44 | `useJudoNavigation` | Whether it keeps a breadcrumb or history. | pf01 |
| B45 | `textMask` vs react-imask | No link between the model `textMask` and a custom-element alternative. | bp09 |
| B46 | Responsive per-device page containers | Mobile, tablet and desktop containers and column counts. | pm05 |
| B47 | Anonymous actor frontend | No how-to for an anonymous actor's own app, only `supportGuestAccess` and the guest page. | bp08 |
| B48 | Flutter | Asset copy rules in `flutter.yaml`. The Flutter section is thin overall. | pf02, pf06 |
| B49 | `.default` scaffold files | The docs say never rename them, but several projects do. | pb03 |

## C. Project-practice topics: decide whether the agent-docs should cover them

None of these are documented. Entries label them as project practice. Whether they belong in agent-docs, or stay as catalog practices only, is your call.

- Capacitor / native clients: password grant, native OIDC token storage, push notifications [bp02, bp11]
- Keycloak SPI extensions: authenticator, token lifespan and reuse [pb04]
- SOAP / JAX-WS / CXF clients and the OSGi-service wrapper [bp13, pb06]. `SOAP` appears in `platform-behavior-reference` and debugging only incidentally.
- SpEL guards [pb06]
- XDocReport / docx4j / JODConverter document generation [bp15]
- JAXB / XSD client bundles [pb04]
- react-intl, hand-built dialog contexts, PWA manifest content [pf05]
- OSGi Declarative Services annotations (`@Designate`, `configurationPolicy`) [bp06]
- Platform secret or token generator [pb01]
- Per-actor access filters for project scoping [bp07]
- Lookup / reference-data and seeding patterns [bp12]

## D. Tooling issues (not agent-docs)

| # | Issue | Owner |
|---|---|---|
| D1 | `kb_get` with a `section` heading path copied from `kb_search` often returns "not found". A path-only call returns the first section only. Reported by almost every batch. | kb extension |
| D2 | `kb_search` ranks openspec sweep and inventory files above `catalog/agent-docs`. `doc_type: doc` does not filter them, and `doc_type: agents` returned nothing. Consider excluding `openspec/changes/**/sweep-inventory` from the index. | kb config |
| D3 | The kb guard ("3 consecutive searches") fires on legitimate CLI and grep work. Bash output containing `ctx_search` or large output gets replaced by a stub. | dashboard / context-mode |
| D4 | The CLI rejects `create --set cardinality=` on Access (it needs `upper`/`lower`), and `accessType=DERIVED` must be set before `getterExpression`. | judo-model-cli skill |
| D5 | An Access to a transfer object needs `fill` first, or `validate --strict` fails with "Columns are not defined". | judo-model-cli skill |
| D6 | `create ... mapping=` auto-creates mapped members, so adding them again gives duplicates. Members bind as `Entity.attr`. | judo-model-cli skill / `fragments.md` |
| D7 | `create -t OneWayRelationMember` ignores `relationKind` when `cardinality` is set, and two-way relation creation auto-creates extra relations. There is no `RelationMember` type. | judo-model-cli |
| D8 | `query esm X --select <relation>` fails with "Subselection required". `query` needs the model name first. | judo-model-cli skill |
| D9 | The CLI session goes stale after a failed run ("Container not found"), and `server stop --force` fixes it. | judo-model-cli |
| D10 | The Sandbox fixture has no `Decimal` or `Binary` type, but the Pass B prompt listed `Decimal`. | author skill fragments fixture |
| D11 | `mermaid model --members` accepts `types`, `names` or `none` (not `all`). The renderer omits operations and faults. | judo-model-mermaid |
| D12 | The `ActorType` realm field is rejected for the default actor. | judo-model-cli |

## E. Catalog follow-ups found during the run

- ~~`capacitor-native-auth-pkce-passkey/frontend.md` mirror sentence~~ softened [bp02].
- Also fixed by claim-check: `panel-dashboard-transfer` and `actor-based-transfer-projection` (an unmapped panel cannot be an access target), and the `bulk-json-upload-entity` one-transaction claim (now says to verify). Removed a broken `../domain/README.md` link in `deployment/tooling-guide.md`.
- Dead related ids were dropped: `category-hierarchy`, `flutter-arb-localization`, `flutter-frontend-framework`, `three-layout-responsive-pattern` and `flutter-clone-edit-save-pattern`. They are candidates for new entries or should simply stay gone.
- 164 of 310 entries have weak kb-use records (fewer than 3 queries or fewer than 2 docs). Prioritise them in the content review.

## F. Reported as missing but actually documented (findability problems)

- Single-valued relation queries return the entity directly: `backend/data-access-guide.md` lines 289 and 304 [pb01].
- `GetReferenceRangeCallPayload` / `_getRangeReference`: `backend/interceptors.md` and `model/esm_metamodel/operation.md` [bp15, pb04]. Only the worked example is missing (B11).
- `confirmationCondition`: in `esm-to-ui-mappings/widgets.md` and `tables-navigation.md`, but not in the authoring guide (B43).
- i18n proxy service: partly in `backend/internationalization-guide.md` [pb03].
- `FileType`: in `backend/data-access-guide.md` and `frontend/advanced-patterns.md`, but not from the FileStore Java API side (B2).
