## Backend guidance

This is project practice on top of the platform. The platform gives you custom operations, DAOs and modeled faults; the start and confirm flow, the expiry check and the identifier strategy are the project's own. Helper names in the examples (`LetterGeneratorService`, `FileStoreService`) are example project code, not platform API.

### Two custom operations

The two operations are custom implementations, each an OSGi component that gets its DAOs and services injected. See [[custom-operation-osgi-component]] and the [custom operations guide](../../agent-docs/backend/custom-operations.md) and [data access guide](../../agent-docs/backend/data-access-guide.md) for the platform side.

- **Start.** Validates the inputs (the source entities exist and are complete), calls the project's generation service, writes the result to `body` or, when large, to a binary, sets `state` to ACTIVE and `expiresAt` to now plus the time to live, creates the Handle through its DAO and returns the Handle to the client as the ticket. It does not write a Document.
- **Confirm.** Takes the Handle reference from the client, loads the Handle through the DAO and rejects it when it is missing, not ACTIVE, or expired. It then sets `state` to CONFIRMED, copies body or file and the source relations into a new Document, generates the `identifier`, creates the Document through the DAO and returns it or its identifier.

### Atomic state change

Mark the Handle CONFIRMED in the same transaction as the Document creation, or before it. The check "state is ACTIVE" and the update must not be separable, otherwise two concurrent confirms can both pass. Platform optimistic locking helps here: the update fails when the Handle changed in between, provided the version is carried in the update payload, see [platform behavior reference](../../agent-docs/backend/platform-behavior-reference.md) (optimistic locking). If the update omits the version the guard is off.

### Lazy expiry

No scheduler is needed. The confirm operation compares `expiresAt` with the current time and rejects. Expired rows stay in the table; an optional admin operation or database job can purge them.

### Rejecting a bad Handle

Reject unknown, expired or already confirmed Handles with a modeled fault declared on the confirm operation, not a silent no-op. A custom operation without a declared fault cannot throw one: the generated interface has no `throws` clause. See the [error handling guide](../../agent-docs/backend/error-handling-guide.md) (modeled faults) and [[typed-exception-error-handling]]. Interceptors do not run around custom operations, so this check belongs in the operation body.

### Overflow and final file

Large content is written to the file store and the Handle keeps a file reference. Binary values travel over REST as file-store tokens, in two phases (see the platform behavior reference, binary upload tokens). Inside the operation, the example project used its own `FileStoreService` wrapper:

```java
// Example project code, not platform API: write large body to the file store
UUID fileId = fileStoreService.put(inputStream, contentLength, "text/plain");
handleForCreate.setBodyOverflow(FileResponse.builder()
    .fileId(fileId).fileName("body.txt").mimeType("text/plain").build());

// Read it back in the confirm step
FileResponse overflow = handle.getBodyOverflow();
InputStream bodyStream = fileStoreService.get(overflow.getFileId());
```

*verify* the exact file store API of your runtime version before copying this.

### Example project use

- **Start** (`GenerateLetter`): validated template, data object and design, rendered the content through a letter generator service, wrote `body` for text outputs and a file for PDF output, set expiry to 30 minutes and created the Handle in state ACTIVE.
- **Confirm** (`ConfirmLetter`): checked state and expiry, marked the Handle CONFIRMED, generated a barcode payload string as `identifier`, created the Document with the same source relations and returned it.
