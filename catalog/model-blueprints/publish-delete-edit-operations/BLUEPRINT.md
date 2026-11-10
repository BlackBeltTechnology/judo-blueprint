---
id: publish-delete-edit-operations
title: Publish, Delete and Edit Content Operations
description: "Instance operations on a content transfer object that run an editorial workflow: publish moves a draft to published, delete removes it or marks it deleted, and an edit operation changes content without touching its status."
aliases: [content publish operations, editorial workflow operations]
keywords: [publish, delete, edit, content, status, instance operation, custom operation]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: []
fragment: publish-delete-edit-operations
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Give editors a fixed set of state-changing actions on a content item. Each action is an instance operation on the content's transfer object, so the UI can call it on the item the user is looking at, and each one checks the current status before it changes anything.

### Each action checks the current status first

Publish accepts only drafts. Delete and edit reject a content item that is already deleted. The status check belongs in the operation, not in the caller, because the operation is the only place every caller passes through.

### Delete depends on the status

A draft has never been visible, so delete can remove it physically. A published item may be referenced elsewhere, so delete marks it with the deleted status and keeps the row.

## Structure

The content entity has a required title, a required status (an enumeration with the values DRAFT, PUBLISHED and DELETED), and an optional published-at timestamp. Its transfer object exposes three instance operations: publish, delete and an edit operation for the content (named after the content type, for example editNews). Each operation is a custom operation, so its behaviour is written in the backend. Guard flags on the transfer object (for example "is not publishable" or "is not deletable") are derived from the status and drive button visibility.

## Constraints

- Publish is allowed only from DRAFT. It sets PUBLISHED and records the publish time in the same transaction.
- Delete of a DRAFT removes the row. Delete of a PUBLISHED item sets DELETED. Delete of a DELETED item is rejected.
- Edit keeps the current status. It is allowed only while the item is DRAFT in the example project.
- Guard flags are derived from the status. They are for display only; the operation still checks the status.
- Interceptors run only for built-in operations, so custom operations get none. Each operation performs its own checks and writes its own audit row if one is required.

## Variations

- **Expiry as a fourth action.** Time-sensitive content adds an expire operation that moves PUBLISHED to EXPIRED. See [[content-lifecycle-status-enum]] for the status values.
- **Moderation delete.** An administrator removes content with a reason and notifies the owner. Authorization is checked in the operation, not in the UI.
- **Status-only enumeration.** When the only action is a status change, use [[draft-done-status-enum]] instead of three operations.

## When to use

- Content moves through draft, published and removed states that editors control.
- The same three actions repeat across several content types.
- Hard delete of drafts and soft delete of published items is the required behaviour.

## When to avoid

- The status changes come from a machine process only. Use the state-transition pattern in [[post-generalization-hierarchy]] or a scheduled job.
- Publish needs an approval step by a second person. Use [[product-with-approval-workflow]].
- Users must restore deleted items. A plain delete status is not enough; keep a history instead.

## Related

- [[content-lifecycle-status-enum]] — the DRAFT, PUBLISHED and DELETED values these operations move between
- [[draft-done-status-enum]] — a simpler status set without soft delete
- [[product-with-approval-workflow]] — a publish step that needs approval
- [[post-generalization-hierarchy]] — the shared post hierarchy these operations often sit on
- [[accept-reject-operations]] — the same custom-operation pattern for review decisions
