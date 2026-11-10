## Backend guidance

### Keep the Keycloak extension separate

Put the magic-link authenticator, its action token handler and its REST endpoint in one extension module that is deployed into the Keycloak server. Keep the client module, which calls the administration interface, in another module. The two have different runtimes and different class loaders.

### Set up the realm once, with retries

Keep it consistent with what the platform generates from the model: the realm and one client per actor type with a `realm` annotation, the client named after the actor FQN with dots replaced by dashes. Configure the extra realm settings on startup: the email settings, the browser flows, the native app client, the passkey policy and the branding. Run the setup on a background thread with exponential backoff, so a Keycloak that starts late does not stop the application. Log every failed attempt.

```java
Retry retry = Retry.of("realm-setup", RetryConfig.custom()
    .maxAttempts(5)
    .waitDuration(Duration.ofSeconds(2))
    .build());
```

### Let the platform map the principal to the actor

This entry only changes how a user proves who they are. The platform still maps the validated token to an actor by its claims; the actor is derived from the token's `azp` claim (dashes become dots and the result must equal an actor FQN). A client with another name, such as a separate native-app client, must be whitelisted through the acceptable-clients setting, and an ambiguous client-to-actor mapping is rejected. Do not add a second mapping of your own.

### Wrap the administration calls behind a service

Expose user creation, the magic-link request and the forgot-password email as services. Callers depend on the service interface, not on the Keycloak client. The service holds the realm name, so callers do not pass it.

### Use the class loader the client needs

In a bundle runtime, the JAX-RS client needs a class loader that can see both the bundle and the system libraries. Build the Keycloak client with that combined loader.

### Mark passkey registration as a required action

To register a passkey for a user, add the passwordless WebAuthn registration as a required action on the user, then issue a magic link. The link opens a browser session that starts the registration.

### Do not put the magic link in logs

A magic link is a credential. Do not log it, and do not return it to a caller that did not request it.

### Project classes are not platform API

The client, the activator, the realm manager, the retry helper and the service implementations in the example are example project code, not JUDO platform API. Copy the approach, not the class names.

## Examples

### mlszksz-platform

- The client module runs the realm setup at startup with retries, then serves the user and link services.
- The extension module adds the magic-link authenticator and the action token that starts a session.
- The native app browser flow is passkey first. The password form is a fallback sub-flow.
- Passkey registration adds the required action, then requests a magic link to open the registration in a browser.
