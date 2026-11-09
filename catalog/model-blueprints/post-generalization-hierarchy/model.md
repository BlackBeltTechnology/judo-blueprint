## Examples

### mlszksz-platform
- **Abstract base**: `MLSZKSZPlatform::entities::Post` (abstract=true)
  - Attributes: title (req), description (req), status (req), createdAt (req), publishedAt, postType (req)
  - Relations: author (1..1 ASSOC to User), organization (1..1 ASSOC to Organization), inquiries (0..* COMPOSITION to Inquiry)
- **Concrete subtypes** (each generalizes Post):
  - `News` -- adds: image
  - `Offer` -- adds: validFrom (req), validUntil (req), price, isExpired; relation: capabilities (0..* ASSOC)
  - `Request` -- adds: deadline (req), isExpired; relation: capabilities (0..* ASSOC)
  - `Announcement` -- adds: isSensitive (default: false), isStrategic (default: false); relation: documents (0..* ASSOC)
- **Enums**: PostStatus (DRAFT, PUBLISHED, EXPIRED, DELETED, PENDING_REVIEW), PostType (NEWS, OFFER, REQUEST, ANNOUNCEMENT)
