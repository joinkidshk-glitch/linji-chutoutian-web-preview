# -*- coding: utf-8 -*-
# v20a227 C1 靜態測試：day24 電視台信件房 banner 裁切位改 80%（枱面信件入鏡）。
# 反證：喺 pristine main（7e05a4d／v226）index 上行會 FAIL（冇 kowloon 80% 分流）。
# 用法：python3 tests/test_wf4_227_c1_static.py [path-to-index.html]
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
ok('覆寫表 day24 唔郁（圖本身不變，唔使重生圖）',
   'wf4_ev_day24:"assets/story/locs/bg_loc_tvb_kowloon.jpg?v=20a104"' in src)

# --- C1：信件房 banner 偏向枱面信件（只限 kowloon 圖） ---
ok('N1：scenePos146 按圖分流，kowloon 圖先加 background-position:center 80%',
   'bg_loc_tvb_kowloon.jpg' in src and 'background-position:center 80%' in src
   and 'scenePos146' in src)
ok('N1：80% 只出現一次（唔係全局規則）', src.count('background-position:center 80%') == 1)
ok('N1：v20a227 C1 註解在場（講明 80% 係 PIL 模擬驗證嘅甜點）', 'v20a227 C1' in src)
ok('N1：分流行同時認 market 75%／taxi 20%／harbour 15%／kowloon 80%（同一條 ternary，唔係兩處分流）',
   'bg_wf4_market.jpg")>=0 ? ";background-position:center 75%" : scene105 && scene105.indexOf("bg_wf4_taxi.jpg")>=0 ? ";background-position:center 20%" : scene105 && scene105.indexOf("bg_loc_film_harbour.jpg")>=0 ? ";background-position:center 15%" : scene105 && scene105.indexOf("bg_loc_tvb_kowloon.jpg")>=0 ? ";background-position:center 80%" : ""' in src)

# --- 回歸守衛：其餘三張圖＋共用 center 原封不動 ---
ok('N1：market 75%／taxi 20%／harbour 15% 仲喺度',
   'background-position:center 75%' in src
   and 'background-position:center 20%' in src
   and 'background-position:center 15%' in src)
ok('N1：共用 .wf4-scene105 嘅 background-position:center 原封不動（其他事件唔變）',
   '.wf4-scene105{ height:150px; border-radius:10px; background-size:cover; background-position:center;' in src)
ok('N1：舞台版 sp-bg-layer 仲係 center（唔郁）',
   'background-size:cover;background-position:center' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
