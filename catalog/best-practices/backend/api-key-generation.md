---
id: api-key-generation
title: SecureRandom API Key Generation Pattern
description: "A static utility generates 32-character alphanumeric keys with java.security.SecureRandom for application tokens, invitation ids and temporary names; storage, expiry and rotation are left to the caller."
aliases: [random token generator, invitation id generator]
keywords: [securerandom, api key, token, random, invitation, utility]
tags: ["domain:backend", "layer:backend", "project:ubives", "status:single-project"]
category: service
status: single-project
projects: [ubives]
evidence: ["ubives:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Backend code sometimes needs an unguessable string: an application token handed to an integration, an invitation id embedded in an e-mail link, or a throwaway name used while a record is being created. A small utility around `SecureRandom` produces such values without any dependency.

## Practice

The platform has no key generator for this: signed identifiers are minted by the runtime only when it serves a response and cannot be produced by custom code ([signed identifiers](../../agent-docs/backend/platform-behavior-reference.md#signed-identifiers)), and variable providers or sequences give environment values or numbers, not secrets ([variables and sequences](../../agent-docs/backend/platform-behavior-reference.md#variables-and-sequences)). An application secret is therefore a practice built on the platform: a plain Java utility class that service classes call.

```java
// Example code (a static utility, not a platform class)
public class ApiKeyGenerator {
    private static final SecureRandom RANDOM = new SecureRandom();
    private static final String CHARACTERS =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    public static String generateApiKey() {
        StringBuilder sb = new StringBuilder(32);
        for (int i = 0; i < 32; i++) {
            sb.append(CHARACTERS.charAt(RANDOM.nextInt(CHARACTERS.length())));
        }
        return sb.toString();
    }
}
```

- Use `SecureRandom`, never `java.util.Random`, and keep one shared instance.
- The generated value is then written through the generated builder, for example an application token or an invitation id field on the created entity.
- The utility does not check for collisions, expire keys or rotate them. Add a unique constraint or a lookup before storing when a collision would matter, and model an expiry or revoked flag if keys must be time-limited.
- For secrets that are checked later, store only a hash of the value, as in [[invitation-with-recipients]].

## Rationale

- Thirty-two characters from 62 symbols give about 190 bits of entropy, enough that guessing is impractical.
- A static class with no dependencies is trivial to reuse from any service and to unit test (length, alphabet).
- Cost: no standard format (a UUID may be easier to trace), no built-in lifecycle.

## Example

One application uses the generator in three places: an application service creates tokens for new applications, an invite service creates the ids used in e-mail invitation links, and the account service creates a temporary realm name that is replaced by the account name once registration completes.

## When to avoid

- When a standard UUID is enough and the value is an identifier, not a secret: `UUID.randomUUID()`.
- When keys need expiry, scopes or rotation: use a token service or a model with explicit lifecycle fields.
- When login is the goal: delegate to the identity provider ([[magic-link-authentication]]).

## Related

- [[two-phase-registration]] — registration flow where temporary names are used
- [[service-delegation-pattern]] — where the generator is called from
- [[magic-link-authentication]] — another use of single-use tokens
- [[invitation-with-recipients]] — stores only hashes of generated tokens
