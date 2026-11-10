## Backend guidance

### Compute the address text in one place

The full-address text and the address line are derived from the parts. Compute them in one shared helper that the create and update operations call, so every path produces the same text.

- The full-address text is built from the country or city, the postal code and the street parts. Its format is fixed by the helper, not by each caller.
- The address line is built from the street name and the optional parts (building, staircase, floor, door, lot number). Skip empty parts.
- Honour a manual override flag. When it is set, keep the value the user typed and skip the automatic computation.

### Check the city and postal code pair in the service

The model references a city and a postal code, but it does not check that they belong together. The service that writes the address reads the postal code's cities and refuses the write when the selected city is not in that list.

- Refuse a mismatch with a modeled business fault that the operation declares (checked generated exception, HTTP 422). A wrong field value on the input is instead a ValidationException (unchecked, HTTP 400), not a fault.
- The service reads the reference data through the data access layer at check time, so it sees current values. The service is project code, not platform API.

### Create the location with its address

The location is composed by the address, so the service creates it in the same operation as the address and removes it with the address. A missing location is valid; do not create an empty one.

- Validate the coordinate range in the service, and require both latitude and longitude when a location is sent.
- Do not rely on an interceptor to set the coordinates. Interceptors run only for built-in operations (create, update, delete, list and similar) and never for custom operations, so for a custom write the logic belongs in the operation.

## Examples

### mlszksz-platform

- The update operation of the organization admin panel calls a shared organization service. The service creates or updates the address and checks the postal code against the city.
- The address helper builds the full-address text and the address line. The registration flow builds the address the same way and strips identifiers before copying it to the organization.

### rackinspect

- A create and update interceptor (project code) on the partner address sets the headquarters, billing and postal designations on the parent, then calls the address service for the computed text. It is registered for the built-in create and update operations, so it runs for those operations only.
- Custom operations for the address are not intercepted, so they must compute the text themselves.
