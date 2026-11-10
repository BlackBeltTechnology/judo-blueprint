## Backend guidance

### Status changes are custom operations

A change of status is a custom operation on the content entity: publish, delete, and optionally expire or moderate. Each operation sets the status and runs its side effects in one place. Interceptors do not run for custom operations (platform behaviour), so the status rules must sit in the operation.

- Publish sets the status to PUBLISHED and records the publication time, then runs the publish side effects, such as creating feed entries or notifications.
- Delete sets the status to DELETED. It is a soft delete: the row stays, so the content can be listed as deleted and audited.
- Each operation checks the current status first. A transition from DELETED back to PUBLISHED is a rule the operation must enforce, not something the enumeration prevents. A refused transition is a business fault, which the operation must declare in its `faults` so the generated interface has a matching `throws` clause.

### Put the transition in a shared service

Operations on different content types should call one shared service that owns the status field, the timestamps and the side effects. The operations stay thin: they check permission, call the service, and return.

### Log each transition

Write one audit entry per status change, inside the same transaction as the change. An audit failure should follow the rule in [[safe-failure-pattern]]: log it and keep the business change, unless the audit is a legal requirement.

### Moderation needs its own role check

A moderation delete is a status change made by a platform administrator, not by the content owner. Check the role inside that operation before the change, and send any notifications only after the change succeeds.

### Project code, not platform API

The example project implements these transitions with its own service classes, operation classes and audit service (example project code). Those names are project code. Copy the pattern, not the names.

## Examples

### mlszksz-platform

- Two enumerations: one for posts with the extra EXPIRED and PENDING_REVIEW values, and one for announcements with the three core values.
- Thin operation classes for publish, delete, edit and expire delegate to a shared post service or announcement service.
- Each transition writes one audit entry. Moderation delete checks the platform-admin role first.
