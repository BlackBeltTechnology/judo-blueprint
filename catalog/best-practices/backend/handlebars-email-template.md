---
id: handlebars-email-template
title: Handlebars Template Rendering
description: "Render emails and other structured text from Handlebars templates compiled at runtime, with templates kept in the FileStore or inline in code, so wording changes need no code change."
aliases: [email template, template rendering, handlebars rendering]
keywords: [handlebars, template, rendering, email, filestore, inline template, compileInline]
tags: ["domain:backend", "layer:backend", "project:park-here", "project:workflow-poc", "status:emerging"]
category: integration
status: emerging
projects: [park-here, workflow-poc]
evidence: ["park-here:unrecorded", "workflow-poc:unrecorded"]
alternatives: []
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Email bodies, reports and generated diagrams are text with variable parts. Keep the text in a Handlebars template and fill it from a context object at runtime. The template can change without a code change when it lives in the FileStore.

## Practice

### Platform base and what is a convention

The agent-docs cover only the surroundings: SMTP is configured through `JUDO_PLATFORM_MAIL_SMTP_*` environment values ([email configuration](../../agent-docs/deployment/application-config.md)), the FileStore is a platform service ([[filestore-mediated-file-transfer]]), and custom services are OSGi components. The agent-docs do not describe a Handlebars library or an email-sending API: rendering with Handlebars and the `EmailService` calls below are what the examples use. Verify the library version and the service API in your application.

### Compile from a stored or inline template

- Load the template text from the FileStore by id (seeded at start-up, see [[init-data-seeding]]) or keep it inline in code.
- Pass the template text and a context object (a map or a small POJO) to the mail service; the platform renders the template with the model, with images attached as inline content.
- For other output, compile it at runtime and apply the context object yourself.

```java
// Example code (Handlebars Java library; EmailService is an application-level API)
String templateContent = convertStreamToString(fileStoreService.get(templateId));

emailService.sendMessage(EmailService.EmailMessage.emailBuilder()
    .from(senderEmail).to(recipientEmail).subject(subject)
    .htmlTemplate(templateContent).model(contextObject)
    .inputStreamInlinedContent(imageId, binaryAttachment)
    .build());
```

- Per-entity variants (for example a template per site) are separate stored templates chosen by id.
- Treat a missing or broken template as a runtime failure: it is only discovered when rendering.

## Rationale

- Templates are editable without a build when stored in the FileStore, and one mechanism serves HTML mail and plain structured text.
- Cost: Handlebars has little logic, template errors appear at runtime, and base64-embedded images enlarge the mail.
- Alternatives: other template engines or an external mail-template service.

## Example

- One application: five email types (booking creation with a per-site template and an embedded layout image, modification, deletion, reminder, and a daily summary). Templates are stored in the FileStore at init and layout images are embedded as base64.
- A workflow example: an inline template generates a workflow state diagram. It loops over states and transitions with a context map, including fork, join and final states.

## When to avoid

- A fixed one-line message: format a string directly.
- Content that non-developers must edit through a UI: keep templates in a model entity instead, as in [[platform-email-template-service]].

## Related

- [[email-service-integration]] — sending the rendered mail
- [[filestore-mediated-file-transfer]] — templates stored in the FileStore
- [[init-data-seeding]] — seeding template files at start-up
- [[platform-email-template-service]] — templates kept in the database
