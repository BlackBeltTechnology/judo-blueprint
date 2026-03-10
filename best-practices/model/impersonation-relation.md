---
id: "impersonation-relation"
title: "Impersonation Relation for Admin-on-Behalf-of Actions"
domain: "model"
category: "relation"
score: 42.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - alba
---
## Description

An entity includes a separate optional relation to a User entity specifically for recording when an administrator performs actions on behalf of another user. This "impersonating" relation is distinct from the primary ownership relation (e.g., `author`), allowing the system to track both the true author and the admin who uploaded content in their name. This supports administrative workflows where admins create or manage content for other users.

## Structure

- Entity has a primary ownership relation (e.g., `author [0..1] -> User`)
- Entity has a separate impersonation relation (e.g., `impersonatingAuthor [0..1] -> User`)
- The impersonation relation is one-way (no partner) and stored
- Both relations point to the same target entity type (User)
- Admin transfer objects expose the impersonation relation; non-admin transfers do not
- The primary author is auto-set via actor context; impersonating author is set explicitly by admin

## Examples

### Alba
`Product.impersonatingAuthor [0..1] -> User` is a one-way stored association, documented as "Admins can upload content in the name of other teachers." This is separate from `Product.author [0..1] -> User` (the actual author, auto-defaulted to current user). `AdminProduct` transfer exposes both relations, while `AuthorProduct` only exposes `author`. This allows admin-created products to be attributed to the correct teacher.

## Trade-offs

- Pros: Clear separation of true author and admin actor, supports "on behalf of" workflows, audit-friendly
- Cons: Additional relation to maintain, requires admin-specific UI for selection, may cause confusion if both are set
- Prefer when: Admin users need to create or manage content attributed to other users in the system

## Related Patterns

- [actor-context-variable-lookup](actor-context-variable-lookup.md) (primary author set via actor context)
- [actor-based-transfer-projection](actor-based-transfer-projection.md) (impersonation exposed only to admin transfers)
