---
id: "range-expression-filtering"
title: "Range Expression Filtering for Relation Selection"
domain: "model"
category: "relation"
score: 60.7
usage_count: 6
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - alba
  - skillmatrix-model
  - viterra_demo
  - park-here
  - reserve-app
---
## Description

Transfer object relations use range expressions to restrict the set of selectable target entities. This limits which entities can be linked through the relation, enforcing business rules at the model level (e.g., only approved items can be selected).

## Structure

- A mapped relation on a transfer object includes a `rangeExpression`
- The expression uses `EntityType!filter(...)` to restrict selectable values
- Typically filters by status enum to ensure only valid entities are linkable
- Often combined with `!sort()` for ordered picker lists

```
fixedQuestions: Question[] 0..*
  range: trivia::entities::Question!filter(q | q.status == QuestionStatus#APPROVED)
```

## Examples

### Trivia
`admin::Contest.fixedQuestions` has a range expression `trivia::entities::Question!filter(q | q.status == QuestionStatus#APPROVED)` -- admin users can only link APPROVED questions to a contest, preventing use of unapproved or rejected questions.

### SkillMatrix
8+ range expressions for pickers. `hrEmployee::Skill.competence` uses `Competence!filter(c | c.active)!sort(c | c.name ASC)` to show only active competences. `professional::Skill.requestedLevel` uses `SkillLevel!sort(l | l.score ASC)` for ordered skill level selection. `report::Definition.selectedUsers` uses `User!filter(u | u.isActiveProfessional)` to restrict to active professionals.

### Alba
`ApprovalTaskInput.users` uses range expression `User!filter(u | u.isActive and (u.role == UserRole#TEACHER or u.role == UserRole#APPROVER))` to restrict approver selection to active teachers and approvers only. This ensures approval tasks can only be assigned to eligible users.

### SkillMatrix-Model
Model source confirms 8+ range expressions with `rangeType="DERIVED"`. Key patterns: `SkillLevel!sort(l | l.score ASC)` (entity-as-enum ordered picker, used 3+ times), `Competence!filter(c | c.active)!sort(c | c.name ASC)` (active-flag filter + sort), `Tag!sort(t | t.name ASC)` (alphabetical sort), `User!filter(u | u.isActiveProfessional)` (role-based filter for report user selection).

### Viterra Demo
`ReportTransfer.client` uses `rangeExpression="viterra::Client!filter(c | c.active)"` to restrict client selection to active clients only, preventing deactivated partners from being assigned to new reports. This integrates with the soft-delete active flag pattern.

### ParkHere
2 range expressions on User entity: `accessedParkingGarages` uses `ParkHere::entities::ParkingGarage!filter(g | g.isActive)` to restrict garage selection to active garages only. `preferredParkingSlot` uses `self.accessedParkingGarages.parkingSlots` to cascade the filter -- preferred slot must be in an accessible (active) garage. This chain of range expressions demonstrates filtering based on navigation through previously-filtered relations.

### ReserveApp
9 range expressions on transfer relations, all filtering by `active` flag: `ManagedUser.company` uses `Company!filter(c | c.active)`, `ReservationForPartner.recipient` uses `Company!filter(c | c.active)`, `ReservationForPartner.project` uses `Project!filter(p | p.active)`, etc. Contextual range: `ReservationForPartner.spot` uses `self.project.spots` to cascade spots based on the selected project, creating a dynamic dependent picker.

## Trade-offs

- Pros: Business rules enforced at model level, no custom code needed, UI automatically shows only valid options
- Cons: Only supports filter-based restrictions (no complex logic), expression must be JQL-compatible
- Prefer when: A relation should only allow linking to a subset of target entities based on status or other criteria

## Related Patterns

- [enum-state-machine](enum-state-machine.md)
- [derived-access-filtering](derived-access-filtering.md)
