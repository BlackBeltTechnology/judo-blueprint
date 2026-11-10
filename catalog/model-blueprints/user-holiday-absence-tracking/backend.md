## Overview

Holiday creation and deletion are custom operations. They delegate to a shared holiday service that checks the dates and the overlap, and that cancels any reservations that the new range covers. A calendar service combines public holidays with the stored single-day overrides.

## Implementation pattern

- **Creation flow.** The operation resolves the user, checks that the current actor may act for that user, validates the dates and the overlap, then creates the holiday. Each panel that can create a holiday runs this same flow.
- **Validation.** The service rejects a range whose end is before its start, a start in the past, and an overlap with an existing holiday of the same user. The overlap check is a query attribute on the user.
- **Reservation cancellation.** Creation cancels the active reservations (other than the guest type) inside the new range, then creates the holiday. Both writes are in one transaction.
- **Preview.** A separate query lists the reservations inside a proposed range, so the UI can warn before the user confirms.
- **Deletion.** The delete operation checks that the holiday belongs to the current user, or that the actor has admin permission, before it deletes.
- **Calendar.** The calendar service decides whether a day is a working day. It combines the public calendar (computed for each year, including the moveable feasts) with stored single-day overrides. The override list is validated so that one day cannot have two overrides.
- **Interceptors.** Interceptors run only on built-in operations ([Interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). These are custom, so each carries its own checks, including the actor-for-user permission check, which is project practice.
- **Errors.** A rule violation is a modeled fault, declared on the operation in the model (HTTP 422; see [Error handling](../../agent-docs/backend/error-handling-guide.md#modeled-faults)). A bad field value is the platform validation exception (HTTP 400). The service and helper classes named below are example project code, not platform API.

## Examples

### park-here

- Key files (example project code): the holiday operations on the panels, the delete operation on the holiday, the preview query, and the holiday and date services.
- All panel creation operations follow the same flow and delegate to the same holiday service.
- The date service computes the public calendar, including the Easter-based moveable holidays, and merges it with the stored overrides.
