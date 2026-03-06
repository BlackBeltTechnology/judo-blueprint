---
id: "standard-type-and-measure-library"
title: "Standard Type and Measure Library (Shared Type System)"
score: 46.0
usage_count: 8
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - bhs-global-operation
  - viterra_demo
  - InterfaceRegister
  - mjsz
  - sanctuary-backend
  - doors-model
  - ams-model
  - skillmatrix-model
---
## Description

A standardized type system and comprehensive SI measurement unit library embedded in a JUDO model. The structure consists of:

- **types package** -- defines primitive data types: numeric types (Long, Integer, Double, Float) with specific precision/scale, string types (String, Phone, Text, URL, Email) with varying maxLength constraints, a Boolean type, a Date type, a Timestamp type, and a Time type. Some projects add domain-specific string types (e.g., IPV4Address, IPV6Address, FinancialCode, LegalCode, CompanyCode, DivisionCode, ContractTypeTemplate, ContractTemplate, SignedContract, CampaignDocument).
- **measures package** -- defines physical measure categories (Mass, Length, Time, Temperature, Area, Volume, Velocity, Acceleration, Momentum, Force, Work, Power, Frequency, Pressure, Density, ElectricCurrent, ThermodynamicTemperature, AmountOfSubstance, LuminousIntensity, ElectricCharge, ElectricPotential, Capacitance, ElectricalResistance, ElectricalConductance, MagneticFlux, MagneticFluxDensity, Inductance, Illuminance) with a full set of SI units (79 total) including metric prefixes (milli, centi, deci, kilo, mega, etc.) and derived units (km/h, m/s, kg/m3, etc.).

This pattern provides a standardized type vocabulary across an organization's JUDO projects, ensuring consistent precision, scale, string length constraints, and measurement units. In some projects (bhs-global-operation) it exists as a standalone type-only model for import. In others (viterra_demo, InterfaceRegister, mjsz, sanctuary-backend, doors-model, ams-model, kozut-eugyfel-client, skillmatrix-model) it is embedded directly within the application model alongside domain entities. The type and measure definitions are virtually identical across projects, indicating a shared organizational standard.

The string types include domain-aware subtypes: Phone (maxLength: 20) for phone numbers, Email (maxLength: 255) for email addresses, URL (maxLength: 1024) for web addresses, and Text (maxLength: 250, 1000, or 2000) for short text fields, in addition to a general-purpose String (maxLength: 255).

## Detection Query

```graphql
{ esm { packages(limit: 10) {
  items { fqn name }
  totalCount
} } }
```

Look for packages named "types" and "measures" containing the standard type and measure definitions.

```graphql
{ esm { measures(limit: 50) {
  items { fqn name units { totalCount } }
  totalCount
} } }
```

Look for a high measure count (20+) covering standard SI categories.

## Creation Mutations

### Types package

```graphql
mutation { create(input: { package: {
  container: "{{ROOT_NAMESPACE}}", name: "types"
} }) { success fqn } }
```

### Numeric types

```graphql
mutation { create(input: { numericType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "Long",
  precision: 18, scale: 0
} }) { success fqn } }
```

```graphql
mutation { create(input: { numericType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "Integer",
  precision: 9, scale: 0
} }) { success fqn } }
```

```graphql
mutation { create(input: { numericType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "Double",
  precision: 15, scale: 4
} }) { success fqn } }
```

```graphql
mutation { create(input: { numericType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "Float",
  precision: 7, scale: 4
} }) { success fqn } }
```

### String types

```graphql
mutation { create(input: { stringType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "String",
  maxLength: 255
} }) { success fqn } }
```

```graphql
mutation { create(input: { stringType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "Phone",
  maxLength: 20
} }) { success fqn } }
```

```graphql
mutation { create(input: { stringType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "Text",
  maxLength: 250
} }) { success fqn } }
```

```graphql
mutation { create(input: { stringType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "URL",
  maxLength: 1024
} }) { success fqn } }
```

```graphql
mutation { create(input: { stringType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "Email",
  maxLength: 255
} }) { success fqn } }
```

### Other primitive types

```graphql
mutation { create(input: { booleanType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "Boolean"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dateType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "Date"
} }) { success fqn } }
```

```graphql
mutation { create(input: { timestampType: {
  container: "{{ROOT_NAMESPACE}}::types", name: "Timestamp"
} }) { success fqn } }
```

### Measures package

```graphql
mutation { create(input: { package: {
  container: "{{ROOT_NAMESPACE}}", name: "measures"
} }) { success fqn } }
```

### Measure definitions (example: Mass)

```graphql
mutation { create(input: { measure: {
  container: "{{ROOT_NAMESPACE}}::measures", name: "{{MEASURE_NAME}}"
} }) { success fqn } }
```

### Unit definitions (example: kilogram for Mass)

```graphql
mutation { create(input: { unit: {
  container: "{{ROOT_NAMESPACE}}::measures::{{MEASURE_NAME}}", name: "{{UNIT_NAME}}", symbol: "{{SYMBOL}}"
} }) { success fqn } }
```

## Examples

### bhs-global-operation
- **Root namespace**: `BHSGlobalOperation`
- **Packages**: `BHSGlobalOperation::types`, `BHSGlobalOperation::measures`

**Types (12 total):**
- Numeric: Long (18,0), Integer (9,0), Double (15,4), Float (7,4)
- String: String (255), Phone (20), Text (250), URL (1024), Email (255)
- Boolean: Boolean
- Temporal: Date, Timestamp

**Measures (28 total, 79 units):**
- Mass (6 units): milligram, gram, dekagram, kilogram, quintal, tonne
- Time (6 units): millisecond, second, minute, hour, day, week
- Length (10 units): nanometre, micrometre, millimetre, centimetre, decimetre, metre, kilometre, inch, foot, mile
- Temperature (1 unit): celsius
- Area (6 units): squareMillimetre, squareCentimetre, squareDecimetre, squareMetre, hectare, squareKilometre
- Volume (9 units): cubicMillimetre, cubicCentimetre, cubicDecimetre, cubicMetre, millilitre, centilitre, decilitre, litre, hectolitre
- Velocity (2 units): kilometrePerHour, metrePerSecond
- Acceleration (1 unit): metrePerSecondSquared
- Momentum (1 unit): kilogramMetrePerSecond
- Force (1 unit): newton
- Work (5 units): joule, kilojoule, megajoule, watthour, kilowatthour
- Power (3 units): watt, kilowatt, megawatt
- Frequency (4 units): hertz, kilohertz, megahertz, gigahertz
- Pressure (2 units): pascal, hectopascal
- Density (2 units): kilogramPerCubicMetre, gramPerCubicCentimetre
- ElectricCurrent (2 units): milliampere, ampere
- ThermodynamicTemperature (1 unit): kelvin
- AmountOfSubstance (1 unit): mol
- LuminousIntensity (1 unit): candela
- ElectricCharge (1 unit): coulomb
- ElectricPotential (2 units): volt, kilovolt
- Capacitance (4 units): pikofarad, nanofarad, microfarad, farad
- ElectricalResistance (3 units): microohm, milliohm, ohm
- ElectricalConductance (1 unit): siemens
- MagneticFlux (1 unit): weber
- MagneticFluxDensity (1 unit): tesla
- Inductance (1 unit): henry
- Illuminance (1 unit): lux

**No domain entities, transfer objects, enumerations, or actors.** This is a pure shared type library model intended for import by application models.

### viterra_demo
- **Root namespace**: `viterra`
- **Packages**: `viterra::types`, `viterra::measures`

**Types (13 total):**
- Numeric: Long (18,0), Integer (9,0), Double (15,4), Float (7,4)
- String: String (255), Phone (20), Text (250), URL (1024), Email (255, with regex validation)
- Boolean: Boolean
- Temporal: Date, Timestamp (second), Time (second)

**Measures (28 total, identical SI categories to bhs-global-operation):**
- Same 28 measure categories with same unit definitions as bhs-global-operation
- Mass (6), Time (6), Length (10), Temperature (1), Area (6), Volume (9), Velocity (2), Acceleration (1), Momentum (1), Force (1), Work (5), Power (3), Frequency (4), Pressure (2), Density (2), ElectricCurrent (2), ThermodynamicTemperature (1), AmountOfSubstance (1), LuminousIntensity (1), ElectricCharge (1), ElectricPotential (2), Capacitance (4), ElectricalResistance (3), ElectricalConductance (1), MagneticFlux (1), MagneticFluxDensity (1), Inductance (1), Illuminance (1)

**Differences from bhs-global-operation:**
- Adds a Time type (not present in bhs-global-operation)
- Email type includes a regex validation pattern
- This is NOT a standalone library -- the same model also contains domain entities (Period, Client, Silo, Stock, Commodity, Report, Application), enumerations (Status, ReportStatus), transfer objects, and actor types

### InterfaceRegister
- **Root namespace**: `InterfaceRegister`
- **Packages**: `InterfaceRegister::types`, `InterfaceRegister::measures`

**Types (16 total):**
- Numeric: Long (18,0), Integer (9,0), Double (15,4), Float (7,4)
- String: String (255), Phone (20), Text (250), URL (1024), Email (255)
- Domain-specific string types: IPV4Address (32), IPV6Address (200)
- Boolean: Boolean
- Binary: BinaryType
- Temporal: Date, Timestamp, Time

**Measures (28 total, 79 units, identical SI categories):**
- Same 28 measure categories and 79 units as bhs-global-operation and viterra_demo
- Acceleration (1), AmountOfSubstance (1), Area (6), Capacitance (4), Density (2), ElectricCharge (1), ElectricCurrent (2), ElectricPotential (2), ElectricalConductance (1), ElectricalResistance (3), Force (1), Frequency (4), Illuminance (1), Inductance (1), Length (10), LuminousIntensity (1), MagneticFlux (1), MagneticFluxDensity (1), Mass (6), Momentum (1), Power (3), Pressure (2), Temperature (1), ThermodynamicTemperature (1), Time (6), Velocity (2), Volume (9), Work (5)

**Differences from other projects:**
- Adds domain-specific string types IPV4Address (maxLength: 32) and IPV6Address (maxLength: 200) for network address validation
- Adds a BinaryType for document/file attachments on InterfaceSpecification entities
- This is embedded within the application model alongside 24 domain entities, 8 enumerations, 21 transfer objects, and 1 actor type

### mjsz
- **Root namespace**: `mjsz`
- **Packages**: `mjsz::types`, `mjsz::measures`

**Types (13 total):**
- Numeric: Long (18,0), Integer (9,0), Double (15,4), Float (7,4)
- String: String (255), Phone (20), Text (250), URL (1024), Email (255, with regex validation)
- Boolean: Boolean
- Temporal: Date, Timestamp (second), Time (second)

**Measures (28 total, identical SI categories):**
- Same 28 measure categories and unit definitions as bhs-global-operation, viterra_demo, and InterfaceRegister
- Mass (6), Time (6), Length (10), Temperature (1), Area (6), Volume (9), Velocity (2), Acceleration (1), Momentum (1), Force (1), Work (5), Power (3), Frequency (4), Pressure (2), Density (2), ElectricCurrent (2), ThermodynamicTemperature (1), AmountOfSubstance (1), LuminousIntensity (1), ElectricCharge (1), ElectricPotential (2), Capacitance (4), ElectricalResistance (3), ElectricalConductance (1), MagneticFlux (1), MagneticFluxDensity (1), Inductance (1), Illuminance (1)

**Differences from other projects:**
- Type set is identical to viterra_demo (13 types including Time, Email with regex)
- Embedded within an application model containing 10 domain entities (sports league management), 7 transfer objects, and 1 actor type
- No enumerations in this project

### sanctuary-backend
- **Root namespace**: `Sanctuary`
- **Packages**: `Sanctuary::types`, `Sanctuary::measures`

**Types (13 total):**
- Numeric: Long (18,0), Integer (9,0), Double (15,4), Float (7,4)
- String: String (255), Phone (20), Text (250), URL (1024), Email (255, with regex validation)
- Boolean: Boolean
- Temporal: Date, Timestamp (second), Time (second)

**Measures (28 total, 79 units, identical SI categories):**
- Same 28 measure categories and 79 unit definitions as all other projects
- Mass (6), Time (6), Length (10), Temperature (1), Area (6), Volume (9), Velocity (2), Acceleration (1), Momentum (1), Force (1), Work (5), Power (3), Frequency (4), Pressure (2), Density (2), ElectricCurrent (2), ThermodynamicTemperature (1), AmountOfSubstance (1), LuminousIntensity (1), ElectricCharge (1), ElectricPotential (2), Capacitance (4), ElectricalResistance (3), ElectricalConductance (1), MagneticFlux (1), MagneticFluxDensity (1), Inductance (1), Illuminance (1)

**Differences from other projects:**
- Type set is identical to viterra_demo and mjsz (13 types including Time, Email with regex)
- Embedded within an application model containing 6 domain entities (user management), 6 transfer objects, 2 enumerations, and 1 actor type
- The model has several empty placeholder packages (unit, article, project, faq) suggesting the project is in early development

### doors-model
- **Root namespace**: `doors`
- **Packages**: `doors::types`, `doors::measures`

**Types (19 total):**
- Numeric: Long (18,0), Integer (9,0), Double (15,4), Float (7,4)
- String: String (255), Phone (20), Text (1000), URL (1024), Email (255)
- Domain-specific string types: FinancialCode (6), LegalCode (6), CompanyCode (6), DivisionCode (6), ContractTypeTemplate (100), ContractTemplate (100), SignedContract (100)
- Boolean: Boolean
- Temporal: Date, Timestamp (second)

**Measures (28 total, 79 units, identical SI categories):**
- Same 28 measure categories and 79 unit definitions as all other projects
- Mass (6), Time (6), Length (10), Temperature (1), Area (6), Volume (9), Velocity (2), Acceleration (1), Momentum (1), Force (1), Work (5), Power (3), Frequency (4), Pressure (2), Density (2), ElectricCurrent (2), ThermodynamicTemperature (1), AmountOfSubstance (1), LuminousIntensity (1), ElectricCharge (1), ElectricPotential (2), Capacitance (4), ElectricalResistance (3), ElectricalConductance (1), MagneticFlux (1), MagneticFluxDensity (1), Inductance (1), Illuminance (1)

**Differences from other projects:**
- Text type has maxLength 1000 instead of the usual 250
- Adds 7 domain-specific string types for contract management codes and document templates (FinancialCode, LegalCode, CompanyCode, DivisionCode, ContractTypeTemplate, ContractTemplate, SignedContract), all with short maxLength (6 or 100)
- No Time type (unlike viterra_demo, mjsz, sanctuary-backend)
- This is embedded within a large application model containing 27 entity types, 10 enumerations, 36 transfer objects, and 2 actor types (contract management domain)

### ams-model
- **Root namespace**: `ams`
- **Packages**: `ams::types`, `ams::measures`

**Types (13 total):**
- Numeric: Long (18,0), Integer (9,0), Double (15,4), Float (7,4)
- String: String (255), Phone (20), Text (2000), URL (1024), Email (255, with regex validation)
- Domain-specific string type: CampaignDocument (1024)
- Boolean: Boolean
- Temporal: Date, Timestamp (second)

**Measures (28 total, 79 units, identical SI categories):**
- Same 28 measure categories and 79 unit definitions as all other projects
- Mass (6), Time (6), Length (10), Temperature (1), Area (6), Volume (9), Velocity (2), Acceleration (1), Momentum (1), Force (1), Work (5), Power (3), Frequency (4), Pressure (2), Density (2), ElectricCurrent (2), ThermodynamicTemperature (1), AmountOfSubstance (1), LuminousIntensity (1), ElectricCharge (1), ElectricPotential (2), Capacitance (4), ElectricalResistance (3), ElectricalConductance (1), MagneticFlux (1), MagneticFluxDensity (1), Inductance (1), Illuminance (1)

**Differences from other projects:**
- Text type has maxLength 2000 (the largest across all projects; bhs/viterra/InterfaceRegister/mjsz/sanctuary use 250, doors uses 1000)
- Adds a domain-specific CampaignDocument string type (maxLength: 1024) for campaign export documents
- Email type includes regex validation pattern (like viterra_demo, mjsz, sanctuary-backend)
- No Time type (like bhs-global-operation and doors-model)
- Embedded within an application model containing 7 entity types, 3 enumerations, 7 transfer objects, and 2 actor types (access management system domain)

### kozut-eugyfel-client
- **Root namespace**: `e_ugyfelszolgalat`
- **Packages**: `e_ugyfelszolgalat::types`, `e_ugyfelszolgalat::measures`

**Types (12 total):**
- Numeric: Long (18,0), Integer (9,0), Double (15,4), Float (7,4)
- String: String (255), Phone (20), Text (250), URL (1024), Email (255, with regex validation)
- Boolean: Boolean
- Temporal: Date, Timestamp

**Measures (28 total, 79 units, identical SI categories):**
- Same 28 measure categories and 79 unit definitions as all other projects
- Mass (6), Time (6), Length (10), Temperature (1), Area (6), Volume (9), Velocity (2), Acceleration (1), Momentum (1), Force (1), Work (5), Power (3), Frequency (4), Pressure (2), Density (2), ElectricCurrent (2), ThermodynamicTemperature (1), AmountOfSubstance (1), LuminousIntensity (1), ElectricCharge (1), ElectricPotential (2), Capacitance (4), ElectricalResistance (3), ElectricalConductance (1), MagneticFlux (1), MagneticFluxDensity (1), Inductance (1), Illuminance (1)

**Differences from other projects:**
- Type set matches bhs-global-operation (12 types, no Time type)
- Email type includes regex validation pattern (like viterra_demo, mjsz, sanctuary-backend)
- Text type has maxLength 250 (standard)
- Embedded within an application model containing 12 entity types, 4 enumerations, multiple transfer objects, and 3 actor types (customer service / complaint management domain)

### skillmatrix-model
- **Root namespace**: `SkillMatrix`
- **Packages**: `SkillMatrix::types`, `SkillMatrix::measures`

**Types (12 total):**
- Numeric: Long (18,0), Integer (9,0), Double (15,4), Float (7,4)
- String: String (255), Phone (20), Text (2000), URL (1024), Email (255, with regex validation)
- Boolean: Boolean
- Temporal: Date, Timestamp (second)

**Measures (28 total, 79 units, identical SI categories):**
- Same 28 measure categories and 79 unit definitions as all other projects
- Mass (6), Time (6), Length (10), Temperature (1), Area (6), Volume (9), Velocity (2), Acceleration (1), Momentum (1), Force (1), Work (5), Power (3), Frequency (4), Pressure (2), Density (2), ElectricCurrent (2), ThermodynamicTemperature (1), AmountOfSubstance (1), LuminousIntensity (1), ElectricCharge (1), ElectricPotential (2), Capacitance (4), ElectricalResistance (3), ElectricalConductance (1), MagneticFlux (1), MagneticFluxDensity (1), Inductance (1), Illuminance (1)

**Differences from other projects:**
- Text type has maxLength 2000 (matching ams-model)
- Email type includes regex validation pattern
- No Time type (like bhs-global-operation, doors-model, ams-model)
- Embedded within an application model containing 20 entity types, 1 enumeration, 36 transfer objects, and 4 actor types (skill matrix / HR competence management domain)
