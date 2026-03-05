---
id: "filestore-mediated-file-transfer"
title: "FileStore-Mediated File Transfer Pattern"
domain: "backend"
category: "integration"
score: 150.8
usage_count: 10
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
  - rackinspect
  - alba
  - mlszksz-platform
  - viterra_demo
  - park-here
  - indamedia-adtrack
  - judo-partner
  - workflow-poc
  - doors-model
---
## Description

File upload and download operations use the JUDO FileStore service as an intermediary rather than handling files directly in REST endpoints. Files are stored via `fsService.put()` which returns an ID, and retrieved via `fsService.get(id)`. The client receives/sends file references (ID, fileName, mimeType) through transfer objects with `FileType` fields.

## Structure

```java
@Reference
FileStoreService fsService;

// Upload: read from FileStore
InputStream stream = fsService.get(input.getFile().getId());
// Process stream content...

// Download: write to FileStore
String fileId = fsService.put(
    new ByteArrayInputStream(jsonBytes),
    "filename.json",
    "application/json"
);
// Return FileType reference with id, fileName, mimeType
return OutputTO.builder()
    .withFile(FileType.builder()
        .withId(fileId)
        .withFileName("filename.json")
        .withMimeType("application/json")
        .build())
    .build();
```

Configuration: `JUDO_PLATFORM_FILESTORE=rdbms` (database-backed storage).

## Examples

### Trivia
Upload operation reads JSON from FileStore via `fsService.get(input.getJson().getId())`, parses questions, creates entities. Download operation serializes questions to JSON, stores via `fsService.put(stream, "questions.json", "application/json")`, returns `JsonData` with FileType reference.

### RackInspect
FileStoreService used for document template storage (DOCX templates for assessment sheets, offers, etc.), generated document storage, and attachment management. Injected with target filter: `@Reference(target = "(&(judo.model.name=rackinspect))")`. Central to the document generation pipeline.

### ALBA
Configured with filesystem backend: `JUDO_PLATFORM_FILESTORE=filesystem`, `JUDO_PLATFORM_FILESTORE_DIRECTORY=/filestore`. Uses OSGi Filestore API (`filestore-api:1.3.0`). Product attachments are copied during DraftNewVersion via `productDao.createAttachments(newProduct, attachments)` which internally manages file references.

### mlszksz-platform
Used for audit log CSV export (`ExportAuditLogCustomImplementation` builds CSV with UTF-8 BOM, stores via `fileStoreService.put()`) and bulk invitation CSV upload (`InviteBulkCustomImplementation` reads CSV from FileStore). In-memory FileStore mock used in integration tests. Production uses filesystem backend.

### viterra_demo
Configured with RDBMS-backed file storage: `JUDO_PLATFORM_FILESTORE=rdbms` in `judo-karaf.env`. Karaf feature includes Apache Tika bundles (tika-core, tika-parsers) and PDFBox for document processing support. No custom file operations implemented yet, but the infrastructure is configured and ready.

### ParkHere
FileStoreService used extensively in Init for storing email templates (4 Handlebars `.html.hbs` files), per-garage email templates (3 garage-specific templates), and floor plan images (4 PNG/JPG files). `EmailSenderServiceImpl` retrieves templates and floor plan images from FileStore by ID for email rendering, converting floor plans to base64 for inline embedding.

### Indamedia-AdTrack
FileStoreService used for secure storage of Google Ads JSON key files. `AccountService.setGoogleCredential()` stores uploaded JSON key file via FileStore. `AdsBusinessApiProviderServiceImpl` retrieves credential files from FileStore, converts to string via `StreamUtils.convertStreamToString()`, and passes to `GoogleAdsApiImpl` constructor. Enables secure credential management without filesystem access.

### judo-partner
FileStoreService used for partner import JSON file uploads. `PartnerImportCustomImplementation` reads uploaded JSON via `FileStoreService`, parses partner data with Jackson, and creates staged `ImportPartner` records. `ImportCountriesCustomImplementation` similarly reads country data from uploaded JSON. Configured as RDBMS-backed: `JUDO_PLATFORM_FILESTORE=rdbms`.

### workflow-poc
FileStoreService used for YAML workflow definition uploads. `UploadCustomImplementation` reads uploaded YAML via `fsService.get(input.getYaml().getId()).readAllBytes()`, deserializes with Jackson `ObjectMapper(YAMLFactory)` into Java record types (`YamlData`), then creates workflow version entities from the parsed data. RDBMS-backed: `JUDO_PLATFORM_FILESTORE=rdbms`.

### doors-model
Three file-handling custom operations on Contract entity: `uploadFile` (uploads contract file, generates DOCX values, prints registration number on PDF uploads, clears signed file and resets state to PENDING), `uploadSignedContract` (uploads signed version, sets `signedFile` attribute, creates SIGNED ContractLog), `generateDocument` (retrieves contract type template and applies DOCX templating). All implementations reside in external `doors-backend` repository.

## Trade-offs

- Pros: Decouples file handling from REST layer, supports RDBMS or filesystem backends, consistent API
- Cons: Extra indirection, files in RDBMS can cause DB bloat, no streaming for large files
- Alternative: Direct filesystem storage, S3-compatible object storage

## Related Patterns

- bulk-json-import-export
- email-service-integration
- document-generation-pipeline
- handlebars-email-template
