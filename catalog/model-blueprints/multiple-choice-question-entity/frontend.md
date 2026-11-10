## Frontend guidance

Question rows come from generated pages, but a quiz app usually replaces the player flow with its own screens.

- Keep the generated admin pages for Question if editors need a list and a view. Hide the create and edit pages, because the backend creates rows.
- For the player flow, use the player projection. Do not bind a player screen to the admin projection, which exposes the solution.
- Show the four choices as a list of options labeled A to D. Map each option to its choice text attribute and to the matching Choice member.
- Use the Choice member NONE as the initial answer before the player picks one. Do not show NONE as a selectable option.
- Reveal the solution only on the results screen, after submission.
- Hook keys are generated per page and per container. Do not write a hook key by hand; find it in the generated page for that container.
