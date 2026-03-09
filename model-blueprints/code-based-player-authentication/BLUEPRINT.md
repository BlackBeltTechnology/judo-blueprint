---
id: "code-based-player-authentication"
title: "Code-Based Player Authentication with Registration Flow"
score: 39.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - trivia
---
## Description

A lightweight authentication pattern for anonymous or semi-anonymous users (players, participants) where access is controlled via a temporary code rather than a full username/password authentication flow. The User entity carries a `code` attribute (the active access code) and a `tmpCode` attribute (a pending code awaiting activation). A separate Admin entity represents the privileged actor with email and active attributes.

The registration flow uses unmapped transfer objects:
1. **RegisterInput** TO: email (req) + name -- the player provides their email and optional name
2. The backend generates a temporary code and stores it in `tmpCode` on the User entity
3. **Credential** TO: email (req) + code (req) -- the player provides their email and the code they received
4. **Application.activate** operation validates the code against tmpCode and promotes it to the active `code`
5. The User entity has a `reset` operation to regenerate the code (e.g., if forgotten)

The Player actor accesses the system through an Application transfer object with `register` (STATIC) and `activate` (STATIC) operations. This pattern avoids the complexity of OAuth/Keycloak integration for simple consumer-facing applications where email-based code verification is sufficient.

This is similar to the token-based verification pattern but simpler: there is no dedicated Token entity, no expiry tracking, and no email template system. The code is stored directly on the User entity.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
