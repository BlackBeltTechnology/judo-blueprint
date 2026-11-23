# Session miner task

You mine ONE chunk of a build session: a pi agent that built a JUDO application in /Users/bmiller/Projects/webshop-test using this catalog as its knowledge base, prompted round by round by an orchestrator. Your chunk is a compact text dump: `[N] USER/ASSISTANT/CALL/TOOLRESULT: ...`, N = session JSONL line.

Read your WHOLE chunk (use Read with offset/limit, ~400 lines at a time; it is large, do not skip). Also use, read-only:
- /Users/bmiller/Projects/webshop-test/GAPS.md, TRACE.md, REPORT-*.md, git log (`git -C /Users/bmiller/Projects/webshop-test log --stat`)
- /Users/bmiller/Projects/judo-blueprint/target/webshop-orchestration-log.md (orchestrator QC notes, if any)
- the catalog via kb_search / kb_get (NEVER the `kb` CLI) when you need to say what the catalog says.

Extract EVERY item of these types from your chunk:
1. **issue**: any problem hit (error, wrong behaviour, bug, missing doc, wrong doc, failed approach, workaround, user/orchestrator correction, builder mistake, slow step).
2. **platform-claim**: any statement the builder made about how JUDO works ("X is not documented", "the CLI cannot Y", "the generator sorts Z") that a catalog entry should or should not contain.
3. **decision**: a design choice with its reason (and catalog entries cited).
4. **built**: one line per function ID built/fixed (F##/S##), with catalog paths used.

Write ONE file: /Users/bmiller/Projects/judo-blueprint/target/gap-analysis-r16/miners/c18.jsonl, one JSON object per line:
{"id":"c18-NN","type":"issue|platform-claim|decision|built","round":"R7","functions":["F14"],
 "what":"one or two plain sentences","why":"root cause as stated or evident","kind":"catalog-gap|catalog-wrong|platform-bug|platform-limit|cli-tool|agent-tool|builder-mistake|test-design|orchestrator-process|none",
 "workaround":"what was done, or null","catalog_paths":["catalog/..."],"gaps_ref":"R7-5 or GAPS item number or null",
 "evidence":["session:L1234","app:path/file.ts:12","commit:abc1234","gaps:R7-5"],
 "proposed":"add-catalog|modify-catalog|platform-ticket|tool-fix|one-off|none","proposed_target":"catalog path or tool name or null",
 "confidence":"high|medium|low"}
Rules: evidence must include at least one `session:L<n>` from your chunk. Do not invent; if unsure, confidence low. Merge exact duplicates inside your chunk; keep one item per distinct problem. Plain language, no em dashes. Do NOT edit anything except your output file. No git commands that change state.
Final answer: three lines only (counts per type and kind; the 3 most important items; anything not done). Detail goes in your output file.

Your chunk: /Users/bmiller/Projects/judo-blueprint/target/gap-analysis-r16/chunks/c18_L10170-10582.txt
Also record every kb problem (kb_search with no useful hit, kb_get failure or empty body, wrong heading path, reading catalog files from disk because kb did not give the section) as kind "agent-tool" with the exact query/call and session line. Record every JUDO CLI problem as kind "cli-tool".
