## Backend guidance

### The operation body links the picked records

The operation consuming the input transfer object creates (or updates) the owning entity and assigns the transient collection to a stored relation. The source projects wrote this with `mutable input.<relation>`:

```
operation assignApproval(input: ApprovalTaskInput): Void {
  body: {
    var task := ApprovalTask!create(new ApprovalTask(
      product := this,
      assignees := mutable input.users,
      dueDate := input.dueDate
    ))
  }
}
```

This is the old projects' form, adapted to use `this` (JCL bodies use `this`, never `self`; see [JCL operation scripts](../../agent-docs/model/jcl-operation-scripts.md)). The agent-docs do not describe what happens when a transient collection is assigned to a stored relation, so treat the following as project experience, *verify* it:

- `input.users` is a transient collection of references to mapped transfer object instances.
- `mutable input.users` turned it into a collection assignable to the stored relation, element by element. The agent-docs say that navigation from `input`, including a transient reference, stays immutable and that changing a collection through an immutable object fails ([JCL operation scripts](../../agent-docs/model/jcl-operation-scripts.md)), so this exact form is the first thing to verify.
- A body without `mutable` persisted the owning entity with an empty collection and raised no error.

Projects: one uses a filtered picker of eligible users in an assign-approval operation, and another uses `mutable input.signs` in a create operation.

### Custom Java implementation

With `customImplementation = true` the editor does not parse the body ([JCL operation scripts](../../agent-docs/model/jcl-operation-scripts.md), validation). Look up each picked record through the generated DAO and assign the resulting collection ([data access guide](../../agent-docs/backend/data-access-guide.md)). The exact calls are not in the agent-docs, *verify*. Interceptors never run around custom operations.

### Test it

Integration test: call the operation with a non-empty selection and assert the persisted collection has the same size and the same members. See [[integration-test-reflection-injection]].
