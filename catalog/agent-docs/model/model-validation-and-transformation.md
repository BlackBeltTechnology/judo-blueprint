---
title: Model Validation and Transformation Options
description: EVL validation entry points, ETL versus ZETA transformation engines, Maven workflow options, measures, static data and known model issues.
---

# Model Validation and Transformation Options

This page covers how models are validated, how the transformation engines are selected, and the build-time artefacts around the ESM. For the CLI-driven pipeline see [transformation-pipeline.md](./transformation-pipeline.md).

## Validation entry points

- ESM models are validated with EVL. `EsmModel.loadEsmModel(LoadArguments)` validates by default and throws `EsmValidationException` when there are ERROR diagnostics; `saveEsmModel(SaveArguments)` refuses to save an invalid model unless validation is switched off in the save arguments. The validator entry point is `EsmEpsilonValidator.validateEsm(Logger, EsmModel, URI)`; `EsmValidator.validateEsm(log, esmModel)` has an overload that takes expected errors and warnings and throws on a mismatch.
- EVL rules live in `model/src/main/epsilon/validations/`. A rule declared as `constraint` reports an ERROR; a `critique` reports a WARNING. Messages have the form `ConstraintName|Error message`. For example the RDBMS naming rules are critiques: table names must match `^[A-Z][A-Z0-9_]*$` and column names `^[a-z][a-z0-9_]*$`.
- The Maven workflow parameter `validateModels` defaults to `false`. When enabled, ESM validation runs before the ESM to UI step and stops the transformation on critical errors, and UI validation runs the UI EVL files. Note that ESM validation is currently commented out in `Esm2UiWork`. In practice rules are checked by the full build, by `validate` in the CLI, and in tests.
- Some rules are only exercised by a full build (the JQL builder, the ASM validator, the TypeScript compile); `transform --skip liquibase --load` does not run them.

## Transformation engines (ETL and ZETA)

Every transformation (PSM to ASM, ASM to RDBMS, ASM to Keycloak, PSM to Measure, RDBMS to Liquibase, ESM to UI) exists in two implementations: the legacy Epsilon (ETL) scripts and the Java rewrite (ZETA). The engine is selected through `TransformationMode` (system property based for the workflow path). The default differs by path: the builder path defaults to ZETA for most transformations, but ESM to UI defaults to ETL, and the OSGi services (`Esm2UiTransformationService`, `Esm2UiPreview`) always run ETL. The ZETA path ignores `createTrace`, `parallel` and `useCache` and runs sequentially. The two engines are known to differ in details such as generated element IDs and clone-persistence semantics; compare outputs before relying on identical results.

In Karaf, the `Esm2UiTransformationEsmModelTracker` only activates when a configuration exists for it, and installing the same model name a second time is refused.

Setting the system property `judo.zeta.metrics` to `true` makes ZETA print `TransformationMetrics` after each run.

## Maven workflow plugin

`judo-tatami-jsl-workflow-maven-plugin` (`hu.blackbelt.judo.tatami`) runs the model workflow, goal `default-model-workflow`, in `generate-sources`. It runs the steps in parallel by default and has `ignore*` toggles per step, a transformation mode (ETL, ZETA or BOTH), `generateDefaultTransferObject`, `generateBehaviours`, and the naming prefix/postfix/midfix triples for generated entity, default, parameter, range and action-input names. ESM to UI accepts `applicationType` (default `default`) and `applicationColumns` (default 12) which set the grid of the generated UI.

## Generated model files

A project keeps exactly one designer-owned model file `model/<app>.model` (the name matches `[_a-zA-Z0-9]*.model`). The build and designer produce `*-esm.model`, `*-ui.model`, `*-keycloak.model`, `*-asm.model`, `*-psm.model`, `*-expression.model`, `*-measure.model`, `*-script.model`, `*-rdbms_*.model` and the trace models `*-psm2asm.model`, `*-psm2measure.model`, `*-asm2keycloak.model`. These are never edited by hand.

## Annotations and RDBMS tailoring

- Semantic annotations on ESM and ASM elements are EAnnotations with the source `http://blackbelt.hu/judo/meta/ExtendedMetadata/<name>` and the value in the detail key `value`. The operation behaviour annotation `type` string (for example `list`, `createInstance`, `getUploadToken`) is the model contract; unknown strings resolve to nothing.
- The RDBMS generator reads three Excel workbooks at build time: `RDBMS_Data_Types_<Dialect>.xlsx` (type to SQL type, size, precision, scale), `RDBMS_Table_Mapping_Rules.xlsx` (relation shape rules) and `RDBMS_Sql_Name_Mapping.xlsx` (FQN to SQL name overrides).

## Reusing schema fragments

The `merge-schema` goal of `judo-esm-schema-merge-maven-plugin` (phase `generate-resources`) copies selected entities, features and enumerations from a source ESM schema into a target model. Inputs are `schemaModelFile`, `targetModelFile` and a YAML `mergeModelFile` with an `entities` list, each entity listing its `features`. It creates missing entities and enumerations, copies missing features with consistency checks, and rewires two-way relation partners; existing elements are re-synchronised, not duplicated.

## Scaffolding and version pinning

`judo-version-updater-maven-plugin` provides `update-judo-versions` (resolves the latest `judo-versions` against the version ruleset and writes `judo-version.properties`), `create-judo-project` (scaffolds an ESM fullstack project from a model name and group id) and `create-jsl-judo-karaf-project`.

## Measures

Measures are base measures (such as `Mass` with `kilogram`) or derived measures built from other measures with exponents (`Area = Length.metre^2`); a derived measure may not reference itself. Units convert to the base unit with `rateDividend` and `rateDivisor` (`kilometrePerHour` has divisor 3.6 relative to `metrePerSecond`). A measure defines one base unit (`rateDividend == rateDivisor`). A measured type ties a numeric type to a stored unit, for example `MassStoredInKilograms` (precision 15, scale 4, store unit `kilogram`). At runtime the DAO converts between the transfer and entity unit using both rates, rounds to scale 20 with `HALF_UP`, and returns an integer when the entity attribute is an integer.

## Static navigations and static data

A *static navigation* exposes a fixed collection through a getter (for example `allCategories` with getter `app::entities::Category`) and can feed relation ranges. *Static data* holds a single value from a getter expression; its names are unique across the model (case-insensitive) and it cannot be required.

## What makes members orderable and filterable

Ordering and filtering are available on a reference whose target is mapped and has at least one non-`TRANSIENT` attribute of a supported type. Orderable: string, numeric, date, timestamp, time and boolean. Filterable: the same plus enumeration. `TRANSIENT` members are excluded. The same rules govern input-parameter ordering and the generated column filters, so they decide which sort and filter controls the generated UI offers.

## Creatable transfer objects

A transfer object used as a `CREATE_INSTANCE` or `VALIDATE_CREATE` target must not map to an abstract entity, and it must bind every required feature of the mapped entity (required relations with a lower bound above zero and required attributes), otherwise EVL fails with `AllRequiredFeaturesHaveBindingIfCreatable`.

## Transformation Mode and Generation Switches

The tatami engine runs in `ETL` (Epsilon), `ZETA` (Java) or `DUAL` (both, compared) mode, chosen with `-Djudo.transformation.mode=ETL` or per step with `transformationMode(...)`. The default is `ZETA`; use `ETL` to compare when debugging.

ESM-to-PSM is gated by `generateActors`, `generateOperations`, `generateBehaviours`, `generateTransferObjectTypes` and `generateDefaultTransferObjectTypes` (all `true`) and `stringMaxLength` (65536). The switches are not uniform: default-transfer-object attribute rules follow `generateDefaultTransferObjectTypes`, and the query customizer, ordering and filter families follow `generateBehaviours`; but not every rule is guarded (query ordering, filter and seeking types and the upload-token type are generated regardless).

### Embedding the transformations

`Esm2Ui.executeEsm2UiTransformation(Esm2UiParameter)` (built with `esm2UiParameter()`; defaults ETL, `parallel=false`, `applicationType` `default`, `applicationColumns` 12, `useCache=true`) or the work unit `Esm2UiWork` inside a `TransformationContext` run the ESM-to-UI step from Java. Workflows compose with `SequentialFlow`, `ParallelFlow`, `ConditionalFlow` and `RepeatFlow` builders; work names must be unique and each work must catch exceptions and report `WorkStatus.FAILED`. `TransformationTraceService` navigates the trace chain from one element (`getAscendantsOfInstanceByModelType`, `getRootAscendantsOfInstance`, `getTraceEntriesForInstance`); it throws `IllegalArgumentException` for an unregistered model name.

## Known issues

- A derived attribute that navigates through a member **inherited** from a supertype can produce SQL with a missing join in the RDBMS query generator (for example `lastWorkReport = self.workReports!any().lastDocument.document` with `lastDocument` inherited from `Task`). It works when the member is declared locally; declare the member on the subtype or avoid the inherited navigation.
- A non-principal `SYSTEM` actor (an unmapped transfer object with `kind = SYSTEM`, no principal) still receives `realm = DEFAULT` in the generated ASM and a default `MenuItemAccess`; remove or ignore the menu item so the actor is not surfaced in the UI.
- CRUD flags are declared on the relation members, not once on a transfer object. The REST endpoints of a relation are only generated when the relation carries the corresponding create/update/delete flag; the entity DAO always keeps full CRUD. A lean transfer object therefore hides mutations from a system actor.
