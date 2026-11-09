## Overview

The Initializer entity's `init` static operation is implemented as a custom Java class that seeds all reference data, the singleton Configuration entity, and the initial admin organization/user at application startup.

## Implementation Pattern

- The `InitCustomImplementation` class implements the generated `Init` operation interface and is registered as an OSGi `@Component`
- It injects multiple DAOs (`CityDao`, `PostalCodeDao`, `CapabilityDao`, `ConfigurationDao`, `OrganizationDao`, `UserDao`, etc.) via `@Reference` annotations
- The init method checks for idempotency (e.g., verifying Configuration doesn't already exist) before seeding
- Reference data is seeded in order: Cities with PostalCodes, Capabilities, Configuration singleton, and then the admin Organization with its admin User
- City-PostalCode relationships are established after creation using DAO `addPostalCodes()` methods
- The admin Organization is created with ACTIVE status and its first User is assigned the PLATFORM_ADMIN role
- A helper `LogoGenerator` class generates default logo images for the admin organization
- A variant pattern uses a delegation approach: `InitCustomImplementation` delegates to a separate `ExcelDataImporter` class that reads seed data from Excel spreadsheets rather than hardcoding values
- A multi-operation variant splits initialization into multiple named static operations (e.g., `initAdminUser`, `initDefaultIdm`) each as a separate OSGi `@Component`, rather than a single `init` operation

## Examples

### mlszksz-platform
- Key files: `custom/.../_default_transferobjecttypes/entities/initializer/InitCustomImplementation.java`, `custom/.../_default_transferobjecttypes/entities/initializer/LogoGenerator.java`
- Pattern: OSGi `@Component` implementing `Init` interface; injects 10+ DAOs for seeding Cities, PostalCodes, Capabilities, Configuration, Organization, User, and FeedEntry data
- Notable: Seeds ~250 Hungarian cities with postal codes, 20+ capabilities, a Configuration singleton with email templates and expiry settings, and the initial admin organization with a generated logo
- Idempotency: checks `configurationDao.query().selectOne().isPresent()` before seeding to prevent duplicate initialization

### rackinspect
- Key files: `custom/.../_default_transferobjecttypes/entities/initializer/InitCustomImplementation.java`, `ExcelDataImporter.java`, `ExcelDataReader.java`
- Pattern: OSGi `@Component` delegates to `ExcelDataImporter` which reads reference data from Excel files via Apache POI; injects 30+ DAOs covering currencies, countries, languages, units, payment methods, document registries, error codes, rack types, dimension templates, permissions, roles, users, and Configuration
- Notable: Uses an `ExcelDataReader` utility with merged-header support to import complex hierarchical data (e.g., dimension templates with groups and parameters) from spreadsheets
- Idempotency: The `ExcelDataImporter.run()` method checks existing data before seeding; also invokes `RecalculatePermissions` after creating users to synchronize denormalized permission booleans
- DI wiring: `InitCustomImplementation` acts as an OSGi bridge -- all `@Reference` setters forward to the `ExcelDataImporter` POJO, keeping OSGi concerns separate from import logic

### park-here
- Key files: `custom/.../_default_transferobjecttypes/entities/initializer/InitCustomImplementation.java`
- Pattern: OSGi `@Component` implementing `Init` interface; injects `InitializerDao`, `ParkingGarageDao`, `ParkingSlotDao`, `UserDao`, `ConfigurationDao`, and `FileStoreService`
- Notable: Seeds Configuration singleton with 4 email templates (doorman, deletion, modification, reminder) loaded from classpath HBS files via `FileStoreService`; creates 3 ParkingGarages (R1, R2, Canada) each with a garage-specific email template; creates 12+ ParkingSlots with floor, id, isExclusive, and floorPlan image associations; seeds 2 Doorman entries and 2 AdditionalDay calendar overrides
- Idempotency: checks `initializerDao.getAll().isEmpty()` and creates an Initializer marker entity at the end to prevent re-runs

### ubives
- Key files: `custom/.../_default_transferobjecttypes/entities/initializer/InitAdminUserCustomImplementation.java`, `custom/.../_default_transferobjecttypes/entities/initializer/InitDefaultIdmCustomImplementation.java`
- Pattern: Multi-operation variant -- two separate OSGi `@Component` classes each implementing a distinct initializer operation (`InitAdminUser` and `InitDefaultIdm`) rather than a single `init` method
- Notable: `InitAdminUserCustomImplementation` injects `AccountEntityDao`, `AccountPrincipalDao`, and `IdentityDao`; queries for an existing "admin" account using `StringFilter.equalTo`, and if not found, creates an `AccountPrincipal` with `isSuperAdmin=true` plus a linked `Identity` entity in a single nested builder call
- Idempotency: checks `accountDao.query().filterByUserName(StringFilter.equalTo("admin")).count() > 0` before seeding
- The second initializer (`InitDefaultIdm`) seeds the default Keycloak IDM server configuration and the platform-level "UBIVES" realm
