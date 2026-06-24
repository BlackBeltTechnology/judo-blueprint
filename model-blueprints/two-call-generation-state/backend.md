## Overview

Two custom operations implement the two-call flow: a **start** operation that creates a Handle, and a **confirm** operation that validates the Handle and writes the Document. Both are backend-only; neither TO exposes CRUD actions to the client.

## Implementation Pattern

### Start operation (creates Handle)

- Registered as an OSGi `@Component` implementing the generated operation interface.
- Injects `GenerationHandleDao` (or equivalent), plus any DAOs for source entities (TemplateDao, DataObjectDao, DesignDao).
- Validates inputs (e.g., template exists, data object is complete).
- Calls the rendering / generation service (injected via `@Reference`).
- Writes result into `body` (LongText) or `bodyOverflow` (BinaryType via `FileStoreService`) depending on size.
- Sets `state = ACTIVE` and `expiresAt = now() + TTL` (TTL typically configured via Karaf config or a constant).
- Creates the Handle record via DAO `.create()` — returns the Handle ID to the client as the "ticket".
- Does **not** write a Document yet.

### Confirm operation (reads Handle → writes Document)

- Takes the Handle ID (passed back by the client as a parameter on the second call).
- Loads the Handle via DAO; rejects if not found, `state != ACTIVE`, or `expiresAt < now()`.
- Calls `handleDao.update()` or a state-transition helper to set `state = CONFIRMED` (prevents double-confirm).
- Copies body / finalFile from Handle into a new `GeneratedDocumentForCreate`, sets `identifier` to the generated reference value (e.g., UUID, barcode payload).
- Copies source-entity relations (`template`, `dataObject`, `design`) from Handle into Document.
- Creates Document via `GeneratedDocumentDao.create()`.
- Returns the Document (or its identifier) to the client.

### Expiry handling

- No background scheduler or timer-based GC is required.
- On the confirm call, the operation checks `handle.getExpiresAt().isBefore(now())` and throws `FaultException` / returns an error TO if expired.
- Expired Handle rows accumulate in the DB; a periodic admin operation or DB job can purge them if storage is a concern, but this is optional.

### FileStoreService usage (bodyOverflow / finalFile)

```java
// Writing large body to overflow
UUID fileId = fileStoreService.put(inputStream, contentLength, "text/plain");
handleForCreate.setBodyOverflow(FileResponse.builder()
    .fileId(fileId).fileName("body.txt").mimeType("text/plain").build());

// Reading overflow in confirm step
FileResponse overflow = handle.getBodyOverflow();
InputStream bodyStream = fileStoreService.get(overflow.getFileId());
```

## Key Rules

1. **Both entities are non-CRUD.** All reads and writes go through custom operation implementations — never through generated CRUD endpoints.
2. **State transition is atomic.** Set `state = CONFIRMED` on the Handle before (or in the same DB transaction as) creating the Document, to prevent double-confirm under concurrent requests.
3. **Copy relations, do not move them.** Document holds its own ASSOCIATION references to Template / DataObject / Design — independent of the Handle's copies. This lets Handle rows be pruned without affecting Document provenance.
4. **Identifier generation.** Choose a strategy (UUID, sequential, barcode payload) and generate it in the confirm operation, not the start operation, so the stable external reference only exists once finalized.
5. **Error handling.** Use the generated `<App>FaultException` (checked) or a domain error enum for invalid state / expired handle rejections. Do not silently swallow stale-handle calls.

## Examples

### compsychletter (add-document-cluster, 2026-05-12)
- **Start operation** (`GenerateLetter`): validates Template + DataObject + Design, calls `LetterGeneratorService` to render content, writes `body` (LongText) for text outputs and `finalFile` (via FileStoreService) for PDF, sets `expiresAt = now() + 30 minutes`, creates `GenerationHandle` with `state = ACTIVE`.
- **Confirm operation** (`ConfirmLetter`): receives Handle ID, checks `state == ACTIVE && expiresAt >= now()`, marks Handle `CONFIRMED`, generates `identifier` (barcode payload string), creates `GeneratedDocument` with same source-entity relations, returns Document TO.
- Both operations implemented under `custom/src/main/java/.../actors/<actor>/letter/`.
