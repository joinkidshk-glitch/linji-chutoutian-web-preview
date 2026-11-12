#!/bin/bash
# Post-rebase drive spot-check on main 632e371 (v141+v144+v143).
# Backs up the 35/35 cum, runs 3 representative phases with a FRESH cum, restores the backup.
cd ~/workspace/linji-work138
PY=/home/hatch/pwenv49/bin/python
cp qa138/drive138_cum.json qa138/drive138_cum_35of35.bak.json
rm -f qa138/drive138_cum.json
echo "===== SPOTCHECK @ $(date +%H:%M:%S) ====="
$PY qa138/drive138.py ~/workspace/linji-work138 branch "e_lok_beats,e_chung_heart,s_fen_intro" 2>&1 | tail -14
echo "----- spotcheck exit: $? @ $(date +%H:%M:%S) -----"
cp qa138/drive138_cum_35of35.bak.json qa138/drive138_cum.json
python3 -c "
import json
c=json.load(open('qa138/drive138_cum.json',encoding='utf-8'))
print('restored cum seen:', len(c['seen']))"
