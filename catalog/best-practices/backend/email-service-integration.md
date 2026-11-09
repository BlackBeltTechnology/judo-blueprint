---
id: email-service-integration
title: Email Service Integration via OSGi
description: "Sending emails from custom operations using the `hu.blackbelt.email.api.EmailService` OSGi service."
aliases: []
keywords: [email, service, integration, osgi]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:alba", "project:mlszksz-platform", "project:ubives", "project:park-here", "status:established"]
category: integration
status: established
projects: [trivia, rackinspect, alba, mlszksz-platform, ubives, park-here]
evidence: ["trivia:unrecorded", "rackinspect:unrecorded", "alba:unrecorded", "mlszksz-platform:unrecorded", "ubives:unrecorded", "park-here:unrecorded"]
alternatives: []
related: [two-phase-registration, filestore-mediated-file-transfer, document-generation-pipeline, handlebars-email-template]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

Sending emails from custom operations using the `hu.blackbelt.email.api.EmailService` OSGi service. The service is injected via `@Reference` and provides a builder-based API for constructing email messages with from, to, subject, and body fields. SMTP configuration is externalized to environment variables.

## Structure

```java
@Reference
EmailService emailService;

// Send email
emailService.sendMessage(
    EmailService.EmailMessage.emailBuilder()
        .from("no-reply@example.com")
        .to(recipientEmail)
        .subject("Subject line")
        .plaintTemplate(bodyText)
        .build()
);
```

Configuration via environment variables:
- `JUDO_PLATFORM_MAIL_SMTP_HOST` -- SMTP server
- `JUDO_PLATFORM_MAIL_SMTP_PORT` -- SMTP port
- `JUDO_PLATFORM_MAIL_SMTP_USER` / `PASSWORD` -- credentials
- `JUDO_PLATFORM_MAIL_SMTP_STARTTLS_ENABLE` -- TLS

## Examples

### Trivia
`RegisterCustomImplementation` injects `EmailService` and sends activation code emails via Mailjet SMTP. Email includes the 4-digit code, a link to the app, and a full GDPR privacy notice. From address is hardcoded as `no-reply@judo.technology`.

### RackInspect
`EmailSenderServiceImpl` wraps `EmailService` with Handlebars HTML templating. Sends assessment sheets, review reports, and offers as binary attachments from FileStoreService. Sender email and company name are loaded from Configuration/CompanyData entities rather than hardcoded.

### ALBA
SendGrid SMTP relay configured via environment variables (`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`). Email API dependency (`osgi-email-api:1.0.1`) included in the application POM. Domain authentication configured via DNS records in SendGrid dashboard. Secrets stored in GCP Secret Manager.

### mlszksz-platform
`PlatformEmailService` interface with 5 email types: invitation, verification, approval notification, user invitation verification, and post-published notification. Email templates stored in Configuration entity (DB-configurable). Template variables like `${recipientEmail}`, `${token}`, `${organizationName}` are substituted at runtime. No-op mock used in tests.

### Ubives
`MailServices` uses SendGrid Java SDK directly (not via OSGi EmailService) with Handlebars template rendering. OSGi Config Admin provides `baseUrl`, `fromAddress`, and `sendGridApiKey` via `@ObjectClassDefinition`. Sends invitation emails with magic link URLs. `configurationPolicy = ConfigurationPolicy.REQUIRE` ensures the service only activates when config is present. Template loaded from `email-inline-template.html.hbs` classpath resource.

### ParkHere
`EmailSenderServiceImpl` wraps `EmailService` with Handlebars template rendering and FileStore-backed templates. Sends 5 email types: reservation creation (per-garage template with embedded floor plan as base64 inline image), modification, deletion, reminder, and doorman daily summary. Sender/contact emails loaded from Configuration entity. Tracks doorman notifications via `DoormanNotified` entity to prevent duplicates.

## Trade-offs

- Pros: Clean OSGi service injection, externalized SMTP config, simple builder API
- Cons: No templating engine (body is plain string), no HTML email support shown, hardcoded from address
- Alternative: Template-based email with Thymeleaf/Freemarker, or external email service API (SendGrid, etc.)

## Related

- [[two-phase-registration]]
- [[filestore-mediated-file-transfer]]
- [[document-generation-pipeline]]
- [[handlebars-email-template]]

