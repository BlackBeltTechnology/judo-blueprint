---
id: work-order-report-completion-pipeline
title: Work Order, Work Report and Completion Certificate Pipeline
description: "An accepted offer generates a work order with numbered items; work reports of two kinds, and a completion certificate, close the work, with guards on item status and kind-based rules on completion."
aliases: [job sheet work report certificate, jobsheet workreport completion, work order completion pipeline, completion certificate workflow, offer to completion certificate]
keywords: [work order, work report, completion certificate, offer, work order item, numbering, status guard, kind, pipeline, photo, won't fix]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:rackinspect, status:single-project]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:model/rackinspect.model", "rackinspect:application/common/src/main/java/hu/blackbelt/rackinspect/common/utils/services/impl/JobTaskServiceImpl.java"]
alternatives: []
related: [work-status-lifecycle-enum, generalization-base-entity]
first_seen: 2026-11-10
last_updated: 2026-11-10
---
## Intent

Turn an accepted offer into field work and a signed-off result. The pipeline has four parts: a work order that splits the offered work into numbered items, work reports that record the work done, a completion certificate that closes the order, and guards that stop an item from being closed without evidence.

### Items are numbered per finding

Each work order item covers one finding and one quantity. Numbers restart for every finding, so the items of finding A are 1 and 2 and the item of finding B is 1 again. The number identifies the item inside its finding. There is no sequence across the whole work order.

### A report has a kind

A work report and a completion certificate use the same entity. The `kind` decides what the report must contain before it can be closed. A plain work report needs its documents. A completion certificate needs a signed document and closes the work order.

## Structure

- **Offer** has a status (draft, accepted, rejected, done), its offer items, and a derived flag that says whether a work order may be generated.
- **WorkOrder** has a number, a creation timestamp and a work status. It composes one or more work order items and has zero or more work reports.
- **WorkOrderItem** has a number (unique within its finding), a quantity, a work status and an optional won't-fix reason. It refers to one offer item, optionally to a finding, and to zero or more attachments (photos).
- **Finding** has a name. Several items can point to the same finding.
- **WorkReport** has a kind (WORK_REPORT or COMPLETION_CERTIFICATE) and a work status. It composes zero or more generated documents and at most one signed document.
- **Document** and **Attachment** each hold one file with its name. A document also carries a number.
- **WorkStatus** is one enumeration with four members: NOT_STARTED, IN_PROGRESS, DONE and WONT_FIX. Work orders, items and reports all use it.

## Constraints

- A work order is generated from an accepted offer only. Generation is not allowed once the offer is done or when a completion certificate already exists for it.
- Each item is created with its finding's own number sequence. Numbers never run across findings.
- A report of kind WORK_REPORT can move to DONE only after a document has been generated for it.
- A report of kind COMPLETION_CERTIFICATE can move to DONE only after a signed document is attached. *verify*: the reference implementation requires the signed document; the catalog wording of this rule is still open.
- An item can move to DONE only when it has at least one attachment (a photo).
- An item can move to WONT_FIX only with a reason. The reason arrives in the operation input and is stored on the item.
- Hiding an action in the user interface does not protect the operation. Each guard runs inside the operation.

## Variations

- **One report kind.** Drop the kind when all reports are alike. The guard then becomes the single rule for the report.
- **Items without findings.** A work order whose items are not split by finding keeps only the quantity and a plain sequence. Use this only when no per-finding numbering is needed.
- **Status history.** Record each status change of the work order, the items and the reports; see [[state-transition-history-entry]].
- **Typed media.** Keep photos, videos and audio in one attachment entity with a media type. See [[document-file-attachment]] for the file part.

## When to use

- An accepted offer becomes work that is scheduled, performed in parts and closed with evidence.
- Each unit of work needs its own proof (a photo) before it counts as done.
- Two different results are issued from the same work: a report while the work runs and a certificate at the end.

## When to avoid

- The work has no items and no evidence: a single task entity is enough.
- Documents need approval steps and a reviewer: use [[document-review-state-machine]].

## Related

- [[work-status-lifecycle-enum]]: the four-state enumeration shared by the work order, the items and the reports
- [[generalization-base-entity]]: the base entity that work orders and work reports can extend
- [[document-registry-sequence]]: allocates the document numbers; a number is taken only when a document is created, never when it is regenerated
- [[document-file-attachment]]: the file entity behind documents and photos
- [[accept-reject-operations]]: the same pattern of a reason passed as operation input
- [[state-transition-history-entry]]: records each status change
