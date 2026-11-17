# production.md — index

Pull-only condensed map. Source: catalog/agent-docs/deployment/production.md.

## Key Concepts
- Production build: optimised, debug info removed.
- Docker deployment: application and dependencies packaged in a container.
- Karaf console: CLI of the running Karaf server (bundles, logs, config at runtime).

## Production Build
- `./judo.sh build -d` (`--docker`) builds Docker images. Without `-d`, judo.sh passes `-DskipDocker -DskipSchemaDocker`.
- `judo.sh` has no `-D` pass-through: `-DskipDocker=false` does not enable Docker (the docker profile activates on `!skipDocker`; defining the property disables it). Extra Maven args: `-ma "<arg>"`.
- Direct Maven: `mvn clean install` (Docker profiles active while `skipDocker` is undefined). Non-Docker: `mvn clean install -DskipDocker`.
- Verification: `mvn clean test`, `mvn clean install`, and `mvn dependency:tree | grep SNAPSHOT` (must return nothing).

## Docker Deployment
- Image details (jib, base image, tags, agents, ports): see `build-process.md#docker-image-build`.
- Docker context: `/application/docker/target/docker/`. Image tag from `DOCKER_IMAGE_TAGS` (default `dev`).
- Image contents: Karaf standalone distribution, OSGi bundles, configuration files, runtime dependencies.
- `docker run` with `-p 8181:8181` and `JUDO_PLATFORM_RDBMS_*` (dialect, host, port, database, user, password), `JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL`, `JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET` (stable base64 secret).
- Compose: `./judo.sh env compose-dev build start` with `compose-dev.properties` (`runtime=compose`, `compose_env=compose-develop`). Orchestrates app, PostgreSQL and Keycloak.
- Profiles under `application/docker/`:
  - `compose-develop`: Traefik, Keycloak in `start-dev` mode, app on `*.traefik.me` over plain HTTP; `JUDO_PLATFORM_FILESTORE=rdbms`.
  - `compose-postgresql-https`: TLS on 80/443; Keycloak and app on PostgreSQL; filesystem filestore (`JUDO_PLATFORM_FILESTORE_DIRECTORY=/filestore`; only `postgres` mounts that volume, see the known issue in the main doc); helper container downloads the traefik.me certificate.
- `compose-postgresql-https` declares network and volumes as external: create them before `docker compose up`. Select with the `compose_env` start option.
- Persisting state: seeded-once data (e.g. `pi-analyzer` seed skips when its auth file exists, so a changed `RI_AUTH_JSON` is ignored) needs a named volume. Container-layer state is lost on replace.

## Environment Configuration
- Maven: `~/.m2/settings.xml` `<server>` entry for the distribution repository.
- `JUDO_PLATFORM_*` variables: database (`JUDO_PLATFORM_RDBMS_DIALECT`, `_DB_HOST`, `_DB_PORT`, `_DB_DATABASE`, `_DB_USER`, `_DB_PASSWORD`), Keycloak (`JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL`, `JUDO_PLATFORM_KEYCLOAK_AUTH_PUBLIC_URL`). Full list in `application-config.md`.
- Frontend: `VITE_API_DEFAULT_BASE_URL`, `VITE_API_RELATIVE_PATH` (`/api`), `VITE_FILE_DEFAULT_BASE_URL`.
- Karaf config in `application/karaf-offline/target/assembly/etc/`:
  - `org.ops4j.datasource-<app>.cfg` (passwords may be `ENC(...)`, see Jasypt in `application-config.md`).
  - `org.ops4j.pax.web.cfg` (web server).
  - `judo-runtime.cfg` (runtime).

## Monitoring and Debugging
- Logs: `application/.karaf/data/log/karaf.log` locally; `docker logs <app>-app` in Docker. Filter with `grep ERROR`.
- Karaf console: `ssh -p 8101 karaf@localhost` (Apache Karaf defaults `karaf:karaf`, change outside local development); Docker: `docker exec -it <app>-app /opt/karaf/bin/client`.
- Commands: `bundle:list`, `bundle:list | grep -i fail`, `service:list`, `shell:jvm` (memory), `thread:list`, `bundle:diag > diagnostics.txt`.
- Health: `/system/health` (there is no `/health` route). `?tags=<app>&format=json` or `format=txt` for overall status.
- Database check: `jdbc:datasources` in the Karaf console.

## Troubleshooting
- Deployment: "Could not resolve dependencies" (check `~/.m2/settings.xml`, credentials, network); "Database connection failed" (check DB, credentials, `psql` test); "Port already in use" (`lsof -i :8181`, `lsof -i :8080`, `docker ps -a`).
- Runtime: "Bundle not starting" (`bundle:diag [bundle-id]`, `log:tail`, `bundle:list`); "Out of memory" (JVM memory in the Karaf startup script, `shell:jvm`).

## Best Practices
- Pre-deployment checklist: tests pass, no snapshot dependencies, clean build, Docker image built, profiles active; env vars and DB credentials set; Keycloak realm configured; TLS certificates in place; integration and performance tests and security scan done.
- Deployment process: back up the current image tag, build with `mvn clean install`, test in staging, deploy (`docker-compose down` then `up -d`), verify logs, bundles and endpoints.
- Security: no credentials in version control; HTTPS; firewall; patch dependencies.
- Performance: connection pooling, query tuning, JVM heap and GC, remove unused Karaf bundles, start levels, thread pools.
- Backup: `pg_dump` of the database, Karaf config directory, env var definitions, deployment scripts; document and test rollback.
- Health and runtime details: see `README.md#health-check-endpoint` and `osgi-runtime-services.md#health-check-endpoint-details`.
- Provisioning: keep prod, test and demo distinct; init-time admin variables via startup template (see `application-config.md`). Signed identifiers need a stable `JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET` on every node.

## Related Documentation
- Build Process (`build-process.md`), Local Development (`local-development.md`), Deployment Overview (`README.md`).
