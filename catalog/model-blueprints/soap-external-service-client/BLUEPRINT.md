---
id: soap-external-service-client
title: SOAP External Service Client (WSDL-Generated OSGi Service)
description: A pattern for integrating with external SOAP/WSDL web services in a JUDO application by wrapping auto-generated JAX-WS client stubs behind a clean OSGi service interface.
aliases: []
keywords: [soap, external, service, client, wsdl, generated, osgi]
tags: ["domain:model", "layer:backend", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-09
last_updated: 2026-03-09
format: legacy
---

## Description

A pattern for integrating with external SOAP/WSDL web services in a JUDO application by wrapping auto-generated JAX-WS client stubs behind a clean OSGi service interface. This is an implementation-only blueprint -- it describes the structural pattern of how an external SOAP API is consumed as a reusable OSGi component, separate from any model entity.

The pattern involves:
- A dedicated Maven module (e.g., `mnb-soap-client/`) containing the WSDL file and a `cxf-codegen-plugin` configuration that generates JAX-WS client stubs at build time
- A clean service interface (e.g., `ExchangeRateService`) exposing domain-oriented methods (not raw SOAP operations)
- An `@Component(immediate=true)` implementation that initializes the CXF `JaxWsProxyFactoryBean` in its `@Activate` method, creates the SOAP proxy, and delegates calls to the generated stubs
- XML response parsing (DOM) to transform SOAP response strings into domain-specific POJOs (builder pattern)
- The OSGi bundle is packaged with `maven-bundle-plugin` and exports only the `osgi` package (service interface + DTOs), hiding generated SOAP stubs

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
