---
id: post-operation-navigation-hook
title: Post-Operation Navigation with Success Feedback
description: "In the page or dialog hook that runs after a backend operation, show a success message, refresh the page and open a related view or navigate to the created entity. Hook names and signatures are generated per page."
aliases: [post-operation hook, success snack and navigate, navigate after create]
keywords: [post operation, action hook, navigation, success feedback, snackbar, refresh, output dialog, signed identifier, operationflowmanager]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: hook
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/pages/registerServicesOffer_servicesOffersPanelOffersRelationViewPageActionsHook.ts", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/pages/registerServicesFault_registry_servicesMyTaskPanelMyOffersRelationViewPageActionsHook.ts", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/pages/registerServicesFault_registry_servicesFaultRegistryFaultRegistry_View_EditGenerateOfferOutputViewActionsHook.ts"]
alternatives: []
related: [pandino-action-hook-override, pdf-preview-inline-display, operation-flow-redirect-pattern]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

After an operation finishes, guide the user to the next step: confirm success, refresh what is on screen, and open the result or the newly created entity.

## Practice

### Platform base

- Page and dialog hook types have optional `post<Operation>Action` handlers; their names and parameters are generated for the page, so read the generated types and the `register<Page>ActionsHook` scaffold instead of copying a name from another page ([action hooks](../../agent-docs/frontend/hooks/action-hooks.md), [PostRefresh action hook](../../agent-docs/frontend/advanced-patterns.md)).
- There is a second, global mechanism for where the user lands after an operation: `OperationFlowManager` (registered as `OPERATION_FLOW_MANAGER_INTERFACE_KEY` from `application-customizer.tsx`). Its `handleResult` receives the stored operation result, with `__entityType`, and returns the actor and access to open ([OperationFlowManager](../../agent-docs/frontend/hooks/action-hooks.md)). Use it when the redirect is the same for every call of an operation type; see [[operation-flow-redirect-pattern]].

### Practice notes: per-page post-operation handlers

- In the handler: show a success snackbar, refresh the page data, then open the related view or dialog with the operation output (an output view dialog for a discount operation).
- After a create operation, take the created entity's identifier from the output, load the entity and navigate to its view page with the signed identifier. Navigation targets use signed identifiers, not raw ids.
- Handle errors for each step; the steps run in sequence.
- The handler names and helpers (`showSuccessSnack`, `openOutputViewDialog`, `fetchCreatedEntity`, `navigate`) in the sketch are illustrative.

```typescript
// Illustrative; the generated hook type defines the real signature.
async postDiscountsAction(data, output) {
  showSuccessSnack(t('judo.action.operation.success'));
  await refresh();
  await openOutputViewDialog({ ownerData: output });
  await refresh();
}
```

## Rationale

The user gets immediate feedback and lands on a relevant view. The cost is several sequential async calls, per-step error handling and extra refreshes.

## Example

One app has three page hooks for discounts: after the operation they show a success snack, refresh, and open the discounts output view dialog. Other hooks navigate to a newly created product or order after creation.

## When to avoid

- A single redirect rule fits all operations of a type; use `OperationFlowManager` instead of per-page hooks.
- The operation output is of no interest to the user; the generated default (refresh and message) suffices.

## Related

- [[pandino-action-hook-override]] — how action hooks are registered
- [[pdf-preview-inline-display]] — a post-operation hook that opens a file
- [[operation-flow-redirect-pattern]] — global post-operation redirect
