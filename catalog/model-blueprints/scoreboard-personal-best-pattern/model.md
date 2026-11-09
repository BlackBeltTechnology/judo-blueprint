## Examples

### trivia
- **PersonalBest TO** (`trivia::actors::player::PersonalBest`): mapped
  - Attributes: score, duration, playerName, timestampOfFinished -- all optional (display-only)
  - Projected from Test entity where personalBest=true, denormalizing the player's name from the User relation
- **Scoreboard TO** (`trivia::actors::player::Scoreboard`): mapped
  - Attributes: title (optional, the contest title)
  - Relations: personalBests (0..* AGGREGATION to PersonalBest)
  - Provides a ranked leaderboard for a contest
- **Player Contest TO** (`trivia::actors::player::Contest`):
  - Relations: scoreboard (0..1 ASSOC to Scoreboard), personalBests (0..* ASSOC to PersonalBest)
  - Players access the scoreboard and their personal bests from the contest view
- **Test entity** (`trivia::entities::Test`):
  - `personalBest` attribute (req, default: false) -- set to true when this test result is the player's best score for the contest
  - When a player submits a test, the backend compares the score against the player's previous best and updates the flag accordingly
- The personalBest flag acts as a materialized filter: rather than computing rankings on every query, the flag is updated on submission and the scoreboard simply queries tests where personalBest=true
