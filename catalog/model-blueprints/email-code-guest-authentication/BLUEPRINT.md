---
id: email-code-guest-authentication
title: Email Code Guest Authentication with Registration Flow
description: A lightweight sign-in pattern for anonymous or semi-anonymous users where access is granted with a short code sent by e-mail, instead of a full username and password flow.
aliases: [code-based-player-authentication, code-based authentication, email code registration, pin activation]
keywords: [code, activation, registration, e-mail code, tmpCode, unmapped transfer object, static operation]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:trivia, status:single-project]
category: pattern
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: [token-based-verification-entity, keycloak-magic-link-passkey-authentication]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let a user who has no full account enter the application with an e-mail address and a short code. The code is the only credential. Registration and activation are two static operations on an unmapped transfer object that a dedicated actor reaches, so no identity provider is needed. The fragment models the transfer objects only. Which actor exposes them, for example an anonymous actor (`anonymous = true` marks an unauthenticated guest), is a project choice.

### Activation promotes a pending code

Registration stores a pending code on the user. Activation compares the e-mailed code with the pending code and, when they match, promotes it to the active code. The pending code is then cleared.

### Registration is idempotent per e-mail

Registering an e-mail that already exists updates the user and issues a new pending code. It does not fail. The user is looked up by e-mail, never created twice.

## Structure

The User entity is non-CRUD and holds an e-mail (required), a name, an active flag (required, default true), an active code and a pending code (tmpCode). Both codes are plain strings. The User has a reset operation that regenerates the active code. A separate Admin entity has an e-mail (required) and an active flag (required, default true); it is not the same type as User.

Two unmapped transfer objects carry the flow. RegisterInput has an e-mail (required) and an optional name. Credential has an e-mail (required) and a code (required). An application transfer object (the entry point for the end-user actor) exposes two static operations, register and activate.

## Constraints

- The User and Admin entities are not createable, updateable or deleteable through generated actions. Changes go through the register, activate and reset operations.
- The active code is never shown to another user. Only the pending code is sent by e-mail.
- Activation fails with one generic error for an unknown e-mail and for a wrong code. The two cases must not be distinguishable to the caller.
- Interceptors run only on built-in operations. Register, activate and reset are custom operations, so each one checks its own rules and writes its own audit trail if needed.
- The actor that calls register and activate must be public: `anonymous` set and no principal mapped. With a mapped principal it needs a token even when flagged anonymous ([access points](../../agent-docs/model/esm_metamodel/accesspoint.md)).
- Static operations are the only kind an unmapped transfer object allows, which is why register and activate are static.
- The generic activation fault is a modeled fault transfer object. Every operation that throws it must declare it in `faults`, or the generated interface has no matching `throws` clause.

## Variations

- **Code length and format.** A 4-digit numeric code keeps entry on a phone simple. A longer random code raises the cost of guessing; add an attempt limit when the code is short.
- **Pending code with an expiry.** Store the time the pending code was issued and reject activation after a window. This is a small step toward [[token-based-verification-entity]].
- **Passwordless sign-in with a provider.** When sign-in must be standard, use an identity provider instead. See [[keycloak-magic-link-passkey-authentication]].

## When to use

- Users are consumers or participants who should join with only an e-mail address.
- Full account management, password recovery and federation are not needed.
- The codes are short-lived and used once, and the application can tolerate a simple code model.

## When to avoid

- Accounts need password policies, MFA, federation or single sign-on.
- Codes must expire, be single-use with a record, or be audited per attempt. Use [[token-based-verification-entity]] instead.
- Any administrative actor must sign in. Admins belong to a separate actor with a stronger sign-in.

## Related

- [[token-based-verification-entity]]: the same verification idea with its own token entity, expiry and e-mail template
- [[keycloak-magic-link-passkey-authentication]]: the identity-provider route when standard sign-in is needed
- [[invitation-with-key-based-acceptance]]: key-based acceptance of an invitation, a related shape
- [[credential-generalization-hierarchy]]: how different credential kinds are modeled as one hierarchy
- [[authentication-event-interceptor]]: recording authentication events for built-in operations
- [[safe-failure-pattern]]: when a failed side effect such as sending the e-mail must not undo the business change
