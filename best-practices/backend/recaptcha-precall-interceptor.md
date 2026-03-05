---
id: "recaptcha-precall-interceptor"
title: "reCAPTCHA Pre-Call Interceptor for Bot Protection"
domain: "backend"
category: "interceptor"
score: 13.1
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - mlszksz-platform
---
## Description

A pre-call interceptor that validates reCAPTCHA tokens on public-facing operations (e.g., registration endpoints) to prevent bot attacks. The interceptor checks for a `recaptcha` field in the operation payload and blocks requests with missing or blank tokens. Supports a configurable bypass mode via system property or environment variable for development and testing.

## Structure

```java
@Component(property = { "judo.model.name=AppName" })
public class RecaptchaWafInterceptor implements OperationCallInterceptor {

    private static final boolean BYPASS_ENABLED =
        Boolean.parseBoolean(System.getProperty("recaptcha.waf.bypass",
            System.getenv().getOrDefault("RECAPTCHA_WAF_BYPASS", "false")));

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        // Target registration/public operations only
        return Stream.of(
            "App.services.registration.Transfer#registration",
            "App.services.registration.Transfer#validate"
        ).map(asmUtils::resolveOperation).map(Optional::orElseThrow).toList();
    }

    @Override
    public Object preCall(EOperation operation, Object parameterPayload) {
        if (BYPASS_ENABLED) return super.preCall(operation, parameterPayload);

        if (parameterPayload instanceof Payload payload) {
            String token = payload.getAs(String.class, "recaptcha");
            if (token == null || token.isBlank()) {
                throw new RuntimeException("Request blocked: reCAPTCHA token required");
            }
        }
        return super.preCall(operation, parameterPayload);
    }
}
```

Configuration:
- System property: `recaptcha.waf.bypass=true`
- Environment variable: `RECAPTCHA_WAF_BYPASS=true`

## Examples

### mlszksz-platform
`RecaptchaWafInterceptor` targets 3 registration operations: registration, validate, verifyUserInvitation. Checks for `recaptcha` field in Payload. Bypass mode enabled via system property or env var for development. Token presence check only (does not verify with Google API). Throws RuntimeException on missing token.

## Trade-offs

- Pros: Protects public endpoints from bot abuse, zero-overhead bypass for development, transparent to operations
- Cons: Only checks token presence (not validity with Google API), throws raw RuntimeException instead of typed error, bypass flag could be accidentally enabled in production
- Alternative: Server-side Google reCAPTCHA API verification, rate limiting, or Web Application Firewall (WAF)

## Related Patterns

- interceptor-security-filter-validation
- interceptor-global-logging
- two-phase-registration
