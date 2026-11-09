## Backend guidance

### Compute the address text in one place

The full-address text and the address line are derived from the parts. Compute them in one shared helper that the create and update operations call, so every path produces the same text.

- The full-address text is built from the country or city, the postal code and the street parts. Its format is fixed by the helper, not by each caller.
- The address line is built from the street name and the optional parts (building, staircase, floor, door, lot number). Skip empty parts.
- Honour a manual override flag. When it is set, keep the value the user typed and skip the automatic computation.

### Check the city and postal code pair in the service

The model references a city and a postal code, but it does not check that they belong together. The service that writes the address reads the postal code's cities and refuses the write when the selected city is not in that list.

- Refuse a mismatch with a modeled business fault that the operation declares. A field error on the input is a platform validation error, not a fault.
- The service re-reads the reference data inside the transaction before the check.

### Create the location with its address

The location is composed by the address, so the service creates it in the same operation as the address and removes it with the address. A missing location is valid; do not create an empty one.

- Validate the coordinate range in the service, and require both latitude and longitude when a location is sent.
- Do not run interceptors to set the coordinates. Interceptors do not run for custom operations, so the write belongs in the operation.

## Examples

### mlszksz-platform

- The update operation of the organization admin panel calls a shared organization service. The service creates or updates the address and checks the postal code against the city.
- The address helper builds the full-address text and the address line. The registration flow builds the address the same way and strips identifiers before copying it to the organization.

### rackinspect

- A create and update interceptor on the partner address sets the headquarters, billing and postal designations on the parent, then calls the address service for the computed text. The interceptor is a built-in create or update hook, so it runs for those operations only.
- Custom operations for the address are not intercepted, so they must compute the text themselves.
