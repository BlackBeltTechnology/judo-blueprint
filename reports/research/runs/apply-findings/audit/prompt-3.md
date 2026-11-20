# Audit "not platform" triage verdicts (judo-ng read findings)

Working directory: /Users/bmiller/Projects/judo-blueprint. Edit nothing except your output file.

Input: target/apply-findings/audit/part-3.jsonl. Each row is a judo-ng finding (a judo-ng doc/spec/index claim that contradicts the code, or a spec-vs-code bug): id, kind, repo, path (judo-ng file:line), claim, fact (what the code does), triage_reason. A triage agent marked every row "not platform" (not relevant to application developers). Audit that verdict; do not trust it.

Question per row: does the FACT describe behaviour an application developer meets when modelling, generating, building, running or testing a JUDO application? That includes: ESM metamodel rules and defaults, validation messages, transformation results visible in generated code or schema, generator/template output (React, Java, REST, SQL, Liquibase), runtime behaviour (REST, DAO, security, interceptors, transactions, errors), maven plugins, judo.sh, the CLI, testkit. NOT platform: IDE/Eclipse editor tooling, internal APIs no app touches, CI/release tooling, archived or proposed change texts that describe nothing shipped, test code of judo-ng itself, purely internal refactoring details.

For each row decide, quickly (most rows are judged from claim+fact; open the judo-ng file under target/judo-ng-read/wt/<group>__<repo>/ only when needed):
- "confirm": not platform (give the category).
- "platform": an app developer meets it. Then kb_search the catalog for it: if the catalog already states it correctly, "platform-covered" with path+heading; if missing or wrong, "platform-gap" with: file (catalog/agent-docs/<best file>.md), heading, proposed (one or two generic sentences: <app>, <Entity>, <Actor>; the fact plus the workaround if it is a defect), evidence (judo-ng path:line, re-checked on latest develop).

Write one JSON line per input row to target/apply-findings/audit/out-3.jsonl:
{"id","verdict":"confirm|platform-covered|platform-gap","category" (for confirm),"file","heading","proposed","evidence","note"}
Every input row gets exactly one line. Plain language. Final answer: counts per verdict (three lines).
