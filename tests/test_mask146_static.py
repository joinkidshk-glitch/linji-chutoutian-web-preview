# -*- coding: utf-8 -*-
# v20a146 MASK146 靜態測試：WF4 舞台 modal 間歇性標題被切（A1）＋街市 banner 空白招牌（B2）。
# 反證：喺 pristine main（f0ae995／v136）index 上行會 FAIL（.mask 仲係 absolute、冇 market 75% 分流）。
# 用法：python3 tests/test_mask146_static.py [path-to-index.html]
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
ok('得一個 #mask 元素（全部 modal 共用同一個 mask）',
   src.count('id="mask"') == 1 and src.count('<div class="mask"') == 1)
ok('modal() 單一 choke point 仲喺度（全部 modal 經佢開）', 'function modal(html, buttons, opts){' in src)
ok('WF4_SCENE_OVERRIDE134 覆寫表唔郁（16 單齊：屋企 5／電話亭 4／街市 5／廠房＋冰室 2）',
   all(('wf4_ev_%s:"assets/story/locs/bg_wf4_%s.jpg?v=20a134"' % (e, g)) in src
       for e, g in [('home01', 'home'), ('home02', 'home'), ('home03', 'home'), ('home04', 'home'),
                    ('day01', 'home'), ('st01', 'booth'), ('st02', 'booth'), ('st03', 'booth'),
                    ('day02', 'booth'), ('st06', 'market'), ('st07', 'market'), ('st11', 'market'),
                    ('day03', 'market'), ('day04', 'market')])
   and 'wf4_ev_set08:"assets/story/locs/bg_loc_film_lion.jpg?v=20a104"' in src
   and 'wf4_ev_st04:"assets/story/locs/bg_loc_cafe_cha.jpg?v=20a104"' in src)

# --- A1：mask 改 viewport 錨定 ---
ok('A1：.mask 改 position:fixed＋top/bottom 0（唔再跟 #app 嘅 100dvh 高）',
   '.mask{position:fixed;top:0;bottom:0;' in src)
ok('A1：舊 absolute＋inset:0 已經拎走', '.mask{position:absolute;inset:0;' not in src)
ok('A1：橫向繼續跟 #app 框（390px 置中，唔係 full-viewport 闊）',
   'left:50%;width:min(390px,100%);transform:translateX(-50%);' in src)
ok('A1：bottom-sheet 行為保留（align-items:flex-end，唔改置中）',
   '.mask{position:fixed;top:0;bottom:0;left:50%;width:min(390px,100%);transform:translateX(-50%);background:rgba(0,0,0,.6);z-index:50;display:none;align-items:flex-end;' in src)
ok('A1：教學卡置中保留（#mask.tut-on align-items:center 唔郁）',
   '#mask.tut-on{align-items:center;padding:16px}' in src)
ok('A1：day-res modal 規則保留（padding-top:52px 唔郁）',
   'body.day-res-open #mask.day-res{' in src and 'padding-top:52px;' in src)
ok('A1：desktop ≥480px mask 上下貼齊 #app 框（top/bottom 14px）',
   '@media(min-width:480px){.mask{top:14px;bottom:14px}}' in src)
ok('A1：desktop ≥900px mask 跟 468px 框＋desktop-rail 偏移（唔會偏離 #app）',
   '@media(min-width:900px){.mask{width:min(468px,100%);top:18px;bottom:18px;left:calc(50% + (min(220px,22vw) + 22px)/2)}}' in src)
ok('A1：MASK146 註解在場（講明點解 fixed＋desktop 對位）', 'v20a146 MASK146' in src)

# --- A1 後備帽：modal 高帽加 svh，dvh 誤報偏大都唔會頂出畫面 ---
ok('A1：非教學 modal 高帽加 78svh（fallback 仍係 L430 嘅 78dvh）',
   '#mask:not(.tut-on) .modal{' in src
   and 'max-height: min(78dvh,78svh,720px) !important;' in src)
ok('A1：矮屏（max-height:820px）高帽加 88svh',
   '@media (max-height: 820px){' in src
   and 'max-height: min(88dvh,88svh,720px) !important;' in src)
ok('A1：教學 modal 高帽加 88svh',
   '#mask.tut-on .modal{background:transparent;border:0;padding:0;max-height:min(88dvh,88svh,760px);' in src)
ok('A1：StoryPlay modal 78dvh 規則原封不動（ui133 釘死；呢句冇 !important，實際由上面 !important 高帽管，唔使加 svh）',
   '#mask.story-play-on .modal{max-height:min(78dvh,720px);overflow:hidden}' in src)
ok('A1：基底 .modal 嘅 78dvh 規則原封不動（svh 唔支援嗰陣嘅 fallback）',
   '.modal{width:100%;max-width:100%;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:12px;max-height:min(78dvh,720px);' in src)

# --- B2：街市 banner 偏向檔口帶（只限 market 圖） ---
ok('B2：sceneHtml105 按圖分流，market 圖先加 background-position:center 75%',
   'bg_wf4_market.jpg' in src and 'background-position:center 75%' in src
   and 'scenePos146' in src)
ok('B2：75% 只出現一次（唔係全局規則）', src.count('background-position:center 75%') == 1)
ok('B2：共用 .wf4-scene105 嘅 background-position:center 原封不動（set08／st04 唔變）',
   '.wf4-scene105{ height:150px; border-radius:10px; background-size:cover; background-position:center;' in src)
ok('B2：舞台版 sp-bg-layer 仲係 center（唔郁）',
   'background-size:cover;background-position:center' in src)
ok('B2：MARKET146／B2 註解在場', 'v20a146 B2' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
