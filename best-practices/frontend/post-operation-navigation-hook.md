---
id: "post-operation-navigation-hook"
title: "Post-Operation Navigation with Success Feedback"
domain: "frontend"
category: "hook"
score: 73.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
---
## Description

Override `postOperationAction` callbacks in page or dialog hooks to provide user feedback and navigate to related views after a backend operation completes. The typical pattern is: (1) show a success snackbar, (2) refresh the current page data, and (3) open a related view or dialog with the operation output. This creates a smooth workflow where the user is guided to the next logical step after completing an action.

## Structure

```typescript
const hookImpl = (data, editMode, storeDiff, refresh) => ({
  async postPriceModifiersForOfferItemAction(data, output) {
    showSuccessSnack(t('judo.action.operation.success'));
    await refresh();
    await openOutputViewDialog({ ownerData: output });
    await refresh();
  },

  async postCreateRackAction(output) {
    const created = await fetchCreatedEntity(output.__identifier);
    navigate(entityViewPageRoute, { signedIdentifier: created.__signedIdentifier });
  },
});
```

## Examples

### RackInspect
Three page hooks implement post-operation navigation for price modifiers: after `postOfferItemsPriceModifiersForOfferItemAction`, shows success snack, refreshes data, and opens the price modifiers output view dialog. Other hooks navigate to newly created entities (racks, fault registries) after creation.

## Trade-offs

- **Pros**: Smooth user workflow; immediate feedback; automatic navigation to relevant views
- **Cons**: Multiple sequential async operations can be slow; error handling needed for each step; refresh-heavy pattern
- **When to use**: After any backend operation where the user should see the result or be guided to a related view

## Related Patterns

- [pandino-action-hook-override](pandino-action-hook-override.md)
- [pdf-preview-inline-display](pdf-preview-inline-display.md)
