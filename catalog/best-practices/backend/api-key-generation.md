---
id: "api-key-generation"
title: "SecureRandom API Key Generation Pattern"
domain: "backend"
category: "service"
score: 44.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - ubives
---
## Description

A utility pattern for generating random alphanumeric API keys using `java.security.SecureRandom`. The generated keys are 32 characters long and used as application tokens, invitation IDs, and temporary realm names. The pattern is implemented as a static utility class with no external dependencies, ensuring cryptographically strong randomness.

## Structure

```java
public class ApiKeyGenerator {
    private static final SecureRandom RANDOM = new SecureRandom();
    private static final String CHARACTERS =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    public static String generateApiKey() {
        StringBuilder sb = new StringBuilder(32);
        for (int i = 0; i < 32; i++) {
            int randomIndex = RANDOM.nextInt(CHARACTERS.length());
            sb.append(CHARACTERS.charAt(randomIndex));
        }
        return sb.toString();
    }
}
```

Usage contexts:
- Application tokens: `withApplicationToken(ApiKeyGenerator.generateApiKey())`
- Invitation IDs: `withInvitationId(ApiKeyGenerator.generateApiKey())`
- Temporary realm names: used during organization creation before renaming to organization name

## Examples

### Ubives
`ApiKeyGenerator.generateApiKey()` used in three contexts: (1) `ApplicationService.createApplication()` generates tokens for new applications, (2) `InviteService.invite()` generates unique invitation IDs for email invite links, (3) `OrganizationService.createOrganization()` generates temporary realm names. Static utility class in `com.ubives.ubives.services` package. No expiration or rotation mechanism built in.

## Trade-offs

- Pros: Cryptographically strong randomness via SecureRandom, simple static utility, no external dependencies, sufficient entropy (62^32 possible keys)
- Cons: No built-in expiration or rotation, no collision detection, not UUID-based (harder to trace), 32-char alphanumeric may not meet all API key standards
- Alternative: `UUID.randomUUID().toString()` for standard UUID format, JWT-based tokens for self-contained claims, external token service (Vault, AWS KMS)

## Related Patterns

- two-phase-registration
- service-delegation-pattern
