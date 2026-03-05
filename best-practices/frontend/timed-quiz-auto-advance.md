---
id: "timed-quiz-auto-advance"
title: "Timed Quiz with Auto-Advance on Expiry"
domain: "frontend"
category: "component"
score: 10.4
usage_count: 1
alternative_count: 0
first_seen: "2026-03-04"
last_updated: "2026-03-04"
projects:
  - trivia
---
## Description

A quiz/survey component that shows one question at a time with a countdown timer. When the timer expires, the component auto-advances to the next question (defaulting the answer to "NONE"). Uses `setInterval` at 100ms ticks with a `LinearProgress` bar for visual feedback. Supports configurable response time per question and CSS fade transitions between questions.

## Structure

```typescript
const [idx, setIdx] = useState(0);
const [progress, setProgress] = useState(0);

useEffect(() => {
  const interval = setInterval(() => {
    setProgress(prev => {
      if (prev >= 100) {
        advanceToNext();  // Auto-advance on timeout
        return 0;
      }
      return prev + (10 / responseTime);  // responseTime in seconds
    });
  }, 100);
  return () => clearInterval(interval);
}, [idx]);

// On answer selection: 200ms delay before advance
const handleAnswer = (choice) => {
  setAnswer(idx, choice);
  setTimeout(() => advanceToNext(), 200);
};

// Completion: auto-submit when all questions answered
useEffect(() => {
  if (idx >= prompts.length) onSubmit(answers);
}, [idx]);
```

## Examples

### Trivia
`PromptListDialog.tsx` shows quiz questions one at a time with a `LinearProgress` countdown bar. Timer ticks every 100ms, incrementing by `10/responseTime` (default 10s). `TransitionWrapper` provides 300ms CSS fade animation between questions. `CheckboxList` renders 4 answer options (A/B/C/D) as styled buttons. Auto-submits to backend when all questions are answered.

## Trade-offs

- **Pros**: Engaging gamified experience; prevents indefinite question dwelling; visual timer creates urgency
- **Cons**: Complex interval/state management; must handle cleanup carefully; accessibility concerns with timed interactions
- **When to use**: Quiz games, timed assessments, gamified learning applications

## Related Patterns

- [pin-code-auto-submit-input](pin-code-auto-submit-input.md)
- [dialog-based-navigation](dialog-based-navigation.md)
