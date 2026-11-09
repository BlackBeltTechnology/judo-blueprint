---
id: "credential-generalization-hierarchy"
title: "Credential Generalization Hierarchy (Platform-Specific API Credentials)"
score: 63.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - indamedia-adtrack
---
## Description

An abstract or minimal Credential base entity that serves as a common reference point for API credentials, with platform-specific concrete subtypes inheriting from it via generalization. The base Credential entity typically has no data attributes of its own (or very few), and carries only a back-reference relation to the parent entity it authenticates (e.g., Account). Each platform-specific subtype (e.g., GoogleCredential, MetaCredential) adds the fields required by that platform's API: API keys, tokens, customer IDs, key files, delegated accounts, etc. The parent entity (Account) holds a single 0..1 association to the base Credential type, which polymorphically resolves to whichever platform subtype was created. A Platform enum discriminates which platform an Account belongs to.

This pattern enables a single Account entity to work with different external API providers while keeping credential schemas cleanly separated. It is the model-layer analog of the Strategy pattern.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.

## Backend Implementation

See [backend.md](backend.md) for backend implementation patterns and examples.
