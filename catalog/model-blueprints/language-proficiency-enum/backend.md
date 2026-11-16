## Backend guidance

### Store the enumeration by ordinal

Enumerations travel as ordinals on the REST wire, and the response conversion turns an ordinal back into the literal. In the generated Java, `query<Attribute>()` on an enumeration attribute can fail with a `ClassCastException` because the runtime delivers the ordinal; read the value through the transfer object or convert it with `<Enum>.getByOrdinal(...)`. Keep the ordinals fixed once data exists. A new level is added with a new ordinal in order, never by renumbering.

### Validate the level on write

Accept a level only if it is one of the four members. The platform docs do not say how an out-of-range ordinal is rejected, so check it in your version. If you reject it in a custom operation, report it as a field error (`ValidationException`, HTTP 400), not a business fault (422).

### Write skills through the owning user

Create and change a skill through an operation on the user, so the skill is always attached to a user. A custom operation is not intercepted by the platform, so keep any permission check inside it. Do not create a skill with no owner.

### Look up the language by code

The language is a shared reference. Find it by its code, and reject a code that does not exist, instead of creating a copy.

### Compare levels by ordinal

When the application must check for a minimum level, compare ordinals in Java code; JQL offers only equality on enumerations. The order of the enumeration is the order of proficiency. This is project practice, not a platform feature.

## Examples

- Four levels, from beginner to native. A user composes its language skills, each with one language reference and one level.
- A user view maps the level and the note, and shows the language code derived from the reference record.
