---
id: "document-generation-pipeline"
title: "Document Generation Pipeline (XDocReport + PDF Conversion)"
domain: "backend"
category: "integration"
score: 66.0
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - rackinspect
  - doors-model
---
## Description

A multi-stage document generation pipeline: (1) load DOCX template from Configuration entity via FileStoreService, (2) build a data model using deeply nested Mask queries, (3) generate DOCX using XDocReport with Freemarker templating engine, (4) optionally convert to PDF via external JODConverter REST API, (5) optionally watermark PDF via PDFBox, (6) store the result in FileStoreService. Supports both final documents and preview (watermarked) versions.

## Structure

```java
// 1. Load template
InputStream template = fileStoreService.get(config.getTemplateFileId());

// 2. Build data model with deep masks
Entity data = entityDao.getById(id, deepMask).orElseThrow();

// 3. Generate DOCX via XDocReport/Freemarker
IXDocReport report = XDocReportRegistry.getRegistry().loadReport(template, TemplateEngineKind.Freemarker);
IContext context = report.createContext();
context.put("entity", data);
ByteArrayOutputStream docx = new ByteArrayOutputStream();
report.process(context, docx);

// 4. Convert to PDF via JODConverter REST
byte[] pdf = documentConversionService.convertToPdf(docx.toByteArray());

// 5. Watermark for preview
byte[] watermarked = pdfWatermarkService.addWatermark(pdf, "PREVIEW");

// 6. Store result
String fileId = fileStoreService.put(new ByteArrayInputStream(result), "document.pdf", "application/pdf");
```

## Examples

### RackInspect
`ReportServiceImpl` (~1240 lines) generates 6 document types: assessment sheets, review reports, offers, job sheets, work reports, completion certificates. Each has a dedicated `*ReportUtil` for data model preparation. Preview operations add "PREVIEW" watermark via PDFBox (80pt, 15% opacity, 45-degree rotation). `DocumentConversionServiceImpl` calls JODConverter via HTTP multipart POST.

### doors-model
`generateDocument` custom operation on Contract entity retrieves the contract type's DOCX template and applies templating to produce the contract document. The templated content replaces the contract's DOCX file. `uploadFile` also generates DOCX values and prints the contract registration number on PDF uploads. Implementations reside in the external `doors-backend` repository.

## Trade-offs

- Pros: Template-driven document generation, non-technical users can modify templates, supports both DOCX and PDF output
- Cons: External JODConverter dependency for PDF, complex template debugging, large mask queries for data, thread-safety requires synchronized methods
- Alternative: Pure Java PDF generation (iText, Apache PDFBox), or cloud document APIs

## Related Patterns

- filestore-mediated-file-transfer
- email-service-integration
