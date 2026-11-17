---
title: Operation Call Interceptors Guide
description: "OperationCallInterceptor contract: which operations interceptors run around (built-in behaviour operations only, never custom (SDK) or script operations), preCall and postCall ordering, throwing business errors from interceptors, and examples."
aliases: [interceptor order, preCall postCall, operation hooks, business error from interceptor, intercept create update, interceptor not running on custom operation]
keywords: [OperationCallInterceptor, preCall, postCall, getOperations, ignoreDecoratedCall, terminateOnException, InterceptorCallBusinessException, AsmUtils, resolveOperation, getOperationFQName, judo.model.name, AuthenticationInterceptor]
tags: [domain:backend, layer:backend, status:platform]
---

# Operation Call Interceptors Guide

> [!IMPORTANT]
> This guide covers `OperationCallInterceptor` for intercepting business logic operations. For handling user authentication events, please see the [Authentication Guide](authentication-guide.md).

## Pattern: Backend-Computed TO Attribute (JQL Escape Hatch)

Certain derived values cannot be expressed as an entity-level `DERIVED` `DataMember`:

- **Bipartite quantifiers** such as "for every supported language ∧ for every paragraph, an approved translation exists" — JQL lambda scopes do not nest, so the outer variable (and `self`) is invisible inside an inner `!forall` / `!filter`.
- **Collection-valued context variables** — `!getVariable(...)` only returns a scalar `String`; `Sequence<String>!getVariable(...)` is not valid JQL grammar.
- **External lookups** — anything that requires I/O at read-time.

The canonical escape hatch keeps the value on the TO (so the UI and consumers see it) without forcing it through JQL:

1. **Remove** the `DERIVED` `DataMember` from the `EntityType`.
2. On each `TransferObjectType` that exposes the value, declare it as `memberType="TRANSIENT"` with **no `binding`**:

    ```xml
    <attributes xsi:type="structure:DataMember"
                name="readyForAllLanguages"
                dataType="_boolTypeId"
                memberType="TRANSIENT"
                identifier="false"/>
    ```

3. Register an `OperationCallInterceptor` that fires **after** the mapped read operations (`_getById`, list queries, etc.), enriching the outgoing payload in place.

```java
@Component(property = { "judo.model.name=<model>" })
public class MyTransientEnricher implements OperationCallInterceptor {
    private AsmUtils asmUtils;                     // built from asmModel.getResourceSet()
    private List<EOperation> operations;

    @Override public String getName() { return getClass().getSimpleName(); }

    @Override public Collection<EOperation> getOperations(AsmModel asmModel) {
        if (operations == null) {
            asmUtils = new AsmUtils(asmModel.getResourceSet());
            operations = Stream.of("<model>.services.MyTO#_getById",     // illustrative FQNs, see
                                   "<model>.services.MyTO#_query")        // "Operation FQN Format Reference"
                    .map(asmUtils::resolveOperation).map(Optional::orElseThrow).toList();
        }
        return operations;
    }

    @Override
    public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload)
            throws InterceptorCallBusinessException {
        Payload result = (Payload) returnPayload;      // list operations return a Collection<Payload>
        result.put("readyForAllLanguages", compute(result));
        return result;
    }
}
```

**Why not a view / union?** A transient TO member is the narrowest, least invasive choice: the entity model stays pure, the TO surface matches the spec, and the value is re-computed per request with no cache-invalidation surface. Use an entity-level denormalisation only when the value must also be filterable/sortable at the DAO layer.

## Advanced Interceptor Patterns

The JUDO framework provides two types of interceptors, `OperationCallInterceptor` and `AuthenticationInterceptor`, which can be used to implement a variety of powerful, cross-cutting patterns.

### Data Denormalization and Aggregation

This pattern uses an `OperationCallInterceptor` to denormalize and aggregate data, which is a common technique to optimize read performance. By pre-calculating and storing aggregated values, the application can avoid complex and potentially slow queries when retrieving data for display.

**Example**

An interceptor like `MyEntityUpdateInterceptor` can be used to listen for updates on `MyEntity`. In the `postCall` hook, it can query for related `Tag` entities, aggregate their names into a comma-separated string, and save that string to a `tagsAggregated` field on `MyEntity`.

```java
// From a hypothetical MyEntityUpdateInterceptor.java
@Override
public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload) throws InterceptorCallBusinessException {
    if (parameterPayload instanceof UpdateInstanceCall.UpdateInstanceCallPayload updateInstanceCallPayload) {
        UUID identifier = updateInstanceCallPayload.getInstance().getAs(UUID.class, "__identifier");
        MyEntity entity = myEntityDao.getById(identifier, MyEntityMask.mask()
                .withTagsAggregated()
        ).orElseThrow();

        String tagsAggregated = myEntityDao.queryTags(entity).selectList().stream()
                                      .map(Tag::getName).sorted().collect(Collectors.joining(", "));
        
        if (!entity.getTagsAggregated().orElse("").equals(tagsAggregated)) {
            entity.setTagsAggregated(tagsAggregated);
            myEntityDao.update(entity, MyEntityMask.mask());
        }
    }
    return OperationCallInterceptor.super.postCall(operation, parameterPayload, returnPayload);
}
```

### Decoupled Service Creation (CQRS-like Pattern)

This pattern uses an `OperationCallInterceptor` to trigger the creation of a resource in a different service or bounded context when an operation is performed. This promotes loose coupling between services.

**Example**

An interceptor like `UserProfileCreateInterceptor` can intercept the creation of a `UserProfile`. In the `preCall` hook, it can take the profile data, transform it, and create a `WelcomeJourney` object using a different DAO. By returning `true` from `ignoreDecoratedCall()`, it prevents the original `UserProfile` from being created directly, effectively replacing the operation.

```java
// From a hypothetical UserProfileCreateInterceptor.java
public Object preCall(EOperation operation, Object parameterPayload) throws InterceptorCallBusinessException {
    if (parameterPayload instanceof CreateInstanceCall.CreateInstanceCallPayload createInstanceCallPayload) {
        UserProfile profile = UserProfile.from(createInstanceCallPayload.getInput());
        
        WelcomeJourneyForCreate create = WelcomeJourneyForCreate.builder()
                .withEmail(profile.getEmail())
                .withStage(WelcomeStage.STARTED)
                .build();

        welcomeJourneyDao.create(create);
    }
    return createInstanceCallPayload;
}

public boolean ignoreDecoratedCall() {
    return true;
}
```



### Derived State Calculation and Enforcement

This pattern uses a pair of `OperationCallInterceptor` instances to manage derived data based on a single "source of truth" field (e.g., an enumeration). One interceptor (`_refresh`) calculates derived fields on read, and the other (`_update`) enforces data consistency on write.

**Example**

- **Refresh Interceptor:** On a `_refresh` operation for a `LocatedItem` entity, the `postCall` hook inspects if a `country`, `state`, or `city` relationship exists. Based on this, it sets a `LocationScope` enum and derived boolean flags like `isCountryScope`. This simplifies UI logic.

- **Update Interceptor:** On an `_update` operation, the `postCall` hook reads the `LocationScope` enum sent from the client. If the scope is `COUNTRY`, it ensures any `state` and `city` relationships on the entity are nullified before saving, guaranteeing data integrity.



## Overview

`OperationCallInterceptor` is a powerful mechanism for implementing cross-cutting concerns that apply to business logic operations. They allow you to execute custom code **before** (`preCall`) and **after** (`postCall`) a modeled operation is invoked.

Common use cases include:
- **Auditing**: Creating a log of who performed what action and when.
- **Payload Manipulation**: Modifying input data before an operation or transforming the result after.
- **Side Effects**: Triggering other operations or external service calls in response to an event.
- **Complex Validation**: Enforcing business rules that involve multiple entities or external state.

### OperationCallInterceptor Interface

JUDO provides the `OperationCallInterceptor` interface for intercepting model operations:

```java
public interface OperationCallInterceptor {
    String getName();
    default Collection<EOperation> getOperations(AsmModel asmModel) { return Collections.emptyList(); }
    default boolean async()                { return false; }
    default boolean terminateOnException() { return true; }
    default boolean ignoreDecoratedCall()  { return false; }
    default Object preCall(EOperation operation, Object parameterPayload)
            throws InterceptorCallBusinessException { return parameterPayload; }
    default Object postCall(EOperation operation, Object parameterPayload, Object returnPayload)
            throws InterceptorCallBusinessException { return returnPayload; }
}
```

### The Interceptor Contract

| Method | Meaning |
| :--- | :--- |
| `getName()` | Name of the interceptor (used for logging). |
| `getOperations(AsmModel)` | Operations the interceptor is registered for. The default is an empty collection, which means **all intercepted (built-in) operations**. |
| `preCall` | Runs before the decorated call. The returned object replaces the input payload and must be assignable to the expected payload type (otherwise `IllegalArgumentException`). When `ignoreDecoratedCall()` is `true` it must return the payload of the decorated call's return type. |
| `postCall` | Runs after the decorated call with the input and the call's return payload (a `Payload` or a collection of payloads). The returned object becomes the result. |
| `ignoreDecoratedCall()` | `true` skips the platform's own DAO call, so the interceptor replaces the operation. The decorated call runs only if no interceptor for the operation returns `true`. |
| `async()` | `true` runs the interceptor on a different thread, outside the transaction and without context variables. Its exceptions are lost and it cannot change the payload. |
| `terminateOnException()` | Defaults to `true`: an exception terminates the call. Ignored for async interceptors. |

Interceptors may throw only `InterceptorCallBusinessException` (see [Throwing a Business Error from an Interceptor](#throwing-a-business-error-from-an-interceptor)).

### Which Operations Are Intercepted

Interceptors fire **only for the built-in behaviour operations**: create, update, delete, list/query, refresh, set/unset/add/remove reference, reference range, input range, getTemplate, getMetadata, getPrincipal, upload token, export and the validate calls. These are the operations that the runtime implements itself (the `*Call` classes in `judo-runtime-core-dispatcher`'s `behaviours` package).

**Custom (SDK-implemented) and script operations never hit interceptors**, even if `getOperations` lists them or returns an empty collection. The Javadoc claim that an empty list intercepts "all operation calls" means all built-in calls only.

Consequences:

- Write guards and permission checks for custom operations (for example `User.toggleActive`, `createUser`, `resendInvitation`) must be written inside each `*CustomImplementation`, not in an interceptor.
- Hiding a UI button does not protect an operation either.
- Range interceptors fire only on the `_getRangeReference*` (reference range) operations, not on plain list or query operations such as `~list`. A range interceptor is the security boundary for relations with a range type that exposes every instance (`rangeType=ANY`) because read-only attributes do not stop enumeration. Model `min`/`max` bounds are UI-only and are not enforced on the server.
- Input validation of exposed operations runs without interceptors.
- Interceptors are called from the dispatcher's behaviour calls (`CallInterceptorUtil` in the `*Call` classes), not from the DAO. A DAO call from Java service code (for example creating a child entity) does not trigger interceptors.

### Ordering and Combining Several Interceptors

All interceptors registered for an operation are called in **registration order** for `preCall` **and** for `postCall` (`postCall` is not reversed). Each `preCall` receives the original input payload, so interceptors see each other's in-place mutations of that payload; the objects they return are accumulated and the last non-null result wins. `postCall` behaves the same with respect to the return payload.

All synchronous interceptors run inside the transaction of the operation. An exception from `preCall` or `postCall` therefore rolls back the DAO write of the operation, including writes done by earlier interceptors.

## Interceptor Component Registration

**Required annotation properties:**

```java
@Component(property = { "judo.model.name=<app>" })
public class MyInterceptor implements OperationCallInterceptor {
    // Implementation
}
```

**Why `property = { "judo.model.name=<app>" }`?**
- Binds interceptor to specific JUDO model
- Runtime uses this to match interceptors to operations
- Multiple models can coexist with different interceptors

### Guice and Spring Registration

The default `OperationCallInterceptorProvider` returns an empty list unless interceptors are configured explicitly: it does not read a Guice `Multibinder` set of `OperationCallInterceptor`. In Spring, a `@Bean` that returns an `OperationCallInterceptor` is not collected; the default Spring configuration returns an empty interceptor list.

## Example 1: Simple Logging Interceptor

**Pattern**: Log all intercepted operations

```java
@Component(property = { "judo.model.name=<app>" })
public class LogOperationCallInterceptor implements OperationCallInterceptor {

    private static final Logger log = LoggerFactory.getLogger(LogOperationCallInterceptor.class);

    @Override
    public String getName() {
        return this.getClass().getSimpleName();
    }

    // No getOperations() override means: intercept ALL built-in operations (never custom/script operations)
    // Uncomment and implement to intercept specific operations only

    @Override
    public Object preCall(EOperation operation, Object parameterPayload) {
        String operationFQName = AsmUtils.getOperationFQName(operation);
        log.info("*** ⬇️ INTERCEPTED OPERATION ⬇️ ***");
        log.info(operationFQName);
        log.info("*** ⬆️ INTERCEPTED OPERATION ⬆️ ***");
        return OperationCallInterceptor.super.preCall(operation, parameterPayload);
    }
}
```

**Key patterns:**
- `@Component(property = { "judo.model.name=<app>" })` - Required for operation interceptors
- No `getOperations()` implementation = intercept ALL built-in operations (custom and script operations are never intercepted)
- `AsmUtils.getOperationFQName()` - Get fully qualified operation name
- `preCall()` - Executed before operation logic

## Example 2: Selective Operation Interception (Create)

**Pattern**: Intercept specific operation and execute post-operation logic

### Create Interceptor Code

```java
@Component(property = { "judo.model.name=<app>" })
public class EntityCreateInterceptor implements OperationCallInterceptor {

    @Reference EntityDao entityDao;
    @Reference RecalculateRelatedData recalculateRelatedData;

    private AsmUtils asmUtils;
    private List<EOperation> interceptedOperations;

    @Override
    public String getName() {
        return this.getClass().getSimpleName();
    }

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        if (interceptedOperations == null) {
            if (asmUtils == null) {
                asmUtils = new AsmUtils(asmModel.getResourceSet());
            }

            // Specify exact operation to intercept by FQN
            EOperation createOperation =
                    asmUtils.resolveOperation("<app>.services.ServiceContext#_createInstanceEntities")
                            .orElseThrow();

            interceptedOperations = List.of(createOperation);
        }
        return interceptedOperations;
    }

    @Override
    public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload) {
        // Extract input payload
        Payload inputPayload = ((CreateInstanceCall.CreateInstanceCallPayload) parameterPayload).getInput();
        
        // Convert to typed input
        [package.path.to.your.entity].Entity input =
                [package.path.to.your.entity].Entity.from(inputPayload);

        // Get created entity ID from return payload
        Serializable entityIdentifier = getIdOf(returnPayload);
        Entity entity = entityDao.getById(entityIdentifier, EntityMask.entityMask().withIdentifier()).orElseThrow();

        // Create related entities
        EntityLocation newLocation = entityDao.createEntityLocations(entity,
                EntityLocationForCreate.builder()
                        .withPostalCode(input.getForm_primaryLocationPostalCode())
                        .withCity(input.getForm_primaryLocationCity())
                        .withAddressLine(input.getForm_primaryLocationAddressLine())
                        .build(),
                EntityLocationMask.entityLocationMask());
        entityDao.setPrimaryEntityLocation(entity, newLocation);

        EntityContact newContact = entityDao.createEntityContacts(entity,
                EntityContactForCreate.builder()
                        .withContactValue(input.getForm_primaryContact())
                        .withContactType(input.getForm_primaryContactType())
                        .build(),
                EntityContactMask.entityContactMask());
        entityDao.setPrimaryEntityContact(entity, newContact);

        EntityDetail newDetail = entityDao.createEntityDetails(entity,
                EntityDetailForCreate.builder()
                        .withDetailValue(entity.getIdentifier())
                        .build(),
                EntityDetailMask.entityDetailMask());
        entityDao.setPrimaryEntityDetail(entity, newDetail);

        // Execute other custom operations; a fault from a service is wrapped for the interceptor
        try {
            recalculateRelatedData.accept(entity);
        } catch (RecalculationFailedException e) {      // generated <Fault>Exception of the operation
            throw new InterceptorCallBusinessException(
                    "<app>.services.RecalculationFailed", "RECALCULATION_FAILED",
                    Map.of("message", String.valueOf(e.getMessage())), e, null);
        }

        return OperationCallInterceptor.super.postCall(operation, parameterPayload, returnPayload);
    }
}
```

#### Key patterns demonstrated

- **Selective interception**: `getOperations()` returns specific operations
- **Operation FQN format**: `[model_name].services.[ServiceName]#_createInstance[EntityName]` (for create operations)
- **Lazy initialization**: Cache `interceptedOperations` and `asmUtils`
- **Post-call processing**: Extract created entity ID and perform additional setup
- **Payload casting**: Cast to specific payload type (`CreateInstanceCallPayload`)
- **Creating related entities**: Use relationship DAO methods
- **Calling other operations**: Reference and invoke other custom operations

## Example 3: Update Interceptor with Batch Processing

**Pattern**: Intercept update and process multiple related entities

```java
@Component(property = { "judo.model.name=<app>" })
public class AccessRoleUpdateInterceptor implements OperationCallInterceptor {

    @Reference EntityDao entityDao;
    @Reference RecalculateRelatedData recalculateRelatedData;

    private AsmUtils asmUtils;
    private List<EOperation> interceptedOperations;

    @Override
    public String getName() {
        return this.getClass().getSimpleName();
    }

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        if (interceptedOperations == null) {
            if (asmUtils == null) {
                asmUtils = new AsmUtils(asmModel.getResourceSet());
            }

            // Intercept update operation
            interceptedOperations = Stream.of(
                    "<app>.services.entity_service.AccessRole#_updateInstance<app>_services_entity_service_AccessRole"
            ).map(asmUtils::resolveOperation).map(Optional::orElseThrow).toList();
        }
        return interceptedOperations;
    }

    @Override
    public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload) {
        if (parameterPayload instanceof UpdateInstanceCall.UpdateInstanceCallPayload) {
            // When role is updated, recalculate related data for ALL entities
            List<Entity> entities = entityDao.query().maskedBy(EntityMask.entityMask()).selectList();
            for (Entity entity : entities) {
                try {
                    recalculateRelatedData.accept(entity);
                } catch (RecalculationFailedException e) {      // generated <Fault>Exception
                    throw new InterceptorCallBusinessException(
                            "<app>.services.RecalculationFailed", "RECALCULATION_FAILED",
                            Map.of("message", String.valueOf(e.getMessage())), e, null);
                }
            }
        }

        return OperationCallInterceptor.super.postCall(operation, parameterPayload, returnPayload);
    }
}
```

#### Key patterns demonstrated

- **Update operation FQN**: `#_updateInstance[FullEntityFQN]`
- **Payload type check**: `instanceof UpdateInstanceCallPayload`
- **Batch processing**: Query and process all related entities
- **Cascading updates**: Propagate changes to dependent entities
- **Old versus new values**: `UpdateInstanceCallPayload.getInput()` holds the values sent by the client (the new values); `getInstance()` identifies the instance (`__identifier`) and does not carry its stored values. To compare, read the stored entity with the DAO in `preCall` (before the write) using the identifier from `getInstance()`, then compare it with `getInput()`.

## Example 4: Pre-Call Payload Manipulation

**Pattern**: Modify input payload before operation execution

### Pre-Call Interceptor Code

```java
@Component(property = { "judo.model.name=<app>" })
public class ParentEntityCreateInterceptor implements OperationCallInterceptor {

    @Reference ChildEntityDao childEntityDao;
    @Reference ParentEntityDao parentEntityDao;
    @Reference LocationService locationService;

    private AsmUtils asmUtils;
    private List<EOperation> interceptedOperations;

    @Override
    public String getName() {
        return this.getClass().getSimpleName();
    }

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        if (interceptedOperations == null) {
            if (asmUtils == null) {
                asmUtils = new AsmUtils(asmModel.getResourceSet());
            }

            EOperation parentEntityCreateOperation =
                    asmUtils.resolveOperation("<app>.services.ServiceContext#_createInstanceParentEntities")
                            .orElseThrow();

            interceptedOperations = List.of(parentEntityCreateOperation);
        }
        return interceptedOperations;
    }

    @Override
    public Object preCall(EOperation operation, Object parameterPayload) {
        Payload input = ((CreateInstanceCallPayload) parameterPayload).getInput();

        // Validate input before operation
        // getAs returns null when the key is absent: compare with Boolean.TRUE instead of unboxing
        if (!Boolean.TRUE.equals(input.getAs(Boolean.class, ParentEntityAttribute.FORM_IS_PRIMARY.getName()))) {
            throw new ValidationException(List.of(ValidationResult.builder()
                    .code("PRIMARY_FLAG_REQUIRED")
                    .level(ValidationResult.Level.ERROR)
                    .location(ParentEntityAttribute.FORM_IS_PRIMARY.getName())
                    .build()));
        }

        // Build complex nested payload from form fields
        input.put(ParentEntityReference.CHILD_ENTITIES.getName(), List.of(Payload.map(
                ChildEntityReference.REFERENCE_DATA.getName(), input.get(ParentEntityReference.FORM_REFERENCE_DATA.getName()),
                ChildEntityAttribute.REGION.getName(), input.get(ParentEntityAttribute.FORM_REGION.getName()),
                ChildEntityAttribute.POSTAL_CODE.getName(), input.get(ParentEntityAttribute.FORM_POSTAL_CODE.getName()),
                ChildEntityAttribute.CITY.getName(), input.get(ParentEntityAttribute.FORM_CITY.getName()),
                ChildEntityAttribute.STREET_NAME.getName(), input.get(ParentEntityAttribute.FORM_STREET_NAME.getName()),
                ChildEntityAttribute.CATEGORY.getName(), input.get(ParentEntityAttribute.FORM_CATEGORY.getName()),
                ChildEntityAttribute.NUMBER.getName(), input.get(ParentEntityAttribute.FORM_NUMBER.getName()),
                ChildEntityAttribute.BUILDING.getName(), input.get(ParentEntityAttribute.FORM_BUILDING.getName()),
                ChildEntityAttribute.FLOOR.getName(), input.get(ParentEntityAttribute.FORM_FLOOR.getName()),
                ChildEntityAttribute.UNIT.getName(), input.get(ParentEntityAttribute.FORM_UNIT.getName()),
                ChildEntityAttribute.REFERENCE_CODE.getName(), input.get(ParentEntityAttribute.FORM_REFERENCE_CODE.getName()),
                ChildEntityAttribute.MANUAL_DATA.getName(), input.get(ParentEntityAttribute.FORM_MANUAL_DATA.getName()),
                ChildEntityAttribute.COMPUTED_DATA.getName(), input.get(ParentEntityAttribute.FORM_COMPUTED_DATA.getName()),
                ChildEntityAttribute.IS_PRIMARY.getName(), true,
                ChildEntityAttribute.IS_DEFAULT.getName(), input.get(ParentEntityAttribute.FORM_IS_DEFAULT.getName()),
                ChildEntityAttribute.IS_ACTIVE.getName(), input.get(ParentEntityAttribute.FORM_IS_ACTIVE.getName()),
                ChildEntityAttribute.IS_VERIFIED.getName(), input.get(ParentEntityAttribute.FORM_IS_VERIFIED.getName())
        )));

        return OperationCallInterceptor.super.preCall(operation, parameterPayload);
    }

```

#### Post-call part of the same interceptor

```java
    @Override
    public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload) {
        Payload input = ((CreateInstanceCallPayload) parameterPayload).getInput();

        ParentEntity parentEntity = parentEntityDao.getById(getIdOf(returnPayload), ParentEntityMask.parentEntityMask()).orElseThrow();
        ChildEntity childEntity = parentEntityDao.queryChildEntities(parentEntity)
                                    .maskedBy(ChildEntityMask.childEntityMask())
                                    .selectList().stream().findAny().orElseThrow();

        // Set relationship references
        parentEntityDao.setPrimaryChild(parentEntity, childEntity);

        if (input.getAs(Boolean.class, "form_isDefault")) {
            parentEntityDao.setDefaultChild(parentEntity, childEntity);
        }
        if (input.getAs(Boolean.class, "form_isVerified")) {
            parentEntityDao.setVerifiedChild(parentEntity, childEntity);
        }

        // Post-process created related entities
        List<ChildEntity> childEntities = parentEntityDao.queryChildEntities(parentEntity).selectList();
        for (ChildEntity child : childEntities) {
            if (!child.getManualData()) {
                locationService.autoUpdateComputedData(child.identifier());
            }
            locationService.updateFullData(child.identifier());
        }

        return returnPayload;
    }
}
```

#### Key patterns demonstrated

- **Payload manipulation**: Modify input before operation execution
- **Payload.map()**: Build nested payloads with key-value pairs
- **Form field mapping**: Transform flat form fields to nested entity structures
- **Pre-call validation**: Validate and throw `ValidationException` (field rule) or `InterceptorCallBusinessException` (business refusal) before the operation
- **Setting relationship references**: `parentEntityDao.setPrimaryChild()`, `setDefaultChild()`
- **Post-processing related entities**: Call external services on created entities

## Example 5: Intercepting Reference Operations

**Pattern**: Intercept add/remove/set/delete reference operations

```java
@Component(property = { "judo.model.name=<app>" })
public class AccessRoleSetAndRemoveAndDeleteInterceptor implements OperationCallInterceptor {

    @Reference EntityDao entityDao;
    @Reference RecalculateRelatedData recalculateRelatedData;
    @Reference EntityValidationQueries validationQueries;   // illustrative: a DAO exposing model-defined validation queries

    private AsmUtils asmUtils;
    private List<EOperation> interceptedOperations;

    @Override
    public String getName() {
        return this.getClass().getSimpleName();
    }

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        if (interceptedOperations == null) {
            if (asmUtils == null) {
                asmUtils = new AsmUtils(asmModel.getResourceSet());
            }

            // Intercept multiple reference operations
            interceptedOperations = Stream.of(
                    "<app>.services.entity_service.AccessRole#_addReferenceAccessPermissions",
                    "<app>.services.entity_service.AccessRole#_removeReferenceAccessPermissions",
                    "<app>.services.entity_service.AccessRole#_setReferenceAccessPermissions",
                    "<app>.services.entity_service.AccessRole#_deleteInstance<app>_services_entity_service_AccessRole"
            ).map(asmUtils::resolveOperation).map(Optional::orElseThrow).toList();
        }
        return interceptedOperations;
    }

    @Override
    public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload) {
        // Validate business rule after any permission change
        Boolean activeEntitiesWithAtLeastManagementPermission = 
            validationQueries.queryActiveEntitiesWithAtLeastManagementPermission().orElse(false);
        Boolean activeEntitiesWithAtLeastAdminPermission = 
            validationQueries.queryActiveEntitiesWithAtLeastAdminPermission().orElse(false);

        if (!(activeEntitiesWithAtLeastManagementPermission && activeEntitiesWithAtLeastAdminPermission)) {
            // IllegalStateException would become a 500; refuse with a business error (rolls back the change)
            throw new InterceptorCallBusinessException(
                    "<app>.services.MinimumPermissionsViolated", "MINIMUM_PERMISSIONS_REQUIRED",
                    Map.of("message", "Maintain minimum required entities with specific permissions"),
                    null, null);
        }

        // Recalculate related data for all entities
        List<Entity> entities = entityDao.query().maskedBy(EntityMask.entityMask()).selectList();
        for (Entity entity : entities) {
            try {
                recalculateRelatedData.accept(entity);
            } catch (RecalculationFailedException e) {      // generated <Fault>Exception
                throw new InterceptorCallBusinessException(
                        "<app>.services.RecalculationFailed", "RECALCULATION_FAILED",
                        Map.of("message", String.valueOf(e.getMessage())), e, null);
            }
        }

        return OperationCallInterceptor.super.postCall(operation, parameterPayload, returnPayload);
    }
}
```

#### Key patterns demonstrated

- **Multiple operation interception**: Single interceptor for related operations
- **Reference operations**: `_addReference`, `_removeReference`, `_setReference`
- **Business rule enforcement**: Validate after changes; an `InterceptorCallBusinessException` rolls back the whole operation
- **Derived query methods**: Use model-generated validation queries

### Narrowing a Range with a Pre-Call Interceptor

The pre-call payload of a reference range operation (`_getRangeReference*`) is `GetReferenceRangeCall.GetReferenceRangeCallPayload`: `owner` (`EReference`), `ownerPayload` (`Payload`), `queryCustomizer` (`DAO.QueryCustomizer`) and `recordCount` (settable). A list operation gets `ListCall.ListCallPayload` with `owner`, `instance`, `queryCustomizer` and `recordCount`. A `QueryCustomizer` is immutable (a Lombok `@Builder` without `toBuilder`): `filter` is a JQL string with `this` as the target (conditions of the request are joined with ` and `), `orderByList`, `seek`, `mask`, `parameters`, `instanceIds`, `withoutFeatures`. To add a constraint, build a new customizer that copies the other fields, and return a new payload from `preCall`:

```java
@Override
public Object preCall(EOperation operation, Object payload) {
    if (!(payload instanceof GetReferenceRangeCall.GetReferenceRangeCallPayload)) {
        return payload;
    }
    var p = (GetReferenceRangeCall.GetReferenceRangeCallPayload) payload;
    var old = p.getQueryCustomizer();
    var oldFilter = old != null ? old.getFilter() : null;
    var extra = "this.<flag>";                       // JQL on the range target type
    var qc = DAO.QueryCustomizer.builder()
            .filter(oldFilter == null || oldFilter.isBlank() ? extra : "(" + oldFilter + ") and " + extra)
            .orderByList(old != null ? old.getOrderByList() : List.of())
            .seek(old != null ? old.getSeek() : null)
            .mask(old != null ? old.getMask() : null)
            .parameters(old != null ? old.getParameters() : null)
            .instanceIds(old != null ? old.getInstanceIds() : null)
            .withoutFeatures(old != null && old.isWithoutFeatures())
            .build();
    return GetReferenceRangeCall.GetReferenceRangeCallPayload.builder()
            .owner(p.getOwner()).ownerPayload(p.getOwnerPayload()).queryCustomizer(qc).build();
}
```

`getOperations` must name the range operation(s); the returned object must be of the same payload type.

## Example 6: Handling Both Create and Update

**Pattern**: Single interceptor for create and update with pattern matching

### Create and Update Interceptor Code

```java
@Component(property = { "judo.model.name=<app>" })
public class ChildEntityCreateAndUpdateInterceptor implements OperationCallInterceptor {

    @Reference ParentEntityDao parentEntityDao;
    @Reference ChildEntityDao childEntityDao;
    @Reference ValidateEntity validateEntity;
    @Reference LocationService locationService;
    @Reference DataInterceptorService dataInterceptorService;

    private AsmUtils asmUtils;
    private List<EOperation> interceptedOperations;

    @Override
    public String getName() {
        return this.getClass().getSimpleName();
    }

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        if (interceptedOperations == null) {
            if (asmUtils == null) {
                asmUtils = new AsmUtils(asmModel.getResourceSet());
            }

            // Intercept both create and update
            interceptedOperations = Stream.of(
                    "<app>.services.parent_service.ParentEntity#_createInstanceChildEntities",
                    "<app>.services.parent_service.ChildEntity#_updateInstance<app>_services_parent_service_ChildEntity"
            ).map(asmUtils::resolveOperation).map(Optional::orElseThrow).toList();
        }
        return interceptedOperations;
    }

    @Override
    public Object preCall(EOperation operation, Object parameterPayload) {
        // Pattern matching with instanceof - handles both create and update
        if (parameterPayload instanceof CreateInstanceCallPayload createInstanceCallPayload) {
            Payload inputPayload = createInstanceCallPayload.getInput();
            dataInterceptorService.createNestedGroupsOnEntity(inputPayload);
        } else if (parameterPayload instanceof UpdateInstanceCall.UpdateInstanceCallPayload updateInstanceCallPayload) {
            Payload inputPayload = updateInstanceCallPayload.getInput();
            dataInterceptorService.createNestedGroupsOnEntity(inputPayload);
        } else {
            throw new IllegalArgumentException("Unsupported parameter payload: " + parameterPayload.getClass().getName());
        }

        return OperationCallInterceptor.super.preCall(operation, parameterPayload);
    }

```

#### Post-call part of the same interceptor

```java
    @Override
    public Object postCall(EOperation operation, Object parameterPayload, Object returnPayload) {
        if (parameterPayload instanceof CreateInstanceCallPayload) {
            ChildEntity childEntity = childEntityDao.getById(getIdOf(returnPayload)).orElseThrow();
            ParentEntity parentEntity = childEntityDao.queryContainer(childEntity, ParentEntityMask.parentEntityMask()).orElseThrow();

            // Set relationships based on flags
            if (childEntity.getIsPrimary()) {
                parentEntityDao.setPrimaryChild(parentEntity, childEntity);
            }
            if (childEntity.getIsDefault()) {
                parentEntityDao.setDefaultChild(parentEntity, childEntity);
            }
            if (childEntity.getIsVerified()) {
                parentEntityDao.setVerifiedChild(parentEntity, childEntity);
            }

            // Call external services
            if (!childEntity.getManualData()) {
                locationService.autoUpdateComputedData(childEntity.identifier());
            }
            locationService.updateFullData(childEntity.identifier());

            validateEntity.accept(parentEntity);
        } else if (parameterPayload instanceof UpdateInstanceCall.UpdateInstanceCallPayload updateInstanceCallPayload) {
            ChildEntity childEntity = childEntityDao.getById(getIdOf(updateInstanceCallPayload.getInstance())).orElseThrow();
            ParentEntity parentEntity = childEntityDao.queryContainer(childEntity, ParentEntityMask.parentEntityMask()).orElseThrow();
            
            if (!childEntity.getManualData()) {
                locationService.autoUpdateComputedData(childEntity.identifier());
            }
            locationService.updateFullData(childEntity.identifier());
            validateEntity.accept(parentEntity);
        } else {
            throw new IllegalArgumentException("Unsupported parameter payload: " + parameterPayload.getClass().getName());
        }

        return returnPayload;
    }
}
```

#### Key patterns demonstrated

- **Pattern matching**: Modern Java `instanceof` with pattern variables
- **Mixed operation types**: Handle create and update in same interceptor
- **Container navigation**: `queryContainer()` to get parent entity
- **Conditional relationship setting**: Set references based on entity flags
- **External service calls**: Injecting and calling custom services
- **Invoking other operations**: Call `validateEntity.accept()` operation

## Throwing a Business Error from an Interceptor

`preCall` and `postCall` declare `throws InterceptorCallBusinessException` (package `hu.blackbelt.judo.runtime.core.dispatcher.behaviours`, a subclass of the platform `BusinessException`). It is the **only** business-level exception an interceptor may throw:

- A modeled fault's generated `<Fault>Exception` is checked and cannot be thrown from an interceptor; catch it from the service you called and rewrap it.
- A raw `RuntimeException` (or `IllegalStateException`) is wrapped by the dispatcher as `InternalServerException` and the client sees a generic 500.
- Interceptors do not handle business problems on their own; they refuse the call by wrapping the problem.

```java
throw new InterceptorCallBusinessException(
        "<app>.services.AlreadyShipped",                 // type: FQN of a modeled fault transfer object
        "ALREADY_SHIPPED",                               // errorCode
        Map.of("message", "The order was already shipped"), // details; never null
        null,                                            // cause (optional)
        null);                                           // locale: replaced by the dispatcher's locale
```

What happens next: the behaviour call catches the exception and returns a `_fault` payload; `DefaultDispatcher` turns it into a `BusinessException`; REST answers **422** with header `X-Fault: <type>` and body `{ "<type>": {details without "_"-prefixed keys and nulls}, "code": "<errorCode>" }`. Because interceptors run inside the operation's transaction, the exception rolls back the DAO write, also when thrown from `postCall`.

Guidance:

- Use the **FQN of a modeled fault transfer object as `type`** and put the message and parameters into `details`. The frontend fault dialog resolves translations with `faults.<type>.<attribute>`; a `type` such as an interceptor or guard name matches no translation. Neither `type` nor `details` is validated against the model, so a typo still produces a 422 but the dialog falls back to raw attribute names. `details` must not be `null`.
- For a field rule on one attribute throw `ValidationException` (400) with the attribute name as `location`; the location is optional.
- To refuse for permission reasons (write guards) use `InterceptorCallBusinessException` with your own stable `errorCode`; it is a business refusal, not a field error.
- For the full mapping see [Error Handling Guide](error-handling-guide.md#how-the-runtime-maps-exceptions-to-http).

## Reading the Principal and Actor in an Interceptor

The dispatcher keeps request context in an exchange map. The key constants are defined on `hu.blackbelt.judo.dispatcher.api.Dispatcher`: `PRINCIPAL_KEY` (`"__principal"`), `ACTOR_KEY` (`"__actor"`), `INSTANCE_KEY_OF_BOUND_OPERATION` (`"__this"`) and `ENTITY_TYPE_MAP_KEY` (`"__entityType"`). The signed identifier of an instance is read from the `__signedIdentifier` payload key. Actor and principal variables are also available to JQL and Java through `VariableResolver.resolve(String.class, "ACTOR", "identifier")` (see [Custom Operations](custom-operations.md)).

## Operation FQN Format Reference

Operation Fully Qualified Names follow specific patterns:

| Operation Type | FQN Pattern | Example |
|----------------|-------------|---------|
| Create (Transfer) | `[model_name].[actor_package].[ActorName]#_createInstance[EntityPlural]` | `<app>.entity_admin.Admin#_createInstanceEntities` |
| Create (Contained) | `[model_name].[entity_package].[Parent]#_createInstance[ChildEntityPlural]` | `<app>.data_management.DataGroup#_createInstanceDataItems` |
| Update | `[model_name].[entity_package].[Entity]#_updateInstance[FullEntityFQN]` | `<app>.access_management.AccessRole#_updateInstance<app>_access_management_AccessRole` |
| Delete | `[model_name].[entity_package].[Entity]#_deleteInstance[FullEntityFQN]` | `<app>.access_management.AccessRole#_deleteInstance<app>_access_management_AccessRole` |
| Add Reference | `[model_name].[entity_package].[Entity]#_addReference[RelationshipName]` | `<app>.access_management.AccessRole#_addReferenceAccessPermissions` |
| Remove Reference | `[model_name].[entity_package].[Entity]#_removeReference[RelationshipName]` | `<app>.access_management.AccessRole#_removeReferenceAccessPermissions` |
| Set Reference | `[model_name].[entity_package].[Entity]#_setReference[RelationshipName]` | `<app>.access_management.AccessRole#_setReferenceAccessPermissions` |
| Custom Operation | `[model_name].[entity_package].[Entity]#[operationName]` | `<app>.entity_management.Entity#toggleStatus` |

**Finding Operation FQNs:**

```bash
# Search in ASM model for operation definitions
grep -r "operation name=" application/model/target/generated-resources/model/

# Use AsmUtils in code to resolve and log operation names
String opFqn = AsmUtils.getOperationFQName(operation);
log.info("Operation FQN: {}", opFqn);
```

## Using .default Template Files

The generator creates `.default` template files as **blueprints** for custom interceptors. These are starting point templates with commented example code.

**Important**: `.java.default` files are **NOT compiled** by Maven. They are blueprints that must be:
1. **Renamed** to `.java` extension to be compiled
2. **Customized** by implementing the method bodies and uncommenting relevant code

**Note**: The renamed `.java` files do NOT need to be added to `.generator-ignore` because the generator only creates `.default` files, never `.java` files. Your `.java` implementations are safe from regeneration. This is case 2 of the `.generator-ignore` rule (see backend [README.md](README.md#generator-ignore--one-rule) or [custom-operations.md](custom-operations.md#generator-ignore--one-rule)).

### Workflow: Using .default Templates

```bash
# 1. Find generated .default blueprint templates
find application/interceptors/src/main/java -name "*.java.default"

# 2. Copy/rename to remove .default extension
cp application/interceptors/src/main/java/[PACKAGE]/[InterceptorName].java.default \
   application/interceptors/src/main/java/[PACKAGE]/[InterceptorName].java

# 3. Edit the file - uncomment and implement the logic
vim application/interceptors/src/main/java/[PACKAGE]/[InterceptorName].java

# 4. Build and deploy
cd application/interceptors
mvn install
```

**Important Notes**:
- Do NOT edit `.java.default` files directly - they are regenerated on each build
- Do NOT add `.java` files to `.generator-ignore` - the generator only creates `.default` files, your `.java` implementations are never overwritten
- Do NOT add `.java.default` files to `.generator-ignore` either — keep them regenerating as a read-only reference. See [`.generator-ignore` — One Rule](README.md#generator-ignore--one-rule).
- Always work with the `.java` file after renaming

### Common .default Template Patterns

| Pattern | Purpose | Must Rename |
|---------|---------|-------------|
| `Log*Interceptor.java.default` | Blueprint for logging interceptors | ✅ Yes → `.java` |
| `*ValidationInterceptor.java.default` | Blueprint for validation logic | ✅ Yes → `.java` |
| `Custom*ServiceImpl.java.default` | Blueprint for custom service operations | ✅ Yes → `.java` |

**Note**: Specific blueprint files generated depend on your model definition. All `.default` files are templates only and will NOT be compiled until renamed to `.java`.

## See Also

- [Authentication Guide](authentication-guide.md) - For intercepting user authentication events.
- [Custom Operations](custom-operations.md) - For implementing the business logic that these interceptors wrap.
- [Patterns and Best Practices](patterns-and-best-practices.md) - For other common backend patterns.
