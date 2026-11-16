## Backend guidance

The notification rows are written and retried by project code. The platform does not deliver push or email on its own.

### Delivery code writes the row first

A delivery service creates the Notification row with status PENDING, then sends, then updates the status to SENT or FAILED. As project practice, write the row in the same transaction as the business change that caused it, or the message can be sent without a record.

### Retry runs from a scheduled job

A scheduled job reads FAILED rows and stuck PENDING rows, increments the retry count and sends again, with a back-off between attempts and a maximum number of retries. The job is project code, not a platform feature.

### Custom operations and interceptors

Custom operations that mark rows as read or delete them must check that the caller is the notification's user. Interceptors run only on built-in operations and may only throw InterceptorCallBusinessException, so the ownership check belongs in the custom operation, which is also never intercepted.

### Services are project code

Helpers such as a push sender or a retry scheduler are example project code. Name them for the project and keep the platform rules (interceptors, custom operations) separate from them.
