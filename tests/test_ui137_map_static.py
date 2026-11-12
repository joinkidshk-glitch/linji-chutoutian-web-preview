# -*- coding: utf-8 -*-
# v20a137 MAP137 靜態測試：地圖 cover 放大＋拎走地區名細字層。
# 反證：喺 v135 index 上行會 FAIL（仲係 contain、冇 cover 換算、地區名 12 個）。
# 用法：python3 tests/test_ui137_map_static.py [path-to-index.html]
import re, struct, sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
root = p.resolve().parent
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

def seg(start, end=None):
    try:
        i = src.index(start)
    except ValueError:
        return ''
    try:
        j = src.index(end, i) if end else len(src)
    except ValueError:
        j = len(src)
    return src[i:j]

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)
ok('MAP_IMG 仍指 assets/hk_map_v6.jpg（唔裁源圖）', 'const MAP_IMG = "assets/hk_map_v6.jpg";' in src)
asset = root / 'assets' / 'hk_map_v6.jpg'
ok('assets/hk_map_v6.jpg 存在', asset.exists())
data = asset.read_bytes() if asset.exists() else b''
def jpeg_size(b):
    i = 2
    while i < len(b) - 9:
        if b[i] != 0xFF: i += 1; continue
        m = b[i + 1]
        if m in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack('>HH', b[i + 5:i + 9])
            return w, h
        if m in (0xD8, 0x01) or 0xD0 <= m <= 0xD9:
            i += 2; continue
        ln = struct.unpack('>H', b[i + 2:i + 4])[0]
        i += 2 + ln
    return None
ok('資產尺寸仍＝1376×1824（冇裁過）', jpeg_size(data) == (1376, 1824))
ok('冇新地圖資產（唔裁源圖，唔加檔）', not (root / 'assets' / 'hk_map_v7.jpg').exists()
   and not (root / 'assets' / 'hk_map_v6_crop137.jpg').exists())

# --- (1) v137 CSS 層：cover＋舞台 aspect＋object-position ---
v137css = seg('/* === v20a137 MAP137', '/* === v20a137 MAP137 完 === */')
ok('v137 CSS 段存在', bool(v137css))
ok('地圖改 cover', 'object-fit:cover !important' in v137css)
ok('object-position 60% 50%（窗 [~62,~1334] 包晒建築）', 'object-position:60% 50% !important' in v137css)
ok('舞台 aspect-ratio 1270/1824（窗闊 1270px）', 'aspect-ratio:1270/1824 !important' in v137css)
ok('舞台 height:auto（等 ratio 計高，唔俾舊 height:100% 搶）', 'height:auto !important' in v137css)
ok('舞台 max-height:100%（700 短屏唔爆版）', 'max-height:100% !important' in v137css)
ok('polaroid 改 flex:1（食返 wrap 剩位）', '#app .map-polaroid{ flex:1 1 auto !important; }' in v137css)
ok('well 變 flex column 置中（舞台喺框內垂直置中）',
   'display:flex !important' in v137css and 'justify-content:center !important' in v137css)
# v43 舊層原封（唔准偷改舊定案，只准後面蓋過）
v43 = seg('/* === v20a43 新 UI 皮膚層', '/* === v20a43 皮膚層完 === */')
ok('v43 層原封（contain 定案仍在）', 'object-fit:contain !important' in v43
   and '#app .map-stage{\n  width:100% !important;\n  height:auto !important;\n}' in v43)
ok('v137 CSS 段喺 v43／v54 段之後（後來居上）',
   ('/* === v20a137 MAP137' in src) and (src.index('/* === v20a137 MAP137') > src.index('/* === v20a54 完 === */')))

# --- (2) JS：cover 換算＋針／名即場定位 ---
ok('map137CoverTransform 存在', 'function map137CoverTransform()' in src)
ok('map137ImgPctToStagePct 存在', 'function map137ImgPctToStagePct(' in src)
ok('positionMapLabels137 存在', 'function positionMapLabels137()' in src)
ok('drawMap 有 v137 hook（fan-out 後換算）', 'v20a137 MAP137' in src and 'map137CoverTransform()' in src)
ok('drawMap 尾叫 positionMapLabels137', 'positionMapLabels137();' in src)
ok('resize 監聽重畫（viewport 變換算變）', 'resize137' in src)
ok('換算用 natural 尺寸兜底（未 load 都有數）', 'MAP137_NATURAL' in src and '1376' in src and '1824' in src)
ok('換算讀 computed object-position（唔同 CSS 硬抄兩份）', 'getComputedStyle(img)' in src and 'objectPosition' in src)

# --- (3) 地區名拎走、會場標籤保留 ---
md = re.findall(r'<div class="md97"[^>]*>([^<]+)</div>', src)
ok('地區名恰好 0 個', len(md) == 0)
ok('會場標籤恰好一個（金禧大酒店保留）', src.count('<div class="md97 md97-venue99"') == 1 and '>金禧大酒店</div>' in src)
ok('地區層容器仍在（淨低會場標籤）', 'id="map-districts97"' in src)
_dist_seg = src[src.index('id="map-districts97"'):src.index('id="map-districts97"') + 800]
ok('地區層入面淨低金禧大酒店', '金禧大酒店' in _dist_seg and '中環' not in _dist_seg
   and '灣仔' not in _dist_seg and '銅鑼灣' not in _dist_seg)

# --- (4) 地點名 15 個原封、LOCS 零改動 ---
mn = re.findall(r'<div class="mn68"[^>]*>([^<]+)</div>', src)
ok('方案 B 地點標籤恰好 15 個', len(mn) == 15)
ok('15 個地點名齊', set(mn) == {
    '獅子山製片', '香江唱片', '星河電視台', '九龍電視台', '海港廣播', '紅棉影業', '維港電影',
    '中環廣告', '金鐘創意', '灣仔唱片', '天星音樂', '金龍茶餐廳', '何生事務所', '廟街禮品', '仁康醫院'})
EXP_LOCS = {
    'film_lion': (52, 12), 'rec_hk': (30, 24), 'tvb_longmen': (41, 14), 'tvb_kowloon': (37, 45),
    'tvb_harbour': (90, 15), 'film_cotton': (68, 11), 'film_harbour': (80, 18), 'ad_central': (64, 57),
    'ad_adm': (85, 60), 'rec_wanchai': (72, 77), 'rec_star': (81, 82), 'cafe_cha': (15, 16),
    'agency_ho': (24, 86), 'gift_shop': (43, 35), 'hospital': (43, 73)}
locs_ok = True
for lid, (ex, ey) in EXP_LOCS.items():
    line = next((ln for ln in src.split('\n') if f'id:"{lid}"' in ln), '')
    m = re.search(r'x:(\d+), y:(\d+)', line)
    if not m or (int(m.group(1)), int(m.group(2))) != (ex, ey): locs_ok = False
ok('LOCS 15 地點座標零改動（圖 % 係 source of truth）', locs_ok)
ok('熱區仍 52px（v43 定案唔郁）', 'width:52px !important' in v43 and 'height:52px !important' in v43)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
