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
last_updated: 2026-11-10
---
## Intent

Run side effects when a user logs in, such as recording the last login time, writing an audit entry, or creating the user row from the token on the first login. The work runs on the authentication path, not in a model operation, so it is written as an authentication interceptor.

### It runs on principal lookup, not on each call

The interceptor is attached to the authentication pipeline. The platform calls it on the framework-level `#_principal` operation after a successful external login, with the token claims in the `attributes` map. It runs before the framework loads the mapped principal row, so it can insert or update the row that the lookup is about to read. It acts only for that operation; the interceptor itself filters on the operation name. It is not an operation call interceptor and does not see ordinary operation calls.

### Failures do not block login

A side effect that fails must not stop the user from logging in. The interceptor catches and logs its own errors. This is the platform guide's recommended default; throwing from `authenticate` is allowed only when blocking the login is intended.

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
- **Platform-managed row (documented, not working).** The model docs describe an actor that is mapped, managed and declares `<claims>` as inserted and updated by the runtime. The agent-docs record that this auto-insert does not happen in the verified runtime versions: the actor lookup throws `AUTHENTICATED_ENTITY_NOT_FOUND` for an unknown user. Until a release ships it, provide this interceptor for the first-login insert even for that actor shape. Keep the existence check, so the interceptor becomes a no-op if the runtime starts inserting. The `<claims>` element covers only email and username; other claims (roles, groups, custom attributes) always need the interceptor.

## When to use

- Login must update a timestamp, write a login audit entry, or create the user on first login.
- The work cannot be expressed in the model declaratively.
- The side effect may fail without blocking the login.

## When to avoid

- The runtime itself creates and updates the principal from the declared claims. The agent-docs say this does not work in the verified versions, so check it on your runtime version before dropping the interceptor.
- The rule is an authorization decision. Use the access model, not an authentication interceptor.
- The side effect must succeed for the login to be valid. A failed side effect would then have to block login, which this pattern does not do.
- The rule applies to business operations, not to login. Use an operation call interceptor, which sees built-in operations only, or put the logic inside the custom operation: custom, mapped and script operations are never intercepted.

## Related

- [[audit-log-entity]] — the audit record a login entry can be written to
- [[operation-call-logging-interceptor]] — logs built-in operation calls from an operation interceptor, a different scope
- [[safe-failure-pattern]] — the failure rule this interceptor follows
- [[keycloak-magic-link-passkey-authentication]] — an authentication flow that the login side effects can follow
