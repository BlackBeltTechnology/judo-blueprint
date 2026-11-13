## Backend guidance

### Module and service layout

Keep the template code separate from the service layer:

- a report module of plain utility classes, one per document type, with no OSGi dependency;
- a service layer with an orchestrator, a template service, a conversion service and a watermark service, each registered as an OSGi service and injected into the operations (see [[custom-operation-osgi-component]] and the [custom operations guide](../../agent-docs/backend/custom-operations.md)).

The class names in the source project (`ReportService`, `DocumentConversionService`, `PdfWatermarkService`, `ConfigurationTemplateService`, the `*ReportUtil` classes, `ImageProvider`) are example project code.

### The pipeline steps

1. Load the template stream from the file store.
2. Query the DAOs and assemble the transfer object that is the data model. Use a mask deep enough for every placeholder.
3. Load the template with the XDocReport registry for the Freemarker engine, create the context, put the data as a plain map, and register image fields. Optional images use the remove-placeholder behaviour.
4. For PDF: convert the DOCX in-process or post it to an external converter service as multipart form data.
5. For previews: overlay text with PDFBox, rotated and semi-transparent.
6. Store the output in the file store and return its token to the caller. Returning the file to the client uses the platform's two-phase binary token flow (see [platform behaviour](../../agent-docs/backend/platform-behavior-reference.md)).

### Images

An image provider wraps a file store read and streams it to XDocReport without copying it to a byte array; a builder can scale to a width with the aspect ratio kept.

### Configuration

The converter URL and timeouts are component configuration; an environment variable overrides the configured URL. See the [application configuration guide](../../agent-docs/deployment/application-config.md) for how environment variables and OSGi configuration are resolved. This override order is project practice.

### Checks and interceptors

The calling operations are custom, so interceptors do not guard them (see [interceptors](../../agent-docs/backend/interceptors.md)). Do the permission check inside the operation, and throw a business fault for missing templates.

## Examples

- Six document types, each with its own report utility; the orchestrator uses a dozen DAOs.
- Two conversion backends: in-process for some documents, an external converter for others.
- A watermark service adds a draft mark to preview documents.
- Templates live as binary attributes on a singleton configuration entity.
