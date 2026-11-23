Context: judo-ng is the operator's own company codebase (BlackBelt Technology's JUDO platform). The operator is a maintainer with access to these repositories. This task writes internal developer documentation for the team's own product: it summarises what each file does, so the team's agent-docs and best practices are accurate.

You are reading part of the JUDO platform source (judo-ng) to build that documentation. You are READ-ONLY on the source. You may create ONE file: your output JSON.

BATCH: /Users/bmiller/Projects/judo-blueprint/target/judo-ng-read/batches/{ID}.json
It contains: repo, ref, sha, worktree (absolute path of a clean checkout), items = list of [kind, path] (path relative to the worktree).
OUTPUT: /Users/bmiller/Projects/judo-blueprint/target/judo-ng-read/out/{ID}.json
CHECKER: python3 /Users/bmiller/Projects/judo-blueprint/target/judo-ng-read/check_batch.py {ID}

How to read each item, by kind:
- "src": source with NO DOX description. Read the whole file.
- "dox": source described in a DOX AGENTS.md (in its folder or an ancestor folder). Read that AGENTS.md row, then open the source and confirm the row. Set "dox_check" to one of:
  "agrees" (everything the row says is true);
  "agrees; omits: <important public behaviour/API the row leaves out>" (true but incomplete);
  "disagrees: <what the row states that is FALSE, with the correct value>" (only for a false statement, never for an omission).
  "no row" if no AGENTS.md row describes this file (do not write "agrees" then).
- "doc": documentation (AGENTS.md, SKILL.md, README, openspec spec/design/proposal, .adoc, .md). Read it fully.

For EVERY item write one entry. Do not skip any item, and do not summarise several files in one entry:
{"path": "<item path>", "kind": "src|dox|doc",
 "purpose": "one or two sentences: what this file is / does",
 "symbols": ["identifiers that literally appear in the file: classes, interfaces, methods, constants, EClasses, template names, config keys, commands"],
 "facts": [ {"type": "api|extension-point|config|command|naming-convention|behaviour|constraint|generated-output|deprecation",
             "text": "precise fact a JUDO application developer or agent-doc writer needs",
             "evidence": "<repo-name>@<sha>:<path>:<line>"} ],
 "dox_check": "agrees | disagrees: ... (only for kind dox)"}
- <repo-name> is the last segment of the repo (e.g. judo-runtime-core), <sha> is the batch sha, <path> is relative to the worktree, <line> is a real line number in that file.
- Facts: only what a developer building a JUDO application, or someone writing JUDO agent-docs, needs: public/extension APIs and their exact signatures, OSGi properties, config keys and env vars, CLI/judo.sh/Maven commands and options, generator naming conventions and output paths, hook/interface keys, validation rules, runtime behaviour, deprecations. 0–8 facts per file; internal plumbing can have 0.
- Get line numbers with: grep -n "<symbol>" "<worktree>/<path>"   (never guess them). Cite the line where the rule or symbol itself is, not a nearby one.
- A script already extracts every EVL rule (name, severity, guard, check, message) exactly, so do NOT list every EVL rule. For an EVL file, give its purpose and up to 8 facts about notable rules (cross-element rules, surprising guards, rules app developers hit often).
- Validation rules (EVL, Java validators): always say whether a rule is an ERROR (EVL `constraint`) or a WARNING (EVL `critique`), and give its name, e.g. "critique AbstractOperationHasNoBody (warning): ...". Never call a critique a constraint.
- Never generalise ("every method ...", "all X ...") unless you checked every case.

Two extra lists (top level, may be empty):
- "doc_conflicts": any statement in a doc in this batch (agent-docs/*.md, SKILL.md, README, INSTALL.md, openspec spec/design, .adoc) that contradicts the code. For a doc, check its key claims (signatures, class/method names, config keys, commands, ordering, defaults) against the code with grep. Each: {"doc": "<path>:<line>", "claim": "what the doc says", "code": "what the code actually does", "evidence": "<repo-name>@<sha>:<path>:<line>"}.
- "suspected_bugs": code that looks wrong (inverted condition, wrong variable, ignored value, copy-paste error). Each: {"where": "<repo-name>@<sha>:<path>:<line>", "what": "what the code does", "expected": "what it most likely should do"}. Only list what you actually see in the code.
  Known NON-issues (do not report): `${java.version}` in a POM (Maven resolves it from the JVM); the `release-judong` profile pointing its release repository at the snapshots URL (deliberate in every judo-ng repo); a deliberately empty EVL/validator placeholder; Handlebars `{{#each ... as |x|}}` scoping.

File format:
{"batch": "{ID}", "repo": "...", "sha": "...", "entries": [ ... one per item ... ], "doc_conflicts": [...], "suspected_bugs": [...]}

Work efficiently: use grep -n to locate symbols and line numbers. Large files (ecore, EVL, big classes, templates) must be read COMPLETELY, in chunks with offset/limit. Never judge a file from its header or from grep counts alone. If you cannot finish a file, say so in its purpose ("PARTIAL: read lines 1-N") instead of claiming it is complete.
You run unattended: nobody will answer questions. Never stop to ask or to offer options. Always finish the whole batch and write the output file. If you truly cannot finish a file, mark it PARTIAL and continue with the next one.
When done, run the CHECKER. If it prints REJECT, fix the listed problems and re-run until it prints ACCEPT.
Reply with exactly one line: "{ID} ACCEPT <n> entries, <f> facts, dox disagreements: <k>, doc conflicts: <c>, suspected bugs: <b>", or "{ID} REJECT <reason>".
