---
title: Frontend Data Hooks
description: usePrincipal and useViewData of the generated React frontend and how hooks receive page data.
---

# Data Hooks

## Overview

Data hooks provide access to application data and state. These hooks allow you to retrieve information about the current user, access page/dialog data, and manage application state.

## usePrincipal Hook

### Purpose

Access the logged-in user (the principal of the actor) anywhere in the frontend.

### API

`usePrincipal()` is generated in `src/auth/principal-context.tsx` (only when the application has a principal). Import it from `~/auth/principal-context`; do not write your own `usePrincipal`, `PrincipalProvider` or fetch the principal manually. It returns:

| Member | Description |
|--------|-------------|
| `principal` | the principal transfer object (`<Actor>Stored`); an empty object until loaded or when not authenticated |
| `setPrincipal(p)` | replace the cached principal |
| `getPrincipal()` | calls the access service again and returns the REST response |
| `refreshPrincipal()` | reloads the principal into the context |
| `errorCode` | error code when loading the principal failed with 403 |

The shape of `principal` is the modeled principal transfer object, not a fixed `roles`/`permissions` structure. Use the attributes you modeled on the actor.

```typescript
import { usePrincipal } from '~/auth/principal-context';

export const UserGreeting: FC = () => {
  const { principal } = usePrincipal();

  if (!principal?.__identifier) {
    return <CircularProgress size={24} />;
  }

  return <Typography variant="h6">Welcome, {principal.email}</Typography>;
};
```

### Usage in Hooks

Hooks created from the scaffolds are called as React hooks, so you can call `usePrincipal()` inside them:

```typescript
const entityPageActions: ServiceEntityViewEditActionsHook = (data, editMode, storeDiff) => {
  const { principal } = usePrincipal();
  return {
    // use principal here
  };
};
```

### Role-Based Rendering

Authorization of data and operations is enforced by the backend; the frontend can only hide controls. Model the information you need (for example a derived `isAdmin` attribute on the principal) and read it from `principal`:

```typescript
export const AdminActions: FC = () => {
  const { principal } = usePrincipal();
  if (!principal.isAdmin) return null;
  return <Button variant="contained">Manage Users</Button>;
};
```

### Refreshing the Principal

```typescript
const { refreshPrincipal } = usePrincipal();
await refreshPrincipal();
```

## useViewData Hook

### Purpose

`useViewData()` (from `~/hooks`) gives access to the data of the view you navigated from, which is useful in hooks of dialogs and pages that need the data of the page behind them. It does not load data and has no `data`, `isLoading` or `refresh` members.

### API

| Member | Description |
|--------|-------------|
| `getLatestViewData()` | data of the view we navigated from, or `null` |
| `getRouterPageData()` | data of the page in the background, regardless of the dialog chain |
| `setLatestViewData(data)` | set by generated pages |
| `setRouterPageData(data)` | set by generated pages |

```typescript
import { useViewData } from '~/hooks';

const dialogActions: SomeDialogActionsHook = (data, editMode, storeDiff) => {
  const { getLatestViewData, getRouterPageData } = useViewData();

  return {
    // example: read the owner when an action runs
    onSomething: async () => {
      const owner = getLatestViewData();
      console.log('Opened from', owner?.__identifier);
    },
  };
};
```

The call must be inside a `ViewDataProvider` (generated in the application root). Never create your own `useViewData`.

### Current Page Data in Hooks

The data of the page or container being customized is the first argument of the hook (`data`), followed by `editMode` and `storeDiff(attributeName, value)`; page hooks may also receive `selectionDiff`, `refresh()` and `submit()` depending on the page kind (see [Action Hooks](./action-hooks.md)). Reload the page with the `refresh` argument:

```typescript
const entityViewHook: ServiceEntityViewEditActionsHook = (data, editMode, storeDiff, refresh) => {
  return {
    onSomething: async () => {
      await refresh();
    },
  };
};
```

## Combining Data Hooks

```typescript
const entityPageActions: ServiceEntityViewEditActionsHook = (data, editMode, storeDiff) => {
  const { principal } = usePrincipal();
  const { getLatestViewData } = useViewData();

  return {
    // combine principal, page data and the view we came from
  };
};
```

## Custom Data Hooks

Service class and method names follow the model (see `src/services/data-axios/`); the names below are illustrative.

### useCurrentEntity

```typescript
// src/custom/hooks/useCurrentEntity.tsx
import { useState, useEffect } from 'react';
import type { ServiceEntityStored } from '~/services/data-api/model/ServiceEntity';
import { ServiceEntityServiceImpl } from '~/services/data-axios/ServiceEntityServiceImpl';
import { judoAxiosProvider } from '~/services/data-axios/JudoAxiosProvider';

const entityServiceImpl = new ServiceEntityServiceImpl(judoAxiosProvider);

export const useCurrentEntity = (entityId: string) => {
  const [entity, setEntity] = useState<ServiceEntityStored>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error>();

  useEffect(() => {
    const fetchEntity = async () => {
      try {
        setLoading(true);
        const data = await entityServiceImpl.getEntity(entityId);
        setEntity(data);
      } catch (err) {
        setError(err as Error);
      } finally {
        setLoading(false);
      }
    };

    fetchEntity();
  }, [entityId]);

  return { entity, loading, error };
};
```

### useFilteredItems

```typescript
// src/custom/hooks/useFilteredItems.tsx
import { useState, useEffect } from 'react';
import type { ServiceItemStored } from '~/services/data-api/model/ServiceItem';
import { ServiceItemServiceImpl } from '~/services/data-axios/ServiceItemServiceImpl';
import { judoAxiosProvider } from '~/services/data-axios/JudoAxiosProvider';

const itemServiceImpl = new ServiceItemServiceImpl(judoAxiosProvider);

interface ItemFilters {
  entityId?: string;
  statusField?: 'COMPLETED' | 'PENDING' | 'CANCELLED';
  fromDate?: Date;
  toDate?: Date;
}

export const useFilteredItems = (filters: ItemFilters) => {
  const [items, setItems] = useState<ServiceItemStored[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchItems = async () => {
      setLoading(true);
      try {
        const response = await itemServiceImpl.listItems({
          page: 0,
          size: 100,
          filters: {
            entityId: filters.entityId,
            statusField: filters.statusField,
            fromDate: filters.fromDate?.toISOString(),
            toDate: filters.toDate?.toISOString(),
          }
        });
        setItems(response.data || []);
      } finally {
        setLoading(false);
      }
    };

    fetchItems();
  }, [filters]);

  return { items, loading };
};

// Usage
const { items } = useFilteredItems({
  entityId: '12345',
  statusField: 'PENDING',
  fromDate: new Date('2024-01-01'),
});
```

## Best Practices

### 1. Use the Generated Principal Context

```typescript
// ✅ Good
const { principal } = usePrincipal();   // from ~/auth/principal-context

// ❌ Bad - own fetch of the principal, own provider
```

### 2. Use Hook Arguments for Current Page Data

```typescript
// ✅ Good - data, editMode, storeDiff, refresh come from the generated hook type
const hook: ServiceEntityViewEditActionsHook = (data, editMode, storeDiff, refresh) => ({ });
```

### 3. Update Page State with storeDiff

```typescript
// ✅ Good - keeps validation and diff tracking consistent
storeDiff('title', 'New title');

// ❌ Bad - mutating data directly
data.title = 'New title';
```

### 4. Memoization

```typescript
// ✅ Good - Memoize computed values
const statistics = useMemo(() => computeStats(data), [data]);
```

### 5. Custom Hooks Live in src/custom

Your hook files in `src/custom/` are not generated (only their `.default` twins are), so no `.generator-ignore` entry is needed.

## Troubleshooting

### "Principal is undefined or empty"

`principal` is an empty object until the principal request has finished and stays empty when the user is not authenticated. Check `principal?.__identifier` and `errorCode` (set when the backend answered 403):

```typescript
const { principal, errorCode } = usePrincipal();
console.log('Principal:', principal, 'error:', errorCode);
```

### "getLatestViewData returns null"

It only holds data after a generated page navigated away from a view. Dialogs opened from the dashboard have no parent view data.

### "Stale data"

Call the `refresh` argument of the page hook after a mutation (`await refresh()`), or `refreshPrincipal()` for the principal.

## Related Documentation

- [Hook System Overview](./README.md)
- [UI Hooks](./ui-hooks.md)
- [Table Hooks](./table-hooks.md)
- [Action Hooks](./action-hooks.md)
- [Development Workflow](../development-workflow.md)
