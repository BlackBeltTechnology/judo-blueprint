---
id: "multi-tenant-keycloak-realm"
title: "Multi-Tenant Isolation via Keycloak Realms"
domain: "backend"
category: "auth"
score: 44.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - ubives
---
## Description

A multi-tenancy pattern where each organization (tenant) receives its own Keycloak realm for complete user and authentication isolation. When an organization is created in the application, a corresponding Keycloak realm is programmatically created via the Keycloak admin API. Users invited to an organization are created in that organization's realm, ensuring tenant-level authentication boundaries. The application maintains a `RealmManager` OSGi service that wraps the Keycloak admin client for realm, user, and client CRUD operations.

## Structure

```java
@Component(service = RealmManager.class)
public class RealmManager {
    @Reference KeycloakFactory keycloakFactory;

    public boolean createRealm(String realmName, boolean registrationAllowed) {
        return keycloakFactory.execute(keycloak -> {
            RealmRepresentation realm = new RealmRepresentation();
            realm.setRealm(realmName);
            realm.setRegistrationAllowed(registrationAllowed);
            realm.setLoginTheme("custom-theme");
            keycloak.realms().create(realm);
            // Configure custom browser flow (WebAuthn, magic link)
            return true;
        });
    }

    public boolean createUser(String realmName, String userName, String email,
            String password, Optional<String> firstName, Optional<String> lastName) {
        return keycloakFactory.execute(keycloak -> {
            UserRepresentation user = new UserRepresentation();
            user.setUsername(userName);
            user.setEmail(email);
            user.setEnabled(true);
            user.setEmailVerified(true);
            user.setCredentials(List.of(passwordCredential));
            keycloak.realm(realmName).users().create(user);
            return true;
        });
    }
}
```

Key elements:
- `KeycloakFactory` handles admin client lifecycle with `CompositeClassLoader` for OSGi compatibility
- Each organization maps to one Keycloak realm
- Admin-level accounts live in a master "UBIVES" realm
- Regular users live in their organization's realm
- Custom authentication flows applied per realm (WebAuthn, magic link)

## Examples

### Ubives
`OrganizationService.createOrganization()` creates a `RealmEntity` in the database and calls `realmManager.createRealm(organizationName, true)` to provision the Keycloak realm. `InviteService.accept()` creates users in the organization's realm via `realmManager.createUser(realmName, ...)`. `AccountService.createAccount()` creates admin users in the "UBIVES" master realm. `KeycloakFlowCreator` configures a custom `webauthn-browser-flow` with cookie + WebAuthn passwordless + password fallback on each new realm.

## Trade-offs

- Pros: Complete tenant isolation (users cannot cross-authenticate), per-tenant authentication policies, per-tenant client registration, standard Keycloak multi-tenancy approach
- Cons: Realm proliferation (one per tenant) increases Keycloak resource usage, realm creation/deletion is slow, hardcoded admin credentials in KeycloakFactory, no connection pooling for admin client
- Alternative: Single realm with groups/roles for tenant isolation (simpler but less isolated), external multi-tenant IdP, application-level tenant filtering

## Related Patterns

- keycloak-jit-user-provisioning
- magic-link-authentication
- osgi-karaf-bundle-architecture
