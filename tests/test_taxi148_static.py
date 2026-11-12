# -*- coding: utf-8 -*-
# v20a148 B1 靜態測試：st08 的士 banner 裁切位改 20%（747＋啟德跑道入鏡）。
# 反證：喺 pristine main（da90957／v146）index 上行會 FAIL（冇 taxi 20% 分流）。
# 用法：python3 tests/test_taxi148_static.py [path-to-index.html]
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('覆寫表 st08 唔郁（的士圖本身不變，唔使重生圖）',
   'wf4_ev_st08:"assets/story/locs/bg_wf4_taxi.jpg?v=20a146"' in src)
ok('覆寫表 st05／st06／set08／st04 唔郁',
   'wf4_ev_st05:"assets/story/locs/bg_wf4_karaoke.jpg?v=20a146"' in src
   and 'wf4_ev_st06:"assets/story/locs/bg_wf4_market.jpg?v=20a134"' in src
   and 'wf4_ev_set08:"assets/story/locs/bg_loc_film_lion.jpg?v=20a104"' in src
   and 'wf4_ev_st04:"assets/story/locs/bg_loc_cafe_cha.jpg?v=20a104"' in src)

# --- B1：的士 banner 偏向 747＋啟德跑道（只限 taxi 圖） ---
ok('B1：scenePos146 按圖分流，taxi 圖先加 background-position:center 20%',
   'bg_wf4_taxi.jpg' in src and 'background-position:center 20%' in src
   and 'scenePos146' in src)
ok('B1：20% 只出現一次（唔係全局規則）', src.count('background-position:center 20%') == 1)
ok('B1：v20a148 B1 註解在場（講明 20% 係 review 模擬驗證嘅甜點）', 'v20a148 B1' in src)
ok('B1：分流行同時認 market 75% 同 taxi 20%（同一條 ternary，唔係兩處分流）',
   'bg_wf4_market.jpg")>=0 ? ";background-position:center 75%" : scene105 && scene105.indexOf("bg_wf4_taxi.jpg")>=0 ? ";background-position:center 20%" : ""' in src)

# --- B2 回歸守衛：街市 75% 原封不動 ---
ok('B2：market 75% 仲喺度', 'background-position:center 75%' in src)
ok('B2：75% 只出現一次（唔係全局規則）', src.count('background-position:center 75%') == 1)
ok('B2：v20a146 B2 註解仲喺度', 'v20a146 B2' in src)
ok('B2：共用 .wf4-scene105 嘅 background-position:center 原封不動（set08／st04／st05 唔變）',
   '.wf4-scene105{ height:150px; border-radius:10px; background-size:cover; background-position:center;' in src)
ok('B2：舞台版 sp-bg-layer 仲係 center（唔郁）',
   'background-size:cover;background-position:center' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
