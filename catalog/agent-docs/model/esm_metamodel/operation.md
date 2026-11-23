---
title: operation Package Reference
description: Reference of the ESM operation package: operations, parameters, faults, statefulness, behaviours and rules.
aliases: [operation metamodel, custom operation implementation, stateful operation, operation faults, operation type enum, initializer operation, GET_RANGE template]
keywords: [Operation, operationType, customImplementation, stateful, faults, OperationType, INITIALIZER, MAPPED, GET_RANGE, GET_TEMPLATE, IllegalStateException]
tags: [domain:model, layer:model, status:platform]
---

# `operation` Package Reference

**[◄ Back to Index](./README.md)**

This package defines the services and methods that encapsulate the application's business logic. It represents the "verbs" of the model, specifying the actions that can be performed on or with the data structures defined in the `structure` package.

---

## Element Reference

### `Operation`
Represents a single service operation or method. It defines the contract for a piece of business logic, including its inputs, outputs, and potential errors.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of the operation (e.g., "deactivateCustomer"). |
| `input` | `Parameter` | `[0..1]` | The input parameter (DTO) for the operation. If absent, the operation takes no input. |
| `output` | `Parameter` | `[0..1]` | The return value (DTO) of the operation. If absent, the operation returns `void`. |
| `faults` | `Parameter` | `[0..*]` | A list of possible exceptions or errors the operation can throw, each defined by a `Parameter` whose `target` is a `TransferObjectType` with cardinality `1..1` (EVL `OperationFaultTargetsAreDefined`, `FaultCardinalityIsValid`). See *Faults and the generated exception* below. |
| `operationType`| `OperationType` Enum | `[1]` | Defines the nature of the operation: `INSTANCE` (operates on an object instance), `STATIC` (class-level operation), `INITIALIZER` (constructor), `ABSTRACT`, `MAPPED`. |
| `stateful` | Boolean | `[1]` | If `true`, the operation can modify the state of the system. If `false`, it is a query with no side effects. |
| `body` | `Script` | `[0..1]` | The implementation logic for the operation, often in a scripting language. |
| `customImplementation` | Boolean | `[1]` | If `true`, the body is provided manually. If `false`, the implementation may be generated. |


### `Parameter`
Defines an input, output, or fault for an `Operation`. It is a named, typed reference that specifies the data structure for the message part.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of the parameter. |
| `target` | `TransferObjectType` | `[1]` | A reference to the DTO that defines the structure of this parameter. |
| `lower` / `upper` | Integer | `[1]` | The cardinality, allowing the parameter to be a single object (`1..1`) or a list of objects (`0..*`). |

### Enums

| Enum | Value | Description |
| :--- | :--- | :--- |
| **`OperationType`** | `INSTANCE` | An operation that is called on an instance of a `TransferObjectType`. |
| | `STATIC` | An operation that is called at the class level, without an instance. |
| | `INITIALIZER` | A special operation that acts as a constructor or factory for a `TransferObjectType`. |
| | `ABSTRACT` | Declares an operation that must be implemented by subclasses. |
| | `MAPPED` | An operation on a TO that is directly mapped from an operation on the underlying `EntityType`. |

### Faults and the generated exception

The SDK generator emits one top-level, checked `<Name>Exception extends java.lang.Exception` per fault transfer object (template `dao.fault.java.hbs`), in the same API package as the DTO. It is generated once per transfer object and can be reused by several operations. It has the constructors `(details)`, `(errorCode, details)` and `(errorCode, details, cause)`, plus `getErrorCode()` (the exception message) and `getDetails()`. The generated `throws` clause of an operation lists its declared faults.

Consequence for custom implementations: an operation implemented in Java (`customImplementation = true`) that throws a business fault **must declare that fault in `faults`**; otherwise the generated interface has no `throws <Name>Exception` and the Maven build fails with "not compatible with throws clause". The same applies to an operation whose output DTO equals the root of the action-container view: the frontend generator then references a non-existent `*OutputView`, so drop the output or make the operation `void`.

### Operation naming and shape constraints

- An operation name may not equal `set` or `get` plus an attribute or relation name (case-insensitive): those names are reserved for generated accessors.
- The `stateful` flag of an `INSTANCE` operation must match every inherited non-abstract operation of the same name.
- An `INITIALIZER` operation must be `STATIC` and take no input.
- A fault parameter must have cardinality `1..1`; an input whose range is `DERIVED` needs a non-blank `rangeExpression`.

### Operation bodies (JCL) and validation

An operation body is a JCL script when `customImplementation = false`; `customImplementation = true` switches to Java. The editor-side EVL constraint `ScriptValid` (severity ERROR) builds the JCL body of every operation whose implementation is not custom and reports any message the JCL validator returns; operations with `customImplementation = true` are skipped. See [Operation script language (JCL)](../jcl-operation-scripts.md).

### Statefulness derived from behaviour

When an operation has a behaviour and no implementation, the PSM→ASM transformation derives its `stateful` annotation from the behaviour type: `VALIDATE_CREATE`, `VALIDATE_UPDATE`, `LIST`, `EXPORT`, `GET_RANGE`, `GET_TEMPLATE`, `GET_PRINCIPAL`, `GET_METADATA` and `VALIDATE_OPERATION_INPUT` are stateless; `REFRESH`, `UPDATE_INSTANCE`, `DELETE_INSTANCE` and `GET_UPLOAD_TOKEN` are stateful. With an implementation it follows the implementation; with neither it defaults to stateful. At runtime the DAO enforces the flag: `INSERT`, `UPDATE`, `DELETE`, `SET`, `UNSET`, `ADD` and `REMOVE` throw `IllegalStateException` (`... is not supported in stateless operation`) when the call context is stateless, unless the context is a rollback. A custom operation that writes must therefore be modelled `stateful`.

### GET_RANGE and GET_TEMPLATE behaviours

`GET_RANGE` sources the options of a reference selector. It is an unbound operation (for example `_getRangeReferenceCategory`) whose input parameter is named `input` (cardinality `0..1`) and typed by an unmapped transfer object with an embedded `owner` relation to the owning transfer object; the output is the range type. Its owner must be a relation or operation of the containing transfer object. `GET_TEMPLATE` produces a prepopulated create/operation-input prototype (REST path `<TO>/~template`); it must be owned by an unbound operation and its owner must be a transfer object type without a relation. A mapped transfer object gets it when a `createable` relation targets it or when it is the input of an operation.

---

## Behaviour Rules

These rules define how operation elements behave based on their context and attribute values.

### OperationType Context Constraints

The `operationType` attribute is constrained by the owner class type and mapping state.

#### In EntityType

| OperationType | Standard Mode | Advanced Mode | Notes |
|---------------|---------------|---------------|-------|
| `INSTANCE` | ✓ | ✓ | Operations on entity instances |
| `STATIC` | ✓ | ✓ | Class-level operations |
| `INITIALIZER` | ✓ | ✓ | Factory/constructor operations |
| `ABSTRACT` | ✗ | ✓ | Only in advanced mode |
| `MAPPED` | ✗ | ✗ | Not available in entities |

#### In TransferObjectType (mapped)

| OperationType | Available | Notes |
|---------------|-----------|-------|
| `INSTANCE` | ✓ | Operations on TO instances |
| `STATIC` | ✓ | Class-level operations |
| `INITIALIZER` | ✓ | Factory operations |
| `MAPPED` | ✓ | Binds to entity operation |

#### In TransferObjectType (unmapped)

| OperationType | Available | Notes |
|---------------|-----------|-------|
| `INSTANCE` | ✗ | No entity instance to operate on |
| `STATIC` | ✓ | Only static operations allowed |
| `INITIALIZER` | ✓ | Factory operations |
| `MAPPED` | ✗ | No entity to map from |

An unmapped transfer object accepts only `STATIC` operations (EVL `UnmappedTransferObjectTypeHasStaticOperations`). The ESM→PSM transformation creates each as an unbound operation placed in that transfer object's own PSM equivalent (rule `CreateInPlaceUnboundOperation`); a `STATIC` operation on an entity is instead placed in the entity's default transfer object. Any unmapped transfer object can therefore carry static operations, not only a `StaticOperations` container. An actor reaches the operation through a derived access on the actor whose target is a mapped transfer object; the validator reports `Access target have to be mapped` otherwise. The REST route is `POST /api/<app>/<Actor>/<TransferObject>/<operation>` with the input as the JSON body; a business fault returns 422 with the `X-Fault` header.

##### Summary Constraints
- `operationType = ABSTRACT` → owner is `EntityType` AND `advanced mode = true`
- `operationType = MAPPED` → owner is `TransferObjectType` AND `mapping` is NOT null
- `operationType = INSTANCE` → owner is `EntityType` OR (owner is `TransferObjectType` AND `mapping` is NOT null)

### INITIALIZER Special Handling

The `INITIALIZER` type is internally stored as a combination of `STATIC` type with an `initializer` flag:

| User Selection | Internal State |
|----------------|----------------|
| `INITIALIZER` | `operationType = STATIC`, `initializer = true` |
| Any other type | `initializer = false` |

#### On type change
- When `INITIALIZER` is selected: sets `initializer = true`, stores `operationType = STATIC`
- When switching from `INITIALIZER` to another type: sets `initializer = false`

#### Creating an initializer with the CLI
The CLI does not apply the Designer's translation. `create`/`update -s operationType=INITIALIZER` stores the literal `INITIALIZER` with `initializer = false`. On an unmapped transfer object `validate` then fails (`must be static in unmapped transfer object type`, exit 1); on an entity it validates, but the operation is an instance operation, not an initializer, and the generated implementation interface is `accept(<Entity> _this)`. Write the stored form directly: `-s operationType=STATIC -s initializer=true` (check with `update <fqn> --schema`). The generated interface is then `void run()` on an entity and on an unmapped transfer object alike (no input, no output; with an output it is `<Output> get()`).

### Operation Attribute Rules

| Attribute | Enabled When | Description |
|-----------|--------------|-------------|
| `body` | Always | JCL script (when `customImplementation = false`) or documentation (when `customImplementation = true`) |
| `customImplementation` | Always (in Implementation page) | `false` = JCL implementation, `true` = Java implementation (body used for documentation) |
| Edit body button | `operationType = STATIC` OR `operationType = INSTANCE` | Opens script editor |

### Operation Page Visibility

| Page | Visible When |
|------|--------------|
| Input | Always |
| Output | Always |
| Implementation | `advanced mode = true` AND (`operationType = INSTANCE` OR `operationType = STATIC`) |
| Faults | `advanced mode = true` |
| CRUD | `output` is NOT null |

### Input Parameter Attribute Rules

| Attribute | Enabled When | Description |
|-----------|--------------|-------------|
| `inputType` | Always | Reference to input TransferObjectType |
| `cardinality` | `input` is NOT null | `0..1`, `1..1`, or `0..*` |
| `rangeType` | `input` is NOT null AND `input.target` is mapped | `ANY` or `DERIVED` |
| `rangeExpression` | `rangeType = DERIVED` | JQL expression for filtering range |
| `wrapAsOptional` | `input` is NOT null AND `input.target` is NOT mapped | Wrap nulls in Optional |

#### Cardinality Mapping

| Display | lower | upper |
|---------|-------|-------|
| `0..1` | 0 | 1 |
| `1..1` | 1 | 1 |
| `0..*` | 0 | -1 |

### Output Parameter Attribute Rules

| Attribute | Enabled When | Description |
|-----------|--------------|-------------|
| `outputType` | Always | Reference to output TransferObjectType |
| `cardinality` | `output` is NOT null | `0..1`, `1..1`, or `0..*` |

A `GET_PRINCIPAL` operation's output must have cardinality `0..1` (lower 0, upper 1); the model validation fails otherwise (`GET_PRINCIPAL output cardinality must be 0..1`).

### Output CRUD Settings

When `output` is NOT null, CRUD permissions can be configured:

| Attribute | Description |
|-----------|-------------|
| `updateable` | External clients can modify instances |
| `deleteable` | External clients can delete instances |

### Mapped Operation Rules

The `generateOperations` flag has two defaults in the Java rules: `isMappedOperation` treats an absent flag as `false`, while `shouldGenerateOperations` treats it as `true`.

**Visible when:** Owner is `TransferObjectType` AND `operationType = MAPPED`

| Attribute | Description |
|-----------|-------------|
| `binding` | Name of the operation in the mapped entity |

**Binding Candidates:** Compatible operations from `mapping.target` (EntityType) where `isOperationCompatible()` returns true.

### Parameter Validation Rules

| Rule | Description |
|------|-------------|
| `target` is NOT null | Parameter must have a target type |
| `name` is NOT empty | Parameter must have a name |
| `isUniqueName()` | Parameter name must be unique within the operation |

### Visual Style Indicators

| Condition | Visual Effect |
|-----------|---------------|
| `operationType = STATIC` | Static style/icon |
| `operationType = ABSTRACT` | Abstract style/icon |
| `operationType = STATIC` AND `initializer = true` | Initializer style/icon |
| `operationType = MAPPED` AND `isValidMapping() = false` | Error/invalid style |

### Context Detection Reference

| Check | True When |
|-------|-----------|
| In EntityType | Operation's container type is `EntityType` |
| In TransferObjectType | Operation's container type is `TransferObjectType` |
| Is Mapped (TO) | `TransferObjectType.mapping` is NOT null |
| Advanced Mode | `Model.advanced = true` |
| Has Valid Mapping | `operationType = MAPPED` AND `binding` references a valid operation |

---

## Related Documentation

- [Structure Package](./structure.md) - Entity and TransferObjectType definitions
- [UI Package](./ui.md) - OperationForm and UI bindings
- [UI Behaviour Rules](./ui-behaviour.md) - Operation-related UI rules