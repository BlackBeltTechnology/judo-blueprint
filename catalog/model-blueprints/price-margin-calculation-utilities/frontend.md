## Overview

The library lives in the frontend as a plain TypeScript module with no React import. Form hooks call it when a user leaves a price or margin field, and they write the computed value into the dependent field.

## Implementation Pattern

- **Pure module.** The functions sit in one `.ts` file under the project's utility folder and export values only. They take numbers and return a number or no value.
- **Core conversions.** One function gives the selling price from cost and margin, using cost divided by one minus margin over 100. One gives the margin from cost and selling price, the inverse. One gives the standard selling price from standard minutes and an hourly rate.
- **Null safety.** Each function returns no value for a margin of 100 or more, a zero divisor, or a missing input. The hook then clears the dependent field.
- **Rounding.** Results round to two decimal places by default. The rounding factor is a parameter, so a caller can ask for more places.
- **Unit tests.** A unit test file covers positive and negative margins, zero and missing inputs, the round trip between the forward and inverse functions, and floating-point tolerance.
- **Hook use.** A form hook calls the function in its blur or value-change handler (the model's `onBlur` widget flag makes the generator produce an `on<Field>BlurAction` handler to hook into) and writes the result into the dependent field. The hook does not repeat the arithmetic.
- **Generator protection.** Custom code you add under `src/custom/` is not generated and survives regeneration with no `.generator-ignore` entry. A test or helper placed in a generated folder such as `src/utilities/` would need a `.generator-ignore` entry, or the checksum check fails the build.

The module and hook names belong to the example project. The pure-function pattern is the part that generalizes.

## Examples

### rackinspect
- Framework: React.
- Key files: a single utility module under the custom hooks utilities folder, and its Vitest test file.
- Pattern: the selling-price and markup functions work in both directions between cost price and selling price. The standard-selling-price function converts standard minutes at an hourly rate into a price.
- Notable: the test file checks that the output of one function, fed into its inverse, returns the original input. It sits in the custom folder, so regeneration does not touch it.
