## Overview

Wraps an external SOAP web service behind a clean OSGi service interface using CXF-generated JAX-WS stubs. The WSDL is included in the module resources, stubs are generated at build time, and the service is initialized via `JaxWsProxyFactoryBean` in the OSGi `@Activate` lifecycle.

## Implementation Pattern

**Module structure:**
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

**Build-time code generation:**
- `cxf-codegen-plugin` with `wsdl2java` goal generates JAX-WS client stubs from the WSDL
- JAXB bindings customize generated code (boolean getters, collection setters)
- Generated sources go to `target/generated-sources/cxf/`

**Service interface:**
- Plain Java interface with domain-oriented method signatures (e.g., `getCurrencyRates(LocalDate, LocalDate, Collection<String>)`)
- No OSGi annotations on the interface -- only the implementation carries `@Component`
- Domain DTOs use builder pattern for clean construction

**Implementation (`@Component`):**
- `@Activate` method initializes `JaxWsProxyFactoryBean` with WSDL URL (loaded from classpath), service class, and endpoint address
- CXF logging interceptors (`LoggingInInterceptor`, `LoggingOutInterceptor`) added for request/response debugging
- Methods delegate to generated SOAP proxy, then parse XML responses into domain DTOs
- XML parsing uses DOM (`DocumentBuilderFactory`) with locale-aware number formatting

**OSGi bundle packaging:**
- `maven-bundle-plugin` with `<Export-Package>` limited to the `osgi` package (interface + DTOs)
- Generated SOAP stubs are internal (not exported), keeping the public API clean
- Import-Package includes `javax.jws` and `javax.xml.ws` with version ranges

**Consumption:**
- Scheduled jobs or custom operations `@Reference` the service interface
- The SOAP client module is a separate Maven module, decoupled from the application logic

## Examples

### rackinspect
- Key files: `mnb-soap-client/src/main/java/hu/mnb/webservices/osgi/ExchangeRateService.java` (interface), `ExchangeRateServiceImpl.java` (CXF implementation), `Rate.java` + `CurrencyRates.java` (domain DTOs)
- Pattern: Integrates with Magyar Nemzeti Bank (Hungarian National Bank) SOAP API for daily exchange rates. WSDL (`arfolyamok.wsdl`) generates `MNBArfolyamServiceSoap` stubs. `ExchangeRateServiceImpl` creates proxy in `@Activate`, parses XML responses with DOM to extract `<Day>` and `<Rate>` elements into `CurrencyRates` / `Rate` POJOs.
- Notable: Hungarian locale-aware `DecimalFormat` for parsing comma-separated decimal rates. Consumed by `UpdateExchangeRatesJobFirst/Second` scheduled jobs via `@Reference UpdateExchangeRates` (which internally uses `ExchangeRateService`). The module exports only the `hu.mnb.webservices.osgi` package.
- DI wiring: `ExchangeRateServiceImpl` (OSGi component) -> consumed by scheduler jobs -> which call the generated `UpdateExchangeRates` custom operation
