#!/bin/bash
# Farewell-only check on v134-rebased code (spotcheck2 skipped it: target already seen via intro).
cd ~/workspace/linji-work138
PY=/home/hatch/pwenv49/bin/python
cp qa138/drive138_cum.json qa138/drive138_cum_35of35.bak.json
rm -f qa138/drive138_cum.json
echo "===== SPOTCHECK3 (farewell only) @ $(date +%H:%M:%S) ====="
$PY qa138/drive138.py ~/workspace/linji-work138 branch "s_fen_farewell" 2>&1 | tail -10
echo "----- spotcheck3 exit: $? @ $(date +%H:%M:%S) -----"
cp qa138/drive138_cum_35of35.bak.json qa138/drive138_cum.json
rm -f qa138/drive138_cum_35of35.bak.json
python3 -c "
import json
c=json.load(open('qa138/drive138_cum.json',encoding='utf-8'))
print('restored cum seen:', len(c['seen']))"
