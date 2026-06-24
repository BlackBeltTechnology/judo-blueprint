---
id: "keycloak-jit-user-provisioning"
title: "Keycloak Just-In-Time User Provisioning via AuthenticationInterceptor"
domain: "backend"
category: "auth"
score: 72.0
usage_count: 7
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-05-13"
projects:
  - alba
  - mlszksz-platform
  - ubives
  - park-here
  - indamedia-adtrack
  - compsych-letter-framework
  - compsych-letter-demo
alternatives:
  - two-phase-registration
---
## Description

An `AuthenticationInterceptor` (not `OperationCallInterceptor`) that auto-provisions users on first Keycloak login. Extracts user attributes (`preferred_username`, `given_name`, `family_name`) from the authentication token, checks if a user record exists by email, and creates one with a default status (e.g., `PENDING_APPROVAL`) if absent. This implements Just-In-Time (JIT) provisioning, meaning no manual user registration is required -- the application user record is created automatically when the user first authenticates through the external identity provider.

## Structure

```java
@Component(property = { "judo.model.name=AppName" })
public class LogAuthenticationInterceptor implements AuthenticationInterceptor {

    @Reference UserDao userDao;

    @Override
    public boolean isSuitableForOperation(EOperation operation,
            String claim, String realm, String client, Map<String, Object> attributes) {
        return true;  // Intercept ALL authentication events
    }

    @Override
    public void authenticate(String operationFQN, Map<String, Object> exchange,
            String claim, String realm, String client, Map<String, Object> attributes) {
        // WARNING: key for USERNAME claim is the actor ATTRIBUTE NAME, not the JWT claim name.
        // KeycloakLoginInterceptor rewrites preferred_username → actor attribute name (e.g. "userName").
        // Claims without a claimType mapping pass through with their raw JWT key (given_name, family_name).
        // Verified against judo-runtime-core-security-keycloak-cxf:1.0.6.20260313.
        // See Implementation Gotchas → "attributes key for USERNAME claim".
        String userName = (String) attributes.get("userName");     // NOT "preferred_username"
        String firstName = (String) attributes.get("given_name");
        String lastName = (String) attributes.get("family_name");

        if (email != null) {
            Optional<User> existing = userDao.query()
                .filterByEmail(StringFilter.equalTo(email))
                .maskedBy(UserMask.userMask().withEmail().withIsActive())
                .selectOne();

            if (existing.isEmpty()) {
                userDao.create(UserForCreate.builder()
                    .withEmail(email)
                    .withFirstName(firstName)
                    .withLastName(lastName)
                    .withStatus(AccountStatus.PENDING_APPROVAL)
                    .build());
            }
        }
    }
}
```

Key: Uses `AuthenticationInterceptor` interface (not `OperationCallInterceptor`), idempotent check prevents duplicate users, default status requires admin approval before access.

## Examples

### ALBA
`LogAuthenticationInterceptor` extracts `preferred_username`, `given_name`, `family_name` from Keycloak token attributes. Creates user with `PENDING_APPROVAL` status on first login. Contains commented-out debug logging for troubleshooting attribute mapping. Keycloak 23.0 with custom realm and theme.

### mlszksz-platform
`LogAuthenticationInterceptor` targets `#_principal` operations only. Extracts email from Keycloak attributes. Instead of creating new users, updates existing user's `lastLogin` timestamp to `LocalDateTime.now()` and logs a `USER_LOGIN` audit action. Safe failure pattern: exceptions caught and logged, never propagated. Variant focused on login tracking rather than user provisioning.

### Ubives
`CreateAuthenticatedUserAuthenticationInterceptor` extracts `preferred_username` from Keycloak attributes. Queries `AccountDao` by username with `AccountMask.accountMask().withUserName()`. Creates minimal `AccountForCreate.builder().withUserName(username).build()` if not found. Paired with a separate `LogAuthenticationInterceptor` that logs all authentication attributes for debugging.

### ParkHere
`LogAuthenticationInterceptor` intercepts `_principal` operations, extracts `given_name`, `family_name`, `email` from OAuth attributes, constructs display name, and creates user if not found. Admin status set from configurable comma-separated email list via `@Activate` and OSGi ConfigAdmin (`PARKHERE_ADMIN_USERS` env var). Uses `synchronized` block for thread-safe user creation to prevent duplicate users during concurrent logins.

### Indamedia-AdTrack
`LogAuthenticationInterceptor` intercepts `#_principal` operations, extracts `given_name`, `family_name`, `email` from OIDC claims. Constructs display name with fallback logic (lastName+firstName, lastName-only, firstName-only, email). Admin status set from `admins` config property (comma-separated email list via `@Activate`). Uses `synchronized(createLock)` block for thread-safe user creation with `UserMask.userMask().withEmail()` for efficient existence check.

### compsych-letter-framework
`com.compsych.letterframework.auth.CompsychAuthInterceptor` extracts `preferred_username` (email-shaped in this IdP), `given_name`, `family_name` from Keycloak claims. Queries `UserDao.query().filterByEmail(StringFilter.equalTo(email))` masked by `userMask().withEmail().withIsActive()`. Inserts `User` row with `isActive=true` and an `isAdmin` flag derived from JWT `realm_access.roles` containing `letter-admin` OR `preferred_username` equalling `admin` (case-insensitive). Idempotent: if row exists, keeps `isAdmin` in sync, writes only on change. Failure semantics: any exception while syncing/inserting logged at WARN and swallowed — a failed insert means the framework's subsequent lookup throws `AccessDeniedException`, which is the correct fallback (no silent access grant).

### compsych-letter-demo
`hu.blackbelt.compsych.letter.interceptors.auth.LetterUserAuthenticationInterceptor` (lives under `application/interceptors/.../auth/`). Closes the `AUTHENTICATED_ENTITY_NOT_FOUND` gap (openspec change `add-letteruser-jit-provisioning`, 2026-05-11). Implements `AuthenticationInterceptor`, `@Component(property = {"judo.model.name=compsychletter"}, immediate = true)`. Filters to `#_principal` inside `authenticate()`. Reads `"userName"` key (NOT `"preferred_username"`) from `attributes` Map — `KeycloakLoginInterceptor` rewrites the JWT `preferred_username` claim to the actor attribute name `userName` (see Implementation Gotchas). Also reads `"email"`, `"given_name"`, `"family_name"` (pass through as-is, no claimType mapping for these). Creates via `UserForCreate.builder().withUserName(...).withEmail(...).withGivenName(...).withFamilyName(...).withIsActive(true).withIsAdmin(false).build()`. **Departures from canonical shape**: (1) Missing username key throws unchecked `AccessDeniedException(PERMISSION_DENIED)` — fail-fast, `BusinessErrorException` (checked) unusable in `authenticate()`. (2) Race safety via `synchronized(CREATE_LOCK)` — `judo-runtime-core-dao-rdbms:1.0.6.20260313` surfaces uniqueness violations as plain `IllegalStateException`, not a typed exception. **2026-05-13 correction**: original interceptor used `CLAIM_PREFERRED_USERNAME = "preferred_username"` (transcribed from auth-guide note "claims arrive verbatim"), causing `PERMISSION_DENIED: missingClaim preferred_username` on every login. Root cause confirmed via `LogAuthenticationInterceptor`: the `attributes` map contained `userName = alice`, not `preferred_username = alice`. Fixed by changing the lookup key to `"userName"`. The auth-guide note was wrong for this runtime version. First IT in the module is wired with class-level `@JudoTest(modelName="compsychletter")`, `UserDao` obtained via `ReferenceInjector.createAndInject(UserDaoImpl.class, fixture.getInjector())`, interceptor package-private ctor reached by reflection.

See `compsych-letter-demo` openspec `add-letteruser-jit-provisioning/{proposal,design,specs,tasks}.md` for the full design record (incl. the SPI-correction the artifacts went through between authoring and apply: spec/design/tasks originally transcribed `OperationCallInterceptor` from the triage's English summary; the triage's blueprint backing — *this very file* — was authoritative).

## Trade-offs

- Pros: No manual user registration required, seamless SSO experience, default approval status prevents unauthorized access, idempotent
- Cons: Trusts Keycloak token blindly (no signature verification at this level), user attributes may not be present in all token configurations, no role mapping from Keycloak groups
- Alternative: Two-phase email registration (see `two-phase-registration`) for applications without external IdP

## Implementation Gotchas

- **SPI lives in `hu.blackbelt.judo.runtime.core.accessmanager.api`**, Maven artifact `hu.blackbelt.judo.runtime:judo-runtime-core-accessmanager-api`. Transitively pulled by `judo-runtime-core-dispatcher`. The `judo-dispatcher-api` jar carries `VariableResolver` etc. but **NOT** `AuthenticationInterceptor` — common transcription mistake.
- **`AuthenticationInterceptor.authenticate()` has no `throws` clause.** Checked exceptions cannot be thrown. Generator-emitted `<App>BusinessErrorException` extends `java.lang.Exception` (checked) → unusable here. For fail-fast variants, throw the unchecked `hu.blackbelt.judo.runtime.core.exception.AccessDeniedException(ValidationResult.builder().code("...").build())` instead. For the canonical swallow-and-log variant, wrap the DAO work in `try { ... } catch (Exception e) { log.warn(...); }`.
- **Identifier-uniqueness violations are NOT a typed exception** in the current runtime (`judo-runtime-core-dao-rdbms:1.0.6.20260313`). They surface as plain `IllegalStateException("Identifier uniqueness violation(s): ...")`. A narrow `catch (UniqueConstraintViolation)` is therefore impossible. Use `synchronized(CREATE_LOCK)` (see `compsych-letter-demo`, `park-here`, `indamedia-adtrack`) for in-JVM race protection; rely on the RDBMS unique index for cross-JVM.
- **`#_principal` filtering belongs inside `authenticate()`**, not at the `isSuitableForOperation` boundary — the `EOperation` argument to `isSuitableForOperation` can be null in some dispatcher paths. The `operationFQName.endsWith("#_principal")` check is the canonical pattern (`mlszksz-platform`, `compsych-letter-demo`, `indamedia-adtrack` all do this).
- **Module placement.** Canonical JUDO convention puts auth interceptors under `application/interceptors/` (template-emitted `LogAuthenticationInterceptor.java.default` lives there). Placing under `application/internal/` works but requires adding `judo-runtime-core-accessmanager-api` + `judo-runtime-core` deps to `internal/pom.xml`. Pick `internal/` only when the spec/triage explicitly prescribes it.
- **`attributes` key for `claimType=USERNAME` is the actor attribute name, NOT the JWT claim name.** `KeycloakLoginInterceptor` (`judo-runtime-core-security-keycloak-cxf:1.0.6.20260313`) rewrites the JWT `preferred_username` claim to the actor's attribute name that carries `claimType=USERNAME` (e.g. `"userName"` in compsych-letter-demo). Claims without a `claimType` mapping (e.g. `given_name`, `family_name`, `sub`) pass through with their raw JWT key. Effect: `attributes.get("preferred_username")` returns `null` even when the JWT has the claim. Use `attributes.get("<actorAttributeName>")` (e.g. `"userName"`) instead. Verified 2026-05-13 via `LogAuthenticationInterceptor` on compsych-letter-demo: `attributes` contained `userName = alice`. The `judo-backend-docs/authentication-guide.md` WARNING block has the full runtime-verified details. **Affects every sister project** that uses `attributes.get("preferred_username")` directly — ALBA, Ubives, compsych-letter-framework etc. may have the same latent bug if running `≥1.0.6.20260313`.

## Related Patterns

- two-phase-registration
- actor-resolution-variable-resolver
- dao-fluent-query-filter
