---
id: self-learning-reference-dictionary
title: "Self-Learning Reference Dictionary (learn() Primitive, Parent-Create Gap, Bulk Import)"
description: "A reference dictionary (city and postal code) grows from user-entered free text through one idempotent learn() primitive wired into every write path, with a bulk path for imports."
aliases: [auto-learn dictionary, city postal code learning, suggestion source, learn primitive]
keywords: [learn, dictionary, interceptor, parent create gap, nested create, find-or-create, bulk import, createAll, n:m, idempotent]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: interceptor
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
fragment: "none: backend-only"
first_seen: 2026-07-12
last_updated: 2026-11-10
---
## Intent

Grow a reference dictionary (for example `City` and `PostalCode`, joined two-way n:m, never as foreign keys on the address) from the free-text values users enter. Every write path converges on one idempotent primitive, so the suggestion list feeds a typeahead while the stored business field stays a string ([[string-field-typeahead-self-learning]]).

## Practice

### Platform base

- Interceptors fire only for the built-in behaviour operations (create, update, delete, reference operations and others). Custom, mapped and script operations never hit them, so a hook for a custom create or import operation has to be called from inside the implementation ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Synchronous interceptors run inside the operation's transaction; an exception from one rolls back the write ([ordering and combining interceptors](../../agent-docs/backend/interceptors.md#ordering-and-combining-several-interceptors)).
- A DAO call such as `createUserAddresses(...)` is not an operation and fires no operation interceptor. The generated DAO of a mapped type offers `create`, `createAll`, `getById`, `delete` and per-relation queries ([generated DAO behaviour](../../agent-docs/backend/data-access-guide.md#which-types-get-a-full-dao)).
- Whether creating a parent with a nested child in one call fires the per-child create interceptor is not stated in the docs. The project observed it does not (below), *verify* for your model.

### Project practice: one primitive, all write paths

This layer is project practice (rackinspect). The primitive lives in an OSGi component service in the project's common module, reachable from interceptors and custom operations; interceptor wiring goes in the interceptors module; the import operation is a thin custom implementation in the app module delegating to the service.

```java
// Example project code: City, PostalCode and the find/link helpers are project types
public void learn(String cityName, String code) {
    if (cityName == null || code == null) return;
    final String name = cityName.trim(), postalCode = code.trim();
    if (name.isEmpty() || postalCode.isEmpty()) return;   // blank-safe
    City city = findOrCreateCity(name);                    // find-or-create by identifier
    PostalCode pc = findOrCreatePostalCode(postalCode);    // + re-query guard for concurrent create
    linkIfAbsent(city, pc);                                // link n:m only if absent: idempotent
}
```

- `findOrCreate` handles the concurrent-create race by re-querying the winner when the unique-identifier insert is rejected.
- `learn()` is idempotent and blank-safe, so it is safe to call on every save. Three paths converge on it: address create/update interceptors (auto-learn), a CSV import operation, and optionally seeding.

### The parent-create interceptor gap

Wiring `learn()` into the child's create-operation interceptor (for example the create-addresses operation on a partner) covers only adding a child to an already existing parent. Creating the parent with a nested child in one form did **not** fire the per-child interceptor in the project: the nested aggregate is created inside the parent-create behaviour, which emitted no per-child operation. Symptom: the address row and its city reach the database, but the city dictionary row never does, and the child interceptor logs zero invocations.

Fix: also wire `learn()` into the parent-create interceptors and iterate the created children.

```java
// Example project code, parent-create interceptor: learn each address of the just-created partner
for (Address a : partnerDao.queryAddresses(partner).selectList()) {
    cityPostalCodeService.learn(a.getCity(), a.getPostalCode());
}
// Another parent-create interceptor: learn from the input form fields (guaranteed populated)
cityPostalCodeService.learn(input.getForm_primaryAddressCity(), input.getForm_primaryAddressPostalCode());
```

- Cover all save paths: parent create, child add, and child update.
- A singleton parent (company data, created once) has no create-with-child path, so its child-add interceptor suffices.
- Learn from the input payload or the created entity directly when the save goes through a DAO call.

### Bulk import: do not call learn() per pair

One `learn()` per pair costs about four round trips (find city, find postal code, check link, creates): thousands of small DAO calls, about two minutes for roughly 3.7k pairs. Keep `learn()` for the single-save path and persist imports in bulk:

1. Parse the whole file into an in-memory map from parent key to a set of child keys (deduplicated); skip blank, `#` and malformed lines while parsing so a skipped line's children never persist.
2. Preload existing rows into lookup maps with two bulk `selectList()` queries.
3. `createAll(...)` the missing rows in batches instead of one `create()` each.
4. One add-children call per parent, only for children not yet linked; freshly created parents skip the link-existence query.

About six times fewer round trips, and the per-pair find storm disappears. Re-import stays idempotent.

## Rationale

- One idempotent primitive shared by all write paths (DRY); free-text business fields never become foreign keys; import and auto-learn stay consistent by construction.
- Cost: nested creates can bypass child interceptors; free-text learning admits typo duplicates (accept, or add fuzzy matching later); the bulk path is a separate implementation from the single-pair primitive.
- The parent-create gap applies to any hook that must fire on creation that can happen as a nested aggregate (audit, denormalization), not only dictionaries.

## Example

rackinspect learns city and postal code pairs from partner and user addresses through create and update interceptors on the child and the parent, and from a CSV import operation that runs the bulk path above.

## When to avoid

- The reference data is a closed, curated list: use a plain lookup entity or enumeration.
- Typo duplicates would be harmful and nobody can dedupe them.
- Hooks that must also run for custom operations: call the primitive from the operation implementation, interceptors will not fire there.

## Related

- [[string-field-typeahead-self-learning]] — the frontend typeahead fed by this dictionary
- [[relation-based-entity-creation]] — creating children through relation DAO methods
- [[form-field-flattening]] — parent-create interceptor that builds nested payloads
