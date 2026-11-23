---
title: Integration Testing - Getting Started Guide
description: "Target Audience: Beginners, new developers starting with JUDO integration tests"
aliases: [first integration test, junit setup, run integration tests, transaction handling in tests, test table truncation, beginner integration testing, integration-test pom empty version, i18n-api version missing, integration-test module build fails]
keywords: [@JudoTest, JudoRuntimeFixture, ReferenceInjector, TransactionHandling, truncateTables, AUTO_ROLLBACK, AUTO_COMMIT, MANUAL, mvn clean test, logback-test.xml, maven-surefire-plugin, i18n-api, integration-test pom]
tags: [domain:testing, layer:test, status:platform]
---
# Integration Testing - Getting Started Guide

**Target Audience**: Beginners, new developers starting with JUDO integration tests

**Prerequisites**: Basic understanding of Java, JUnit, and the JUDO framework

For other topics, see the [Integration Testing Documentation Hub](./README.md).

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Dependencies](#dependencies)
3. [Testing Fundamentals](#testing-fundamentals)
4. [Writing Your First Tests](#writing-your-first-tests)
5. [Running Tests](#running-tests)

---

## Project Structure

The integration test module follows a standard Maven project structure:

```
application/integration-test/
├── pom.xml                                    # Maven configuration
├── src/
│   └── test/
│       ├── java/
│       │   └── [your/package]/[yourmodel]/integration/
│       │       ├── dao/                       # DAO-layer tests
│       │       │   ├── EntityDaoTest.java
│       │       │   └── ...
│       │       ├── service/                   # Service-layer tests
│       │       │   ├── EntityServiceTest.java
│       │       │   └── ...
│       │       ├── custom/                    # Custom operation tests
│       │       │   ├── CreateOperationTest.java
│       │       │   └── ...
│       │       └── utils/                     # Test utilities
│       │           ├── VariableResolverMockHelper.java
│       │           ├── AddressTestFixtures.java
│       │           └── ...
│       └── resources/
│           └── logback-test.xml               # Test logging configuration
└── .classpath                                 # Eclipse project configuration
```

### Key Directories

- **`dao/`**: Tests for Data Access Objects - direct database operations
- **`service/`**: Tests for service-layer operations - business logic with type conversions
- **`custom/`**: Tests for custom operations (computed attributes, event handlers, validations)
- **`utils/`**: Reusable test fixtures and helper classes

---

## Dependencies

### Core JUDO Dependencies

```xml
<dependency>
    <groupId>hu.blackbelt.judo.runtime</groupId>
    <artifactId>judo-runtime-core-guice-testkit</artifactId>
    <version>${judo-runtime-core-version}</version>
    <scope>test</scope>
</dependency>
```

This provides:
- `@JudoTest` annotation
- `JudoRuntimeFixture` for accessing DAOs
- Transaction management utilities

### Project Dependencies

```xml
<dependency>
    <groupId>[your.package]</groupId>
    <artifactId>[yourmodel]-model</artifactId>
    <version>${project.version}</version>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>[your.package]</groupId>
    <artifactId>[yourmodel]-service</artifactId>
    <version>${project.version}</version>
    <scope>test</scope>
</dependency>
```

Platform libraries that the app module declares with `provided` scope (for example PDFBox) are not on the integration-test class path, because provided dependencies are not passed on to other modules. A test that uses such a library fails with `NoClassDefFoundError`. Declare the same artifact in the integration-test module with `provided` scope as well. The generated integration-test pom has no dependency fragment, so keep the edit under generator-ignore control (see [generator-ignore config protection](../../best-practices/backend/generator-ignore-config-protection.md)).

### Testing Dependencies

```xml
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>

<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <scope>test</scope>
</dependency>
```

### Logging Dependencies

```xml
<dependency>
    <groupId>ch.qos.logback</groupId>
    <artifactId>logback-classic</artifactId>
    <scope>test</scope>
</dependency>
```

### Maven Surefire Plugin

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>3.2.5</version>
    <configuration>
        <includes>
            <include>**/*Test.java</include>
            <include>**/*IntegrationTest.java</include>
        </includes>
    </configuration>
</plugin>
```

---

## Testing Fundamentals

### The `@JudoTest` Annotation

All JUDO integration tests must be annotated with `@JudoTest`. This annotation:

1. **Sets up the test environment**: Initializes JUDO runtime, DAOs, and dependency injection
2. **Manages transactions**: Controls how transactions are handled during tests
3. **Truncates tables**: Optionally cleans up database tables after a test (only in `AUTO_COMMIT` and `MANUAL` mode)

### Basic Test Structure

```java
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoTest;
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoRuntimeFixture;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

@JudoTest
public class MyFirstIntegrationTest {

    @Test
    public void testSomething(JudoRuntimeFixture fixture) {
        // Your test code here
        // fixture.getInjector() provides access to DAOs and services
    }
}
```

### `@JudoTest` Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `transaction` | `TransactionHandling` | `AUTO_ROLLBACK` | Controls transaction behavior |
| `truncateTables` | `boolean` | `true` | Whether to truncate tables **after** each test; applies only to `AUTO_COMMIT` and `MANUAL` (`AUTO_ROLLBACK` never truncates, rollback does the cleanup) |
| `modelName` | `String` | `"example"` | Name of the model to load |
| `dialect` | `String` | `"hsqldb"` | `hsqldb` or `postgresql`; overridden by env `JUDO_TEST_DIALECT` |
| `container` | `String` | `"none"` | `none`, `postgresql`, `yugabytedb`; overridden by env `JUDO_TEST_CONTAINER` |
| `modelSource` | `ModelSource` | `AUTO` | `AUTO` (filesystem, then classpath), `FILESYSTEM`, `CLASSPATH` |
| `modules` | `Class<? extends Module>[]` | `{}` | Extra Guice modules (public no-arg constructor) |
| `dataSourceMode` | `DataSourceMode` | `BY_METHOD` | `BY_METHOD`, `BY_CLASS`, `SINGLETON` (datasource lifecycle) |
| `shareInjector` | `boolean` | `false` | Reuse the Guice injector across the methods of a class (with `BY_CLASS`/`SINGLETON`). Derived test artifacts are reused across methods only when this is `true`; the default `false` rebuilds them |
| `interceptors` | `Class<? extends OperationCallInterceptor>[]` | `{}` | Interceptors registered for the test |

With `dialect` `postgresql`, `container` `none` and `postgresql` start a PostgreSQL container, and `yugabytedb` starts a YugabyteDB container. Any other value creates no container, and datasource setup then fails. With `dialect` `hsqldb` the `container` value is not used.

The yugabytedb container's liveness check is built with the wrong constructor and is effectively empty. Do not rely on the liveness check for yugabytedb tests.

### Transaction Handling Modes

The `transaction` parameter accepts the following values:

#### 1. `AUTO_ROLLBACK` (Default)

```java
@JudoTest(transaction = TransactionHandling.AUTO_ROLLBACK)
public class MyTest {
    // Transactions automatically roll back after each test
}
```

##### Behavior
- Transaction starts before test method
- Transaction rolls back after test method (success or failure)
- Database remains clean between tests

##### Use when
- You want test isolation
- You don't need to verify post-commit behavior
- Most common mode for unit-style integration tests

#### 2. `AUTO_COMMIT`

```java
@JudoTest(transaction = TransactionHandling.AUTO_COMMIT)
public class MyTest {
    // Transactions automatically commit after each test
}
```

##### Behavior
- Transaction starts before test method
- Transaction commits after successful test
- Transaction rolls back only on test failure

##### Use when
- You need to verify data persistence
- Testing cascading operations
- Verifying post-commit triggers

**Warning**: Committed data stays until it is truncated; keep `truncateTables = true` (default) or clean up manually

#### 3. `MANUAL`

```java
@JudoTest(transaction = TransactionHandling.MANUAL)
public class MyTest {
    @Test
    public void testWithManualControl(JudoRuntimeFixture fixture) {
        fixture.beginTransaction();
        try {
            // Your test logic
            fixture.commitTransaction();
        } catch (Exception e) {
            fixture.rollbackTransaction();
            throw e;
        }
    }
}
```

##### Behavior
- No automatic transaction management
- You control `beginTransaction()`, `commitTransaction()`, and `rollbackTransaction()` on the `JudoRuntimeFixture`

##### Use when
- Testing complex multi-transaction scenarios
- Verifying transaction boundary behavior
- Testing error recovery

#### 4. `NONE`

```java
@JudoTest(transaction = TransactionHandling.NONE)
public class MyTest {
    // No transaction management at all
}
```

##### Behavior
- No transactions created by framework
- Each DAO/service operation may run in its own transaction

##### Use when
- Testing read-only operations
- Testing transaction-less operations
- Performance testing without transaction overhead

**Warning**: Many operations will fail without transactions

### Table Truncation Behavior

```java
@JudoTest(truncateTables = true)  // Default
public class MyTest {
    // All tables are truncated AFTER each test method
    // (only with AUTO_COMMIT or MANUAL; AUTO_ROLLBACK never truncates)
}

@JudoTest(truncateTables = false)
public class MyTest {
    // Tables are NOT truncated - data persists between tests
}
```

`AUTO_ROLLBACK` ignores `truncateTables`: the rollback is the cleanup, tables are never truncated. In `MANUAL` mode tables are truncated after the test even if you committed nothing. In `NONE` mode nothing is cleaned.

#### When to disable truncation
- Tests require expensive setup data
- Testing data migration scenarios
- Debugging - want to inspect data after test

**Warning**: Disabling truncation can cause test interdependencies

---

## Writing Your First Tests

### Pattern 1: Simple DAO Test

This is the simplest integration test pattern - testing Data Access Object operations directly.

```java
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoTest;
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoRuntimeFixture;
import org.junit.jupiter.api.Test;

import [your.package].[yourmodel].api.[yourmodel]._default_transferobjecttypes.entity.user.User;
import [your.package].[yourmodel].api.[yourmodel]._default_transferobjecttypes.entity.user.UserDao;
import [your.package].[yourmodel].api.[yourmodel]._default_transferobjecttypes.entity.user.UserForCreate;

import static org.junit.jupiter.api.Assertions.*;

@JudoTest
public class UserDaoTest {

    @Test
    public void testCreateUser(JudoRuntimeFixture fixture) {
        // 1. Get the DAO from the fixture
        UserDao userDao = fixture.getInjector().getInstance(UserDao.class);

        // 2. Create a new entity using the ForCreate builder
        User createdUser = userDao.create(UserForCreate.builder()
                .withUserName("testuser")
                .withEmail("admin@example.com")
                .withIsActive(true)
                .build());

        // 3. Verify the creation
        assertNotNull(createdUser);
        assertNotNull(createdUser.identifier());
        assertEquals("testuser", createdUser.getUserName());
        assertEquals("admin@example.com", createdUser.getEmail());
        assertTrue(createdUser.getIsActive());

        // 4. Verify it's in the database
        assertTrue(userDao.getById(createdUser.identifier()).isPresent());
    }

    @Test
    public void testUpdateUser(JudoRuntimeFixture fixture) {
        UserDao userDao = fixture.getInjector().getInstance(UserDao.class);

        // Create initial entity
        User user = userDao.create(UserForCreate.builder()
                .withUserName("original")
                .withEmail("admin@example.com")
                .withIsActive(true)
                .build());

        // Update the entity
        user.setEmail("admin@example.com");
        userDao.update(user);

        // Verify the update
        User fetched = userDao.getById(user.identifier()).orElseThrow();
        assertEquals("admin@example.com", fetched.getEmail());
    }

    @Test
    public void testDeleteUser(JudoRuntimeFixture fixture) {
        UserDao userDao = fixture.getInjector().getInstance(UserDao.class);

        // Create entity
        User user = userDao.create(UserForCreate.builder()
                .withUserName("todelete")
                .withEmail("admin@example.com")
                .withIsActive(true)
                .build());

        // Delete it
        userDao.delete(user);

        // Verify deletion
        assertFalse(userDao.getById(user.identifier()).isPresent());
    }
}
```

#### Key Points
- Use `fixture.getInjector().getInstance(DaoClass.class)` to get DAOs
- Use `EntityForCreate.builder()` to create entities
- Use `identifier()` to get entity identifiers for queries
- Default `AUTO_ROLLBACK` transaction cleans up after each test

---

### Pattern 2: Testing Custom Operations with ReferenceInjector

When testing custom operations (business logic), you need to instantiate the custom implementation class with its dependencies injected.

```java
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoTest;
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoRuntimeFixture;
import hu.blackbelt.judo.runtime.core.guice.testkit.util.ReferenceInjector;
import org.junit.jupiter.api.Test;

import [your.package].[yourmodel].api.[yourmodel]._default_transferobjecttypes.entity.user.User;
import [your.package].[yourmodel].api.[yourmodel]._default_transferobjecttypes.entity.user.UserDao;
import [your.package].[yourmodel].api.[yourmodel]._default_transferobjecttypes.entity.user.UserForCreate;
import [your.package].[yourmodel].api.[yourmodel]._default_services.entity.complexentity.ComplexEntityForCreate;
import [your.package].[yourmodel].service.[yourmodel]._default_services.entity.complexentity.CreateComplexEntityCustomImplementation;

import static org.junit.jupiter.api.Assertions.*;

@JudoTest
public class CreateComplexEntityTest {

    @Test
    public void testCreateComplexEntity(JudoRuntimeFixture fixture) {
        // 1. Get required DAOs
        UserDao userDao = fixture.getInjector().getInstance(UserDao.class);

        // 2. Create prerequisite entities
        User user = userDao.create(UserForCreate.builder()
                .withUserName("testuser")
                .withEmail("admin@example.com")
                .withIsActive(true)
                .build());

        // 3. Instantiate custom operation with dependency injection
        CreateComplexEntityCustomImplementation createOperation = 
            ReferenceInjector.createAndInject(
                CreateComplexEntityCustomImplementation.class,
                fixture.getInjector()
            );

        // 4. Create the input transfer object
        ComplexEntityForCreate input = ComplexEntityForCreate.builder()
                .withSomeField("test value")
                .withRelatedUser(user)
                .build();

        // 5. Execute the custom operation
        createOperation.customCall(input);

        // 6. Verify the result
        // (Verification depends on what the operation does)
    }
}
```

#### Key Points
- Use `ReferenceInjector.createAndInject(CustomClass.class, fixture.getInjector())` to instantiate custom operations
- `ReferenceInjector` (`hu.blackbelt.judo.runtime.core.guice.testkit.util`) injects by **type**: every non-static, non-final field (and every single-argument `set*` method) whose type the Guice injector can provide is filled. It does not read `@Reference` / `@Inject`, because OSGi's `@Reference` has CLASS retention and is invisible to reflection. Use `createAndInject(Class, injector)` to create and wire an instance, `injectReferences(instance, injector)` for an existing one
- Create all prerequisite entities before calling custom operations
- Custom operations may modify the input or create new entities

---

### Pattern 3: Manual Transaction Control

For complex scenarios requiring multiple transaction boundaries:

```java
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoTest;
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoRuntimeFixture;
import hu.blackbelt.judo.runtime.core.guice.testkit.fixture.JudoTest.TransactionHandling;
import org.junit.jupiter.api.Test;

import [your.package].[yourmodel].api.[yourmodel]._default_transferobjecttypes.entity.user.User;
import [your.package].[yourmodel].api.[yourmodel]._default_transferobjecttypes.entity.user.UserDao;
import [your.package].[yourmodel].api.[yourmodel]._default_transferobjecttypes.entity.user.UserForCreate;

import static org.junit.jupiter.api.Assertions.*;

@JudoTest(transaction = TransactionHandling.MANUAL)
public class MultiTransactionTest {

    @Test
    public void testMultipleTransactions(JudoRuntimeFixture fixture) {
        UserDao userDao = fixture.getInjector().getInstance(UserDao.class);

        // Transaction 1: Create user
        fixture.beginTransaction();
        User user1 = null;
        try {
            user1 = userDao.create(UserForCreate.builder()
                    .withUserName("user1")
                    .withEmail("admin@example.com")
                    .withIsActive(true)
                    .build());
            fixture.commitTransaction();
        } catch (Exception e) {
            fixture.rollbackTransaction();
            throw e;
        }

        // Verify user1 is persisted
        fixture.beginTransaction();
        try {
            assertTrue(userDao.getById(user1.identifier()).isPresent());
            fixture.commitTransaction();
        } catch (Exception e) {
            fixture.rollbackTransaction();
            throw e;
        }

        // Transaction 2: Create second user
        fixture.beginTransaction();
        try {
            User user2 = userDao.create(UserForCreate.builder()
                    .withUserName("user2")
                    .withEmail("admin@example.com")
                    .withIsActive(true)
                    .build());
            fixture.commitTransaction();

            // Both users should exist
            fixture.beginTransaction();
            assertEquals(2, userDao.query().selectList().size());
            fixture.commitTransaction();
        } catch (Exception e) {
            fixture.rollbackTransaction();
            throw e;
        }
    }

    @Test
    public void testRollbackBehavior(JudoRuntimeFixture fixture) {
        UserDao userDao = fixture.getInjector().getInstance(UserDao.class);

        // Transaction that will be rolled back
        fixture.beginTransaction();
        try {
            userDao.create(UserForCreate.builder()
                    .withUserName("rollbackuser")
                    .withEmail("admin@example.com")
                    .withIsActive(true)
                    .build());

            // Intentionally rollback
            fixture.rollbackTransaction();
        } catch (Exception e) {
            fixture.rollbackTransaction();
            throw e;
        }

        // Verify user was NOT persisted
        fixture.beginTransaction();
        try {
            assertEquals(0, userDao.query().selectList().size());
            fixture.commitTransaction();
        } catch (Exception e) {
            fixture.rollbackTransaction();
            throw e;
        }
    }
}
```

#### Transaction rules

##### Key Points
- Always wrap operations in `beginTransaction()` / `commitTransaction()` / `rollbackTransaction()` blocks
- Calling `beginTransaction()` while a transaction is still open throws `IllegalStateException`: 'Previous transaction was not completed'. Commit or roll back the open transaction first.
- Use try-catch to ensure rollback on exceptions
- Each transaction boundary is explicit and controlled
- Useful for testing transaction isolation and consistency
- `JudoRuntimeFixture.tearDown()` only rolls back a transaction that is still open. It does not close the injector or the datasource, so close the datasource yourself (for example in `@AfterEach`) when a test manages its own datasource.

---

## Running Tests

The `application/integration-test` module is not listed in `application/pom.xml`, so `mvn -pl application/integration-test` from the project root fails with `Could not find the selected project in the reactor`. Run Maven from the module directory:

```bash
cd application/integration-test
```

### Known Issue: empty `i18n-api` version

The generated `application/integration-test/pom.xml` declares `hu.blackbelt.osgi.i18n:i18n-api` with `<version></version>`. The generator never sets the `osgiI18nApiVersion` template variable, so the value is empty and Maven fails to resolve the dependency. Before running the tests, set the version explicitly to the `i18n-api` version your platform release uses, then run the commands below.

### Run All Integration Tests

```bash
mvn clean test
```

### Run Specific Test Class

```bash
mvn clean test -Dtest=UserDaoTest
```

### Run Specific Test Method

```bash
mvn clean test -Dtest=UserDaoTest#testCreateUser
```

### Run with Debug Logging

Edit `src/test/resources/logback-test.xml`:

```xml
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <root level="DEBUG">
        <appender-ref ref="STDOUT" />
    </root>
</configuration>
```

Then run:

```bash
mvn clean test
```

### Model Load Errors

With `modelSource` `AUTO`, a model that cannot be loaded from the filesystem or the classpath fails with `Could not load model '<name>'. Filesystem error: ... Classpath error: ...`. Check the model name and that the model artifact is on the test classpath.

### Skip Tests During Build

```bash
mvn clean install -DskipTests
```

---

## Next Steps

Now that you understand the basics, explore more advanced topics:

- **[Type Safety Guide](./type-safety.md)**: Deep dive into Entity vs Service layer types and `adaptTo()` conversions
- **[Advanced Patterns](./advanced-patterns.md)**: VariableResolver mocking, Optional field handling, entity reference validation
- **[Best Practices](./best-practices.md)**: Patterns, anti-patterns, and maintainable test design

Return to the [Integration Testing Documentation Hub](./README.md) for the complete overview.
