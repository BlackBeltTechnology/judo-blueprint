---
id: "moderation-operation-pattern"
title: "Moderation Delete Operation Pattern"
domain: "model"
category: "operation"
score: 13.1
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - mlszksz-platform
---
## Description

Content entities expose a separate `moderationDelete` operation alongside the regular `delete` operation. The moderation variant accepts an input transfer object with a reason field, creates a specific audit trail entry (distinct from regular deletion), and may have different permission requirements. This pattern separates user-initiated deletion from administrative moderation actions.

## Structure

- Content entity has two delete paths:
  - `delete`: Regular delete by content owner, creates standard audit entry (e.g., POST_DELETED)
  - `moderationDelete`: Admin/moderator delete with reason, creates moderation-specific audit entry (e.g., POST_MODERATION_DELETED)
- `moderationDelete` accepts an input TO with a `reason` field
- Both operations transition the entity to the same DELETED status
- Audit log distinguishes the two paths via separate AuditActionType members
- Moderation operations are typically accessible only to PLATFORM_ADMIN or higher roles

## Examples

### MLSZKSZPlatform
Three content entities have dual delete paths: `News.delete` + `News.moderationDelete`, `Offer.delete` + `Offer.moderationDelete`, `Request.delete` + `Request.moderationDelete`. The `moderationDelete` operations accept an input TO with a reason parameter and create `POST_MODERATION_DELETED` audit entries (distinct from `POST_DELETED`). All moderation operations are exposed through the `companyadmin` service package. Regular `delete` operations are parameterless bound operations.

## Trade-offs

- Pros: Clear separation of user vs admin actions, moderation reasons preserved for accountability, distinct audit trail for compliance
- Cons: Duplicates delete logic (two operations per entity), adds complexity to the operation surface
- Prefer when: Content management systems where administrative moderation must be tracked separately from user actions

## Related Patterns

- [audit-event-entity](audit-event-entity.md) (distinct audit entries for moderation actions)
- [enum-state-machine](enum-state-machine.md) (both paths lead to DELETED status)
- [soft-delete-active-flag](soft-delete-active-flag.md) (status-based soft delete preserves moderated content)
