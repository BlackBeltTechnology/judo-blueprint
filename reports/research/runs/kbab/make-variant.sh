#!/bin/bash
# make-variant.sh <name> <variants>  -> /tmp/kbab/<name> with catalog copy, transform, kb index, eval line
set -e
N=$1; V=$2; ROOT=/Users/bmiller/Projects/judo-blueprint
KB=$(npm root -g)/@blackbelt-technology/pi-dashboard-kb-extension/node_modules/@blackbelt-technology/pi-dashboard-kb/dist/cli.js
D=/tmp/kbab/$N; rm -rf $D; mkdir -p $D/.pi/dashboard
rsync -a $ROOT/catalog $D/
python3 $ROOT/target/kbab/variants.py $D/catalog $V
printf '{"sources":[{"kind":"filesystem","ref":".","priority":0}],"include":["catalog/**/*.md"],"dbPath":".pi/dashboard/kb/index.db"}' > $D/.pi/dashboard/knowledge_base.json
(cd $D && node $KB index >/dev/null 2>$D/index.err) || { cat $D/index.err; exit 1; }
g=$(cd $D && node $KB eval --golden $ROOT/tests/golden/kb-golden.json --limit 10 --no-reindex 2>&1 | tail -1)
h=$(cd $D && node $KB eval --golden $ROOT/tests/golden/kb-holdout.json --limit 10 --no-reindex 2>&1 | tail -1)
echo "{\"variant\":\"$N\",\"golden\":$g,\"holdout\":$h}" | tee $D/eval.json
