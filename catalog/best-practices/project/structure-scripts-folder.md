---
id: structure-scripts-folder
title: Project Scripts Folder Outside the Generated Build
description: "Keep project utility scripts (i18n checks, data and workbook fixes, report comparisons, cloud helpers) in one root scripts/ folder grouped by topic, with pinned dependencies and a docstring header, never inside generated application modules or loose at the root."
aliases: [scripts folder, utility scripts, tooling scripts, helper scripts]
keywords: [scripts, python, requirements.txt, i18n, data fix, workbook, apps script, gcloud, schema migrate, docstring]
tags: ["domain:project", "layer:backend", "project:rackinspect", "project:mlszksz-platform", "project:park-here", "status:emerging"]
category: structure
status: emerging
projects: [rackinspect, mlszksz-platform, park-here]
evidence: ["rackinspect:scripts/", "rackinspect:apps-script/", "mlszksz-platform:scripts/extract-i18n-keys.py", "park-here:src/scripts/", "park-here:src/schema-migrate.sh"]
alternatives: []
fragment: "none: infrastructure"
first_seen: 2026-11-12
last_updated: 2026-11-12
---
## Intent

Projects collect helper scripts: locale key checks, master-data workbook fixes, report comparisons, cloud console helpers, schema migration shortcuts. Give them one home outside the generated build so they are found, versioned with their dependencies and not mistaken for platform tooling.

## Practice

### Platform base

The platform's own entry points are the root build script and Maven ([build process](../../agent-docs/deployment/build-process.md)); the generated `application/` modules are regenerated from the model and protected only file by file through `.generator-ignore`. Project scripts are not part of either. Whether the template generates a root `scripts/` folder: *verify* (the clean template baseline project has none).

### Practice notes: one folder, grouped by topic

```
scripts/
  requirements.txt           # pinned Python dependencies for all scripts
  i18n/                      # locale key sets, glossaries, coverage checks
  <topic>/                   # one subfolder per feature area
  <single-purpose>.py        # one-off data or report scripts
```

- Group by topic once there are more than a handful of scripts (for example `i18n/`, `ticketing/`).
- Pin the dependencies in `scripts/requirements.txt` (or a lock file) so a script runs the same months later.
- Start every script with a header that says what it does, why, what it changes and how to run it from the repository root. A workbook script in one project explains why it edits the sheet XML directly instead of round-tripping through a spreadsheet library.
- Share definitions between scripts instead of copying them: One project keeps one key-set predicate and one glossary file in `scripts/i18n/` and imports them from every check.
- Scripts that run inside another product (spreadsheet macros, for example Google Apps Script) get their own folder named after that runtime, such as `apps-script/`, with a note on which document they belong to.
- Environment operator scripts belong in the environments folder, not here; see [[structure-environments-folder]].
- Locale maintenance scripts that must sit next to the locale files (as in [[hungarian-full-localization]]) can stay there; everything else moves to `scripts/`.

### Keep out of scripts

- Credentials and hard-coded connection strings: read them from the environment. A root `schema-migrate.sh` in one project passed a database password on the command line.
- Anything the build needs: wire it into Maven or a generator override instead.

## Rationale

- One folder is easy to find, to review and to exclude from the generator.
- Pinned dependencies and headers make scripts runnable by someone who did not write them.
- Cost: scripts are not covered by the application build or tests; checks that matter should move into the test suite or CI.

## Example

- One project: `scripts/` with `requirements.txt`, `i18n/` (key predicate, glossary JSON, label assertions), `ticketing/`, and single-purpose scripts for workbook fixes and report comparison; Apps Script code for a report in `apps-script/`.
- Another project: `scripts/extract-i18n-keys.py` compares translation keys used in custom frontend code with the override fragments and the locale files; `scripts/cleanup-extra-fragments.py` removes dead keys.
- A third project: `scripts/` with a cloud console helper, but a schema migration shell script left at the root.

## When to avoid

- A script used by exactly one environment or one module lives next to it (an environment's `manage.sh`, a frontend package script).

## Related

- [[structure-repository-root-layout]] — the rest of the root layout
- [[structure-translation-sources]] — the translation sources the i18n scripts read
- [[hungarian-full-localization]] — locale maintenance scripts next to the locale files
