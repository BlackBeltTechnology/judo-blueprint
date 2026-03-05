---
id: "three-layout-responsive-pattern"
title: "Three-Layout Responsive Pattern (Mobile/Tablet/Desktop)"
domain: "frontend"
category: "page"
score: 63.8
usage_count: 4
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - skillmatrix-frontend
  - kozut-eugyfel-client
  - kozut-eugyfel-model-test
  - ams-frontend
---
## Description

Every generated JUDO Flutter page produces three separate body layout files -- mobile, tablet, and desktop -- each with different column grid counts. The page widget measures the viewport width and selects the appropriate layout at runtime. This creates a truly responsive experience where each breakpoint has its own optimized layout rather than reflowing the same layout. The navigation drawer also adapts: collapsed hamburger on mobile/tablet, always-visible side panel on desktop.

## Structure

```
page_type/
  page.dart                # Page widget, PageStore, layout selection
  page_actions.dart        # AppBar action buttons
  desktop/body.dart        # Desktop layout (>=840px, 12 columns)
  tablet/body.dart         # Tablet layout (600-839px, 8 columns)
  mobile/body.dart         # Mobile layout (0-599px, 4 columns)
```

Breakpoint selection:
```dart
if (width >= 0 && width <= 599)     -> Mobile  (4 columns)
if (width >= 600 && width <= 839)   -> Tablet  (8 columns)
if (width >= 840 && width <= 32767) -> Desktop (12 columns)
```

Additionally, a responsive content margin formula scales horizontal padding from 10px (at 1300px) to 116px (at 2000px) on desktop.

## Examples

### SkillMatrix
98 pages across 3 actors, each with 3 layout variants (294 body.dart files total). Desktop uses 12-column grid with sections like "Personal (col 4) | Contact (col 5) | Spacer (col 3)". Drawer is 304px on desktop, hamburger on mobile/tablet. Content margin linearly interpolates between 10-116px for viewports 1300-2000px wide.

### kozut-eugyfel-client
~120 pages across 3 actors, each with 3 layout variants (~360 body.dart files). Includes dashboard, table, view, create, update, operation_input, and operation_output page types. Same breakpoints (mobile 0-599, tablet 600-839, desktop 840+) and content margin formula.

### kozut-eugyfel-model-test
Model generates 7 page types (dashboard, table, view, create, update, operation_input, operation_output) each with 3 responsive layouts. Admin actor has 58 routes, Munkatars has 52 routes, EugyfelAlkalmazas has minimal pages -- all with consistent breakpoints.

### ams-frontend
Admin actor pages (Applications table/view/create/update, Campaigns table/view/create/update/dashboard, Users table/view) and Manager actor pages (Approval List table/view/dashboard, Subordinates table/view, Approve All view) all implement the three-layout pattern. Campaigns View uses tabs with embedded tables for Confirmation Requests and Applications within responsive layouts.

## Trade-offs

- **Pros**: Optimized layouts per device class; true responsive design not just reflowing; generated automatically from model
- **Cons**: 3x the layout files per page; changes to form layout must be done in the model (affects all 3 variants); no custom breakpoint configuration
- **When to use**: Standard JUDO Flutter pattern -- automatically generated for all pages

## Related Patterns

- [flutter-frontend-framework](flutter-frontend-framework.md)
