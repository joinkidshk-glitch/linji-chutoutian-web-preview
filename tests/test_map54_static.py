# v20a54 大地圖紙面填充＋預解碼 靜態測試。
# 用法：python3 tests/test_map54_static.py [path-to-index.html]
# v20a106 更新（QA 工人 D）：DLG106 對話皮膚段合法追加喺 v76 段之後，v54 完結標記
# 被推出舊 2500 字尾窗——「last skin」斷言改驗「v54 後只有已知後繼段（v20a76＋
# v20a106 DLG106）先到 </style>」，保留偵測未知皮膚追加嘅原意，唔再用死字數窗。
# v20a108 更新：DLG108 對話舞台微調段合法追加（遮腿＋60%＋自動收細＋定高＋文字鏈），
# 已知後繼段加 v20a108，要求埋 DLG108 完結標記。
# v20a119 更新：DLG119 剪影 CSS 段合法追加（光暈層＋「影」黑卡，喺 DLG106 段內、
# DLG106 完結標記之前），已知後繼段加 v20a119，要求埋 DLG119 完結標記。
# v20a131 更新：UI131 B批 CSS 段合法追加（B2 事業 tab 筆記紙＋B4 對話框短句置中，
# 喺 v128 A6 段之後、</style> 之前），已知後繼段加 v20a131。
import sys

path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
html = open(path, encoding='utf-8').read()
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def seg(start, end=None, src=None):
    src = html if src is None else src
    try:
        i = src.index(start)
    except ValueError:
        return ''
    try:
        j = src.index(end, i) if end else len(src)
    except ValueError:
        j = len(src)
    return src[i:j]

v54 = seg('/* === v20a54 新 UI 皮膚層', '/* === v20a54 完 === */')
ok('v54 segment present', bool(v54))
try:
    _between = html[html.index('/* === v20a54 完 === */'):html.index('</style>')]
    _segs_after = [s.split('===')[0] for s in _between.split('/* === ')[1:]
                   if 'v20a54 完' not in s]
    _last = bool(_segs_after) and all(('v20a76' in s or 'v20a106' in s or 'v20a108' in s or 'v20a119' in s or 'v20a128' in s or 'v20a131' in s) for s in _segs_after) \
        and 'v20a106 DLG106 完' in _between and 'v20a108 DLG108 完' in _between and 'v20a119 DLG119 完' in _between
except ValueError:
    _last = False
ok('v54 segment followed only by known skins (v76+dlg106+dlg108+dlg119+v128+v131) before </style>', _last)

# ---- 1. 紙面填充（只准油漆屬性） ----
wrap = seg('#app .map-wrap{', '}', v54)
ok('wrap paper rule inside v54', bool(wrap))
ok('wrap has compass SVG layer', "data:image/svg+xml" in wrap and '香江' in wrap)
ok('wrap has fiber gradients + cream radial', 'repeating-linear-gradient(93deg' in wrap and 'radial-gradient(' in wrap and '#f6ead2' in wrap)
ok('wrap rule is background-only (no layout props)', not any(k in wrap for k in ('margin:', 'padding:', 'flex:', 'height:', 'width:', 'position:', 'display:')))
pol = seg('#app .map-polaroid{', '}', v54)
ok('polaroid inner frame is box-shadow only', 'box-shadow' in pol and 'inset 0 0 0 6px' in pol and not any(k in pol for k in ('margin:', 'padding:', 'flex:', 'height:', 'width:')))
ok('well paper backing', '#app .map-well{ background:#f3e7c9 !important; }' in v54)
ok('stage paper backing', '#app .map-stage{ background:#f3e7c9 !important; }' in v54)
ok('img paper backing', '#app .map-img{ background:#f3e7c9; }' in v54)

# ---- 2. v20a43 舞台幾何定案原封（紅線） ----
v43 = seg('/* === v20a43 新 UI 皮膚層', '/* === v20a43 皮膚層完 === */')
ok('v43 segment present', bool(v43))
ok('v43 stage width/height auto intact', '#app .map-stage{\n  width:100% !important;\n  height:auto !important;\n}' in v43)
ok('v43 img contain intact', 'object-fit:contain !important' in v43 and 'height:auto !important' in v43)
ok('v43 hotzone 52px intact', 'width:52px !important' in v43 and 'height:52px !important' in v43)
ok('v43 area list still hidden (no resurrection)', '#app #map-area-list{ display:none !important; }' in v43)
ok('v43 legend still hidden', '#app #map-legend{ display:none !important; }' in v43)
ok('v54 adds no map-area-list resurrection', 'map-area-list' not in v54)

# ---- 3. 預解碼接線 ----
wire = seg('/* v20a54：開始畫面階段就預解碼', 'catch(_e){}')
ok('predecode wiring present', bool(wire))
ok('predecode calls decode on #map-img', '_mi.decode().catch(()=>{})' in wire)
ok('predecode detached Image too', 'new Image()' in wire and '_pm.decode().catch(()=>{})' in wire)
ok('boot img src wiring intact', 'const _mi=document.getElementById("map-img"); if(_mi){ _mi.onload=' in html)

# ---- 4. 紅線守護（承前版） ----
ok('SAVE key unchanged', 'starVolunteer_map_v19w' in html)
ok('push-door z-15 intact (v51)', '.push-door{' in html)
ok('studio scene embedded (v53)', 'studio:"data:image/jpeg;base64,' in html)
ok('new title present', '<title>臨記埋位' in html)
ok('old name absent player-facing', '臨記出頭天' not in seg('<title>', '</title>'))

print('TOTAL FAILS:', len(fails))
sys.exit(1 if fails else 0)
