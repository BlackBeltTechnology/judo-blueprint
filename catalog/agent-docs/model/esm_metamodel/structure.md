---
title: structure Package Reference
description: Reference of the ESM structure package: entity types, transfer objects, members, relations, mappings and behaviour rules.
aliases: [entity type definition, transfer object type, relation member rules, data member attributes, generalization inheritance, member context rules]
keywords: [EntityType, TransferObjectType, DataMember, TwoWayRelationMember, OneWayRelationMember, Generalization, Mapping, InvariantConstraint, QueryFeature, RelationKind, MemberType]
tags: [domain:model, layer:model, status:platform]
---

# `structure` Package Reference

**[◄ Back to Index](./README.md)**

The `structure` package is the core of the ESM, defining the business entities, their data structures, and how they relate to one another. This package represents the "nouns" of the application domain.

---

## Core Structural Elements

### `Class` (Abstract)
The abstract base for all complex types in the model, such as entities and transfer objects. It provides the common features of having attributes, relationships, and inheritance.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `attributes` | `DataFeature` | `[0..*]` | The list of data attributes (fields) for this class. |
| `relations` | `RelationFeature` | `[0..*]` | The list of relationships this class has with other classes. |
| `generalizations` | `Generalization`| `[0..*]` | The list of superclasses this class inherits from. Supported for entities only: inheritance between transfer object types is not supported, even though the `judo-cli` schema for `TransferObjectType` exposes `superTypes`. Declare each purpose-specific transfer object separately. |
| `createable` | Boolean | `[1]` | Specifies if instances of this class can be created. |
| `updateable` | Boolean | `[1]` | Specifies if instances can be updated. |
| `deleteable` | Boolean | `[1]` | Specifies if instances can be deleted. |

The class-level `createable`, `updateable` and `deleteable` flags are not read by the ESM→PSM, ESM→UI or generator code; they are only copied by the schema merge. Setting one to `false` on a whole entity or transfer object therefore does not remove pages or endpoints. The create, update, delete and refresh behaviours (and with them the generated REST operations and UI actions) come from the flags of the elements that reach the type:

- **create**: a relation or actor access with `createable = true` whose target is a mapped, non-abstract transfer object (for a stored relation the owner must be mapped too);
- **update**: the type is mapped and at least one relation, access, static navigation or output parameter targeting it has `updateable = true`;
- **delete**: the type is mapped and at least one such element has `deleteable = true` and is optional or to-many;
- **refresh**: the type is mapped.

Control CRUD per relation or access, not per type.

### `EntityType`
Represents a core, persistent business object with its own lifecycle and identity (e.g., `Customer`, `Product`). This is the primary element for defining the domain model.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of the entity. |
| `abstract` | Boolean | `[1]` | If `true`, this entity cannot be instantiated directly and must be subclassed. |
| `constraints` | `InvariantConstraint` | `[0..*]` | A list of business rules that must always hold true for this entity. |
| `sequences` | `EntitySequence` | `[0..*]` | Defines any database sequences associated with this entity. |
| `mapping` | `Mapping` | `[1]` | **Mandatory self-reference** — must point back to the owning `EntityType` itself (`target=<own xmi:id>`). EVL rejects an `EntityType` without it. See note below. |

**Mandatory self-mapping on `EntityType`.** Every `EntityType` must carry a `<mapping target="<own xmi:id>"/>` child (`target` = the entity's own id). EVL rejects an entity without it (`EntityTypeHasMapping`); removing these because they look redundant produces a cascade of validation errors. This is distinct from a `TransferObjectType`'s `mapping`, which projects the TO from an entity and carries the optional `filter`.

### `TransferObjectType`
A Data Transfer Object (DTO) used as a data structure for service operations or UI components. It acts as a "view" or "projection" of an `EntityType` and is the primary vehicle for data exchange.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of the TO (e.g., "CustomerDTO"). |
| `mapping` | `Mapping` | `[0..1]` | A reference to the `EntityType` this TO is based on, with an optional filter. |
| `operations` | `Operation` | `[0..*]` | The list of operations that can be performed on or with this TO. |
| `form` / `table` / `view` | UI Elements | `[0..1]` each | Direct references to the primary UI components defined for this TO. |

---

## Feature & Member Elements

### `DataMember`
A data-holding attribute within a `Class` (like `EntityType` or `TransferObjectType`). It represents a single piece of information, like a name or a date.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of the attribute (e.g., "firstName"). |
| `dataType` | `Primitive` | `[1]` | A reference to a logical data type from the `type` package. |
| `required` | Boolean | `[1]` | If `true`, this attribute must have a value. |
| `identifier` | Boolean | `[1]` | If `true`, this attribute is part of the natural key for the entity. The runtime enforces that the attribute's value is unique among the stored instances (and `null` is not checked). Each `identifier` attribute is checked on its own: two identifier attributes are two separate unique constraints, not one composite key. A violation fails the create or update with `IDENTIFIER_ATTRIBUTE_UNIQUENESS_VIOLATION`. The check is made by the runtime (payload validator and a SQL check per declaring table on the inheritance chain), not by a database constraint, and covers duplicates inside one batch. Model a composite key as an extra stored attribute with a value you compute, or as a hand-written validation. |
| `memberType` | `MemberType` Enum | `[1]` | Defines how the value is obtained: `STORED` (persistent), `DERIVED` (calculated), `MAPPED` (from a mapped entity), `TRANSIENT`. |
| `defaultExpression` | `DataExpression` | `[0..1]` | An expression to calculate the default value for this attribute. |

### `TwoWayRelationMember`
A bidirectional relationship between two classes, where both ends are explicitly linked and aware of each other (e.g., `Customer.orders` and `Order.customer`). `target` and `lower`/`upper` are not declared on this class: they are inherited (`target` from `ClassReference`, cardinality from `Cardinality`); `partner` and `primary` are its own features.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of this end of the relation (e.g., "orders"). |
| `target` | `Class` | `[1]` | The class on the other side of the relationship (e.g., `Order`). |
| `partner` | `TwoWayRelationMember` | `[1]` | A direct link to the corresponding member on the `target` class, making the relation bidirectional. |
| `lower` / `upper` | Integer | `[1]` | The cardinality of this end of the relationship (e.g., a Customer has `0..*` orders). |
| `relationKind`| `RelationKind` Enum | `[1]` | The nature of the relationship: `ASSOCIATION` (a simple link), `COMPOSITION` (a strong "owns" relationship with cascade delete), `AGGREGATION` (a weaker "part-of" relationship). **CLI note:** `judo-cli` `create`/`update` accept only `ASSOCIATION` and `COMPOSITION` for relation members, although the schema lists `AGGREGATION`; models that need `AGGREGATION` (see the asymmetric bidirectional pattern in [advanced-modeling-patterns.md](../advanced-modeling-patterns.md)) carry it from the modeling tool or a direct XMI edit. |
| `primary` | Boolean | `[1]` | In a many-to-many relationship, one side must be designated as primary to resolve ownership. |

### `OneWayRelationMember`
A unidirectional relationship from one class to another, like a simple reference or lookup where the target class has no knowledge of the source.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of the relationship. |
| `target` | `Class` | `[1]` | The class being pointed to. |
| `lower` / `upper` | Integer | `[1]` | The cardinality of the relationship. |
| `relationKind`| `RelationKind` Enum | `[1]` | The nature of the relationship (`ASSOCIATION`, `COMPOSITION`, or `AGGREGATION`). `judo-cli` sets only `ASSOCIATION` or `COMPOSITION` (see the CLI note above). |

---

## Other Structural Elements

### `Generalization`
Represents an inheritance relationship (`is-a`) between two classes, linking a subclass to a superclass.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `target` | `Class` | `[1]` | A reference to the superclass that is being inherited from. |

### `Mapping`
Links a `TransferObjectType` to an `EntityType`, defining how the DTO is projected from the underlying entity.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `target` | `Class` | `[1]` | The mapped class (`#//structure/Class` in `esm.ecore`; for a `TransferObjectType` it is the source `EntityType`, for an `EntityType`'s own mapping it is the entity itself). |
| `filter` | `LogicalExpression` | `[0..1]`| An optional expression to filter the instances of the `EntityType` that are visible through this TO. |

### `InvariantConstraint`
A validation rule or business invariant that must always be true for an instance of an `EntityType`.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of the constraint. |
| `expression` | `LogicalExpression` | `[1]` | The expression that must evaluate to `true` for the entity to be valid. |

### `QueryFeature` (Abstract)
The abstract base for features that can act as data queries, defining a common structure for inputs.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `input` | `TransferObjectType`| `[0..1]` | A reference to the TO that provides the input parameters for the query. |
| `isQuery` | Boolean | `[1]` | A flag indicating that this feature represents a query. |

---

## Behaviour Rules

These rules define how structural elements behave based on their context and attribute values.

### MemberType Context Constraints

The `memberType` attribute is constrained by the owner class type and mapping state.

#### Class Hierarchy
- `Class` (abstract base)
  - `EntityType` - persistent business object
  - `TransferObjectType` - DTO, can be **mapped** (has `mapping` to entity) or **unmapped**

#### DataMember Constraints

| MemberType | EntityType | TO (mapped) | TO (unmapped) | Notes |
|------------|------------|-------------|---------------|-------|
| `STORED` | ✓ | ✗ | ✗ | Only entities persist to database |
| `DERIVED` | ✓ | ✓ | ✓ | Calculated values allowed in all |
| `MAPPED` | ✗ | ✓ | ✗ | Requires entity source to map from |
| `TRANSIENT` | ✗ | ✓ | ✓ | Temporary values, not persisted |

#### RelationMember Constraints

##### Relation Hierarchy
- `RelationFeature` (abstract)
  - `OneWayRelationMember` - unidirectional reference
  - `TwoWayRelationMember` - bidirectional (has `partner`)

| Relation Type | EntityType | TO (mapped) | TO (unmapped) | Notes |
|---------------|------------|-------------|---------------|-------|
| `TwoWayRelationMember` | ✓ | ✗ | ✗ | Requires partner on target entity |
| `OneWayRelationMember` | ✓ | ✓ | ✓ | Simple reference |

##### OneWayRelationMember MemberType

| MemberType | EntityType | TO (mapped) | TO (unmapped) | Notes |
|------------|------------|-------------|---------------|-------|
| `STORED` | ✓ | ✗ | ✗ | Persistent relation |
| `DERIVED` | ✓ | ✓ | ✓ | Calculated relation |
| `MAPPED` | ✗ | ✓ | ✗ | Projects relation from entity |
| `TRANSIENT` | ✗ | ✓ | ✓ | Temporary relation |

##### Summary Constraints
- `memberType = STORED` → owner is `EntityType`
- `memberType = MAPPED` → owner is `TransferObjectType` AND `mapping` is not null
- `memberType = TRANSIENT` → owner is `TransferObjectType`
- `memberType = DERIVED` → valid in any `Class`
- `TwoWayRelationMember` → owner is `EntityType`
- **Transient relation on an unmapped transfer object**: the target of an unmapped transfer object's relation must be `AGGREGATION`. `relationKind=ASSOCIATION` fails validation with `Relation: <rel> (in: <TO>) must be aggregation if transient.` and `Unmapped transfer object type: <TO> can only have aggregation kind relations.` The CLI creates a relation with `relationKind=AGGREGATION` by default; `aggregation=true` is rejected as read-only, and `relationKind` is the field to set. When the target is also unmapped, the UI generator treats the relation as an inline transient relation (create is supported inline); a mapped target is chosen from existing instances. *Verify:* what `mutable input.<rel>` means for a transient relation in JCL, and the exact widget (nested form vs picker).

### DataMember Attribute Rules

| Attribute | Available When | Description |
|-----------|----------------|-------------|
| `identifier` | Container is **EntityType** AND `memberType = STORED` | Natural key field |
| `required` | Always | Field must have a value |
| `defaultExpression` | `memberType = STORED` | Default value calculation |
| `binding` | `memberType = MAPPED` | Source attribute from mapped entity |

#### Context Checks
- **In EntityType**: Container's type is `EntityType`
- **Read-only**: `memberType = MAPPED` AND binding source is read-only

### RelationMember Rules

#### TwoWayRelationMember

| Attribute | Description |
|-----------|-------------|
| `partner` | Required - links to the opposite end of the relationship |
| `primary` | In many-to-many, designates which side owns the relationship |
| `reverseCascadeDelete` | Partner side also has cascade delete |

#### RelationKind Behaviour

| RelationKind | Visual Style | Cascade Behaviour |
|--------------|--------------|-------------------|
| `COMPOSITION` | Filled diamond | `relationKind = COMPOSITION` → parent deletion deletes children |
| `AGGREGATION` | Empty diamond | `relationKind = AGGREGATION` → reference only, no cascade |
| `ASSOCIATION` | Simple line | `relationKind = ASSOCIATION` → simple link, no ownership |

**Note:** See [UI Visual Style Guide](./ui-visual-styleguide.md) for complete visual style rules.

Deleting an instance that is the target of an association:

- the referencing relation is cleared (the foreign key or join row is removed); the referencing instance stays;
- if the referencing relation has `reverseCascadeDelete = true`, the referencing instance is deleted as well;
- if the referencing relation is required (lower bound above 0) and not `reverseCascadeDelete`, the delete fails with `There are mandatory references that cannot be removed`;
- deleting an instance deletes its compositions; a reference with `reverseCascadeDelete` on the opposite end deletes the referenced instance too.

For a two-way association the same rules apply from either end.

### Range expressions on relations

- `rangeExpression` is only editable when `rangeType = DERIVED`; with `rangeType = DERIVED` a non-blank `rangeExpression` is required (EVL `DerivedRangeHasRangeExpression`). It applies to a stored entity relation and to a transient or editable mapped transfer object relation.
- `self` is allowed: `self.<relation>` and `self!container(<Type>).<path>` are valid range expressions (they build and the range is evaluated per instance), as is a type-level expression such as `<Model>::<Entity>!filter(e | ...)`.
- The server enforces the range. A value that is not in the range of the reference is rejected with `NOT_ACCEPTED_BY_RANGE`; an empty range only logs a warning.
- With `rangeType = ANY` the whole target type is the range and `rangeExpression` is read-only (the CLI rejects setting it).

### TransferObjectType Rules

| Attribute | Available When | Description |
|-----------|----------------|-------------|
| `mapping.filter` | `mapping` is NOT null | Filter expression for mapped entities |
| CRUD page | `mapping` is NOT null | CRUD tab only shown for mapped TOs |

#### Context Checks
- **Is Mapped**: `mapping` attribute is NOT null (has EntityType reference)
- **Purify**: Removes invalid references after modifications

### Context Detection Reference

| Check | True When |
|-------|-----------|
| In EntityType | Element's container type is `EntityType` |
| In TransferObjectType | Element's container type is `TransferObjectType` |
| Is Mapped (TO) | `TransferObjectType.mapping` is NOT null |
| Is Composition | `relationKind = COMPOSITION` |
| Is Aggregation | `relationKind = AGGREGATION` |
| Is Association | `relationKind = ASSOCIATION` |
| Has Valid Binding | `memberType = MAPPED` AND `binding` references a valid source |
| Is Read-Only | `memberType = MAPPED` AND source attribute cannot be modified |

---

## Related Documentation

- [UI Visual Style Guide](./ui-visual-styleguide.md) - Visual indicators and styling rules
- [UI Behaviour Rules](./ui-behaviour.md) - Conditional attributes and validation
- [Operation Package](./operation.md) - Operation and method definitions
- [Type Package](./type.md) - Data type definitions