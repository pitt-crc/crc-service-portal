# Design Guidelines

The Keystone-API project adheres to the following design guidelines.

### Serializing Relational Data

Serialized records will always reference related entities using ID values.
When serializing a one-to-one relationship, ID values are included for both directions of the relationship.

!!! example "Example: Serializing A One-to-One Relationship"

    The following example demonstrates a one-to-one relationship between the `Library` and `Address` models.

    ```mermaid
    classDiagram
        direction LR
        Library "1" -- "1" Address : Related (by ID)
        class Library {
          +id: int
          +name: string
          +address_id: int
        }
        class Address {
          +id: int
          +street: string
        }
    ```

    When serializing a `Library` instance, the corresponding `Address` record is linked to by its ID.

    ```json
    {
      "id": 1,
      "name": "Franklin Public Library",
      "address": 5
    }
    ```

    ID values are always included in both directions of a one-to-one relationship.
    
    ```json
    {
      "id": 1,
      "street": "Franklin Public Library",
      "library": 5
    }
    ```

In all other cases ID values are only required in one direction.
Including ID values in both directions is allowed but not required.

!!! example "Example: Serializing A One-to-Many Relationship"

    The following example demonstrates a one-to-many relationship between the `Library` and `Book` models.

    ```mermaid
    classDiagram
        direction LR
        Library "1" *-- "0..*" Book : Contains
        class Library {
          +id: int
          +name: string
        }
        class Book {
          +id: int
          +title: string
        }
    ```

    When serializing instances of the `Library` model, any related `Book` instances are returned as a list of ID vlaues.

    ```json
    {
      "id": 1,
      "name": "Franklin Public Library",
      "books": [1, 2]
    }
    ```
