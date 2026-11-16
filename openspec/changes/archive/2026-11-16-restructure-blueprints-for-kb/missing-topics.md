# Missing topics

Knowledge the catalog is missing that is **not** in `knowledge-gaps-report.md`.
Collected during review and in discussion with developers.

How to add one: write a `## <topic in one line>` heading, then one sentence on what is
missing. Optional fields: `- **Target:**` (agent-docs, best-practices, model-blueprints, other),
`- **Decision:**`, `- **Proposed by:**`, and a `**Notes:**` paragraph.
The review app (`python3 target/review-app/server.py`) reads and writes this file.
