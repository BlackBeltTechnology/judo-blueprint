---
id: "soap-client-integration"
title: "CXF SOAP Client Integration for External Services"
domain: "backend"
category: "integration"
score: 8.8
usage_count: 1
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - rackinspect
alternatives:
  - jaxb-external-api-client
---
## Description

Integration with external SOAP web services using Apache CXF `JaxWsProxyFactoryBean`. The client is created programmatically with CXF logging interceptors for debugging. Response XML is parsed manually. The service is wrapped in an OSGi component with a database-first/SOAP-fallback strategy for resilience. Handles locale-specific data formats (e.g., Hungarian decimal separator).

## Structure

```java
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
        // Parse XML response
        // Handle Hungarian decimal format (comma separator)
        DecimalFormat df = (DecimalFormat) NumberFormat.getInstance(new Locale("hu"));
        BigDecimal rate = new BigDecimal(df.parse(rateStr).toString());
        return result;
    }
}
```

## Examples

### RackInspect
MNB (Hungarian National Bank) SOAP client in dedicated `mnb-soap-client/` module. Fetches daily exchange rates. Uses `JaxWsProxyFactoryBean` with CXF logging interceptors. Parses XML response with Hungarian locale decimal handling (comma as decimal separator). Wrapped in `ExchangeRateService` with DB-first lookup fallback to SOAP. Called by scheduled job at 13:00 daily.

## Trade-offs

- Pros: Standard JAX-WS/CXF approach, OSGi service abstraction, built-in logging, database caching reduces external calls
- Cons: SOAP is verbose, XML parsing is manual, CXF classloader issues in OSGi, external service dependency
- Alternative: JAXB-based HTTP client (see `jaxb-external-api-client`) for non-WSDL XML APIs, REST API client, or third-party exchange rate REST APIs

## Related Patterns

- quartz-scheduled-job
- custom-operation-osgi-component
- jaxb-external-api-client
