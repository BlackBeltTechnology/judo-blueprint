---
id: "magic-link-authentication"
title: "Keycloak Magic Link Authentication Flow"
domain: "backend"
category: "auth"
score: 57.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - mlszksz-platform
  - ubives
---
## Description

A custom Keycloak authenticator that enables passwordless email-based login via magic links. The authentication flow generates a time-limited token, sends it via email with a login link, and authenticates the user when they click the link. The custom authenticator is deployed as a Keycloak SPI extension, with token management handled by a dedicated MagicLinkService in the application backend. The Keycloak admin client (KeycloakFactory) is integrated via OSGi for user and group management.

## Structure

```java
// Keycloak SPI Authenticator (deployed to Keycloak)
public class MagicLinkAuthenticator implements Authenticator {
    @Override
    public void authenticate(AuthenticationFlowContext context) {
        // Show email form or process magic link token
        String token = context.getHttpRequest().getUri()
            .getQueryParameters().getFirst("token");
        if (token != null) {
            // Validate token and authenticate user
        } else {
            // Show email entry form
        }
    }
}

// Application-side Keycloak client (OSGi component)
@Component(configurationPid = "...KeycloakFactoryComponent",
           configurationPolicy = ConfigurationPolicy.REQUIRE)
public class KeycloakFactoryComponent {
    // Creates Keycloak admin client from OSGi config
    // Provides: serverUrl, realm, username, password, clientId
}

// Magic link service
@Component(immediate = true, service = MagicLinkService.class)
public class MagicLinkServiceImpl implements MagicLinkService {
    String generateToken(String email);
    boolean validateToken(String token);
}
```

Configuration:
- `ext-magic-token-life-span`: Token lifespan in seconds (default: 300)
- `ext-magic-allow-token-reuse`: Allow token reuse (default: true)

## Examples

### mlszksz-platform
Custom `MagicLinkAuthenticator` deployed as Keycloak SPI extension. `KeycloakFactoryComponent` provides admin client via OSGi config. `KeycloakUserServiceImpl` manages users (create, reset password, manage groups) via Keycloak admin API. `MagicLinkServiceImpl` handles token generation/validation. Email sending via `PlatformEmailService.sendInvitationEmail()`. Token lifespan configurable (5 min default).

### Ubives
`MagicLinkAuthenticator`, `EmailOtpAuthenticator`, and `MagicLinkContinuationAuthenticator` deployed as Keycloak SPI extensions in a dedicated `keycloak-magic-link` module. `KeycloakFactory` provides admin client with `CompositeClassLoader` for OSGi compatibility. Supports WebAuthn passwordless flow alongside magic link. Custom `webauthn-browser-flow` with fallback to password form. Token lifespan configurable, default 1 day.

## Trade-offs

- Pros: Passwordless authentication (better UX), no credential management in application, standard Keycloak integration, configurable token lifespan
- Cons: Requires Keycloak deployment and SPI extension, email delivery latency affects login experience, token reuse can be a security concern, complex deployment (custom JAR in Keycloak)
- Alternative: Standard Keycloak password-based login, OIDC with social login providers, two-phase code registration (see `two-phase-registration`)

## Related Patterns

- keycloak-jit-user-provisioning
- two-phase-registration
- email-service-integration
