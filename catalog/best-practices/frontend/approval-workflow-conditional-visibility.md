---
id: approval-workflow-conditional-visibility
title: Approval Workflow with Conditional Button Visibility
description: An approval workflow UI driven entirely by the model: per-operation derived booleans decide which action buttons and fields are hidden or enabled for the current status and user, with no frontend code.
aliases: [state-driven buttons, workflow button visibility]
keywords: [approval, workflow, hiddenBy, enabledBy, derived boolean, confirmation, status, operation, role]
tags: ["domain:frontend", "layer:frontend", "project:itracker", "project:doors-model", "status:emerging"]
category: form
status: emerging
projects: [itracker, doors-model]
evidence: ["itracker:unrecorded", "doors-model:unrecorded"]
alternatives: []
related: [zero-customization-generated-frontend, model-defined-color-palette, ui-control-transfer-fields, action-group-conditional-enabling]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

In a status-driven process (new, review, approved, rejected) each action button is valid only in some statuses and for some roles. The practice keeps those rules in the model as derived booleans, and the generated UI shows, hides, enables or disables buttons and fields from them.

## Practice

### Platform base

- `hiddenBy`, `enabledBy` and `requiredBy` each reference a **boolean data member on the same transfer object** that owns the page; no cross-object reference exists. `hiddenBy` hides the element when the boolean is true; `enabledBy` enables it when true and disables it otherwise ([UI authoring guide](../../agent-docs/model/ui-authoring-guide.md)). The generated React binds them to form state ([access control via boolean attributes](../../agent-docs/frontend/hooks/navigation-and-access.md)).
- An operation button can ask for confirmation: `confirmationType` is `NONE`, `CONDITIONAL` (decided by a boolean member through `confirmationCondition`) or `MANDATORY` (always, with a `confirmationMessage`) ([UI authoring guide: operations wiring](../../agent-docs/model/ui-authoring-guide.md)).
- A derived member is computed on read from a getter expression, so it can combine the entity's status with data about the calling actor. The getter may read actor variables ([derived getters that depend on the actor](../../agent-docs/integration-testing/access-and-derived-testing.md)).
- The booleans only control the generated UI. An API client can still call the operation, so the operation implementation (or a before-interceptor) must reject calls that are invalid for the current status or role ([interceptors](../../agent-docs/backend/interceptors.md)).

### Project practice: one flag per button, status and role inside the flag

This layer is project practice, not a platform feature:

- Add one derived boolean per action on the transfer object (hide-send-for-approval, hide-approve, hide-reject, hide-archive) and one editability flag for the form fields. Combine status and role inside the derived expression, not in the UI model.
- Wire each operation form with `hiddenBy` (or `enabledBy`) to its flag and set mandatory confirmation on state-changing operations.
- Wire the form fields with `enabledBy` to the editability flag; a field that depends on a different role gets its own flag (dual control).
- After an operation succeeds, refresh the page data, because the flags change with the status.

## Rationale

The workflow rules live in the model next to the data they read, so every client and page shows the same buttons and no frontend code exists for visibility. The cost: many flags for complex workflows, rules invisible in frontend code, and the need to guard the operations themselves on the server.

## Example

- itracker: an initiative with four statuses (new, review, approved, rejected). The owner sees send-for-approval on new or rejected; a finance user sees approve and reject on review; everyone sees archive on approved. All use mandatory confirmation. Twelve form fields follow one editability flag; a forecast has dual control, with one value editable by owners and another only by finance users on approved initiatives.
- doors-model: a contract with six statuses (created, pending, approved, rejected, signed, closed). Five derived booleans (close, upload, upload-signed, ready-for-approval, ready-for-upload) combine status with file presence and drive `enabledBy` on the operation forms.

## When to avoid

- Visibility depends on data that cannot be computed on the owning transfer object.
- Rules need client-only context such as unsaved form state.
- Only one or two buttons are conditional; see [[action-group-conditional-enabling]] for grouping them.

## Related

- [[ui-control-transfer-fields]] — transfer fields that carry UI-control booleans
- [[action-group-conditional-enabling]] — one boolean enabling a group of operations
- [[zero-customization-generated-frontend]] — the generated frontend this relies on
- [[model-defined-color-palette]] — other UI behavior defined in the model
