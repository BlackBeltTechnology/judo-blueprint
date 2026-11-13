## Overview

Four operations need backend code: generating the work order, the report's `toDone`, the item's `toDone` and the item's `toWontFix`. They are custom, so the platform runs no interceptor for them. Every guard in this pipeline therefore lives inside the operation body, in the same transaction as the write it protects.

Platform facts: an `OperationCallInterceptor` fires only for built-in operations such as create, update, delete and list. Custom, mapped and script operations are never intercepted (see [agent-docs interceptors](../../agent-docs/backend/interceptors.md)).

## Generating the work order

- Load the offer and check its status is accepted. Check that no work report of kind COMPLETION_CERTIFICATE exists under its work orders. Throw a business error with a stable code when either check fails.
- Build one work order item per offer item and finding pair, and one item for a finding-less offer item. Give each item a number from the counter of its own finding (or of its offer item when it has no finding). Do not share one counter across findings.
- Create the work order and its items in one call, so a failure leaves no partial order.
- *verify*: the reference implementation numbers all items of one work order with one running counter across findings. That contradicts the per-finding numbering above and must not be copied.

## Item status operations

- `toDone`: reject when the item has no attachment. Set the status to DONE only after the check passes.
- `toWontFix`: read `reason` from the input, trim it and reject a blank value with a business error. Store it in `wontFixReason`, then set WONT_FIX. A reason kept only on the client does not count.
- In both operations, refuse the change when the parent work order is already done.
- Bulk actions call the same operation per item. Report each failing item in the response instead of failing the whole batch silently. *verify*: the exact bulk contract is not yet decided in the catalog.

## Report `toDone`

- Read the kind first.
- WORK_REPORT: require at least one generated document (the last generated document of the report).
- COMPLETION_CERTIFICATE: require the signed document. *verify* the rule, see the Constraints section of the entry.
- Set the report to DONE. For a completion certificate, also set its work order to DONE. *verify*: whether closing the order belongs in the same operation or in a separate step.

## Document numbers

Take a document number only when a document is created, never when it is regenerated. Read and increment the number sequence under a database lock in the same transaction (see [[document-registry-sequence]]). A regenerated document keeps its number and gets a new version.

## Generic Java sketch

```java
public void toDone(WorkOrderItem item) throws BusinessErrorException {
    if (!itemDao.queryAttachment(item).isPresent()) {
        throw ExceptionUtils.createBusinessErrorException("ATTACHMENT_REQUIRED", "A photo is needed to mark the item done");
    }
    item.setWorkStatus(WorkStatus.DONE);
    itemDao.update(item);
}
```

The sketch shows the shape of the guard only. Use the generated DAO and error helpers of the project.
