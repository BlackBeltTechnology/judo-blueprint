## Examples

### reserve-app
- **FreightState enum**: `ReserveApp::entities::FreightState`
  - Members: NOT_SUBMITTED(1), SUBMITTED(2), REJECTED(3), APPROVED(4), SUSPENDED(5), ARRIVED(6), FINISHED(7), DELAYED_UNLOADING(8), DELAYED_ARRIVAL(9)
  - Used by: FreightReservation entity (state attribute)
  - Workflow: Partner creates reservation (NOT_SUBMITTED) -> submits to logistician (SUBMITTED) -> logistician approves (APPROVED) or rejects (REJECTED) -> vehicle arrives (ARRIVED) -> unloading completes (FINISHED)
  - Either party can suspend a reservation (SUSPENDED), tracked via suspendedByPartner and suspendedByLogistician relations to User
  - Delay states (DELAYED_ARRIVAL, DELAYED_UNLOADING) track schedule deviations
- Supports 5 actor roles (AdminActor, PartnerActor, LogisticianActor, DoormanActor, Readonly) that participate in different stages of the freight lifecycle
