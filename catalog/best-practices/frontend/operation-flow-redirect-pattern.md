---
id: operation-flow-redirect-pattern
title: Operation Flow Redirect via Generator Override and OperationFlowManager
description: "Implement dynamic post-operation navigation by combining a Handlebars generator template override with a custom `OperationFlowManager` service."
aliases: []
keywords: [OperationFlowManager, redirect, processRedirect, workflow navigation, generator fragment, post-operation]
tags: ["domain:frontend", "layer:frontend", "project:workflow-poc", "status:single-project"]
category: navigation
status: single-project
projects: [workflow-poc]
evidence: ["workflow-poc:unrecorded"]
alternatives: []
related: [post-operation-navigation-hook, handlebars-generator-template-override, application-customizer-hub, operation-return-type-navigation]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Let the backend decide where the user goes after an operation: to a record, to another operation, or to a page. Operations return a redirect transfer object, a generator fragment hands such results to `processRedirect`, and an `OperationFlowManager` service translates the payload into navigation. Used for multi-step workflows.

## Practice

### Platform base

- Try the declarative route first: an operation form can navigate to an access whose target type matches the operation's output type ([[operation-return-type-navigation]]).
- `OperationFlowManager` and `OPERATION_FLOW_MANAGER_INTERFACE_KEY` come from `~/utilities/application`. You register your implementation as a Pandino service from `application-customizer.tsx`. `handleResult(input)` receives the stored operation result, including `__entityType`, and returns `{ actor, access, filterRecords?, operation? }`. `shouldUseCustomFlow(input)` limits it to chosen result types ([OperationFlowManager](../../agent-docs/frontend/hooks/action-hooks.md)).
- Per-page `post<Operation>Action` handlers cover one operation ([[post-operation-navigation-hook]]).
- Fragment overrides work by placing a same-named file in the override directory. The docs prefer hooks over template overrides because you maintain them at every upgrade ([template override process](../../agent-docs/frontend/README.md), [[handlebars-generator-template-override]]).

### Project practice: redirect objects plus a fragment override

The `@redirect` annotation, the `processRedirect` call and the fragment path below are project practice (workflow-poc); they are not covered by the agent-docs. Confirm the fragment name and the template context on your generator version.

- **Model**: operations that decide the next screen return a small redirect transfer object: target actor and access, plus either an id name and value (open a record) or an operation (start a follow-up). The output carries the `redirect` annotation.
- **Fragment**: the project overrides the generated fragment that handles an operation's primary output, so that a result whose output type has the annotation goes to `processRedirect(result)` and any further code runs only when there is no redirect.
- **Manager**: `handleResult` maps the payload: with an id name and value return `filterRecords` on that attribute, with an operation return `operation`, otherwise only actor and access.

```typescript
// Example project code (application-customizer.tsx)
const operationFlowManager: OperationFlowManager = {
  handleResult: (input) => {
    const { actor, access, idName, idValue, operation } = input as any;
    if (idName && idValue) {
      return { filterRecords: { [idName]: [{ operator: 'equal', value: idValue }] }, access, actor };
    }
    if (operation) return { operation, access, actor };
    return { access, actor };
  },
};
context.registerService(OPERATION_FLOW_MANAGER_INTERFACE_KEY, operationFlowManager);
```

Keep the redirect payload in the model so backend and frontend agree on one contract.

## Rationale

One override and one manager serve every annotated operation, with no hook per page, and the backend drives the flow. The costs: Handlebars knowledge, a tight contract between backend and frontend, an override that breaks if the template structure changes, and a flow that is harder to debug than plain navigation.

## Example

workflow-poc operations (start, navigate, execute, assign) return create or update redirect objects. The fragment routes them to `processRedirect`, and the manager opens the target record with a filter or triggers the next operation, giving a multi-step task flow without per-page hooks.

## When to avoid

- The destination is fixed: use the output type navigation ([[operation-return-type-navigation]]).
- A few operations need navigation: use post-operation hooks ([[post-operation-navigation-hook]]).
- You do not want to maintain a template override across upgrades.

## Related

- [[post-operation-navigation-hook]] — per-page alternative
- [[handlebars-generator-template-override]] — the fragment override mechanism
- [[application-customizer-hub]] — where the manager is registered
- [[operation-return-type-navigation]] — declarative navigation by output type
