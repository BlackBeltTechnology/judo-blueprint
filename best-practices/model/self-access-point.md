---
id: "self-access-point"
title: "Self-Referencing Access Point for Own Profile"
domain: "model"
category: "access"
score: 42.3
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - alba
  - skillmatrix-model
  - judo-partner
---
## Description

An actor's access point uses `self` as the getter expression to expose the logged-in user's own entity record. This provides a "my profile" or "my dashboard" entry point where the actor accesses their own data with cardinality `0..1`. The target transfer object is typically a specialized view of the principal entity that includes editable relations and self-service operations.

## Structure

- Access point with cardinality `0..1`
- Getter expression: `self`
- Target is a transfer object that maps to the same entity as the actor's principal
- The transfer may extend the principal transfer via generalization (adding relations/operations)
- CRUD is typically update-only (the user can edit their own profile but not create/delete)
- Multiple `self`-based access points can coexist on the same actor, each targeting a different transfer projection

## Examples

### SkillMatrix
ProfessionalActor has 3 access points, 2 using `self`: `myProfession -> MyProfessional [0..1]` with getter `self` (own profile with skills management, CRUD: update), `allForApproval -> UnapprovedSkillsView [0..1]` with getter `self` (consolidated view of all unapproved skills across subordinates). The third access `subordinates` navigates from self: `self.subordinates!sort(u | u.indexName ASC)`.

### Alba
`userProfile` access point (0..1) targets `UserTransfer` with a derived getter resolving to the current user's own record. This provides a "my profile" entry point where users can view their data and invoke `finalizeAccount()` for teacher account setup. The profile includes `isTeacherAndNeedsToBeFInalized` derived attribute to prompt profile completion.

### SkillMatrix-Model
Model source confirms 2 `self`-based access points on `ProfessionalActor`: `myProfession` (target: MyProfessional, CRUD: update-only) and `allForApproval` (target: UnapprovedSkillsView, read-only). Both use `getterExpression="self"` with `accessType="DERIVED"`. The dual `self` access demonstrates using different transfer projections of the same user record for different UI views.

### judo-partner
`Actor.partnerList` access point (0..1) uses `self` as getter expression, targeting the `PartnerList` transfer object. `PartnerList` maps to the `User` entity and provides a personalized dashboard with derived `partners` and `partnerLogs` collections, plus `createPartner` operation. CRUD: update-only. Demonstrates the self-access pattern used as a dashboard entry point rather than a profile editor.

### AMS-Frontend
Manager actor's `approvalAll [0..1]` uses `self` getter targeting `ManagerApprovalList` transfer. This maps the logged-in manager's own User entity into a bulk approval view with a filtered `approvals` relation (pending + open campaign) and an `approveAll` operation. Demonstrates `self` access used for a workflow aggregation view rather than a profile.

## Trade-offs

- Pros: Simple and declarative "my data" access, no filtering logic needed, framework resolves the current user automatically
- Cons: Limited to single-record access (0..1), the transfer must map to the actor's principal entity
- Prefer when: An actor needs to access and manage their own profile or dashboard data

## Related Patterns

- [derived-access-filtering](derived-access-filtering.md)
- [actor-based-transfer-projection](actor-based-transfer-projection.md)
- [transfer-generalization](transfer-generalization.md)
