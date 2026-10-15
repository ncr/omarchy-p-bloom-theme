#!/bin/bash
# Render the release matrix one set at a time, at nice 18 (heavy; one pipeline at a time).
#   tools/run_matrix.sh                 every sheet in every profile and level; resumable: a rerun skips sets whose
#                                       audit.json is newer than the run's start marker and lists all 42 sheets
#   tools/run_matrix.sh o02,b13,c042    only these sheets, in every profile and level (a fix to a few wallpapers);
#                                       their entries are merged into each set's existing audit.json
# The two 5K masters are re-accepted (docs/collection/native-masters.json); review them before publishing.
cd "$(dirname "$0")/.."
ONLY=$1
mkdir -p dist
LOG=dist/matrix-$(date +%F)${ONLY:+-only}.log
MARK=dist/.matrix-started
[ -z "$ONLY" ] && [ ! -f $MARK ] && touch $MARK
PROFILES=$(python3 -c "import sys; sys.path.insert(0,'tools'); import aspect_layout as A; print(' '.join([p[0] for p in A.MATRIX]+[p[0] for p in A.MASTERS]))")
for level in default muted vivid; do
  for p in $PROFILES; do
    sid=$p; [ $level != default ] && sid=$p-$level
    a=dist/wallpaper-sets/$sid/audit.json
    if [ -z "$ONLY" ] && [ -f $a ] && [ $a -nt $MARK ] && python3 -c "import json,sys; sys.exit(0 if len(json.load(open('$a'))['sheets'])==42 else 1)"; then echo "skip $sid" >> $LOG; continue; fi
    jobs=2; case $p in 32x9-2160p|64x27-2160p|16x10-2400p|16x9-2880p) jobs=1;; esac
    echo "=== $sid (jobs $jobs) $(date +%T)" >> $LOG
    accept=; [ $level = default ] && case $p in 16x9-2880p|64x27-2160p) accept=--accept-masters;; esac
    nice -n 18 python3 tools/render_wallpaper_sets.py --profile $p --level $level --jobs $jobs $accept ${ONLY:+--only $ONLY} >> $LOG 2>&1 || echo "FAILED $sid" >> $LOG
  done
done
[ -z "$ONLY" ] && rm -f $MARK
echo "=== MATRIX DONE $(date +%T)" >> $LOG
