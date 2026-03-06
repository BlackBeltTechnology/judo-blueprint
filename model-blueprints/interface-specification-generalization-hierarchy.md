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

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { like: "%Interface%" } }) {
  items { fqn name abstract
    attributes { items { name } }
    generalizations { items { fqn } totalCount }
  }
} } }
```

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    generalizations { items { fqn } totalCount }
  }
} } }
```

Look for entities with generalizations pointing to a common base that has specification/protocol-related attributes (id, name, description, URL link, binary document).

## Creation Mutations

### Base entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "InterfaceSpecification",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InterfaceSpecification", name: "id"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InterfaceSpecification", name: "name"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InterfaceSpecification", name: "description"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InterfaceSpecification", name: "linkToTheSpecification"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InterfaceSpecification", name: "specificationDocument"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::InterfaceSpecification", name: "directionOfTransmission"
} }) { success fqn } }
```

### REST subtype

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Rest",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::Rest",
  target: "{{NAMESPACE}}::InterfaceSpecification"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Rest", name: "linkToOpenApiSpecification"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Rest", name: "openApiDocument"
} }) { success fqn } }
```

### SOAP subtype

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "SOAP",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::SOAP",
  target: "{{NAMESPACE}}::InterfaceSpecification"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::SOAP", name: "WSDLDocument"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::SOAP", name: "linkToWSDLSpecification"
} }) { success fqn } }
```

### DBLink subtype

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "DBLink",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::DBLink",
  target: "{{NAMESPACE}}::InterfaceSpecification"
} }) { success fqn } }
```

### AsynchronCommunication intermediate subtype

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "AsynchronCommunication",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::AsynchronCommunication",
  target: "{{NAMESPACE}}::InterfaceSpecification"
} }) { success fqn } }
```

### Email subtype (extends AsynchronCommunication)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Email",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::Email",
  target: "{{NAMESPACE}}::AsynchronCommunication"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Email", name: "bodyTemplate"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Email", name: "tos",
  target: "{{NAMESPACE}}::EmailRecipient", lower: 0, upper: -1,
  relationKind: "COMPOSITION"
} }) { success fqn } }
```

### FileTransfer subtype (extends AsynchronCommunication)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "FileTransfer",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::FileTransfer",
  target: "{{NAMESPACE}}::AsynchronCommunication"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FileTransfer", name: "fileTransferMethod"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FileTransfer", name: "encoding"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::FileTransfer", name: "extension"
} }) { success fqn } }
```

### MessageQueue subtype (extends AsynchronCommunication)

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "MessageQueue",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { generalization: {
  container: "{{NAMESPACE}}::MessageQueue",
  target: "{{NAMESPACE}}::AsynchronCommunication"
} }) { success fqn } }
```

### Direction of transmission enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "DirectionOfDataTransmission"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DirectionOfDataTransmission", name: "SERVER_TO_CLIENT", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::DirectionOfDataTransmission", name: "CLIENT_TO_SERVER", ordinal: 2
} }) { success fqn } }
```

## Examples

### InterfaceRegister
- **Base entity**: `InterfaceRegister::entities::InterfaceSpecification` (non-CRUD)
  - Attributes: id (req, identifier), name (req, identifier), description (Text), linkToTheSpecification (URL), specificationDocument (BinaryType), directionOfTransmission (DirectionOfDataTransmission, req)
  - No relations, no operations

- **Synchronous subtypes** (generalize InterfaceSpecification directly):
  - `Rest` -- adds linkToOpenApiSpecification (URL), openApiDocument (BinaryType)
  - `SOAP` -- adds WSDLDocument (BinaryType), linkToWSDLSpecification (URL)
  - `DBLink` -- no additional attributes

- **Asynchronous intermediate type**:
  - `AsynchronCommunication` -- generalizes InterfaceSpecification; no additional attributes of its own but serves as grouping parent

- **Asynchronous subtypes** (generalize AsynchronCommunication):
  - `Email` -- adds bodyTemplate (Text, req), attachmentSpecification (Text); composes tos/ccs/bccs (0..* COMPOSITION -> EmailRecipient)
  - `FileTransfer` -- adds fileTransferMethod (FileTransferMethod enum: FTP/SFTP/FTPS/SSH/FOLDER, req), encoding (CharacterEncoding enum: ANSI/UTF8/UTF8_BOM, req), extension (String, req)
  - `MessageQueue` -- no additional attributes

- **EmailRecipient entity**: `InterfaceRegister::entities::EmailRecipient` -- address (Email, req); composed by Email entity

- **Transfer objects**: Each subtype has a corresponding TO in `InterfaceRegister::enterpriseArchitect`:
  - `InterfaceSpecification` TO -- base attributes only (read-only polymorphic view)
  - `Rest` TO -- base attributes + linkToOpenApiSpecification, openApiDocument
  - `SOAP` TO -- base attributes + WSDLDocument, linkToWSDLSpecification
  - `DBLink` TO -- base attributes only
  - `Email` TO -- base attributes + bodyTemplate, attachmentSpecification + tos/ccs/bccs relations to EmailRecipient TO
  - `MessageQueue` TO -- base attributes only

- **Actor access pattern**: EnterpriseArchitect actor has:
  - `interfaceSpecifications` [0..*] -> InterfaceSpecification TO (read-only, no CRUD) -- polymorphic view of all specifications
  - `restSpecifications` [0..*] -> Rest TO (createable, updateable)
  - `soapInterfaceSpecifications` [0..*] -> SOAP TO (createable, updateable)
  - `dblinkInterfaceSpecifications` [0..*] -> DBLink TO (createable, updateable)
  - `messageQueueInterfaceSpecifications` [0..*] -> MessageQueue TO (createable, updateable)
  - `emailInterfaceSpecifications` [0..*] -> Email TO (createable, updateable)

- **Supporting enums**:
  - `DirectionOfDataTransmission` -- SERVER_TO_CLIENT(1), CLIENT_TO_SERVER(2)
  - `CharacterEncoding` -- ANSI(1), UTF8(2), UTF8_BOM(3)
  - `FileTransferMethod` -- FTP(1), SFTP(2), FTPS(3), SSH(4), FOLDER(5)
