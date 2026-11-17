---
title: Frontend Validation Hooks
description: Date, field, async and cross-field validation customization in container hooks of the generated React frontend.
aliases: [form validation frontend, date picker limits, custom field validator, async field validation, cross field validation, real time validation, password confirmation check]
keywords: [getDateFieldValidationProps, shouldDisableDate, validateForm, validateField, onFieldChange, validateTitle, debounceAsync, applicationCustomizer, getAction, registerService, ContainerHook]
tags: [domain:frontend, layer:frontend, status:platform]
---

# Validation Hooks

## Overview

**Naming note.** The hook type names (`ServiceItemViewEditContainerHook`, ...) are generated per container in `~/containers/<path>/customization`, and the handler names in the examples (`get...ValidationProps`, `validate...`, `validateForm`) are illustrative: your returned object must match the generated container action type. Registration uses `<CONTAINER>_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY` from the same module, normally through the scaffold `register<Container>ActionsHook` (see [Action Hooks](./action-hooks.md)). Server-side validation results use `{ location, code, message }` (see [Frontend Error Handling](../error-handling.md)).

Validation hooks allow you to customize input validation for forms. These hooks enable date/datetime validation, field-specific rules, custom error messages, and complex validation logic.

## Date/DateTime Validation

### Purpose

Customize date and datetime picker constraints, such as minimum/maximum dates, disabled dates, and custom validation rules.

### Basic Implementation

```typescript
// src/custom/hooks/containerActions.tsx
import type { ServiceItemViewEditContainerHook } from '~/containers/Service/Item/ServiceItemViewEdit/customization';

export const itemFormHook: ServiceItemViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    // Date field must be in the future
    getDateFieldValidationProps: (data) => {
      return {
        minDate: new Date(), // Today
        shouldDisableDate: (date) => {
          // Disable weekends
          const day = date.getDay();
          return day === 0 || day === 6;
        }
      };
    }
  };
};
```

### Registration

```typescript
// src/custom/hooks/containers/registerServiceItemViewEditActionsHook.ts
import type { BundleContext } from '@pandino/pandino-api';
import { SERVICE_ITEM_VIEW_EDIT_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY } from '~/containers/Service/Item/ServiceItemViewEdit/customization';
import { itemFormHook } from '../containerActions';

export function registerServiceItemViewEditActionsHook(context: BundleContext) {
  context.registerService(SERVICE_ITEM_VIEW_EDIT_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY, itemFormHook);
}
```

### Advanced Examples

#### Entity Date Range

```typescript
export const entityFormHook: ServiceEntityViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    // From date validation
    getFromDateValidationProps: (formData) => {
      return {
        minDate: new Date(), // Can't start in the past
        maxDate: formData.toDate ? new Date(formData.toDate) : undefined,
      };
    },

    // To date validation
    getToDateValidationProps: (formData) => {
      return {
        minDate: formData.fromDate
          ? new Date(formData.fromDate)
          : new Date(),
        shouldDisableDate: (date) => {
          // To date must be at least 7 days after from date
          if (formData.fromDate) {
            const fromDate = new Date(formData.fromDate);
            const minToDate = new Date(fromDate);
            minToDate.setDate(minToDate.getDate() + 7);
            return date < minToDate;
          }
          return false;
        }
      };
    }
  };
};
```

#### Item Within Entity Period

```typescript
export const itemFormHook: ServiceItemViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    getDateFieldValidationProps: (formData) => {
      if (formData.entity) {
        return {
          minDate: formData.entity.fromDate
            ? new Date(formData.entity.fromDate)
            : undefined,
          maxDate: formData.entity.toDate
            ? new Date(formData.entity.toDate)
            : undefined,
          shouldDisableDate: (date) => {
            // Disable weekends if entity requires weekdays only
            if (formData.entity.weekdaysOnly) {
              const day = date.getDay();
              return day === 0 || day === 6;
            }
            return false;
          }
        };
      }
      return {};
    }
  };
};
```

#### Business Days Only

```typescript
export const formHook: ServiceFormViewEditContainerHook = (data, editMode, storeDiff) => {
  const isBusinessDay = (date: Date) => {
    const day = date.getDay();
    // Not weekend
    if (day === 0 || day === 6) return false;

    // Check if it's a holiday
    const holidays = [
      '2025-01-01', // New Year
      '2025-12-25', // Christmas
      // Add more holidays
    ];

    // Format with LOCAL date parts: toISOString() is UTC and shifts the day
    // for users east or west of UTC, while getDay() above is local.
    const pad = (n: number) => String(n).padStart(2, '0');
    const dateStr = `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
    return !holidays.includes(dateStr);
  };

  return {
    getDeadlineDateValidationProps: (formData) => {
      return {
        shouldDisableDate: (date) => !isBusinessDay(date),
        helperText: 'Select a business day (Mon-Fri, excluding holidays)'
      };
    }
  };
};
```

#### Time-Based Validation

```typescript
export const itemFormHook: ServiceItemViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    getDateFieldTimeValidationProps: (formData) => {
      return {
        minDateTime: new Date(), // Must be in future
        shouldDisableTime: (value, clockType) => {
          // Disable hours outside business hours
          if (clockType === 'hours') {
            return value < 8 || value > 18; // 8 AM - 6 PM
          }
          return false;
        },
        helperText: 'Items must be scheduled between 8 AM and 6 PM'
      };
    }
  };
};
```

## Field Validation

### Purpose

Add custom validation rules for specific fields beyond date/datetime.

The generated numeric input checks the `minValueBy` attribute only when both the entered value and the `minValueBy` attribute value are truthy, so an entered `0` is accepted even when the minimum is above it.

### Basic Implementation

```typescript
// src/custom/application-customizer.tsx
export const applicationCustomizer: ApplicationCustomizer = {
  validators: {
    'ServiceEntityForm': {
      title: (value) => {
        if (!value || value.length < 3) {
          return 'Title must be at least 3 characters';
        }
        if (value.length > 100) {
          return 'Title must be less than 100 characters';
        }
      },
    },
  },
};
```

### Hook member names

- The handler for a required rule is `is<Field>Required`, with `<Field>` the attribute name with its first letter in upper case (`isNameRequired`). The generated types contain no `isFieldRequired`; `isFieldRequired` is a placeholder name only. The same pattern applies to `is<Field>Hidden`, `is<Field>Disabled` and `is<Field>Readonly`. The signature is `(data, editMode, isLoading...) => boolean`: take it from the generated `types.ts`.
- Range and refresh members of an actions hook are named `<relation><Kind>Action`, where `<relation>` is the relation name (omitted on a container's own table) and `<Kind>` is the action kind: `refreshAction`, `<relation>AutocompleteRangeAction`, `<relation>SelectorRangeAction`. A range override receives `(queryCustomizer)` and returns the target rows.
- Cards container configuration: see Extension Points, Cards Configuration Hook.

### Advanced Examples

#### Email Validation

```typescript
export const applicationCustomizer: ApplicationCustomizer = {
  validators: {
    'ServiceUserForm': {
      email: (value) => {
        if (!value) {
          return 'Email is required';
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
          return 'Invalid email address';
        }
      },
    },
  },
};
```

#### Phone Number Validation

```typescript
export const applicationCustomizer: ApplicationCustomizer = {
  validators: {
    'ServiceContactForm': {
      phone: (value) => {
        if (!value) return; // Optional field

        // Remove spaces and dashes
        const cleaned = value.replace(/[\s-]/g, '');

        // Check if it's all digits
        if (!/^\d+$/.test(cleaned)) {
          return 'Phone number must contain only digits';
        }

        // Check length (example: 10 digits)
        if (cleaned.length !== 10) {
          return 'Phone number must be 10 digits';
        }
      },
    },
  },
};
```

#### URL Validation

```typescript
export const applicationCustomizer: ApplicationCustomizer = {
  validators: {
    'ServiceWebsiteForm': {
      url: (value) => {
        if (!value) return; // Optional

        try {
          new URL(value);
        } catch {
          return 'Invalid URL format';
        }
      },
    },
  },
};
```

#### Number Range Validation

```typescript
export const applicationCustomizer: ApplicationCustomizer = {
  validators: {
    'ServiceEntityForm': {
      amount: (value) => {
        if (!value) {
          return 'Amount is required';
        }

        const numValue = parseFloat(value);

        if (isNaN(numValue)) {
          return 'Amount must be a number';
        }

        if (numValue < 0) {
          return 'Amount cannot be negative';
        }

        if (numValue > 1000000) {
          return 'Amount cannot exceed $1,000,000';
        }
      },

      quantity: (value) => {
        if (!value) return; // Optional

        const numValue = parseInt(value, 10);

        if (isNaN(numValue)) {
          return 'Must be a whole number';
        }

        if (numValue < 1) {
          return 'Must be at least 1';
        }

        if (numValue > 10000) {
          return 'Maximum 10,000';
        }
      },
    },
  },
};
```

#### Conditional Validation

```typescript
export const entityFormHook: ServiceEntityViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    validateField: (fieldName, value, formData) => {
      // Amount required for ACTIVE entities
      if (fieldName === 'amount' && formData.statusField === 'ACTIVE') {
        if (!value) {
          return 'Amount is required for active entities';
        }
      }

      // To date required for non-DRAFT entities
      if (fieldName === 'toDate' && formData.statusField !== 'DRAFT') {
        if (!value) {
          return 'To date is required';
        }
      }

      // Details required if entity is public
      if (fieldName === 'details' && formData.isPublic) {
        if (!value || value.length < 50) {
          return 'Public entities require details of at least 50 characters';
        }
      }
    }
  };
};
```

## Async Validation

### Purpose

Validate fields by calling external APIs or performing database checks.

### Basic Implementation

**IMPORTANT**: For async validation in JUDO, you can call custom validation operations through the `context.actions` object.

```typescript
export const activityFormHook: ServiceActivityViewEditContainerHook = (data, editMode, storeDiff, context) => {
  return {
    validateTitle: async (title: string) => {
      if (!title || title.length < 3) {
        return 'Title must be at least 3 characters';
      }

      try {
        // ✅ CORRECT: Call custom validation operation via context actions
        const result = await context.actions.getAction('validateTitle')({ title });

        if (result.data?.exists) {
          return 'Activity title already exists';
        }
      } catch (error) {
        console.error('Validation error:', error);
        return 'Unable to validate title. Please try again.';
      }
    }
  };
};
```

### Advanced Examples

#### Debounced Async Validation

Put `debounceAsync` in `src/custom/utils/debounceAsync.ts` and import it where needed.

```typescript
// lodash debounce() is NOT suitable here: it returns the result of the previous
// call (undefined for the first one) instead of a promise for the current call.
// Use a promise-based debounce that resolves every call with its own result.
function debounceAsync<A extends unknown[], R>(fn: (...args: A) => Promise<R>, wait: number) {
  let timer: ReturnType<typeof setTimeout> | undefined;
  return (...args: A): Promise<R> =>
    new Promise((resolve, reject) => {
      if (timer) clearTimeout(timer);
      timer = setTimeout(() => fn(...args).then(resolve, reject), wait);
    });
}

export const activityFormHook: ServiceActivityViewEditContainerHook = (data, editMode, storeDiff, context) => {
  const checkTitleAvailability = debounceAsync(async (title: string) => {
    return await context.actions.getAction('validateTitle')({ title });
  }, 500);

  return {
    validateTitle: async (title: string) => {
      if (!title || title.length < 3) {
        return 'Title must be at least 3 characters';
      }

      try {
        const result = await checkTitleAvailability(title);

        if (result.data?.exists) {
          return 'This activity title is already taken';
        }
      } catch (error) {
        console.error('Validation error:', error);
      }
    }
  };
};
```

#### Related Entity Validation

```typescript
export const addressFormHook: ServiceAddressViewEditContainerHook = (data, editMode, storeDiff, context) => {
  return {
    validateAddress: async (fullAddress: string) => {
      if (!fullAddress) {
        return 'Address is required';
      }

      try {
        // ✅ CORRECT: Use custom validation operation
        const result = await context.actions.getAction('validateAddress')({
          fullAddress,
          settlementId: data.settlement?.__identifier
        });

        if (!result.data?.isValid) {
          return result.data?.message || 'Address validation failed';
        }

        if (result.data?.qualityScore === 'LOW') {
          return 'Address is too vague. Please provide more details.';
        }
      } catch (error) {
        console.error('Address validation error:', error);
        return 'Unable to validate address. Please try again.';
      }
    }
  };
};
```

## Cross-Field Validation

### Purpose

Validate fields based on values of other fields in the form.

### Basic Implementation

```typescript
export const entityFormHook: ServiceEntityViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    validateForm: (formData) => {
      const errors: Record<string, string> = {};

      // From date must be before to date
      if (formData.fromDate && formData.toDate) {
        const from = new Date(formData.fromDate);
        const to = new Date(formData.toDate);

        if (from >= to) {
          errors.toDate = 'To date must be after from date';
        }
      }

      return errors;
    }
  };
};
```

### Advanced Examples

#### Amount vs Quantity Validation

```typescript
export const entityFormHook: ServiceEntityViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    validateForm: (formData) => {
      const errors: Record<string, string> = {};

      // Check amount per unit
      if (formData.amount && formData.quantity) {
        const costPerUnit = formData.amount / formData.quantity;

        if (costPerUnit < 10) {
          errors.amount = 'Amount too low: minimum $10 per unit';
        }

        if (costPerUnit > 1000) {
          errors.amount = 'Amount too high: maximum $1,000 per unit';
        }
      }

      return errors;
    }
  };
};
```

#### Password Confirmation

```typescript
export const userFormHook: ServiceUserViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    validateForm: (formData) => {
      const errors: Record<string, string> = {};

      // Password strength: report the first failing rule only, so a later
      // check cannot overwrite an earlier message.
      if (formData.password) {
        if (formData.password.length < 8) {
          errors.password = 'Password must be at least 8 characters';
        } else if (!/[A-Z]/.test(formData.password)) {
          errors.password = 'Password must contain an uppercase letter';
        } else if (!/[a-z]/.test(formData.password)) {
          errors.password = 'Password must contain a lowercase letter';
        } else if (!/[0-9]/.test(formData.password)) {
          errors.password = 'Password must contain a number';
        }
      }

      // Password confirmation
      if (formData.password !== formData.confirmPassword) {
        errors.confirmPassword = 'Passwords do not match';
      }

      return errors;
    }
  };
};
```

## Real-Time Validation

### Purpose

Validate as user types, providing immediate feedback.

### Basic Implementation

```typescript
export const entityFormHook: ServiceEntityViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    onFieldChange: (fieldName, value, formData) => {
      if (fieldName === 'title') {
        // Real-time title validation
        if (value.length < 3) {
          return { error: 'Title too short' };
        }

        if (value.length > 100) {
          return { error: 'Title too long' };
        }

        return { error: null };
      }
    }
  };
};
```

### Advanced Examples

#### Character Counter with Validation

```typescript
export const entityFormHook: ServiceEntityViewEditContainerHook = (data, editMode, storeDiff) => {
  return {
    onFieldChange: (fieldName, value, formData) => {
      if (fieldName === 'details') {
        const length = value?.length || 0;
        const maxLength = 500;

        if (length > maxLength) {
          return {
            error: `Details are too long (${length}/${maxLength})`,
            value: value.substring(0, maxLength), // Truncate
          };
        }

        return {
          helperText: `${length}/${maxLength} characters`,
        };
      }
    }
  };
};
```

## Best Practices

### 1. Provide Clear Error Messages

```typescript
// ✅ Good - Specific message
return 'Title must be between 3 and 100 characters';

// ❌ Bad - Vague message
return 'Invalid title';
```

### 2. Validate Early

```typescript
// ✅ Good - Check if value exists first
if (!value) {
  return 'Field is required';
}

// ❌ Bad - Assume value exists
if (value.length < 3) { ... }
```

### 3. Use Async Validation Sparingly

```typescript
// ✅ Good - Debounce async calls
const debouncedCheck = debounceAsync(checkAPI, 500);  // not lodash debounce

// ❌ Bad - Call API on every keystroke
validateName: async (value) => await checkAPI(value);
```

### 4. Handle Errors Gracefully

```typescript
// ✅ Good - Try/catch for API calls
try {
  await validateLocation(value);
} catch (error) {
  return 'Validation failed. Please try again.';
}

// ❌ Bad - No error handling
await validateLocation(value);
```

### 5. Keep Custom Validators Under src/custom

```bash
# Nothing to do: your hook file is not generated (only its .default twin is), so no .generator-ignore entry is needed
```

## Complete Example

```typescript
// src/custom/hooks/containerActions.tsx
import type { ServiceActivityViewEditContainerHook } from '~/containers/Service/Activity/ServiceActivityViewEdit/customization';
import { debounceAsync } from '~/custom/utils/debounceAsync';

export const activityFormHook: ServiceActivityViewEditContainerHook = (data, editMode, storeDiff, context) => {
  const checkTitleAvailability = debounceAsync(async (title: string) => {
    return await context.actions.getAction('validateTitle')({ title });
  }, 500);

  return {
    // Date validation
    getFromDateValidationProps: (formData) => ({
      minDate: new Date(),
      maxDate: formData.toDate ? new Date(formData.toDate) : undefined,
    }),

    getToDateValidationProps: (formData) => ({
      minDate: formData.fromDate
        ? new Date(formData.fromDate)
        : new Date(),
    }),

    // Field validation
    validateTitle: async (title: string) => {
      if (!title || title.length < 3) {
        return 'Title must be at least 3 characters';
      }

      if (title.length > 100) {
        return 'Title must be less than 100 characters';
      }

      const result = await checkTitleAvailability(title);
      if (result.data?.exists) {
        return 'Entity title already exists';
      }
    },

    // Cross-field validation
    validateForm: (formData) => {
      const errors: Record<string, string> = {};

      if (formData.fromDate && formData.toDate) {
        const from = new Date(formData.fromDate);
        const to = new Date(formData.toDate);

        if (from >= to) {
          errors.toDate = 'To date must be after from date';
        }
      }

      return errors;
    },
  };
};
```

## Troubleshooting

### "Validation not triggering"

**Check hook registration:**
```typescript
context.registerService(
  SERVICE_ENTITY_VIEW_EDIT_CONTAINER_ACTIONS_HOOK_INTERFACE_KEY,
  entityFormHook,
);
```

### "Async validation too slow"

**Add debouncing** (promise-based, not lodash `debounce`):
```typescript
const debouncedCheck = debounceAsync(async (value) => {
  return await checkAPI(value);
}, 500); // Wait 500ms after typing stops
```

### "Error message not showing"

**Return string, not throw:**
```typescript
// ✅ Good
return 'Error message';

// ❌ Bad
throw new Error('Error message');
```

## Related Documentation

- [Hook System Overview](./README.md)
- [Action Hooks](./action-hooks.md)
- [Data Hooks](./data-hooks.md)
- [Development Workflow](../development-workflow.md)
