---
id: multi-tenant-keycloak-realm
title: Multi-Tenant Isolation via Keycloak Realms
description: Project practice for multi-tenancy where each organization gets its own Keycloak realm, created at runtime through the Keycloak admin API behind a project RealmManager service.
aliases: [realm per tenant, tenant realm, per-organization realm]
keywords: [multi-tenant, tenant, isolation, keycloak, realm, admin client, RealmManager, organization]
tags: ["domain:backend", "layer:backend", "project:ubives", "status:single-project"]
category: auth
status: single-project
projects: [ubives]
evidence: ["ubives:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Give every organization (tenant) its own Keycloak realm, so users and authentication policies are isolated per tenant at the identity-provider level. This is project practice layered on the platform's Keycloak integration; the platform itself does not create realms per tenant at runtime.

## Practice

### Platform: realms come from the model

- The ASM-to-Keycloak transformation turns every distinct non-blank `realm` annotation on actor types into a realm, and every actor type with a `realm` annotation into a client named after the actor FQN with `.` replaced by `-` ([realm and client generation](../../agent-docs/deployment/osgi-runtime-services.md#realm-and-client-generation-from-the-model)).
- The realm synchronizer provisions those realms, clients and users when the runtime starts, only if `managementEnabled` is `true` ([connector and synchronizer configuration](../../agent-docs/deployment/osgi-runtime-services.md#keycloak-connector-and-realm-synchronizer-configuration)).
- The actor is derived from the token's `azp` claim (dashes become dots and must equal an actor FQN); several clients in one realm are whitelisted with `acceptableClients` ([several Keycloak clients in one realm](../../agent-docs/backend/authentication-guide.md#several-keycloak-clients-in-one-realm)).
- The runtime then reads the actor row from the database on every authenticated request; a missing row gives `AUTHENTICATED_ENTITY_NOT_FOUND` ([principal-to-actor resolution](../../agent-docs/backend/authentication-guide.md#principal-to-actor-resolution-and-multi-client-mapping)). Users created in a tenant realm therefore still need a matching actor row ([[keycloak-jit-user-provisioning]]).

Realms known at model time need no custom code. Tenants created while the application runs do not fit that mechanism, which is what the project practice below covers.

### Project practice: RealmManager service over the Keycloak admin client

The project (ubives) wraps the Keycloak admin client in an OSGi service (example project code, not a platform type):

```java
// Example project code: RealmManager and KeycloakFactory are project classes
@Component(service = RealmManager.class)
public class RealmManager {
    @Reference KeycloakFactory keycloakFactory;

    public boolean createRealm(String realmName, boolean registrationAllowed) {
        return keycloakFactory.execute(keycloak -> {
            RealmRepresentation realm = new RealmRepresentation();
            realm.setRealm(realmName);
            realm.setRegistrationAllowed(registrationAllowed);
            keycloak.realms().create(realm);
            return true;
        });
    }

    public boolean createUser(String realmName, String userName, String email) {
        return keycloakFactory.execute(keycloak -> {
            UserRepresentation user = new UserRepresentation();
            user.setUsername(userName);
            user.setEmail(email);
            user.setEnabled(true);
            keycloak.realm(realmName).users().create(user);
            return true;
        });
    }
}
```

- Creating an organization saves a realm record in the database and calls `createRealm` for the new tenant.
- Accepting an invitation creates the user in the organization's realm; platform-level administrators live in a separate master-style realm.
- A flow-configuration helper applies a custom browser flow (cookie, passwordless WebAuthn, password fallback) to each new realm.
- The `KeycloakFactory` owns the admin client lifecycle and works around OSGi class loading with a composite class loader.
- Because realms created at runtime are not in the model, each new realm needs its own client for the actor FQN-derived name, otherwise the `azp` mapping above cannot resolve the actor.

## Rationale

- Users cannot authenticate across tenants, and each tenant can have its own login flow, password policy and client registration.
- It is the standard Keycloak multi-tenancy approach and keeps tenant separation out of application queries.
- Costs: one realm per tenant raises Keycloak memory use, realm creation and deletion are slow, and the project's factory hard-codes admin credentials and keeps no connection pool (the platform's own `adminPassword` default is also a development value, so override it outside local use).

## Example

In ubives, creating an organization creates its realm; inviting a person creates the user in that realm; creating a platform administrator uses the master-style realm; a flow creator configures the passwordless browser flow on every new realm. The tenant's database record keeps the realm name so later calls pick the right realm.

## When to avoid

- When a small, fixed set of realms is enough: declare the realm annotations in the model and let the synchronizer provision them.
- When tenant separation can be done with data access rules in one realm (groups, roles or a tenant attribute on the actor); it is simpler and avoids realm proliferation.
- When the number of tenants is large or tenants are created at a high rate.

## Related

- [[keycloak-jit-user-provisioning]] — creates the actor row for users that exist only in Keycloak
- [[magic-link-authentication]] — a passwordless flow applied per realm
- [[osgi-karaf-bundle-architecture]] — the OSGi service layout RealmManager lives in
