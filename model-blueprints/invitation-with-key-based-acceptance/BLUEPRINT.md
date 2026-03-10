---
id: "invitation-with-key-based-acceptance"
title: "Invitation Entity with Key-Based Acceptance Flow"
score: 44.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - ubives
---
## Description

An Invitation entity that implements an invitation workflow using cryptographic keys (public/private key pair) rather than simple verification tokens. The invitation carries:

- **invitationType** -- an enum (USER/ACCOUNT) distinguishing whether the invitation is for a new organization-scoped user or an existing platform account to join an organization
- **email** -- the invitee's email address
- **expiration** -- when the invitation expires
- **inviteId** -- a unique identifier for the invitation link
- **invitePrivateKey / invitePublicKey** -- a cryptographic key pair for secure invitation verification
- **Feature support flags** -- isApplicationFeatureSupported, isOrganizationFeatureSupported (with defaults of false) that determine what the invitee can access after joining

The invitation is composed by an Organization (0..* COMPOSITION) and has a derived back-reference to it. Operations include acceptInvitation (triggered when the invitee clicks the link and provides credentials) and cancelInvitation (for revoking pending invitations). The accept operation takes an AcceptInvitationLinkParameter unmapped TO with userName, firstName, lastName, password, and passwordAgain fields for account creation.

An InvitationType enum (USER/ACCOUNT) discriminates the two invitation flows: USER invitations create a new user scoped to the organization, while ACCOUNT invitations grant an existing platform account access to the organization.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
