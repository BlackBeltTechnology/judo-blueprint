## Frontend guidance

### Register one error handler hook

Create the hook in the customizer's registration function, and register it under the platform's error-handler interceptor key. The hook exposes two callbacks: a predicate that says whether it handles an error, and a handler that shows the message.

### Match the business error by status

The predicate checks for HTTP 422, the status of a business error. Other statuses are not handled here. Use one shared detection callback for the predicate and the handler, so the two cannot disagree.

### Read the message from the body

The response body is keyed by the fault's type name, and each entry carries a message. Take the first key's message and show it. If there is no message, let the generated fault dialog handle the error.

### Show a short snackbar

Show the message as an error snackbar with an automatic hide (about three seconds). Use the translation hook for any fixed text around it.

### Log for debugging

Log the intercepted error to the console during development, so a missing message is easy to trace.

## Examples

### rackinspect

- The hook intercepts every 422 and shows the first error's message as a three-second snackbar, instead of the generated fault dialog.
- Its predicate and handler share the same detection callback.
- The backend's business error type is a guard name rather than the business fault's full name. The generated fault dialog therefore finds no translation for it, and the snackbar shows the message from the body instead. Using the fault's full name would let the generated dialog work.

### park-here

- The same hook structure, with the same shared detection callback, confirming the pattern is stable across projects.
