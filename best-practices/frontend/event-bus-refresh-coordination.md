---
id: "event-bus-refresh-coordination"
title: "Event Bus for Cross-Page Refresh Coordination"
domain: "frontend"
category: "state"
score: 21.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - itracker
---
## Description

Generated JUDO pages use a publish/subscribe event bus to coordinate data refreshes across related pages. When one page performs a CRUD operation, it publishes a "refreshed" event. Other pages subscribing to that event can trigger their own refresh, keeping data consistent across open views. Event keys are derived from the page's UI model FQN.

## Structure

```typescript
// Publishing after a refresh
publish(
  'Admin/(esm/_xxxxx)/AccessViewPageDefinition:refreshed',
  refreshedData
);

// Subscribing in another page
useEffect(() => {
  const unsubscribe = subscribe(
    'refresh:Admin/(esm/_xxxxx)/AccessViewPageDefinition',
    async () => { await refresh(); }
  );
  return unsubscribe;
}, []);
```

Event key format: `{Actor}/(esm/{model-id})/{PageDefinition}:{event-type}`

## Examples

### Trivia
Admin frontend's Categories AccessViewPage publishes a `refreshed` event after each successful data refresh. Other pages displaying category data (e.g., Contest Categories RelationViewPage) can subscribe to this event to stay in sync. The event bus keys use ESM model IDs like `esm/_k9l8kGt-Ee-Yh8kDEDkPWA`.

### itracker
Event bus coordinates refreshes across the initiative workflow. When the Initiative AccessViewPage refreshes after an approve/reject/sendForApproval operation, the event propagates to the Initiatives AccessTablePage (dashboard) to update status columns. Also coordinates between embedded tab content (MonthlyForecasts, ForecastVersions) and the parent view.

## Trade-offs

- **Pros**: Loose coupling between pages; no direct page-to-page dependencies; consistent data across views; standard JUDO framework pattern
- **Cons**: Event key strings are opaque (model IDs); hard to debug event flows; no guaranteed delivery order
- **When to use**: Automatically used in generated JUDO pages -- understanding this helps when debugging data synchronization issues

## Related Patterns

- [viewmodel-context-pattern](viewmodel-context-pattern.md)
- [pandino-action-hook-override](pandino-action-hook-override.md)
