#!/bin/bash
# v138r2 drive chunks — sequential, each chunk a fresh drive invocation (fresh browser+server).
# Run detached: setsid nohup qa138/run_chunks.sh > qa138/run_chunks.log 2>&1 < /dev/null &
cd ~/workspace/linji-work138
PY=/home/hatch/pwenv49/bin/python
run() { echo "===== CHUNK $1 @ $(date +%H:%M:%S) ====="; $PY qa138/drive138.py ~/workspace/linji-work138 branch "$1" 2>&1 | tail -12; echo "----- chunk $1 exit: $? @ $(date +%H:%M:%S) -----"; }
run "e_chai_heart,e_chai_beats,e_chung_heart"
run "e_liu_T1,e_lok_T2,e_lok_beats"
run "e_mak_heart,e_ngai_first,e_ngai_T0,e_ngai_T0sup"
run "e_ngai_heart,e_ngai_stageup,e_ngai_pool,e_so_T1"
run "s_hakfan_end,s_c2,s_c19,s_fong_crisis,s_tsijun_crisis,s_tsijun_meet,s_fen_rumor,s_f4,s_ho_meet"
run "s_w3_liao,s_c12,s_hiu_meet,s_hiu_end,s_lei_end,s_xu_meet,s_xu_end,s_vera_meet"
echo "===== ALL CHUNKS DONE @ $(date +%H:%M:%S) ====="
python3 -c "
import json
c=json.load(open('qa138/drive138_cum.json',encoding='utf-8'))
print('FINAL seen:', len(c['seen']), sorted(c['seen'].keys()))
print('FINAL missing phases:')
for t,v in c['phases'].items():
    if v.get('missing'): print(' ', t, v['missing'])"
