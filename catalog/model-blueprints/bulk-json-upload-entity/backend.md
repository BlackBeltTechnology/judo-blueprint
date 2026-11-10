## Backend guidance

The import and export are custom operations. The platform does not generate their logic, so it lives in project code: a `*CustomImplementation` OSGi component (`@Component(immediate = true, service = <generated interface>.class)`) that implements the generated operation interface. An operation that writes must be modelled stateful. Faults it throws must be declared on the operation in the model.

### Import is a custom operation

A custom operation implements the generated operation interface and gets its collaborators by injection. Interceptors never run for custom, mapped or script operations, so a rule that must hold on import belongs in the operation itself.

```java
public class UploadCustomImplementation implements UploadOperation {
    private final FileStoreService fileStore;   // project service, reads the uploaded file
    private final UploadDao uploadDao;          // generated DAO
    private final QuestionDao questionDao;      // generated DAO

    public JsonData upload(JsonData input) {
        Upload batch = uploadDao.create(/* json, timestamp, count set later */);
        List<Q> records = parse(fileStore.read(input));
        int created = 0;
        for (Q record : records) {
            if (questionDao.findByText(record.text()).isEmpty()) {
                questionDao.create(record.toQuestion(batch));
                created++;
            }
        }
        batch.setNrOfUploadedQuestions(created);
        return input;
    }
}
```

The sketch is illustrative. `FileStoreService`, the `Q` record and the DAO names are project code, not platform API.

### Write the batch row first

The Upload row is written before the items, so each item can refer to it. The count is set at the end. The project expects the operation to run in one transaction, so that an exception thrown out of it rolls back the batch row and the items together. The agent-docs do not state the transaction scope of a custom operation, so verify the rollback with an integration test before relying on it.

### Skip duplicates, do not fail

Items that match an existing identifier are skipped. Validation failures on a record are reported as field errors (validation exceptions, 400) rather than business faults, since they come from input data, not business rules.

### Reference data is resolved by name

Categories named in the JSON are looked up by name. A category that does not exist is created at import time. This get-or-create step is project logic.

### Export mirrors import

A static download operation reads the items through the DAO, serializes them with the same record class, stores the result in the file store, and returns a file reference. Keeping one record class for both directions keeps the round trip consistent.

### Binary input

When the JSON is uploaded as a binary file, the transfer field that maps the binary on a create-capable transfer gets a generated `getUploadTokenFor<Field>` operation. The client requests the token, uploads the content to the file store with it, and sends the token as the attribute value; an invalid token fails with `INVALID_FILE_TOKEN`. Only the operation's input type changes; the record handling is the same.
