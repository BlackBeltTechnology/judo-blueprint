---
id: user-holiday-absence-tracking
title: "User Holiday/Absence Tracking Entity"
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - park-here
---

## Description

A Holiday (or Absence) entity composed by a User that tracks date ranges when the user is unavailable. Each Holiday has a startDate, endDate, and a derived back-reference to the owning user (holidayOwner). The User entity composes holidays (0..* COMPOSITION) and carries a queryCollidingHolidays query attribute to detect scheduling conflicts. Transfer objects expose holiday management through panels: a HolidayPanel lists all holidays with a create operation, and Holiday TOs have guard attributes (isNotDeletable) and a deleteHoliday operation. A HolidayInput unmapped TO carries the date range plus references to the user and potentially affected reservations for conflict detection. An AdditionalDay entity complements this pattern by defining calendar overrides -- marking specific dates as WORK or HOLIDAY using a DayType enum, enabling business day/holiday exceptions beyond the standard calendar.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Holiday" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind memberType } }
  }
} } }
```

```graphql
{ esm { enumerationtypes(where: { name: { eq: "DayType" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Holiday",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Holiday", name: "startDate"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Holiday", name: "endDate"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::User", name: "holidays",
  target: "{{NAMESPACE}}::Holiday", lower: 0, upper: -1,
  relationKind: COMPOSITION
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "DayType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DayType", name: "WORK", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DayType", name: "HOLIDAY", ordinal: 2
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "AdditionalDay",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AdditionalDay", name: "day"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::AdditionalDay", name: "typeOfDay"
} }) { success fqn } }
```

## Examples

### park-here
- **Holiday entity**: `ParkHere::entities::Holiday` (non-CRUD)
  - Attributes: startDate (req), endDate (req)
  - Relations: holidayOwner (0..1 DERIVED back to User)
- **User entity** composes holidays (0..* COMPOSITION) and has queryCollidingHolidays (query attribute) for conflict detection
- **AdditionalDay entity**: `ParkHere::entities::AdditionalDay` (non-CRUD)
  - Attributes: day (req), typeOfDay (req, DayType enum)
  - Managed via Configuration entity (additionalDays 0..* ASSOC)
- **DayType enum**: `ParkHere::entities::DayType` -- WORK(1), HOLIDAY(2)
  - Allows overriding calendar: marking a Saturday as WORK day, or a weekday as HOLIDAY
- **Transfer Objects**:
  - `Holiday` TO -- startDate, endDate, isNotDeletable (guard); operation: deleteHoliday (custom INSTANCE)
  - `HolidayInput` (unmapped) -- startDate, endDate, hiddenByCustom, userHidden, currentDate; relations: user (1..1 AGGREGATION), reservationsForDeleteInfo (0..* AGGREGATION)
  - `HolidayPanel` TO -- holidays (0..* ASSOC); operation: holiday (custom INSTANCE for creation)
  - `UserReservationPanel` TO -- includes holidays (0..* ASSOC) alongside reservation collections
- Holiday creation checks for colliding reservations via the HolidayInput's reservationsForDeleteInfo relation, enabling the UI to warn users about affected bookings
