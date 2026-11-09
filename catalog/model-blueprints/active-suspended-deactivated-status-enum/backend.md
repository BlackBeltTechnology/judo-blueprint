## Backend guidance

### Check the current status in each transition

Each transition is a custom operation. Interceptors do not run for custom operations, so no interceptor enforces the state rules. Each operation must read the current status, refuse the transition when the status is not the expected one, and then set the new value.

- Suspend requires ACTIVE. Reactivate requires SUSPENDED. Deactivate may be allowed from ACTIVE or SUSPENDED, depending on the domain rule.
- Refuse an invalid transition with a modeled business fault that the operation declares. Platform errors are not used for business rules.
- Write the status and any related change in one operation, so the transaction covers both.

### Guard the last administrator in the service

Rules such as "the last platform administrator cannot be suspended" depend on other rows. Put them in a domain service that the operations call, and count the remaining administrators inside the same transaction.

- The service class is project code. Its name belongs to the example project, not to the platform.
- Re-read the entity from the database inside the service before the check, so a concurrent change is seen.

### Audit each transition

Log one audit record per transition, with the previous status, the new status and the acting user. See [[audit-log-entity]] for the record shape. The audit call goes inside the operation, not in an interceptor.

## Examples

### mlszksz-platform

- Users and organizations each have a status with these three values. Both share the same member names and ordinals.
- Each transition on the user and on the organization admin panel is a separate custom operation class. Each class delegates to a user service or an organization service.
- The user service enforces the transitions and the last-administrator guards. The organization service enforces suspension and reactivation with a protection for administrator organizations.
- Each operation writes an audit record with a transition-specific action type.
- The service and class names are example project code. Copy the pattern, not the names.
