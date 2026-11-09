## Overview

Reference data lookup entities (City, PostalCode, Capability) are seeded by the Initializer's init operation and managed through a `MasterDataService` that handles CRUD operations and toggle-active. Admin custom operations for creating and updating reference data delegate to this shared service.

## Implementation Pattern

- The `MasterDataService` interface defines `createCity()`, `updateCity()`, `toggleCityActive()`, `createCapability()`, `updateCapability()`, `toggleCapabilityActive()` methods
- The `MasterDataServiceImpl` OSGi `@Component` injects `CityDao`, `PostalCodeDao`, `CapabilityDao` and validates uniqueness (e.g., duplicate city/capability names) before creating
- City creation also links PostalCodes via `cityDao.addPostalCodes()` after creation
- The Initializer seeds reference data in bulk: ~250 cities with postal code associations, 20+ capabilities with descriptions
- Custom operations: `CreateCityCustomImplementation` and `CreateCapabilityCustomImplementation` (AdminDashboard), `UpdateCityCustomImplementation` and `UpdateCapabilityCustomImplementation` (instance operations)
- All reference data operations log via `AuditLogService`
- In simpler variants (no dedicated management operations), lookup entities are consumed by product-creation operations via DAO `findAllById()` to resolve selected lookup items by identifier

## Examples

### mlszksz-platform
- Key files: `common/services/MasterDataService.java`, `common/services/impl/MasterDataServiceImpl.java`, `custom/.../admindashboard/CreateCityCustomImplementation.java`, `custom/.../admin/city/UpdateCityCustomImplementation.java`
- Pattern: Centralized `MasterDataService` for City and Capability CRUD; Initializer bulk-seeds reference data; dashboard-level create + instance-level update/toggle operations
- Notable: City-PostalCode many-to-many relationships are managed via DAO `addPostalCodes()` and `removeCities()` methods; PostalCode-City validation is reused across registration and organization address update flows

### alba
- Key files: `custom/.../services/adminproduct/CreateProductCustomImplementation.java`, `custom/.../services/authorproduct/CreateProductCustomImplementation.java`
- Pattern: No dedicated management operations for lookup entities (Audience, Curriculum, ResultType). Instead, `AudienceDao.findAllById()`, `CurriculumDao.findAllById()`, `ResultTypeDao.findAllById()` are called within product-creation custom operations to resolve user-selected lookup items by UUID
- Notable: Lookup entity names are aggregated into denormalized comma-separated strings (e.g., `audienceAggregated`, `curriculumAggregated`, `resultTypesAggregated`) using `stream().map(Audience::getName).sorted().collect(Collectors.joining(", "))` for display without joins
