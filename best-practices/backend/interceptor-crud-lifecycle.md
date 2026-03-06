---
id: "interceptor-crud-lifecycle"
title: "Interceptor as CRUD Lifecycle Hook"
domain: "backend"
category: "interceptor"
score: 58.4
usage_count: 5
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - alba
  - park-here
  - judo-partner
  - reserve-app
---
## Description

Interceptors that hook into the generated CRUD operations (_createInstance, _updateInstance, _deleteInstance) to add cross-cutting behavior that the framework cannot express in the model. Common uses: setting singular reference relations after create, validating format constraints in preCall, cascading updates in postCall, and transforming flat form fields into nested structures.

## Structure

```java
@Component(property = { "judo.model.name=appname" })
public class EntityCreateInterceptor implements OperationCallInterceptor {
    @Reference EntityDao entityDao;
    @Reference ParentDao parentDao;

    @Override
    public Collection<EOperation> getOperations(AsmModel asmModel) {
        // Target specific CRUD operations
        return List.of(asmUtils.resolveOperation(
            "app.actors.Actor#_createInstanceChildren").orElseThrow());
    }

    @Override
    public Object preCall(EOperation op, Object payload) {
        // Validate before CRUD executes
        CreateInstanceCallPayload create = (CreateInstanceCallPayload) payload;
        Payload input = create.getInput();
        // Validate, transform input...
        return OperationCallInterceptor.super.preCall(op, payload);
    }

    @Override
    public Object postCall(EOperation op, Object paramPayload, Object returnPayload) {
        // Set relations, cascade updates after CRUD
        Payload created = (Payload) returnPayload;
        UUID id = created.getAs(UUID.class, "__identifier");
        // Set relations, trigger validation...
        return OperationCallInterceptor.super.postCall(op, paramPayload, returnPayload);
    }
}
```

## Examples

### RackInspect
38 interceptors organized by domain. `PartnerCreateInterceptor` validates headquarters address in preCall, transforms 15+ flat `form_*` fields into nested Address payload, then sets headquarters/billing/postal relations in postCall. `BankAccountCreateAndUpdateInterceptor` validates account number format via regex in preCall, sets primary relation in postCall.

### ALBA
`AdminUserCreateInterceptor` intercepts `_createInstanceAdminProfiles` in preCall, extracts profile data from `AdminAuthorProfile`, creates a `UserTransfer` entity, and uses `ignoreDecoratedCall()=true` to completely replace the original create operation. `ProductUpdateInterceptor` hooks into `_updateInstance` postCall to recompute aggregated string fields.

### ParkHere
`CarUpdateInstanceInterceptor` intercepts `Car#_updateInstanceParkHere_services_Car` in postCall to validate and enforce favorite car settings. After a car is updated, if the favorite flag is set, it calls `carService.setFavoriteCarWithValidationException()` to ensure only one car per user is marked as favorite. Uses `ValidationException` for immediate UI feedback.

### judo-partner
`PartnerUpdateInterceptor` intercepts `Partner#_updateInstancePartner_partner_Partner` in postCall. After every partner update: corrects company name format, normalizes name for duplicate detection, validates tax identifier uniqueness, re-validates against NAV, recalculates `isDuplicateName` flags across all partners with the same normalized name, and creates a `PartnerLog` audit entry with `LogType.UPDATE`.

### ReserveApp
`PartnerActorInterceptor` intercepts `PartnerActor#_createInstanceReservationsForPartner` in postCall. After a partner-role user creates a FreightReservation, resolves the current user via `VariableResolver`, navigates to their Partner entity via `userDao.queryPartner()`, and sets the partner relation on the new reservation via `freightReservationDao.setPartner()`. Demonstrates ownership assignment via postcall enrichment.

## Trade-offs

- Pros: Extends generated CRUD without modifying generated code, cross-cutting concerns centralized, supports complex post-creation wiring
- Cons: Interceptors interact with raw Payload objects (less type-safe than custom operations), harder to debug, order dependency between interceptors
- Alternative: Custom operations that wrap CRUD logic entirely (more control but more boilerplate)

## Related Patterns

- interceptor-global-logging
- interceptor-access-control-flags
- interceptor-range-override
- form-field-flattening
