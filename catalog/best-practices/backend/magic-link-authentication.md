---
id: magic-link-authentication
title: Keycloak Magic Link Authentication Flow
description: "A custom Keycloak authenticator deployed as a Keycloak extension that signs users in by a time-limited e-mailed link, with token handling in an application service and the Keycloak admin client wrapped as an OSGi component; local practice outside the JUDO platform."
aliases: ["passwordless email login", "magic link authenticator", "Keycloak SPI authenticator"]
keywords: ["Keycloak", "magic link", "authenticator", "SPI", "passwordless", "token lifespan", "admin client", "OSGi", "email"]
tags: ["domain:backend", "layer:backend", "project:ubives", "status:single-project"]
category: auth
status: single-project
projects: [ubives]
evidence: ["ubives:unrecorded"]
alternatives: []
related: [keycloak-jit-user-provisioning, two-phase-registration, email-service-integration, multi-tenant-keycloak-realm, keycloak-magic-link-passkey-authentication]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---

## Intent

Users should sign in without a password: they enter an e-mail address, receive a link with a short-lived token, and are authenticated when they open it. JUDO delegates authentication to Keycloak, so the mechanism is a Keycloak extension, not a JUDO feature. The application side manages users and tokens through the Keycloak administration API.

## Practice

### Platform: what JUDO gives and what it does not

- The runtime trusts Keycloak tokens and maps the token to the actor; it has no magic-link support of its own. The principal is resolved after login by claim (username, then e-mail, then the first identifier) and a missing row gives `AUTHENTICATED_ENTITY_NOT_FOUND` ([principal-to-actor resolution](../../agent-docs/backend/authentication-guide.md#principal-to-actor-resolution-and-multi-client-mapping)). The user row can be created on the first login with an `AuthenticationInterceptor` ([[keycloak-jit-user-provisioning]]).
- With management enabled the runtime registers a Keycloak admin client, realm synchronizer and user manager from OSGi configuration (`serverUrl`, `adminUser`, `adminPassword`, `managementEnabled`, `requiredActions` and others) ([Keycloak connector configuration](../../agent-docs/deployment/osgi-runtime-services.md#keycloak-connector-and-realm-synchronizer-configuration)). Check this before writing your own admin-client component; the platform's user manager may already cover user creation.
- Keycloak and the application database are two stores that drift apart; invitation and first-login flows must create the database row, not assume Keycloak membership implies it. Invitation e-mails from Keycloak use the SMTP settings the connector writes at start ([Keycloak users and the entity store](../../agent-docs/backend/platform-behavior-reference.md#keycloak-users-and-the-entity-store)).
- Several Keycloak clients in one realm must be whitelisted for the actor mapping ([acceptable clients](../../agent-docs/backend/authentication-guide.md#several-keycloak-clients-in-one-realm)).

### Practice notes: authenticator in Keycloak, services in the application

```java
// Example code, deployed INTO Keycloak (a Keycloak SPI, not a JUDO component)
public class MagicLinkAuthenticator implements Authenticator {
    @Override
    public void authenticate(AuthenticationFlowContext context) {
        String token = context.getHttpRequest().getUri().getQueryParameters().getFirst("token");
        if (token != null) {
            // validate the token, then context.success() for the user it belongs to
        } else {
            // challenge with the e-mail entry form
        }
    }
}

// Example code, application side (OSGi, runs in the JUDO runtime)
@Component(configurationPid = "...KeycloakFactoryComponent",
           configurationPolicy = ConfigurationPolicy.REQUIRE)
public class KeycloakFactoryComponent {
    // builds the Keycloak admin client from OSGi configuration: server URL, realm, admin user, client id
}
```

- **Two modules, two class loaders.** The authenticator (plus its token handling and REST endpoint) is a separate extension module deployed into the Keycloak server; the module that calls the admin API stays in the application. Do not share classes between them ([[osgi-karaf-bundle-architecture]]; see also [Keep the Keycloak extension separate](../../model-blueprints/keycloak-magic-link-passkey-authentication/backend.md)).
- **Configuration of the authenticator** (as named in the examples): token lifespan in seconds (default 300 in one example, one day in the other) and a flag that allows or forbids reuse. Defaults that allow reuse are a security trade-off: a link in a forwarded mail logs in again.
- **Application services**: a service that creates users, resets passwords and manages groups through the admin API, a token service (`generate`, `validate`), and an e-mail step that sends the link ([[email-service-integration]]).
- **OSGi class loading.** The Keycloak admin client needs a composite class loader inside OSGi; one application builds it in its factory.
- Never log the link or token.
- A second flow (passkeys through WebAuthn with a fallback to the password form) can sit next to the magic link in the same extension module; the full pattern is in [[keycloak-magic-link-passkey-authentication]].

## Rationale

- Passwordless sign-in improves usability and removes password storage from the application.
- It uses standard Keycloak extension points, so the JUDO side needs no custom login code.
- Cost: a custom artifact deployed into Keycloak with its own upgrade cycle, mail delivery latency in the login path, and reuse-of-token risk. Keycloak upgrades can break the extension.

## Example

A platform with invited users: an administrator creates a user through the application service (which calls the Keycloak admin API and sends an invitation e-mail with a magic link). The user opens the link, the authenticator validates the token and signs the user in; the runtime then resolves the actor from the token. A second variant adds an e-mail code authenticator and a continuation authenticator in the same extension module, and a browser flow that offers passkeys first.

## When to avoid

- When a standard Keycloak login (password, social login) is enough.
- When the application cannot deploy extensions into Keycloak (managed Keycloak hosting).
- When the application has no outbound e-mail that can be relied on at login time.
- For registration of unknown users: use [[two-phase-registration]] or provisioning on first login.

## Related

- [[keycloak-jit-user-provisioning]] — creates the application row after login
- [[two-phase-registration]] — code-based registration without an external IdP
- [[email-service-integration]] — sending the link
- [[multi-tenant-keycloak-realm]] — managing realms and users from the application
- [[keycloak-magic-link-passkey-authentication]] — the blueprint with the passkey variant
