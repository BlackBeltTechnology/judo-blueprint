---
id: "operation-flow-manager-redirect"
title: "OperationFlowManager Redirect to Access-Context View"
domain: "frontend"
category: "navigation"
score: 0.0
usage_count: 0
alternative_count: 0
first_seen: "2026-05-11"
last_updated: "2026-05-11"
projects:
  - compsych-letter-demo
---
## Purpose

Override default mapped-TO navigation. Redirect custom-op results to canonical access-context views. Avoid dual-view modelling.

## §1 Why redirect

Default mapped-TO output navigation lands on generated standalone `<TO>View` route. Same row also reachable via `Actor.access.<area>.<rel> → row → detail` — a DIFFERENT generated page. Two views drift; bug-fixes land in one. Two URLs for same row.

Rule: **one representation per concept**. Pick access-context view as canonical. Redirect every post-op landing into it. Standalone routes generated but unvisited.

See [relation-driven-crud-with-custom-input.md — §3 return-type matrix](../model/relation-driven-crud-with-custom-input.md#3-return-type-matrix).

## §2 Extension point

Pandino DI service. Register under `OPERATION_FLOW_MANAGER_INTERFACE_KEY` from `~/generated`.

```typescript
// src/custom/hooks/operationFlowManager.tsx
import { OperationFlowManager, OperationInput } from '~/generated';

export const customFlowManager: OperationFlowManager = {
  shouldUseCustomFlow: (input: OperationInput) => {
    return input.operation === 'CREATE' || input.operation === 'UPDATE';
  },

  handleResult: (input: OperationInput) => {
    return null; // fall through to default per-op recipe
  },
};
```

`shouldUseCustomFlow` returns `true` → framework calls `handleResult`. Return spec drives navigation.

## §3 Recipes

| Goal | `handleResult` return |
|---|---|
| Access-context detail (canonical view) | `{ actor, access, id: result.__identifier }` |
| Filtered list landing on specific row | `{ actor, access, filterRecords: { entityId: [{ operator: 'equal', value: result.entityId }] } }` |
| Stay + refresh caller page | `{ refresh: true }` |
| Fall through to default `<TO>View` | `null` |

`actor` = actor FQN string (e.g. `'LetterUser'`). `access` = access link name (e.g. `'users'`). `id` = signed `__identifier` from the result payload.

## §4 Worked example — `inviteUser`

Custom op `AdminDashboard.inviteUser(input: UserInvitationInput) : UserTO`. Returns the newly-created `UserTO`. Default behaviour: navigate to standalone `<UserTO>View` route. Desired behaviour: land on new user's row inside `admin.users` access-context detail.

```typescript
import { OperationFlowManager, OperationInput } from '~/generated';

export const customFlowManager: OperationFlowManager = {
  shouldUseCustomFlow: (input: OperationInput) =>
    input.operationName === 'inviteUser',

  handleResult: (input: OperationInput) => {
    return {
      actor: 'LetterUser',
      access: 'users',
      filterRecords: {
        entityId: [{ operator: 'equal', value: input.result.entityId }],
      },
    };
  },
};
```

Result: `admin.users` table opens, filtered to the new user's row, row selected. Single canonical view. No standalone `<UserTO>View` URL ever visited.

Pair with model-side admin pattern: [managed-actor-admin-pattern.md](../backend/managed-actor-admin-pattern.md).

## §5 Registration boilerplate

```typescript
// src/custom/application-customizer.tsx
import {
  BundleContext,
  OPERATION_FLOW_MANAGER_INTERFACE_KEY,
} from '~/generated';
import { customFlowManager } from './hooks/operationFlowManager';

export const applicationCustomizer = (context: BundleContext) => {
  context.registerService(
    OPERATION_FLOW_MANAGER_INTERFACE_KEY,
    customFlowManager,
  );
};
```

`.generator-ignore` protects `src/custom/application-customizer.tsx` from generator overwrite.

## See also

- [relation-driven-crud-with-custom-input.md](../model/relation-driven-crud-with-custom-input.md) — §3 return-type matrix; §4 capability ladder
- [managed-actor-admin-pattern.md](../backend/managed-actor-admin-pattern.md) — admin-surface example combining custom-op + redirect
- [operation-flow-redirect-pattern.md](operation-flow-redirect-pattern.md) — alternative for `@redirect`-annotated multi-step workflows
- [post-operation-navigation-hook.md](post-operation-navigation-hook.md) — per-action navigation hook (narrower than `OperationFlowManager`)
- [application-customizer-hub.md](application-customizer-hub.md) — registration entry point conventions
- action-hooks.md `OperationFlowManager` section in `judo-frontend-docs` skill — full hook reference
