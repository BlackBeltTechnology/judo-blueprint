---
id: recaptcha-waf-interceptor
title: reCAPTCHA WAF Interceptor for Public Operations
description: "An OperationCallInterceptor that refuses calls to public-facing built-in operations when the reCAPTCHA token in the input is missing, with a bypass for development and tests."
aliases: [recaptcha interceptor, bot filter]
keywords: [recaptcha, waf, interceptor, public operations, bot protection, InterceptorCallBusinessException]
tags: ["domain:backend", "layer:backend", "project:mlszksz-platform", "status:single-project"]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:application/interceptors/src/main/java/hu/blackbelt/mlszksz/platform/interceptors/RecaptchaWafInterceptor.java"]
alternatives: []
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Block bot traffic on operations that anonymous users can call, such as registration or invitation checks, by requiring a reCAPTCHA token in the input. The check is a cross-cutting rule, so it is one interceptor and not a line in every operation.

### Only a presence check

The interceptor checks that a non-blank token is present. It does not call the reCAPTCHA service. Full verification belongs in a separate service that the interceptor or the operation may call later.

### Refusal is a business error

A missing token refuses the call with `InterceptorCallBusinessException`, the only business-level exception an interceptor may throw. The client then gets HTTP 422 with the `X-Fault` header and an error code. A bare `RuntimeException` would be wrapped as `InternalServerException` and show up as a generic 500.

### A bypass for development

A system property or an environment variable turns the check off for development, CI and integration tests.

## Structure

The platform part is an `OperationCallInterceptor` registered as an OSGi component for the application model. It lists the operations it protects and reads the token in `preCall`. The model part is one attribute (the token) on the input of each protected operation, so the frontend sends it in the payload. The bypass flag and the check are project code.

## Constraints

- Interceptors fire only for built-in operations (create, update, delete, list, validate calls and the like). Custom, MAPPED and script operations never reach an interceptor, even when listed. A public operation that is custom must check the token inside its own implementation, or call the same check helper.
- The interceptor may throw only `InterceptorCallBusinessException`. Give it the full name of a modeled fault transfer object as the type, so the frontend fault dialog can translate the message, and a stable error code. Details must not be null.
- The exception is thrown inside the operation's transaction, so the call is rolled back.
- The token attribute must exist on the input transfer object in the model, or the payload has no value to read.
- The bypass flag must never be on in production. It is read once at class load, so a change needs a restart.
- An empty operation list means all built-in operations, so list the protected operations explicitly.

## Variations

- **Server-side verification.** After the presence check, call the reCAPTCHA verify endpoint through an injected service and refuse on a failed score.
- **Check in the custom operation.** When the public operation is custom, put the same check at the top of its implementation.
- **Edge filtering.** A web application firewall in front of the application blocks bots before they reach the backend. Use it as well, or instead.

## When to use

- Anonymous users can call built-in operations that create data, such as self-registration.
- Bot traffic is a real risk and a client token is enough as a first filter.

## When to avoid

- The protected operations are custom, MAPPED or script operations. An interceptor never runs for them.
- The token must be verified against the reCAPTCHA service. Add a verification service, because a presence check does not stop a forged token.

## Related

- [[error-handler-interceptor-customization]] — how interceptor errors reach the client
- [[operation-call-logging-interceptor]] — another operation-call interceptor with an operation list
- [[invitation-with-key-based-acceptance]] — a public invitation flow that such a filter protects
