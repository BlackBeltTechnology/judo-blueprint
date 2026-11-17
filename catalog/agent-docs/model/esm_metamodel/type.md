---
title: type Package Reference
description: Reference of the ESM type package: primitive types, enumerations, cardinality and attribute rules.
aliases: [primitive data types in model, numeric precision and scale, enumeration values, binary file type, cardinality lower upper, required type attributes]
keywords: [StringType, NumericType, BinaryType, EnumerationType, EnumerationMember, Cardinality, maxLength, precision, scale, mimeTypes, maxFileSize, ordinal]
tags: [domain:model, layer:model, status:platform]
---

# `type` Package Reference

**[◄ Back to Index](./README.md)**

This package defines the logical, platform-independent data types used throughout the model. These types are abstract and are meant to be mapped to concrete physical types by a code generator for a specific target platform (e.g., a `StringType` might become a `VARCHAR` in SQL or a `java.lang.String` in Java).

---

## Primitive Types
These are the basic, indivisible data types. All inherit from the abstract `Primitive` element.

| Element | Description | Key Attributes / References |
| :--- | :--- | :--- |
| **`StringType`** | Represents a sequence of characters. | `maxLength` (Integer, Required), `regExp` (String) |
| **`NumericType`** | Represents a number with fixed precision. | `precision` (Integer, Required), `scale` (Integer, Required) |
| **`BooleanType`** | Represents a `true` or `false` value. | - |
| **`DateType`** | Represents a calendar date (year, month, day). | - |
| **`TimeType`** | Represents a time of day. | `baseUnit` (`DurationType` Enum: `second`, `millisecond`, etc.) |
| **`TimestampType`** | Represents a specific point in time (date and time). | `baseUnit` (`DurationType` Enum) |
| **`BinaryType`** | Represents binary data, such as a file. | `maxFileSize` (Long), `mimeTypes` (`MimeType`, 1..*) |
| **`PasswordType`**| A specialized string type that implies masked UI widgets and secure handling. **Not usable in a generated application:** the PSM→ASM transformation throws `Password type is not supported yet.` | - |
| **`CustomType`**| A primitive type whose implementation is defined externally. | - |
| **`XMLType`**| A string-based type that represents XML content. **Not usable in a generated application:** the PSM→ASM transformation throws `XML type is not supported yet.` | `xmlNamespace` (String), `xmlElement` (String) |


## Enumeration Types

### `EnumerationType`
A type that has a predefined, finite set of named values (e.g., `Status { NEW, PENDING, CLOSED }`).

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of the enumeration type. |
| `members` | `EnumerationMember` | `[1..*]` | The list of possible values for this enumeration. |

### `EnumerationMember`
A single, named value within an `EnumerationType`.

| Attribute / Reference | Type | Cardinality | Description |
| :--- | :--- | :--- | :--- |
| `name` | String | `[1]` | The name of the enumeration member (e.g., "PENDING"). |
| `ordinal`| Integer | `[1]` | The numeric value associated with the member. |

## Cardinality

### `Cardinality` (Abstract)
Defines the multiplicity (or allowed number of elements) of a relationship. It is inherited by relationship members.

| Attribute / Reference | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `lower` | Integer | `0` | The minimum number of elements in the relationship. A value of `1` or more indicates a required relationship. |
| `upper` | Integer | `-1` | The maximum number of elements. A value of `-1` signifies an unbounded (many) relationship. |

---

## Behaviour Rules

These rules define how type elements behave based on their context and attribute values.

### StringType Attribute Rules

| Attribute | Required | Description |
|-----------|----------|-------------|
| `maxLength` | Yes | Maximum allowed length of the string |
| `regExp` | No | Regular expression for validation |

### NumericType Attribute Rules

| Attribute | Required | Default | Description |
|-----------|----------|---------|-------------|
| `precision` | Yes | 9 | Maximum total decimal digits (left + right of decimal point) |
| `scale` | Yes | 0 | Decimal digits to the right of decimal point |

**Precision vs Scale:**
- `precision` = total digits stored
- `scale` = digits after decimal point
- Digits before decimal = `precision - scale`

**Example:** `precision=9, scale=2` → max value `9999999.99`

### TimestampType Attribute Rules

| Attribute | Required | Description |
|-----------|----------|-------------|
| `baseUnit` | Yes | Duration unit enum: `second`, `millisecond`, etc. |

### TimeType Attribute Rules

| Attribute | Required | Description |
|-----------|----------|-------------|
| `baseUnit` | Yes | Duration unit enum: `second`, `millisecond`, etc. |

### BinaryType Attribute Rules

| Attribute | Required | Default | Description |
|-----------|----------|---------|-------------|
| `maxFileSize` | No | 52428800 (50MB) | Maximum upload size in bytes |
| `mimeTypes` | Yes (1..*) | - | Allowed MIME types |

**MimeType Format:** `type/subType` (e.g., `image/png`, `application/pdf`)

**MimeType Candidates:** Selected from `Model.mimeTypes` collection.

**`MimeType` attribute rules:** only `type` and `subType` — no `name`, no `label`. Adding `name="image/png"` fails ESM transform with `Feature 'name' not found`.

**Declaration site:** `<mimeTypes>` is a direct child of the root `<namespace:Model>`; `BinaryType.mimeTypes` references them as a space-separated id list (`mimeTypes="_id1 _id2"`).

Omitting `mimeTypes` on a `BinaryType` fails EMF validation: *"The feature 'mimeTypes' … with 0 values must have at least 1 values"*.

### EnumerationType Attribute Rules

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Enumeration type name |
| `members` | Yes (1..*) | List of enumeration members |

**Numeric to Java mapping.** The SDK generator (`JavaApiHelper`) chooses the Java type from precision and scale: integer numerics with precision 1-9 become `java.lang.Integer`, 10-19 `java.lang.Long`, larger ones `java.math.BigDecimal`; decimal numerics with precision 1-7 and scale at most 4 become `java.lang.Float`, precision 8-15 with scale at most 4 `java.lang.Double`, anything else `java.math.BigDecimal`. `BinaryType` becomes `hu.blackbelt.judo.dispatcher.api.FileType`; an unmapped data type falls back to `java.lang.Object`.

**JSL binary modifiers.** In JSL a binary primitive declares both `mime-type:` (entries `type/subtype`, the subtype may be `*`; the keyword is the singular `mime-type`) and `max-file-size:`. The size takes an optional unit: decimal `KB`/`MB`/`GB` (1000-based) or binary `KiB`/`MiB`/`GiB` (1024-based); the unit needs an uppercase `K`, so `kB` does not parse. Values are converted to bytes.

### EnumerationMember Attribute Rules

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Member name (e.g., `PENDING`) |
| `ordinal` | Yes | Integer value (auto-generated); must be unique within the enumeration and, in JSL models, between 0 and 9999 |

**On Member Creation:**
- `ordinal` = `getNextOrdinal()` (auto-incremented)
- `name` = `LITERAL_` + `ordinal` (default, can be changed)

### FlatPrimitiveType (No Extra Attributes)

These types share a common properties page with only base attributes:

| Type | Description |
|------|-------------|
| `BooleanType` | True/false values |
| `DateType` | Calendar date |
| `PasswordType` | Masked string |
| `CustomType` | External implementation |

### XMLType Attribute Rules

| Attribute | Required | Description |
|-----------|----------|-------------|
| `xmlNamespace` | No | XML namespace URI |
| `xmlElement` | No | XML root element name |

### Type-to-UI Widget Mapping

When a `DataField` is bound to a `DataMember`, the available widget properties depend on the `dataType`:

| DataType | UI Property Group | Widget Options |
|----------|-------------------|----------------|
| `StringType` | String widget properties | `textWidget`, `textMultiLine`, `textMask`, `isTypeAheadField`, `textCountCharacters` |
| `NumericType` | Numeric widget properties | `formatValue`, `minValueBy`, `maxValueBy` |
| `BooleanType` | Boolean widget properties | `booleanWidget`, `valueLabelPlacement` |
| `DateType` | Date widget properties | `minValueBy`, `maxValueBy` |
| `TimestampType` | Timestamp widget properties | `minValueBy`, `maxValueBy` |
| `TimeType` | Time widget properties | `minValueBy`, `maxValueBy` |
| `EnumerationType` | Enumeration widget properties | `enumWidget` |
| `BinaryType` | Binary widget properties | File upload |

### Default Values on Type Creation

| Type | Attribute | Default |
|------|-----------|---------|
| `NumericType` | `precision` | 9 |
| `NumericType` | `scale` | 0 |
| `BinaryType` | `maxFileSize` | 52428800 (50MB) |
| `EnumerationMember` | `ordinal` | Auto-incremented |
| `EnumerationMember` | `name` | `LITERAL_` + ordinal |

String type limits are model data, not platform constants; the platform enforces a string type's `maxLength` with `MAX_LENGTH_VALIDATION_FAILED`. *Verify:* the seeded string and numeric types of a new model (names, `maxLength`, `regExp`) against the project template before documenting them.

### Cardinality Conventions

| Display | lower | upper | Meaning |
|---------|-------|-------|---------|
| `0..1` | 0 | 1 | Optional single |
| `1..1` | 1 | 1 | Required single |
| `0..*` | 0 | -1 | Optional many |
| `1..*` | 1 | -1 | Required many |

---

## Related Documentation

- [Structure Package](./structure.md) - DataMember uses types via `dataType` reference
- [UI Behaviour Rules](./ui-behaviour.md) - Type-specific widget rules
- [UI Package](./ui.md) - DataField widget definitions