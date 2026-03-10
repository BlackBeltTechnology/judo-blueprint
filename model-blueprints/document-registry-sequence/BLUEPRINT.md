---
id: "document-registry-sequence"
title: "Document Registry Sequence Number Generator"
score: 73.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - rackinspect
---
## Description

A DocumentRegistry entity that manages sequential document numbering for different document types. It maintains a prefix (string), financial period boundaries (financialPeriodStart, financialPeriodEnd), a transition period (transitionPeriodStart, transitionPeriodEnd), and a numeric sequence range (startIndex, endIndex, currentIndex). The documentType attribute (typed to a DocumentType enum) identifies which kind of document this registry tracks. Each document type gets its own registry instance so that fault registries, offers, assessment sheets, review reports, job sheets, and work reports each maintain independent sequence counters. The currentIndex is incremented by backend code when a new document is generated.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
