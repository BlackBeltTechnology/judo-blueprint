# JUDO knowledge check: claim validation against judo-ng source

Each claim in `judo-knowledge-check.md` (C1…), and each factual statement in the developer's answers (D1…), checked against the read-only judo-ng checkout (`target/judo-ng-read/wt/`). Evidence is `repo/path:line`.

**Scope: ESM only.** JSL does not matter: JSL code is not used as evidence, the JSL-only topics K01 and K03 are dropped, and claims that exist only for JSL (including Spring Boot) are marked 🚫 N/A-ESM.

| Verdict | Meaning | Claims (C) | Developer statements (D) |
|---|---|---|---|
| ✅ TRUE | Code confirms it | 64 | 37 |
| ⚠️ PARTLY | Partly right; the note gives the correction | 63 | 22 |
| ❌ FALSE | Code contradicts it | 7 | 0 |
| ❔ NOT FOUND | No evidence either way | 13 | 12 |
| 📐 PRACTICE | Application practice; code cannot confirm | 34 | 19 |
| 🚫 N/A-ESM | Exists only for JSL; does not apply to ESM | 6 | 1 |

Total: 278 verdicts. Every factual sentence in the developer's answers is covered (a coverage audit added the D20 rows). Verdicts come from a code search, not from running the platform; NOT FOUND does not mean wrong.

## Contradicted (❌)

- **K16.C3** Relation kinds, CRUD flags and generated endpoints: `fixRelationProperties` sets AGGREGATION when the source or target is not mapped (or is transient), not for lower bound 1, compositions or derived associations. The `transfer_` prefix appears only as a test-generator constant (judo-platform-itest CRUD_Object_Attribute.java:29), not in any transformation. (`models__judo-meta-esm/model/src/main/java/hu/blackbelt/judo/meta/esm/runtime/EsmUtils.java:3901`)
- **K34.C1** Schema migration manual steps and version checks: The generated changelog contains the column for a fresh DB, but with an existing DB the prehook throws "There are RDBMS model changes which have not been applied to database"; incremental migration (generate steps, review, execute) is needed. (`runtime__judo-services/judo-services-persistence/src/main/java/hu/blackbelt/judo/services/persistence/LiquibaseModelDataSourcePrehook.java:166-185`)
- **K40.C1** Local e-mail testing with Mailpit and Keycloak SMTP: Defaults: with logSmtpServer=true (set in judo-karaf.env.hbs:3 and dev compose) host=localhost, port=10025 (a log SMTP server), else port 25; localhost:1025 appears nowhere. Env names mailSmtpHost/mailSmtpPort/mailSmtpFrom (JUDO_PLATFORM_MAIL_SMTP_*) are the override mechanism (application-config.md.hbs:262+). Pointing the mail catcher at 10025 or overriding host/port works; 1025 is not the default. (`runtime__judo-platform/judo-platform-config-templates/src/main/resources/judo-platform-config-templates/hu.blackbelt.email.impl.JavaMailSenderActivator.template:12,16`)
- **K49.C2** API-level tests with ApiClient and Postman: Postman v2.1 collections (schema v2.1.0) with localhost:8181 live in the platform's judo-platform-itest, not in the generated application; no postman files in the fullstack template or the PSM generators. (`runtime__judo-platform/judo-platform-itest/itests/UrlVariables.postman_environment.json:6`)
- **K54.C2** Generated DAO read and write performance: createAll is just a for-loop calling create() per payload; no batching or caching. (`runtime__judo-runtime-core/judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/AbstractRdbmsDAO.java:217`)
- **K55.C1** Derived fields need explicit mask inclusion: With mask == null features are included (except parameterized ones); with a mask only masked features are; derived attributes need no extra mask unless a mask is given. (`runtime__judo-runtime-core/judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/query/model/RdbmsResultSet.java:707`)
- **K77.C3** Typed media attachment with several owner types: The modelled API only returns a download token (ResponseConverter.java:117-128); the bytes are served by the separate HTTP DownloadServlet (getOutputStream :200) for every client, frontend included; upload likewise goes through UploadServlet. (`runtime__osgi-filestore/filestore-servlet/src/main/java/hu/blackbelt/osgi/filestore/servlet/DownloadServlet.java:145`)

## Not applicable to ESM (🚫)

- **K06.C1** `query ... (Integer limit = 100)` and `self.ordersOver(limit = 10)` are JSL syntax; in ESM a query feature has an `input` transfer object type (ParameterizedQueryTest.java:138 builds it via withInput) with no default-value syntax shown.
- **K06.C2** Generators only read the `ParameterObject` annotation; no non-JSL transformation creates `_<Entity>_<Query>Parameters` objects (rg finds the naming only in JSL tatami).
- **K43.C1** Spring Boot runtime assembly is JSL-only.
- **K43.C2** Spring Boot application.properties/Liquibase config is JSL-only.
- **K43.C3** judo-spring-maven-plugin / Spring DaoModules is JSL-only.
- **K43.D1** Developer "yes" confirms a Spring-Boot (JSL-only) claim set.
- **K45.C1** judo-jsl-springboot-archetype is a JSL/Spring Boot archetype.

## Developer statements the code does not fully back (⚠️ / ❌ on D)

- **K06.D1** ⚠️ Parameterized queries and operation input ranges are working features covered by itests (ParameterizedQueryTest, RangeTest); the JSL-syntax parts of the claims are not covered. (`runtime__judo-runtime-core-esm-itest/src/test/java/hu/blackbelt/judo/runtime/core/dao/rdbms/ParameterizedQueryTest.java:93`)
- **K10.D2** ⚠️ Small table flag is handled (TabularReferenceFieldTableTransformations.java:195); the validation limiting small tables is commented out (ui validations/table.evl:15-21); "gets all items without pagination" and "only eager" are not verified in ESM code (the eager rule is JSL-only, viewTableDeclaration.etl:18 "currently the runtime only supports inline edit for eager tables"). (`runtime__judo-tatami-client/judo-tatami-esm2ui/src/main/epsilon/transformations/ui/modules/ui/tabularReferenceFieldTable.etl:75`)
- **K15.D1** ⚠️ The backend accepts `X-Judo-CountRecords` on every operation and counts when the header is non-blank; whether the frontend sends it only when needed was not checked. SignedIdentifier is required only on bound operations (rest.service.operation.fragment.hbs:78). (`template__judo-psm-generator-jaxrs/judo-psm-generator-jaxrs-impl/src/main/resources/rest/impl/rest.service.impl.java.hbs:27`)
- **K17.D1** ⚠️ The server always emits UTC offsets, and the frontend turns strings into JS `Date` (serialization.ts.hbs:16-20), which shows in browser-local time. Browser-zone display is plausible; I did not read the frontend timestamp formatting. (`runtime__judo-runtime-core/judo-runtime-core-jackson/src/main/java/hu/blackbelt/judo/runtime/core/jackson/serializer/LocalDateTimeSerializer.java:16`)
- **K20.D1** ⚠️ The code shows owner = relation or operation. An owner "with a signed identifier" is not checked here: bound operations get the `X-Judo-SignedIdentifier` header (rest.service.operation.fragment.hbs:78). (`models__judo-meta-psm/model/src/main/epsilon/validations/service/getRangeBehaviour.evl:5`)
- **K21.D2** ⚠️ Signed identifier's producing reference/type must match the TO type (hasCorrectSigner), else AccessDeniedException ACCESS_DENIED_INVALID_TYPE; so a different TO type for the same entity is rejected - but the code is ACCESS_DENIED_INVALID_TYPE / INVALID_IDENTIFIER, not literally ERROR_INVALID_IDENTIFIER. (`runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultIdentifierSigner.java:259-265`)
- **K21.D3** ⚠️ An instance produced by a reference/operation not exposed to the actor is rejected (ACCESS_DENIED_FOR_INSTANCE_OF_BOUND_OPERATION), and RequestConverter checks signature-vs-type; the specific "range TO cannot set a reference" case follows from the producedBy/type check but no dedicated test was found. (`runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultAccessManager.java:125-131`)
- **K22.D1** ⚠️ customImplementation=true ops must be bound by an SDK service; with none the SDK-operations-ready check does not complete (activation waits, unless skipMissingSdkOperationsCheck). The "we write/overwrite the .default custom op" part is a generator workflow (empty-custom-operation-implementation-osgi.java.hbs usage text), not runtime behaviour. (`runtime__judo-platform/judo-platform-services/judo-services-dispatcher-osgi/.../DefaultDispatcherFunctionProvider.java:92-125`)
- **K22.D3** ⚠️ Only get<X>/set<X> names are rejected by validation; create/delete prefixes are not validated (advice only). (`models__judo-meta-esm/model/src/main/epsilon/validations/operation/operation.evl:140-148`)
- **K23.D1** ⚠️ Developer's doubt is right for custom operations: behaviour operations are intercepted, custom ones are not (see K23.C1). (`runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultDispatcher.java:740-800`)
- **K27.D3** ⚠️ "yes" is wrong for default access types (HUMAN=CONFIDENTIAL, SYSTEM=BEARER_ONLY in guice config). (`see K27.C3`)
- **K32.D1** ⚠️ The file is uploaded to the filestore first and the entity stores only a reference, but it holds four values as JSON: id, fileName, size and mimeType (not three). (`runtime__judo-runtime-core/judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/converters/FileTypeFormatter.java:36-60`)
- **K33.D2** ⚠️ Conversion rule is documented as stated but its code is not in the checkout. (`template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/application-config.md.hbs:76-96`)
- **K34.D1** ⚠️ Steps generate Liquibase SQL for review with data-update phases that can be edited, then executed; "never use apply" is advice (PRACTICE). The "production yes, can be triggered manually locally" part is not checkable in code, and per K34.C1 a manual migration step is needed whenever the model changes. (`runtime__judo-rdbms-schema/judo-rdbms-schema-incremental/src/main/java/hu/blackbelt/judo/rdbms/schema/incremental/IncrementalLiquibaseExecutor.java:157-247`)
- **K35.D1** ⚠️ "yes" to C1 is right for limits but columns are upper-cased in the generator. (`runtime__judo-tatami-base/judo-tatami-asm2rdbms/src/main/java/hu/blackbelt/judo/tatami/asm2rdbms/zeta/Asm2RdbmsHelper.java:308`)
- **K40.D1** ⚠️ "yes" holds for the Keycloak-vs-application split, but not for the 1025 default (see K40.C1). (`runtime__judo-platform/judo-platform-config-templates/src/main/resources/judo-platform-config-templates/hu.blackbelt.email.impl.JavaMailSenderActivator.template:12-16`)
- **K42.D1** ⚠️ judo.sh has `-i/--ignore-checksum`, which passes -DvalidateChecksum=false to Maven. The Maven property is `validateChecksum=false`, there is no `ignoreChecksum=true` property. (`template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-root/src/main/resources/judo.sh.hbs:14,105,819`)
- **K45.D1** ⚠️ A `generateAgentCli` template parameter (default false) exists for AI agent CLI docs; that generating a fresh ESM fullstack project yields the newest CLI version was not verified. (`template__judo-esm-fullstack-project-template/README.md:428`)
- **K47.D1** ⚠️ Javadoc says class-level sharing gives ~5-10x speedup, but BY_CLASS alone shares only DataSource/model loader; QueryFactory is rebuilt per method unless shareInjector=true as well. (`runtime__judo-runtime-core/judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoTest.java:184-189`)
- **K49.D1** ⚠️ Yes holds for the ApiClient part (C1); not for the generated Postman collections (C2). (`template__judo-psm-generator-restassured/judo-psm-generator-restassured-api/src/main/resources/restassured/api/apiClient.java.hbs:77`)
- **K14.D20** ⚠️ "Required attributes get plain getters, optional ones Optional<T>" — Not re-verified line by line. Related D2 shows the optional getter exists; a required-plain/optional-Optional split is consistent with it. (added by the coverage audit) (`template__judo-psm-generator-sdk-core/judo-psm-generator-sdk-core-api/src/main/resources/dao/api/dto.java.hbs:261`)
- **K22.D20** ⚠️ "errorCode can be an enum or a string; string is looser" — The fault map's _errorCode (FAULT_ERROR_CODE, line 93) is cast to String, so a string works. An enum-typed errorCode is not handled in the dispatcher. The "stricter to the model" point is a modelling opinion. (added by the coverage audit) (`runtime__judo-runtime-core/judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/DefaultDispatcher.java:408-413`)

## All verdicts by topic

### K02 JQL built-in function reference

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | JQL ships temporal functions (`current_date`, `current_timestamp`, `date(y,m,d)`, `elapsedTimeInMinutes`), collection selectors `head`/`tail`/`heads`/`tails`, a… | `models__judo-meta-expression/builder-jql/src/main/java/hu/blackbelt/judo/meta/expression/builder/jql/JqlTransformers.java:245-251,403,440-476` | head/tail/heads/tails, date, lpad/rpad/ltrim/rtrim/capitalize/ilike are registered; `elapsedTimeInMinutes` does NOT exist (the function is `elapsedTimeFrom`, line 391); `current_date`/`current_timestamp` are not functions but SYSTEM variables reached via `Date!now()`/`Timestamp!now()` (NowFunctionTransformer.java:37-38) or getVariable. |
| C2 | ✅ TRUE | `sum` accepts only integer and decimal values; strings or temporal values fail with "Invalid expression for aggregation". | `models__judo-meta-expression/builder-jql/src/main/java/hu/blackbelt/judo/meta/expression/builder/jql/function/collection/JqlAggregatedExpressionTransformer.java:66,95` | sum is built with only Integer and Decimal aggregators (others null) and any other type throws IllegalArgumentException "Invalid expression for aggregation: ...". |
| C3 | ⚠️ PARTLY | Measured literals use `measure#unit` or `unit`, not `[kg]`; equality is only `==`/`!=`, enum literals are `Type#VALUE`, and the ternary is right-associative. //… | `models__judo-meta-jql/model/src/main/java/hu/blackbelt/judo/meta/jql/JqlDsl.xtext:134-135,149` | Measured literal IS bracketed: `5 [kg]` or `5 [measure#unit]` (MEASURE_NAME terminal `[...]`, regex `((.*)#)?(.*)` in JqlMeasuredLiteralTransformer.java:42), so "not [kg]" is wrong; equality `==`/`!=` only (line 31), enum `Type#VALUE` (line 76), and ternary is right-associative (line 8-12) are correct. |
| D1 | 📐 PRACTICE | (developer statement) | `runtime__judo-runtime-core-esm-itest/src/test/java/hu/blackbelt/judo/runtime/core/dao/rdbms/PrimitiveOperationTest.java:485-488` | Pointer to itests as the source of truth; they exist and cover functions (e.g. `'apple'!lpad(10, '*')`), advice not a platform fact. |
| D20 | 📐 PRACTICE | (developer statement) | `models__judo-meta-esm/model/src/main/epsilon/validations/measure/measure.evl:1` | "Measured literals ... // NOT IN USE" — Team usage status. Code shows measures are a live ESM feature: ESM!Measure and ESM!MeasuredType validations (measure.evl, measuredType.evl:1), esm2ui measuredType.etl, runtime MeasuredDecimalConstantTranslator (runtime__judo-runtime-core/judo-runtime-core-dao-rdbms/.../query/translators/), psm2measure transformation. Not dead code. (added by the coverage audit) |

Developer answer: _runtume-core-esm-itest expression examples -> test for what works and what not, use the testkit_

### K04 Expression variable categories and custom providers

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | `getVariable(category, key)` resolves from built-in categories `SYSTEM` (`current_date`, `current_time`, `current_timestamp`), `ENVIRONMENT` (env var, falling b… | `runtime__judo-runtime-core/judo-runtime-core-guice/src/main/java/hu/blackbelt/judo/runtime/core/guice/dispatcher/DefaultVariableResolverProvider.java:47-52` | Core registers SYSTEM (current_timestamp/date/time), ENVIRONMENT (getenv then System.getProperty, EnvironmentVariableProvider.java:33-36), SEQUENCE, REQUEST; USER, ACTOR, PRINCIPAL are registered by OSGi components in runtime__judo-services (DefaultAccessTokenVariableResolverComponent.java:32, DefaultActorVariableResolverComponent.java:32, DefaultPrincipalVariableResolverComponent.java:35), so they exist only in the OSGi deployment. |
| C2 | ✅ TRUE | `SEQUENCE` advances a named sequence and returns its next value. | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/environment/SequenceProvider.java:40-41` | SEQUENCE is a function category; apply(name) returns sequence.getNextValue(name). |
| C3 | ⚠️ PARTLY | Custom providers register as OSGi components with property `judo.environment-variable-provider=true` plus a category property, or programmatically through `Vari… | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/environment/DefaultVariableResolver.java:75-91` | registerSupplier/registerFunction exist (VariableResolverManager); the `judo.environment-variable-provider=true` + `category`/`key`/`cacheable` property is only described in documentation/.../02_jql_variables.adoc and no code in the checked repos consumes it (rg finds that string only in the doc). |
| D1 | ✅ TRUE | (developer statement) | `models__judo-meta-expression/builder-jql/src/main/java/hu/blackbelt/judo/meta/expression/builder/jql/JqlTransformers.java:385` | getVariable is used as `PrimitiveType!getVariable('CAT','key')` (doc 02_jql_variables.adoc:16-17); the type prefix gives the result type, e.g. `String!getVariable('ACTOR','email')`. |

Developer answer: _getVariable has to came the type form it will provide, like fqn:String!getVariable('ACTOR', 'email'), chekc the intern documentation in the documentaion repository in judo ng for more details, and where this variable can be used._

### K05 Numeric type mapping and enumeration constraints

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | Integer numerics map by precision: 1–9 → `Integer`, 10–19 → `Long`, otherwise `BigDecimal`; precision and scale also determine the Java type of decimal numerics… | `runtime__judo-tatami-base/judo-tatami-psm2asm/src/main/epsilon/transformations/asm/modules/type.etl:39-45,57-63` | Integer numerics: precision 1-9 Integer, 10-19 Long, else BigDecimal; decimals: precision<=7 and scale<=4 Float, <=15 and scale<=4 Double, else BigDecimal. |
| C2 | ⚠️ PARTLY | Enum ordinals must be in the range 0–9999, and names (case-insensitive) and ordinals must each be unique, with at least one literal. Values persist by ordinal, … | `models__judo-meta-esm/model/src/main/epsilon/validations/type/enumerationMember.evl:2-5` | Only ordinal uniqueness is a constraint; no 0-9999 range or case-insensitive name uniqueness check found in ESM/PSM validations; enumerationType.evl:4-8 requires more than one member (a critique, not "at least one"); ASM literal value = ordinal (type.etl:13), so persisted-by-ordinal consequence is plausible but not shown in the DAO. |
| C3 | ✅ TRUE | Password and XML data types are not supported; transformation aborts with "not supported yet". | `runtime__judo-tatami-base/judo-tatami-psm2asm/src/main/epsilon/transformations/asm/modules/type.etl:109,149` | Transformation throws "Password type is not supported yet." and "XML type is not supported yet.". |
| D1 | ✅ TRUE | (developer statement) | `runtime__judo-tatami-base/judo-tatami-psm2asm/src/main/epsilon/transformations/asm/modules/type.etl:57-63` | Java type of decimals depends on both precision and scale (scale<=4 needed for Float/Double); integer type depends on precision (39-45). |
| D2 | ✅ TRUE | (developer statement) | `models__judo-meta-esm/model/src/main/epsilon/validations/type/enumerationMember.evl:2-5` | Only uniqueness of ordinals is validated, so gaps (1,5,8) are allowed. |
| D3 | ✅ TRUE | (developer statement) | `runtime__judo-tatami-base/judo-tatami-psm2asm/src/main/epsilon/transformations/asm/modules/type.etl:109` | Password/XML remain unsupported in the transformation. |

Developer answer: _1. yes this is the behavore, but its depends on the precison and the scale and the scale count to the precision u should create a spike to check whether this is true or not. / 2. yes its true, the numbers can be like 1,5,8 so gaps are allowed / 3. stay not supported_

### K06 Parameterized queries and parameter ranges

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 🚫 N/A-ESM | A JSL query can declare parameters with defaults, e.g. `query Order[] ordersOver(Integer limit = 100)`, and a derived relation can call it: `self.ordersOver(lim… | `models__judo-meta-esm/model/model/esm.ecore:405` | `query ... (Integer limit = 100)` and `self.ordersOver(limit = 10)` are JSL syntax; in ESM a query feature has an `input` transfer object type (ParameterizedQueryTest.java:138 builds it via withInput) with no default-value syntax shown. |
| C2 | 🚫 N/A-ESM | A static query with parameters generates an unmapped transfer object named `_<Entity>_<Query>Parameters`, annotated `ParameterObject`. | `template__judo-psm-generator-sdk-core/judo-psm-generator-sdk-core-api/src/main/java/hu/blackbelt/judo/psm/generator/sdk/core/api/ObjectTypeHelper.java:89` | Generators only read the `ParameterObject` annotation; no non-JSL transformation creates `_<Entity>_<Query>Parameters` objects (rg finds the naming only in JSL tatami). |
| C3 | ✅ TRUE | An operation input parameter can carry a range (`RangeType.DERIVED` or `ANY`) with an expression such as `self.products`, which restricts the values a caller ma… | `models__judo-meta-esm/model/model/esm.ecore:399-402,550-552` | Operation parameter has rangeType (ANY default, DERIVED) and rangeExpression; parameter.evl:9-12 requires an expression for DERIVED; DefaultDispatcher.java:513 validates range, RangeTest.java:139-168 exercises DERIVED/ANY (expression is a type or path, e.g. `Apple`). |
| D1 | ⚠️ PARTLY | (developer statement) | `runtime__judo-runtime-core-esm-itest/src/test/java/hu/blackbelt/judo/runtime/core/dao/rdbms/ParameterizedQueryTest.java:93` | Parameterized queries and operation input ranges are working features covered by itests (ParameterizedQueryTest, RangeTest); the JSL-syntax parts of the claims are not covered. |

Developer answer: _Same as K01, u should check it in ESM runtime-core-itest wheter its a working feature or not._

### K07 Measures, units and store-unit conversion

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | A measure is either a base measure with a base unit, or a derived measure built from other measures' units with exponents (e.g. `Area = Length.metre^2`). A meas… | `models__judo-meta-measure/model/model/measure.ecore:27-36` | BaseMeasure and DerivedMeasure with terms exist; a term is BaseMeasure + integer exponent (not another measure's unit); self-reference rejected by NoCircularReferencesOfMeasureWithTerms (esm validations/measure/measure.evl:3-7). `Length.metre^2` syntax itself is JSL. |
| C2 | ✅ TRUE | Each non-base unit converts to the base unit through `rateDividend`/`rateDivisor`; a `MeasuredType` fixes the store unit, e.g. kilograms with precision 15 and s… | `models__judo-meta-measure/model/model/measure.ecore:15-18` | Unit has rateDividend/rateDivisor; esm.ecore:512 MeasuredType has storeUnit; precision/scale come from the numeric type. |
| C3 | ✅ TRUE | The DAO converts values between transfer and entity units at scale 20 with `HALF_UP` rounding, and returns `BigInteger` for integer entity attributes. | `runtime__judo-runtime-core/judo-runtime-core-dao-core/src/main/java/hu/blackbelt/judo/runtime/core/dao/core/processors/PayloadDaoProcessor.java:56,319-328` | Conversion uses MEASURE_CONVERTING_SCALE=20, RoundingMode.HALF_UP, and returns decimal.toBigInteger() for integer entity attributes (note: query/Constants.java:39 uses scale 15 in the query layer). |
| D1 | 📐 PRACTICE | (developer statement) | `-` | "Not in use" is an adoption statement, not verifiable in code. |

Developer answer: _Not in use_

### K08 Static navigations and static data

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | A static navigation exposes a fixed collection of entities through a getter expression, with no owning instance, e.g. for reference-data lists. | `models__judo-meta-esm/model/model/esm.ecore:194-199` | StaticNavigation is a namespace element with a getterExpression of reference type and no owning instance; used in itests (ScriptTest, EnvironmentVariableTest). |
| C2 | ✅ TRUE | Static data is a model element with a single constant value from a getter expression; in `'0 // COUNT(...)'` the text after `//` is a comment, so the value is a… | `models__judo-meta-esm/model/model/esm.ecore:200-203` | StaticData has one getterExpression (DataExpression); JqlDsl.xtext:1,179 declares SL_COMMENT `//` hidden, so `0 // COUNT(...)` evaluates to 0. |
| D1 | 📐 PRACTICE | (developer statement) | `-` | "Yes" confirms the claims; nothing extra to validate. |

Developer answer: _Yes_

### K09 UI model values that break frontend generation

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | `booleanWidget: "SWITCH"` has no generator template and breaks the frontend build; use `CHECKBOX` or `COMBO`. | `runtime__judo-tatami-client/judo-tatami-esm2ui/src/main/epsilon/transformations/ui/modules/ui/dataField.etl:71` | ESM→UI maps SWITCH to a UI!Switch widget (spec boolean-switch-widget), but the React template has no Switch handling (no template/helper references outside openspec); that it "breaks the build" is not demonstrated here, only the missing template. |
| C2 | ❔ NOT FOUND | An operation whose output type equals the action container's view root type makes the generator reference a non-existent `*OutputView` dialog, breaking the Type… | `runtime__judo-tatami-client/judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/zeta/transformations/ui/OperationFormOutputTransformations.java:203` | Output-view dialogs are produced by the transformation, but no `*OutputView` reference in React/TS generators and no evidence of the output-type == view-root-type failure. |
| C3 | ⚠️ PARTLY | Self-referential relation pages lose `targetPageDefinition` in the ESM→UI transformation, causing an NPE in the React generator; `UiValidationException: All con… | `models__judo-meta-ui/model/src/main/java/hu/blackbelt/judo/meta/ui/runtime/UiValidator.java:13-14` | The message "All constraints have been satisfied" is printed when the validator throws with no errors/warnings (known quirk, openspec add-zeta-transformation tasks.md:524); the self-referential NPE/lost targetPageDefinition is not confirmed (Esm2UiZetaTransformation.java:380-394 has fixups for targetPageDefinition but no self-reference case). |
| D1 | ✅ TRUE | (developer statement) | `template__judo-ui-react-template/judo-ui-react/src/main/java/hu/blackbelt/judo/ui/generator/react/UiWidgetHelper.java:1` | Switch is not supported by the React generator (no Switch template found); developer confirms. |
| D2 | ❔ NOT FOUND | (developer statement) | `-` | Developer says to check; no evidence either way. |
| D3 | ❔ NOT FOUND | (developer statement) | `-` | Developer says to check; no evidence either way. |

Developer answer: _Yes it is not supported yet / We should check this problem 2. / We should check this problem 3._

### K10 UI-model presentation attributes

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | A Group with null or DEFAULT layout inherits the nearest ancestor Group layout, defaulting to HORIZONTAL; `applicationColumns` sets the grid width, default 12. | `runtime__judo-tatami-client/judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/zeta/transformations/ui/GroupTransformations.java:338-360` | DEFAULT/null layout inherits the nearest Group ancestor layout, else HORIZONTAL; applicationColumns defaults to 12 (Esm2Ui.java:84, Esm2UiWork.java:52). |
| C2 | ⚠️ PARTLY | Tables expose `tableRepresentation`, `isSmallTable`, `isExportable` and `additionalMaskAttributes`; `isInlineEditable` equals the relation's `isEager`, so only … | `models__judo-meta-ui/model/model/ui.ecore:186,207,218-220` | UI table has isSmallTable, additionalMaskAttributes, isInlineEditable, tableRepresentation (TableRepresentation enum, line 776); ESM has exportable (esm.ecore:191); but `isInlineEditable = isEager` exists only in the JSL transformation (jsl2ui viewTableDeclaration.etl:18); in ESM it is an independent table attribute (esm.ecore:877) copied by esm2ui (tabularReferenceFieldTable.etl:30). |
| C3 | ⚠️ PARTLY | A link representation column needs a string-typed field on the target transfer object; a string <u>field</u> with the predictive modifier becomes a type-ahead `… | `runtime__judo-tatami-client/judo-tatami-esm2ui/src/main/epsilon/transformations/ui/modules/ui/dataField.etl:215-225` | A string field becomes a UI TextInput (StringTypeTextInput) and relation links have autocomplete actions (Esm2UiConstraintNames.java:313-314); no "predictive" modifier or link-string validation exists outside JSL, so those details are not confirmed. |
| D1 | ✅ TRUE | (developer statement) | `runtime__judo-tatami-client/judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/Esm2Ui.java:84` | Default applicationColumns is 12. |
| D2 | ⚠️ PARTLY | (developer statement) | `runtime__judo-tatami-client/judo-tatami-esm2ui/src/main/epsilon/transformations/ui/modules/ui/tabularReferenceFieldTable.etl:75` | Small table flag is handled (TabularReferenceFieldTableTransformations.java:195); the validation limiting small tables is commented out (ui validations/table.evl:15-21); "gets all items without pagination" and "only eager" are not verified in ESM code (the eager rule is JSL-only, viewTableDeclaration.etl:18 "currently the runtime only supports inline edit for eager tables"). |
| D3 | ❔ NOT FOUND | (developer statement) | `-` | No ESM code/validation found for link representation type rules; derived string attribute as autocomplete label is design advice. |

Developer answer: _i think its true, default is 12 / Yes, check what does small table do, isInlineEditable now only works on isEager BUT its a fragile feature. Small table is used not frequntly, it can be useful when we know there wull be a few listed item only, becouse its get all if the list items without pagination. / For link no, for table based single relation association or aggregations yes, for example it will be used for autocomplitions and typahead AND in can be derived string type attribute, we usually combine more then one attribute to idnetify the element correctly. Like Kiss and Joska will become Ki_

### K11 Frontend customization extension points

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | `src/extra-routes.tsx` exports `extraRoutes` (`path`, `element`, `exact?`), which the generated routes prepend to the generated ones. | `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/src/routes.tsx.hbs:11` | `extraRoutes` (typed `{path, element, exact?}[]`, extra-routes.tsx.hbs:5) seeds the `routes` array before the generated routes are added. |
| C2 | ✅ TRUE | The menu-actions hook registers under objectClass `MENU_ACTIONS_HOOK`, without the `Hook` suffix every other hook key uses. | `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/src/layout/Drawer/DrawerContent/Navigation/menuCustomization.ts.hbs:6` | `MENU_ACTIONS_HOOK_INTERFACE_KEY = 'MENU_ACTIONS_HOOK'`; the other keys end in Hook (`'RedirectServiceHook'` Redirect.tsx.hbs:11, `'SubThemeHook'` SubThemeWrapper.tsx.hbs:7). |
| C3 | ✅ TRUE | `useFaultDialog()` returns `(faultObjectKey, payload) => void`, opening a dialog that renders a business-fault payload as translated key/value pairs. | `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/src/components/dialog/OperationFaultDialog.tsx.hbs:16` | `useFaultDialog()` returns `(faultObjectKey: string, payload: any)` that opens a dialog listing `t('faults.<key>.<field>')`: value for each payload entry (lines 62-67). |
| D1 | 📐 PRACTICE | (developer statement) | `-` | Asking for a catalogue of hooks is a documentation request, not a platform fact. |
| D2 | ✅ TRUE | (developer statement) | `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/src/utilities/error-handling.ts.hbs:75` | The default error handling calls `useFaultDialog()`; the custom interceptor template (custom/default-error-handler-interceptor.ts.hbs:28-35) shows replacing it with `showErrorSnack` (toast). |

Developer answer: _Yes / Make sure this will be documneted, u should make a cataloge form the hooks / Yes this is the default behavoure, but i overwrote it to use a toast snackbar error for it._

### K12 MUI X Pro/Premium license configuration (React)

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | The `muiLicensePlan` generator property (`community`, `pro`, `premium`) drives template branches such as pinned action columns in tables. | `template__judo-ui-react-template/judo-ui-react/src/main/java/hu/blackbelt/judo/ui/generator/react/ReactStoredVariableHelper.java:66` | `muiLicensePlan` (community/pro/premium) is read and drives branches, but the pinned actions column in EagerTable.tsx.hbs:503 / LazyTable.tsx.hbs:660 is under `isMUILicensePlanPro`, which is true only for `pro` (line 61), not `premium`; the pickers use a `-pro` suffix for pro and premium (line 110). |
| C2 | ✅ TRUE | The generated frontend reads the license key from `VITE_MUI_LICENSE_KEY` at build time and calls `LicenseInfo.setLicenseKey`. | `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/src/main.tsx.hbs:37` | When a plan is set (`isMUILicensed`), `LicenseInfo.setLicenseKey(import.meta.env.VITE_MUI_LICENSE_KEY)` runs; `VITE_MUI_LICENSE_KEY` is declared in vite-env.d.ts.hbs:5 and README.md.hbs:70. It is a Vite build-time env var. |

Developer answer: _Yes_

### K13 Long-running operations return 503 in the frontend

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ❔ NOT FOUND | The React frontend service layer drops operation calls that run longer than about 30 seconds with HTTP 503, even when the backend completes and responds. The ti… | `template__judo-psm-generator-jaxrs/judo-psm-generator-jaxrs-impl/src/main/resources/rest/impl/rest.service.impl.java.hbs:22` | No timeout (30 s or otherwise) in the axios provider or services of the React or TypeScript REST templates. The only generated 503 is a backend `SERVICE_UNAVAILABLE` when the dispatcher service is not bound (lines 22-23). A 503 after about 30 s would have to come from a proxy or gateway outside the generated code. |

Developer answer: _Yes_

### K14 Generated DAO null handling, enum query bug

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | `set<Relation>(obj, null)` throws NPE because it calls `identifier()` unchecked; use `unset<Relation>(obj)` to clear. `add<Relation>`/`remove<Relation>` also fa… | `template__judo-psm-generator-sdk-core/judo-psm-generator-sdk-core-impl/src/main/resources/dao/impl/fragment.dao.single.relation.implementation.mapped.java.hbs:193` | `set<Relation>` calls `relatedObject.identifier()` with no null check (NPE); `unset<Relation>` (line 201) calls `dao.unsetReference`. `add`/`remove` map every list element with `relatedObject.identifier()` (fragment.dao.multi.relation.implementation.java.hbs:79) and fail on null elements. |
| C2 | ✅ TRUE | Typed `BooleanFilter` has only `isTrue()`/`isFalse()`; query "no value" with raw JQL, e.g. `filterBy("this.approved!isUndefined()")`. Required attributes get pl… | `runtime__judo-sdk-common/src/main/java/hu/blackbelt/judo/sdk/query/BooleanFilter.java:32` | Only `isTrue()` and `isFalse()` factories exist; the query builder has a raw `filterBy(String)` (fragment.querycustomizer.builder.java.hbs:45). Attribute getters are `Optional<T>` only for optional attributes (JavaApiHelper.java:353-358 `attributeTargetTypeDefinition`). |
| C3 | ✅ TRUE | `query<Attribute>()` on an enumeration attribute throws `ClassCastException`: it casts the stored ordinal `Integer` to the enum. Read via the DTO getter or `<En… | `template__judo-psm-generator-sdk-core/judo-psm-generator-sdk-core-impl/src/main/resources/dao/impl/fragment.dao.query.attribute.implementation.mapped.java.hbs:13` | `query<Attr>` does `(<Type>) r.get("name")`, where the type is the enum FQ name for enumeration attributes (JavaApiHelper.java:287). Payload enums are ordinals, so this cast fails with ClassCastException (inferred from the cast; not run). The enum class offers `getByOrdinal(Integer)` (sdk-core-api enum.java.hbs:28). |
| D1 | ✅ TRUE | (developer statement) | `template__judo-psm-generator-sdk-core/judo-psm-generator-sdk-core-impl/src/main/resources/dao/impl/fragment.dao.single.relation.implementation.mapped.java.hbs:201` | `unset<Relation>(object)` exists and takes no related object, so it is the way to clear a single relation. |
| D2 | ✅ TRUE | (developer statement) | `template__judo-psm-generator-sdk-core/judo-psm-generator-sdk-core-api/src/main/resources/dao/api/fragment.querycustomizer.builder.java.hbs:45` | A string `filterBy(java.lang.String ...)` exists and takes JQL, so a custom string filter can express "no value". |
| D3 | ✅ TRUE | (developer statement) | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/backend/data-access-guide.md.hbs:472` | Fields outside the mask come back `null`; the generated getter for a required attribute returns the raw value with `.orElse(null)` (no Optional wrapper, line 13 of the query-attribute template). Required and Optional values can therefore both be null when masked out. |
| D20 | ⚠️ PARTLY | (developer statement) | `template__judo-psm-generator-sdk-core/judo-psm-generator-sdk-core-api/src/main/resources/dao/api/dto.java.hbs:261` | "Required attributes get plain getters, optional ones Optional<T>" — Not re-verified line by line. Related D2 shows the optional getter exists; a required-plain/optional-Optional split is consistent with it. (added by the coverage audit) |

Developer answer: _use the unset in this case / yes maybe for a ticket for this, but the filterBy as a custom string filter.Required attributes get plain getters, optional ones `Optional<T>`. Yes BUT u should not guard the reuwired ones with null check, an Optional and a Rewuired attribute can be null when the mask filter its out. SO Optional<Null> can be NULL in this cas this is a feature not a bug. / Yes_

### K15 Generated REST paths, headers and wire formats

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | Endpoints live under `/api/<Model>/<Actor>/` with `~`-suffixed verbs: `~create`, `~validate`, `~update`, `~delete`, `~list`, `~get`, `~range`, `~set`, `~unset`,… | `template__judo-psm-generator-jaxrs/judo-psm-generator-jaxrs-api/src/main/java/hu/blackbelt/judo/psm/generator/jaxrs/api/OperationHelper.java:116` | Paths are built as `<rel or class>/~list\|~get\|~create\|~validate\|~update\|~delete\|~set\|~unset\|~add\|~remove\|~range\|~upload-token` (lines 116-170; also `~export`, `~template`, `~principal`, `~meta`). The base is `{baseUrl}/api/{model}/{actor}` (application.config.java.hbs:15). |
| C2 | ✅ TRUE | Headers include `X-Judo-SignedIdentifier`, `X-Judo-Mask`, `X-Judo-CountRecords`, `X-Judo-RequestParameters`, `X-Judo-MarkSelectedRangeItems`; responses carry `_… | `template__judo-psm-generator-jaxrs/judo-psm-generator-jaxrs-api/src/main/resources/rest/api/rest.service.operation.fragment.hbs:68` | The five `X-Judo-*` headers are declared as `@HeaderParam`; `__signedIdentifier`, `__version`, `__updateable`, `__deleteable` are in dtoForResponse.java.hbs (lines 55-130). `X-Judo-MarkSelectedRangeItems` exists only on range operations (lines 74-77) and `X-Judo-SignedIdentifier` only on bound operations (lines 78-81). |
| C3 | ⚠️ PARTLY | Enums travel as integer ordinals, binaries as filestore tokens, `Date` parameters as `yyyy-MM-dd`; a list call without seek returns all rows. | `runtime__cxf-jaxrs-application-manager/src/main/java/hu/blackbelt/jaxrs/providers/ISO8601DateParamHandler.java:50` | Dates use `yyyy-MM-dd` (also ui-typescript-rest serialization.ts.hbs:11); enums carry an `ordinal` in the generated enum class and `~upload-token` exists for binaries. I did not find the wire-level enum-as-integer serialization or the "list without seek returns all rows" behaviour directly. |
| D1 | ⚠️ PARTLY | (developer statement) | `template__judo-psm-generator-jaxrs/judo-psm-generator-jaxrs-impl/src/main/resources/rest/impl/rest.service.impl.java.hbs:27` | The backend accepts `X-Judo-CountRecords` on every operation and counts when the header is non-blank; whether the frontend sends it only when needed was not checked. SignedIdentifier is required only on bound operations (rest.service.operation.fragment.hbs:78). |
| D2 | ✅ TRUE | (developer statement) | `template__judo-psm-generator-jaxrs/judo-psm-generator-jaxrs-impl/src/main/resources/rest/impl/rest.service.impl.java.hbs:48` | `X-Judo-MarkSelectedRangeItems` is handled only when `operation.isRangeOperation`; bulk-action use was not checked. |
| D3 | ✅ TRUE | (developer statement) | `template__judo-ui-typescript-rest-template/judo-ui-typescript-rest-api/src/main/resources/rest/serialization.ts.hbs:11` | The frontend formats dates as `yyyy-MM-dd`, and the backend parses them with `ISO8601DateParamHandler` (default `yyyy-MM-dd`). |

Developer answer: _Yes u can check the openApi generated swagger for the available api enpoint, most of them needed sigendIdnentifer which getted for signed adentiders trough accesses / Yes, but there are headers which added only for different condition like CountRecords (mode parameter), its add only if its needed for that associoation its cost in real performace, markselecteditems is used for bulk action and range calls to mark that element which already added (check it) , check how th count record came back / yes, the forntend convert the elements and the backend also_

### K16 Relation kinds, CRUD flags and generated endpoints

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | CRUD flags are declared on each relation, not on the transfer object; REST and range endpoints are generated only for relations with create, update or delete fl… | `models__judo-meta-esm/model/src/main/java/hu/blackbelt/judo/meta/esm/runtime/EsmUtils.java:2163` | With `GENERATE_CRUD_OPERATIONS_BASED_ON_FLAGS = true` (line 129), create, update, delete and get-range support is decided from `isCreateAllowed`/`isUpdateAllowed`/`isDeleteAllowed` on the relations (ReferenceTypedElement) that point at the transfer object (lines 2163, 2186, 2220, 2360). |
| C2 | ⚠️ PARTLY | An association generates generic `~add`/`~remove`/`~set` endpoints, while a composition exposes ownership operations instead; the relation kind decides where de… | `models__judo-meta-esm/model/src/main/java/hu/blackbelt/judo/meta/esm/runtime/EsmUtils.java:2281` | `~set`/`~add`/`~remove` are supported only for stored, non-composition relations and require update support (lines 2285-2347), which matches. The "composition exposes ownership operations, relation kind decides where delete lives" part is not shown: `isDeleteSupported` (line 2215) depends on delete flags and cardinality, not on the relation kind. |
| C3 | ❌ FALSE | On mapped transfer objects, entity relations with lower bound 1, compositions and derived associations become AGGREGATION; derived members appear with a `transf… | `models__judo-meta-esm/model/src/main/java/hu/blackbelt/judo/meta/esm/runtime/EsmUtils.java:3901` | `fixRelationProperties` sets AGGREGATION when the source or target is not mapped (or is transient), not for lower bound 1, compositions or derived associations. The `transfer_` prefix appears only as a test-generator constant (judo-platform-itest CRUD_Object_Attribute.java:29), not in any transformation. |
| D1 | ✅ TRUE | (developer statement) | `models__judo-meta-esm/model/src/main/java/hu/blackbelt/judo/meta/esm/runtime/EsmUtils.java:2181` | Update-type support (which gates set/add/remove) requires `isUpdateAllowed()` on a relation, so "yes if it has the update flag" holds. |

Developer answer: _Yes, yes. U can see in the openAPi definitions / Yes if it has update flag / NOOOOO, its not true_

### K17 Time zones and date/time wire format

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | `Timestamp!now()` resolves via `CurrentTimestampProvider` using `JUDO_PLATFORM_DEFAULT_ZONE_ID`, not the JVM time zone, so it can disagree with `LocalDateTime.n… | `runtime__judo-services/judo-services-dispatcher-osgi/src/main/java/hu/blackbelt/judo/services/dispatcher/osgi/component/DefaultCurrentTimestampVariableResolverComponent.java:56` | `CurrentTimestampProvider` returns `LocalDateTime.now(zoneId)` (CurrentTimestampProvider.java:41); `zoneId` comes from the `zoneId` config set from `defaultZoneId` (default `UTC`, config template DispatcherServiceActivator.template:82), and it falls back to the JVM zone only if config is null. The name `JUDO_PLATFORM_DEFAULT_ZONE_ID` appears nowhere in the sources. |
| C2 | ⚠️ PARTLY | REST serializes date-times as ISO offset strings `yyyy-MM-dd'T'HH:mm:ss.SSSXXX`, rendering a zero offset as `Z`. | `runtime__judo-runtime-core/judo-runtime-core-jackson/src/main/java/hu/blackbelt/judo/runtime/core/jackson/serializer/LocalDateTimeSerializer.java:16` | Timestamps are written with `DateTimeFormatter.ISO_OFFSET_DATE_TIME` at `ZoneOffset.UTC`, so the offset renders as `Z`. It is not the fixed pattern `yyyy-MM-dd'T'HH:mm:ss.SSSXXX`: fraction digits are variable. |
| C3 | ✅ TRUE | Incoming `OffsetDateTime` values are converted to `LocalDateTime` with `atZoneSameInstant(UTC)`, so stored values are normalized to UTC. | `runtime__judo-runtime-core/judo-runtime-core-jackson/src/main/java/hu/blackbelt/judo/runtime/core/jackson/deserializer/LocalDateTimeDeserializer.java:23` | A string that is not a plain ISO local date-time is parsed as `OffsetDateTime` and converted with `atZoneSameInstant(ZoneOffset.UTC).toLocalDateTime()`. |
| D1 | ⚠️ PARTLY | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-jackson/src/main/java/hu/blackbelt/judo/runtime/core/jackson/serializer/LocalDateTimeSerializer.java:16` | The server always emits UTC offsets, and the frontend turns strings into JS `Date` (serialization.ts.hbs:16-20), which shows in browser-local time. Browser-zone display is plausible; I did not read the frontend timestamp formatting. |
| D2 | 📐 PRACTICE | (developer statement) | `-` | Statement about a planned bug fix. |
| D3 | ✅ TRUE | (developer statement) | `documentation/docs/modules/ROOT/pages/administrator-guide/platform_parameters/07_other.adoc:22` | `defaultZoneId` sets the zone for current timestamp/date and defaults to `UTC`, so the workaround is to keep it at UTC. |
| D20 | ✅ TRUE | (developer statement) | `runtime__osgi-configuration-mapper/src/main/java/hu/blackbelt/configuration/mapper/TemplateProcessor.java:163-170` | "JUDO_PLATFORM_DEFAULT_ZONE_ID sets the default zone" — the config mapper turns JUDO_PLATFORM_<X> env vars into lowerCamel keys, so JUDO_PLATFORM_DEFAULT_ZONE_ID → defaultZoneId, which feeds zoneId (default UTC) in judo-platform-config-templates/.../DispatcherServiceActivator.template:82. (added by the coverage audit) |

Developer answer: _Yes it use it, and on forntend it will be added to the location of the browsers timezone ehich can be confussing, its a bug on the backend, which will be fixed later, not we can avoid this to set the timestamp used in UTC for now in backend and intercpeotrs if hte JUDO_PLATFORM_DEFAULT_ZONE_ID is not UTC. / Yes / Check it_

### K18 Custom JAX-RS resources and REST-only operations

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | Custom REST endpoints are OSGi Declarative Services components that are also JAX-RS root resources annotated with `@Path`, served through Apache CXF inside Kara… | `runtime__cxf-jaxrs-application-manager/README.md:552` | The documented example is an OSGi DS `@Component` with `@Path("/")`, matched by `jaxrs.resource.components=(appName=poc)`; REST runs on Apache CXF in Karaf (documentation 06_rest_customization.adoc:10-12). |
| C2 | ✅ TRUE | Custom `@Provider` classes are tracked only if the bundle manifest sets `X-JAXRS-Provider: true`; providers without `applications.filter` apply to every applica… | `runtime__cxf-jaxrs-application-manager/src/main/java/hu/blackbelt/jaxrs/SharedProviderStore.java:95` | The provider tracker reads the bundle header `X-JAXRS-Provider` (line 44, 95); a provider without `applications.filter` (read at line 108) is global and applies to every application (README.md:344, 368). |
| C3 | ⚠️ PARTLY | An operation modeled without an operation form becomes a REST-only endpoint with no web UI, e.g. for mobile clients. | `template__judo-psm-generator-jaxrs/judo-psm-generator-jaxrs-impl/src/main/resources/rest/impl/rest.service.impl.java.hbs:19` | The JAX-RS service is generated for every transfer operation (`each self.operations`), so a REST endpoint exists. "No web UI/no operation form" and "no TS function" are not confirmed: the TS service templates iterate operations from the UI model (classService.ts.hbs:61-76), and I did not find where form-less operations are filtered. |
| D1 | ❔ NOT FOUND | (developer statement) | `-` | I found no direct evidence for "REST endpoint but no TS function from react-rest-template"; see K18.C3. |

Developer answer: _Yes, / Yes? Check it / Yes its true, its get a rest endpoint, check in this case frontend not create an a ts funciton for it trough the react-rest-template._

### K19 OpenAPI spec generation and Swagger UI

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | With `generateOpenApiAnnotations=true`, the REST module annotates services and DTOs with `@Schema` and writes `openapi.json`/`openapi.yaml` to `target/api-docum… | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-application/src/main/resources/rest/pom.xml.hbs:153` | With `isGenerateOpenApiAnnotations`, swagger-maven-plugin writes `openapi.json`/`.yaml` to `target/api-documentation-swagger` (JSONANDYAML), and maven-bundle-plugin includes it in the bundle (lines 30-31). `@Schema` annotations are generated under `generateOpenApiAnnotations` (dtoForResponse.java.hbs:58). |
| C2 | ✅ TRUE | Swagger UI is served per model at `/api-spec/<model>`; the spec's `basePath` is `apiRoot` (default `/api`) + `/<model>`. | `runtime__judo-services/judo-services-swagger-ui/src/main/java/hu/blackbelt/judo/services/swagger/ui/SwaggerUIServlet.java:200` | Swagger UI is registered at `/api-spec/<model>` (SwaggerServletActivatorOpenAPIModelServiceTracker.java:41,98); `basePath = apiServletBaseUrl + "/" + model name`, with `apiRoot` default `/api` (tracker line 51). |
| C3 | ✅ TRUE | The `jaxrs-cxf-client-osgi-ds` generator produces CXF JAX-RS clients from OpenAPI specs, packaged as OSGi bundles with Declarative Services. | `tools__openapi-generator-cxf-jaxrs-client-osgi-ds/src/main/java/hu/blackbelt/openapi/codegen/JavaCXFClientOsgiDsCodegen.java:55` | The generator name is `jaxrs-cxf-client-osgi-ds`; the README says it produces CXF JAX-RS client stubs as OSGi DS bundles with an `@Component` activator. |

Developer answer: _yes, u have to use this to answer the otherproblems. / check it / check it_

### K20 GET_RANGE, GET_TEMPLATE and create-target rules

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | `GET_RANGE` is an unbound operation behaviour that supplies the options for a reference dropdown or autocomplete. | `models__judo-meta-psm/model/src/main/epsilon/validations/service/getRangeBehaviour.evl:5` | `GET_RANGE` supplies range values, but its owner may be a relation or an operation (line 5), so it is not only a standalone unbound operation. The dropdown/autocomplete purpose is not stated in the code. |
| C2 | ✅ TRUE | `GET_TEMPLATE` returns a prefilled form template; an unbound operation must own it, the owner must be a transfer object type, and it must not reference a relati… | `models__judo-meta-psm/model/src/main/epsilon/validations/service/getTemplateBehaviour.evl:7` | Validation messages: must be owned by an unbound operation (line 7), owner must be a transfer object type (line 12), relation must be undefined (line 17). This is the PSM model; ESM `isGetTemplateSupported` is EsmUtils.java:2434. |
| C3 | ✅ TRUE | A `CREATE_INSTANCE` or `VALIDATE_CREATE` target cannot map to an abstract entity and must bind every required feature of the entity, or validation fails with `A… | `models__judo-meta-psm/model/src/main/epsilon/validations/service/boundBehaviour.evl:37` | `CreateTargetIsNotAbstract` applies to CREATE_INSTANCE and VALIDATE_CREATE (guard, lines 24-30) and rejects abstract entity targets. `AllRequiredFeaturesHaveBindingIfCreatable` is the ESM rule in TransferObjectTypeValidations.java:553, which fails when required features are not bound. |
| D1 | ⚠️ PARTLY | (developer statement) | `models__judo-meta-psm/model/src/main/epsilon/validations/service/getRangeBehaviour.evl:5` | The code shows owner = relation or operation. An owner "with a signed identifier" is not checked here: bound operations get the `X-Judo-SignedIdentifier` header (rest.service.operation.fragment.hbs:78). |
| D2 | ❔ NOT FOUND | (developer statement) | `-` | I did not verify that GET_TEMPLATE is static or that it returns the input transfer objects' defaults; only the validation constraints (getTemplateBehaviour.evl) were confirmed. |
| D3 | ✅ TRUE | (developer statement) | `models__judo-meta-psm/model/src/main/epsilon/validations/service/boundBehaviour.evl:37` | `CreateTargetIsNotAbstract`: "cannot reference the mapped transfer object of an abstract entity type". |

Developer answer: _Yes its unbound but check its need an owner ehich hase a signedidnetifer / Yes its static, its add back the defaults of the renasfer obejct of the input transfers, or the trnadferobjects / Yes, abstrat entiy cannot be created_

### K21 Runtime error codes and payload validation

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | Runtime codes include `AUTHENTICATED_ENTITY_NOT_FOUND` (403), `ACCESS_DENIED_FOR_INSTANCE_OF_BOUND_OPERATION` (403), `MISSING_REQUIRED_PARAMETER` (400) and `NOT… | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultActorResolver.java:202` | AUTHENTICATED_ENTITY_NOT_FOUND and ACCESS_DENIED_FOR_INSTANCE_OF_BOUND_OPERATION (DefaultAccessManager.java:129) are thrown as AccessDeniedException (getStatusCode 403, judo-runtime-core/.../exception/AccessDeniedException.java:37); MISSING_REQUIRED_PARAMETER (DefaultDispatcher.java:541) and NOT_ACCEPTED_BY_RANGE (RangeValidator.java:107) are ValidationException (400, ValidationException.java:47). |
| C2 | ⚠️ PARTLY | Payload validation raises `MISSING_REQUIRED_ATTRIBUTE` and `MISSING_REQUIRED_RELATION` (with `__referenceId`); derived references are skipped. Errors such as `A… | `runtime__judo-runtime-core/judo-runtime-core-validator/.../DefaultPayloadValidator.java:362` | MISSING_REQUIRED_ATTRIBUTE/RELATION carry __referenceId (line 362, 330) and derived refs are skipped (lines 131-143) - true; but the identifier code string is INVALID_IDENTIFIER (Validator.java:35, only the Java constant is ERROR_INVALID_IDENTIFIER), INVALID_TOKEN is AuthenticationRequiredException (401, DefaultAccessManager.java:107), and the RequestConverter.java:282 variant of INVALID_IDENTIFIER does include a location (DefaultDispatcher.java:321 variant has none). |
| C3 | ✅ TRUE | The dispatcher rejects operations on bound instances whose signed identifier carries the `immutable` flag, throwing `AccessDeniedException`. | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultDispatcher.java:663-669` | For bound operations called via an exposed (REST) call, a signed identifier with immutable=true throws AccessDeniedException with code BOUND_OPERATION_INSTANCE_IS_IMMUTABLE (Validator.java:38); only checked when `exposed`. |
| D1 | ❔ NOT FOUND | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-validator/.../Validator.java:35` | "Check codes/identifiers" - the actual code is INVALID_IDENTIFIER (not ERROR_INVALID_IDENTIFIER); no error-code catalogue file found beyond constants in Validator.java. |
| D2 | ⚠️ PARTLY | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultIdentifierSigner.java:259-265` | Signed identifier's producing reference/type must match the TO type (hasCorrectSigner), else AccessDeniedException ACCESS_DENIED_INVALID_TYPE; so a different TO type for the same entity is rejected - but the code is ACCESS_DENIED_INVALID_TYPE / INVALID_IDENTIFIER, not literally ERROR_INVALID_IDENTIFIER. |
| D3 | ⚠️ PARTLY | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultAccessManager.java:125-131` | An instance produced by a reference/operation not exposed to the actor is rejected (ACCESS_DENIED_FOR_INSTANCE_OF_BOUND_OPERATION), and RequestConverter checks signature-vs-type; the specific "range TO cannot set a reference" case follows from the producedBy/type check but no dedicated test was found. |

Developer answer: _Yes, but check the codes and identifiers of the erros. / Yes, u can always check the response for this for more information , ERROR_INVALID_IDENTIFER can be triggerd when for example you have tow transfer object which map to the same entity and u want to use the another trnasferobject for a reference (the entity is the same, but its not the same transferobject type or could came for ma diffenrent access) / Yes for example if u use a range transferobject is cannot be used for set a reference or update it._

### K22 Custom operation implementation contract

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ❔ NOT FOUND | With `customImplementation=false` and no Java implementation, the generated body is only a `//sdk` comment; the operation runs successfully and does nothing. | `runtime__judo-runtime-core/.../DefaultDispatcherFunctionProvider (runtime__judo-platform/judo-platform-services/judo-services-dispatcher-osgi/.../DefaultDispatcherFunctionProvider.java:92-97)` | No `//sdk` literal exists in any ESM generator/runtime; non-custom operations are treated as script operations (scriptOperations) and customImplementation=true ones need an SDK/OSGi implementation (lines 108-114), consistent with the developer answer, but the exact generated body text was not found. |
| C2 | ⚠️ PARTLY | A custom operation throwing a checked `BusinessErrorException` must declare the fault explicitly in the model, otherwise the code does not compile. | `template__judo-psm-generator-sdk-core/judo-psm-generator-sdk-core-api/.../OperationHelper.java:81-83` | Generated operation interface declares `throws` only for the model's faults; generated fault exceptions are checked (`extends java.lang.Exception`, dao.fault.java.hbs:8), so undeclared faults fail to compile. But hu.blackbelt.judo.dispatcher.api.BusinessException itself is a RuntimeException (BusinessException.java:31), not checked. |
| C3 | ✅ TRUE | Operation names may not equal `get`/`set` + an attribute or relation name; `stateful` must match inherited operations of the same name, with compatible paramete… | `models__judo-meta-esm/model/src/main/epsilon/validations/operation/operation.evl:140-148,77-80` | OperationNameIsNotSetter/Getter forbid names equal (case-insensitive) to set/get+feature; StatefulFlagIsValid requires same stateful as inherited non-abstract ops; OverridingOperationWithValidParameters (line 64) checks parameter compatibility. Only get/set are enforced, not create/delete as developer suggests. |
| D1 | ⚠️ PARTLY | (developer statement) | `runtime__judo-platform/judo-platform-services/judo-services-dispatcher-osgi/.../DefaultDispatcherFunctionProvider.java:92-125` | customImplementation=true ops must be bound by an SDK service; with none the SDK-operations-ready check does not complete (activation waits, unless skipMissingSdkOperationsCheck). The "we write/overwrite the .default custom op" part is a generator workflow (empty-custom-operation-implementation-osgi.java.hbs usage text), not runtime behaviour. |
| D2 | 📐 PRACTICE | (developer statement) | `template__judo-psm-generator-sdk-core/judo-psm-generator-sdk-core-internal-wrapper/.../dto.dispatcher.wrapper.java.hbs:43-50` | Fault pattern (UnmappedTransferObject with errorCode string) is design advice; platform confirms faults are carried as errorCode/type/details (BusinessException) and mapped to generated fault exceptions. |
| D3 | ⚠️ PARTLY | (developer statement) | `models__judo-meta-esm/model/src/main/epsilon/validations/operation/operation.evl:140-148` | Only get<X>/set<X> names are rejected by validation; create/delete prefixes are not validated (advice only). |
| D20 | ⚠️ PARTLY | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/DefaultDispatcher.java:408-413` | "errorCode can be an enum or a string; string is looser" — The fault map's _errorCode (FAULT_ERROR_CODE, line 93) is cast to String, so a string works. An enum-typed errorCode is not handled in the dispatcher. The "stricter to the model" point is a modelling opinion. (added by the coverage audit) |

Developer answer: _Yes, becouse its has a jcl body with a comment. We dont use pure jcl operaiton anymore, we write or overwrite them, so even its customImplementation is false, but we write the .default custom ooperaiton or registrey it it will be overwrite it. Altough if its TRUE and no jcl body declared then the application willn ost start it will be in a state which wait the operaion form an osgi  service and only if it is written then go on. / We declare it as a UnmappedTransfer object with the attributes we want (all attribute will be siplayed or sent trought the rest as a response like ({errorCode:NOT_ALL_

### K23 Interceptor coverage and composition

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | `OperationCallInterceptor`s fire only for behaviour operations (CRUD, list, refresh, range, reference); custom and mapped operations bypass them despite the int… | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../CallInterceptorUtil.java:57 and behaviours/*Call.java (e.g. ListCall.java:71-167)` | Interceptor invocation is only inside behaviour call classes (CRUD, list, refresh, ranges, references, plus validate/template/export/principal/metadata); DefaultDispatcher custom/script/SDK path (DefaultDispatcher.java:740-800) never calls CallInterceptorUtil. |
| C2 | ⚠️ PARTLY | Range interceptors run only on `_getRangeReference*` operations; a direct `~list` call bypasses them, so `rangeType=ANY` transfer objects expose all instances. | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../OperationCallInterceptorProvider.java:37-40` | Interceptors are selected per operation (getOperations(asmModel).contains(operation) or empty=all), so range interceptors registered on range operations do not run on ~list (ListCall runs its own). rangeType=ANY exposure consequence was not verified. |
| C3 | ⚠️ PARTLY | Multiple interceptors run sequentially, each `preCall` sees peers' in-place payload mutations, and return values combine last-non-null-wins. | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../CallInterceptorUtil.java:57-75` | Interceptors run sequentially and each preCall receives the same inputParameter object (so in-place mutations are visible); but the result is `ret = o` for every interceptor INCLUDING null (last wins, a null overrides), not last-non-null-wins; async interceptors run fire-and-forget (and postCall async actually calls preCall, line 91). |
| D1 | ⚠️ PARTLY | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultDispatcher.java:740-800` | Developer's doubt is right for custom operations: behaviour operations are intercepted, custom ones are not (see K23.C1). |
| D2 | ✅ TRUE | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../CallInterceptorUtil.java:57-75` | Confirms C2/C3 mechanics for sequential invocation and shared payload (see C3 caveat on null). |
| D3 | ✅ TRUE | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../CallInterceptorUtil.java:57-75` | Same as D2. |

Developer answer: _are you sure about that check the intercpetors  catch the operaitons? ITs not a big problem if not beouse we could doanything in the cutstom operation / yes / yes_

### K24 JCL operation-body language

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Operation bodies are JCL scripts with variables, if/for/while/return, `new`/`delete`/`unset`, reference `+=`/`-=` and subtype spawning via `x as Type`; `customI… | `models__judo-meta-jcl/model/src/main/java/hu/blackbelt/judo/meta/jcl/JclDsl.xtext:59-103` | Grammar has var, if, for, while, return, unset, delete, new, `+=`/`-=`; spawn exists in script builder (models__judo-meta-script SpawnOperation per builder-jcl spec); `customImplementation=true` => body not JCL (DefaultDispatcherFunctionProvider.java:94). JCL is deprecated per developer. |
| C2 | ⚠️ PARTLY | The `ScriptValid` constraint fails the model build on invalid JCL for every non-custom operation. | `eclipse__judo-jcl-ide-eclipse/sirius/src/main/epsilon/validations/esmjcl.evl:3-14` | ScriptValid exists with guard `not self.customImplementation`, but lives in the Eclipse/Sirius designer validation (esmjcl.evl), not in the ESM model-build validations. |
| C3 | ⚠️ PARTLY | `immutable` creates a detached copy and requires `var immutable <Type>`; `principal` and `iscurrentactor` give scripts access to the authenticated actor. | `models__judo-meta-jcl/model/src/main/java/hu/blackbelt/judo/meta/jcl/JclDsl.xtext:59,95 ; models__judo-meta-script/builder-jcl/.../JclScriptBuilder.java:125-131` | `var immutable <Type>` and `new immutable` exist and `principal`/`iscurrentactor` functions are registered; "detached copy" and "requires var immutable" semantics not verified. |
| D1 | 📐 PRACTICE | (developer statement) | `-` | Developer says JCL is outdated/deprecated; tag claims K24 as JCL, deprecated (the JCL grammar/ScriptValid code is still present). |
| D20 | 📐 PRACTICE | (developer statement) | `-` | "OUTDATED, we don't use, tag it for JCL and Deprecated" — Project status and tagging advice. Code cannot confirm it. (added by the coverage audit) |

Developer answer: _OUTDATED we dont use, tag it for JCL and Depricated_

### K25 Request exchange-id tracing

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | The `ExchangeIdDecorator` CXF interceptor assigns a UUID to each request, stores it on the Exchange as `exchangeId` and puts it in the SLF4J MDC as `RequestExch… | `runtime__judo-runtime-core/judo-runtime-core-jaxrs-cxf/.../ExchangeIdDecorator.java:36-60` | Phase.RECEIVE interceptor creates UUID, stores under exchange key "exchangeId", puts "RequestExchangeId" in MDC; ExchangeIdResponseWriter.java:38 writes header X-Exchange-Id on the response. |
| D1 | ✅ TRUE | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-jaxrs-cxf/.../ExchangeIdDecorator.java:36-60` | Verified (see C1). |

Developer answer: _Check it but it is okay_

### K26 Authorizing non-principal SYSTEM actors

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | A bound operation such as `Order.delete` lives on the mapped transfer object; its guard checks `exposedBy` on the producing transfer object, not the access gett… | `runtime__judo-runtime-core/judo-runtime-core-accessmanager/.../DefaultAccessManager.java:99,125-127` | Operation guard checks `exposedBy` extension annotation on the operation, and for bound instances on the signedIdentifier's producedBy element; CRUD flags are not consulted there. |
| C2 | 📐 PRACTICE | A restricted actor needs a new transfer object when the candidate's operation closure (own operations plus those reachable via relations) contains any mutating … | `-` | Design advice about when to create a new TO for an actor; platform code only enforces exposedBy (DefaultAccessManager.java:99); no "operation closure" computation found. |
| C3 | ⚠️ PARTLY | A SYSTEM actor without a principal uses realm `DEFAULT`, has no menu items and no principal. | `models__judo-meta-esm/model/src/main/epsilon/validations/accesspoint/actorType.evl:15-19` | A realm is required for any non-anonymous actor and anonymous (no realm) actors skip realm (ActorRules.java:115 sets realm only if not anonymous); no "DEFAULT" realm constant was found, and menu-item absence not verified. Principal is optional (hasPrincipal) so no-principal actors exist. |
| D1 | ✅ TRUE | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-accessmanager/.../DefaultAccessManager.java:99,125` | Guard via exposedBy confirmed. |
| D2 | 📐 PRACTICE | (developer statement) | `-` | Security advice (protect public endpoint); no code claim. |
| D3 | ❔ NOT FOUND | (developer statement) | `-` | Developer "I think yes" about SYSTEM actor realm/menu/principal; no DEFAULT realm found. |

Developer answer: _Yes / For guard yes. but we should protect his endpoint carfully becouse it can be used for anyone. / i thin yes_

### K27 Principal-to-actor resolution and multi-client Keycloak

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | `DefaultActorResolver.getActorByClaims` looks up the actor by the USERNAME-claim attribute, then EMAIL-claim, then the first identifier attribute; this DB looku… | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultActorResolver.java:117-146` | Order is USERNAME claim, then EMAIL claim, then first identifier attribute among claims (sorted by name) - true; the DB lookup (dao.search limit 1, line ~180) runs per request when checkMappedActors and no actor is already in the exchange (lines 100-104), only for mapped actors. |
| C2 | ✅ TRUE | The token `azp` maps to an actor by replacing `-` with `.`; clients whose names do not match an actor FQN must be listed in `JUDO_PLATFORM_ACCEPTABLE_CLIENTS`. | `runtime__judo-runtime-core/judo-runtime-core-security-keycloak-cxf/.../KeycloakLoginInterceptor.java:206-216` | Client name (azp, KeycloakSecurityContext.java:36) has `-` replaced by `.` and used as actor FQN unless in clientToActorMap built from acceptableClients (AcceptableClientsParser.java:53); env var JUDO_PLATFORM_ACCEPTABLE_CLIENTS in documentation/.../04_security.adoc:225. |
| C3 | ⚠️ PARTLY | `KeycloakRealmSynchronizer` provisions realms, clients and users from the model at injector creation; system actors default to `CONFIDENTIAL`, HUMAN actors to `… | `runtime__judo-runtime-core/judo-runtime-core-guice-keycloak/.../KeycloakRealmSynchronizerProvider.java:33,38 ; KeycloakRealmSynchronizer.java:105,184-203` | Realms/clients/users are synced via synchronizeAllRealms() called in the provider (line 113) at injector creation - true; but defaults are reversed: HUMAN actors default to CONFIDENTIAL and SYSTEM actors to BEARER_ONLY (JudoKeycloakModuleConfiguration.java:35,38). (The synchronizer class field initialisers say the opposite but are overridden by the provider.) |
| D1 | ✅ TRUE | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultActorResolver.java:129-135` | Falls back to a mapped identifier attribute; ESM validation AtLeastOneClaimAttributeIsIdentifier (actorType.evl:3-6) requires an identifier claim; email/username claims preferred. |
| D2 | ✅ TRUE | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-security-keycloak-cxf/.../KeycloakLoginInterceptor.java:206-210` | Acceptable clients map to an actor so extra clients (not named as the actor) can authenticate as it. |
| D3 | ⚠️ PARTLY | (developer statement) | `see K27.C3` | "yes" is wrong for default access types (HUMAN=CONFIDENTIAL, SYSTEM=BEARER_ONLY in guice config). |

Developer answer: _yes, its idnetify the user in the database it has to be a attribute which is idnetifier true, we use the amil mainly / yes the accpeted client map to a actor, we use it for settings the client differently then the web client / yes_

### K28 Signed identifier lifecycle and secret

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | A signed identifier is a JWS with claims `ver`, `immutable` and issuer (the producing reference or operation FQN); it changes on every update, so clients re-que… | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultIdentifierSigner.java:294-312` | JWS claims: sub=id, iat, entity type, `ver` (only if entity has a version), `immutable` (only if true), issuer=reference or operation FQN; the version changes on update so re-query is needed, but `ver` and `immutable` are conditional and sub/entity claims also exist. |
| C2 | ✅ TRUE | Identifiers stay stable across restarts only with a configured `@IdentifierSignerSecret` binding (Base64). | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultIdentifierSigner.java:156-175` | Configured secret is Base64-decoded HMAC key; otherwise a random key is generated on each start, so identifiers do not survive restart. Bound via @IdentifierSignerSecret (DefaultIdentifierSignerProvider.java:47). (EC/public-key configuration is an alternative, lines 118-139.) |
| C3 | ⚠️ PARTLY | Signed identifiers are minted only while serving a REST response; no public mint API exists. Updates are rejected when the instance was reached through a non-up… | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultDispatcher.java:434-439` | Signing happens in DefaultDispatcher.processResponse for every dispatch result (not only REST), and IdentifierSigner.signIdentifiers is a public interface method (IdentifierSigner.java:34), so it's not REST-only. `__updateable` is derived from permissions (DefaultIdentifierSigner.java:192-205); the explicit rejection of updates through non-updatable access was not located. |
| D1 | ❔ NOT FOUND | (developer statement) | `-` | "check them" - no checkable factual statement. |
| D2 | ✅ TRUE | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/.../DefaultIdentifierSigner.java:156-175` | "Yes but check" about secret: confirmed behaviour for C2. |
| D3 | ❔ NOT FOUND | (developer statement) | `-` | "check it" - no factual statement. |

Developer answer: _check them / yes but check it / check it_

### K29 Frontend OIDC metadata, logout and guest access

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | Each actor with a realm gets a `_metadata` operation (`GET /api/<Model>/Actor/<Actor>/~meta`) returning OIDC client data such as `tokenEndpoint`, `clientId` and… | `template__judo-psm-generator-jaxrs/judo-psm-generator-jaxrs-api/.../OperationHelper.java:166-167 ; runtime__judo-runtime-core/.../behaviours/GetMetadataCall.java:70-96` | `_metadata` unbound operation on actor (OperationRules.java:96, guard shouldGenerateBehaviours) is exposed at <ActorFq>/~meta and returns security entries (name, openIdConfigurationUrl, clientId, issuer, authEndpoint, tokenEndpoint, logoutEndpoint) only when the actor has a realm. Note: generated for every actor, but security list is empty without realm. |
| C2 | ⚠️ PARTLY | Actors with a principal also expose `~principal`, returning the authenticated principal with `__identifier`/`__signedIdentifier`. | `runtime__judo-tatami/judo-tatami-esm2psm/.../rules/OperationRules.java:3172-3181 ; OperationHelper.java:165` | `_principal` at <Actor>/~principal is generated only when the actor has a principal; response carries the principal payload (signed identifier signing in DefaultDispatcher) - `__identifier` specifics not checked. |
| C3 | ✅ TRUE | Logout calls `signoutRedirect` back to the current URL without its hash; with `supportGuestAccess`, unauthenticated users see an overridable guest page instead … | `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/src/auth/AuthErrorBox.tsx.hbs:19-23 ; auth/Auth.tsx.hbs:7-70` | Logout calls signoutRedirect with post_logout_redirect_uri = href.split('#')[0] (also in DrawerProfile, ProfilePopup, BottomProfile); with supportGuestAccess no auto signinRedirect and an unauthenticated user gets a GuestPage ComponentProxy (overridable via OSGi-like registry), else "Unable to log in"/auto sign-in. (Note: with guest access off the page auto-redirects to login.) |
| D1 | ❔ NOT FOUND | (developer statement) | `-` | "check it" - no factual statement. |
| D2 | ✅ TRUE | (developer statement) | `template__judo-ui-typescript-rest-template/judo-ui-typescript-rest-axios/src/main/resources/data-axios/accessServiceImpl.ts.hbs:19` | ~principal is called by the frontend to fetch the principal (with signed identifier). |
| D3 | ❔ NOT FOUND | (developer statement) | `-` | "yes" to C3; see C3 verdict. |

Developer answer: _check it / yes its the starting point for a user to get  asignedIDNentifer / yes_

### K30 Customizing the Keycloak login theme

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | The generated project includes a Keycloak theme module (`<model>-theme`, a zip of `src/main/resources/themes`) with FreeMarker pages such as `login.ftl`, `regis… | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-application/src/main/resources/keycloak-theme/pom.xml.hbs:11 ; src/assembly/assembly.xml.hbs:5-15` | Module artifactId is `<model>-keycloak-theme` (not `-theme`), assembled as zip of src/main/resources/themes; includes login.ftl, register.ftl, error.ftl, template.ftl (also footer.ftl); generated only when #shouldGenerateKeycloakTheme() (StoredVariableHelper.java:82). |
| C2 | ✅ TRUE | The theme extends the stock theme through `parent=base` and `import=common/keycloak` in `theme.properties`. Login features such as remember-me and forgot-passwo… | `template__judo-esm-fullstack-project-template/.../keycloak-theme/src/main/resources/themes/keycloak-theme/login/theme.properties.hbs:1-2 ; login.ftl.hbs:44,57` | theme.properties has parent=base and import=common/keycloak; login.ftl wraps remember-me in `<#if realm.rememberMe ...>` and forgot-password in `<#if realm.resetPasswordAllowed>`. |
| D1 | 📐 PRACTICE | (developer statement) | `-` | Deployment advice (custom Keycloak image with themes); the template provides the theme zip and a docker-compose test setup (keycloak-theme/docker-compose.yml.hbs). |

Developer answer: _yes we can change the theme, in another projects we create custom keycloak image with megiclink and we put the themes to that custom image._

### K31 Backend CORS filter configuration

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Each model gets a CXF CORS filter configured by OSGi keys: `cors_allowOrigin` (default `*`, comma-separated), `cors_allowCredentials` (default `true`), `cors_al… | `runtime__judo-platform/judo-platform-services/judo-services-security-cxf-osgi/src/main/java/hu/blackbelt/judo/services/security/cxf/osgi/CxfSecurityActivator.java:61-82,150-160` | Keys cors_allowOrigin (default "*"), cors_allowCredentials (true), allowHeaders, exposeHeaders, maxAge, etc. exist and one CrossOriginResourceSharingFilter is registered per model (application.filter judo.model.name); allowOrigin is comma-split. Caveat: with "*" setAllowOrigins is not called (CXF default), and the filter's settings are applied only when a config object is present. |
| D1 | 📐 PRACTICE | (developer statement) | `runtime__judo-platform/judo-platform-services/judo-services-security-cxf-osgi/src/main/java/hu/blackbelt/judo/services/security/cxf/osgi/CxfSecurityActivator.java:61-64` | Defaults are "*" and credentials=true (matches "for default yes"); setting restrictive origins in production is advice, the code only offers the keys. |

Developer answer: _FOr defautl yes, on prod i think we should set this attributes_

### K32 Two-phase token flow for binary upload

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | A create-capable transfer field mapping a binary type gets a `getUploadTokenFor<Field>` operation returning `UploadToken` (one required `token` string, max 2048… | `runtime__judo-tatami/judo-tatami-esm2psm/src/main/java/hu/blackbelt/judo/tatami/esm2psm/zeta/rules/OperationRules.java:3498-3501; runtime__judo-tatami/judo-tatami-esm2psm/src/main/java/hu/blackbelt/judo/tatami/esm2psm/zeta/rules/TypeRules.java:985-1000; models__judo-meta-esm/model/src/main/java/hu/blackbelt/judo/meta/esm/runtime/EsmUtils.java:2245-2262` | Operation is named "_getUploadTokenFor"+Capitalized field (leading underscore) for BinaryType members when update is supported or a create-capable reference reaches the type; returns `_UploadToken` with one required `token` string. Max length is the configurable stringMaxLength (default 65536, PsmWorkflowProcessConfiguration.java:72), not 2048; no 2048 found. |
| C2 | ✅ TRUE | Upload first POSTs `<attributePath>/~upload-token` for a JWT, then POSTs multipart data to the filestore servlet with header `X-Token`; tokens expire after 1440… | `template__judo-ui-typescript-rest-template/judo-ui-typescript-rest-axios/src/main/resources/data-axios/accessServiceImpl.ts.hbs:34-44; template__judo-psm-generator-jaxrs/judo-psm-generator-jaxrs-api/src/main/java/hu/blackbelt/judo/psm/generator/jaxrs/api/OperationHelper.java:168-170; runtime__osgi-filestore/filestore-security/src/main/java/hu/blackbelt/osgi/filestore/security/TokenServiceConfig.java:40-43; runtime__osgi-filestore/filestore-servlet/src/main/java/hu/blackbelt/osgi/filestore/servlet/Constants.java:86` | uploadFile POSTs `<attributePath>/~upload-token`, then multipart-POSTs to the upload file path; header X-Token; expirationTime default 1440 (minutes), allowedClockSkew default 60. |
| C3 | ✅ TRUE | `RdbmsFileStoreService.put(InputStream, …)` records size from `in.available()` without buffering, so non-buffered streams can store a wrong BLOB size. | `runtime__osgi-filestore/filestore-rdbms/src/main/java/hu/blackbelt/osgi/filestore/rdbms/helper/FileEntity.java:52-58` | FileEntity constructor sets `this.size = data.available()` on the given InputStream (put() passes it straight through, RdbmsFileStoreService.java:128-129); available() is only an estimate for non-buffered streams. |
| D1 | ⚠️ PARTLY | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/converters/FileTypeFormatter.java:36-60` | The file is uploaded to the filestore first and the entity stores only a reference, but it holds four values as JSON: id, fileName, size and mimeType (not three). |
| D2 | ✅ TRUE | (developer statement) | `runtime__osgi-filestore/filestore-rdbms/src/main/java/hu/blackbelt/osgi/filestore/rdbms/helper/FileEntity.java:58` | "yes" confirms C3 (available()-based size); consistent with the code. |
| D3 | ✅ TRUE | (developer statement) | `runtime__osgi-filestore/AGENTS.md:1` | Modules filestore-rdbms, filestore-filesystem and filestore-s3 exist (directory listing of runtime__osgi-filestore); S3FileStoreService.java is the S3 backend. |

Developer answer: _yes, first we upload it to the filestore and we only renfenrce three paramet in the db the silestore id. name, and type if im right. / yes / FIlestore has 3 mode now rdmsfilestore, filesystem, s3_

### K33 Filestore on S3-compatible storage and GCS

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | `FileStoreService` has filesystem, RDBMS and S3 backends; select S3 with `JUDO_PLATFORM_FILESTORE=s3` plus `JUDO_PLATFORM_S3_BUCKET`, `JUDO_PLATFORM_S3_ENDPOINT… | `runtime__osgi-filestore/filestore-s3/src/main/java/hu/blackbelt/osgi/filestore/s3/S3FileStoreService.java:38-55; template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/application-config.md.hbs:235-250` | Three backends exist (rdbms, filesystem, s3) and JUDO_PLATFORM_FILESTORE selects them. But the documented bucket variable is JUDO_PLATFORM_FILESTORE_S3_BUCKET, not JUDO_PLATFORM_S3_BUCKET; the S3 config keys are bucketName/endpoint/region/accessKey/secretKey; no JUDO_PLATFORM_S3_ENDPOINT/_REGION wiring found in this checkout. |
| C2 | ⚠️ PARTLY | The configuration mapper strips the `JUDO_PLATFORM_` prefix and converts UPPER_SNAKE_CASE env names to lowerCamelCase config keys. | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/application-config.md.hbs:76-96` | Documented rule: strip JUDO_PLATFORM_ prefix, SNAKE_CASE -> camelCase (JUDO_PLATFORM_RDBMS_DIALECT -> rdbmsDialect). The mapper implementation itself is not in the checkout, so only the documentation confirms it. |
| C3 | ✅ TRUE | Google Cloud Storage works through its S3-compatible API: point the S3 endpoint at `https://storage.googleapis.com` and use HMAC credentials; no GCS-specific co… | `runtime__osgi-filestore/docs/gcs/setup.md:6,20` | GCS is used as ordinary S3 config with endpoint https://storage.googleapis.com and an HMAC key (accessKey/secretKey); no GCS-specific backend (S3FileStoreService only has generic multipart/header workarounds, lines 189-190). |
| D1 | ✅ TRUE | (developer statement) | `runtime__osgi-filestore/filestore-s3/src/main/java/hu/blackbelt/osgi/filestore/s3/S3FileStoreService.java:38-55` | Confirms the S3 variables/keys are supported (with the naming caveat noted under C1). |
| D2 | ⚠️ PARTLY | (developer statement) | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/application-config.md.hbs:76-96` | Conversion rule is documented as stated but its code is not in the checkout. |
| D3 | 📐 PRACTICE | (developer statement) | `runtime__osgi-filestore/docs/gcs/assessment.md:1` | Which S3 provider is in use is a deployment choice; code supports generic S3 and has a GCS interop test (docs/gcs). |

Developer answer: _yes / yes / we support many S3 solution but we use now google_

### K34 Schema migration manual steps and version checks

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ❌ FALSE | Adding a stored attribute to an entity needs no manual migration step; the generated Liquibase changelog already contains the new column. | `runtime__judo-services/judo-services-persistence/src/main/java/hu/blackbelt/judo/services/persistence/LiquibaseModelDataSourcePrehook.java:166-185` | The generated changelog contains the column for a fresh DB, but with an existing DB the prehook throws "There are RDBMS model changes which have not been applied to database"; incremental migration (generate steps, review, execute) is needed. |
| C2 | ✅ TRUE | Incremental migration produces eight changeset phases (check, backup, before/after incremental, data updates, dropBackup); review-required changes get `.sql.mis… | `runtime__judo-rdbms-schema/judo-rdbms-schema-incremental/src/main/java/hu/blackbelt/judo/rdbms/schema/incremental/RdbmsIncrementalGenerator.java:76-84,373` | ExecutionPhase enum has 8 phases (check, backup, beforeIncremental, updateDataBeforeIncremental, incremental, updateDataAfterIncremental, aferIncremental [sic], dropBackup); missing scripts are written as `<name>.missing`, and IncrementalLiquibaseExecutor.java:239-247 throws IllegalStateException while any are missing; docs (04_schema_migration.adoc:101-105) say rename to .sql. |
| C3 | ⚠️ PARTLY | At startup `LiquibaseModelDataSourcePrehook` migrates or checks the model version in `JUDO_MODEL_VERSIONS` against the database; `ignoreVersionCheck` disables t… | `runtime__judo-services/judo-services-persistence/src/main/java/hu/blackbelt/judo/services/persistence/LiquibaseModelDataSourcePrehook.java:126-185` | JUDO_MODEL_VERSIONS is the model-store table. No stored version -> runs the full Liquibase model and records it; otherwise it only CHECKS that the stored RDBMS model is identical and throws if not (no migration at startup). ignoreVersionCheck=true skips the model-store/check entirely and just executes the Liquibase model (line 129-132), not merely "disables the check". |
| D1 | ⚠️ PARTLY | (developer statement) | `runtime__judo-rdbms-schema/judo-rdbms-schema-incremental/src/main/java/hu/blackbelt/judo/rdbms/schema/incremental/IncrementalLiquibaseExecutor.java:157-247` | Steps generate Liquibase SQL for review with data-update phases that can be edited, then executed; "never use apply" is advice (PRACTICE). The "production yes, can be triggered manually locally" part is not checkable in code, and per K34.C1 a manual migration step is needed whenever the model changes. |
| D2 | ✅ TRUE | (developer statement) | `runtime__judo-rdbms-schema/judo-rdbms-schema-incremental/src/main/java/hu/blackbelt/judo/rdbms/schema/incremental/IncrementalLiquibaseExecutor.java:239-247` | `.missing` files must be written as `.sql`; execution fails with "Missing scripts" otherwise. |
| D3 | 📐 PRACTICE | (developer statement) | `runtime__judo-services/judo-services-persistence/src/main/java/hu/blackbelt/judo/services/persistence/LiquibaseModelDataSourcePrehook.java:129` | Advice not to set ignoreVersionCheck; the code does provide the flag, which skips version storage and checking. |

Developer answer: _on produciotn yes, but we coukld trigger we manualy if we want in locally, steps generate it will produce the liqibase sql for schema migration and we could add the chnages for data manipulations, then execute, never use apply which make the change without question / yes. missing is has to be write to .sql / yes, we should never ignoreTheCheck_

### K35 Generated database schema naming and columns

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Table names are UPPER_SNAKE and column names lower_snake; names are abbreviated deterministically to dialect length limits (default 62/58, Oracle 30/30). | `runtime__judo-tatami-base/judo-tatami-asm2rdbms/src/main/java/hu/blackbelt/judo/tatami/asm2rdbms/zeta/Asm2RdbmsHelper.java:274-308; runtime__judo-tatami-base/judo-tatami-asm2rdbms/src/main/java/hu/blackbelt/judo/tatami/asm2rdbms/zeta/Asm2RdbmsZetaTransformation.java:119-121` | Limits right: default 62/58, Oracle 30/30, abbreviated deterministically. But table AND column sqlNames are built with `.toUpperCase()` (tablePrefix/columnPrefix + abbreviate(...).toUpperCase()), so columns are UPPER_SNAKE (C_ prefix), not lower_snake. |
| C2 | ✅ TRUE | Default prefixes are `T_`, `C_`, `FK_`, `FK_INV_` and `J_`; setting a prefix to `-` suppresses it. | `runtime__judo-tatami/judo-tatami-workflow/src/main/java/hu/blackbelt/judo/tatami/workflow/DefaultWorkflowSetupParameters.java:153-163; runtime__judo-tatami/judo-tatami-workflow-maven-plugin/src/main/java/hu/blackbelt/judo/tatami/workflow/maven/plugin/DefaultWorkflowMojo.java:514` | Defaults T_, C_, FK_, FK_INV_, J_; the Mojo strips "-" (`rdbmsTablePrefix.trim().replace("-","")`), so "-" gives an empty prefix. Empty column prefix also maps reserved ID/TYPE/VERSION to DOMAIN_* (Asm2RdbmsHelper.java:297-306). |
| C3 | ✅ TRUE | Every entity table gets nine system columns: `ID` (UUID), `TYPE`, `VERSION` and create/update username, user ID and timestamp; m:n join-table FK columns get no … | `runtime__judo-tatami-base/judo-tatami-asm2rdbms/src/main/java/hu/blackbelt/judo/tatami/asm2rdbms/zeta/Asm2RdbmsRuleNames.java:40-49; runtime__judo-tatami-base/judo-tatami-asm2rdbms/src/main/java/hu/blackbelt/judo/tatami/asm2rdbms/zeta/rules/AttributeRules.java:260-285` | Nine system fields: ID, TYPE, VERSION, create/update username, user id, timestamp. The only RdbmsIndex rule is EAttributeToIndex (identifier attributes of entity types), so no index is created on join-table FK columns. |
| D1 | ⚠️ PARTLY | (developer statement) | `runtime__judo-tatami-base/judo-tatami-asm2rdbms/src/main/java/hu/blackbelt/judo/tatami/asm2rdbms/zeta/Asm2RdbmsHelper.java:308` | "yes" to C1 is right for limits but columns are upper-cased in the generator. |
| D2 | ✅ TRUE | (developer statement) | `runtime__judo-tatami/judo-tatami-workflow-maven-plugin/src/main/java/hu/blackbelt/judo/tatami/workflow/maven/plugin/DefaultWorkflowMojo.java:210-220,514` | Confirms C2. |
| D3 | ✅ TRUE | (developer statement) | `runtime__judo-tatami-base/judo-tatami-asm2rdbms/src/main/java/hu/blackbelt/judo/tatami/asm2rdbms/zeta/Asm2RdbmsRuleNames.java:40-49` | Confirms C3. |

Developer answer: _yes / yes / yes_

### K36 Optimistic locking and `__version` on updates

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | The RDBMS DAO enables optimistic locking by default (`rdbmsDaoOptimisticLockEnabled=true`), and every entity carries a `VERSION` field exposed as the reserved p… | `runtime__judo-runtime-core/judo-runtime-core-guice/src/main/java/hu/blackbelt/judo/runtime/core/guice/JudoDefaultModuleConfiguration.java:54; runtime__judo-services/judo-services-dao-rdbms-osgi/src/main/java/hu/blackbelt/judo/services/dao/rdbms/osgi/component/RdbmsDaoComponent.java:59; runtime__judo-runtime-core/judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/DefaultDispatcher.java:79` | rdbmsDaoOptimisticLockEnabled=true by default in the Guice config (OSGi key is optimisticLockEnabled, default true); "__version" is the reserved key (VERSION_KEY). |
| C2 | ✅ TRUE | The version check runs only when the update payload contains `__version`; a mismatch throws `IllegalArgumentException` "Outdated instance to update". Payloads w… | `runtime__judo-runtime-core/judo-runtime-core-dao-core/src/main/java/hu/blackbelt/judo/runtime/core/dao/core/processors/UpdatePayloadDaoProcessor.java:144-149` | If optimisticLockEnabled and updatePayload __version != null, checkArgument(equals) fails with IllegalArgumentException "Outdated instance to update"; null version skips the check. |
| D1 | ✅ TRUE | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dao-core/src/main/java/hu/blackbelt/judo/runtime/core/dao/core/processors/UpdatePayloadDaoProcessor.java:144-149` | Confirms C1 (check enabled when flag true). |
| D2 | ✅ TRUE | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dao-core/src/main/java/hu/blackbelt/judo/runtime/core/dao/core/processors/UpdatePayloadDaoProcessor.java:146-148` | Confirms C2. |

Developer answer: _yes / yes_

### K37 Liquibase executor and QueryCustomizer

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | The `LiquibaseExecutor` OSGi service runs a changelog from a bundle via `executeLiquibaseScript(Connection, path, Bundle)`, with an overload that accepts change… | `runtime__osgi-liquibase/src/main/java/hu/blackbelt/osgi/liquibase/LiquibaseExecutor.java:38,48` | Interface has executeLiquibaseScript(Connection, String scriptPathInBundle, Bundle) and an overload with Map<String,Object> parameters. |
| C2 | ✅ TRUE | `QueryCustomizer` is a builder with `filter` (JQL), `orderBy`, `seek`, `withoutFeatures`, `mask`, `parameters` and `instanceIds` for low-level DAO calls. | `runtime__judo-dao-api/src/main/java/hu/blackbelt/judo/dao/api/DAO.java:620-638` | Lombok @Builder class QueryCustomizer with filter (String JQL), orderBy (@Singular list), seek, withoutFeatures, mask, parameters, instanceIds. |
| D1 | 📐 PRACTICE | (developer statement) | `runtime__judo-dao-api/src/main/java/hu/blackbelt/judo/dao/api/DAO.java:620-638` | Statement that DAO-level API is usually used is advice; "suggest missing DAO-level concepts" is a request, not a claim. |

Developer answer: _yes but usually we use the Dao level api, u could sugges missing dao level conecptions_

### K38 Multi-module Maven build order and stale jars

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Modules depend on each other (model, schema, sdk, internal, app); install model and schema before building sdk standalone, e.g. with `-pl`, `-o` and `validateMo… | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-application/src/main/resources/pom.xml.hbs:233-294; template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-application/src/main/resources/pom.xml.model-properties-definition.fragment.hbs:9` | Modules model, schema, sdk, internal, app (plus rest, frontend etc.) exist and the sdk depends on the -model artifact (sdk/pom.xml.hbs:117); validateModels property exists (default false). `-pl`/`-o` are plain Maven; build-process.md.hbs:351 shows `mvn clean install -pl application/model,application/sdk,application/rest`. |
| C2 | ⚠️ PARTLY | The SDK regenerates at `generate-sources` from the model jar installed in `~/.m2`, not the edited source; a stale jar silently produces stale code. Rebuild with… | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-application/src/main/resources/sdk/pom.xml.hbs:26-34,117` | The SDK is generated by judo-psm-generator-maven-plugin in generate-sources from the -model dependency (resolved from reactor/~/.m2 when built standalone). But `judo.sh build -i` means --ignore-checksum (judo.sh.hbs:201), not "rebuild stale jars"; agent-docs list it as the usual build command (backend/README.md.hbs:78). |
| D1 | 📐 PRACTICE | (developer statement) | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-application/src/main/resources/sdk/pom.xml.hbs:117` | Confirmation only; see C1/C2 for the code facts. |

Developer answer: _yes they are_

### K39 Runtime container, datasource and Docker configuration

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | Felix health checks (`ModelsCheck`, `OperationsCheck`, `PlatformComponentsCheck`) are served at `http://localhost:8181/system/health?tags=<ModelName>`. | `runtime__judo-services/judo-services-healthcheck-osgi/src/main/java/hu/blackbelt/judo/services/healthcheck/osgi/ModelsCheck.java:51; template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-root/src/main/resources/agent-docs/deployment/README.md.hbs:140` | ModelsCheck, OperationsCheck, PlatformComponentsCheck are HealthChecks (default tc_tags "platform"); the template documents http://localhost:8181/system/health?tags=<model name lower-case>; servlet path /system/health per healthcheck-osgi spec.md:81. |
| C2 | ⚠️ PARTLY | The PostgreSQL datasource waits for the database with retry settings `retryMaxAttempts` (1000), `retryExponentialBackoff` (true) and `retryWaitDuration` (1000 m… | `runtime__judo-services/judo-services-persistence-postgresql/src/main/java/hu/blackbelt/judo/services/persistence/postgresql/LiquibaseModelToPostgresqlDatabaseServiceTracker.java:66-73; runtime__judo-services/judo-services-hsqldb-server/src/main/java/hu/blackbelt/judo/services/hsqldb/server/HsqldbServer.java:61` | Retry defaults retryMaxAttempts=1000, retryExponentialBackoff=true, retryWaitDuration=1000L are correct. HsqldbServer port defaults to 9001; that dev runs it "embedded" as a TCP server is not shown in the template (only JUDO_PLATFORM_LOG_SMTP_SERVER found in dev compose). |
| C3 | ⚠️ PARTLY | The docker module builds one image tar per architecture with jib on a hard-coded `azul/zulu-openjdk-debian:21-latest` base; generated POMs include empty `*.frag… | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-application/src/main/resources/docker/pom.xml.hbs:219-243,324,429-456` | jib-maven-plugin buildTar with base image azul/zulu-openjdk-debian:21-latest; there are x86_64, amd64 and arm64 profiles activated by os.arch (so a build makes the tar for the host arch, tar named *_x86_64/_arm64). No `*.fragment.hbs` extension point found in the docker module (fragments exist for root/app/karaf-features/e2e per build-process.md.hbs:148-160). |
| D1 | ✅ TRUE | (developer statement) | `runtime__judo-services/judo-services-healthcheck-osgi/src/main/java/hu/blackbelt/judo/services/healthcheck/osgi/ModelsCheck.java:42` | The checks report model/operation/component health state. |

Developer answer: _yes they give information of the health state of the applicaiton_

### K40 Local e-mail testing with Mailpit and Keycloak SMTP

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ❌ FALSE | For local runs, application SMTP settings come from `judo-karaf.env` (`localhost:1025`, no auth or TLS), which suits a mail catcher like Mailpit; deployed envir… | `runtime__judo-platform/judo-platform-config-templates/src/main/resources/judo-platform-config-templates/hu.blackbelt.email.impl.JavaMailSenderActivator.template:12,16` | Defaults: with logSmtpServer=true (set in judo-karaf.env.hbs:3 and dev compose) host=localhost, port=10025 (a log SMTP server), else port 25; localhost:1025 appears nowhere. Env names mailSmtpHost/mailSmtpPort/mailSmtpFrom (JUDO_PLATFORM_MAIL_SMTP_*) are the override mechanism (application-config.md.hbs:262+). Pointing the mail catcher at 10025 or overriding host/port works; 1025 is not the default. |
| C2 | ⚠️ PARTLY | Keycloak sends user-invitation e-mails, not the application, so `JUDO_PLATFORM_MAIL_SMTP_*` covers only application mail; the Keycloak realm needs its own SMTP … | `runtime__judo-services/judo-services-security-keycloak-osgi/src/main/java/hu/blackbelt/judo/services/security/keycloak/osgi/component/KeycloakUserManagerComponent.java:50-53` | The app only sets Keycloak required actions when creating users; no application code sends invitation mail, so those mails come from Keycloak. No code in the realm synchronizer sets realm SMTP, so the realm SMTP config is separate (consistent with the claim) but I found no direct evidence. |
| D1 | ⚠️ PARTLY | (developer statement) | `runtime__judo-platform/judo-platform-config-templates/src/main/resources/judo-platform-config-templates/hu.blackbelt.email.impl.JavaMailSenderActivator.template:12-16` | "yes" holds for the Keycloak-vs-application split, but not for the 1025 default (see K40.C1). |

Developer answer: _yes_

### K41 Frontend build modes, env vars and context path

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | The frontend reads `VITE_API_DEFAULT_BASE_URL` (default `window.location.origin`), `VITE_API_RELATIVE_PATH` (default `/api`), `VITE_FILE_DEFAULT_BASE_URL` (defa… | `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/src/main.tsx.hbs:37,45-48` | Reads VITE_MUI_LICENSE_KEY (optional, line 37), VITE_API_DEFAULT_BASE_URL\|\|window.location.origin, VITE_API_RELATIVE_PATH\|\|'/api', VITE_FILE_DEFAULT_BASE_URL\|\|API base URL. |
| C2 | ✅ TRUE | `frontend-build-type` selects `full` (install, format, build, test), `CI` (install, build, test) or `quick` (format + `build:reckless`); Node and pnpm versions … | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-application/src/main/resources/frontend-react/actor/pom.xml.hbs:235-290,302-355,359-400` | Profile build-frontend-full (default when property unset) runs pnpm install, run format, run build, run --if-present test; CI runs install/build/test; quick runs format + `run build:reckless`. Node/pnpm versions are template params (frontend-react/pom.xml.hbs:16-17, defaults 24.13.1/10.15.0) and install-node-and-pnpm runs in frontend-react/pom.xml.hbs:69. |
| C3 | ⚠️ PARTLY | In multi-actor apps each actor frontend is served at `/<model-name><frontend-postfix>/<actor-name>`; a single-actor app uses `singleApplicationPath` or `/`. | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-application/src/main/resources/frontend-react/actor/pom.xml.hbs:28-38` | Multi-actor Web-ContextPath is /${model-name}{{frontendTypePostfix frontendType '_react'}}/${actor-name}; single-actor uses singleApplicationPath or "/". But the postfix is "_react" only when multiple frontend types are generated (EsmProjectHelper.java:156-162), otherwise empty. |
| D1 | ✅ TRUE | (developer statement) | `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/package.json.scripts.fragment.hbs:1` | `pnpm run dev` = vite dev server (README.md.hbs:15); the build also packages dist as an OSGi web bundle with Web-ContextPath (actor/pom.xml.hbs:28-38) served by Karaf. |

Developer answer: _yes we could run it with vite or trough the karaf_

### K42 Forced regeneration and Biome "manually changed" false positives

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Files matching the gitignore-style globs in `.generator-checksum-ignore` skip checksum validation and are always regenerated; `.generator-ignore` instead stops … | `runtime__judo-generator-commons/src/main/java/hu/blackbelt/judo/generator/commons/ModelGenerator.java:364-370,466-475` | Right: globs in .generator-checksum-ignore (ChecksumIgnore.java:41) skip checksum validation, and .generator-ignore files are not written (and protected from deletion, :319-327). Wrong: checksum-ignored files are NOT "always regenerated"; the haveToGenerate filter at :466-470 excludes them from writing too, so they are neither validated nor rewritten. |
| C2 | ✅ TRUE | In the `full` frontend build, `pnpm run format` (Biome) rewrites generated files after the generator records their checksums, so the next build reports them as … | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-application/src/main/resources/frontend-react/actor/pom.xml.hbs:115,266` | Checksum goal (process-sources, UiProjectChecksumMojo recalculates from the directory) is declared in the generate profile before the `pnpm run format` execution (biome format --write, package.json.scripts.fragment.hbs:8) in the same phase, so Biome rewrites change files vs recorded checksums. Also applies to `quick` (pom.xml.hbs:380), not only `full`. |
| D1 | ⚠️ PARTLY | (developer statement) | `template__judo-esm-fullstack-project-template/judo-esm-fullstack-project-template-root/src/main/resources/judo.sh.hbs:14,105,819` | judo.sh has `-i/--ignore-checksum`, which passes -DvalidateChecksum=false to Maven. The Maven property is `validateChecksum=false`, there is no `ignoreChecksum=true` property. |

Developer answer: _yes we usually have to use the -i, ignoreChecksum=true for the leftovers the frontend files_

### K43 Running JUDO on Spring Boot (Spring Boot)

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 🚫 N/A-ESM | Autoconfiguration modules (`judo-runtime-core-spring`, `spring-hsqldb`, `spring-postgresql`) assemble the RDBMS runtime (DAO, dispatcher, query factory, variabl… | `-` | Spring Boot runtime assembly is JSL-only. |
| C2 | 🚫 N/A-ESM | `application.properties` sets `spring.datasource.*`, `spring.liquibase.change-log=classpath:model/<Model>-liquibase_hsqldb.changelog.xml` and `judo.modelName=<M… | `-` | Spring Boot application.properties/Liquibase config is JSL-only. |
| C3 | 🚫 N/A-ESM | The `judo-spring-maven-plugin` goal `transformerWorkflow` runs at `generate-sources` and picks the SQL dialects from the project dependencies (HSQLDB, PostgreSQ… | `-` | judo-spring-maven-plugin / Spring DaoModules is JSL-only. |
| D1 | 🚫 N/A-ESM | (developer statement) | `-` | Developer "yes" confirms a Spring-Boot (JSL-only) claim set. |

Developer answer: _yes_

### K44 Custom configuration parameters and encrypted values

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Custom application parameters use the OSGi Configuration Mapper: a configset declares `templatePath` (FreeMarker `*.template` files), `envPrefix` (e.g. `MY_APP_… | `runtime__osgi-configuration-mapper/src/main/java/hu/blackbelt/configuration/mapper/DefaultTemplatedConfigSetConfig.java:33,40,46` | templatePath (default /config-templates), envPrefix (required) and FreeMarker .template files (TemplateProcessor.java:28, OsgiTemplatedConfigurationSetHandler.java:53) are right. The attribute is named `variableScopePrecedence` (default "osgi,environment,system"), not `variableScopePreference`; judo-platform feature.xml:925 uses the "Preference" spelling, which the code does not read (value equals the default anyway). |
| C2 | ✅ TRUE | Configuration values written as `ENC(...)` are decrypted with Jasypt, e.g. a PAX-JDBC `password=ENC(...)`. `ENC(value, alias)` selects the encryptor service tha… | `runtime__osgi-encryption/osgi-encryption-services/src/main/java/hu/blackbelt/encryption/services/impl/BaseConfigDecryptor.java:33-35` | ENC(x) and ENC(x, alias) patterns; OsgiConfigDecryptor.java:40,50 looks up the Encryptor service by filter (encryptor.alias={alias}); encryptors are Jasypt-based (karaf-jasypt-support DefaultStringEncryptorConfig.java:30,77); README.md:22 shows password=ENC(...) in DBCP2 config (PAX-JDBC wording itself not verified). |
| D1 | ✅ TRUE | (developer statement) | `runtime__karaf-jasypt-support/README.md:20-23` | Developer "yes" matches; ENC(...) in config files decrypted via Jasypt encryptor services as C1/C2 show. |

Developer answer: _yes, check it_

### K45 Creating and upgrading a JUDO project

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 🚫 N/A-ESM | The `judo-jsl-springboot-archetype` needs only `modelName` (`^[a-zA-Z0-9]+$`). groupId defaults to `com.example`, artifactId to the lowercase model name, and th… | `-` | judo-jsl-springboot-archetype is a JSL/Spring Boot archetype. |
| C2 | ✅ TRUE | The `judo-version-updater-maven-plugin` goal `update-judo-versions` resolves the latest `judo-versions` against a channel ruleset, applying major/minor/incremen… | `tools__judo-version-updater-maven-plugin/src/main/java/hu/blackbelt/judo/maven/plugin/mojos/GetLatestVersionsMojo.java:22` | Goal update-judo-versions resolves latest hu.blackbelt.judo:judo-versions (GetLatestJudoVersionsArtifactVersion.java:36-56) with allowMajor/Minor/IncrementalUpdates (AbstractVersionUpdateMojo.java:62,81) and a version-ruleset-<channel>.xml (PluginHelper.java:99, channel default "develop"). |
| D1 | ⚠️ PARTLY | (developer statement) | `template__judo-esm-fullstack-project-template/README.md:428` | A `generateAgentCli` template parameter (default false) exists for AI agent CLI docs; that generating a fresh ESM fullstack project yields the newest CLI version was not verified. |

Developer answer: _yes, should generate agent cli esm fullstack to get the newest version of the cli._

### K46 Building Flutter frontends with Maven (Flutter)

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | The Maven goal `install-flutter` installs the Flutter SDK from a pinned version or a Git channel (default `stable`); the `flutter` goal runs Flutter CLI command… | `tools__flutter-maven-plugin/src/main/java/hu/blackbelt/flutter/maven/plugin/mojos/flutter/InstallFlutterMojo.java:35,53,59` | install-flutter installs from flutter-version or Git channel (default "stable"); FlutterMojo.java:35,44 goal `flutter` default arguments "pub get". |
| D1 | 📐 PRACTICE | (developer statement) | `tools__flutter-maven-plugin` | Deprecation is a status statement; nothing in the ESM fullstack template or platform references the plugin (no flutter in template__judo-esm-fullstack-project-template), consistent with it being unused. |

Developer answer: _DEPRICATED FOR A LONG TIME_

### K47 @JudoTest runtime caching and database selection

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | `@JudoTest(shareInjector=true)` reuses Injector, QueryFactory, Liquibase and TxManager across methods, only for datasource modes `BY_CLASS` or `SINGLETON`. | `runtime__judo-runtime-core/judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoTestExtensionRouting.java:46-54` | Cache is used only at class level, mode != BY_METHOD, and shareInjector=true; JudoTest.java:184-189 lists Injector/QueryFactory/Liquibase/TxManager as shared. |
| C2 | ⚠️ PARTLY | System properties `dialect` (`hsqldb` default or `postgresql`), `container` (`none`/`yugabytedb`) and `tz` (default `GMT`) select the test database; other diale… | `runtime__judo-runtime-core/judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoDatasourceFixture.java:48-52,151` | Fixture reads system props dialect (hsqldb default), container (none default) and tz (GMT) and throws IllegalStateException("Unsupported dialect") for others. But under @JudoTest the dialect/container are set from env JUDO_TEST_DIALECT/JUDO_TEST_CONTAINER > annotation attributes (JudoTestExtension.java:143-171,243-247); only tz comes from the system property. Container values include yugabytedb (:101). |
| C3 | ⚠️ PARTLY | `BY_CLASS`/`SINGLETON` extensions commit the transaction in `afterEach` and swallow exceptions silently; `JudoRuntimeFixture` combines modules via `Modules.comb… | `runtime__judo-runtime-core/judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoDatasourceByClassExtension.java:35-42` | BY_CLASS and SINGLETON extensions (JudoDatasourceSingletonExtension.java:39-45) commit in afterEach, but swallow only IllegalTransactionStateException (no active tx), not all exceptions. JudoRuntimeFixture.java:317 does use Modules.combine. |
| D1 | ⚠️ PARTLY | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-guice-testkit/src/main/java/hu/blackbelt/judo/runtime/core/guice/testkit/fixture/JudoTest.java:184-189` | Javadoc says class-level sharing gives ~5-10x speedup, but BY_CLASS alone shares only DataSource/model loader; QueryFactory is rebuilt per method unless shareInjector=true as well. |

Developer answer: _For now the queryFactor build is slow for testing, so we should  build it by class level._

### K48 Test-suite JVM heap exhaustion skips test classes

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ❔ NOT FOUND | The test suite forks several JVMs, each with its own heap set in `test/pom.xml`; when one JVM runs out of memory, every class still queued on it never runs. | `template__judo-esm-fullstack-project-template/pom.xml:211-225` | No test/pom.xml with multi-JVM heap/forkCount settings in platform or template repos (only argLine entries); claim describes an application's test setup / generic Surefire behaviour. |
| C2 | ❔ NOT FOUND | Surefire can still report a green result, such as "524 tests, 0 failures", while those classes never ran. Raising the per-JVM heap makes the results trustworthy… | `-` | No platform evidence of a "524 tests, 0 failures" report-while-skipping case; generic Surefire/OOM behaviour, not verifiable in this source. |
| D1 | ❔ NOT FOUND | (developer statement) | `-` | Developer "Yes" cannot be checked against source; no code on this. |

Developer answer: _Yes_

### K49 API-level tests with ApiClient and Postman

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | The REST Assured generator emits `ApiClient.api(Config)` with `BASE_URL_<ACTOR>` constants and `authTo<Actor>(grantType, userName, password)` helpers that get t… | `template__judo-psm-generator-restassured/judo-psm-generator-restassured-api/src/main/resources/restassured/api/apiClient.java.hbs:34,77-90` | Emits ApiClient.api(Config) (:55), BASE_URL_<ACTOR> constants and authTo<Actor>(grantType,userName,password) posting form client_id=<model>-<actor>, username, password, grant_type to the Keycloak realm token URL; only for actors with a realm; grant type is a caller-supplied argument (not fixed to "password"). |
| C2 | ❌ FALSE | The generated application includes Postman v2.1 collections that test the REST API against a running local instance (`http://localhost:8181`). | `runtime__judo-platform/judo-platform-itest/itests/UrlVariables.postman_environment.json:6` | Postman v2.1 collections (schema v2.1.0) with localhost:8181 live in the platform's judo-platform-itest, not in the generated application; no postman files in the fullstack template or the PSM generators. |
| D1 | ⚠️ PARTLY | (developer statement) | `template__judo-psm-generator-restassured/judo-psm-generator-restassured-api/src/main/resources/restassured/api/apiClient.java.hbs:77` | Yes holds for the ApiClient part (C1); not for the generated Postman collections (C2). |

Developer answer: _Yes_

### K50 Adding or removing a model attribute

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Adding an attribute touches the entity, service transfer-object mappings, backend query mask, frontend custom hook mask, i18n, imports and tests; missing the ma… | `template__judo-ui-react-template/judo-ui-react/src/main/resources/actor/src/pages/index.tsx.hbs:159` | Page mask defaults to the generated serializeMaskForView (derived from the model); a custom hook getMask overrides it, so only customised masks need manual updating. Remaining items (entity, mappings, i18n, tests) are application practice. |
| C2 | 📐 PRACTICE | Removing an attribute, relation or entity requires deleting it from transfer views, tables, forms, derived members and bindings, otherwise model validation fail… | `-` | Authoring advice; build-time ESM validation failure for dangling references was not verified here. |
| C3 | 📐 PRACTICE | Consolidating a duplicate entity or transfer object across service packages changes generated frontend hook names and Java interceptor imports. | `-` | Authoring advice; effect on generated hook names/interceptor imports not verified. |

### K51 Workflow conditions as derived predicates

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | Transient workflow conditions (e.g. "is dispatched") are derived from status and timestamps; stored booleans drift from the state machine. Store only genuine pe… | `-` | Modeling advice on derived vs stored booleans; code cannot confirm. |
| C2 | 📐 PRACTICE | Role guards like `User!filter(u \| u.email == ...getVariable("ACTOR","email") and (u.roleX or u.roleY))!empty()` and their negation can wrongly exclude users hol… | `-` | JQL-guard design pitfall (and/or with role flags); not a platform fact, no platform evidence checked. |

### K52 Model changes that break custom frontend code

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Removing or renaming a model attribute, operation or transfer object regenerates the TypeScript surface; custom hooks referencing old members or module paths fa… | `template__judo-ui-react-template/judo-ui-react/src/main/resources/ui-react.yaml:311` | Frontend is regenerated from the model so removed members break custom code; TS2339/TS2307 is a TypeScript compiler consequence, not platform code. |
| C2 | ⚠️ PARTLY | The frontend generator emits a hook file only when the hook flag (e.g. `generateActionsHook`) is set in the model; `src/custom` is gitignored, so hooks need no … | `template__judo-ui-react-template/judo-ui-react/src/main/java/hu/blackbelt/judo/ui/generator/react/UiPandinoHelper.java:137` | Hook registration files (src/custom/hooks/.../register*ActionsHook.ts.default) are only generated for pages with isGenerateActionsHook; but the generated actor/gitignore has no src/custom entry, so src/custom is NOT gitignored (docs/pages/01_ui_react.adoc:456 even says files must go into .generator-ignore). |
| C3 | 📐 PRACTICE | New fields, columns and operations are modeled as ESM UI elements on `<TO>View`/`<TO>Form`/`<TO>Table` transfer objects and customized via hooks, not built as r… | `template__judo-ui-react-template/docs/pages/01_ui_react.adoc:907` | Customization via hooks (typeahead, columns) is documented; the "model on View/Form/Table, not replacement components" is design advice. |

### K53 Type-ahead with a learning reference dictionary

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Setting the `typeAHead` designer flag on a string attribute makes the frontend use `TextWithTypeAHead` with `getForm_*Options` getters backed by reference-data … | `runtime__judo-tatami-client/judo-tatami-esm2ui/src/main/java/hu/blackbelt/judo/tatami/esm2ui/zeta/transformations/ui/DataFieldTransformations.java:476` | ESM isTypeAheadField maps to UI and view-imports.fragment.hbs:39-40 imports TextWithTypeAhead when container has typeahead; the hook is a custom getXxxOptions (docs adoc:907-925 shows getNameOptions); the flag name is isTypeAheadField and "getForm_*Options"/reference-data lookup backing was not found (user-implemented hook). |
| C2 | ❔ NOT FOUND | The reference dictionary learns new values when the parent is created and supports bulk CSV import. | `-` | No platform code for a learning reference dictionary or bulk CSV import found; an application pattern. |
| D1 | 📐 PRACTICE | (developer statement) | `-` | Design advice about access/transfer modelling; not confirmable in code. |

Developer answer: _U should create a new access as a single transfer which contains this typehead relation to avoid the access which not availabe for all users_

### K54 Generated DAO read and write performance

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | In report or collection generation the dominant cost is usually the shared per-header projection read of a nested graph, not the writes; profile and bound reads… | `-` | Profiling advice; no platform fact. |
| C2 | ❌ FALSE | Bulk initial-data imports use `createAll` batching, cached lookups and create-with-mask instead of one-by-one creates with per-row DAO lookups. | `runtime__judo-runtime-core/judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/AbstractRdbmsDAO.java:217` | createAll is just a for-loop calling create() per payload; no batching or caching. |
| C3 | ❔ NOT FOUND | Owned relations on editable views are eagerly embedded in the read mask, and mandatory aggregation members are materialized as empty `{}` objects that can fail … | `-` | Did not trace eager owned-relation embedding or empty {} materialization in the generated mask/update validation. |
| D1 | ✅ TRUE | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/AbstractRdbmsDAO.java:217-222` | createAll (and updateAll at ~245) is a plain loop over create(); no caching shown in DAO. |

Developer answer: _The current batching is NOT QUICKER, it is just a loop. ITs not cache anything._

### K55 Derived fields need explicit mask inclusion

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ❌ FALSE | A derived attribute does not render unless it is explicitly added to the mask or the interceptor projection. | `runtime__judo-runtime-core/judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/query/model/RdbmsResultSet.java:707` | With mask == null features are included (except parameterized ones); with a mask only masked features are; derived attributes need no extra mask unless a mask is given. |
| D1 | ✅ TRUE | (developer statement) | `runtime__judo-runtime-core/judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/query/model/RdbmsResultSet.java:707` | No mask returns all attributes; a given mask restricts to listed ones (empty mask = identifier only, per catalog agent-docs). |

Developer answer: _NOOOOOOOOOOO, its rendered always, withouth mask all attributes rendered, if we give a mask we explicitly tell what we want to add, the Parnter.mask() without attribute only give back the idnetife!!!!, Parnter.mask().attributeName, its add the attributeName to the query._

### K56 Report and export SPIs

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | The report generator creates a `{Type}Report` facade per qualifying transfer object with `generate{Type}Report(OutputType, dto, File\|OutputStream[, Map<String,O… | `template__judo-psm-generator-report/judo-psm-generator-report-jasper-java/src/main/resources/java/report/report.java.hbs:20-36` | Generates generate{Dto}Report overloads for File and OutputStream, each with and without Map<String,Object> additionalParameters; uses ReportUtil (Jasper). |
| C2 | ✅ TRUE | Modeled EXPORT operations run through an Export SPI whose reference implementation, `JxlsExport`, produces XLSX via JXLS/POI. | `runtime__judo-runtime-core/judo-runtime-core-export-jxls/src/main/java/hu/blackbelt/judo/runtime/core/export/JxlsExport.java:13` | JxlsExport implements Export; JxlExportUtil.java:124 builds an XSSFWorkbook (jxls/POI) producing XLSX. |
| D1 | 📐 PRACTICE | (developer statement) | `-` | Bare "yes" confirmation; no additional factual statement. |

Developer answer: _yes_

### K57 Business errors: one fault, a factory, interceptor wrapping

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Model one general business fault transfer object (`code`, `message`) and declare it as `fault` on every failing operation; without `<faults>` the generated inte… | `template__judo-psm-generator-jaxrs/judo-psm-generator-jaxrs-api/src/main/resources/rest/api/rest.service.operation.fragment.hbs:58` | Business faults map to HTTP 422 "Business fault"; no evidence found for a single general fault TO convention or the exact throws-clause rule. |
| C2 | ⚠️ PARTLY | Construct exceptions through a project factory; use `ValidationException` with the attribute name for field problems and the business fault with a code for rule… | `runtime__judo-runtime-core/judo-runtime-core/src/main/java/hu/blackbelt/judo/runtime/core/exception/ValidationException.java:28` | ValidationException exists (ClientException); the project-factory convention is practice. |
| C3 | ⚠️ PARTLY | Interceptors throw `InterceptorCallBusinessException` with the fault FQN as `type` so the generated `faults.<fqn>.<attr>` dialog translates it; wrapping faults … | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/DefaultDispatcher.java:764-770` | InterceptorCallBusinessException(type, errorCode, ...) becomes a _fault payload with type; RuntimeExceptionMapper.java:94-96 returns 500 INTERNAL_SERVER_ERROR for other runtime exceptions, BusinessException gives 422 (jaxrs/providers/RuntimeExceptionMapper.java:97). The faults.<fqn>.<attr> dialog translation was not verified. |

### K58 Validation problems as returned data

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | Operations that validate many items can return an optional transient output transfer listing errors (item id, position, code, message) instead of throwing; no r… | `-` | Modeling pattern for returning validation errors. |
| C2 | 📐 PRACTICE | Persisted validation errors can be a composition child at entity level, exposed as a transfer-level association that loads only when the user expands the list. | `-` | Modeling pattern. |
| C3 | 📐 PRACTICE | Readiness checks return the full list so users see every missing item; real rule violations still throw. | `-` | Design advice. |

### K59 Operation input prefill and range selectors

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | Generate-style operations take a separate `*Input` transfer object, prefilled by an initializer, instead of reading the entity directly; range-selector relation… | `-` | Modeling pattern for operation input/initializer; range selectors not traced. |

### K60 Server-side rule enforcement

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ❔ NOT FOUND | Model min/max range bounds only drive frontend display; the backend still persists out-of-range values. | `-` | No server-side min/max enforcement found in runtime-core (only frontend); not conclusively searched across ESM validations. |
| C2 | 📐 PRACTICE | Hidden UI buttons or menus do not protect operations; generated REST endpoints remain callable, so workflow state and role guards live in the operation or a wri… | `-` | Design advice; REST endpoints are generated regardless of UI visibility (not traced). |
| C3 | 📐 PRACTICE | Interceptors cover built-in operations only; custom operations repeat the check in their implementation. Write-guard interceptors list target operation FQNs dir… | `-` | Design advice on interceptors; not verified. |

### K61 Field-level role-based edit guards

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Restricting specific fields of a shared entity to certain roles combines a server-side update guard with hiding the field from views for unauthorized roles. | `runtime__judo-runtime-core/judo-runtime-core-accessmanager/src/main/java/hu/blackbelt/judo/runtime/core/accessmanager/behaviours/UpdateInstanceAuthorizer.java:52` | Update is guarded per transfer-object CRUD flag (UPDATE) and hiding is via VisualElement hiddenBy (esm.ecore:1006); but no per-field role guard exists in the platform, so the field-by-role combination is an application pattern (custom interceptor/model design). |

### K62 Actor role gates and visibility attributes

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ✅ TRUE | Menu and visibility gate attributes (`hiddenBy`, menu-hidden flags, access gates) belong on the principal or service-user transfer projection, not the plain ent… | `models__judo-meta-esm/model/src/main/epsilon/validations/ui/component.evl:17-22` | HiddenByIsValid requires hiddenBy to be a Boolean attribute of the root transfer object type of the view (HiddenByIsBooleanType :24); MenuItem has hidden/hiddenBy/enabledBy (models__judo-meta-esm/model/model/esm.ecore:1006), so they live on the projection backing the page (principal projection for menus), not the plain entity. |
| C2 | ✅ TRUE | Adding an actor role to an access's role gate controls who may open the access; it does not scope rows to the actor's own data. | `runtime__judo-runtime-core/judo-runtime-core-accessmanager/src/main/java/hu/blackbelt/judo/runtime/core/accessmanager/behaviours/ListAuthorizer.java:50` | The authorizer only checks the actor FQ name against the `exposedBy` annotation (allow/deny); it adds no row filter, so row scoping to own data must come from the model's mapping/expressions. |

### K63 Serving stored binaries securely

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | `FileType` references carry the filestore key as id; exposing it in public URLs lets callers fetch any stored file by guessing ids, so binaries are served throu… | `runtime__osgi-filestore/filestore-servlet/src/main/java/hu/blackbelt/osgi/filestore/servlet/DownloadServlet.java:72` | FileType carries the file id (FileTypeFormatter.java:40, ids are random UUIDs FileEntity.java:53) and downloads can require a signed JWT token (DefaultTokenIssuer.java:102), but `tokenRequired` defaults to false so with tokens off any known id is downloadable (ids are random UUIDs, not sequential); the "access-checking indirection" is a practice, and the guessing risk is only real when tokens are off. |

### K64 Native SQL from custom code

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | Queries that JQL and the generated QueryCustomizer cannot express (e.g. lookups through a join table) run as native SQL via the JDBC DataSource in a custom serv… | `runtime__judo-runtime-core/judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/RdbmsDAOImpl.java` | A JDBC DataSource is used by the RDBMS DAO and could be injected into custom code; the specific "QueryCustomizer cannot express join-table lookup" advice is app design (QueryCustomizer itself not found as a platform name in main code). |

### K65 Non-Java sidecar services

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | Adding a Node or AI sidecar to a JUDO Karaf app involves publishing its artifact, naming environment variables consistently and wiring it in compose. | `packages__karaf-features` | Publishing artifacts, env var naming and compose wiring are app/devops practice; the platform code does not define sidecar services. |
| C2 | ⚠️ PARTLY | Asynchronous external work uses an instance-bound custom operation with no input parameter that fires and returns; the client polls the instance for the result. | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/OperationCallInterceptor.java` | Operations are synchronous call interceptors; no built-in async/fire-and-return support was found, so the fire-and-poll pattern is an app-level design (custom operation spawning its own work); instance-bound operations without input are valid ESM. |

### K66 E2E testing methodology for JUDO apps

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | Build one prepared database dump, including Keycloak users (Keycloak shares the backend DB), once; derive all test groups from it and run parallel stacks on dis… | `runtime__judo-platform/.github/workflows/build.yml` | Dump/parallel-stack E2E methodology is application practice; no platform evidence that Keycloak shares the backend DB (not found in judo-keycloak or platform config). |
| C2 | 📐 PRACTICE | E2E tests navigate real pages and assert visible elements; only access checks such as hidden menu items or authorization stay REST-only. | `template__judo-ui-e2e-template` | Test-writing methodology; platform code cannot confirm. |
| C3 | 📐 PRACTICE | Keep each run within about two minutes; a cloneable PostgreSQL speeds up resets. | `-` | Run-time target and cloneable PostgreSQL (TEMPLATE database) are test-ops advice; nothing in platform code. |

### K67 Self-contained integration tests

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Integration tests are class-scoped and create only the entities they need via DAO builders or fixtures, not application-wide master-data seeding. | `runtime__judo-runtime-core/docs/JNG-6374-testkit-runtime-cache.md:3` | Testkit supports BY_CLASS and SINGLETON runtime modes with DAO/fixture builders; "class-scoped, create only needed entities" is a practice, not enforced. |
| C2 | ✅ TRUE | A runtime version that caches the model loader makes this style faster. | `runtime__judo-runtime-core/docs/JNG-6374-testkit-runtime-cache.md:1` | JNG-6374 "Cache model loader in testkit for BY_CLASS and SINGLETON modes" (commit e0bfe372) was added specifically to speed up tests; note shareInjector defaults to false (doc line 6). |

### K68 DOCX template syntax and null safety

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ❔ NOT FOUND | XDocReport/FreeMarker DOCX templates put directives in MERGEFIELD codes: `#list x as y`/`/#list`, `#if cond??`/`/#if`, `@before-row[#list ...]`/`@after-row[/#li… | `packages__karaf-features/karaf-features-xdocreport/src/main/feature/feature.xml` | XDocReport is only packaged as a Karaf feature (also docx4j bundles); directive syntax (MERGEFIELD, @before-row) belongs to XDocReport/FreeMarker, not defined in judo-ng code. |
| C2 | ❔ NOT FOUND | Every possibly-null merge field needs a default (`!false`, `!''`, `??`, `?filter(...)`), otherwise rendering fails with "evaluated to null or missing"; mismatch… | `packages__karaf-features/karaf-features-xdocreport/src/main/feature/feature.xml` | FreeMarker null-handling behaviour is third-party; judo-ng has no template or error handling code for it. |

### K69 Handlebars document templates

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ❔ NOT FOUND | Handlebars loops expose `@index`, `@index_1` (1-based), `@key`, `@first`, `@last`, `@odd`, `@even`, so hierarchical numbering like 1.1 needs no custom helpers. | `template__judo-psm-generator-report/pom.xml:93` | Handlebars (jknack) is a dependency, but `@index_1`, `@odd`, `@even` appear nowhere in judo-ng; they are not platform-defined (index_1 is not a standard Handlebars.java built-in either: verify upstream). |
| C2 | ❔ NOT FOUND | Markdown report templates (`.md.hbs`) render with Handlebars, then convert to DOCX and PDF, replacing the XDocReport DOCX pipeline; frontmatter content needs es… | `template__judo-psm-generator-report/pom.xml:93` | No `.md.hbs` template pipeline or markdown→DOCX/PDF conversion found in judo-ng; handlebars is used for report generation helpers only; the replacement of XDocReport is an application-level setup. |

### K70 Registry number allocation and concurrency

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ❔ NOT FOUND | A document registry's `currentIndex` is consumed only on the create path; regenerating an existing document does not allocate a new number. | `runtime__judo-operation-utils/src/main/java/hu/blackbelt/judo/operation/utils/FunctionRunner.java` | `currentIndex` is only an application-model attribute; the platform has no registry concept, so create-only consumption is application logic. |
| C2 | ⚠️ PARTLY | `synchronized` around number generation is insufficient when the DAO update lands outside the atomic section; the read-modify-write needs real database locking. | `runtime__judo-runtime-core/judo-runtime-core-dao-rdbms/src/main/java/hu/blackbelt/judo/runtime/core/dao/rdbms/RdbmsDAOImpl.java` | General Java fact: JVM `synchronized` does not cover DB updates committed outside it nor multi-node; no pessimistic locking (SELECT FOR UPDATE) exists in runtime-core DAO, so real locking must use native SQL/DB. |
| C3 | 📐 PRACTICE | Separate the displayed document number from the rendered version. | `-` | Design advice about separating numbers from versions; no platform fact. |

### K71 Detailed bilingual history messages

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | Audit history messages use i18n in both languages with interpolated dates and enum labels rather than raw values. | `models__judo-meta-esm/model/model/esm.ecore (no i18n/translation feature on audit data)` | History message wording, bilingual text and enum-label interpolation are application model design; platform has no audit-message feature to confirm. Not verified further. |

### K72 Ticket lifecycle with role and state gates

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | A ticket entity has an enumeration state (e.g. RECEIVED → SUPPLEMENTED → FINALIZED, or DISCARDED). Derived boolean flags such as `canFinalize` combine the state… | `models__judo-meta-esm/model/model/esm.ecore:679` | ESM has `enabledBy`/`hiddenBy` references to a DataFeature (boolean derived) that drive UI buttons (also :1005); runtime-core has no reference to enabledBy, so the operations themselves are NOT gated by the flag - server-side gating needs separate model checks/permissions. State enum and role-combining flags are model practice. |
| C2 | 📐 PRACTICE | Close-with-follow-up and close-without-follow-up are two separate operations that exclude each other. Permission to close is a per-user flag, not just a role. | `-` | Two exclusive close operations and a per-user close permission flag are model design; platform provides nothing specific (no per-user flag concept beyond modelled attributes). |
| C3 | 📐 PRACTICE | Delegating a ticket sets the assigned user. That user becomes the owner of every document generated downstream. Non-assignee roles see the ticket read-only and … | `-` | Owner propagation to generated documents, read-only for non-assignees and reopen blocking are application logic; no platform feature found. |

### K73 Job sheet → work report → completion certificate

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | From an accepted offer, a `generateJobSheet` operation creates job-sheet items, split by fault and quantity and numbered per fault (no global sequence). It is v… | `-` | generateJobSheet, per-fault numbering and validity preconditions are application operation logic; not platform behaviour. |
| C2 | 📐 PRACTICE | A work report has a `kind` (WORK_REPORT or COMPLETION_CERTIFICATE) and a `workStatus`. The prerequisite for `toDone` depends on the kind. | `-` | `kind`/`workStatus` and kind-dependent toDone prerequisite are model-specific. |
| C3 | 📐 PRACTICE | A work item goes to DONE only with at least one photo, and to WONT_FIX only with a reason given in the operation input. | `-` | Photo requirement and WONT_FIX reason are application-level validations. |

### K74 Offline-first mobile ingest

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | The client gives each pushed object, and each of its media files, a stable `localId`. The ID is filterable (`filterByLocalId`), so a resend after a lost reply i… | `-` | localId and filterByLocalId are modelling conventions; platform does not provide idempotent resend detection. |
| C2 | ✅ TRUE | The upload has two stages. Each file is sent on its own (short-lived permit, then bytes, which return a file reference). One final call then submits the record … | `runtime__osgi-filestore/filestore-servlet/src/main/java/hu/blackbelt/osgi/filestore/servlet/UploadServlet.java:273` | Upload needs a short-lived upload token (issued by GetUploadTokenCall.java:82, header token), bytes are POSTed to UploadServlet, which returns JSON with file id/url/token (:309); the record is then submitted with the reference (modelled call). |
| C3 | ⚠️ PARTLY | Change-stamp timestamps on the root transfer object (e.g. `catalogueChangedAt`) let the client pull only what changed. A resend of the same status change is a 2… | `template__judo-psm-generator-jaxrs/judo-psm-generator-jaxrs-impl/src/main/resources/rest/impl/rest.service.impl.java.hbs:101` | Void operations return 204 NO_CONTENT in the generated REST; change-stamp attributes and treating a repeated status change as no-op vs update are application logic, not platform. |

### K75 Offer pricing: cost, price, markup and minimum floor

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | An offer keeps a cost side (cost price per line, total cost) apart from a price side (unit and selling price, per-line minimum price). Profit and overall markup… | `-` | Cost/price separation and derived profit/markup are model design (derived expressions are available, but the split is app-specific). |
| C2 | 📐 PRACTICE | A minimum offer price per currency is filled up by one dummy offer item that covers only the gap in included services. Materials and non-included items are adde… | `-` | Minimum-price dummy item is application logic. |
| C3 | 📐 PRACTICE | `expectedQuantity` on an offer item is recalculated on each save as the sum of `fault.quantity × multiplier` over the related faults (multiplier defaults to 1). | `-` | expectedQuantity recalculation is app logic. Platform note: ESM derived attributes are expressions evaluated on read, not recalculated on save (no evidence otherwise found). |

### K76 Partner-scoped multi-role users

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | 📐 PRACTICE | Users belong to role families: operator-side (inner) roles and partner-side roles. One user cannot hold both, and the server checks this rule when the user is c… | `-` | Role families and mutual exclusion check at user creation are application validation; platform has no such built-in rule. |
| C2 | 📐 PRACTICE | Partner roles reach users and data only through their own partner's access, never through a global users access. The service admin sees all users. | `-` | Scoping through partner-bound accessors is model design; the platform only provides actor access points (esm.ecore actor/access model). |
| C3 | 📐 PRACTICE | An external advisor-type role has a two-way advisor relation to the users it serves. Partner-side users must have an assigned advisor, while inner roles delegat… | `-` | Advisor relation and assignment rules are model design. |

### K77 Typed media attachment with several owner types

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | A media attachment is its own entity with a `FileType` binary and a `MediaType` enumeration (PHOTO, VIDEO, AUDIO). Several entity types own it through back-refe… | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/behaviours/GetUploadTokenCall.java:84` | FileType is a platform binary attribute type (upload/download via tokens) and MediaType enum/back-references are plain model design; owner lookup via back-references is practice, not enforced. |
| C2 | 📐 PRACTICE | Derived filters such as "photos only" select by `MediaType`. | `-` | Derived filter by enum is ordinary ESM derived/expression design; nothing platform-specific. |
| C3 | ❌ FALSE | External or system clients read attachments through the same modelled attachment API as the frontend, not through a separate HTTP servlet. | `runtime__osgi-filestore/filestore-servlet/src/main/java/hu/blackbelt/osgi/filestore/servlet/DownloadServlet.java:145` | The modelled API only returns a download token (ResponseConverter.java:117-128); the bytes are served by the separate HTTP DownloadServlet (getOutputStream :200) for every client, frontend included; upload likewise goes through UploadServlet. |

### K78 Delete versus discard with retention

| # | Verdict | Claim | Evidence | Note |
|---|---|---|---|---|
| C1 | ⚠️ PARTLY | Instant physical delete behind a confirmation dialog is the simpler choice when there is no restore requirement and personal data (such as voice recordings) mus… | `runtime__judo-runtime-core/judo-runtime-core-dispatcher/src/main/java/hu/blackbelt/judo/runtime/core/dispatcher/behaviours/DeleteInstanceCall.java:77` | Platform delete is a physical DAO delete (dao.delete) with no soft-delete or restore; confirmation dialog is a UI option (confirmationType in ui model). Choice advice is practice. File blob removal on delete was not verified. |
| C2 | 📐 PRACTICE | Discard with retention adds a discarded state, a separate list and permission, and an age-based cleanup job that deletes discarded records after the retention p… | `-` | Discarded state, list, permission are model design; the platform has no retention/cleanup scheduler (no such job found in runtime-core/services), so the age-based job is an external/app concern. |
