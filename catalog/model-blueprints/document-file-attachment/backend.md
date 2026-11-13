## Overview

Binary attributes are held in the platform file store. On the wire the client sends and receives a file token, and in the generated Java a binary is a `FileType` value (id, file name, MIME type), not the bytes. The upload is two-phase: a generated token operation, then the content upload with that token, then the token as the attribute value in create or update. Creating and removing attachments in this blueprint is done by custom operations on the parent entity, which call project services. Those services are application code, not platform code.

## Implementation Pattern

- **Upload.** A custom operation on the parent takes a DocumentInput. The `FileType` of its `file` field is handed to the application service, which creates the document through the parent's relation method on the generated DAO. If the client can create the document through a built-in create instead, the token flow described above applies and no custom operation is needed.
- **Download.** The generated download is token-gated. Common practice: serve a file through an operation that checks access, not through a public URL built from the stored id. A public URL lets anyone who can guess an id retrieve the file.
- **Delete.** A custom delete operation removes the document from the parent and cleans up the stored file; the cleanup call is application code. Keep the cleanup in an application service so the rule is in one place.
- **Services (application code).** A parent-specific service, for example `FaultRegistryService`, owns the parent composition and calls the parent's data access to add the document. Name it for the domain. The platform does not provide it.
- **Interceptors do not run here.** Interceptors run only on built-in operations, so an upload or delete that is a custom operation never triggers one (the built-in upload token and create do). Put any audit step in the custom operation.
- **Inline creation.** When the file is only a field of the parent, map the input's attachment list while the parent is created. This needs no separate upload operation.

```java
public class AddAttachmentCustomImplementation implements AddAttachment {
    private final AttachmentService attachments; // application code

    @Override
    public Document execute(Parent _this, DocumentInput input) {
        return attachments.attach(_this, input.getFile());
    }
}
```

The class is application code. The operation interface is generated.

## Examples

### Variant seen in practice
- Pattern: add and delete operations delegate to an application service. Add takes an input with the file and a description, and the service creates the attachment through the parent's data access. Delete removes the attachment.
- Notable: two document-like entities exist. One holds version and rendition fields for generated documents. The other is a simple attachment with a file and a description, for files uploaded by users.

### Second variant seen in practice
- Pattern: attachments are created inline with the product, by mapping the input's attachment list to the create input. On a version draft the attachments are copied to the new product.
- Notable: there are no standalone upload or delete operations. Attachments follow the parent's create and version lifecycle.
