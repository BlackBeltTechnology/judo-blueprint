---
id: string-field-typeahead-self-learning
title: String-Field Typeahead with Self-Learning Suggestions and Postal-to-City Autofill
description: "Turn a plain string field into a free-solo typeahead with the typeahead flag and fill its suggestions and a dependent field from a container hook, without making the field a relation."
aliases: [typeahead string field, city postal autofill, freeSolo autocomplete]
keywords: [typeahead, isTypeAheadField, TextWithTypeAhead, getForm options, getView options, storeDiff, autofill, container hook]
tags: ["domain:frontend", "layer:frontend", "project:rackinspect", "status:single-project"]
category: hook
status: single-project
projects: [rackinspect]
evidence: ["rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/utils/cityPostalCodeTypeahead.ts", "rackinspect:application/frontend-react/rackinspect__services__generic_user/src/custom/hooks/containers/registerServicesPartner_servicePartnerPartner_FormContainerActionsHook.ts"]
alternatives: []
fragment: "none: frontend-only"
first_seen: 2026-07-12
last_updated: 2026-11-10
---
## Intent

A plain string field such as an address city or postal code should offer suggestions without becoming a foreign key. The value stays a string and new values can always be typed, so the suggestions help but never constrain. The suggestion list comes from small reference entities that a backend primitive grows over time ([[self-learning-reference-dictionary]]), so the dictionary fills itself.

## Practice

### Platform base

- `StringType` has the attribute `isTypeAheadField`, documented as autocomplete from previously entered values ([widget mapping](../../agent-docs/frontend/esm-to-ui-mappings/widgets.md), [UI behaviour rules](../../agent-docs/model/esm_metamodel/ui-behaviour.md)).
- A container hook can supply typeahead options through a getter that takes the search text and returns the suggestions ([typeahead in action hooks](../../agent-docs/frontend/hooks/action-hooks.md)). Hooks receive `(data, editMode, storeDiff, context)`, and `context.actions.getRangeAction` fetches related data.
- Custom hooks under `src/custom/` are never regenerated, and the register function is called from `application-customizer.tsx`.
- The agent-docs do not name the `TextWithTypeAhead` widget, the `freeSolo` behaviour, the `getForm_<field>Options` / `getView_<field>Options` getter names or the extra `(searchText, data, editMode, validation)` arguments. These come from one example: *verify* them in the regenerated container's `customization.ts` and `types.ts` before writing the hook.

### Practice notes: flag, getters and one shared helper

- With the flag set on a string field, the generated UI used a free-solo autocomplete whose value stays a string, wired to an overridable getter: container form contexts `getForm_<field>Options`, and the form and view/edit action hooks `getCityOptions` and `getPostalCodeOptions`.
- This replaced a custom attribute renderer for field-level typeahead: no custom input component and no form fork.
- Implement the getters in a container hook, keeping every address surface on the same two-getter shape and one shared helper.
- The helper queries the generated data services with a "like" string filter, a mask and a seek limit, then removes duplicates and sorts.
- Postal-to-city autofill: the postal-code getter looks up the cities linked to the exact code. If exactly one exists and the city field is empty, it writes the city through the hook's `storeDiff`. A manually typed city is never overwritten. When several cities share the code, the city getter narrows its dropdown to them.
- After setting the flag, regenerate the frontend with the build tooling; the generator refuses to run over manual changes in generated files unless the checksum check is skipped (observed in practice, *verify* for your version).

```typescript
// Example code: container hook registered in src/custom; helper names are illustrative
context.registerService<UserFormContainerHook>(
  USER_FORM_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY,
  (data, editMode, storeDiff) => ({
    async getForm_primaryAddressCityOptions(searchText, currentData) {
      return scopedCityOptions(searchText, currentData?.form_primaryAddressPostalCode);
    },
    async getForm_primaryAddressPostalCodeOptions(searchText, currentData) {
      await autofillCityFromPostal(searchText, currentData?.form_primaryAddressCity, 'form_primaryAddressCity', storeDiff);
      return postalCodeOptions(searchText);
    },
  }),
);

export async function autofillCityFromPostal(postalCode, currentCity, cityField, storeDiff) {
  const code = (postalCode ?? '').trim();
  if (!code || (currentCity ?? '').trim()) return;   // never clobber a typed city
  const linked = await citiesForPostalCode(code);     // exact code -> linked cities
  if (linked.length === 1) storeDiff(cityField, linked[0]);
}
```

## Rationale

- The value stays a plain string, so no string-to-relation migration is needed and novel entries remain possible.
- Autofill and dropdown scoping use the hook's `storeDiff` closure; one helper serves all contexts.
- Cost: suggestions are only as good as the dictionary, autofill must guard manual input, and typos create new dictionary entries (softened because the suggestions surface existing spellings).

## Example

In one app the address `city` and `postalCode` fields of the user form and the view pages carry the flag. Typing a postal code suggests codes and fills the city when one city is linked; with several linked cities, the city dropdown offers only those. Both getters use the same helper in every address surface.

## When to avoid

- When the value must be one of a fixed set: use a relation with a range instead.
- When there is no growing reference list to source suggestions from.

## Related

- [[self-learning-reference-dictionary]] — backend primitive that grows the suggestion source
- [[application-customizer-hub]] — where container hooks are registered
