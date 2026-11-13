## Frontend guidance

### Register one error handler hook

Create the hook in the customizer's registration function, and register it under the platform's error-handler interceptor key. The hook exposes two callbacks: a predicate that says whether it handles an error, and a handler that shows the message.

### Match the business error by status

The predicate checks for HTTP 422, the status of a business error. Other statuses are not handled here. Use one shared detection callback for the predicate and the handler, so the two cannot disagree.

### Read the message from the body

The 422 response body is keyed by the fault's full name (a `code` key follows it), and the entry for the fault carries its attributes. Take the first key's `message` attribute (present only if the fault defines one) and show it. If there is no message, let the generated fault dialog handle the error.

### The batch dialog is not covered

The generated batch/CRUD dialog builds fault messages from the response itself, so the interceptor does not replace them there. Test both paths.

### Show a short snackbar

Show the message as an error snackbar with an automatic hide (about three seconds). Use the translation hook for any fixed text around it.

### Log for debugging

Log the intercepted error to the console during development, so a missing message is easy to trace.

## Examples

### Variant seen in practice

- The hook intercepts every 422 and shows the first error's message as a three-second snackbar, instead of the generated fault dialog.
- Its predicate and handler share the same detection callback.
- The backend's business error type is a guard name rather than the business fault's full name (application code). The generated fault dialog therefore finds no translation for it, and the snackbar shows the message from the body instead. Using the fault's full name would let the generated dialog work.

### Second variant seen in practice

- The same hook structure, with the same shared detection callback, confirming the pattern is stable across projects.

### Third variant seen in practice

- The same hook in a React frontend: a predicate matching HTTP 422, a handler that reads the first body key's `message` and shows a three-second error snackbar. The generated default hook already has this shape; the application keeps it.
