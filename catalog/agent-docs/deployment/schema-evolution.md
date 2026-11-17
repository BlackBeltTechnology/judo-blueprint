---
title: Database Schema Evolution
description: Incremental schema migration with judo-rdbms-schema: generate, review scripts, execute, Docker migration, rollback and production strategy.
aliases: [database migration, schema migration, liquibase migration, migrate database, rollback migration, docker schema migration]
keywords: [judo-rdbms-schema, Liquibase, judo.properties, app_name, migration, Docker, rollback]
tags: [domain:deployment, layer:infrastructure, status:platform]
---

# Database Schema Evolution Guide

## Overview

The `application/schema` module provides database schema migration capabilities for <app>. It uses Liquibase under the hood to perform incremental schema updates when the model evolves.

**Note**: Throughout this document, `<app>` refers to the application name from `judo.properties` (app_name property).

## Table of Contents

- [Quick Start Workflow](#quick-start-workflow)
- [Key Concepts](#key-concepts)
- [Review Workflow](#review-workflow-for-incremental-migrations)
- [Migration Commands](#migration-commands)
- [Production Migration Strategy](#production-migration-strategy)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

---

## Quick Start Workflow

This section provides a condensed workflow for the most common migration task: generating and applying a schema update in a local development environment.

1.  **Ensure your model changes are built:**
    ```bash
    # From the project root
    cd application/model
    mvn clean install
    ```

2.  **Generate the migration scripts:**
    The `generate` goal takes the base and the updated RDBMS model files (`baseModel`, `updateModel`; each a file path or a `mvn:` URL such as `mvn:<groupId>:<app>-model:<version>!model/<app>-rdbms_postgresql.model`), the `modelName`, the `dbType` and an `outputDirectory`. If no base model is given, the base is read from the `latest.version` / `previous.version` marker files in the output directory.
    ```bash
    # From application/schema/
    mvn judo-rdbms-schema:generate \
      -DmodelName=<app> -DdbType=postgresql \
      -DbaseModel=<base_model_file_or_mvn_url> \
      -DupdateModel=<update_model_file_or_mvn_url>
    ```
    The `execute` goal takes `baseModelVersion` and `updateModelVersion` (see below).

3.  **Apply the migration to your local database:**
    ```bash
    # From application/schema/
    mvn judo-rdbms-schema:execute \
      -DbaseModelVersion=<base_version> \
      -DupdateModelVersion=<update_version> \
      -DjdbcUrl=jdbc:postgresql://localhost:5432/<app> \
      -DdbUser=<app> \
      -DdbPassword=[password]
    ```

4.  **Start the application** to verify the changes:
    ```bash
    # From the project root
    ./judo.sh start
    ```

## Key Concepts

### What is Schema Evolution?

When you modify the ESM model (using Judo Designer), the database schema often needs to change:
- Adding/removing entities → Adding/removing tables
- Adding/removing attributes → Adding/removing columns
- Changing types → Altering column types
- Modifying relationships → Changing foreign keys

Schema evolution manages these database changes safely and incrementally.

### When No Manual Step Is Needed

Adding a **stored** member (for example a new attribute) to an entity needs **no** manual migration or `schema-upgrade` run for a fresh database (empty or newly created, so Liquibase creates everything): the generated Liquibase changelog (`application/model/target/generated-resources/model/<app>-liquibase_postgresql.changelog.xml`) already contains the new column. **An existing database is not migrated automatically:** if the model changed since the data was created, startup fails with `There are RDBMS model changes which have not been applied to database`, so a persistent development database (for example a kept PostgreSQL volume) needs the migration too. Run it, or discard the database and volume. Never skip the version check (`ignoreVersionCheck`) to get past this. A manual schema-upgrade step is relevant for a persistent database that already holds data, and for genuinely non-additive or backward-incompatible changes (renames, type changes, removals). For a local persistent PostgreSQL database `./judo.sh schema-upgrade` generates the difference against the running database and applies it. `judo.sh` takes the schema module path from `schema_dir` (default: the model directory, `model_dir`), so when the schema module is not directly under that directory set `schema_dir=<dir>` in `judo.properties` or the environment, for example `schema_dir=application ./judo.sh schema-upgrade`.

The line `DATABASE HAVE TO BE UPDATED!` that `generate` logs at error level lists pending database operations from the model compatibility check. It is a notice, not a build failure: the build still ends with `BUILD SUCCESS`, and a migration is needed before the new model runs against that database.

**⚠️ IMPORTANT: When Schema Migration is Required**

Schema migration is **ONLY necessary when entity types change** in the model. The JUDO platform generates SQL schema from entity type definitions.

**Schema migration IS required when:**
- ✅ Adding/removing/modifying entity types (mapped entities)
- ✅ Adding/removing attributes on entity types
- ✅ Changing attribute types (String → Integer, etc.)
- ✅ Adding/removing relationships between entities
- ✅ Modifying entity inheritance hierarchy

**Schema migration is NOT required when:**
- ❌ Changing transfer object types (view models, DTOs)
- ❌ Modifying actors or access points
- ❌ Changing UI layouts or forms
- ❌ Adding/removing operations (unless they affect entity structure)
- ❌ Modifying validations or derived attributes (computed fields)

**Why?** The database schema is generated exclusively from **entity types**. Transfer objects, actors, and UI definitions exist only at runtime and do not affect the database structure.

### Schema Migration Module

**Location**: `application/schema/`

**Purpose**: CLI tool and Docker image for database migrations

**Key Features**:
- **Automatic migration script generation** from model versions
- **Incremental migrations** - migrate from any version to any version
- **Manual migration support** - custom SQL when needed
- **Docker image** - containerized migration tool
- **Multiple database support** - PostgreSQL, HSQLDB, etc.

## Module Structure

```
application/schema/
├── pom.xml                          # Schema module build configuration
├── migration/                       # Manual migration scripts directory
│   └── [manual-scripts].sql        # Custom SQL migrations
├── README.adoc                      # Original migration instructions
└── target/
    └── <app>-schema-[version].jar   # Executable JAR
```

## Schema Migration Workflow

### Step 1: Identify Model Versions

When migrating, you need two model versions:
- **Base version** (FROM): Current database schema version
- **Update version** (TO): Target database schema version

**Model versions** are embedded in the generated model artifacts. The generated model POM sets `model-version` to `${project.version}`; build pipelines often use a timestamped form such as `1.1.0.20210929_004050_9602796_develop` (set it with `./judo.sh build -v <version>`).

**Important**: This is the MODEL version (the `Judo-Models` bundle header / `model-version` property), NOT a separate application version.

### Step 2: Generate Migration Scripts

**Automatic generation** compares the base and the updated RDBMS model:

```bash
cd application/schema

mvn judo-rdbms-schema:generate \
  -DmodelName=<app> -DdbType=postgresql \
  -DbaseModel=<base rdbms model file or mvn: url> \
  -DupdateModel=<update rdbms model file or mvn: url> \
  -DoutputDirectory=migration
```

**What gets generated** in `migration/<previous>_to_<latest>/` (dots and dashes of the versions become underscores):
- an aggregated `00_<app>_incremental_<dialect>.changeset.xml` plus eight phase changesets: `check`, `backup`, `beforeIncremental`, `updateDataBeforeIncremental`, `incremental`, `updateDataAfterIncremental`, `aferIncremental` (sic, script `07_aferIncremental`) and `dropBackup`;
- the model `<app>-rdbms_<version>_<dialect>.model`;
- marker files `latest.version` and `previous.version` in the output directory, which drive base/update version resolution for the next run.

Only changesets that contain developer knowledge matter in practice: the data-migration changesets (`updateDataBeforeIncremental`, `updateDataAfterIncremental`) are empty unless you write them.

### Step 3: Manual Migration Scripts (Optional)

Sometimes automatic generation cannot handle complex migrations:
- Data transformations
- Complex logic changes
- Splitting/merging columns
- Custom data fixes

**Write the data-migration changesets** (`updateDataBeforeIncremental` / `updateDataAfterIncremental`) in the generated version folder under `application/schema/migration/`. Entity tables are named `T_ENTITIES_<NAME>` and columns `C_<NAME>` (check the generated changelog for the exact names):

```sql
-- Custom data migration
UPDATE T_ENTITIES_USER
SET C_FULL_NAME = CONCAT(C_FIRST_NAME, ' ', C_LAST_NAME)
WHERE C_FULL_NAME IS NULL;

-- Complex transformation
-- ... your custom SQL
```

## Review Workflow for Incremental Migrations

The schema generator classifies model changes as **identical**, **applyable** (can be done automatically) or **review-required** (for example renames, narrowing type changes, data loss). At application startup the runtime stops with an error when the base model stored in the database differs from the application's base model, so an incremental model must be executed first.

- When a change needs review, generation writes `<name>.sql.missing` placeholder files. Replace them with the real SQL: rename each `.sql.missing` to `.sql` and place it in the review script directory (`reviewScriptDirectory`) before the migration can be applied. Without them `isApplyable()` is false and `execute` / `apply` fail with `IllegalStateException: Missing scripts`.
- Generation overwrites every file in the output folder **except** the review files.
- `useXmiId` (default `true`) lets a rename be detected as a *modify* rather than delete + create. Keep it `true` when entities or attributes are renamed.
- `ignoreReview` defaults to `false` for `generate` and to `true` for the Maven `execute` / `apply` goals; `./update.sh ... --ignoreReview`-style pipelines set it explicitly.
- Several accumulated per-snapshot migration folders (for example `130051 -> 175110` plus hand-written steps) can be consolidated: regenerate one continuous folder from the two model files (oldest base model -> current model), move the hand-written steps into it and delete the intermediate folder, so production goes through one continuous step. An exit with `DATABASE HAVE TO BE UPDATED` during this generate step is part of the normal flow.
- A project can keep many steps (for example 18 steps with changesets `00`..`08`); only the non-empty data-migration changesets carry developer knowledge.

In managed pipelines the same flow is exposed as a script, for example `./update.sh --version <v> --schema generate|execute --ignoreReview`, where the runner snapshots a database backup (such as a Neon backup branch `backup-<ts>`) before `execute` and rollback is `--schema restore --branch backup-<ts>`.

### Step 4: Test Migration

**Always test migrations before production!**

```bash
# 1. Start with old version database
# Checkout old version, build, and run
git checkout v1.1.0
mvn clean install
./judo.sh start

# 2. Stop application (keep database running)
./judo.sh stop

# 3. Backup database
pg_dump -h localhost -U <app> <app> > backup_v1.1.0.sql

# 4. Execute migration
cd application/schema
mvn judo-rdbms-schema:execute \
  -DbaseModelVersion=1.1.0 \
  -DupdateModelVersion=1.2.0 \
  -DjdbcUrl=jdbc:postgresql://localhost:5432/<app> \
  -DdbType=postgresql \
  -DdbUser=<app> \
  -DdbPassword=[password]

# 5. Upgrade application
git checkout v1.2.0
mvn clean install -DskipDocker
./judo.sh start

# 6. Verify application works with migrated schema
```

### Step 5: Rollback (If Migration Fails)

If something goes wrong:

```bash
# 1. Stop database
docker stop <app>-postgres
# or: sudo systemctl stop postgresql

# 2. Remove database content
docker rm <app>-postgres
# or: dropdb <app>

# 3. Start fresh database
docker run -d --name <app>-postgres -e POSTGRES_DB=<app> -e POSTGRES_USER=<app> -e POSTGRES_PASSWORD=[password] -p 5432:5432 postgres:15

# 4. Restore from backup
psql -h localhost -U <app> -d <app> < backup_v1.1.0.sql

# 5. Start application with old version
git checkout v1.1.0
./judo.sh start
```

## Migration Commands

### Maven-Based Migrations

#### Apply Fresh Schema

Create schema from scratch (development):

```bash
cd application/schema

mvn judo-rdbms-schema:apply \
  -DjdbcUrl=jdbc:postgresql://localhost:5432/<app> \
  -DdbType=postgresql \
  -DdbUser=<app> \
  -DdbPassword=[password]
```

**Use case**: Fresh development database, testing. `apply` takes `modelName`, `updateModel`, `reviewScriptDirectory` and `outputDirectory` (default `target/classes/schema`) in addition to the connection parameters.

#### Generate Migration Scripts

Compare two models and generate the changesets:

```bash
mvn judo-rdbms-schema:generate \
  -DmodelName=<app> -DdbType=postgresql \
  -DbaseModel=<base model> -DupdateModel=<update model>

# Output: migration/<previous>_to_<latest>/
```

#### Execute Migration

Run migration from one version to another:

```bash
mvn judo-rdbms-schema:execute \
  -DbaseModelVersion=1.1.0.20210929_004050 \
  -DupdateModelVersion=1.2.0.20211021_085156 \
  -DjdbcUrl=jdbc:postgresql://localhost:5432/<app> \
  -DdbType=postgresql \
  -DdbUser=<app> \
  -DdbPassword=[password]
```

### Docker-Based Migrations

The schema module can be built as a **Docker image** for containerized migrations.

#### Build Docker Image

```bash
cd application/schema

# Build with Docker profile
mvn clean install -Pdocker

# Image created: <app>-schema:[version]  (the image name is the schema module artifactId)
```

#### Run Migration with Docker

```bash
docker run --rm \
  <app>-schema:latest \
  execute \
  --baseModelVersion=1.1.0.20210929_004050_9602796_develop \
  --updateModelVersion=1.2.0.20211021_085156_21efaed_develop \
  --modelName=<app> \
  --incrementalDirectory=/ \
  --jdbcUrl=jdbc:postgresql://host.docker.internal:5432/<app> \
  --dbType=postgresql \
  --dbUser=<app> \
  --dbPassword=[password]
```

**Note**: Use `host.docker.internal` to access host database from container (Docker Desktop), or use actual hostname/IP.

#### Docker Compose Example

```yaml
version: '3.8'

services:
  db-migration:
    image: <app>-schema:${VERSION}
    command:
      - execute
      - --baseModelVersion=${BASE_VERSION}
      - --updateModelVersion=${UPDATE_VERSION}
      - --modelName=<app>
      - --jdbcUrl=jdbc:postgresql://postgres:5432/<app>
      - --dbType=postgresql
      - --dbUser=<app>
      - --dbPassword=${DB_PASSWORD}
    depends_on:
      - postgres
    networks:
      - app-network

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: <app>
      POSTGRES_USER: <app>
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - app-network

networks:
  app-network:

volumes:
  postgres-data:
```

## Production Migration Strategy

### Recommended Approach

1. **Prepare Migration**
   ```bash
   # Generate and review migration scripts
   mvn judo-rdbms-schema:generate \
     -DmodelName=<app> -DdbType=postgresql \
     -DbaseModel=${CURRENT_PROD_RDBMS_MODEL} \
     -DupdateModel=${NEW_RDBMS_MODEL}
   
   # Review generated changesets and any *.sql.missing placeholders
   ls migration/*_to_*/
   ```

2. **Test in Staging**
   ```bash
   # Clone production database to staging
   # Execute migration on staging
   # Test application thoroughly
   ```

3. **Backup Production**
   ```bash
   # Full database backup
   pg_dump -h prod-db -U <app> <app> > prod_backup_$(date +%Y%m%d_%H%M%S).sql
   ```

4. **Maintenance Window**
   ```bash
   # Stop application
   # Execute migration
   # Deploy new application version
   # Verify
   # Start application
   ```

5. **Verify and Monitor**
   - Check application logs
   - Verify data integrity
   - Monitor performance
   - Keep backup for quick rollback

### Blue-Green Deployment Consideration

For zero-downtime deployments:
- Ensure migrations are **backward compatible** when possible
- Use **additive changes** (add columns as nullable, add tables, etc.)
- Deploy application first, then remove deprecated schema elements later
- Consider **feature flags** for database-dependent features

## Configuration

### Model Version Configuration

The generated model module sets the model version from the project version:

```xml
<model-version>${project.version}</model-version>
```

The composite timestamp/commit/branch form (for example `1.2.0.20211021_085156_21efaed_develop`) is not generated; supply it through the build version, for example `./judo.sh build -v <version>`. Override the property with a `pom.xml.model-properties-definition.fragment.hbs` fragment if you need a different scheme.

### Schema Module Properties

In `application/schema/pom.xml`:

```xml
<properties>
    <modelName><app></modelName>
    <incrementalDirectory>${basedir}/migration</incrementalDirectory>
    <updateModelArtifactVersion>${project.version}</updateModelArtifactVersion>
</properties>
```

## Troubleshooting

### Migration Fails with "Unknown version"

**Problem**: Cannot find model version in Maven repository

**Solution**:
```bash
# Ensure model is built and installed
cd application/model
mvn clean install

# Check version matches exactly
mvn dependency:tree | grep <app>-model
```

### Migration Scripts Not Generated

**Problem**: `migration/` directory is empty after generate

**Solution**:
- Check both models are valid and different (`Update model is not defined` means `updateModel` is missing)
- Verify model artifacts exist in local Maven repo (`~/.m2/repository`)
- Check for errors in Maven output

### Application stops at startup with "RDBMS model changes which have not been applied"

**Problem**: The model version stored in the database (`JUDO_MODEL_VERSIONS`) differs from the deployed model. Run the incremental migration first, or restore the database. Do not set `ignoreVersionCheck=true` as a shortcut on a database that really needs migrating (see [OSGi Runtime Services](./osgi-runtime-services.md#runtime-model-version-check)).

### Migration Fails Halfway

**Problem**: Migration executed partially, database is in inconsistent state

**Solution**:
```bash
# Check Liquibase changelog lock
SELECT * FROM databasechangeloglock;

# Release lock if stuck
UPDATE databasechangeloglock SET locked = false;

# Restore from backup and retry
```

### Column Type Mismatch

**Problem**: Migration tries to change column type incompatibly

**Solution**:
- Create manual migration script
- Convert data explicitly:
  ```sql
  -- Add new column with new type
  ALTER TABLE T_ENTITIES_USER ADD COLUMN C_AGE_NEW INTEGER;
  
  -- Convert data
  UPDATE T_ENTITIES_USER SET C_AGE_NEW = CAST(C_AGE_OLD AS INTEGER);
  
  -- Drop old column
  ALTER TABLE T_ENTITIES_USER DROP COLUMN C_AGE_OLD;
  
  -- Rename new column
  ALTER TABLE T_ENTITIES_USER RENAME COLUMN C_AGE_NEW TO C_AGE;
  ```

### Docker Migration Cannot Connect to Database

**Problem**: `connection refused` or `unknown host`

**Solution**:
- Use `host.docker.internal` instead of `localhost` (Docker Desktop)
- Use `--network host` for Docker run
- Ensure database is accessible from container network
- Check firewall rules

## Best Practices

1. **Always backup before migration** - No exceptions in production
2. **Test migrations in staging** - Identical environment to production
3. **Review generated SQL** - Automatic isn't always correct
4. **Version control migrations** - Commit `migration/` directory
5. **Document manual steps** - Complex migrations need runbooks
6. **Use transactions** - Wrap migrations in transactions when possible
7. **Monitor migration time** - Large migrations may need downtime planning
8. **Keep old backups** - Retain backups across several versions
9. **Automate testing** - CI/CD should test migrations automatically
10. **Plan rollback strategy** - Know how to rollback before executing

## Integration with CI/CD

### GitLab CI Example

```yaml
migration-test:
  stage: test
  services:
    - postgres:15
  variables:
    POSTGRES_DB: <app>_test
    POSTGRES_USER: <app>
    POSTGRES_PASSWORD: test
  script:
    # Apply base schema
    - cd application/schema
    - mvn judo-rdbms-schema:apply -DjdbcUrl=jdbc:postgresql://postgres/<app>_test -DdbUser=<app> -DdbPassword=test
    # Generate migration
    - mvn judo-rdbms-schema:generate -DmodelName=<app> -DdbType=postgresql -DbaseModel=${BASE_RDBMS_MODEL} -DupdateModel=${NEW_RDBMS_MODEL}
    # Execute migration
    - mvn judo-rdbms-schema:execute -DbaseModelVersion=${BASE_VERSION} -DupdateModelVersion=${CI_COMMIT_TAG} -DjdbcUrl=jdbc:postgresql://postgres/<app>_test -DdbUser=<app> -DdbPassword=test
```

## See Also

- **Liquibase Documentation**: https://docs.liquibase.com/
- **Model Development**: [Model Guide](../model/README.md) - For information on editing the ESM model.
- **Deployment Guides**: [Deployment Overview](./README.md) - For the full build and deployment process.
- **Application Configuration**: [Application Config](./application-config.md) - For database connection settings.

## File Locations

- Schema module: `application/schema/`
- Migration scripts: `application/schema/migration/<previous>_to_<latest>/`
- Generated models: `application/model/target/generated-resources/model/`
- Liquibase changelogs: `application/model/target/generated-resources/model/<app>-liquibase_[db].changelog.xml`
- Schema JAR: `application/schema/target/<app>-schema-[version].jar`
