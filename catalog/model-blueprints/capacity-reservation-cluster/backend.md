## Overview

Platform facts: an `OperationCallInterceptor` fires only for built-in operations such as create, update, delete, list and set/add/remove reference. Custom and script operations are never intercepted; built-in operations on a mapped type are. A create on an actor's collection is built-in, so it can be intercepted. `postCall` receives the input payload and the return payload; the value it returns becomes the result. Synchronous interceptors run in the operation's transaction, so an exception rolls the write back. The classes and names below (`PartnerActorInterceptor`, `InterceptorOperationLogger`, the reservation and user DAOs) are reference implementation code, not platform classes.

The capacity reservation cluster uses an interceptor-based backend pattern where the platform's built-in CRUD operations handle core entity lifecycle, and targeted `OperationCallInterceptor` implementations auto-wire actor-specific relations (e.g., partner association) during entity creation.

## Implementation Pattern

- No custom operation classes (`customImplementation: true`) are defined on the CapacityReservation or related entities -- all CRUD is handled by the JUDO platform's standard dispatch
- A `PartnerActorInterceptor` (OSGi `@Component` implementing `OperationCallInterceptor`) intercepts specific actor-level create operations to augment the default CRUD behavior
- The interceptor targets `PartnerActor#_createInstanceReservationsForPartner` and uses `postCall` to auto-assign the partner relation after the platform creates the CapacityReservation
- Actor identity resolution: `VariableResolver.resolve(String.class, "ACTOR", "email")` retrieves the current user's email, then `UserDao.query().filterByEmail()` fetches the User entity, and `userDao.queryPartner()` with a `PartnerMask` retrieves the associated Partner
- Relation wiring: `CapacityReservationDao.setPartner(reservation, partner)` links the new reservation to the partner via the generated DAO's relation setter
- Reference data entities (Dock, Slot, ResourceType, HandlingType, TimeWindow, ProductCategory, Unit, StorageType) and organizational entities (Partner, Company, Project) are seeded by the `User.init` static operation using model expressions (not custom Java code)
- An `InterceptorOperationLogger` provides cross-cutting operation logging for debugging all intercepted operations

## Examples

### Variant seen in practice
- Pattern: Interceptor-based post-creation wiring -- the `PartnerActorInterceptor` hooks into the partner actor's reservation create operation to auto-link the current user's partner entity to the new CapacityReservation. Uses `CapacityReservationDao`, `UserDao`, and `VariableResolver` injected via OSGi `@Reference`.
- Notable: The interceptor uses `getOperations()` to register for specific operations by FQN string (`App.services.PartnerActor#_createInstanceReservationsForPartner`), and `AsmUtils.resolveOperation()` to resolve the operation from the model at startup. The `postCall` handler casts `parameterPayload` to `CreateInstanceCall.CreateInstanceCallPayload` and `returnPayload` to `Payload` to extract the created entity.
- DI wiring: `UserDao`, `CapacityReservationDao`, and `VariableResolver` injected via `@Reference`; `@Component(property = "judo.model.name=App")` binds the interceptor to the correct model.
