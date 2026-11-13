---
id: timed-step-auto-advance
title: Timed Step with Auto-Advance on Expiry
description: "A custom component that shows one step at a time with a countdown and moves on, with a default answer, when the time runs out."
aliases: [countdown question, timed survey, timed-questionnaire-auto-advance, timed questionnaire]
keywords: [timer, countdown, auto advance, setInterval, LinearProgress, step, survey, custom component]
tags: ["domain:frontend", "layer:frontend", "project:trivia", "status:single-project"]
category: component
status: single-project
projects: [trivia]
evidence: ["trivia:unrecorded"]
alternatives: []
related: [pin-code-auto-submit-input, dialog-based-navigation, custom-visual-element-override]
fragment: "none: frontend-only"
first_seen: 2026-03-04
last_updated: 2026-11-10
---
## Intent

A timed sequence of questions or steps shows one at a time under a time limit. When the limit passes, the component records a default answer and advances; when the last step is done, it submits all answers at once.

## Practice

### Platform base

The platform has no timer or question widget. What it supplies is the place to put one and the way to send the result:

- A custom component is attached through a custom implementation visual element of the model and registered as a service under `CUSTOM_VISUAL_ELEMENT_INTERFACE_KEY`; the scaffold generated under `src/custom/hooks/custom-implementations/` shows the proxy props type ([component replacement hook](../../agent-docs/frontend/advanced-patterns.md)). A dialog or page of your own can be reached by [[dialog-based-navigation]].
- Submitting the answers is an ordinary call of a bound or unbound operation of the model, through the generated service layer. Whether an answer is correct is decided on the server, not in the component.
- Custom code lives in `src/custom/`; files you add there are not generated ([extension points](../../agent-docs/frontend/extension-points.md)).

### Practice notes: interval-driven step flow

The countdown and advance logic is custom code, not a platform feature:

- State: the current step index and a progress value from 0 to 100.
- A `setInterval` ticks every 100 ms and adds `10 / responseTime` (response time in seconds) to the progress; a `LinearProgress` bar renders it. At 100 the component advances and resets progress.
- The effect depends on the step index, so each step gets a fresh interval and the cleanup function clears the old one.
- Picking an answer stores it and advances after a short delay (200 ms) so the choice is visible; an expired step stores the default answer "none".
- A CSS fade wrapper (about 300 ms) softens the change between steps.
- When the index passes the last step, an effect calls the submit callback with all answers.

```typescript
// Example code
useEffect(() => {
  const interval = setInterval(() => {
    setProgress(prev => {
      if (prev >= 100) { advanceToNext(); return 0; }
      return prev + 10 / responseTime;
    });
  }, 100);
  return () => clearInterval(interval);
}, [idx]);
```

## Rationale

A per-step interval keeps the time limit local to one step and prevents dwelling. The cost is careful timer cleanup and an accessibility concern: people who need more time cannot get it unless the response time is configurable or the limit can be switched off.

## Example

In one app a dialog shows one question with four options and a progress bar over a 10-second default, fades between steps and submits all answers to the backend after the last one.

## When to avoid

- Flows where users need unlimited time or assistive technology; offer an untimed mode.
- When the time limit must be enforced: a client timer is not trustworthy, so the server has to check timestamps itself.

## Related

- [[pin-code-auto-submit-input]] — another auto-advancing custom input
- [[dialog-based-navigation]] — presenting the questions in a dialog
- [[custom-visual-element-override]] — attaching a custom component to a generated page
