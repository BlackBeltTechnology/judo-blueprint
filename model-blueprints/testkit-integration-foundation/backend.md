# Backend Test Code

This layer covers the Java side of the testkit foundation: the eight reusable support classes, the activation-flag protocol, three coverage-grid templates, two docker overlay templates, ten hard-won gotchas, and a verbatim source appendix.

For Maven setup (`pom.xml`, `surefire`/`failsafe`/`-Pdocker`, tooling), see [model.md](model.md).

## The eight support classes (`testkit/support/`)

```
TestContext           thin facade over JudoRuntimeFixture; captures testStart
Roles                 JudoPrincipal factory matching seeded User rows
Seed                  fluent fixture builders + minimalWorld() aggregate
Calls                 dispatcher helper (list/get/create/update/delete + static + bound-unexposed)
AuditAssertions       window-based [testStart, now] audit row asserts
FieldInjector         reflective injector for OSGi @Reference volatile fields
Layer0Module          Guice module: DAO bindings via ReferenceInjector + 4 registrars
SdkFunctionRegistry   mutable DispatcherFunctionProvider for custom-op exchange functions
```

| Class | Reusable | Replace |
|---|---|---|
| `TestContext` | ✅ paste verbatim | nothing |
| `Calls` | ✅ paste verbatim | only `User`/`UserDao` import + javadoc `<app>` references |
| `FieldInjector` | ✅ paste verbatim, project-agnostic | nothing |
| `AuditAssertions` | ✅ template | `AuditEntry`/`AuditEntryDao` imports |
| `SdkFunctionRegistry` | ✅ paste verbatim | nothing |
| `Roles` | ✅ template | actor FQN, claim shape, role names, email host |
| `Seed` | template | every fixture builder (project-specific entities) |
| `Layer0Module` | template | every `@Provides` (project-specific DAOs and services) |

## Per-IT class shape

```java
@JudoTest(
        modelName = "<app>",            // app_name from judo.properties
        dialect = "hsqldb",
        transaction = TransactionHandling.AUTO_ROLLBACK,
        modules = { Layer0Module.class })
class MyAccessIT {

    @BeforeAll
    static void enableTestkit() {
        Layer0Module.enableActorResolution();        // always
        Layer0Module.enableSdkFunctions();           // operations/ ITs only
        Layer0Module.enableOperationInterceptors();  // derived/ ITs only
        Layer0Module.enableAuthInterceptors();       // Layer-2 docker overlay only
    }

    @Test
    void list_as_admin(JudoRuntimeFixture fixture) {
        TestContext ctx = TestContext.from(fixture);
        Seed.minimalWorld(ctx);

        List<Map<String, Object>> rows = Calls.list(ctx,
                "<app>.actors.<Actor>#_listFoos", Roles.admin());
        // assert ...
    }
}
```

**`@JudoTest` MUST be class-level**, not via meta-annotation. `JudoTestExtension` reads it through `Class.getAnnotation(JudoTest.class)`, which does not walk meta-annotations — a `@MyAppTest → @JudoTest` indirection silently produces NPEs because the extension never finds `@JudoTest` and the fixture parameter resolves to `null`.

## The activation-flag protocol

Four global flags on `Layer0Module` are flipped from each IT class's `@BeforeAll`. They MUST run before the testkit's `JudoTestExtension.beforeEach` builds the injector — `@BeforeAll` is the only safe site (a static initializer on the module class fires too late because `@JudoTest(modules = Layer0Module.class)` resolves the class object without triggering static init).

| Flag | Purpose | Required by |
|---|---|---|
| `enableActorResolution()` | sets `JudoDefaultModuleConfiguration.DEFAULT.setActorResolverCheckMappedActors(true)` so JQL `getVariable('ACTOR', ...)` resolves | every IT that uses a `JudoPrincipal` |
| `enableSdkFunctions()` | populates `DispatcherFunctionProvider.getSdkFunctions()` via the `SdkFunctionRegistrar` eager singleton | custom-op ITs (operations/) |
| `enableOperationInterceptors()` | adds production `OperationCallInterceptor` instances to the dispatcher's mutable list | derived-attribute ITs (derived/) |
| `enableAuthInterceptors()` | adds production `AuthenticationInterceptor` to the dispatcher's auth chain | Layer-2 JWT overlay only |

See [Gotcha G3 — Lombok dual-cased fields](#g3-lombok-dual-cased-fields-in-judodefaultmodulebuilder) for *why* the natural-looking `DEFAULT.setDispatcherFunctionProvider(...)` does not work and the registrars reach into bound-provider closures via reflection instead.

## Coverage-grid templates

### Access-link role × ownership matrix

For every `Access` link on the actor, walk this 3×6 grid (admin / scoped-operator / orphan-operator × list / get-own / get-other / create / update-own / update-other):

```
                       admin            operator(P1)            operator(none)
  list                 sees P1 + P2     sees only P1            empty
  get(own=P1)          ok               ok                      [bypass note]
  get(other=P2)        ok               [bypass note]           [bypass note]
  create               ok               ok (link allows)        — (no scope)
  update(own=P1)       ok               ok                      [bypass note]
  update(other=P2)     ok               [bypass note]           [bypass note]
```

**`[bypass note]`**: JUDO `_refreshInstance` and `_updateInstance` dereference a tamper-proof signed identifier and do **not** re-evaluate the link's `getterExpression`. Cross-scope enforcement lives on `LIST` (filters the row out, so an out-of-scope operator never obtains the signed id). The matrix asserts actual JUDO behaviour and pins the LIST guarantee.

**Pair this read-side rule with the write-side membership invariant.** Read-side scope = LIST issuance (pre-update scope NOT re-evaluated). Write-side membership = UPDATE predicate satisfaction (post-update state MUST satisfy the filter; filter attributes are read-only through the filtered path). Orthogonal rules — both apply on the same derived relation / access. See [derived-relation-membership-invariant.md](../../best-practices/model/derived-relation-membership-invariant.md).

Operation FQNs follow the generated REST resource:
```
<app>.actors.<Actor>#_list<LinkName>
<app>.actors.<Actor>#_createInstance<LinkName>
<app>.services.<TO>#_refreshInstance<App>_services_<TO>
<app>.services.<TO>#_updateInstance<App>_services_<TO>
```

### Custom-operation smoke pattern

Per custom op, assert: format / regex of return value, audit row emitted with correct actor, and (where applicable) idempotence / monotonicity. Dispatch via:

| Op shape | `Calls` helper | Required exchange keys |
|---|---|---|
| Static (unbound, declared `scope: static`) | `callStatic(ctx, op, principal, input)` | `__exposed=false` (default), `__principal`, optional `input` |
| Instance-bound + exposed by actor (default CRUD path) | `update/get/...` | `__exposed=true`, `__principal`, `__signedIdentifier`, optional `input` |
| Instance-bound but invoked internally | `callBoundUnexposed(ctx, op, principal, id, entityType, thisMap, input)` | `__exposed=false`, `__identifier`, `__entityType`, `__this`, optional `input` |

**Why `__exposed=false` for static ops**: static-scope ops carry no `exposedBy` annotation. `DefaultDispatcher.callOperation` only runs `accessManager.authorizeOperation` when `__exposed=true`. With `__exposed=false` the actor-resolver still runs (so a non-null principal populates `USER`-scope claims read by `AuditService.resolveActor()`) but the access gate is skipped. This mirrors production internal-call semantics — these ops are only ever invoked through the generated SDK wrapper from inside other custom operations, never from REST.

### Audit-window assertion

Every IT class instantiates `TestContext.from(fixture)` *once per test method*. `testStart` is captured at construction. `AuditAssertions.assertEmitted(ctx, action)` then queries `AuditEntryDao` and asserts the row's `at` timestamp lies within `[testStart, Instant.now()]`. Tests MUST NOT assert exact timestamps — wall-clock equality is brittle and `Clock` injection was deliberately punted (would require touching production `AuditService`).

## Docker overlay templates

### `BaseDockerIT` (image-presence policy)

```java
@Tag("docker")
public abstract class BaseDockerIT {
    public static final String REQUIRE_DOCKER_IMAGES_ENV = "REQUIRE_DOCKER_IMAGES";

    protected static void requireImage(String imageRef) {
        boolean present;
        try {
            DockerClientFactory.lazyClient().inspectImageCmd(imageRef).exec();
            present = true;
        } catch (NotFoundException e) {
            present = false;
        }
        if (present) return;
        String msg = "Required docker image not found: '" + imageRef + "'.";
        if ("1".equals(System.getenv(REQUIRE_DOCKER_IMAGES_ENV))) {
            throw new IllegalStateException("[" + REQUIRE_DOCKER_IMAGES_ENV + "=1] " + msg);
        }
        assumeTrue(false, msg);  // local default: skip cleanly
    }
}
```

CI sets `REQUIRE_DOCKER_IMAGES=1` to flip "skip with `assumeTrue`" to fail-fast. Other testcontainers exceptions (e.g. "daemon not reachable") propagate unchanged so host-level misconfiguration surfaces, not silently skips.

### `Layer1DockerModule` (real document-converter)

Extends `Layer0Module` purely to inherit every binding. The external-service swap is driven by a **static flag on `Layer0Module`** and consumed by the `@Provides DocumentConverterClient` method. Subclass-overriding `@Provides` is not safe — Guice's `ProviderMethodScanner` registers both parent and child bindings for the same key and fails with `DUPLICATE_BINDING`.

```java
public class Layer1DockerModule extends Layer0Module {
    public static void configure(String endpoint, String apiKey) {
        Layer0Module.configureDockerDocumentConverter(endpoint, apiKey);
    }
}
```

### `Layer2KeycloakModule` (real JWT)

Same extension pattern. Adds two static helpers (full source in [Appendix J](#j-layer2keycloakmodulejava-jwt-helpers-paste-verbatim--replace-realm--client_id--role-names)):

```java
public static String mintToken(KeycloakContainer kc, String user, String pw, List<String> roles)  { ... }
public static JudoPrincipal principalFromToken(String jwt, String actorFqn)                       { ... }
```

`principalFromToken` decodes the JWT payload (signature verification deliberately skipped — at Layer-2 we trust the local Keycloak we just talked to) and projects claims into the same attribute-map shape `Roles.admin()` produces, so the actor lookup and JQL filters resolve identically against hand-built and JWT-derived principals.

## Gotchas (the hard-won knowledge)

These are testkit-vs-runtime gaps every JUDO project hits. Each line below cost the framework a debugging session.

### G1. `@JudoTest` must be class-level, not meta-annotation

`JudoTestExtension` reads via `Class.getAnnotation(JudoTest.class)`, which is non-recursive (does not walk meta-annotations) and the testkit doesn't use JUnit's `AnnotationSupport.findAnnotation`. A `@MyAppTest → @JudoTest` indirection produces NPEs because the extension never finds `@JudoTest`, and the fixture parameter resolves to `null`.

### G2. `enableActorResolution()` MUST run before injector creation

`JudoRuntimeFixture` captures `JudoDefaultModuleConfiguration.DEFAULT.getActorResolverCheckMappedActors()` during `prepare() → initModules()`, which fires *before* `JudoTestExtension` instantiates user-supplied modules. A static initializer on the module class fires too late because `@JudoTest(modules = Layer0Module.class)` resolves the class object without forcing static init. **Only `@BeforeAll` works.**

Without this flag, `getVariable('ACTOR', 'isAdmin')` evaluates to `null`, generating SQL `WHERE C_USER_NAME = NULL` which HSQLDB rejects under strict mode and which would silently match no rows under Postgres.

### G3. Lombok dual-cased fields in `JudoDefaultModuleBuilder`

The builder generated by Lombok has two fields whose names differ only in case (e.g. `dispatcherFunctionProvider` vs `DispatcherFunctionProvider`). The constructor copies `DEFAULT` into the upper-cased field that `build()` never reads; the lower-cased field consumed by `build()` is only ever populated by an explicit setter call which `JudoRuntimeFixture` never invokes.

**Consequence**: setters on `JudoDefaultModuleConfiguration.DEFAULT` for `dispatcherFunctionProvider`, `operationCallInterceptorProvider`, and `authenticationInterceptorProvider` do **not** propagate to the dispatcher.

**Workaround**: each `*Registrar` eager singleton in `Layer0Module` injects the bound provider Guice produces and reaches into its closure-captured mutable list/map (the testkit's default providers are anonymous inner classes that close over local `ArrayList`/`HashMap`), populating it after injector construction. The dispatcher re-reads the collection on every call so late population is safe.

### G4. `DefaultActorResolver` returns claim-only payloads under the testkit

`DefaultActorResolver.getActorByClaims` calls `dao.search(actorType, ...)` with no mask. Under the Guice testkit the resulting `Payload` contains only the claim attributes (`userName`, `email`) plus entity metadata. Mapped non-claim attributes such as `isAdmin` and `isActive` are not included, so JQL filters `getVariable('ACTOR', 'isAdmin')` resolve to `null` → `WHERE ((NULL OR …))` → HSQLDB strict-mode rejection.

**Workaround**: `Calls.preloadActor(ctx, exchange, principal)` queries `UserDao` for the row matching the principal's `userName` claim and threads its full payload into `exchange.put(Dispatcher.ACTOR_KEY, ...)`. `DefaultDispatcher.callOperation` respects an already-present `ACTOR_KEY` entry and skips its own resolution call.

**Important nuance**: the helper skips preload when the matched user has `isActive=false` so the dispatcher's own resolver runs and applies the actor's `isActiveExpression`. Unconditional preload would let inactive users pass the access filter.

### G5. `@Reference volatile` fields not walked by `ReferenceInjector`

JUDO's `ReferenceInjector` (testkit util) walks setter-style methods of the form `setXxx(T)`. Production custom ops, services, and interceptors declare collaborators via `@Reference volatile` *fields* (the OSGi DS field-injection convention) — these are silently left null.

**Workaround**: `FieldInjector.inject(target, Map.of("fieldName", dep, ...))` walks the class hierarchy, sets `setAccessible(true)`, writes via reflection. Throws on missing field name (typo) or static field (cannot be a DS reference).

### G6. `signedIdentifier` is the only valid input to refresh / update / delete

Every `Calls.list(...)` and `Calls.create(...)` response payload carries a tamper-proof signed identifier under `IdentifierSigner.SIGNED_IDENTIFIER_KEY`. Pass it via `exchange.put(SIGNED_IDENTIFIER_KEY, ...)` for subsequent `_refreshInstance` / `_updateInstance` / `_deleteInstance` calls. Use `Calls.signedIdentifierOf(payload)` to extract it.

### G7. `AUTO_ROLLBACK` keeps tests isolated without explicit cleanup

`@JudoTest(transaction = TransactionHandling.AUTO_ROLLBACK)` rolls back each test method's writes. No `@AfterEach` cleanup needed; even sequence-allocated values (e.g. barcode counters) reset.

### G8. Belt-and-braces docker exclusion

`@Tag("docker")` and the path-based `<excludes>**/testkit/docker/**</excludes>` are both needed. A tag-less docker IT (e.g. an oversight) and a `@Tag("docker")` IT outside `testkit/docker/` are both possible; either exclusion alone has been observed to leak.

### G9. Identifier-only payloads vs containment payloads

JUDO `*ForCreate` types accept either an inline payload (creates a new related row — containment) or an identifier-only payload (references an existing row — association). The builder API doesn't expose the identifier shape; use `*ForCreate.from(Map)` with:

```java
Map<String, Object> identifierMap(Serializable id, String entityType, Integer version) {
    Map<String, Object> m = new HashMap<>();
    m.put("__identifier", id);
    m.put("__entityType", entityType);
    m.put("__version", version);
    return m;
}
```

For mandatory AGGREGATION (containment) relations, embed a fresh `*ForCreate.builder()` payload — `from(Map)` would still create rather than reference.

### G10. `PayloadValidator` runs before parent-link auto-population

For composition rows, the framework's `PayloadValidator` runs before the DAO auto-populates the parent back-reference. Seeding via `parentDao.createChildren(parent, child)` requires threading the parent through the child's `from(Map)` factory as an identifier-only reference — the builder API doesn't expose the back-ref because it's the parent's containment.

---

# Appendix — Verbatim Source

The four small reusable utilities below paste in essentially as-is. Replace `compsychletter` / `hu.blackbelt.compsych.letter` / `LetterUser` / `User` / `UserDao` with the local app name, package, actor type, and user entity.

The two large project-specific files (`Layer0Module`, `Seed`, `SdkFunctionRegistry`) are skeletal — reproduce their *structure* (the registrar pattern, the DAO `@Provides` pattern, the fluent fixture builders) but every method body is project-specific. See the framework source at `compsych-letter-framework/application/integration-test/src/test/java/hu/blackbelt/compsych/letter/integration/testkit/support/` for the full implementations.

## A. `TestContext.java` (paste verbatim)

```java
package <pkg>.integration.testkit.support;

import com.google.inject.Injector;
import hu.blackbelt.judo.dispatcher.api.Dispatcher;
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoRuntimeFixture;

import java.time.Instant;

/**
 * Convenience wrapper over a JudoRuntimeFixture. Constructed once per
 * test method via {@link #from(JudoRuntimeFixture)}. {@code testStart}
 * is captured at construction so audit-row assertions can use the
 * [testStart, testEnd] window pattern.
 */
public final class TestContext {

    private final JudoRuntimeFixture fixture;
    private final Instant testStart;

    private TestContext(JudoRuntimeFixture fixture) {
        this.fixture = fixture;
        this.testStart = Instant.now();
    }

    public static TestContext from(JudoRuntimeFixture fixture) {
        return new TestContext(fixture);
    }

    public JudoRuntimeFixture fixture()  { return fixture; }
    public Injector injector()           { return fixture.getInjector(); }
    public Dispatcher dispatcher()       { return fixture.getInjector().getInstance(Dispatcher.class); }
    public <T> T get(Class<T> type)      { return fixture.getInjector().getInstance(type); }
    public Instant testStart()           { return testStart; }
}
```

## B. `Roles.java` (template — replace actor FQN, claim shape)

```java
package <pkg>.integration.testkit.support;

import hu.blackbelt.judo.dispatcher.api.JudoPrincipal;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class Roles {

    public static final String ADMIN_USERNAME    = "alice";
    public static final String ADMIN_EMAIL       = "alice@<host>.test";
    public static final String OPERATOR_USERNAME = "bob";
    public static final String OPERATOR_EMAIL    = "bob@<host>.test";

    /** Actor FQN — set on JudoPrincipal.client; matched by AccessManager
     *  against the operation's @exposedBy annotation. */
    public static final String ACTOR_FQN = "<app>.actors.<Actor>";

    private Roles() {}

    public static JudoPrincipal admin() {
        return JudoPrincipal.builder()
                .name(ADMIN_USERNAME).realm("<app>").client(ACTOR_FQN)
                .attributes(claimMap(ADMIN_USERNAME, ADMIN_EMAIL, "Alice", "Admin", true,
                        List.of("<admin-role>")))
                .build();
    }

    public static JudoPrincipal operatorOf(String partnerCode) {
        // partnerCode informational; scope resolved via User.partners on the seeded User row.
        return JudoPrincipal.builder()
                .name(OPERATOR_USERNAME).realm("<app>").client(ACTOR_FQN)
                .attributes(claimMap(OPERATOR_USERNAME, OPERATOR_EMAIL, "Bob", "Operator", false,
                        List.of()))
                .build();
    }

    public static JudoPrincipal operatorWithoutPartner(String userName) {
        return JudoPrincipal.builder()
                .name(userName).realm("<app>").client(ACTOR_FQN)
                .attributes(claimMap(userName, userName + "@<host>.test",
                        "Orphan", "Operator", false, List.of()))
                .build();
    }

    private static Map<String, Object> claimMap(String userName, String email,
                                                String givenName, String familyName,
                                                boolean isAdmin, List<String> realmRoles) {
        Map<String, Object> attrs = new LinkedHashMap<>();
        // Actor-claim attribute names — must match UserTO field names.
        attrs.put("userName", userName);
        attrs.put("email",    email);
        // JWT-shape claims (mirrored so Layer-0 + Layer-2 principals round-trip identically).
        attrs.put("preferred_username", userName);
        attrs.put("given_name",         givenName);
        attrs.put("family_name",        familyName);
        attrs.put("realm_access",       Map.of("roles", realmRoles));
        // Transient claim consumed by JQL getVariable('ACTOR', 'isAdmin').
        attrs.put("isAdmin", isAdmin);
        return attrs;
    }
}
```

## C. `Calls.java` (paste verbatim — replace `User`/`UserDao` import + `<app>` references in javadoc)

```java
package <pkg>.integration.testkit.support;

import <pkg>.<app>.api.<app>._default_transferobjecttypes.entities.user.User;
import <pkg>.<app>.api.<app>._default_transferobjecttypes.entities.user.UserDao;
import hu.blackbelt.judo.dao.api.Payload;
import hu.blackbelt.judo.dispatcher.api.Dispatcher;
import hu.blackbelt.judo.dispatcher.api.JudoPrincipal;
import hu.blackbelt.judo.runtime.core.dispatcher.security.IdentifierSigner;
import hu.blackbelt.judo.sdk.query.StringFilter;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

public final class Calls {

    private Calls() {}

    @SuppressWarnings("unchecked")
    public static List<Map<String, Object>> list(TestContext ctx, String op, JudoPrincipal p) {
        Map<String, Object> ex = baseExchange(p);
        preloadActor(ctx, ex, p);
        Map<String, Object> out = ctx.dispatcher().callOperation(op, ex);
        Object output = out == null ? null : out.get("output");
        return output instanceof List ? (List<Map<String, Object>>) output : List.of();
    }

    @SuppressWarnings("unchecked")
    public static Map<String, Object> create(TestContext ctx, String op, JudoPrincipal p, Map<String, Object> input) {
        Map<String, Object> ex = baseExchange(p);
        preloadActor(ctx, ex, p);
        ex.put("input", input);
        Map<String, Object> out = ctx.dispatcher().callOperation(op, ex);
        return out == null ? Map.of() : (Map<String, Object>) out.getOrDefault("output", Map.of());
    }

    @SuppressWarnings("unchecked")
    public static Map<String, Object> get(TestContext ctx, String op, JudoPrincipal p, Object signedId) {
        Map<String, Object> ex = baseExchange(p);
        preloadActor(ctx, ex, p);
        ex.put(IdentifierSigner.SIGNED_IDENTIFIER_KEY, signedId);
        Map<String, Object> out = ctx.dispatcher().callOperation(op, ex);
        return out == null ? Map.of() : (Map<String, Object>) out.getOrDefault("output", Map.of());
    }

    @SuppressWarnings("unchecked")
    public static Map<String, Object> update(TestContext ctx, String op, JudoPrincipal p,
                                             Object signedId, Map<String, Object> input) {
        Map<String, Object> ex = baseExchange(p);
        preloadActor(ctx, ex, p);
        ex.put(IdentifierSigner.SIGNED_IDENTIFIER_KEY, signedId);
        ex.put("input", input);
        Map<String, Object> out = ctx.dispatcher().callOperation(op, ex);
        return out == null ? Map.of() : (Map<String, Object>) out.getOrDefault("output", Map.of());
    }

    public static void delete(TestContext ctx, String op, JudoPrincipal p, Object signedId) {
        Map<String, Object> ex = baseExchange(p);
        preloadActor(ctx, ex, p);
        ex.put(IdentifierSigner.SIGNED_IDENTIFIER_KEY, signedId);
        ctx.dispatcher().callOperation(op, ex);
    }

    public static Object signedIdentifierOf(Map<String, Object> payload) {
        return payload.get(IdentifierSigner.SIGNED_IDENTIFIER_KEY);
    }

    /**
     * Static (unbound) operation. {@code __exposed} deliberately defaulted
     * to false: skips access-manager but still threads the principal so
     * AuditService.resolveActor() reads USER claims. Mirrors the
     * generated SDK-wrapper internal-call semantics.
     */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> callStatic(TestContext ctx, String op,
                                                 JudoPrincipal p, Map<String, Object> input) {
        Map<String, Object> ex = new HashMap<>();
        if (p != null) ex.put(Dispatcher.PRINCIPAL_KEY, p);
        preloadActor(ctx, ex, p);
        if (input != null) ex.put("input", input);
        Map<String, Object> out = ctx.dispatcher().callOperation(op, ex);
        return out == null ? Map.of() : (Map<String, Object>) out.getOrDefault("output", Map.of());
    }

    /**
     * Instance-bound op invoked internally (skipping access manager).
     * Mirrors the shape generated *DispatcherWrapper helpers produce.
     */
    @SuppressWarnings("unchecked")
    public static Map<String, Object> callBoundUnexposed(TestContext ctx, String op, JudoPrincipal p,
                                                         Object identifier, String entityType,
                                                         Map<String, Object> thisPayload,
                                                         Map<String, Object> input) {
        Map<String, Object> ex = new HashMap<>();
        if (p != null) ex.put(Dispatcher.PRINCIPAL_KEY, p);
        preloadActor(ctx, ex, p);
        ex.put("__identifier", identifier);
        ex.put("__entityType", entityType);
        ex.put("__this",        thisPayload);
        if (input != null) ex.put("input", input);
        Map<String, Object> out = ctx.dispatcher().callOperation(op, ex);
        return out == null ? Map.of() : (Map<String, Object>) out.getOrDefault("output", Map.of());
    }

    private static Map<String, Object> baseExchange(JudoPrincipal p) {
        Map<String, Object> ex = new HashMap<>();
        ex.put("__exposed", Boolean.TRUE);
        if (p != null) ex.put(Dispatcher.PRINCIPAL_KEY, p);
        return ex;
    }

    /**
     * Stuff the principal's full User row payload into the exchange under
     * Dispatcher.ACTOR_KEY to short-circuit DefaultActorResolver's
     * claim-only payload (which trips JQL access filters). Skips the
     * preload when the user is inactive so the resolver runs its
     * isActiveExpression and produces production "deactivated user is
     * denied" semantics.
     */
    public static void preloadActor(TestContext ctx, Map<String, Object> exchange, JudoPrincipal p) {
        if (p == null) return;
        String userName = (String) p.getAttributes().get("userName");
        if (userName == null) return;
        Optional<User> match = ctx.get(UserDao.class).query()
                .filterByUserName(StringFilter.equalTo(userName))
                .selectOne();
        match.ifPresent(u -> {
            if (Boolean.FALSE.equals(u.getIsActive())) return;
            exchange.put(Dispatcher.ACTOR_KEY, Payload.asPayload(u.toMap()));
        });
    }
}
```

## D. `FieldInjector.java` (paste verbatim, project-agnostic)

```java
package <pkg>.integration.testkit.support;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.Map;

/**
 * Reflective field injector for OSGi DS components. Production code
 * declares collaborators via {@code @Reference volatile} fields, which
 * the testkit's setter-only ReferenceInjector silently leaves null.
 * This helper closes that gap.
 */
public final class FieldInjector {

    private FieldInjector() {}

    public static <T> T inject(T target, Map<String, Object> fields) {
        if (target == null) throw new IllegalArgumentException("target must not be null");
        for (Map.Entry<String, Object> e : fields.entrySet()) {
            Field f = findField(target.getClass(), e.getKey());
            if (f == null)
                throw new IllegalArgumentException("No field '" + e.getKey() + "' on " + target.getClass().getName());
            if (Modifier.isStatic(f.getModifiers()))
                throw new IllegalArgumentException("Field '" + e.getKey() + "' is static");
            try {
                f.setAccessible(true);
                f.set(target, e.getValue());
            } catch (IllegalAccessException ex) {
                throw new IllegalStateException("Cannot inject field '" + e.getKey() + "'", ex);
            }
        }
        return target;
    }

    private static Field findField(Class<?> cls, String name) {
        for (Class<?> c = cls; c != null && c != Object.class; c = c.getSuperclass()) {
            try { return c.getDeclaredField(name); } catch (NoSuchFieldException ignore) {}
        }
        return null;
    }
}
```

## E. `AuditAssertions.java` (template — replace `AuditEntry` / `AuditEntryDao`)

```java
package <pkg>.integration.testkit.support;

import <pkg>.<app>.api.<app>._default_transferobjecttypes.entities.auditentry.AuditEntry;
import <pkg>.<app>.api.<app>._default_transferobjecttypes.entities.auditentry.AuditEntryDao;
import hu.blackbelt.judo.sdk.query.StringFilter;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

public final class AuditAssertions {

    private AuditAssertions() {}

    public static AuditEntry assertEmitted(TestContext ctx, String action) {
        Instant testStart = ctx.testStart();
        Instant testEnd   = Instant.now();
        AuditEntryDao dao = ctx.get(AuditEntryDao.class);

        List<AuditEntry> matches = dao.query()
                .filterByAction(StringFilter.equalTo(action))
                .selectList();

        if (matches.isEmpty()) fail("No audit row for action '" + action + "'");
        AuditEntry row = matches.get(matches.size() - 1);
        assertWithinWindow(row, testStart, testEnd, action);
        return row;
    }

    public static void assertNotEmitted(TestContext ctx, String action) {
        AuditEntryDao dao = ctx.get(AuditEntryDao.class);
        Instant testStart = ctx.testStart();
        for (AuditEntry row : dao.query().filterByAction(StringFilter.equalTo(action)).selectList()) {
            Instant rowAt = toInstant(row.getAt());
            assertFalse(!rowAt.isBefore(testStart),
                    () -> "Unexpected audit row for action '" + action + "' inside test window: " + row);
        }
    }

    public static AuditEntry assertEmittedBy(TestContext ctx, String action, String expectedActor) {
        AuditEntry row = assertEmitted(ctx, action);
        if (!expectedActor.equals(row.getActorUsername()))
            fail("Expected actorUsername '" + expectedActor + "' but got '" + row.getActorUsername() + "'");
        return row;
    }

    private static void assertWithinWindow(AuditEntry row, Instant start, Instant end, String action) {
        Instant at = toInstant(row.getAt());
        assertTrue(!at.isBefore(start) && !at.isAfter(end),
                () -> "Audit row for '" + action + "' has at=" + at + " outside [" + start + ", " + end + "]");
    }

    private static Instant toInstant(LocalDateTime ldt) {
        return ldt == null ? Instant.EPOCH : ldt.toInstant(ZoneOffset.UTC);
    }
}
```

## F. `Layer0Module.java` (skeleton — full file is ~900 LoC, mostly project-specific `@Provides`)

```java
package <pkg>.integration.testkit.support;

import com.google.inject.AbstractModule;
import com.google.inject.Inject;
import com.google.inject.Injector;
import com.google.inject.Provides;
import com.google.inject.Singleton;
import hu.blackbelt.judo.dispatcher.api.Context;
import hu.blackbelt.judo.dispatcher.api.VariableResolver;
import hu.blackbelt.judo.runtime.core.dispatcher.OperationCallInterceptor;
import hu.blackbelt.judo.runtime.core.dispatcher.OperationCallInterceptorProvider;
import hu.blackbelt.judo.runtime.core.dispatcher.VariableResolverManager;
import hu.blackbelt.judo.runtime.core.dispatcher.environment.AccessTokenVariableProvider;
import hu.blackbelt.judo.runtime.core.dispatcher.environment.ActorVariableProvider;
import hu.blackbelt.judo.runtime.core.accessmanager.api.AuthenticationInterceptor;
import hu.blackbelt.judo.runtime.core.accessmanager.api.AuthenticationInterceptorProvider;
import hu.blackbelt.judo.runtime.core.guice.JudoDefaultModuleConfiguration;
import hu.blackbelt.judo.runtime.core.guice.testkit.util.ReferenceInjector;

import java.util.List;
import java.util.Map;

public class Layer0Module extends AbstractModule {

    // --- Activation flags (called from each IT's @BeforeAll) ---
    public static void enableActorResolution() {
        JudoDefaultModuleConfiguration.DEFAULT.setActorResolverCheckMappedActors(Boolean.TRUE);
    }
    public static void enableSdkFunctions()         { sdkFunctionsEnabled = true; }
    public static void enableOperationInterceptors(){ operationInterceptorsEnabled = true; }
    public static void enableAuthInterceptors()     { authInterceptorsEnabled = true; }

    // Static-flag pattern for docker overlay external-service swap.
    // Subclass-overriding @Provides is unsafe — Guice's ProviderMethodScanner
    // registers both parent and child bindings → DUPLICATE_BINDING.
    public static void configureDockerDocumentConverter(String endpoint, String apiKey) {
        dockerDocumentConverterEndpoint = endpoint;
        dockerDocumentConverterApiKey   = apiKey == null ? "" : apiKey;
    }

    private static volatile boolean sdkFunctionsEnabled         = false;
    private static volatile boolean operationInterceptorsEnabled = false;
    private static volatile boolean authInterceptorsEnabled      = false;
    private static volatile String  dockerDocumentConverterEndpoint;
    private static volatile String  dockerDocumentConverterApiKey = "";

    @Override
    protected void configure() {
        // Stub TokenIssuer / TokenValidator — see G* note on ResponseConverter.
        bind(TokenIssuer.class).toInstance(new StubTokenIssuer());
        bind(TokenValidator.class).toInstance(new StubTokenValidator());

        // Eager registrars — fire after Guice resolves them.
        bind(ActorVariableRegistrar.class).asEagerSingleton();
        bind(SdkFunctionRegistrar.class).asEagerSingleton();
        bind(AuthenticationInterceptorRegistrar.class).asEagerSingleton();
        bind(OperationCallInterceptorRegistrar.class).asEagerSingleton();
    }

    // --- Pattern 1: ACTOR + USER variable provider registration ---
    static class ActorVariableRegistrar {
        @Inject
        ActorVariableRegistrar(VariableResolver resolver, Context context) {
            VariableResolverManager mgr = (VariableResolverManager) resolver;
            mgr.registerFunction("ACTOR", new ActorVariableProvider(context),       false);
            mgr.registerFunction("USER",  new AccessTokenVariableProvider(context), false);
        }
    }

    // --- Pattern 2: AuthenticationInterceptor registrar (Layer-2 only) ---
    static class AuthenticationInterceptorRegistrar {
        @Inject
        AuthenticationInterceptorRegistrar(AuthenticationInterceptorProvider provider, UserDao userDao) {
            if (!authInterceptorsEnabled) return;
            var interceptors = provider.getAuthenticationInterceptors();
            if (!(interceptors instanceof List))
                throw new IllegalStateException("not a List — rebinding strategy needed");
            @SuppressWarnings("unchecked")
            List<AuthenticationInterceptor> list = (List<AuthenticationInterceptor>) interceptors;
            list.add(FieldInjector.inject(new <ProductionAuthInterceptor>(), Map.of("userDao", userDao)));
        }
    }

    // --- Pattern 3: OperationCallInterceptor registrar (derived/ ITs) ---
    static class OperationCallInterceptorRegistrar {
        @Inject
        OperationCallInterceptorRegistrar(OperationCallInterceptorProvider provider /*, deps*/) {
            if (!operationInterceptorsEnabled) return;
            var interceptors = provider.getCallOperationInterceptors();
            if (!(interceptors instanceof List))
                throw new IllegalStateException("not a List — rebinding strategy needed");
            @SuppressWarnings("unchecked")
            List<OperationCallInterceptor> list = (List<OperationCallInterceptor>) interceptors;
            // list.add(FieldInjector.inject(new <Production*Interceptor>(), Map.of(...)));
        }
    }

    // --- Pattern 4: SDK function registrar (operations/ ITs) ---
    static class SdkFunctionRegistrar {
        @Inject
        SdkFunctionRegistrar(Injector injector, AsmModel asmModel,
                             DispatcherFunctionProvider provider) {
            if (!sdkFunctionsEnabled) return;
            var sdkMap = provider.getSdkFunctions();
            if (sdkMap == null) throw new IllegalStateException("getSdkFunctions() == null");
            // mutability probe
            try { sdkMap.put(null, null); sdkMap.remove(null); }
            catch (UnsupportedOperationException u) {
                throw new IllegalStateException("immutable map; rebinding needed", u);
            }
            AsmUtils utils = new AsmUtils(asmModel.getResourceSet());
            // for each custom op:
            //   register(utils, sdkMap, "<app>.operations.<X>#<op>", () -> {
            //       var fn = new <Op>ExchangeFunctions();
            //       fn.bindOperation(injector.getInstance(<Op>CustomImplementation.class));
            //       return fn;
            //   });
        }

        private static void register(AsmUtils utils, Map<EOperation, Function<Payload, Payload>> map,
                                     String fqn, Supplier<Function<Payload, Payload>> fn) {
            utils.all(EOperation.class)
                 .filter(o -> fqn.equals(AsmUtils.getOperationFQName(o)))
                 .findFirst()
                 .ifPresent(op -> map.put(op, fn.get()));
        }
    }

    // --- DAO bindings: one @Provides per generated DAO via ReferenceInjector ---
    @Provides @Singleton
    UserDao provideUserDao(Injector injector) {
        return ReferenceInjector.createAndInject(UserDaoImpl.class, injector);
    }
    // Repeat for every DAO an IT needs (entity-side + service-side TO DAOs).

    // --- Service / custom-op @Provides via FieldInjector ---
    @Provides @Singleton
    AuditService provideAuditService(AuditEntryDao auditEntryDao, VariableResolver judoVariableResolver) {
        return FieldInjector.inject(new AuditService(), Map.of(
                "auditEntryDao", auditEntryDao,
                "judoVariableResolver", judoVariableResolver));
    }
    // Repeat for every custom-op impl + every production service the ops depend on.

    // --- External-service swap: stub default, real-via-static-flag for docker overlay ---
    @Provides @Singleton
    DocumentConverterClient provideDocumentConverterClient() {
        if (dockerDocumentConverterEndpoint != null) {
            // build real HTTP client against testcontainer
            ...
        }
        // wrap canned-bytes stub
        ...
    }

    // Stub Token{Issuer,Validator} so ResponseConverter can serialise FileType payloads.
    private static final class StubTokenIssuer    implements TokenIssuer    { ... }
    private static final class StubTokenValidator implements TokenValidator { ... }
}
```

## G. `SdkFunctionRegistry.java` (paste verbatim — needed only when `enableSdkFunctions()` is used)

```java
package <pkg>.integration.testkit.support;

import hu.blackbelt.judo.dao.api.Payload;
import hu.blackbelt.judo.runtime.core.dispatcher.DispatcherFunctionProvider;
import org.eclipse.emf.ecore.EOperation;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Function;

/**
 * Mutable DispatcherFunctionProvider populated by Layer0Module's
 * SdkFunctionRegistrar after the Guice injector is built.
 * The dispatcher reads getSdkFunctions() on every callOperation,
 * so late population is safe.
 */
public final class SdkFunctionRegistry implements DispatcherFunctionProvider {

    private final Map<EOperation, Function<Payload, Payload>> sdkFunctions    = new ConcurrentHashMap<>();
    private final Map<EOperation, Function<Payload, Payload>> scriptFunctions = new HashMap<>();

    @Override public Map<EOperation, Function<Payload, Payload>> getSdkFunctions()    { return sdkFunctions; }
    @Override public Map<EOperation, Function<Payload, Payload>> getScriptFunctions() { return scriptFunctions; }

    public void register(EOperation operation, Function<Payload, Payload> fn) { sdkFunctions.put(operation, fn); }
    public void reset() { sdkFunctions.clear(); }
}
```

## H. `Seed.java` (skeleton — fluent builders + identifier-only payload helper)

```java
package <pkg>.integration.testkit.support;

public final class Seed {

    private Seed() {}

    public static <UserEntity> insertAdminUser(TestContext ctx) {
        return ctx.get(<UserDao>.class).create(
                <UserForCreate>.builder()
                        .withUserName(Roles.ADMIN_USERNAME)
                        .withEmail(Roles.ADMIN_EMAIL)
                        .withIsAdmin(Boolean.TRUE)
                        .withIsActive(Boolean.TRUE)
                        .build());
    }

    public static <PartnerEntity> insertPartner(TestContext ctx, String code, String name) {
        // ... builder() ... .build();
        return ctx.get(<PartnerDao>.class).create(...);
    }

    /** Aggregate fixture used by access-link matrix ITs. Returned as a record
     *  so tests can refer to seeded rows by business key. */
    public static World minimalWorld(TestContext ctx) {
        var p1 = insertPartner(ctx, "ACME", "ACME Corp");
        var p2 = insertPartner(ctx, "INIT", "Init Inc");
        var admin    = insertAdminUser(ctx);
        var operator = insertOperatorUser(ctx);
        linkUserToPartner(ctx, operator, p1);
        return new World(p1, p2, admin, operator);
    }

    /** Identifier-only payload for *ForCreate.from(Map). Use for
     *  ASSOCIATION-style references; AGGREGATION embeds a fresh builder. */
    public static Map<String, Object> identifierMap(Serializable id, String entityType, Integer version) {
        Map<String, Object> m = new HashMap<>();
        m.put("__identifier", id);
        m.put("__entityType", entityType);
        m.put("__version",    version);
        return m;
    }

    public record World(<PartnerEntity> p1, <PartnerEntity> p2, <UserEntity> admin, <UserEntity> operator) {}
}
```

## I. `BaseDockerIT.java` (paste verbatim — testcontainers + docker-java only)

```java
package <pkg>.integration.testkit.docker;

import com.github.dockerjava.api.DockerClient;
import com.github.dockerjava.api.exception.NotFoundException;
import org.junit.jupiter.api.Tag;
import org.testcontainers.DockerClientFactory;

import static org.junit.jupiter.api.Assumptions.assumeTrue;

@Tag("docker")
public abstract class BaseDockerIT {
    public static final String REQUIRE_DOCKER_IMAGES_ENV = "REQUIRE_DOCKER_IMAGES";

    protected static void requireImage(String imageRef) {
        boolean present;
        try {
            DockerClient client = DockerClientFactory.lazyClient();
            client.inspectImageCmd(imageRef).exec();
            present = true;
        } catch (NotFoundException e) {
            present = false;
        }
        if (present) return;
        String message = "Required docker image not found locally: '" + imageRef + "'.";
        if ("1".equals(System.getenv(REQUIRE_DOCKER_IMAGES_ENV))) {
            throw new IllegalStateException("[" + REQUIRE_DOCKER_IMAGES_ENV + "=1] " + message);
        }
        assumeTrue(false, message);
    }
}
```

## J. `Layer2KeycloakModule.java` JWT helpers (paste verbatim — replace REALM / CLIENT_ID / role names)

```java
public static String mintToken(KeycloakContainer keycloak,
                               String username, String password,
                               List<String> realmRoles) throws Exception {
    try (var admin = keycloak.getKeycloakAdminClient()) {
        var realm = admin.realm(REALM);

        UserRepresentation user = new UserRepresentation();
        user.setUsername(username);
        user.setEmail(username + "@<host>.test");
        user.setEnabled(true);
        user.setEmailVerified(true);

        CredentialRepresentation cred = new CredentialRepresentation();
        cred.setType("password"); cred.setValue(password); cred.setTemporary(false);
        user.setCredentials(List.of(cred));

        try (var created = realm.users().create(user)) {
            if (created.getStatus() != 201)
                throw new IllegalStateException("Keycloak user create: HTTP " + created.getStatus());
        }
        String userId = realm.users().searchByUsername(username, true).get(0).getId();

        if (realmRoles != null && !realmRoles.isEmpty()) {
            var roleResources = realm.roles();
            var assignments = realmRoles.stream()
                    .map(name -> roleResources.get(name).toRepresentation())
                    .toList();
            realm.users().get(userId).roles().realmLevel().add(assignments);
        }
    }

    String body = "grant_type=password"
            + "&client_id=" + CLIENT_ID
            + "&username=" + URLEncoder.encode(username, StandardCharsets.UTF_8)
            + "&password=" + URLEncoder.encode(password, StandardCharsets.UTF_8)
            + "&scope="    + URLEncoder.encode("openid profile email <custom-roles-scope>", StandardCharsets.UTF_8);

    HttpResponse<String> resp = HttpClient.newHttpClient().send(
            HttpRequest.newBuilder(URI.create(
                    keycloak.getAuthServerUrl() + "/realms/" + REALM + "/protocol/openid-connect/token"))
                    .header("Content-Type", "application/x-www-form-urlencoded")
                    .POST(HttpRequest.BodyPublishers.ofString(body))
                    .build(),
            HttpResponse.BodyHandlers.ofString());
    if (resp.statusCode() != 200)
        throw new IllegalStateException("token endpoint HTTP " + resp.statusCode() + " body=" + resp.body());

    @SuppressWarnings("unchecked")
    Map<String, Object> tokenJson = JSON.readValue(resp.body(), Map.class);
    return (String) tokenJson.get("access_token");
}

public static JudoPrincipal principalFromToken(String jwt, String actorFqn) throws Exception {
    String[] parts = jwt.split("\\.");
    if (parts.length < 2) throw new IllegalArgumentException("not a JWT");
    String payloadJson = new String(Base64.getUrlDecoder().decode(parts[1]), StandardCharsets.UTF_8);
    @SuppressWarnings("unchecked")
    Map<String, Object> claims = JSON.readValue(payloadJson, Map.class);

    String preferred = (String) claims.get("preferred_username");
    String email     = (String) claims.get("email");
    String given     = (String) claims.get("given_name");
    String family    = (String) claims.get("family_name");
    @SuppressWarnings("unchecked")
    Map<String, Object> realmAccess = (Map<String, Object>) claims.get("realm_access");
    @SuppressWarnings("unchecked")
    List<String> roles = realmAccess == null ? List.of()
            : (List<String>) realmAccess.getOrDefault("roles", List.of());
    boolean isAdmin = roles.contains(ROLE_ADMIN);

    Map<String, Object> attrs = new LinkedHashMap<>();
    attrs.put("userName", preferred);   // actor-claim attribute name
    attrs.put("email",    email);
    attrs.put("preferred_username", preferred);
    attrs.put("given_name",         given);
    attrs.put("family_name",        family);
    attrs.put("realm_access",       Map.of("roles", roles));
    attrs.put("isAdmin",            isAdmin);

    return JudoPrincipal.builder()
            .name(preferred).realm("<app>").client(actorFqn)
            .attributes(attrs).build();
}
```

## K. Sample IT class shapes

### Access-link matrix (per link)

```java
@JudoTest(modelName = "<app>", dialect = "hsqldb",
        transaction = TransactionHandling.AUTO_ROLLBACK,
        modules = { Layer0Module.class })
class FoosAccessIT {
    @BeforeAll static void wire() { Layer0Module.enableActorResolution(); }

    private static final String OP_LIST    = "<app>.actors.<Actor>#_listFoos";
    private static final String OP_CREATE  = "<app>.actors.<Actor>#_createInstanceFoos";
    private static final String OP_GET     = "<app>.services.FooTO#_refreshInstance<App>_services_FooTO";
    private static final String OP_UPDATE  = "<app>.services.FooTO#_updateInstance<App>_services_FooTO";

    @Test void list_admin_sees_all(JudoRuntimeFixture f) { /* ... */ }
    @Test void list_operator_sees_own(JudoRuntimeFixture f) { /* ... */ }
    @Test void list_orphan_sees_empty(JudoRuntimeFixture f) { /* ... */ }
    @Test void create_admin(JudoRuntimeFixture f) { /* ... */ }
    @Test void update_own(JudoRuntimeFixture f) { /* ... */ }
    @Test void update_other_denied(JudoRuntimeFixture f) { /* ... */ }
    // — refresh tests document the JUDO bypass note (see G6)
}
```

### Custom-operation smoke

```java
@JudoTest(modelName = "<app>", dialect = "hsqldb",
        transaction = TransactionHandling.AUTO_ROLLBACK,
        modules = { Layer0Module.class })
class ReserveBarcodeIT {
    @BeforeAll static void wire() {
        Layer0Module.enableActorResolution();
        Layer0Module.enableSdkFunctions();   // custom op exchange function
    }

    private static final String OP = "<app>.operations.StaticOperations#reserveBarcode";
    private static final Pattern FORMAT = Pattern.compile("^<PREFIX>-\\d{8}-\\d{5}$");

    @Test void admin_happy(JudoRuntimeFixture f) {
        TestContext ctx = TestContext.from(f);
        Seed.minimalWorld(ctx);

        Map<String, Object> out = Calls.callStatic(ctx, OP, Roles.admin(), null);
        String code = (String) out.get("code");
        assertTrue(FORMAT.matcher(code).matches());

        AuditEntry row = AuditAssertions.assertEmitted(ctx, "<action.code>");
        assertEquals(Roles.ADMIN_USERNAME, row.getActorUsername());
    }
}
```

### Layer-2 JWT round-trip

```java
@Testcontainers
@JudoTest(modelName = "<app>", dialect = "hsqldb",
        transaction = TransactionHandling.AUTO_ROLLBACK,
        modules = { Layer2KeycloakModule.class })
class KeycloakJwtToPrincipalIT extends BaseDockerIT {

    @Container
    static final KeycloakContainer KEYCLOAK = new KeycloakContainer("quay.io/keycloak/keycloak:24.0")
            .withRealmImportFile("/<app>-realm.json");

    @BeforeAll static void wire() {
        Layer0Module.enableActorResolution();
        Layer0Module.enableAuthInterceptors();
        Layer2KeycloakModule.enableDirectGrants(KEYCLOAK);
    }

    @Test void admin_jwt_provisions_user(JudoRuntimeFixture f) throws Exception {
        TestContext ctx = TestContext.from(f);
        String jwt = Layer2KeycloakModule.mintToken(KEYCLOAK,
                "kc_alice", "s3cret", List.of(Layer2KeycloakModule.ROLE_ADMIN));
        JudoPrincipal alice = Layer2KeycloakModule.principalFromToken(jwt, Roles.ACTOR_FQN);

        // Call #_principal through dispatcher (no preloadActor — let the
        // resolver run so the AuthInterceptor's provisioning side-effect
        // is observable).
        Map<String, Object> ex = new HashMap<>();
        ex.put("__exposed", Boolean.TRUE);
        ex.put(Dispatcher.PRINCIPAL_KEY, alice);
        ctx.dispatcher().callOperation("<app>.actors.<Actor>#_principal", ex);

        // assert User row was provisioned with isAdmin/isActive/email/etc.
    }
}
```
