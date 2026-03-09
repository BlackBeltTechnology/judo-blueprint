---
id: "idm-realm-keycloak-integration"
title: "IDM/Realm Keycloak Integration Entity Cluster"
score: 44.0
usage_count: 1
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - ubives
---
## Description

A pair of entities that model external Identity Management (IDM) system integration, specifically for Keycloak or similar OIDC providers. The structure consists of:

- **IdmEntity** -- represents an external identity management server instance with a URL (the Keycloak server address) and an optional name. It holds a one-to-many association to Realm entities, since one IDM server can host multiple realms.
- **RealmEntity** -- represents a Keycloak realm (a security namespace) with a name attribute and a back-reference to its IDM server (0..1 ASSOCIATION). A realm is composed by an Organization (0..1 COMPOSITION), meaning each organization can have its own dedicated authentication realm.

This pattern enables multi-tenant authentication where each organization gets its own Keycloak realm for user registration, while the platform manages the IDM server connection centrally. The Initializer entity has an `initDefaultIdm` operation to seed the default IDM server configuration on first startup. Application entities (composed by Organization) carry applicationId and applicationToken fields for Keycloak client registration.

## Model Definition

See [model.md](model.md) for detection queries, creation mutations, and examples.
