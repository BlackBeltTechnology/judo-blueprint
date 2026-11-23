## Overview

A dashboard transfer object is the landing point for an actor. Its operations are either mapped to the entity's operations or implemented as custom code. Custom operations are application code, not platform code. This is an example pattern from one project.

## Implementation Pattern

- **Mapped operations** delegate to the entity's own operations. The dashboard does not repeat the business rules.
- **Custom operations** on the dashboard are plain classes that implement the generated operation interface. Each receives the dashboard as the first parameter and an input transfer object. Keep each class thin: validate, call a project service, record what matters.
- **Services** named like `OrganizationService` or `FeedService` are application code. The platform does not provide them. Name them for the domain and keep them out of the generated code.
- **Interceptors do not run here.** Interceptors only run on built-in operations (see [interceptors](../../agent-docs/backend/interceptors.md)), so a custom dashboard operation never triggers one. Put audit or counting logic inside the custom operation, or in a built-in operation that the dashboard reads.
- **A DAO call does not run them either.** Calls from service code through the DAO skip them too: interceptors are attached to the dispatcher's built-in behaviours, and the DAO layer has no interceptor hook, so creating a child through the DAO skips the built-in create interceptor. Call the built-in operation through the dispatcher when its interceptor must run.
- **Statistics** come from built-in list or refresh operations on the counted entity, where an interceptor can fill the transient counts. See [[interceptor-derived-statistics-calculation]].

```java
public class CreateOrganizationCustomImplementation implements CreateOrganization {
    private final OrganizationService organizations; // application code

    @Override
    public Organization execute(Dashboard _this, CreateOrganizationInput input) {
        return organizations.create(input.getName());
    }
}
```

The class and the service are application code. The operation interface is generated.

## Examples

### Variant seen in practice
- Pattern: seven custom operation classes in one package, each delegating to an application service
- Notable: `SyncFeedCustomImplementation` runs a full feed synchronization through a feed service; `ExportAuditLogCustomImplementation` builds a CSV with date filtering and stores it through a file store service. Both services are application code.
