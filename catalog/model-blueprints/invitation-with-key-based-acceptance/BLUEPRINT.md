---
id: invitation-with-key-based-acceptance
title: Invitation Entity with Key-Based Acceptance Flow
description: An invitation entity that is accepted through a link carrying an unguessable key, so the invitee can accept without a prior account.
aliases: [invite link, key invitation, anonymous invitation acceptance]
keywords: [invitation, key, acceptance, invite link, expiration, anonymous, accept, cancel]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:ubives, project:mlszksz-platform, status:emerging]
category: pattern
status: emerging
projects: [ubives, mlszksz-platform]
evidence: ["ubives:unrecorded", "mlszksz-platform:model/MLSZKSZPlatform.model"]
alternatives: [invitation-with-recipients]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let someone who has no account yet accept an invitation. The invitation is an entity with an email, an expiration and a key. The key is carried in a link, so the invitee can open the link and accept without first signing in. On the platform this is an actor marked anonymous (an unauthenticated guest) whose access reaches the link transfer object; the key scheme itself is common practice, not a platform feature. Accepting or cancelling is an operation on the invitation, and the link itself is a transfer object that exposes only what the invitee needs.

### The key is the access credential

Possession of the key is what allows acceptance. The key is random and long enough that it cannot be guessed. The invitation expires, so an old link stops working.

### Acceptance is an operation on the invitation

Accept and cancel are operations on the invitation entity. The invitee reaches them through the link transfer object, not through a generic create form.

## Structure

The Invitation entity is non-CRUD (not createable, updateable or deleteable through generated actions). It holds a required invitation type (an enumeration with USER and ACCOUNT values), a required email, a required expiration timestamp, and an optional invite identifier. Two operations sit on it, accept and cancel. Two transfer objects shape the access: a link transfer object that maps the invitation's fields for the invitee, and an accept parameter transfer object that carries the new user's password and its confirmation. The enumeration says whether the invitation adds a new user or an existing account to an organization.

## Constraints

- The invitation is non-CRUD: create, update and delete do not happen through generated actions. Invitations are created by dedicated operations.
- The invitation type is required and must be one of the enumeration values.
- The password and its confirmation are transient parameters, not stored attributes.
- The key must be random and unguessable. A short or sequential key lets anyone accept invitations.
- Accept and cancel are custom operations. The platform runs interceptors only for built-in operations (create, update, delete, list, refresh and the like), never for custom, MAPPED or script operations, so any audit, permission check or side effect must be written inside the operation. Hiding a button protects nothing.
- The actor is public only when `anonymous` is set and no principal is mapped; an actor with a mapped principal needs a token even when flagged anonymous ([access points](../../agent-docs/model/esm_metamodel/accesspoint.md)).
- The anonymous actor reaches the invitation only through the link transfer object. The key and expiration checks are the only protection, and they run in the operation, not in the platform.
- The invitation has an expiration. An expired invitation must be refused at accept time.

## Variations

- **Accept for a new user.** The invitation type is USER. Acceptance creates a user with the password from the accept parameter.
- **Accept for an existing account.** The invitation type is ACCOUNT. Acceptance adds the existing account to the organization and needs no new password.
- **Re-invite supersedes a pending invitation.** Inviting an address that already has a pending invitation deletes the old one and creates the new one, so the old key stops working. An invitation the invitee already verified is not superseded; the new invite is refused. See the backend guidance.
- **Invitee must be a Keycloak user.** The generated realm leaves self sign-up off (see `multi-tenant-keycloak-realm`), so an anonymous actor cannot accept the key without an account. The model has no setting for self sign-up, so enable it on the realm through the Keycloak admin console or admin API. Then let the invitee register first, then accept the key as the signed-in actor.
- **Cancel.** The inviter or an administrator cancels a pending invitation. Cancel deletes it.

## When to use

- A new user or a partner must join without an account first.
- An invitation link is sent by email and must work from the email alone.
- Invitations must expire and be cancellable.

## When to avoid

- Recipients are known users who can sign in and accept from inside the app. A simpler flow fits.
- The invitation must be sent to a list of recipients with per-recipient state. See [[invitation-with-recipients]].
- The key would be sent in a place where others can read it, such as a shared log.

## Related

- [[invitation-with-recipients]]: invitations to a recipient list with per-recipient status
- [[email-code-guest-authentication]]: key-based acceptance of an invitation for an end user
- [Two-phase registration](../../best-practices/backend/two-phase-registration.md), registration with email verification, the same link-based idea
