# Grade kb test answers (blind)

Input: {WORK}/blind.jsonl: one answer per line {key, task, answer}. Checklists: {TASKS} (`check` per task).

For every line, score each checklist point: 1 = stated correctly, 0.5 = partly or vaguely, 0 = missing or wrong. Also count "wrong": statements in the answer that contradict the checklist or are clearly false about the platform. Judge only against the checklist and plain correctness; do not use any tool except reading these two files.

Write {WORK}/grades.jsonl: {"key","points":[..],"score":<sum/len>,"wrong":<n>}. Every input line gets one output line. Three-line answer.
