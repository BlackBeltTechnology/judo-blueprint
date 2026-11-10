## Backend guidance

The cluster is a set of operations that call a service layer. Interceptors do not run on custom operations (platform behaviour), so the rules for credentials, budgets and synchronisation sit in the services. Services, DAOs and the external adapter are example project code, not platform API.

### Operations are thin

A custom operation receives its input, calls one service method, and returns. It holds no business rule of its own. The services are injected components, and the operation class is a small wrapper around them.

```java
public class SetCredentialCustomImplementation implements SetCredentialOperation {
    private final AccountService accountService;   // project service

    public Account setCredential(Account account, CredentialInput input) {
        return accountService.setCredential(account, input);
    }
}
```

### Put platform differences behind an adapter

Each ad platform differs in its API. Put them behind one adapter interface with the calls the cluster needs (check the connection, list campaigns, read cost to date). A factory picks the adapter from the platform enumeration. The rest of the code never mentions a specific platform.

### Budgets are recalculated from the children

The aggregated campaign's spend is the sum of its tracked campaigns' spend. Recalculate it inside the service after a sync, not in the operation, so every path that changes a child updates the budget.

### Deleting a parent removes the owned children

Client owns its accounts and its budget groups through compositions, so deleting a client deletes those children. Tracked campaigns are associations, so they must be handled explicitly: decide whether to unlink or delete them before the parent goes.

### Scheduled sync uses the same services

Background jobs fetch costs, reset daily figures and archive expired budget groups. They call the same services as the operations. A sync that fails for one account should log the failure and continue with the next account, rather than stop the whole job.

### Map external errors to business faults

A failed call to an external platform is a business fault in the operation's contract, not a raw exception. Translate it in the service. A custom operation that throws a business fault must declare that fault in its `faults`, otherwise the generated interface has no matching `throws` clause and the build fails.
