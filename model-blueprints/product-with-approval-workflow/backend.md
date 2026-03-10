## Overview

The Product approval workflow is implemented through seven custom operation classes spanning entity-level instance operations (finalize, approve, revoke, assign, draft new version) and transfer-level static operations (create product for admin and author roles). Each operation validates state preconditions, transitions the ProductState enum, manages versioning through ProductVersion/ProductVersions entities, and logs events via EventDao.

## Implementation Pattern

- Each workflow transition is an OSGi `@Component` implementing a generated operation interface (e.g., `implements ...product.Finalize`)
- State validation pattern: load the product via `productDao.getById()` with a `ProductMask` selecting the `state` field, then check `product.getState() != ProductState.EXPECTED_STATE` and throw `RuntimeException` if invalid
- State transition: `product.setState(ProductState.NEW_STATE)` followed by `productDao.update(product)`
- Actor resolution: `userDao.query().filterByEmail(StringFilter.equalTo(variableResolver.resolve(String.class, "ACTOR", "email"))).selectOne()` -- common pattern in every operation
- Versioning: `ProductVersions` is a container entity; `DraftNewVersionCustomImplementation` copies all product content attributes, lookup relations (audience, curriculum, resultTypes), and attachments into a new Product, then creates a new `ProductVersion` with an incremented version number
- Event logging: every operation (except draftNewVersion) creates an Event via `EventDao.create(EventForCreate.builder()...)` at the end
- Role-specific create operations: `AdminCreateProductCustomImplementation` sets `impersonatingAuthor` (admin acting on behalf of an author) while `AuthorCreateProductCustomImplementation` sets the current user as `author`
- Lookup entity aggregation: during product creation, lookup entity names are joined into comma-separated denormalized strings for display

## Examples

### alba
- Key files: `custom/.../entities/product/FinalizeCustomImplementation.java`, `custom/.../entities/product/ApproveVersionCustomImplementation.java`, `custom/.../entities/product/RevokeApprovalCustomImplementation.java`, `custom/.../entities/product/AssignApprovalCustomImplementation.java`, `custom/.../entities/product/DraftNewVersionCustomImplementation.java`, `custom/.../services/adminproduct/CreateProductCustomImplementation.java`, `custom/.../services/authorproduct/CreateProductCustomImplementation.java`
- Pattern: Seven custom operation classes implement the full DRAFT->FINALIZED->APPROVED lifecycle with state guards, versioning via ProductVersion/ProductVersions, event logging, and task creation for approval assignment
- Notable: `ApproveVersionCustomImplementation` rolls back any previously APPROVED versions to FINALIZED before approving the current one (single-approved-version constraint); `DraftNewVersionCustomImplementation` deep-copies product content, relations, and attachments into a new DRAFT product with an incremented version number; `AssignApprovalCustomImplementation` creates Task entities as side effects for each selected assignee user
- DI: All classes use OSGi `@Reference` to inject `ProductDao`, `UserDao`, `EventDao`, `VariableResolver`, and additional DAOs as needed (e.g., `TaskDao`, `ProductVersionDao`, `ProductVersionsDao`, `AudienceDao`, `CurriculumDao`, `ResultTypeDao`)
