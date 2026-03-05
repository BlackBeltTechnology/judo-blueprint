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

## CLI Documentation

For JUDO Model CLI commands (queries, mutations, tracing), see the `judo-model-cli` skill in `.claude/skills/judo-model-cli/`.
