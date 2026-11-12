# v20a131 B4 對話框維持固定高，短句留空用文字垂直置中去減・靜態守門測試。
# 用法：python3 tests/test_ui131b4_static.py [path-to-index.html]
# 對 pristine main 行 → 置中規則缺席 → 乾淨 FAIL（唔 crash）。
# 紅線：高度邏輯一律唔郁（主線 118px／巧遇 4.65em），絕對唔准走返去跟字數伸縮。
import os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# 基線不變
ok('SAVE key 不變', 'starVolunteer_map_v19w' in html)
ok('softRev 不變', 's107' in html)
ok('產品 ?v= 不變', 'v20a10' in html)

# ---------- 固定高不變 ----------
ok('主線對話框定高 118px（height＋min＋max 三齊）',
   '.story-play .dlg106-plate{height:118px;min-height:118px;max-height:118px;flex:1}' in html)
ok('巧遇對白行定 3 行 4.65em 不變',
   '#enc79-overlay .e79-line{margin:0 0 10px;line-height:1.55;font-size:1rem;height:4.65em;min-height:4.65em;overflow-y:auto;white-space:pre-wrap;}' in html)
ok('巧遇名牌行定高 1.5em 不變',
   '#enc79-overlay .e79-name{font-weight:800;color:#8a5a00;margin:0 0 4px;font-size:.95rem;line-height:1.5;min-height:1.5em;}' in html)
ok('主線牌無 height:auto（唔准跟字數伸縮）',
   'dlg106-plate{height:auto' not in html and 'dlg106-plate{ height:auto' not in html)

# ---------- 主線：plate flex 縱向＋.sp-line margin auto 置中 ----------
ok('主線 plate 改 flex 縱向',
   '.story-play .dlg106-plate{ display:flex; flex-direction:column; }' in html)
ok('主線內文 .sp-line margin-top/bottom auto 置中',
   '.story-play .dlg106-plate .sp-line{ margin-top:auto; margin-bottom:auto; }' in html)
ok('主線置中只限 .dlg106-plate（舊 bust 牌唔郁）',
   '.story-play .sp-plate{ display:flex' not in html)

# ---------- 巧遇：.e79-line display:flex＋align-items:safe center ----------
ok('巧遇 .e79-line display:flex 置中',
   '#enc79-overlay .e79-line{ display:flex; align-items:safe center; }' in html)
ok('巧遇置中用 safe center（超長句溢出跌返 flex-start，首行唔裁走）',
   'align-items:safe center' in html)

# 反證：刪走置中規則，置中斷言必須轉 False
def center_ok(s):
    return ('.story-play .dlg106-plate .sp-line{ margin-top:auto; margin-bottom:auto; }' in s) \
        and ('#enc79-overlay .e79-line{ display:flex; align-items:safe center; }' in s)
ok('反證：刪走置中規則後 center_ok 必須轉 False',
   center_ok(html) and not center_ok(html.replace(
       '.story-play .dlg106-plate .sp-line{ margin-top:auto; margin-bottom:auto; }', '')))
ok('反證：主線定高改 120px 後固定高斷言必須 FAIL',
   '.story-play .dlg106-plate{height:118px;min-height:118px;max-height:118px;flex:1}' in html
   and '.story-play .dlg106-plate{height:118px;min-height:118px;max-height:118px;flex:1}' not in
   html.replace('.story-play .dlg106-plate{height:118px;min-height:118px;max-height:118px;flex:1}',
                '.story-play .dlg106-plate{height:120px;min-height:120px;max-height:120px;flex:1}'))

print('TOTAL %s' % ('PASS' if not fails else 'FAIL: ' + ', '.join(fails)))
sys.exit(1 if fails else 0)
