---
id: ticket-case-management-entity
title: "Ticket/Case Management Entity with Forwarding, Events, and Permission Guards"
usage_count: 2
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
---

## Description

A Ticket/Case entity (Bejelentes = Report) that models a multi-step customer service workflow with assignment, forwarding, commenting, and closure operations. The entity carries an identifier, a status enum (AKTIV/LEZART), a subject, a location/description, reporter contact info, and timestamp fields. It links to multiple user roles: an assignee (ugyintezo = case worker), a responsible person (felelos), and participants (resztvevok). It maintains a full event log (esemenyek) via a bidirectional association to an Event entity, with DERIVED filtered views for comments (megjegyzesek) and forwardings (tovabbitasok) using getter expressions with filters and sorts.

The key architectural feature is **permission guard attributes**: multiple DERIVED boolean attributes on the entity (e.g., tovabbitasEngedely, lezarasEngedely, megnyitasEngedely, megjegyzesEngedely, resztvevoHozzadasEngedely, leiratkozasEngedely) that compute whether the current user is permitted to perform each operation. These guards are based on the ticket's state, the current user's role, and their relationship to the ticket (assignee, responsible, participant). The transfer object exposes these guards alongside the corresponding operations, enabling the UI to show/hide action buttons dynamically.

Operations on the ticket include:
- **tovabbitas** (forward) -- reassign to another user, with a TovabbitasAction input TO carrying szoveg (text) and celFelhasznalo (target user 1..1)
- **tovabbitasFelelosnek** (forward to responsible) -- reassign to the designated responsible person
- **lezaras** (close) -- close the ticket
- **megnyitas** (reopen) -- reopen a closed ticket
- **megjegyzes** (comment) -- add a comment
- **hozzaadResztvevo** (add participant) -- add a user as participant, with a ResztvevoAction input TO carrying ujResztvevo (new participant 1..1)
- **leiratkozas** (unsubscribe) -- remove self as participant

The ticket also supports image attachments (kepek 0..* COMPOSITION to Kep entity with a URL attribute) and external system integration (via a szinkronizal STATIC operation and external identifiers like jarokeloAzonosito, eUgyfelszolgalatAzonosito).

An Erkezteto (Dispatcher/Router) entity defines default responsible person assignment per BejelentesTipus (report type), enabling automatic routing of incoming tickets.

Some variants (e.g., kozut-eugyfel-model-test) use a generalization-based approach where the base Bejelentes entity is abstract and concrete subtypes (JarokeloBejelentes, EUgyfelszolgalatBejelentes) add source-specific attributes. In this variant, the event log also uses a generalization hierarchy (abstract Esemeny with concrete subtypes: Tovabbitas, Lezaras, Megjegyzes, Letrehozas) rather than an event type enum.

## Detection Query

```graphql
{ esm { entitytypes(limit: 50) {
  items { fqn name
    attributes { items { name required memberType } }
    relations { items { name lower upper relationKind memberType } }
    operations { items { name operationType } }
  }
} } }
```

Look for entities with:
- A status attribute typed to a two-state enum (active/closed)
- Multiple user relations (assignee, responsible, participants)
- An events/comments relation to an Event entity
- Multiple instance operations for workflow transitions (forward, close, reopen, comment)
- Multiple DERIVED boolean attributes for permission guards

## Creation Mutations

### Status enum

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "{{TICKET_NAME}}Status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}Status", name: "ACTIVE", ordinal: 1
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}Status", name: "CLOSED", ordinal: 2
} }) { success fqn } }
```

### Ticket entity

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "{{TICKET_NAME}}",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "identifier"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "status"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "subject"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "description"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "createdAt"
} }) { success fqn } }
```

### User relations

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "assignee",
  target: "{{NAMESPACE}}::User", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "responsible",
  target: "{{NAMESPACE}}::User", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Event relation

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "events",
  target: "{{NAMESPACE}}::Event", lower: 0, upper: -1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

### Workflow operations

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "forward",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "close",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "reopen",
  operationType: INSTANCE
} }) { success fqn } }
```

```graphql
mutation { create(input: { operation: {
  container: "{{NAMESPACE}}::{{TICKET_NAME}}", name: "comment",
  operationType: INSTANCE
} }) { success fqn } }
```

### Forward action input TO

```graphql
mutation { create(input: { transferObjectType: {
  container: "{{NAMESPACE}}", name: "ForwardAction"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::ForwardAction", name: "text"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::ForwardAction", name: "targetUser",
  target: "{{NAMESPACE}}::User", lower: 1, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

## Examples

### kozut-eugyfel-client
- **Bejelentes (Report/Ticket) entity**: `e_ugyfelszolgalat::entities::Bejelentes`
  - Core attributes: azonosito (req, identifier), allapot (req, BejelentesAllapot enum), targy (req, subject), helyszin (req, location), lakottTerulet (req, boolean inhabited area), bejelentoNeve (reporter name), szoveg (text), bejelentoEmail (reporter email), url, bejelentesTipus (BejelentesTipus enum), letrehozasIdopont (creation timestamp), lezaroDokumentum (closing document), jkStatusz (external status)
  - External system identifiers: jarokeloAzonosito (Jarokelo ID), eUgyfelszolgalatAzonosito (e-service ID)
  - DERIVED display fields: felelosNev (responsible name), ugyintezoNev (assignee name)
  - Permission guard DERIVED booleans: tovabbitasEngedely, tovabbitasFelelosnekEngedely, megjegyzesEngedely, lezarasEngedely, resztvevoHozzadasEngedely, megnyitasEngedely, leiratkozasEngedely
  - Relations: ugyintezo (assignee 0..1 TwoWay ASSOC to Felhasznalo), felelos (responsible 0..1 OneWay ASSOC to Felhasznalo), resztvevok (participants 0..* TwoWay ASSOC to Felhasznalo), esemenyek (events 0..* TwoWay ASSOC to Esemeny), kepek (images 0..* COMPOSITION to Kep), megjegyzesek (comments 0..* DERIVED from events), tovabbitasok (forwardings 0..* DERIVED from events)
  - Instance operations: tovabbitas, tovabbitasFelelosnek, lezaras, megnyitas, megjegyzes, hozzaadResztvevo, leiratkozas
  - Static operations: szinkronizal, letrehozJarokeloBejelentes, letrehozEUgyfelszolgalatBejelentes, letezikJarokeloBejelentes, nyitottJarokeloBejelentesek
- **BejelentesAllapot enum**: `e_ugyfelszolgalat::entities::BejelentesAllapot` -- AKTIV(1), LEZART(2)
- **BejelentesTipus enum**: `e_ugyfelszolgalat::entities::BejelentesTipus` -- JAROKELO(1), ALTALANOS(2)
- **EsemenyTipus enum**: `e_ugyfelszolgalat::entities::EsemenyTipus` -- LETREHOZAS(1), LAZARAS(2), MEGJEGYZES(3), TOVABBITAS(4), UJRESZTVEVO(5), MEGNYITAS(6), LEIRATKOZAS(7)
- **Action input TOs**:
  - `TovabbitasAction` -- szoveg (text) + celFelhasznalo (target user 1..1 ASSOC)
  - `ResztvevoAction` -- ujResztvevo (new participant 1..1 ASSOC)
  - `Lezaras` (unmapped) -- szoveg + lezaroDokumentum
  - `Megjegyzes` (unmapped) -- szoveg
  - `Megnyitas` (unmapped) -- szoveg
- **Erkezteto (Dispatcher)**: `e_ugyfelszolgalat::entities::Erkezteto` -- bejelentesTipus (req, identifier) + felelos (0..1 ASSOC to Felhasznalo); maps report types to default responsible users
- **Kep (Image)**: `e_ugyfelszolgalat::entities::Kep` -- url (req); composed by Bejelentes for photo attachments
- **Worker (Munkatars) detail view TO** (`munkatars::BejelentesMegtekinto`): exposes all 23 attributes + 7 permission guards + 7 mapped operations + 4 AGGREGATION relations (tovabbitasok, esemenyek, resztvevok, kepek) -- the richest projection of the ticket entity
- **Admin summary view TO** (`admin::Bejelentes`): exposes only azonosito, letrehozasIdopont, allapot, felelosNev, ugyintezoNev + felelos/ugyintezo relations -- a minimal list view
- **External app creation view TO** (`eUgyfelAlkalmazas::Bejelentes`): exposes only display (DERIVED) + letrehoz (create STATIC operation) -- API-level creation only

### kozut-eugyfel-model-test
- **Simplified test variant** of the kozut-eugyfel-client ticket system using **generalization hierarchies** instead of a flat entity model
- **Bejelentes (base Report) entity**: `e_ugyfelszolgalat::Bejelentes::Bejelentes` (non-CRUD)
  - Core attributes: targy (req, subject), szoveg (text), allapot (req, BejelentesAllapot enum), helyszin (req, location), bejelentoNeve (req, reporter name)
  - Relations: kepek (images 0..* COMPOSITION to Kep), esemenyek (events 0..* ASSOC to Esemeny), bejelentesTipus (1..1 ASSOC to BejelentesTipus), felelos (0..1 DERIVED ASSOC to Felhasznalo -- computed via event history), ugyintezo (0..1 TwoWay ASSOC to Felhasznalo)
  - Instance operations: tovabbitas, lezaras, tovabbitasRogzites, megjegyzes
- **JarokeloBejelentes** (extends Bejelentes): adds jarokeloAzonosito (req), url; static operations: szinkronizal (customImpl=true), letrehoz2
- **EUgyfelszolgalatBejelentes** (extends Bejelentes): adds lakottTerulet (req, boolean), bejelentoEmail, eUgyfelszolgalatAzonosito (req); static operation: letrehoz
- **BejelentesAllapot enum**: AKTIV(1), LEZART(2) -- same as production variant
- **BejelentesTipusMegnevezes enum**: JAROKELO(1), ALTALANOS(2)
- **BejelentesTipus entity**: megnevezes attribute (typed to BejelentesTipusMegnevezes enum) + felelos (0..1 ASSOC to Felhasznalo)
- **Event hierarchy** uses generalization instead of event type enum: abstract Esemeny with concrete subtypes Tovabbitas (extends UgyintezoBeallitas), Lezaras (extends Esemeny), Megjegyzes (extends Esemeny), Letrehozas (extends Esemeny)
- **Key differences from kozut-eugyfel-client**: no permission guard DERIVED booleans, no participants (resztvevok), no reopen operation, events use generalization hierarchy instead of type enum, report types use a separate entity (BejelentesTipus) with an enum attribute rather than a direct enum on the ticket, the felelos (responsible) relation is DERIVED from event history using a complex getter expression
