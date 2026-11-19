---
title: Frontend Development Guide
description: Frontend development guide for JUDO React applications. Covers generated structure, checksum protection, .generator-ignore, template overrides, hooks, theming and i18n.
aliases: [react frontend guide, customize generated frontend, frontend checksum error, where to put react customizations, frontend hooks overview]
keywords: [.generator-ignore, .generated-files, src/custom, application-customizer.tsx, ui-react.yaml, generator-overrides, judo-ui-react-template, customize, extra-routes.tsx, palette.ts]
tags: [domain:frontend, layer:frontend, status:platform]
---

# Frontend Development Guide

## Overview

The React frontend in <app> is generated from the ESM and UI models using JUDO generators. Customization is achieved through a hook system rather than direct code modification.

**Note**: Throughout this documentation:
- `<app>` refers to the application name from `judo.properties` (app_name property)
- `[actor_fqn]` represents the modeled actor's fully qualified name (without the model name prefix)
  - Generated from ESM model: `[model_name]::[namespace]::[ActorName]` → `[namespace]__[actor_name]` (lowercased, `::` replaced with `_`)
  - Example: Model name `<Model>` (lowercased: `<model>`), Actor FQN `<model>::service::Admin` → actor path becomes `service__admin`
- Frontend module naming pattern: `<app>__[actor_fqn]`
  - Double underscore (`__`) separates app name from actor path
  - Single underscores (`_`) replace namespace separators (`::`) within the actor path
  - Full example: `application/frontend-react/<app>__[actor_fqn]/` (e.g., `<app>__service__admin/`)

## Key Concepts

- **Model-Driven Generation**: The entire frontend is generated from the ESM and UI models. This ensures consistency and reduces boilerplate code.
- **Hook System**: Customizations are achieved through a hook system based on Pandino. Instead of editing generated code, you register custom hooks to override or extend functionality.
- **Checksum Protection**: To prevent accidental edits to generated files, a checksum system is in place. Modifying a generated file will cause the build to fail unless it's explicitly ignored in `.generator-ignore`.
- **`.default` Files**: The generator creates `.default` scaffold files for hook registrations (under `src/custom/hooks/...`, for example `src/custom/hooks/pages/register<Page>ActionsHook.ts.default`). You copy a scaffold and drop the `.default` suffix to activate it. A hook scaffold is generated only when the matching hook flag is set in the model (for example `generateActionsHook`). `src/custom/application-customizer.tsx` itself is a plain generated file, not a `.default` scaffold.
- **Custom folder**: Custom hook code lives in `src/custom/`. `src/custom/` and its generated files are written by the React code generation in the actor module's Maven build (`./judo.sh build`), not by `./judo.sh generate`; a freshly generated module has no `src/custom/` until the first build. Hook scaffolds are generated as `.default` files under `src/custom/` (the frontend `.gitignore` ignores `*.ts.default` / `*.tsx.default`). A copy without `.default`, and any file you add yourself, is outside generator scope and needs no `.generator-ignore` entry. `src/custom/` itself is **not** gitignored: commit your custom code. The generator does write four files there without `.default` (`application-customizer.tsx`, `index.tsx`, `custom-element-types.ts`, `interfaces.ts`); if you hand-edit one of those, list it in `.generator-ignore`.

## Architecture

### Routing

The frontend uses a hash router (`createHashRouter`). Routes are in the URL fragment: pages open at `/<app-path>/#/<route>`; a direct path without the `#` is not a route. Browser tests must navigate to the hash URL.

### Generated vs Custom Code

**Generated (Do Not Edit Directly):**
- `src/containers/`, `src/pages/`, `src/dialogs/`, `src/components/`, `src/layout/`, `src/utilities/`, `src/auth/` - React containers, pages, dialogs, components and helpers
- `src/App.tsx` - Main application component
- `src/routes.tsx` - Route definitions (custom routes go in `src/extra-routes.tsx`, see below)
- API client services
- Model type definitions

**Custom Code (Edit Here):**
- `src/custom/` - Hooks and customizations
- `src/theme/` - Theme and styling customizations
- `src/custom/application-customizer.tsx` - Hook registration (a plain generated file; the `customize(context)` method is where you register Pandino services)

### Code Generation and Checksum Protection

**How Generation Works:**
1. All generated files are tracked by **checksum** in `.generated-files__[actor_fqn]` (located in the frontend module root)
2. Files NOT in `.generator-ignore` will be regenerated on `./judo.sh build` or `mvn clean install`
3. **Checksum validation**: Before overwriting, the generator checks if a file was manually edited
   - If file was edited (checksum mismatch) → ❌ **Build FAILS** with error
   - If file unchanged → ✅ File is regenerated normally

**When You Must Edit Generated Files:**

Sometimes there's no hook available for customization, and you must edit generated code directly. This is **NOT the preferred way**, but when necessary:

1. **Edit the generated file** with your changes (e.g., `src/containers/...`)
2. **Add to `.generator-ignore`** to protect it from regeneration
   ```bash
   echo "src/pages/MyCustomPage.tsx" >> .generator-ignore
   ```
3. Place the entry in `.generator-ignore` near related overrides (it's used like `.gitignore`)

See [Understanding .generator-ignore](#understanding-generator-ignore) below for the full rule.

**Handling Checksum Errors:**

If you get checksum errors due to code formatting changes (e.g., after `git checkout`, Prettier/Biomé auto-format, or dev mode changes):

```bash
# Ignore checksum errors and force regeneration (frontend module)
cd application/frontend-react/<app>__[actor_fqn]
mvn clean install -Dignore-checksums

# Or from root with judo.sh
./judo.sh build -i
```

**Checksum File Locations:**
- `.generated-files__[actor_fqn]` - In frontend module root directory
- Format: Tracks file paths and their checksums for the specific actor module

**Best Practice:** Always prefer using hooks over editing generated files. Only edit generated code when absolutely no hook exists for your use case.

## Project Structure

```
application/frontend-react/<app>__[actor_fqn]/
├── model/                              # UI model generation
│   ├── pom.xml                         # UI model generator config
│   └── target/generated-resources/
│       └── model/<app>-ui.model
├── src/
│   ├── containers/                     # ⚠️ GENERATED - DO NOT EDIT
│   ├── pages/                          # ⚠️ GENERATED
│   ├── dialogs/                        # ⚠️ GENERATED
│   ├── components/                     # ⚠️ GENERATED
│   ├── layout/ utilities/ auth/        # ⚠️ GENERATED
│   ├── extra-routes.tsx                # ✏️ extra React Router routes
│   ├── custom/                         # ✏️ CUSTOMIZATIONS HERE
│   │   ├── application-customizer.tsx  # Hook registration
│   │   ├── hooks/
│   │   ├── components/
│   │   └── hooks/**/*.default         # Hook registration scaffolds
│   ├── theme/                          # ✏️ THEME CUSTOMIZATION
│   │   └── palette.ts
│   └── App.tsx                         # Generated entry point
├── public/
│   ├── i18n/                           # Internationalization
│   │   ├── default/
│   │   ├── en-US/
│   │   └── hu-HU/
│   └── manifest.json
├── .generator-ignore                   # Exclude files from generation
├── package.json
├── vite.config.ts
└── pom.xml                             # Frontend build config
```

## Generation Process

### Build Flow

```
ESM Model (<app>.model) ⚠️ Edit with Judo Designer only
    ↓
[UI Model Generation] (application/frontend-react/model/pom.xml)
    ↓
UI Model (<app>-ui.model)
    ↓
[React Code Generation] (application/frontend-react/<app>__[actor_fqn]/pom.xml)
    ↓
Generated React Code (src/containers, src/pages, src/dialogs, ...)
    ↓
[PNPM Build] (vite)
    ↓
Frontend JAR
    ↓
[Auto-Deploy to Karaf] (when server running)
```

**Important**: The ESM model file cannot be edited directly. Use the **Judo Designer** modeling tool for all model changes. See `../model/README.md` for details.

### Generator Configuration

**UI Model Generation** (`application/frontend-react/model/pom.xml`):
```xml
<plugin>
    <groupId>hu.blackbelt.judo.tatami</groupId>
    <artifactId>judo-tatami-psm2ui-maven-plugin</artifactId>
    <!-- Transforms PSM → UI Model -->
</plugin>
```

**React Code Generation** (`application/frontend-react/<app>__[actor_fqn]/pom.xml`):
```xml
<plugin>
    <groupId>hu.blackbelt.judo</groupId>
    <artifactId>judo-ui-react-maven-plugin</artifactId>
    <!-- Generates React code from UI Model -->
</plugin>

<plugin>
    <groupId>com.github.eirslett</groupId>
    <artifactId>frontend-maven-plugin</artifactId>
    <!-- Runs pnpm install and build -->
</plugin>
```

## Understanding .generator-ignore

### One Rule

`.generator-ignore` uses `.gitignore`-style matching, scoped to generator output. Single purpose: stop the generator from re-emitting a file at path X because you hand-edited that exact generated file in place. It is **not** a "this file is custom" marker, and it is **not** needed for files the generator never produces.

Three cases:

1. **Generator emits file at path X, you hand-edit X in place.** → Add `X` to `.generator-ignore`. The only legitimate case. Examples: `src/pages/MyPage.tsx`, `src/theme/palette.ts`, or a generator-emitted stub like `src/custom/application-customizer.tsx`.
2. **`.default` rename pattern.** Generator emits `X.default` (e.g. `src/custom/application-customizer.tsx.default`). Rename to `X` once and fill in the body. Generator re-emits `X.default` next round as a reference; never touches `X`. → `X` is OUTSIDE generator scope. **No entry needed.** Do NOT add `X.default` either — you want it to keep regenerating as a reference.
3. **Brand-new hand-written file the generator never emits at that path** (new components, new helper hooks under `src/custom/...`). → OUTSIDE generator scope. **No entry needed.**

Adding purely-custom files to `.generator-ignore` is noise; remove such entries.

**Location:** `application/frontend-react/<app>__[actor_fqn]/.generator-ignore`

**Syntax:**
```
# Comments start with #

# Exact file
src/custom/application-customizer.tsx

# Wildcards
src/custom/**/*.tsx

# Directories
src/custom/

# Patterns
*.custom.tsx
**/custom-*.tsx
```

Entries are glob patterns only. `!` negation is not supported; a leading `!` is matched literally. Ignore files in parent directories also apply to the files below them.

**Common Patterns:**
```
# Ignore all customizations
src/custom/

# Ignore specific customizer
src/custom/application-customizer.tsx

# Ignore theme
src/theme/

# Ignore a specific generated file you edited by hand
src/theme/table-row-highlighting.ts
```

**Workflow:**
1. Generate code initially
2. Identify file you need to customize
3. Add to `.generator-ignore`
4. Make your changes
5. On rebuild, your changes are preserved

**Verification:**
```bash
# Check if file is ignored
grep "src/custom/application-customizer.tsx" .generator-ignore

# List all ignored files
cat .generator-ignore
```

## Generated File Headers

Every generated file contains a header that provides important metadata about how it was generated:

```
//////////////////////////////////////////////////////////////////////////////
// G E N E R A T E D    S O U R C E
// --------------------------------
// Factory expression: <actor>
// Path expression: 'src/App.tsx'
// Template name: actor/src/App.tsx
// Template file: actor/src/App.tsx.hbs
```

### Header Fields Explained

- **`Template file`**: The Handlebars template (`.hbs`) used for generation
  - Location: Inside `judo-ui-react-template` or `judo-ui-typescript-rest-template` Maven artifacts
  - Example: `actor/src/App.tsx.hbs`

- **`Template name`**: The logical name of the template
  - Used for the override mechanism
  - To override: Create file with same name in `generator-overrides/` directory

- **`Path expression`**: A SpringEL expression that determines the output file path
  - Evaluates to the actual file location
  - Example: `'src/App.tsx'` means file will be at `src/App.tsx`

- **`Factory expression`**: A SpringEL expression defining the data context
  - Determines what model elements are used to generate this file
  - Example: `<actor>` means this file is generated for each Actor in the model

### Why This Matters

1. **Override Decisions**: The template name tells you which template to override
2. **Understanding Regeneration**: Knowing the factory expression helps understand when a file is regenerated
3. **Debugging**: Path expression helps track where generated files end up
4. **Template Customization**: Template file location helps you find the original template to base overrides on

## Code Generation Templates

The JUDO platform uses two main template projects for code generation:

### 1. judo-ui-typescript-rest-template

**Purpose**: Generates TypeScript REST API client

**Generated Content:**
- Model type definitions (interfaces for entities)
- Service implementations (API calls)
- DTO transformations
- Error handling
- HTTP client configuration

**Template Technology**: Handlebars (`.hbs` files)

**Typical Generated Files:**
- `data-api/**/*.ts` - Type definitions and service interfaces
- `data-service/*.ts` - Service implementations (the typescript-rest template writes to `data-service/`)
- Axios-based HTTP clients (`data-axios` template, e.g. `accessServiceImpl`)

### 2. judo-ui-react-template

**Purpose**: Generates React frontend UI components

**Generated Content:**
- React components (pages, dialogs, forms, tables)
- Route definitions
- Navigation structure
- Internationalization scaffolding
- Theme structure
- Hook placeholders

**Template Technology**: Handlebars (`.hbs` files)

**Typical Generated Files:**
- `src/containers/**/*.tsx` - Container components (views, forms, tables; `ui-react.yaml` path `src/containers/<containerPath>/<Component>.tsx`)
- `src/pages/*.tsx` - Page components
- `src/components/**/*.tsx` - Reusable components
- `src/dialogs/**/*.tsx` - Dialog components
- `src/App.tsx` - Main application entry
- `src/routes.tsx` - Route configuration

### Template Override Process

**When to Override:**
- Hook system cannot achieve desired behavior
- Need to change generated code structure
- Want to use different libraries/patterns

**How to Override:**

1. **Identify template name** from generated file header
   ```
   Template name: actor/src/App.tsx
   ```

2. **Create override directory structure**
   ```bash
   mkdir -p generator-overrides/actor/src
   ```

3. **Create custom template** with same name
   ```bash
   # generator-overrides/actor/src/App.tsx.hbs
   # Your custom Handlebars template here
   ```

4. **Regenerate**
   ```bash
   mvn clean install
   ```

5. **Result**: Your custom template is used instead of default

**Important Notes:**
- Overrides are checked before default templates
- You must maintain the template on upgrades
- Prefer hooks over overrides for maintainability
- Document why override was necessary

### Template Variables

Each template is declared in a YAML descriptor (for example `ui-react.yaml`) with these per-template fields:

- `name`, `templateName` - logical name (used for overrides) and the `.hbs` file
- `pathExpression` - SpEL expression for the output path
- `factoryExpression` - SpEL expression iterating over model elements (one output per result)
- `applicationBased` - run once per application instead of once per factory result
- `conditionExpression` - SpEL condition; the template is skipped when false
- `copy`, `exclude`, `permission` (POSIX), `templateContext`

The template context exposes `#self`, `#application`, `#applications`, `#model`, `#template`, and `#addDebugToTemplate` (set when the `-DtemplateDebug` JVM property is present).

Override layering: a same-name template with a new `templateName`/`pathExpression` replaces the original; a `<name>.override.hbs` file decorates it (and can include the original as a partial); `exclude: true` removes it. Fragment overrides (for example the theme fragments, see [Theming](./theming.md)) work by creating a same-named file in the override directory.

Handlebars helpers are provided by the generator helper classes (for example `toSafeCamelCase`, `firstToUpperCase`). Use `-DtemplateDebug` to see the context available in a template.

Naming helpers only uppercase the first character of the joined name: `classDataName('MyPackage::MyClass', '')` generates `MyPackageMyClass`, not `MypackageMyclass`.

## Related Documentation

**Authoring vs customizing.** This skill covers **customizing the generated React frontend** (hooks, theming, i18n, overrides). The UI layout itself — Form / Table / View scaffolds on each `TransferObjectType`, the menu on each `ActorType` — is **authored in the ESM model**. For that, see the model skill's [UI Authoring Guide](../model/ui-authoring-guide.md).

### Core Topics
- [Development Workflow](./development-workflow.md) - Dev server, build, testing
- [Theming](./theming.md) - MUI theme customization
- [Internationalization](./i18n.md) - i18n setup and translations
- [Advanced Patterns](./advanced-patterns.md) - Production patterns for complex requirements

### Hook System
- [Hook System Overview](./hooks/README.md) - Understanding the hook system
- [Data Hooks](./hooks/data-hooks.md) - usePrincipal, useViewData
- [UI Hooks](./hooks/ui-hooks.md) - AppBar, Hero, Logo, Footer
- [Table Hooks](./hooks/table-hooks.md) - Row highlighting, custom columns, sidekicks
- [Action Hooks](./hooks/action-hooks.md) - Container actions, page actions, operation flows
- [Navigation and Access](./hooks/navigation-and-access.md) - Redirects, access filtering, hotkeys
- [Validation Hooks](./hooks/validation-hooks.md) - Date/DateTime validation

### Platform Topics
- [Error Handling](./error-handling.md) - 400/422/401/403/404/500 handling, fault dialog, fault i18n keys
- [Extension Points](./extension-points.md) - Extra routes, guest page, sub-themes, menu actions hook, application switcher, table state
- [Build and Deployment](./build-and-deployment.md) - Maven build modes, MUI license plan, base href, checksum handling
- [UI Model Pitfalls](./ui-model-pitfalls.md) - Model values that break the generator, renames, E2E guidance

## External Documentation

- [JUDO UI React Template](https://github.com/BlackBeltTechnology/judo-ui-react-template/blob/develop/docs/pages/01_ui_react.adoc)
- [Generator Commons](https://github.com/BlackBeltTechnology/judo-generator-commons/blob/develop/README.adoc)
- [Material-UI Documentation](https://mui.com/)
- [Vite Documentation](https://vitejs.dev/)
- [React 19 Documentation](https://react.dev/)

## Best Practices

1. **Always use hooks over direct edits** - Maintainable and upgrade-safe
2. **Add files to .generator-ignore** - Prevent overwriting custom code
3. **Keep customizations minimal** - Easier to maintain and upgrade
4. **Test after regeneration** - Ensure hooks still work
5. **Use TypeScript strictly** - Catch errors early
6. **Follow Material-UI patterns** - Consistent with generated code
7. **Leverage generated services** - Don't reimplement API calls
8. **Document custom hooks** - Help future developers

## Troubleshooting

### "File overwritten after build"
→ Add file to `.generator-ignore`

### "Build fails with checksum mismatch error"

The generated frontend is formatted after it is written: `generate-sources` runs `pnpm install` and `pnpm run format` (Biome) before the build. The formatted files no longer match their checksums, so a build can report generated files as changed. Option 3 below (`-i`) is the fix for such formatting-only changes.

```bash
# Option 1: Add the file to .generator-ignore (keep your changes)
echo "src/pages/MyPage.tsx" >> .generator-ignore
mvn clean install

# Option 2: Discard your changes (let it regenerate)
git checkout src/pages/MyPage.tsx
mvn clean install

# Option 3: Formatting-only changes - ignore checksums
mvn clean install -Dignore-checksums
# or
./judo.sh build -i
```

### "Hook not being called"
→ Check registration in `application-customizer.tsx`
→ Verify export name matches expected interface

### "Type errors after regeneration"
→ Run `pnpm install` to update type definitions
→ Check for breaking changes in generated types

## File Locations Reference

- UI Model: `application/frontend-react/model/target/generated-resources/model/<app>-ui.model`
- Generated React: `application/frontend-react/<app>__[actor_fqn]/src/` (everything outside `src/custom/` and the files you protect in `.generator-ignore`)
- Custom hooks: `application/frontend-react/<app>__[actor_fqn]/src/custom/`
- Build output: `application/frontend-react/<app>__[actor_fqn]/target/*.jar`
- Vite config: `application/frontend-react/<app>__[actor_fqn]/vite.config.ts`
