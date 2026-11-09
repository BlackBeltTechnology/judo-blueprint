---
id: "privacy-visibility-enum"
title: "Privacy Visibility Enum (Granular Data Visibility Levels)"
score: 33.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - sanctuary-backend
---
## Description

An enumeration representing granular visibility levels for user data fields. Instead of a binary public/private toggle, this enum provides multiple scoping levels that control who can see a particular piece of user information. The levels form an expanding hierarchy of visibility:

- **publicForPeers** -- visible only to direct peers (closest circle)
- **publicForTeam** -- visible to the user's team members
- **publicForUnit** -- visible to the user's organizational unit
- **publicForEveryone** -- visible to all users in the system

This enum is typically used as the data type for multiple attributes on a UserPrivacySettings entity (composed by the User entity), where each attribute controls the visibility of a specific user data field (e.g., phone number, badges). This enables per-field privacy control rather than a single global privacy setting.

The scoping levels assume an organizational hierarchy (peer < team < unit < everyone) and are suitable for enterprise or community platforms where users belong to nested organizational structures.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
