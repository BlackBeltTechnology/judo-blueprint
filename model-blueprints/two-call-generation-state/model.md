## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Handle" } }) {
  items { fqn name createable updateable deleteable
    attributes { items { name dataType } }
    relations { items { name lower upper relationKind memberType } }
  }
} } }
```

```graphql
{ esm { entitytypes(where: { name: { eq: "Document" } }) {
  items { fqn name createable updateable deleteable
    attributes { items { name dataType } }
    relations { items { name lower upper relationKind memberType } }
  }
} } }
```

```graphql
{ esm { enumerationtypes(where: { name: { eq: "HandleState" } }) {
  items { fqn name literals { items { name } } }
} } }
```

## Creation Mutations

### HandleState enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}::types", name: "HandleState"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationLiteral: {
  container: "{{NAMESPACE}}::types::HandleState", name: "ACTIVE"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationLiteral: {
  container: "{{NAMESPACE}}::types::HandleState", name: "CONFIRMED"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationLiteral: {
  container: "{{NAMESPACE}}::types::HandleState", name: "EXPIRED"
} }) { success fqn } }
```

### Handle entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Handle",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Handle", name: "state",
  memberType: "{{NAMESPACE}}::types::HandleState", required: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Handle", name: "expiresAt",
  dataType: "judo::types::TimeStamp", required: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Handle", name: "body",
  dataType: "judo::types::LongText", required: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Handle", name: "bodyOverflow",
  dataType: "judo::types::BinaryType", required: false
} }) { success fqn } }
```

### Handle → source entity relations (0..1 ASSOCIATION, repeat per source)

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Handle", name: "{{SOURCE_ENTITY_LCNAME}}",
  target: "{{NAMESPACE}}::{{SOURCE_ENTITY}}", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

### Document entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Document",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Document", name: "identifier",
  dataType: "judo::types::String", required: true
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Document", name: "content",
  dataType: "judo::types::LongText", required: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Document", name: "finalFile",
  dataType: "judo::types::BinaryType", required: false
} }) { success fqn } }
```

### Document → source entity relations (0..1 ASSOCIATION — keeps document alive after source deletion)

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Document", name: "{{SOURCE_ENTITY_LCNAME}}",
  target: "{{NAMESPACE}}::{{SOURCE_ENTITY}}", lower: 0, upper: 1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

### Back-reference on source entity → Document (0..* ASSOCIATION, optional but useful)

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{SOURCE_ENTITY}}", name: "documents",
  target: "{{NAMESPACE}}::Document", lower: 0, upper: -1,
  relationKind: "ASSOCIATION"
} }) { success fqn } }
```

## Examples

### compsychletter (add-document-cluster, 2026-05-12)

**Entities:** `GenerationHandle`, `GeneratedDocument`

**HandleState enum** (`compsychletter::entities::types::HandleState`):
- Literals: `ACTIVE`, `CONFIRMED`, `EXPIRED`

**GenerationHandle** (`compsychletter::entities::GenerationHandle`): non-CRUD
- Attributes:
  - `state` (req, HandleState enum) — lifecycle discriminator
  - `expiresAt` (req, TimeStamp) — lazy-expiry sentinel; no background GC
  - `body` (opt, LongText) — inline output for text-based outputs (MD, TEXT)
  - `bodyOverflow` (opt, BinaryType) — overflow for large bodies exceeding in-memory limit
- Relations (all 0..1 ASSOCIATION):
  - `template` → Template
  - `dataObject` → DataObject
  - `design` → Design

**GeneratedDocument** (`compsychletter::entities::GeneratedDocument`): non-CRUD
- Attributes:
  - `identifier` (req, String) — external reference value, e.g. barcode payload or UUID
  - `content` (opt, LongText) — document body for text output types
  - `finalFile` (opt, BinaryType) — rendered file for binary output types (PDF, DOCX); null for MD/TEXT
- Relations (all 0..1 ASSOCIATION — document survives source deletion):
  - `template` → Template
  - `dataObject` → DataObject
  - `design` → Design

**Design rationale:**
- ASSOCIATION (not COMPOSITION) on all cross-cluster relations ensures Document rows survive if Template / DataObject / Design are deleted.
- `finalFile` is 0..1 because some output types (MD, TEXT) produce no separate binary file.
- No GC operation for expired Handles — callers re-check `expiresAt` on the start-operation response; the confirm operation rejects stale Handles without a separate cleanup job.
- Both entities have createable=false, updateable=false, deleteable=false — all writes go through backend custom operations.
