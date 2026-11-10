## Backend guidance

### Toggle operations keep the parent valid

Each toggle operation is a custom instance operation. Interceptors do not run for custom operations (platform behaviour), so the operation itself must check the rules that matter after a change.

- Toggling a contact off must not leave the parent without an active primary. If the contact is the primary, either refuse the change with a business fault (declared in the operation's `faults`, otherwise the generated interface has no matching `throws`) or move the primary to another active contact in the same operation.
- Toggling a contact on does not change the primary.
- Re-read the parent after the change and run its validation again, so the parent's rules see the new flag.

### Set the primary in the same transaction as the create

When a contact is created with a flag that says it is primary, the operation that creates it should also set the parent's primary association. Do both in one transaction so a failure leaves neither change.

### Keep one primary per parent

The primary association has an upper bound of one. Setting a new primary replaces the old one; the old contact stays in the list with its active flag unchanged.

### Project code, not platform API

The example project implements these rules in its own toggle classes and create interceptors (interceptors on the built-in create operations, which run inside the operation's transaction), with its own data-access classes. Those names are project code. Copy the pattern, not the names.

## Examples

### rackinspect

- Three parallel sets of contact entities exist, one for each parent type, with the same structure.
- Create interceptors run after the parent's create operations and set the primary when the new contact is flagged as primary.
- Toggle operations re-run the parent's validation after the flag changes.
