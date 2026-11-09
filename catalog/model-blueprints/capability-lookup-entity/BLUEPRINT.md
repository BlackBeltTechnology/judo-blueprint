---
id: capability-lookup-entity
title: Capability/Tag Lookup Entity
description: A Capability lookup entity with a soft on/off flag, tagged onto other entities through many-to-many associations.
aliases: [capability, tag lookup, classification entity]
keywords: [capability, tag, lookup, association, toggle, soft-disable]
tags: [domain:model, layer:model, layer:backend, layer:frontend, project:mlszksz-platform, status:single-project]
category: pattern
status: single-project
projects: [mlszksz-platform]
evidence: ["mlszksz-platform:unrecorded"]
alternatives: [reference-data-lookup-entity]
fragment: capability-lookup-entity
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-09
---
## Intent

Keep a managed list of capabilities, or tags, that other entities can reference. Administrators create and maintain the list. A capability can be switched off so it stops appearing as a choice, while records that already carry it keep their tags.

### Tags are associations, not owned parts

Organizations and offers reference capabilities through many-to-many associations. Removing a tag leaves the capability in the list. A capability is not owned by any one record.

### Turning off hides, it does not delete

The isActive flag removes a capability from new choices. Existing tags stay valid, and the capability can be turned back on later.

## Structure

The Capability entity has a required name identifier, an optional description text and a required isActive boolean that defaults to true. Organization and Offer each hold a 0..* association to Capability. Other entities can add the same association.

## Constraints

- A capability is a shared lookup. It is never composed inside an organization or an offer.
- The name is the identifier and is required. Uniqueness is enforced by project logic, not by the model.
- Choice lists show only active capabilities. Existing tags show all of them.
- Administrators manage the list. Other actors see it as a read-only projection.

## Variations

- **Flat tags.** Only the name is needed. Drop the description and the flag when the list is small and never retired.
- **Hierarchical categories.** A capability with a parent capability forms a tree. Model the parent as a self-association, and keep the flag on each node.
- **Per-actor visibility.** Other actors see only the active capabilities, through a projection that filters on isActive.

## When to use

- Records need one or more tags from a shared, managed list.
- Tags must be added and retired without losing history on the records that carry them.
- Several entities share the same classification.

## When to avoid

- The list is fixed and never changes. An enumeration is simpler.
- The lookup has its own fields that matter to each tagged record. Use a reference-data entity with its own relations.
- Records must own their tags, so deleting a record removes them. Use a composition for owned tags.

## Related

- [[reference-data-lookup-entity]] — the general reference list pattern this entry specialises with a flag and many-to-many tags
- [[active-inactive-status-enum]] — a two-state status when the on/off state is not a managed list
- [[contact-info-composition-cluster]] — owned parts that are composed rather than tagged
