---
title: JUDO Model Development Guide
description: Primary reference for JUDO model development: layers, workflow, patterns, the JQL expression language reference, pitfalls and best practices.
aliases: [model development guide, how to model entities, JQL expression language, access getter rules, model design patterns, naming conventions for model elements, derived access filter]
keywords: [getVariable, getterExpression, accessType, OperationCallInterceptor, TRANSIENT, Generalization, EntityType, TransferObjectType, MenuItemAccess, judo-model-cli, ReferenceBindingExpressionIsValid, xmi:id]
tags: [domain:model, layer:model, status:platform]
---

# JUDO Model Development Guide

This document is the primary reference for understanding and working with the JUDO application model. It synthesizes foundational concepts, a practical workflow for getting started, and a comprehensive catalog of advanced design patterns for solving real-world modeling problems.

## Table of Contents
1.  [**Part 1: Foundational Concepts**](#part-1-foundational-concepts)
2.  [**Part 2: The Core Modeling Workflow**](#part-2-the-core-modeling-workflow)
3.  [**Part 3: Advanced Modeling Patterns & Use Cases**](#part-3-advanced-modeling-patterns--use-cases)
4.  [**Part 4: Judo Query Language (JQL)**](#part-4-judo-query-language-jql)
5.  [**Part 5: Rules and Best Practices**](#part-5-rules-and-best-practices)

---

## Part 1: Foundational Concepts

### 1.1 The JUDO Two-Layer Architecture

JUDO models have a mandatory two-layer logical structure that promotes abstraction, security, and reusability.

*   **Domain Logic Layer**: This is the core of the application. It contains the **`EntityType`s`**, which are the classes that represent the real-world business objects and rules. This layer is the single source of truth for how data is structured, persisted, and changed.

*   **Service Layer**: This layer acts as a front-facing interface or API for the application, defined by **`TransferObjectType`s`** (TOs). It masks the underlying domain model, providing a simpler and more secure view to clients (like a UI or external systems).

> **Best Practice**: Never expose `EntityType`s directly in an `Access` link. The Service Layer (`TransferObjectType`s) should always be the entry point for any external actor.

### 1.2 Core Object-Oriented Principles

*   **Entity**: A class representing the persistent, core business objects.
*   **Attributes (`Stored` vs. `Derived`)**:
    *   A **`Stored`** attribute is a data field that is persisted in the database.
    *   A **`Derived`** attribute (or "Property") is a read-only, calculated value whose logic is defined in a `Getter expression`.
*   **Relationships (Associations)**:
    *   **Association (`-->`)**: A general "has a" reference between independent objects.
    *   **Composition (`[solid diamond]-->`)**: A strong "is part of" ownership where the child is destroyed with the parent.
    *   **Aggregation (`[hollow diamond]-->`)**: A weaker "owns a" relationship where the child can exist independently.
*   **Inheritance (`Generalization`)**: An "is-a" relationship where a subclass inherits all members from its superclass. A key rule is that **member overriding is not allowed**.

---

## Part 2: The Core Modeling Workflow

This section provides a step-by-step guide to the fundamental process of creating a simple, functional application component from scratch. The steps are written in Designer terms; each of them can also be done with the [JUDO Model CLI](./judo-cli.md) (`create`, `update`, `fill`).

1.  **Create a Project**: Use the "New project" icon in the Designer.
2.  **Define an Entity**: Drag the **Entity** tool from the Palette to create a core business object (e.g., `SalesPerson`).
3.  **Add Attributes**: Drag the **Attribute** tool into the entity. Set its **Attribute Type** to **`Stored`** to ensure it's saved in the database.
4.  **Modify Properties**: Use the **Properties View** to change an element's behavior (e.g., set an attribute to **`Required`**).
5.  **Generate the Default UI**: Right-click the entity and select **"Add features to representations"** to automatically create a `Table`, `Form`, and `View` for it.
6.  **Define an Actor**: Drag the **Actor** tool to create a user role (e.g., `Manager`).
7.  **Create an Access Link**: Use the **Access** tool to connect the `Actor` to the entity's `TransferObjectType`. This exposes the entity's CRUD services through the access point — it does **not** by itself add anything to the UI navigation.
8.  **Add the Menu Item Entry**: Whenever an `Access` is created on an `ActorType` that is intended to be reachable from the UI, a matching `MenuItemAccess` **must** be added under that actor's `<menuItems>` (optionally nested in a `MenuItemGroup`) with its `access` reference pointing to the `Access` from step 7. Without this pairing the data is reachable only via the API, never from the menu. With the model CLI, `create -t Access --ns <actor> --set target=<transferObject>` creates the `MenuItemAccess` together with the `Access` (named `Menu`, labelled with the target type name); `create -t MenuItemAccess` is refused. A transfer object created with a `mapping` also gets its mapped members generated: reuse them, and give any additional derived member a different name (a same-named member is reported as not unique). See [UI Authoring Guide](./ui-authoring-guide.md) and [accesspoint reference](./esm_metamodel/accesspoint.md).

### Working-copy safety during multi-stage ESM changes

The `.model` file is a single XMI document that accumulates every mutation from every stage of a change. Standard git commands treat it as one opaque blob, so it is very easy to lose hours of authoring work with a single rollback.

#### Rules of thumb when a change spans multiple stages (Stage A, B, C…)

1.  **Commit per stage, or at least per green checkpoint.** `git commit -m "Stage B: ..."` after each stage validates. This gives you an explicit rollback target and prevents accidental loss.
2.  **Never run `git restore model/*.model` (or `git checkout -- model/*.model`) with uncommitted mutations unless you have a backup.** It silently reverts *every* ESM mutation made since the last commit — there is no partial undo. One wrong `git restore` has cost full stages of work.
3.  **Before any `git restore` / `git checkout` / branch switch that could touch the model, copy the file aside first:** `cp model/<name>.model /tmp/<name>.model.stageB.bak`. If the restore was a mistake, `cp` the backup back and diff against HEAD to verify.
4.  **Prefer JUDO Model CLI mutations (see [judo-cli.md](./judo-cli.md)) over hand-editing the XMI**, so the set of changes is reproducible from transcripts even if the working copy is lost.

This is workflow advice, not a metamodel rule — but in practice it is the single most common cause of large rework in multi-stage modeling work.

---

## Part 3: Advanced Modeling Patterns & Use Cases

This section is a "cookbook" of reusable design patterns for solving common modeling problems.

### Service Layer Architecture

#### Pattern: Mapped vs. Unmapped Transfer Objects
*   **Mapped TO**: A TO that is structurally linked to a source `EntityType` via a `Mapping`. It acts as a projection or view of the underlying entity. Its members can be:
    *   **Mapped/Bound**: Directly linked to a member on the entity.
    *   **Derived/Property**: A read-only, calculated value with a `Getter expression`.
    *   **Simple/Transient**: A field that exists only on the TO for temporary UI state.
*   **Unmapped TO**: A standalone data container with no underlying entity, often used for complex inputs to an `Operation`.

#### Pattern: Purpose-Built Transfer Objects (DTOs)
*   **Use Case**: The data required for a list view is often a small subset of the data needed for a detail view.
*   **Implementation**: Create multiple TOs for the same `EntityType`: a minimal `...ListTO` for tables and a full `...DetailTO` for forms. The `Access` rule for the table view should target the `...ListTO` to avoid over-fetching data.

### Action & Operation Patterns

#### Pattern: Grouping Contextual Actions
*   **Use Case**: Displaying a group of related actions that operate on a single object's view page.
*   **Solution**: Use a `ui:ActionGroup` in a `View` to hold multiple `OperationForm` buttons.

#### Pattern: Table Actions (Bulk vs. Row)
*   **Use Case**: Defining actions that apply to multiple selected rows (bulk) or to each individual row.
*   **Solution**: In a table's definition, add actions to the `tableOperations` collection (with `isBulk="true"` for bulk) or the `rowOperations` collection.

### Security & Access Control

#### Pattern: User-Specific Data with Derived Accesses
*   **Use Case**: Ensuring a logged-in user can only see their own data (e.g., "My Orders").
*   **Solution**: On an `Access` link, set the **`Access type`** to **`Derived`** and write a **`Getter expression`** that filters data using the `!getVariable("ACTOR", "claim_name")` function.

### UI Modeling & Display Patterns

#### Pattern: Dynamic Page Titles
*   **Use Case**: Make a page title reflect the data being viewed (e.g., "John Doe" instead of "Customer").
*   **Solution**: On a View/Edit page, set the **`titleFrom`** property to **`Attribute`** and select the desired `DataMember` as the **`titleAttribute`**.

#### Pattern: Conditional UI Element Visibility
*   **Use Case**: A UI element (field, group, button) should only be visible or enabled based on other data in the form.
*   **Solution**: Use `enabledBy` or `hiddenBy` on any `ui:VisualElement`, pointing it to a `Boolean` `DataMember`.

#### Pattern: Alternative Data Representations
*   **Use Case**: Display a list as a grid of cards, chips, or an autocomplete field instead of a table.
*   **Solution**: Use the `representationComponent` attribute on a `TabularReferenceField` (`"table"`, `"tag"`, `"card"` or `"button"`). A dropdown/autocomplete selector for a relation is a separate widget (`isTypeAheadField`, `autocompleteRows`), not a `representationComponent` value.

### Advanced Data Modeling Patterns

#### Pattern: Polymorphism with Inheritance
*   **Use Case**: Model a base concept with several specialized types (e.g., `Pro` and `Con` are types of `Argument`).
*   **Solution**: Use `Generalization` to establish an "is-a" hierarchy between `EntityType`s. Note that inheritance between `TransferObjectType`s is not supported.

#### Pattern: Parameterized Queries
*   **Use Case**: Create a derived feature that accepts a parameter for its calculation (e.g., find all `Order`s placed after a user-specified date).
*   **Solution**: Use a `primitive query` (for attributes) or a `complex query` (for relations). This is a derived feature with an `input` (`TransferObjectType`). The `getterExpression` can access this via the `input` variable (attributes only).

---

## Part 4: Judo Query Language (JQL)

JQL is the powerful expression language used in model scripts, such as `Getter expression`s and `Operation` bodies. It provides a rich set of features for data manipulation, navigation, and logic execution.

### Key Concepts
-   **The `self` variable** to refer to the current object context.
-   **Navigation** across relationships using the `.` operator.
-   A library of **built-in functions** for strings, numbers, and collections, called with the `!` operator.
-   Specific handling of the **`undefined`** value.

### JQL Reference Guide

This document provides a detailed reference for JQL (Judo Query Language), the expression language used throughout JUDO models in places like `Getter expression`s and `Operation` bodies.

## 1. General Concepts

### Comments
JQL supports two types of comments:
-   **Single-line**: Begins with `//`.
-   **Multi-line**: Enclosed between `/*` and `*/`.

### `undefined` Value
`undefined` represents the absence of a value. It has special behavior in expressions:
-   **Propagation**: Any arithmetic or logical operation involving `undefined` evaluates to `undefined`. For example, `undefined + 2` results in `undefined`.
-   **Comparisons**: Logical comparisons with `undefined` always result in `undefined`, not `true` or `false`.
-   **Function Calls**: Calling a function on `undefined` results in `undefined`. For example, an `undefined` collection's `!count()` is `undefined`, not `0`.

---

## 2. Special JQL Functions

### `!getVariable(category, name)`
This powerful function retrieves request-scoped context variables. It is the primary way to access information about the currently authenticated user.

*   **`!getVariable('PRINCIPAL', 'claim_name')`**
    *   **Purpose**: To read an attribute of the current **principal `TransferObjectType`**. The runtime calls the actor's generated `_principal` operation and returns the named attribute of its result (`PrincipalVariableProvider`).
    *   **Use Case**: Actors whose `principal` is an `unmapped` `TransferObjectType` populated by the framework from the IdP token. The values come from the principal TO's attributes, not directly from the raw JWT. An actor with **no** `principal` has no `_principal` operation, so `PRINCIPAL.*` yields nothing.
    *   **Example**: `String!getVariable('PRINCIPAL', 'preferred_username')`.

*   **`!getVariable('USER', 'claim_name')`**
    *   **Purpose**: To access **raw JWT claims** of the logged-in user.
    *   **Use Case**: **Required** for token-only actors (no `principal` TO). For such actors the JWT claims surface under the `USER` category — `PRINCIPAL.*` returns empty and silently breaks access filters, custom ops, and audit logic. This is the single most common source of "mysterious empty claim" bugs. The `USER` category reads the attributes of the authenticated `JudoPrincipal` (the token claims) and works for every actor shape.
    *   **Example**: `String!getVariable('USER', 'sub')` retrieves the subject identifier directly from the JWT.

*   **`!getVariable('ACTOR', 'attribute_name')`**
    *   **Purpose**: To access attributes from the *persisted `Actor` entity* that is associated with the current user's session.
    *   **Use Case**: Used in `Derived Access` rules to filter data based on properties of the logged-in user's persisted record.
    *   **Example**: `CRM::SalesPerson!filter(sp | sp.email == String!getVariable("ACTOR", "email"))!any()` assumes the `Actor` is a `SalesPerson` and filters based on its `email` attribute.

> [!IMPORTANT]
> **Picking the right category**
>
> | Actor shape | JWT claims via | Persisted attrs via |
> |---|---|---|
> | Token-only: no `principal` TO (no persisted record) | `USER.*` | n/a |
> | Unmapped principal TO | `PRINCIPAL.*` (principal TO attributes) or `USER.*` (raw claims) | n/a |
> | Mapped principal TO (persisted Actor entity) | `USER.*` for raw claims | `ACTOR.*` |
>
> Using `PRINCIPAL.*` against an actor with no `principal` TO is valid JQL but returns empty at runtime. See [ACTOR vs PRINCIPAL vs USER](./advanced-modeling-patterns.md#actor-vs-principal-vs-user-context-variables).

### Other environment-variable categories

Besides `PRINCIPAL`, `USER` and `ACTOR`, the engine knows more categories, mostly used implicitly:

- **`SYSTEM`**: `current_date`, `current_timestamp`, `current_time`, reached through `<Type>!now()` (see *Temporal functions*).
- **`PARAMETER`**: the attributes of an input parameter transfer object of a parameterized query become `PARAMETER`-category variables while the expression is resolved.
- **`ENVIRONMENT`, `SEQUENCE`, `REQUEST`**: runtime providers registered by the default variable resolver (environment configuration values, database sequences, per-request parameters). An undefined variable resolves to `null` with a warning.

`!getVariable` is typed by the primitive it is called on (`Integer`, `Decimal`, `Boolean`, `String`, an enumeration, a custom type, `Date`, `Timestamp`, `Time`); for measured numerics the variable carries the unit. It always returns a scalar, never a collection.

### JQL grammar quirks

- The ternary `cond ? then : else` is right-associative and compiles to a typed switch expression. The condition must be a logical expression; `then` and `else` must be of the same kind (a decimal result is chosen when either side is decimal; entity branches resolve to a common supertype, and an ambiguous or missing common supertype fails the build).
- Equality is `==` and `!=` only (no `=` and no `<>`). Keywords are case-insensitive.
- There is a `^` power operator between multiplication and the `as` (spawn) operator.
- Enumeration literals are `EnumType#LITERAL`; a function call is `expr!name(args)` and its result can be navigated further.
- Collection iterator functions take a lambda over **one** iterator variable and may select only an immediate field of it; multi-step navigation inside the lambda body is out of scope (see *Lambda scopes do not nest*).

---

## 3. Primitive Data Types

### String
Represents a text value. String literals are enclosed in single (`'`) or double (`"`) quotes.

| Operation | Result | Meaning | Example |
| :--- | :--- | :--- | :--- |
| `==` | Boolean | Case-sensitive equality comparison. | `"apple" == "apple"` is `true`. |
| `<` , `>` | Boolean | Case-insensitive ordering comparison. | `"apple" < "pear"` is `true`. |
| `+` | String | Concatenates two strings. | `"apple" + "tree"` is `"appletree"`. |
| `!length()` | Numeric | Returns the number of characters in the string. | `'apple'!length()` is `5`. |
| `!first(n)` | String | Returns the first `n` characters. | `'apple'!first(2)` is `'ap'`. |
| `!last(n)` | String | Returns the last `n` characters. | `'apple'!last(1)` is `'e'`. |
| `!position(sub)` | Numeric | Returns the 1-based index of the first occurrence of substring `sub`, or `0` if not found. | `'apple'!position('p')` is `2`. |
| `!substring(pos, len)` | String | Returns a substring of `len` characters starting from the 1-based `pos`. | `'apple'!substring(2,3)` is `'ppl'`. |
| `!lowerCase()` | String | Converts the string to lowercase. | `'ApPlE'!lowerCase()` is `'apple'`. |
| `!upperCase()` | String | Converts the string to uppercase. | `'ApPlE'!upperCase()` is `'APPLE'`. |
| `!matches(regex)` | Boolean | Returns `true` if the string matches the given regular expression. | `'apple'!matches('.*pl.')` is `true`. |
| `!like(pattern)` | Boolean | Returns `true` if the string matches the SQL-style LIKE `pattern` (`%` wildcard, `_` single char). | `'apple'!like('%pl_')` is `true`. |
| `!replace(old, new)` | String | Replaces all occurrences of `old` with `new`. | `'apple'!replace('le', 'endix')` is `'appendix'`. |
| `!trim()` | String | Removes leading and trailing whitespace. | `'   apple '!trim()` is `'apple'`. |
| `!ltrim()` / `!rtrim()` | String | Removes leading / trailing whitespace only. | `'  apple'!ltrim()` is `'apple'`. |
| `!lpad(size [, pad])` / `!rpad(size [, pad])` | String | Pads the string on the left / right up to `size` characters; the default pad string is a single space. | `'7'!lpad(3, '0')` is `'007'`. |
| `!capitalize()` | String | Upper-cases the first character and lower-cases the rest. | `'aPPLE'!capitalize()` is `'Apple'`. |
| `!ilike(pattern)` | Boolean | Case-insensitive variant of `!like`. | `'Apple'!ilike('a%')` is `true`. |

### Numeric
Represents numeric values. Literals are written as digits with an optional decimal point (e.g., `10`, `3.14`).

| Operation | Result | Meaning | Example |
| :--- | :--- | :--- | :--- |
| `==`, `!=`, `<`, `>`, `<=`, `>=` | Boolean | Standard numerical comparison. | `1.00 == 1` is `true`. |
| `+`, `-`, `*`, `/` | Numeric | Arithmetic operations. | `9.0 / 2` is `4.5`. |
| `mod`, `div` | Numeric | Integer modulus and division. Both arguments must have a scale of 0. | `9 mod 2` is `1`. |
| `!round()` | Numeric | Rounds a non-integer number to the nearest integer. | `7.89!round()` is `8`. |
| `!round(scale)` | Numeric | Rounds to `scale` decimal places (a decimal result). | `7.891!round(2)` is `7.89`. |
| `!abs()`, `!ceil()`, `!floor()` | Numeric | Absolute value, round up, round down. | `(-3)!abs()` is `3`. |
| `-` (unary) | Numeric | Negation. | `5 + -5` is `0`. |
| `!asString()` | String | Converts the number to its string representation. | `123.45!asString()` is `"123.45"`. |

### Measured Numeric
Represents a numeric value with a unit of measure (e.g., `5 [kg]`). JUDO automatically handles unit conversions during comparisons and assignments.
-   `5 [km] == 5000 [m]` is `true`.
-   `1 [kg] + 50 [dkg]` evaluates to `1.5 [kg]` if the target's unit is `kg`.

**Literal syntax.** A measured literal is a number followed by the unit in brackets. The bracket content is either the unit alone (`10[kg]`) or `measure#unit` (`10[Mass#kilogram]`) when the unit name is ambiguous; measure namespaces are joined with `::`. An unknown unit or measure fails the expression build (`No unit found in model` / `Unknown measure`).

**Durations.** Only the duration units `MILLISECOND`, `SECOND`, `MINUTE`, `HOUR`, `DAY` and `WEEK` support addition; `MONTH` and `YEAR` do not (a month has no fixed length). Adding or subtracting a temporal value requires a unit that supports addition. `!elapsedTimeFrom(other [, measure])` (the difference of two dates, timestamps or times) takes the duration measure as an optional second argument; without it the model must contain exactly one default duration measure (`No single duration measure in the model` otherwise).

### Boolean
Represents a logical value: `true` or `false`. JQL uses a three-valued logic system (Kleene logic) that includes `undefined`.

| Keyword | Meaning |
| :--- | :--- |
| `not` | Logical negation (`!` is only the prefix of functions such as `!empty()`, not a negation operator: write `not n.read` or `n.read == false`, never `!n.read`) |
| `and` | Logical AND |
| `or` | Inclusive logical OR |
| `xor` | Exclusive logical OR |
| `implies` | Logical material implication |

### Enumeration
Represents a value from a predefined set of members. Members are referenced by `EnumerationName#MEMBER_NAME`.

| Operation | Result | Meaning |
| :--- | :--- | :--- |
| `==`, `!=` | Boolean | Equality comparison. |
| `!asString()`| String | Returns the literal name of the member as a string. |

An enumeration literal is written `<Model>::<EnumType>#<LITERAL>`, for example `defaultExpression = "<Model>::<EnumType>#<LITERAL>"` on a stored attribute. Use the fully qualified type name, as for other types (see 5.2); `<EnumType>#<LITERAL>` also passes `validate` in the CLI.

### Date & Timestamp
-   **Date**: Represents a calendar date. Literals are delimited by backticks (e.g., `` `2024-01-01` ``).
-   **Timestamp**: Represents a point in time with a mandatory time zone. Literals are ISO-8601 strings in backticks (e.g., `` `2024-01-01T12:00:00Z` ``).

Both support standard chronological comparisons (`<`, `>`, `==`, etc.) and `!asString()`.

#### Temporal functions

| Function | Applies to | Meaning |
| :--- | :--- | :--- |
| `<Type>!now()` | Date, Timestamp, Time types | Current date / timestamp / time. These are `SYSTEM`-category environment variables (`current_date`, `current_timestamp`, `current_time`), e.g. `<app>::types::Timestamp!now()`. As an attribute default it fills the value at creation. |
| `!year()`, `!month()`, `!day()` | Date, Timestamp | Extract the part as an integer. |
| `!hour()`, `!minute()`, `!second()`, `!millisecond()` | Timestamp, Time | Extract the part. |
| `!dayOfWeek()`, `!dayOfYear()` | Date | Day number within the week / year. |
| `!date()`, `!time()` | Timestamp | The date / time part of a timestamp. |
| `<Type>!of(...)` | Constructors | Date: exactly three integers `(year, month, day)`. Time: 2 to 4 integers `(hour, minute [, second [, millisecond]])`. Timestamp: `(date [, time])` or `(year, month, day, hour, minute [, second [, millisecond]])`. |
| `!elapsedTimeFrom(other [, measure])` | Date, Timestamp, Time | Difference as a measured number (dates are counted in days, timestamps and times in seconds, then converted to the measure unit), e.g. `self.end!elapsedTimeFrom(self.start)`. |
| `!asMilliseconds()` / `<Type>!fromMilliseconds(n)` | Temporal | Convert to / from epoch milliseconds. |
| `!plusYears(n)`, `!plusMonths(n)`, `!plusDays(n)`, `!plusHours(n)`, `!plusMinutes(n)`, `!plusSeconds(n)`, `!plusMilliseconds(n)` | Date, Timestamp | Timestamp arithmetic. |

---

## 4. Reference Functions

These functions operate on object instances or collections of instances.

### Instance Functions
Operate on a single object instance.

| Function | Result | Meaning |
| :--- | :--- | :--- |
| `!container(type)` | Instance | Returns the container of the instance if it's part of a `COMPOSITION`. |
| `!kindof(type)` | Boolean | Returns `true` if the instance is of the given `type` or a descendant of it. |
| `!typeof(type)` | Boolean | Returns `true` only if the instance is of the exact `type` specified. |
| `!asType(type)` | Instance | Returns the instance if its type matches, otherwise `undefined`. |
| `!isDefined()` | Boolean | Returns `true` if the object is not `undefined`. |
| `!isUndefined()`| Boolean | Returns `true` if the object is `undefined`. |
| `!memberOf(coll)`| Boolean | Returns `true` if the instance is a member of the specified collection `coll`. |

`!container(Type)` also works as the getter of a derived relation on the contained entity, typed as the container with cardinality `0..1`: `self!container(<Parent>)`. The result can be narrowed with `!asType(<Sub>)`. `Type` must be a type that can contain `self` (a composition owner, including its supertypes or subtypes); otherwise the expression build fails with `<Type> type is not a container type of <Self type>`, also when `Type` is the type itself. A mapped transfer object relation can expose the derived relation by binding to it.

### Collection Functions
Operate on a collection of object instances. The `i` in examples represents an iterator variable.

| Function | Result | Meaning & Example |
| :--- | :--- | :--- |
| `!any()` | Instance | Returns an arbitrary single instance from the collection. **Use sparingly** — see the *Using `!any()` correctly* note below. |
| `!contains(obj)` | Boolean | Returns `true` if the collection contains the specified `obj`. |
| `!count()` | Numeric | Returns the number of items in the collection. |
| `!empty()` | Boolean | Returns `true` if the collection has no items. There is no `!isEmpty()` (it fails with `Unknown function: isempty`); negate with `not ...!empty()` or use `!count() > 0`. |
| `!exists(i \| expr)` | Boolean | Returns `true` if the logical `expr` is true for at least one item `i`. |
| `!filter(i \| expr)` | Collection | Returns a new collection containing only items `i` for which the logical `expr` is true.<br>`self.items!filter(i \| i.price > 10)` |
| `!forAll(i \| expr)` | Boolean | Returns `true` if the logical `expr` is true for all items `i`. |
| `!anytrue(i \| expr)` / `!alltrue(...)` / `!anyfalse(...)` / `!allfalse(...)` | Boolean | Quantifiers over a boolean-valued selector. `!alltrue` is equivalent to `!forAll`; `!anyfalse` to `not !forAll`. |
| `!head()` / `!heads(i \| key)` | Instance / Collection | `!head()` without a key returns the first item; the order is deterministic only after `!sort`. `!head(i \| key)` returns one item with the smallest `key` (`DESC`: the largest). `!heads(i \| key)` returns **all** items that share that smallest (or, with `DESC`, largest) key, so it is the tie set, not the first `n` items. There is no top-N function: sort, then limit through paging (`rowsPerPage`, `limit`). |
| `!tail()` / `!tails(i \| key)` | Instance / Collection | The mirror of `head` / `heads` (largest key first). |
| `!sort(i \| sel [,...])`| Collection | Returns a new collection sorted by one or more selectors (`sel`). `ASC` (default) or `DESC` can be specified.<br>`self.items!sort(i \| i.price DESC, i.name)` |
| `!join(i \| selector, separator)` | String | ⚠️ **Recognised by the JQL grammar and expression builder, but not implemented by the query engine** (the converter throws `Not supported yet`). The function name is registered in the parser (so expressions using it pass `transform` without an `Unknown function` error), but evaluation fails downstream — there is currently no built-in string-aggregation function. For concatenating a string attribute across a collection, use a **backend-computed `TRANSIENT` TO attribute** populated from an `OperationCallInterceptor` (see Pitfall 5.1 below and the backend Interceptors guide). Do **not** use `!collectAsString` or `!mkString` either — they do not exist at all. |
| `!asCollection(type)`| Collection | Casts the collection to a collection of the specified `type`. |
| `!anyTrue(i \| expr)` etc. | Boolean | `!anyTrue`/`!anyFalse` compile to an exists test; `!allTrue`/`!allFalse` compile to a for-all test that also requires the value to be defined. |
| `!avg(i \| selector)` | Numeric | Returns the average value of the `selector` across the collection (integer, decimal, date, timestamp or time values; not strings). |
| `!sum(i \| selector)` | Numeric | Returns the sum of the `selector` across the collection (integer and decimal values only; other types fail with `Invalid expression for aggregation`). |
| `!min(i \| selector)` | Numeric | Returns the minimum value of the `selector` across the collection. |
| `!max(i \| selector)` | Numeric | Returns the maximum value of the `selector` across the collection. |

#### Aggregates on empty collections and combining collections

`!count()` of an empty or missing collection is `0` (the query wraps it in `COALESCE(..., 0)`). `!sum`, `!min` and `!max` are plain SQL aggregates without a default: on an empty collection the result is `undefined` (SQL `NULL`), not `0`; item values that are `undefined` are skipped by the aggregate. Use `!isDefined()` or a conditional to supply a default, for example `self.items!sum(i | i.points)!isDefined() ? self.items!sum(i | i.points) : 0` (derived from the generated SQL; the example expression is unverified).

JQL has no union operator. To combine items reached directly with items reached through another relation, navigate through the multi-valued relations or filter the target type:

```
// items of the related groups only (navigation flattens collections)
self.<groups>.<items>
// direct items plus group items, each item once
<Model>::<Item>!filter(i | self.<items>!contains(i) or self.<groups>.<items>!contains(i))
```

Use the second form as the getter of a derived `0..*` relation.

#### Using `!any()` correctly

`!any()` exists to **collapse a collection to a single instance** at the *end* of a navigation chain. Two rules govern its use:

1. **`!any()` is only required when the final value of the expression must be a single instance** — for example a singleton `Access` (`upper = 1`) whose `getterExpression` resolves to one row, or a `DERIVED` attribute typed as a single entity reference. If the next step in the expression is a *relation navigation*, `!any()` is **redundant whenever the upstream filter is guaranteed to produce at most one element** (e.g. a filter on a unique key such as `userName == ACTOR.userName`). In that case the collection navigation flattens identically.
2. **`!any()` may appear at most once in an expression.** Chaining multiple `!any()` calls is invalid.

**Canonical example.** Given a unique-by-`userName` filter:

```jql
-- Equivalent: navigation flattens through a guaranteed-singleton collection
<app>::entities::User
  !filter(u | u.userName == <app>::types::String!getVariable('ACTOR', 'userName'))
  .accessibleTemplates

-- Same result, redundant !any()
<app>::entities::User
  !filter(u | u.userName == <app>::types::String!getVariable('ACTOR', 'userName'))
  !any().accessibleTemplates
```

**When you DO need `!any()`** — the expression must terminate at a *single instance*, not a relation:

```jql
-- getterExpression of a singleton Access (upper=1) returning the current user row
<app>::entities::User
  !filter(u | u.userName == <app>::types::String!getVariable('ACTOR', 'userName'))
  !any()
```

**Heuristic:** if the expression ends with a *relation step* (`.someRelation`) and the upstream filter is on a unique key, drop the `!any()`. Keep `!any()` only when the expression's final type must be a single instance and the upstream is a collection.

---

### Authoritative function registry

The JQL builder registers exactly this closed set of collection functions:

```
count, head, heads, tail, tails, any, filter, exists, forall,
anytrue, alltrue, anyfalse, allfalse, empty,
join, sort, min, max, sum, avg, contains, memberof, ascollection
```

Any `!<name>(...)` call whose `<name>` is not in this list fails the builder with `Unknown function: <name>`. In particular `!collectAsString` and `!mkString` **do not exist** — there is no working string-aggregation function: `!join(lambda, separator)` is parsed but not supported by the query engine (see the `!join` row above), so compute the string in a backend `TRANSIENT` TO attribute.

---

## 5. JQL Pitfalls & Scoping Rules

Four grammar/scope rules cause the majority of `Errors during building expression` failures. They are enforced by the JQL parser / builder / ASM validator, and surface only under the full `./judo.sh build` (EVL → ESM→Expression → PSM→ASM) — not under `transform --skip liquibase --load`.

### 5.1 Lambda scopes do not nest

Every `!forAll(x | …)` / `!filter(x | …)` / `!exists(x | …)` lambda receives exactly one iteration variable `x` and **nothing else from the enclosing scope** — not `self`, not the outer lambda's variable.

```jql
// ❌ DOES NOT COMPILE — `self` is not re-bound inside the inner lambda
self.partner.supportedLanguages!forAll(psl |
  self.paragraphs!forAll(tp | …))

// ❌ DOES NOT COMPILE — outer `tp` is not visible inside the inner lambda
tp.template.partner.supportedLanguages!forAll(psl |
  self.paragraphs!forAll(tp2 | psl.language == tp.paragraph.language))
```

When the inner predicate must reach the outer collection, navigate via a relation (e.g. `y.parent.xs`). Bipartite / cross-product predicates of the form "∀ a ∈ A, ∀ b ∈ B, ∃ c ∈ C(a,b)" are **not expressible** as a single JQL expression — compute them in Java via an `OperationCallInterceptor` writing to a `TRANSIENT` TO attribute. See [Interceptors Guide](../backend/interceptors.md), *Backend-Computed TO Attribute (JQL Escape Hatch)*.

### 5.2 Primitives must be fully qualified

JQL's `QualifiedName` rule requires either a bare lambda variable (`p`, `self`, …) or a **fully-qualified type path**. `String`, `Integer`, `Boolean`, etc. are not reserved builtins — they are ordinary `DataType` elements that live in some package.

```jql
// ❌ Unknown symbol: String — Use fully qualified name (:: separated)
String!getVariable('PRINCIPAL', 'claim_name')

// ✅ correct for a project whose primitives live under `<Model>::types`
<app>::types::String!getVariable('PRINCIPAL', 'claim_name')
```

### 5.3 `!getVariable` returns a scalar String only

`!getVariable(category, name)` has no collection-returning variant, and JQL has no generic-type syntax. Both of the following fail the Xtext parser (`no viable alternative at input '!'`):

```jql
Sequence<String>!getVariable('PRINCIPAL', 'partner_scope')
String[]!getVariable('PRINCIPAL', 'partner_scope')
```

Multi-value claims (e.g. an array `partner_scope` claim) are therefore **not consumable in JQL**. Options: (a) flatten at the IdP and compare with `==`; or (b) compute the scope in Java from `SecurityContext` and narrow via an `OperationCallInterceptor`. See [Architectural Patterns](../backend/architectural-patterns.md), §1 *Model-Driven Multi-Tenancy*.

### 5.4 `self` is not in scope on access getters

`ActorType.accesses[*].getterExpression` runs at actor-level and has no `self`. The filter base must be the **entity** FQN, not the TO:

```jql
// ❌ Unknown symbol: self (on an ActorType access getter)
self.code!memberOf(…)

// ✅ entity-first pattern
<app>::entities::Partner!filter(p |
  p.code == <app>::types::String!getVariable('PRINCIPAL', 'partner_code'))

// ❌ fails ASM ReferenceExpressionMatchesBinding
<app>::services::PartnerTO!filter(…)
```

Additionally, `accessType="DERIVED"` requires a **reference-returning** expression; a boolean literal (`getterExpression="true"`) is rejected by `ReferenceBindingExpressionIsValid`. For an unrestricted access, use `accessType="ALL"` with **no** getter.

See [Architectural Patterns](../backend/architectural-patterns.md), *Rules for `accesses[*].getterExpression`*, for the complete set of four rules.

---

## Part 5: Rules and Best Practices

### ⚠️ CRITICAL: Prefer the CLI; document every hand-edit

The ESM model file (`/model/<app>.model`) is complex XML (XMI). **The primary authoring tool is `judo-model-cli`** (or the Judo Designer GUI). Direct edits should be avoided because they are easy to get wrong and bypass schema validation.

In practice, a narrow class of edits cannot be performed through the CLI and must be applied directly to the XMI:

| Case | Why the CLI can't do it |
|---|---|
| `xsi:type` polymorphic child (`<columns xsi:type="ui:DataColumn">`) | CLI does not address polymorphic child containers. |
| Adding a new `xmlns:` to the root element | CLI does not touch XMI namespace declarations. |
| Space-separated ID list on multi-reference features (e.g. `BinaryType.mimeTypes="_id1 _id2"`) | CLI's `-s key=value` flag uses commas as the separator. |
| Root-level `<mimeTypes>` objects referenced from `BinaryType` | No CLI mutation for model-level `MimeType` children. |

When a hand-edit is required:

1. Record what was in the model, what the validator / build error said, and what was changed — agents should keep such a ledger alongside their proposals.
2. Verify by running the full `./judo.sh build` (not `transform --skip liquibase --load`, which does not exercise EVL, JQL builder, ASM validator, or TypeScript compile).
3. Keep the diff minimal — touch only the specific element; do not re-flow the file or re-renumber IDs.

### Reserved member names on `createable` TOs

JUDO auto-generates factory methods per createable TO; a member named identically to one of those methods collides at frontend build time with `TS2393 Duplicate function implementation`. For the current list of reserved names and the detection/rename pattern, see [Generator Reserved Names](./esm_metamodel/generator-reserved-names.md).

### JQL cheatsheet for access-getter authoring

When writing `getterExpression` on an `ActorType.accesses` element:

- **Filter base = entity FQN**, not TO FQN: `<app>::entities::<Entity>!filter(x | …)`.
- **No `self`** (unbound at actor scope; see §5.4).
- **No boolean literals** — `getterExpression="true"` on a `DERIVED` access fails ASM `ReferenceBindingExpressionIsValid`. For an unfiltered access, use `accessType="ALL"` with no getter.
- **Fully-qualified primitives** in any `!getVariable(…)` call (see §5.2).

### Do not edit the model file by hand
The ESM model file (`model/<app>.model`) is XMI. Never edit it as text: change it only through the JUDO Model CLI (see [judo-cli.md](./judo-cli.md)) or the JUDO Designer. Hand edits break cross-references (`xmi:id`) and can corrupt the model.

### Naming Conventions
*   Names are case-sensitive.
*   Allowed characters: letters (a-z, A-Z), digits (0-9), and underscores (_).
*   Must start with a letter or an underscore. Cannot end with an underscore or contain `__`.
*   Names must be unique within their container.

### General Best Practices
1.  **Start Simple**: Add complexity incrementally.
2.  **Use Clear Names**: `CanvassingEvent` is better than `Event`.
3.  **Define Relationships Carefully**: Consider cardinality and ownership (`Composition` vs. `Association`).
4.  **Use Constraints**: Use `required` and `Identifier` where applicable.
5.  **Coordinate with Team**: Model changes affect the entire application.
