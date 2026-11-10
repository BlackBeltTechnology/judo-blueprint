## Overview

The sequence is advanced by a project service that reads the registry row for a date and increments `currentIndex` under a lock. The platform does not provide this service. Platform sequences (the `SEQUENCE` variable category, or a custom `Sequence` component) can have gaps because values of rolled-back transactions are not reused, which is why this blueprint keeps its own counter row. The names below are examples of project code.

## Implementation Pattern

- **Service (project code).** A `*Service` class, for example `RegistryService`, exposes one method that takes the document type and a date, and returns the next number as text. It is a plain project component, not a generated one.
- **Lock.** The method runs inside one lock, so the read and the increment cannot interleave. A `synchronized` method works on a single application instance. Several instances need a database-level lock or an atomic update instead.
- **Period lookup.** The service first checks whether the date falls in a transition period. If it does, it uses the period matching the target date. Otherwise it uses the financial period matching the current date.
- **Increment.** Start at `startIndex` when `currentIndex` is empty, otherwise add one. Stop when the index passes `endIndex` and report the exhaustion as a `ValidationException` (400), not a bare runtime exception, which the platform turns into a generic 500.
- **Format.** Return `prefix` followed by the index, zero-padded to the digit count of `endIndex`.
- **Callers.** Generation operations for each document kind call the service. The service is called from the operation's implementation, not from a client.

```java
public String getNextNumber(DocumentType type, LocalDate date) {
    synchronized (this) {
        DocumentRegistry registry = findRegistry(type, date);
        int next = registry.getCurrentIndex() == null
                ? registry.getStartIndex()
                : registry.getCurrentIndex() + 1;
        if (next > registry.getEndIndex()) {
            throw new ValidationException(List.of(ValidationResult.builder()
                    .code("REGISTRY_RANGE_EXHAUSTED").level(ValidationResult.Level.ERROR).build()));
        }
        registry.setCurrentIndex(next);
        return registry.getPrefix() + pad(next, registry.getEndIndex());
    }
}
```

The sample is project code. The entity and the enumeration are generated from the model.

## Examples

### rackinspect
- Key files: `common/utils/services/RegistryService.java`, `common/utils/services/impl/RegistryServiceImpl.java`
- Pattern: a `synchronized` method looks up the registry row for the period, increments `currentIndex`, updates the row and returns `prefix` plus a zero-padded index.
- Notable: transition periods are handled explicitly, and six document kinds each keep their own counter. The registry rows are seeded from a spreadsheet import during setup.
