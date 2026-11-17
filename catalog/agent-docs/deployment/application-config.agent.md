# application-config.md — index

Pull-only condensed map. Source: catalog/agent-docs/deployment/application-config.md.

## Overview
- Config = env vars, prefix `JUDO_PLATFORM_`. Local: `judo-karaf.env` (project root) + vars `judo.sh` exports. Compose: `environment:` block.
- `<app>` = app name from `judo.properties` (`app_name`).
- Never edit `application/karaf-offline/etc/*.cfg`; overwritten on rebuild.

## Table of Contents
- Section list only; pull the section you need with `kb_get`.

## Quick Reference
- Core vars: `JUDO_PLATFORM_RDBMS_DIALECT` (`postgresql`|`hsqldb`), `_RDBMS_DB_HOST/_PORT/_DATABASE/_USER/_PASSWORD`, `JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL` (backend, e.g. `http://auth:8080`), `JUDO_PLATFORM_KEYCLOAK_AUTH_PUBLIC_URL` (browsers), `JUDO_PLATFORM_FILESTORE` + `_FILESTORE_DIRECTORY`, `JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET`.

## Configuration Methods
- Primary: `/judo-karaf.env`, lines `JUDO_PLATFORM_NAME=value`. Generated file has only defaults (signer secret, password policy, `JUDO_PLATFORM_LOG_SMTP_SERVER`, `JUDO_PLATFORM_FILESTORE=rdbms`). Apply: `./judo.sh stop && ./judo.sh start`.
- `./judo.sh env <name>` selects an alternate custom properties file (e.g. `compose-dev.properties`), not `judo.properties`. Template does NOT generate per-environment `judo-karaf.env.<env>` files.
- Not recommended: `JAVA_EXTRA_OPTS="-Djudo.platform.parameterName=value"`; direct `.cfg` editing.

## Parameter Naming Convention
- Env: prefix `JUDO_PLATFORM_`, no hyphen, SNAKE_CASE.
- OSGi/system: camelCase, no prefix (`rdbmsDialect`). System props keep dots (`${system.java_home}` → `java.home`).
- Custom params are case-sensitive: `myprop=${ mypropDev ! "My DEV Prop"}` reads `mypropDev`; `dev` falls back to "My DEV Prop", `qa` to "My QA Prop".
- Conversion: `JUDO_PLATFORM_RDBMS_DIALECT` → `rdbmsDialect`; `JUDO_PLATFORM_KEYCLOAK_AUTH_PUBLIC_URL` → `keycloakAuthPublicUrl`.

## Configuration Categories
- Database: see `schema-evolution.md`; Spring Boot → `spring-boot-runtime.md`; pax-jdbc/version checks → `osgi-runtime-services.md`.
- DB connection: `DB_DATABASE`, `DB_USER`, `DB_PASSWORD` default to lower-case model name in Compose. No `JUDO_PLATFORM_DATASOURCE_URL/_USERNAME/_PASSWORD`; JDBC URL is built from the parts.
- Pool/timeouts: `JUDO_PLATFORM_HIKARI_MAXIMUM_POOL_SIZE`, `_HIKARI_CONNECTION_TIMEOUT` (ms), `_NARAYANA_DEFAULT_TIMEOUT` (ms), `_CASE_INSENSITIVE_LIKE` (`true` for PostgreSQL case-insensitive like).
- Pool: `rdbmsDbPool` / env `JUDO_PLATFORM_RDBMS_DB_POOL`; options `none|hikari|dbcp2|transx`; default `hikari`. No `rdbmsDbPoolType`/`dbPoolType`.
- `managedDatasourceFactory`: `none` (default, JDBC datasource handles tx) | `transx` (Transx JTA).
- Keycloak: `_AUTH_SERVER_URL` (required); `_AUTH_PUBLIC_URL` (param `keycloakAuthPublicUrl`, not `keycloakPublicUrl`); `_KEYCLOAK_REALM`, `_KEYCLOAK_CLIENT_ID`; `_KEYCLOAK_DEFAULT_PASSWORD_POLICY` (shipped env `SAME_EMAIL`, Compose `SAME_USERNAME`); `_KEYCLOAK_MANAGEMENT_ENABLED`, `_USER_MANAGER_ENABLED`, `_KEYCLOAK_USER`, `_KEYCLOAK_PASSWORD`.
- REST: `JUDO_PLATFORM_SWAGGER_UI` / `_SWAGGER_UI_PATH` (default `/swagger-ui`; disable in prod); `JUDO_PLATFORM_CORS_ALLOW_ORIGIN` (don't leave open in prod).
- File storage: `JUDO_PLATFORM_FILESTORE` = `rdbms` (shipped env, compose-develop) | `filesystem` (compose-postgresql-https) | `s3`. `_FILESTORE_DIRECTORY` (Compose `/filestore`); `_FILESTORE_PATH` does not exist.
- S3: `_S3_BUCKET`, `_S3_REGION`, `_S3_ENDPOINT`, `_S3_ACCESS_KEY`, `_S3_SECRET_KEY`, `_FILESTORE_TOKEN_EXPIRY`.
  - `http://` endpoint accepted; activation logs WARN (cleartext), not an error. Use `https://` outside local tests.
- GCS: works via S3 API. `FILESTORE=s3`, endpoint `https://storage.googleapis.com`, HMAC keys as access/secret. Lifecycle rules set in GCS.
- Identifier signing: `JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET` (Base64 HMAC for `__signedIdentifier`).
  - Unset → new random 1024-bit key on EVERY start: signed ids invalid after restart and across cluster nodes. Set the same stable secret on all nodes.
- Mail (SMTP): `_MAIL_SMTP_HOST`/`_PORT`, `_MAIL_SMTP_USER`/`_PASSWORD`, `_MAIL_SMTP_AUTH`, `_MAIL_SMTP_STARTTLS_ENABLE`, `_MAIL_SMTP_FROM`, `_MAIL_TRANSPORT_PROTOCOL`, `_MAIL_SMTP_SSL_TRUST`, `_LOG_SMTP_SERVER` (`true` in shipped files).
  - Default port 25; with `logSmtpServer=true` default `mailSmtpPort` becomes `10025`.
  - Local log SMTP listens on `logSmtpServerPort` (default `1025`), host `logSmtpServerHost` (default `localhost`).
  - Mailpit local: point SMTP at `localhost:1025`, no auth/TLS. Activation/new-user mails use same SMTP config.
  - Test/demo/prod read `_MAIL_SMTP_*` from deployment env (e.g. `environments/<env>/app-compose/docker-compose.yml`).
- Other: `JUDO_PLATFORM_DEFAULT_ZONE_ID` (e.g. `Europe/Budapest`); `_METRICS_ENABLED`; `_MARK_SELECTED_RANGE_ITEMS` (`true` in Compose); `_BUNDLE_WATCHER` (`false` disables hot deployment); `JUDO_STARTUP_FEATURE` (overrides offline Karaf startup feature).
- Banner/JMX: banner printed once all model platform services ready. Keys: `bannerEnabled` (default `true`), `bannerFonts`, `bannerHslStart`/`bannerHslEnd` (`<hue>,<sat>,<light>`, random if unset), `enableJMX` (default `false`; MBean `hu.blackbelt.judo:type=<model>,name=Application`). System prop `disableJudoAnsiColors` (any value) disables ANSI. Readiness: `osgi-runtime-services.md#startup-banner-and-readiness`.

## Configuration Precedence
- `JUDO_PLATFORM_*` env vars are recommended source. `.cfg` edits lost on rebuild; Karaf console changes lost on restart. Keep permanent settings in `judo-karaf.env` or compose env.

## Environment-Specific Configuration
- Local dev: `./judo.sh start` → Karaf port 8181, Keycloak 8080 (under `/auth`); DB from `dbtype` (`hsqldb` default; PostgreSQL via `-o dbtype=postgresql`).
  - Example: `RDBMS_DIALECT=hsqldb`, `FILESTORE=rdbms`, `LOG_SMTP_SERVER=true`.
- Docker Compose: see `production.md#shipped-docker-compose-environments` (`compose-develop`, `compose-postgresql-https`).
- Production example: `RDBMS_DIALECT=postgresql`, DB host/port/database/user `<app>_prod`, password from secrets; Keycloak server and public URL `https://auth.example.com`; signer secret stable; `FILESTORE=filesystem` + `/filestore`; `SWAGGER_UI=false`.
- New environment (prod/test/demo):
  - Separate Keycloak address, seed data and secrets per env.
  - Init-time admin users must pass through the whole chain: startup template (e.g. `app-startup.sh.tpl`) and infra config (e.g. terraform). A missing link → Keycloak admin users silently not created on first init.
  - Schema updates: run schema tool in `generate` or `execute` mode; back up DB before `execute`; keep restore command ready. See `schema-evolution.md`.

## Encrypted Values (Jasypt)
- `password=ENC(<encrypted>)` in config files. `org.jasypt.encryption.StringEncryptor` OSGi service (features `karaf-jasypt-support` / `osgi-encryption`) decrypts on read. Encrypt via Karaf command; replace in PAX-JDBC / DBCP2 files.
- Password source order: `encryption_password` → `encryption_passwordFile` → env var named by `encryption_passwordEnvName`.
  - `encryption_passwordEnvName` has no default and no fallback; if none set, no source read.
  - `encrypt`/`decrypt` shell commands without explicit password read env `ENCRYPTION_PASSWORD`.

## Applying Configuration Changes
- Method 1 (recommended): `./judo.sh stop` then `./judo.sh start`.
- Method 2 (runtime): `./application/.karaf/bin/client`, then `config:edit hu.blackbelt.judo.runtime`, `config:property-set <name> <value>`, `config:update`; `config:list`. Lost on restart; also persist in env.

## Security Best Practices
- Never commit secrets; commit templates with placeholders (`${DB_PASSWORD}`).
- Use a secrets manager (Vault, cloud, K8s Secrets) or Jasypt `ENC(...)`.
- Rotate secrets; rotating `JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET` invalidates all signed identifiers held by clients.
- Least privilege for DB user and Keycloak client.

## Troubleshooting
- Not applied: restart (`stop` + `start`); check `JUDO_PLATFORM_` prefix, no hyphen, exact names; `tail -f application/.karaf/data/log/karaf.log`.
- Effective config: `./application/.karaf/bin/client` → `config:list | grep judo`.
- DB connection failed: check `JUDO_PLATFORM_RDBMS_DB_*` and `_DIALECT`; test `psql -h localhost -U <app> -d <app>`. After PostgreSQL retry loop fails, platform only logs an error and creates no datasource for the model (`osgi-runtime-services.md#postgresql-bootstrap-retry-and-datasource-keys`).
- Keycloak auth failed: check `_AUTH_SERVER_URL` / `_AUTH_PUBLIC_URL`, realm exists: `curl http://localhost:8080/realms/<app>` (path prefix depends on Keycloak version).

## Reference Documentation
- JUDO Platform Parameters: https://internal-documentation.judo.technology/administrator-guide/03_platform_parameters.html

## File Locations
- `/judo-karaf.env`; `/application/karaf-offline/etc/`; `/application/.karaf/data/log/karaf.log`.

## Related Documentation
- `build-process.md`, `production.md`, `local-development.md`, `schema-evolution.md`.
- `../backend/` — custom operations and other backend topics.
