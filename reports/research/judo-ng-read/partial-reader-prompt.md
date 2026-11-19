You are re-reading ONLY the files a previous reader marked PARTIAL in batch {ID}.

Context: judo-ng is the operator's own company codebase (BlackBelt Technology's JUDO platform), used to write internal developer documentation. You are READ-ONLY on the source. You may update ONE file: out/{ID}.json.

- BATCH: /Users/bmiller/Projects/judo-blueprint/target/judo-ng-read/batches/{ID}.json
- EXISTING OUTPUT: /Users/bmiller/Projects/judo-blueprint/target/judo-ng-read/out/{ID}.json
- The existing output already has one entry per item. The PARTIAL files are listed in the existing output under entries whose "purpose" starts with "PARTIAL".
- For EACH PARTIAL entry: open the real file in the worktree and read it COMPLETELY (in chunks with offset/limit if large). Rewrite that entry so it is complete: accurate purpose, symbols that literally appear, and facts with real line evidence (repo-name@sha:path:line). Replace the "PARTIAL:" prefix in purpose with a normal one.
- Do not touch entries that are not PARTIAL.
- Checker: python3 /Users/bmiller/Projects/judo-blueprint/target/judo-ng-read/check_batch.py {ID}
- When done, run the checker; fix until ACCEPT.
- Reply with exactly one line: "{ID} ACCEPT <n> partial files completed, <f> facts"
