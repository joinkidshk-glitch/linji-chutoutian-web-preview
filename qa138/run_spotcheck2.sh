#!/bin/bash
# Post-v134-rebase drive spot-check on main c881530 (v134 WF4 灰底已入)。
# 重點：兩個 WF4 芬姐 route（v134 郁 WF4 舞台）＋ lok sweep（v144 每週上限）。
cd ~/workspace/linji-work138
PY=/home/hatch/pwenv49/bin/python
cp qa138/drive138_cum.json qa138/drive138_cum_35of35.bak.json
rm -f qa138/drive138_cum.json
echo "===== SPOTCHECK2 @ $(date +%H:%M:%S) ====="
$PY qa138/drive138.py ~/workspace/linji-work138 branch "s_fen_intro,s_fen_farewell,e_lok_beats" 2>&1 | tail -14
echo "----- spotcheck2 exit: $? @ $(date +%H:%M:%S) -----"
cp qa138/drive138_cum_35of35.bak.json qa138/drive138_cum.json
python3 -c "
import json
c=json.load(open('qa138/drive138_cum.json',encoding='utf-8'))
print('restored cum seen:', len(c['seen']))"
