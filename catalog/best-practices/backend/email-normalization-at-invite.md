---
id: email-normalization-at-invite
title: Normalize E-mail at Every Entry Point
description: Trim and lowercase e-mail addresses with one shared helper at every boundary that creates or matches a user, so case variants cannot slip past duplicate checks or mismatch the identity server.
aliases: [email lowercase, normalizeEmail, case-insensitive invite, duplicate invitation guard]
keywords: [email, normalize, trim, lowercase, invitation, bulk invite, duplicate, StringFilter, equalTo, identity server, EmailUtils]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: operation
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/utils/EmailUtils.java", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/impl/UserServiceImpl.java"]
alternatives: [duplicate-detection-normalization]
related: [duplicate-detection-normalization, invitation-with-key-based-acceptance]
fragment: "none: backend-only"
first_seen: 2026-11-10
last_updated: 2026-11-10
---
## Intent

The same person typed as a padded mixed-case address and its lowercase form must be one user. Normalize (trim, lowercase) the address before it is stored, compared or sent to the identity server, so a duplicate check cannot be bypassed by case and the stored value matches the identity server's lowercase username.

## Practice

### Platform base

- Typed DAO string filters such as `StringFilter.equalTo` are used for exact matches, and `ilike` exists for case-insensitive matching ([DAO filters](../../agent-docs/backend/data-access-guide.md)). Whether `equalTo` is case-sensitive on the configured database is not stated in the agent-docs, *verify*; the example treats it as case-sensitive.
- The platform provides no e-mail normalization; it is plain application code.

### Practice notes: one helper, every boundary

This layer is a convention built on the platform, not a platform feature.

- One static helper `normalizeEmail(String)`: null stays null, otherwise `trim().toLowerCase()`. Keep it in the shared utils package with unit tests for mixed case plus whitespace, already normal, null, empty and blank.
- Call it at the entry of every service method that creates or matches a user: single invite, bulk invite (replacing an inline `trim().toLowerCase()`), re-invite (superseding a pending invitation), direct user creation, registration submission (all e-mail fields), and the lookup of the identity-server account.
- Also normalize inside the user-creation method, the chokepoint where all flows converge, even though entry points already did: intermediate entities (invitation requests, registration requests) need clean values for their own duplicate checks, and the chokepoint guarantees nothing mixed-case reaches the identity server.
- Forward-only: existing mixed-case rows are not migrated.
- Test through the runtime: mixed-case input is stored lowercase; the duplicate check catches case variants for verified users and for pending invitations; a re-invite supersedes across case variants; bulk lists are normalized; accepting an invitation creates the user with the normalized address.

```java
// Example code
public static String normalizeEmail(String email) {
    return email == null ? null : email.trim().toLowerCase();
}
String email = EmailUtils.normalizeEmail(rawEmail);   // first line of invite, inviteBulk, createUser, register
```

## Rationale

- Closes the duplicate-invitation hole and the login mismatch with the identity server in one place.
- Cost: every new entry point must remember to call the helper; the chokepoint call is the safety net.
- Lowercasing the whole address is a simplification (the local part is technically case-sensitive); it is the accepted trade-off for identity matching.

## Example

The helper `normalizeEmail` is called in the invitation, bulk invitation, user and registration services; a normalization test covers each path.

## When to avoid

- The database or filter already compares case-insensitively and the identity server keeps the original case: normalizing adds no value.
- Names rather than addresses need fuzzy matching: see [[duplicate-detection-normalization]].

## Related

- [[duplicate-detection-normalization]] — the same idea applied to names, with similarity
- [[invitation-with-key-based-acceptance]] — the invitation flow whose entry points call the helper
