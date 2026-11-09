---
id: attribute-renaming-in-transfer
title: Attribute Renaming in Transfer Projection
description: "Transfer objects map entity attributes to differently-named transfer attributes, providing more meaningful or context-appropriate names for the API/UI layer."
aliases: []
keywords: [attribute, renaming, transfer, projection]
tags: ["domain:model", "layer:model", "project:trivia", "status:single-project"]
category: transfer
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
related: [derived-attribute-flattening, actor-based-transfer-projection]
fragment: pending
first_seen: 2026-03-04
last_updated: 2026-03-06
format: legacy
---
## Description

Transfer objects map entity attributes to differently-named transfer attributes, providing more meaningful or context-appropriate names for the API/UI layer. This includes renaming stored attributes (via mapped binding) and renaming derived attributes (via getter expressions that reference the original field).

## Structure

- Mapped attribute with a different name than the entity attribute it binds to
- Derived attribute whose getter references the entity attribute under a new name
- Examples: `result -> score`, `timestampOfCreation -> timestampOfUpload`

## Examples

### Trivia
`admin::Test.result` maps to entity `Test.score` (renamed for the admin UI context). `admin::Upload.timestampOfCreation` maps to `self.timestampOfUpload` (unified naming in the transfer layer). Both provide more intuitive names for the consumer.

### AMS-Frontend
`manager::Subordinate.identifier` maps to `User.email` -- the email attribute is renamed to `identifier` in the subordinate context, providing a more semantically appropriate name. The Manager actor sees subordinate users with their email displayed as an identifier field rather than an email field.

## Trade-offs

- Pros: API/UI names can differ from storage names, enables consistent naming across transfers
- Cons: Mapping indirection can make debugging harder, must document the name mapping
- Prefer when: Entity attribute names are technical/internal and a more user-friendly name is needed at the API level

## Related

- [[derived-attribute-flattening]]
- [[actor-based-transfer-projection]]

