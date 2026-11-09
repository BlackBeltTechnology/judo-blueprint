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
