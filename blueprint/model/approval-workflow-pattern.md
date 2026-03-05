---
id: "approval-workflow-pattern"
title: "Approval Workflow with Requested/Approved Levels"
domain: "model"
category: "operation"
score: 24.2
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - skillmatrix-frontend
  - skillmatrix-model
---
## Description

An entity models an approval workflow using two parallel relation fields: one for the requested value (set by the requester) and one for the approved value (set by the approver). A derived boolean attribute compares the two to determine approval status. An `approve` operation copies the requested value to the approved field. Bulk approval operations cascade through entity hierarchies.

## Structure

- Entity has two optional relations to the same target type:
  - `requestedLevel -> LevelType [0..1]` (editable by requester)
  - `approvedLevel -> LevelType [0..1]` (set by approver)
- Derived boolean: `approved = self.approvedLevel!isDefined() and self.requestedLevel!isDefined() and self.approvedLevel == self.requestedLevel`
- Instance operation `approve`: copies `this.requestedLevel` to `this.approvedLevel`
- Bulk operations cascade approval:
  - `approveAllSkills()` iterates a collection and calls `approve()` on each
  - `approveAllSubordinatesSkills()` iterates subordinates and calls `approveAllSkills()` on each
- Derived boolean `hasApprovalRequest = not self.skills!filter(s | not s.approved)!empty()` on the parent

## Examples

### SkillMatrix
`Skill` entity has `requestedLevel -> SkillLevel [0..1]` and `approvedLevel -> SkillLevel [0..1]`. `approved = self.approvedLevel!isDefined() and self.requestedLevel!isDefined() and self.approvedLevel == self.requestedLevel`. `Skill.approve()` sets `this.approvedLevel = this.requestedLevel`. Cascade: `User.approveAllSkills()` -> each `skill.approve()`, `User.approveAllSubordinatesSkills()` -> each `subordinate.approveAllSkills()`.

### SkillMatrix-Model
Model source confirms the full cascade chain: `Skill.approve()` (instance, sets `this.approvedLevel = this.requestedLevel`), `User.approveAllSkills()` (iterates `this.skills` calling `skill.approve()`), `User.approveAllSubordinatesSkills()` (iterates `this.subordinates` calling `subordinate.approveAllSkills()`). Also `User.completeAllTargets()` uses the same iteration pattern for training target completion.

## Trade-offs

- Pros: Clear audit trail (requested vs approved), simple approve operation, supports bulk approval cascades, derived status is always in sync
- Cons: Two relations for what is conceptually one value, requires careful handling when either is undefined
- Prefer when: A value must go through an approval process before becoming effective

## Related Patterns

- [mapped-operation-delegation](mapped-operation-delegation.md)
- [derived-attribute-flattening](derived-attribute-flattening.md)
