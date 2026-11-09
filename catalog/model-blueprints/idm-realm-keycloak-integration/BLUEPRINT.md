---
id: idm-realm-keycloak-integration
title: IDM Server and Realm Integration (Keycloak)
description: "A pair of entities that model an external identity management server (such as Keycloak) and the per-organization realm it hosts, with applications registered as clients in each realm."
aliases: []
keywords: [idm, realm, keycloak, oidc, multi-tenant, identity]
tags: [domain:model, layer:model, layer:backend, project:ubives, status:single-project]
category: pattern
status: single-project
projects: [ubives]
evidence: ["ubives:unrecorded"]
alternatives: []
fragment: idm-realm-keycloak-integration
diagram: { kinds: [entity, enum], members: types }
first_seen: 2026-03-05
last_updated: 2026-11-09
---
## Intent

Connect the platform to an external identity management server and give each organization its own authentication realm on that server. The platform keeps one connection to the server and manages the realms from there.

### One realm per organization

Each organization owns one realm. Users of the organization register and sign in inside that realm, so the realms stay separate from each other.

### The server is a configuration record

The identity server is a record with a URL and an optional name. It holds the realms it hosts. Its connection details are set once and read by the platform.

## Structure

The identity server entity has a required URL and an optional name. It is associated with zero or more realms.

The realm entity has a required name and an optional association to the server that hosts it. An organization composes at most one realm.

The application entity holds a required name, a required client identifier and a required client token. It is composed by an organization, and it represents a client registered in that organization's realm. Its instance operation deletes the application.

## Constraints

- The server URL is required. A realm must name a server only through the association.
- An organization has at most one realm. The realm is removed with the organization.
- Each application belongs to one organization and carries the client identifier and token of its realm client.
- The client token is a secret. It is written by backend code and not shown in the generated views.

## Variations

- **One shared realm.** Put every organization in one realm and separate them by an attribute. This removes the per-organization isolation the realm gives.
- **Realm per deployment.** Use one realm for the whole deployment and skip the organization association. This fits single-tenant installs.
- **Application as a shared registry.** Keep the client registry outside the organization. See [[application-vendor-integration-registry]] for a shared registry pattern.

## When to use

- Multiple organizations need separate sign-in namespaces on one identity server.
- Each organization registers its own clients.
- The platform must manage the server connection in one place.

## When to avoid

- A single realm is enough for all users.
- The identity provider is not OIDC-compatible or has no realm concept.
- Organizations must share one sign-in namespace.

## Related

- [[identity-account-organization-cluster]] — the accounts and organizations that use these realms
- [[application-vendor-integration-registry]] — a shared registry of external integrations
- [[external-api-adapter-provider-pattern]] — adapting an external provider behind a common interface
