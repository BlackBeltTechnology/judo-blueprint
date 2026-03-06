---
id: "handlebars-email-template"
title: "Handlebars Template Rendering"
domain: "backend"
category: "integration"
score: 53.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - park-here
  - workflow-poc
---
## Description

Content is rendered using Handlebars templates compiled at runtime. Templates can be stored in the FileStore service and loaded by ID, or defined inline in code. They are compiled via `Handlebars.compileInline()` and applied with a context object (Map or POJO). This enables dynamic content generation for emails (with embedded images, per-entity variants) or other structured text output (diagrams, reports) without code changes.

## Structure

```java
Handlebars handlebars = new Handlebars();
String templateContent = convertStreamToString(fileStoreService.get(templateId));
Template template = handlebars.compileInline(templateContent);

Context context = Context.newContext(Config.builder()
    .title(title)
    .reserverName(name)
    .date(formattedDate)
    .base64Image(base64FloorPlan)
    .build());

String htmlBody = template.apply(context);

emailService.sendMessage(EmailService.EmailMessage.emailBuilder()
    .from(senderEmail)
    .to(recipientEmail)
    .subject(subject)
    .htmlTemplate(htmlBody)
    .inputStreamInlinedContent(imageId, binaryAttachment)
    .build());
```

## Examples

### ParkHere
`EmailSenderServiceImpl` renders 5 email types using Handlebars: reservation creation (per-garage template with embedded floor plan), modification, deletion, reminder, and doorman daily summary. Templates stored in FileStore during Init operation. Floor plan images embedded as base64 inline content.

### workflow-poc
`DiagramUtils.getDiagram()` uses Handlebars with an inline Mermaid `stateDiagram` template to generate workflow state diagrams. The template iterates `{{#each states}}` and `{{#each transitions}}` to render state definitions and transition arrows with event/role annotations. Context is a `Map<String, Object>` with states and transitions lists. Handles fork (`<<fork>>`), join (`<<join>>`), and final states (`[*]`).

## Trade-offs

- Pros: Templates editable without code changes, rich HTML with embedded images, per-entity template variants, FileStore-backed for persistence
- Cons: Handlebars has limited logic capabilities, template errors are runtime failures, base64 images increase email size
- Alternative: Freemarker/Thymeleaf templates, external email service (SendGrid templates), or plain-text emails

## Related Patterns

- email-service-integration
- filestore-mediated-file-transfer
- init-data-seeding
