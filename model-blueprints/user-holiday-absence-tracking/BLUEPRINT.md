---
id: "user-holiday-absence-tracking"
title: "User Holiday/Absence Tracking Entity"
score: 61.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - park-here
---
## Description

A Holiday (or Absence) entity composed by a User that tracks date ranges when the user is unavailable. Each Holiday has a startDate, endDate, and a derived back-reference to the owning user (holidayOwner). The User entity composes holidays (0..* COMPOSITION) and carries a queryCollidingHolidays query attribute to detect scheduling conflicts. Transfer objects expose holiday management through panels: a HolidayPanel lists all holidays with a create operation, and Holiday TOs have guard attributes (isNotDeletable) and a deleteHoliday operation. A HolidayInput unmapped TO carries the date range plus references to the user and potentially affected reservations for conflict detection. An AdditionalDay entity complements this pattern by defining calendar overrides -- marking specific dates as WORK or HOLIDAY using a DayType enum, enabling business day/holiday exceptions beyond the standard calendar.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
