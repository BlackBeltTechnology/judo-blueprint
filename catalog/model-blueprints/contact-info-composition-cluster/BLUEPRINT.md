---
id: contact-info-composition-cluster
title: Contact Info Composition Cluster (Email, Phone, Address)
description: A set of small contact entities composed under one parent, each with an active flag and a primary designation, so the parent can hold several e-mails, phones and addresses with one preferred.
aliases: [contact details, multiple contact points, primary contact]
keywords: [contact, composition, email, phone, address, primary, active flag, toggle]
tags: ["domain:model", "layer:model", "layer:backend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: pattern
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:model/rackinspect.model"]
alternatives: [partner-with-contact-details]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let one parent entity hold many contact points of each kind, with one of them marked as primary. Each contact point can be switched off without being deleted, so history stays readable and the preferred contact is always clear.

### Contact points are composed under the parent

Each contact entity is owned by its parent through a composition. Deleting the parent removes its contacts. A contact cannot exist on its own.

### One contact is primary, found through an association

The parent keeps a separate association to its primary contact (0..1). The contact itself does not know it is primary. Setting a new primary replaces the association and leaves the others untouched.

### Contacts are switched off, not deleted

Every contact has an active flag, true by default. Toggle operations flip it. This keeps old contact details on record for audit and lets a person be re-enabled.

## Structure

The parent (for example a partner or a user) has three composition relations, each to zero or more contacts: EmailAddress, PhoneNumber and Address. It also has one optional association to a primary EmailAddress.

EmailAddress holds an e-mail address (required, e-mail type), an optional name and an active flag (required, default true). PhoneNumber holds a phone number (required, phone type), an optional name, an active flag (required, default true) and a fax flag (default false). Address holds a street name, a city and a postal code (all required), an optional full address text, and an active flag (required, default true).

Each contact entity has an instance toggle-active operation. The e-mail contact type also has a toggle-primary operation.

## Constraints

- Contacts belong to exactly one parent. Deleting the parent deletes its contacts, because a composition cascades. The primary link is an association and cascades nothing: deleting the primary contact clears the parent's primary link and leaves the parent in place. The link is optional (0..1) and has no reverse cascade delete, so the contact delete is not refused.
- The primary association points to one of the parent's own contacts, never to another parent's.
- The active flag is required and defaults to true. A contact that is switched off stays visible in the parent but is not used for notifications.
- Creating a contact does not set the primary. Setting the primary is a separate step, so the first contact added is not made primary by accident.
- Interceptors run only on built-in operations. Toggle operations are custom, so they must check their own rules, such as keeping at least one active primary. A refusal is a business fault, which the operation must declare in its `faults`.

## Variations

- **Several contact sets per parent type.** A system with different parents (for example a partner, a company record and a user) can use one set of contact entities per parent, each with the same structure. Keep the parents separate so their rules do not mix.
- **Flags for role.** Instead of one primary, the contact can carry flags such as billing, delivery or headquarters. Use this when a contact has more than one role.
- **Bank accounts as a fourth kind.** A bank account follows the same pattern with a currency relation. See [[partner-with-contact-details]] for the partner form.

## When to use

- A parent needs several contact points of the same kind, with one preferred.
- Contact details change over time and old values must stay visible but inactive.
- The contact kinds have the same lifecycle, so one pattern covers all of them.

## When to avoid

- A parent has exactly one contact of each kind. Plain attributes on the parent are simpler.
- Contacts are shared between parents. Use an association to a shared entity instead of composition.
- Contacts need their own permissions, workflow or history. Model them as independent entities.

## Related

- [[partner-with-contact-details]]: a partner that holds contact details, the same need in a simpler form
- [[address-entity-with-location]]: an address entity with location data, when an address needs more than text fields
- [[address-field-auto-composition]]: computing a single address line from its parts
- [[masked-input-integration]]: input masking for phone and bank-type fields
- [[safe-failure-pattern]]: keeping the parent change valid when a side effect fails
