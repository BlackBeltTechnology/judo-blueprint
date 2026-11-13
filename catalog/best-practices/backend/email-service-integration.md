---
id: email-service-integration
title: Email Service Integration via OSGi
description: Send application e-mail from custom operations through an injected mail service, keep the SMTP settings in platform configuration, and keep sending out of the business transaction.
aliases: [sending email, SMTP, EmailService, mail from operation]
keywords: [email, SMTP, EmailService, OSGi, reference, template, Handlebars, attachment, configuration, mailpit, transaction]
tags: ["domain:backend", "layer:backend", "project:trivia", "project:rackinspect", "project:alba", "project:mlszksz-platform", "project:ubives", "project:park-here", "status:established"]
category: integration
status: established
projects: [trivia, rackinspect, alba, mlszksz-platform, ubives, park-here]
evidence: ["trivia:unrecorded", "rackinspect:application/app/src/main/java/hu/blackbelt/rackinspect/rackinspect/custom/rackinspect/services/job_task_services/jobsheet/SendEmailCustomImplementation.java", "alba:unrecorded", "mlszksz-platform:application/common/src/main/java/hu/blackbelt/mlszksz/platform/common/services/impl/PlatformEmailServiceImpl.java", "ubives:unrecorded", "park-here:unrecorded"]
alternatives: []
related: [two-phase-registration, filestore-mediated-file-transfer, document-generation-pipeline, handlebars-email-template]
fragment: "none: backend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

Custom operations send e-mail (activation codes, reports, reminders). Inject a mail service, build the message in a small service, and take sender, server and templates from configuration rather than code.

## Practice

### Inject a mail service and wrap it

Custom operations get OSGi services with `@Reference` (see [Injecting DAOs and Services](../../agent-docs/backend/data-access-guide.md#injecting-daos-and-services)). Most applications use the `EmailService` of the `hu.blackbelt.email.api` module with a builder-style message (from, to, subject, body). The agent-docs do not describe that API, so check the artifact version in your application. One application used a vendor SDK directly instead.

Put the call in one service (`EmailSenderService` in the examples) with a method per mail type. Operations then call the service, and tests replace it with a no-op implementation.

### Take server settings from platform configuration

The platform's own SMTP settings are the `JUDO_PLATFORM_MAIL_SMTP_*` variables: host, port, user, password, auth, STARTTLS, from, plus the transport protocol and SSL trust (see [Email (SMTP)](../../agent-docs/deployment/application-config.md#6-email-smtp)). A vendor SDK needs its own parameters. Custom application parameters can use the OSGi Configuration Mapper or Config Admin (see [Configuration Mapper for Custom Parameters](../../agent-docs/backend/platform-behavior-reference.md#configuration-mapper-for-custom-parameters)). Never hard-code the sender or API keys.

### Invitation mail is a different path

E-mail for user invitations is sent by Keycloak, not by the application. On every Karaf start the Keycloak connector rewrites the default realm's SMTP settings from the `JUDO_PLATFORM_MAIL_SMTP_*` values. Do not build your own invitation sender unless you need a different flow (see [Keycloak Users and the Entity Store](../../agent-docs/backend/platform-behavior-reference.md#keycloak-users-and-the-entity-store)).

### Render bodies from templates

Plain strings do not scale. Render HTML bodies from templates (Handlebars in most applications), stored in a configuration entity or as files, with variables substituted at send time (see [[handlebars-email-template]]). Attachments such as generated reports come from the file store (see [[filestore-mediated-file-transfer]] and [[document-generation-pipeline]]).

### Keep sending out of the business change

A send error must not leave half-done business data, and a rolled-back operation must not have sent mail. Operations run in a transaction, and an exception rolls back the DAO write. Send after the change is complete, catch send errors and log them (see [[two-phase-registration]]). Do not send from an `async()` interceptor if you need the transaction's data: it runs outside the transaction and without context variables.

### Test locally with a mail catcher

Run a mail catcher such as mailpit (SMTP 1025, web inbox 8025) and point `JUDO_PLATFORM_MAIL_SMTP_*` at it.

## Rationale

- One service isolates the mail API, so a change of provider or a test double touches one class.
- Configuration through platform variables keeps secrets out of the model and the code.
- Limit: the injected service is application infrastructure, not part of the model. The model cannot see or test it.

## Example

- A registration operation sends a four-digit activation code through the injected service over a hosted SMTP relay.
- One application: an `EmailSenderService` wraps the mail service, renders Handlebars templates, attaches stored files and loads sender data from a configuration entity.
- One application: SMTP relay settings come from environment variables, secrets from a secret manager.
- One application: an interface with five mail types, templates stored in a configuration entity, and a no-op implementation in tests.
- Another application: a vendor SDK is called directly, with its settings from Config Admin and the component activated only when configured.

## When to avoid

- Only user invitations are needed: the Keycloak mail already does that.
- Mail volume or deliverability needs queueing, retries or bounce handling: use a mail provider API behind the same wrapper.
- Sending must be atomic with the business change: use an outbox entity that a separate job sends.

## Related

- [[two-phase-registration]] — registration flow that sends a code
- [[filestore-mediated-file-transfer]] — attachments from the file store
- [[document-generation-pipeline]] — generated documents sent by mail
- [[handlebars-email-template]] — templated mail bodies
