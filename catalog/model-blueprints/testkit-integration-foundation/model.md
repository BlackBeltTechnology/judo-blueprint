# Build & Module Layout

This layer covers the **structural** side of the testkit foundation: how the test module is organised, how Maven separates the four tiers (DS / Layer-0 / Layer-1 / Layer-2 / pure-infra), the `pom.xml` shape that wires `surefire`, `failsafe`, `-Pdocker`, and the tooling around it (`logback-test.xml`, `.sdkmanrc`, dependency pinning).

For Java code (support classes, IT shapes, gotchas, verbatim source), see [backend.md](backend.md).

## Module layout

```
application/integration-test/
├── pom.xml                              # surefire/failsafe + -Pdocker profile
├── README.md                            # usage docs (mvn verify, -Pdocker, REQUIRE_DOCKER_IMAGES)
├── resources/                           # classpath resources for *Test.java + *IT.java
│   └── logback-test.xml
└── src/test/
    ├── java/<pkg>/integration/
    │   ├── dscomponent/                 # Tier 1 — *Test.java, OSGi descriptor asserts
    │   │   └── ProfileTargetFilterDescriptorTest.java
    │   ├── testkit/                     # Tier 2 — *IT.java, dispatcher-level
    │   │   ├── support/                 #   The 8 reusable scaffolding classes
    │   │   │   ├── TestContext.java
    │   │   │   ├── Roles.java
    │   │   │   ├── Seed.java
    │   │   │   ├── Calls.java
    │   │   │   ├── AuditAssertions.java
    │   │   │   ├── FieldInjector.java
    │   │   │   ├── Layer0Module.java
    │   │   │   └── SdkFunctionRegistry.java
    │   │   ├── BootIT.java              #   Smoke (must turn green first)
    │   │   ├── access/                  #   12 access-link matrix ITs (Phase 2)
    │   │   ├── operations/              #    9 custom-op ITs (Phase 4)
    │   │   ├── derived/                 #    3 derived-attribute ITs (Phase 5)
    │   │   └── docker/                  #   Layer-1 + Layer-2 overlays (Phase 6)
    │   │       ├── BaseDockerIT.java
    │   │       ├── Layer1DockerModule.java
    │   │       └── Layer2KeycloakModule.java
    │   ├── filestore/                   # Tier 3 — pure-infra IT (testcontainers only)
    │   ├── keycloak/                    # Tier 3 — pure-infra IT
    │   └── stack/                       # Tier 3 — full-stack IT (4-container compose)
    └── resources/
        └── compsych-realm.json          # Keycloak realm import for Layer-2 / Tier-3
```

**Why a separate `testkit/` directory?** Each tier has different runtime requirements and different lifecycle expectations. Putting the testkit suite under its own package keeps the surefire/failsafe configuration straightforward and lets future profiles (`-Pdocker`, `-Pnightly`, etc.) include or exclude it mechanically without resorting to `@Tag` indirection.

## Tier model in detail

| Tier | What it asserts | Runs against | When excluded |
|---|---|---|---|
| **1. DS component** | OSGi DS descriptor XML (`OSGI-INF/*.xml`) — `@Reference target=` filters, service properties | classpath only (no fixtures) | never; runs on every `mvn test` |
| **2a. Layer-0 testkit** | Dispatcher path (access manager, actor resolver, JQL filters, custom ops, interceptors), DAO surface | in-process JUDO runtime + HSQLDB | only excluded under `-Pdocker` (positive group scoping pins to docker) |
| **2b. Layer-1 docker** | Same dispatcher path, but external services (e.g. document-converter) swapped from canned-bytes stub to a real testcontainer | in-process JUDO + HSQLDB + 1+ testcontainer | excluded by default; opt-in via `-Pdocker` |
| **2c. Layer-2 docker** | JWT → `JudoPrincipal` → dispatcher round-trip; production `AuthenticationInterceptor` provisioning side-effects | in-process JUDO + HSQLDB + Keycloak testcontainer | excluded by default; opt-in via `-Pdocker` |
| **3. Pure infra** | Direct contract on a single external service (e.g. MinIO sha256 round-trip), or full-stack compose smoke | testcontainers only (no JUDO runtime, no dispatcher) | excluded by default; opt-in via `-Pdocker` |

### Why two docker overlay sub-tiers (2b / 2c)?

Same Guice module pattern (extend `Layer0Module`, swap one external-service `@Provides` via static flag), different concerns. Layer-1 isolates `DocumentConverterClient` (or any other backend HTTP client) so the IT can assert PDF-bytes / page-count properties impossible at Layer-0. Layer-2 isolates `AuthenticationInterceptor` wiring so the IT can mint a real JWT and prove the production claim-decoding path works.

Both subclass `Layer0Module` to inherit every other binding — DAOs, `ActorVariableRegistrar`, `SdkFunctionRegistrar`, `OperationCallInterceptorRegistrar`. **Do not subclass-override `@Provides` methods** (Guice's `ProviderMethodScanner` registers both parent and child bindings for the same key → `DUPLICATE_BINDING`); use the static-flag pattern documented in `backend.md`.

## `pom.xml` shape

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project ...>
    <parent>
        <artifactId><app>-application</artifactId>
        <groupId><pkg></groupId>
        <version>${revision}</version>
    </parent>

    <artifactId><app>-application-integration-test</artifactId>
    <packaging>jar</packaging>

    <dependencyManagement>
        <dependencies>
            <!-- Force consistent logback version. JUDO transitive deps drag
                 in older versions that throw NoSuchMethodError on <encoder>. -->
            <dependency>
                <groupId>ch.qos.logback</groupId>
                <artifactId>logback-core</artifactId>
                <version>1.5.12</version>
            </dependency>
            <dependency>
                <groupId>ch.qos.logback</groupId>
                <artifactId>logback-classic</artifactId>
                <version>1.5.12</version>
            </dependency>
        </dependencies>
    </dependencyManagement>

    <build>
        <plugins>
            <!-- ============================================================
                 SUREFIRE: drives *Test.java (DS component descriptor tests).
                 ============================================================ -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <configuration>
                    <systemPropertyVariables>
                        <dialect>hsqldb</dialect>
                        <container>none</container>
                    </systemPropertyVariables>
                    <!-- Symmetric with failsafe; in practice no *Test.java
                         here carries @Tag("docker"), but kept for safety. -->
                    <excludedGroups>docker</excludedGroups>
                    <excludes>
                        <exclude>**/testkit/docker/**</exclude>
                    </excludes>
                </configuration>
            </plugin>

            <!-- ============================================================
                 FAILSAFE: drives *IT.java (testkit suite + pure-infra ITs).
                 The parent pom's pluginManagement only registers
                 :integration-test; we MUST add :verify here so `mvn verify`
                 fails on test failures. The :verify goal re-checks the
                 failsafe-summary file and is what actually fails the build.
                 Without :verify, every *IT.java in this module is silently
                 invisible to `mvn verify`.
                 ============================================================ -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-failsafe-plugin</artifactId>
                <executions>
                    <execution>
                        <id>integration-test</id>
                        <goals>
                            <goal>integration-test</goal>
                            <goal>verify</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <systemPropertyVariables>
                        <dialect>hsqldb</dialect>
                        <container>none</container>
                    </systemPropertyVariables>
                    <!-- BELT-AND-BRACES: tag-based AND path-based exclusion.
                         A tag-less docker IT is possible (oversight), and a
                         @Tag("docker") IT outside testkit/docker/ is also
                         possible; either alone has been observed to leak. -->
                    <excludedGroups>docker</excludedGroups>
                    <excludes>
                        <exclude>**/testkit/docker/**</exclude>
                    </excludes>
                </configuration>
            </plugin>

            <plugin>
                <groupId>org.apache.felix</groupId>
                <artifactId>maven-bundle-plugin</artifactId>
            </plugin>
        </plugins>
    </build>

    <dependencies>
        <!-- Generated SDK + app + internal modules (test-scoped where appropriate). -->
        <dependency>
            <groupId><pkg></groupId>
            <artifactId><app>-application-sdk</artifactId>
            <version>${project.version}</version>
        </dependency>
        <dependency>
            <groupId><pkg></groupId>
            <artifactId><app>-application-app</artifactId>
            <version>${project.version}</version>
        </dependency>
        <dependency>
            <groupId><pkg></groupId>
            <artifactId><app>-application-internal</artifactId>
            <version>${project.version}</version>
        </dependency>
        <!-- Production interceptors: pulled in test-scoped so derived/ ITs
             can register them with the dispatcher's
             OperationCallInterceptorProvider, mirroring DS wiring. -->
        <dependency>
            <groupId><pkg></groupId>
            <artifactId><app>-application-interceptors</artifactId>
            <version>${project.version}</version>
            <scope>test</scope>
        </dependency>

        <!-- JUDO runtime testkit + HSQLDB. -->
        <dependency>
            <groupId>hu.blackbelt.judo.runtime</groupId>
            <artifactId>judo-runtime-core-guice-testkit</artifactId>
            <version>${judo-runtime-core-version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>hu.blackbelt.judo.runtime</groupId>
            <artifactId>judo-runtime-core-guice</artifactId>
            <version>${judo-runtime-core-version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>hu.blackbelt.judo.runtime</groupId>
            <artifactId>judo-runtime-core-guice-hsqldb</artifactId>
            <version>${judo-runtime-core-version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.hsqldb</groupId>
            <artifactId>hsqldb</artifactId>
            <version>2.6.1</version>
            <scope>test</scope>
        </dependency>

        <!-- JUnit + Mockito. -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-core</artifactId>
            <version>3.12.4</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.mockito</groupId>
            <artifactId>mockito-junit-jupiter</artifactId>
            <version>3.12.4</version>
            <scope>test</scope>
        </dependency>

        <!-- Testcontainers (Tier-2 docker overlay + Tier-3 pure-infra). -->
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>testcontainers</artifactId>
            <version>${testcontainers-version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.testcontainers</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>${testcontainers-version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>com.github.dasniko</groupId>
            <artifactId>testcontainers-keycloak</artifactId>
            <version>${testcontainers-keycloak-version}</version>
            <scope>test</scope>
        </dependency>
        <dependency>
            <groupId>org.keycloak</groupId>
            <artifactId>keycloak-admin-client</artifactId>
            <version>${keycloak-admin-client-version}</version>
            <scope>test</scope>
        </dependency>
        <!-- Add testcontainers/minio, gotenberg image puller, etc., as needed. -->
    </dependencies>

    <profiles>
        <!-- ============================================================
             -Pdocker — enable Layer-1 / Layer-2 docker overlay ITs and
             Tier-3 pure-infra ITs. Requires:
               * a running Docker daemon;
               * locally-built / pulled testcontainer images (project-specific).

             REQUIRE_DOCKER_IMAGES=1 flips missing-image behaviour from
             "skip with assumeTrue" to fail-fast (used in CI;
             see backend.md → BaseDockerIT).
             ============================================================ -->
        <profile>
            <id>docker</id>
            <build>
                <plugins>
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-surefire-plugin</artifactId>
                        <configuration>
                            <excludedGroups combine.self="override"></excludedGroups>
                            <excludes        combine.self="override"></excludes>
                            <groups>docker</groups>
                        </configuration>
                    </plugin>
                    <plugin>
                        <groupId>org.apache.maven.plugins</groupId>
                        <artifactId>maven-failsafe-plugin</artifactId>
                        <configuration>
                            <excludedGroups combine.self="override"></excludedGroups>
                            <excludes        combine.self="override"></excludes>
                            <groups>docker</groups>  <!-- positive scoping -->
                        </configuration>
                    </plugin>
                </plugins>
            </build>
        </profile>
    </profiles>
</project>
```

### Key `pom.xml` decisions

1. **Failsafe `:verify` MUST be in child `<plugins>` block.** Most JUDO parent POMs only register `:integration-test` in `pluginManagement`. Without `:verify` failsafe runs but the build never fails on test failures — every `*IT.java` is silently invisible to `mvn verify`. Verify by running `mvn -pl <module> verify` with a deliberately broken IT and confirming the build fails.

2. **Belt-and-braces docker exclusion.** `<excludedGroups>docker</excludedGroups>` covers any `@Tag("docker")`-annotated subclass; the path `<excludes>**/testkit/docker/**</excludes>` covers any future tag-less docker IT. Either alone has been observed to leak — keep both.

3. **`-Pdocker` uses `combine.self="override"` + positive `<groups>docker</groups>`.** The negative excludes are wiped (so docker tests can run) and the positive group scoping pins the run to `@Tag("docker")` ITs only — preventing the docker profile from unintentionally re-executing the whole Layer-0 suite.

4. **System properties `dialect=hsqldb` and `container=none`** are read by the JUDO datasource fixture. They MUST be set on both surefire and failsafe — surefire-only ITs will fail because the fixture defaults to a different dialect.

5. **Force-pin Logback to a single 1.5.x version** in `<dependencyManagement>`. JUDO transitive deps drag in older versions that throw `NoSuchMethodError` when Logback parses `<encoder>` blocks in `logback-test.xml`.

## Tooling

### `src/test/resources/logback-test.xml`

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <root level="INFO">
        <appender-ref ref="STDOUT" />
    </root>

    <!-- Project-specific debug logger -->
    <logger name="<your.app.package>" level="DEBUG" />

    <!-- Tame noisy frameworks -->
    <logger name="org.hibernate" level="WARN" />
    <logger name="org.hsqldb"    level="WARN" />

    <!-- Hide Liquibase chatter -->
    <logger name="liquibase"            level="WARN" />
    <logger name="liquibase.database"   level="WARN" />
    <logger name="liquibase.changelog"  level="WARN" />
    <logger name="liquibase.lockservice" level="WARN" />
    <logger name="liquibase.executor"   level="WARN" />
    <logger name="liquibase.snapshot"   level="WARN" />
</configuration>
```

### `.sdkmanrc` (project root, generated by `./judo.sh generate-root`)

```
java=21.0.7-zulu
maven=3.9.10
mvnd=1.0.2
```

The compsych-letter-framework pins these as the only versions that build the testkit cleanly. Java 17 fails on `pattern-matching switch` (used in some custom-op impls); Maven 3.6 fails on `combine.self` semantics in the `-Pdocker` profile.

### How to run

```bash
# Default suite (no Docker): DS component + Layer-0 testkit
mvn -pl application/integration-test verify

# Docker overlay tier (Layer-1 + Layer-2 + pure-infra)
mvn -pl application/integration-test -Pdocker verify

# CI fail-fast on missing testcontainer images
REQUIRE_DOCKER_IMAGES=1 mvn -pl application/integration-test -Pdocker verify
```

### Build locally-required testcontainer images first (project-specific)

The compsych-letter-framework Layer-1 expects a tagged image `compsych-document-converter:dev` built from the local Dockerfile:

```bash
docker build -t compsych-document-converter:dev services/document-converter
```

CI typically builds this image as a pre-step. Locally only needed when running the `-Pdocker` profile.
