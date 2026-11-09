## Overview

The DocumentRegistry entity's sequence numbering is managed by a `RegistryService` that atomically retrieves and increments the next document number, accounting for financial periods and transition periods.

## Implementation Pattern

- `RegistryServiceImpl` is an OSGi `@Component` implementing the `RegistryService` interface with a single method: `getNextRegistryNumberForDate(DocumentType, LocalDate)`
- The method is `synchronized` to prevent concurrent sequence conflicts
- Sequence resolution follows a two-phase period lookup: (1) check if current date falls within a transition period, (2) if not, use the financial period matching the current date; if in a transition period, use the financial period matching the target date
- The method queries `DocumentRegistryDao` with `filterByDocumentType()` and date range filters (`filterByFinancialPeriodStart/End` or `filterByTransitionPeriodStart/End`)
- The `currentIndex` is incremented (or initialized from `startIndex` if null), persisted via `documentRegistryDao.update()`, and the formatted registry number is returned as `prefix + paddedIndex`
- Padding uses the digit count of `endIndex` to determine zero-fill width (e.g., endIndex=9999 produces 4-digit padding)
- Document generation operations (e.g., `GenerateFaultRegistryDocumentCustomImplementation`, `GenerateOfferDocumentCustomImplementation`) call `registryService.getNextRegistryNumberForDate()` to assign sequential document numbers

## Examples

### rackinspect
- Key files: `common/utils/services/RegistryService.java`, `common/utils/services/impl/RegistryServiceImpl.java`
- Pattern: `synchronized` method queries `DocumentRegistryDao` for the matching period, increments `currentIndex`, updates the entity, returns `prefix + zeroPaddedIndex`
- Notable: Supports transition periods (overlapping financial year boundaries) where the target date determines which period's sequence to use; six document types (FAULT_REGISTRY, OFFER, ASSESSMENT_SHEET, REVIEW_REPORT, JOB_SHEET, WORK_REPORT) each maintain independent registries
- Registry instances are seeded by the `ExcelDataImporter` during initialization with prefix, period boundaries, and start/end indices
