## Overview

The Configuration singleton entity is created by the Initializer and updated through a custom `updateConfiguration` operation. A `ConfigurationTemplateService` provides read access to configuration values for other services (email templates, expiry durations, URLs).

## Implementation Pattern

- The `UpdateConfigurationCustomImplementation` class implements the `UpdateConfiguration` interface, injecting `ConfigurationDao`
- It queries the singleton Configuration entity via `configurationDao.query().selectOne()`, then applies partial updates from the `ConfigurationInput` unmapped TO (each field uses `Optional.ifPresent()` for null-safe updates)
- The `ConfigurationTemplateServiceImpl` OSGi service caches and provides read access to configuration values: `getVerificationExpiryMinutes()`, `getInvitationExpiryDays()`, `getBaseUrl()`, `getSenderEmail()`, email template content, and Keycloak client settings
- The Initializer seeds the singleton with default values: senderEmail, baseUrl, platformName, invitationExpiryDays, verificationExpiryMinutes, and email template placeholders
- In projects where Configuration is fully non-CRUD (all flags false), updates happen through the admin UI operations rather than direct entity update

## Examples

### mlszksz-platform
- Key files: `custom/.../adminconfigurationto/UpdateConfigurationCustomImplementation.java`, `common/services/ConfigurationTemplateService.java`, `common/services/impl/ConfigurationTemplateServiceImpl.java`
- Pattern: Singleton queried via `configurationDao.query().selectOne()`; partial update applies only non-null fields from input TO; read access via dedicated template service
- Notable: Configuration holds both platform settings (URLs, expiry durations) and email templates (invitation, verification, approval, post-published); consumed by RegistrationService, InvitationService, PlatformEmailService, and MagicLinkService

### rackinspect
- Key files: `common/utils/services/ConfigurationTemplateService.java`, `common/utils/services/impl/ConfigurationTemplateServiceImpl.java`
- Pattern: `ConfigurationTemplateService` interface provides getter methods for each template (assessment sheet, review report, offer, completion certificate, work report, job sheet, email) plus `getSenderEmail()`; implementation queries `configurationDao.query().selectOne()` and retrieves binary template files via `FileStoreService`
- Notable: Configuration stores binary document templates (assessmentSheetTemplate, offerTemplate, etc.) rather than text-only email templates; also stores business parameters (netMarginPercent, closingTime, incidentNotificationEmail, updateExchangeRates flag) and composed MinimumOfferPrice sub-entities for per-currency minimum offer thresholds
- The Configuration singleton is seeded by the `ExcelDataImporter` during initialization with default values for all required fields

### park-here
- Key files: `custom/.../configurationsettings/ConfigurationCustomImplementation.java`, `custom/.../configurationsettings/CreateDayCustomImplementation.java`, `custom/.../configurationsettings/CreateDoormanCustomImplementation.java`, `common/ConfigurationService.java`, `common/impl/ConfigurationServiceImpl.java`
- Pattern: `ConfigurationCustomImplementation` implements a create-or-update operation: queries `configurationDao.query().selectOne()` -- if empty, creates with all template fields; if present, updates all fields from the `ConfigurationInput` TO. A separate `ConfigurationService` interface provides `getConfiguration()` for read access, throwing `CONFIGURATION_NOT_FOUND` if missing.
- Notable: Configuration is fully non-CRUD (all flags false). Three separate custom operations manage the Configuration: `configuration` (create/update settings), `createDay` (add AdditionalDay calendar overrides with duplicate-day validation), and `createDoorman` (add Doorman entries with duplicate-email validation). Both CreateDay and CreateDoorman delegate to `ConfigurationService.getConfiguration()` and use `ErrorCode.NOT_VALID_DATA` for business rule violations.
- The `EmailSenderService` consumes Configuration for sender email, contact email, and Handlebars email templates (doorman, deletion, modification, reminder) loaded from `FileStoreService`.
