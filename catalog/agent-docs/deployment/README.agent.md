# README.md — index

Pull-only condensed map. Source: catalog/agent-docs/deployment/README.md.

## Overview
- Build/deploy orchestrated by `judo.sh` + Maven. `<app>` = `app_name` from `judo.properties`; used in artifact, bundle and deployment names.

## Quick Reference
- Commands: `./judo.sh build` (from scratch, several minutes), `build start`, `stop`, `status`, `reckless` (fast iteration), `build -d` (with Docker images), `build -i` (ignore checksums; use when build fails or artifacts look stale), `env <name> build start` (alternate properties, e.g. `compose-dev`), `update`, `generate`, `generate-root`, `dump`, `import`, `schema-upgrade`, `prune`, `clean`, `--help`.
- Automated/agent runs: `judo.sh` uses mvnd, which needs a PTY. Use `screen` or `tmux`; if neither exists, stop and notify the user. Without one: `StaleAddressException`.
- Long build: run detached (`screen -dmS judo-build bash -c './judo.sh build 2>&1 | tee /tmp/judo-build.log'`), then tail the log.
- Workflows: first setup `./judo.sh build start`; iteration `./judo.sh reckless`; production image `./judo.sh build -d` (no `-D` pass-through; `-DskipDocker=false` still skips Docker); stop `./judo.sh stop`.
- Build chain: judo.sh → Maven → model transformation, schema, SDK, backend compile (app, interceptors), frontend generation, Karaf assembly, Docker image.

## Deployment Guides
- Pointers to sibling guides: build-process, local-development, production, application-config, schema-evolution, osgi-runtime-services, spring-boot-runtime, generator-plugins, tooling-guide.

## Build System Architecture
- Component diagram in source: judo.sh orchestrates Maven, which builds each module (see Quick Reference chain).

## File Locations Reference
- Build script `/judo.sh`; root POM `/pom.xml`; app POM `/application/pom.xml`.
- Karaf distribution `/application/karaf-offline/target/assembly/`; Docker context `/application/docker/target/docker/`.
- Runtime log `/application/.karaf/data/log/karaf.log`.

## Access Points
- App: `http://localhost:8181/<model>/<Actor>/` (`/apps/` lists bundles only).
- API spec: `http://localhost:8181/api-spec/<app>`.
- Health: `http://localhost:8181/system/health?tags=<app>`.
- Keycloak admin: `http://localhost:8080/auth` (started with `--http-relative-path /auth`; app is on 8181).
- Karaf SSH: `ssh -p 8101 karaf@localhost`, password `karaf` (Karaf defaults, not set by the template).

## Health Check Endpoint
- Endpoint is `/system/health`, not `/health`. Query-param, status-code and serializer details: OSGi Runtime Services guide (health-check endpoint details). Custom checks are implemented there too.
- Formats: HTML (default); JSON recommended for automation.
- Status values: `OK` (statusOK, green), `WARN` (yellow), `TEMPORARILY_UNAVAILABLE` (purple), `CRITICAL` (orange), `HEALTH_CHECK_ERROR` (red, check itself failed).
- Checks: `ModelsCheck` (models active), `OperationsCheck` (operations registered/active), `PlatformComponentsCheck` (platform OSGi components active).
- URL params: `tags` (comma list), `names`, `format` (`html`, `json`, `jsonp`, `txt`, `verbose.txt`), `httpStatus` (e.g. `CRITICAL:503`), `timeout` (ms), `forceInstantExecution=true` (bypass cache).
- HTTP mapping: OK/WARN → 200; TEMPORARILY_UNAVAILABLE/CRITICAL → 503; HEALTH_CHECK_ERROR → 500. `format=txt` returns only the status name (load balancers).
- Per-check breakdown: Felix Web Console `/system/console/healthcheck?tags=*&overrideGlobalTimeout=` with HTTP Basic `karaf`/`karaf`. Empty `overrideGlobalTimeout` disables the global timeout (otherwise slow checks become `HEALTH_CHECK_TIMED_OUT`). Use when health is CRITICAL/WARN.
- Typical failure: `TEMPORARILY_UNAVAILABLE` with `Missing platform components: [...JaxRsApplicationsReady]`.
- Tracing a missing component: SCR components at `/system/console/components` (or `.json`; detail `/components/<name>.json`); states: `active` (healthy), `satisfied` (usually fine), `no config` (check `etc/<pid>.cfg`, configMgr), `unsatisfied (reference)` (find missing `Reference …` line and its provider), `failed activation` (`@Activate` threw; see `karaf.log`), component absent (bundle not started; check `/system/console/bundles` for Installed/Resolved).
- Marker services such as `*Ready` are often registered programmatically by per-model SCR components; a "missing component" may be a missing service.
- Configuration status dump: `/system/console/config/configuration-status-<timestamp>.txt`, `.zip` (every tab as file) or `<Tab>.nfo` (e.g. `Components`, `Bundles`, `Services`). Use for bug reports and before/after diffs.

## Next Steps
- New to project: Local Development. Production: Production Deployment. Build: Build Process.
