#!/bin/bash
# v138 fix-up chunk — only the 2 remaining live targets (resume skips the other 33).
# e_chung_heart (C9 seed) + s_fen_intro (open_loc_retry). Run detached.
cd ~/workspace/linji-work138
PY=/home/hatch/pwenv49/bin/python
echo "===== FIXUP @ $(date +%H:%M:%S) ====="
$PY qa138/drive138.py ~/workspace/linji-work138 branch "e_chung_heart,s_fen_intro" 2>&1 | tail -20
echo "----- fixup exit: $? @ $(date +%H:%M:%S) -----"
python3 -c "
import json
c=json.load(open('qa138/drive138_cum.json',encoding='utf-8'))
print('seen:', len(c['seen']), 'missing:', sorted(set(['chai_zanhoi_angry.webp','chai_zanhoi_shy.webp','chai_zanhoi_smile.webp','chai_zanhoi_think.webp','cheung_hakfan_serious.webp','cheung_tsijun_sad.webp','cheung_tsijun_think.webp','crew_laolinji_serious.webp','extra_ad_fen_sad.webp','extra_ad_fen_serious.webp','ho_sang_surprise.webp','ko_chunkit_shy.webp','ko_chunkit_think.webp','lin_hiu_serious.webp','lin_hiu_smile.webp','liu_bingxing_sad.webp','liu_bingxing_surprise.webp','liu_bingxing_think.webp','lok_gasing_angry.webp','lok_gasing_shy.webp','lok_gasing_smile.webp','lok_gasing_surprise.webp','lui_ging_serious.webp','luk_baakyin_angry.webp','luk_baakyin_sad.webp','luk_baakyin_smile.webp','mak_zhendong_angry.webp','mak_zhendong_smile.webp','ngai_wingnaam_angry.webp','ngai_wingnaam_serious.webp','ngai_wingnaam_smile.webp','ngai_wingnaam_surprise.webp','ngai_wingnaam_think.webp','so_jiyan_surprise.webp','tsui_poushan_serious.webp','vera_serious.webp','chung_choning_angry.webp']) - set(c['seen'])))" 
