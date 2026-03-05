---
id: "approval-workflow-conditional-visibility"
title: "Approval Workflow with Conditional Button Visibility"
domain: "frontend"
category: "form"
score: 50.8
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - itracker
  - doors-model
  - ams-frontend
---
## Description

Implement a multi-step approval workflow UI entirely through model-level configuration using derived boolean attributes for conditional visibility. Each action button (approve, reject, send for approval, archive) has a corresponding `hide*` or `*Enabled` derived boolean on the transfer object. The backend computes these booleans based on the entity status and the current user's role. The generated UI automatically hides/shows or enables/disables buttons based on these flags, creating a state-machine-driven UX with no frontend code.

## Structure

ESM model pattern:
```
TransferObject Initiative {
  // Status enum
  status: InitiativeStatus

  // Derived visibility flags (computed by backend)
  hideSendForApproval: Boolean  // true when status != NEW/REJECTED or not owner
  hideApproval: Boolean         // true when status != REVIEW or not finance user
  hideReject: Boolean           // true when status != REVIEW or not finance user
  hideArchive: Boolean          // true when status != APPROVED

  // Derived editability flag
  editable: Boolean             // true when owner AND (status == NEW or REJECTED)

  // Operations with visibility and confirmation
  operation sendForApproval { hiddenBy: hideSendForApproval, confirmation: MANDATORY }
  operation approve { hiddenBy: hideApproval, confirmation: MANDATORY }
  operation reject { hiddenBy: hideReject, confirmation: MANDATORY }
  operation archiveForecast { hiddenBy: hideArchive, confirmation: MANDATORY }
}
```

Generated UI renders action buttons with `hidden={data.hideApproval}` and confirmation dialogs with custom messages. Field editability is controlled by `enabledBy="editable"`.

## Examples

### itracker
Initiative workflow has 4 states (NEW, REVIEW, APPROVED, REJECTED) with role-based transitions. Owner sees "Send For Approval" on NEW/REJECTED. Finance user sees "Approve"/"Reject" on REVIEW. All users see "Archive Forecast" on APPROVED. All buttons use mandatory confirmation dialogs. 12 form fields are controlled by an `editable` derived boolean. MonthlyForecast has dual-control: `savingPotential` editable by owners, `saving` editable only by finance users on APPROVED initiatives.

### doors-model
Contract lifecycle has 6 states (CREATED, PENDING, APPROVED, REJECTED, SIGNED, CLOSED) with `enabledBy` attributes on `OperationForm` elements. Five derived booleans control UI: `closeEnabled` (status == SIGNED), `uploadEnabled` (status != CLOSED), `uploadSignedEnabled` (file exists AND status != CLOSED), `readyForApproval` (file exists AND status in CREATED/REJECTED), `readyForUpload` (not template-based AND status in CREATED/PENDING/REJECTED). Operations include approve, reject, sign, uploadSignedContract, and close.

### ams-frontend
Campaign management has 2 states (OPEN, CLOSED) with derived booleans `isOpen`, `isClosed`, and `isEmpty` controlling 3 operations: **Close** (enabled when `isOpen == true`, confirmation "Are you sure to close the campaign?"), **Open** (enabled when `isClosed == true`, confirmation "Are you sure to re-open the campaign?"), and **Load** (enabled when `isEmpty == true`). The Download button for campaign status Excel is always available.

## Trade-offs

- **Pros**: Entire workflow logic stays on backend; no frontend code for visibility rules; consistent across all clients; secure (backend enforces, frontend only hides)
- **Cons**: Requires careful backend design of derived booleans; visibility logic not visible in frontend code; complex workflows need many derived flags; UI refresh required after state changes
- **When to use**: State machine workflows (approval, review, publishing) where button visibility depends on entity status and user role

## Related Patterns

- [zero-customization-generated-frontend](zero-customization-generated-frontend.md)
- [model-defined-color-palette](model-defined-color-palette.md)
