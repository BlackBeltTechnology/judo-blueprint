# Judo knowledge decisions for framework developers

The **71 decisions** that need a judo framework developer — someone who knows the
platform internals. Each row is a knowledge gap the review **accepted** (324
validated gaps grouped into these topics). One row = one entry to write, confirm
against source, and place.

Excluded on purpose: CLI tooling/syntax (owned by the `judo-cli` skill), how the
catalog was mined/validated, model/reader-role picks, and task planning. For the
specific *wrong facts* to correct (API names, signatures, EVL rule names), see
`catalog-update-report.md` §3.

**Scope gates** (`⚠scope`): JSL and Flutter are **out of scope** — skip unless
reinstated. Spring Boot runtime is **in scope**.

Counts: agent-docs 49 · best-practices 15 · model-blueprints 7. Priority:
High 40 · Medium 25 · Low 6.

---

## agent-docs — missing platform knowledge (49)

| Pri | Area | Decision | Goes to |
|---|---|---|---|
| High | backend | Generated DAO/SDK behaviour that surprises developers (known issues) | agent-docs/backend/data-access-guide.md |
| High | frontend | UI model values that break the generator (known issues) | agent-docs/frontend/esm-to-ui-mappings/ |
| High | integration | Binary upload/download: two-phase token flow | agent-docs/backend/file-upload-download.md (new) |
| High | security | SYSTEM / non-principal actors: exposure, transfer-object closure, realm | agent-docs/model/system-actors.md (new) |
| High | deployment | Multi-module build order and stale artifacts | agent-docs/deployment/build-process.md |
| High | model | JQL / derived-member rules that fail late | agent-docs/model/jql-reference.md |
| High | backend | Platform error codes and payload-validation semantics | agent-docs/backend/error-handling-guide.md |
| High | backend | Custom operation runtime contract (no impl bundle, customImplementation=false, stateful ops) | agent-docs/backend/custom-operations.md |
| High | security | Principal-to-actor resolution and multi-client Keycloak mapping | agent-docs/backend/authentication-guide.md |
| High | testing | JUDO testkit: runtime caching, DB selection, fixtures, Guice composition | agent-docs/integration-testing/getting-started.md |
| High | backend | Signed identifiers: lifecycle, churn and secret | agent-docs/backend/signed-identifiers.md (new) |
| High | integration | Generated REST API contract (paths, headers, metadata fields, wire formats) | agent-docs/backend/rest-api-contract.md (new) |
| High | backend | Which operations interceptors see, and how several compose | agent-docs/backend/interceptors.md |
| High | deployment | Schema migration: manual steps, `.missing` review scripts, version checks | agent-docs/deployment/schema-evolution.md |
| High | model | Relation kinds, CRUD flags and the endpoints they generate | agent-docs/model/model-development.md |
| High | deployment | Filestore on S3/GCS: configuration and access URLs | agent-docs/deployment/application-config.md |
| High | backend | Time zones and date/time wire format | agent-docs/backend/data-access-guide.md |
| High | model | JQL function reference: temporal, collection, aggregation, string, measured literals | agent-docs/model/jql-reference.md (new) |
| High | model | Undocumented UI-model attributes | agent-docs/model/esm_metamodel/ui.md |
| High | model | JSL (textual model) language: events, errors, opposite-add, escaping, build constraints ⚠scope | agent-docs/model/jsl/ (new) |
| High | deployment | Runtime/container configuration (health checks, datasource, Karaf, Docker image) | agent-docs/deployment/production.md |
| High | model | Generated database schema: naming, audit columns, indexes | agent-docs/deployment/schema-evolution.md |
| High | frontend | Frontend OIDC metadata, logout and guest access | agent-docs/frontend/authentication.md (new) |
| High | model | JCL operation-body language reference | agent-docs/model/jcl-reference.md (new) |
| High | frontend | Frontend extension points not yet documented | agent-docs/frontend/hooks/ |
| Medium | backend | Custom JAX-RS resources and REST-only endpoints | agent-docs/backend/custom-rest-resources.md (new) |
| Medium | frontend | MUI X Pro/Premium license configuration | agent-docs/frontend/mui-license.md (new) |
| Medium | testing | Test-suite memory: multi-JVM heap exhaustion hides unrun classes | agent-docs/integration-testing/best-practices.md |
| Medium | testing | Local e-mail testing (Mailpit) incl. Keycloak realm SMTP | agent-docs/deployment/local-development.md |
| Medium | backend | Optimistic locking (`__version`) on updates | agent-docs/backend/data-access-guide.md |
| Medium | model | Expression variable categories beyond ACTOR/PRINCIPAL, and custom providers | agent-docs/model/model-development.md |
| Medium | model | Type mapping and type-level constraints (precision→Java, enums, unsupported types) | agent-docs/model/esm_metamodel/type.md |
| Medium | model | Parameterized queries and parameter ranges | agent-docs/model/model-development.md |
| Medium | model | Measures and units: store unit, precision, conversion | agent-docs/model/esm_metamodel/other.md |
| Medium | frontend | Frontend build properties, environment variables and base path | agent-docs/frontend/development-workflow.md |
| Medium | frontend | Forcing regeneration: `.generator-checksum-ignore`, Biome false positives | agent-docs/frontend/development-workflow.md |
| Medium | deployment | Running JUDO on Spring Boot ⚠scope | agent-docs/deployment/spring-boot.md (new) |
| Medium | integration | OpenAPI: generating and serving API docs, generating clients | agent-docs/backend/rest-api-contract.md |
| Medium | backend | Custom application parameters (OSGi Configuration Mapper) and encrypted values | agent-docs/deployment/application-config.md |
| Medium | security | Customizing the Keycloak login theme | agent-docs/deployment/keycloak-theme.md (new) |
| Medium | model | Generated operation behaviours (GET_RANGE, GET_TEMPLATE, create validation) | agent-docs/model/esm_metamodel/operation.md |
| Medium | frontend | Long-running operations: frontend/proxy timeout (503) | agent-docs/deployment/production.md |
| Medium | deployment | Creating and upgrading a JUDO project (archetypes, version updater) | agent-docs/deployment/new-project.md (new) |
| Low | model | Static navigations and static data | agent-docs/model/esm_metamodel/ |
| Low | backend | Request tracing (exchange id) and validation-message localization | agent-docs/backend/debugging-and-monitoring-guide.md |
| Low | backend | Low-level persistence hooks worth one paragraph each | agent-docs/backend/data-access-guide.md |
| Low | testing | API-level tests against generated REST (ApiClient, Postman) | agent-docs/integration-testing/api-level-tests.md (new) |
| Low | deployment | Backend CORS filter configuration | agent-docs/deployment/application-config.md |
| Low | deployment | Flutter frontend build ⚠scope | agent-docs/deployment/build-process.md |

---

## best-practices — missing patterns (15)

| Pri | Area | Decision | Goes to |
|---|---|---|---|
| High | frontend | Model changes that break generated/custom frontend code | best-practices/frontend/model-change-propagation.md (new) |
| High | backend | DAO read/write performance: seek, batching, eager owned relations | best-practices/backend/dao-read-write-performance.md (new) |
| High | security | Enforce rules server-side, not only in the UI | best-practices/backend/server-side-guards.md (new) |
| High | testing | E2E methodology: baseline dump, real-UI first, time budget | best-practices/ e2e entry + agent-docs/e2e-testing/testing-patterns.md |
| High | model | Model workflow gates as derived predicates over status | best-practices/model/ (new entry) |
| High | backend | Document template authoring (FreeMarker/DOCX, Handlebars) and repair | best-practices/backend/document-template-authoring.md (new) |
| High | integration | Report/export SPIs: JasperReports, Excel export, Markdown reports | best-practices/backend/ (one entry per SPI) |
| High | backend | Registry numbering: no burn on regenerate, real locking | model-blueprints/document-registry-sequence (update) |
| Medium | integration | Adding a non-Java sidecar service (Node/AI) to a JUDO app | best-practices/backend/sidecar-service.md (new) |
| Medium | model | Report validation problems as optional transient output, lazily loaded | best-practices/model/ (new entry) |
| Medium | backend | Native SQL / DataSource access from custom code | best-practices/backend/native-sql-datasource.md (new) |
| Medium | model | Type-ahead with a self-learning reference dictionary | best-practices/model/ (new entry) |
| Medium | domain | Detailed bilingual history/audit messages | model-blueprints/history-audit-trail-entity (extend) |
| Medium | model | Operation input prefill (initializer) and range selectors | best-practices/model/ (new entry) |
| Medium | security | Serving stored binaries without exposing filestore ids | best-practices/backend/ (new entry) |

---

## model-blueprints — missing domain knowledge (7)

| Pri | Area | Decision | Goes to |
|---|---|---|---|
| High | domain | Inspection fault-registry / ticketing lifecycle | model-blueprints/inspection-fault-registry-ticketing (new) |
| High | domain | Job sheet → work report → completion certificate pipeline | model-blueprints/jobsheet-workreport-certificate (new) |
| High | domain | Offline-first mobile ingest: localId idempotency, two-stage upload, change stamps | model-blueprints/offline-mobile-ingest (new) |
| High | domain | Offer pricing: cost vs price, markup, minimum floor, quantity reconciliation | model-blueprints/offer-cost-price-minimum (new) |
| High | domain | Partner-scoped multi-role users and visibility matrix | model-blueprints/partner-scoped-multi-role-users (new) |
| High | domain | Typed media-attachment entity with polymorphic owners | model-blueprints/typed-media-attachment (new) |
| Medium | domain | Discard with retention and age-based cleanup | best-practices/model/soft-delete-active-flag.md (extend) |

---

## Open questions needing a developer's judgement

1. **Known-issue framing.** Validated platform bugs (`catalog-update-report.md`
   §3.1 — `KeycloakLoginInterceptor` realm cache, `DefaultLiquibaseExecutor`
   swallowed exceptions, `PathInfoRealmExtractor` boundary, Playwright
   `retries: 4`): a short "known issue" note in agent-docs *and* a linked
   judo-ng issue, or issue-tracker only? (Review leaned: do both.)
2. **Scope confirmation.** Keep JSL and Flutter out, Spring Boot in?

## Parallel model edits: one writer per file, join with CLI merge (2026-11-09)

Operator rule: a model file is never edited by two sessions at once, and never by hand. Parallel model work runs in separate worktrees (or separate copies from the same base) and is joined with `judo-cli merge <theirs> --base <base>`.

Verified with the pinned CLI: two copies from the same base, each adding its own package, merge with 0 conflicts; without `--base` the shared parent package is reported as an add-add conflict with fix commands. Recorded in `catalog/agent-docs/model/judo-cli.md` (rules 4 and 5) and `skills/judo-model-mermaid/references/fragments.md`.
