## Overview

The abstract Post and its subtypes (News, Offer, Request, Announcement) are handled by a small service layer: a facade, a creation service that builds each subtype, and a lifecycle service that changes status. Each subtype has its own custom operations, and they call the shared services. The services and their names are project code, not platform classes.

## Implementation Pattern

### Creation sets the shared fields first

A creation method sets the fields every post has (title, description, draft status, creation time, the type discriminator, author and organization). It then sets the fields of its own subtype. The type discriminator must match the subtype, so each creation method sets it itself.

### Lifecycle changes check state first

Publish, unpublish, edit and delete check the current status before they change it. Publishing moves a draft to published. Deleting a draft removes it; deleting a published post changes its status to deleted and removes its feed entry, so the history of the feed stays consistent.

### Polymorphic handling

When a subtype must appear in a shared list, such as the feed, the code treats it as a Post. Because the platform does not allow an abstract entity as a field type, code that needs a shared list works with the base type through the platform's `adaptTo` type conversion; the agent-docs describe `adaptTo` only between the service and entity layers, so using it for the base type is project practice. Code that needs subtype fields uses the subtype type.

### Expiry is a scheduled job

Offers expire when their validity end passes, and requests when their deadline passes. A scheduled job queries published items with those dates in the past and sets them to expired. This runs outside any user operation, so it is not an interceptor and it does not depend on the hierarchy.

### Business faults

A rule that fails in an operation, such as publishing an offer whose validity has already ended, is a modeled fault (HTTP 422 with the X-Fault header) that is declared on the operation in the model; the platform generates a checked `<Fault>Exception` for it, and the operation code throws it. An interceptor cannot throw a modeled fault; it would use `InterceptorCallBusinessException`. A missing required field is a ValidationException (HTTP 400) and comes from the platform.

### Interceptors do not cover custom operations

The creation and lifecycle operations are custom, so an interceptor does not run for them. Any audit row or guard must be called from the operation itself.

## Examples

### Example (project code)
- Pattern: creation sets draft status and the type discriminator; publishing moves to published and creates a feed entry; delete is hard for drafts and soft for published posts.
- Notable: the expiry job handles offers by their validity end and requests by their deadline. The `adaptTo` conversion lets feed code treat any subtype as a Post (project practice).
