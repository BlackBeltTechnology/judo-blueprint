## 1. Remove fragments

- [x] 1.1 Delete `fragments/`, `judo-model-mermaid/scripts/check` and `references/fragments.md`; reduce `render` to `--model/--scope`.
- [x] 1.2 Strip `fragment:`/`diagram:` frontmatter and `mermaid:generated` markers from the catalog; diagram text unchanged.
- [x] 1.3 `entry-lint` rejects the retired keys; `spec-check` drops the sandbox rule.
- [x] 1.4 `check-all` drops the fragments gate and `--no-sandbox`; CI drops the sandbox job.
- [x] 1.5 Update skills, references, the sweep author agent, README and AGENTS.md; delete the one-off `pass-a` migration script.
- [x] 1.6 `check-all` passes.
