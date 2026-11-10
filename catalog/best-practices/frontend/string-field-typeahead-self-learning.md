---
id: "string-field-typeahead-self-learning"
title: "String-Field Typeahead with Self-Learning Suggestions and Postal→City Autofill"
domain: "frontend"
category: "hook"
score: 55.0
usage_count: 1
alternative_count: 0
first_seen: "2026-07-12"
last_updated: "2026-07-12"
projects:
  - rackinspect
---
## Description

Add typeahead suggestions to a **plain string** DataField (e.g. address `city` / `postalCode`) **without** turning it into a foreign key. Setting the designer **`typeAhead` flag** (`isTypeAheadField=true`) on a string DataField regenerates it as a **`TextWithTypeAhead`** widget — a `freeSolo` MUI Autocomplete whose stored value stays a plain string — wired to an overridable container-hook option getter:

- Form contexts → `getForm_<field>Options(searchText, data, editMode, validation) => Promise<string[]>`
- View/Edit contexts → `getView_<field>Options(...)`

Because it is `freeSolo`, novel values are always enterable — the suggestions are a convenience, not a constraint. The suggestion list is sourced from lightweight **reference entities** that a backend primitive grows over time (see the backend companion pattern `self-learning-reference-dictionary`), so the dictionary is self-populating rather than seeded/rigid.

This supersedes the older `CUSTOM_ATTRIBUTE_RENDERER_HOOK` approach for field-level typeahead — no custom input component or form fork is required; the widget and hook are generated from the flag.

## Structure

Register the option getters in a container-actions hook under `src/custom/` (protected by `.generator-ignore`), keyed by the generated interface constant + typed hook for that page container:

```typescript
// src/custom/hooks/containers/registerServicesUser_serviceUserUser_FormContainerActionsHook.ts
import {
  SERVICES_USER_SERVICE_USER_USER_FORM_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY,
  type ServicesUser_serviceUserUser_FormContainerHook,
} from '~/containers/Services/User_service/User/User_Form/customization';
import { autofillCityFromPostal, postalCodeOptions, scopedCityOptions } from '~/custom/hooks/utils/cityPostalCodeTypeahead';

export function registerServicesUser_serviceUserUser_FormContainerActionsHook(context: BundleContext) {
  context.registerService<ServicesUser_serviceUserUser_FormContainerHook>(
    SERVICES_USER_SERVICE_USER_USER_FORM_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY,
    (data, editMode, storeDiff) => ({
      async getForm_primaryAddressCityOptions(searchText, currentData) {
        // multiple cities on the same postal → dropdown scoped to that postal's linked cities
        return scopedCityOptions(searchText, (currentData as any)?.form_primaryAddressPostalCode);
      },
      async getForm_primaryAddressPostalCodeOptions(searchText, currentData) {
        // postal→city autofill: exactly-one linked city → write it via the closed-over storeDiff
        await autofillCityFromPostal(searchText, (currentData as any)?.form_primaryAddressCity, 'form_primaryAddressCity', storeDiff);
        return postalCodeOptions(searchText);
      },
    }),
  );
}
```

The shared helper (`src/custom/hooks/utils/cityPostalCodeTypeahead.ts`) queries the generated `*ServiceForX` data-axios services with a `StringOperation.like` filter + `_mask` + `_seek: { limit }`, dedupes/sorts, and implements the autofill:

```typescript
export async function autofillCityFromPostal(postalCode, currentCity, cityFieldName, storeDiff) {
  const code = (postalCode ?? '').trim();
  if (!code || (currentCity ?? '').trim()) return;      // never clobber a manually-typed city
  const linked = await citiesForPostalCode(code);        // exact-code → linked cities (n:m traversal)
  if (linked.length === 1) storeDiff(cityFieldName, linked[0]);
}
```

Register the hook in `application-customizer.tsx` alongside the other container hooks. Apply the same two-getter shape to every address surface (Form and View), reusing the one helper (DRY).

## When To Use

- A free-text field where users repeatedly type the same values (city, postal code, tags) and you want suggestions + light cross-field autofill, but must keep the value a string (novel entries always allowed).
- Any "suggest-don't-constrain" field backed by a growing reference list.

## Pros / Cons

- **Pros**: no custom renderer/input component (flag-driven); value stays a plain string (`freeSolo`) so no string→relation migration; postal→city autofill and dropdown-scoping via the container hook's `storeDiff` closure; one shared helper across all contexts.
- **Cons**: suggestions only as good as the reference dictionary; autofill must guard against clobbering manual input; typos create new dictionary entries (free-text tradeoff — mitigated because the autofill/scoping surfaces existing spellings for selection).

## Gotchas

- After setting the `typeAhead` flag in the model, regenerate the frontend with **`./judo.sh build -f -q -i`** — the `-i` (ignore-checksum) is required or the UI generator aborts with *"There are manual changes in the generated files."*
- The generated getter name is `getForm_<fieldName>Options` / `getView_<fieldName>Options`; confirm the exact name and the container interface key in the regenerated `.../<Container>/customization.ts` + `types.ts` before writing the hook.
