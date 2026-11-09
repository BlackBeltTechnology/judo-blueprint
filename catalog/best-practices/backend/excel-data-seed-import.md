---
id: excel-data-seed-import
title: Excel-Based Initial Data Seeding
description: An initialization custom operation that seeds the database with master data from Excel files on application startup.
aliases: []
keywords: [excel, based, initial, data, seeding, seed, import]
tags: ["domain:backend", "layer:backend", "project:rackinspect", "status:single-project"]
category: operation
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: [init-data-seeding]
related: [custom-operation-osgi-component, service-delegation-pattern, bulk-json-import-export, init-data-seeding]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

An initialization custom operation that seeds the database with master data from Excel files on application startup. An `InitCustomImplementation` OSGi component delegates to an `ExcelDataImporter` POJO that reads Excel spreadsheets and creates entities for countries, currencies, languages, permissions, roles, users, brands, dimension templates, error categories, rack types, and more. The OSGi component bridges 30+ DAO references to the POJO via setter injection.

## Structure

```java
@Component(immediate = true, service = Init.class)
public class InitCustomImplementation implements Init {
    // 30+ @Reference DAOs injected via setters
    @Reference public void setCountryDao(CountryDao dao) { importer.setCountryDao(dao); }

    private ExcelDataImporter importer = new ExcelDataImporter();

    @Override
    public void accept(Initializer _this) {
        importer.importAll();
    }
}

// POJO importer (testable without OSGi)
public class ExcelDataImporter {
    public void importAll() {
        importCountries();
        importCurrencies();
        importPermissions();
        importRoles();
        // ... 10+ import methods
    }
}
```

## Examples

### RackInspect
`InitCustomImplementation` bridges 30+ DAOs via setter `@Reference` methods to `ExcelDataImporter`. `ExcelDataReader` utility reads rows/cells from classpath Excel files. Imports: countries, currencies, languages, permissions, roles, users, brands, dimension templates, error categories/codes, rack types, repair types, items. Uses setter injection to bridge OSGi context to testable POJO.

## Trade-offs

- Pros: Non-technical users can prepare seed data in Excel, POJO importer is testable without OSGi, comprehensive initial data setup
- Cons: 30+ setter injections are verbose, Excel parsing adds dependency (Apache POI), no incremental update support
- Alternative: SQL scripts, Liquibase/Flyway migrations, JSON seed files, model-script-based init (see init-data-seeding), or database dump restore

## Related

- [[custom-operation-osgi-component]]
- [[service-delegation-pattern]]
- [[bulk-json-import-export]]
- [[init-data-seeding]]

