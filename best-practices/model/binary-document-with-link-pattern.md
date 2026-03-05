---
id: "binary-document-with-link-pattern"
title: "Binary Document with URL Link Pair"
domain: "model"
category: "entity"
score: 17.7
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - InterfaceRegister
---
## Description

An entity stores both a binary document attribute (for uploaded files) and a companion URL string attribute (for external links to the same document). This dual-storage pattern allows specifications and documents to be either uploaded directly or referenced by URL, supporting both online and offline access patterns.

## Structure

- Binary attribute for the uploaded document (e.g., `specificationDocument: Binary`)
- String/URL attribute for the external link (e.g., `linkToTheSpecification: String`)
- Both attributes are optional (the user provides one or both)
- Pattern repeats for protocol-specific documents (OpenAPI, WSDL, etc.)
- Base entity defines the generic pair; subtypes add protocol-specific pairs

## Examples

### InterfaceRegister
`InterfaceSpecification` base entity defines the generic pair: `specificationDocument` (Binary, optional) + `linkToTheSpecification` (URL, optional). Subtypes add protocol-specific pairs: `Rest` has `openApiDocument` (Binary) + `linkToOpenApiSpecification` (URL); `SOAP` has `WSDLDocument` (Binary) + `linkToWSDLSpecification` (URL). This allows each interface type to carry both a general specification and a protocol-specific specification document/link.

## Trade-offs

- Pros: Flexible document access (upload or link), supports both online and offline documentation, protocol-specific document types
- Cons: Potential inconsistency if both link and document are provided but differ, doubles the storage fields
- Prefer when: Users need flexibility to either upload documents or reference them by URL

## Related Patterns

- [standard-type-library](standard-type-library.md) (Binary and URL types)
- [generalization-base-entity](generalization-base-entity.md) (shared document attributes inherited by subtypes)
