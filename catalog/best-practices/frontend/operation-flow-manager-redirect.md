---
id: operation-flow-manager-redirect
title: OperationFlowManager Redirect to Access-Context View
description: "Register a custom OperationFlowManager so that the result of an operation lands on the access-context view of the row instead of a generated standalone transfer object view, keeping one representation per concept."
aliases: [post-operation redirect, access-context redirect, flow manager override]
keywords: [OperationFlowManager, shouldUseCustomFlow, handleResult, filterRecords, access context, redirect, OPERATION_FLOW_MANAGER_INTERFACE_KEY]
tags: ["domain:frontend", "layer:frontend", "project:compsych-letter-demo", "status:single-project"]
category: navigation
status: single-project
projects: [compsych-letter-demo]
evidence: ["compsych-letter-demo:unrecorded"]
alternatives: [operation-flow-redirect-pattern, post-operation-navigation-hook]
fragment: "none: frontend-only"
first_seen: 2026-05-11
last_updated: 2026-11-10
---
## Intent

By default, the output of a custom operation that returns a mapped transfer object navigates to the generated standalone view of that transfer object. The same row is also reachable through the actor's access (`Actor.access.<area>.<rel>`, then row, then detail), which is a different generated page. Two pages for one row drift apart, bug fixes land in one of them, and the row has two URLs.

The rule is one representation per concept: choose the access-context view as canonical and redirect every post-operation landing into it. The standalone routes are still generated but are never visited.

## Practice

### Platform base

- `OperationFlowManager` and `OPERATION_FLOW_MANAGER_INTERFACE_KEY` (value `'OperationFlowManager'`) are exported from `~/utilities/application`. You register your implementation as a Pandino service from `application-customizer.tsx` ([OperationFlowManager](../../agent-docs/frontend/hooks/action-hooks.md)).
- `handleResult(input)` receives the stored result of the operation, with `__entityType`, and returns `{ actor, access, filterRecords?, operation? }`. `shouldUseCustomFlow(input)` limits the manager to chosen result types. Branch on `input.__entityType`; examples in the docs that use `input.operation`, `tab` or `refresh` are illustrative.
- Files under `src/custom/` are never regenerated ([action hooks, keep custom hooks under src/custom](../../agent-docs/frontend/hooks/action-hooks.md)).
- The agent-docs state the same design principle and link here for the recipes.

### Practice notes: land on the filtered access table

The recipes below are practice on top of that hook. Where the old text used `input.operationName`, `input.result.entityId` or an `id` key, treat those as *verify*: the documented input is the result object itself and the documented return keys are `actor`, `access`, `filterRecords`, `operation`.

| Goal | `handleResult` returns |
|---|---|
| Filtered access table landing on a specific row | `{ actor, access, filterRecords: { entityId: [{ operator: 'equal', value: <row entityId> }] } }` |
| Access-context detail by signed identifier | `{ actor, access, id: <row __identifier> }` (*verify*: `id` is not in the documented return type) |
| Stay on the caller page and refresh | `{ refresh: true }` (*verify*: appears only in illustrative docs examples) |
| Default generated view | `null` |

`actor` is the actor name string and `access` the access name, as generated.

```typescript
// Example code: src/custom/hooks/operationFlowManager.tsx
import { OPERATION_FLOW_MANAGER_INTERFACE_KEY, type OperationFlowManager } from '~/utilities/application';

export const customFlowManager: OperationFlowManager = {
  // inviteUser returns the newly created user transfer object
  shouldUseCustomFlow: (input) => (input as any)?.__entityType === 'UserTO',
  handleResult: (input) => ({
    actor: 'Viewer',
    access: 'users',
    filterRecords: { entityId: [{ operator: 'equal', value: (input as any).entityId }] },
  }),
};

// src/custom/application-customizer.tsx
context.registerService<OperationFlowManager>(OPERATION_FLOW_MANAGER_INTERFACE_KEY, customFlowManager);
```

Registration lives in `application-customizer.tsx`, which this frontend protects with `.generator-ignore`.

## Rationale

- One canonical view means one place for fixes and one URL per row.
- The result opens the `users` table filtered to the new row, so the user sees it in its normal context.
- Cost: the standalone generated views remain as dead code, and the manager is global, so `shouldUseCustomFlow` must be narrow.

## Example

In one app a custom operation `AdminDashboard.inviteUser(input)` returns the created user transfer object. Without a custom manager the app opened the standalone user view. With the manager above it opens the admin users table filtered to the new user's row. The model side of this admin surface is described in [[managed-actor-admin-pattern]].

## When to avoid

- When the declarative route is enough: an operation form can navigate to an access whose target type matches the output type.
- When only one page's operation needs a different landing: use the per-page post-operation hook ([[post-operation-navigation-hook]]).
- When the backend decides the destination through redirect objects: see [[operation-flow-redirect-pattern]].

## Related

- [[relation-driven-crud-with-custom-input]] — return-type matrix and capability ladder that motivate the redirect
- [[managed-actor-admin-pattern]] — admin surface combining a custom operation with the redirect
- [[operation-flow-redirect-pattern]] — backend-driven redirect variant
- [[post-operation-navigation-hook]] — narrower, per-action navigation hook
- [[application-customizer-hub]] — registration entry point conventions
