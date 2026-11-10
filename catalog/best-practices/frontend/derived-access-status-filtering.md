---
id: derived-access-status-filtering
title: Derived Access Points for Status-Based Filtered Views
description: Give each lifecycle status its own derived access on the actor so the generated menu offers pre-filtered table pages instead of runtime filter controls.
aliases: [status menu items, filtered access tables, task-oriented menu]
keywords: [derived access, getterExpression, status filter, menu, table page, lifecycle, navigation]
tags: ["domain:frontend", "layer:frontend", "project:doors-model", "status:single-project"]
category: mapping
status: single-project
projects: [doors-model]
evidence: ["doors-model:unrecorded"]
alternatives: []
related: [approval-workflow-conditional-visibility, dual-actor-frontend-architecture, admin-default-generated-ui]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Users of a workflow application want to open "my drafts", "pending" or "rejected" items directly. Modeling one filtered access per status yields one menu entry and one generated table page per status, with no frontend code.

## Practice

### Platform base

- Every access of an actor becomes a navigation entry, and the access target determines the generated page type: a table access gives a table page ([navigation controller and actor accesses](../../agent-docs/frontend/model-screen-layout.md), [navigation elements](../../agent-docs/frontend/esm-to-ui-mappings/tables-navigation.md)).
- An access of type `DERIVED` carries a `getterExpression` that selects the rows; `ALL` has no getter ([access point reference](../../agent-docs/model/esm_metamodel/accesspoint.md)).
- Getter rules at actor scope ([architectural patterns: getter rules](../../agent-docs/backend/architectural-patterns.md), [JQL cheatsheet](../../agent-docs/model/model-development.md)): the filter starts from the entity, not from the transfer object (`<model>::entities::<Entity>!filter(x | ...)`); there is no `self` at actor scope; a boolean literal is rejected for `DERIVED` (use `ALL` for an unfiltered access); primitives in `!getVariable` calls must be fully qualified.
- Filtering runs in the backend as part of the access query, so the page only receives matching rows. Row-level permissions of the access (creatable, updatable, deletable) are set per access ([access testing patterns](../../agent-docs/integration-testing/access-and-derived-testing.md)).

### Project practice: one access per status

- Add one `DERIVED` access per status of interest, all pointing to the same transfer object, with a filter on the status attribute. Reusing one table definition for all of them keeps columns identical across the status pages.
- Give each access its own menu entry, and group the entries (for example "my tasks", "my items by status", "all items") to keep the menu readable.
- Make accesses read-only or editable per status, depending on what users may do in that state.
- Add a new status by adding an access and an entry; there is no runtime combination of status filters. If users need free filtering, keep one unfiltered table with the table's own filter controls instead.
- Test each access getter per actor (see the access testing guide above): a wrong predicate silently shows the wrong rows.

## Rationale

Navigation becomes task-oriented and the filter is enforced in the model rather than client controls. The cost is one generated page per access (duplicated generated code), a longer menu, and a model change per new status.

## Example

doors-model, employee actor: nineteen accesses, a dozen of them `DERIVED` status filters over the contract entity (created, uploaded, rejected, finalized, to close, in progress, plus global and division views). The menu groups them as my tasks, my contracts as officer, contracts and partners. One contract table definition with eight columns is reused by all filtered views.

## When to avoid

- Few statuses or ad-hoc filtering needs: a single table with filter controls is enough.
- The filter needs several values or external data: a plain getter cannot express it; see [[derived-access-filtering]] for the model side.
- Many statuses that would flood the menu: group them or use tabs inside one page.

## Related

- [[derived-access-filtering]] — the model-side derived access with getter filtering
- [[approval-workflow-conditional-visibility]] — status-driven visibility inside a page
- [[dual-actor-frontend-architecture]] — separate actors for separate audiences
- [[admin-default-generated-ui]] — fully generated actor UI
