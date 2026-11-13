# -*- coding: utf-8 -*-
# v20a143 BOOK143 靜態測試：手帳內臟紙面化（v141 review B1＋B2＋B3）。
# 反證：喺 pristine main（4832b85）index 上行會 FAIL（冇 BOOK143 段）。
# 用法：python3 tests/test_book143_static.py [path-to-index.html]
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
ok('BOOK143 段在場', 'v20a143 BOOK143' in src and 'BOOK143 完' in src)

# --- v141 定案唔郁 ---
ok('v141 plan 組手寫行原封不動（plan 專屬選擇器仲喺度）',
   '#home-subtabs .hsub-group[data-hsubgroup="plan"] .home-tab.on::after' in src
   and '#home-subtabs .hsub-group[data-hsubgroup="plan"] .home-tab{ ' in src)
ok('鎖定態印章原封不動（24px、3px double 紅框、斜 -4.5°、letter-spacing .32em）',
   '#nb-actions #btn-confirm-plan.is-locked{' in src and 'font-size:24px' in src
   and 'border:3px double #c0452c !important' in src and 'rotate(-4.5deg)' in src
   and 'letter-spacing:.32em' in src)
ok('五個大 tab／備忘紙／吊牌唔郁（v141 選擇器仲喺度；v20a197 C1：選中格改 32px）',
   '#home-tabs .home-tab.on{ height:32px' in src and 'class="memo141" id="home-stats"' in src
   and 'width:102px !important' in src)

# --- B2：其餘四組 subtab 照 plan 組做法 ---
ok('B2：四組經 :not(plan) 擴展（career／status／news／favor 唔使逐組窮舉）',
   '#home-subtabs .hsub-group:not([data-hsubgroup="plan"]) .home-tab{' in src
   and '#home-subtabs .hsub-group:not([data-hsubgroup="plan"]) .home-tab.on::after' in src)
ok('B2：手寫字體 17px、未選褪色 #a08a68、選中紅墨圈（%23c0452c SVG）',
   '#home-subtabs .hsub-group:not([data-hsubgroup="plan"]) .home-tab:not(.on){ color:#a08a68; }' in src
   and '#home-subtabs .hsub-group:not([data-hsubgroup="plan"]) .home-tab.on{ background:transparent' in src)
ok('B2：四組容器同 plan 組一樣排版（gap 22px、左 inset 46px）',
   '#home-subtabs .hsub-group:not([data-hsubgroup="plan"]){ justify-content:flex-start; gap:22px; padding:4px 12px 4px 46px' in src)
ok('B2：四組 subtab 掣仲齊（作品／獎項／回憶／記數／標籤／庫存／傳聞／剪報／人情債／人脈）',
   all(('>%s</button>' % s) in src for s in
       ['作品', '獎項', '回憶', '記數', '標籤', '庫存', '傳聞', '剪報', '人情債', '人脈']))

# --- B1：編輯態掣群紙面化 ---
ok('B1：快捷四掣改紙標籤＋手寫字（直屬 > button，唔搶訓練選擇器掣；15px 要 !important 蓋 v17l）',
   '.nb-quick > button{ font-family:"Kaiti TC"' in src and 'font-size:15px !important' in src
   and 'border-radius:3px' in src and 'background:#fbf3df' in src)
ok('B1：複製 chip 改紙標籤（radius 3px、選中紅墨邊 #c0452c）',
   '.nb-copy-chips button, .nb-copy-chips .chip-day{ border-radius:3px' in src
   and '.nb-copy-chips button.on, .nb-copy-chips .chip-day.on{ background:#fdf6e0; border-color:#c0452c' in src)
ok('B1：複製預設＋套用改紙標籤手寫字；套用 .ink 由深啡實底改紅墨字',
   '.nb-copy-actions button{ font-family:"Kaiti TC"' in src
   and '.nb-copy-actions button.ink{ background:rgba(192,69,44,.07); color:#c0452c; border:2px solid #c0452c; }' in src)
ok('B1：每行「複製」改手寫墨字＋虛線底線（唔再係米色 pill）',
   '.day-row .cp{ background:transparent; border:0; border-bottom:1px dashed #b99b62' in src
   and 'font-size:13px; font-weight:700; padding:2px 2px; min-width:0; }' in src)
ok('B1：底部 bar 由深色底改紙面色 #f5eddc',
   '.nb-actions{ background:#f5eddc; border-top:1px solid #cbb98d; }' in src)
ok('B1：「還原」改手寫墨字＋虛線底線（2×id＋!important 先搶得贏 904 行 grouped !important）',
   '#nb-actions #btn-reset-plan{ background:transparent !important; border:0 !important' in src
   and 'border-bottom:1px dashed #b99b62 !important' in src
   and 'font-size:15px !important' in src)
ok('B1：可編輯態「確定」改紅墨字掣（2px 實線紅框、18px 手寫字；:not(.is-locked) 保鎖定態印章唔受影響）',
   '#nb-actions #btn-confirm-plan:not(.is-locked){ background:rgba(192,69,44,.07) !important; border:2px solid #c0452c !important' in src
   and 'font-size:18px !important' in src and 'letter-spacing:.14em' in src)
ok('B1：全部掣 id／class 仲齊（全日休息／全日訓練／清空本週／複製到…／套用複製／還原／確定）',
   all(s in src for s in ['id="nb-q-rest"', 'id="nb-q-train"', 'id="nb-q-clear"', 'id="nb-q-copy"',
                          'id="nb-copy-apply"', 'id="btn-reset-plan"', 'id="btn-confirm-plan"'])
   and all(s in src for s in ['>全日休息</button>', '>全日訓練</button>', '>清空本週</button>',
                              '>複製到…</button>', '>套用複製</button>', '>還原</button>', '>確定本週行程</button>']))

# --- B3：短屏印章收細，932 唔變 ---
ok('B3：短屏 media query（max-height:780px）印章 24px→20px、收窄 padding／margin',
   '@media (max-height:780px){' in src
   and '#nb-actions #btn-confirm-plan.is-locked{ font-size:20px; padding:4px 14px 4px 16px; margin:0; }' in src)  # v20a197 B2：700 印章都係 flex:1 佔滿 bar，margin 歸零（舊 margin:4px auto 3px 會令印章收窄置中）
ok('B3：短屏 nb-actions padding 一併收窄（慳多約 8px）',
   '#nb-actions{ padding:6px 10px calc(6px + env(safe-area-inset-bottom)); }' in src)
ok('B3：932 印章規則無全局改動（24px 只出現喺 v141 原規則，唔係 BOOK143 段入面改大）',
   src.count('font-size:24px') == 1)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
