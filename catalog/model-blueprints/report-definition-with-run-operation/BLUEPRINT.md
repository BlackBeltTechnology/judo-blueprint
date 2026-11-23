---
id: report-definition-with-run-operation
title: Report Definition Entity with Run Operation and Result Export
description: "A report definition entity that captures report parameters (selected entities, filters) and produces report results via a `run` instance operation."
aliases: [report configuration, saved report, report run history]
keywords: [report, definition, run, operation, result, export, snapshot, excel]
tags: ["domain:model", "layer:model", "project:skillmatrix-model", "status:single-project"]
category: pattern
status: single-project
projects: [skillmatrix-model]
evidence: ["skillmatrix-model:unrecorded"]
alternatives: []
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let a user configure a report once, run it many times and keep each run as a timestamped result. The definition holds the parameters (which units or users to include). Every run adds a result that captures the output of that moment, for example a generated Excel file.

### A definition owns its results

Results are composed inside the definition. Deleting a definition deletes its run history. A result knows its definition by navigating up to its container.

### A run is an instance operation

The user triggers the run on one definition. The operation creates a new result, snapshots the matching subjects and stores a timestamp.

## Structure

- `ReportDefinition`: a required `name`, an association `subjects` (0..*) to the entities the report covers, and a composition `results` (0..*) to `ReportResult`. It has an instance operation `run`.
- `ReportResult`: a timestamp `executedAt`, a binary `file` that holds the export, an association `subjects` (0..*) to the entities included in this run, and a derived `reportName` that reads the name from the owning definition with the container navigation. It has an instance operation `createExcel` with a custom implementation.
- Reporting transfer objects live in their own package, apart from the core domain. They flatten the reported entities into rows with denormalized attributes (full name, unit name, score) so that a table needs no nested navigation. A row transfer object whose attributes are all transient serves as a flat row for the export.

## Constraints

- `run` and `createExcel` are instance operations, so they are bound to one instance. The caller must reach that instance through a transfer object that its actor can see, otherwise the platform denies the call. See [platform behavior reference](../../agent-docs/backend/platform-behavior-reference.md). The operations are exposed as mapped operations on the report transfer objects.
- The result keeps what the run produced. Later changes to the subjects do not change an existing result: it is a snapshot, which is project practice.
- Creating the result and filling it is custom backend code. The platform generates the operation interface; the body is project code. See [custom operations](../../agent-docs/backend/custom-operations.md).
- A binary attribute travels as a file-store token: the client downloads the file in a separate call after reading the token. See [platform behavior reference](../../agent-docs/backend/platform-behavior-reference.md).
- The report overlay is a read model. Keep it in its own package and do not add business rules to it.

## Variations

- **Run returns the result.** The run operation returns the new result as its output instead of void, so the client can open it directly.
- **Export as a separate step.** As in the source project, `createExcel` is a second operation on the result. The run only snapshots, and the user exports on demand.
- **Parameters on the run.** Pass filters as an input transfer object instead of storing them on the definition, when they change on every run.
- **Different output.** Replace the Excel file by a PDF or a Markdown text. The result shape stays the same.

## When to use

- Users need repeatable reports with saved parameters.
- Each run must be kept as a snapshot for later comparison.
- The report needs a downloadable file.

## When to avoid

- The report is a live view with no history. Use a dashboard transfer object, see [[dashboard-transfer-object]].
- Results do not need to be stored. A static operation that returns the data is enough.
- The report parameters change on every call and nothing needs saving.

## Related

- [[dashboard-transfer-object]] — a live read model instead of stored run results
- [[exchange-rate-entity]] — another entity that stores dated snapshots
