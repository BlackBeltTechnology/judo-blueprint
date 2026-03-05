---
id: "container-back-reference"
title: "Derived Container Back-Reference Pattern"
domain: "model"
category: "relation"
score: 135.0
usage_count: 9
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
  - skillmatrix-frontend
  - skillmatrix-model
  - kozut-eugyfel-client
  - mjsz
  - ams-model
  - park-here
  - judo-partner
  - ams-frontend
---
## Description

Child entities have a DERIVED ASSOCIATION relation named `container` with cardinality `0..1` pointing back to their parent entity. This provides a computed reverse navigation path from child to parent without storing an explicit foreign key on the child. The getter expression navigates the inverse of the parent's composition or association.

## Structure

- Child entity defines: `container -> ParentType [0..1] ASSOCIATION DERIVED`
- The getter expression computes the parent reference (inverse navigation)
- Cardinality is `0..1` because the child may not yet be attached to a parent
- Used for both composition and association reverse navigation
- Commonly named `container` by convention, though the name may vary by context
- Can also be used inline in derived expressions: `self!container(ParentType).attribute`

## Examples

### RackInspect
14+ entities use the container pattern: `Address.container -> Partner`, `BankAccount.container -> Partner`, `Warehouse.container -> Address`, `Rack.container -> Warehouse`, `CompanyAddress.container -> CompanyData`, `CompanyEmail.container -> CompanyData`, `UserAddress.container -> User`, `UserEmail.container -> User`, `UserPhone.container -> User`, `DimensionTemplateGroup.container -> DimensionTemplate`, `PhoneNumber.container -> Partner`.

### SkillMatrix
`self!container()` used in derived expressions: `TrainingPlan.incompleteSkillTargets = self!container(SkillMatrix::User).incompleteSkillTargets` navigates from a composed TrainingPlan up to its owning User. `report::Result.reportName = self!container(SkillMatrix::report::Definition).name` navigates from Result up to its parent Definition. `TrainingPlan.subordinateName = self!container(SkillMatrix::User).fullName` in the manager transfer.

### SkillMatrix-Model
3 container references confirmed in model source: `self!container(SkillMatrix::User).fullName` (TrainingPlan back to User for subordinate name), `self!container(SkillMatrix::User).incompleteSkillTargets` (TrainingPlan navigates to User's filtered targets), `self!container(SkillMatrix::report::Definition).name` (Result navigates to parent Definition for report name). All use inline `!container()` syntax rather than explicit container relations.

### KozutEugyfelClient
`Ertesites` (Notification) uses `self!container(e_ugyfelszolgalat::entities::Esemeny)` to navigate from notification up to its parent Esemeny (Event) entity, deriving `idopont`, `kezdemenyezoNev`, and `esemenyTipus` from the containing event without storing them directly on the notification.

### MJSZ
Extensive container navigation across composed children. `Team.name = self!container(mjsz::Club).name` derives the team name from its owning club. `Match.season = self!container(mjsz::Tournament).season.year` navigates Match -> Tournament -> Season (multi-hop). `Match.tournament = self!container(mjsz::Tournament).name`. `License.player = self!container(mjsz::Player).firstName` derives the player's name.

### AMS-Model
`ConfirmationRequest.campaignStatus = self!container(ams::entities::Campaign).status` navigates from the composed ConfirmationRequest up to its owning Campaign entity to derive the campaign's current status. This allows the transfer object to display campaign context without a stored relation, since ConfirmationRequest is composed within Campaign via `Campaign.confirmationRequests [0..*] COMPOSITION`.

### ParkHere
2 explicit container back-references: `Car.carOwner = self!container(ParkHere::entities::User)` navigates from composition child Car to owning User, and `Holiday.holidayOwner = self!container(ParkHere::entities::User)` navigates from composition child Holiday to owning User. Both use domain-specific naming (`carOwner`, `holidayOwner`) rather than the generic `container` convention.

### judo-partner
`Address.partner [0..1]` and `Contact.partner [0..1]` are DERIVED ASSOCIATION back-references from composition children to their owning Partner. `TaxpayerAddress.taxpayer [0..1]` similarly derives back to the owning Taxpayer. These enable child-to-parent navigation for display purposes (e.g., showing which partner an address belongs to).

### AMS-Frontend
`ConfirmationRequest.campaignStatus = self!container(ams::entities::Campaign).status` navigates upward from composed child to parent Campaign. This enables the Manager actor's `approvalList` filtering by campaign status without a stored relation: `self.approvals!filter(r | r.campaignStatus == CampaignStatus#OPEN)`.

## Trade-offs

- Pros: No stored foreign key needed, computed on demand, enables child-to-parent navigation in getter expressions
- Cons: Derived relations are read-only, slight runtime computation cost, naming convention must be followed
- Prefer when: Child entities need to navigate to their parent for display or computed attributes

## Related Patterns

- [composition-ownership](composition-ownership.md)
- [derived-relation-navigation](derived-relation-navigation.md)
- [derived-access-filtering](derived-access-filtering.md)
