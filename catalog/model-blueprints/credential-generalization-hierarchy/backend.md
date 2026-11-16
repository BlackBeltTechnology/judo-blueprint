## Overview

The platform generates a DAO with full create, read and delete methods only for mapped, non-abstract types ([data access guide](../../agent-docs/backend/data-access-guide.md)). The abstract Credential therefore has no create or lookup-by-id methods of its own; it is reached only through the Account's relation query, and every write goes through a subtype DAO. On top of that, the reference implementation (application code, not platform) implements the hierarchy through a provider service that resolves the polymorphic Credential reference to the correct platform-specific subtype, extracts its fields, and instantiates the corresponding API adapter. Credential CRUD operations work directly with the platform-specific DAO (e.g., `GoogleCredentialDao`), while the base `Credential` type is used only for polymorphic lookup through the Account entity.

## Implementation Pattern

- **Credential creation**: The `setGoogleCredential` operation (a custom operation, so no interceptor runs around it; it checks the caller's rights itself) first deletes any existing credential via the base Credential reference on Account, then creates a new `GoogleCredentialForCreate` with platform-specific fields (customerId, delegatedAccount, developerToken, jsonKeyFile). This replace-on-set pattern ensures only one credential exists per account
- **Polymorphic resolution**: The application's `ExternalApiProviderService` (application helper) queries the Account's credential via `accountDao.queryCredential(account)` (returns base `Credential`), then uses the platform-specific DAO (`googleCredentialDao.getById(credential.identifier())`) to downcast and retrieve the full subtype with all fields
- **Platform dispatch**: The provider service switches on `account.getPlatform()` (the Platform enum) to determine which credential subtype to resolve and which API adapter to instantiate. Unsupported platforms throw project-defined `PLATFORM_NOT_SUPPORTED` or `PLATFORM_NOT_IMPLEMENTED` errors (a business fault, not a platform exception)
- **API adapter instantiation**: The resolved credential fields are passed to the adapter constructor (e.g., `new GoogleAdsApiImpl(developerToken, delegatedAccount, loginCustomerId, jsonKey)`). File-type credentials (JSON key files) are read via `FileStoreService`
- **OSGi wiring** (common practice): The provider service is an OSGi `@Component` injecting `AccountDao`, `GoogleCredentialDao`, `FileStoreService`, and `AppI18n` via `@Reference`

## Examples

### Variant seen in practice
- Key files: the external API provider service and its implementation, the account service implementation, and the Google Ads adapter.
- Pattern: application helpers: `AccountServiceImpl.setGoogleCredential()` deletes existing credential then creates `GoogleCredentialForCreate`; `ExternalApiProviderServiceImpl.getExternalApi()` resolves base Credential to GoogleCredential via Platform enum dispatch, reads JSON key from FileStoreService, and returns `GoogleAdsApiImpl`
- Notable: MetaCredential exists in the model as a placeholder but backend throws `PLATFORM_NOT_IMPLEMENTED` for Platform.META, demonstrating the extensibility point. The `getCustomerId()` method also dispatches on Platform enum to extract the correct customer identifier from the platform-specific credential subtype.
