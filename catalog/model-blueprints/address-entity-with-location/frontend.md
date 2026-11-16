## Frontend guidance

### Keep the address form and the view in step

The address form and the view-edit section show the same fields. Use the same computation on both, so the address line shown in the view matches what the form computes.

- Recompute the address line when a part loses focus, and only write it when the manual override flag is off.
- Keep the manual override flag visible in the form. When it is on, the computed value is not overwritten.

### Fill the city from the postal code

When the postal code is reference data with a list of cities, fill the city automatically only when exactly one city matches. When several match, leave the city empty for the user to choose.

### Show the location read-only

The latitude and longitude come from a map step or a geocoding service, not from typed input. Show them as read-only values in the view, and keep the location fields out of the generated edit form unless a map control is provided.

## Examples

### Variant seen in practice

- Framework: React.
- Form action hooks on the organization admin panel address fetch the address with the city and the postal code, and fill the city when one postal code maps to a single city.

### Second variant seen in practice

- Framework: React.
- Five parallel hooks (form and view-edit for the partner address and the company address, plus the partner create form) recompute the address line on blur. The manual override flag lets the user keep their own text.
- This variant uses a country association instead of city and postal code lookups, so it has no postal code auto-fill.
