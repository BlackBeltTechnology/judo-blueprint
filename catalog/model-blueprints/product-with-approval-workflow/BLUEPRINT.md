---
id: product-with-approval-workflow
title: Product Entity with Draft/Finalize/Approve Workflow and Versioning
description: "A content item that moves through DRAFT, FINALIZED and APPROVED states by custom operations, keeps a version history, assigns approval tasks and logs events."
aliases: [approval workflow, versioned product]
keywords: [product, draft, finalize, approve, workflow, versioning, approval, task, event log]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:alba", "status:single-project"]
category: pattern
status: single-project
projects: [alba]
evidence: ["alba:unrecorded"]
alternatives: []
fragment: product-with-approval-workflow
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let authors prepare a content item, submit it for review and have an approver accept it, with a recorded history. The item has three states (draft, finalized, approved). Each change of state is a custom operation, so the state rules, the approver task and the audit event are written once and each role sees only the operations it may use.

### Versions keep history

A new draft is created as a copy of the current item and gets the next version number. The version entity points back to the item it was created from, and a container entity holds all versions.

### Tasks and events support the workflow

Assigning an approver creates a task for that user. Every state change writes an event row, so the lifecycle is auditable.

## Structure

Product is the content item. It has content attributes, a required state attribute typed to the ProductState enumeration (DRAFT, FINALIZED, APPROVED), and several classification relations to lookup entities. It has author, delegating author and approvedBy associations to User, and composed attachments. A ProductVersion entity holds a version number, a finalized timestamp and a state snapshot, with a required association back to its Product (origin). A ProductVersions container holds all versions, and Product has a required association to it.

A Task entity has a state (TODO, APPROVED, REJECTED), a required assignee and creator (both User) and an optional target Product. An Event entity is the audit log: an event type, a message, a timestamp and optional associations to the Product and the performing User.

Product has custom instance operations: finalize, assignApproval, approveVersion, revokeApproval and draftNewVersion. Role-specific transfer objects expose the content with only the operations of that role (admin: all; author: create, finalize, new draft; approver: approve only; guest: read only). Boolean attributes on those transfer objects (is draft, is finalized, is approved and similar) drive visibility and enablement of the operations.

## Constraints

- State changes only through the custom operations. The operation loads the item, checks the current state and rejects a wrong state before it writes.
- A rejected transition is a business rule failure. Model it as a fault declared on the operation (HTTP 422 with the X-Fault header); a plain RuntimeException would reach the client as a generic 500. A missing required value stays a platform ValidationException (HTTP 400).
- Interceptors run only for built-in operations, so they do not run around these custom operations. State checks, event rows and task creation are called from the operations themselves.
- Only one version may be approved at a time. Approving rolls any earlier approved version back to finalized (project rule, not platform behaviour).
- Visibility of an operation is a hint for the UI. The backend operation still checks state and role; the frontend can only hide controls.
- Enumeration ordinals are persisted, unique and within 0 to 9999. Do not renumber members.
- Each operation resolves the acting user from the actor's email claim. This is project code on top of the platform's variable resolver.

## Variations

- **Event log as an entity.** The shape used here: audit rows are explicit Event entities. A lighter option is to write them only for the transitions that matter.
- **Task per approver.** Assignment creates one task per selected approver. A single approver field on Product is enough when there is no inbox.
- **No version container.** Keep a version number on Product and a link to the previous product. Use this when no version list view is needed.
- **State machine engine.** For many states or configurable transitions, see [[workflow-engine-state-machine-cluster]].

## When to use

- Content needs review and approval before it counts as official.
- Reviewers and authors have different permitted operations on the same item.
- A history of versions and an audit trail are required.

## When to avoid

- There are only two states and no review; use [[open-close-status-toggle]] or a status enumeration.
- Transitions are configured at runtime; use a workflow engine.
- The item needs no history; drop the version entities.

## Related

- [[accept-reject-operations]] — a smaller accept and reject pair with a status enumeration
- [[workflow-engine-state-machine-cluster]] — a configurable state machine for many states
- [[open-close-status-toggle]] — a two-state toggle with a custom operation
- [[cards-container-configuration-hook]] — the card layout used for the product lists
