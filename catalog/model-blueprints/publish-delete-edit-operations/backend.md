## Overview

Each of the three operations is a custom operation on the transfer object. Custom operations get no operation-call interceptor, so every check and side effect lives in the operation body. The example project keeps the logic in a shared lifecycle service and makes each operation a thin class that delegates to it. The service names and file layout below belong to that example project, not to the platform.

## Implementation pattern

- Put each operation in its own class that implements the generated operation interface and delegates to one service. The service is project code (example: a post lifecycle service); the platform does not provide it.
- Re-read the content inside the operation before changing it. Do not trust the status the client sent.
- Check preconditions in this order: the current status, then the caller's authorization, then the input.
- Modeled business faults are declared on the operation. A failed status check raises the business fault (HTTP 422). Field errors from the input are validation errors (HTTP 400) and come from the framework, not from the operation.
- Write the audit row, if the project keeps one, last, inside the same transaction. A rollback then removes it too.

## Operation rules

- **Publish.** Allowed only from DRAFT. Sets PUBLISHED and the publish time. Side effects such as a feed entry or a notification run after the status change, in the same transaction where the project's services allow it.
- **Delete.** A DRAFT row is removed. A PUBLISHED row gets status DELETED and its side-effect rows (for example a feed entry) are removed. A DELETED row is rejected.
- **Edit.** Allowed only while DRAFT in the example. Copies the editable fields from the input into the entity and keeps the status. Relations that depend on the input (for example capabilities) are replaced inside the same operation.

## Errors and faults

- Declare the business fault on each operation that can raise it, for example a "content not in the right state" fault. Without the declaration the generated interface has no `throws` clause and the build fails; the generated exception is checked and answers HTTP 422 with the `X-Fault` header.
- Do not throw a bare `RuntimeException` for a business rule: the dispatcher turns it into a generic 500. A business rule uses the modeled fault; a bad field value uses the platform `ValidationException` (400).
- Authorization is not done by interceptors here, since they do not run for custom operations; the check is written in the operation.
- Moderation delete (if present) checks the caller's platform role before it changes anything, and notifies the owner after the change.

## Examples

### mlszksz-platform

- Operation classes sit next to the content type's services (example files: `PublishCustomImplementation`, `DeleteCustomImplementation`, `EditRequestCustomImplementation`, `ModerationDeleteCustomImplementation`). Names are project code.
- News, offer and request in the company-admin package each have publish, delete, edit and moderation delete. The announcement in the admin package has publish, delete and edit.
- Delete is the example of the two-branch rule: physical delete for drafts, status change for published items.
