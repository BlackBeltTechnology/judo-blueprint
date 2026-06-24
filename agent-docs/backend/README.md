---
name: judo-backend-docs
description: Backend development guide for JUDO applications. Covers custom operations, interceptors, validators, data access, and error handling.
disable-model-invocation: false
user-invocable: false
agent: general-purpose
---

# Backend Development Guide

## Overview

Backend development in webshop involves implementing custom business logic in Java while leveraging the JUDO-generated SDK and runtime infrastructure.

**Note**: Throughout this document, `webshop` refers to the application name from `judo.properties` (app_name property). Package names, file paths, and generated artifacts use this value.

## Key Concepts

- **Model-Driven Development**: The application's structure, including entities, services, and APIs, is defined in high-level models. All development work is grounded in these models.
- **Code Generation**: The JUDO platform automatically generates a significant portion of the codebase (like SDKs and REST endpoints) from the models. This ensures consistency and reduces boilerplate code.
- **Custom Implementation**: Your primary focus as a developer is to implement custom business logic in specific, designated directories (`application/app/`, `application/interceptors/`). These areas are protected from the code generation process.
- **Checksum Protection**: To prevent accidental edits to generated files, a checksum system is in place. Modifying a generated file will cause the build to fail unless it's explicitly ignored.
- **Hot Deployment**: For rapid development cycles, changes to custom code can be deployed to a running Karaf instance without a full server restart.

## Architecture

### Code Generation vs Custom Implementation

**Generated (Do Not Edit Directly):**
- SDK API interfaces (`application/sdk/`)
- Internal SDK wrappers (`application/internal/`)
- REST API endpoints (`application/rest/`)
- Entity runtime models (from ASM)

**Custom Implementation (Edit Here):**
- Business logic operations (`application/app/`)
- Request/response interceptors (`application/interceptors/`)
- Custom validators and processors

### Code Generation and Checksum Protection

**How Generation Works:**
1. All generated files are tracked by **checksum** in `.generated-files` (located in generator output directories)
2. Files NOT in `.generator-ignore` will be regenerated on `./judo.sh build` or `./judo.sh generate`
3. **Checksum validation**: Before overwriting, the generator checks if a file was manually edited
   - If file was edited (checksum mismatch) → ❌ **Build FAILS** with error
   - If file unchanged → ✅ File is regenerated normally

**When You Must Edit Generated Files:**

Before editing a generated file directly, check the two extension mechanisms offered by the template — they keep the file under generator control and survive future template upgrades:

1. **Generator parameter** — some aspects of generation are controlled via `generator-parameter.properties` (see `deployment/build-process.md` → *When to Check Templates Instead of Patching*).
2. **Fragment extension point** — most `pom.xml`, `feature.xml`, and similar files expose named fragments you can fill in by dropping a file under `application/generator-overrides/<fragment-path>`. Look for paired marker comments such as
   ```xml
   <!-- To define create 'app/pom.xml.extra-dependencies.fragment.hbs' file -->
   <!-- End of 'app/pom.xml.extra-dependencies.fragment.hbs' -->
   ```
   See `deployment/build-process.md` → *Extending Generated Files via Fragment Overrides* for the full list and a worked example.

Only if neither mechanism offers a hook should you fall back to editing the generated file directly. This is **NOT the preferred way**, but when necessary:

1. **Edit the generated file** with your changes
2. **Add to `.generator-ignore`** to protect it from regeneration. Only this case (case 1 below) belongs in `.generator-ignore`:
   ```bash
   echo "application/sdk/src/main/java/[PACKAGE]/[GeneratedFile].java" >> .generator-ignore
   ```
3. Place the entry in `.generator-ignore` near related overrides (it's used like `.gitignore`)

#### `.generator-ignore` — One Rule

`.generator-ignore` uses `.gitignore`-style matching, scoped to generator output. Single purpose: stop the generator from re-emitting a file at path X because you hand-edited that exact generated file in place. It is **not** a "this file is custom" marker.

Three cases:

1. **Generator emits file at path X, you hand-edit X in place.** → Add `X` to `.generator-ignore`. Only legitimate case (example above).
2. **`.default` rename pattern** (custom operations, interceptors, validators). Generator emits `X.java.default`. Rename to `X.java` once and fill in the body. Generator re-emits `X.java.default` next round as a reference and never touches `X.java`. → `X.java` is OUTSIDE generator scope. **No entry needed.** Do NOT add `X.java.default` either — you want it to keep regenerating as a reference.
3. **Brand-new hand-written file the generator never emits at that path** (new helper classes, new factories like `ExceptionUtils.java`). → OUTSIDE generator scope. **No entry needed.**

Adding purely-custom files or `.default` paths to `.generator-ignore` is noise; remove such entries.

**Handling Checksum Errors:**

If you get checksum errors due to code formatting changes (e.g., after `git checkout` or IDE auto-format in dev mode):

```bash
# Ignore checksum errors and force regeneration
./judo.sh generate -i
# or
./judo.sh build -i
```

**Checksum File Locations:**
- `.generated-files` - In each generator output directory
- Format: Tracks file paths and their checksums

## Prerequisites

### Required Tool Versions

This project uses SDKMAN for version management. Required versions are specified in `.sdkmanrc`:

```bash
java=21.0.7-zulu
maven=3.9.10
mvnd=1.0.2
```

**Setup**:
```bash
# 1. Install SDKMAN (if not already installed)
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"

# 2. Enable auto-env (recommended - automatic version switching)
echo "sdkman_auto_env=true" >> ~/.sdkman/etc/config

# 3. Install versions from .sdkmanrc
cd [project-name]
sdk env install

# 4. Verify
java -version   # Should show 21.0.7-zulu
mvn -version    # Should show 3.9.10
```

**How It Works**:
- `.sdkmanrc` is generated by `./judo.sh generate-root` command
- When `sdkman_auto_env=true`, SDKMAN automatically switches to project versions when you enter the directory
- `./judo.sh` script automatically installs required versions if missing

**Maven Daemon (mvnd)**: Optional but recommended for faster builds
```bash
# Use mvnd instead of mvn for faster incremental builds
mvnd clean install
```

## Project Structure

```
application/
├── sdk/                    # Generated API interfaces
│   └── src/main/java/[PACKAGE]/
│       └── [Entity]Dao.java, [Entity]Service.java
├── internal/               # Generated SDK wrappers (binds custom to runtime)
├── app/                    # ✏️ CUSTOM OPERATIONS HERE
│   └── src/main/java/[PACKAGE]/
│       └── Custom[Entity]ServiceImpl.java
├── interceptors/           # ✏️ CUSTOM INTERCEPTORS HERE
│   └── src/main/java/[PACKAGE]/
│       ├── LogAuthenticationInterceptor.java
│       └── LogOperationCallInterceptor.java
└── rest/                   # Generated JAX-RS endpoints
    └── resources/
```

**Note**: Package structure is generated from the model and typically follows patterns like `hu.blackbelt.model.webshop` or `party.mkkp.webshop`.

## See Also

- **[Architectural Patterns](./architectural-patterns.md)** - High-level architectural patterns for building robust and scalable applications.
- **[Data Access Guide](data-access-guide.md)** - A guide to querying, filtering, and using masks for performance.
- **[Type System Guide](type-system-guide.md)** - Explains the critical Service vs. Entity layer type system.
- **[Custom Operations](custom-operations.md)** - Implementing custom business logic.
- **[Interceptors](interceptors.md)** - For intercepting business logic operations.
- **[Authentication Guide](authentication-guide.md)** - For handling user authentication events.
- **[Internationalization Guide](internationalization-guide.md)** - A guide to localizing messages for a global audience.
- **[Error Handling Guide](error-handling-guide.md)** - A guide to creating robust and user-friendly error responses.
- **[Testing Guide](testing-guide.md)** - A guide to writing unit and integration tests.
- **[Debugging and Monitoring Guide](debugging-and-monitoring-guide.md)** - A guide to debugging, monitoring, and performance profiling.
- **Integration Testing (see `judo-integration-testing-docs` skill)** - Testing custom operations with judo-runtime-core-testkit.
- **[Patterns and Best Practices](patterns-and-best-practices.md)** - A comprehensive guide to backend patterns and best practices.
