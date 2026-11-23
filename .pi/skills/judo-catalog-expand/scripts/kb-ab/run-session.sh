#!/bin/bash
# run-session.sh <variant> <taskId> <rep>  ->  new pi session in $KBAB_TMP/<variant> answering one task with kb only;
# waits until idle, archives it, appends "variant task rep sessionId" to $KBAB_WORK/runs.txt
source "$(dirname "$0")/env.sh"
V=$1; T=$2; R=$3; BUS="npx tsx $DASHBOARD_BUS"
Q=$(python3 -c "import json;print(next(t['prompt'] for t in json.load(open('$HERE/tasks.json')) if t['id']=='$T'))")
TAG="kbab-$V-$T-$R-$RANDOM$RANDOM"
P="[run $TAG] Answer a question about the JUDO platform from the knowledge base. Use ONLY the kb_search and kb_get tools: no file reads, no bash, no other tools. When you have enough, write the answer (concise, every point backed) and list the sources you used (path and heading). Question: $Q"
$BUS spawn "$KBAB_TMP/$V" --prompt "$P" --model "$KBAB_MODEL" --thinking "$KBAB_THINKING" >/dev/null 2>&1
# the id comes from the session log that carries this run's tag, never from the spawn output (sibling ids leak into it)
SD=$(sessdir "$KBAB_TMP/$V"); ID=""
for i in $(seq 1 60); do F=$(grep -l "\[run $TAG\]" "$SD"/*.jsonl 2>/dev/null | head -1)
  [ -n "$F" ] && { ID=$(basename "$F" .jsonl | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'); break; }; sleep 2; done
[ -z "$ID" ] && { echo "SPAWN FAILED $V $T $R" >&2; exit 1; }
sleep 20; $BUS until "$ID" idle >/dev/null 2>&1
$BUS archive "$ID" >/dev/null 2>&1
echo "$V $T $R $ID" | tee -a "$KBAB_WORK/runs.txt"
