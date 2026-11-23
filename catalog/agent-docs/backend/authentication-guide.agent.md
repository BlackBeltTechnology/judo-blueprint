# authentication-guide.md — index

Pull-only condensed map. Source: catalog/agent-docs/backend/authentication-guide.md.

## Overview
- `AuthenticationInterceptor`: cross-cutting auth hook, e.g. just-in-time user provisioning from Keycloak.

## Table of Contents
- Section list only; pull the section you need with `kb_get`.

## AuthenticationInterceptor Interface
- Methods: `getName()`, `isSuitableForOperation(EOperation, claim, realm, client, attributes)`, `authenticate(operationFQName, exchange, claim, realm, client, attributes)`, `success(EOperation, SignedIdentifier, exchange, claim, realm, client, attributes)`.
- `authenticate` runs at the start of EVERY dispatcher call that has a principal, before the mapped principal is loaded. It is called on every registered interceptor; `isSuitableForOperation` is NOT consulted there, so filter on `operationFQName`, `client` or `claim` inside.
- `isSuitableForOperation` is only the filter for `success`.
- `success` runs after exposure/actor checks, BEFORE the CRUD authorizers and the body, only where `isSuitableForOperation` returns `true`; it can fire for an operation that later fails with `PERMISSION_DENIED`.
- Defaults are no-ops; `isSuitableForOperation` defaults to `true`.

## The `#_principal` Operation
- Framework-level op, invoked automatically after a successful external login. Main hook for JIT provisioning.
- `attributes` in `authenticate` holds all JWT claims.
- Check for an existing local user here; create if missing.

## Token Attribute Extraction
- Standard Keycloak claims: `email`, `preferred_username`, `given_name`, `family_name`, `sub`.
- JQL reach via `!getVariable(category, 'claim_name')`; category depends on actor shape:
  - Token-only actor (no `principal`; no `claimPrincipal` flag) → `USER.*` (raw JWT).
  - Unmapped principal TO (transient) → `PRINCIPAL.*`.
  - Mapped principal TO (persisted actor) → `ACTOR.*` for persisted attributes, `USER.*` for raw claims.
- Wrong category fails silently. Matrix: `../model/advanced-modeling-patterns.md#actor-vs-principal-vs-user-context-variables`.

## Example: Just-in-Time User Provisioning
- First check the actor shape. Mapped + `managed="true"` + `<claims>` (`EMAIL`, `USERNAME` only) is meant to auto-insert on first login.
- VERIFIED GOTCHA: in judo-runtime-core-dispatcher 1.0.6.20241030 / 1.0.6.20251205 the auto-insert does NOT happen. First login throws `AccessDeniedException` `AUTHENTICATED_ENTITY_NOT_FOUND` (log: "authenticated entity not found in database").
- Until a runtime ships auto-insert, an `AuthenticationInterceptor` doing the insert is REQUIRED even for mapped + managed + `<claims>`.
- Use a custom interceptor for: non-standard claims to plain attributes, roles/flags from `groups` or `realm_access.roles`, audit/events/external calls on first login, legacy unmapped or token-only actors.
- Interceptor runs before the framework's actor lookup on the same `#_principal` call.
- Example class: `@Component(property = {"judo.model.name=<app>"})` (required binding), implements `AuthenticationInterceptor`.
  - `isSuitableForOperation` returns `true`.
  - `authenticate` returns unless `operationFQName.endsWith("#_principal")`.
  - Requires `email`; blank → warn and return.
  - `synchronized (createLock)` guards the concurrent first-login race. Alternative: skip lock, let unique-constraint violation be logged and swallowed.
  - Idempotent: `existingUser.isPresent()` → return. Keep this check even if a future runtime auto-inserts.
  - `ensureUniqueUsername`: appends a counter to `preferred_username` (fallback: email local part) until unused.
  - Create with `withIsActive(true)`.
- Error handling: catch and log, NEVER rethrow (would block login).

## Keycloak managed-realm sync — trigger surface
- `ActorType.managed=true`: CUD on the principal TO is synced to Keycloak's managed realm (create/update/delete realm user).
- Sync follows the TO's metadata, not the entity. Only the principal TO's DAO triggers it.
- Admin/list TOs mapping the same entity do NOT sync; the Keycloak user is left stale.
- Multiple TOs may map one entity; only one principal TO per actor (`actorType` back-link is exclusive).
- Route admin mutations through a custom op that calls the principal TO's DAO when realm sync is needed. Otherwise admin TO writes are DB-only.
- Design rule: one lean principal TO owns `actorType` and sync; other TOs are projections.
- Sync skipped when the transaction is marked rollback-only.
- Pattern: `../../best-practices/backend/managed-actor-admin-pattern.md`.

## Principal-to-Actor Resolution and Multi-Client Mapping
- `ActorResolver` SPI: `authenticateActor(Map exchange)`, `authenticateByPrincipal(JudoPrincipal)` → `Optional<Payload>`, `getActorByClaims(EClass, Map claims)`. `JudoDefaultModule` wires `DefaultActorResolver`; bind your own to customise.
- Lookup attribute order in `getActorByClaims`:
  1. attribute with `claim = USERNAME` (if in token);
  2. attribute with `claim = EMAIL` (if present);
  3. first identifier attribute (sorted by name) whose name is a claim key; else `IllegalStateException`.
- The actor row is read from the DB on every request carrying a principal. Profile/index the claim column if slow.
- Zero matches → `AccessDeniedException` `AUTHENTICATED_ENTITY_NOT_FOUND`; several → `SecurityException` ("Multiple actors found in database by token").
- `authenticateByPrincipal` runs only if the exchange has no actor yet AND `checkMappedActors=true` (default `false`).
- Claims matching `transient` attributes are copied onto the actor payload.
- Lookup attribute: `claim` is `USERNAME`/`EMAIL`, or name equals a claim key and maps to an identifier attribute. Missing → `IllegalStateException` ("ID attribute in Entity type matching any access token claim not found").
- Only string-valued token attributes feed the lookup; others ignored.
- Lookup value coerced to attribute type (string, numeric, date, time, timestamp, boolean, enum by literal). Other types: warning and search without filter.
- Multi-client: actor is derived from token `azp` (dashes → dots; must equal an actor FQN). The `client` arg in `isSuitableForOperation`/`authenticate` is this resolved value (after `clientToActorMap` rename), not the raw Keycloak client id.
- One realm, several actors: return early for actors the interceptor does not handle; don't assume one actor per user.
- Whitelist `JUDO_PLATFORM_ACCEPTABLE_CLIENTS` (OSGi/Guice key `acceptableClients`, default empty), format `ActorTypeFQN=client1,client2;OtherActor=client3`.
- Client ids normalised (dash → dot); ambiguous client-to-actor mapping rejected.
- Login via a client whose actor has no matching row → `AUTHENTICATED_ENTITY_NOT_FOUND`. Generated React shows "User not found" and signs out; a custom access-denied page is needed.
- Keycloak login interceptor accepts `clientToActorMap` (renames `azp` values). Realm side: `../deployment/osgi-runtime-services.md#keycloak-connector-and-realm-synchronizer-configuration`.

### Discovery endpoints for custom frontends
- `GET /api/<Model>/<Actor>/<Actor>/~meta` — `security` entry has `tokenEndpoint`, `clientId`, `openIdConfigurationUrl`.
- `GET /api/<Model>/<Actor>/<Actor>/~principal` — returns `__identifier` and `__signedIdentifier`.
- Generated React waits for `principal.__signedIdentifier`; logout is `signoutRedirect` with current URL minus hash as `post_logout_redirect_uri`.
- Provisioning a new user from a script: a user-written interceptor filtering on `#_principal` (creating the actor row) runs only for that call. A data call (`.../~list`) with a new user's token → 403 `AUTHENTICATED_ENTITY_NOT_FOUND`, no row created. Call `GET /api/<Model>/<Actor>/<Actor>/~principal` with the bearer token once first; the interceptor creates the row, later calls succeed.

## Operation Exposure, Public Access and Password Policy
- No `exposedBy` annotation → empty expected-role list. An access point without `@actor` is public; one public access point makes the whole operation public.
- `PasswordPolicy<ID>` extends `Function<Map<String,Object>,Optional<ID>>` and declares no `validatePassword()`; custom policies implement `apply()`.

## Testing and Best Practices
- Unit testing is hard (mocks the whole auth flow). Use integration tests: local Karaf, real Keycloak, new user → check app log and DB row → re-login to confirm no duplicate.
- DO: JIT provisioning in `AuthenticationInterceptor`; sync name/roles from claims; audit-log auth events; keep creation thread-safe and idempotent.
- DON'T: put complex business logic there (use `OperationCallInterceptor` or custom ops); make authorization decisions there (use the JUDO access control model); throw from `authenticate` unless intended.

## See Also
- `interceptors.md` — operation call interceptors, for standard business operations.
- `patterns-and-best-practices.md` — other common backend patterns.
