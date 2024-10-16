# Design Guidelines

The Keystone-API project adheres to the following design guidelines.

## Serializing Relational Data

When serializing relational data, the handling of child records is determined by their relationship to the parent record.
If an entity is _contained_ by a parent record (e.g., by aggregation or composition) it is included in the serialized parent as a nested field.
In all other cases related entities are linked to in the serialized parent via a reference (e.g. as an ID or URL).

??? example "Example: Related Entities"

    In example model below, the `Library` model shares a generic relationship with the `Address` model.

    ```mermaid
    classDiagram
        direction LR
        Library "1" -- "1" Address : Related (by ID)
        class Library {
          +id: int
          +name: string
        }
        class Address {
          +id: int
          +street: string
        }
    ```

    When serializing generic relationships, the related records are linked to by a reference identifier (in this case by ID).

    ```json
    {
      "id": 1,
      "name": "Franklin Public Library",
      "address": 1
    }
    ```

??? example "Example: Nested Entities"

    In example model below, the `Library` model contains zero or more `Book` instances.

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

    When serializing instances of the `Library` model, any related `Book` instances are also serialized and included in the rendered response.

    ```json
    {
      "id": 1,
      "name": "Franklin Public Library",
      "books": [
        {
          "id": 1,
          "title": "Title 1",
        }, {
          "id": 2,
          "title": "Title 2",
        },
      ]
    }
    ```

Write operations are always supported for nested data, however, the values in a nested record are immutable.
One or more nested records may be removed or replaced when modifying a parent record, but the content of the nested records cannot be changed.
