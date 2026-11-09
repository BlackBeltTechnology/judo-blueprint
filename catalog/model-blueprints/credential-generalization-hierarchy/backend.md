## Overview

The Credential generalization hierarchy is implemented through a provider service that resolves the polymorphic Credential reference to the correct platform-specific subtype, extracts its fields, and instantiates the corresponding API adapter. Credential CRUD operations work directly with the platform-specific DAO (e.g., `GoogleCredentialDao`), while the base `Credential` type is used only for polymorphic lookup through the Account entity.

## Implementation Pattern

- **Credential creation**: The `setGoogleCredential` operation first deletes any existing credential via the base Credential reference on Account, then creates a new `GoogleCredentialForCreate` with platform-specific fields (customerId, delegatedAccount, developerToken, jsonKeyFile). This replace-on-set pattern ensures only one credential exists per account
- **Polymorphic resolution**: `AdsBusinessApiProviderService` queries the Account's credential via `accountDao.queryCredential(account)` (returns base `Credential`), then uses the platform-specific DAO (`googleCredentialDao.getById(credential.identifier())`) to downcast and retrieve the full subtype with all fields
- **Platform dispatch**: The provider service switches on `account.getPlatform()` (the Platform enum) to determine which credential subtype to resolve and which API adapter to instantiate. Unsupported platforms throw `PLATFORM_NOT_SUPPORTED` or `PLATFORM_NOT_IMPLEMENTED` errors
- **API adapter instantiation**: The resolved credential fields are passed to the adapter constructor (e.g., `new GoogleAdsApiImpl(developerToken, delegatedAccount, loginCustomerId, jsonKey)`). File-type credentials (JSON key files) are read via `FileStoreService`
- **OSGi wiring**: The provider service is an OSGi `@Component` injecting `AccountDao`, `GoogleCredentialDao`, `FileStoreService`, and `AdTrackI18n` via `@Reference`

## Examples

### indamedia-adtrack
- Key files: `common/impl/AdsBusinessApiProviderServiceImpl.java`, `common/impl/AccountServiceImpl.java`, `adapters/google-ads/.../GoogleAdsApiImpl.java`
- Pattern: `AccountServiceImpl.setGoogleCredential()` deletes existing credential then creates `GoogleCredentialForCreate`; `AdsBusinessApiProviderServiceImpl.getAdsBusinessApi()` resolves base Credential to GoogleCredential via Platform enum dispatch, reads JSON key from FileStoreService, and returns `GoogleAdsApiImpl`
- Notable: MetaCredential exists in the model as a placeholder but backend throws `PLATFORM_NOT_IMPLEMENTED` for Platform.META, demonstrating the extensibility point. The `getCustomerId()` method also dispatches on Platform enum to extract the correct customer identifier from the platform-specific credential subtype.
