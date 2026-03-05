---
id: "single-access-entity-pattern"
title: "Single Access Entity Fetch and Create-If-Missing"
domain: "frontend"
category: "page"
score: 11.9
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - actiongroup-test-react
---
## Description

Fetch a singleton entity (single access pattern) using `godServiceForEntity.get('{}')` with an empty JSON key. If the entity exists, proceed to the view page. If not, redirect to a create page. This handles the case where a domain model has exactly one instance of an entity type (e.g., "Earth" in a universe model, or application settings). The "god" service provides root-level access to the single instance.

## Structure

```typescript
const init = async () => {
  try {
    const { __signedIdentifier } = await godServiceForEarthImpl.get('{}');
    if (__signedIdentifier) {
      setSignedIdentifier(__signedIdentifier);
      await fetchData(); // Load full entity with relations
    } else {
      navigate('/earth/create'); // Redirect to create
    }
  } catch (error) {
    errorHandling(error, enqueueSnackbar);
  }
};

// Two-phase fetch: get identifier first, then refresh with mask
const fetchData = async () => {
  const res = await viewPlanetServiceImpl.refresh(
    { __signedIdentifier } as JudoIdentifiable<ViewPlanetStored>,
    queryCustomizer
  );
  setData(res);
};
```

## Examples

### ActionGroupTestReact
Earth entity uses `godServiceForEarthImpl.get('{}')` to check existence. If found, loads full entity via `viewPlanetServiceImpl.refresh()` with relations (creatures table). If not found, navigates to `/earth/create`. Create page uses `godServiceForEarthImpl.create()`. View page supports conditional action buttons based on entity state (habitable, inhabited, peaceful).

## Trade-offs

- **Pros**: Clean handling of singleton entities; automatic redirect to create; two-phase fetch separates existence check from data loading
- **Cons**: Extra API call for existence check; empty key `'{}'` is a JUDO convention that may confuse developers; create flow needs back navigation
- **When to use**: Any entity that follows the single-access pattern in the JUDO model (exactly one instance per actor)

## Related Patterns

- [action-group-input-output-routing](action-group-input-output-routing.md)
- [view-edit-mode-toggle](view-edit-mode-toggle.md)
