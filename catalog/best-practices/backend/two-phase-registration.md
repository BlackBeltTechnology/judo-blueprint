---
id: two-phase-registration
title: Two-Phase Registration with Email Verification
description: A lightweight code-based registration flow in custom operations, where registration stores and e-mails a temporary code and activation checks it and promotes it to a permanent credential, as an alternative to an identity provider.
aliases: [email code registration, temporary code activation, code-based signup, registration with activation code]
keywords: [registration, activation, temporary code, email verification, tmpCode, invitation, custom operation, authentication, DAO query]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:ubives", "status:emerging"]
category: auth
status: emerging
projects: [trivia, ubives]
evidence: ["trivia:unrecorded", "ubives:unrecorded"]
alternatives: [keycloak-jit-user-provisioning]
related: [email-service-integration, typed-exception-error-handling, keycloak-jit-user-provisioning, magic-link-authentication, recaptcha-precall-interceptor, api-key-generation]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

For small applications an e-mail address is enough proof of identity. Registration creates (or updates) a user with a temporary code and mails the code. Activation verifies the code and stores a permanent code that later calls present instead of a token from an identity provider.

This is a convention built from custom operations and the DAO. It is not the platform's authentication. The platform authenticates through an external identity provider and an `AuthenticationInterceptor`, which resolves the principal to an actor ([Authentication Guide](../../agent-docs/backend/authentication-guide.md)). Use the pattern only where that route is not wanted, and read the weaknesses below first.

## Practice

### Phases

1. Register: generate a temporary code, create or update the user with `tmpCode`, send the code by e-mail ([[email-service-integration]]). A repeated registration for an existing user re-sends a code.
2. Activate: query the user by e-mail and temporary code. On a match, clear `tmpCode` and store the permanent `code`.
3. Authenticate on later calls: each protected custom operation takes e-mail and code as input, queries for a matching active user, and fails otherwise.

```java
Optional<User> user = userDao.query()
    .filterByEmail(StringFilter.equalTo(email))
    .filterByTmpCode(StringFilter.equalTo(code))
    .selectOne();
user.ifPresent(u -> {
    // clear the temporary code, store the permanent one, then update with a mask
});
```

`User`, `userDao` and the filter methods are generated for the example model; see [[dao-fluent-query-filter]] for the filters. To clear an optional attribute, check how the generated setter and mask treat `null` ([Absent, Null and Empty Are Different](../../agent-docs/backend/data-access-guide.md#absent-null-and-empty-are-different)).

### Platform constraints that matter

- The registration and activation operations must be reachable by a caller who has no identity yet. How that is modelled (an actor without authentication, or an access rule) is a model decision; check the authentication and access documentation before choosing, because a hidden UI button is no protection ([Which Operations Are Intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Custom operations are not intercepted, so abuse protection such as a captcha check must be written inside the operation, or placed in front of it ([[recaptcha-precall-interceptor]] covers built-in operations only).
- Failures (wrong code, expired code) should surface as a modeled fault or validation exception the client can show, not a generic runtime exception, which becomes a 500 ([How the Runtime Maps Exceptions to HTTP](../../agent-docs/backend/error-handling-guide.md#how-the-runtime-maps-exceptions-to-http), [[typed-exception-error-handling]]).

### Known weaknesses

A four-digit code can be brute-forced, the codes in the original examples do not expire, and nothing limits attempts. Add an expiry timestamp, an attempt counter and a long random code if you copy this. Prefer [[keycloak-jit-user-provisioning]] or [[magic-link-authentication]] when an identity provider is available.

## Rationale

- Simple, with no external identity provider and little code.
- Weaker than OAuth/OIDC: the permanent code is a shared secret that travels with each request.
- Variants with an admin step or a link instead of a code are in use, see the examples.

## Example

- One application: registration mails a 4-digit code through an SMTP provider. Activation verifies e-mail plus temporary code and stores a permanent `code`. A group entry authenticates with e-mail, code and an active flag. Existing users can request a new code.
- Another application: multi-step account registration: submit with reCAPTCHA validation, verify e-mail by token, an admin accepts or rejects, approval creates the account, the user and the identity-provider account. Invitations follow the same token, verify, accept shape.
- A third application: invitation-based registration. An admin invites a user or account; an invitation entity with a one-month expiry and an API-key-style id is created and mailed as a link. The user submits credentials, the accept operation checks them, creates the user and the identity-provider user, and deletes the invitation. User and account invitations differ in access level.

## When to avoid

- An identity provider is available: use the platform authentication flow.
- The data behind the account is sensitive: a mailed code is weak proof.
- You cannot add expiry and rate limiting.

## Related

- [[email-service-integration]] — sending the code
- [[typed-exception-error-handling]] — reporting a wrong or expired code
- [[keycloak-jit-user-provisioning]] — the platform-standard alternative
- [[magic-link-authentication]] — link instead of a typed code
- [[recaptcha-precall-interceptor]] — abuse protection for registration
- [[api-key-generation]] — generating the random key or code
