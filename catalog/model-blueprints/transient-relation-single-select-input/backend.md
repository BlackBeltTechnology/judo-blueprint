## Backend guidance

### The operation body links the picked record

The operation that consumes the input transfer object creates (or updates) the owning entity and assigns the transient picker selection to a stored relation. The source project wrote this in the operation body with `mutable input.<relation>`:

```
operation createInitiative(input: InitiativeInput): Initiative {
  body: Initiative!create(new Initiative(
    title := input.title,
    region := mutable input.region,
    category := mutable input.category
  ))
}
```

This sketch is the old project's form. Check it against the [JCL operation scripts](../../agent-docs/model/jcl-operation-scripts.md) reference before use: JCL bodies refer to the instance as `this` (not `self`), `input` is immutable unless declared mutable, and `mutable` is a unary prefix operator. The agent-docs do not say what a transient reference means when assigned to a stored relation, so the claims below are project experience, *verify* them.

- `input.region` is a transient reference to an instance of the mapped transfer object.
- `mutable input.region` turned it into the reference to the stored entity, usable as the value of the stored relation on the new entity.
- A body without `mutable` produced an entity without the link and no compile or runtime error in the source project.

### Custom Java implementation

When the operation has `customImplementation = true`, no JCL body exists and the editor does not parse the Java ([JCL operation scripts](../../agent-docs/model/jcl-operation-scripts.md), validation). Resolve the picked record yourself through the generated DAO and assign it to the stored relation of the new entity ([data access guide](../../agent-docs/backend/data-access-guide.md)). The exact API calls are not in the agent-docs, *verify*.

Interceptors never run around custom, mapped or script operations, so any eligibility check beyond the range expression belongs in the body.

### Test it

Write an integration test that calls the operation with a picked record and asserts that the persisted relation is set and points to that record. See [[integration-test-reflection-injection]] for how such tests are built.
