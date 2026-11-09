---
id: platform-email-template-service
title: "Platform Email Service with Database-Stored Handlebars Templates"
impl_only: true
usage_count: 3
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - mlszksz-platform
  - rackinspect
  - park-here
---

## Description

A transactional email service pattern that uses Handlebars templates stored in the database (via a Configuration singleton entity) to send various platform emails: invitations, verification links, approval notifications, post-published alerts, moderation notices, and rejection emails. This is an implementation-only blueprint -- the email service is a shared OSGi component used across multiple custom operations, not tied to any single model entity.

The pattern combines:
- A `ConfigurationTemplateService` interface that reads email templates and configuration values (base URL, sender email, expiry settings) from the platform Configuration entity
- An email service implementation that renders Handlebars templates with dynamic context variables and sends via an injected `EmailService`
- Type-safe email methods for each transactional email type
- Document attachment support (retrieving files from FileStoreService and attaching as binary email attachments)

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
