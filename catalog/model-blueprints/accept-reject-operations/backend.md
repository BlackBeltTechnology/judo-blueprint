## Backend guidance

### Put the status check in the custom operation

Accept and reject are custom operations. Interceptors run only for built-in operations (create, update, delete, list and similar), so no interceptor checks the transition or guards the status. The custom implementation must read the current status, refuse any value other than pending, and then change the status.

- Read the current status first. If it is not pending, throw the modeled business fault for an invalid transition.
- Change the status and the decision time in the same operation call, so both are written together.
- Reject takes the RejectInput. Pass the reason to the service or the audit call; do not store it on the status enumeration.

### Declare the fault on the operation

A business fault is a transfer object declared as a fault parameter of the operation. The generated interface then throws the matching checked exception only for that operation. Without the declaration, throwing the exception does not compile.

- Use a modeled fault for an invalid transition. The client receives HTTP 422 with the fault type in the X-Fault header, and the generated frontend shows its fault dialog.
- Platform errors such as ValidationException (400) and NotFoundException (404) are unchecked and are not modeled faults. They come from the platform, not from the model. Use ValidationException for a wrong input value (for example a missing reason) and the modeled fault for the business refusal.

### Keep the logic in a service

Put the transition and its checks in a service class, and let the two operations call it. The operations stay thin. Reject validates the same preconditions as accept and changes only the status.

- The service is project code. Its name and layout belong to the example project, not to the platform.
- Log an audit record after the transition, from the same operation (project practice). See [[audit-log-entity]] for the record shape.

### Interceptors cannot guard these operations

An interceptor does not run for accept or reject, because they are custom operations. If the rule must hold for every path that can decide a request, enforce it in the operation and in the service. An interceptor can still guard the built-in update of the status, if the model exposes one. It cannot throw the generated checked fault; it raises its refusal as InterceptorCallBusinessException, which also reaches the client as 422.

## Examples

### mlszksz-platform

- Two pairs of accept and reject operations: one for the registration request and one for the user invitation request. Each pair is a thin custom operation class that calls a shared service.
- The registration service checks that the request is verified, creates the organization and user, and sends an approval email. The invitation service checks the organization access rule and then creates the user.
- Each accept and reject writes an audit record with the action type and the email.
- The service and class names are example project code. Copy the pattern, not the names.
