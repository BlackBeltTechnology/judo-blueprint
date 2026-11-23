#!/bin/bash
# make-variant.sh <name> <transforms>  ->  $KBAB_TMP/<name>: copy of catalog/, transforms (variants.py), own kb config, fresh index, static eval
set -e; source "$(dirname "$0")/env.sh"
N=$1; V=$2; D=$KBAB_TMP/$N
rm -rf "$D"; mkdir -p "$D/.pi/dashboard"
rsync -a "$ROOT/catalog" "$D/"
python3 "$HERE/variants.py" "$D/catalog" "$V"
printf '{"sources":[{"kind":"filesystem","ref":".","priority":0}],"include":["catalog/**/*.md"],"dbPath":".pi/dashboard/kb/index.db"}' > "$D/.pi/dashboard/knowledge_base.json"
(cd "$D" && kbcli index >/dev/null 2>"$D/index.err") || { cat "$D/index.err"; exit 1; }
g=$(cd "$D" && kbcli eval --golden "$ROOT/tests/golden/kb-golden.json" --limit 10 --no-reindex 2>&1 | tail -1)
h=$(cd "$D" && kbcli eval --golden "$ROOT/tests/golden/kb-holdout.json" --limit 10 --no-reindex 2>&1 | tail -1)
echo "{\"variant\":\"$N\",\"golden\":$g,\"holdout\":$h}" | tee "$D/eval.json"
