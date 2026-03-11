## Overview

Implements a complete document generation pipeline using XDocReport (Freemarker-templated DOCX files) with multiple conversion backends (docx4j, JODConverter REST), PDF watermarking (PDFBox), and file storage integration. The pipeline spans a dedicated `report` module (template utilities), a `common` module (ReportService orchestrator + supporting services), and the application's FileStoreService for template retrieval and output storage.

## Implementation Pattern

**Module structure:**
```
application/
  report/                  -- XDocReport utility classes (static, no OSGi)
    ReportUtil.java        -- Base DOCX/PDF generation with Freemarker
    OfferReportUtil.java   -- Offer-specific template with logo image
    JobSheetReportUtil.java -- JobSheet template with multiple images
    ReviewReportReportUtil.java -- Review report with photos + dual logos
    ImageProvider.java     -- FileStore-backed image for template embedding
    StreamImageProvider.java -- InputStream-based IImageProvider implementation
  common/
    services/
      ReportService.java              -- Orchestrator interface
      DocumentConversionService.java  -- DOCX-to-PDF conversion interface
      PdfWatermarkService.java        -- PDF watermark overlay interface
      ConfigurationTemplateService.java -- Template retrieval from DB
    services/impl/
      ReportServiceImpl.java          -- Full pipeline orchestration
      DocumentConversionServiceImpl.java -- JODConverter REST client
      PdfWatermarkServiceImpl.java    -- PDFBox watermark implementation
      ConfigurationTemplateServiceImpl.java -- Reads templates from Configuration entity
```

**Report utility classes (report module):**
- Static utility classes, one per document type (assessment sheet, review report, job sheet, offer, work report, completion certificate)
- Load DOCX template via `XDocReportRegistry.getRegistry().loadReport(templateStream, TemplateEngineKind.Freemarker)`
- Create `IContext`, populate with `transferObject.toMap()` (converts Optional values to plain values for Freemarker)
- Image embedding via `FieldsMetadata.addFieldAsImage()` with `NullImageBehaviour.RemoveImageTemplate` for optional images
- PDF generation: write DOCX to temp file, then convert via `ConverterRegistry` (docx4j) with ClassLoader bridging (`Thread.currentThread().setContextClassLoader(Docx4J.class.getClassLoader())`)
- All `generateDocx/generatePdf` methods are `synchronized` to handle XDocReport thread-safety limitations

**ImageProvider pattern:**
- `ImageProvider` wraps `FileStoreService.get(id)` to retrieve images by FileStore ID
- `StreamImageProvider` extends `AbstractImageProvider` (XDocReport) to stream images without byte-array conversion
- Builder pattern with optional width override and `getImageWithRatio()` for proportional scaling

**ReportService orchestrator (common module):**
- `@Component(immediate=true, service=ReportService.class)` with `@Reference` to multiple DAOs, FileStoreService, ConfigurationTemplateService, PdfWatermarkService, DocumentConversionService
- Pipeline for each document: (1) load template from `ConfigurationTemplateService`, (2) query DAOs to assemble transfer object model, (3) call report utility to generate DOCX in memory, (4) convert to PDF via `DocumentConversionService`, (5) optionally add watermark via `PdfWatermarkService`, (6) store result via `FileStoreService.put()`

**DocumentConversionService (JODConverter REST):**
- `@Component` with `@Designate(ocd=Config.class)` for configurable base URL, connection timeout, read timeout
- Environment variable (`JODCONVERTER_URL`) takes precedence over OSGi configuration
- Sends multipart form POST to `/lool/convert-to/pdf` endpoint
- Pure `HttpURLConnection` -- no external HTTP client library dependency

**PdfWatermarkService (PDFBox):**
- Overlays rotated semi-transparent text on every page of a PDF
- Uses `PDExtendedGraphicsState` for opacity control and `Matrix.getRotateInstance()` for 45-degree rotation
- Configurable font size (80pt), opacity (15%), and rotation angle

## Examples

### rackinspect
- Key files: `report/ReportUtil.java`, `report/OfferReportUtil.java`, `report/JobSheetReportUtil.java`, `report/ReviewReportReportUtil.java`, `report/CompletionCertificateReportUtil.java`, `report/ImageProvider.java`, `report/StreamImageProvider.java`, `common/services/impl/ReportServiceImpl.java`, `common/services/impl/DocumentConversionServiceImpl.java`, `common/services/impl/PdfWatermarkServiceImpl.java`
- Pattern: 6 document types (assessment sheet, review report, job sheet, offer, work report, completion certificate) each with a dedicated report utility class. `ReportServiceImpl` orchestrates the full pipeline with 10+ DAO references. Templates are stored as `BinaryType` fields on a singleton `Configuration` entity and retrieved via `ConfigurationTemplateService`.
- Notable: Dual conversion backends -- docx4j (in-process, used for assessment sheets and review reports) and JODConverter REST (external Docker service, used for offers and job sheets). `ImageProvider` supports embedded photos (fault registry images) and company logos. The `PdfWatermarkService` adds "DRAFT" watermarks to preview documents. Hungarian locale-specific formatting throughout.
- DI wiring: Custom operations -> `ReportService` (orchestrator) -> `ConfigurationTemplateService` (template retrieval) + report utilities (DOCX generation) + `DocumentConversionService` (PDF conversion) + `PdfWatermarkService` (watermark) + `FileStoreService` (storage)
