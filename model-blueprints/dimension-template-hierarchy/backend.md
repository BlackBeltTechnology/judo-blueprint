## Overview

The dimension template hierarchy is managed through interceptors for template/group CRUD validation, custom operations for template parameter retrieval, and a shared `DimensionService` that handles validation logic and template instantiation.

## Implementation Pattern

- `DimensionTemplateCreateInterceptor` and `DimensionTemplateUpdateInterceptor` validate template structure in `preCall`: ensure at least one group exists, then delegate to `DimensionService.validateDimensionTemplate()` for deeper checks
- In `postCall`, both interceptors auto-generate the template name via `DimensionService.calculateDimensionTemplateName()` if the name is blank
- `DimensionTemplateGroupUpdateInterceptor` validates group-level constraints: calls `DimensionService.validateGroupRelations()` and `validateGroupParametersMatch()` to ensure groups and parameters are consistent with the template type (RACK vs RACK_ELEMENT)
- `GetTemplateParametersCustomImplementation` retrieves a template's group hierarchy by ID and returns it as a `DimensionTemplateParametersGetterOutput` DTO -- used to populate dynamic forms
- `QueryTemplateGroupCustomImplementation` queries a DimensionGroup's linked template group with full parameter masks (including selectable values) for the instance-to-template back-reference
- `GetDimensionTemplateParametersCustomImplementation` retrieves template parameters starting from a RackElement (traversing the dimensionTemplate relation)
- The `DimensionService` (common module) is an OSGi `@Component` with validation methods and a `DimensionInterceptorService` handles dimension group creation during rack operations

## Examples

### rackinspect
- Key files: `interceptors/dimensiontamplate/DimensionTemplateCreateInterceptor.java`, `interceptors/dimensiontamplate/DimensionTemplateUpdateInterceptor.java`, `interceptors/dimensiontamplate/dimensiontemplategroup/DimensionTemplateGroupUpdateInterceptor.java`, `custom/.../dimensiontemplate/GetTemplateParametersCustomImplementation.java`, `custom/.../dimensiongroup/QueryTemplateGroupCustomImplementation.java`, `custom/.../rackelement/GetDimensionTemplateParametersCustomImplementation.java`, `common/services/DimensionService.java`
- Pattern: Interceptors validate template structure (min 1 group, group-parameter consistency); `DimensionService` provides shared validation and name calculation; custom operations return template parameters for dynamic form rendering
- Notable: Template name auto-generation in `postCall` when left blank; group validation differentiates between RACK and RACK_ELEMENT template types; `RackInspectI18n` provides localized error messages
- The `ExcelDataImporter` seeds initial dimension templates with groups and parameters from Excel spreadsheets during initialization
