---
id: "thin-identifiable-result-for-parent-relation-create"
title: "Thin Identifiable Result for Parent-Relation Create Operations"
domain: "model"
category: "transfer"
score: 0.0
usage_count: 0
alternative_count: 0
first_seen: "2026-05-13"
last_updated: "2026-05-13"
projects:
  - compsych-letter-demo
---
## Purpose

Custom create operation on a parent (`A.createB(input) : ?`) should return a **thin Identifiable projection of B** — mapped TO carrying only `__identifier` plus a dummy attribute — and let `OperationFlowManager` redirect the UI to the **caller's relation view** of B. Avoids modelling a full B transfer projection just for the post-create landing page. Avoids the standalone `<BTO>View` route ever being the canonical surface for B.

## §1 The rule

For `A → B` via relation `A.bs : B[0..*]` (or single-valued `A.b : B[0..1]`), when create-B is a custom op `A.createB(input: BInput)`:

| Decision | Choice |
|---|---|
| Return type | **Mapped TO of B**, with a single dummy attribute. Carries `__identifier`. |
| Default Layer-1 navigation (standalone `<TO>View`) | **Suppressed** by `OperationFlowManager`. |
| Post-op landing | **Caller's relation view** — the same list the user opened the create form from, filtered/selected to the new row. |
| Full `BTO` mapped TO | Continues to exist for the relation list + detail. Not used as the op's return type. |

Effect: one canonical UI for B (the parent-rooted relation detail), one source of truth for B's mapped projection (`BTO`), and an id-carrying result that the frontend can route on without re-fetching by query.

## §2 Why a thin Identifiable, not the full `BTO`

JUDO requires a mapped TO to declare at least one mapped attribute. An identity-only return is therefore modelled as a **separate, minimal** mapped TO over B:

```
TransferObjectType IdentifiableB mapping B {
    name : String   // dummy. Never rendered. Exists to satisfy ESM mapping rule.
}
```

Reasons to prefer this over returning the full `BTO`:

| Reason | Detail |
|---|---|
| **Standalone `<BTO>View` stays unused** | Generator emits the route, but no op ever returns `BTO`, so no link/breadcrumb funnels users into it. One representation per concept. |
| **Decouples op contract from list/detail projection** | Adding/removing fields on `BTO` for the relation row UI does not change the op's payload contract. |
| **Wire payload minimal** | Result carries identifier only. Browser re-fetches via the canonical access-context detail after redirect. |
| **No accidental write-back coupling** | If the op result is ever piped into a `_refreshInstance<BTO>` / inline edit form by the generator, only the identifier is meaningful — no half-populated edit surface. |

The dummy attribute exists purely to satisfy the metamodel. `visible=false` on it removes it from the auto-form if any view ever instantiates the TO; in practice the TO is never rendered, only the id is read.

## §3 Why not `void` and refresh?

`void` return causes the caller list to refresh — new row appears, but the user has to scan/click it to open detail. Thin Identifiable carries the new `__identifier` out, enabling **direct row landing** via `OperationFlowManager` filterRecords/id navigation. Use `void` only when the create is fire-and-forget and the user should stay on the list with no row-selection signal.

## §4 Worked example — `A.createB`

Model (ESM mutation outline; adapt names to the local model):

```
// Full mapped TO for relation list + detail (canonical surface for B)
TransferObjectType BTO mapping B {
    name        : String
    description : String
    // … other rendered attributes
}

// Thin Identifiable TO — only ever used as createB's return type
TransferObjectType IdentifiableB mapping B {
    name : String   // dummy, satisfies mapping requirement
}

// Unmapped input TO — shape-divergent from BTO (see relation-driven-crud-with-custom-input §2)
TransferObjectType BCreateInput {
    name        : String  required
    description : String
    // …input-shape fields, may include parent reference, sentinels, etc.
}

// Custom op on parent
ATO.createB(input: BCreateInput) : IdentifiableB
    enabledBy: <expr gating create on A>
```

Frontend redirect (see [operation-flow-manager-redirect.md](../frontend/operation-flow-manager-redirect.md) for registration):

```typescript
import { OperationFlowManager, OperationInput } from '~/generated';

export const customFlowManager: OperationFlowManager = {
  shouldUseCustomFlow: (input: OperationInput) =>
    input.operationName === 'createB',

  handleResult: (input: OperationInput) => {
    // input.result is the IdentifiableB payload — only __identifier matters.
    return {
      actor: 'AActor',           // FQN of the actor whose access link surfaces the A→B relation
      access: 'as',              // access link name on the actor that resolves to the A row
      // navigate into the A's `bs` relation detail, filtered to new row:
      filterRecords: {
        __identifier: [{ operator: 'equal', value: input.result.__identifier }],
      },
    };
  },
};
```

If the relation list lives under a deeper path (`actor.as → A → bs`), use the navigation shape supported by your `OperationFlowManager` contract — id-based detail vs filterRecords list — per §3 return-type matrix of [relation-driven-crud-with-custom-input.md](relation-driven-crud-with-custom-input.md#3-return-type-matrix). The principle is the same: land in the **caller's relation view**, not in a standalone `<BTO>View`.

## §5 When this rule does NOT apply

| Case | Why thin-Identifiable is wrong |
|---|---|
| Op returns a different entity than what was created (e.g. returns the parent or a sibling) | Layer-1 default navigation is meaningful; redirect target depends on the actual returned entity. |
| Result needs immediate inline edit on the caller page (OPERATION_OUTPUT_UPDATE) | Generator emits an inline edit form from the returned mapped TO. Use the full `BTO`. See [operation-output-with-behaviors.md](operation-output-with-behaviors.md). |
| Multi-step workflow where the next step depends on backend-computed state (not just id) | Return a redirect TO carrying actor/access/operation per [operation-flow-redirect-pattern.md](../frontend/operation-flow-redirect-pattern.md). |
| Create is fire-and-forget; user should not be moved off the list | Return `void`. List refreshes; no row selection. |

## §6 Trade-offs

- **Pros** — single canonical view for B; op contract independent of `BTO` projection drift; minimal wire payload; standalone `<BTO>View` becomes inert; aligns with one-representation-per-concept rule (`relation-driven-crud-with-custom-input` §3).
- **Cons** — one extra TO declaration (`IdentifiableB`); requires `OperationFlowManager` registration for every such op; the dummy attribute is awkward and must be documented to discourage future readers from rendering it.
- **Prefer when** — create-on-relation custom op exists, parent has a canonical access-context relation list/detail for B, and you do not want generated standalone `<BTO>View` to be a reachable surface.

## See also

- [relation-driven-crud-with-custom-input.md](relation-driven-crud-with-custom-input.md) — §2 shape-divergent create rule; §3 return-type matrix; §5 anti-patterns
- [operation-flow-manager-redirect.md](../frontend/operation-flow-manager-redirect.md) — `OperationFlowManager` registration + handleResult recipes
- [operation-return-type-navigation.md](operation-return-type-navigation.md) — Layer-1 default behaviour that this rule overrides
- [operation-flow-redirect-pattern.md](../frontend/operation-flow-redirect-pattern.md) — `@redirect`-annotated multi-step workflow alternative
- [actor-based-transfer-projection.md](actor-based-transfer-projection.md) — one-TO-per-relation-target rule
- [managed-actor-admin-pattern.md](../backend/managed-actor-admin-pattern.md) — admin surface combining custom op + access-context redirect
