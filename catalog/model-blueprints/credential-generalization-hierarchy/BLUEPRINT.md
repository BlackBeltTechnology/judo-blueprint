---
id: credential-generalization-hierarchy
title: Credential Generalization Hierarchy (Platform-Specific API Credentials)
description: An abstract Credential base that an account refers to polymorphically, with one concrete subtype per external platform holding that platform's secrets and settings.
aliases: [platform credential hierarchy, polymorphic credential, credential subtypes]
keywords: [credential, generalization, hierarchy, platform, abstract, subtype, polymorphic lookup]
tags: ["domain:model", "layer:model", "layer:backend", "project:indamedia-adtrack", "status:single-project"]
category: pattern
status: single-project
projects: [indamedia-adtrack]
evidence: ["indamedia-adtrack:unrecorded"]
alternatives: [interface-specification-generalization-hierarchy, partner-generalization-hierarchy]
first_seen: 2026-03-05
last_updated: 2026-11-10
---
## Intent

Let an account hold one set of API credentials without knowing which platform they belong to. Each platform keeps its own fields in its own subtype, so the platform-specific fields stay typed and validated.

### The base type is abstract and polymorphic

Credential has no fields of its own. An account refers to the base type, and the platform decides which subtype holds the real data.

### Each platform has its own subtype

A platform's credential fields live only in its subtype. Adding a platform means adding one subtype and one enumeration value, not changing the existing ones.

## Structure

The Credential entity is abstract. It has no attributes and is not createable, updateable or deleteable. An Account refers to zero or one Credential.

GoogleCredential extends Credential with a customer identifier, a delegated account (e-mail), a developer token and a JSON key file, all required. MetaCredential extends Credential with no fields yet, as a placeholder for another platform.

The Account has a platform (required, from the Platform enumeration with values META and GOOGLE) and an active flag (required, default true).

## Constraints

- An account holds at most one credential. Setting a new credential replaces the old one.
- The platform on the account must match the subtype that holds its credential. The model does not enforce this link; the operations must.
- A platform without an implementation must fail clearly, not fall back to another platform's credential.
- Interceptors do not run for the custom operations that set or test a credential. Each one checks the platform and the caller's rights itself.
- Secrets such as the key file and the developer token are never returned to the client; only a masked form is shown.

## Variations

- **Single subtype per platform, many per account.** If an account can hold several credentials for one platform, the association becomes to-many and each subtype stays the same.
- **Shared fields on the base.** Fields that every platform needs, such as an identifier or an expiry, can move to the abstract base, but only when every subtype really uses them.
- **Subtype without fields.** A subtype with no fields is a valid placeholder while the platform is planned.

## When to use

- Several external platforms each need different credential fields.
- The account is the same kind of object for every platform, and only the credential differs.
- Each platform's fields must stay typed, required and validated.

## When to avoid

- Only one platform exists and will not grow. A single credential entity is simpler.
- The credentials are one generic key and value store. A plain structure is enough.
- Every platform shares the same fields. Put them on one entity with a platform value.

## Related

- [[interface-specification-generalization-hierarchy]]: another generalization hierarchy, with an abstract interface and concrete specifications
- [[partner-generalization-hierarchy]]: a generalization of one party type into subtypes
- [[post-generalization-hierarchy]]: a generalization of content into subtypes
- [[derived-attribute-flattening]]: exposing a subtype field on the account without copying it
