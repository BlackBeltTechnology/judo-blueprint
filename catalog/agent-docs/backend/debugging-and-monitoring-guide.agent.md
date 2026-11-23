# debugging-and-monitoring-guide.md — index

Pull-only condensed map. Source: catalog/agent-docs/backend/debugging-and-monitoring-guide.md.

## Overview
- Tools for debugging, monitoring and profiling a running JUDO application, from dev loop to production triage.

## Hot Deployment Workflow (Development)
- Start with `./judo.sh start`; build only the changed module (`mvn install` in its directory); the running server redeploys the changed JAR.
- Confirm in `application/.karaf/data/log/karaf.log`: expect `Bundle updated: <app>-app`.

## Logging
- SLF4J facade over Log4j 2. Use Lombok `@Slf4j` in custom components.
- MDC attributes: `RequestExchangeId`, `operation` (operation FQN), `user` (OAuth 2.0 token user).
- `ExchangeIdDecorator` (incoming, `Phase.RECEIVE`) sets the exchange id and MDC `RequestExchangeId`.
- `RequestExchangeId` is never removed from the MDC, so pooled threads can log an earlier request's id. Correlate with the `X-Exchange-Id` header.
- `ExchangeIdResponseWriter` (outgoing, `Phase.POST_LOGICAL`) echoes it as the `X-Exchange-Id` response header (only when the decorator set an id), including on error responses.
- Dispatcher log messages that exist: `Operation {} completed in {} ms` (`DefaultDispatcher`) and `Unable to rollback transaction` (`TransactionalOperationCall`). Do not search for "Dispatching operation" or "Resolved actor": they are not logged.
- To log operation names, add an interceptor that logs `AsmUtils.getOperationFQName(operation)`.
- Runtime log levels: `application/.karaf/bin/client`, then `log:set DEBUG <package>`; reset with `log:set DEFAULT <package>`. Example package: `hu.blackbelt.judo.services.dao`.

## Remote Debugging
- Set `KARAF_DEBUG=true` and optionally `JAVA_DEBUG_PORT=*:5005`, then `./judo.sh start`. The JVM starts suspended.
- IDE: Remote JVM Debug configuration, host `localhost`, port `5005`.

## Monitoring and Health Checks
- JMX: `JConsole` or `VisualVM`; MBean `hu.blackbelt.judo:type=<ModelName>,name=Application`; attribute `Started` (boolean).
- Health: `http://localhost:8181/system/health?tags=<ModelName>`. `200 OK` means models, operations and platform components (Dispatcher, REST endpoints, persistence) are deployed.
- Felix Web Console health: `/system/console/healthcheck?tags=*&overrideGlobalTimeout=` (HTTP Basic `karaf` / `karaf`). Empty `overrideGlobalTimeout=` disables the timeout; a number sets it in ms. Shows `HEALTH_CHECK_TIMED_OUT` when the timeout hits.
- SCR components: `/system/console/components(.json)`. Drill down with `components/<component.name>.json`; `Reference …` lines show what is unsatisfied.
- Component states: `active` (healthy); `satisfied` (lazy or factory, usually fine); `no config` (check `etc/<pid>.cfg` and `/system/console/configMgr`); `unsatisfied (reference)` (find the missing provider); `failed activation` (check the log); absent (check `/system/console/bundles`, state `Installed` or `Resolved`).
- Worked example: `TEMPORARILY_UNAVAILABLE` with missing `JaxRsApplicationsReady`. Empty jq result means not registered; check the bundle; `unsatisfied (reference)` means read the Reference lines.
- Chain across three tiers per model:
  - Tier 1: `judo-services-karaf-model-deployer`, `judo-services-model-bundle-deployer`, `judo-services-application-index` publish `EsmModel` / `PsmModel` / `AsmModel` services and post `MODEL_CHANGED` events (`eventType=DEPLOY|UNDEPLOY`, `modelName`).
  - Tier 2: `*Activator` components (e.g. `HealthCheckActivator`, `CxfActivator`, `DispatcherServiceActivator`, `KeycloakSecurityActivator`, `RdbmsDaoActivator`) create factory configs via `ConfigurationAdmin`.
  - Tier 3: target components activate per factory config. Programmatic markers such as `JaxRsApplicationsReady` are service registrations, not `@Component`s; check `/system/console/services`.
- Activator conventions: `configurationPolicy=REQUIRE`, so the activator needs its root config `etc/<activator-pid>.cfg`; without it, no downstream config is created. Spawned configs carry the `.__createdBy` marker, used on UNDEPLOY cleanup. `.target` filters (`asmModel.target`, `openIdConfigurationProvider.target`) wire per-model services.
- Trace-back checklist: check SCR or service for `X`; find the publisher with `grep -rn "registerService(X.class"`; check its state (`no config` → activator did not create config; `unsatisfied` → `.target` mismatch; `active` but unregistered → tracker waiting); find the activator; verify Tier 1 bundles are Active.
- Endpoints: `healthcheck`, `components`, `services`, `configMgr`, `bundles`, `events` (recent `MODEL_CHANGED`).
- Configuration Status dump: `/system/console/config/configuration-status-<any>.txt` (full text), `.zip` (one file per tab), `/system/console/config/<tab>.nfo` (single tab, e.g. `Components.nfo`, `Configurations.nfo`). Use it for bug reports, before-and-after `diff`, LLM analysis, offline triage.

## Performance Monitoring
- Apache Karaf Decanter collects metrics; Grafana visualises them.
- Inject `hu.blackbelt.judo.services.core.MetricsCollector` and wrap the code in `try (MetricsCollector.MetricsCancelToken token = metricsCollector.start("my-custom-timer"))`.
- Built-in timers: `dispatcher`, `call-script`, `call-sdk`, `dao-query`, `dao-change`.

## Troubleshooting
- "Service not registered": check `@Component`, the `@Service` interface, bundle `ACTIVE` (`bundle:list | grep <app>-app`), and `log:tail`.
- "ClassNotFoundException": check `pom.xml` dependency, `Import-Package` in `MANIFEST.MF`, rebuild with `mvn clean install`.
- Changes not applied after hot deployment: check `bundle:list -t 0`, the JAR timestamp in `~/.m2/repository`, then `bundle:refresh [id]` or `bundle:restart [id]`.

## See Also
- Testing Guide (`testing-guide.md`), Custom Operations (`custom-operations.md`), Patterns and Best Practices (`patterns-and-best-practices.md`).
