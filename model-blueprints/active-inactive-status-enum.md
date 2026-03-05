---
id: active-inactive-status-enum
title: "Active/Inactive Two-State Status Enum"
usage_count: 4
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - viterra_demo
  - sanctuary-backend
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
---

## Description

A minimal two-state status enumeration with ACTIVE and INACTIVE (or semantically equivalent) members. This is the simplest form of a status lifecycle enum, representing entities that are either currently in use (ACTIVE) or no longer in use (INACTIVE/ARCHIVED). Unlike the three-state ACTIVE/SUSPENDED/DEACTIVATED pattern, this enum has no intermediate state -- entities are either on or off. Unlike a simple boolean `active` flag, using an enum provides extensibility (additional states can be added later) and clearer semantics in queries and UI.

Variants include:
- **ACTIVE/INACTIVE** -- the classic binary toggle, used when entities are simply enabled or disabled
- **active/archived** -- a softer variant where the second state implies the entity is preserved for historical reference but no longer actively used
- **AKTIV/LEZART** -- a Hungarian-language variant meaning ACTIVE/CLOSED, used for ticket/case lifecycle where a case is either open for processing or closed after resolution

This enum is typically used as a `status` attribute on entities that need lifecycle management, such as users, reference data entries, configuration items, or service tickets.

## Detection Query

```graphql
{ esm { enumerationtypes(limit: 50) {
  items { fqn name members { items { name ordinal } } }
} } }
```

Look for enums with exactly two members where one represents an active/enabled state and the other represents an inactive/archived/closed state.

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "{{STATUS_NAME}}"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{STATUS_NAME}}", name: "{{ACTIVE_MEMBER}}", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{STATUS_NAME}}", name: "{{INACTIVE_MEMBER}}", ordinal: 2
} }) { success fqn } }
```

## Examples

### viterra_demo
- **Enum**: `viterra::Status` -- ACTIVE(1), INACTIVE(2)
- Not directly used as a status attribute on any entity in this model
- Instead, Client and Silo entities each have a boolean `active` attribute for the same purpose
- The enum exists alongside the boolean flags, suggesting it may be intended for future use or for expression-based filtering

### sanctuary-backend
- **Enum**: `Sanctuary::ActiveStatus` -- active(1), archived(2)
- Named "ActiveStatus" rather than "Status", with lowercase member names and "archived" instead of "inactive"
- Used as the `status` attribute on both the `User` entity and the `PositionTitle` entity
- The "archived" semantics suggest data is preserved for reference but no longer actively used, rather than simply being toggled off
- This is the first observed variant where the second state uses "archived" instead of "inactive"

### kozut-eugyfel-client
- **Enum**: `e_ugyfelszolgalat::entities::BejelentesAllapot` -- AKTIV(1), LEZART(2)
- Hungarian-language variant meaning "Report Status" with ACTIVE and CLOSED members
- Used as the `allapot` (status) required attribute on the Bejelentes (Report/Ticket) entity
- The AKTIV state represents an open ticket under processing; LEZART represents a resolved/closed ticket
- The Munkatars (Worker) actor separates active and closed tickets into two different access points: `aktivBejelentesek` (active reports) and `lezartBejelentesek` (closed reports)
- State transitions are controlled by operations: `lezaras` (closure) moves from AKTIV to LEZART, `megnyitas` (reopening) moves from LEZART to AKTIV
- Permission guard DERIVED booleans (lezarasEngedely, megnyitasEngedely) control which operations are available based on the current state

### kozut-eugyfel-model-test
- **Enum**: `e_ugyfelszolgalat::Bejelentes::BejelentesAllapot` -- AKTIV(1), LEZART(2)
- Same Hungarian-language ACTIVE/CLOSED semantics as kozut-eugyfel-client, but in a different package (`Bejelentes` sub-package rather than `entities`)
- Used as the `allapot` (status) required attribute on the base Bejelentes (Report/Ticket) entity in a generalization hierarchy
- In this test variant, the Bejelentes entity is part of a generalization hierarchy (JarokeloBejelentes and EUgyfelszolgalatBejelentes extend the base Bejelentes), so the status enum applies uniformly across all ticket subtypes
- State transitions are controlled by operations on the base entity: `lezaras` (closure) moves from AKTIV to LEZART
- Unlike kozut-eugyfel-client, this variant does not have a `megnyitas` (reopen) operation or permission guard DERIVED booleans
