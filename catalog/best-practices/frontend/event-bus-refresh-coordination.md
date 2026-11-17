---
id: event-bus-refresh-coordination
title: Event Bus for Cross-Page Refresh Coordination
description: How generated pages are observed to publish refresh events to a publish/subscribe bus, and when to use post-refresh handlers or table refresh actions instead of depending on it.
aliases: [cross-page refresh, publish subscribe refresh, refresh events]
keywords: [event bus, refresh, publish, subscribe, post refresh, page actions hook, refreshTable, cross-page]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "project:itracker", "project:park-here", "status:emerging"]
category: state
status: emerging
projects: [trivia, itracker, park-here]
evidence: ["trivia:unrecorded", "itracker:unrecorded"]
alternatives: []
related: [viewmodel-context-pattern, pandino-action-hook-override]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

When one page changes data, other open views of related data must refresh. This entry records what was observed about the event bus in generated pages and states which documented mechanisms to build on.

## Practice

### Platform base

- The agent-docs do not document the event bus: no publish or subscribe API and no event key format are specified there. Treat the bus as an internal detail of the generated frontend; do not rely on its key strings in custom code.
- Documented refresh mechanisms: page and dialog hooks (`<Container>PageActionsExtended`) have an optional `post<RefreshAction>` handler (for example `postRefreshAction`) that runs after a data refresh. Return it from the page actions hook created from the `register<Page>ActionsHook` scaffold; its parameters are generated per page ([PostRefresh action hook](../../agent-docs/frontend/advanced-patterns.md)). The `context.actions.refreshTable` style helpers in the docs are illustrative, so check the generated types.
- Page actions hooks receive `(data, editMode, storeDiff, refresh, submit)` depending on the page kind, so a custom handler can call `refresh` itself ([action hooks: page actions](../../agent-docs/frontend/hooks/action-hooks.md)). Operation flows can request a refresh after an operation completes.

### Practice notes: observations and guidance

- Observed behavior: a generated page publishes a "refreshed" event after a successful refresh, keyed by its UI model page definition, and that related generated pages (a relation page of the same data, an embedded tab and its parent view, a dashboard table after approve or reject operations) stay in sync through it. The keys contain opaque model identifiers.
- Do not hard-code those keys: they change when the model changes. If a custom page must react to another page's data change, use the documented post-refresh handler of the page that owns the data, or refresh on navigation.
- When debugging stale data across pages, first check whether the operation triggers a refresh at all, then whether the second page was mounted during the change.
- Event delivery order is not guaranteed; do not chain logic on it.

## Rationale

The bus gives generated pages loose coupling, so no page needs a direct reference to another. The cost is opaque keys, hard-to-trace event flows and no guaranteed order, which is why custom code should use documented hooks.

## Example

- An admin page publishes a refresh event after each successful refresh, and pages showing the same data can stay in sync through it.
- After approve, reject or send-for-approval operations on a document view, the event reaches the documents dashboard table, and coordinates embedded tabs with their parent view.

## When to avoid

- Writing custom code against event keys: use the post-refresh handler or the page's `refresh` instead.
- Data that changes outside the UI (other users, backend jobs): the bus does not cover it; refresh on a timer or on demand.

## Related

- [[viewmodel-context-pattern]] — sharing state across pages
- [[pandino-action-hook-override]] — the documented hook route for refresh handling
