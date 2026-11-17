# internationalization-guide.md — index

Pull-only condensed map. Source: catalog/agent-docs/backend/internationalization-guide.md.

## Overview
- Backend i18n: type-safe i18n interface injected into custom operations; runtime picks the language.
- Related: `error-handling-guide.md` (throwing), `custom-operations.md` (examples).

## Internationalization (i18n)
- Parts: generated i18n interface from translation keys; OSGi service injected via `@Reference`; each key = one method; runtime language resolution.
- Interface `ApplicationI18n` lives in the project's common utils (`...utils.services.i18n`). Methods with params: `value_must_be_between(int min, int max)`, `field_exceeds_maximum_length(int maxLength)`.
- Message resolution order per method:
  1. Property named after the method; an existing property wins, even over `@Message(value=...)`.
  2. `@Message(key=...)`, looked up only if step 1 found nothing. If the key lookup returns nothing, the inline `@Message(value=...)` is discarded too.
  3. `@Message(value=...)` inline template, when no key is set.
  4. Auto-generated template from method name and parameters.
- `@MessageByEnum` is declared only, no processor. Enum messages are resolved by `EnumI18nService` by constant name.
- `ExceptionUtils` in the examples is the example project's own helper, NOT platform API: `createValidationResult(location, message)` → `ValidationResult` (level ERROR); `createValidationException(results)` → `ValidationException`; `createBusinessException(title, details)` builds the project's generated fault. Sketch: `error-handling-guide.md#example-project-helpers-not-platform-api`.
- Field errors = `ValidationException` (HTTP 400). Business faults = modeled faults (HTTP 422). Neither can be thrown as a modeled fault from an interceptor (`interceptors.md#throwing-a-business-error-from-an-interceptor`).
- Pattern 1: inject `ApplicationI18n i18n` into a custom op and throw with `i18n.<key>()`.
- Pattern 2: validation collects `ValidationResult`s per attribute name (`EntityAttribute.X.getName()`), throws once at the end.
- Pattern 3: complex validation — date not in future, no existing record for date (MANUAL method filter), source ≠ target (one result per reference), amount must be positive (reject `<= 0`); throw all results together; create only if none.
- Recommended key categories: generic validation, entity-specific, date/time, business rule, system errors, success messages.

## Localization of Validation Messages by the Runtime
- Bean validation uses a Hibernate Validator OSGi component with a `MessageInterpolator`:
  1. `I18nService.getTemplate(message)`; `null` → raw message used.
  2. `{min}`, `{max}` params interpolated; `${validatedValue}` EL evaluated.
  3. Escaped literals `\{ \} \\ \$` become literal characters.
- Locale: `LocaleProvider.getLocale()` if present, else configured `defaultLocale` (an empty value gives `Locale.ROOT`), else `Locale.getDefault()`.
- Malformed format → original message used, warning logged.

## Localized Business Error Transfer Objects
- Fault/error TOs with `message` and `location` (e.g. upload error on a row): localize both; return translated text in the fault TO, not a raw exception.

## I18n Best Practices
- DO: descriptive keys (`field_is_required`, not `ERR_001`); generic reusable messages; parameters for dynamic values; group keys by category in `ApplicationI18n`.
- DON'T: hardcode English strings in Java; put stack traces or technical detail in user messages; duplicate message definitions.

## Translation File Setup
- Java property files in resources: `messages_en.properties`, `messages_hu.properties` (lines `key:Text`).
- Example keys: `field_is_required`, `invalid_email_format`, `primary_entity_is_required`, `primary_entity_cannot_be_inactive`, `status_change_failed`, `entity_not_ready_error`, `function_under_development`.

## See Also
- `error-handling-guide.md` — throwing exceptions with i18n messages.
- `../frontend/i18n.md` — how backend messages reach the frontend.
- `custom-operations.md` — i18n in business logic.
