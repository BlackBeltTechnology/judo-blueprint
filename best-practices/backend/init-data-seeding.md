---
id: "init-data-seeding"
title: "Application Init Data Seeding Operation"
domain: "backend"
category: "operation"
score: 66.2
usage_count: 8
alternative_count: 1
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - itracker
  - mlszksz-platform
  - viterra_demo
  - judo-demo-miniworkflow
  - ubives
  - park-here
  - InterfaceRegister
  - doors-model
alternatives:
  - excel-data-seed-import
---
## Description

An `Init` operation on a singleton `Application` entity that seeds the database with essential reference data on first startup. The operation creates lookup entities (categories, regions, roles) and initial user accounts. This pattern bootstraps the application so it is usable immediately after deployment without manual data entry. Can be implemented via model scripts (simple cases) or custom Java with Excel import (complex cases).

## Structure

Model-script approach (simple):
```
// Init operation on Application entity
new Category(name = "Category A")
new Category(name = "Category B")
new Region(name = "Europe")
new Region(name = "US")
new User(name = "Admin", email = "admin@example.com", isAdmin = true)
```

Custom Java approach (complex -- see excel-data-seed-import):
```java
@Component(immediate = true, service = Init.class)
public class InitCustomImplementation implements Init {
    @Reference CategoryDao categoryDao;
    @Override
    public void accept(Initializer _this) {
        categoryDao.create(CategoryForCreate.builder().withName("Category A").build());
        // ...
    }
}
```

The operation uses the `Runnable` functional pattern (`void run()`) with no input or output.

## Examples

### itracker
`InitCustomImplementation` (model-script-driven, not custom Java) seeds 3 SRT categories ("SRT-MRO/SER", "SRT-Labor", "Non-SRT"), 2 regions ("Europe", "US"), and 3 users with different roles (1 finance user, 2 regular users with email addresses). Simple and sufficient for a small reference data set.

### mlszksz-platform
`InitCustomImplementation` generates default platform logos using `LogoGenerator` helper class and initializes platform configuration. Custom Java implementation rather than model scripts. Bootstraps the platform so it is visually branded from first startup.

### viterra_demo
`InitCustomImplementation.java.default` stub with extensive sample data documented in Javadoc comments: 7 Commodities (agricultural products), 4 Silos (storage locations), 4 Periods (monthly reporting windows Feb-May 2024), 2 Clients, 4 Reports with different statuses (SUBMITTED/PENDING), and multiple Stock entries per report with quantities, quality metrics (moisture, temperature, infestation), and ISCC certification data.

### judo-demo-miniworkflow
`InitUsersCustomImplementation` seeds 2 default users with idempotency guards: Admin (admin@example.org, approver + admin + active) and Demo User (user@example.org, approver + active, not admin). Uses `exists()` check before creation to prevent duplicates. Signature is `void run()` with no parameters. Callable via REST endpoint for bootstrap.

### Ubives
Two init operations: `InitAdminUserCustomImplementation` creates default admin with `AccountPrincipal` (isSuperAdmin=true, email="test@judo.it") and linked `Identity` entity, with `count() > 0` idempotency guard. `InitDefaultIdmCustomImplementation` creates default IDM configuration with URL "http://localhost:8080/". Both use `void run()` signature.

### ParkHere
Complex multi-step init: (1) stores 4 email templates (Handlebars `.html.hbs` files) in FileStore, (2) creates Configuration with template references and contact/sender email, (3) creates additional days (holidays), (4) stores per-garage email templates, (5) creates 3 parking garages, (6) creates doormen with garage assignments, (7) stores floor plan images, (8) creates parking slots with floor plans. Uses `initializerDao.getAll().isEmpty()` idempotency guard. Injects 6 DAOs and FileStoreService.

### InterfaceRegister
4 separate init operations: `InitBrandsCustomImplementation`, `InitBusinessDataTypesCustomImplementation`, `InitUsersCustomImplementation`, `InitVendorsCustomImplementation`. Each is a parameterless void method (e.g., `void initBrands()`). All remain as `.java.default` stubs. Demonstrates the pattern of splitting init seeding into multiple focused operations per reference data domain rather than a single monolithic Init.

### doors-model
Massive seed data initialization via `ContractType.init` (static custom operation) and `Initializer.init` (versioned migration). ContractType init creates ~170 contract types with associated financial and legal categories. Initializer uses a numbered migration pattern (`executedInitialization` counter) with 7 incremental steps (init1_legacy through init7_addDivisionTestingPositions) to safely apply seed data changes, preventing re-execution. Seeds ~90 financial categories, ~24 legal groups, ~50 divisions, ~60 banks, and real employee data.

## Trade-offs

- Pros: Application is immediately usable after deployment, reference data is version-controlled in the model, simple for small data sets
- Cons: No idempotency guard (running twice creates duplicates unless handled), hardcoded data in model/code, not suitable for large data sets
- Alternative: Excel-based import (see `excel-data-seed-import`) for large reference data, SQL migration scripts, or external data loading tools

## Related Patterns

- excel-data-seed-import
- script-driven-operations
- custom-operation-osgi-component
