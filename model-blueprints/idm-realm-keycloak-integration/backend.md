## Overview

The IDM/Realm entity cluster is backed by a dedicated `keycloak-client` module that provides a `RealmManager` OSGi service for managing Keycloak realms, users, and clients. The `InitDefaultIdm` initializer operation seeds the default IDM server and platform realm on first startup. All account and invitation operations that create users also provision them in Keycloak through `RealmManager`.

## Implementation Pattern

- A separate Maven module (`keycloak-client`) encapsulates all Keycloak admin API interactions, keeping the dependency on `org.keycloak:keycloak-admin-client` isolated from the main application module
- `KeycloakFactoryComponent` is an OSGi `@Component` with `ConfigurationPolicy.REQUIRE` and `@Designate` for external configuration (serverUrl, realm, username, password, clientId). On activation it creates a `KeycloakFactory` instance and registers it as an OSGi service
- `RealmManager` is an OSGi `@Component` that injects `KeycloakFactory` and `KeycloakConnectorReady` via `@Reference`. It exposes methods: `createRealm(name, registrationAllowed)`, `deleteRealm(name)`, `createClient(realmName, clientName, baseUrl)`, `createUser(realmName, userName, email, password, firstName, lastName)`, and `userExists(realmName, userName)`
- `KeycloakFlowCreator` is a static utility that programmatically creates a custom WebAuthn browser authentication flow (cookie + identity-provider-redirector + username + webauthn-or-password) and sets it as the realm's browser flow. It also enables WebAuthn passwordless registration as a default required action
- The `InitDefaultIdmCustomImplementation` initializer operation seeds the `IdmEntity` with the Keycloak server URL and creates the platform-level "UBIVES" `RealmEntity` via `RealmManager.createRealm()`
- Service layer classes (`AccountService`, `InviteService`) inject `RealmManager` via `@Reference` and call `realmManager.createUser()` after creating entity-level Account/User records, ensuring dual provisioning (database + Keycloak)
- Error handling: if `RealmManager.createUser()` returns false (Keycloak failure), the service throws `BusinessErrorException` with `ErrorCode.IDM_DOES_NOT_EXISTS` or `ErrorCode.KEYCLOAK_USER_ALREADY_EXISTS_WITH_THIS_NAME`

## Examples

### ubives
- Key files: `keycloak-client/.../osgi/RealmManager.java`, `keycloak-client/.../osgi/KeycloakFactoryComponent.java`, `keycloak-client/.../osgi/KeycloakFlowCreator.java`, `custom/.../_default_transferobjecttypes/entities/initializer/InitDefaultIdmCustomImplementation.java`
- Pattern: Separate `keycloak-client` module with OSGi DS wiring. `KeycloakFactoryComponent` reads Keycloak admin credentials from OSGi ConfigAdmin and publishes a `KeycloakFactory` service. `RealmManager` wraps all Keycloak admin operations (realm CRUD, user CRUD, client CRUD) behind simple boolean-returning methods
- Notable: `KeycloakFlowCreator.createBrowserFlow()` programmatically builds a custom WebAuthn-based authentication flow with passwordless support, cookie fallback, and identity-provider-redirector -- enabling passkey login alongside traditional passwords. Each organization realm gets this custom flow applied automatically
- Integration points: `AccountService.createAccount()` calls `realmManager.createUser("UBIVES", ...)` for platform-level accounts; `InviteService.accept()` calls `realmManager.createUser(organization.getRealm().getName(), ...)` for organization-scoped users, demonstrating the multi-realm architecture where each organization has its own Keycloak realm
