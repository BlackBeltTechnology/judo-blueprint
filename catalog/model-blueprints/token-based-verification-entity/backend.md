## Overview

The verification flow is implemented by custom operations on the request entity. Each one checks the status and the token before it changes anything. A scheduled cleanup (project practice, see [[osgi-scheduled-background-jobs]]) removes requests that are expired or already decided.

## Implementation pattern

- **Token creation.** The plain token is generated with a secure random source. Only its hash is stored. The plain token goes to the email.
- **Submission.** Submission creates the request in Pending with the hash and an expiry computed from a configured number of minutes.
- **Verification.** The incoming token is hashed and matched against the stored hash. The status must be Pending and the token must not have expired. Success sets Verified and the verified-at time.
- **Approval.** Approval requires Verified. The example creates the organization, the user and the external identity account, then sends a login link and moves the request to Approved.
- **Rejection.** Rejection requires Verified and moves the request to Rejected.
- **Cleanup.** A scheduled job removes expired pending requests and decided requests.
- **Custom operations.** Interceptors do not run for these ([Interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)), so every check is in the operation.
- **Errors.** A failed status or token check raises a modeled fault, which must be declared on the model operation so the generated interface has a `throws` clause (HTTP 422; see [Error handling](../../agent-docs/backend/error-handling-guide.md#modeled-faults)). A bad field value raises the platform validation exception (HTTP 400). The helper classes named below are example project code, not platform API.

## Examples

- Example project code: the registration and user service implementations, a token utility, and a cleanup job.
- The two request entities use the same token helper and the same hash-and-verify logic. They differ only in the names of the token and expiry fields and in the status enumeration.
