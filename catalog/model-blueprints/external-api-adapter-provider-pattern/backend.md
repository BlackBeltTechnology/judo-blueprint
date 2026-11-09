## Backend guidance

### Module layout

Keep the three layers in separate modules, so the API module has no dependency on any platform SDK:

- An API module: the interface and its data objects, packaged as a standalone bundle with no model dependency.
- One adapter module per platform: it depends on the API module and on that platform's SDK. Its implementation is a plain object.
- The common module: the provider interface and its factory implementation, which is the only component.
- The application's custom operations and services, which reference the provider.

### The API interface

- Define a plain interface with business-oriented methods that return the module's own data objects.
- Build the data objects with a builder. They are not the model's transfer objects, so the API module stays free of the model.
- Do not add component annotations or SDK types to the interface.

### The adapter

- The adapter is a plain object constructed by the provider with the runtime credentials (tokens, keys, account ids). It is not a component.
- Its methods translate between the platform SDK's types and the module's data objects. The SDK types do not leak out of the adapter.

### The factory

- The provider is a component in the common module. It injects the data-access services it needs and the file store service for credential files.
- The lookup method does three things: load the entity, read its platform, load the platform's credentials. Then it constructs the adapter and returns it.
- Dispatch on the platform with one branch per platform. An unknown or not-yet-implemented platform fails with a business error that carries a code and a localized message.

### Business errors, not raw exceptions

- A connection failure to the external platform is not a 500 for the user. Catch it in the factory or the calling operation, log the cause, and rethrow it as the business fault declared on the operation, with a code and a message.
- An error that the platform's API returns is translated to a business error at the adapter boundary or in the calling operation, not passed through as a raw exception.
- Use the fault's type as the business error's type, so the client's fault dialog can find its translations.

### Consumption

- Custom operations and services reference the provider service, never an adapter.
- A call looks like: obtain the client from the provider with the entity, then call the method with the platform's identifier. The provider can supply helpers that return that identifier.

### Project code, not platform API

The example project's names for the provider, the adapter and the data objects, and its error helper, are project code. Copy the pattern, not the names.

## Examples

### indamedia-adtrack

- The API interface has seven methods, covering account information, connection status, the campaign list, budget and usage, campaign history, cost to date, and campaign details.
- The Google Ads adapter is a plain object built from a developer token, a delegated account, an optional login customer id, and a service-account key. It uses the Google Ads Java SDK.
- The provider switches on the platform enumeration (Google or Meta). The Google branch loads the key file through the file store service and passes it to the adapter as a string. The Meta branch is declared but throws a not-implemented business error, which marks the extension point.
- Two campaign services consume the provider for their API calls.
