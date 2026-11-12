# -*- coding: utf-8 -*-
# v20a156 HAND156 靜態測試：v145 review B1（空狀態三組佔位框）＋B3（700 picker 捲到 chips）。
# 反證：喺 pristine main（e08a070）index 上行會 FAIL（冇 EMPTY156／PICKER156 段）。
# 用法：python3 tests/test_handbook156_static.py [path-to-index.html]
# 註：本 test 用內容搜尋，唔寫死行號；rebase 後唔使 resync。
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

def seg_between(start, end, src=src):
    a = src.find(start)
    b = src.find(end, a + 1) if a >= 0 else -1
    return src[a:b] if a >= 0 and b > a else ""

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('v145 BOOK145 段仲喺度（本票冇郁佢）', 'v20a145 BOOK145' in src and 'BOOK145 完' in src)
ok('作品牆佔位框寫法原封不動（.works-frames142／.works-frame142／cap）',
   '.works-frames142{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:14px 2px 2px}' in src
   and '.works-frame142{aspect-ratio:3/4;border:2px dashed rgba(185,138,47,.6);' in src
   and '.works-frames142-cap{font-size:.78rem;color:var(--muted-ink);line-height:1.5;margin:8px 2px 2px}' in src)

# --- B1：共用 CSS（跟作品牆同一套語言） ---
ok('EMPTY156 段在場', 'v20a156 EMPTY156' in src and 'EMPTY156 完' in src)
css = seg_between('v20a156 EMPTY156', 'EMPTY156 完')
ok('B1 CSS：.empty156-frames 兩欄／三欄＋.empty156-frame＋.empty156-wide＋.empty156-cap',
   '.empty156-frames{display:grid;gap:8px;margin:14px 2px 2px}' in css
   and '.empty156-frames.cols2{grid-template-columns:repeat(2,1fr)}' in css
   and '.empty156-frames.cols3{grid-template-columns:repeat(3,1fr)}' in css
   and '.empty156-frame{aspect-ratio:3/4;border:2px dashed rgba(185,138,47,.6);' in css
   and '.empty156-wide{border:2px dashed rgba(185,138,47,.6);' in css
   and '.empty156-cap{font-size:.78rem;color:var(--muted-ink);' in css)
ok('B1 CSS：沿用作品牆色水（虛線金 rgba(185,138,47,.6)／米紙 rgba(255,248,232,.55)／墨字 #6b4e2e）',
   'rgba(185,138,47,.6)' in css and 'rgba(255,248,232,.55)' in css and 'color:#6b4e2e' in css)

# --- B1：獎項空狀態（四格典禮框） ---
awd_empty = seg_between('未有頒獎紀錄', '</div>\';', src)
ok('B1 獎項：空狀態原文一字唔郁', '未有頒獎紀錄。每年四季都有典禮' in src)
ok('B1 獎項：四格典禮框（廣告賞春／金碟夜夏／影藝獎秋／台慶冬）',
   'empty156-frames cols2' in awd_empty
   and '廣告賞' in awd_empty and '春季' in awd_empty
   and '金碟夜' in awd_empty and '夏季' in awd_empty
   and '影藝獎' in awd_empty and '秋季' in awd_empty
   and '台慶' in awd_empty and '冬季' in awd_empty
   and awd_empty.count('<div class="empty156-frame">') == 4)
ok('B1 獎項：引導句「第一個獎入嚟，就會擺入上面嗰格。」', '第一個獎入嚟，就會擺入上面嗰格。' in awd_empty)
awd_full = seg_between('el.innerHTML = log.map', 'function awards62SeasonHints', src)
ok('B1 獎項：有內容嗰陣唔出佔位框（log.map 段冇 empty156）', 'empty156' not in awd_full)

# --- B1：剪報空狀態 ---
clip_empty = seg_between('function renderClippingsPane(){', 'wireEndingBtn();', src)
ok('B1 剪報：空狀態原文一字唔郁', '未有剪報' in src and '殺青、頒獎或劇情見報之後' in src)
ok('B1 剪報：闊框「等你第一張剪報」＋三格虛線框＋引導句',
   'empty156-wide' in clip_empty and '等你第一張剪報' in clip_empty
   and 'empty156-frames cols3' in clip_empty
   and clip_empty.count('<div class="empty156-frame">') == 3
   and '第一張剪報一到，就會黐喺呢度；之後逐張疊上去。' in clip_empty)
clip_full = seg_between('box.innerHTML = endingCard + rows.map', 'function newspaperCheck(){', src)
ok('B1 剪報：有內容嗰陣唔出佔位框（rows.map 段冇 empty156）', 'empty156' not in clip_full)

# --- B1：庫存空狀態 ---
inv_fn = seg_between('function inv72Html(){', 'function inv72GoShop(){', src)
ok('B1 庫存：空狀態原文＋「去廟街禮品檔」掣一字唔郁',
   '庫存空空。去油麻地「廟街禮品」' in inv_fn and 'inv72-goshop' in inv_fn and '去廟街禮品檔' in inv_fn)
ok('B1 庫存：兩行×三格禮物格（6 格）＋引導句',
   'empty156-frames cols3' in inv_fn and inv_fn.count('<div class="empty156-frame">') == 6
   and '買咗禮物，就會擺入呢啲格。' in inv_fn)
inv_full = seg_between('} else {', 'function inv72GoShop(){', inv_fn)
ok('B1 庫存：有內容嗰陣唔出佔位框（else 段冇 empty156）', 'empty156' not in inv_full)

# --- B3：picker 捲到 chips ---
ok('PICKER156 段在場', 'v20a156 PICKER156' in src and 'PICKER156 完' in src)
pk = seg_between('v20a156 PICKER156', 'PICKER156 完')
ok('B3：train71ScrollChips156 存在＋scrollIntoView 置中',
   'function train71ScrollChips156()' in pk
   and 'chips.scrollIntoView({ block:"center" })' in pk)
ok('B3：chips 已經全見嗰陣唔郁（932 guard：top／bottom 齊喺 notebook 入面先 return）',
   'r.top >= nr.top && r.bottom <= nr.bottom' in pk)
ok('B3：開 picker 先調 scroll（train71TogglePanel 入面 if(open) 調用）',
   'if(open) train71ScrollChips156();' in src)
ok('B3：冇郁 chips／picker 其餘邏輯（train71PickerHtml／train71RenderPanel 原封不動）',
   'function train71PickerHtml(ctx){' in src and 'function train71RenderPanel(){' in src)

# --- B2 唔郁 ---
ok('B2 唔郁：700 鎖定態收起標題行規則仲喺度', '#nb-actions #btn-confirm-plan.is-locked{ font-size:20px;' in src)

print('TOTAL FAIL %d' % len(fails))
sys.exit(1 if fails else 0)
