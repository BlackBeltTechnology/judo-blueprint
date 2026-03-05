---
id: "responsive-multi-device-layout"
title: "Responsive Multi-Device Page Layout Pattern"
domain: "model"
category: "ui"
score: 45.8
usage_count: 3
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - actiongroup-test-react
  - kozut-eugyfel-client
  - ams-frontend
---
## Description

Every page definition in the UI model contains four device-specific PageContainer variants (mobile, tablet, desktop, default) with a column-based grid system. Each container adapts its layout to the screen size by adjusting column counts and component widths. This ensures responsive design is built into the model layer rather than handled by custom CSS.

## Structure

- Every `PageDefinition` has 4 `PageContainer` children, one per layout type
- Layout types define screen breakpoints:
  - `mobile`: 4 columns, 0-599px width
  - `tablet`: 8 columns, 600-839px width
  - `desktop`: 12 columns, 840-32767px width (marked as default)
  - `default`: 12 columns, fallback layout
- Components specify `col` attribute (number of columns to span):
  - Desktop: full=12.0, half=6.0, third=4.0
  - Tablet: full=8.0, half=4.0
  - Mobile: no explicit col (full width by default)
- Nested Flex containers provide vertical/horizontal layout within each device container
- All 4 containers replicate the same logical structure with device-appropriate sizing

```xml
<containers name="default" col="12.0" layoutType=".../default"/>
<containers name="mobile" layoutType=".../mobile"/>
<containers name="tablet" col="8.0" layoutType=".../tablet"/>
<containers name="desktop" col="12.0" layoutType=".../desktop"/>
```

## Examples

### ActionGroupTest
31 pages each have 4 device containers. The "Play God" ActionGroup uses `col="6.0"` on desktop/tablet but omits col on mobile for full width. Tables, forms, and action buttons all adapt across breakpoints. Total of 864 Flex containers and 374 Spacers manage responsive spacing. Page types (TABLE, CREATE, UPDATE, VIEW, OPERATION_INPUT, OPERATION_OUTPUT, DASHBOARD) all follow the same 4-container pattern.

### KozutEugyfelClient
UI model (6.7 MB) defines responsive interfaces with mobile (col="4.0"), tablet (col="8.0"), and desktop (col="12.0") breakpoints. 316 tables, 130 data fields, and 33 groups are arranged across responsive containers. Action buttons bound to entity operations adapt per breakpoint.

### AMS-Frontend
40 pages across 2 actor applications (20 Manager, 14 Admin, plus relation views) each with 4 device-specific containers (mobile, tablet, desktop, default). UI features include tab bars (Campaign view with Confirmation Requests and Applications tabs), grouped fields (Request view with User and Application groups using frames), and mandatory confirmation dialogs on approve/reject/open/close operations.

## Trade-offs

- Pros: Responsive design declared in the model, consistent breakpoints across all pages, no custom CSS needed
- Cons: 4x replication of component structure increases model size, changes must be applied to all 4 containers
- Prefer when: Always for JUDO UI models -- this is the standard responsive layout approach

## Related Patterns

- [action-group-conditional-enabling](action-group-conditional-enabling.md) (ActionGroups adapt across device layouts)
