# -*- coding: utf-8 -*-
# v20a97 MAP97 靜態測試：大地圖換 v6 全圖重畫定版（資產檔）＋地區名細字層。
# 反證：喺 v20a96 index 上行會 FAIL（MAP_IMG 仍係內嵌 data URI、冇 hk_map_v6.jpg、冇地區層）。
# 用法：python3 tests/test_map97_static.py [path-to-index.html]
import re, struct, sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
root = p.resolve().parent
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- (1) 換圖：MAP_IMG 改指 v6 資產檔 ---
ok('MAP_IMG 指向 assets/hk_map_v6.jpg', 'const MAP_IMG = "assets/hk_map_v6.jpg";' in src)
ok('MAP_IMG 唔再係內嵌 data URI', 'const MAP_IMG = "data:image' not in src)
asset = root / 'assets' / 'hk_map_v6.jpg'
ok('assets/hk_map_v6.jpg 存在', asset.exists())
data = asset.read_bytes() if asset.exists() else b''
ok('資產係 JPEG（FFD8 開頭）', data[:2] == b'\xff\xd8')
ok('資產唔硬減（>700,000 bytes；實檔 q88＝793,164）', len(data) > 700000)

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
ok('資產尺寸＝1376×1824（同 v3 同座標系）', jpeg_size(data) == (1376, 1824))
ok('舊圖資產保留唔刪（hk_map.jpg／hk_map_full.jpg 仍在）',
   (root / 'assets' / 'hk_map.jpg').exists() and (root / 'assets' / 'hk_map_full.jpg').exists())
ok('fallback 仍指現存舊圖（MAP_IMG 未定義時唔會 404）', '"assets/hk_map.jpg"' in src)

# --- (2) 地點標籤沿用：15 個 .mn68 原封 ---
mn = re.findall(r'<div class="mn68"[^>]*>([^<]+)</div>', src)
ok('方案 B 地點標籤恰好 15 個', len(mn) == 15)
ok('15 個地點名齊（同 v96 一致）', set(mn) == {
    '獅子山製片', '香江唱片', '星河電視台', '九龍電視台', '海港廣播', '紅棉影業', '維港電影',
    '中環廣告', '金鐘創意', '灣仔唱片', '天星音樂', '金龍茶餐廳', '何生事務所', '廟街禮品', '仁康醫院'})

# --- (3) LOCS 座標零改動（釘位／熱區沿用） ---
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
ok('LOCS 15 地點座標同 v96 逐一一致', locs_ok and len(re.findall(r'\{ id:"', src.split('const NPCS')[0].split('const LOCS')[1])) == 15)

# --- (4) 地區名細字層 ---
ok('地區層容器存在（map-districts97）', 'id="map-districts97"' in src)
i_names = src.find('id="map-names68"'); i_dist = src.find('id="map-districts97"'); i_stage_end = src.find('map-polaroid', i_dist)
ok('地區層喺 map-stage 內、名稱層之後', 0 < i_names < i_dist)
md = re.findall(r'<div class="md97"[^>]*>([^<]+)</div>', src)
ok('地區名恰好 12 個', len(md) == 12)
ok('地區名清單正確', set(md) == {
    '中環', '金鐘', '灣仔', '銅鑼灣', '尖沙咀', '紅磡', '油麻地', '旺角', '九龍城', '鑽石山', '清水灣', '薄扶林'})
ok('地區層 pointer-events:none（唔擋熱區）', '.map-districts97{ position:absolute; inset:0; pointer-events:none;' in src)
ok('地區名 pointer-events:none', bool(re.search(r'\.md97\{[^}]*pointer-events:none', src)))
m_md = re.search(r'\.md97\{[^}]*font-size:([\d.]+)px', src)
m_mn = re.search(r'\.mn68\{[^}]*font-size:([\d.]+)px', src)
ok('地區名字體細過地點名（細字層唔搶主標籤）',
   bool(m_md and m_mn) and float(m_md.group(1)) < float(m_mn.group(1)))
ok('地區名係 app 排字（圖檔路徑冇地區名、層係 HTML div）', 'map-districts97' in src and 'hk_map_v6_districts' not in src)

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
