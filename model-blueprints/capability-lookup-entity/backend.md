## Overview

The Capability entity is managed through a `MasterDataService` OSGi service that handles creation, update, and toggle operations. Custom operations on the admin Capability transfer object delegate to this shared service. The Initializer seeds initial capabilities at application startup.

## Implementation Pattern

- A `MasterDataService` interface defines `createCapability()`, `updateCapability()`, and `toggleCapabilityActive()` methods
- Custom operation classes (`ActivateToggleCustomImplementation`, `UpdateCapabilityCustomImplementation`, `CreateCapabilityCustomImplementation`) are thin OSGi `@Component` wrappers that inject `@Reference MasterDataService` and delegate
- The `CreateCapabilityCustomImplementation` lives in the `admindashboard` package (dashboard-level operation), while toggle and update live in the `capability` package (instance-level operations)
- The Initializer's `init()` method seeds capabilities using `CapabilityDao.create(CapabilityForCreate.builder()...)`

## Examples

### mlszksz-platform
- Key files: `custom/.../admindashboard/CreateCapabilityCustomImplementation.java`, `custom/.../capability/ActivateToggleCustomImplementation.java`, `custom/.../capability/UpdateCapabilityCustomImplementation.java`, `common/services/MasterDataService.java`
- Pattern: Dashboard-level create operation + instance-level toggle/update operations, all delegating to `MasterDataService`
- Notable: The same `MasterDataService` manages both City and Capability entities, providing a unified master data management layer
