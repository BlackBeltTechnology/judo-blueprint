---
id: "derived-relation-membership-invariant"
title: "Derived Relation / Access Membership Invariant on Update"
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

Derived relations and accesses enforce post-update membership invariant. Filter attributes are read-only through the filtered path.

## §1 The rule

Update through a derived relation or access is rejected with a validation error when the post-update state no longer satisfies the path's predicate.

- Derived relation `X.relY : Y[0..*]` filtered by `Y!filter(y | <predicate>)`. Updating an attribute referenced by `<predicate>` such that the post-update row falls outside the predicate → validation error. Update aborted; row unchanged.
- `ActorType.access` link with `getterExpression` filter. Updating an attribute referenced by the filter such that the post-update row falls outside → same validation error.

Rung 5 of the capability ladder. See [relation-driven-crud-with-custom-input.md — §4](relation-driven-crud-with-custom-input.md#4-capability-ladder).

## §2 Distinction from read-side scope enforcement

Two orthogonal rules govern derived paths:

| Side | Trigger | Mechanism | Bypass surface |
|---|---|---|---|
| Read | LIST issuance | Filter evaluated when LIST returns rows. Out-of-scope rows never appear; signed `__identifier` never issued for them. | `_refreshInstance` and `_updateInstance` dereference signed identifier and do NOT re-evaluate filter (caller already proved scope at LIST time). |
| Write | UPDATE | Post-update predicate satisfaction checked. Filter attribute change that exits the predicate → reject. | Custom op on parent / entity scope bypasses filter; direct entity DAO write bypasses filter. |

Pre-update scope NOT re-evaluated. Caller-proven-scope-via-signed-id principle. See [testkit-integration-foundation/backend.md — bypass note](../../model-blueprints/testkit-integration-foundation/backend.md).

## §3 Worked example — plain TO relation

```
EntityType Car { color : String }
TransferObjectType GarageTO mapped Garage {
  redCars : CarTO[0..*]  derived  Garage.cars!filter(c | c.color == 'red')
}
TransferObjectType CarTO mapped Car { color : String  updateable=true }
```

`PUT garages/<id>/redCars/<carId>` with `{ color: 'blue' }` → rejected. Post-update `color == 'red'` fails. Validation error.

To recolour a red car blue:
- Plain access `cars : CarTO[*]` on parent scope (unfiltered) — write through it.
- Custom op `Garage.repaintCar(target: CarTO, color: String) : CarTO` bypassing the filter.
- state-based-transfer-partitioning (§5).

## §4 Applies to actor access

`getterExpression` filter on `ActorType.access` enforces the same invariant.

```
ActorType LetterUser {
  access myDrafts : LetterTO[0..*]
    getterExpression = self.letters!filter(l | l.status == LetterStatus#DRAFT)
}
TransferObjectType LetterTO mapped Letter { status : LetterStatus  updateable=true }
```

`PUT users/<actor>/myDrafts/<letterId>` with `{ status: 'PUBLISHED' }` → rejected. Post-update `status == DRAFT` fails. Validation error.

Publish flow needs:
- Unfiltered access `myLetters : LetterTO[*]`.
- Or custom op `LetterUser.publish(target: LetterTO) : LetterTO` returning the published letter's TO (typically a different partition's TO).

## §5 Workarounds

Three canonical patterns to perform state transitions through filtered paths:

1. **Unfiltered access containing all states.** Add second access link without `getterExpression` filter (or with broader predicate). Write through it. Read still through filtered access for scoped display.
2. **Custom op on parent / entity scope.** Op body uses entity DAO (or unfiltered TO DAO) to bypass the predicate. Op signature owns the gate via `enabledBy`. Returns mapped target TO routed via `OperationFlowManager` to the destination partition's view.
3. **State-based transfer partitioning.** Separate mapped TO per state group. Custom op flips state and returns the destination partition's TO. UI navigates by return-type. See [state-based-transfer-partitioning.md](state-based-transfer-partitioning.md).

## See also

- [state-based-transfer-partitioning.md](state-based-transfer-partitioning.md) — canonical pattern for write-side state transitions
- [relation-driven-crud-with-custom-input.md](relation-driven-crud-with-custom-input.md) — capability ladder rung 5
- [testkit-integration-foundation/backend.md](../../model-blueprints/testkit-integration-foundation/backend.md) — read-side bypass via signed `__identifier`
- [derived-access-filtering.md](derived-access-filtering.md) — derived access link filtering patterns
- [operation-return-type-navigation.md](operation-return-type-navigation.md) — return-type navigation for partition-crossing ops
