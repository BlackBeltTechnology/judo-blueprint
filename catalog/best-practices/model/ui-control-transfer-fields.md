---
id: "ui-control-transfer-fields"
title: "UI Control Fields on Transfer Objects"
domain: "model"
category: "transfer"
score: 61.9
usage_count: 8
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - itracker
  - alba
  - skillmatrix-model
  - viterra_demo
  - judo-demo-miniworkflow
  - ams-model
  - park-here
  - judo-partner
---
## Description

Actor-level transfer objects include additional boolean or string attributes that control UI behavior (form editability, button visibility, display labels) but have no corresponding entity attribute. These fields are populated by derived getter expressions or custom backend logic, enabling the model to drive UI state without client-side business rules.

## Structure

- Transfer object adds attributes not present on the mapped entity
- Common field types:
  - **Editability flag**: `editable: Boolean` -- controls whether a form/field is editable
  - **Button visibility flags**: `hide<ActionName>: Boolean` -- controls whether an action button is shown
  - **Display labels**: `label: String` -- computed display text
  - **Role indicators**: `financialUser: Boolean` -- indicates current user's role for UI branching
  - **enabledBy references**: Links an operation or field to a boolean attribute that controls its enabled state
  - **confirmationType CONDITIONAL**: Delete operations show confirmation dialogs based on a condition attribute
  - **hiddenBy references**: Links a UI group to a boolean attribute that controls its visibility
- These fields are typically `required: false` (optional)
- They may be populated by getter expressions or custom backend logic

## Examples

### itracker
`user::Initiative` adds 7 UI-control fields not on the entity: `label` (display label), `editable` (form editability), `hideSendForApproval`, `hideApproval`, `hideReject`, `hideArchive` (button visibility per lifecycle state), `initiator` (display name of owning user). `user::MonthlyForecast` adds `financialUser` (role indicator) and `editable` (field editability).

### SkillMatrix
`enabledBy` pattern: Delete User button enabled by `actorIsAdmin` (session-level role check), HR/Admin checkboxes enabled by `actorIsAdmin`, Training plan fields enabled by `isOpen` (derived: `not self.closed`), Approve button enabled by `unapproved` (derived: `not self.approved`). `confirmationType CONDITIONAL`: Delete User confirms when `hasSkills = true`, Delete Competence confirms when `hasReferences = true`.

### Alba
Extensive UI control fields on role-based transfers: `AuthorProduct.isEditEnabled` (only drafts editable), `AuthorProduct.canNotFinalize` (hides finalize button for non-owners/non-drafts), `AuthorProduct.isApproveDisabled` (complex approval logic), `AuthorProduct.fixNotEnabled = false` (literal constant). `PublicAuthorProfile.isTrue = true` and `PublicAuthorProfile.isNotTeacher` control visibility. Operations use `hiddenBy` and `enabledBy` attributes plus `confirmationType="MANDATORY"` for critical actions.

### SkillMatrix-Model
Model source confirms `enabledBy` and `confirmationType="CONDITIONAL"` on multiple transfer operations. Derived UI control attributes: `isOpen = not self.closed` (TrainingPlan editability), `unapproved = not self.approved` (Skill approval enablement), `hasReferences` (Competence delete confirmation). The pattern integrates with the guard-clause-delete pattern: UI conditional confirmation mirrors the operation's guard logic.

### Viterra Demo
`ReportTransfer.showAcceptButton` (`self.status == SUBMITTED or self.status == REVIEW`) and `showReviewButton` (`self.status == SUBMITTED`) are derived booleans controlling operation button visibility. Operation forms use `enabledBy` to reference these attributes. `PartnerClientTransfer.hasNoOpenReport` uses `self.reports!filter(r | r.status == PENDING)!empty()` to control a `hiddenBy` warning group: "You have open reports. Please click on Open Reports menu."

### KozutEugyfelClient
`BejelentesMegtekinto` transfer exposes 7 permission booleans from entity-level derived attributes: `tovabbitasEngedely`, `tovabbitasFelelosnekEngedely`, `megjegyzesEngedely`, `lezarasEngedely`, `resztvevoHozzadasEngedely`, `megnyitasEngedely`, `leiratkozasEngedely`. Each evaluates state + user role + user relationship to the report, controlling which operation buttons are enabled in the UI viewer.

### judo-demo-miniworkflow
`DocumentTransfer` adds 4 negative derived attributes not on the entity: `isNotClosable = not self.isClosable`, `isNotRejectable = not self.isRejectable`, `isNotReviewable = not self.isReviewable`, `isNotAcceptable = not self.isAcceptable`. These are used in `hiddenBy` bindings to hide workflow operation buttons. `GenericUser` adds `isNotAdmin = not self.admin` and `isNotApprover = not self.approver` for menu item conditional hiding.

### AMS-Model
`manager::Request` transfer includes derived boolean fields: `isPending = self.status == Status#PENDING`, `isOpen`, `isClosed`, `isEmpty` for controlling UI state. These enable/disable approve/reject buttons based on request status. The `manager::Campaign` transfer uses `isOpen` and `isClosed` derived booleans to control visibility of open/close toggle operations, preventing invalid state transitions in the UI.

### ParkHere
Entity-level UI control attributes: `User.isNotAdministrator = not self.isAdministrator` used in `hiddenBy` for admin-only menu items and accesses. `Holiday.isNotDeletable` controls delete button visibility (past holidays cannot be deleted). `ConfigurationSettings.isConfigurationExist` enables doorman creation only when configuration exists. `HolidayInput` uses `hiddenBy` on `userHidden` and `hiddenByCustom` to show/hide fields based on admin role and form state.

### judo-partner
`isActorPartnerAdmim` (note: typo in model) is a DERIVED Boolean appearing on Partner, Contact, Address, and PartnerList transfer objects. It controls role-based UI visibility, enabling partner admin functionality. `User.isNotAdmin` derived attribute (negation of `isAdmin`) is used for UI control via `hiddenBy`.

### AMS-Frontend
`Campaign` transfer adds 4 derived UI control booleans: `isOpen = self.status == CampaignStatus#OPEN`, `isClosed = self.status == CampaignStatus#CLOSED`, `isEmpty = self.confirmationRequests!count() == 0`. These control `enabledBy` bindings on campaign operations (close enabled when open, open enabled when closed, load enabled when empty). `Request.isPending` enables/disables approve/reject buttons. UI includes mandatory confirmation dialogs on approve, reject, open, and close operations.

## Trade-offs

- Pros: UI state driven by the model, no client-side business logic needed, different actors can see different controls
- Cons: Transfer objects become larger than their entities, may need custom backend logic to populate
- Prefer when: UI needs to conditionally show/hide buttons or toggle editability based on entity state or user role

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md)
- [conditional-visibility-getter](conditional-visibility-getter.md)
