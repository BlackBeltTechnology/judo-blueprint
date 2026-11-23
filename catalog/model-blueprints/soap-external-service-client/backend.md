## Overview

Wraps an external SOAP web service behind a clean OSGi service interface using CXF-generated JAX-WS stubs. The WSDL is included in the module resources, stubs are generated at build time, and the service is initialized via `JaxWsProxyFactoryBean` in the OSGi `@Activate` lifecycle.

All classes below (service interface, implementation, DTOs) are example project code, not platform API. The only platform rule used is that an implementation is registered as an OSGi component (`@Component(immediate = true, service = ...)`), see [custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern). Callers do their own permission checks, because interceptors do not fire for custom operations.

## Implementation Pattern

### Module structure
```
application/
  <soap-client-module>/
    src/main/resources/<service>.wsdl       -- WSDL file for code generation
    src/main/resources/jaxb-bindings.xml    -- JAXB customization bindings
    src/main/java/.../osgi/
      <ServiceInterface>.java               -- Clean domain-oriented interface
      <ServiceImpl>.java                    -- @Component wrapping generated stubs
      <DomainDTO>.java                      -- Domain POJOs (builder pattern)
    pom.xml                                 -- cxf-codegen-plugin for wsdl2java
```

### Build-time code generation
- `cxf-codegen-plugin` with `wsdl2java` goal generates JAX-WS client stubs from the WSDL
- JAXB bindings customize generated code (boolean getters, collection setters)
- Generated sources go to `target/generated-sources/cxf/`

### Service interface
- Plain Java interface with domain-oriented method signatures (e.g., `getCurrencyRates(LocalDate, LocalDate, Collection<String>)`)
- No OSGi annotations on the interface -- only the implementation carries `@Component`
- Domain DTOs use builder pattern for clean construction

### Implementation (`@Component`)
- `@Activate` method initializes `JaxWsProxyFactoryBean` with WSDL URL (loaded from classpath), service class, and endpoint address
- CXF logging interceptors (`LoggingInInterceptor`, `LoggingOutInterceptor`) added for request/response debugging
- Methods delegate to generated SOAP proxy, then parse XML responses into domain DTOs
- XML parsing uses DOM (`DocumentBuilderFactory`) with locale-aware number formatting

### OSGi bundle packaging
- `maven-bundle-plugin` with `<Export-Package>` limited to the `osgi` package (interface + DTOs)
- Generated SOAP stubs are internal (not exported), keeping the public API clean
- Import-Package includes `javax.jws` and `javax.xml.ws` with version ranges

### Consumption
- Scheduled jobs or custom operations `@Reference` the service interface
- The SOAP client module is a separate Maven module, decoupled from the application logic

## Examples

### Example (project code)
- Pattern: integrates with an external SOAP service that publishes daily exchange rates. The WSDL generates the service stubs. The implementation creates the proxy in `@Activate`, parses the XML responses with DOM and maps the day and rate elements into simple rate POJOs.
- Notable: a locale-aware `DecimalFormat` parses comma-separated decimal rates. Scheduled jobs consume the service through an update operation. The client module exports only its own service package.
- DI wiring: the service implementation (OSGi component) -> consumed by scheduler jobs -> which call a generated `UpdateExchangeRates` custom operation
