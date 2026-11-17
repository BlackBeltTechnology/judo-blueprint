# structure.md — index

Pull-only condensed map. Source: catalog/agent-docs/model/esm_metamodel/structure.md.

## Core Structural Elements
- `Class` (abstract): base of entities and TOs. Features `attributes` (DataFeature), `relations` (RelationFeature), `generalizations`, flags `createable`/`updateable`/`deleteable`.
- `generalizations`: entities only. Inheritance between TOs is not supported (CLI `superTypes` on TO exists but do not use); declare purpose-specific TOs separately.
- Class-level `createable`/`updateable`/`deleteable` are copied by schema merge only; ESM→PSM, ESM→UI and generator ignore them. Setting `false` on a type does NOT remove pages/endpoints.
- Real CRUD comes from element flags, per relation or access (not per type):
  - create: relation/actor access with `createable=true` targeting a mapped, non-abstract TO (stored relation: owner must be mapped too).
  - update: type mapped AND some relation/access/static navigation/output param targeting it has `updateable=true`.
  - delete: type mapped AND such element has `deleteable=true` AND is optional or to-many.
  - refresh: type mapped.
- `EntityType`: `name`, `abstract` (cannot instantiate), `constraints` (InvariantConstraint), `sequences` (EntitySequence), `mapping` [1].
- EntityType MUST carry self-mapping `<mapping target="<own xmi:id>"/>`. EVL rejects without it (`EntityTypeHasMapping`). Do not remove as redundant.
- `TransferObjectType`: `name`, `mapping` [0..1] (source EntityType + optional `filter`), `operations`, `form`/`table`/`view` [0..1] each.

## Feature & Member Elements
- `DataMember`: `name`, `dataType` (Primitive from `type` package), `required`, `identifier`, `memberType`, `defaultExpression`.
- `identifier`: natural key. Runtime checks uniqueness per attribute (each is its own unique constraint, not composite; null not checked). Violation → `IDENTIFIER_ATTRIBUTE_UNIQUENESS_VIOLATION`. Enforced by runtime (payload validator + SQL check per declaring table incl. inheritance chain, covers same-batch duplicates), not DB constraint. Composite key: add computed stored attribute or hand-written validation.
- `memberType` enum: `STORED`, `DERIVED`, `MAPPED`, `TRANSIENT`.
- `TwoWayRelationMember`: `name`, `target` and cardinality inherited (`lower`/`upper`), `partner` (required, opposite end), `relationKind`, `primary` (many-to-many owner side).
- `OneWayRelationMember`: `name`, `target`, `lower`/`upper`, `relationKind`. Unidirectional.
- `relationKind` enum: `ASSOCIATION` (link), `COMPOSITION` (owns, cascade delete), `AGGREGATION` (part-of).
- CLI gotcha: `judo-cli` create/update accept only `ASSOCIATION` and `COMPOSITION` for relation members. `AGGREGATION` needs the modeling tool or direct XMI edit (see advanced-modeling-patterns.md, asymmetric bidirectional pattern).

## Other Structural Elements
- `Generalization`: `target` (superclass), is-a.
- `Mapping`: `target` (TO → source EntityType; entity's own mapping → itself), `filter` [0..1] (LogicalExpression limiting visible instances).
- `InvariantConstraint`: `name`, `expression` [1] (must evaluate true).
- `QueryFeature` (abstract): `input` (TO with query input params) [0..1], `isQuery` [1].

## Behaviour Rules
- MemberType by owner (DataMember):
  - `STORED`: EntityType only (persisted).
  - `DERIVED`: any (EntityType, mapped TO, unmapped TO).
  - `MAPPED`: mapped TO only; requires entity source.
  - `TRANSIENT`: mapped or unmapped TO only; not persisted.
- RelationMember memberType: `TwoWayRelationMember` → EntityType only, needs partner on target. `OneWayRelationMember`: STORED → entity; DERIVED → any; MAPPED → mapped TO; TRANSIENT → any TO.
- Summary: STORED ⇒ owner EntityType; MAPPED ⇒ owner TO AND `mapping` not null; TRANSIENT ⇒ owner TO; DERIVED valid anywhere.
- Unmapped TO transient relation: target must be `AGGREGATION`. ASSOCIATION fails: `Relation: <rel> (in: <TO>) must be aggregation if transient.` / `Unmapped transfer object type: <TO> can only have aggregation kind relations.`
- CLI default relationKind for relations is AGGREGATION; set `relationKind`, not `aggregation=true` (rejected read-only).
- Unmapped target → UI treats relation as inline transient (create inline). Mapped target → pick from existing instances.
- Open verify item: meaning of `mutable input.<rel>` for transient relation in JCL, and widget (nested form vs picker).
- DataMember attribute availability: `identifier` only in EntityType AND STORED; `defaultExpression` only STORED; `binding` only MAPPED; `required` always.
- Read-only: MAPPED AND binding source read-only.
- TwoWayRelationMember: `partner` required; `primary` for many-to-many; `reverseCascadeDelete` = partner side also cascade delete.
- RelationKind visuals/cascade: COMPOSITION = filled diamond, parent delete deletes children; AGGREGATION = empty diamond, reference only; ASSOCIATION = plain line, no ownership. Full style rules: ui-visual-styleguide.md.
- Deleting the target of an association:
  - referencing relation cleared (FK/join row removed); referencing instance stays;
  - if referencing relation has `reverseCascadeDelete=true`, referencing instance is deleted too;
  - if referencing relation is required (lower > 0) and not reverseCascadeDelete → fails `There are mandatory references that cannot be removed`;
  - deleting an instance deletes its compositions.
  - Same rules from either end of two-way association.
- Range expressions:
  - `rangeExpression` editable only when `rangeType = DERIVED`; then non-blank required (EVL `DerivedRangeHasRangeExpression`). Applies to stored entity relations and transient or editable mapped TO relations.
  - `self.<rel>`, `self!container(<Type>).<path>`, and `<Model>::<Entity>!filter(e | ...)` are valid.
  - Server enforces: out-of-range value → `NOT_ACCEPTED_BY_RANGE`; empty range only warns.
  - `rangeType = ANY`: whole target type is range; `rangeExpression` read-only (CLI rejects setting).
- TransferObjectType: `mapping.filter` only when mapping not null; CRUD tab only for mapped TOs. Purify removes invalid references after modifications.
- Context checks: In EntityType / In TO (container type); Is Mapped (TO.mapping not null); Is Composition / Aggregation / Association (relationKind); Has Valid Binding (MAPPED and binding valid); Is Read-Only (MAPPED and source not modifiable).

## Related Documentation
- ui-visual-styleguide.md — visual indicators and styling
- ui-behaviour.md — conditional attributes and validation
- operation.md — operation and method definitions
- type.md — data type definitions
