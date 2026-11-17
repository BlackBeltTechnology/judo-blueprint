# local-development.md — index

Pull-only condensed map. Source: catalog/agent-docs/deployment/local-development.md.

## Table of Contents
- Navigation list; section headings below mirror source order.

## Key Concepts
- Hot deployment: apply backend code changes to a running server without full restart.
- Karaf console: CLI for bundles, logs, config at runtime.
- Incremental builds: build only changed modules.

## Development Server Setup
- Start: `./judo.sh start`; stop: `./judo.sh stop`; status: `./judo.sh status`.
- Starts: PostgreSQL (Docker, 5432) only when `dbtype=postgresql`; generated `judo.properties` sets `dbtype=hsqldb` (embedded HSQLDB). Keycloak (Docker, 8080). Karaf (HTTP 8181; override `-o karaf_port=<port>`).
- Needs Docker daemon (`docker info` first). Karaf runs in background (console output `application/.karaf/console.out`); command returns before app is ready: wait for HTTP 200 before tests. Connection refused usually = stack not up.
- Java 21 required (`java.version` 21). No `run-offline-postgresql.sh`; use `./judo.sh start -o dbtype=postgresql`.
- Access: app `http://localhost:8181/<model>/<Actor>/` (per-actor context path; `/apps/` lists bundles only); Keycloak admin `http://localhost:8080/auth` (`--http-relative-path /auth`; with `keycloak_port=<port>` base is `http://localhost:<port>/auth`); Karaf SSH `ssh -p 8101 karaf@localhost` (password `karaf`, Apache defaults).
- Start options: `-o "runtime=karaf|compose,dbtype=hsqldb|postgresql,compose_env=...,karaf_port=...,postgres_port=...,keycloak_port=..."`; `-K` skips Keycloak; `-w` disables bundle watching (`-W` is not parsed).
- First login: fresh app has no user. Create user in Keycloak (realm `<app>`) and ensure matching actor instance, or let backend create it on first login (Keycloak JIT provisioning).
- Local email: Mailpit at `localhost:1025` (no auth/TLS) set in `judo-karaf.env`.

### Starting Services / Stopping Services / Checking Status
- Commands as above (`start`, `stop`, `status`).

## Hot Deployment
- Flow: `mvn install` in module → JAR to `~/.m2/repository/` → Karaf watches → bundle updated → services re-registered.
- Hot-deployable: custom operations (`application/app/`), interceptors (`application/interceptors/`), frontend JAR (`application/frontend-react/`), REST endpoints (bundle update).
- Requires restart: model changes (schema evolution), configuration changes, feature definition changes.
- Example: start Karaf, edit `application/app/`, `mvn install`, watch `karaf.log` for bundle update and service registration, test without restart.

## Development Workflow
- Rapid iteration: start once, use `./judo.sh reckless`, rebuild modules with `mvn install`; changes auto-deploy.
- Incremental: `mvn install` in `application/app` (backend), `application/frontend-react/<app>__[actor_fqn]` (frontend), or `mvn install -pl application/app,application/interceptors` (multiple).

## Monitoring and Debugging
### Karaf Console
- Connect: `./application/.karaf/bin/client` or `ssh -p 8101 karaf@localhost`.
- Commands: `bundle:list | grep <app>`, `bundle:info <app>-app`, `service:list`, `log:tail`, `bundle:restart <app>-app`, `config:list`.
### Logs
- Karaf log `application/.karaf/data/log/karaf.log`; Docker `docker logs <app>-app`.
- Tail; filter with `grep ERROR` or `grep "Bundle"`.

## IDE Launch Configurations
- Eclipse m2e launchers in generated `launcher` folder: `BuildApplication`, `BuildApplicationWithoutFrontend`, `CompileCustomApp`, `RunApplication`, `RunFrontend`. Details in Build Process.

## Local Database Choice and Tests
- Default `dbtype=hsqldb` (generated `judo.properties`). `-o dbtype=postgresql` (or in `judo.properties`) runs PostgreSQL in Docker.

## Troubleshooting
### Runtime Issues
- Port 8181 or 8080 in use: `lsof -i :<port>`; stop conflicting service or `-o karaf_port=<port>`.
- Database connection failed: check PostgreSQL container (`docker ps | grep postgres`), restart it.
- Keycloak auth failed: check Keycloak container and env vars.
- Bundle not starting: `bundle:diag`, `bundle:info`, `log:tail`.
- `Unable to access jarfile` for `target/judo-cli.jar`: only `generate-root` produces it (plain `mvn install` does not); run `./judo.sh generate-root` after clean, prune or fresh checkout.
### Hot Deployment Issues
- Changes not applied: `bundle:list -t 0`, check JAR timestamp in `~/.m2`, `bundle:update [id]`.
- Service not registered: `bundle:list | grep <app>`, `bundle:restart [id]`, `log:tail`.

## Best Practices
### Development Workflow
- Keep Karaf running (hot deploy); tail logs in a separate terminal; incremental builds; reckless mode for iteration; full clean build before commits.
### Performance Tips
- `mvn install -T 4 -pl application/app,application/interceptors` for parallel builds.
- `mvn install -DskipDocker -DskipFrontendReact` to skip profiles.
- Keep Maven repository cache; avoid frequent cleans.
### Environment Variables
- Frontend env: `VITE_API_DEFAULT_BASE_URL=http://localhost:8181`, `VITE_KEYCLOAK_URL=http://localhost:8080/auth`, `VITE_KEYCLOAK_REALM=<app>`.

## Related Documentation
- Build Process, Production Deployment, Deployment Overview.
