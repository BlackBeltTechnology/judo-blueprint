## Overview

Implements a transactional email service using Handlebars templates stored in the database. A `ConfigurationTemplateService` reads email templates and platform settings from a singleton Configuration entity, while the email service implementation renders templates with dynamic context and sends via the JUDO `EmailService` API.

## Implementation Pattern

**Service interfaces (common module):**
- `ConfigurationTemplateService` -- reads configuration values from the database: `getInvitationEmailTemplate()`, `getVerificationEmailTemplate()`, `getApprovalEmailTemplate()`, `getSenderEmail()`, `getBaseUrl()`, `getPlatformName()`, `getInvitationExpiryDays()`, `getMagicLinkExpirySeconds()`, etc.
- Email service interface -- type-safe methods for each transactional email: `sendInvitationEmail()`, `sendVerificationEmail()`, `sendApprovalNotificationEmail()`, etc.

**Implementation (common module):**
- `@Component(immediate=true, service=<EmailServiceInterface>.class)` with `@Reference` to `EmailService`, `ConfigurationTemplateService`, and entity DAOs
- Uses `com.github.jknack.handlebars.Handlebars` for template rendering: `handlebars.compileInline(templateContent)` with `Context.newContext(model)`
- Each email method: (1) loads template from `ConfigurationTemplateService`, (2) builds a context model with dynamic values, (3) renders HTML, (4) sends via `EmailService.sendMessage(EmailMessage.emailBuilder()...)`
- Graceful degradation: if template is null (not configured in DB), the method logs and returns without error
- Document attachment support: retrieves files from `FileStoreService` by ID and attaches as `BinaryAttachment`

**Template variable conventions:**
- `{{registrationUrl}}`, `{{verificationUrl}}`, `{{magicLinkUrl}}` -- action URLs constructed from `baseUrl` + route + token parameters
- `{{platformName}}`, `{{organizationName}}`, `{{userName}}`, `{{partner}}`, `{{companyName}}` -- display names
- `{{title}}`, `{{subjectName}}` -- email subject and content title
- `{{expiryDays}}`, `{{expiryMinutes}}` -- configurable expiration periods

**Email context pattern:**
- A dedicated context POJO (e.g., `EmailContext`) with builder pattern, holding all template variables
- Context object is passed to `Handlebars.Context.newContext()` for type-safe rendering

## Examples

### mlszksz-platform
- Key files: `common/services/PlatformEmailService.java`, `common/services/impl/PlatformEmailServiceImpl.java`, `common/services/ConfigurationTemplateService.java`
- Pattern: `PlatformEmailServiceImpl` renders Handlebars templates stored in the database Configuration entity, using `ConfigurationTemplateService` to load templates and platform settings. Sends via JUDO's `EmailService` OSGi service.
- Notable: Invitation emails construct a registration URL with token and email pre-fill. Approval emails include a magic link for one-click first login. Post-published emails are broadcast to all platform admins (queried by `UserRole.PLATFORM_ADMIN`). Moderation emails use inline HTML when no template is configured.
- DI wiring: `ConfigurationTemplateService` (reads DB) + `EmailService` (JUDO provided) -> `PlatformEmailServiceImpl` -> consumed by custom operations, `FeedServiceImpl`, `PushNotificationServiceImpl`

### rackinspect
- Key files: `common/utils/services/EmailSenderService.java`, `common/utils/services/impl/EmailSenderServiceImpl.java`, `common/utils/services/ConfigurationTemplateService.java`, `common/utils/services/impl/ConfigurationTemplateServiceImpl.java`, `common/utils/email/EmailContext.java`
- Pattern: `EmailSenderServiceImpl` sends documents (assessment sheets, review reports, offers) as email attachments. Uses `ConfigurationTemplateService` to load the email HTML template and sender address from the Configuration entity. Renders with `Handlebars.compileInline()` using an `EmailContext` builder POJO. Retrieves document files from `FileStoreService` and attaches via `BinaryAttachment`.
- Notable: Three document-specific email methods (`sendAssessmentSheet`, `sendReviewReport`, `sendOffer`) that share a common `sendDocumentEmail()` pipeline. Company name is dynamically queried from `CompanyDataDao` with a mask (`CompanyDataMask.companyDataMask().withName()`). Uses `RackInspectI18n` for localized email subjects and error messages. `EmailContext` is a simple builder POJO with `title`, `partner`, `subjectName`, `companyName` fields.
- DI wiring: `EmailSenderServiceImpl` `@Reference` `EmailService` (JUDO) + `FileStoreService` + `ConfigurationTemplateService` + `CompanyDataDao` + `RackInspectI18n` -> consumed by custom operations for sending documents to partners
