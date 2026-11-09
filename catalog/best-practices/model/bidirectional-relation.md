---
id: "bidirectional-relation"
title: "Bidirectional (Two-Way) Relation Pattern"
domain: "model"
category: "relation"
score: 73.6
usage_count: 15
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - itracker
  - actiongroup-test-react
  - alba
  - skillmatrix-model
  - mlszksz-platform
  - viterra_demo
  - mjsz
  - judo-demo-miniworkflow
  - ams-model
  - sanctuary-backend
  - park-here
  - indamedia-adtrack
  - judo-partner
  - workflow-poc
  - reserve-app
---
## Description

Two entities define a TwoWayRelationMember that represents both sides of a bidirectional association. When one side is set, the other is automatically maintained. This is used when both entities need navigable references to each other and the framework should enforce referential consistency.

## Structure

- Both entities define `TwoWayRelationMember` with `partner` referencing each other
- One side is marked `primary="false"` (the non-owning side)
- Cardinalities can differ on each side (e.g., `1..1` on one side, `0..*` on the other)
- Both sides use `ASSOCIATION` kind and `STORED` member type
- Setting the relation on either side automatically updates the other

## Examples

### itracker
`Initiative.user [1..1] <--> [0..*] User.initiatives` -- every Initiative must reference its owning User, and each User can have multiple Initiatives. This is the only bidirectional relation in the model, used for the core ownership relationship. The User side is not exposed on the actor-level User transfer, keeping initiatives navigation internal.

### SkillMatrix
6 TwoWay relations forming a rich bidirectional graph: `User.unit <-> Unit.members`, `User.managedUnits <-> Unit.manager`, `User.skills <-> Skill.user`, `Competence.skills <-> Skill.competence`, `Competence.tags <-> Tag.competences`, `Competence.skillTargets <-> SkillTarget.competence`. Each has a `primary` side for ownership semantics.

### ActionGroupTest
`Planet.creatures [0..*] <-> Creature.planet [0..1]` forms a bidirectional many-to-one. The Planet side is AGGREGATION (collection with ADD/REMOVE), while the Creature side is a single relation with SET/UNSET. This allows navigation from both directions: a Planet knows its Creatures, and a Creature knows its Planet.

### Alba
7 TwoWay relation pairs: `Institution.teachers <-> User.institution`, `Product.author <-> User.products`, `Product.version <-> ProductVersion.origin`, `Product.events <-> Event.product`, `Product.relatedTasks <-> Task.targetProduct`, `Task.createdBy <-> User.createdTasks`, `Task.assignee <-> User.tasks`. The primary side is typically the "many" end (e.g., Task.createdBy is primary=true, User.createdTasks is primary=false).

### SkillMatrix-Model
12 TwoWayRelationMember declarations confirmed in model source (6 pairs). Key pairs include `User.skills [0..*] <-> Skill.user [0..1]` (junction entity), `Competence.tags [0..*] <-> Tag.competences [0..*]` (many-to-many), and `User.managedUnits [0..*] <-> Unit.manager [0..1]` (management hierarchy). Two-way relations enable derived navigation like `User.subordinates = self.managedUnits.members!filter(...)`.

### MLSZKSZPlatform
6 TwoWay relation pairs for user-centric entities: `Device <-> User` (1..1 <-> 0..*), `Document <-> Announcement` (0..1 <-> 0..*), `FeedEntry <-> Organization` (0..1 <-> 0..*), `Inquiry <-> User` (1..1 <-> 0..*), `Notification <-> User` (1..1 <-> 0..*), `Invitation <-> InvitationRecipient` (1..1 <-> 0..*). Common pattern: user-adjacent system entities (Device, Notification, Inquiry) use two-way relations so both the user and the system entity can navigate to each other.

### Viterra Demo
2 bidirectional pairs: `Client.reports [0..*] <-> Report.client [1..1]` (clients own reports, primary on Report side) and `Period.reports [0..*] <-> Report.period [1..1]` (periods contain reports). Both link the Report entity to reference data for two-way navigation, enabling derived attributes like `ReportTransfer.clientName = self.client.name`.

### KozutEugyfelClient
Bidirectional relations on `Bejelentes`: `resztvevok [0..*] <-> Felhasznalo` (participants can navigate back to their reports), `esemenyek [0..*] <-> Esemeny.bejelentes` (events reference their parent report). Operations like `hozzaadResztvevo` and `leiratkozas` use `this.resztvevok += / -=` to modify the two-way participant collection.

### MJSZ
6 bidirectional pairs forming a rich sports domain graph: `Player.club [0..1] <-> Club.players [0..*]`, `Player.teams [0..*] <-> Team.players [0..*]` (many-to-many), `Season.tournaments [0..*] <-> Tournament.season [1..1]`, `Tournament.teams [0..*] <-> Team.tournament [1..1]`, `Match.homeTeam [1..1] <-> Team.homeMatches [0..*]`, `Match.visitorTeam [1..1] <-> Team.visitorMatches [0..*]`. Notable: Team has two separate two-way relations to Match for home/visitor roles.

### judo-demo-miniworkflow
`Document.owner [1..1] <-> User.documents [0..*]` forms a bidirectional ownership relationship. The Document side is required (every document must have an owner), while the User side is a collection (users can own multiple documents). This relation is used in permission checks: `self.owner == currentUser` determines if the current actor is the document owner.

### AMS-Model
10 two-way relations across the model. Self-referencing: `User.manager [0..1] <-> User.subordinates [0..*]` (organizational hierarchy). Cross-entity: `Application.requests [0..*] <-> Request.application [1..1]`, `User.requests [0..*] <-> Request.user [1..1]`, `User.applications [0..*] <-> Application.admin [0..1]`, `User.approvals [0..*] <-> ConfirmationRequest.approver [1..1]`, `User.issues [0..*] <-> AccessRequest.issuer [1..1]`. The User entity has 6 bidirectional relations, serving as the hub of the domain graph.

### Sanctuary Backend
2 bidirectional pairs for many-to-many role management: `User.roles [0..*] <-> Role.users [0..*]` (User is primary) and `User.roleGroups [0..*] <-> RoleGroup.users [0..*]` (User is primary). Both sides marked `createable="false"`, preventing circular CRUD issues while maintaining navigability from both User and Role/RoleGroup.

### ParkHere
3 bidirectional pairs: `ParkingGarage.parkingSlots [0..*] <-> ParkingSlot.parkingGarage [1..1]` (primary on garage side), `ParkingGarage.accessedUsers [0..*] <-> User.accessedParkingGarages [0..*]` (many-to-many access control), `User.reservations [0..*] <-> Reservation.owner [1..1]` (primary on user side). The User-ParkingGarage many-to-many relation enables bidirectional access control navigation.

### IndamediaAdTrack
Multiple bidirectional pairs for the campaign tracking domain: `Client.accounts [0..*] <-> Account.client [1..1]`, `Client.aggregatedCampaigns [0..*] <-> AggregatedCampaign.client [1..1]`, `Account.trackedCampaigns [0..*] <-> TrackedCampaign.account [0..1]`, `AggregatedCampaign.trackedCampaigns [0..*] <-> TrackedCampaign.aggregatedCampaign [1..1]`, `Credential.account [1..1] <-> Account.credential [0..1]`. All use ASSOCIATION kind with no cascade delete.

### judo-partner
Extensive TWO-WAY relations across both domains: `Partner.participants [0..*] <-> CaseParticipant.partner [1..1]`, `Case.records [0..*] <-> Record.case [0..1]`, `Case.participants [0..*] <-> CaseParticipant.case [1..1]`, `Register.records [0..*] <-> Record.register [1..1]`, `Record.versions [0..*] <-> RecordVersion.record [1..1]`, `Taxpayer.query [1..1] <-> TaxpayerQuery.taxpayer [0..1]`. The registry domain is heavily interconnected via two-way relations.

### KozutEugyfelModelTest
2 bidirectional pairs: `Felhasznalo.esemenyek [0..*] <-> Esemeny.kezdemenyezo [0..1]` (user initiated events, navigable from both sides) and `Felhasznalo.intezendok [0..*] <-> Bejelentes.ugyintezo [0..1]` (user's assigned complaints, with `primary=true` on the Felhasznalo side). These enable the derived `intezendoBejelentesek` access.

### workflow-poc
Multiple bidirectional pairs for the workflow engine: `Token.assignee [0..1] <-> User.tokens [0..*]` (token assignment), `Token.context [1..1] <-> Context.tokens [0..*]` (token-context linkage), `Role.users [0..*] <-> User.roles [0..*]` (many-to-many role membership), `User.contexts [0..*] <-> Context.assignables [0..*]` (user-context assignment). The two-way relations enable the derived authorization expressions like `self.state.transitions.role.users` for computing authorized users.

### ReserveApp
9 bidirectional pairs forming the logistics domain graph: `FreightReservation.partner [0..1] <-> Partner.freightReservations [0..*]`, `FreightReservation.gate [0..1] <-> Gate.freightReservations [0..*]`, `FreightReservation.project [0..1] <-> Project.freightReservations [0..*]`, `FreightReservation.spot [0..1] <-> Spot.freightReservations [0..*]`, `FreightReservation.items [0..*] <-> Item.freightReservation [0..1]`, `Partner.contacts [0..*] <-> User.partner [0..1]`, `Company.contacts [0..*] <-> User.company [0..1]`, `Project.users [0..*] <-> User.projects [0..*]` (many-to-many), `Project.spots [0..*] <-> Spot.projects [0..*]` (many-to-many).

### AMS-Frontend
10 two-way relations. Self-referencing: `User.manager [0..1] <-> User.subordinates [0..*]` (manager hierarchy, drives `isActiveExpression`). Cross-entity pairs: `Application.requests <-> Request.application`, `User.requests <-> Request.user`, `User.approvals <-> ConfirmationRequest.approver`, `User.issues <-> AccessRequest.issuer`, `User.applications <-> Application.admin`. User entity is the hub with 6 bidirectional relations.

## Trade-offs

- Pros: Automatic referential consistency, navigable from both directions, framework-managed
- Cons: Tighter coupling between entities, both entities must be aware of the relation, may add complexity
- Prefer when: Both entities need to navigate to each other and referential consistency must be enforced automatically

## Related Patterns

- [composition-ownership](composition-ownership.md)
- [container-back-reference](container-back-reference.md) (alternative for one-way back-navigation)
