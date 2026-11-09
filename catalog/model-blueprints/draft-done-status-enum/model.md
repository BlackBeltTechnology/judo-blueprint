## Examples

### rackinspect
- **FaultRegistryStatus**: `rackinspect::entities::FaultRegistryStatus` -- DRAFT(1), DONE(2)
  - Used by: FaultRegistry entity (status attribute, default: DRAFT)
  - FaultRegistry transitions from DRAFT to DONE when the fault inspection is completed
- **OfferStatus**: `rackinspect::entities::OfferStatus` -- DRAFT(1), DONE(2)
  - Used by: Offer entity (status attribute)
  - Offer transitions from DRAFT to DONE when the pricing offer is finalized
