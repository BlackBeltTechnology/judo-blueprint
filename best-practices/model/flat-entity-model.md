---
id: "flat-entity-model"
title: "Flat Entity Model (No Generalization)"
domain: "model"
category: "entity"
score: 184.9
usage_count: 13
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - itracker
  - actiongroup-test-react
  - alba
  - skillmatrix-model
  - viterra_demo
  - kozut-eugyfel-client
  - mjsz
  - judo-demo-miniworkflow
  - sanctuary-backend
  - park-here
  - judo-partner
  - reserve-app
alternatives:
  - generalization-base-entity
---
## Description

All entity types are concrete with no abstract parents or inheritance hierarchies. The domain model is completely flat with no generalization relationships. Variation is handled through composition, enums, and different transfer projections rather than entity inheritance.

## Structure

- All entities are concrete (not abstract)
- No generalization/inheritance relationships between entities
- No shared base entity types
- Variation is achieved through:
  - Enum-typed status attributes for lifecycle variation
  - Different transfer projections per actor for view variation
  - Composition for parent-child ownership

## Examples

### Trivia
All 9 entities (User, Question, Contest, Test, Category, Prompt, Application, Upload, Admin) are concrete with no inheritance. `User` and `Admin` are separate entities despite similar attributes (email, active) -- no shared base type.

### itracker
All 8 entities (Initiative, Region, SRTCategory, MonthlyForecast, ForecastVersion, MonthlyForecastVersion, User, Application) are concrete with zero generalization hierarchies. MonthlyForecast and MonthlyForecastVersion are separate entities (not sharing a base) despite similar attributes.

### ActionGroupTest
All 11 entity types (God, Galaxy, Star, Planet, Creature, CreatureTemplate, Matter, MatterCreator, Astronomer, Sign, Message) are concrete with zero generalization. Template types (CreatureTemplate, MatterCreator, Message) are separate unmapped types rather than inheriting from their corresponding entities.

### Alba
All 11 entities (Product, ProductVersion, ProductVersions, User, Institution, Attachment, Audience, Curriculum, ResultType, Event, Task) are concrete with no inheritance. Role-based polymorphism is achieved through 44 transfer objects instead of entity generalization. The research explicitly notes "No explicit inheritance hierarchies exist in this model."

### SkillMatrix-Model
All 21 entities confirmed flat with zero `GeneralizationType` declarations in the model source. Entities like `User`, `Competence`, `Skill`, `SkillLevel`, `TrainingPlan`, `SkillTarget`, `Tag`, `Note` are all standalone. Role-based polymorphism achieved via 37 transfer objects and boolean role flags (`isActiveAdmin`, `isActiveHREmployee`, `isActiveProfessional`) rather than entity inheritance.

### Viterra Demo
All 7 entities (Period, Client, Silo, Stock, Commodity, Report, Application) are concrete with no inheritance. No abstract entities or supertypes defined. Variation handled through 10 transfer objects providing different views per actor (3 Report projections, 2 Client projections, 2 Stock projections).

### KozutEugyfelClient
All 13 entities (Bejelentes, Kep, Erkezteto, Megye, SzervezetiEgysegTipus, Esemeny, Ertesites, Felhasznalo, SzervezetAzonosito, Munkakor, TovabbitasAction, ResztvevoAction, JarokeloStaging) are concrete with no inheritance. Role variation achieved via derived boolean flags on Felhasznalo and 20 transfer objects across 3 actors.

### MJSZ
All 10 entities (License, Player, Season, Tournament, Transfer, Match, Club, Team, Venue, Application) are concrete with no inheritance. No abstract entities. The research explicitly notes this as unusual: common patterns like a base entity with audit fields are absent. Simplicity is the design goal.

### judo-demo-miniworkflow
All 4 entities (Document, Files, DocumentHistoryEntry, User) are concrete with no inheritance. Despite the small model size, no shared base type is used. Variation is handled entirely through 10 transfer objects (4 self-mapped, 4 enhanced/actor-specific, 2 transient input DTOs) and the DocumentState enum.

### Sanctuary Backend
All 6 entities (User, UserPrivacySettings, UserSettings, PositionTitle, Role, RoleGroup) are concrete with no inheritance. No abstract entities or generalization hierarchies. Variation is handled through composition (settings as composed children of User) and a shared `ActiveStatus` enum for lifecycle status across User and PositionTitle.

### ParkHere
All 12 entities (User, Car, Guest, Reservation, ParkingGarage, ParkingSlot, Configuration, Doorman, DoormanNotified, Holiday, AdditionalDay, Initializer) are concrete with no inheritance. Polymorphism achieved through enum-based type discrimination (ReservationType), role boolean flags on User, and 41 transfer objects providing different views. Research explicitly notes this as a flat entity model with behavior in operations rather than type hierarchies.

### judo-partner
All 23 entity types are concrete with no abstract parents or generalization hierarchies. Despite having two distinct domains (partner and registry) with substantial entity count, the model remains completely flat. Variation across similar entities (e.g., Address and TaxpayerAddress) is handled through separate entity types rather than shared base types.

### ReserveApp
All 15 entity types are concrete with no abstract parents or inheritance relationships. The entity graph is entirely flat despite moderately complex domain (freight reservations, partners, gates, spots, projects). Variation is handled through the `Role` enum for user classification and 40 transfer objects across 5 actors for view variation.

## Trade-offs

- Pros: Simple to understand, no inheritance complexity, straightforward persistence mapping
- Cons: Potential attribute duplication across similar entities, no polymorphic queries
- Prefer when: Domain is small or entities are sufficiently distinct that inheritance would add unnecessary complexity

## Related Patterns

- [enum-state-machine](enum-state-machine.md) (alternative to inheritance for variation)
- [actor-based-transfer-projection](actor-based-transfer-projection.md) (alternative to inheritance for different views)
- [generalization-base-entity](generalization-base-entity.md) (alternative: use inheritance for shared infrastructure)
