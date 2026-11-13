## Frontend guidance

The source project shows the leaderboard in a custom dialog. The components are project code, registered under the hook keys the framework generates. See [action hooks](../../agent-docs/frontend/hooks/action-hooks.md).

### Two-tier display

Split the rows: the top three appear as a podium list with gold, silver and bronze avatars, the rest in a scrolling list from position four.

### Request the order explicitly

Fetch the rows ordered by score descending, duration ascending, then finish time ascending. Higher scores come first, faster times break ties, earlier finish breaks the rest. The order is requested by the client; the model does not fix it.

### Highlight the current participant

Compare each row's participant name with the current participant and render a match in the theme's primary colour in both tiers.

### Auto-scroll and refresh

The lower list scrolls by itself in small steps. At the bottom it requests a refresh after a cooldown (ten seconds in the source project). A touch pauses and resumes scrolling for mobile users.

### Format durations

Convert raw seconds to readable text (for example minutes and seconds) in one utility function.

### Entry points

Open the dialog from the event view with a button, and from the results dialog after a submit. Framework in the source project: React.
