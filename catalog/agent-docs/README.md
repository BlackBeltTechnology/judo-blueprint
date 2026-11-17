---
title: Technical Documentation
description: "This directory contains all technical documentation for the JUDO framework, organized by domain."
aliases: [agent docs index, platform docs map, where are the docs, which doc to read, JUDO documentation folders]
keywords: [README.md, backend, frontend, model, deployment, judo-cli.md, transformation-pipeline.md, integration-testing, e2e-testing, Playwright]
tags: [domain:backend, domain:frontend, domain:model, domain:deployment, domain:testing, layer:backend, layer:frontend, layer:model, layer:infrastructure, layer:test, status:platform]
---
# Technical Documentation

This directory contains all technical documentation for the JUDO framework, organized by domain. AI assistants should reference these files directly when working on domain-specific tasks.

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `backend/` | Java backend development, custom operations, interceptors |
| `frontend/` | React frontend development, hooks, theming |
| `model/` | ESM model development, metamodel reference |
| `domain/` | Domain documentation generation |
| `deployment/` | Build, configuration, deployment |
| `integration-testing/` | Backend integration tests |
| `e2e-testing/` | Playwright E2E tests |

## Documentation Modules

- **backend**: Java backend development including custom operations, interceptors, data access, authentication, and testing.
- **frontend**: React frontend development including hooks, theming, i18n, and model-to-UI mappings.
- **model**: ESM model development including metamodel reference, advanced patterns, and traceability.
- **domain**: Domain documentation generation including templates and diagram generation.
- **deployment**: Build process, local development, production deployment, configuration, and schema evolution.
- **integration-testing**: Integration testing with judo-runtime-core-testkit.
- **e2e-testing**: End-to-end testing with Playwright.

## Usage

AI assistants should read the relevant README.md in each subdirectory for detailed guidance:

```
agent-docs/backend/README.md     → Backend development guide
agent-docs/frontend/README.md    → Frontend development guide
agent-docs/model/README.md       → Model development guide
agent-docs/deployment/README.md  → Deployment guide
```

## Platform CLI

For the JUDO Model CLI tool and the model transformation pipeline, see:

- [model/judo-cli.md](./model/judo-cli.md) — what the CLI is, why it is mandatory, and the platform invariants every assistant must follow.
- [model/transformation-pipeline.md](./model/transformation-pipeline.md) — ESM → PSM → ASM → RDBMS → Liquibase, server-side vs client-side regeneration, and in-memory state.
