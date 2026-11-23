---
title: Backend Authentication Guide
description: AuthenticationInterceptor, the principal operation, token attribute extraction and just-in-time user provisioning.
aliases: [create user on first login, jwt claims to user, keycloak user sync, auto create user after login, login user not found, authentication interceptor example]
keywords: [AuthenticationInterceptor, authenticate, isSuitableForOperation, "#_principal", DefaultActorResolver, getActorByClaims, AUTHENTICATED_ENTITY_NOT_FOUND, JUDO_PLATFORM_ACCEPTABLE_CLIENTS, azp, acceptableClients, getVariable, managed]
tags: [domain:backend, layer:backend, status:platform]
---

# Authentication Guide

## Overview

This guide provides a comprehensive overview of `AuthenticationInterceptor` in the JUDO framework. Authentication interceptors are a powerful mechanism for handling cross-cutting concerns related to user authentication, such as just-in-time user provisioning from an external identity provider like Keycloak.

## Table of Contents

- [AuthenticationInterceptor Interface](#authenticationinterceptor-interface)
- [The `#_principal` Operation](#the-_principal-operation)
- [Token Attribute Extraction](#token-attribute-extraction)
- [Keycloak managed-realm sync — trigger surface](#keycloak-managed-realm-sync--trigger-surface)
- [Example: Just-in-Time User Provisioning](#example-just-in-time-user-provisioning)
- [Testing and Best Practices](#testing-and-best-practices)

---

## AuthenticationInterceptor Interface

The core of this pattern is the `AuthenticationInterceptor` interface. Your custom interceptor will implement this interface to hook into the authentication lifecycle.

```java
public interface AuthenticationInterceptor {
    String getName();
    boolean isSuitableForOperation(EOperation operation, String claim, String realm, String client, Map<String, Object> attributes);
    void authenticate(String operationFQName, Map<String, Object> exchange, String claim, String realm, String client, Map<String, Object> attributes);
    void success(EOperation operation, SignedIdentifier signedIdentifier, Map<String, Object> exchange, String claim, String realm, String client, Map<String, Object> attributes);
}
```

The methods are called at two different points:

- `authenticate(operationFQName, exchange, claim, realm, client, attributes)` runs at the start of **every** dispatcher operation call that has a principal, before the mapped principal is loaded. It is called on every registered interceptor; `isSuitableForOperation` is **not** consulted, so filter on `operationFQName`, `client` or `claim` inside the method.
- `isSuitableForOperation(operation, claim, realm, client, attributes)` is only the filter for `success`.
- `success(operation, signedIdentifier, exchange, claim, realm, client, attributes)` runs after the exposure and actor checks of the operation and before the CRUD authorizers and the operation body, so it can fire for an operation that later fails with `PERMISSION_DENIED`; it runs only on interceptors whose `isSuitableForOperation` returns `true`.

`isSuitableForOperation`, `authenticate` and `success` default to no-ops (`isSuitableForOperation` defaults to `true`).

## The `#_principal` Operation

The `#_principal` operation is a special, framework-level operation that is automatically invoked after a user successfully authenticates with an external identity provider. This is the primary point of interception for just-in-time provisioning.

### Key Characteristics
- **Triggered Automatically**: Called by the JUDO framework after a successful external login.
- **Provides Token Claims**: The `attributes` map in the `authenticate` method contains all the claims from the user's JWT token.
- **Ideal for User Creation**: It's the perfect place to check if a user exists in your local database and create them if they don't.

## Token Attribute Extraction

When a user authenticates, their JWT token contains claims that are passed to the interceptor as the `attributes` map. You can extract standard and custom claims to populate your local user entity.

### Standard Keycloak Token Attributes
- `email` - User's email address
- `preferred_username` - Username from the identity provider
- `given_name` - First name
- `family_name` - Last name
- `sub` - The subject identifier (a unique user ID from the IdP)

> [!NOTE]
> **Accessing these claims from JQL**
>
> The same claims are reachable from JQL expressions (access filters, derived features, custom-op preconditions) via `!getVariable(category, 'claim_name')`. The correct category depends on the actor shape:
>
> - Token-only actors (no `principal`; there is no `claimPrincipal` flag) → use **`USER.*`** (raw JWT).
> - Unmapped principal TO (transient principal) → use **`PRINCIPAL.*`**.
> - Mapped principal TO (persisted actor entity) → use **`ACTOR.*`** for persisted attributes, **`USER.*`** for raw claims.
>
> See [ACTOR vs PRINCIPAL vs USER](../model/advanced-modeling-patterns.md#actor-vs-principal-vs-user-context-variables) for the full decision matrix and the silent-failure pitfall.

---

## Example: Just-in-Time User Provisioning

> [!IMPORTANT]
> **Model-driven provisioning comes first — check the actor shape before writing an interceptor.**
>
> If the `ActorType` in your ESM is **mapped + `managed="true"` + has `<claims>`** (see [Mapped Managed Principal with Claim Mapping](../model/advanced-modeling-patterns.md#pattern-mapped-managed-principal-with-claim-mapping)), the JUDO runtime is *intended* to insert the principal row on first login and update it on every subsequent `#_principal` call, directly from the JWT claims declared in `<claims>`. In that intended case you do not need an `AuthenticationInterceptor` for the baseline insert.
>
> Use a custom `AuthenticationInterceptor` only when you need behaviour **beyond** what `<claims>` can express:
> -  Copying a non-standard JWT claim to a plain entity attribute (the `<claims>` element only covers `EMAIL` and `USERNAME`).
> -  Initialising roles or permission flags from a `groups` / `realm_access.roles` claim.
> -  Writing an audit row, emitting a domain event, or calling an external system on first login.
> -  Coping with legacy actors that are **not** mapped + managed (e.g. an unmapped principal TO, or a token-only actor with no `principal`), where the runtime does no persistence of its own.
>
> When both are in play, the interceptor runs **before** the framework's actor lookup on the same `#_principal` call (per the [AuthenticationInterceptor contract](./interceptors.md) — *"after the extraction of principal but before the load of the mapped principal load"*), so it can safely insert/update the row that the lookup is about to read.

> [!WARNING]
> **Verified runtime behaviour (judo-runtime-core-dispatcher 1.0.6.20241030 / 1.0.6.20251205): the auto-insert does NOT happen.**
>
> `DefaultActorResolver.getActorByClaims` only calls `dao.search(actorType, …)` on the principal entity and, when the result is empty, throws:
>
> ```
> hu.blackbelt.judo.runtime.core.exception.AccessDeniedException
>   ValidationResult.code = "AUTHENTICATED_ENTITY_NOT_FOUND"
>   at DefaultActorResolver.getActorByClaims(DefaultActorResolver.java:~205)
>   at DefaultActorResolver.authenticateByPrincipal
>   at DefaultActorResolver.authenticateActor
>   at DefaultDispatcher.callOperation
>   at <YourActor>Impl._principal
> ```
>
> No row insertion code path exists in the dispatcher source for `managed=true` actors as of these versions. The `INFO` log line `"Operation failed, authenticated entity not found in database"` (visible on every first-login attempt) is the giveaway.
>
> **Until a runtime release ships the documented auto-insert, you MUST provide an `AuthenticationInterceptor` that performs the first-login insert yourself**, even for the textbook *mapped + managed + `<claims>`* case. The example below is exactly that interceptor; it is required, not optional. The `synchronized` block in the example is one defence against the concurrent-first-login race; an alternative is to skip the lock and let the unique-constraint violation surface as a `RuntimeException` that you log and swallow (the loser's request still benefits from the winner's row on the upcoming framework lookup).
>
> If a future runtime version actually implements the auto-insert, the interceptor's pre-query check (`if (existingUser.isPresent()) return;`) makes it a safe no-op — keep it in place rather than removing it.

The following example demonstrates how to create a user in the local application database on their first login — appropriate when the actor is **not** using the mapped + managed shape, or when extra fields must be populated beyond the declared `<claims>`.

### Provisioning Interceptor Code

```java
@Component(property = {"judo.model.name=<app>"})
public class AutoUserCreationAuthenticationInterceptor implements AuthenticationInterceptor {

    private static final Logger log = LoggerFactory.getLogger(AutoUserCreationAuthenticationInterceptor.class);
    private final Object createLock = new Object();

    @Reference
    private UserDao userDao;

    @Override
    public String getName() {
        return this.getClass().getSimpleName();
    }

    @Override
    public boolean isSuitableForOperation(EOperation operation, String claim, String realm, String client, Map<String, Object> attributes) {
        // This interceptor is applicable to all authentication operations.
        return true;
    }

    @Override
    public void authenticate(String operationFQName, Map<String, Object> exchange, String claim, String realm, String client, Map<String, Object> attributes) {
        // We only care about the #_principal operation.
        if (!operationFQName.endsWith("#_principal")) {
            return;
        }

        // Extract user information from the token claims.
        String email = (String) attributes.get("email");
        if (email == null || email.isBlank()) {
            log.warn("Cannot auto-provision user: email not found in token.");
            return;
        }

        // Use a synchronized block to prevent race conditions during user creation.
        synchronized (createLock) {
            Optional<User> existingUser = userDao.query()
                    .filterByEmail(StringFilter.equalTo(email))
                    .selectOne();

            if (existingUser.isPresent()) {
                return; // User already exists, do nothing.
            }

            log.info("Auto-provisioning new user: email={}", email);
            try {
                String username = (String) attributes.getOrDefault("preferred_username", email.split("@")[0]);
                
                UserForCreate newUser = UserForCreate.builder()
                        .withUserName(ensureUniqueUsername(username))
                        .withEmail(email)
                        .withIsActive(true)
                        .build();

                userDao.create(newUser);
                log.info("User auto-provisioned successfully: {}", email);

            } catch (Exception e) {
                log.error("Failed to auto-provision user: {}", email, e);
                // IMPORTANT: Do not rethrow the exception. This would block the user from logging in.
            }
        }
    }

    private String ensureUniqueUsername(String baseUsername) {
        String username = baseUsername;
        int counter = 1;
        while (userDao.query().filterByUserName(StringFilter.equalTo(username)).count() > 0) {
            username = baseUsername + counter++;
        }
        return username;
    }
}
```

### Key Patterns in the Example

- **`@Component(property = {"judo.model.name=..."})`**: This property is **required** to bind the interceptor to your specific JUDO model.
- **Filtering for `#_principal`**: The interceptor immediately returns if the operation is not the principal creation hook.
- **Thread Safety**: A `synchronized` block on a dedicated lock object (`createLock`) is crucial to prevent race conditions where two concurrent login attempts could try to create the same user, resulting in a unique constraint violation.
- **Idempotency**: The check for `existingUser.isPresent()` ensures that the logic is idempotent—it can run multiple times for the same user without creating duplicate accounts.
- **Error Handling**: Exceptions during user creation are caught and logged but **not re-thrown**. This is a critical design choice to ensure that a failure in the provisioning logic does not prevent a valid user from logging in.

---

## Keycloak managed-realm sync — trigger surface

With `ActorType.managed=true`, the JUDO framework delegates CUD on the principal TO to Keycloak's managed realm (create / update / delete the realm user matching the row). The dispatcher injects this sync **only** when the DAO layer is invoked with the **principal TO's metadata**. Sync follows TO metadata, not the underlying entity.

Consequences:

-  Other TOs mapping the same principal entity (e.g., an admin user-management `UserTO`, a list `UserListTO`) do **NOT** auto-sync when their endpoints mutate the row. The entity row updates; the Keycloak realm user does not.
-  Multiple TOs CAN map the same principal entity. The metamodel allows it; only the `actorType` back-link is exclusive — at most ONE principal TO per actor. See *Principal back-link exclusivity* in [accesspoint.md](../model/esm_metamodel/accesspoint.md) for why.
-  To get Keycloak sync from an admin user-management surface, write a custom operation on the admin TO that delegates through the **principal TO's DAO** (re-dispatch with principal-TO metadata). Direct CUD on admin TOs skips Keycloak.
-  Design rule: keep ONE lean principal TO that owns `actorType` AND framework-managed Keycloak sync. Use other mapped TOs for admin / list projections. Route admin mutations through a custom op calling the principal TO's DAO when realm sync is required; otherwise accept that admin TO mutations are DB-only.

See *Managed-realm sync trigger* and *Principal back-link exclusivity* in [accesspoint.md](../model/esm_metamodel/accesspoint.md) for the metamodel side.

For the canonical admin-surface shape and the custom-op delegation pattern that routes admin mutations through the principal TO's DAO, see the [managed actor admin pattern](../../best-practices/backend/managed-actor-admin-pattern.md).

**Source**: `judo-runtime-core-security` `UserManagedWrappedDao` calls `userManager.createUser/updateUser/deleteUser` only when `KeycloakUserManager.getManagedActorOfPrincipal(clazz)` resolves the DAO call's class to a managed actor, i.e. only for the principal transfer object of an actor with `managed=true`. Sync is skipped when the transaction is marked for rollback.


## Principal-to-Actor Resolution and Multi-Client Mapping

### Resolution order (`DefaultActorResolver`)

`ActorResolver` is the SPI that maps a `JudoPrincipal` or token claims to the persisted actor payload: `authenticateActor(Map exchange)`, `authenticateByPrincipal(JudoPrincipal)` (returns `Optional<Payload>`) and `getActorByClaims(EClass actorType, Map claims)`. `JudoDefaultModule` wires `DefaultActorResolver`; bind your own implementation to add custom matching, just-in-time provisioning or rejection.

`getActorByClaims` chooses the lookup attribute in this order:

1. the attribute with `claim = USERNAME`, if its claim is present in the token;
2. the attribute with `claim = EMAIL`, if present;
3. the first identifier attribute (sorted by name) whose name is in the claims; otherwise `IllegalStateException`.

It then runs `dao.search` on the actor type, so **the actor row is read from the database on every request that carries a principal**. Zero matches give `AccessDeniedException` `AUTHENTICATED_ENTITY_NOT_FOUND`; several matches give `SecurityException` ("Multiple actors found in database by token"). When the principal resolution is slow, profile this read (index the claim column) rather than the application's `#_principal` interceptor. `authenticateByPrincipal` runs only when the exchange has no actor yet and `checkMappedActors` is `true` (default `false`). Claims whose matching attribute is `transient` are copied onto the returned actor payload.

Details of the lookup:

- The lookup attribute is an actor attribute whose `claim` is `USERNAME` or `EMAIL`, or one whose name equals a token claim key **and** that maps to an entity identifier attribute. A mapped actor with no such attribute fails with `IllegalStateException` ("ID attribute in Entity type matching any access token claim not found").
- `authenticateByPrincipal` builds the claims map from the string-valued token attributes only; non-string claims are ignored for the lookup.
- The lookup value is coerced to the attribute type (string, numeric, date, time, timestamp, boolean, enumeration by literal); other types log a warning and run the search without a filter.
- Transient actor attributes whose name equals a claim key receive the claim value on the actor payload.
- **Timing.** The actor lookup runs after the `authenticate` hooks and before the operation body. A first call from a new user, with no actor row yet, fails with `AUTHENTICATED_ENTITY_NOT_FOUND` unless an `AuthenticationInterceptor.authenticate` hook has already created the row; a row created in `success` or in the operation body is too late for that request.

### Several Keycloak clients in one realm

JUDO derives the actor from the token's `azp` claim: dashes become dots and the result must equal an actor FQN. A frontend client with another name cannot be resolved. The `client` argument of `AuthenticationInterceptor.isSuitableForOperation` and `authenticate` is this resolved value (the `azp` claim with dashes turned into dots, then renamed through `clientToActorMap` if configured), not the raw Keycloak client id. When one realm serves several actors (for example an admin who also logs in through another actor's client), decide on the actor FQN this value holds and return early for actors the interceptor does not handle; do not assume the user belongs to one actor. Set the whitelist `JUDO_PLATFORM_ACCEPTABLE_CLIENTS` (OSGi/Guice key `acceptableClients`, default empty):

```
ActorTypeFQN=client1,client2;OtherActor=client3
```

Client ids are normalised (dash to dot) and an ambiguous client-to-actor mapping is rejected. A user who signs in through the client of an actor that has no matching row gets `AUTHENTICATED_ENTITY_NOT_FOUND`; the generated React client shows this as "User not found" and signs the user out, so an access-denied message needs a custom page. The Keycloak login interceptor also accepts a `clientToActorMap` that renames `azp` values to actor names. See [OSGi Runtime Services](../deployment/osgi-runtime-services.md#keycloak-connector-and-realm-synchronizer-configuration) for the realm side.

Client resolution has no acceptable-clients fallback: an unknown client throws `IllegalStateException` ("Unsupported client"). Keycloak deployments are cached per realm only. On a cache hit the client name is ignored, so actors that share a realm reuse the first cached client. `KeycloakLoginInterceptor` verifies the token without an explicit issuer-to-realm check.

### Actor path matching

Actor lookup from the request path is a plain string prefix match with no segment boundary. An actor path that is a prefix of another actor's name also matches the requests of that longer name (for example `<Actor>` matches `<Actor>Admin`).

### Discovery endpoints for custom frontends

Each actor exposes `GET /api/<Model>/<Actor>/<Actor>/~meta` and `GET /api/<Model>/<Actor>/<Actor>/~principal` (the authenticated principal with `__identifier` and `__signedIdentifier`). The `security` entry of `~meta` carries `tokenEndpoint`, `clientId` and `openIdConfigurationUrl`, which a custom frontend needs to obtain an access token for that actor. The generated React layout waits for `principal.__signedIdentifier` before rendering, maps `AUTHENTICATED_ENTITY_NOT_FOUND` to a "User not found" message, and logs out with `signoutRedirect` using the current URL without its hash as `post_logout_redirect_uri`.

#### Provisioning a new user from a script

A user-written interceptor that filters on `#_principal` and creates the actor row runs only for that call. A data call (`.../~list`) with a new user's token answers 403 `AUTHENTICATED_ENTITY_NOT_FOUND` and creates no row. Call `GET /api/<Model>/<Actor>/<Actor>/~principal` with the bearer token once first (the generated frontend does this); the interceptor then creates the row and later calls succeed.

## Operation Exposure, Public Access and Password Policy

- An operation without an `exposedBy` annotation gets an empty expected-role list.
- An access point without `@actor` counts as public. One public access point makes the whole operation public, so its expected-role list is empty.
- `PasswordPolicy<ID>` extends `Function<Map<String, Object>, Optional<ID>>` and declares no `validatePassword()` method. A custom policy implements `apply()`.

## Testing and Best Practices

### Testing Authentication Interceptors

Direct unit testing is challenging because it requires mocking the entire authentication flow. The recommended approach is **integration testing**:

1.  Deploy the application to a local Karaf instance.
2.  Configure a real identity provider like Keycloak.
3.  Log in with a new user that does not exist in the application database.
4.  Verify in the application logs and database that the user was created correctly.
5.  Log out and log back in with the same user to test for idempotency (i.e., ensure no duplicate user is created).

### Best Practices

✅ **DO:**
- Use `AuthenticationInterceptor` for just-in-time user provisioning.
- Synchronize user attributes (like name or roles) from token claims.
- Log authentication events for auditing purposes.
- Make your user creation logic thread-safe and idempotent.

❌ **DON'T:**
- Use `AuthenticationInterceptor` for complex business logic (use `OperationCallInterceptor` or custom operations instead).
- Use it for authorization decisions (this should be handled by the JUDO access control model).
- Block the authentication flow by throwing exceptions from the `authenticate` method, unless that is the intended behavior.

---

## See Also

- [Operation Call Interceptors](interceptors.md) - For intercepting standard business operations.
- [Patterns and Best Practices](patterns-and-best-practices.md) - For other common backend patterns.