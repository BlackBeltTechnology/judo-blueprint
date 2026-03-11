---
id: "report-definition-with-run-operation"
title: "Report Definition Entity with Run Operation and Result Export"
score: 30.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - skillmatrix-model
---
## Description

A report definition entity that captures report parameters (selected entities, filters) and produces report results via a `run` instance operation. The pattern consists of:

- **Definition** -- a named report configuration with associations to the entities being reported on (e.g., selected users, selected units). It owns a collection of Result instances via COMPOSITION.
- **Result** -- a timestamped report execution result that stores the output (e.g., an Excel binary file) and references the entities included in the report. A `createExcel` operation with custom implementation generates the actual export file.
- **Report transfer objects** -- projections that flatten reported entities for tabular display, with denormalized attributes (e.g., fullName, unitName, competenceScore) to avoid nested navigation.

This pattern enables repeatable, parameterized reporting: the user configures a report definition once (selecting which units/users to include), then runs it multiple times to produce timestamped result snapshots. Each result captures the state of the data at the time of execution.

The report layer typically lives in its own package (e.g., `report::`) separate from the core domain entities, acting as a read-model overlay.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
