# interceptors.md — index

Pull-only condensed map. Source: catalog/agent-docs/backend/interceptors.md.

## Pattern: Backend-Computed TO Attribute (JQL Escape Hatch)
- Use when a value cannot be a `DERIVED` DataMember: bipartite quantifiers (JQL lambdas do not nest), collection-valued context variables (`!getVariable` returns scalar `String` only), external I/O at read time.
- Steps: remove the `DERIVED` DataMember from the EntityType; declare it on each TO as `memberType="TRANSIENT"` with no `binding`; register an `OperationCallInterceptor` whose `postCall` fills it after the mapped read ops (`_getById`, list queries).
- Transient member is re-computed per request, no cache invalidation. Use an entity-level denormalisation only if the value must be filtered/sorted at the DAO layer.

## Advanced Interceptor Patterns
- Two interceptor types: `OperationCallInterceptor` and `AuthenticationInterceptor`.
- Denormalise/aggregate: `postCall` on update updates related `Tag`-style entities to keep read-side data precomputed.
- Decoupled creation (CQRS-like): `preCall` on create transforms data and triggers creation in another service/bounded context.
- Derived state enforcement: pair of interceptors on one source-of-truth enum field. Refresh interceptor reconciles derived relations in `postCall`; update interceptor reads the enum sent by the client and enforces the matching relations.

## Overview
- Cross-cutting logic on built-in business operations: auditing, payload manipulation (pre/post), side effects, complex validation.
- Interface `OperationCallInterceptor` methods: `getName()` (logging), `getOperations(AsmModel)`, `preCall`, `postCall`, `ignoreDecoratedCall()`, `async()`, `terminateOnException()`.
- `getOperations` default (empty) = all built-in operations. Must be resolved via `AsmUtils` and cached.
- `preCall` return replaces input; must be assignable to expected payload type (else `IllegalArgumentException`). With `ignoreDecoratedCall()==true` it must return the decorated call's return payload type.
- `postCall` gets input and return payload (`Payload` or collection); returned object becomes result.
- `ignoreDecoratedCall()` true skips the platform DAO call; decorated call runs only if no interceptor returns true.
- Validate-create/update: skipping the original call makes the operation fail with NullPointerException; do not skip it.
- `async()` true: different thread, outside transaction, no context variables; exceptions lost; cannot change payload.
- `async()` true: the runtime calls `preCall` (not `postCall`) after the operation, so `postCall` never runs; use a sync interceptor for post-operation logic.
- `terminateOnException()` defaults to `true`; ignored for async.
- Interceptors may throw only `InterceptorCallBusinessException`.

### OperationCallInterceptor Interface
- Implement with `@Component(property = { "judo.model.name=<model>" })`.

### The Interceptor Contract
- See Overview bullets above (method table).

### Which Operations Are Intercepted
- Only built-in behaviour ops: create, update, delete, list/query, refresh, set/unset/add/remove reference, reference range, input range, getTemplate, getMetadata, getPrincipal, upload token, export, validate calls.
- Custom (SDK) and script operations never hit interceptors, even if listed in `getOperations`. Write guards for custom ops (e.g. `toggleActive`, `createUser`, `resendInvitation`) inside each `*Custom` impl.
- Hiding a UI button does not protect an operation.
- Range interceptors fire only on `_getRangeReference*`, not `~list`. They are the security boundary for `rangeType=ANY`; model `min`/`max` are UI-only.
- Input validation of exposed operations runs without interceptors.
- Called from dispatcher behaviour calls (`CallInterceptorUtil` in `*Call` classes), not from DAO. DAO calls from Java service code do not trigger them.

### Ordering and Combining Several Interceptors
- `preCall` and `postCall` both run in registration order.
- Each preCall gets the original input payload, so it sees earlier in-place mutations; returned objects accumulate, last non-null wins. postCall same for return payload.
- Synchronous interceptors run inside the operation transaction; an exception from preCall/postCall rolls back the DAO write, including writes by earlier interceptors.

## Interceptor Component Registration
- `@Component(property = { "judo.model.name=<app>" })` required.
- Binds interceptor to one model; runtime matches interceptors to operations by it; multiple models can coexist.

## Example 1: Simple Logging Interceptor
- Pattern: log all intercepted ops. No `getOperations()` = all built-in ops.
- `AsmUtils.getOperationFQName()` gives FQN; `preCall()` runs before operation logic.

## Example 2: Selective Operation Interception (Create)
- `getOperations()` returns specific ops; FQN for create: `[model].services.[Service]#_createInstance[EntityName]`.
- Cache `interceptedOperations` and `asmUtils` lazily.
- postCall: cast to `CreateInstanceCallPayload`, read created ID, create related entities via relationship DAO, call other custom operations.

## Example 3: Update Interceptor with Batch Processing
- Update FQN: `#_updateInstance[FullEntityFQN]`; check `instanceof UpdateInstanceCallPayload`.
- `getInput()` = new values sent by client; `getInstance()` identifies the instance (`__identifier`) and carries no stored values; read old values with the DAO in `preCall`.
- Batch-query and cascade updates to dependent entities.

## Example 4: Pre-Call Payload Manipulation
- Modify input before execution; `Payload.map()` builds nested payloads (flat form fields to nested structure).
- preCall validation: `ValidationException` (field rule) or `InterceptorCallBusinessException` (business refusal) before the operation.
- Set references with `parentEntityDao.setPrimaryChild()` / `setDefaultChild()`.
- postCall can call external services on created entities.

## Example 5: Intercepting Reference Operations
- Single interceptor for `_addReference`, `_removeReference`, `_setReference` (and delete).
- Validate after change; `InterceptorCallBusinessException` rolls back the whole op.
- Use model-generated validation queries.

### Narrowing a Range with a Pre-Call Interceptor
- Pre-call payload of `_getRangeReference*` is `GetReferenceRangeCall.GetReferenceRangeCallPayload`: `owner` (EReference), `ownerPayload`, `queryCustomizer`, `recordCount` (settable).
- List op payload: `ListCall.ListCallPayload` (`owner`, `instance`, `queryCustomizer`, `recordCount`).
- `QueryCustomizer` is immutable (Lombok `@Builder`, no `toBuilder`): `filter` is JQL with `this` as target, conditions joined with ` and `; also `orderByList`, `seek`, `mask`, `parameters`, `instanceIds`, `withoutFeatures`.
- To add a constraint, build a new customizer copying other fields.
- `getOperations` must name the range op(s); return same payload type.

## Example 6: Handling Both Create and Update
- Single interceptor for create and update via `instanceof` pattern matching.
- `queryContainer()` gets parent entity; set references conditionally on entity flags.
- Injected custom services; invoke `validateEntity.accept()` operation.

## Throwing a Business Error from an Interceptor
- Only `InterceptorCallBusinessException` (package `hu.blackbelt.judo.runtime.core.dispatcher.behaviours`, subclass of `BusinessException`) may be thrown; declared on preCall/postCall.
- Modeled fault's generated `<Fault>Exception` is checked: cannot be thrown; catch it and rewrap.
- Raw `RuntimeException`/`IllegalStateException` becomes `InternalServerException` (generic 500).
- Response: dispatcher returns `_fault`; REST 422, header `X-Fault: <type>`, body `{ "<type>": {details}, "code": "<errorCode>" }` (keys starting `_` and nulls dropped).
- Exception rolls back DAO write, also when thrown from postCall.
- Use FQN of modeled fault TO as `type`; message/parameters in `details` (frontend resolves `faults.<type>` translations).
- Field rule on one attribute: `ValidationException` (400), `location` = attribute name (optional).
- Permission refusals: `InterceptorCallBusinessException` with stable `errorCode`.
- Mapping: see error-handling guide.

## Reading the Principal and Actor in an Interceptor
- Exchange map keys on `hu.blackbelt.judo.dispatcher.api.Dispatcher`: `PRINCIPAL_KEY` (`"__principal"`), `ACTOR_KEY` (`"__actor"`), `INSTANCE_KEY_OF_BOUND_OPERATION` (`"__this"`), `ENTITY_TYPE_MAP_KEY` (`"__entityType"`).
- Signed identifier of an instance: payload key `__signedIdentifier`.
- JQL/Java: `VariableResolver.resolve(String.class, "ACTOR", "identifier")`.

## Operation FQN Format Reference
- Create (transfer): `[model].[actor_pkg].[Actor]#_createInstance[EntityPlural]`.
- Create (contained): `[model].[entity_pkg].[Parent]#_createInstance[ChildPlural]`.
- Update / Delete: `[model].[entity_pkg].[Entity]#_updateInstance|_deleteInstance[FullEntityFQN]` (FQN with `_` separators, e.g. `<app>_access_management_AccessRole`).
- Add / Remove / Set reference: `[model].[entity_pkg].[Entity]#_addReference|_removeReference|_setReference[RelationshipName]`.
- Custom: `[model].[entity_pkg].[Entity]#[operationName]`.
- Find real FQNs with the bash snippet in the source (Finding Operation FQNs).

## Using .default Template Files
- Generator writes `.java.default` blueprints; they are NOT compiled by Maven.
- Workflow: rename `.java.default` to `.java`, implement bodies, uncomment code.
- Never edit `.default` files (regenerated each build). Do not add `.java` or `.java.default` to `.generator-ignore`.
- Templates: `Log*Interceptor`, `*ValidationInterceptor`, `Custom*ServiceImpl` (all must be renamed). Generated set depends on the model.

## See Also
- Authentication guide (authentication events), Custom operations (business logic wrapped), Patterns and best practices.
