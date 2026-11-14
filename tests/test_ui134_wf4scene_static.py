# v20a134 WF4 灰底場景覆寫表・靜態守門測試。
# 用法：python3 tests/test_ui134_wf4scene_static.py [path-to-index.html]
# 反證意識：每項同時驗「新寫法在」＋「舊寫法不在」。
# 對 pristine main 行 → WF4_SCENE_OVERRIDE134 唔存在 → 乾淨 FAIL。
import os, re, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
root = os.path.dirname(os.path.abspath(path))
html = open(path, encoding='utf-8').read()
fails = []

def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

# --- 覆寫表存在＋結構 ---
m = re.search(r'const WF4_SCENE_OVERRIDE134 = \{(.*?)\};', html, re.S)
ok('WF4_SCENE_OVERRIDE134 存在', m is not None)
table = {}
if m:
    for em in re.finditer(r'(wf4_ev_\w+):"([^"]+)"', m.group(1)):
        table[em.group(1)] = em.group(2)
ok('覆寫表 48 單（48 單無 loc，全覆蓋，v20a203 新 day 事件 12 單入埋表）', len(table) == 48)

# --- 全部事件 id（DAILY_EVENTS_WF4） ---
ev_ids = set(re.findall(r'id:"(wf4_ev_\w+)"', html))
ok('DAILY_EVENTS_WF4 113 單（v20a203 Phase 2）', len(ev_ids) == 113)
ok('覆寫表全部 id 都係真事件', table and all(k in ev_ids for k in table))
ok('覆寫表無重複 id', len(table) == len(set(table)))

# --- 覆蓋會計：無 loc 嘅 day 事件＝16 覆寫＋2 留灰 ---
arr = re.search(r'DAILY_EVENTS_WF4\s*=\s*\[(.*?)\n\];', html, re.S)
ok('DAILY_EVENTS_WF4 陣列搵到', arr is not None)
nolocev = set()
if arr:
    for chunk in re.split(r'(?=\{\s*id:"wf4_ev_)', arr.group(1)):
        im = re.match(r'\{\s*id:"(wf4_ev_\w+)"', chunk)
        if im and 'loc:"' not in chunk:
            nolocev.add(im.group(1))
ok('無 loc 事件 48 單（v20a203：18 舊＋18 v193 新 day＋12 v203 新 day）', len(nolocev) == 48)
leftover = set()
ok('48 單無 loc＝48 覆寫＋0 留灰（v20a203 新 day 事件入埋表）',
   nolocev == set(table) | leftover)
ok('st05／st08 喺覆寫表（v20a146 補圖，無留灰）',
   {'wf4_ev_st05', 'wf4_ev_st08'} <= set(table))

# --- 場景檔存在 ---
for ev, url in sorted(table.items()):
    f = url.split('?')[0]
    ok('場景檔存在：%s → %s' % (ev, f), os.path.isfile(os.path.join(root, f)))

# --- wf4Scene105 優先查覆寫表 ---
fm = re.search(r'function wf4Scene105\(ev\)\{(.*?)\n\}', html, re.S)
ok('wf4Scene105 存在', fm is not None)
body = fm.group(1) if fm else ''
ok('wf4Scene105 先查覆寫表（喺 locId fallback 之前）',
   body.find('WF4_SCENE_OVERRIDE134') != -1
   and body.find('WF4_SCENE_OVERRIDE134') < body.find('const locId'))
ok('wf4Scene105 保留舊 fallback（有 loc 事件／atLoc）',
   'LOC_SHEET_BG[locId]' in body)

# --- v133 唔郁 ---
ok('v133 舞台 viewport-aware 唔郁（min(480px,52dvh)）',
   'min-height:min(480px,52dvh)' in html)
ok('對話框定高 118px 唔郁（B4）',
   '.story-play .dlg106-plate{height:118px;min-height:118px;max-height:118px;flex:1}' in html)

# --- 新圖 3 張齊晒＋格式 ---
for f in ['bg_wf4_home.jpg', 'bg_wf4_booth.jpg', 'bg_wf4_market.jpg',
          'bg_wf4_karaoke.jpg', 'bg_wf4_taxi.jpg']:
    p = os.path.join(root, 'assets/story/locs', f)
    ok('新場景圖存在：' + f, os.path.isfile(p))
    if os.path.isfile(p):
        from PIL import Image
        im = Image.open(p)
        ok('新場景圖 720×1280：' + f, im.size == (720, 1280))

print('TOTAL ' + ('PASS' if not fails else 'FAIL %d' % len(fails)))
sys.exit(1 if fails else 0)
