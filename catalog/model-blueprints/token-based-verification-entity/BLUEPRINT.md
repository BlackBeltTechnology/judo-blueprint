---
id: token-based-verification-entity
title: Token-Based Verification Entity
description: An entity that confirms a request through a one-time token, with a stored token hash, an expiry time, a verified-at time, and a status enumeration that moves from pending to verified and then to approved, rejected or expired.
aliases: [verification request, invitation token entity]
keywords: [token, verification, expiry, hash, status, invitation]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: [code-based-player-authentication]
related: [code-based-player-authentication, invitation-with-recipients, invitation-with-key-based-acceptance]
fragment: token-based-verification-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Confirm that a request really comes from the person who received a one-time token by email. The entity keeps the request until a reviewer decides, and it expires the token after a set time.

### The token is not stored in plain text

The plain token goes only to the email. The entity stores a hash of it, so a leaked table does not expose usable tokens. Verification hashes the incoming token and compares it with the stored hash.

### Status records the step, the timestamps record the time

The status enumeration says where the request is in the process. The expiry and verified-at timestamps say when the token expires and when verification happened.

## Structure

The VerificationRequest entity has a stored token hash, an expiry timestamp, a verified-at timestamp, a required status (VerificationStatus enumeration: Pending, Verified, Approved, Rejected, Expired), and an email. The status starts at Pending. Verification moves it to Verified. A reviewer then moves it to Approved or Rejected. A request whose token has expired becomes Expired.

## Constraints

- The stored value is a hash. The plain token exists only in the email and in the request that the recipient sends back.
- Verification checks, in order: the status is Pending, the hash matches, and the token has not expired. Then it sets Verified and the verified-at time.
- Approval and rejection are allowed only from Verified.
- A failed check raises a modeled fault, declared on the operation in the model (HTTP 422 with an `X-Fault` header). A bad field value raises the platform validation exception (HTTP 400). See [Error handling](../../agent-docs/backend/error-handling-guide.md#modeled-faults).
- Interceptors do not run for custom operations ([Interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). The verification and decision operations must carry their own checks.

## Variations

- **Separate registration and invitation requests.** Two entities with the same token fields, one for new organizations and one for users invited into an existing organization. The example uses this split.
- **Expiry as a status.** Mark the request Expired by a scheduled job instead of checking the timestamp on each call. The job must run before anyone reads the status.
- **Single entity for both flows.** Put both flows in one entity with a request type attribute. This is simpler, but the statuses then carry both meanings.

## When to use

- A user must prove ownership of an email address before a request can be processed.
- A reviewer must decide on a request after verification, and the decision must be recorded.
- Tokens must expire, and a leaked table must not expose valid tokens.

## When to avoid

- The entity is only a short code shown on screen, with no email step. See [[code-based-player-authentication]].
- The request is an invitation that a recipient accepts with a key, and no review step exists. See [[invitation-with-key-based-acceptance]].
- Several recipients share one invitation. See [[invitation-with-recipients]].

## Related

- [[code-based-player-authentication]] — a short code confirmation without an email token or hash
- [[invitation-with-recipients]] — an invitation sent to several recipients
- [[invitation-with-key-based-acceptance]] — an invitation accepted with a key
