---
id: recaptcha-precall-interceptor
title: reCAPTCHA Pre-Call Interceptor for Bot Protection
description: Practice that checks for a reCAPTCHA token in the input payload of public operations from a preCall interceptor, with a bypass switch for development; it only tests presence, not validity.
aliases: [captcha check, bot protection interceptor, WAF interceptor, recaptcha token guard]
keywords: [recaptcha, preCall, interceptor, bot, protection, captcha, public, registration, bypass]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: interceptor
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:application/interceptors/src/main/java/hu/blackbelt/mlszksz/platform/interceptors/RecaptchaWafInterceptor.java"]
alternatives: []
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Keep bots away from public operations such as registration by requiring a reCAPTCHA token in the request. This is a convention built on the platform's `preCall` hook; the platform has no captcha support. The observed implementation is incomplete: it checks only that a token is present.

## Practice

### Platform: what the interceptor can and cannot do

- A `preCall` receives the operation and the input payload and may return a (changed) payload; throwing stops the call ([interceptor contract](../../agent-docs/backend/interceptors.md#the-interceptor-contract)). The component needs `@Component(property = { "judo.model.name=<app>" })` ([registration](../../agent-docs/backend/interceptors.md#interceptor-component-registration)).
- `preCall` and `postCall` declare only `InterceptorCallBusinessException`. A business refusal is raised as `InterceptorCallBusinessException` (422 with `X-Fault`), a field rule as `ValidationException` (400). Any other `RuntimeException` becomes a 500 `INTERNAL_SERVER_ERROR` ([exceptions thrown from interceptors](../../agent-docs/backend/error-handling-guide.md#exceptions-thrown-from-interceptors), [HTTP mapping](../../agent-docs/backend/error-handling-guide.md#how-the-runtime-maps-exceptions-to-http)). A refused captcha is therefore better reported with a business error than with a raw `RuntimeException`.
- Interceptors fire only for built-in behaviour operations (create, update, delete, refresh, list, reference operations and so on). Custom, MAPPED and script operations never hit them, so an interceptor on a custom `registration` or `verify` operation would never run; the captcha check must then be coded inside the operation's implementation ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Input validation of an exposed operation's parameters runs without interceptors ([interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)), so a guard on the input of a custom registration call cannot rely on an interceptor.
- Public operations are exposed through an actor that needs no login (an anonymous actor, see [actor types in the screen layout](../../agent-docs/e2e-testing/model-screen-layout.md)); the operation input must declare the token as an attribute (here `recaptcha`) so the payload carries it.

### Practice notes: presence check with a bypass flag

```java
// Example code: RecaptchaWafInterceptor is a class
@Component(property = { "judo.model.name=<app>" })
public class RecaptchaWafInterceptor implements OperationCallInterceptor {

    private static final boolean BYPASS = Boolean.parseBoolean(
        System.getProperty("recaptcha.waf.bypass",
            System.getenv().getOrDefault("RECAPTCHA_WAF_BYPASS", "false")));

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        // resolve only the public operations with AsmUtils, by operation FQN
        return resolvePublicOperations(asmModel);
    }

    @Override
    public Object preCall(EOperation operation, Object parameterPayload)
            throws InterceptorCallBusinessException {
        if (!BYPASS && parameterPayload instanceof Payload payload) {
            String token = payload.getAs(String.class, "recaptcha");
            if (token == null || token.isBlank()) {
                throw new InterceptorCallBusinessException(/* type, errorCode, details, cause, locale */);
            }
        }
        return parameterPayload;
    }
}
```

- The observed implementation threw a raw `RuntimeException` (a 500 for the client); the block above shows the typed form the platform documents instead.
- Bypass via the system property `recaptcha.waf.bypass` or the environment variable `RECAPTCHA_WAF_BYPASS`, for development and tests.
- The operation list names three registration-related operations (register, validate, verify invitation). Check each against the built-in rule above.
- The token is not verified with Google; a real check calls the verification API with the secret key and the token and rejects low scores. Add it before relying on this.

## Rationale

- One class guards several public operations without touching the operations.
- The bypass keeps automated tests and local runs simple.
- Costs: presence-only checking stops only the laziest bots, a forgotten bypass flag disables the guard in production, and a verification call adds network latency and a failure mode.

## Example

A visitor opens the public registration page, solves the captcha in the browser and submits the form with the token in the `recaptcha` field. The interceptor sees a non-blank token and lets the call through; a request without the field is refused. In the test environment the bypass variable is set, so form posts without a token succeed.

## When to avoid

- When the operation is custom, MAPPED or a script: the interceptor never fires; check inside the operation.
- When real bot protection is needed: verify the token with the provider, or put rate limiting or a web application firewall in front of the platform.
- When the environment-variable bypass cannot be guaranteed off in production.

## Related

- [[interceptor-security-filter-validation]] — other interceptor-side request validation
- [[interceptor-global-logging]] — a pass-through interceptor on all built-in operations
- [[two-phase-registration]] — the registration flow this guards
