## Overview

Event entities are created as side effects within product lifecycle custom operations. Every state transition (create, finalize, approve, revoke) produces an Event record via `EventDao.create()` with the appropriate `EventType` enum value, a human-readable message, a timestamp, and relations to the affected product and the performing user.

## Implementation Pattern

- `EventDao` is injected via OSGi `@Reference` into each product lifecycle custom operation class
- Events are created using the builder pattern: `EventForCreate.builder().withType(...).withMessage(...).withCreatedAt(LocalDateTime.now()).withProduct(...).withPerformedBy(...).build()`
- The `EventType` enum (PRODUCT_CREATED, PRODUCT_FINALIZED, PRODUCT_APPROVED, PRODUCT_APPROVAL_REVOKED) determines the event category
- The performing user is resolved from the current actor's email via `VariableResolver` and `UserDao.query().filterByEmail()`
- Events are append-only (non-CRUD entity): no update or delete operations exist on Event
- The message attribute contains a human-readable string with the version number (e.g., "Version 3 approved")
- No separate event service layer -- event creation is embedded directly in each operation class

## Examples

### alba
- Key files: `custom/.../entities/product/FinalizeCustomImplementation.java`, `custom/.../entities/product/ApproveVersionCustomImplementation.java`, `custom/.../entities/product/RevokeApprovalCustomImplementation.java`, `custom/.../services/adminproduct/CreateProductCustomImplementation.java`, `custom/.../services/authorproduct/CreateProductCustomImplementation.java`
- Pattern: Each product lifecycle operation injects `EventDao` and creates an Event at the end of execution; the EventType enum value is chosen per operation (e.g., `EventType.PRODUCT_FINALIZED` in `FinalizeCustomImplementation`)
- Notable: Messages are in Hungarian (e.g., "Produktum letrehozva.", "Verzio 1 jovahhagyva."); the `product` and `performedBy` relations link the event to the domain entity and actor via associations rather than denormalized strings
- The `DraftNewVersionCustomImplementation` is the only product operation that does not create an Event
