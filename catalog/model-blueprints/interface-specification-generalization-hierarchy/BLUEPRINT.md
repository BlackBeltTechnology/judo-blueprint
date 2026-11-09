---
id: "interface-specification-generalization-hierarchy"
title: "Interface Specification Generalization Hierarchy (Protocol Type Registry)"
score: 36.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - InterfaceRegister
---
## Description

A generalization hierarchy of interface specification entities representing different communication protocol types. The base entity InterfaceSpecification carries common attributes shared by all protocol types: id, name, description, a link to documentation (URL), a specification document (binary attachment), and direction of data transmission (enum). Concrete subtypes specialize for specific protocols, adding protocol-specific attributes:

- **Rest** -- adds a link to OpenAPI specification (URL) and an OpenAPI document (binary)
- **SOAP** -- adds a WSDL document (binary) and a link to the WSDL specification (URL)
- **DBLink** -- no additional attributes; inherits the base specification fields
- **AsynchronCommunication** -- an intermediate abstract-like subtype that itself has further specializations:
  - **Email** -- adds bodyTemplate, attachmentSpecification, and composes tos/ccs/bccs collections of EmailRecipient entities
  - **FileTransfer** -- adds fileTransferMethod (enum: FTP/SFTP/FTPS/SSH/FOLDER), encoding (enum: ANSI/UTF8/UTF8_BOM), and extension
  - **MessageQueue** -- no additional attributes; inherits the base specification fields

This two-level hierarchy (InterfaceSpecification -> protocol subtypes, with AsynchronCommunication as an intermediate grouping for non-synchronous protocols) allows an enterprise integration registry to manage all protocol types through a common interface while preserving protocol-specific metadata. Transfer objects mirror the hierarchy: each subtype has its own TO with the base attributes plus subtype-specific ones. The actor accesses both a read-only collection of all InterfaceSpecification TOs (polymorphic view) and separate CRUD-enabled collections for each concrete subtype.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
