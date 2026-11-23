---
title: Local Development
description: Starting the application locally, hot deployment, Karaf console, logs and local troubleshooting.
aliases: [run locally, start the app locally, hot deploy, karaf console, local logs, local troubleshooting]
keywords: [judo.sh, karaf_port, karaf.log, bundle:restart, bundle:update, service:list, mvn install, reckless, hsqldb, judo-karaf.env]
tags: [domain:deployment, layer:infrastructure, status:platform]
---

# Local Development

This guide covers local development setup, hot deployment, and development workflows for the <app> project.

## Table of Contents

- [Development Server Setup](#development-server-setup)
- [Hot Deployment](#hot-deployment)
- [Development Workflow](#development-workflow)
- [Monitoring and Debugging](#monitoring-and-debugging)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Key Concepts

- **Hot Deployment**: A development feature that allows you to apply backend code changes to a running server without a full restart. This enables a fast and efficient development loop.
- **Karaf Console**: A command-line interface for the running Karaf server. It allows you to manage bundles, view logs, and change configurations at runtime.
- **Incremental Builds**: The process of building only the modules that have changed, rather than the entire application. This significantly speeds up the development workflow.

## Development Server Setup

### Starting Services

#### Start all services
```bash
./judo.sh start
```

#### What starts
- PostgreSQL (Docker container, port 5432) when `dbtype=postgresql`; the generated `judo.properties` sets `dbtype=hsqldb`, which runs the embedded HSQLDB instead
- Keycloak (Docker container, port 8080)
- Karaf (standalone, HTTP port **8181** by default; override with `./judo.sh start -o karaf_port=<port>`)

`./judo.sh start` needs a running Docker daemon for the PostgreSQL and Keycloak containers (or the Compose stack); run `docker info` first and start Docker if it fails. The command launches Karaf in the background (console output in `application/.karaf/console.out`) and returns before the application is ready, so wait until the application URL answers with HTTP 200 before running tests; connection-refused errors in tests usually mean the stack is not up yet.

**Prerequisites:** generated projects and the workflow plugin build with Java 21 (`java.version` 21), not Java 1.8 or 11. There is no `run-offline-postgresql.sh` script in generated projects; use `./judo.sh start -o dbtype=postgresql` to get a PostgreSQL database.

#### Access points
- Application: http://localhost:8181/<model>/<Actor>/ (each actor frontend is served under its own context path; `/apps/` only lists the bundles)
- Keycloak Admin: http://localhost:8080/auth (`judo.sh` starts Keycloak with `--http-relative-path /auth`; with `keycloak_port=<port>` the base URL is `http://localhost:<port>/auth`; 8080 is the Keycloak port, not the application's)
- Karaf SSH: `ssh -p 8101 karaf@localhost` (password: karaf) - these are Apache Karaf defaults, not set by the project template

**Start options:** `./judo.sh start -o "runtime=karaf|compose,dbtype=hsqldb|postgresql,compose_env=...,karaf_port=...,postgres_port=...,keycloak_port=..."`, `-K` skips Keycloak, `-w` disables bundle watching (`--skip-watch-bundles`). See [Build Process](./build-process.md#command-reference). Compose-based runs are described in [Production Deployment](./production.md#shipped-docker-compose-environments).

**First login:** a fresh local app has no user. Open the Keycloak admin console (`/auth`, realm `<app>`), create a user there, and make sure a matching actor instance exists, or let the backend create it on first login (see [Keycloak JIT User Provisioning](../../best-practices/backend/keycloak-jit-user-provisioning.md)).

**Local email:** run a mail catcher such as Mailpit and point the app at `localhost:1025` (no auth/TLS) in `judo-karaf.env`; see [Application Configuration](./application-config.md#6-email-smtp).

### Stopping Services

#### Stop all services
```bash
./judo.sh stop
```

### Checking Status

#### Check service status
```bash
./judo.sh status
```

## Hot Deployment

Hot deployment allows you to make changes and see them immediately without restarting the entire application.

### How It Works

1. Build module: `mvn install`
2. JAR installed to local Maven repo (`~/.m2/repository/`)
3. Karaf watches for changes
4. Bundle automatically updated
5. Services re-registered

### What Supports Hot Deployment

#### Supports hot deployment
- Custom operations (`application/app/`)
- Interceptors (`application/interceptors/`)
- Frontend JAR (`application/frontend-react/`)
- REST endpoints (via bundle update)

#### Requires restart
- Model changes (schema evolution)
- Configuration changes
- Feature definition changes

### Example Workflow

```bash
# 1. Start Karaf
./judo.sh start

# 2. Make changes in application/app/
vim application/app/src/main/java/.../CustomService.java

# 3. Build
cd application/app
mvn install

# 4. Watch Karaf logs
tail -f application/.karaf/data/log/karaf.log

# Output:
# Bundle updated: <app>-app
# Service registered: CustomAddressService

# 5. Test immediately - no restart needed
curl http://localhost:8181/api/entity/Address
```

## Development Workflow

### Rapid Iteration

For fast development cycles:

```bash
# 1. Start services once
./judo.sh start

# 2. Use reckless mode for fast builds
./judo.sh reckless

# 3. Make changes and rebuild specific modules
cd application/app
mvn install

# 4. Changes auto-deploy to running Karaf
```

### Incremental Builds

Build only changed modules:

```bash
# Backend code changed
cd application/app
mvn install

# Frontend changed
cd application/frontend-react/<app>__[actor_fqn]
mvn install

# Multiple modules
mvn install -pl application/app,application/interceptors
```

## Monitoring and Debugging

### Karaf Console

#### Connect to Karaf console
```bash
./application/.karaf/bin/client
# or
ssh -p 8101 karaf@localhost
```

#### Useful commands
```bash
# List bundles
bundle:list | grep <app>

# View bundle details
bundle:info <app>-app

# View services
service:list

# View logs
log:tail

# Restart bundle
bundle:restart <app>-app

# View configuration
config:list
```

### Logs

#### Locations
- Karaf: `application/.karaf/data/log/karaf.log`
- Docker: `docker logs <app>-app`

#### Tail logs
```bash
tail -f application/.karaf/data/log/karaf.log

# Filter errors
tail -f karaf.log | grep ERROR

# Watch bundle updates
tail -f karaf.log | grep "Bundle"
```

## IDE Launch Configurations

The template ships Eclipse m2e launchers in the generated `launcher` folder: `BuildApplication`, `BuildApplicationWithoutFrontend`, `CompileCustomApp`, `RunApplication` and `RunFrontend` (details in [Build Process](./build-process.md#eclipse-launch-configurations)).

## Local Database Choice and Tests

`./judo.sh start -o dbtype=hsqldb` runs against HSQLDB, the default from the generated `judo.properties` is `dbtype=hsqldb`; `-o dbtype=postgresql` (or `dbtype=postgresql` in `judo.properties`) runs PostgreSQL in Docker. After a rebuild always use `./judo.sh build -i` when tests and the running application disagree (stale `~/.m2` artifacts, see [Build Process](./build-process.md#stale-artifacts-and-multi-module-build-order)). Do not run the long `initdatatests` in the normal cycle.

## Troubleshooting

### Runtime Issues

#### "Port 8181 (or 8080) already in use"

##### Solution
- Check running processes: `lsof -i :8181` (Karaf) or `lsof -i :8080` (Keycloak)
- Stop the conflicting service or start with another port: `./judo.sh start -o karaf_port=<port>`

#### "Database connection failed"

##### Solution
- Check PostgreSQL running: `docker ps | grep postgres`
- Restart PostgreSQL: `docker restart [container-name]`

#### "Keycloak authentication failed"

##### Solution
- Check Keycloak running: `docker ps | grep keycloak`
- Verify Keycloak configuration in environment variables

#### "Bundle not starting"

##### Solution
- Check dependencies: `bundle:diag [bundle-id]`
- View bundle details: `bundle:info [bundle-id]`
- Check logs: `log:tail`

#### `Unable to access jarfile` for `target/judo-cli.jar`

`target/judo-cli.jar` is copied into the root `target/` only by a `generate-root` run (the download execution overwrites it each time); a plain `mvn install` does not produce it. If the jar is missing (after a clean, a prune or a fresh checkout), run `./judo.sh generate-root` to restore it before calling the CLI.

### Hot Deployment Issues

#### "Changes not applied"

##### Solution
- Verify bundle updated: `bundle:list -t 0`
- Check JAR timestamp: `ls -l ~/.m2/repository/.../<app>-app/`
- Force refresh: `bundle:update [bundle-id]`

#### "Service not registered"

##### Solution
- Check bundle status: `bundle:list | grep <app>`
- Restart bundle: `bundle:restart [bundle-id]`
- Check for errors: `log:tail`

## Best Practices

### Development Workflow

1. **Keep Karaf running** - Leverage hot deployment instead of restarting
2. **Monitor logs** - Keep `tail -f karaf.log` in separate terminal
3. **Use incremental builds** - Build only what changed
4. **Use reckless mode** - For rapid iteration during development
5. **Test before committing** - Run full clean build before commits

### Performance Tips

1. **Use parallel builds** when building multiple modules:
   ```bash
   mvn install -T 4 -pl application/app,application/interceptors
   ```

2. **Skip unnecessary profiles** during development:
   ```bash
   mvn install -DskipDocker -DskipFrontendReact
   ```

3. **Keep dependencies cached** - Don't clean Maven repository frequently

### Environment Variables

**Frontend** (`.env` or export):
```bash
VITE_API_DEFAULT_BASE_URL=http://localhost:8181
VITE_KEYCLOAK_URL=http://localhost:8080/auth
VITE_KEYCLOAK_REALM=<app>
```

## Related Documentation

- [Build Process](./build-process.md) - Detailed build system documentation
- [Production Deployment](./production.md) - Production deployment guide
- [Deployment Overview](./README.md) - Main deployment documentation
