---
id: action-group-input-output-routing
title: Action Group Input/Output Routing Pattern
description: A frontend that replaces the generated operation dialogs gives each action group operation its own input route and, when it returns a transfer object, an output route or dialog.
aliases: [operation input page, operation output page]
keywords: [action group, operation, input, output, routing, template, signed identifier, extra routes]
tags: ["domain:frontend", "layer:frontend", "project:actiongroup-test-react", "status:single-project"]
category: page
status: single-project
projects: [actiongroup-test-react]
evidence: ["actiongroup-test-react:unrecorded"]
alternatives: []
related: [promise-based-dialog-system, breadcrumb-navigation-context, complete-frontend-replacement]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Operations of an action group that take an input transfer object or return an output transfer object need UI for both. This practice gives every such operation a dedicated input page and, when the operation returns data, a dedicated output page that can itself offer further operations.

## Practice

### Platform base

- The generator already produces UI for an operation with input and output: an operation button on the view or table, an input form dialog when an input is declared, and a result display when an output is declared ([ESM operations to UI actions](../../agent-docs/frontend/model-screen-layout.md)). Use that default unless the UX needs more.
- An unbound operation can be marked as a template provider (`GET_TEMPLATE`); it returns a prepopulated prototype of the input transfer object, served by the REST layer under `<TO>/~template` ([operation reference](../../agent-docs/model/esm_metamodel/operation.md)). An input page can load this prototype on mount.
- Bound operations are called with the instance's signed identifier, which the server issues in responses and which changes after every update of the entity. Never store or rebuild it; take it from the latest response ([signed identifiers](../../agent-docs/backend/platform-behavior-reference.md)).
- Custom routes are added in `src/extra-routes.tsx`; the generated `routes.tsx` prepends them ([extra routes](../../agent-docs/frontend/extension-points.md)).

### Project practice: dedicated input and output routes

This layer is project practice (actiongroup-test-react), not a platform feature:

- Input route: `/{entity}/:signedIdentifier/{actionName}`. The page fetches the template on mount, edits it in a form, calls the bound operation with the signed identifier from the route and navigates back on success.
- Output route: `/{entity}/{actionName}/:signedIdentifier`. The page shows the returned transfer object in view or edit mode and may carry further operation buttons.
- Chained operations: the result of a follow-up operation is shown in a page dialog opened over the output page; the output page refreshes after the dialog closes.
- Complex inputs with nested associations use a range dialog for multi-selection.

```typescript
// Example project code: service names are generated per page, not fixed API
const template = await matterCreatorService.getTemplate();
setData(template);

await galaxyService.createDarkMatter({ __signedIdentifier: signedIdentifier }, data);
back(); // navigate back on success
```

```typescript
// Output page triggers a further operation and shows its result in a dialog
const result = await creatureService.hateGod(data);
if (result) {
  await openPageDialog(<CreatureHateGodOutput data={result} />);
  await fetchData(); // refresh after the action
}
```

## Rationale

Dedicated routes make operations linkable and keep each form small. Separating input and output pages lets an output page offer follow-up operations without growing the input form. The cost is routes and page components per operation.

## Example

actiongroup-test-react has three simple action inputs (create dark matter, interstellar dust, interstellar medium) as plain forms. One complex input (create creature) has a nested signs table that uses a range dialog for multi-selection. One output page (choose the messiah) works in view and edit mode and has three further action buttons; two of them render their results in a page dialog.

## When to avoid

- The generated operation dialogs are enough: no dedicated routes needed.
- Few operations exist, so extra routes and page components cost more than they give.
- Output-to-output chains get deep and make back navigation hard to follow.

## Related

- [[promise-based-dialog-system]] — dialogs opened from output pages
- [[breadcrumb-navigation-context]] — navigation context across nested pages
- [[complete-frontend-replacement]] — the frontend that hosts these routes
