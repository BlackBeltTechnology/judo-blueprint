#!/bin/bash
# run-session.sh <variant> <taskId> <rep>  -> spawns a session in /tmp/kbab/<variant>, waits idle, archives; prints "variant task rep sessionId"
V=$1; T=$2; R=$3; ROOT=/Users/bmiller/Projects/judo-blueprint
BUS="npx tsx /Users/bmiller/Projects/Pi-Packages/pi-agent-dashboard/packages/extension/.pi/skills/pi-dashboard/scripts/dashboard-bus.ts"
Q=$(python3 -c "import json,sys;print(next(t['prompt'] for t in json.load(open('$ROOT/target/kbab/tasks.json')) if t['id']=='$T'))")
P="Answer a question about the JUDO platform from the knowledge base. Use ONLY the kb_search and kb_get tools: no file reads, no bash, no other tools. When you have enough, write the answer (concise, every point backed) and list the sources you used (path and heading). Question: $Q"
cd $ROOT/target/kbab
OUT=$($BUS spawn /tmp/kbab/$V --prompt "$P" --model anthropic/claude-sonnet-5-5 --thinking medium 2>&1)
ID=$(echo "$OUT" | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -1)
[ -z "$ID" ] && { echo "SPAWN FAILED $V $T $R: $OUT" >&2; exit 1; }
sleep 20; $BUS until $ID idle >/dev/null 2>&1
$BUS archive $ID >/dev/null 2>&1
echo "$V $T $R $ID" | tee -a $ROOT/target/kbab/runs.txt
