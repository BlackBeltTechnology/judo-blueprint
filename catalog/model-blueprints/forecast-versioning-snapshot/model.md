## Model shape

The shape has one parent entity, two kinds of monthly row and one version entity. Every relation is a composition, so a version and its rows are deleted with the parent, and the monthly rows of a version are deleted with that version.

- **Initiative** is the parent. It has an integer version counter and an instance operation `archiveForecast`. It composes the current monthly forecasts (0..*) and the archived versions (0..*).
- **MonthlyForecast** is the current row: month (required), projected saving (required), realized saving and date (optional). It has no relations and no operations.
- **ForecastVersion** is the archive: timestamp and the two totals (all required). It composes its monthly rows (0..*).
- **MonthlyForecastVersion** is the frozen copy of a row: date (required), projected saving (required), realized saving (optional). Nothing edits it after the archive.

The current rows, the version and its rows are not createable, updateable or deleteable through generated actions; the archive operation and the backend write them.

### Archive operation

`archiveForecast` is an instance operation on the parent entity, with a custom implementation (the body is not generated). A transfer object that exposes the parent maps the operation as a mapped operation, so a user can call it from the generated page. Because the operation is custom, no interceptor runs for it: it does its own copying inside its transaction.

### Transfer objects

The user-facing transfer objects mirror the entities: the parent exposes the current rows and the versions as aggregations (embedded lists of mapped transfer objects), and each version exposes its monthly rows the same way. A parent relation's updateable and deleteable flags decide which actions the generated page offers on the navigated child. Keep the version rows view-only.

## Structure diagram

<!-- mermaid:generated fragment=forecast-versioning-snapshot cli=1.1.0.20261108_202643_d9769d90_develop -->
```mermaid
classDiagram
  class ForecastVersion {
    <<Entity>>
    +Timestamp timestamp [1]
    +Integer sumOfSavingPotential [1]
    +Integer sumOfSaving [1]
  }
  class Initiative {
    <<Entity>>
    +Integer version
  }
  class MonthlyForecast {
    <<Entity>>
    +String month [1]
    +Integer savingPotential [1]
    +Integer saving
    +Date date
  }
  class MonthlyForecastVersion {
    <<Entity>>
    +Date date [1]
    +Integer savingPotential [1]
    +Integer saving
  }
  ForecastVersion *-- "*" MonthlyForecastVersion : monthlyForecasts
  Initiative *-- "*" ForecastVersion : forecastVersions
  Initiative *-- "*" MonthlyForecast : monthlyForecasts
```
<!-- /mermaid:generated -->
