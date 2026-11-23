## Overview

(Interface and class names below are example project code, not platform API; only `EmailService` is provided by the platform.) Implements a transactional email service using Handlebars templates stored in the database. A `ConfigurationTemplateService` reads email templates and platform settings from a singleton Configuration entity, while the email service implementation renders templates with dynamic context and sends via the JUDO `EmailService` API.

## Implementation Pattern

### Service interfaces (common module)
- `ConfigurationTemplateService` -- reads configuration values from the database: `getInvitationEmailTemplate()`, `getVerificationEmailTemplate()`, `getApprovalEmailTemplate()`, `getSenderEmail()`, `getBaseUrl()`, `getPlatformName()`, `getInvitationExpiryDays()`, `getMagicLinkExpirySeconds()`, etc.
- Email service interface -- type-safe methods for each transactional email: `sendInvitationEmail()`, `sendVerificationEmail()`, `sendApprovalNotificationEmail()`, etc.

### Implementation (common module)
- `@Component(immediate=true, service=<EmailServiceInterface>.class)` with `@Reference` to `EmailService`, `ConfigurationTemplateService`, and entity DAOs
- Uses `com.github.jknack.handlebars.Handlebars` for template rendering: `handlebars.compileInline(templateContent)` with `Context.newContext(model)`
- Each email method: (1) loads template from `ConfigurationTemplateService`, (2) builds a context model with dynamic values, (3) renders HTML, (4) sends via `EmailService.sendMessage(EmailMessage.emailBuilder()...)`
- Interceptors do not run around the custom operations that call this service (they fire only on built-in operations), so each caller invokes the send explicitly.
- Graceful degradation: if template is null (not configured in DB), the method logs and returns without error
- Document attachment support: retrieves files from `FileStoreService` by ID and attaches as `BinaryAttachment`

### Template variable conventions
- Action URLs (registration, verification, magic link): built from the base URL plus a route and a token parameter.
- Display names: platform name, organization name, user name, partner name, company name.
- Subject and content title.
- Expiration periods, in days or minutes.

Names are listed in prose rather than as template placeholders, so the guidance stays free of template syntax.

### Email context pattern
- A dedicated context POJO (e.g., `EmailContext`) with builder pattern, holding all template variables
- Context object is passed to `Handlebars.Context.newContext()` for type-safe rendering

## Examples

### Example (project code)
- Pattern: the email service renders Handlebars templates stored in the database Configuration entity, using `ConfigurationTemplateService` to load templates and platform settings. Sends via JUDO's `EmailService` OSGi service.
- Notable: Invitation emails construct a registration URL with token and email pre-fill. Approval emails include a magic link for one-click first login. Post-published emails are broadcast to all administrators (queried by an administrator role). Moderation emails use inline HTML when no template is configured.
- DI wiring: the configuration template service (reads the database) + `EmailService` (JUDO provided) -> the email service implementation -> consumed by custom operations and by the feed and push notification services

### Example (project code)
- Pattern: the sender service sends documents (for example reports and offers) as email attachments. Uses the configuration template service to load the email HTML template and sender address from the Configuration entity. Renders with `Handlebars.compileInline()` using an `EmailContext` builder POJO. Retrieves document files from `FileStoreService` and attaches via `BinaryAttachment`.
- Notable: Three document-specific email methods that share a common `sendDocumentEmail()` pipeline. The company name is queried from a company data DAO with a mask. An i18n interface provides localized email subjects and error messages. The context is a simple builder POJO with `title`, `recipient`, `subjectName` and `companyName` fields.
- DI wiring: `EmailSenderServiceImpl` `@Reference` `EmailService` (JUDO) + `FileStoreService` + `ConfigurationTemplateService` + `CompanyDataDao` + the i18n interface -> consumed by custom operations for sending documents to recipients
