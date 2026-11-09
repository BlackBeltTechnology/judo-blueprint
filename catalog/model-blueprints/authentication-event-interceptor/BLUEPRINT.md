---
id: authentication-event-interceptor
title: Authentication Event Interceptor (Login Tracking)
description: "An authentication interceptor that runs on the principal lookup at login, to record the login time, write an audit entry, or create the user row on first login."
aliases: [login interceptor, principal interceptor, login tracking]
keywords: [authentication, login, interceptor, principal, last login, audit, provisioning]
tags: [domain:backend, layer:backend, project:mlszksz-platform, project:indamedia-adtrack, project:park-here, status:emerging]
category: pattern
status: emerging
projects: [mlszksz-platform, indamedia-adtrack, park-here]
evidence: ["mlszksz-platform:unrecorded", "indamedia-adtrack:unrecorded", "park-here:unrecorded"]
alternatives: [audit-log-entity]
fragment: none: backend-only
first_seen: 2026-03-09
last_updated: 2026-11-09
---
## Intent

Run side effects when a user logs in, such as recording the last login time, writing an audit entry, or creating the user row from the token on the first login. The work runs on the authentication path, not in a model operation, so it is written as an authentication interceptor.

### It runs on principal lookup, not on each call

The interceptor is attached to the authentication pipeline. It acts only when the principal is resolved (the principal operation), so it does not run again on every operation call.

### Failures do not block login

A side effect that fails must not stop the user from logging in. The interceptor catches and logs its own errors.

## Structure

This is a backend pattern with no model shape. An authentication interceptor is a component that the platform calls during authentication. It receives the operation name and the token attributes. It acts only for the principal operation, and it reads the email and name claims from the token. It writes to the user entity or to an audit service through injected references. The model is unchanged; the user entity must have the fields the interceptor writes, such as a last-login timestamp.

## Constraints

- The interceptor implements the authentication interceptor interface, not the operation call interceptor. The two have different scope and must not be mixed.
- The interceptor acts only when the operation name is the principal operation. Other operations are ignored.
- All side effects are wrapped so that an exception is logged and not rethrown.
- Creating the user row on first login must be safe under concurrent logins: two requests for the same new user must not create two rows.

## Variations

- **Login tracking.** Find the existing user by email and update the last-login time. Nothing is created.
- **Audit entry.** Write a login entry through an audit service, with the user identifier and email. See [[audit-log-entity]].
- **Auto-provisioning.** If no user exists for the email, create one from the token name claims. Assign roles from a configured list of administrator emails.
- **Platform-managed row.** If the actor is mapped and managed and declares claims in the model, the platform inserts and updates the principal row itself. In that case no interceptor is needed for the basic insert.

## When to use

- Login must update a timestamp, write a login audit entry, or create the user on first login.
- The work cannot be expressed in the model declaratively.
- The side effect may fail without blocking the login.

## When to avoid

- The model already creates or updates the principal from the token claims. Use the platform setting first.
- The side effect must succeed for the login to be valid. A failed side effect would then have to block login, which this pattern does not do.
- The rule applies to business operations, not to login. Use an operation call interceptor or an operation of its own.

## Related

- [[audit-log-entity]] — the audit record a login entry can be written to
- [[operation-call-logging-interceptor]] — logs built-in operation calls from an operation interceptor, a different scope
- [[safe-failure-pattern]] — the failure rule this interceptor follows
- [[keycloak-magic-link-passkey-authentication]] — an authentication flow that the login side effects can follow
