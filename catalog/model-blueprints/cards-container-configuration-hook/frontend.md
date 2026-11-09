## Frontend guidance

A cards container shows relation data as rows in a grid by default. This pattern swaps the row rendering for custom cards and keeps the container's paging, filtering and data loading. The framework generates the hook interface and its key for each container, so the names below follow the pattern rather than being fixed constants.

### Register the hook under the generated key

Each container generates a typed hook interface and a key for it. The key is named after the page and container, so take it from the generated customization module of that container. Register the hook through the project's customizer, and do not hard-code the key string.

### Return only the card element

The hook returns an object. The card element is the required part. Toolbar, action bar, layout and pagination overrides are optional and are used only when the default is wrong for the data. Leaving them out keeps the container's own behaviour.

### The card receives the row

The card element receives the row, the column definitions, a row-click handler and the container's actions. It reads what it needs and calls an action by name with the row. Destructive actions should open a confirmation first.

```tsx
const ActiveCard: React.FC<CardProps<Row, Actions>> = ({ row, actions }) => (
  <Grid item xs={12} md={6} lg={4}>
    <Card>
      <CardContent>{row.title}</CardContent>
      <CardActions>
        <Button onClick={() => actions.cancelAction?.(row)}>Cancel</Button>
      </CardActions>
    </Card>
  </Grid>
);
```

The sketch is illustrative; `Row`, `Actions` and the action name come from the generated types of the container.

### Wrap each card in a grid item

Each card must sit in a responsive grid item, otherwise the container lays cards out as a single column. Choose the breakpoints by card density: a dense card can take a narrower column than a wide one.

### Hide actions the row does not allow

Rows carry state flags for what can be deleted or cancelled. The card reads those flags and renders only the buttons that are allowed, so the user never sees an action the server would refuse.

### Several views can use the same card

One project may register several cards for different containers. Keep each card in its own module, so a card can be reused where the same data appears in another view.

### Use the native timeline for time ranges

For time-bounded rows, a timeline component shows the start and end. Keep the timeline inside the card, not in the container, so the container's paging still works.
