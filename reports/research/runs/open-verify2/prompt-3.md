Working directory: /Users/bmiller/Projects/judo-blueprint. Edit no catalog file; write only your output file and scratch files under /tmp.

Input: target/open-verify2/part-3.jsonl. Each item was left OPEN twice. `why_left_open` is the earlier excuse. Your job is to SETTLE each item. "Needs a running app" and "not in source" are not accepted: the framework is entirely in judo-ng.

Routes, use as many as needed (no lookup limit):
1. Code: target/judo-ng-read/wt/<group>__<repo>/ is on the latest develop (read-only). Trace the full chain: ESM metamodel (models__judo-meta-esm), transformations (runtime__judo-tatami-*: esm2psm, psm2asm, esm2ui, asm2rdbms), generators and templates (template__*/**/*.hbs, including judo-ui-react-template), runtime (dispatcher, DAO, security, validation), maven plugins, and judo.sh.hbs.
2. Reproduce: copy tests/fixtures/Sandbox.model to /tmp/ov3/, then use java -jar target/judo-cli.jar -m /tmp/ov3/Sandbox.model (create, update, validate --strict, transform -o /tmp/ov3/out, fill, ...). Inspect the derived models (PSM, ASM, UI XMI) to see what the generator gets. Never touch a repo model or the webshop.
3. App evidence: ~/Projects/webshop-test (read-only): its generated sources (application/frontend-react/**, application/app/**), logs and model show what the generator really produced.

For EVERY item write one JSON line to target/open-verify2/out-3.jsonl:
{"work":..,"id":..,"status":"proposed|already-correct|rejected|not-platform","file":"catalog/<path>.md","heading":..,"replaces":"<exact current sentence or empty>","proposed":"<exact new text>","evidence":"<repo>/<path>:<line> | cli:<command and result> | app:<path>"}
- Generic wording only: no project, client or domain names; use <app>, <Entity>, <Actor>.
- If the code shows a platform bug, that is a settled fact. Document it as a known issue with the evidence and the workaround.
- There is NO open status. Everything about the framework is in judo-ng: the metamodel, transformations, generators, templates, runtime, plugins and judo.sh. Every item can be settled from that code. Keep tracing until you find the answer.
kb_search to find catalog sections; read short files whole. Reply with counts per status.
