## Overview

The freight reservation cluster uses an interceptor-based backend pattern where the platform's built-in CRUD operations handle core entity lifecycle, and targeted `OperationCallInterceptor` implementations auto-wire actor-specific relations (e.g., partner association) during entity creation.

## Implementation Pattern

- No custom operation classes (`customImplementation: true`) are defined on the FreightReservation or related entities -- all CRUD is handled by the JUDO platform's standard dispatch
- A `PartnerActorInterceptor` (OSGi `@Component` implementing `OperationCallInterceptor`) intercepts specific actor-level create operations to augment the default CRUD behavior
- The interceptor targets `PartnerActor#_createInstanceReservationsForPartner` and uses `postCall` to auto-assign the partner relation after the platform creates the FreightReservation
- Actor identity resolution: `VariableResolver.resolve("ACTOR", "email")` retrieves the current user's email, then `UserDao.query().filterByEmail()` fetches the User entity, and `userDao.queryPartner()` with a `PartnerMask` retrieves the associated Partner
- Relation wiring: `FreightReservationDao.setPartner(fr, partner)` links the new reservation to the partner via the generated DAO's relation setter
- Reference data entities (Gate, Spot, VehicleType, LoadingType, LoadingTime, ProductCategory, Unit, StorageType) and organizational entities (Partner, Company, Project) are seeded by the `User.init` static operation using model expressions (not custom Java code)
- An `InterceptorOperationLogger` provides cross-cutting operation logging for debugging all intercepted operations

## Examples

### reserve-app
- Key files: `interceptors/services/PartnerActorInterceptor.java`, `interceptors/InterceptorOperationLogger.java`
- Pattern: Interceptor-based post-creation wiring -- the `PartnerActorInterceptor` hooks into the partner actor's reservation create operation to auto-link the current user's partner entity to the new FreightReservation. Uses `FreightReservationDao`, `UserDao`, and `VariableResolver` injected via OSGi `@Reference`.
- Notable: The interceptor uses `getOperations()` to register for specific operations by FQN string (`ReserveApp.services.PartnerActor#_createInstanceReservationsForPartner`), and `AsmUtils.resolveOperation()` to resolve the operation from the model at startup. The `postCall` handler casts `parameterPayload` to `CreateInstanceCall.CreateInstanceCallPayload` and `returnPayload` to `Payload` to extract the created entity.
- DI wiring: `UserDao`, `FreightReservationDao`, and `VariableResolver` injected via `@Reference`; `@Component(property = "judo.model.name=ReserveApp")` binds the interceptor to the correct model.
