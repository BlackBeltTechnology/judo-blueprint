## Frontend guidance

### Recompute the summary on blur of each part

Give every address part a blur handler. Each handler calls one shared function that joins the non-empty parts into the summary. Register the handlers on each form and view-edit section that edits the address, so the summary stays current in every context.

- Join the non-empty parts with the separators the address format uses. Do not add a separator for an empty part.
- Write the summary through the form's own store-diff call, so the change is part of the normal save.

### Respect the manual override flag

Before recomputing, check the manual override flag on the address. When it is set, return without writing the summary. Show the flag as a toggle next to the summary, so the user can turn it on or off.

- When the flag is turned off, recompute the summary once so it matches the parts again.

### Register the hooks per page

Generated hook keys are per page or container (names end with the actions hook interface key). Register one set of blur handlers for each page that edits the address. Do not copy a fixed key from another page.

## Examples

### rackinspect

- Framework: React.
- Blur handlers for the street name, public place category, number, building, staircase, floor, door and lot number, plus a handler for the manual override toggle. All of them call one shared update function.
- The same handlers are registered for the partner address and the company address, in both the form and the view-edit section.
