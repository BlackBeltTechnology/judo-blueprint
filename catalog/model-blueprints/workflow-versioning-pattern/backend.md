## Backend guidance

### Upload creates the next head

Upload is a custom operation on the parent, with its DAOs and services injected as an OSGi component (see [[custom-operation-osgi-component]] and the [custom operations guide](../../agent-docs/backend/custom-operations.md)). Its flow:

1. Read the uploaded file. The input binary uses the two-phase upload-token flow; an invalid token fails with `INVALID_FILE_TOKEN` (see [platform behaviour](../../agent-docs/backend/platform-behavior-reference.md)).
2. Parse and validate the definition, including that its name matches the parent.
3. If the head is uncommitted, delete it with the structure it owns and reset the head pointer to the latest remaining version, found by ordering versions by descending version number.
4. Create the new version with number head+1 (or 1), link it to the parent and set it as head.
5. Create the owned structural entities and set the content, diagram and upload time.
6. Return the admin projection of the version.

When structural elements reference each other, remove the incoming references first, then delete the version, which removes the owned elements.

### Commit and publish

Commit sets committed and the commit time and stores the comment. Publish checks that the version is committed and moves the published pointer. They are simple, but because they are custom operations no interceptor guards them: put the checks inside.

### Example project code

The upload operation and the helper classes in the source project are example project code, not platform classes.

## Examples

### Example

- The upload operation is the largest class; the cleanup helper breaks transition links before deleting states.
