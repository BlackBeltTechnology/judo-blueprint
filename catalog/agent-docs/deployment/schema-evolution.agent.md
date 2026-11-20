# schema-evolution.md — index

Pull-only condensed map. Source: catalog/agent-docs/deployment/schema-evolution.md.

## Overview
- Module `application/schema/` (Liquibase under the hood) migrates DB when model evolves. `<app>` = `app_name` in `judo.properties`.

## Table of Contents
- Quick Start, Key Concepts, Review Workflow, Migration Commands, Production Strategy, Troubleshooting, Best Practices.

## Quick Start Workflow
- 1. `cd application/model && mvn clean install`.
- 2. `mvn judo-rdbms-schema:generate -DmodelName=<app> -DdbType=postgresql -DbaseModel=<file|mvn:> -DupdateModel=<file|mvn:>` from `application/schema/`. Without base model, base read from `latest.version` / `previous.version` in output dir.
- 3. `mvn judo-rdbms-schema:execute -DbaseModelVersion=… -DupdateModelVersion=… -DjdbcUrl=jdbc:postgresql://localhost:5432/<app> -DdbUser=<app> -DdbPassword=[password]`.
- 4. `./judo.sh start` to verify.

## Key Concepts

### What is Schema Evolution?
- Model changes → table/column/type/FK changes. Managed incrementally.

### When No Manual Step Is Needed
- Adding a stored member to a fresh/new DB: no manual step; generated Liquibase changelog (`application/model/target/generated-resources/model/<app>-liquibase_postgresql.changelog.xml`) already creates the column.
- Existing DB is NOT migrated automatically. Startup fails `There are RDBMS model changes which have not been applied to database`. Migrate or discard DB+volume. Never use `ignoreVersionCheck` to get past it.
- Manual schema-upgrade needed for persistent DB with data and for non-additive changes (renames, type changes, removals).
- Local persistent PostgreSQL: `./judo.sh schema-upgrade` (generates diff vs running DB and applies).
- `judo.sh` schema module path = `schema_dir` (default `model_dir`). Set `schema_dir=<dir>` in `judo.properties` or env, e.g. `schema_dir=application ./judo.sh schema-upgrade`.
- `DATABASE HAVE TO BE UPDATED!` logged at error level by `generate` = notice, not failure; build still `BUILD SUCCESS`; migration needed before new model runs on that DB.
- Migration REQUIRED when entity types change: add/remove/modify mapped entities; attributes on entities; attribute types; relationships; entity inheritance.
- NOT required for: transfer object types, actors/access points, UI layouts/forms, operations (unless they affect entity structure), validations, derived attributes. Reason: schema generated only from entity types.
- Module: `application/schema/`; CLI tool + Docker image; auto script generation; incremental any-to-any; manual SQL support; PostgreSQL, HSQLDB, etc.

## Module Structure
- `application/schema/`: `pom.xml`, `migration/` (manual scripts `[manual-scripts].sql`), `README.adoc`, `target/<app>-schema-[version].jar`.

## Schema Migration Workflow

### Step 1: Identify Model Versions
- Base (FROM) = current DB schema version; Update (TO) = target.
- Model version = `model-version` property = `${project.version}` in generated model POM. Pipelines use timestamped form (`1.1.0.20210929_004050_9602796_develop`) via `./judo.sh build -v <version>`.
- This is the MODEL version (`Judo-Models` bundle header / `model-version`), not app version.

### Step 2: Generate Migration Scripts
- `mvn judo-rdbms-schema:generate -DmodelName=<app> -DdbType=postgresql -DbaseModel=… -DupdateModel=… -DoutputDirectory=migration`.
- Output `migration/<previous>_to_<latest>/` (dots/dashes → underscores):
  - `00_<app>_incremental_<dialect>.changeset.xml` aggregate + 8 phase changesets: `check`, `backup`, `beforeIncremental`, `updateDataBeforeIncremental`, `incremental`, `updateDataAfterIncremental`, `aferIncremental` (sic; script `07_aferIncremental`), `dropBackup`.
  - model `<app>-rdbms_<version>_<dialect>.model`.
  - marker files `latest.version`, `previous.version` drive version resolution next run.
- Only data-migration changesets (`updateDataBeforeIncremental`, `updateDataAfterIncremental`) need developer input; empty unless written.

### Step 3: Manual Migration Scripts (Optional)
- For data transformations, complex logic, splitting/merging columns, data fixes.
- Write data changesets in generated version folder under `application/schema/migration/`.
- Table names `T_ENTITIES_<NAME>`, columns `C_<NAME>` (verify in changelog). Example: `UPDATE T_ENTITIES_USER SET C_FULL_NAME = CONCAT(...) WHERE C_FULL_NAME IS NULL`.

## Review Workflow for Incremental Migrations
- Changes classified: `identical`, `applyable` (automatic), `review-required` (renames, narrowing type changes, data loss).
- Startup stops when DB-stored base model differs from app's base model: execute incremental first.
- Review needed → generate writes `<name>.sql.missing`. Rename to `.sql` in `reviewScriptDirectory`. Without them `isApplyable()` false; `execute`/`apply` fail `IllegalStateException: Missing scripts`.
- Generation overwrites all output files EXCEPT review files.
- `useXmiId` (default `true`): keeps renames detected as modify. Keep `true` when renaming entities/attributes.
- `ignoreReview`: default `false` for `generate`, `true` for Maven `execute`/`apply`. Pipelines set explicitly (`--ignoreReview`).
- Consolidate per-snapshot folders: regenerate one folder from oldest base → current model; move hand-written steps in; delete intermediates. `DATABASE HAVE TO BE UPDATED` during this generate is normal.
- Projects may have many steps (e.g. 18 steps, changesets `00`..`08`); only non-empty data changesets carry knowledge.
- PK constraints are `PK_<column>` (no table name): same-named key/mandatory columns across entities break the migration; rename in the model.
- Multi-field unique constraints: one single-column constraint per field (combined uniqueness not enforced; add a manual index) and one `DropUniqueConstraint` per field.
- DbCheckup emits `TableExists` for every table, including new ones; review preconditions.
- Zeta incremental compares previous model with itself (container checks always true): constraints on new elements can be missing; review changelog.
- Known issue: backup names for long table names are truncated in the post-check and backup-delete steps but not in the pre-check; check `BACKUP_` names in the script before running it.
- Pipeline script example: `./update.sh --version <v> --schema generate|execute --ignoreReview`; runner snapshots backup (e.g. Neon branch `backup-<ts>`) before `execute`; rollback `--schema restore --branch backup-<ts>`.

### Step 4: Test Migration
- Always test in staging first. Flow: checkout old version, build, start; stop app; `pg_dump` backup; `mvn judo-rdbms-schema:execute -DbaseModelVersion=1.1.0 -DupdateModelVersion=1.2.0 -DjdbcUrl=… -DdbType=postgresql …`; checkout new, `mvn clean install -DskipDocker`, `./judo.sh start`; verify.

### Step 5: Rollback
- Stop DB; drop/recreate DB (docker `postgres:15` or `dropdb`); restore `psql < backup`; start old version.

## Migration Commands

### Maven-Based Migrations
- Apply fresh schema (dev only): `mvn judo-rdbms-schema:apply -DjdbcUrl=… -DdbType=postgresql -DdbUser=… -DdbPassword=…`. `apply` also takes `modelName`, `updateModel`, `reviewScriptDirectory`, `outputDirectory` (default `target/classes/schema`).
- Generate: see Step 2.
- Execute: `mvn judo-rdbms-schema:execute -DbaseModelVersion=1.1.0.20210929_004050 -DupdateModelVersion=1.2.0.20211021_085156 -DjdbcUrl=… -DdbType=postgresql -DdbUser=… -DdbPassword=…`.

### Docker-Based Migrations
- Build: `mvn clean install -Pdocker` in `application/schema`; image `<app>-schema:[version]` (artifactId name).
- Run: `docker run --rm <app>-schema:latest execute --baseModelVersion=… --updateModelVersion=… --modelName=<app> --incrementalDirectory=/ --jdbcUrl=jdbc:postgresql://host.docker.internal:5432/<app> --dbType=postgresql --dbUser=… --dbPassword=…`.
- `host.docker.internal` for host DB (Docker Desktop), else hostname/IP.
- Compose: service `db-migration` with `command: [execute, --baseModelVersion=${BASE_VERSION}, --updateModelVersion=${UPDATE_VERSION}, …]`, depends on `postgres:15` service.

## Production Migration Strategy

### Recommended Approach
1. Prepare: generate from `${CURRENT_PROD_RDBMS_MODEL}` → `${NEW_RDBMS_MODEL}`; review changesets and `*.sql.missing`.
2. Test in staging (clone prod DB, execute, test).
3. Backup prod (`pg_dump`, timestamped).
4. Maintenance window: stop app, execute migration, deploy new version, verify, start.
5. Verify/monitor: logs, data integrity, performance; keep backup for rollback.

### Blue-Green Consideration
- Backward-compatible migrations; additive changes (nullable columns, new tables); deploy app first, remove deprecated elements later; feature flags.

## Configuration

### Model Version Configuration
- Generated model sets `<model-version>${project.version}</model-version>`.
- Composite form (`1.2.0.20211021_085156_21efaed_develop`) not generated; supply via build version (`./judo.sh build -v <version>`). Override via `pom.xml.model-properties-definition.fragment.hbs`.

### Schema Module Properties
- In `application/schema/pom.xml`: `modelName`, `incrementalDirectory` (`${basedir}/migration`), `updateModelArtifactVersion` (`${project.version}`).

## Troubleshooting
- "Unknown version": model not built/installed; `mvn clean install` in `application/model`; check `mvn dependency:tree | grep <app>-model`.
- Scripts not generated: check both models valid and different (`Update model is not defined` = `updateModel` missing); model artifacts in `~/.m2/repository`.
- Startup "RDBMS model changes which have not been applied": stored version in `JUDO_MODEL_VERSIONS` differs. Run incremental migration or restore DB. Never `ignoreVersionCheck=true` as shortcut (see deployment osgi-runtime-services.md#runtime-model-version-check).
- Halfway failure: check `databasechangeloglock`; release lock (`UPDATE databasechangeloglock SET locked = false`) if stuck; restore backup and retry.
- Column type mismatch: manual script: add new column, `CAST` copy, drop old, rename new (`ALTER TABLE T_ENTITIES_USER …`).
- Docker cannot connect: `host.docker.internal` not `localhost`; or `--network host`; check network/firewall.

## Best Practices
- Backup before every production migration; test in staging; review generated SQL; version control `migration/`; document manual steps; use transactions; plan downtime for large migrations; keep old backups; automate migration tests in CI; plan rollback first.

## Integration with CI/CD
- GitLab example: service `postgres:15`; `mvn judo-rdbms-schema:apply` on base; `generate` from base/new RDBMS models; `execute` with `${BASE_VERSION}` → `${CI_COMMIT_TAG}`.

## See Also
- Liquibase docs; model/README.md (ESM editing); deployment/README.md (build/deploy); deployment application-config.md (DB connection).

## File Locations
- Schema module `application/schema/`; migrations `application/schema/migration/<previous>_to_<latest>/`; generated models `application/model/target/generated-resources/model/`; Liquibase changelog `…/<app>-liquibase_[db].changelog.xml`; schema JAR `application/schema/target/<app>-schema-[version].jar`.
