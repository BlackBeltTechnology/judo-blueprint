---
id: "self-learning-reference-dictionary"
title: "Self-Learning Reference Dictionary (learn() Primitive, Parent-Create Gap, Bulk Import)"
domain: "backend"
category: "interceptor"
score: 55.0
usage_count: 1
alternative_count: 0
first_seen: "2026-07-12"
last_updated: "2026-07-12"
projects:
  - rackinspect
---
## Description

Grow a reference dictionary (e.g. `City` ⟷ `PostalCode`, joined **two-way n:m**, never FKs on the address) automatically from the free-text values users enter, converging every write-path on **one primitive**:

```java
public void learn(String cityName, String code) {
    if (cityName == null || code == null) return;
    final String name = cityName.trim(), postalCode = code.trim();
    if (name.isEmpty() || postalCode.isEmpty()) return;   // blank-safe
    City city = findOrCreateCity(name);                    // find-or-create by identifier
    PostalCode pc = findOrCreatePostalCode(postalCode);    // + concurrent-create re-query guard
    linkIfAbsent(city, pc);                                // link n:m only if not already linked → idempotent
}
```

`findOrCreate` handles the concurrent-create race by re-querying the winner if the unique-identifier insert is rejected. `learn()` is idempotent + blank-safe, so it is safe to call on **every** save. Three write-paths converge on it: address create/update interceptors (auto-learn), a CSV import operation, and (optionally) seeding.

## Critical Gotcha — the Parent-Create Interceptor Gap

Wiring `learn()` into the child's `#_createInstance<Children>` operation interceptor (e.g. `Partner#_createInstanceAddresses`) covers only *adding a child to an already-existing parent*. **Creating the parent WITH a nested child in one form does NOT fire the per-child operation interceptor** — the nested aggregate is created inside the parent-create behaviour, which emits no per-child operation. Symptom: a new address (and its city) reaches `T_..._ADDRESS` but the city never reaches `T_..._CITY`, and the child interceptor shows **0 invocations** in `karaf.log`.

Fix: also wire `learn()` into the **parent-create** interceptors and iterate the created children:

```java
// GenericUser#_createInstancePartners  → learn each address of the just-created partner
for (Address a : partnerDao.queryAddresses(partner).selectList()) {
    cityPostalCodeService.learn(a.getCity(), a.getPostalCode());
}
// GenericUser#_createInstanceUsers      → learn from the input form fields (guaranteed populated)
cityPostalCodeService.learn(input.getForm_primaryAddressCity(), input.getForm_primaryAddressPostalCode());
```

Cover all save paths: parent-create (`_createInstance<Parents>`), child-add (`_createInstance<Children>`), and child update (`#_updateInstance...`). A **singleton** parent (e.g. company data, created once) has no create-with-child path, so its child-add interceptor already suffices. DAO calls like `createUserAddresses(...)` are NOT operations and do not fire operation interceptors — learn from the input payload or the created entity directly.

## Bulk Import — Don't Call learn() Per Pair

Calling `learn()` once per pair costs ~4 DB round-trips/pair (find city, find postal, check link, plus creates) → thousands of tiny JUDO DAO calls (~2 min for ~3.7k pairs). For the CSV import path, keep `learn()` for the single-save interceptor path but persist the import in **bulk**:

1. Parse the whole file into an in-memory `Map<parentKey, Set<childKey>>` (dedup); skip blank/`#`/malformed lines while parsing so a skipped line's children never persist.
2. Preload existing rows into lookup maps — **2 bulk `selectList()` queries**.
3. `createAll(...)` the missing rows (batched) instead of one `create()` each.
4. One `addChildren(parent, ...)` per parent, only for not-yet-linked children (freshly created parents skip the link-existence query).

→ ~6× fewer round-trips, and the per-pair find-SELECT storm disappears. Idempotent re-import preserved.

## When To Use

- Any "suggestion source that grows itself" — a reference list fed by user input plus optional bulk import, where the stored business field stays a string (pairs with the frontend `string-field-typeahead-self-learning` pattern).
- Whenever auto-learn / audit / denormalization must fire on **entity creation that can happen as a nested aggregate** — the parent-create gap applies to any such hook, not just dictionaries.

## Pros / Cons

- **Pros**: one idempotent primitive shared by all write-paths (DRY); free-text business fields never become FKs; import and auto-learn stay consistent by construction.
- **Cons**: must remember the parent-create gap (nested creates bypass child interceptors); free-text learning admits typo-duplicates (accept, or add fuzzy-match/dedupe later); bulk path needs a separate implementation from the single-pair primitive.

## Placement

`learn()` / import primitive: an OSGi `@Component` service in `application/common/.../services/` (reachable from both interceptors and custom operations). Interceptor wiring: `application/interceptors/`. Import `CustomImplementation`: `application/app/` (thin delegator → the common service). Never in `application/internal/`.
