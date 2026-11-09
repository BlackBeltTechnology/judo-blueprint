## Model shape

The shape has one address entity, one composed location, and two lookup entities that the address references.

- **Address** holds the street name (required), building, floor and door, plus a derived full-address text. It is not createable, updateable or deleteable through the generated actions; its owner creates it.
- **Location** holds latitude and longitude, both required decimal values. It is composed by the address (0..1), so it belongs to one address and is removed with it.
- **City** holds a name. The address references one city (1..1, association).
- **PostalCode** holds a code. The address references one postal code (1..1, association).

Location and the lookup entities are not part of the generated address pages. The address form lets the user pick the city and postal code; the location is set from a map or a geocoding step, and the view shows the coordinates as read-only values.

## Structure diagram

<!-- mermaid:generated fragment=address-entity-with-location cli=1.1.0.20261108_202643_d9769d90_develop -->
```mermaid
classDiagram
  class Address {
    <<Entity>>
    +String streetName [1]
    +String building
    +String floor
    +String door
    +String /fullAddress
  }
  class City {
    <<Entity>>
    +String name
  }
  class Location {
    <<Entity>>
  }
  class PostalCode {
    <<Entity>>
    +String code
  }
  Address *-- "0..1" Location : location
  Address --> "1" City : city
  Address --> "1" PostalCode : postalCode
```
<!-- /mermaid:generated -->
