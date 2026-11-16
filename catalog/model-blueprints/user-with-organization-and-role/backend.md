## Overview

The user lifecycle is handled by a user service. It creates the user with an organization and a role, changes the status, and handles invitations. An authentication interceptor (platform extension point, see [Authentication guide](../../agent-docs/backend/authentication-guide.md)) records the last login on each authentication event.

## Implementation pattern

- **Creation.** The service creates the user with the organization association and the role. It then provisions the external identity account.
- **Status transitions.** Suspend and activate each check the current status first. Suspension also checks that the last administrator in the scope is not removed. The example project models no user deactivate operation; a role change (`changeRole`) is the other lifecycle operation (whether it guards the last administrator: *verify*).
- **Last-administrator guards.** The guard counts the active users with the administrator role, both platform-wide and inside the organization. The count runs as a query.
- **Invitations.** An invitation stores a hashed token with an expiry and moves through a pending and then a verified state.
- **Interceptor.** The authentication interceptor updates the last-login time and writes an audit entry. It is called on authentication events, not on the custom operations.
- **Custom operations.** Interceptors do not run for custom operations ([Interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)). Activate, suspend, change role, visibility change, user creation and invitation are custom, so each carries its own checks.
- **Errors.** A rule violation is a modeled fault, declared on the operation in the model (HTTP 422; see [Error handling](../../agent-docs/backend/error-handling-guide.md#modeled-faults)). A bad field value is the platform validation exception (HTTP 400). The service and helper classes named below are example project code, not platform API.

## Examples

- Example project code: the user service and its implementation, the authentication interceptor, and the suspend and change-role operations on an admin view.
- The last-administrator guards are the main rule. They are the reason the role check runs in the organization context.
