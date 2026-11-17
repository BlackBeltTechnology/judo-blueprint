# access-and-derived-testing.md — index

Pull-only condensed map. Source: catalog/agent-docs/integration-testing/access-and-derived-testing.md.

## Coverage matrix
- Pattern A: DERIVED getter using only `self.*` (e.g. `not self.isAdmin`). No actor. Layer: DAO projection.
- Pattern B: `Access.getterExpression` per-actor scoping and CRUD flags. Needs `JudoPrincipal` in exchange. Layer: dispatcher / access point.
- Pattern C: DERIVED getter reading `!getVariable("ACTOR", "...")`. Needs principal. Layer: dispatcher → access point → projection.

## Limitations to be aware of
- Plain DAO reads have no `__principal`: `getVariable("ACTOR", …)` evaluates empty. Never test ACTOR-dependent getters via Pattern A; use C.
- `managed=true` first-login auto-insert NOT implemented. Tests must `dao.create(...)` the principal row before dispatcher call (see backend authentication-guide.md).
- Only Managed Mapped Principal actor shape exposes `ACTOR.*` to JQL. Token-only and Transient principal shapes: only `USER.*` / `PRINCIPAL.*`; exchange must carry attributes; no persisted row.

## Pattern A — Testing pure `DERIVED` attributes via DAO
- Derived attributes on self/entity members are projected on TO from any `<TO>Dao` query. Getter `Optional<T>` (e.g. `Optional<Boolean> getIsNotAdmin()`). No dispatcher.
- Use for: negated flags (`not self.isAdmin`), labels (`self.firstName + ' ' + self.lastName`), aggregates (`self.orders!count()`, `self.invoices!sum(i | i.amount)`).
- Proves: JQL parses/evaluates (catches wrong member name, missing `not`, wrong type, missing `!any()` on singleton expressions).
- Does NOT prove actor-context correctness.
- Test: `@JudoTest(modelName = "<app>", dialect = "hsqldb", transaction = TransactionHandling.AUTO_ROLLBACK)` with `JudoRuntimeFixture`; `fixture.getInjector().getInstance(UserDao.class)`; `userDao.create(UserForCreate.builder()...build())`; assert `getIsNotAdmin().orElseThrow()`.

## Pattern B — Testing `Access.getterExpression` per actor via the Dispatcher
- Evaluated by dispatcher when request enters through access point, not DAO.
- Steps: (1) seed principal row via entity DAO; (2) seed scoped data; (3) build `JudoPrincipal` with `attributes` map (keys used by getter, e.g. `userName`); (4) resolve `Dispatcher` from injector; (5) call access-point query op with principal under `Dispatcher.PRINCIPAL_KEY`; (6) assert scoped subset.
- Op FQN: `<modelPackage>::<ActorName>::<AccessName>` (generator names it; confirm in generated SDK `application/sdk/target/generated-sources/.../services/` or OpenAPI; do not invent). Example used: `<app>::accesspoint::GenericUser::orders::__get`; result rows in `response.get("__output")`.
- Proves: getter compiles, runs, scopes per actor. Also test admin principal for the role branch.
- Catches: wrong ACTOR attribute name (empty results for everyone); wrong typed prefix (`String!getVariable` vs `Boolean!…`); missing `!any()` on single-instance expression; `!filter` predicate off-by-one; `Access.upper`, `createable`, `updateable`, `deleteable` mismatches (dispatcher rejects).
- Does NOT prove menu surfacing (needs paired `MenuItemAccess`; E2E).

## Pattern C — Testing DERIVED getters that depend on `ACTOR.*`
- Same mechanics as B (principal in exchange, call access-point query). Assert the DERIVED field on the projected TO in the dispatcher response, not row count.
- Example: `ownedByMe = self.owner.userName == String!getVariable("ACTOR", "userName")`. Make principal admin so access returns all rows; assert true only for principal's row.
- Counter-example: DAO-query assertion gives empty/false regardless → silently passes or always fails. Always route ACTOR-dependent getters through dispatcher.

## Cross-references
- advanced-patterns.md (mocking VariableResolver for custom ops); model advanced-modeling-patterns.md (role flags on principal: ship Pattern A for `isNotAdmin` and Pattern B for role-scoped access); model esm_metamodel/accesspoint.md (three actor shapes: which of USER/PRINCIPAL/ACTOR is populated).
