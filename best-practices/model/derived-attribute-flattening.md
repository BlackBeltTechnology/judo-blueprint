---
id: "derived-attribute-flattening"
title: "Derived Attribute Flattening"
domain: "model"
category: "transfer"
score: 82.4
usage_count: 17
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - trivia
  - rackinspect
  - itracker
  - actiongroup-test-react
  - alba
  - skillmatrix-model
  - mlszksz-platform
  - viterra_demo
  - mjsz
  - judo-demo-miniworkflow
  - ams-model
  - park-here
  - indamedia-adtrack
  - InterfaceRegister
  - judo-partner
  - workflow-poc
  - reserve-app
---
## Description

Transfer objects flatten navigation paths from entity relations into derived attributes, eliminating the need for clients to traverse relations. This includes single-hop flattening (`self.category.name`), multi-hop navigation (`self.question.category.name`), aggregate computations (`self.questions!count()`), and boolean computations (`self.status == ContestStatus#CLOSED`).

## Structure

- Derived attributes on transfer objects use `Getter expression` to navigate entity relations
- Common sub-patterns:
  - **Relation-to-string**: `self.relation.nameAttribute` (e.g., `categoryName = self.category.name`)
  - **Aggregate count**: `self.collection!count()` (e.g., `nrOfQuestions = self.questions!count()`)
  - **Aggregate sum**: `self.collection!sum(x | x.field)` (e.g., `annualSavingPotential = self.monthlyForecasts!sum(mf | mf.savingPotential)`)
  - **Boolean computation**: `self.field == Enum#VALUE` (e.g., `isClosed = self.status == CLOSED`)
  - **Deep navigation**: `self.rel1.rel2.attribute` (e.g., `category = self.question.category.name`)
  - **Computed concatenation**: Computed strings from multiple fields (e.g., `fullAddress`, `aggregatedName`)
  - **Date computation**: Derived from date fields with arithmetic (e.g., year/month extraction)
  - **Difference calculation**: Subtraction of two fields (e.g., `reportedQuantity - totalQuantity`)
  - **Container navigation**: `self!container(ParentType).attribute` for composition hierarchies
  - **Conditional expression**: Ternary operators for polymorphic display (e.g., guest vs owner)

## Examples

### Trivia
`admin::Question.categoryName` uses `self.category.name` to flatten the category relation. `admin::Category.nrOfQuestions` uses `self.questions!count()` for an aggregate. `player::Prompt.category` navigates 3 levels deep: `self.question.category.name`.

### RackInspect
Entity-level computed attributes: `Address.fullAddress` (composite from street, city, postal code), `Brand.aggregatedName` (composite from name, manufacturer, type), `RepairCategory.rackElementName`/`repairTypeName`/`brandName` (flattened from relations), `Address.cityAndPostalCode` (computed concatenation).

### itracker
Entity-level derived attributes: `Initiative.annualSavingPotential = self.monthlyForecasts!sum(mf | mf.savingPotential)` and `Initiative.annualSaving = self.monthlyForecasts!sum(mf | mf.saving)` aggregate financial data from compositions. `Initiative.actionDueMonth` uses date arithmetic: `Timestamp!of(self.actionDueDate)!year() * 12 + Timestamp!of(self.actionDueDate)!month() - 1`.

### SkillMatrix
Extensive entity-level flattening on `Skill`: `competenceName = self.competence.name`, `unitName = self.user.unit.name` (2-hop), `userFullName = self.user.fullName` (chained derived). Professional transfer flattens relations to strings: `unit = self.unit.name`, `manager = self.unit.manager.fullName` (3-hop), `nationality = self.nationality.code`.

### ActionGroupTest
Planet has 3 derived boolean attributes (`peaceful`, `inhabited`, `habitable`) computed from entity state. These are DERIVED memberType, Boolean, and filterable. Notably, `habitable` is used by the UI ActionGroup `enabledBy` mechanism to conditionally enable action groups, demonstrating derived attributes as UI control drivers.

### Alba
Extensive entity-level flattening: `User.fullName = self.lastName + " " + self.firstName` (concatenation), `Product.institutionName = self.author.institution.name` (2-hop), `Task.createdByName = self.createdBy.fullName` (chained derived), `Task.assigneeName = self.assignee.fullName`, `Task.productTitle = self.targetProduct.title`. Boolean state checks: `Product.isFinalizedOrApproved`, `User.isActive = self.status == AccountStatus#ACTIVE`.

### SkillMatrix-Model
64 derived members confirmed in model source. `Skill` entity has all 7 attributes derived (zero stored attributes): `competenceName`, `unitName` (2-hop: `self.user.unit.name`), `userFullName`, `approvedLevelName`, `requestedLevelName`, `approved`, `competenceScore`. `User.fullName = self.firstName + ' ' + self.lastName`, `User.indexName = self.lastName + ', ' + self.firstName`. `Result.reportName` uses container navigation: `self!container(Definition).name`.

### MLSZKSZPlatform
Extensive denormalized/derived fields: `Organization.cityName`, `Organization.regionName`, `Organization.fullAddress` flattened from the composed Address entity. `Address.cityName` and `Address.regionName` flattened from city/region relations. `FeedEntry` fully denormalizes post + organization data: `title`, `summary`, `organizationName`, `authorName`, `capabilities` for fast feed rendering without joins.

### Viterra Demo
Multi-level flattening across transfers: `ReportTransfer.clientName = self.client.name`, `ReportTransfer.clientId = self.client.id`, `ReportTransfer.displayPeriodName = self.period.displayName` (chained derived -- displayName is itself derived on Period). `PartnerOpenStockTransfer` flattens relation data: `commodityHun = self.commodity.hun`, `siloName = self.silo.name`, `siloPlace = self.silo.place`. Difference calculations: `StockTransfer.totalQuantityDiff = self.reportedQuantity - self.totalQuantity`.

### KozutEugyfelClient
Extensive flattening on `Felhasznalo`: `nev` concatenates `vezetekNev + " " + keresztNev` with null-safe ternary, `munkakorNev = self.munkakor.megnevezes`, `megyeNev = self.megye.megnevezes`, `szervezetiEgysegNev` computes composite from multiple relations. `Bejelentes` flattens: `felelosNev = self.felelos.nev`, `ugyintezoNev = self.ugyintezo.nev`. `cimke` builds a display label: `self.nev + " (" + self.email + ") " + self.szervezetiEgysegNev`.

### MJSZ
23 derived attributes across 10 entities (56% of non-transfer attributes). Key examples: `Player.fullName = self.lastName + " " + self.firstName` (Hungarian name order), `Player.clubName = self.club.name`, `Team.name = self!container(Club).name` (container navigation), `Match.venueAddress = self.venue.city + ", " + self.venue.address`, `Match.season = self!container(Tournament).season.year` (multi-hop container navigation), `Team.goalsFor/goalsAgainst` (conditional collection sums).

### judo-demo-miniworkflow
`Document.ownerRepresentation = self.owner.firstName + " " + self.owner.lastName + "(" + self.owner.email + ")"` flattens owner data for display. `DocumentHistoryEntryTransfer.userRepresentation` uses the same pattern. `Document.currentState = self.documentHistoryEntries!head(h | h.eventTime DESC).toState` derives the current state from the latest history entry using collection ordering.

### AMS-Model
Entity-level derived flattening on abstract `Request`: `applicationName = self.application.name`, `userName = self.user.fullName` (chained derived), `userEmail = self.user.email`, `responsibleName = self.user.manager.fullName` (2-hop navigation through self-referencing hierarchy). `User.fullName = self.lastName + " " + self.firstName` (Hungarian name order). `ConfirmationRequest.campaignStatus = self!container(Campaign).status` (container navigation for composed child). `isPending = self.status == Status#PENDING` (boolean computation).

### ParkHere
Entity-level derived attributes: `ParkingSlot.aggregaredName = self.id + " / " + self.floor!asString() + " (" + self.parkingGarage.name + ")"` (composite display string), `ParkingSlot.parkingGarageName = self.parkingGarage.name` (navigation shortcut). Conditional ternary expressions on Reservation: `reserverName = self.guest!isDefined() ? self.guest.name : self.owner.name`, `reserverCarId`, `reserverEmail` adapt display based on guest vs owner. `User.isNotAdministrator = not self.isAdministrator` (logical negation).

### IndamediaAdTrack
Calculated fields on `AggregatedCampaign`: `remainingBudget = totalBudget - totalSpend`, `remainingAverageDailySpend = remainingBudget / remainingDays`, `remainingDays` computed from end date. `todaySumSpend` aggregates from tracked campaigns. `User.isNotAdmin` derives as the negation of `isAdmin`. These stored-but-recalculated fields are maintained by `syncData` operations rather than being true derived attributes.

### InterfaceRegister
Dashboard transfer uses `welcomeText = 'Hi, ' + self.firstName` to derive a greeting from the User entity. Input DTOs use derived attributes with `self.*` getters for pre-populating from selected reference entities: `CreateApplicationVendorInput.address = self.address`, `CreateHighLevelConnectionApplicationInput.name = self.name`. These serve as read-only display fields in nested creation forms.

### judo-partner
Extensive derived display fields on transfers: `Partner.title` (display title), `Partner.primaryContactName` (flattened from primary contact relation), `Partner.primaryAddressSingleLine` (formatted single-line address), `Address.fullAddress` (composite), `Address.countryName` (denormalized from Country), `PartnerLog.name` (derived partner name for log display), `Taxpayer.queryTimestamp` (from related TaxpayerQuery).

### KozutEugyfelModelTest
Derived Boolean attributes on `Felhasznalo` using `!kindof()`: `szervezetiEgysegVezeto = self!kindof(SzervezetiEgysegVezeto)`, `ugyfelszolgalatiMunkatars = self!kindof(UgyfelszolgalatiMunkatars)`, `szervezetiEgysegMunkatars = self!kindof(SzervezetiEgysegMunkatars)`. These role-detection flags drive the forwarding authorization logic in `tovabbitas`.

### workflow-poc
Extensive derived attributes on the `Task` transfer (maps Token): `isAssigneeLogged` and `isSupervisorLogged` use ACTOR variable to check current user roles. `isCheckoutEnabled`, `isReleaseEnabled`, `isNavigable` derive enablement from assignee state and supervisor membership. `label = self.context.label` flattens context data. `workflow = self.context.workflow.name` chains 2-hop navigation. Count-based attributes on `TaskList`: `userTasksCount`, `unassignedTasksCount`, `supervisedAssignedTasksCount`.

### ReserveApp
`ReservationForPartner` includes derived string attributes for display: `projectAsString`, `recipientAsString`, `gateAsString`, `spotAsString` flatten related entity names into read-only table columns. Also includes computed `duration` and `durationHuman` derived from `start`/`end` timestamps. These provide display-friendly representations of related entities without relation traversal.

### AMS-Frontend
Same model as AMS-Model. Abstract `Request` uses 5 derived attributes for denormalization: `applicationName = self.application.name`, `userName = self.user.fullName`, `userEmail = self.user.email`, `responsibleName = self.user.manager.fullName` (2-hop through manager hierarchy), `isPending = self.status == Status#PENDING`. Transfer-level: `Campaign.ratio` concatenates `!count()!asString()` for progress display, `Campaign.isOpen`/`isClosed`/`isEmpty` compute UI guards.

## Trade-offs

- Pros: Simplifies client data access, reduces round-trips, enables table columns without relation traversal
- Cons: Derived attributes are read-only, may introduce performance overhead for deep navigation
- Prefer when: UI needs flat tabular data from related entities

## Related Patterns

- [actor-based-transfer-projection](actor-based-transfer-projection.md)
- [literal-derived-attribute](literal-derived-attribute.md)
