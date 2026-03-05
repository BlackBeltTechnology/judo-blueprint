---
id: "flutter-bound-operation-pages"
title: "Flutter Bound Operation Input/Output Pages"
domain: "frontend"
category: "page"
score: 38.5
usage_count: 2
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - kozut-eugyfel-model-test
  - ams-frontend
---
## Description

Domain operations defined in the JUDO ESM model as bound operations on transfer objects generate dedicated Flutter pages for capturing operation input parameters and displaying operation output results. Each bound operation gets its own input page (form for operation parameters) and optionally an output page (result display). These are separate navigable pages, not dialogs, following the same page-config-actions triad as entity CRUD pages. This contrasts with React JUDO frontends where operations typically use dialog-based input forms.

## Structure

```
entity/operation_name/
  operation_input/
    page.dart              # MobX store for input form state
    page_actions.dart      # Execute operation action
    page__config.dart      # Form configuration
    mobile/body.dart       # Mobile layout
    tablet/body.dart       # Tablet layout
    desktop/body.dart      # Desktop layout with input fields
  operation_output/        # (optional, if operation returns data)
    page.dart
    desktop/body.dart
    ...
```

The operation flow:
1. User triggers operation from a view page action button
2. Navigation opens the operation input page
3. User fills in parameters (e.g., closure reason, comment text)
4. Execute action calls the API bound operation endpoint
5. On success, navigates back (or to output page if applicable)

## Examples

### kozut-eugyfel-model-test
Munkatars (Worker) actor has 6 bound operation pages for report management: Lezaras (Close), Megjegyzes (Comment), Megnyitas (Open), Tovabbitas (Forward), Tovabbitas Felelosnek (Forward to Responsible), and Hozzaad Resztvevo (Add Participant). Each follows the full page triad with 3 responsive layouts.

### ams-frontend
Admin actor has 3 bound operations on Campaign: **Close** (`amsActorsAdminCampaignClose`, enabled when `isOpen == true`), **Open** (`amsActorsAdminCampaignOpen`, enabled when `isClosed == true`), and **Load** (`amsActorsAdminCampaignLoad`, enabled when `isEmpty == true`). Manager actor has **ApproveAll** (`amsActorsManagerManagerApprovalListApproveAll`) for bulk approval. All use confirmation dialogs before execution.

## Trade-offs

- **Pros**: Consistent UX for all operations; full responsive layout support; generated automatically from model; complex input forms supported
- **Cons**: Full page navigation for simple operations (vs. quick dialogs); higher page count; each operation adds 7+ files
- **When to use**: Standard JUDO Flutter pattern for model-defined bound operations

## Related Patterns

- [page-config-actions-triad](page-config-actions-triad.md)
- [three-layout-responsive-pattern](three-layout-responsive-pattern.md)
- [post-operation-navigation-hook](post-operation-navigation-hook.md)
