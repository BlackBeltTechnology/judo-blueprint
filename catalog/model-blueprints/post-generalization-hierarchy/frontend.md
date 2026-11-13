## Overview

Each post subtype has its own page layout in the React frontend. The generated form and view are replaced for the subtypes that need a custom layout. The feed sends the user to the page of the matching subtype.

## Implementation Pattern

- **Per-type container hooks.** Each subtype registers a container hook that swaps the generated view for a custom component. The hook hides the generated container and places the custom component in its parent element.
- **Custom view components.** One component per subtype renders the fields of that subtype: organization, validity or deadline dates, price, documents or image, and an inquiry action where the subtype allows it.
- **Type-aware feed navigation.** The feed reads the type discriminator of each entry and opens the page of the matching subtype, so each entry shows its own fields.
- **Inquiry on offers and requests.** The inquiry action calls a custom operation. The page mask must include the fields that show whether the user already inquired.

The hook and component names belong to the example project; the framework's hook interface and the pattern are what generalize.

## Examples

### Example (project code)
- Framework: React.
- Structure: one custom view per subtype, a shared layout component and a shared contact component, and one container hook per subtype.
- Pattern: each hook uses a DOM observer to hide the generated container and portal the custom view in its place. Views receive the loaded data and a loading flag and render a card layout suited to mobile screens.
- Notable: the shared layout and contact components keep the four views consistent.
