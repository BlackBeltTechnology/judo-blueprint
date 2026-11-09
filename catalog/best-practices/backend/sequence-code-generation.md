---
id: "sequence-code-generation"
title: "Sequential Code Generation via VariableResolver SEQUENCE"
domain: "backend"
category: "operation"
score: 47.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - judo-partner
---
## Description

Auto-generating sequential human-readable codes for entities using the JUDO `VariableResolver` with the `SEQUENCE` category. Each call to `variableResolver.resolve(Long.class, "SEQUENCE", sequenceName)` returns the next sequential number for the given sequence name, which is then formatted into a padded string code (e.g., `PRT-00001`). Multiple independent sequences can coexist by using different sequence names.

## Structure

```java
@Reference(target = "(judo.model.name=AppName)")
VariableResolver variableResolver;

// Generate sequential code with prefix and zero-padding
String code = String.format("PRT-%05d",
    variableResolver.resolve(Long.class, "SEQUENCE", "partner").intValue());
// -> PRT-00001, PRT-00002, PRT-00003, ...

// Different sequence for different entity type
String recordNumber = String.format("%s-%05d",
    register.getRegisterCode(),
    variableResolver.resolve(Long.class, "SEQUENCE", register.getRegisterCode()).intValue());
// -> REG-00001, REG-00002, ...
```

Key elements:
- `VariableResolver` injected with model-name target filter
- `"SEQUENCE"` category for auto-incrementing numbers
- Third parameter is the sequence name (allows multiple independent sequences)
- `String.format()` with `%05d` for zero-padded formatting
- Sequences are persistent (survive restarts)

## Examples

### judo-partner
Two independent sequences: (1) `PartnerServices.createPartner()` generates partner codes as `PRT-XXXXX` using `variableResolver.resolve(Long.class, "SEQUENCE", "partner")`. (2) `RegisterServices.createRecord()` generates record numbers using `variableResolver.resolve(Long.class, "SEQUENCE", register.getRegisterCode())`, where each register has its own sequence keyed by the register code. Both use `%05d` formatting for 5-digit zero-padded numbers.

## Trade-offs

- Pros: Simple API, persistent across restarts, supports multiple independent sequences, human-readable codes
- Cons: Not transactional (gaps possible if operation fails after sequence increment), centralized (potential bottleneck under high concurrency), format is application-specific
- Alternative: Database sequences (more standard but less portable), UUID (no gaps but not human-readable), timestamp-based codes (no collisions but longer)

## Related Patterns

- actor-resolution-variable-resolver
- builder-pattern-entity-creation
