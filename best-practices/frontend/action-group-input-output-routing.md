---
id: "action-group-input-output-routing"
title: "Action Group Input/Output Routing Pattern"
domain: "frontend"
category: "page"
score: 34.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - actiongroup-test-react
---
## Description

Model action groups as dedicated routes with separate input and output page components. Input pages collect form data and call the action service method. Output pages display action results, optionally with further action buttons. Routes follow the pattern `/{entity}/:signedIdentifier/{actionName}` for inputs and `/{entity}/{actionName}/:signedIdentifier` for outputs. Output pages can also be rendered in PageDialogs for nested action chains.

## Structure

```
routes:
  /galaxies/:id/createDarkMatter       -> Action input page
  /planet/:id/createCreature            -> Action input with nested associations
  /planet/chooseTheMessiah/:id          -> Action output page
```

Input page pattern:
```typescript
// Fetch template on mount
const res = await viewMatterCreatorServiceImpl.getTemplate();
setData(res);

// Submit action
await viewGalaxyServiceImpl.createDarkMatter(
  { __signedIdentifier: signedIdentifier } as JudoIdentifiable<ViewGalaxy>,
  data,
);
back(); // Navigate back on success
```

Output page pattern:
```typescript
// Output page can trigger further actions
const result = await viewCreatureServiceImpl.hateGod(data);
if (exists(result)) {
  await openPageDialog(<ViewCreatureHateGodOutput data={result} />);
  await fetchData(); // Refresh after action
}
```

## Examples

### ActionGroupTestReact
3 action group inputs (CreateDarkMatter, CreateIntergalacticDust, CreateInterstellarMedium) as simple forms. 1 complex input (CreateCreature) with nested Signs table using RangeDialog for multi-selection. 1 output page (ChooseTheMessiah) with View/Edit mode and 3 further action buttons (HateGod, LoveGod, TalkToGod), where HateGod/LoveGod results render in PageDialog.

## Trade-offs

- **Pros**: Clean separation of action input/output UI; dedicated routes enable direct linking; output pages support chained actions; complex inputs with nested associations
- **Cons**: Each action group adds routes and page components; navigation flow can be deep; output-to-output chains complicate back navigation
- **When to use**: When model operations require dedicated input forms or display structured output results

## Related Patterns

- [promise-based-dialog-system](promise-based-dialog-system.md)
- [breadcrumb-navigation-context](breadcrumb-navigation-context.md)
- [complete-frontend-replacement](complete-frontend-replacement.md)
