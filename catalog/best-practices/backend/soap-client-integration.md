---
id: soap-client-integration
title: SOAP Client Integration with CXF in an OSGi Service
description: "An external SOAP service is wrapped in an OSGi component that builds a CXF JAX-WS proxy, parses the XML reply and falls back from a database cache to the remote call."
aliases: [CXF SOAP client, JaxWsProxyFactoryBean, JAX-WS client]
keywords: [soap, cxf, jax-ws, wsdl, external service, exchange rate, locale decimal, database cache]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: integration
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/mnb-soap-client/src/main/java/hu/mnb/webservices/osgi/ExchangeRateServiceImpl.java", "rackinspect:application/app/src/main/java/hu/blackbelt/rackinspect/rackinspect/custom/rackinspect/_default_transferobjecttypes/entities/exchangerate/UpdateExchangeRatesCustomImplementation.java"]
alternatives: [jaxb-external-api-client]
related: [quartz-scheduled-job, custom-operation-osgi-component, jaxb-external-api-client, soap-external-service-client]
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

An application must read data from a third-party SOAP web service (here: daily exchange rates of a national bank). The call is isolated in one OSGi service with a domain-shaped interface. The service hides the CXF proxy, parses the XML reply and prefers a locally stored copy over a remote call.

## Practice

### Platform base

- The agent-docs describe no SOAP or JAX-WS client support, so everything about the client is a convention built on plain CXF. The only platform rules used are: the implementation is an OSGi Declarative Services component, and other components inject it with `@Reference` ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)).
- The platform itself ships a generator for REST clients (an OpenAPI client for OSGi, see [generator plugins](../../agent-docs/deployment/generator-plugins.md)); it does not cover WSDL. For XML over HTTP without a WSDL see [[jaxb-external-api-client]].
- Interceptors do not fire for custom operations or for calls made by a service, so a permission check on the caller side belongs in the operation or the service ([which operations are intercepted](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- Failures of the remote call reach the caller as ordinary Java exceptions. A business-level refusal must be mapped to a modeled fault the operation declares ([modeled faults](../../agent-docs/backend/error-handling-guide.md#modeled-faults)); a raw runtime exception becomes a generic server error.

### Practice notes: a cached SOAP service

This layer is a convention built on the platform, not a platform feature:

- Put the client in its own module with a plain Java service interface and domain DTOs. Only the implementation carries `@Component`; the generated SOAP stubs stay internal.
- Create the proxy with `JaxWsProxyFactoryBean` (service class, address) and add CXF logging in and out interceptors for debugging. Note these are CXF interceptors, unrelated to JUDO operation interceptors.
- Parse the XML reply into DTOs yourself and normalise locale-specific formats, for example a decimal comma, with an explicit locale rather than the JVM default.
- Look in the database first and call the remote service only when the data is missing. A scheduled job ([[quartz-scheduled-job]]) fills the table once a day, so user requests rarely reach SOAP.
- Treat the external service as unreliable: time out, log, and surface a clear error when neither cache nor remote has the answer.

```java
// Example code: SoapServicePort is generated from the WSDL, ENDPOINT_URL and Rate are types
@Component(immediate = true, service = ExchangeRateService.class)
public class ExchangeRateServiceImpl implements ExchangeRateService {

    private SoapServicePort createClient() {
        JaxWsProxyFactoryBean factory = new JaxWsProxyFactoryBean();
        factory.setServiceClass(SoapServicePort.class);
        factory.setAddress(ENDPOINT_URL);
        factory.getInInterceptors().add(new LoggingInInterceptor());
        factory.getOutInterceptors().add(new LoggingOutInterceptor());
        return (SoapServicePort) factory.create();
    }

    public Map<LocalDate, Collection<Rate>> getRates(String currency) {
        String xml = createClient().getExchangeRates(params);
        DecimalFormat df = (DecimalFormat) NumberFormat.getInstance(new Locale("hu"));
        BigDecimal rate = new BigDecimal(df.parse(rateStr).toString());
        // ... build the result from the parsed values
        return result;
    }
}
```

## Rationale

- One service is the only code that knows about SOAP, so the rest of the application stays testable and replaceable.
- The cache keeps the application working when the remote service is slow, down or rate-limited.
- Costs: verbose SOAP and manual XML parsing, classloader friction between CXF and OSGi, and a hard dependency on a third party.

## Example

One application has a dedicated SOAP client module for an external exchange-rate service. It fetches daily rates through `JaxWsProxyFactoryBean` with CXF logging, parses the XML with a locale-specific decimal comma, and exposes them through an exchange-rate service that reads the database first and falls back to SOAP. A scheduled job at 13:00 each day calls it.

## When to avoid

- A REST or JSON alternative exists: use a REST client, ideally one generated from the OpenAPI description.
- The XML API has no WSDL: use a JAXB-based HTTP client ([[jaxb-external-api-client]]).
- The data must be real-time: a cache that is filled once a day is stale by design.

## Related

- [[soap-external-service-client]] — the blueprint with the WSDL-generated module layout
- [[jaxb-external-api-client]] — XML over HTTP without a WSDL
- [[quartz-scheduled-job]] — the job that fills the cache
- [[custom-operation-osgi-component]] — component registration used by the service
