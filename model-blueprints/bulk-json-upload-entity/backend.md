## Overview

The bulk JSON upload and download operations are implemented as custom Java classes that parse/generate JSON files via Jackson, interact with the JUDO FileStoreService for binary storage, and create/query entity records through injected DAOs.

## Implementation Pattern

- The `UploadCustomImplementation` class implements the generated `Upload` operation interface and is registered as an OSGi `@Component`
- It injects `FileStoreService` (for reading the uploaded JSON blob), `QuestionDao`, `CategoryDao`, and `UploadDao` via `@Reference`
- The upload operation creates an `Upload` audit record first, reads the JSON input stream from the file store, deserializes it into a list of POJOs using Jackson `ObjectMapper`, then iterates and creates entity records (with deduplication checks via DAO query filters)
- A companion `DownloadCustomImplementation` reverses the process: queries all entities via DAO, serializes to JSON via Jackson, stores the result in `FileStoreService`, and returns a `JsonData` TO with the file reference
- An inner POJO class (e.g., `Q`) with `@JsonProperty` annotations defines the JSON schema for import/export, shared between upload and download implementations
- The upload records the count of newly created items on the Upload entity for audit purposes
- Category/classification entities referenced in the JSON are resolved by name via DAO query (`.filterByName(StringFilter.equalTo(...))`) and created on-the-fly if not found (get-or-create pattern)

## Examples

### trivia
- Key files: `custom/.../actors/admin/question/UploadCustomImplementation.java`, `custom/.../actors/admin/question/DownloadCustomImplementation.java`
- Pattern: OSGi `@Component` injecting `FileStoreService`, `QuestionDao`, `CategoryDao`, `UploadDao`; inner `Q` POJO with `@JsonProperty` for JSON serialization; Upload creates an Upload audit record, reads JSON from file store, creates Question entities with shuffled answer positions; Download queries all questions and writes a pretty-printed JSON file back to file store
- Notable: Answer choice positions are shuffled during import using `Collections.shuffle()` to randomize the display order while preserving the correct solution mapping; categories are auto-created if they do not already exist; duplicate questions (matched by question text) are skipped
