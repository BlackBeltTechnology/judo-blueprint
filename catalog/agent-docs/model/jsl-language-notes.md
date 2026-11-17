---
title: JSL Language Rules
description: JSL identifiers, built-in libraries, actor grammar limits and the validator rules that fail a model build.
aliases: [JSL syntax rules, why model build fails, reserved word as name, actor declaration syntax, JSL editor plugin, built-in functions list]
keywords: [judo::types, judo::functions, actor, realm, claim, identity, guard, getVariable, _MetadataSecurityFor, jsl-language.vsix, eager, required]
tags: [domain:model, layer:model, status:platform]
---

# JSL Language Rules

JSL is the textual modelling language of newer JUDO projects (the ESM XMI models used by the CLI and Designer are the other authoring form). This page collects the grammar limits and validator rules that most often fail a model build.

## Identifiers and reserved words

Identifiers are ASCII letters and digits starting with a letter. A reserved word (`void`, `self`, `true`, `false`, `not`, ...) can be used as an element name by quoting it in backticks (`` `void` ``); the parser strips the backticks and serialisation writes reserved words back quoted. Qualified names are split on `::` and each segment is converted separately.

## Built-in libraries

Every JSL model implicitly imports two framework models. `judo::types` declares `Boolean`, `Date`, `Time`, `Timestamp`, `Integer` (numeric, precision 9, scale 0), `Long` (precision 15, scale 0) (project type libraries often declare their own `Long` with precision 18; the SDK maps precision 10-19 to `java.lang.Long` either way, see [type.md](esm_metamodel/type.md)) and `String` (min-size 0, max-size 4000). `judo::functions` provides the string functions (`matches`, `like`, `ilike`, `replace`, `lpad`, `rpad`, `substring`), `isDefined`/`isUndefined`/`orElse`/`asString` on each type, the collection lambdas (`first`, `last`, `front`, `back`, `filter`, `anyTrue`, `allTrue`, `anyFalse`, `allFalse`, `min`, `max`, `avg`, `sum`), the entity functions (`typeOf`, `kindOf`, `container`, `asType`, `memberOf`, `all`, `any`, `contains`, `size`) and `getVariable(category, key)`, which is only declared on boolean, numeric, string, date, time and timestamp types. Collection iterator lambdas take one boolean or numeric expression and may select only an immediate field of the iterator variable.

When JSL is translated to JQL some functions are renamed: `right` to `last`, `left` to `first`, `lower`/`upper` to `lowerCase`/`upperCase`, `size` to `length` (string) or `count` (collection); `first`/`last`/`front`/`back` lambdas become `!heads(...)`/`!tails(...)` with a trailing `DESC`, and `^` becomes repeated multiplication.

## Actor declarations

`actor Name [realm:"..."] [claim:"..."] [identity:Transfer::field] [guard <expr>] { access ... }`. Only the modifiers `realm`, `claim`, `identity` and `guard` exist (there is no `human` modifier); the body accepts only `access` declarations (actor group, link and table rules are commented out in the grammar). `identity` references a transfer field as `TransferName::fieldName`; `guard` takes a boolean expression and compiles to a filter on the managed mapped actor type.

## Constraints that fail the build

- A collection cannot be `required`; a bidirectional relation cannot be required on both ends.
- An abstract entity cannot be used as a field type and can only be inherited.
- An identifier cannot be calculated and cannot be a numeric type with a scale.
- `eager` is invalid on primitive fields. Entity relations are lazy by default (writing `eager:false` only produces an informational hint).
- A default expression cannot reference `self`; calculated and composition members cannot have a default.
- A cycle of required members is an ERROR; eager cycles are only warnings.
- Enumerations need at least one literal; ordinals must be 0 to 9999 and unique, names unique (case-insensitive).
- Binary primitives need `mime-type:` and `max-file-size:` (see the binary rules in [esm_metamodel/type.md](./esm_metamodel/type.md)).

### Syntax limits

- `Long` is not a keyword; it is a type declared in `judo::types`. For other widths declare a numeric type with a precision.
- The size unit keyword is `KB` (upper-case K); `kB` does not parse.
- Transfer events take no parameter list and no `on` modifier: `event create Name;`, `event update Name;`, `event initialize Name;` (likewise `fetch` and `delete`).
- Transfer fields and actor accesses have no `bind` modifier (`bind:true` is not valid); read-write binding is written with the `<=>` operator.
- A `union` with a single member parses.
- `Time.of(hour = .., minute = ..[, second = ..][, millisecond = ..])`: `second` and `millisecond` are optional numeric parameters.
- JQL equality operators are `==` and `!=` only; `=` and `<>` are not tokens. Operator precedence from loosest to tightest: `implies`, `or`, `xor`, `and`.

## Queries with parameters

A static JSL query with parameters generates an unmapped parameter transfer object named `_<EntityOrContainer>_<Query>Parameters`, annotated `OriginalSource` and `ParameterObject`. The query appears on the default transfer object as a transfer attribute (primitive result) or transfer object relation (entity result); entity-less queries become static data or a static navigation.

## Actor metadata generated from JSL and ESM

Every actor gets a `_metadata` operation (`GET_METADATA`) returning `_MetadataFor<Actor>`, and an actor with a principal also a `_principal` operation. `_MetadataSecurityFor<Actor>` is an unmapped type with the attributes `name`, `openIdConfigurationUrl`, `issuer`, `authEndpoint`, `tokenEndpoint`, `logoutEndpoint`, `clientId`, `clientBaseUrl` and `defaultScopes` (strings up to 8192 characters; `name`, `clientId` and `defaultScopes` are required). A claim attribute is generated when `identity` and `claim` are both present.

## Editor Support for JSL

JSL files (`.jsl`) get IDE support from the JUDO JSL VS Code extension (activates on `onLanguage:jsl`, language id `jsl`, grammar scope `source.jsl`, embeds a Java language server started over LSP stdio; packaged as `jsl-language.vsix`) and from the `judo-jsl-tmbundle` TextMate bundle for VS Code, JetBrains and Sublime. In IntelliJ install the TextMate Bundles plugin, point it at the cloned bundle directory and associate `*.jsl`.
