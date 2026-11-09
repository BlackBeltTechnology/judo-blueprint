## Examples

### skillmatrix-model
- **LanguageSkillLevel enum**: `SkillMatrix::LanguageSkillLevel`
  - Members: BEGINNER(1), CONVERSATIONAL(2), FLUENT(3), NATIVE(4)
  - Ordinals increase with proficiency level

- **LanguageSkill entity**: `SkillMatrix::LanguageSkill` (non-CRUD)
  - Attributes: level (LanguageSkillLevel, req), note (Text, optional)
  - Relations: language (1..1 OneWay ASSOC Language)
  - Owned by User via `languageSkills` [0..*] COMPOSITION

- **Language entity**: `SkillMatrix::Language` (reference data)
  - Attributes: code (String, req, identifier)
  - No relations, no operations
  - Represents ISO language codes (e.g., "en", "hu", "de")

- **Transfer object projections**:
  - hrEmployee::LanguageSkill -- languageCode (DERIVED from language.code), level (MAPPED), note (MAPPED) + language relation (1..1 AGGREGATION Language)
  - hrEmployee::Language -- code (MAPPED)
  - The HR employee can manage language skills for professionals through the Professional TO's `languages` relation
