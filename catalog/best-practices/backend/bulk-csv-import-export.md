---
id: "bulk-csv-import-export"
title: "Bulk CSV Import/Export via FileStore"
domain: "backend"
category: "operation"
score: 68.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-06"
projects:
  - mlszksz-platform
---
## Description

Custom operations for bulk data import and export using CSV files mediated through the FileStore service. Export operations query data, build CSV content with UTF-8 BOM (for Excel compatibility), store via FileStoreService, and return a FileType reference. Import operations read CSV from FileStoreService, parse rows, and create entities for each entry. This pattern handles compliance exports and bulk administrative operations.

## Structure

```java
// CSV Export
@Override
public ExportOutput apply(Dashboard _this, ExportInput input) {
    List<Entity> data = entityDao.query()
        .filterByTimestamp(TimestampFilter.greaterOrEqualThan(input.getFrom()))
        .selectList();

    StringBuilder csv = new StringBuilder();
    csv.append('\uFEFF');  // UTF-8 BOM for Excel
    csv.append("header1,header2,header3\n");
    for (Entity entry : data) {
        csv.append(escapeCsv(entry.getField1())).append(",")
           .append(escapeCsv(entry.getField2())).append("\n");
    }

    byte[] bytes = csv.toString().getBytes(StandardCharsets.UTF_8);
    String fileId = fileStoreService.put(new ByteArrayInputStream(bytes), "export.csv", "text/csv");

    ExportOutput output = ExportOutput.create();
    output.setExport(FileType.builder().id(fileId).fileName("export.csv")
        .mimeType("text/csv").size((long) bytes.length).build());
    return output;
}

// CSV Import (Bulk invite)
@Override
public void accept(Dashboard _this, BulkInput input) {
    InputStream csvStream = fileStoreService.get(input.getCsvFile().getId());
    List<String> emails = parseCsvEmails(csvStream);
    for (String email : emails) {
        recipientDao.create(RecipientForCreate.create()...);
        emailService.sendVerificationEmail(email, ...);
    }
}
```

## Examples

### mlszksz-platform
Two CSV operations: (1) `ExportAuditLogCustomImplementation` exports audit logs to CSV with optional date filter, UTF-8 BOM, quoted fields, and escaped quotes. Returns FileType metadata. (2) `InviteBulkCustomImplementation` parses CSV file from FileStore to extract email addresses, creates Invitation+InvitationRecipient entities, and sends verification emails to each recipient.

## Trade-offs

- Pros: Handles bulk data efficiently, FileStore decouples from REST layer, UTF-8 BOM ensures Excel compatibility, reusable FileType return pattern
- Cons: Loads entire CSV into memory (no streaming), no CSV library used (manual escaping), no validation of CSV format, N+1 email sends
- Alternative: Apache Commons CSV for parsing, streaming CSV for large datasets, background job for bulk email sending

## Related Patterns

- filestore-mediated-file-transfer
- bulk-json-import-export
- email-service-integration
