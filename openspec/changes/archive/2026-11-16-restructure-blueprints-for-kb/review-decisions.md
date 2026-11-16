# Review decisions

Generated 2026-11-06 13:11 from `review-state.json`.

## Missing knowledge (`openspec/changes/restructure-blueprints-for-kb/knowledge-gaps-report.md`)

### 1. Summary
Topic decision: **accept**
- **accept** · 324 validated gaps in 72 topics.
- **accept** · The biggest holes are platform runtime behaviour that developers had to dig for:
- **accept** · The model languages have no reference.
- **accept** · Model changes break the frontend in ways nobody documented.
- **accept** · Configuration that every production app needs is absent:
- **accept** · Testing knowledge is thin.
- **accept** · Domain knowledge:
- **accept** · agent-docs
- **accept** · best-practices
- **accept** · model-blueprints
- **accept** · cli
- **accept** · High:
- **accept** · Medium:
- **accept** · Low:

### Scope decisions needed
- **reject** · JSL (textual model language);
- **accept** · Spring Boot runtime;
- **reject** · Flutter frontend.

### How to read an item
Topic decision: **accept**
- **accept** · the priority and its evidence;
- **accept** · where the knowledge should go;
- **accept** · what the catalog has today, when there is a partial mention;
- **accept** · the facts to add.

### Method
Topic decision: **accept**
- **accept** · Mining.
- **accept** · Validation.
- **accept** · Grouping.

### Limits
Topic decision: **accept**
- **accept** · Session counts come from the miners and may overcount.
- **accept** · The session corpus is two developers on one project.
- **accept** · The fact text is the miner's wording; only the sampled claims were checked against source line by line.
- **accept** · Confirm each topic against source when you write the entry, as the catalog's own validation rule requires.

## Catalog updates (`openspec/changes/restructure-blueprints-for-kb/catalog-update-report.md`)

