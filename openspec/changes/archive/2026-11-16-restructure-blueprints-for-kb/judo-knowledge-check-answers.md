# JUDO knowledge check: developer answers and their ripple effects

- **Source:** the developer's answered copy (`~/Downloads/judo-knowledge-check.md`).
- **What he answered:** K01–K56, with his comments written below the topics.
- **Not answered:** K57–K78. Part 3 has no answers at all, and Part 2 has answers only for K53–K56.

Many of his comments state general rules, so they also apply to the topics he did not answer and to the catalog. This file has four parts:

1. His verdict on each answered topic.
2. The general rules his comments establish.
3. What those rules mean for K57–K78. These are proposals only; he has not confirmed them.
4. Where the same rules touch the catalog.

Nothing in the catalog or in `judo-knowledge-check.md` has been changed yet.

## 1. Verdicts K01–K56

| ID | Verdict | His point |
|---|---|---|
| K01 | Tag | JSL: tag it as a separate, incomplete stack |
| K02 | In, minus one bullet | Measured literals are **not in use**. Use the runtime-core-esm-itest expression examples and the testkit to check what works |
| K03 | Tag | Same as K01 (JSL) |
| K04 | In, fix | `getVariable` needs the type of the value it returns: `String!getVariable('ACTOR','email')`. See the internal docs in the judo-ng documentation repo. Custom providers: **ask Robi** |
| K05 | In, plus a spike | 1: depends on precision **and** scale (scale counts inside the precision). Needs a spike to confirm. 2: true, enum ordinals may have gaps (1, 5, 8). 3: stays unsupported |
| K06 | Check | JSL tag. Check in the ESM runtime-core itest whether this works at all |
| K07 | **Out** | Measures are not in use |
| K08 | In | |
| K09 | In, check | SWITCH is not supported yet. Problems 2 and 3 need checking |
| K10 | In, extend | Default is 12. Small table has **no paging** (loads every row), so use it only for short lists. Inline edit works only with `isEager` and is fragile. Type-ahead and autocomplete apply to table-based single association/aggregation (not to links), often with a derived string label such as `firstName + ' ' + lastName` |
| K11 | In, extend | Build a **catalogue of the hooks**. The default error display can be overridden (he uses a toast/snackbar) |
| K12 | In | |
| K13 | In | |
| K14 | In, fix | Use `unset`. The enum bug may be worth a ticket; meanwhile use `filterBy` with a custom string filter. **Required attributes can be null too** when the mask filters them out (intended behaviour, not a bug), so do not null-guard on `required` alone |
| K15 | In, extend | The OpenAPI/Swagger spec is the reference. Most calls need a signed identifier, obtained through an access. Some headers appear only when needed: `CountRecords` (mode parameter) costs performance; `markSelectedItems` marks already-added rows in bulk and range calls (check). Frontend and backend both convert the wire formats |
| K16 | In, but bullet 3 **false** | The mapped-TO "AGGREGATION / `transfer_`" claim is false (also confirmed in the judo-ng code). The OpenAPI spec shows the endpoints. CRUD endpoints exist only with the update flag |
| K17 | In, plus a workaround | The frontend shows timestamps in the **browser's** time zone, which is a known backend bug. Until it is fixed, store timestamps in UTC in the backend and interceptors when `JUDO_PLATFORM_DEFAULT_ZONE_ID` is not UTC |
| K18 | In, check | REST-only operations get an endpoint, but the react-rest-template generates no TypeScript function for them (check) |
| K19 | In | **Use the OpenAPI spec to answer the other questions** |
| K20 | In, check | GET_RANGE is unbound but needs an owner with a signed identifier. GET_TEMPLATE is static and returns the transfer object defaults. Abstract entities cannot be created |
| K21 | In, check the codes | `ERROR_INVALID_IDENTIFIER`: e.g. a different transfer object mapped to the same entity, or one from another access, used as a reference. A range transfer object cannot be used to set a reference or to update |
| K22 | In, rewrite | Pure JCL operations are no longer used: the `.default` custom implementation is written instead. With `customImplementation=true` and no body, the app waits for the OSGi service. Error payload: an **unmapped TO with a string `errorCode`** (an enum is stricter and less extensible). Avoid operation names that start with set/get/create/delete combined with a relation name |
| K23 | Questioned, not a problem | "Are you sure?" **Confirmed in code**: the dispatcher hands interceptors only to built-in behaviour calls, and SDK and script operations bypass them. His position: put the checks in the custom operation |
| K24 | **Deprecated** | JCL is outdated. Tag it JCL + Deprecated |
| K25 | In | Check it, but OK |
| K26 | In, warning | Protect SYSTEM-actor endpoints carefully, because anyone can call them |
| K27 | In | The user is matched through an `identifier=true` attribute, usually e-mail. Extra Keycloak clients map to actors, e.g. a mobile client configured differently from the web client |
| K28 | Check | All three bullets need checking |
| K29 | In, check | The OIDC metadata endpoint is where a user gets a signed identifier |
| K30 | In, extend | Other projects build a custom Keycloak image with the themes and a magic-link login |
| K31 | In, extend | Default yes. Set the CORS attributes explicitly in production |
| K32 | In, extend | The DB stores only the filestore id, name and type. **The filestore has 3 modes: RDBMS, filesystem, S3** |
| K33 | In | Many S3 providers are supported. Google is used now |
| K34 | In, rewrite | Production runs migrations automatically. Locally: generate the Liquibase SQL, add the data changes, then execute. **Never use `apply`.** `.missing` scripts are written to `.sql`. **Never ignore the version check** |
| K35–K36 | In | |
| K37 | In, steer | Normally the DAO-level API is used. Suggest missing DAO-level concepts instead |
| K38–K40 | In | Health checks report the application's health state |
| K41 | In, extend | The frontend runs either with Vite or through Karaf |
| K42 | In, extend | Use `-i` / `ignoreChecksum=true` for leftover frontend files |
| K43 | In | |
| K44 | In, check | |
| K45 | In, extend | Generate the project with the agent CLI ESM fullstack to get the newest version |
| K46 | **Out (deprecated)** | Flutter has been deprecated for a long time |
| K47 | In, fix | Building the QueryFactory is slow, so build the runtime per test class |
| K48–K49 | In | |
| K50–K52 | No answer | See section 3 |
| K53 | In, fix | Put the type-ahead relation on a **separate single-TO access**, so users without the main access can still use it |
| K54 | **Bullet 2 false** | `createAll` "batching" is **not faster**: it is a loop and caches nothing |
| K55 | **False** | No mask means **all attributes are returned, derived ones included**. `X.mask()` with no attributes returns only the identifier. `X.mask().attr` adds `attr` |
| K56 | In | |

## 2. General rules from his answers

Each rule cites the topic it comes from.

| # | Rule | From |
|---|---|---|
| R1 | JCL is deprecated: tag every JCL mention JCL + Deprecated | K24, K22 |
| R2 | Flutter is deprecated: drop or tag it | K46 |
| R3 | JSL is a separate, incomplete stack: tag it | K01, K03, K06 |
| R4 | Measures and measured literals are not in use | K07, K02 |
| R5 | Mask semantics: no mask = everything (derived included); empty mask = identifier only; `.mask().attr` adds `attr` | K55 |
| R6 | Required ≠ non-null: a masked-out required attribute is null | K14 |
| R7 | `createAll` is a plain loop: no speed-up and no caching | K54 |
| R8 | Interceptors cover built-in behaviour calls only (confirmed in code); custom operations do their own checks | K23 |
| R9 | Timestamps: browser time zone bug; store in UTC when the default zone is not UTC | K17 |
| R10 | The OpenAPI/Swagger spec is the reference for endpoints, headers and identifiers | K19, K15, K16 |
| R11 | Check claims against runtime-core-esm-itest with the testkit before stating them | K02, K06 |
| R12 | Filestore: 3 modes (RDBMS, filesystem, S3); the DB stores filestore id, name and type | K32, K33 |
| R13 | Migrations: generate SQL, add data changes, execute; never `apply`; never skip the version check | K34 |
| R14 | Leftover frontend files: regenerate with `-i` / `ignoreChecksum=true` | K42 |
| R15 | Error payloads: an unmapped TO with a string `errorCode` | K22 |
| R16 | Operation names: avoid set/get/create/delete combined with a relation name | K22 |
| R17 | Prefer the DAO-level API over QueryCustomizer and native SQL | K37 |
| R18 | Type-ahead lives on its own single-TO access | K53, K10 |
| R19 | Small table loads all rows (no paging); inline edit only with `isEager` and is fragile | K10 |
| R20 | `getVariable` needs the type of the value it returns: `String!getVariable(...)` | K04 |
| R21 | Endpoints reachable by SYSTEM actors or external clients need explicit protection | K26 |
| R22 | Principal = the `identifier=true` attribute, usually e-mail | K27 |
| R23 | A range TO, or another TO of the same entity, cannot set a reference (`ERROR_INVALID_IDENTIFIER`) | K21 |
| R24 | Test runtime: build per class (the QueryFactory is slow) | K47 |
| R25 | CORS explicit in production; Keycloak themes in a custom image | K31, K30 |

## 3. What the rules mean for the unanswered topics (proposals)

| ID | Proposed | Why |
|---|---|---|
| K50 | Fix bullet 1 | "Missing the mask means the value is never queried" is true only when a mask is given (R5). With no mask, everything comes back |
| K51 | Fix bullet 2 | The example uses `getVariable("ACTOR","email")` without the type of the returned value. Write `String!getVariable(...)` (R20). E-mail as the identifier matches R22 |
| K52 | Extend | Add regeneration with `-i` / `ignoreChecksum=true` (R14) |
| K53–K56 | Answered | See section 1 |
| K57 | In, fix | Prefer a string `errorCode` on an unmapped TO (R15). The interceptor-wrapping bullet agrees with R8 |
| K58 | In | Agrees with R15 (returned data instead of an exception) |
| K59 | In, add caveat | A range TO cannot be used to set the reference afterwards (R23) |
| K60 | In | Bullet 3 matches R8 and the code check |
| K61–K62 | In | Nothing contradicts them |
| K63 | Check | The DB holds the filestore id (R12). Whether the id is exposed depends on the mode and endpoint; check the OpenAPI spec (R10) |
| K64 | Weaken | Last resort only. Prefer the DAO-level API or suggest a DAO concept (R17) |
| K65 | In, add warning | External or sidecar callers need protected endpoints (R21) |
| K66 | In | Add the UTC timestamp caveat for date assertions (R9) |
| K67 | In, fix | Replace "runtime version that caches the model loader" with "build the runtime per test class" (R24) |
| K68–K69 | **Ask** | K68 (DOCX/XDocReport) and K69 ("Markdown templates replace XDocReport") contradict each other. Which pipeline is current? |
| K70 | In | Nothing contradicts it |
| K71 | In, add caveat | Interpolated dates are subject to R9 |
| K72 | In | Derived gate flags match K51. Close permission per user agrees with R22 |
| K73 | In | Nothing contradicts it |
| K74 | In, add notes | The two-stage upload matches K32 and R12. The mobile client maps to its own Keycloak client (K27). Protect the endpoints (R21) |
| K75–K76 | In | Nothing contradicts them. K76 role scoping agrees with K62 |
| K77 | In, add notes | External clients use the modelled API (agrees with R21). Storage per R12 |
| K78 | In | Nothing contradicts it |

## 4. Where the rules touch the catalog

These counts come from a quick grep and are not yet reviewed.

| Rule | Catalog files hit | Action |
|---|---|---|
| R1 JCL | 26 | Tag JCL + Deprecated; point to `.default` custom implementations |
| R2 Flutter | 9 | Tag deprecated or remove |
| R3 JSL | 27 | Tag as a separate, incomplete stack |
| R4 Measures | 6 | Mark not in use |
| R5 Mask semantics | 3 (e.g. `agent-docs/backend/platform-behavior-reference.md`, `best-practices/backend/entity-re-fetch-pattern.md`, `document-generation-pipeline.md`) | Correct the mask and derived-member claims |
| R7 `createAll` | 5 (e.g. `agent-docs/backend/data-access-guide.md`, `best-practices/backend/builder-pattern-entity-creation.md`) | Remove "batched/faster" claims |
| R8 Interceptors | `agent-docs/backend/interceptors.md`, `custom-operations.md` and blueprints that rely on interceptors | Check that nothing promises interception of custom operations |
| R12 Filestore | 28 | Add the 3-mode statement where storage is described |
| R14 Regeneration | 6 | Add `-i` / `ignoreChecksum=true` |
| R19 Small table | 7 | Add the "no paging, fragile inline edit" caveat |
| R20 `getVariable` | 77 uses, 28 with a type prefix | Add the type prefix to every expression example |
| K16 bullet 3 | Not in the catalog. Only `judo-doc-problems.md` lines 581–582 have it | Remove it there |

## Open questions for the developer

- **K04:** custom variable providers (ask Robi).
- **K05:** precision and scale spike.
- **K09:** problems 2 and 3.
- **K28** (signed identifiers) and **K44** (custom configuration parameters): need checking.
- **K68 vs K69:** which document pipeline is current?
- **K57–K78:** confirm the proposals in section 3.
