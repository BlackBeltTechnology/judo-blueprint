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
