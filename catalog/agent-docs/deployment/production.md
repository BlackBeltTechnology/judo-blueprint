---
title: Production Deployment
description: Production builds, Docker and Compose deployment, environment configuration, monitoring and deployment checklist.
aliases: [deploy to production, production docker image, docker compose deployment, production environment variables, production health check, deployment checklist]
keywords: [skipDocker, JUDO_PLATFORM_RDBMS_DIALECT, JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL, JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET, DOCKER_IMAGE_TAGS, compose-postgresql-https, /system/health, bundle:list, judo-runtime.cfg, VITE_API_DEFAULT_BASE_URL]
tags: [domain:deployment, layer:infrastructure, status:platform]
---

# Production Deployment

This guide covers production deployment, Docker deployment, environment configuration, and production best practices for the <app> project.

## Table of Contents

- [Production Build](#production-build)
- [Docker Deployment](#docker-deployment)
- [Environment Configuration](#environment-configuration)
- [Monitoring and Debugging](#monitoring-and-debugging)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Key Concepts

- **Production Build**: A build that is optimized for performance and security, with debugging information removed.
- **Docker Deployment**: The process of packaging the application and its dependencies into a Docker container for easy deployment and scaling.
- **Karaf Console**: A command-line interface for the running Karaf server. It allows you to manage bundles, view logs, and change configurations at runtime.

## Production Build

### Full Production Build

Build everything including the Docker images (`-d` / `--docker`):

```bash
./judo.sh build -d
```

Without `-d`, `judo.sh build` skips Docker (it passes `-DskipDocker -DskipSchemaDocker`). `judo.sh` has no `-D` pass-through; `-DskipDocker=false` does **not** enable Docker, because the docker profile activates on `!skipDocker` (the property being defined at all disables it). Use `-ma "<arg>"` for extra Maven arguments.

Or with Maven directly (Docker profiles active as long as no `skipDocker` property is defined):

```bash
mvn clean install
```

### Build Without Docker

If you're deploying to a non-Docker environment:

```bash
mvn clean install -DskipDocker
```

### Build Verification

Before deploying to production, verify:

1. **All tests pass:**
   ```bash
   mvn clean test
   ```

2. **Full clean build succeeds:**
   ```bash
   mvn clean install
   ```

3. **No snapshot dependencies:**
   ```bash
   mvn dependency:tree | grep SNAPSHOT
   # Should return nothing
   ```

## Docker Deployment

### Building Docker Image

The build process creates Docker image tars when Docker building is requested:

```bash
./judo.sh build -d
```

Image details (jib, base image, tags, agents, ports) are in [Build Process](./build-process.md#docker-image-build).

#### Output
- Docker context: `/application/docker/target/docker/`
- Docker image: Tagged with project version

### Docker Image Contents

The Docker image includes:
- Karaf standalone distribution
- All OSGi bundles
- Configuration files
- Runtime dependencies

### Running Docker Container

#### Basic deployment
```bash
docker run -d \
  --name <app>-app \
  -p 8181:8181 \
  -e JUDO_PLATFORM_RDBMS_DIALECT=postgresql \
  -e JUDO_PLATFORM_RDBMS_DB_HOST=postgres \
  -e JUDO_PLATFORM_RDBMS_DB_PORT=5432 \
  -e JUDO_PLATFORM_RDBMS_DB_DATABASE=<app> \
  -e JUDO_PLATFORM_RDBMS_DB_USER=<app> \
  -e JUDO_PLATFORM_RDBMS_DB_PASSWORD=yourpassword \
  -e JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL=http://auth:8080 \
  -e JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET=<stable base64 secret> \
  <image>:<tag>
```

The image tag comes from `DOCKER_IMAGE_TAGS` (default `dev`). All variables are described in [Application Configuration](./application-config.md).

### Docker Compose

For a complete stack including database and Keycloak:

```bash
./judo.sh env compose-dev build start
```

where `compose-dev.properties` contains `runtime=compose` and `compose_env=compose-develop`. This orchestrates the application, PostgreSQL and Keycloak containers.

### Shipped Docker Compose Environments

The project template ships two Compose profiles under `application/docker/`:

| Profile | Description |
|---------|-------------|
| `compose-develop` | Traefik + Keycloak in `start-dev` mode + the app, on `*.traefik.me` over plain HTTP (`proxy.traefik.me`, `auth.traefik.me:8080`, `app.traefik.me:8181`); `JUDO_PLATFORM_FILESTORE=rdbms` |
| `compose-postgresql-https` | Production-like: TLS on 80/443, Keycloak on PostgreSQL, the app on PostgreSQL with a filesystem filestore (`JUDO_PLATFORM_FILESTORE_DIRECTORY=/filestore`), a helper container that downloads the traefik.me certificate |

`compose-postgresql-https` declares its network and volumes as **external**: create them before `docker compose up`. Select a profile with the `compose_env` start option.

**Known issue:** in `compose-postgresql-https` only the `postgres` service mounts the filestore volume (at `/filestore`). The `app` service sets `JUDO_PLATFORM_FILESTORE_DIRECTORY=/filestore` but has no volume for it, so files it writes are not stored in that volume.

**Known issue:** the `app` router in `compose-postgresql-https` gets the auth service certificate domains (`auth.traefik.me`, `auth-*.traefik.me`), not the app hostname (`app.traefik.me`), so the app certificate does not match the app hostname. Open the app through the hostname the certificate covers, or use `compose-develop` (plain HTTP) for local work.

### Persisting container state

If a container seeds credentials or data only once on first start (for example the AI analyzer plugin `pi-analyzer`, whose seed script skips when its auth file already exists, so a changed `RI_AUTH_JSON` is ignored afterwards), rotating the value requires deleting the seeded file (for example `docker compose rm -sf <service>` and recreating it). Mount such state on a **named volume**; otherwise it lives in the container layer and is lost on replace, and a persisted volume means the data lives on the host's boot disk.

## Environment Configuration

### Maven Configuration

**Distribution Repository** (`~/.m2/settings.xml`):

```xml
<settings>
  <servers>
    <server>
      <id>[private-maven-repo]</id>
      <username>YOUR_USERNAME</username>
      <password>YOUR_PASSWORD</password>
    </server>
  </servers>
</settings>
```

### Environment Variables

#### Application Configuration

The platform reads `JUDO_PLATFORM_*` variables (full list in [Application Configuration](./application-config.md)):

```bash
# Database
JUDO_PLATFORM_RDBMS_DIALECT=postgresql
JUDO_PLATFORM_RDBMS_DB_HOST=localhost
JUDO_PLATFORM_RDBMS_DB_PORT=5432
JUDO_PLATFORM_RDBMS_DB_DATABASE=<app>
JUDO_PLATFORM_RDBMS_DB_USER=<app>
JUDO_PLATFORM_RDBMS_DB_PASSWORD=yourpassword

# Keycloak
JUDO_PLATFORM_KEYCLOAK_AUTH_SERVER_URL=http://localhost:8080
JUDO_PLATFORM_KEYCLOAK_AUTH_PUBLIC_URL=http://localhost:8080
```

#### Frontend Configuration

**Frontend** (`.env` or export):

```bash
VITE_API_DEFAULT_BASE_URL=https://api.yourdomain.com
VITE_API_RELATIVE_PATH=/api
VITE_FILE_DEFAULT_BASE_URL=https://api.yourdomain.com
```

### Karaf Configuration

Production Karaf configurations are located in:
- `application/karaf-offline/target/assembly/etc/`

#### Important files
- `org.ops4j.datasource-<app>.cfg` - Database configuration (passwords may be stored as `ENC(...)`, see [Encrypted Values](./application-config.md#encrypted-values-jasypt))
- `org.ops4j.pax.web.cfg` - Web server configuration
- `judo-runtime.cfg` - Application runtime configuration

## Monitoring and Debugging

### Logs

#### Locations
- Karaf: `application/.karaf/data/log/karaf.log`
- Docker: `docker logs <app>-app`

#### Tail logs
```bash
# Local Karaf
tail -f application/.karaf/data/log/karaf.log

# Docker container
docker logs -f <app>-app

# Filter errors
docker logs <app>-app | grep ERROR
```

### Karaf Console

#### Connect to Karaf console

```bash
# Local (8101 / karaf:karaf are Apache Karaf defaults; change them outside local development)
ssh -p 8101 karaf@localhost

# Docker
docker exec -it <app>-app /opt/karaf/bin/client
```

#### Production monitoring commands

```bash
# Check bundle status
bundle:list | grep <app>

# Check for failed bundles
bundle:list | grep -i fail

# View service status
service:list

# Check memory usage
shell:jvm

# View active threads
thread:list

# Export diagnostics
bundle:diag > diagnostics.txt
```

### Health Checks

#### Verify application health

The health endpoint is `/system/health` (there is no `/health` route). Use the model name as tag:

```bash
curl "http://localhost:8181/system/health?tags=<app>&format=json"
curl -s "http://localhost:8181/system/health?tags=<app>&format=txt"   # overall status only

# Check bundle status via SSH
ssh -p 8101 karaf@localhost "bundle:list" | grep Active

# Check database connectivity
ssh -p 8101 karaf@localhost "jdbc:datasources"
```

## Troubleshooting

### Deployment Issues

#### "Could not resolve dependencies"

##### Solution
- Check Maven settings: `~/.m2/settings.xml`
- Verify repository credentials
- Check network connectivity to artifact repository

#### "Database connection failed"

##### Solution
- Verify database is running and accessible
- Check database credentials in configuration
- Test connection: `psql -h $JUDO_PLATFORM_RDBMS_DB_HOST -U $JUDO_PLATFORM_RDBMS_DB_USER -d $JUDO_PLATFORM_RDBMS_DB_DATABASE`

#### "Port already in use"

##### Solution
- Check running processes: `lsof -i :8181` (Karaf) / `lsof -i :8080` (Keycloak)
- Stop conflicting service or change port
- For Docker: Check for orphaned containers: `docker ps -a`

### Runtime Issues

#### "Bundle not starting"

##### Solution
- Check dependencies: `bundle:diag [bundle-id]`
- View detailed errors: `log:tail` or check log files
- Verify all required bundles are installed: `bundle:list`

#### "Out of memory"

##### Solution
- Increase JVM memory in Karaf startup script
- Check for memory leaks: `shell:jvm`
- Review and optimize application code

## Best Practices

### Pre-Deployment Checklist

1. **Code Quality**
   - All tests passing
   - No snapshot dependencies
   - Code reviewed and approved

2. **Build Verification**
   - Clean build successful: `mvn clean install`
   - Docker image built successfully
   - All profiles activated

3. **Configuration**
   - Environment variables set correctly
   - Database credentials configured
   - Keycloak realm configured
   - SSL/TLS certificates in place

4. **Testing**
   - Integration tests passed
   - Performance tests completed
   - Security scan performed

### Deployment Process

1. **Backup current version**
   ```bash
   docker tag <app>-manager:latest <app>-manager:backup-$(date +%Y%m%d)
   ```

2. **Build new version**
   ```bash
   mvn clean install
   ```

3. **Test in staging environment**
   - Deploy to staging
   - Run smoke tests
   - Verify functionality

4. **Deploy to production**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

5. **Verify deployment**
   - Check logs for errors
   - Verify all bundles active
   - Test critical endpoints
   - Monitor performance

### Security Considerations

1. **Credentials**
   - Never commit credentials to version control
   - Use environment variables or secrets management
   - Rotate credentials regularly

2. **Network**
   - Use HTTPS in production
   - Configure firewall rules
   - Limit exposed ports

3. **Updates**
   - Keep dependencies updated
   - Monitor security advisories
   - Apply security patches promptly

### Performance Optimization

1. **Database**
   - Configure connection pooling
   - Optimize queries
   - Regular maintenance and vacuum

2. **JVM**
   - Tune heap size appropriately
   - Configure garbage collection
   - Monitor memory usage

3. **Karaf**
   - Remove unused bundles
   - Optimize start levels
   - Configure appropriate thread pools

### Backup and Recovery

1. **Database Backups**
   ```bash
   pg_dump -h $JUDO_PLATFORM_RDBMS_DB_HOST -U $JUDO_PLATFORM_RDBMS_DB_USER $JUDO_PLATFORM_RDBMS_DB_DATABASE > backup-$(date +%Y%m%d).sql
   ```

2. **Configuration Backups**
   - Backup Karaf configuration directory
   - Backup environment variable definitions
   - Version control deployment scripts

3. **Recovery Plan**
   - Document rollback procedure
   - Test recovery process regularly
   - Maintain previous version images

### Health Check and Runtime Details

The `/system/health` endpoint, its formats, status-to-HTTP mapping and custom health checks are described in [Deployment Overview](./README.md#health-check-endpoint) and [OSGi Runtime Services](./osgi-runtime-services.md#health-check-endpoint-details).

### Environment provisioning notes

Keep prod/test/demo environments distinct and wire the init-time admin-user variables through your startup template and infrastructure config, see [Application Configuration](./application-config.md#provisioning-a-new-environment-prod--test--demo). Signed identifiers need a stable `JUDO_PLATFORM_IDENTIFIER_SIGNER_SECRET` on every node.

## Related Documentation

- [Build Process](./build-process.md) - Detailed build system documentation
- [Local Development](./local-development.md) - Development environment setup
- [Deployment Overview](./README.md) - Main deployment documentation
