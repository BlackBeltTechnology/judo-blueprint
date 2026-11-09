## Examples

### alba
- **Product entity**: `Alba::entities::Product` (non-CRUD)
  - Content attributes: title (req), introduction (req), goal (req), areaOfDevelopment (req), extent (req), requiredResources (req), relatedLiterature
  - State: state (req, default: DRAFT), createdAt, finalizedAt
  - Denormalized: institutionName, curriculumAggregated, resultTypesAggregated, audienceAggregated, isFinalizedOrApproved, ownVersion, userOwnsProduct
  - Relations: author (0..1 ASSOC), impersonatingAuthor (0..1 ASSOC), approvedBy (0..1 ASSOC), audience (0..* ASSOC), curriculum (0..* ASSOC), resultTypes (0..* ASSOC), attachments (0..* COMPOSITION), events (0..* ASSOC), version (0..1 ASSOC to ProductVersion), currentVersion (0..1 DERIVED), productVersions (1..1 ASSOC to ProductVersions), relatedTasks (0..* ASSOC)
  - Operations: finalize (custom), approveVersion (custom), revokeApproval (custom), assignApproval (custom), draftNewVersion
- **ProductState enum**: `Alba::entities::ProductState` -- DRAFT(1), FINALIZED(2), APPROVED(3)
- **ProductVersion entity**: `Alba::entities::ProductVersion` (non-CRUD)
  - Attributes: version (default: 0), finalizedAt, state
  - Relations: origin (1..1 ASSOC to Product)
- **ProductVersions entity**: `Alba::entities::ProductVersions` (non-CRUD)
  - A container entity; Relations: versions (0..* ASSOC to ProductVersion), allProducts (0..* DERIVED)
- **EventType enum**: `Alba::entities::EventType` -- PRODUCT_CREATED(4), PRODUCT_FINALIZED(3), PRODUCT_APPROVED(1), PRODUCT_APPROVAL_REVOKED(2)
- **Event entity**: `Alba::entities::Event` (non-CRUD) -- type (req), message, createdAt (req); relations: product (0..1 ASSOC), performedBy (0..1 ASSOC to User)
- **TaskType enum**: `Alba::entities::TaskType` -- APPROVAL(1)
- **TaskState enum**: `Alba::entities::TaskState` -- TODO(3), APPROVED(1), REJECTED(2)
- **Task entity**: `Alba::entities::Task` (non-CRUD) -- createdAt (req), type (req), state (req), isActive (default: false), createdByName, assigneeName, productTitle, isAssigneeCurrentUser; relations: createdBy (1..1 ASSOC), assignee (1..1 ASSOC), targetProduct (0..1 ASSOC); ops: closeTask (custom), activate, deactivate
- **Transfer Objects** (role-specific):
  - `AdminProduct` -- 25 attributes with guard flags (isDraft, isFinalized, isApproved, isNotApproved, isNotFinalized, isApproveDisabled, isPendingDelegated, fixFalse); ops: draftNewVersion, approveVersion, createProduct (STATIC, custom), revokeApproval, assignApproval
  - `AuthorProduct` -- 25 attributes; ops: createProduct (STATIC, custom), finalize, draftNewVersion, approve
  - `ApproverProduct` -- 20 attributes; ops: approveVersion
  - `GuestProduct` -- 15 attributes; read-only, no operations
  - `AuthorTask` / `ApproverTask` / `AdminTask` -- task projections per role with closeTask, activate/deactivate operations
- **AccountStatus enum**: `Alba::entities::AccountStatus` -- PENDING_APPROVAL(1), ACTIVE(2), SUSPENDED(3) -- used for User.status
- **UserRole enum**: `Alba::entities::UserRole` -- GUEST(1), TEACHER(2), APPROVER(3), ADMIN(4)
