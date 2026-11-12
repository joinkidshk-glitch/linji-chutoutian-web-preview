#!/bin/bash
# Post-v136-rebase drive spot-check on main f0ae995 (v136 結局閘已入)。
# 重點：chung（C9 seed＋story gate 互動）＋ fen intro（WF4）＋ lok sweep。
cd ~/workspace/linji-work138
PY=/home/hatch/pwenv49/bin/python
cp qa138/drive138_cum.json qa138/drive138_cum_35of35.bak.json
rm -f qa138/drive138_cum.json
echo "===== SPOTCHECK4 @ $(date +%H:%M:%S) ====="
$PY qa138/drive138.py ~/workspace/linji-work138 branch "e_chung_heart,s_fen_intro,e_lok_beats" 2>&1 | tail -14
echo "----- spotcheck4 exit: $? @ $(date +%H:%M:%S) -----"
cp qa138/drive138_cum_35of35.bak.json qa138/drive138_cum.json
rm -f qa138/drive138_cum_35of35.bak.json
python3 -c "
import json
c=json.load(open('qa138/drive138_cum.json',encoding='utf-8'))
print('restored cum seen:', len(c['seen']))"
