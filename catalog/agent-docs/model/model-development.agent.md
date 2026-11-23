# model-development.md — index

Pull-only condensed map. Source: catalog/agent-docs/model/model-development.md.

## Table of Contents

- Lists Parts 1–5 of the source; pull a part with `kb_get`.

## Part 1: Foundational Concepts

- Two layers: Domain Logic (EntityType = source of truth) and Service (TransferObjectType = API view). Never expose EntityType directly in an `Access`; TOs are the entry point.
- Attributes: `Stored` (persisted) vs `Derived` (read-only, `Getter expression`).
- Relations: Association `-->` (has-a); Composition (solid diamond, child destroyed with parent); Aggregation (hollow diamond, child independent).
- Generalization = is-a. Member overriding NOT allowed.

## Part 2: The Core Modeling Workflow

- Designer steps: new project; add Entity; add Attribute (`Stored`); set properties (e.g. `Required`); "Add features to representations" for Table/Form/View; add Actor; add Access linking Actor to TO (exposes API only).
- Step 8: every UI-reachable Access needs a `MenuItemAccess` under the actor's `<menuItems>` (optionally in `MenuItemGroup`) pointing to the Access. Without it, API only.
- CLI: `create -t Access --ns <actor> --set target=<TO>` creates the MenuItemAccess too (named `Menu`, labelled with target type); `create -t MenuItemAccess` is refused. A mapped TO gets generated mapped members: reuse them; a new derived member needs a different name (same-name reported as not unique).
- Working-copy safety for multi-stage changes:
  - Commit per stage or green checkpoint.
  - Never `git restore`/`git checkout` `model/*.model` with uncommitted mutations: silently reverts every change since last commit.
  - Before any restore or branch switch, `cp model/<name>.model /tmp/<name>.model.stageB.bak`.
  - Prefer CLI mutations (judo-cli.md) over hand-edited XMI.

## Part 3: Advanced Modeling Patterns & Use Cases

### Service Layer Architecture

- Mapped TO: projection of an EntityType via `Mapping`. Members: mapped/bound, derived (getter), simple/transient (UI state only).
- Unmapped TO: standalone container, often for operation inputs.
- Purpose-built TOs: small `...ListTO` for tables, full `...DetailTO` for forms; table Access targets the ListTO.

### Action & Operation Patterns

- Grouping actions on a view: `ui:ActionGroup` holding `OperationForm` buttons.
- Table actions: `tableOperations` (`isBulk="true"` for bulk) vs `rowOperations` (per row).

### Security & Access Control

- User-specific data: Access `Access type` = `Derived`; `Getter expression` filters with `!getVariable("ACTOR", "claim_name")`.

### UI Modeling & Display Patterns

- Dynamic page title: View/Edit `titleFrom` = `Attribute`; `titleAttribute` = DataMember.
- Conditional visibility: `enabledBy` / `hiddenBy` on any `ui:VisualElement`, pointing to a Boolean DataMember.
- Alternative representations: `representationComponent` on `TabularReferenceField`: `"table"`, `"tag"`, `"card"`, `"button"`. Dropdown/autocomplete is a separate widget (`isTypeAheadField`, `autocompleteRows`), not a `representationComponent` value.

### Advanced Data Modeling Patterns

- Polymorphism: `Generalization` between EntityTypes (e.g. `Pro`, `Con` of `Argument`). Inheritance between TOs NOT supported.
- Parameterized queries: derived feature with an `input` TO; `primitive query` (attributes) or `complex query` (relations). `getterExpression` reads `input` variable (attributes only).

## Part 4: Judo Query Language (JQL)

- Key concepts: `self`; navigation with `.`; built-in functions called with `!`; `undefined` handling.

## 1. General Concepts

- Comments: `//` single-line, `/* */` multi-line.
- `undefined`: propagates through arithmetic and logic; comparisons with `undefined` yield `undefined` (not true/false); function on `undefined` yields `undefined` (`!count()` of undefined is `undefined`, not 0).

## 2. Special JQL Functions

- `!getVariable('PRINCIPAL', 'claim')`: attribute of the principal TO (via actor `_principal` operation). Actor with no `principal` TO yields nothing.
- `!getVariable('USER', 'claim')`: raw JWT claims of the authenticated `JudoPrincipal`. REQUIRED for token-only actors (no principal TO). Works for every shape. Most common "mysterious empty claim" bug is using PRINCIPAL here.
- `!getVariable('ACTOR', 'attr')`: attribute of the persisted Actor entity. Example `CRM::SalesPerson!filter(sp | sp.email == String!getVariable("ACTOR", "email"))!any()`.
- Category choice table:
  - Token-only (no principal TO): JWT via `USER.*`; persisted n/a.
  - Unmapped principal TO: `PRINCIPAL.*` or `USER.*`; persisted n/a.
  - Mapped principal TO: JWT via `USER.*`; persisted via `ACTOR.*`.
  - `PRINCIPAL.*` against no-principal actor is valid but empty at runtime.
- Other categories: `SYSTEM` (`current_date`, `current_timestamp`, `current_time`, via `<Type>!now()`); `PARAMETER` (input TO attributes of parameterized query); `ENVIRONMENT`, `SEQUENCE`, `REQUEST` (undefined resolves to `null` with warning).
- `!getVariable` is typed by the primitive it's called on; measured numerics carry the unit; always scalar.
- Grammar quirks:
  - Ternary `cond ? a : b` is right-associative; `a` and `b` must be the same kind; ambiguous entity supertype fails build.
  - Equality is `==` / `!=` only (no `=`, no `<>`). Keywords case-insensitive.
  - `^` power operator sits between `*` and `as` (spawn).
  - Enum literal `EnumType#LITERAL`; function call `expr!name(args)` may be navigated further.
  - Iterator lambdas take ONE variable and select only an immediate field.

## 3. Primitive Data Types

- String: `==` case-sensitive; `<`/`>` case-insensitive; `+` concat; `!length()`, `!first(n)`, `!last(n)`, `!position(sub)` (1-based, 0 if absent), `!substring(pos,len)` (1-based), `!lowerCase()`, `!upperCase()`, `!matches(regex)`, `!like(pattern)` (`%`, `_`), `!ilike(pattern)`, `!replace(old,new)` (all), `!trim()`, `!ltrim()`, `!rtrim()`, `!lpad(size[,pad])`, `!rpad(size[,pad])` (default pad space), `!capitalize()`.
- Numeric: comparisons; `+ - * /`; `mod`, `div` (scale 0 args only); `!round()`, `!round(scale)` (decimal result); `!abs()`, `!ceil()`, `!floor()`; unary `-`; `!asString()`. `9.0 / 2` is `4.5`.
- Measured numeric: literal `10[kg]` or `10[Mass#kilogram]` (namespaces joined `::`). Unknown unit fails (`No unit found in model` / `Unknown measure`). Auto unit conversion in comparisons and arithmetic.
- Durations: only `MILLISECOND`, `SECOND`, `MINUTE`, `HOUR`, `DAY`, `WEEK` support addition; `MONTH` and `YEAR` do not. `!elapsedTimeFrom(other [, measure])` needs a single default duration measure in the model if no measure given (`No single duration measure in the model`).
- Boolean: three-valued (Kleene) logic. Keywords `not`, `and`, `or`, `xor`, `implies`. `!` is only a function prefix; write `not n.read` or `n.read == false`, never `!n.read`.
- Enumeration: `==`, `!=`, `!asString()` (literal name). Literal in model: `<Model>::<EnumType>#<LITERAL>`, fully qualified.
- Date: backticks `` `2024-01-01` ``. Timestamp: ISO-8601 in backticks with mandatory zone `` `2024-01-01T12:00:00Z` ``.
- Temporal functions: `<Type>!now()` (SYSTEM vars; as attribute default fills at creation); `!year()`, `!month()`, `!day()` (Date/Timestamp); `!hour()`, `!minute()`, `!second()`, `!millisecond()` (Timestamp/Time); `!dayOfWeek()`, `!dayOfYear()` (Date); `!date()`, `!time()` (Timestamp); `<Type>!of(...)` constructors (Date 3 ints; Time 2–4; Timestamp `(date[,time])` or 5–7 ints); `!elapsedTimeFrom(other[,measure])` (dates in days, timestamps/times in seconds, then converted); `!asMilliseconds()`, `<Type>!fromMilliseconds(n)`; `!plusYears/Months/Days/Hours/Minutes/Seconds/Milliseconds(n)` (Date, Timestamp).

## 4. Reference Functions

- Instance functions: `!container(type)` (composition container; use `!asType(<Sub>)` to narrow; `Type` must be able to contain self, else `<Type> type is not a container type of <Self type>`); `!kindof(type)` (type or descendant); `!typeof(type)` (exact type); `!asType(type)` (instance or undefined); `!isDefined()`, `!isUndefined()`; `!memberOf(coll)`.
- Collection functions:
  - `!any()`: arbitrary single instance; see usage rules below.
  - `!contains(obj)`; `!count()`; `!empty()` (no `!isEmpty()`, fails `Unknown function: isempty`; use `not ...!empty()` or `!count() > 0`).
  - `!exists(i | expr)`; `!forAll(i | expr)`; `!filter(i | expr)`.
  - `!anytrue` / `!alltrue` / `!anyfalse` / `!allfalse` quantifiers; `!alltrue` = `!forAll`; `!anyfalse` = `not !forAll`.
  - `!head()` (no key: first, deterministic only after `!sort`); `!head(i | key)` (smallest key; DESC largest); `!heads(i | key)` returns ALL tied items, not first n. `!tail()`/`!tails()` mirror. No top-N: sort then page (`rowsPerPage`, `limit`).
  - `!sort(i | sel [DESC], ...)`; ASC default.
  - `!join(i | selector, sep)`: parsed but NOT implemented by query engine (`Not supported yet`). No string aggregation function exists. Compute in a backend `TRANSIENT` TO attribute populated by an `OperationCallInterceptor`. `!collectAsString` and `!mkString` do not exist.
  - `!asCollection(type)`.
  - `!avg` (int, decimal, date, timestamp, time; not strings); `!sum` (int and decimal only; else `Invalid expression for aggregation`); `!min`; `!max`.
- Empty aggregates: `!count()` of empty = 0 (COALESCE). `!sum`/`!min`/`!max` of empty = `undefined` (SQL NULL), not 0; undefined items skipped. Default via `!isDefined()` conditional (example unverified).
- No union operator. Direct items plus group items: `<Model>::<Item>!filter(i | self.<items>!contains(i) or self.<groups>.<items>!contains(i))` as getter of a derived `0..*` relation. `self.<groups>.<items>` flattens.
- Authoritative registry (closed set): `count, head, heads, tail, tails, any, filter, exists, forall, anytrue, alltrue, anyfalse, allfalse, empty, join, sort, min, max, sum, avg, contains, memberof, ascollection`. Others fail `Unknown function: <name>`.
- `!any()` rules:
  1. Only required when the final value must be a single instance (e.g. singleton Access `upper = 1`, or a single-entity DERIVED attribute). If the next step is relation navigation and the upstream filter is on a unique key (e.g. `userName == ACTOR.userName`), drop it: navigation flattens.
  2. At most once per expression.
  - Heuristic: relation step ending + unique-key filter → drop `!any()`. Keep only when final type must be single and upstream is a collection.

## 5. JQL Pitfalls & Scoping Rules

- Build failures (`Errors during building expression`) surface only in full `./judo.sh build` (EVL → ESM→Expression → PSM→ASM), not `transform --skip liquibase --load`.

### 5.1 Lambda scopes do not nest

- Each lambda gets ONE variable and nothing else from outer scope (not `self`, not outer lambda var).
- Inner lambda cannot reference `self` or the outer iterator. Navigate via relation instead (`y.parent.xs`).
- Cross-product predicates (∀a∈A ∀b∈B ∃c∈C(a,b)) are not expressible; compute in Java via `OperationCallInterceptor` into a `TRANSIENT` TO attribute. See `../backend/interceptors.md` (Backend-Computed TO Attribute).

### 5.2 Primitives must be fully qualified

- `String`, `Integer`, `Boolean` are ordinary DataType elements, not builtins. Use `<app>::types::String!getVariable('PRINCIPAL', 'claim_name')`. Bare `String!...` fails `Unknown symbol: String`.

### 5.3 `!getVariable` returns scalar String only

- No collection variant; no generic syntax. `Sequence<String>!getVariable(...)` and `String[]!getVariable(...)` fail the Xtext parser.
- Multi-value claims are not consumable in JQL. Options: flatten at IdP and compare with `==`; or compute scope in Java from `SecurityContext` and narrow via `OperationCallInterceptor`. See `../backend/architectural-patterns.md` §1 Model-Driven Multi-Tenancy.

### 5.4 `self` is not in scope on access getters

- `ActorType.accesses[*].getterExpression` runs at actor level; no `self`. Filter base must be the ENTITY FQN, not the TO.
- `<app>::entities::Partner!filter(p | p.code == <app>::types::String!getVariable('PRINCIPAL', 'partner_code'))` is correct; `<app>::services::PartnerTO!filter(...)` fails `ReferenceExpressionMatchesBinding`.
- `accessType="DERIVED"` requires a reference-returning expression; `getterExpression="true"` fails `ReferenceBindingExpressionIsValid`. For unrestricted access use `accessType="ALL"` with no getter.
- Full set of four rules: `../backend/architectural-patterns.md` *Rules for `accesses[*].getterExpression`*.

## Part 5: Rules and Best Practices

### CRITICAL: Prefer the CLI; document every hand-edit

- `/model/<app>.model` is XMI. Primary tool: `judo-model-cli` or Judo Designer. Avoid direct edits.
- Hand-edit only when CLI cannot: `xsi:type` polymorphic children (`<columns xsi:type="ui:DataColumn">`); adding `xmlns:` to root; space-separated ID lists on multi-reference features (e.g. `BinaryType.mimeTypes="_id1 _id2"`, since CLI `-s key=value` uses commas); root-level `<mimeTypes>` objects referenced from `BinaryType`.
- When hand-editing: record what was in the model, the validator/build error, and the change; verify with full `./judo.sh build` (not `transform --skip liquibase --load`); keep the diff minimal; do not re-flow or renumber IDs.

### Reserved member names on `createable` TOs

- Generated factory methods per createable TO: a same-named member causes `TS2393 Duplicate function implementation` at frontend build. See `./esm_metamodel/generator-reserved-names.md`.

### JQL cheatsheet for access-getter authoring

- Filter base = entity FQN; no `self`; no boolean literals on DERIVED; fully-qualified primitives in `!getVariable`.

### Do not edit the model file by hand

- Never edit XMI as text; use judo-cli or Designer. Hand edits break `xmi:id` references.

### Naming Conventions

- Case-sensitive. Letters, digits, underscores. Start with letter or underscore. Cannot end with `_` or contain `__`. Unique within container.

### General Best Practices

1. Start simple; add complexity incrementally.
2. Clear names (`CanvassingEvent` over `Event`).
3. Define relationships carefully (Composition vs Association; cardinality, ownership).
4. Use constraints (`required`, `Identifier`).
5. Coordinate with the team: model changes affect the whole application.
