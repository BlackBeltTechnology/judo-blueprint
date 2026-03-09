## Overview

The task entity with assignment blueprint has a targeted React frontend customization: a dialog action hook that filters the CloseTask input form's result enum options to remove invalid choices, plus comprehensive Hungarian i18n translations for task-related forms, enums, and menu items.

## Implementation Pattern

- **Dialog form action hooks for enum filtering**: A Pandino action hook registered for the CloseTask input form dialog overrides the `filterResultOptions` function to remove the `TODO` value from the `TaskState` enum options. This ensures that when an author or approver closes a task, they can only select `APPROVED` or `REJECTED` as the result -- not reset it back to `TODO`.
- **i18n for task workflow**: The translations file provides Hungarian labels for all task-related UI elements: CloseTaskInput form title ("Feladat leazarasa"), result field ("Eredmeny"), ApprovalTaskInput form for selecting approvers ("Jovahagyasi Feladat Urlap"), TaskState enum values (Jovahagyott/Approved, Visszautasitott/Rejected, Elvegzendo/TODO), TaskType enum values (Jovahagyasi/Approval), and menu navigation items ("Feladataim"/"My Tasks", "Feladatok"/"Tasks").

## Examples

### alba
- Framework: React
- Key files: `custom/hooks/dialogs/registerServicesAuthorTaskAuthorTask_View_EditCloseTaskInputFormActionsHook.ts`
- Pattern: A Pandino dialog action hook registered with the `SERVICES_AUTHOR_TASK_AUTHOR_TASK_VIEW_EDIT_CLOSE_TASK_INPUT_FORM_ACTIONS_HOOK_INTERFACE_KEY` provides a `filterResultOptions` override that filters out `TaskState.TODO` from the enum dropdown options. The hook receives `(ownerData, data, editMode, storeDiff, submit, onSubmit)` parameters and returns `{ filterResultOptions: (data, options) => options.filter(o => o.value !== TaskState.TODO) }`.
- Notable: This is a minimal but important UX refinement -- without this hook, the generated form would display all three TaskState options including TODO, which would not make sense when closing a task. The hook is registered only for the AuthorTask view; the ApproverTask view uses the same CloseTask pattern but appears to rely on the generated defaults (or a separate hook could be registered for it using a different interface key).
