## Backend guidance

### Use the authentication interceptor, not the operation interceptor

The platform has two interceptor types. The authentication interceptor runs in the authentication pipeline and sees the principal lookup. The operation call interceptor runs around built-in operations only. Custom (SDK-implemented), mapped and script operations are never intercepted by it, and its `postCall` runs in registration order, not reverse. Login work belongs in the authentication interceptor.

- Implement `AuthenticationInterceptor` (`getName`, `isSuitableForOperation`, `authenticate`) in a component with the property `judo.model.name=<app>`. Without it the interceptor is not bound to the model.
- Accept every operation in the suitability check and filter inside the authenticate method, so the login work is decided in one place.
- Check that the operation FQ name ends with `#_principal`. Return at once for every other operation. The `authenticate` method returns nothing; it cannot change the token.
- The interceptor runs before the framework resolves the actor row, so a row inserted here is found by the lookup of the same call.

### Read the claims defensively

Token claims arrive in the `attributes` map (standard Keycloak names: `email`, `preferred_username`, `given_name`, `family_name`, `sub`). They can be missing. Read the email first, and skip the work when it is absent. Build the display name from the given and family name only when present.

### Create the row once

On first login, check for an existing row by email and create one only if none exists. Guard the check and the insert with one lock or one unique constraint, so two concurrent first logins do not create two rows. The platform guide's example uses a `synchronized` block on a lock object. It also names an alternative: no lock, and the unique-constraint violation is logged and swallowed. A lock in the component covers one JVM only, so keep a unique constraint when several nodes run.

### Keep login from failing

Wrap each side effect in a try and catch block. Log the error with the email and the operation name, and return the token. Do not rethrow (common practice): a failed audit write or a failed timestamp update must not stop the user from signing in.

- Use a short field mask when reading the user, so only the needed columns are loaded.
- Assign roles only from a configured list, read when the component is activated.

## Examples

### Variant seen in practice

- One login interceptor filters for the principal operation. It finds the user by email, updates the last-login time and writes a login entry through the application's audit service.
- The interceptor uses a short field mask when it reads the user. Its whole body is in a try and catch block, so a failure does not stop the login.

### Second variant seen in practice

- A login interceptor creates the user on first login from the email and name claims. It assigns the admin flag from a comma-separated list of administrator emails in the component properties.
- A lock around the check and the insert prevents duplicate rows under concurrent logins. This variant has no audit service.
- The service and class names are application-specific. Copy the pattern, not the names.
