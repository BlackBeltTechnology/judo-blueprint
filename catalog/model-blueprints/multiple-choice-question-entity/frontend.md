## Overview

The multiple-choice question entity manifests in the React frontend as a custom quiz-taking interface where questions are presented one at a time in a timed dialog, with answer choices rendered as styled option buttons (A/B/C/D) and results shown in a detailed review dialog after submission.

## Implementation Pattern

- **Timed question presentation**: The `PromptListDialog` displays one question at a time with a `LinearProgress` bar that counts down based on `responseTime` (seconds per question). When time expires, the dialog auto-advances to the next question. The progress is updated via `setInterval` with 100ms ticks.
- **Choice rendering**: The `CheckboxList` component maps the `choiceA`/`choiceB`/`choiceC`/`choiceD` attributes from the `Prompt` transfer object to styled `OptionButton` components, each with an `OptionAvatar` showing the letter (A/B/C/D). Tapping a choice triggers a 200ms delay before advancing to the next question.
- **Choice enum integration**: The `Choice` enum (A, B, C, D, NONE) from the generated model is used directly -- answers default to `Choice.NONE` and are set to the selected letter on click.
- **Results review**: The `ResultsDialog` shows each question with color-coded results: green for correct answers, red for incorrect selections, and grey with strikethrough for wrong options. It accesses `choice${answer}` dynamically using `keyof ActorsplayerPrompt` to display the text of both the player's answer and the correct solution.
- **Transition animations**: Questions use a `TransitionWrapper` component for fade-in/fade-out effects when navigating between questions, providing smooth visual transitions.
- **Custom styled components**: `BlurDialog`, `OptionButton`, `OptionAvatar`, and `TransitionWrapper` are purpose-built MUI styled components shared across the quiz flow.

## Examples

### trivia
- Framework: React
- Key files: `src/trivia/PromptListDialog.tsx`, `src/trivia/CheckboxList.tsx`, `src/trivia/ResultsDialog.tsx`, `src/trivia/CustomComponents.tsx`
- Pattern: Full-screen timed quiz dialog presenting `ActorsplayerPrompt` items one at a time. `CheckboxList` renders A/B/C/D options as styled buttons. Timer auto-advances on expiry. Results show correct/incorrect answers with color coding.
- Notable: The question flow bypasses all JUDO generated pages. The `PromptListDialog` manages its own state machine (current index, progress, answer list) independently from the JUDO navigation system.
