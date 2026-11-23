---
title: Backend Testing Guide
description: Unit testing custom operations with mocks and running integration tests.
aliases: [unit test custom operation, mock DAO in backend tests, JUnit 5 Mockito, run backend integration tests, backend test commands]
keywords: [MockitoExtension, InjectMocks, EntityDao, VariableResolver, assertThrows, MinimumPermissionsViolatedException, mvn test, mvn clean install, skipTests, integration-test]
tags: [domain:backend, layer:backend, status:platform]
---

# Backend Testing Guide

## Overview

This guide provides an overview of testing strategies for custom backend code in a JUDO application. It covers both unit testing with mocks and the execution of integration tests.

For a comprehensive guide on writing integration tests, including detailed examples and advanced patterns, please refer to the main [Integration Testing Guide](../integration-testing/README.md).

## Table of Contents

- [Unit Testing](#unit-testing)
- [Integration Testing](#integration-testing)

---

## Unit Testing

Unit tests for custom operations should be small, focused, and use mocks to isolate the specific logic being tested. This ensures that tests are fast and not dependent on external systems like a database.

The recommended stack is **JUnit 5** with **Mockito**.

### Example: Unit Testing a Custom Operation

```java
@ExtendWith(MockitoExtension.class)
class ToggleStatusCustomImplementationTest {

    @Mock
    private EntityDao entityDao;

    @Mock
    private EntityValidationDao validationDao;   // illustrative DAO for model-defined validation queries

    @Mock
    private VariableResolver variableResolver;

    @InjectMocks
    private ToggleStatusCustomImplementation implementation;

    @Test
    void testToggleStatus_preventsSelfModification() {
        Entity entity = new Entity();
        entity.setIdentifier("entity@example.com");

        when(variableResolver.resolve(String.class, "ACTOR", "identifier"))
            .thenReturn("entity@example.com");

        implementation.accept(entity);

        // Verify that the update method was never called, isolating the security check.
        verify(entityDao, never()).update(any());
    }

    @Test
    void testToggleStatus_validatesMinimumRequiredEntities() {
        Entity entity = new Entity();
        entity.setIdentifier("entity@example.com");
        entity.setStatus(true);

        when(variableResolver.resolve(String.class, "ACTOR", "identifier"))
            .thenReturn("admin@example.com");
        when(entityDao.getById(any())).thenReturn(Optional.of(entity));
        when(entityDao.update(any())).thenReturn(entity);
        when(validationDao.queryActiveEntitiesWithAtLeastManagementPermission())
            .thenReturn(Optional.of(false));

        // Assert that the declared fault (generated checked exception) is thrown when the rule is violated.
        assertThrows(MinimumPermissionsViolatedException.class, () -> {
            implementation.accept(entity);
        });
    }
}
```

## Integration Testing

Integration tests provide a way to test your custom operations against a real (in-memory) database, ensuring that your logic, DAO interactions, and the JUDO runtime all work together correctly.

For a complete guide on how to set up, write, and run integration tests, please see the **[Integration Testing Guide](../integration-testing/README.md)**.

### Running Integration Tests

The generated root project has no `integration-tests` Maven profile (the profiles it defines are for building: `build-model`, `build-schema`, `build-sdk`, `build-karaf`, `build-frontend-*`, `build-docker`, `build-e2e`, ...). Integration tests live in a separate test project that uses the runtime testkit and run with `mvn test` after the application artifacts were installed. Follow the [Integration Testing Guide](../integration-testing/README.md) for the exact commands.

```bash
# Build and install the application first, then run the tests of the separate test project
mvn clean install -DskipTests
cd application/integration-test
mvn test
```

Unit tests for interceptors and custom operations that mock DAOs run in the module they belong to with `mvn test`.

---

## See Also

- [Integration Testing Guide](../integration-testing/README.md) - The main, comprehensive guide for integration testing.
- [Debugging and Monitoring Guide](debugging-and-monitoring-guide.md) - For debugging and monitoring your application.
- [Custom Operations](custom-operations.md) - For the business logic you will be testing.
