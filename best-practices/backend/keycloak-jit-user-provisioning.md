---
id: "keycloak-jit-user-provisioning"
title: "Keycloak Just-In-Time User Provisioning via AuthenticationInterceptor"
domain: "backend"
category: "auth"
score: 59.0
usage_count: 5
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - alba
  - mlszksz-platform
  - ubives
  - park-here
  - indamedia-adtrack
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
        String email = (String) attributes.get("preferred_username");
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

## Trade-offs

- Pros: No manual user registration required, seamless SSO experience, default approval status prevents unauthorized access, idempotent
- Cons: Trusts Keycloak token blindly (no signature verification at this level), user attributes may not be present in all token configurations, no role mapping from Keycloak groups
- Alternative: Two-phase email registration (see `two-phase-registration`) for applications without external IdP

## Related Patterns

- two-phase-registration
- actor-resolution-variable-resolver
- dao-fluent-query-filter
