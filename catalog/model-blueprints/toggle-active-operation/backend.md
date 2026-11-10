## Overview

The toggle is a custom operation class per entity. The platform part is the generated interface and the OSGi registration; the rest below is project practice seen in rackinspect and mlszksz-platform. The platform's own toggle example is in [Custom operations](../../agent-docs/backend/custom-operations.md#example-1-simple-toggle-operation).

## Implementation Pattern

### Platform: one class per operation

- Each `ToggleActiveCustomImplementation` is an OSGi `@Component` that implements the interface generated from the model operation, and is registered as a service of that interface.
- Custom operations are not intercepted. Any permission or consistency rule must be inside the class ([Interceptors](../../agent-docs/backend/interceptors.md#which-operations-are-intercepted)).
- A typed business error needs a fault declared on the model operation. Without it the generated interface has no `throws` clause ([Custom operations](../../agent-docs/backend/custom-operations.md#rules-for-custom-operations), [Error handling](../../agent-docs/backend/error-handling-guide.md#modeled-faults)).

### Project practice: three steps

1. Reload the entity by id through its DAO.
2. Flip the boolean and update through the DAO.
3. For child entities, query the owner through the DAO container query and run the shared validate operation on it.

```java
@Component(immediate = true, service = ToggleActive.class)
public class ToggleActiveCustomImplementation implements ToggleActive {
    @Reference AccountDao accountDao;

    @Override
    public void accept(Account _this) {
        Account account = accountDao.getById(_this.identifier()).orElseThrow();
        account.setActive(!account.getActive());
        accountDao.update(account);
    }
}
```

The class and DAO names are illustrative. Use a mask on the update when only the flag changes ([Data access](../../agent-docs/backend/data-access-guide.md#pattern-4-partial-updates)).

### Project practice: sibling toggles

Primary, billing, headquarters, postal and delivery toggles reuse the three steps on different flags. A shared `Validate` operation injected with `@Reference` re-runs owner rules after the flip.

### Project practice: self-lock guard

In rackinspect the user toggle resolves the current actor with `VariableResolver` and refuses to deactivate that user. It also uses a validation DAO to confirm that at least one active user keeps the roles and users permissions. The platform doc shows the same guard ([Custom operations](../../agent-docs/backend/custom-operations.md#example-1-simple-toggle-operation)). Raise a declared fault, not a plain Java exception.

### Project practice: delegating service

In mlszksz-platform the operation class is thin and calls `MasterDataService.toggleCityActive()` or `toggleCapabilityActive()`, an example project service that queries the entity, flips `isActive` and updates through the DAO.
