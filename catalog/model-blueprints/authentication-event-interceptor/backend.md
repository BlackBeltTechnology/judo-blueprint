## Backend guidance

### Use the authentication interceptor, not the operation interceptor

The platform has two interceptor types. The authentication interceptor runs in the authentication pipeline and sees the principal lookup. The operation call interceptor runs around built-in operations only. Custom operations never get an operation interceptor, so login work must use the authentication interceptor.

- Implement the authentication interceptor interface in a component registered with the model name.
- Accept every operation in the suitability check and filter inside the authenticate method, so the login work is decided in one place.
- Compare the operation name with the principal operation name. Return the token unchanged for every other operation.

### Read the claims defensively

Token claims can be missing. Read the email first, and skip the work when it is absent. Build the display name from the given and family name only when present.

### Create the row once

On first login, check for an existing row by email and create one only if none exists. Guard the check and the insert with one lock or one unique constraint, so two concurrent first logins do not create two rows.

### Keep login from failing

Wrap each side effect in a try and catch block. Log the error with the email and the operation name, and return the token. Do not rethrow: a failed audit write or a failed timestamp update must not stop the user from signing in.

- Use a short field mask when reading the user, so only the needed columns are loaded.
- Assign roles only from a configured list, read when the component is activated.

## Examples

### mlszksz-platform

- One login interceptor filters for the principal operation. It finds the user by email, updates the last-login time and writes a login entry through the project's audit service.
- The interceptor uses a short field mask when it reads the user. Its whole body is in a try and catch block, so a failure does not stop the login.

### indamedia-adtrack

- A login interceptor creates the user on first login from the email and name claims. It assigns the admin flag from a comma-separated list of administrator emails in the component properties.
- A lock around the check and the insert prevents duplicate rows under concurrent logins. This variant has no audit service.
- The service and class names are example project code. Copy the pattern, not the names.
