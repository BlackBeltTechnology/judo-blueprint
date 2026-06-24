# Debugging, Monitoring, and Performance Guide

## Overview

This guide provides a comprehensive overview of the tools and techniques available for debugging, monitoring, and profiling a running JUDO application. It covers everything from rapid development workflows to production troubleshooting.

## Table of Contents

- [Hot Deployment Workflow (Development)](#hot-deployment-workflow-development)
- [Logging](#logging)
- [Remote Debugging](#remote-debugging)
- [Monitoring and Health Checks](#monitoring-and-health-checks)
- [Performance Monitoring](#performance-monitoring)
- [Troubleshooting](#troubleshooting)

---

## Hot Deployment Workflow (Development)

Hot deployment allows you to apply backend code changes to a running server without a full restart, enabling a fast and efficient development loop.

1.  **Start the Karaf server** in one terminal:
    ```bash
    ./judo.sh start
    ```

2.  **Make changes** in your custom code (e.g., in `application/app/` or `application/interceptors/`).

3.  **Build only the changed module** from within its own directory:
    ```bash
    cd application/app
    mvn install
    ```

4.  **Watch the Karaf logs** to confirm the bundle is updated. The running server will automatically detect the changed JAR and redeploy it.
    ```bash
    tail -f application/.karaf/data/log/karaf.log
    ```
    You should see a message like `Bundle updated: webshop-app`.

5.  **Test your changes immediately** in the running application.

---

## Logging

JUDO applications use the **SLF4J** facade over the **Log4j 2** implementation.

### Adding Logs to Custom Code
The recommended approach is to use the `@Slf4j` annotation from Lombok to reduce boilerplate code.

```java
import lombok.extern.slf4j.Slf4j;

@Slf4j
@Component
public class CustomOperation implements operation.demo.CustomOperation {

    @Override
    public void apply(InputParameter inputParameter) {
        log.info("Custom operation called with input: {}", inputParameter);
        log.debug("Detailed input: {}", inputParameter.getDetails());
        
        try {
            // ... operation logic ...
        } catch (Exception e) {
            log.error("Error during custom operation", e);
            throw e;
        }
    }
}
```

### Mapped Diagnostic Context (MDC)
JUDO automatically enriches every log message with a request-specific context, which is invaluable for tracing and debugging in a multi-user environment.

| MDC Attribute | Description |
| :--- | :--- |
| `RequestExchangeId` | A unique identifier for the entire HTTP request. |
| `operation` | The fully qualified name of the JUDO operation being executed. |
| `user` | The username from the OAuth 2.0 access token. |

### Changing Log Levels at Runtime
You can dynamically change log levels for any package or class without restarting the application by using the Karaf console.

1.  Log in to the console: `application/.karaf/bin/client`
2.  Use the `log:set` command. For example, to enable detailed SQL logging:
    ```karaf
    log:set DEBUG hu.blackbelt.judo.services.dao
    ```
    To reset to the default level, use `log:set DEFAULT <package>`.

---

## Remote Debugging

You can attach a Java debugger from your IDE (like IntelliJ or VS Code) to a running JUDO application.

### Enabling the Debugger
Start the JUDO application with the `KARAF_DEBUG` environment variable set to `true`.

```bash
export KARAF_DEBUG=true
# Optional: Configure the port and allow remote connections
export JAVA_DEBUG_PORT=*:5005

./judo.sh start
```
The JVM will start suspended, waiting for a debugger to attach on the specified port.

### Attaching from an IDE
1.  In your IDE, create a new **Remote JVM Debug** run configuration.
2.  Set the **Host** to `localhost` and the **Port** to `5005` (or your configured port).
3.  Start the debug configuration. Your IDE will attach to the running JVM, and you can now use breakpoints, inspect variables, and step through your custom Java code.

---

## Monitoring and Health Checks

### JMX Monitoring
Java Management Extensions (JMX) provide a standard way to monitor a running Java application.

*   **Tools**: `JConsole` (included with the JDK) or `VisualVM`.
*   **Key JUDO MBean**: `hu.blackbelt.judo:type=<ModelName>,name=Application`
*   **Key Attribute**: `Started` (boolean). You can monitor this attribute to confirm that the application has started successfully and all components are initialized.

### Application Health Checks
JUDO uses Apache Felix Health Check to provide a status endpoint for automated monitoring.

*   **Endpoint URL**: `http://localhost:8181/system/health?tags=<ModelName>`
*   **Checks**: The endpoint verifies that all models, operations, and platform components (Dispatcher, REST endpoints, persistence layer) have been deployed and initialized successfully. A `200 OK` response indicates a healthy application.

#### Detailed Health Check (Felix Web Console)

For a per-check breakdown (each registered check, its status, log messages, and execution time):

*   **Endpoint URL**: `http://localhost:8181/system/console/healthcheck?tags=*&overrideGlobalTimeout=`
*   **Auth**: HTTP Basic, `karaf` / `karaf` (default Karaf user).
*   **`tags=*`**: include every check; replace with a specific tag (e.g. `<ModelName>`) to narrow.
*   **`overrideGlobalTimeout=`**: empty disables the global timeout (slow checks complete instead of returning `HEALTH_CHECK_TIMED_OUT`); pass a number in ms to set a custom timeout.

```bash
curl -u karaf:karaf \
  "http://localhost:8181/system/console/healthcheck?tags=*&overrideGlobalTimeout="
```

Use when `/system/health` reports a non-OK overall status and you need to identify which individual check failed.

#### Tracing a Failure Back to a Missing SCR Component

JUDO platform health checks (`Components`, `Bundles`, the per-model `<modelname>` check) typically fail because an OSGi Declarative Services component never reached `active`. The Felix Web Console SCR Components endpoint is the next hop after reading the health check log.

- **URL**: `http://localhost:8181/system/console/components` (HTML) or `…/components.json` (JSON).
- **Auth**: HTTP Basic, `karaf` / `karaf`.
- **Drill-down**: `…/components/<component.name>.json` returns the component's bundle, configuration policy, and every `Reference …` line — each `unsatisfied (reference)` row points at exactly the service the SCR is waiting on.

**Component states to recognise:**

| State | Meaning | Action |
|---|---|---|
| `active` | Running. | Healthy. |
| `satisfied` | References bound, not yet activated (lazy / factory). | Usually fine. |
| `no config` | `configurationPolicy=require` and PID has no config. | Check `etc/<pid>.cfg` and `/system/console/configMgr`. |
| `unsatisfied (reference)` | One or more `@Reference`s not bound. | Open component JSON, find missing `Reference …` line, locate its provider. |
| `failed activation` | `@Activate` threw. | Check `data/log/karaf.log` for the stack trace. |
| *(component absent)* | Bundle not started, or `@Component` annotation / SCR descriptor missing. | Check `/system/console/bundles` for owning bundle (`Installed`/`Resolved` instead of `Active`). |

**Worked example** (real failing run):

```
/system/console/healthcheck?tags=*&overrideGlobalTimeout=
  → TEMPORARILY_UNAVAILABLE
    Missing platform components:
      [hu.blackbelt.judo.services.healthcheck.osgi.JaxRsApplicationsReady]
```

Look it up:

```bash
curl -s -u karaf:karaf "http://localhost:8181/system/console/components.json" \
  | jq -r '.data[] | select(.name | test("JaxRsApplicationsReady")) | "\(.state)\t\(.bundleId)\t\(.name)"'
```

- **Empty result** → component not registered. Inspect owning bundle:
  ```bash
  curl -s -u karaf:karaf "http://localhost:8181/system/console/bundles.json" \
    | jq -r '.data[] | select(.symbolicName | test("healthcheck")) | "\(.state)\t\(.symbolicName)"'
  ```
- **State `unsatisfied (reference)`** → fetch component detail and read each `Reference …` to find the missing service:
  ```bash
  curl -s -u karaf:karaf \
    "http://localhost:8181/system/console/components/<component.name>.json" \
    | jq -r '.data[0].props[] | select(.key | startswith("Reference ")) | "\(.key): \(.value)"'
  ```

#### The Activator → ConfigAdmin → Component Chain (Per-Model Wiring)

Many JUDO "missing component" failures are wiring failures along a 3-tier chain JUDO uses to instantiate platform services *per model*. Understanding the chain is the difference between a 30-second diagnosis and an hour of grepping.

**Tier 1 — Model deployers publish model services and fire events.**

- Bundles: `judo-services-karaf-model-deployer`, `judo-services-model-bundle-deployer`, `judo-services-application-index`.
- Discover `*-internal` model bundles, register `EsmModel` / `PsmModel` / `AsmModel` OSGi services with property `name=<modelName>`, post `EventAdmin` event on topic `hu/blackbelt/judo/Event/MODEL_CHANGED` with `eventType=DEPLOY|UNDEPLOY`, `modelName=<modelName>`.

**Tier 2 — Per-area `*Activator` components react to those events and spawn factory configs via `ConfigurationAdmin`.**

Canonical examples in `judo-platform-services/`:

| Activator | Spawns factory configs for |
|---|---|
| `HealthCheckActivator` | `ModelsCheck`, `PlatformComponentsCheck`, `OperationsCheck`, `JaxRsApplicationListener`, `ApplicationListener`, `StatusTracker` |
| `CxfActivator` | per-model CXF bus / JAX-RS server configs |
| `DispatcherServiceActivator` | per-model dispatcher PIDs |
| `KeycloakSecurityActivator`, `CxfSecurityActivator` | per-model security wiring |
| `RdbmsDaoActivator`, `SingleDatasourceRdbmsDaoActivator` | per-model DAO / datasource configs |

Shape of every activator:

```java
@Component(immediate = true,
           configurationPolicy = ConfigurationPolicy.REQUIRE,
           property = EventConstants.EVENT_TOPIC + "=" + MODEL_CHANGED_EVENT)
public class XxxActivator implements EventHandler {
    @Reference ConfigurationAdmin configAdmin;

    void registerFor(String modelName) {
        configAdmin.createFactoryConfiguration(targetPid, "?")
            .update(props(
                "modelName", modelName,
                "hc.tags",   modelName,
                "asmModel.target", "(" + DEFAULT_SOURCE_NAME_PROPERTY_KEY + "=" + modelName + ")",
                CREATED_BY,  this.getClass().getName()));   // marker for cleanup
    }
}
```

Key conventions:

- **Marker prop** `.__createdBy = <ActivatorFQN>` on every spawned config → used on UNDEPLOY to filter and delete only this activator's configs.
- **`.target` filters** wire each spawned component to the right per-model service: `asmModel.target=(name=<model>)`, `openIdConfigurationProvider.target=(judo.model.name=<model>)`, etc. See `hu.blackbelt.judo.services.core.osgi.TrackerBasedComponentActivator` for the `DEFAULT_SOURCE_NAME_PROPERTY_KEY` (`name`) / `DEFAULT_TARGET_NAME_PROPERTY_KEY` (`judo.model.name`) constants.
- **Activator itself has `configurationPolicy=REQUIRE`** → needs its own root config in `etc/<activator-pid>.cfg`. If that file is missing/empty, the activator never starts and *none* of its downstream factory configs get created.

**Tier 3 — Target components activate per spawned factory config; some programmatically register marker services.**

Example: `JaxRsApplicationListener` is `@Component(configurationPolicy=REQUIRE)`. Once its per-model factory config exists and `AsmModel` is bound, `@Activate` opens a `ServiceTracker` for JAX-RS `Application` services filtered by `(judo.model.name=<model>)`. When all actor-type applications are tracked, it calls:

```java
context.registerService(JaxRsApplicationsReady.class, new JaxRsApplicationsReady() {}, props);
```

**Critical:** `JaxRsApplicationsReady` is *only* a service registration — not an `@Component`. It will never appear in `/system/console/components`. The only places to verify it are `/system/console/services` or via OSGi `BundleContext.getServiceReferences(...)`.

Other marker services that follow this same "register programmatically when ready" pattern: `*Ready` services published by `TrackerBasedComponentActivator` subclasses across `judo-services-dispatcher-osgi`, `judo-services-dao-rdbms-osgi`, `judo-services-security-osgi`.

#### Trace-Back Checklist

When a per-model health check reports `Missing platform components: [X]`:

1. **Is `X` an SCR component or a programmatically-registered service?**
   - `curl -s -u karaf:karaf .../components.json | jq -r '.data[].name' | grep X` — if absent, NOT an SCR component.
   - Then check services: `curl -s -u karaf:karaf .../services.json | jq -r '.data[].types[]' | grep X`.

2. **Find the publisher** that programmatically registers `X` — in `judo-platform-services/`:
   ```bash
   grep -rn "registerService(X.class\|registerService(.*X\.class" --include="*.java"
   ```

3. **Check the publisher component's SCR state**:
   - `no config` → Tier-2 activator did not create the factory config. Go to step 4.
   - `unsatisfied (reference)` → a `.target` filter does not match. Read the component JSON's `Reference …` lines.
   - `active` but `X` still not registered → publisher's `ServiceTracker` is waiting on a runtime condition. Check `/system/console/services` for the tracked type.

4. **Find the activator** that creates the publisher's factory config:
   ```bash
   grep -rn "<PublisherClass>\.class" --include="*.java" judo-platform-services/
   ```

5. **Check the activator's SCR state and root config**:
   - `no config` → root cause: `etc/<activator-pid>.cfg` missing or empty in the Karaf assembly.
   - `unsatisfied (reference)` → `@Reference ConfigurationAdmin` or model reference not bound.
   - `active` → inspect spawned factory configs: `curl -s -u karaf:karaf .../configMgr.json | jq -r '.pids[] | select(.fpid=="<publisher-pid>")'`. If absent, the `MODEL_CHANGED` event never reached the activator.

6. **Verify Tier 1**: are `judo-services-karaf-model-deployer` and `judo-services-model-bundle-deployer` bundles `Active`? Is the `<app>-internal` bundle active? Without these, no model services exist and no `MODEL_CHANGED` events are posted.

**Endpoints used in the checklist:**

| Endpoint | Purpose |
|---|---|
| `/system/console/healthcheck?tags=*&overrideGlobalTimeout=` | Per-check failure log |
| `/system/console/components(.json)` | SCR component states, unsatisfied references |
| `/system/console/services(.json)` | Programmatically registered services (e.g. `*Ready` markers) |
| `/system/console/configMgr(.json)` | Existing PIDs and factory configs |
| `/system/console/bundles(.json)` | Bundle states (Active vs. Installed/Resolved) |
| `/system/console/events` | Recent EventAdmin events incl. `MODEL_CHANGED` |

All endpoints share the same HTTP Basic auth (`karaf` / `karaf`).

#### One-shot Dump: Configuration Status

For offline analysis, bug reports, or LLM-assisted diagnosis, grab the entire runtime state in a single file via the Felix Web Console **Configuration Status** page (`/system/console/config`). It aggregates every registered `ConfigurationPrinter` — bundles, services, DS components, ConfigAdmin PIDs, framework properties, threads, memory, system properties, and any health-check or platform-specific printers.

**Download endpoints** (the filename segment is a placeholder — the server only inspects the extension):

| Format | URL |
|---|---|
| Full text | `http://localhost:8181/system/console/config/configuration-status-<any>.txt` |
| Full ZIP (one file per tab) | `http://localhost:8181/system/console/config/configuration-status-<any>.zip` |
| Single tab text (`<tab>` = printer label, lowercased / URL-safe) | `http://localhost:8181/system/console/config/<tab>.nfo` |

Examples:

```bash
# Full text snapshot for archival / diff
curl -u karaf:karaf -o judo-status.txt \
  "http://localhost:8181/system/console/config/configuration-status-$(date +%Y%m%d-%H%M%S).txt"

# Zip (each tab as a separate file inside)
curl -u karaf:karaf -o judo-status.zip \
  "http://localhost:8181/system/console/config/configuration-status-$(date +%Y%m%d-%H%M%S).zip"

# Just the DS Components or Configurations tab
curl -u karaf:karaf "http://localhost:8181/system/console/config/Components.nfo"
curl -u karaf:karaf "http://localhost:8181/system/console/config/Configurations.nfo"
```

When to prefer the dump over the JSON endpoints:

- **Reproducing an issue**: capture once, share or attach to a ticket; everyone sees the same state.
- **Trace-back over time**: take a `.txt` snapshot before and after a deploy/undeploy; `diff` them to see exactly which configs / services / components changed.
- **LLM analysis**: paste relevant tab sections directly into an agent prompt instead of stitching together multiple `curl | jq` outputs.
- **Offline triage**: production systems where you can pull a snapshot once but can't interactively poke the console.

For live drill-down (single component, current state), keep using the `*.json` endpoints from the table above.

---

## Performance Monitoring

JUDO uses **Apache Karaf Decanter** to collect and store application metrics, which can be visualized with **Grafana**.

### Pattern: Measuring Code Performance
You can measure the execution time of specific blocks of your custom code to identify performance bottlenecks.

1.  Inject the `hu.blackbelt.judo.services.core.MetricsCollector` OSGi component.
2.  Use a `try-with-resources` block around the code you want to measure.

    ```java
    @Reference
    private MetricsCollector metricsCollector;

    public void myMeasuredMethod() {
        try (MetricsCollector.MetricsCancelToken token = metricsCollector.start("my-custom-timer")) {
            // ... code to be measured ...
        } // The timer stops automatically when the try block exits.
    }
    ```
*   **Built-in Timers**: The JUDO platform already measures key phases of every request, including: `dispatcher`, `call-script`, `call-sdk`, `dao-query`, and `dao-change`.

---

## Troubleshooting

### "Service not registered"
- **Cause**: Your custom OSGi component did not start correctly.
- **Solution**:
    - Check for `@Component` and that it implements a `@Service` interface.
    - Verify the bundle is `ACTIVE` in the Karaf console: `bundle:list | grep webshop-app`
    - Check the Karaf logs (`log:tail`) for OSGi errors related to your bundle.

### "ClassNotFoundException"
- **Cause**: A required class is not available to your bundle's classloader.
- **Solution**:
    - Ensure the dependency is correctly defined in your `pom.xml`.
    - Check the OSGi `Import-Package` statement in your bundle's `MANIFEST.MF`.
    - Rebuild the entire project to ensure all dependencies are correctly packaged: `mvn clean install`.

### Changes not applied after Hot Deployment
- **Cause**: Karaf did not correctly pick up the changes to your bundle.
- **Solution**:
    - Confirm the bundle's timestamp was updated in the Karaf console: `bundle:list -t 0 | grep webshop-app`
    - Check the JAR timestamp in your local Maven repository (`~/.m2/repository/...`).
    - If needed, force a refresh or restart the bundle manually in the Karaf console: `bundle:refresh [id]` or `bundle:restart [id]`.

---

## See Also
- [Testing Guide](testing-guide.md) - For how to write unit and integration tests.
- [Custom Operations](custom-operations.md) - For the business logic you may be debugging.
- [Patterns and Best Practices](patterns-and-best-practices.md) - For other common backend patterns.