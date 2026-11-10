---
id: invitation-with-recipients
title: Invitation with Recipient Tracking
description: A batch invitation entity that owns one recipient entity per invited address, each with its own send time and verification window.
aliases: [bulk invitation, batch invitation, recipient list invitation]
keywords: [invitation, recipient, batch, bulk, tracking, sentAt, verification, expiry]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: [invitation-with-key-based-acceptance]
fragment: invitation-with-recipients
diagram: { kinds: [entity], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Invite a list of people in one action and keep track of each of them. One invitation groups the batch, with its message, creation time and creator. Each recipient is its own record, so the system can show when each was sent, whether its window has expired, and whether it was used.

### One invitation, many recipients

The batch is one entity and each address is one recipient entity. The recipients are composed by the invitation, so they go away with it.

### Each recipient has its own state

Sent time and verification expiry belong to the recipient, not to the batch. A batch may be partly sent, and each recipient can expire on its own schedule.

## Structure

The Invitation entity is non-CRUD. It has an optional message, a required creation timestamp and an optional recipient count. It has one required association to the creator, an Account. It composes zero or more InvitationRecipient entities. Each InvitationRecipient is non-CRUD, with a required email, an optional sent timestamp and an optional verification expiry timestamp. Invitations are created by custom operations, not by a generated create action.

## Constraints

- The invitation is non-CRUD. Creation happens in a custom operation that also creates the recipients.
- The creator is required, so every invitation names who sent it.
- Recipients are composed. A composition relation is owned by its parent and deleted with it, so deleting the invitation removes its recipients.
- Creation runs in a custom operation. The platform runs interceptors only for built-in operations, so permission checks on who may invite, and any audit, must be written inside that operation.
- A recipient's verification token is stored only as a hash, never in plain text. The plain token is sent once, by email. This is project practice (see [[token-based-verification-entity]]), not something the platform does for you.
- A recipient's verification window is checked on each use. An expired recipient is refused.
- A recipient is used at most once. After it is used, it must not be accepted again.

## Variations

- **Admin bulk invitation.** An administrator uploads a list of addresses. One invitation, one recipient per address.
- **Single-user invitation inside an organization.** One invitation with one recipient, created from the organization's admin panel.
- **Recipient-level verification.** Each recipient keeps its own token and expiry, as in the reference project.

## When to use

- A batch of people must be invited at once, and each must be tracked.
- The system must show per-recipient status: sent, expired, used.
- Invitations must be cancelable or removable as a group.

## When to avoid

- One key opens acceptance for anyone. Use [[invitation-with-key-based-acceptance]].
- The recipients are existing users who accept inside the app. A simple membership is enough.
- Per-recipient state is not needed. A single invitation entity is simpler.

## Related

- [[invitation-with-key-based-acceptance]] — a single key-based invitation accepted through a link
- [[token-based-verification-entity]] — the hashed-token verification each recipient uses
- [[user-with-organization-and-role]] — an organization user invited by an admin
