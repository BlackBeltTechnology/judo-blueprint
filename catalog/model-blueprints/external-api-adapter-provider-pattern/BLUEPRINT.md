---
id: external-api-adapter-provider-pattern
title: "External API Adapter with Provider Service Pattern"
impl_only: true
usage_count: 1
first_seen: "2026-03-09"
last_updated: "2026-03-09"
projects:
  - indamedia-adtrack
---

## Description

A multi-module adapter pattern for integrating with external platform APIs (e.g., Google Ads, Meta Ads) through a pluggable provider architecture. This is an implementation-only blueprint -- it describes a pure backend architectural pattern for abstracting multiple external API implementations behind a single interface, with a factory/provider OSGi service that resolves the correct adapter at runtime based on configuration or entity state.

The pattern uses three layers:
1. **API interface module** -- a standalone OSGi bundle containing a platform-agnostic Java interface and DTO classes, with no dependencies on the JUDO model or any specific external SDK
2. **Adapter implementation module(s)** -- one module per external platform (e.g., `google-ads`), each implementing the API interface using the platform's SDK
3. **Provider service** -- an OSGi service in the `common` module that acts as a factory, resolving the correct adapter implementation at runtime based on entity state (e.g., a `Platform` enum on an Account entity), loading credentials from the database, and returning a ready-to-use API client

This pattern enables adding new external platform integrations (e.g., Meta Ads, TikTok Ads) without modifying existing code -- only a new adapter module and a new branch in the provider service are needed.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
