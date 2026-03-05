---
id: accept-reject-operations
title: "Accept/Reject Approval Operations Pattern"
usage_count: 7
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - mlszksz-platform
  - judo-demo-miniworkflow
  - trivia
  - itracker
  - doors-model
  - ams-model
  - skillmatrix-model
---

## Description

A pair of instance operations `accept` and `reject` (or `approve` and `reject`) on transfer objects representing requests that require approval. The reject operation typically takes a ModerationInput (or similar) parameter with a `reason` or `message` field. The underlying entity status transitions from VERIFIED (or PENDING or REVIEW_REQUESTED or REVIEW or NEW) to APPROVED/ACCEPTED or REJECTED. This pattern appears on registration requests, user invitation requests, document approval workflows, question moderation, initiative approval, contract approval, access confirmation requests, skill level approval, and any entity following an approval workflow. Guard attributes on the transfer object control when the operations are available. Some variants add additional state transition operations (e.g., requestReview, close, review, sendForApproval, sign, reset) alongside the accept/reject pair, enabling multi-step approval flows. Some variants include a preceding sendForApproval operation that transitions the entity into a review-eligible state before approve/reject can be invoked. Advanced variants chain multiple approval stages dynamically based on workflow configuration, with conditional auto-approval based on contract attributes. Some variants include a `reset` operation to return a decided request back to PENDING status, and a bulk `approveAll` operation on a parent entity for batch approval of all pending requests. In skill management contexts, the approve operation confirms a requested skill level matches the approved level, using a derived boolean `approved` attribute computed from comparing `approvedLevel` and `requestedLevel`.

## Detection Query

```graphql
{ esm { transferobjecttypes(limit: 100) {
  items { fqn name
    operations { items { name } }
  }
} } }
```

Look for transfer objects that have both `accept`/`approve` and `reject` operations.

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    operations { items { name operationType } }
  }
} } }
```

Look for entities with `approve` and `reject` instance operations.

## Creation Mutations

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::{{REQUEST_TO}}", name: "accept",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{SERVICE_NAMESPACE}}::{{REQUEST_TO}}", name: "reject",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{SERVICE_NAMESPACE}}", name: "{{REJECTION_INPUT_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{SERVICE_NAMESPACE}}::{{REJECTION_INPUT_NAME}}", name: "reason"
} }) { success fqn } }
```

## Examples

### mlszksz-platform
- **RegistrationRequest TO** (`MLSZKSZPlatform::services::admin::RegistrationRequest`):
  - Operations: accept, reject
  - Transitions RegistrationRequestStatus from VERIFIED -> APPROVED or REJECTED
- **UserInvitationRequestTO** (`MLSZKSZPlatform::services::companyadmin::UserInvitationRequestTO`):
  - Operations: accept, reject
  - Transitions InvitationStatus from VERIFIED -> APPROVED or REJECTED
  - Guard attribute: operationAvailable (boolean)
- **ModerationInput** (`MLSZKSZPlatform::services::admin::ModerationInput`):
  - Unmapped transfer object with single `reason` attribute
  - Used as input parameter for reject operations

### judo-demo-miniworkflow
- **Document entity** (`MiniWorkflow::Document`):
  - Operations: accept, reject (plus requestReview, close)
  - Transitions DocumentState: REVIEW_REQUESTED -> ACCEPTED or REJECTED
  - Guard attributes: isAcceptable, isRejectable (with negations isNotAcceptable, isNotRejectable on DocumentTransfer)
- **DocumentTransfer** (`MiniWorkflow::DocumentTransfer`):
  - Operations: accept (MAPPED), reject (MAPPED), requestReview (MAPPED), close (MAPPED), createDocument (STATIC)
  - Guard attributes: isAcceptable, isRejectable, isReviewable, isClosable plus their negations (isNotAcceptable, isNotRejectable, isNotReviewable, isNotClosable)
- **Message** (`MiniWorkflow::Message`):
  - Unmapped transfer object with single `message` attribute
  - Used as input parameter for reject operation (equivalent to ModerationInput in mlszksz-platform)
- This variant extends the accept/reject pair with requestReview and close operations, forming a full four-step document review workflow

### trivia
- **Question entity** (`trivia::entities::Question`):
  - Operations: approve (INSTANCE), reject (INSTANCE), review (INSTANCE)
  - Transitions QuestionStatus: REVIEW -> APPROVED or REJECTED; also APPROVED/REJECTED -> REVIEW via the review operation
  - QuestionStatus enum members: REVIEW(1), APPROVED(2), REJECTED(3)
  - Default status: REVIEW (questions start in review state)
- **Admin Question TO** (`trivia::actors::admin::Question`):
  - Operations: approve (MAPPED), reject (MAPPED), review (MAPPED), upload (STATIC), download (STATIC)
  - Additional admin operations for bulk question management (upload JSON, download JSON)
- This variant uses `approve`/`reject` naming (instead of `accept`/`reject`) and adds a `review` operation for cycling questions back to the review state
- Three-way cycling: REVIEW <-> APPROVED and REVIEW <-> REJECTED, allowing questions to be re-reviewed after approval or rejection
- No separate rejection reason input -- the reject operation takes no parameters in this variant

### itracker
- **Initiative entity** (`itracker::entities::Initiative`):
  - Operations: sendForApproval (INSTANCE), approve (INSTANCE), reject (INSTANCE), archiveForecast (INSTANCE)
  - Transitions InitiativeStatus: NEW -> REVIEW (via sendForApproval) -> APPROVED or REJECTED (via approve/reject)
  - InitiativeStatus enum members: APPROVED(1), COMPLETE(3), NEW(4), REVIEW(5), REJECTED(6)
  - Default status: NEW (initiatives start in new state)
- **User Initiative TO** (`itracker::actors::user::Initiative`):
  - Operations: createInitiative (STATIC), sendForApproval (MAPPED), approve (MAPPED), reject (MAPPED), archiveForecast (MAPPED)
  - Guard attributes: hideSendForApproval, hideApproval, hideReject, hideArchive, editable -- control operation visibility based on current status
- This variant uses a three-step flow: create (NEW) -> sendForApproval (REVIEW) -> approve/reject (APPROVED/REJECTED)
- The `sendForApproval` operation acts as a gating step before approval/rejection is possible
- No separate rejection reason input -- the reject operation takes no parameters
- Guard attributes use "hide*" naming convention (hideSendForApproval, hideApproval, hideReject) instead of "isNot*" or "is*Disabled"

### doors-model
- **Contract entity** (`doors::entities::Contract`):
  - Operations: startApproval (INSTANCE), approve (INSTANCE), reject (INSTANCE), sign (INSTANCE), close (INSTANCE), setNextStage (INSTANCE), setResponsible (INSTANCE), addSignee (INSTANCE), validate (INSTANCE, custom), addLog (INSTANCE), uploadFile (INSTANCE, custom), uploadSignedContract (INSTANCE, custom), generateDocument (INSTANCE, custom), updateDocument (INSTANCE)
  - Transitions DocumentStatus: CREATED -> PENDING (via startApproval) -> APPROVED (via multi-stage approve) or REJECTED (via reject) -> SIGNED (via sign) -> CLOSED (via close)
  - Reject can return to PENDING when restarted via startApproval
  - DocumentStatus enum: CREATED(1), PENDING(2), APPROVED(3), SIGNED(4), REJECTED(5), CLOSED(6)
- **RejectInput TO** (`doors::entities::RejectInput`):
  - Unmapped transfer object with single `text` attribute
  - Used as input parameter for the reject operation
- **StartApprovalResult / ValidateContractResult / ContractValidationError TOs**: output transfer objects for the startApproval and validate operations, providing success/failure status and error messages
- This is the most complex approval variant: it combines approve/reject with a dynamic multi-stage workflow engine where ContractStage entities are created from WorkflowStage templates, each stage has condition-based routing (conditionNetValueUpperLimit/LowerLimit, conditionTemplateBased, conditionSpecial), and stages can be auto-approved when conditions are not met
- The workflow progresses through stages sequentially (by order), with each stage requiring approval from responsible Position holders based on the contract's division
- Additional operations beyond approve/reject: sign (for physical document signing after approval), close (for archiving after signing), uploadFile/uploadSignedContract (for document management)

### ams-model
- **Request entity** (`ams::entities::Request`, abstract base):
  - Operations: approve (INSTANCE), reject (INSTANCE), reset (INSTANCE)
  - Transitions Status: PENDING -> APPROVED (via approve) or REJECTED (via reject); reset returns to PENDING
  - Status enum members: PENDING(1), APPROVED(2), REJECTED(3)
  - The approve operation sets `this.status = Status#APPROVED` and records `this.decisionTime = Timestamp!now()`
  - The reject operation sets `this.status = Status#REJECTED` and records `this.decisionTime = Timestamp!now()`
  - The reset operation sets `this.status = Status#PENDING` and unsets decisionTime
  - Guard attribute: isPending (DERIVED: `self.status == Status#PENDING`) controls when approve/reject are available
- **ConfirmationRequest entity** (`ams::entities::ConfirmationRequest`, extends Request):
  - Inherits approve/reject/reset from Request
  - Adds: approver [1..1] ASSOC User, campaignStatus (DERIVED from container Campaign)
- **Manager Request TO** (`ams::actors::manager::Request`, maps ConfirmationRequest):
  - Operations: approve (MAPPED), reject (MAPPED)
  - Attributes: applicationName, userName, userEmail, responsibleName, status, type, loginName, effectiveDate, isPending, roles, campaignStatus
  - Guard: isPending controls operation availability in UI; approve/reject buttons use `enabledBy` pointing to isPending with confirmationType: MANDATORY
- **User.approveAll** (`ams::entities::User`):
  - INSTANCE operation that iterates over `this.approvals!filter(r | r.status == Status#PENDING)` and calls `request.approve()` on each
  - Enables bulk approval of all pending confirmation requests assigned to a manager
- **ManagerApprovalList TO** (`ams::actors::manager::ManagerApprovalList`, maps User):
  - Aggregates pending approvals via DERIVED relation filtered by `status == PENDING and campaignStatus == CampaignStatus#OPEN`
  - Operations: approveAll (MAPPED) for one-click bulk approval
- This variant uses an abstract Request base entity with approve/reject defined once and inherited by ConfirmationRequest and AccessRequest subtypes
- No separate rejection reason input -- reject takes no parameters
- Adds a `reset` operation for returning decided requests back to PENDING state
- Includes a bulk `approveAll` operation on the User entity for batch processing
- Guard attributes use `isPending` derived boolean with UI `enabledBy` binding

### skillmatrix-model
- **Skill entity** (`SkillMatrix::Skill`):
  - Operations: approve (INSTANCE)
  - The approve operation sets the `approvedLevel` to match the `requestedLevel`, confirming the skill assessment
  - Derived boolean: `approved` (DERIVED: `self.approvedLevel!isDefined() and self.requestedLevel!isDefined() and self.approvedLevel == self.requestedLevel`) -- true when levels match
  - No explicit status enum; approval state is computed by comparing the approvedLevel and requestedLevel relations
  - Relations: competence (1..1 TwoWay ASSOC Competence), approvedLevel (0..1 OneWay ASSOC SkillLevel), requestedLevel (0..1 OneWay ASSOC SkillLevel), user (0..1 TwoWay ASSOC User)
  - Derived display attributes: approvedLevelName, requestedLevelName, competenceName, userFullName, unitName, competenceScore
- **Manager Skill TO** (`actor::manager::Skill`):
  - Operations: approve (MAPPED)
  - Attributes: competenceName (DERIVED), approvedLevel (DERIVED), requestedLevel (DERIVED), approved (DERIVED), professionalName (DERIVED), professionalIndexName (DERIVED), unapproved (DERIVED)
  - The `unapproved` attribute serves as a guard for showing the approve button
- **User bulk operations**:
  - User.approveAllSkills -- INSTANCE operation that bulk-approves all pending skills for a user
  - User.approveAllSubordinatesSkills -- INSTANCE operation that bulk-approves all pending skills across all subordinates
- **Manager TOs for bulk approval**:
  - manager::Subordinate -- operations: approveAllSkills, createTrainingPlan, completeAllTargets
  - manager::UnapprovedSkillsView -- relation: skillsToApprove (0..* AGGREGATION Skill); operations: approveAllSubordinatesSkills
- This variant is unique in that it does not use a status enum or reject operation; instead, approval state is computed by comparing two relation fields (approvedLevel vs requestedLevel)
- The professional (self-assessment) sets the requestedLevel, and the manager sets the approvedLevel via the approve operation
- Bulk approval operates at both the individual user level (approveAllSkills) and across all subordinates (approveAllSubordinatesSkills)
