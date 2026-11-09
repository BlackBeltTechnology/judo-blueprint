---
id: document-registry-sequence
title: Document Registry Sequence Number Generator
description: A DocumentRegistry entity that manages sequential document numbering for different document types.
aliases: []
keywords: [document, registry, sequence, number, generator]
tags: ["domain:model", "layer:model", "layer:backend", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:unrecorded"]
alternatives: []
fragment: pending
first_seen: 2026-03-05
last_updated: 2026-03-05
format: legacy
---
## Description

A DocumentRegistry entity that manages sequential document numbering for different document types. It maintains a prefix (string), financial period boundaries (financialPeriodStart, financialPeriodEnd), a transition period (transitionPeriodStart, transitionPeriodEnd), and a numeric sequence range (startIndex, endIndex, currentIndex). The documentType attribute (typed to a DocumentType enum) identifies which kind of document this registry tracks. Each document type gets its own registry instance so that fault registries, offers, assessment sheets, review reports, job sheets, and work reports each maintain independent sequence counters. The currentIndex is incremented by backend code when a new document is generated.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
