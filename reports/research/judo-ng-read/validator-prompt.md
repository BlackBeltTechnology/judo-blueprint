Context: judo-ng is the operator's own company codebase (BlackBelt Technology's JUDO platform). A reader agent summarised one batch of its files to write internal developer documentation, and reported where the existing DOX AGENTS.md rows disagree with the code. Your job is to check ONLY those disagreements, quickly. You are READ-ONLY on the source. You may create ONE file: your validation JSON.

BATCH: /Users/bmiller/Projects/judo-blueprint/target/judo-ng-read/batches/{ID}.json   (worktree, items)
READER OUTPUT: /Users/bmiller/Projects/judo-blueprint/target/judo-ng-read/out/{ID}.json
YOUR OUTPUT: /Users/bmiller/Projects/judo-blueprint/target/judo-ng-read/out/{ID}.validate.json

Steps:
1. Take every entry whose dox_check starts with "disagrees", every item in the top-level "doc_conflicts" list, and every item in "suspected_bugs" (the lists may be missing). Ignore everything else. For a doc conflict, the "row" is the doc claim. For a suspected bug, decide "confirmed" (the code really is wrong) or "reader wrong" (it is intended or correct), and give the reason.
2. For each one, find the DOX row it refers to (the AGENTS.md row for that file in the worktree) and open the real file. Decide:
   - "confirmed": the row states something false, and the reader's correction is true (cited line correct within ±5 lines).
   - "omission": the row is true but incomplete. The label should be "agrees; omits: ...".
   - "reader wrong": the row is actually true, or the reader's correction is false.
   - "correction imprecise": the row is false, but the reader's correction is itself wrong or imprecise. Give the right one.
3. Check only what is needed to decide. Do not re-read the batch or check other facts.

Write the JSON file:
{"batch": "{ID}", "mode": "disagreements", "by_type": {"dox": n, "doc_conflict": n, "bug": n}, "checked": n, "confirmed": n, "omission": n, "reader_wrong": n, "imprecise": n,
 "entries_ok": n, "facts_checked": n, "facts_wrong": n, "verdict": "pass|fail",
 "issues": [{"type": "dox|doc_conflict|bug", "path": "...", "problem": "confirmed | omission | reader wrong | correction imprecise",
             "detail": "what the row says vs what the code does", "correct": "what is actually true, with path:line"}]}
Record EVERY checked disagreement in issues, including confirmed ones. Set entries_ok = confirmed + omission, facts_checked = checked, facts_wrong = reader_wrong + imprecise.
Verdict "pass" if reader_wrong + imprecise <= 1 and they are at most a quarter of the checked disagreements (always pass when checked <= 1 and it is not "reader wrong"). Otherwise "fail".
Reply with exactly one line: "{ID} pass|fail <confirmed> confirmed, <omission> omission, <reader_wrong> reader wrong, <imprecise> imprecise of <checked>".
