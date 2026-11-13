## Overview

The reCAPTCHA filter is an `OperationCallInterceptor` that checks the token on public-facing built-in operations and refuses the call when the token is missing. A bypass mode serves development and tests. The class names, property names and the check are project code; the interceptor contract is the platform's.

## Implementation Pattern

**Interceptor structure:**
- An OSGi `@Component` with the property `judo.model.name=<ModelName>`, implementing `OperationCallInterceptor`.
- `getOperations()` returns the protected operations explicitly. The default (an empty list) would mean every built-in operation.
- `preCall()` reads the `recaptcha` field from the input `Payload` and refuses the call when it is missing or blank. It returns the payload unchanged otherwise.
- Interceptors do not run for custom, MAPPED or script operations. Operations of that kind need the check in their own implementation.

**Refusing the call:**
- Throw `InterceptorCallBusinessException` (package `hu.blackbelt.judo.runtime.core.dispatcher.behaviours`), the only business-level exception an interceptor may throw. Pass the full name of a modeled fault transfer object as the type, a stable error code (for example `RECAPTCHA_REQUIRED`) and a non-null details map with the message. The dispatcher turns it into HTTP 422 with the `X-Fault` header, and the frontend dialog finds the translation under `faults.<type>.<attribute>`.
- A raw `RuntimeException` does not do this: the dispatcher wraps it as `InternalServerException` and the client sees a generic 500.
- The throw happens inside the operation's transaction, so nothing is written.

**Bypass mechanism:**
- A static final boolean evaluated at class load: the system property `recaptcha.waf.bypass` first, then the environment variable `RECAPTCHA_WAF_BYPASS`.
- When enabled, `preCall()` returns immediately.
- Intended for development, CI and integration test environments only.

**Key design decisions:**
- Token presence only. Full server-side verification can be added as a separate service.
- The `recaptcha` attribute is added to the input transfer object in the model so the frontend sends it.

## Examples

### Example (project code)
- Pattern: protects the registration, validate and verify-invitation operations of the registration transfer object. `preCall()` reads the `recaptcha` field and refuses the call when it is missing. Bypass through the `RECAPTCHA_WAF_BYPASS` environment variable.
- Notable: the original code threw `RuntimeException("Request blocked: reCAPTCHA token required")`, which gives a 500, not a typed error; the entry recommends `InterceptorCallBusinessException` instead. Operations are resolved lazily with `AsmUtils.resolveOperation()` and cached. Whether each protected operation is built-in must be confirmed in the project, because an interceptor never runs for a custom one.
