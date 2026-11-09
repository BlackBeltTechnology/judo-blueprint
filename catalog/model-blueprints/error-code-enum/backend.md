## Backend guidance

### Declare the business error on each operation that can raise it

A business failure is a modeled fault. The operation declares the general business error as its fault parameter. Without that declaration the generated operation interface has no checked exception for it, and throwing it does not compile. Declare it on every operation that can fail for a business reason.

### Throw through one factory, never inline

Build the business error and wrap it in the business exception in one factory of the application. Operations call the factory, and do not construct the error object themselves. This keeps the codes and the translation keys in one place.

- The factory takes the code and a message key or text, and builds the error object and the exception.
- Overloads can take the enumeration member or a string code, depending on the variant chosen.
- The factory is project code, not platform API. Copy the pattern, not the class name.

### Keep the failure a business error, not a 500

- A business rule (not found, not allowed, already exists, wrong state) is thrown as the business error with its code. The client then gets the business answer.
- An external failure (a connection to another system is down, credentials are missing, a result is unavailable) is wrapped in the same business error with a code, and the cause is logged. Do not let a raw runtime exception escape: the client would see a server error.
- A business invariant is never an illegal-state runtime exception. It is a business error with a code.
- A typed business error caught and re-thrown as a generic runtime exception turns into a 500. Let it pass unchanged.

### Interceptors wrap, they do not invent

An interceptor runs only for built-in operations. When a rule must stop a built-in operation, the interceptor throws the interceptor wrapper, not a generated fault class (which is checked and cannot be thrown there). The wrapper carries the fault type, the error code, and the details. Use the fault's full name as the type, so the client's fault dialog finds its translations.

### Field errors are not business errors

A problem with one field is a field validation error with the attribute name as its location. Put a business error on the operation only for failures that are not about one field.

### Readiness checks return a list

For a check that the user runs before submitting (is this ready to close), return the list of every missing item in one result. Reserve the business error for a real rule violation.

## Examples

### mlszksz-platform

- The project uses plain string codes with a general business error object, and no enumeration. Codes are constants in application code.
- Authorization checks and validation checks in custom operations raise the business error with a code.

### indamedia-adtrack

- The project uses an enumeration of twelve codes (lookups, credentials, integration, platform support) in the model.
- The factory takes the enumeration member and a localized message from the translation service.
- The platform provider raises the platform-not-supported and not-implemented codes when it dispatches on the platform enumeration.

### park-here

- The project uses an enumeration of eight codes and a business error object where code and message are both required.

### ubives

- The project uses an enumeration of about twenty codes for identity management, and the business error object uses `code` rather than `errorCode`.
- External identity-provider failures have their own codes, separate from the domain codes.

### workflow-poc

- The project uses a domain-scoped enumeration with one code for workflow declaration validation, which grows as rules are added.

### trivia

- The project uses an actor-scoped enumeration of five codes in the player namespace, for quiz state preconditions.
