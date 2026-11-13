---
id: post-generalization-hierarchy
title: Abstract Post with Concrete Content Subtypes
description: An abstract Post base entity holding the common content attributes and relations, with concrete subtypes (News, Offer, Request, Announcement) that add their own fields through generalization.
aliases: [abstract post, content subtypes]
keywords: [abstract, post, concrete, content, subtypes, generalization, hierarchy]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:model/MLSZKSZPlatform.model"]
alternatives: [credential-generalization-hierarchy]
fragment: post-generalization-hierarchy
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Publish several kinds of content (news, offers, requests, announcements) through one lifecycle and one feed. Common fields and relations live on an abstract Post. Each kind adds only the fields it needs, so the feed and the status rules are written once, and each kind keeps its own form and page.

### One abstract base for the shared fields

Title, description, status, creation and publication times, the type discriminator, the author and the organization are declared once on Post. Subtypes inherit them and never repeat them.

### Each kind is a concrete subtype

News, Offer, Request and Announcement each extend Post and add their own attributes. An Offer has a validity period and a price; a Request has a deadline; an Announcement has sensitivity flags. Each subtype is created and read through its own generated pages.

## Structure

Post is abstract and is not created directly; its subtypes are created. Post carries a status enumeration (draft, published, expired, deleted and pending review), a post-type enumeration that names the kind, and the common text, timestamp and date attributes. Post has a required association to User (the author) and a required association to Organization. Post also has a composition to Inquiry (a list the subtypes may use).

Each subtype generalizes Post. News adds an optional image. Offer adds required validity dates, an optional price and an expired flag, and an association to Capability (zero or more). Request adds a required deadline, an expired flag and the same capability association. Announcement adds two optional flags and an association to documents.

## Constraints

- The JSL build rejects an abstract entity as a field type and allows it only as a base to inherit from. So no relation can target Post; relations target concrete subtypes.
- The subtypes are the only entities that are created. Post itself is the shared base and is read through its subtypes or through a polymorphic list.
- A post starts in draft status. Publishing moves it to published; a published post is removed by changing its status, not by deleting its row, so feed history stays readable.
- Required attributes on a subtype are validated by the platform; a missing value is a field error (ValidationException, HTTP 400).
- Lifecycle rules such as "an offer cannot be published after its validity ends" are business rules raised as modeled faults (HTTP 422) declared on the operation and thrown by its code. The platform does not do this check; it is project practice.
- Interceptors do not run for custom operations, so the lifecycle checks and the feed updates must be called from the custom operations themselves.

## Variations

- **Abstract base with subtypes.** The shape used here. Fields are shared, and each kind has its own entity.
- **Single entity with a type field.** All kinds share one entity and a type enumeration. Use this when the kinds differ in only one or two attributes.
- **Separate entities without a base.** Each kind is a standalone entity that repeats the common fields. Use this when the kinds never appear in one list.
- **Expiry by scheduled job.** A scheduled job, not a field check, moves offers and requests to expired. This is project code and is independent of the hierarchy.

## When to use

- Several content kinds share fields, a status lifecycle and one list or feed.
- A polymorphic list must show all kinds together.
- Each kind needs its own form, page and fields.

## When to avoid

- The kinds share almost no attributes. A single entity with a type field is simpler.
- A kind needs its own lifecycle that the others do not have. Model that kind separately.
- Users must change the kind of an existing post. Subtypes cannot be converted in place.

## Related

- [[credential-generalization-hierarchy]] — the same abstract-base pattern for platform credentials
- [[interface-specification-generalization-hierarchy]] — an abstract base with concrete subtypes for specifications
- [[partner-generalization-hierarchy]] — another generalization hierarchy used for partners
