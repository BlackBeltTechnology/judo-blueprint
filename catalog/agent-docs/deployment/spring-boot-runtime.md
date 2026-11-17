---
title: Running JUDO on Spring Boot
description: Spring Boot archetype, build plugin, autoconfiguration, test database selection and adding database dialects.
aliases: [spring boot setup, spring boot archetype, spring boot autoconfiguration, test database selection, add database dialect, build plugin configuration]
keywords: [transformerWorkflow, autoconfiguration, SDK DAO, Spring Boot, dialect]
tags: [domain:deployment, layer:infrastructure, status:platform]
---

# Running JUDO on Spring Boot

Besides the Karaf/OSGi runtime shipped by the fullstack project template, JUDO models can run in a Spring Boot application. This guide covers bootstrapping, wiring keys, model discovery and the database test fixtures. Examples use `<app>` for the model name.

## Bootstrapping a Spring Boot Project

A project can be generated from the Maven archetype `judo-jsl-springboot-archetype` (`maven-archetype-plugin:generate`). `modelName` is the only required parameter (regex `^[a-zA-Z0-9]+$`); `groupId` defaults to `com.example`, `artifactId` to the lower-cased model name, the package to `groupId.artifactId` and the main class to `<ModelName>Application`.

The generated project inherits from `hu.blackbelt.judo.jsl:judo-jsl-springboot` and must define two properties:

- `sdkPackagePrefix` - Java package of the generated SDK
- `modelName` - must match **exactly** the `.jsl` file name under `src/main/resources/model/` and the `model` declaration inside it. The name is interpolated into the generated-source path `target/generated-sources/model/sdk/<modelName>`; a mismatch yields an empty source root and a silent compile of nothing.

For custom-operation implementation projects there is the `judo-sdk-archetype` (started with `run-offline.sh` / `Run-Offline.ps1`, which start Karaf).

## Build Plugin Configuration (`transformerWorkflow`)

The build runs the goal `transformerWorkflow` of `judo-spring-maven-plugin` in `generate-sources`. Key parameters:

- `dialects` - auto-detected from project dependencies (`hsqldb` when `org.hsqldb:hsqldb` is present, `postgresql` when `org.postgresql:postgresql` is present); a user-set value overrides. HSQLDB takes precedence when both are present and one Liquibase master `liquibaseFile` is written.
- `sdkTemplateCartridges` - defaults to the `mvn:hu.blackbelt.judo.generator:judo-psm-generator-sdk-core-{common,api,impl,spring}` set (URL scheme `mvn:<groupId>:<artifactId>[:<extension>:<classifier>][:<version>][!path/in/archive]`).
- `sdkTemplateParameters` - `generateOptionalTypes=true`, `generatePayloadValidator=true`, `apiPrefix`/`implPrefix`/`springPrefix` derived from `sdkPackagePrefix`.
- `ignore*` trace flags (`ignoreJsl2Psm`, `ignorePsm2Asm`, `ignoreAsm2Rdbms`, `ignoreRdbms2Liquibase`, `ignoreAsm2Expression`, ...).
- Output defaults: `sources=src/main/resources/model`, `destination=target/generated-sources/model`, `sdkOutputDirectory=<destination>/sdk/<modelName>`; `modelName` is auto-set from the single root model when the project has no `judo-model-name` property.

## Application Wiring Keys

```properties
spring.datasource.url=jdbc:hsqldb:mem:<app>
spring.datasource.username=sa
spring.datasource.password=
spring.liquibase.change-log=classpath:model/<Model>-liquibase_hsqldb.changelog.xml
judo.modelName=<Model>
```

The application class is a plain `SpringApplication.run` main that can listen for `ApplicationReadyEvent`.

## Autoconfiguration and Model Discovery

The modules `judo-runtime-core-spring`, `-spring-hsqldb` and `-spring-postgresql` assemble the RDBMS runtime (DAO, dispatcher, query factory, variable resolver, identifier signer) without OSGi.

- The model is discovered from `judo.modelName` (default empty). If blank, the context scans `classpath*:/model/*.model` for a `*-asm.model` file; startup fails with `modelName is not set and could not be determined` when none is found.
- Dialect autoconfiguration is gated on the datasource URL containing `hsqldb` or `postgresql` (`@ConditionalOnExpression` on `spring.datasource.url`).
- The ANTLR runtime version check (< 3.5) runs unconditionally on startup.
- The signed-identifier secret behaves as on Karaf: without a configured `@IdentifierSignerSecret` binding a random key is generated on every start (see [Application Configuration](./application-config.md#5-identifier-signing)).

### SDK DAO autoconfiguration

The Spring part of the SDK generator emits one `@Configuration` class per model (`<Model>DaoModules` in the `springPrefix` package) with `@Autowired` DAO, `AsmModel` and `PayloadValidator` fields and one `@Bean` per DAO, static navigation and static data. It also writes `META-INF/spring.factories` and `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`, so the configuration registers itself when the SDK is on the classpath.

## Integration-Test Database Selection

The JUDO test fixtures select the database from system properties:

| Property | Values | Default |
|----------|--------|---------|
| `dialect` | `hsqldb`, `postgresql` | `hsqldb` |
| `container` | `none`, `yugabytedb` (only with `postgresql`) | `none` |
| `tz` | time zone id | `GMT` |

Any other dialect throws `IllegalStateException`. A YugabyteDB test container (`YugabytedbSQLContainer`, image `yugabytedb/yugabyte:2.1.8.2-b1`, PostgreSQL wire protocol, port 5433, default database/user/password `yugabyte`, overridable with `withDatabaseName` / `withUsername` / `withPassword`) is used with `-Dcontainer=yugabytedb`; PostgreSQL tests use Testcontainers.

**`initdatatests` are very long.** Run them only when the init data actually changes; they are not part of the normal baseline build and test cycle.

## Adding a New Database Dialect

JUDO ships only the `hsqldb` and `postgresql` dialect bundles. Another RDBMS needs: an implementation of the `Dialect` interface (`getName()`, `getDualTable()`), an `RdbmsParameterMapper` (or a subclass of `DefaultRdbmsParameterMapper`: String -> `VARCHAR(2000)`, Integer -> `NUMERIC(10,0)`, Long -> `NUMERIC(20,0)`, Boolean -> `BOOLEAN`, BigDecimal via `RdbmsDecimalType`), an `RdbmsInit` (`execute(DataSource)` creating the schema via Liquibase) and a function mapper whose `getFunctionBuilderMap()` maps function signatures to `MessageFormat` SQL patterns (an unregistered signature throws `UnsupportedOperationException: Unsupported function`). Dialects are resolved by name; an unknown name such as `oracle` throws `IllegalArgumentException`.

## Related Documentation

- [OSGi Runtime Services](./osgi-runtime-services.md)
- [Application Configuration](./application-config.md)
- [Build Process](./build-process.md)
