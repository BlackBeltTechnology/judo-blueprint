---
id: error-code-enum
title: Error Code Enumeration with Business Error Transfer Object
description: "A way to name the business errors an application can raise: an enumeration of error codes, or plain string codes, carried by one general business error object, and thrown through a single factory."
aliases: [error code enum, business error code vocabulary]
keywords: [error, code, enumeration, business, fault, transfer, object, factory, i18n]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:indamedia-adtrack", "project:park-here", "project:ubives", "project:workflow-poc", "project:trivia", "project:mlszksz-platform", "status:established"]
category: pattern
status: established
projects: [indamedia-adtrack, park-here, ubives, workflow-poc, trivia, mlszksz-platform]
evidence: ["indamedia-adtrack:unrecorded", "park-here:unrecorded", "ubives:unrecorded", "workflow-poc:unrecorded", "trivia:unrecorded", "mlszksz-platform:unrecorded"]
alternatives: [validation-exception-hierarchy, typed-exception-error-handling]
fragment: error-code-enum
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-09
---
## Intent

Give every business failure a stable, named code and a message, so that the client can show the right text and the backend keeps one vocabulary of failures. A business failure is a rule the user can break (not found, not allowed, already exists, not in the right state), not a field error and not a crash.

### The code is the vocabulary, the message is for people

The code is what the program branches on. The message is text for the user, and is translated. A client never parses the message to decide what happened.

### One general error object carries the code

One business error object with a code and a message is thrown across the operation boundary. It is declared as the operation's fault, so the generated client knows about it. Field errors stay with the field validation mechanism.

## Structure

Three parts. An error code vocabulary, either a modeled enumeration (one member per error) or plain string constants in code. One business error object, a transfer object that is not mapped to an entity, with the code and the message. A factory in the application that builds the error object and wraps it in the business exception, so that no operation builds it inline.

## Constraints

- Every business failure an operation can raise is declared on that operation. A failure that is not declared cannot be thrown as a checked error.
- The code is stable. A renamed code breaks any client that branches on it; add a new code instead.
- Messages come from the application's translation service, not from string literals in operations.
- A business failure is raised as a business error. It must not escape as a raw runtime exception, because the client would see a server error (500) instead of the business answer.
- Field-level errors use the field validation mechanism with the attribute name as their location. They are not business errors.

## Variations

- **Modeled enumeration.** The codes are an enumeration in the model, one member per error, with ordinals. Type-safe, and the vocabulary is part of the model. Used by projects that want the codes in the API contract.
- **Plain string codes.** The business error object has a string code and a message, and the codes are constants in application code. Simpler: no enumeration to maintain, and a new code needs no model change. Used by projects that keep the vocabulary in code.
- **Domain-scoped enumeration.** A separate enumeration per domain, such as workflow declaration validation, instead of one for the whole application.
- **Actor-scoped enumeration.** The enumeration and the error object live in the namespace of one actor (for example a player), so that the codes belong to that actor's API.
- **Direct construction.** The service constructs the business error object itself and throws it, with no factory. Works, but the codes end up spread across the code base.

## When to use

- The client must tell apart several failures of one operation and show a different message for each.
- Several operations share the same few failures (not found, not allowed).
- The application needs one place to see and translate all its business failures.

## When to avoid

- There is one kind of failure, and a plain message is enough.
- The failure is about one field. Use the field validation mechanism with the field as location.
- The application is too small to justify a factory. Construct the error directly, but keep the code strings in one class.

## Related

- [[error-handler-interceptor-customization]] — the frontend hook that shows the business error message from a 422 response
- [[validation-exception-hierarchy]] — the separate field-level validation mechanism
- [[typed-exception-error-handling]] — typed exception handling in the backend
