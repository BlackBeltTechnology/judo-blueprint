---
id: "two-phase-registration"
title: "Two-Phase Registration with Email Verification"
domain: "backend"
category: "auth"
score: 64.7
usage_count: 3
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - mlszksz-platform
  - ubives
alternatives:
  - keycloak-jit-user-provisioning
---
## Description

A lightweight custom authentication flow using two phases: (1) Registration generates a temporary code and sends it via email, (2) Activation verifies the code and promotes it to a permanent credential. This avoids the complexity of full OAuth/JWT flows for simple applications where email-based identity is sufficient.

## Structure

Phase 1 - Register:
```java
String tmpCode = String.format("%04d", rand.nextInt(10000));
// Create or update user with tmpCode
// Send email with tmpCode
```

Phase 2 - Activate:
```java
Optional<User> user = userDao.query()
    .filterByEmail(StringFilter.equalTo(email))
    .filterByTmpCode(StringFilter.equalTo(code))
    .selectOne();
// If match: clear tmpCode, set permanent code field
user.get().setTmpCode(null);
user.get().setCode(input.getCode());
```

Phase 3 - Authenticate on action:
```java
userDao.query()
    .filterByEmail(StringFilter.equalTo(email))
    .filterByCode(StringFilter.equalTo(code))
    .filterByActive(BooleanFilter.isTrue())
    .selectOne();
```

## Examples

### Trivia
Register sends a 4-digit code via Mailjet SMTP to the player's email. Activate verifies email+tmpCode, promotes to permanent `code` field. Contest entry authenticates via email+code+active flag. Supports re-registration (code resend) for existing users.

### mlszksz-platform
Multi-phase organization registration: (1) submit registration with reCAPTCHA validation, (2) verify email via token, (3) admin accepts/rejects request, (4) approval creates Organization+User+Keycloak account. Invitation flow: invite with token, verify token, accept/reject invitation creating User entity. More sophisticated than Trivia's approach with admin approval step and Keycloak integration.

### Ubives
Invitation-based registration: (1) admin invites user/account with email, creating Invitation entity with 1-month expiration and API-key-based invite ID, (2) invitation email sent via SendGrid with magic link URL, (3) user clicks link and submits username/password, (4) AcceptInvitation validates passwords match, creates User or Account entity with Keycloak user, deletes invitation. Differentiates USER vs ACCOUNT invitation types with different access levels.

## Trade-offs

- Pros: Simple, no external IdP dependency for basic use, lightweight code-based auth
- Cons: Not as secure as OAuth/JWT, 4-digit code is brute-forceable, no expiry on codes, no rate limiting
- Alternative: Keycloak integration with AuthenticationInterceptor for JIT provisioning (more secure, standard)

## Related Patterns

- email-service-integration
- typed-exception-error-handling
- keycloak-jit-user-provisioning
