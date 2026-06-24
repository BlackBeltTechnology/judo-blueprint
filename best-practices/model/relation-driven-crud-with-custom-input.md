---
id: "relation-driven-crud-with-custom-input"
title: "Relation-Driven CRUD with Custom-Input Operations"
domain: "model"
category: "transfer"
score: 0.0
usage_count: 0
alternative_count: 0
first_seen: "2026-05-11"
last_updated: "2026-05-11"
projects:
  - compsych-letter-demo
---
## Purpose

JUDO CRUD philosophy. Relation auto-wiring + custom-op shape divergence + return-type-driven UI navigation + capability ladder. Mandatory reading before designing any access link, custom op, or admin surface.

## §1 Relation auto-wiring from mapped target TO

`[0..*]` relation `X.relY : Y[0..*]` auto-generates UI affordances from `Y` mapped attributes. Same engine for `ActorType.access` links and plain `TransferObjectType` relations.

| `Y` outer flag | Relation flag | Auto-generated UI |
|---|---|---|
| — | (R always) | Table view. Columns = `Y` mapped attributes. |
| — | (R always) | Row-click → detail form bound to `Y`. |
| `Y.updateable=true` | U-flag | Inline edit on detail form. Save → `_updateInstance<Y>`. |
| `Y.createable=true` | C-flag | "Add" button → create form from `Y` mapped attributes. |
| `Y.deleteable=true` | D-flag | Row delete action. |

Access link vs. plain relation differs in:
- Security gating (`enabledBy` chain, `getterExpression` filter, scope on LIST).
- Routing (access link surfaces in menu; plain relation reached via parent navigation).
- Principal-projection semantics (`actorType` back-link exclusivity — see [accesspoint.md — Principal back-link exclusivity](../../agent-docs/model/esm_metamodel/accesspoint.md#principal-back-link-exclusivity)).

Access link vs. plain relation does NOT differ in form / table generation. Same affordances from same `Y` flags.

**One TO per relation target.** Single `Y` per relation. Table columns + detail form + create form + edit form all from `Y`. Row-click → detail bound to same `Y`. No drift.

See §5 anti-patterns for `<X>ListTO` separate-from-detail anti-pattern.

## §2 Custom operations for shape-divergent mutations

Auto-generated create form derives fields from `Y`'s mapped attributes. Shape-divergent create — input fields ≠ target TO attributes — needs a custom operation with **unmapped input TO**.

Examples:
- `inviteUser(input: UserInvitationInput) : UserTO` where `UserInvitationInput { email, givenName, familyName, isAdmin }` differs from `UserTO` mapped attrs.
- Composite create taking parent reference + child attrs in single payload.
- Factory op picking concrete subtype from sentinel field.

Pattern:
1. Define **unmapped** `TransferObjectType` for input. Outer CRUD flags irrelevant (not persisted).
2. Define op on appropriate scope (parent / view-model / access target).
3. Op body builds target entity row via DAO. Returns mapped target TO.
4. Default UI navigation = standalone `<TO>View` (§3 layer 1).
5. Production: `OperationFlowManager` redirects to access-context detail or caller's relation view (§3 layer 2).

**Return shape rule — prefer thin Identifiable over full target TO.** When the op is a create-on-relation (`A.createB(input) : ?`) and the canonical view for B is the parent-rooted relation list/detail, return a **thin Identifiable mapped TO of B** (single dummy attribute, exists only to satisfy mapping requirement) rather than the full `BTO`. Result carries `__identifier`; `OperationFlowManager` reads it and redirects to the caller's relation view. Standalone `<BTO>View` is generated but never reached. Full recipe + worked example: [thin-identifiable-result-for-parent-relation-create.md](thin-identifiable-result-for-parent-relation-create.md).

## §3 Return-type matrix

### Layer 1 — generation defaults

| Op output type | Generated UI navigation | Refreshable |
|---|---|---|
| Mapped TO | Standalone `<TO>View` route. Re-fetch via `_refreshInstance<TO>` + signed `__identifier`. | Yes |
| Unmapped TO | Inline view-mode form on caller page. No `__identifier`, no re-fetch endpoint. | No |
| `void` | Stay on caller page. Default refresh fires. | n/a |

### Layer 2 — production with `OperationFlowManager`

`OPERATION_FLOW_MANAGER_INTERFACE_KEY` Pandino DI extension overrides layer-1 default.

| Returned spec | Effect |
|---|---|
| `{ actor, access, id }` | Navigate to access-context detail. Canonical view. Dashboard breadcrumbs + gating preserved. |
| `{ actor, access, filterRecords }` | Navigate to access list filtered to specific row. Use for parent-relation create landing on new row — see [thin-identifiable-result-for-parent-relation-create.md](thin-identifiable-result-for-parent-relation-create.md). |
| `{ refresh: true }` | Stay on caller. Re-fetch. |
| `null` | Fall through to layer-1 default. |

See [operation-flow-manager-redirect.md](../frontend/operation-flow-manager-redirect.md).

**One representation per concept.** Default mapped-TO navigation lands on standalone `<TO>View`. Same row also reachable via `Actor.access.<area>.<rel> → row → detail` — DIFFERENT generated page. Two views drift; maintenance burden doubles.

**Rule.** Pick access-context view as canonical. Redirect every post-op landing into it via `OperationFlowManager`. Standalone routes generated but unvisited.

**U/D on result page.** Conditional on target row's `__updateable` / `__deletable` evaluated against the redirect-target context, not the caller's ladder gate. See §4 for ladder; see [managed-actor-admin-pattern.md](../backend/managed-actor-admin-pattern.md) for worked example where parent's outer `updateable=false` but result row's `__updateable=true` (computed in admin access-context).

## §4 Capability ladder

For C / U / D on `Y` via `X.relY`, ALL rungs hold:

| Rung | C on Y | U on Y | D on Y |
|---|---|---|---|
| 1. Y outer CRUD | `Y.createable` | `Y.updateable` | `Y.deleteable` |
| 2. Relation flag | C-flag | U-flag | D-flag |
| 3. Access reachability | `enabledBy` chain to X | same | same |
| 4. Parent per-instance | `X.__updateable` | `X.__updateable` | `X.__deletable` |
| 5. Filter membership post-state | new row satisfies `getterExpression` | post-update Y satisfies | n/a |
| 6. LIST scope at signed-ID issuance | row visible on LIST | same | same |

Rungs 1–3 model-time. Rungs 4–6 per request.

- **Rung 1** declares `Y`'s outer capability. Path-agnostic (§Mapped TO outer CRUD is path-agnostic, below). TO is unit of capability declaration; path is navigation only.
- **Rung 2** restricts the parent-rooted relation. `relY.createable=false` blocks C even if `Y.createable=true`.
- **Rung 3** gates the access link via `ActorType.access[*].enabledBy`. Chain must hold from actor → X.
- **Rung 4** `X.__updateable` for both C and U on Y. Both mutate parent's relation set / linked-row state. D rides `X.__deletable` (composition / decomposition semantics).
- **Rung 5** derived-relation/access membership invariant. Read-only state through filtered path. See [derived-relation-membership-invariant.md](derived-relation-membership-invariant.md).
- **Rung 6** signed-identifier issuance gated on LIST scope. Out-of-scope row never obtains signed id; cross-scope refresh / update bypass impossible. See [testkit-integration-foundation/backend.md — bypass note](../../model-blueprints/testkit-integration-foundation/backend.md).

**Custom-op bypass.** Custom operations on X are NOT subject to this ladder. Own gate via op's `enabledBy` + op body logic. Op may read/write Y rows the ladder forbids.

**Mapped TO outer CRUD is path-agnostic.** `Y.createable / updateable / deleteable` state maximum capability anywhere `Y` rendered: relation row, custom-op result, deep link, access detail. Declaration ≠ runtime authorization — effective capability per request still walks full ladder.

## §5 Anti-patterns

| Anti-pattern | Why bad | Correct shape |
|---|---|---|
| Separate `<X>ListTO` for relation target without picker / audience-hide / expensive-derived justification | Row-click navigates to `<X>ListTO` detail; needs custom handler to swap to `<X>TO` detail. Dual TOs drift. | One mapped TO per relation. Use audience-hide attributes (`visible=false` on data members) for column thinning. |
| `Y.createable=true` when create input shape diverges from `Y` mapped attrs | Auto-form is misshapen. User types into wrong fields. Validation surface wrong. | Custom op with **unmapped input TO**. Returns mapped target TO. §2. |
| `X.updateable=true` purely to enable relation CUD on children | Opens parent surface for unintended U. Self-elevation risk on principal entities (admin editing own row via `~admin` PUT). | Custom ops on X with `enabledBy` gating. C/U/D each own op. Single security gate per op. See [managed-actor-admin-pattern.md](../backend/managed-actor-admin-pattern.md). |
| Two TOs for same representation — standalone `<TO>View` + access-context detail — both authored, both maintained | Auto-generated routes drift; bug-fix lands one place only. Two URLs for same row. | One canonical access-context view. `OperationFlowManager` redirects every op result. §3 layer 2. |
| Create-on-relation op returns full target TO purely to carry `__identifier` for post-create redirect | Pulls standalone `<TO>View` into the funnel as a plausible landing; op contract coupled to mapped projection drift; wire payload bloated. | Return **thin Identifiable mapped TO** (id + dummy attr). Redirect to caller's relation view. See [thin-identifiable-result-for-parent-relation-create.md](thin-identifiable-result-for-parent-relation-create.md). |

## See also

- [derived-relation-membership-invariant.md](derived-relation-membership-invariant.md) — write-side membership rule (rung 5)
- [operation-flow-manager-redirect.md](../frontend/operation-flow-manager-redirect.md) — return-type navigation override
- [managed-actor-admin-pattern.md](../backend/managed-actor-admin-pattern.md) — canonical admin surface combining §2 + §3 + §4
- [accesspoint.md — Principal back-link exclusivity](../../agent-docs/model/esm_metamodel/accesspoint.md#principal-back-link-exclusivity)
- [accesspoint.md — Managed-realm sync trigger](../../agent-docs/model/esm_metamodel/accesspoint.md#managed-realm-sync-trigger)
- [actor-based-transfer-projection.md](actor-based-transfer-projection.md) — multi-TO same-entity projection rules
- [operation-return-type-navigation.md](operation-return-type-navigation.md) — return-type → view navigation (Layer 1 behaviour)
- [state-based-transfer-partitioning.md](state-based-transfer-partitioning.md) — partition + return-type pattern as rung-5 workaround
- [thin-identifiable-result-for-parent-relation-create.md](thin-identifiable-result-for-parent-relation-create.md) — return-shape rule for create-on-relation ops
