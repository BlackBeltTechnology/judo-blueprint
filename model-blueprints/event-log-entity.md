---
id: event-log-entity
title: "Event Log Entity with Type Enum and Actor Reference"
usage_count: 3
first_seen: "2026-03-05"
last_updated: "2026-03-05"
projects:
  - alba
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
---

## Description

An Event entity that records domain-level events as a chronological log. Each event has a type attribute (typed to an EventType enum defining specific event kinds), a message string for human-readable details, a createdAt timestamp, a reference to the entity the event is about (e.g., product 0..1 ASSOC), and a reference to the user who performed the action (performedBy 0..1 ASSOC). The entity is non-CRUD, created by backend operations when significant state changes occur.

Unlike the full AuditLog pattern (which includes entityType/entityId string fields and denormalized userName), this is a lightweight, relation-based approach where the event directly links to the domain entity and actor via associations. The EventType enum defines the vocabulary of possible events (e.g., PRODUCT_CREATED, PRODUCT_FINALIZED, PRODUCT_APPROVED, PRODUCT_APPROVAL_REVOKED).

This pattern is suitable when events need to be displayed on a specific entity's timeline (via the entity's events relation) rather than in a platform-wide audit dashboard.

Some variants (e.g., kozut-eugyfel-client) denormalize the actor information into string attributes on the event (kezdemenyezoNev/initiatorName, celFelhasznaloNev/targetUserName) rather than using a relation to the User entity, and add a subsidiary Ertesites (Notification) entity composed by each event for user notification delivery.

Some variants (e.g., kozut-eugyfel-model-test) use a **generalization-based event hierarchy** instead of a type enum: an abstract Esemeny base entity with concrete subtypes (Tovabbitas, Lezaras, Megjegyzes, Letrehozas) that each extend the base entity via generalization. In this variant, the event type is determined by the concrete subtype rather than an enum attribute, and subtypes can carry additional type-specific attributes and relations (e.g., UgyintezoBeallitas has a celFelhasznalo relation that Lezaras does not). The base entity provides shared attributes (szoveg, idopont) and a relation to the initiating user (kezdemenyezo). This approach is used with static email-sending operations (emailKuldes, emailKuldesTobbCimzett) on the abstract base entity.

## Detection Query

```graphql
{ esm { entitytypes(where: { name: { eq: "Event" } }) {
  items { fqn name
    attributes { items { name } }
    relations { items { name lower upper relationKind } }
  }
} } }
```

```graphql
{ esm { enumerationtypes(where: { name: { eq: "EventType" } }) {
  items { fqn name members { items { name ordinal } } }
} } }
```

## Creation Mutations

```graphql
mutation { create(input: { enumerationType: {
  container: "{{NAMESPACE}}", name: "EventType"
} }) { success fqn } }
```

```graphql
mutation { create(input: { enumerationMember: {
  container: "{{NAMESPACE}}::EventType", name: "{{EVENT_NAME}}", ordinal: {{ORDINAL}}
} }) { success fqn } }
```

```graphql
mutation { create(input: { entityType: {
  container: "{{NAMESPACE}}", name: "Event",
  createable: false, updateable: false, deleteable: false
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Event", name: "type"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Event", name: "message"
} }) { success fqn } }
```

```graphql
mutation { create(input: { dataMember: {
  container: "{{NAMESPACE}}::Event", name: "createdAt"
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Event", name: "{{ENTITY_RELATION}}",
  target: "{{NAMESPACE}}::{{ENTITY_TYPE}}", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

```graphql
mutation { create(input: { oneWayRelationMember: {
  container: "{{NAMESPACE}}::Event", name: "performedBy",
  target: "{{NAMESPACE}}::User", lower: 0, upper: 1,
  relationKind: ASSOCIATION
} }) { success fqn } }
```

## Examples

### alba
- **Event entity**: `Alba::entities::Event` (non-CRUD)
  - Attributes: type (req, EventType enum), message, createdAt (req)
  - Relations: product (0..1 ASSOC to Product), performedBy (0..1 ASSOC to User)
- **EventType enum**: `Alba::entities::EventType` -- PRODUCT_APPROVED(1), PRODUCT_APPROVAL_REVOKED(2), PRODUCT_FINALIZED(3), PRODUCT_CREATED(4)
- Product entity has `events` (0..* ASSOC) relation to Event, creating a timeline of product lifecycle events
- **Transfer Objects**:
  - `Alba::services::AuthorEventTransfer` -- message, type (req), performedByUser, createdAt (req); relations: performedBy (0..1 AGGREGATION), product (0..1 AGGREGATION)
  - `Alba::services::AdminEventTransfer` -- createdAt (req), message, type (req), performedByUser; no relations (fully denormalized view)
- Events are displayed on both AdminProduct and AuthorProduct TOs via `events` (0..* ASSOC) relation

### kozut-eugyfel-client
- **Esemeny (Event) entity**: `e_ugyfelszolgalat::entities::Esemeny` (non-CRUD)
  - Attributes: azonosito (identifier), szoveg (text/message), idopont (timestamp), esemenyTipus (req, EsemenyTipus enum), celFelhasznaloNev (target user name), celFelhasznaloCimke (target user label), kezdemenyezoNev (req, initiator name), kezdemenyezoCimke (req, initiator label), szinkronizalt (synchronized flag)
  - Relations: ertesitesek (notifications 0..* COMPOSITION to Ertesites), bejelentes (report 1..1 TwoWay ASSOC to Bejelentes)
- **EsemenyTipus (EventType) enum**: `e_ugyfelszolgalat::entities::EsemenyTipus` -- LETREHOZAS(1, creation), LAZARAS(2, closure), MEGJEGYZES(3, comment), TOVABBITAS(4, forwarding), UJRESZTVEVO(5, new participant), MEGNYITAS(6, reopening), LEIRATKOZAS(7, unsubscription)
- Bejelentes (Report/Ticket) entity has:
  - `esemenyek` (events 0..* TwoWay ASSOC) -- full event history
  - `megjegyzesek` (comments 0..* DERIVED) -- filtered view: only events with non-empty text, sorted ASC
  - `tovabbitasok` (forwardings 0..* DERIVED) -- filtered view: all non-MEGJEGYZES events, sorted DESC
- **Key differences from alba**:
  - Actor info is denormalized as string attributes (kezdemenyezoNev, celFelhasznaloNev) rather than User relations
  - Each event COMPOSES child Ertesites (Notification) entities for delivery to affected users
  - Event type enum covers ticket lifecycle transitions (creation, closure, forwarding, commenting) rather than product lifecycle
  - A szinkronizalt (synchronized) boolean tracks whether the event has been synced to an external system (Jarokelo)
  - The parent Bejelentes entity exposes DERIVED filtered views of the events collection (megjegyzesek for comments, tovabbitasok for forwardings)
- **Transfer Objects**:
  - `munkatars::Esemeny` -- bejelentesAzonosito (DERIVED), szoveg, idopont, esemenyTipus (req), celFelhasznaloNev, kezdemenyezoNev (req) -- flattened event view for the worker actor

### kozut-eugyfel-model-test
- **Generalization-based event hierarchy** (instead of type enum):
  - **Esemeny (Event) abstract entity**: `e_ugyfelszolgalat::Esemeny::Esemeny` (non-CRUD, abstract)
    - Attributes: szoveg (text/message), idopont (timestamp)
    - Relations: kezdemenyezo (initiator 0..1 TwoWay ASSOC to Felhasznalo)
    - Static operations: emailKuldes (customImpl=true, EmailKuldesInput), emailKuldesTobbCimzett (customImpl=true, EmailKuldesTobbCimzettInput)
  - **UgyintezoBeallitas (AssigneeSettings) abstract entity** extends Esemeny:
    - Adds: celFelhasznalo (target user 1..1 OneWay ASSOC to Felhasznalo)
  - **Tovabbitas (Forwarding)** extends UgyintezoBeallitas -- concrete forwarding event
  - **Lezaras (Closure)** extends Esemeny -- concrete closure event
  - **Megjegyzes (Comment)** extends Esemeny -- adds ertesitesiLista (notification list 0..* ASSOC to Felhasznalo)
  - **Letrehozas (Creation)** extends Esemeny -- concrete creation event
- **Key differences from kozut-eugyfel-client**:
  - Event type is determined by the concrete entity subtype rather than an EsemenyTipus enum
  - Subtypes can have type-specific relations (UgyintezoBeallitas.celFelhasznalo, Megjegyzes.ertesitesiLista) that do not exist on all events
  - Two-level generalization: Esemeny -> UgyintezoBeallitas -> Tovabbitas
  - Email sending is implemented as static operations on the abstract Esemeny entity with dedicated input TOs (EmailKuldesInput: targy, szoveg, cimzett; EmailKuldesTobbCimzettInput: targy, szoveg, cimzettek 0..* Cimzett)
  - No denormalized actor name attributes -- uses relation (kezdemenyezo) to Felhasznalo directly
