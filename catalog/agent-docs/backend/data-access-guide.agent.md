# data-access-guide.md — index

Pull-only condensed map. Source: catalog/agent-docs/backend/data-access-guide.md.

## Table of Contents
- Sections: Injecting DAOs and Services; Query Patterns; CRUD Operations; Using Masks (Projections) (why, basics, patterns, performance); Generated DAO Behaviour and Known Issues.

## Injecting DAOs and Services
- Inject with OSGi `@Reference`: generated `<Entity>Dao`, custom operation classes, `VariableResolver`, external bundle services.

## Query Patterns
- Fluent: `dao.query().filterBy<Attr>(Filter.x(...)).orderBy...(…Attribute.X).selectList()|selectOne()|count()`. Filters are AND-combined.
- Filter classes in `hu.blackbelt.judo.sdk.query`:
  - `StringFilter`: `equalTo`, `notEqualTo`, `like` (SQL LIKE, `%`), `ilike` (case-insensitive).
  - `NumberFilter`: `equalTo`, `notEqualTo`, `greaterThan`, `greaterOrEqualThan`, `lessThan`, `lessOrEqualThan` (Integer/Long/BigDecimal).
  - `DateFilter`: same comparisons on `LocalDate`.
  - `TimestampFilter`: same comparisons on `LocalDateTime`.
  - `TimeFilter`: same comparisons on `LocalTime` (time-of-day, not interval overlap; express overlap as two filters on start and end).
  - `BooleanFilter`: ONLY `isTrue()` / `isFalse()`. Never `equalTo(boolean)`.
  - `EnumerationFilter`: `equalTo`, `notEqualTo`; enum implements `hu.blackbelt.judo.sdk.Enumeration`.
- OR logic: `filterBy("expr")` with JQL. Multiple `filterBy` chain as AND.
- JQL syntax: `this.field`; equality `==` (NOT `=`); `!=`; `< > <= >=`; pattern `(this.field)!like('%x%')`; booleans `== true`; `and`/`or`; parentheses; single-quoted strings.
- JQL does NOT support: navigation `this.relation.field`; `this.field = value`; `this.field like 'x'`.
- Results: `selectList()` (List), `selectOne()` (Optional), `count()`; exists = `count() > 0`.
- Relation queries:
  - One-to-many: `countyDao.querySettlements(county)` returns query customizer (filter, mask, selectList). NO ordering methods; sort in Java (`Comparator.comparing(Settlement::getCode)`).
  - Many-to-one: `settlementDao.queryCounty(s)` returns entity directly for `1..1` (not `.selectOne()`); `Optional<T>` for `0..1`. Check generated DAO signature.
- Common mistakes: `BooleanFilter.equalTo(true)` → `isTrue()`; multiple `filterBy` for OR → single JQL; `this.field = value` → `==`; `like` without method syntax; navigation in `filterBy`.

## CRUD Operations
- Create: `dao.create(<Entity>ForCreate.builder().withX(...).build())`.
- Read: `getById(id)` (Optional; `.orElseThrow()`), `getById(id, mask)`.
- Update: `dao.update(entity)`; `dao.update(entity, mask)`.
- Delete: `dao.delete(entity)`.

## Using Masks (Projections)
- Masks are the key performance tool; prevent N+1 and over-fetch.
- Without mask: all attributes incl. derived members loaded. Empty mask: identifier only.
- `[Entity]Mask.<entityName>Mask()` with `.withAttr()`; nested `.withRel(RelMask.relMask()...)`.
- Patterns:
  - Existence check: `dao.getById(id, EntityMask.entityMask()).isPresent()`.
  - List view: `maskedBy(...)` with only displayed columns.
  - Detail view: nested masks for relations.
  - Partial update: `update(entity)` and `update(entity, mask)` write only attributes present in the payload; unloaded/unset fields are left unchanged (not nulled). Stale version: re-read, set changed attributes on the fresh copy, retry (business rule in the retry code). Mask only shapes the read-back, does not limit writes. `update` requires identifier; defaults applied only to payloads without identifier, so updates do not reset to defaults.
- Best practices: always mask queries; empty mask for existence; minimal masks in loops; chain nested masks; masks in updates.
- Don't: full loads for few fields; omit masks; load large collections unmasked; read unmasked fields (they are `null`).

## Generated DAO Behaviour and Known Issues

### Which Types Get a Full DAO
- Full CRUD only for mapped, non-abstract TOs: `create`/`createAll` (± mask), `getById`, `existsById`, `getAll`, `countAll`, `delete`, `query()`, per-relation `create`/`set`/`unset`/`add`/`remove`/range (subject to allowed-operation flags).
- Unmapped TOs and unmapped single relations: only `query<...>()` accessors.

### Unmapped (Static) Data and Navigations
- Static-data DAO interfaces: `selectValue()` (or with parameter) → primitive; missing → `null`.
- Static navigation: `query()` → collection; `selectOne()` → single value.

### Absent, Null and Empty
- `required = true`: plain getter (e.g. `Boolean getX()`); `null` = caller omitted. Read directly; no Java null workarounds.
- `required = false`: `Optional<T>` getter.
- Required attribute may still be `null` if masked out (required ≠ non-null unless loaded).
- DTO getters check `containsKey`: missing key ≠ key with null.

### Clearing a Relation: `unset`, Not `set(null)`
- `set<Relation>(object, related)` calls `related.identifier()` without null check → NPE on `null`. Clear optional single relation with `unset<Relation>(object)` (generated only when unset allowed).
- `add`/`remove` also call `identifier()` per element → null element fails.

### Filtering for "Not Set" on Optional Booleans
- `BooleanFilter` has only true/false. Use `filterBy("this.attr!isUndefined()")` (verify expression against model) or count all minus isTrue minus isFalse.

### Known Issues
- `query<Attribute>()` on enum attribute may throw `ClassCastException` (Integer → enum): runtime delivers ordinal. Workaround: read via DTO or `<Enum>.getByOrdinal(...)`. Same possible when navigation returns enum.
- Derived attribute navigating through inherited member may produce query missing a JOIN. No known generator workaround; check generated SQL when derived value is empty.
- Generated DAO code is under `target/` (not in git); open `<Entity>DaoImpl` when debugging.

### Pagination
- List without seek returns ALL rows; pagination opt-in.
- `selectList()`, `selectList(limit)`, `selectList(limit, offset)` (limit first).
- Keyset: `selectList(limit, lastItem)`, `selectList(limit, lastItem, reverse)`.
- `selectOne()`, `selectOne(offset)` → Optional.
- DAO: `getAll()`, `countAll()`, `existsById(id)`, `getById(id[, mask])` (Optional), `findAllById(Iterable<id>[, mask])` (List; use for bulk instead of looping).
- Per multi-valued relation: `count<Rel>(owner)`, `create<Rel>(owner, related|relatedObjects[, mask])` (if create allowed), `add<Rel>`, `remove<Rel>` (if allowed), `getRangeOf<Rel>` / `countRangeOf<Rel>` (with range). Single-valued: `query<Rel>(id|identifier|owner[, mask])`.

### Low-Level DAO and `QueryCustomizer`
- Generic `DAO` takes `QueryCustomizer` (Lombok `@Builder`): `filter` (JQL string), `orderBy` (`OrderBy.attribute` @NonNull), `seek`, `withoutFeatures`, `mask`, `parameters`, `instanceIds`.

### The `Payload` Type
- `hu.blackbelt.judo.dao.api.Payload` = `Map<String,Object>`. Factories `asPayload(map)`, `map(k1,v1,...)` (1–20 pairs), `map(Entry...)`, `entry(k,v)`.
- `getAs(Class, key)` returns `null` for absent key; never unbox directly (use `Boolean.TRUE.equals(...)`). Also `getAsPayload`, `getAsCollectionPayload`.

### Native SQL from a Custom Service
- No DAO method for native SQL. Inject a JDBC `DataSource` via `@Reference` in own component; test kit must bind it too. No platform precedent: isolate in one service.

## See Also
- platform-behavior-reference.md, custom-operations.md, patterns-and-best-practices.md
