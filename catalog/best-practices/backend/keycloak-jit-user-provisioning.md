---
id: keycloak-jit-user-provisioning
title: Keycloak Just-In-Time User Provisioning via AuthenticationInterceptor
description: "An AuthenticationInterceptor that runs on the principal operation after a Keycloak login, reads the token claims and creates the application's user row on first login with a default status, idempotently and without ever blocking the login; plus the model-driven alternative and its runtime limits."
aliases: ["JIT provisioning", "first login user creation", "auto user creation", "AuthenticationInterceptor"]
keywords: ["Keycloak", "just-in-time", "provisioning", "AuthenticationInterceptor", "principal", "claims", "first login", "idempotent", "synchronized", "AUTHENTICATED_ENTITY_NOT_FOUND"]
tags: ["domain:backend", "layer:backend", "project:alba", "project:mlszksz-platform", "project:ubives", "project:park-here", "project:indamedia-adtrack", "status:established"]
category: auth
status: established
projects: [alba, mlszksz-platform, ubives, park-here, indamedia-adtrack]
evidence: ["alba:unrecorded", "mlszksz-platform:application/interceptors/src/main/java/hu/blackbelt/mlszksz/platform/interceptors/LogAuthenticationInterceptor.java", "ubives:unrecorded", "park-here:unrecorded", "indamedia-adtrack:unrecorded"]
alternatives: [two-phase-registration]
related: [two-phase-registration, actor-resolution-variable-resolver, dao-fluent-query-filter, mask-field-projection, interceptor-global-logging, safe-failure-pattern, magic-link-authentication]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---

## Intent

A user who logs in through Keycloak must have an application user row (the actor's entity) before the runtime can resolve the actor. Instead of registering users by hand, an `AuthenticationInterceptor` creates the row on the first login from the token claims. This is just-in-time (JIT) provisioning.

## Practice

### Platform: the hook and what the runtime does itself

- `AuthenticationInterceptor` (not `OperationCallInterceptor`) has `getName`, `isSuitableForOperation(operation, claim, realm, client, attributes)` and `authenticate(operationFQName, exchange, claim, realm, client, attributes)`. The `attributes` map holds the claims of the JWT (`email`, `preferred_username`, `given_name`, `family_name`, `sub`) ([interface](../../agent-docs/backend/authentication-guide.md#authenticationinterceptor-interface), [token attributes](../../agent-docs/backend/authentication-guide.md#token-attribute-extraction)).
- It is called on the framework-level `#_principal` operation after a successful external login, after the principal is extracted and **before** the framework loads the mapped actor, so the row it inserts is the one the lookup then reads ([the #_principal operation](../../agent-docs/backend/authentication-guide.md#the-_principal-operation)).
- The actor row is read from the database on every request that carries a principal. No row gives `AccessDeniedException` with `AUTHENTICATED_ENTITY_NOT_FOUND`; the generated frontend shows "User not found" ([principal-to-actor resolution](../../agent-docs/backend/authentication-guide.md#principal-to-actor-resolution-and-multi-client-mapping)).
- The platform guide records that a mapped, managed actor with `<claims>` is meant to be inserted by the runtime, but the verified runtime versions do **not** insert it, so this interceptor is required even for that shape. If a later runtime does insert, the existence check turns the interceptor into a no-op; keep it ([provisioning example and warning](../../agent-docs/backend/authentication-guide.md#example-just-in-time-user-provisioning)).
- The `<claims>` element covers only `EMAIL` and `USERNAME`; roles, flags or other claims need the interceptor.
- The Keycloak user and the database row are two stores that can drift: a user can exist in Keycloak without a row ([Keycloak users and the entity store](../../agent-docs/backend/platform-behavior-reference.md#keycloak-users-and-the-entity-store)).
- Like operation interceptors, the component needs `judo.model.name=<model>` ([registration](../../agent-docs/backend/interceptors.md#interceptor-component-registration)).

### Practice notes: idempotent create under a lock, never throw

```java
// Example code: UserDao, User, UserForCreate, AccountStatus are generated types
@Component(property = { "judo.model.name=<model>" })
public class UserProvisioningInterceptor implements AuthenticationInterceptor {

    @Reference UserDao userDao;
    private final Object createLock = new Object();

    @Override public String getName() { return getClass().getSimpleName(); }

    @Override
    public boolean isSuitableForOperation(EOperation op, String claim, String realm,
                                          String client, Map<String, Object> attributes) {
        return true;
    }

    @Override
    public void authenticate(String operationFQName, Map<String, Object> exchange, String claim,
                             String realm, String client, Map<String, Object> attributes) {
        if (!operationFQName.endsWith("#_principal")) return;
        String email = (String) attributes.get("email");
        if (email == null || email.isBlank()) return;

        synchronized (createLock) {
            boolean exists = userDao.query()
                    .filterByEmail(StringFilter.equalTo(email))
                    .maskedBy(UserMask.userMask().withEmail())
                    .selectOne().isPresent();
            if (!exists) {
                try {
                    userDao.create(UserForCreate.builder()
                            .withEmail(email)
                            .withFirstName((String) attributes.get("given_name"))
                            .withLastName((String) attributes.get("family_name"))
                            .withStatus(AccountStatus.PENDING_APPROVAL)
                            .build());
                } catch (Exception e) {
                    // log and swallow: a provisioning failure must not block the login
                }
            }
        }
    }
}
```

- **Filter for `#_principal`** (most implementations do; the pattern also "intercepts all events" and returns early otherwise).
- **Pick the claim that matches the actor's lookup attribute** (email or `preferred_username`); the runtime looks the actor up by the attribute with `claim = USERNAME`, then `EMAIL`, then the first identifier ([resolution order](../../agent-docs/backend/authentication-guide.md#resolution-order-defaultactorresolver)). A different claim here than in the lookup leaves the user unfound.
- **Idempotency**: check existence first with a minimal mask ([[mask-field-projection]], [[dao-fluent-query-filter]]).
- **Thread safety**: concurrent first logins can both pass the check. Implementations wrap check and create in `synchronized` on a dedicated lock; the alternative is no lock and a swallowed unique-constraint failure. A lock protects one node only; a cluster needs the unique constraint as the final guard.
- **Do not rethrow.** Exceptions from `authenticate` block the login; use the safe-failure approach ([[safe-failure-pattern]]) unless blocking is intended.
- **Default status** such as `PENDING_APPROVAL` so an admin approves before access. Authorization still comes from the model's access rules, not from this interceptor.
- Variants seen: update `lastLogin` and write an audit entry on every login instead of creating users; set admin status from a configured list of e-mail addresses; build a display name with fallbacks; create a minimal account row (user name only).
- Test by logging in with a new user, checking the row, and logging in again to prove no duplicate ([testing](../../agent-docs/backend/authentication-guide.md#testing-authentication-interceptors)).

## Rationale

- No manual registration; the application row appears with the first SSO login.
- A default approval status keeps unapproved users out.
- Cost: the application trusts the claims the runtime already verified (it does no verification itself); claims can be missing for some client or token configurations; there is no automatic role mapping from Keycloak groups unless coded.

## Example

A user logs in through Keycloak for the first time. The interceptor sees `#_principal`, reads e-mail, given and family name from the claims, finds no user with that e-mail, and creates one with status "pending approval". The runtime then resolves the actor from the new row. An administrator approves the user later. Several applications use this shape; one also sets admin rights from a configured address list, under a lock.

## When to avoid

- When users are created by an invitation or registration flow before the first login ([[two-phase-registration]]).
- When the actor is mapped and managed and the runtime in use inserts the row itself (verify; at the documented versions it does not).
- For business logic or authorization decisions: use the model's access rules and operation interceptors.
- When the identity provider is not Keycloak-like (no stable e-mail or username claim).

## Related

- [[two-phase-registration]] — registration without an external IdP
- [[actor-resolution-variable-resolver]] — reads the row this interceptor creates
- [[dao-fluent-query-filter]] — the existence query
- [[mask-field-projection]] — minimal mask for the check
- [[interceptor-global-logging]] — the logging twin for authentication events
- [[safe-failure-pattern]] — never block the login
- [[magic-link-authentication]] — passwordless login in front of this flow
