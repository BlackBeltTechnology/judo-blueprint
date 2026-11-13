## Backend guidance

### Write the snapshot in the same operation as the change

Interceptors run only for built-in operations, and custom operations get no interceptor. So every operation that changes a tracked attribute writes its own snapshot. Write it after the parent is saved, in the same operation, so that the snapshot and the change succeed or fail together.

- Build the snapshot from the saved values: copy each tracked field, set `changed` to the current time, and set the association to the parent.
- The snapshot is written through the generated DAO. Full create is generated only for mapped, non-abstract transfer object types, so the history needs a mapped transfer object (service layer, not drawn), created through the parent's relation method.
- Use one shared helper for the snapshot, so every operation writes the same fields in the same way.
- Write the first snapshot when the parent is created, as the baseline.

### Delete the snapshots with the parent

The association is owned by the parent. Before deleting a parent, delete its snapshot rows first. With a plain association a delete of the parent leaves orphan rows (a composition would remove them).

### Use the read side for reports

Expose the snapshots as a read-only transfer object, with the copied fields and `changed`. Report queries filter by `changed` to find the value that applied on a given date.

### Errors

Common practice: do not turn a snapshot failure into a business fault. An unexpected runtime exception becomes a generic 500 and fails the operation, so the change and its snapshot stay consistent. Report bad user input with a `ValidationException` before the write.

## Examples

### Variant seen in practice

- The parent service writes a snapshot on create (baseline) and on each update, after the parent is saved.
- Delete runs the snapshot deletion first, then the parent.
- The snapshot copies name, start, end, total and daily amount, which are the fields a user can change.
- The application's own service classes are application code. Copy the pattern, not the names.
