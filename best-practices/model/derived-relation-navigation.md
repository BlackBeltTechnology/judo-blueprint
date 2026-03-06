---
id: "derived-relation-navigation"
title: "Derived Relation via Navigation Expression"
domain: "model"
category: "relation"
score: 54.0
usage_count: 8
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - alba
  - skillmatrix-model
  - sanctuary-backend
  - park-here
  - judo-partner
  - workflow-poc
---
## Description

Entity or transfer relations use derived getter expressions to compute their contents by navigating through other relations, applying filters, or combining multiple sources. This avoids storing redundant relation data and keeps computed collections in sync with their source data.

## Structure

Common derived relation patterns:
- **Transitive navigation**: `self.relation1.relation2` (aggregates nested collections)
- **Filter expression**: `self.collection!filter(x | condition)` (subset of existing relation)
- **Self-reference**: `self` (presents same entity through different transfer projection)
- **Head expression**: `self.collection!filter(...)!head(x | x.field DESC)` (pick first from sorted filtered set)
- **Container navigation**: `self!container(ParentType).relation` (navigate up composition then down)
- **Alias**: `self.relation` (simple alias providing alternative naming or future extension point)

## Examples

### Trivia
Entity: `Contest.questions` is derived as `self.categories.questions` -- computes the union of all questions from linked categories. Transfer: `player::Contest.personalBests` uses `self.tests!filter(t | t.status == TestStatus#FINISHED and t.personalBest)` to show only finished personal-best tests.

### RackInspect
Entity derived relations: `FaultRegistry.racks` (all racks across fault headers), `Offer.serviceOffterItems` (filtered service-type offer items), `User.permissions` (aggregated from all assigned roles), `Partner.deliveryAddresses` (addresses filtered by isDelivery flag). Derived back-references: `container` relations on 14+ entities navigate to parent.

### SkillMatrix
Complex derived relations on `User`: `subordinates = self.managedUnits.members!filter(m | m.isActiveProfessional)` (transitive + filter), `skillTargets = self.trainingPlans.skillTargets` (flattening compositions), `lastTrainingPlan = self.trainingPlans!filter(p | not p.closed)!head(p | p.date DESC)` (filter + head). `TrainingPlan.incompleteSkillTargets = self!container(User).incompleteSkillTargets` (container navigation).

### Alba
`Product.currentVersion` uses head expression: `self.productVersions.versions!head(p | p.version desc)` to derive the latest version by sorting descending. `User.publicApprovedProducts` uses filter: `self.products!filter(p | p.state == ProductState#APPROVED)`. `ProductVersions.allProducts` uses transitive navigation: `self.versions.origin`.

### SkillMatrix-Model
7+ derived relations confirmed in model source. Key patterns: transitive navigation (`User.skillTargets = self.trainingPlans.skillTargets`), filter + head (`User.lastTrainingPlan = self.trainingPlans!filter(p | not p.closed)!head(p | p.date DESC)`), chained derived (`Tag.users = self.competences.users` reuses `Competence.users` derived relation), and container-based (`TrainingPlan.incompleteSkillTargets = self!container(User).incompleteSkillTargets`).

### KozutEugyfelClient
Filtered event collections on `Bejelentes`: `megjegyzesek` filters `esemenyek` for comments only, `tovabbitasok` filters for forwards. Complex filter: `self.esemenyek!filter(e | e.szoveg!isDefined() and e.szoveg!trim()!length() > 0 and e.szoveg!trim() != "null")!sort(e | e.idopont ASC)` -- filters non-empty text events and sorts chronologically.

### Sanctuary Backend
`User.effectiveRoles` is a derived relation with `getterExpression="self.roles"`, serving as an alias for the stored roles relation. Currently identical to `self.roles`, this pattern provides a future extension point for filtering or computing effective roles differently from directly assigned roles (e.g., including roles inherited through RoleGroups).

### ParkHere
`Reservation.parkingGarage` is a derived relation with getter `self.parkingSlot.parkingGarage` -- navigates through the parking slot to reach the garage without storing a direct reference. This single-hop transitive navigation avoids a redundant stored relation while keeping garage information accessible on the reservation.

### judo-partner
`Partner.primaryContact [0..1]` and `Partner.primaryAddress [0..1]` are derived relations that filter the composed collections by the `isPrimary` Boolean flag. `Taxpayer.headquarter [0..1]` derives from filtering `addresses` by type. `Taxpayer.taxNumber` and `Taxpayer.taxIdentifier` are derived from related `TaxpayerQuery` navigation. The `PartnerList.partners` and `PartnerList.partnerLogs` are derived collections providing user-scoped dashboard data.

### KozutEugyfelModelTest
`Bejelentes.felelos` is a derived relation using a complex chained expression: `self.esemenyek!asCollection(UgyintezoBeallitas)!filter(e | e.celFelhasznalo!kindof(FelelosFelhasznalo))!head(e | e.idopont DESC).celFelhasznalo`. This computes the current responsible user by finding the most recent handler-assignment event whose target is of type `FelelosFelhasznalo`.

### workflow-poc
`Token.authorizedUsers` is derived via transitive navigation: `self.state.transitions.role.users` -- navigates through current state to transitions, then to roles, then to users, collecting all authorized users. `Context.assignees` and `Context.lastTransitions` are also derived. Transfer-level: `TaskList.allTasks` and `TaskList.myTasks` use derived relations for filtered task views, and `Task.assignables`, `Task.authorizedUsers`, `Task.logEntries` are all derived from the mapped entity.

### AMS-Frontend
`ManagerApprovalList.approvals` is a derived relation with a compound filter: `self.approvals!filter(r | r.status == Status#PENDING and r.campaignStatus == CampaignStatus#OPEN)` -- filters the manager's approvals to show only pending requests from open campaigns. This demonstrates layered filtering where the access point filters by campaign status and the transfer relation further filters by request status.

## Trade-offs

- Pros: No data duplication, always consistent with source, supports complex navigation and filtering
- Cons: Derived relations are read-only, may have performance implications for deep/complex navigation
- Prefer when: Collection data can be computed from existing relations using navigation or filtering

## Related Patterns

- [derived-attribute-flattening](derived-attribute-flattening.md)
- [self-referencing-derived-relation](self-referencing-derived-relation.md)
- [container-back-reference](container-back-reference.md)
