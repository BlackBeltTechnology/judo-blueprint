---
title: Frontend Action Hooks
description: Container and page action hooks, enumeration filtering, typeahead and the operation flow manager.
aliases: [frontend action hooks, hook before save, filter dropdown options, custom page button, redirect after create, autocomplete hook, operation flow redirect]
keywords: [OperationFlowManager, OPERATION_FLOW_MANAGER_INTERFACE_KEY, CONTAINER_ACTIONS_HOOK_INTERFACE_KEY, registerService, onBeforeSave, onAfterDelete, filterUserOptions, getRangeAction, getAction, handleResult, shouldUseCustomFlow]
tags: [domain:frontend, layer:frontend, status:platform]
---

# Action Hooks

## Overview

Action hooks control operations and user interactions within the application. These hooks allow you to customize container actions (form/table operations), page actions (custom button handlers), operation flow management, and enumeration filtering.

## Container Actions

### Purpose

Customize behavior of forms and tables by hooking into their lifecycle events (save, delete, validate) and providing dynamic options for dropdowns.

**Real names.** Each container generates `<CONTAINER>_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY` and the type `<Container>ContainerHook` in `~/containers/<path>/customization` (the container component name is the PascalCase model name, for example `ServiceEntityViewEdit`). The scaffold `src/custom/hooks/containers/register<Container>ActionsHook.ts.default` already contains the correct imports and `registerService` call; copy it and fill in the returned object. The handler names shown in the examples below (`onSave`, `filter...Options`, `get...Options`) are illustrative: the object you return must match the generated action definition type of your container, so check `customization.ts` and `types.ts` of the generated container for the available handlers. There is no generic `CONTAINER_HOOK_INTERFACE_KEY`.

### Basic Implementation

```typescript
// src/custom/hooks/containerActions.tsx
import type { ServiceEntityViewEditContainerHook } from '~/containers/Service/Entity/ServiceEntityViewEdit/customization';

export const entityFormHook: ServiceEntityViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    onSave: async (formData) => {
      // Custom save logic
      console.log('Saving entity:', formData);
      await validateEntity(formData);
      // Continue with default save
    },

    onDelete: async (id) => {
      // Custom delete confirmation
      const confirmed = window.confirm('Are you sure?');
      if (!confirmed) {
        throw new Error('Delete cancelled');
      }
      // Continue with default delete
    },
  };
};
```

### Registration

Registration lives in the scaffold function `register<Container>ActionsHook(context)`, which you call from `application-customizer.tsx`:

```typescript
// src/custom/hooks/containers/registerServiceEntityViewEditActionsHook.ts
import type { BundleContext } from '@pandino/pandino-api';
import {
  SERVICE_ENTITY_VIEW_EDIT_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY,
} from '~/containers/Service/Entity/ServiceEntityViewEdit/customization';
import { entityFormHook } from '../containerActions';

export function registerServiceEntityViewEditActionsHook(context: BundleContext) {
  context.registerService(SERVICE_ENTITY_VIEW_EDIT_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY, entityFormHook);
}
```

### Advanced Examples

#### Custom Validation on Save

```typescript
export const entityFormHook: ServiceEntityViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    onBeforeSave: async (formData) => {
      // Validate date range
      if (formData.fromDate && formData.toDate) {
        const start = new Date(formData.fromDate);
        const end = new Date(formData.toDate);

        if (start >= end) {
          throw new Error('From date must be before to date');
        }
      }

      // Check for duplicate titles
      const existingEntities = await entityService.list({
        filter: { title: formData.title }
      });

      if (existingEntities.length > 0 && !editMode) {
        throw new Error('Entity with this title already exists');
      }
    },

    onAfterSave: async (savedData) => {
      // Show success message
      showNotification('Entity saved successfully');

      // Refresh related data
      await refreshDashboard();
    },
  };
};
```

#### Conditional Delete

```typescript
export const entityFormHook: ServiceEntityViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    onBeforeDelete: async (id) => {
      // Check if entity has items
      const items = await itemService.list({
        filter: { entityId: id }
      });

      if (items.length > 0) {
        const confirmed = window.confirm(
          `This entity has ${items.length} items. Delete anyway?`
        );
        if (!confirmed) {
          throw new Error('Delete cancelled');
        }
      }
    },

    onAfterDelete: async (id) => {
      showNotification('Entity deleted');
      // Navigate back to list
      navigate('/entities');
    },
  };
};
```

## Enumeration Filtering

### Purpose

Dynamically filter dropdown options based on form state or other criteria.

### Basic Implementation

```typescript
export const entityFormHook: ServiceEntityViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    // Filter user options based on entity status
    filterUserOptions: (formData, options) => {
      if (formData.statusField === 'ACTIVE') {
        // Only show active users for active entities
        return options.filter(user => user.active === true);
      }
      return options;
    },
  };
};
```

### Advanced Examples

#### Cascading Dropdowns

```typescript
export const locationFormHook: ServiceLocationViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    // Filter regions based on selected country
    filterRegionOptions: (formData, options) => {
      if (formData.country) {
        return options.filter(region =>
          region.countryId === formData.country.__identifier
        );
      }
      return options;
    },

    // Filter cities based on selected region
    filterCityOptions: (formData, options) => {
      if (formData.region) {
        return options.filter(city =>
          city.regionId === formData.region.__identifier
        );
      }
      return [];
    },
  };
};
```

#### Role-Based Filtering

```typescript
import { usePrincipal } from '~/auth/principal-context';

export const entityFormHook: ServiceEntityViewEditContainerHook = (data, editMode, storeDiff) => {
  const principal = usePrincipal();

  return {
    filterUserOptions: (formData, options) => {
      // Admins see all users
      if (principal?.roles?.includes('ADMIN')) {
        return options;
      }

      // Managers see only their team
      if (principal?.roles?.includes('MANAGER')) {
        return options.filter(user =>
          user.teamId === principal.teamId
        );
      }

      // Regular users see only themselves
      return options.filter(user =>
        user.__identifier === principal.__identifier
      );
    },
  };
};
```

## Typeahead/Autocomplete

### Purpose

Provide autocomplete suggestions for text fields, often with API calls.

### Basic Implementation

```typescript
export const locationFormHook: ServiceLocationViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    // Autocomplete for location input
    getFullLocationOptions: async (searchText: string) => {
      if (searchText.length < 3) return [];

      // Call location validation service
      const suggestions = await locationService.search(searchText);
      return suggestions.map(s => s.fullLocation);
    },
  };
};
```

### Advanced Examples

#### API-Based Autocomplete

```typescript
export const addressFormHook: ServiceAddressViewEditContainerHook = (data, editMode, storeDiff, context) => {
  return {
    getSettlementOptions: async (searchText: string) => {
      if (searchText.length < 2) return [];

      // ✅ CORRECT: Use getRangeAction from context to fetch related data
      const result = await context.actions.getRangeAction('settlement')({
        query: searchText,
        page: 0,
        size: 20,
      });

      return result.data.map(settlement => ({
        label: settlement.name,
        value: settlement.__identifier,
      }));
    },
  };
};
```

#### Debounced Autocomplete

```typescript
import { debounce } from 'lodash';

export const addressFormHook: ServiceAddressViewEditContainerHook = (data, editMode, storeDiff, context) => {
  // Note: lodash debounce returns the result of the LAST completed call and
  // undefined while a call is pending, so early calls resolve to undefined.
  // Treat undefined as "no suggestions yet" or use a promise-based debounce.
  const debouncedSearch = debounce(async (searchText: string) => {
    return await context.actions.getRangeAction('publicSpaceName')({
      query: searchText,
      page: 0,
      size: 10,
    });
  }, 300);

  return {
    getPublicSpaceNameOptions: async (searchText: string) => {
      if (searchText.length < 3) return [];
      const result = await debouncedSearch(searchText);
      return result?.data ?? [];
    },
  };
};
```

## Page Actions

### Purpose

Handle custom button clicks on pages, add custom action buttons, or override default actions.

### Basic Implementation

Page hooks use the per-page key `<PAGE>_ACTIONS_HOOK_INTERFACE_KEY` (value `'<camelCaseName>_ACTIONS_HOOK'`) and the type `<Container>ActionsHook`, both generated in the page's `customization.ts` (dialogs: `~/dialogs/<path>/customization`). The hook receives `(data, editMode, storeDiff, [selectionDiff], [refresh], [submit])` depending on the page kind and returns the page action handlers. Use the scaffold `src/custom/hooks/pages/register<Page>ActionsHook.ts.default`. The `context.getData()` / `context.getSelectedIds()` style in the examples below is illustrative; use the arguments of the generated hook type (`data`, `refresh`, `submit`) and the services you instantiate in the scaffold.

```typescript
// src/custom/hooks/pages/registerServiceEntityViewPageActionsHook.ts
import type { BundleContext } from '@pandino/pandino-api';
import {
  SERVICE_ENTITY_VIEW_PAGE_ACTIONS_HOOK_INTERFACE_KEY,
  type ServiceEntityViewEditActionsHook,
} from '~/pages/Service/Entity/ServiceEntityViewPage/customization';

export function registerServiceEntityViewPageActionsHook(context: BundleContext) {
  context.registerService<ServiceEntityViewEditActionsHook>(
    SERVICE_ENTITY_VIEW_PAGE_ACTIONS_HOOK_INTERFACE_KEY,
    entityPageActions,
  );
}

const entityPageActions: ServiceEntityViewEditActionsHook = (data, editMode, storeDiff, refresh, submit) => ({
  // implement actions here
});
```

### Registration

Call `registerServiceEntityViewPageActionsHook(context)` from `DefaultApplicationCustomizer.customize`. There is no `page` service property; the key itself is page specific. The same operation shown on N pages (for example a view that exists as several generated pages) needs N hook registrations, one per page key.

### `getMask`, `queryCustomizer` and template hooks

- **`getMask?: () => string`** is an optional member of the page actions hook for pages that show a view or a table, not for forms. A generated page calls it when it builds the `_mask` of its own load request, and falls back to a mask serialized at generation time. Return only the fields the page needs.
- **`_mask` syntax:** `{<attr>,<attr>,<relation>{<attr>,<attr>},...}`. The mask is wrapped in braces, plain attributes are comma separated and sorted, and a relation name is followed by its own braces. For example `{name,createdAt,owner{name}}`. Include every attribute that a visibility, enabled, required or range-bound field refers to, or the page cannot evaluate it.
- **`queryCustomizer`:** the page's refresh action takes a `QueryCustomizer` argument (`refreshAction?: (queryCustomizer) => Promise<JudoRestResponse<...>>`). It carries `_mask`, filters, sort and `_seek`. Overriding `refreshAction` replaces the load call, so pass the received `queryCustomizer` through (with your changes) to the generated service. Tables build it internally and add `_mask` from `getMask` when present.
- **`post<GetTemplateAction>(ownerData, data, storeDiff)`** exists only on dialog (create-form) hooks. It runs after the template (default values for a new instance) has loaded. Use `storeDiff(attributeName, value)` to write defaults into the form data. It is not generated on plain pages.

### Refreshing Custom Components After an Operation

The generated page does not hand new data to a custom visual element after an operation, so such a component keeps stale values (for example a summary that shows a total). Use the optional `post<Operation>` handler of the page actions hook (one per page, see above) to signal the component, and reload in the component:

```typescript
// in the page actions hook
postApplyCoupon: async () => {
  window.dispatchEvent(new CustomEvent('<app>:data-changed'));
},

// in the custom component
useEffect(() => {
  const reload = () => { /* fetch the data again */ };
  window.addEventListener('<app>:data-changed', reload);
  return () => window.removeEventListener('<app>:data-changed', reload);
}, []);
```

### Refreshing the menu after an operation

The navigation menu is filtered by the `principal` held in the principal context: an item whose `hiddenBy` names a boolean of the principal is hidden while it is `true`, and the menu re-filters whenever `principal` changes. After an operation that changes those flags (for example joining a group), call `await refreshPrincipal()` from `usePrincipal()` in the post-operation hook; the menu updates without a page reload.

```typescript
const { refreshPrincipal } = usePrincipal();
await refreshPrincipal();
```

### Advanced Examples

#### Export to CSV

```typescript
export const entityPageActions: PageActionHook = () => {
  return {
    'export-csv': async (context) => {
      const entities = context.getData();

      // Convert to CSV
      const headers = ['Title', 'Status', 'From Date', 'To Date'];
      const rows = entities.map(e => [
        e.title,
        e.statusField,
        e.fromDate,
        e.toDate,
      ]);

      const csv = [
        headers.join(','),
        ...rows.map(row => row.join(','))
      ].join('\n');

      // Download file
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'entities.csv';
      a.click();
    },
  };
};
```

#### Bulk Operations

```typescript
export const entityPageActions: PageActionHook = () => {
  return {
    'bulk-activate': async (context) => {
      const selectedIds = context.getSelectedIds();

      if (selectedIds.length === 0) {
        alert('Please select entities to activate');
        return;
      }

      const confirmed = confirm(
        `Activate ${selectedIds.length} entity(ies)?`
      );

      if (!confirmed) return;

      // Activate each entity
      await Promise.all(
        selectedIds.map(id =>
          entityService.update(id, { statusField: 'ACTIVE' })
        )
      );

      // Refresh view
      await refresh();
      showNotification(`${selectedIds.length} entities activated`);
    },

    'bulk-delete': async (context) => {
      const selectedIds = context.getSelectedIds();

      if (selectedIds.length === 0) {
        alert('Please select entities to delete');
        return;
      }

      const confirmed = confirm(
        `Delete ${selectedIds.length} entity(ies)? This cannot be undone.`
      );

      if (!confirmed) return;

      await Promise.all(
        selectedIds.map(id => entityService.delete(id))
      );

      await refresh();
      showNotification(`${selectedIds.length} entities deleted`);
    },
  };
};
```

#### Custom Operation Action

```typescript
export const activityPageActions: PageActionHook = () => {
  return {
    'export-to-excel': async (context) => {
      const activity = context.getData();

      context.showNotification('Generating Excel export...');

      try {
        // ✅ CORRECT: Use getAction from context to call custom operation
        const result = await context.actions.getAction('exportToExcel')(activity.__signedIdentifier);

        // If operation returns a download token, use it
        if (result.data?.downloadToken) {
          const blob = await context.actions.downloadFile(result.data.downloadToken, 'attachment');

          // Download file
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `activity-${activity.title}-export.xlsx`;
          a.click();
          URL.revokeObjectURL(url);
        }

        context.showNotification('Export generated successfully');
      } catch (error) {
        context.showErrorDialog('Export Failed', 'Could not generate Excel export', 'error');
      }
    },
  };
};
```

## OperationFlowManager

> **Design principle: one representation per concept.** Default mapped-TO output navigation lands on a generated standalone `<TO>View` route. Same row also reachable via `Actor.access.<area>.<rel> → row → detail` — a DIFFERENT generated page. Use `OperationFlowManager` to redirect every post-op landing into the access-context view; standalone routes are generated but unvisited. See [operation-flow-manager-redirect.md](../../../best-practices/frontend/operation-flow-manager-redirect.md) for the redirect recipes and [relation-driven-crud-with-custom-input.md](../../../best-practices/model/relation-driven-crud-with-custom-input.md) for the capability ladder and return-type matrix that motivate the redirect.

### Purpose

Control navigation and behavior after operations (create, update, delete). Customize where users go after completing actions.

### Basic Implementation

`OperationFlowManager` and `OPERATION_FLOW_MANAGER_INTERFACE_KEY` (value `'OperationFlowManager'`) are exported from `~/utilities/application`. `handleResult(input)` receives the stored result of the operation (with `__entityType`) and returns `ProcessProps`: `{ actor, access, filterRecords?, operation? }`. The examples below that use `input.operation`, `entityType`, `id` or `tab` show an illustrative shape; real inputs are the operation result object, so branch on `input.__entityType`.

```typescript
// src/custom/application-customizer.tsx
import type { BundleContext } from '@pandino/pandino-api';
import type { ApplicationCustomizer } from './interfaces';
import { OPERATION_FLOW_MANAGER_INTERFACE_KEY, type OperationFlowManager } from '~/utilities/application';

const customFlowManager: OperationFlowManager = {
  shouldUseCustomFlow: (input) => ['entities.Item'].includes(input?.__entityType || ''),
  handleResult: (input) => ({
    actor: 'ServiceActor',
    access: 'ServiceItemsTable',
    filterRecords: { entityId: [{ operator: 'equal', value: (input as any).entityId }] },
  }),
};

export class DefaultApplicationCustomizer implements ApplicationCustomizer {
  async customize(context: BundleContext): Promise<void> {
    context.registerService<OperationFlowManager>(OPERATION_FLOW_MANAGER_INTERFACE_KEY, customFlowManager);
  }
}
```

### Advanced Examples

#### Context-Based Navigation

```typescript
export const customFlowManager: OperationFlowManager = {
  shouldUseCustomFlow: (input) => {
    return input.operation === 'CREATE' || input.operation === 'UPDATE';
  },

  handleResult: (input) => {
    const { operation, entityType, result, context } = input;

    if (operation === 'CREATE') {
      if (entityType === 'Entity') {
        // After creating entity, go to entity view
        return {
          actor: 'ServiceActor',
          access: 'ServiceEntityView',
          id: result.__identifier,
        };
      }

      if (entityType === 'Item') {
        // After creating item, stay on entity view with items tab
        return {
          actor: 'ServiceActor',
          access: 'ServiceEntityView',
          id: result.entityId,
          tab: 'items',
        };
      }
    }

    if (operation === 'UPDATE') {
      // After update, refresh current view
      return {
        refresh: true,
      };
    }

    if (operation === 'DELETE') {
      // After delete, go back to list
      return {
        actor: 'ServiceActor',
        access: `Service${entityType}sTable`,
      };
    }

    return null;
  },
};
```

#### With Custom Messages

```typescript
export const customFlowManager: OperationFlowManager = {
  shouldUseCustomFlow: (input) => true,

  handleResult: (input) => {
    const { operation, entityType, result } = input;

    // Show custom success message
    const messages = {
      CREATE: `${entityType} created successfully`,
      UPDATE: `${entityType} updated successfully`,
      DELETE: `${entityType} deleted successfully`,
    };

    showNotification(messages[operation] || 'Operation successful');

    // Navigate based on operation
    if (operation === 'CREATE') {
      return {
        actor: 'ServiceActor',
        access: `Service${entityType}View`,
        id: result.__identifier,
      };
    }

    return null;
  },
};
```

The generated action queue (`CRUDDialog` in `src/hooks/useCRUDDialog.tsx`) changes queue items in place, and `runActions` reads the `inProgress` flag without listing it in its dependency array, so queue status can be stale. Workaround: do not start a second action run while one is in progress.

## Best Practices

### 1. Async/Await for API Calls

```typescript
// ✅ Good
onBeforeSave: async (data) => {
  await validateData(data);
}

// ❌ Bad
onBeforeSave: (data) => {
  validateData(data); // Not awaited
}
```

### 2. Error Handling

```typescript
// ✅ Good
onSave: async (data) => {
  try {
    await customValidation(data);
  } catch (error) {
    showNotification(error.message, 'error');
    throw error; // Prevent save
  }
}

// ❌ Bad
onSave: async (data) => {
  await customValidation(data); // Errors not caught
}
```

### 3. Check Form State

```typescript
// ✅ Good
filterUserOptions: (formData, options) => {
  if (formData.status === 'ACTIVE') {
    return options.filter(u => u.active);
  }
  return options;
}

// ❌ Bad
filterUserOptions: (formData, options) => {
  return options.filter(u => u.active); // Ignores form state
}
```

### 4. Keep Custom Hooks Under src/custom

```bash
# Nothing to do: your hook file is not generated (only its .default twin is), so no .generator-ignore entry is needed.
```

### 5. Debounce Autocomplete

```typescript
// ✅ Good - Debounced (lodash debounce yields undefined while a call is pending)
const debouncedSearch = debounce(searchAPI, 300);

// ❌ Bad - No debouncing
getOptions: async (text) => await searchAPI(text);
```

## Complete Example

```typescript
// src/custom/application-customizer.tsx
import type { BundleContext } from '@pandino/pandino-api';
import type { ApplicationCustomizer } from './interfaces';
import { OPERATION_FLOW_MANAGER_INTERFACE_KEY, type OperationFlowManager } from '~/utilities/application';
import { registerServiceEntityViewEditActionsHook } from './hooks/containers/registerServiceEntityViewEditActionsHook';
import { registerServiceEntityViewPageActionsHook } from './hooks/pages/registerServiceEntityViewPageActionsHook';
import { customFlowManager } from './hooks/operationFlowManager';

export class DefaultApplicationCustomizer implements ApplicationCustomizer {
  async customize(context: BundleContext): Promise<void> {
    registerServiceEntityViewEditActionsHook(context);   // container actions
    registerServiceEntityViewPageActionsHook(context);   // page actions
    context.registerService<OperationFlowManager>(OPERATION_FLOW_MANAGER_INTERFACE_KEY, customFlowManager);
  }
}
```

## Troubleshooting

### "Hook not executing"

#### Check registration
```typescript
console.log('Registering container hook');
context.registerService(
  SERVICE_ACTIVITY_VIEW_EDIT_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY,
  activityFormHook,
);
```

#### Verify component name
```bash
# Check generated component names
grep -rn "_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY =" src/containers | head
```

### "Filtering not working"

#### Debug filter logic
```typescript
filterUserOptions: (formData, options) => {
  console.log('Form data:', formData);
  console.log('Options:', options);
  const filtered = options.filter(u => u.active);
  console.log('Filtered:', filtered);
  return filtered;
}
```

### "Operation flow not redirecting"

#### Check return value
```typescript
handleResult: (input) => {
  console.log('Operation input:', input);
  const result = {
    actor: 'ServiceActor',
    access: 'ServiceActivityView',
    id: input.result.__identifier,
  };
  console.log('Returning:', result);
  return result;
}
```

## Related Documentation

- [Hook System Overview](./README.md)
- [Data Hooks](./data-hooks.md)
- [Table Hooks](./table-hooks.md)
- [Validation Hooks](./validation-hooks.md)
- [Navigation and Access](./navigation-and-access.md)
- [Development Workflow](../development-workflow.md)
