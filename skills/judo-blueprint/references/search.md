# Searching the catalog

## Queries that work

- **Use domain words, not JUDO class names.** "approval workflow", "audit log", "guarded delete", "invitation with token". Every entry carries `aliases` and `keywords` for this.
- **Add the layer** when you know it: "interceptor read tracking backend", "table row highlighting frontend".
- **Ask for the rule, then the pattern.** "custom operation interceptor scope" finds the agent-docs rule; "audit event entity" finds the blueprint.
- **Two short queries beat one long query.** BM25 ranks by term match; long questions dilute it.

## Filter out index rows

For a content question, pass `doc_type: "doc"` to `kb_search`. It drops the directory `AGENTS.md` index rows, which otherwise take top slots. On the catalog test sets this raises top-5 hits from 92% to 97% (tuned set) and from 80% to 87% (held-out set). Leave it unset when you are looking for *which file* covers a topic.

## Reading results

- Each hit is `<path> :: <heading>`. A hit on `AGENTS.md` is a directory index: its rows name the files, so open the file the row points to.
- `(+N more sections)` means the same file matched in several places. Read it with `kb_get <path>`, then `kb_get <path> section=<heading path>` for one section.
- A large doc has a companion `<name>.agent.md` (a condensed map with the same `##` headings). Read it first, then `kb_get` only the section you need from the full doc.
- `kb_get` needs the **full** heading path (from `format: "json"` output, `headingPath`), not just the last heading.

## Entry facets

Entries are tagged in frontmatter `tags`:

| Facet | Values |
|---|---|
| `domain:` | model, backend, frontend, project (entries); model, backend, frontend, deployment, testing (agent-docs) |
| `layer:` | which layers the entry touches |
| `project:` | the projects the pattern was seen in |
| `status:` | `platform` (agent-docs: platform facts), `established` (4+ projects), `emerging` (2–3), `single-project` (1) |

Prefer `status:established`. A `single-project` entry was seen in one project only; read its *When to avoid* section before adopting it.

## When nothing fits

Search the agent-docs area directly ("frontend hooks", "data access guide"). If the platform does not cover it either, say so and do not invent a platform rule.
