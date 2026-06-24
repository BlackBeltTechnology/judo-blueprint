---
name: judo-deployment-docs
description: Deployment and build documentation for JUDO applications. Covers judo.sh commands, Docker setup, Karaf configuration, and production deployment.
disable-model-invocation: false
user-invocable: false
agent: general-purpose
---

# Deployment Documentation

## Overview

The {{ lowerCase model.name \}} project uses a sophisticated build system orchestrated by `judo.sh` script and Maven. This documentation provides comprehensive guidance for building, deploying, and troubleshooting the application.

**Note**: Throughout this documentation, `{{ lowerCase model.name \}}` refers to the application name from `judo.properties` (app_name property). This value is used in artifact names, bundle names, and deployment configurations.

## Quick Reference

### Essential Commands

```bash
# Build from scratch (WARNING: Takes several minutes for complete project)
./judo.sh build

# Build and start
./judo.sh build start

# Stop services
./judo.sh stop

# Check status
./judo.sh status

# Fast iteration mode
./judo.sh reckless

# Clean everything
./judo.sh clean

# View help
./judo.sh --help
```

> **Important**: A full `./judo.sh build` for the complete project can take **several minutes** (5-15+ minutes depending on hardware). When running in automated environments or background processes, ensure appropriate timeouts are configured. Never run multiple concurrent builds as they will conflict.

> **Critical for AI Agents**: The `judo.sh` script uses **mvnd (Maven Daemon)** which requires a stable PTY (pseudo-terminal) environment. When running `judo.sh` commands from automated/background processes:
>
> 1. **Always use `screen` or `tmux`** to provide a stable terminal session
> 2. **Check for availability first** - if neither `screen` nor `tmux` is installed, **terminate the task and notify the user**
> 3. Running without a session manager will cause `StaleAddressException` errors due to daemon communication failures
>
> Example usage with screen:
> ```bash
> # Check if screen or tmux is available
> command -v screen || command -v tmux || { echo "ERROR: screen or tmux required for judo.sh"; exit 1; }
>
> # Start build in detached screen session
> screen -dmS judo-build bash -c './judo.sh build 2>&1 | tee /tmp/judo-build.log'
>
> # Monitor progress
> tail -f /tmp/judo-build.log
>
> # Or check screen output directly
> screen -r judo-build
> ```

### Common Workflows

- **First-time setup**: `./judo.sh build start`
- **Development iteration**: `./judo.sh reckless` (fast builds)
- **Production build**: `./judo.sh build -DskipDocker=false`
- **Stop all services**: `./judo.sh stop`

## Deployment Guides

This documentation is organized into context-specific guides:

### [Build Process](./build-process.md)
Comprehensive guide to the build system:
- judo.sh command reference
- Maven profiles and configuration
- Build workflows (full, incremental, reckless)
- Build system architecture
- Performance optimization

### [Local Development](./local-development.md)
Development environment setup and workflow:
- Hot deployment explained
- Development server setup
- Local deployment workflow
- Troubleshooting local development
- Development best practices

### [Production Deployment](./production.md)
Production deployment guide:
- Production deployment process
- Docker deployment
- Environment configuration
- Production best practices
- Monitoring and debugging

### [Application Configuration](./application-config.md)
Configuration for different environments:
- Environment variables
- `judo-karaf.env` file
- Security and database settings

## Build System Architecture

### Components

```
judo.sh (orchestration)
    ↓
Maven (build tool)
    ├→ Model Transformation (application/model/)
    ├→ Schema Generation (application/schema/)
    ├→ SDK Generation (application/sdk/)
    ├→ Backend Compilation (application/app/, interceptors/)
    ├→ Frontend Generation (application/frontend-react/)
    ├→ Karaf Assembly (application/karaf-offline/)
    └→ Docker Image (application/docker/)
```

## File Locations Reference

- Build script: `/judo.sh`
- Root POM: `/pom.xml`
- Application POM: `/application/pom.xml`
- Karaf distribution: `/application/karaf-offline/target/assembly/`
- Docker context: `/application/docker/target/docker/`
- Runtime logs: `/application/.karaf/data/log/karaf.log`

## Access Points

When services are running locally:

- **Application**: http://localhost:8181/apps/
- **API Spec**: http://localhost:8181/api-spec/{{ lowerCase model.name \}}
- **Health Check**: http://localhost:8181/system/health?tags={{ lowerCase model.name \}}
- **Keycloak Admin**: http://localhost:8080
- **Karaf SSH**: `ssh -p 8101 karaf@localhost` (password: karaf)

## Health Check Endpoint

Check backend health at: `http://localhost:8181/system/health?tags={{ lowerCase model.name \}}`

### Response Format

**HTML format** (default):
```
http://localhost:8181/system/health?tags={{ lowerCase model.name \}}
```

**JSON format** (recommended for automation):
```
http://localhost:8181/system/health?tags={{ lowerCase model.name \}}&format=json
```

### JSON Response Structure

```json
{
    "overallResult": "OK",
    "results": [
        {
            "name": "ModelsCheck",
            "status": "OK",
            "timeInMs": 0,
            "finishedAt": "2025-12-02T20:45:21.339",
            "tags": ["{{ lowerCase model.name \}}"],
            "messages": [
                {
                    "status": "OK",
                    "message": "All models are active"
                }
            ]
        },
        {
            "name": "OperationsCheck",
            "status": "OK",
            "timeInMs": 0,
            "finishedAt": "2025-12-02T20:45:21.339",
            "tags": ["{{ lowerCase model.name \}}"],
            "messages": [
                {
                    "status": "OK",
                    "message": "All operations are active"
                }
            ]
        },
        {
            "name": "PlatformComponentsCheck",
            "status": "OK",
            "timeInMs": 10,
            "finishedAt": "2025-12-02T20:45:21.349",
            "tags": ["{{ lowerCase model.name \}}"],
            "messages": [
                {
                    "status": "OK",
                    "message": "All platform components are active"
                }
            ]
        }
    ]
}
```

### Health Check Status Values

| Status | Description | CSS Class |
|--------|-------------|-----------|
| `OK` | All checks passed | `statusOK` (green) |
| `WARN` | Warning condition | `statusWARN` (yellow) |
| `TEMPORARILY_UNAVAILABLE` | Temporary issue | `statusTEMPORARILY_UNAVAILABLE` (purple) |
| `CRITICAL` | Critical failure | `statusCRITICAL` (orange) |
| `HEALTH_CHECK_ERROR` | Check itself failed | `statusHEALTH_CHECK_ERROR` (red) |

### Health Checks Performed

1. **ModelsCheck** - Verifies all JUDO models are active
2. **OperationsCheck** - Verifies all operations are registered and active
3. **PlatformComponentsCheck** - Verifies all platform OSGi components are active

### URL Parameters

| Parameter | Description |
|-----------|-------------|
| `tags` | Comma-separated list of health check tags (e.g., `{{ lowerCase model.name \}}`) |
| `names` | Comma-separated list of specific health check names |
| `format` | Output format: `html`, `json`, `jsonp`, `txt`, `verbose.txt` |
| `httpStatus` | Custom HTTP status mapping (e.g., `CRITICAL:503`) |
| `timeout` | Timeout in milliseconds for health checks |
| `forceInstantExecution` | If `true`, bypasses cache and executes checks immediately |

### Example: Check Health with curl

```bash
# HTML format (human-readable)
curl "http://localhost:8181/system/health?tags={{ lowerCase model.name \}}"

# JSON format (for scripts/automation)
curl -s "http://localhost:8181/system/health?tags={{ lowerCase model.name \}}&format=json" | jq .

# Check overall status only
curl -s "http://localhost:8181/system/health?tags={{ lowerCase model.name \}}&format=json" | jq -r '.overallResult'
```

### Detailed Health Check (Felix Web Console)

The public `/system/health` endpoint returns only the aggregate result. For a per-check breakdown (each Felix Health Check's status, log messages, and execution time) use the Web Console endpoint:

```
http://localhost:8181/system/console/healthcheck?tags=*&overrideGlobalTimeout=
```

- **Auth**: HTTP Basic, default Karaf user — username `karaf`, password `karaf`.
- **`tags=*`**: include every registered check (use a specific tag, e.g. `{{ lowerCase model.name \}}`, to narrow).
- **`overrideGlobalTimeout=`** (empty): disables the global timeout so slow checks complete instead of being reported as `HEALTH_CHECK_TIMED_OUT`. Provide a value in ms to set a custom timeout.

```bash
curl -u karaf:karaf \
  "http://localhost:8181/system/console/healthcheck?tags=*&overrideGlobalTimeout="
```

Use this endpoint when `/system/health` reports `CRITICAL`/`WARN` and you need to see which individual check failed and its log output.

### Tracing a Failure Back to a Missing Component

Most JUDO platform health checks (`Components`, `Bundles`, the per-model `<modelname>` check) fail because an OSGi Declarative Services component never reached `active`. The Felix Web Console SCR Components endpoint is the next hop after the health check log.

- **URL**: `http://localhost:8181/system/console/components` (HTML) or `…/components.json` (JSON).
- **Auth**: HTTP Basic, `karaf` / `karaf`.
- **Drill-down**: `…/components/<component.name>.json` returns the component's bundle, configuration policy, and every `Reference …` line — the unsatisfied reference is what the SCR is waiting on.

**States to recognise:**

| State | Meaning | Action |
|---|---|---|
| `active` | Running. | Healthy. |
| `satisfied` | All refs bound, not yet activated (lazy / factory). | Usually fine. |
| `no config` | `configurationPolicy=require`, no PID configured. | Check `etc/<pid>.cfg` and `/system/console/configMgr`. |
| `unsatisfied (reference)` | One or more `@Reference`s not bound. | Open the component JSON, find the missing `Reference …` line, then locate its provider bundle/component. |
| `failed activation` | `@Activate` threw. | Check `data/log/karaf.log` for the stack trace. |
| *(component absent from list)* | Bundle not started, or `@Component` annotation/SCR descriptor missing. | Check `/system/console/bundles` for the owning bundle's state (`Installed`/`Resolved` instead of `Active`). |

**Worked example** (real failing run from a JUDO project):

```
/system/console/healthcheck?tags=*&overrideGlobalTimeout=
  → TEMPORARILY_UNAVAILABLE
    Missing platform components:
      [hu.blackbelt.judo.services.healthcheck.osgi.JaxRsApplicationsReady]
```

Look it up in the components endpoint:

```bash
curl -s -u karaf:karaf "http://localhost:8181/system/console/components.json" \
  | jq -r '.data[] | select(.name | test("JaxRsApplicationsReady")) | "\(.state)\t\(.bundleId)\t\(.name)"'
```

If the grep returns **nothing**, the component is not even registered — inspect its owning bundle:

```bash
curl -s -u karaf:karaf "http://localhost:8181/system/console/bundles.json" \
  | jq -r '.data[] | select(.symbolicName | test("healthcheck")) | "\(.state)\t\(.symbolicName)"'
```

If the grep returns a row with state `unsatisfied (reference)`, fetch the component detail and read the `Reference …` properties to identify the missing service:

```bash
curl -s -u karaf:karaf \
  "http://localhost:8181/system/console/components/<component.name>.json" \
  | jq -r '.data[0].props[] | select(.key | startswith("Reference ")) | "\(.key): \(.value)"'
```

> **Per-model wiring & marker services**: many "missing component" failures are actually missing *services* (e.g. `*Ready` markers) registered programmatically by per-model SCR components, which in turn are spawned via `ConfigurationAdmin` factory configs from `*Activator` components in `judo-platform-services/`. For the full 3-tier chain (model deployer → activator → target component) and the matching trace-back checklist, see [`../backend/debugging-and-monitoring-guide.md`](../backend/debugging-and-monitoring-guide.md) → *"The Activator → ConfigAdmin → Component Chain"*.

### One-shot Runtime Snapshot (Configuration Status Dump)

For a single-file capture of *everything* the Felix Web Console can show — bundles, services, DS components, ConfigAdmin PIDs, framework properties, threads, memory, system properties, and platform-specific printers — use the **Configuration Status** download.

```bash
# Full plain-text snapshot
curl -u karaf:karaf -o judo-status.txt \
  "http://localhost:8181/system/console/config/configuration-status-$(date +%Y%m%d-%H%M%S).txt"

# Full ZIP (each tab as a separate file)
curl -u karaf:karaf -o judo-status.zip \
  "http://localhost:8181/system/console/config/configuration-status-$(date +%Y%m%d-%H%M%S).zip"

# Single tab (e.g. Components, Configurations, Bundles, Services, Health Checks)
curl -u karaf:karaf "http://localhost:8181/system/console/config/Components.nfo"
```

The filename segment is a placeholder — the server only inspects the `.txt` / `.zip` / `.nfo` extension. Useful for: attaching to bug reports, diffing before-vs-after a deploy/undeploy, and feeding into LLM-assisted diagnosis. See backend debugging guide for details and integration with the trace-back checklist.

## Next Steps

1. **New to the project?** Start with [Local Development](./local-development.md)
2. **Building for production?** See [Production Deployment](./production.md)
3. **Understanding the build?** Read [Build Process](./build-process.md)
