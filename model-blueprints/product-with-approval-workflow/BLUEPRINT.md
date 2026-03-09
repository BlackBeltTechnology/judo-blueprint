---
id: "product-with-approval-workflow"
title: "Product Entity with Draft/Finalize/Approve Workflow and Versioning"
score: 42.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - alba
---
## Description

A Product entity representing a content item (educational resource, document, or similar) that follows a three-stage approval workflow: DRAFT (being authored), FINALIZED (submitted for review), and APPROVED (officially accepted). The Product has rich content attributes (title, introduction, goal, areaOfDevelopment, extent, requiredResources, relatedLiterature), a state attribute typed to a ProductState enum, and multiple classification relations (audience, curriculum, resultTypes -- all 0..* ASSOCIATION to lookup entities). The Product carries authorship relations: an author (0..1 ASSOC to User), an impersonatingAuthor (0..1 ASSOC to User for delegation), and an approvedBy (0..1 ASSOC to User recording who approved it). File attachments are composed (0..* COMPOSITION to Attachment).

A ProductVersion entity tracks version history: each version has a version number (default: 0), a finalizedAt timestamp, a state snapshot, and an origin relation (1..1 ASSOC back to the Product it was created from). A ProductVersions container entity holds all versions (0..*) and a derived allProducts collection. The Product references both its version container (productVersions 1..1) and the current version (currentVersion 0..1 DERIVED). Denormalized fields on Product (ownVersion, institutionName, curriculumAggregated, resultTypesAggregated, audienceAggregated) provide quick display without joins.

Instance operations on Product implement the approval lifecycle:
- **finalize** (custom) -- transitions from DRAFT to FINALIZED
- **assignApproval** (custom) -- assigns an approver to review the product
- **approveVersion** (custom) -- transitions from FINALIZED to APPROVED
- **revokeApproval** (custom) -- reverts from APPROVED back to FINALIZED
- **draftNewVersion** -- creates a new DRAFT copy from the current version

A Task entity supports the approval workflow: it has a type (TaskType enum: APPROVAL), a state (TaskState enum: TODO/APPROVED/REJECTED), an assignee (1..1 ASSOC to User), a createdBy (1..1 ASSOC to User), and a targetProduct (0..1 ASSOC to Product). Operations on Task include closeTask (custom), activate, and deactivate. Denormalized fields (createdByName, assigneeName, productTitle) provide display strings.

An Event entity serves as an audit log, recording product lifecycle events: type (EventType enum: PRODUCT_CREATED/PRODUCT_FINALIZED/PRODUCT_APPROVED/PRODUCT_APPROVAL_REVOKED), message, createdAt, and relations to product (0..1) and performedBy user (0..1).

Transfer objects provide role-specific views: AdminProduct (full access with all operations), AuthorProduct (create/finalize/draftNewVersion), ApproverProduct (approveVersion only), GuestProduct (read-only). Guard attributes (isDraft, isFinalized, isApproved, isNotFinalized, canNotFinalize, isApproveDisabled, draftNewVersionDenied) control operation visibility per state and role.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
