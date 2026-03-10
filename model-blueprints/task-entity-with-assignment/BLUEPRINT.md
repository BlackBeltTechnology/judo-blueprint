---
id: "task-entity-with-assignment"
title: "Task Entity with Assignee, Type, and State Enums"
score: 51.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - alba
---
## Description

A Task entity that models assignable work items within an approval or review workflow. Each task has a type (TaskType enum categorizing the kind of work, e.g., APPROVAL), a state (TaskState enum tracking progress: TODO/APPROVED/REJECTED), a createdAt timestamp, and an isActive boolean flag (default: false). The task links to a createdBy user (1..1 ASSOC), an assignee user (1..1 ASSOC) responsible for completing the task, and a targetProduct or target entity (0..1 ASSOC) that the task relates to. Denormalized display fields (createdByName, assigneeName, productTitle) provide quick rendering without joins. A derived isAssigneeCurrentUser flag enables UI personalization.

Operations on the Task include:
- **closeTask** (custom) -- resolves the task, typically setting state to APPROVED or REJECTED
- **activate** / **deactivate** -- toggle the isActive flag for task visibility

The CloseTaskInput unmapped TO carries a `result` attribute (the TaskState value) for the closeTask operation. The ApprovalTaskInput unmapped TO carries a `users` relation (0..* AGGREGATION) for selecting which users to assign approval tasks to.

Transfer objects provide role-specific task views: AuthorTask (for the product author, with closeTask operation), ApproverTask (for the assigned approver, with closeTask), AdminTask (for administrators, with activate/deactivate operations to manage task visibility).

This pattern is distinct from the workflow-engine Task/Token pattern in that it is a simple, domain-embedded task model without a full state machine engine. Tasks are created as side effects of product operations (assignApproval) rather than being driven by a generic workflow definition.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.

## Frontend Implementation

See [frontend.md](frontend.md) for frontend implementation patterns and examples.
