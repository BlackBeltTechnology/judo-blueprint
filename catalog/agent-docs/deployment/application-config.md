---
title: Application Configuration
description: JUDO_PLATFORM environment variables for database, Keycloak, filestore, mail and identifier signing, per-environment setup and encrypted values.
aliases: [environment variables config, judo-karaf.env settings, database connection settings, keycloak url config, signed identifier secret, mail smtp settings, configuration not applied]
keywords: [JUDO_PLATFORM_RDBMS_DIALECT, JUDO_PLATFORM_KEYCLOAK_AUTH_PUBLIC_URL, JUDO_PLATFORM_FILESTORE, JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET, judo-karaf.env, judo.sh, JUDO_PLATFORM_MAIL_SMTP_HOST, JUDO_PLATFORM_SWAGGER_UI, bannerEnabled, enableJMX, ENC]
tags: [domain:deployment, layer:infrastructure, status:platform]
---

# Configuration Guide

## Overview

The <app> application is configured through **environment variables** (prefix `JUDO_PLATFORM_`). Locally they come from the `judo-karaf.env` file in the project root and from the variables `judo.sh` exports; in Docker Compose they are set in the `environment:` block of the compose file. Configuration is externalized, so it can be changed without modifying code.

**Note**: Throughout this document, `<app>` refers to the application name from `judo.properties` (app_name property). Use this value in database names, Keycloak realms, and other application-specific settings.

**Important**: Do NOT edit `.cfg` files in `application/karaf-offline/etc/` directly. They are overwritten on rebuild; use environment variables.

## Table of Contents

- [Quick Reference](#quick-reference)
- [Configuration Methods](#configuration-methods)
- [Parameter Naming Convention](#parameter-naming-convention)
- [Configuration Categories](#configuration-categories)
- [Environment-Specific Configuration](#environment-specific-configuration)
- [Encrypted Values (Jasypt)](#encrypted-values-jasypt)
- [Security Best Practices](#security-best-practices)
- [Troubleshooting](#troubleshooting)

---

## Quick Reference

These are the variables the shipped `judo.sh` and the Docker Compose stacks of the project template actually set.

| Parameter | Example Value | Purpose |
| :--- | :--- | :--- |
| `JUDO_PLATFORM_RDBMS_DIALECT` | `postgresql` | Database dialect (`postgresql` or `hsqldb`) |
| `JUDO_PLATFORM_RDBMS_DB_HOST` | `postgres` | Database host |
| `JUDO_PLATFORM_RDBMS_DB_PORT` | `5432` | Database port |
| `JUDO_PLATFORM_RDBMS_DB_DATABASE` | `<app>` | Database name |
| `JUDO_PLATFORM_RDBMS_DB_USER` | `<app>` | Database user |
| `JUDO_PLATFORM_RDBMS_DB_PASSWORD` | `secret` | Database password |
| `JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL` | `http://auth:8080` | Keycloak URL used by the backend |
| `JUDO_PLATFORM_KEYCLOAK_AUTH_PUBLIC_URL` | `https://auth.example.com` | Keycloak URL as seen by browsers |
| `JUDO_PLATFORM_FILESTORE` | `filesystem` | File storage backend |
| `JUDO_PLATFORM_FILESTORE_DIRECTORY` | `/filestore` | Directory for the `filesystem` filestore |
| `JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET` | Base64 string | Secret used to sign entity identifiers |

---

## Configuration Methods

### Primary Method: judo-karaf.env

**Location:** `/judo-karaf.env`

The generated file contains only a few defaults (identifier signer secret, Keycloak password policy, `JUDO_PLATFORM_LOG_SMTP_SERVER`, `JUDO_PLATFORM_FILESTORE=rdbms`). The generated signer secret is a fixed placeholder; replace it per environment. Add or change variables there, then restart: `./judo.sh stop && ./judo.sh start`.

**Format:**
```bash
JUDO_PLATFORM_PARAMETER_NAME=value
```

### Selecting an environment: `judo.sh env`

`./judo.sh env <name>` selects an **alternate custom properties file** (for example `compose-dev.properties`) instead of the default `judo.properties`. The properties file carries `judo.sh start` options such as `runtime=compose` and `compose_env=compose-develop` (see [Build Process](./build-process.md#judosh-script)). The template does not generate per-environment `judo-karaf.env.development` / `judo-karaf.env.production` files; if you want per-environment env files you create and manage them yourself.

### Alternative Methods (Not Recommended)

**Java System Properties:**
```bash
export JAVA_EXTRA_OPTS="-Djudo.platform.parameterName=value"
```

**Direct .cfg file editing** (avoid this):
- Files in `application/karaf-offline/etc/*.cfg`
- Changes are overwritten on rebuild
- Not portable across environments

## Parameter Naming Convention

### Environment Variables
- Prefix: `JUDO_PLATFORM_` (no hyphen)
- Format: `SNAKE_CASE` (uppercase with underscores)
- Example: `JUDO_PLATFORM_RDBMS_DIALECT`

### Java System Properties / OSGi Config
- No prefix needed
- Format: `camelCase`
- Example: `rdbmsDialect`
- System properties in config templates keep their dots: `${system.java_home}` resolves the JVM property `java.home`; dots are not replaced by underscores.

### Custom application parameters

Custom parameter names are case-sensitive. A template line such as `myprop=${ mypropDev ! "My DEV Prop"}` reads the parameter `mypropDev` (lowercase `p`), so the environment-variable and `-D` forms must use that exact name. In a conditional template the `dev` branch falls back to `"My DEV Prop"` and the `qa` branch to `"My QA Prop"` when the parameter is not set.

### Conversion Rule
```
Environment Variable                       → OSGi Parameter
JUDO_PLATFORM_RDBMS_DIALECT               → rdbmsDialect
JUDO_PLATFORM_KEYCLOAK_AUTH_PUBLIC_URL    → keycloakAuthPublicUrl
```

## Configuration Categories

### 1. Database (RDBMS)

**For database schema migration and evolution**, see [Schema Evolution](./schema-evolution.md).

**JUDO_PLATFORM_RDBMS_DIALECT**
- **Description**: Database dialect for SQL generation
- **Options**: `postgresql`, `hsqldb` (JUDO ships only these two dialect bundles)

**JUDO_PLATFORM_RDBMS_DB_HOST / _PORT / _DATABASE / _USER / _PASSWORD**
- **Description**: Connection settings of the application database. `judo.sh` exports them for a local PostgreSQL container; the Compose stacks set them to the `postgres` service (`DB_DATABASE`, `DB_USER` and `DB_PASSWORD` default to the lower-case model name).
- **Note**: There is no `JUDO_PLATFORM_DATASOURCE_URL` / `_USERNAME` / `_PASSWORD` variable in the template. The JDBC URL is built by the platform from these parts.

**Connection pool and transaction timeouts** (used in the project's run scripts):
- `JUDO_PLATFORM_HIKARI_MAXIMUM_POOL_SIZE` (e.g. `10`)
- `JUDO_PLATFORM_HIKARI_CONNECTION_TIMEOUT` (milliseconds, e.g. `120000`)
- `JUDO_PLATFORM_NARAYANA_DEFAULT_TIMEOUT` (milliseconds, e.g. `120000`)
- `JUDO_PLATFORM_CASE_INSENSITIVE_LIKE` (`true` for case-insensitive `like` on PostgreSQL)

**Pool and datasource factory parameters:** the connection pool is selected by `rdbmsDbPool` (env `JUDO_PLATFORM_RDBMS_DB_POOL`; options `none`, `hikari`, `dbcp2`, `transx`; default `hikari`). There is no `rdbmsDbPoolType` or `dbPoolType`. `managedDatasourceFactory` (options `none`, `transx`) defaults to `none`, meaning transactions are handled by the JDBC datasource; `transx` wraps the datasource in the Transx JTA transaction manager.

For running JUDO on Spring Boot (`spring.datasource.*`), see [Spring Boot Runtime](./spring-boot-runtime.md). For runtime datasource behaviour (pax-jdbc keys, version checks) see [OSGi Runtime Services](./osgi-runtime-services.md).

### 2. Keycloak (Security)

**JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL**
- **Description**: Keycloak URL used by the backend (inside the Compose network, e.g. `http://auth:8080`)
- **Required**: Yes

**JUDO_PLATFORM_KEYCLOAK_AUTH_PUBLIC_URL**
- **Description**: Keycloak URL as reachable by browsers (e.g. `https://auth-<ip>.traefik.me`). The parameter is `keycloakAuthPublicUrl`, not `keycloakPublicUrl`.

**JUDO_PLATFORM_KEYCLOAK_REALM / JUDO_PLATFORM_KEYCLOAK_CLIENT_ID**
- **Description**: Realm and client id (used in real-world deployments).

**JUDO_PLATFORM_KEYCLOAK_DEFAULT_PASSWORD_POLICY**
- **Description**: Password policy for users created by the platform. The shipped `judo-karaf.env` sets `SAME_EMAIL`; the Compose stack sets `SAME_USERNAME`.

**JUDO_PLATFORM_KEYCLOAK_MANAGEMENT_ENABLED / JUDO_PLATFORM_USER_MANAGER_ENABLED / JUDO_PLATFORM_KEYCLOAK_USER / JUDO_PLATFORM_KEYCLOAK_PASSWORD**
- **Description**: Enable the built-in Keycloak user management and the Keycloak admin credentials the backend uses for it (seen in production Compose files of real applications). When unset, the admin user is `admin` and the admin password is `judo`.

### 3. REST API

**JUDO_PLATFORM_SWAGGER_UI / JUDO_PLATFORM_SWAGGER_UI_PATH**
- **Description**: Switch on the Swagger UI (default path `/swagger-ui`). Consider disabling it in production.

**JUDO_PLATFORM_CORS_ALLOW_ORIGIN**
- **Description**: Allowed CORS origin(s) (used by real deployments; do not leave it open in production). In the Guice CXF JAX-RS runtime this variable has no effect: `CrossOriginResourceSharingFilterProvider` returns an unconfigured filter.

### 4. File Storage

**JUDO_PLATFORM_FILESTORE**
- **Options**: `rdbms` (files in the database; the shipped `judo-karaf.env` and the `compose-develop` stack use it), `filesystem` (the `compose-postgresql-https` stack), `s3`.

**JUDO_PLATFORM_FILESTORE_DIRECTORY**
- **Description**: Directory for the `filesystem` store (Compose stack: `/filestore`). The old name `JUDO_PLATFORM_FILESTORE_PATH` does not exist.

**S3 settings**: `JUDO_PLATFORM_S3_BUCKET`, `JUDO_PLATFORM_S3_REGION`, `JUDO_PLATFORM_S3_ENDPOINT`, `JUDO_PLATFORM_S3_ACCESS_KEY`, `JUDO_PLATFORM_S3_SECRET_KEY`, plus `JUDO_PLATFORM_FILESTORE_TOKEN_EXPIRY`.

An `http://` S3 endpoint is accepted: activation logs a WARN that the endpoint is cleartext (signed requests and file bytes travel unencrypted), but it is not an error and does not stop activation. Use `https://` outside local tests.

The upload token audience is prefixed with the `audiencePrefix` property of the file-store token service config; the validator expects the same prefix.

#### Using a Google Cloud Storage bucket

Google Cloud Storage exposes an S3-compatible XML API, so the platform's S3 file store works against it with no GCS-specific code: set `JUDO_PLATFORM_FILESTORE=s3`, point `JUDO_PLATFORM_S3_ENDPOINT` at `https://storage.googleapis.com` and use **HMAC credentials** for the access/secret keys. Bucket lifecycle rules (for example delete after one day for temporary uploads) are configured in GCS, not in JUDO.

### 5. Identifier Signing

**JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET**
- **Description**: Base64-encoded HMAC secret used to sign the entity identifiers sent to clients (`__signedIdentifier`).
- **Important**: If the secret is not configured, the runtime generates a **new random 1024-bit key on every start**. Signed identifiers then become invalid after a restart and are not valid across cluster nodes. Always set the same secret on every node and keep it stable between restarts; treat it as a secret in production.

### 6. Email (SMTP)

| Variable | Purpose |
|----------|---------|
| `JUDO_PLATFORM_MAIL_SMTP_HOST` / `_PORT` | SMTP server |
| `JUDO_PLATFORM_MAIL_SMTP_USER` / `_PASSWORD` | Credentials |
| `JUDO_PLATFORM_MAIL_SMTP_AUTH` | Enable authentication |
| `JUDO_PLATFORM_MAIL_SMTP_STARTTLS_ENABLE` | Enable STARTTLS |
| `JUDO_PLATFORM_MAIL_SMTP_FROM` | Sender address |
| `JUDO_PLATFORM_MAIL_TRANSPORT_PROTOCOL` | Transport protocol |
| `JUDO_PLATFORM_MAIL_SMTP_SSL_TRUST` | Trusted SSL hosts |
| `JUDO_PLATFORM_LOG_SMTP_SERVER` | Log SMTP interactions (`true` in the shipped files) |

**Mail defaults:** without configuration the SMTP port is `25`; with `logSmtpServer=true` (`JUDO_PLATFORM_LOG_SMTP_SERVER`) the default of `mailSmtpPort` becomes `10025` instead. The local log SMTP server itself listens on `logSmtpServerPort`, which defaults to `10025` (host `logSmtpServerHost`, default `localhost`).

**Local testing with Mailpit:** run a mail catcher such as Mailpit locally; the app only knows an SMTP host and port, so for local runs point them at `localhost:1025` (no TLS) in `judo-karaf.env`. Set `JUDO_PLATFORM_LOG_SMTP_SERVER=false` (`true` in the shipped files, which sends mail to the log server instead), and set `JUDO_PLATFORM_MAIL_SMTP_USER` and `JUDO_PLATFORM_MAIL_SMTP_PASSWORD` to any value with `JUDO_PLATFORM_MAIL_SMTP_AUTH=false`: the mail service (`JavaMailSenderActivator`) is only created when the log SMTP server is on or user, password and host are all set, so with the log server off, host and port alone give no `EmailService`. Test/demo/production read the `JUDO_PLATFORM_MAIL_SMTP_*` variables from the deployment environment (for example `environments/<env>/app-compose/docker-compose.yml`). Nothing in the app depends on Mailpit; new-user and activation emails go through the same SMTP configuration, so Mailpit captures them too.

### 7. Other platform switches

- `JUDO_PLATFORM_DEFAULT_ZONE_ID` - default time zone id (e.g. `Europe/Budapest`).
- `JUDO_PLATFORM_METRICS_ENABLED` - enable metrics.
- `JUDO_PLATFORM_MARK_SELECTED_RANGE_ITEMS` - set in the shipped Compose stacks (`true`).
- `JUDO_PLATFORM_BUNDLE_WATCHER` - `false` disables watching bundle changes (hot deployment).
- `JUDO_STARTUP_FEATURE` - overrides the startup feature of the offline Karaf assembly at runtime.

### 8. Startup banner and JMX

The banner is printed once all platform services of a model are ready. Config keys: `bannerEnabled` (default `true`), `bannerFonts`, `bannerHslStart` / `bannerHslEnd` (`<hue>,<saturation>,<lightness>`, random when unset) and `enableJMX` (default `false`, registers MBeans `hu.blackbelt.judo:type=<model>,name=Application`). The system property `disableJudoAnsiColors` (any value) disables ANSI colours. See [OSGi Runtime Services](./osgi-runtime-services.md#startup-banner-and-readiness) for the readiness services.

## Configuration Precedence

Environment variables (`JUDO_PLATFORM_*`) are the recommended source. Edits of `.cfg` files are overwritten on rebuild and Karaf console changes are lost on restart, so keep every permanent setting in `judo-karaf.env` or the compose environment.

## Environment-Specific Configuration

### Development (Local)

**judo-karaf.env** / start options: `./judo.sh start` runs Karaf on port **8181**, Keycloak on 8080 (under `/auth`) and the database chosen by `dbtype` (`hsqldb` in the generated `judo.properties`; PostgreSQL with `-o dbtype=postgresql`).

```bash
JUDO_PLATFORM_RDBMS_DIALECT=hsqldb
JUDO_PLATFORM_FILESTORE=rdbms
JUDO_PLATFORM_LOG_SMTP_SERVER=true
```

### Docker Compose

See [Production Deployment](./production.md#shipped-docker-compose-environments) for the two shipped stacks (`compose-develop`, `compose-postgresql-https`) and their environment blocks.

### Production

```bash
JUDO_PLATFORM_RDBMS_DIALECT=postgresql
JUDO_PLATFORM_RDBMS_DB_HOST=db.example.com
JUDO_PLATFORM_RDBMS_DB_PORT=5432
JUDO_PLATFORM_RDBMS_DB_DATABASE=<app>
JUDO_PLATFORM_RDBMS_DB_USER=<app>_prod
JUDO_PLATFORM_RDBMS_DB_PASSWORD=${DB_PASSWORD}          # from secrets management

JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL=https://auth.example.com
JUDO_PLATFORM_KEYCLOAK_AUTH_PUBLIC_URL=https://auth.example.com
JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET=${SIGNER_SECRET}  # stable across restarts and nodes
JUDO_PLATFORM_FILESTORE=filesystem
JUDO_PLATFORM_FILESTORE_DIRECTORY=/filestore
JUDO_PLATFORM_SWAGGER_UI=false
```

### Provisioning a new environment (prod / test / demo)

- Keep environments distinct: separate Keycloak reachable address (in `karaf.env`), separate seed data and separate secrets.
- Wire the **init-time admin users** through the whole chain: the application's startup template (for example `app-startup.sh.tpl`) and the infrastructure config (for example terraform) must pass the admin-user and admin-password variables of your application. If one link is missing, the Keycloak admin users are silently not created on first init.
- Schema updates in such a pipeline run the schema tool in `generate` or `execute` mode; take a database backup (for example a managed-database backup branch) before `execute` and keep the restore command ready. See [Schema Evolution](./schema-evolution.md).

## Encrypted Values (Jasypt)

Configuration files can embed secrets as `password=ENC(<encrypted>)`. The `org.jasypt.encryption.StringEncryptor` OSGi service (from the `karaf-jasypt-support` / `osgi-encryption` features) decrypts them when the configuration is read. Passwords can be encrypted with a Karaf command and replaced in the PAX-JDBC / DBCP2 configuration files.

The password source is read in this order: `encryption_password`, then `encryption_passwordFile`, then the environment variable named by `encryption_passwordEnvName`. `encryption_passwordEnvName` has no default and there is no fallback: if none of the three is set, no password source is read, and the environment variable is used only when that property names it. (The `encrypt`/`decrypt` shell commands, without an explicit password, read the `ENCRYPTION_PASSWORD` environment variable.)

## Applying Configuration Changes

### Method 1: Restart Application (Recommended)

```bash
./judo.sh stop
./judo.sh start
```

### Method 2: Karaf Console (Runtime Changes)

```bash
./application/.karaf/bin/client

config:edit hu.blackbelt.judo.runtime
config:property-set parameterName newValue
config:update

config:list
```

**Note**: Runtime changes via console are lost on restart. Always update the environment for persistence.

## Security Best Practices

1. **Never commit secrets.** Keep real credentials out of version control; commit templates with placeholders such as `${DB_PASSWORD}`.
2. **Use a secrets manager** (Vault, cloud secret managers, Kubernetes Secrets) to inject values at deploy time, or Jasypt `ENC(...)` values.
3. **Rotate secrets** (database passwords, Keycloak client secret). Rotating `JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET` invalidates all signed identifiers currently held by clients.
4. **Least privilege** for the database user and Keycloak client.

## Troubleshooting

### Configuration Not Applied

1. Ensure the application was restarted: `./judo.sh stop && ./judo.sh start`
2. Check that the variable name matches the convention (`JUDO_PLATFORM_` prefix, no hyphen, names from the list above)
3. Check Karaf logs: `tail -f application/.karaf/data/log/karaf.log`

### Viewing Effective Configuration

```bash
./application/.karaf/bin/client
config:list | grep judo
```

### Database Connection Failed

Check `JUDO_PLATFORM_RDBMS_DB_*` and `JUDO_PLATFORM_RDBMS_DIALECT`, then test the connection: `psql -h localhost -U <app> -d <app>`. Note that if the connection still fails after the PostgreSQL retry loop, the platform only logs an error and creates no datasource for the model (see [OSGi Runtime Services](./osgi-runtime-services.md#postgresql-bootstrap-retry-and-datasource-keys)).

### Keycloak Authentication Failed

Check `JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL` / `_AUTH_PUBLIC_URL` and that the realm exists: `curl http://localhost:8080/realms/<app>` (the Keycloak path prefix depends on the Keycloak version).

## Reference Documentation

- **JUDO Platform Parameters**: https://internal-documentation.judo.technology/administrator-guide/03_platform_parameters.html

## File Locations

- Configuration file: `/judo-karaf.env`
- Karaf config directory: `/application/karaf-offline/etc/`
- Runtime logs: `/application/.karaf/data/log/karaf.log`

## Related Documentation

- [Build Process](./build-process.md), [Production Deployment](./production.md), [Local Development](./local-development.md)
- [Schema Evolution](./schema-evolution.md)
- **Backend Guides**: `../backend/` - custom operations and other backend topics.
