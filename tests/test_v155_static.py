# -*- coding: utf-8 -*-
# v20a155 靜態測試：v142 review B1＋B2＋B3。
# 反證：喺 pristine main（e08a070／v148）index 上行，B1／B2／B3 斷言會乾淨 FAIL，唔會 crash。
# 用法：python3 tests/test_v155_static.py [path-to-index.html]
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
ok('content pack JSON 唔郁（今次唔涉及）', 'content/gigs_1988.json' in src and 'story_detail_c1_to_c17.json' in src)
ok('幕次序唔郁（v153 範圍，唔掂）',
   'const order71 = [["C1",1],["C2",2],["C3",3],["C4",4],["C5",5],["C6",6],["C6F",20],["C18",18],["C19",19],["C7",7],["C8",8],["C9",9],["C10",10],["C11",11],["C12",12],["C13",13],["C14",14],["C15",15],["C16",16],["C17",17]];' in src)
ok('機制說明一字唔郁',
   '逐幕列出開放條件同你而家嘅進度：✓ 係已達標，○ 係未達。完成一幕，之後嘅幕會逐漸揭曉。' in src)
ok('寄語卡文案／樣式唔郁',
   '臨記呢行，冇一步登天——每一日跑嘅通告、練嘅功、識嘅人，都係之後嗰幕嘅伏線。' in src
   and '.prog71-next142{ margin:2px 0 0; border:1px dashed rgba(185,138,47,.6); background:linear-gradient(180deg,#fdf6e0,#fbf2da); border-radius:12px; padding:12px 12px 13px; }' in src)

# --- B1：故事舞台底罅（根因：v20a41 大註解提早閂，吞咗 #mask.story-play-on 呢條 rule；
#      另 #modal-inner 12px padding-bottom  specificity 輸 L3506） ---
ok('B1：v20a41 註解多餘閂標記已刪（「已申報」句後唔再提早閂）', '已申報）。 */' not in src)
ok('B1：v20a41 註解其餘內容仲喺度（唔係成段刪走）',
   '目標：《明星志願》式全屏分層' in src and '唔會爛版）。 */' in src)
ok('B1：#mask.story-play-on 底色／padding rule 仲喺度',
   '#mask.story-play-on{padding:0;align-items:stretch;background:#0a0705 !important}' in src)
ok('B1：#modal-inner story 作用域 padding 加 !important（贏 L3506 (2,2,0)）',
   '#mask.story-play-on #modal-inner{overflow:hidden !important;padding:0 !important}' in src)
ok('B1：L3506 通用 rule 唔郁（其他 modal 嘅 12px 照舊）',
   '#mask:not(.casting-sheet-on):not(.tut-on) #modal-inner{\n  padding-bottom:12px;\n}' in src)
ok('B1：v20a155 B1 註解在場', 'v20a155 B1' in src)
ok('B1：.modal／.story-play 全屏 rule 唔郁',
   '#mask.story-play-on .modal{' in src
   and '#mask.story-play-on .story-play{\n  position:relative;height:100%;max-height:none;gap:0;overflow:hidden;\n}' in src)
ok('B1：對話框遮腿幾何唔郁（sp-stage-inner 底 padding 66px）',
   'padding:10px 12px calc(66px + env(safe-area-inset-bottom,0px));' in src)

# --- B2：進度頁寄語橫跨摺線（上面收窄，慳 108px 在場態／54px 唔在場態） ---
ok('B2：行 padding 9→4、行距 8→5', '.prog71-row{ border:1px solid #c4a574; background:#fff8e8; border-radius:12px; padding:4px 11px; margin:0 0 5px; }' in src)
ok('B2：intro margin 10→6、行高 1.6→1.5', '.prog71-intro{ font-size:.78rem; color:#8a755a; line-height:1.5; margin:0 0 6px; }' in src)
ok('B2：幕頂行高 1.3', '.prog71-top{ display:flex; align-items:baseline; gap:8px; line-height:1.3; }' in src)
ok('B2：條件 ul margin 8→6、li 行高 1.55→1.4',
   '.prog71-items{ list-style:none; margin:6px 0 0; padding:0; }' in src
   and '.prog71-items li{ font-size:.8rem; line-height:1.4; color:#6b5636; }' in src)
ok('B2：note 行高 1.55→1.45、margin 6→5', '.prog71-note{ font-size:.78rem; color:#6b5636; line-height:1.45; margin:5px 0 0; }' in src)
ok('B2：播掣 min-height 40→36、margin-top 8→6', '.prog71-play{ margin-top:6px; min-height:36px; padding:8px 16px;' in src)
ok('B2：標題 margin 4→2、wrap 頂 padding 2→0、捲動器頂 padding 4→2',
   '.prog71-h{ margin:0 0 2px;' in src
   and '.prog71-wrap{ padding:0 0 8px; }' in src
   and '#home-pane-progress .journal-scroll{ flex:1 1 auto; min-height:0; overflow:auto; padding:2px 2px 16px;' in src)
ok('B2：v20a155 B2 註解在場（列明慳位預算）', 'v20a155 B2' in src and '要慳 108／54px' in src)

# --- B3：會場標籤「金禧大酒店」對比弱（跟返 15 張標籤：深啡墨字＋米紙光暈） ---
ok('B3：.md97-venue99 專用規則在場（深啡 #43301c、opacity 1、.mn68 同級光暈）',
   '.md97-venue99{ color:#43301c; opacity:1;' in src
   and 'text-shadow:0 0 3px #f3e7c8, 0 0 3px #f3e7c8, 1px 0 2px #f3e7c8, -1px 0 2px #f3e7c8, 0 1px 2px #f3e7c8, 0 -1px 2px #f3e7c8; }' in src)
ok('B3：v20a155 B3 註解在場', 'v20a155 B3' in src)
ok('B3：.md97 底色 rule 唔郁（淡金 #7a5c33／.88 仲喺 base 度，其他 .md97 唔受影響）',
   'font-size:10.5px; font-weight:700; letter-spacing:.22em; color:#7a5c33; line-height:1.2; opacity:.88;' in src)
ok('B3：.mn68 15 張標籤樣式唔郁',
   '.mn68{ position:absolute; transform:translate(-50%,0); white-space:nowrap; pointer-events:none;' in src
   and 'font-size:12.5px; font-weight:800; letter-spacing:.08em; color:#43301c; line-height:1.2;' in src)
ok('B3：會場標籤 HTML／位置唔郁（left:11%;top:32%）',
   '<div class="md97 md97-venue99" style="left:11%;top:32%">金禧大酒店</div>' in src)
ok('B3：positionMapLabels137 位置邏輯唔郁',
   'document.querySelectorAll(".map-names68 .mn68, #map-districts97 .md97-venue99")' in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
