## Overview

A shared TypeScript utility library providing bidirectional gross margin calculations (price to selling price, selling price to margin, time-based standard selling price), consumed by multiple form action hooks for real-time price field computation. Includes comprehensive unit tests. Framework: React.

## Implementation Pattern

- **Utility module**: A standalone `.ts` file in `custom/hooks/utils/` exporting pure functions with no React dependencies
- **Core functions**: `calculateSellingPrice(price, margin)` (gross margin formula: `price / (1 - margin/100)`), `calculateMarkup(price, sellingPrice)` (inverse: `(1 - price/sellingPrice) * 100`), `calculateStandardSellingPrice(standardMinute, sellingPrice)` (time-based: `(standardMinute / 60) * sellingPrice`), `roundToDecimals(value, decimals)`
- **Null safety**: All functions return `null` for invalid inputs (margin >= 100, division by zero, null/undefined inputs)
- **Rounding**: Results rounded to 2 decimal places by default using `Math.round(value * factor) / factor`
- **Unit tests**: Comprehensive Vitest test suite covering positive/negative margins, edge cases (zero, null), bidirectional consistency, and floating-point tolerance
- **Consumption**: Imported by dialog form action hooks (CostPrice create/edit) that call these functions in `onFieldBlur` or `onValueChange` handlers to auto-compute dependent fields
- **Generator-ignore**: Test files listed in `.generator-ignore` to prevent overwriting

## Examples

### rackinspect
- Framework: React
- Key files: `custom/hooks/utils/priceCalculationHelper.ts`, `src/__tests__/priceCalculationHelper.test.ts`
- Pattern: `calculateSellingPrice` and `calculateMarkup` provide bidirectional computation between cost price and selling price via gross margin; `calculateStandardSellingPrice` computes time-based pricing from standard minutes and hourly rate
- Notable: 200+ lines of Vitest tests covering bidirectional consistency (the output of one function fed into the inverse equals the original input), floating-point tolerance, and edge cases. Test file is protected via `.generator-ignore`.
