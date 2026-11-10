---
id: platform-email-template-service
title: Platform Email Service with Database-Stored Handlebars Templates
description: A backend email service that renders Handlebars templates kept in the Configuration singleton and sends transactional mails through one typed method per email type.
aliases: [template email service, transactional email service]
keywords: [email, handlebars, template, configuration, transactional, attachment]
tags: [domain:model, layer:backend, project:mlszksz-platform, project:rackinspect, project:park-here, status:emerging]
category: pattern
status: emerging
projects: [mlszksz-platform, rackinspect, park-here]
evidence: ["mlszksz-platform:unrecorded", "rackinspect:unrecorded", "park-here:unrecorded"]
alternatives: []
fragment: none: backend-only
first_seen: 2026-03-09
last_updated: 2026-11-10
---
## Intent

Send the platform's transactional emails (invitations, verification links, approval notices and similar) from one backend service. The text of each email is a template that administrators can change in the Configuration singleton, so the wording does not need a deployment. The service keeps the rendering and sending steps in one place, so custom operations call one method per email type.

### Templates live in the database

Each email type has its template text in a configuration field (see [[platform-configuration-singleton]]). The service reads the template on each send and renders it with the values of that send.

### One method per email type

The service exposes a typed method for each email, such as one for invitations and one for verification links. Each method builds its own context and does not expose the raw template engine to callers.

## Structure

This is a backend pattern with no model shape of its own. The service depends on three things: a configuration reader that returns the templates and platform settings, the platform's email sending service, and, for attachments, the file store that holds the documents. The service has no entity and no transfer object. Its context is a plain builder object that carries the values a template may use, such as action URLs, display names and expiry periods.

## Constraints

- A template that is not configured is a skipped send. The service logs it and returns; it does not fail the caller. Projects decide whether to fall back to inline HTML.
- Rendering uses a Handlebars engine with an explicit context object. Templates may only read the variables the context provides.
- Action URLs are built from the configured base URL plus a route and a token. The token is created by project code, not by the template.
- Document attachments are fetched from the file store by id and attached as binary attachments. Only the file id is passed around, not the file content.
- The service runs inside the caller's operation. A send that fails is an infrastructure error, not a modeled business fault (a business rule violation is a modeled fault, HTTP 422); the caller decides whether the business action must roll back.
- Interceptors fire only on built-in operations, never on custom ones, so the sending logic is called explicitly from each operation (or service) that needs it.
- The service interfaces and class names here are example project code. The mail sending API (`EmailService`) is a platform service; the agent-docs do not describe it, so check the project's own dependency before relying on its signature.

## Variations

- **Single template store.** All emails read from the Configuration singleton. Simple projects use this.
- **Per-email template fields.** Each email type has its own text field on the singleton. This is the common layout.
- **File-store templates.** Templates are stored as files and read from the file store instead of a text field. Use this when templates are large or are edited as documents.
- **Document-sending variant.** A set of methods sends generated documents as attachments and shares one send pipeline for all of them.

## When to use

- Several custom operations send emails with the same sender and layout.
- Administrators must change email wording without a deployment.
- Emails carry links with tokens and need the configured base URL.

## When to avoid

- A single email with fixed text. A plain call to the mail API is simpler.
- Templates that must be versioned or approved before use. Add a review step outside this service.
- Notifications pushed to a device rather than mailed. See [[push-notification-system]].

## Related

- [[platform-configuration-singleton]] — holds the templates and sender settings this service reads
- [[document-file-attachment]] — how the attached documents are stored and fetched
- [[push-notification-system]] — the alternative channel for user notifications
