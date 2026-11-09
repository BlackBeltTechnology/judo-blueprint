## Examples

### itracker
- **Enum**: `itracker::entities::RiskLevel` -- LOW(1), MEDIUM(2), HIGH(3)
- **Initiative entity** (`itracker::entities::Initiative`): uses `riskLevel` attribute to classify cost-saving initiatives by risk
  - The riskLevel attribute has no default value -- it must be set explicitly when creating an initiative
  - Used alongside other classification attributes: SavingType (FIXED/VARIABLE) and ActionType (PRICING/USAGE/LABOR/OEE/SCRAP)
- **User Initiative TO** (`itracker::actors::user::Initiative`): exposes `riskLevel` attribute for display and editing in the initiative form
