## Examples

### rackinspect
**Template layer:**
- `DimensionTemplate` -- name, type (DimensionTemplateType: RACK/RACK_ELEMENT); composes groups (0..*)
- `DimensionTemplateGroup` -- name (req), label (req), order (req), attributePerRow (default: 3), multiLine (default: false), isRequired (default: false); composes parameters (0..*)
- `DimensionTemplateParameter` -- name (req), label (req), order (req), valueType (req, ValueType enum), isRequired (default: false), isInSimpleReviewReport (default: false); relations: unit (0..1 ASSOC to Unit), selectableValues (0..* ASSOC to SelectableValue)

**Instance layer:**
- `DimensionGroup` -- name (req), label (req), order (req), attributePerRow (default: 3), multiLine (default: false), isRequired (default: false); composes parameters (0..*) and rows (0..*); relation: dimensionTemplateGroup (1..1 ASSOC back to template)
- `DimensionGroupRow` -- order (req); composes parameters (0..*)
- `DimensionParameter` -- name (req), label (req), order (req), valueType (req), numericValue, stringValue, booleanValue, unitName, isRequired (default: false), isInSimpleReviewReport (default: false); relations: dimensionTemplateParameter (1..1 ASSOC), selectedValue (0..1 ASSOC to SelectableValue)

**Supporting entities:**
- `SelectableValue` -- name (req), order (req) -- predefined dropdown options for ENUM-typed parameters
- `ValueType` enum -- NUMERIC(1), STRING(2), ENUM(3), BOOLEAN(4)
- `DimensionTemplateType` enum -- RACK(1), RACK_ELEMENT(2)
