---
id: "generator-ignore-config-protection"
title: "Generator-Ignore for Configuration Protection"
domain: "backend"
category: "config"
score: 224.6
usage_count: 15
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - rackinspect
  - itracker
  - alba
  - mlszksz-platform
  - viterra_demo
  - bhs-global-operation
  - judo-demo-miniworkflow
  - ubives
  - park-here
  - indamedia-adtrack
  - InterfaceRegister
  - judo-partner
  - workflow-poc
  - reserve-app
---
## Description

The `.generator-ignore` file at the project root lists files that should be excluded from code generation overwrites. This protects developer-customized configuration files (especially those containing secrets) from being overwritten when regenerating code from the model. The file itself is also listed to prevent self-overwrite.

## Structure

```
# .generator-ignore
.generator-ignore
judo.properties
judo-karaf.env
generator-parameter.properties
```

Protected files typically include:
- `.generator-ignore` itself
- `judo.properties` -- runtime configuration (ports, DB type, admin settings)
- `judo-karaf.env` -- environment secrets (SMTP credentials, signer secret, FileStore config)
- `generator-parameter.properties` -- code generation parameters

## Examples

### Trivia
Root `.generator-ignore` protects 4 files: itself, `judo.properties`, `judo-karaf.env` (contains Mailjet SMTP credentials and identity signer secret), and `generator-parameter.properties`. Frontend submodules also have their own `.generator-ignore` files.

### RackInspect
Root `.generator-ignore` protects 5 files (adds `judo.sh`). Additionally, `application/app/.generator-ignore` protects `pom.xml` and 2 `.java.default` files. `application/app/src/main/java/.generator-ignore` lists 11 custom operation `.java.default` files to prevent regeneration of manually-implemented operations.

### itracker
Root `.generator-ignore` protects the standard 4 files: itself, `judo.properties`, `judo-karaf.env`, and `generator-parameter.properties`. No application-level `.generator-ignore` exists since no custom operations have been implemented yet. Frontend submodules have their own `.generator-ignore` files.

### ALBA
Root `.generator-ignore` protects the standard 4 files: itself, `judo.properties`, `judo-karaf.env`, and `generator-parameter.properties`. Frontend submodule also has its own `.generator-ignore`. No application-level overrides needed since custom operations live in dedicated `custom/` directories.

### mlszksz-platform
Root `.generator-ignore` protects standard 4 files. `application/app/src/main/java/.generator-ignore` lists 44 `.java.default` files for all customized operations, preventing regeneration of hand-written implementations. Largest `.generator-ignore` observed, reflecting the 65+ custom operations in the project.

### viterra_demo
Root `.generator-ignore` protects the standard 4 files: itself, `judo.properties`, `judo-karaf.env`, and `generator-parameter.properties`. No application-level `.generator-ignore` since all operations remain as `.java.default` stubs. Frontend submodules (admin + partner) each have their own `.generator-ignore` files.

### bhs-global-operation
Root `.generator-ignore` protects the standard 4 files with the standard EPL-2.0 license header. No application-level `.generator-ignore` since the project has zero entities and zero custom operations. Represents the minimal baseline `.generator-ignore` in a freshly generated JUDO project.

### judo-demo-miniworkflow
Root `.generator-ignore` protects the standard 4 files (itself, `judo.properties`, `judo-karaf.env`, `generator-parameter.properties`) with standard EPL-2.0 license header. No application-level `.generator-ignore` since all 10 operations remain as `.java.default` stubs. Frontend submodule has its own `.generator-ignore`.

### Ubives
Root `.generator-ignore` protects 5 files: itself, `judo.properties`, `judo-karaf.env`, `generator-parameter.properties`, and `judo.sh`. No application-level `.generator-ignore` since custom operations live in dedicated `custom/` directories (not overwriting `.java.default` files). Frontend submodules and keycloak-theme have their own `.generator-ignore` files.

### ParkHere
Root `.generator-ignore` protects 5 files: itself, `.gitignore`, `judo.properties`, `judo-karaf.env`, and `generator-parameter.properties`. Application-level `.generator-ignore` protects `schema/pom.xml`. Custom operations live in `custom/` directories. Frontend submodules and theme directories each have their own `.generator-ignore` files.

### Indamedia-AdTrack
Root `.generator-ignore` protects the standard 4 files: itself, `judo.properties`, `judo-karaf.env`, and `generator-parameter.properties`. No application-level `.generator-ignore` since custom operations live in `custom/` directories. Frontend submodules have their own `.generator-ignore` files.

### InterfaceRegister
Minimal `.generator-ignore` protects only `judo.properties` (single entry, no self-reference or other files). No application-level `.generator-ignore` since all 10 operations remain as `.java.default` stubs. This is the most minimal `.generator-ignore` observed, suggesting an early-stage project with no customized files beyond the runtime configuration.

### judo-partner
Root `.generator-ignore` protects the standard 4 files: itself, `judo.properties`, `judo-karaf.env`, and `generator-parameter.properties`. No application-level `.generator-ignore` since all 15 custom operations live in dedicated `custom/` directories (renamed from `.java.default`). Frontend submodule has its own `.generator-ignore`.

### workflow-poc
Root `.generator-ignore` protects the standard 4 files: itself, `judo.properties`, `judo-karaf.env`, and `generator-parameter.properties`. Standard EPL-2.0 license header. No application-level `.generator-ignore` -- custom operations live in `custom/` directories. Frontend submodule has its own `.generator-ignore`.

### ReserveApp
Root `.generator-ignore` protects the standard 4 files: itself, `judo.properties`, `judo-karaf.env`, and `generator-parameter.properties`. Standard EPL-2.0 license header. No application-level `.generator-ignore` since no custom operations exist (app module is empty). Frontend submodules (5 actor-specific UIs) each have their own `.generator-ignore` files.

## Trade-offs

- Pros: Prevents accidental loss of secrets and custom config during regeneration, simple gitignore-like syntax
- Cons: Must be manually maintained, forgetting to add a file means it gets overwritten on next build
- Alternative: External configuration management (Vault, K8s secrets), environment-only config

## Related Patterns

- osgi-karaf-bundle-architecture
