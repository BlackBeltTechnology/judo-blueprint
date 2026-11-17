# backend.md — index

Pull-only condensed map. Source: catalog/model-blueprints/testkit-integration-foundation/backend.md.

## Backend guidance
- Project practice on top of the platform testkit; `Calls`, `Seed`, `Roles`, `FoundationModule` are example project code, not platform API.
- Covers: eight support classes, activation-flag protocol, three coverage-grid templates, two docker overlay templates, ten gotchas, verbatim appendix.
- Maven setup (`pom.xml`, surefire/failsafe, `-Pdocker`) lives in model.md.

## The eight support classes (`testkit/support/`)
- `TestContext`: thin facade over `JudoRuntimeFixture`; captures `testStart`. Reusable verbatim.
- `Roles`: `JudoPrincipal` factory matching seeded `User` rows (`admin()`, `operatorOf(...)`, `operatorWithoutPartner(...)`). Template.
- `Seed`: fluent fixture builders + `minimalWorld()` aggregate. Template (every builder is project-specific).
- `Calls`: dispatcher helper (`list/get/create/update/delete`, `callStatic`, `callBoundUnexposed`, `preloadActor`). Reusable verbatim.
- `AuditAssertions`: window-based `[testStart, now]` audit asserts. Template (`AuditEntry`/`AuditEntryDao`).
- `FieldInjector`: reflective injector for OSGi `@Reference volatile` fields. Reusable verbatim.
- `FoundationModule`: Guice module, DAO bindings via `ReferenceInjector` + 4 registrars. Template (every `@Provides`).
- `SdkFunctionRegistry`: mutable `DispatcherFunctionProvider` for custom-op exchange functions. Reusable verbatim.

## Per-IT class shape
- `@JudoTest(modelName = "<app>", dialect = "hsqldb", transaction = TransactionHandling.AUTO_ROLLBACK, modules = { FoundationModule.class })` at class level.
- `@BeforeAll static void enableTestkit()` calls the four `FoundationModule.enable*()` flags as needed.
- Test methods take `JudoRuntimeFixture fixture`, build `TestContext.from(fixture)`, call `Seed.minimalWorld(ctx)`, then `Calls.list(ctx, "<app>.actors.<Actor>#_listFoos", Roles.admin())`.
- Gotcha: `@JudoTest` MUST be class-level; meta-annotation indirection gives NPE (fixture parameter `null`).

## The activation-flag protocol
- Four static flags on `FoundationModule`, set only in `@BeforeAll` (static init on the module is too late).
- `enableActorResolution()`: sets `setActorResolverCheckMappedActors(true)`; needed by every IT using a `JudoPrincipal`.
- `enableSdkFunctions()`: populates `getSdkFunctions()` via `SdkFunctionRegistrar`; custom-op ITs (`operations/`).
- `enableOperationInterceptors()`: adds production `OperationCallInterceptor` to the mutable list; derived-attribute ITs (`derived/`).
- `enableAuthInterceptors()`: adds production `AuthenticationInterceptor` to the auth chain; Layer-2 JWT overlay only.
- Why registrars exist: see G3.

## Coverage-grid templates

### Access-link role × ownership matrix
- Walk a 3×6 grid per `Access` link: admin / scoped-operator / orphan-operator × list / get-own / get-other / create / update-own / update-other.
- `[bypass note]` marks cells where JUDO does not re-check scope: `_refreshInstance` and `_updateInstance` use the signed identifier and do not re-evaluate `getterExpression`. Flagged "verify" against runtime version.
- Scope enforcement is on LIST (out-of-scope rows are filtered, so no signed id is issued).
- Write side: UPDATE predicate must hold after update; filter attributes are read-only through the filtered path. Both rules apply; see the membership invariant best practice.
- Operation FQN patterns: `<app>.actors.<Actor>#_list<LinkName>`, `#_createInstance<LinkName>`, `<app>.services.<TO>#_refreshInstance<App>_services_<TO>`, `#_updateInstance<App>_services_<TO>`.

### Custom-operation smoke pattern
- Per custom op assert: return format or regex, audit row with correct actor, idempotence or monotonicity where it applies.
- Dispatch table: static (`callStatic`, `__exposed=false`, `__principal`, optional `input`); instance-bound exposed (`update/get/...`, `__exposed=true`, `__signedIdentifier`); instance-bound internal (`callBoundUnexposed`, `__exposed=false`, `__identifier`, `__entityType`, `__this`).
- Gotcha: `DefaultDispatcher.callOperation` runs `authorizeOperation` only when `__exposed=true`. Static ops use `__exposed=false` so the actor resolver still populates `USER`-scope claims read by `AuditService.resolveActor()`, while the access gate is skipped.

### Audit-window assertion
- `TestContext.from(fixture)` once per test method; `testStart` captured at construction.
- `AuditAssertions.assertEmitted(ctx, action)` checks row `at` within `[testStart, Instant.now()]`.
- Never assert exact timestamps; `Clock` injection was deliberately not done (would touch production `AuditService`).

## Docker overlay templates

### `BaseDockerIT` (image-presence policy)
- `@Tag("docker")` abstract base; `requireImage(imageRef)` uses `inspectImageCmd`, catches `NotFoundException`.
- Missing image: if env `REQUIRE_DOCKER_IMAGES=1` throw `IllegalStateException`; otherwise `assumeTrue(false, msg)` (skip).
- Other testcontainers errors (daemon unreachable) propagate, so misconfiguration does not silently skip.

### `Layer1DockerModule` (real document-converter)
- Extends `FoundationModule` to inherit bindings; swap driven by static flag via `FoundationModule.configureDockerDocumentConverter(endpoint, apiKey)`.
- Do not override `@Provides` in a subclass: Guice `ProviderMethodScanner` raises `DUPLICATE_BINDING`.

### `Layer2KeycloakModule` (real JWT)
- Same extension pattern; helpers `mintToken(KeycloakContainer, user, pw, roles)` and `principalFromToken(jwt, actorFqn)`.
- `principalFromToken` decodes the payload without signature verification (trusts the local Keycloak); claims map to the same shape as `Roles.admin()`.

## Gotchas (the hard-won knowledge)
- G1: `JudoTestExtension` uses non-recursive `Class.getAnnotation(JudoTest.class)`; meta-annotations yield NPE.
- G2: `enableActorResolution()` must run before injector creation (fixture reads the flag in `prepare() → initModules()`). Without it `getVariable('ACTOR', 'isAdmin')` is `null` → `WHERE C_USER_NAME = NULL`; HSQLDB rejects in strict mode.
- G3: Lombok dual-cased fields in `JudoDefaultModuleBuilder`; setters on `DEFAULT` for `dispatcherFunctionProvider`, `operationCallInterceptorProvider`, `authenticationInterceptorProvider` do not propagate. Workaround: `*Registrar` eager singletons reach into closure-captured mutable collections via reflection.
- G4: `DefaultActorResolver.getActorByClaims` returns claim-only payload (`userName`, `email`); `isAdmin`/`isActive` missing. Workaround `Calls.preloadActor` puts full payload into `ACTOR_KEY`. Skip preload when `isActive=false` so the actor's `isActiveExpression` still applies.
- G5: `ReferenceInjector` walks `setXxx(T)` only; `@Reference volatile` fields stay null. `FieldInjector.inject` throws on missing field name or static field.
- G6: `signedIdentifier` (`IdentifierSigner.SIGNED_IDENTIFIER_KEY`) is the only valid input to refresh/update/delete. It changes after every update; re-read from latest response via `Calls.signedIdentifierOf(payload)`. Test code cannot mint it.
- G7: `@JudoTest(transaction = TransactionHandling.AUTO_ROLLBACK)` rolls back each test; no `@AfterEach` cleanup; sequence values reset too.
- G8: Keep both `@Tag("docker")` and path exclusion `**/testkit/docker/**`; either alone leaks.
- G9: `*ForCreate` takes inline payload (containment) or identifier-only payload (association). Use `*ForCreate.from(Map)` with `__identifier`, `__entityType`, `__version`. Transfer-object relations are usually `AGGREGATION` (reference); `from(Map)` still creates (verify).
- G10: `PayloadValidator` runs before DAO auto-populates the parent back-reference; seed children through identifier-only parent reference.

## A. `TestContext.java` (paste verbatim)
- `public final class TestContext`; `from(JudoRuntimeFixture)`; accessors `fixture()`, `injector()`, `dispatcher()`, `get(Class<T>)`, `testStart()`.

## B. `Roles.java` (template — replace actor FQN, claim shape)
- Constants: `ADMIN_USERNAME`, `OPERATOR_USERNAME`, emails on a test host, `ACTOR_FQN = "<app>.actors.<Actor>"`.
- Factories: `admin()`, `operatorOf(partnerCode)`, `operatorWithoutPartner(userName)`; private `claimMap(...)`.

## C. `Calls.java` (paste verbatim — replace `User`/`UserDao` import + `<app>` references in javadoc)
- Operation helpers: `list`, `create`, `get`, `update`, `delete`; `signedIdentifierOf(payload)`.
- Static and bound-unexposed: `callStatic(...)`, `callBoundUnexposed(...)`; private `baseExchange(p)`.
- `preloadActor(ctx, exchange, principal)`: see G4; respects an existing `ACTOR_KEY`.

## D. `FieldInjector.java` (paste verbatim, project-agnostic)
- `inject(target, Map<String,Object> fields)`: walks class hierarchy, `setAccessible(true)`, writes via reflection.
- Throws on missing field name (typo) and on static fields.

## E. `AuditAssertions.java` (template — replace `AuditEntry` / `AuditEntryDao`)
- `assertEmitted(ctx, action)` returns row; `assertNotEmitted(ctx, action)`; `assertEmittedBy(ctx, action, expectedActor)`.
- Private `assertWithinWindow(row, start, end, action)` and `toInstant(LocalDateTime)`.

## F. `FoundationModule.java` (skeleton; full file is ~900 LoC, mostly project-specific `@Provides`)
- `public class FoundationModule extends AbstractModule`; four static enable flags; `configureDockerDocumentConverter(endpoint, apiKey)`.
- Static volatile flags: `sdkFunctionsEnabled`, `operationInterceptorsEnabled`, `authInterceptorsEnabled`, docker endpoint and API key.
- `configure()` binds registrars: `ActorVariableRegistrar`, `AuthenticationInterceptorRegistrar`, `OperationCallInterceptorRegistrar`, `SdkFunctionRegistrar`.
- Stub `TokenIssuer` and `TokenValidator` (private static classes).

## G. `SdkFunctionRegistry.java` (paste verbatim — needed only when `enableSdkFunctions()` is used)
- Implements `DispatcherFunctionProvider`; `getSdkFunctions()`, `getScriptFunctions()`, `register(EOperation, Function<Payload,Payload>)`, `reset()`.

## H. `Seed.java` (skeleton — fluent builders + identifier-only payload helper)
- Builders: `insertAdminUser`, `insertPartner(ctx, code, name)`; aggregate `minimalWorld(ctx)` returns `World` record (two partners, admin and operator users).
- `identifierMap(id, entityType, version)` builds the identifier-only payload (G9).

## I. `BaseDockerIT.java` (paste verbatim — testcontainers + docker-java only)
- Abstract `@Tag("docker")` class; `REQUIRE_DOCKER_IMAGES_ENV`; `requireImage(imageRef)`. Policy as in the Docker overlay section.

## J. `Layer2KeycloakModule.java` JWT helpers (paste verbatim — replace REALM / CLIENT_ID / role names)
- `mintToken(KeycloakContainer, user, pw, roles)` and `principalFromToken(jwt, actorFqn)`; replace realm, client ID and role names.

## K. Sample IT class shapes
- Access-link matrix: `FoosAccessIT` with `OP_LIST`, `OP_CREATE`, `OP_GET`, `OP_UPDATE` constants; tests `list_admin_sees_all`, `list_operator_sees_own`, `list_orphan_sees_empty`, `create_admin`, `update_own`, `update_other_denied`.
- Custom-operation smoke: `ReserveBarcodeIT`; static op `<app>.operations.StaticOperations#reserveBarcode`; regex format check; `admin_happy`.
- Layer-2 JWT round-trip: `KeycloakJwtToPrincipalIT extends BaseDockerIT`; Keycloak container; `admin_jwt_provisions_user`.
