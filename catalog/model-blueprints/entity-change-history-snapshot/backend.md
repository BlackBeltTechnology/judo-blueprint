## Backend guidance

### Write the snapshot in the same operation as the change

Interceptors run only for built-in operations, and custom operations get no interceptor. So every operation that changes a tracked attribute writes its own snapshot. Write it after the parent is saved, inside the same transaction, so that the snapshot and the change commit or roll back together.

- Build the snapshot from the saved values: copy each tracked field, set `changed` to the current time, and set the association to the parent.
- Use one shared helper for the snapshot, so every operation writes the same fields in the same way.
- Write the first snapshot when the parent is created, as the baseline.

### Delete the snapshots with the parent

The association is owned by the parent. Before deleting a parent, delete its snapshot rows first. A plain delete of the parent leaves orphan rows.

### Use the read side for reports

Expose the snapshots as a read-only transfer object, with the copied fields and `changed`. Report queries filter by `changed` to find the value that applied on a given date.

### Errors

Writing a snapshot is a platform write. Do not throw a business fault for it. A failure should fail the operation, so the change and its snapshot stay consistent.

## Examples

### indamedia-adtrack

- The parent campaign service writes a snapshot on create (baseline) and on each update, after the campaign is saved.
- Delete runs the snapshot deletion first, then the parent.
- The snapshot copies name, start, end, total budget and daily budget, which are the fields a user can change.
- The project's own service classes are project code. Copy the pattern, not the names.
