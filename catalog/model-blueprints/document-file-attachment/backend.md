## Overview

Document and Attachment entities are managed through custom operations that create, delete, and associate file attachments with parent entities (RegistryHeader, Task). Backend operations handle binary file storage and parent-child relationship management.

## Implementation Pattern

- Attachment creation is handled by custom operations like `AddFaultRegistryAttachmentCustomImplementation` that accept an input TO (AttachmentInput) with the binary file and delegates to a shared service (e.g., `FaultRegistryService`)
- Attachment deletion uses a custom `DeleteAttachmentCustomImplementation` that delegates to the same service for cleanup logic
- The service layer manages the parent composition relationship: creating the Attachment via the parent DAO's `createAttachments()` method and handling cascading concerns
- Document entities (with version and documentPDF attributes) are typically created by document generation operations rather than direct user upload
- Binary file content is stored and retrieved through the platform's `FileStoreService` integration
- In simpler variants, attachments are created inline during parent entity creation by mapping input TO attachment lists to `AttachmentForCreate` builders

## Examples

### rackinspect
- Key files: `custom/.../registryheader/AddFaultRegistryAttachmentCustomImplementation.java`, `custom/.../attachment/DeleteAttachmentCustomImplementation.java`, `common/utils/services/impl/FaultRegistryServiceImpl.java`
- Pattern: Both add and delete operations delegate to `FaultRegistryService`; add accepts `AttachmentInput` (binary file + description) and creates via parent DAO composition; delete removes the attachment entity
- Notable: Two document-like entities exist -- `Document` (with version and documentPDF) for generated task documents, and `Attachment` (simpler, binary + description) for user-uploaded files on RegistryHeader
- Document generation operations (e.g., `GenerateFaultRegistryDocumentCustomImplementation`) create Document entities programmatically with version tracking

### alba
- Key files: `custom/.../services/adminproduct/CreateProductCustomImplementation.java`, `custom/.../services/authorproduct/CreateProductCustomImplementation.java`, `custom/.../entities/product/DraftNewVersionCustomImplementation.java`
- Pattern: Attachments (single binary field) are created inline during product creation by mapping form input to `AttachmentForCreate.builder().withAttachment(a.getAttachment()).build()` and passing the list to `ProductForCreate.withAttachments()`; on version draft, existing attachments are copied to the new product via `productDao.createAttachments()`
- Notable: No standalone attachment upload/delete operations; attachments are managed entirely through the parent Product's create and version-copy lifecycle operations
