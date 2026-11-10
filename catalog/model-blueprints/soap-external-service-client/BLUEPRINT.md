---
id: soap-external-service-client
title: SOAP External Service Client (WSDL-Generated OSGi Service)
description: "Wraps an external SOAP/WSDL web service behind a domain-oriented OSGi service interface, so custom operations and jobs never touch generated stubs or XML."
aliases: [wsdl client, jax-ws client, cxf client]
keywords: [soap, external, service, client, wsdl, generated, osgi, cxf]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: [external-api-adapter-provider-pattern]
fragment: "none: backend-only"
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Consume an external SOAP service as one reusable OSGi component. The WSDL generates the client stubs at build time; a small interface with business-oriented methods and plain data objects hides them. Callers see neither SOAP operations nor XML.

### Callers see a domain interface

The interface exposes methods named for the business need (for example "rates between two dates for some currencies"), not for the SOAP operations. Its data objects are plain value objects. This is project code; the platform does not provide it.

### The generated stubs stay private

The bundle exports only the package with the interface and the data objects. The generated stubs and the XML parsing live in internal packages.

## Structure

One dedicated module, separate from the model and the application logic:

- The WSDL file and the build configuration that generates the client stubs from it.
- A service interface with domain methods and no OSGi annotations.
- A service implementation registered as an OSGi component (immediate, registered under the interface). At activation it builds the SOAP proxy from the WSDL, the stub class and the endpoint address, and optionally adds request/response logging for debugging.
- Plain data objects, built with a builder, that carry the parsed result.
- Parsing code that turns the response (often an XML string inside the SOAP reply) into those data objects, including locale-aware number and date handling.

The implementation component is wired the same way as any other project service. See [custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern) for the platform rule on registering OSGi components. Custom operation implementations and scheduled jobs then reference the service interface. The platform's DAOs and generated operations are unaffected.

## Constraints

- Only the interface and data objects are exported from the bundle.
- The interface carries no OSGi annotations. Only the implementation is a component.
- The model is not involved. There is no entity, transfer object or operation for the SOAP client itself. The business operations that use it are ordinary custom operations.
- Interceptors do not protect custom operations, so any permission check before an external call belongs inside the calling operation ([interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Endpoint address and credentials are configuration, not constants. The sample project hard-codes the endpoint; treat that as a weakness.
- A failing remote call must be translated into a business error or a safe fallback by the caller. Modeled faults must be declared in the model to be thrown from a custom operation ([error handling](../../agent-docs/backend/error-handling-guide.md#modeled-faults)).

## Variations

- **Database first, SOAP fallback.** The service reads stored results first and calls the remote service only for missing ones. See [[soap-client-integration]].
- **Hand-written JAXB client.** For a small payload, a JAXB-bound client replaces the generated stubs. See [[jaxb-external-api-client]].
- **Several providers.** When more than one external platform supplies the same data, put them behind a provider service instead. See [[external-api-adapter-provider-pattern]].
- **Scheduled consumer.** A scheduled job calls the service on a timer and stores the result in an entity. See [[osgi-scheduled-background-jobs]].

## When to use

- The external system offers only a WSDL contract.
- More than one operation or job needs the same remote data.
- The generated stub types must not leak into the rest of the application.

## When to avoid

- The remote service is plain REST or JSON. Use a small HTTP client class instead.
- Only one operation calls it once. A private helper in that operation is enough.
- The WSDL is unstable or unavailable at build time. Wrap a hand-written client instead.

## Related

- [[exchange-rate-entity]] — the entity that stores rates fetched through such a service
- [[soap-client-integration]] — the best-practice version, with the fallback strategy
- [[jaxb-external-api-client]] — hand-written client without generated stubs
- [[external-api-adapter-provider-pattern]] — several providers behind one interface
- [[osgi-scheduled-background-jobs]] — scheduled callers of the service
- [[custom-operation-osgi-component]] — how the calling operation is registered
