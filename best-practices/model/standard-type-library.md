---
id: "standard-type-library"
title: "Standard Primitive Type and Measures Library"
domain: "model"
category: "type"
score: 328.5
usage_count: 22
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - rackinspect
  - itracker
  - skillmatrix-frontend
  - actiongroup-test-react
  - alba
  - skillmatrix-model
  - mlszksz-platform
  - viterra_demo
  - bhs-global-operation
  - kuzut-test-eugyfel-model
  - mjsz
  - judo-demo-miniworkflow
  - ams-model
  - sanctuary-backend
  - park-here
  - InterfaceRegister
  - judo-partner
  - kozut-eugyfel-model-test
  - workflow-poc
  - reserve-app
  - ams-frontend
---
## Description

JUDO projects include a standard library of primitive types and physical measures in dedicated packages (`types` and `measures`). The types package provides String (max 255), Text (max 4000), Email (regex-validated), Phone, URL, Long, Integer, Double, Float, Boolean, Date, Timestamp, and Time. The measures package includes 28+ SI unit measures. These are included by default and reused across all entities.

## Structure

- `<root>::types` package: 13 primitive types covering strings, numerics, boolean, date/time
- `<root>::measures` package: 28+ physical measures (Mass, Time, Length, Temperature, etc.)
- Key type characteristics:
  - `String`: max 255 chars (general purpose)
  - `Text`: max 4000 chars (descriptions, long content) -- but some projects use max 250 or 2000
  - `Email`: max 255 chars with regex validation
  - `Integer`: precision 9
  - `Long`: precision 18
  - `Timestamp`: base unit second
- Binary types defined at model root (e.g., `JSON` with application/json MIME)

## Examples

### Trivia
Uses `String` (names, codes, IDs), `Text` (question text, descriptions), `Email` (user/admin emails with regex), `Long` (question identifier), `Integer` (scores, durations, counts), `Boolean` (active flags), `Timestamp` (creation/start/finish times). Measures package included but unused by domain entities.

### RackInspect
Uses the same types package (`rackinspect::types`) plus custom `Numeric` type. Timestamps for audit trails (`Timestamp!now()`), Email for notifications and actor variable defaults (`Email!getVariable('ACTOR', 'email')`). Binary types used for documents (PDF), images (pictures), and logos. Measures package included.

### itracker
Standard 13 types in `itracker::types`. Notable: `Text` max length is 250 (not 4000 as in other projects), `Double` (precision 15, scale 4) and `Float` (precision 7, scale 4) for financial amounts. Uses `Integer` for sequence IDs (not Long). Measures package included but unused. No binary types defined.

### SkillMatrix
Standard 12 types in `SkillMatrix::types` including `Phone` (maxLength=20), `Text` (maxLength=2000), `URL` (maxLength=1024), and `Email` (maxLength=255, regex-validated). Uses `Double` (precision 15, scale 4) and `Float` (precision 7, scale 4). Measures package included as `SkillMatrix::measures`.

### ActionGroupTest
Custom domain-specific types: `massInKg` (NumericType, precision=16, scale=2) for mass measurements, `LowerCaseString` (maxLength=127, regex=`^[a-z]*$`) for constrained input, `Phone` (maxLength=20) reused from standard library. System operator enums (`_StringOperation`, `_NumericOperation`, `_BooleanOperation`, `_EnumerationOperation`) define filter operations per type.

### Alba
Standard types in `Alba::types`: String, RichText (for long-form educational content), Email (user identifier), URL (institution website), Boolean, Integer, Timestamp. `Alba::measures` includes comprehensive SI units (length, mass, time, area, volume, temperature). AttachmentType for file uploads. RichText heavily used for educational content fields (areaOfDevelopment, introduction, goal, etc.).

### SkillMatrix-Model
12 standard types in `SkillMatrix::types` confirmed. Distinctive type usage: `String` (max 255) for identifiers/names/codes, `Text` (max 2000) for descriptions/profiles/notes, `URL` (max 1024) for report download links (`Result.excel`). `Phone` (max 20) for user contact. Clear String vs Text distinction observed: `name`, `code`, `email` use String; `description`, `profile` use Text. Measures package included but unused by domain entities.

### MLSZKSZPlatform
13 enumeration types plus standard primitives. Custom numeric types: `Coordinate` (precision 10, scale 7) for latitude/longitude geographic data, `Double` (15,4), `Float` (7,4), `Integer` (9,0), `Long` (18,0). Temporal types: `Timestamp` for event tracking, `Date` for validity periods (Offer.validFrom/validUntil, Request.deadline). String types include `Email`, `Phone`, `URL`, `Text`, `LongText` for various content lengths. Binary type for document file attachments (`Document.file`).

### Viterra Demo
Standard types in `viterra::types`: String, Long, Integer, Double, Float, Boolean, Date, Timestamp, Time, plus specialized Phone, Text, URL, Email (regex-validated). Comprehensive `viterra::measures` package with Mass, Time, Length, Temperature, Area, Volume, Velocity, Acceleration, Momentum, Force, and Work units. Measures are defined but not used by domain entities -- Stock quantities use simple Integer type rather than Mass measures.

### BHS Global Operation
Skeleton project with 14 standard types in `BHSGlobalOperation::types` (Text maxLength=250) and the most comprehensive measures package observed: 25 measures with 100+ units covering all 7 SI base units plus 18 derived quantities (Velocity, Acceleration, Force, Work, Power, Frequency, Pressure, Density, Capacitance, Resistance, etc.). No domain entities defined to consume these types.

### KuzutTestEugyfelModel
12 standard types in `E_Ugyfel::types`: String (255), Long (18), Integer (9), Double (15,4), Float (7,4), Boolean, Date, Timestamp (second), Phone (20), Text (250), URL (1024), Email (255, regex). Comprehensive measures package with 20+ measures (Mass, Time, Length, Temperature, Area, Volume, Velocity, etc.) -- none used by domain entities. Text maxLength=250, matching the itracker/BHS pattern rather than the 4000 default.

### MJSZ
Standard types in `mjsz::types`: String, Long, Integer, Double, Float, Boolean, Date, Timestamp, Time, Phone, Text, URL, Email (regex-validated). Comprehensive `mjsz::measures` package with 9 measures (Mass, Time, Length, Temperature, Area, Volume, Velocity, Acceleration, Momentum, Force, Work). Notable: Boolean type defined but not used in the model -- Integer flags (0/1) used instead for summation support in Match.homeWin/draw/visitorWin.

### judo-demo-miniworkflow
Standard types in `MiniWorkflow::types`: String (255), Text (250), Email (255, regex-validated), Boolean, Timestamp, plus unused Phone, URL, Long, Integer, Double, Float, Date, Time. Binary type `FileType` with `mimeTypes="*/*"` and `maxFileSize="0"` (unlimited) for document attachments. Measures package with 15 measures included but unused. Text maxLength=250, consistent with the itracker/BHS/kozut pattern.

### AMS-Model
13 standard types in `ams::types`: String (255), Long (18), Integer (9), Double (15,4), Float (7,4), Boolean, Date, Timestamp (second), Phone (20), Text (2000), URL (1024), Email (255, regex-validated). Custom domain type: `CampaignDocument` (String, maxLength=1024) for campaign report download URLs. Comprehensive measures package with 25+ measures (Mass through Inductance) -- none used by domain entities. Text maxLength=2000, matching the SkillMatrix pattern.

### Sanctuary Backend
13 standard types in `Sanctuary::types`: String (255), Long (18), Integer (9), Double (15,4), Float (7,4), Boolean, Date, Timestamp (second), Time (second), Phone (20), Text (250), URL (1024), Email (255, regex-validated). Comprehensive measures package with 28 measures covering all 7 SI base units plus 21 derived quantities -- none used by domain entities. The model has the most extensive measures library observed, including Capacitance, ElectricalResistance, Inductance, and Illuminance.

### ParkHere
Standard types in `ParkHere::types` and `ParkHere::measures` packages. Uses String (names, identifiers), Text (email templates, floor plan descriptions), Email (user/doorman identifiers with regex validation), Integer (floor numbers, reservation quotas), Boolean (active flags, role flags, notification tracking), Date (holiday periods, reservation dates), Time (start/end times, working hours, reminder timers), Timestamp (audit timestamps). Notably uses all three temporal types (Date, Time, Timestamp) for different business contexts.

### InterfaceRegister
Standard types in `InterfaceRegister::types` (String, Text, Email, etc.) plus a Binary type for document storage (`specificationDocument`, `openApiDocument`, `WSDLDocument`). Uses URL type for specification links (`linkToTheSpecification`, `linkToOpenApiSpecification`, `linkToWSDLSpecification`). The model uses Binary and URL types in tandem for the "link + document" pattern where specifications can be either referenced by URL or uploaded as binary documents.

### judo-partner
Standard 14 types in `Partner::types` including a custom `TaxNumberHun` string type (maxLength=13, regex `^\d{8}-\d-\d{2}$`) for Hungarian tax number validation, and a `JSON` binary type for bulk import payloads. Text maxLength=250. Measures package with standard SI units included but unused by domain entities.

### KozutEugyfelModelTest
12 standard types in `e_ugyfelszolgalat::types`: String (255), Long (18), Integer (9), Double (15,4), Float (7,4), Boolean, Date, Timestamp (second), Phone (20), Text (250), URL (1024), Email (255, regex). Comprehensive measures package included but unused by domain entities. Text maxLength=250, consistent with related KOZUT projects.

### workflow-poc
Standard 13 types in `workflow::types` (String 255, Long 18, Integer 9, Double 15/4, Float 7/4, Boolean, Date, Timestamp, Time, Phone 20, Text 250, URL 1024, Email 255 with regex). Additional types at model root: `LongText` (String) for extended text and `YAML` (Binary) for workflow definition uploads. Comprehensive measures package with 25+ measures (Mass through Illuminance) -- none used by domain entities.

### ReserveApp
Standard types in `ReserveApp::types`: String, Phone, Text, URL, Email, Long, Integer, Double, Float, Boolean, Date, Timestamp, Time. Comprehensive `ReserveApp::measures` package with 28 measures. Binary type `Picture` defined at root for attachment images. Uses Phone type for both vehicle and loading driver contact numbers.

### AMS-Frontend
13 standard types in `ams::types` plus custom `CampaignDocument` (String, maxLength=1024) for download URLs. Standard set: String (255), Long (18), Integer (9), Double (15,4), Float (7,4), Boolean, Date, Timestamp, Phone (20), Text (2000), URL (1024), Email (regex-validated). Comprehensive measures package included but unused.

## Trade-offs

- Pros: Consistent type definitions across projects, regex validation on Email, measures available if needed
- Cons: Measures package included even when unused, limited customization of standard types
- Prefer when: Always -- this is the standard JUDO type library

## Related Patterns

- [naming-conventions](naming-conventions.md)
