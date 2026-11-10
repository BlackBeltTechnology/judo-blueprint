## Overview

The backend reads the single Configuration row and applies updates to it. The platform's generated update operation covers simple cases. When the update must accept partial input, or must check or change more than the generated code does, a custom operation takes over.

## Implementation Pattern

### Read the single row

Read the row through the generated data access for the entity, selecting one row. Treat a missing row as a startup error, because the row is seeded once (see [[initializer-entity-with-init-operation]]). Do not create the row in a read path.

```java
// selectOne() returns an Optional in the generated DAO query API
Configuration config = configurationDao.query().selectOne()
        .orElseThrow(() -> new IllegalStateException("Configuration row is missing: run the seed step"));
```

`configurationDao` is an example name from project code, not a platform class.

### Partial update in a custom operation

A custom update operation takes an input transfer object whose fields are all optional. It loads the row, copies only the non-null input fields onto it, and saves. Validation of required values happens in the platform; a missing required value returns a ValidationException (HTTP 400).

Interceptors fire only on built-in operations, never on custom ones. If the update must be audited, call the audit logic from the operation itself (see [[audit-log-entity]]).

### Business faults

A business rule that fails in the operation, such as an expiry below a minimum, is a modeled fault (HTTP 422). The exception class is generated per project from the modeled fault. Project code may wrap the check in its own helper class; that helper is project code, not part of the platform.

### Settings consumers

Services that send email or compute expiries read the row through the same read path. They do not cache the values for longer than one request unless the project decides so.

## Examples

### mlszksz-platform
- The update is a custom operation `updateConfiguration` on the admin transfer object. It takes an input transfer object with all fields optional and applies the non-null ones to the Configuration row.
- The row is read with the generated data access, selecting one row.

### rackinspect
- The entity is fully non-CRUD. Settings change through custom operations and a related list of minimum offer prices is maintained in the same operation.

### park-here
- The configuration transfer object is mapped to the entity and carries a flag that tells the client whether the row exists. Two custom operations maintain the related doorman and calendar-day lists.

The helper classes named in these examples (for example the admin configuration services) are example project code, not platform classes.
