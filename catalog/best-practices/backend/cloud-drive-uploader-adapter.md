---
id: cloud-drive-uploader-adapter
title: Cloud Drive Uploader Adapter with Unconfigured Outcome
description: A domain-agnostic upload interface in its own bundle that reads credentials from OSGi configuration or environment, returns an UNCONFIGURED outcome instead of throwing, and reports each file independently.
aliases: [drive uploader, cloud storage uploader, upload adapter, batch uploader]
keywords: [upload, cloud drive, adapter, osgi config, credentials, unconfigured, outcome, batch, service account]
tags: ["domain:backend", "layer:backend", "project:park-here", "status:single-project"]
category: integration
status: single-project
projects: [park-here]
evidence: ["park-here:application/google-drive/src/main/java/hu/blackbelt/park/here/google/drive/DriveUploader.java", "park-here:application/google-drive/src/main/java/hu/blackbelt/park/here/google/drive/DriveUploaderImpl.java", "park-here:application/google-drive/src/main/java/hu/blackbelt/park/here/google/drive/UploadOutcome.java"]
alternatives: [external-api-adapter-pattern]
related: [external-api-adapter-pattern, filestore-mediated-file-transfer]
fragment: "none: backend-only"
first_seen: 2026-11-10
last_updated: 2026-11-10
---
## Intent

An application must push generated files (reports, documents) to a cloud drive folder. The callers should not know the drive SDK, and a missing credential in a development or test environment must not break the business operation that wants to upload. This is the single-provider, upload-only case of [[external-api-adapter-pattern]]: it keeps the interface and bundle boundary but has no provider service, and adds an outcome object instead of exceptions for the unconfigured state.

## Practice

### Platform base

- The runtime turns an uncaught exception from a custom operation into a generic 500 ([How the Runtime Maps Exceptions to HTTP](../../agent-docs/backend/error-handling-guide.md#how-the-runtime-maps-exceptions-to-http)). An upload failure that is only a side effect should therefore come back as data, not as an exception.
- Custom operations reach services with `@Reference` ([custom operations](../../agent-docs/backend/custom-operations.md#osgi-component-registration-pattern)). Do not call out from an interceptor ([[external-api-adapter-pattern]]).

### Project practice: separate bundle, neutral interface

The interface, outcome class and implementation are example project code.

1. Put the uploader in its own bundle. Its interface knows nothing of the business domain: the caller passes a parent folder id, a subfolder name and a list of named byte streams, and interprets the result.
2. Read the credential from the OSGi configuration property of the component, which can interpolate an environment variable, and fall back to the raw environment variable. Resolve it at activation and again on modification.
3. Register the component unconditionally (optional configuration policy), so callers' `@Reference` stays satisfied when nothing is configured.
4. When the credential or the parent folder is missing or invalid, return `UNCONFIGURED` with a message. Do not throw.
5. Upload each file independently. One failing file does not stop the others.
6. Return one outcome object with a status (`ALL_OK`, `PARTIAL`, `TOTAL_FAILURE`, `UNCONFIGURED`), a folder link when there is one, uploaded and failed counts, and an error message. The caller renders it, for example into a notice e-mail.
7. Keep a package-private initialization seam so integration tests can supply a credential without changing the process environment.

```java
UploadOutcome outcome = uploader.uploadBatch(parentFolderId, "2026-11-run", files);
switch (outcome.status()) {
    case ALL_OK, PARTIAL -> notice.withLink(outcome.folderLink());
    case TOTAL_FAILURE, UNCONFIGURED -> notice.withError(outcome.errorMessage());
}
```

Library-specific hardening (class loader and security provider handling inside the OSGi container) stays inside the implementation. Whether it is needed depends on the SDK and container: *verify*.

## Rationale

- Environments without credentials (tests, local runs) keep working and show a clear status.
- Callers can degrade gracefully because partial success is part of the contract.
- The domain-agnostic interface lets the same bundle serve several callers.
- Cost: callers must read the status, because nothing is thrown; a mistyped configuration shows up as `UNCONFIGURED`, not as a startup failure.

## Example

A travel-report operation builds a set of documents, asks the uploader to put them in a new per-run subfolder of a shared drive and mails the folder link. With no credential, the mail states that upload is not configured and the rest of the operation succeeds.

## When to avoid

- Several providers do the same job: use the full adapter and provider service of [[external-api-adapter-pattern]].
- The upload must be atomic with the data change: use an outbox entity and a separate job.
- Files are small and only need to be stored in the platform: use the file store ([[filestore-mediated-file-transfer]]).

## Related

- [[external-api-adapter-pattern]] — the general adapter with a provider service; this entry is its single-provider case
- [[filestore-mediated-file-transfer]] — files held in the platform file store
