# Grade kb test answers (blind)

Input: /Users/bmiller/Projects/judo-blueprint/target/kbab/blind6.jsonl: one answer per line {key, task, answer}. Checklists: /Users/bmiller/Projects/judo-blueprint/target/kbab/tasks.json (`check` per task).

For every line, score each checklist point: 1 = stated correctly, 0.5 = partly or vaguely, 0 = missing or wrong. Also count "wrong": statements in the answer that contradict the checklist or are clearly false about the platform. Judge only against the checklist and plain correctness; do not use any tool except reading these two files.

Write /Users/bmiller/Projects/judo-blueprint/target/kbab/grades6.jsonl: {"key","points":[..],"score":<sum/len>,"wrong":<n>}. Every input line gets one output line. Three-line answer.
