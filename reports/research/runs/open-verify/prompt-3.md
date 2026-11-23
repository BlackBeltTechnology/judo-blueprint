Working directory: /Users/bmiller/Projects/judo-blueprint. Do NOT edit any file except your output file.

Input: target/open-verify/part-3.jsonl. Each line is an OPEN catalog finding: work (findings pass), id, doc (catalog file it concerns), finding (the claim or question), found (what an earlier quick check found). Quick checks could not settle these, so trace each one properly in the judo-ng code: target/judo-ng-read/wt/<group>__<repo>/ (read-only). Follow the call chain: grammar or metamodel, transformations (esm2psm, psm2asm, esm2ui, jsl2*), generators and templates (.hbs), runtime (dispatcher, DAO, interceptors, security). The CLI (java -jar target/judo-cli.jar ... --help, scratch model copies only) is also evidence. Up to about 10 lookups per item.

For EVERY input line write one JSON line to target/open-verify/out-3.jsonl:
{"work":..,"id":..,"status":"proposed|already-correct|not-platform|rejected|open","file":"catalog/<path>.md","heading":"<heading>","replaces":"<exact current sentence to correct, or empty for an addition>","proposed":"<exact new text>","evidence":"<repo>/<path>:<line>[, ...]"}
- proposed: the code settles it and the catalog must change. Generic wording (no project, client or domain names; <app>, <Entity>, <Actor>). The best file is usually "doc"; another file is fine if it fits better.
- already-correct: the catalog already states what the code does. rejected: the finding is wrong per the code. not-platform: app-specific or framework-internal.
- open: ONLY if the code really cannot answer (for example, runtime behaviour that needs a running app). Say exactly what is missing in evidence.
Use kb_search to find catalog sections, and read short files whole. At the end, check you wrote one output line per input id. Reply with counts per status.
