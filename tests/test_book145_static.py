# -*- coding: utf-8 -*-
# v20a145 BOOK145 靜態測試：手帳紙面化收尾（v143 review B1＋B2＋B3）。
# 反證：喺 pristine main（c881530）index 上行會 FAIL（冇 BOOK145 段）。
# 用法：python3 tests/test_book145_static.py [path-to-index.html]
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
ok('BOOK145 段在場', 'v20a145 BOOK145' in src and 'BOOK145 完' in src)

seg = src[src.find('v20a145 BOOK145'):src.find('BOOK145 完')]

# --- v141／v143 定案唔郁 ---
ok('v141 plan 組手寫行原封不動（plan 專屬選擇器仲喺度）',
   '#home-subtabs .hsub-group[data-hsubgroup="plan"] .home-tab.on::after' in src
   and '#home-subtabs .hsub-group[data-hsubgroup="plan"] .home-tab{ ' in src)
ok('鎖定態印章原封不動（24px、3px double 紅框、斜 -4.5°、letter-spacing .32em）',
   '#nb-actions #btn-confirm-plan.is-locked{' in src and 'font-size:24px' in src
   and 'border:3px double #c0452c !important' in src and 'rotate(-4.5deg)' in src
   and 'letter-spacing:.32em' in src)
ok('v143 B3 短屏印章 20px 規則仲喺度（唔係本票改走；v20a197 B2：margin 歸零）',
   '#nb-actions #btn-confirm-plan.is-locked{ font-size:20px; padding:4px 14px 4px 16px; margin:0; }' in src)
ok('五個大 tab／備忘紙／吊牌唔郁（v141 選擇器仲喺度；v20a197 C1：選中格改 32px）',
   '#home-tabs .home-tab.on{ height:32px' in src and 'class="memo141" id="home-stats"' in src
   and 'width:102px !important' in src)
ok('v143 B1 紙標籤／B2 其餘四組 subtab 規則仲喺度',
   '.nb-quick > button{ font-family:"Kaiti TC"' in src
   and '#home-subtabs .hsub-group:not([data-hsubgroup="plan"]) .home-tab.on::after' in src)

# --- B2：其餘八組 pane 底換紙面（跟 v131 B2 事業三頁同一套） ---
for pane in ('ledger', 'inv', 'rumor', 'clippings', 'debt', 'people', 'tags', 'progress'):
    ok('B2：#home-pane-%s .journal-scroll 入紙面組' % pane,
       ('#home-pane-%s .journal-scroll' % pane) in seg)
ok('B2：紙面係事業頁同一套（#f3e6c8＋金邊 #c4a574＋圓角 14px＋padding 12px 10px 16px）',
   'background:#f3e6c8; color:#2a2118;' in seg
   and 'border-radius:14px 14px 0 0; border:2px solid #c4a574; border-bottom:0;' in seg
   and 'padding:12px 10px 16px;' in seg)
ok('B2：三處深底淺字覆寫還原返墨色（ledger-enroll／people-next／debt pane-intro）',
   '#home-pane-ledger .ledger-enroll{ color:#6b4e2e; }' in seg
   and '#home-pane-people .people-next{ color:#6b4e2e; }' in seg
   and '#home-pane-debt .pane-intro{ color:#5a4328; }' in seg)
ok('B2 續：v76 淺字覆寫 .jobs72-h（庫存／人脈標題）＋進度頁 .prog71-h／.prog71-intro 還原返墨色',
   '#home-pane-inv .jobs72-h, #home-pane-people .jobs72-h{ color:#43301c; }' in seg
   and '#home-pane-progress .prog71-h{ color:#43301c; }' in seg
   and '#home-pane-progress .prog71-intro{ color:#8a755a; }' in seg)
ok('B2 續：傳聞頁 .weak-whisper 故意淡化鬼影字冇新規則（v76 保留決定；段入面得註解提及）',
   '.weak-whisper{' not in seg)
ok('B2：事業三頁（works／awards／memory）唔喺 BOOK145 段入面——唔同 v142 撞',
   'home-pane-works' not in seg and 'home-pane-awards' not in seg and 'home-pane-memory' not in seg)
ok('B2：v131 事業三頁紙面規則本身仲喺度',
   '#home-pane-works .journal-scroll,' in src and '#home-pane-memory .journal-scroll{' in src)
ok('B2：plan pane 唔喺紙面組入面（notebook 本身已經係紙面；段入面得 B1 :has 規則提及佢）',
   '#home-pane-plan .journal-scroll' not in seg)

# --- B3：訓練選擇器換紙面語言 ---
ok('B3：屬性 chips（.guide68-chips .guide68-chip）換紙標籤（#fbf3df＋金邊 #b99b62＋radius 3px＋手寫字）',
   '.guide68-chips .guide68-chip{ background:#fbf3df; border:1px solid #b99b62; border-radius:3px; color:#3a2e22;' in seg)
ok('B3：chips 選中用紅墨（#c0452c＋淡紅底，跟複製 chip .on）',
   '.guide68-chips .guide68-chip.on{ background:#fdf6e0; border-color:#c0452c; color:#c0452c;' in seg)
ok('B3：排入掣（.train71-acts .train71-pick）同樣換紙標籤（唔再係實色金掣）',
   '.train71-acts .train71-pick{ background:#fbf3df; border:1px solid #b99b62; border-radius:3px; color:#3a2e22;' in seg)
ok('B3：選擇器用 0,2,0 親層（.guide68-chips／.train71-acts）先搶得贏 .nb-quick button（0,1,1）',
   '0,2,0' in seg and '.nb-quick button' in seg)
ok('B3：chips／排入掣生成邏輯仲喺度（train71PickerHtml 出 data-gstat／data-t71pick）',
   'class="guide68-chip' in src and 'data-gstat="' in src
   and 'class="train71-pick" data-t71pick="' in src)

# --- B1：短屏鎖定態再慳 67px，七日成行全見 ---
ok('B1：短屏鎖定態先收起標題行＋提示列（:has(.is-locked)，可編輯態唔受影響）',
   '#home-pane-plan:has(#btn-confirm-plan.is-locked) #nb-plan-title,' in seg
   and '#home-pane-plan:has(#btn-confirm-plan.is-locked) #nb-plan-mode{ display:none !important; }' in seg)
ok('B1：range 底 margin 6px→2px（短屏鎖定態限定，!important 蓋舊規則）',
   '#home-pane-plan:has(#btn-confirm-plan.is-locked) .nb-range{ margin-bottom:2px !important; }' in seg)
ok('B1：footer padding 短屏鎖定態同未確認態一致（v20a197 B2：5px→6px，印章 y 唔差 1px）',
   '#nb-actions:has(#btn-confirm-plan.is-locked){ padding:6px 10px calc(6px + env(safe-area-inset-bottom)); }' in seg)
ok('B1：成段收窄只喺 @media (max-height:780px) 入面——932 唔受影響',
   seg.count('@media (max-height:780px){') == 1)
ok('B1：標題行／提示列本身仲喺 HTML（淨係 CSS 收起，DOM／文字唔郁）',
   'id="nb-plan-title">本週行程</p>' in src and 'id="nb-plan-mode" hidden></p>' in src)

print('RESULT ' + ('FAIL (%d)' % len(fails) if fails else 'PASS'))
sys.exit(1 if fails else 0)
