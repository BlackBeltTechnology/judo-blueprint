## Examples

### mlszksz-platform
- **Entity**: `MLSZKSZPlatform::entities::Document`
  - Attributes: file (req, binary), uploadedAt (req)
  - Relations: announcement (0..1 ASSOC to Announcement)
  - Non-CRUD
- **Transfer Objects**:
  - `admin::Document`: file (req), uploadedAt (req) -- read-only view
  - `admin::DocumentInput`: file (req) -- unmapped, upload input
  - `feed::Document`: file (req), uploadedAt (req) -- read-only view
- Announcement entity has `documents` (0..* ASSOC) relation to Document

### rackinspect
- **Document entity**: `rackinspect::entities::Document` (non-CRUD)
  - Attributes: document (req, binary), version (req), description (req, default: " "), documentPDF
  - No relations -- documents are owned via composition from Task (documents 0..*)
- **Attachment entity**: `rackinspect::entities::Attachment` (non-CRUD)
  - Attributes: document (req, binary), description (req, default: " ")
  - No relations -- owned via composition from RegistryHeader (attachments 0..*)
- Both Document and Attachment serve as file containers; Document adds versioning and PDF rendition

### reserve-app
- **Attachment entity**: `ReserveApp::entities::Attachment` (non-CRUD)
  - Attributes: picture (req, binary) -- minimal variant with a single binary field
  - No relations on the entity itself
  - Owned by FreightReservation via `attachments` (0..* COMPOSITION)
- Simplest form of the pattern: a bare file container with no metadata, composed by the parent entity

### alba
- **Attachment entity**: `Alba::entities::Attachment` (non-CRUD)
  - Attributes: attachment (req, binary) -- single binary field named `attachment`
  - No relations on the entity itself
  - Owned by Product via `attachments` (0..* COMPOSITION)
- **Transfer Objects**:
  - `Alba::services::Attachment` -- attachment (req) -- read-only view
  - `Alba::services::FormAttachment` (unmapped) -- attachment (req) -- input for product creation forms
- Used in AuthorProductForm and AdminProductForm via `attachments` (0..* AGGREGATION) relation

### judo-demo-miniworkflow
- **Files entity**: `MiniWorkflow::Files` (non-CRUD)
  - Attributes: type (req), description, file (req, binary)
  - No relations on the entity itself
  - Owned by Document via `files` (0..* COMPOSITION)
- Named "Files" instead of "Document" or "Attachment" but follows the same pattern: a non-CRUD entity with a binary file attribute composed by a parent
- Adds a `type` discriminator attribute (e.g., to distinguish PDF vs image vs Word document)
- **Transfer Objects**:
  - `MiniWorkflow::FilesTransfer` -- type (req), description, file (req) -- read-only projection

### doors-model
- **Inline file attributes on Contract**: `doors::entities::Contract`
  - Attributes: file (ContractTemplate type, maxLength: 100), signedFile (SignedContract type, maxLength: 100)
  - Operations: uploadFile (INSTANCE, customImplementation=true), uploadSignedContract (INSTANCE, customImplementation=true), generateDocument (INSTANCE, customImplementation=true)
- **UploadFileInput TO** (`doors::entities::UploadFileInput`):
  - Unmapped transfer object with single `file` (ContractTemplate) TRANSIENT attribute
  - Used as input parameter for the uploadFile operation
- **UploadSignedFileInput TO** (`doors::entities::UploadSignedFileInput`):
  - Unmapped transfer object with single `file` (SignedContract) TRANSIENT attribute
  - Used as input parameter for the uploadSignedContract operation
- This variant stores files directly as attributes on the parent entity (Contract) rather than creating a separate Document entity
- Two separate file fields: `file` for the generated contract document and `signedFile` for the physically signed version
- The generateDocument operation creates the contract document from a template (customImplementation=true, delegated to backend Java code)
- The uploadSignedContract operation stores the signed version after physical signature
- **ContractLog entity** also stores file versions: contractVersion (ContractTemplate) and signedContractVersion (SignedContract), providing a history of document versions alongside event logs
