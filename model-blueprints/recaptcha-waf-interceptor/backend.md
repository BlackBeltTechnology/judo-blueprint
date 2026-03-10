## Overview

Implements a reCAPTCHA Web Application Firewall (WAF) as an `OperationCallInterceptor` that validates reCAPTCHA tokens on public-facing operations, blocking requests without valid tokens. Supports bypass mode for development/testing.

## Implementation Pattern

**Interceptor structure:**
- `@Component(property = { "judo.model.name=<ModelName>" })` implementing `OperationCallInterceptor`
- `getOperations()` returns the specific public-facing operations to protect (e.g., registration, verification)
- `preCall()` extracts the `recaptcha` field from the `Payload` parameter and blocks if missing/blank

**Bypass mechanism:**
- Static final boolean evaluated at class load: checks system property `recaptcha.waf.bypass` first, then environment variable `RECAPTCHA_WAF_BYPASS`
- When bypass is enabled, `preCall()` returns immediately without validation
- Useful for development, CI/CD testing, and integration test environments

**Key design decisions:**
- Token presence check only (not server-side verification) -- the WAF layer blocks trivially missing tokens; full reCAPTCHA verification can be added in a separate service
- Throws `RuntimeException` on missing token, which the JUDO dispatcher translates into an appropriate error response
- The `recaptcha` field must be added to the transfer object in the model for the frontend to include it in the payload

## Examples

### mlszksz-platform
- Key files: `interceptors/RecaptchaWafInterceptor.java`
- Pattern: Protects `RegistrationTransfer#registration`, `RegistrationTransfer#validate`, and `RegistrationTransfer#verifyUserInvitation` operations. In `preCall()`, extracts `recaptcha` field from payload and throws `RuntimeException("Request blocked: reCAPTCHA token required")` if missing. Bypass via `RECAPTCHA_WAF_BYPASS` env var.
- Notable: The bypass check uses `System.getProperty()` with `System.getenv()` fallback, evaluated once at class load time as a `static final boolean`. Operations are resolved lazily via `AsmUtils.resolveOperation()` and cached in a field.
