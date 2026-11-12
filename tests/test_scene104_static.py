# -*- coding: utf-8 -*-
# v20a104 SCENE104 靜態測試：灣仔唱片場景圖補強（譜架／磁帶櫃空間／推光）＋背景版本參數升 20a104。
# 反證：喺 v20a103 index 上行會 FAIL（版本參數仍係 20a103、灣仔圖 sha 仍係舊版 eedd38e1f9e6）。
# 用法：python3 tests/test_scene104_static.py [path-to-index.html]
import hashlib, re, struct, sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
root = p.resolve().parent
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／產品 ?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

LOCS15 = ['cafe_cha','agency_ho','film_lion','film_cotton','film_harbour','tvb_longmen',
          'tvb_kowloon','tvb_harbour','ad_central','ad_adm','rec_hk','rec_wanchai','rec_star',
          'gift_shop','hospital']
FILES16 = ['bg_c1_tea_restaurant'] + ['bg_loc_' + x for x in LOCS15]

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

# --- (1) 版本參數：全域冇 ?v=20a103 殘留；兩處載入點都係 20a104 ---
ok('index 冇 ?v=20a103 殘留', '?v=20a103' not in src)
# v20a118 LOCPANEL118：廟街禮品＋仁康醫院場景圖補齊（另一統籌一次生成，QC 全 pass），
# LOC_SHEET_BG 13→15，?v=20a104 共 18 處（builder 1＋LOC_SHEET_BG 15＋v134 WF4 覆寫表重用 2：set08→bg_loc_film_lion、st04→bg_loc_cafe_cha）。
ok('index ?v=20a104 共 18 處（builder 1＋LOC_SHEET_BG 15＋v134 重用 2）', src.count('?v=20a104') == 18)

m = re.search(r'const LOC_SHEET_BG = \{(.*?)\n\};', src, re.S)
ok('搵到 LOC_SHEET_BG', bool(m))
if m:
    block = m.group(1)
    for loc in LOCS15:
        ok(f'LOC_SHEET_BG[{loc}] 指檔 ?v=20a104',
           f'{loc}:"assets/story/locs/bg_loc_{loc}.jpg?v=20a104"' in block)

m2 = re.search(r'function spBgImageCandidates\(bgKey\)\{(.*?)\n  \}', src, re.S)
ok('搵到 spBgImageCandidates', bool(m2))
if m2:
    body = m2.group(1)
    ok('locs 候選用 ?v=20a104', '"assets/story/locs/"+key+"."+ext+"?v=20a104"' in body)
    ok('locs 候選冇 ?v=20a103', '?v=20a103' not in body)

# --- (2) 灣仔唱片補強圖：規格啱、新 sha、唔係舊圖 ---
EXPECT_SHA = {
 'bg_c1_tea_restaurant': 'f2e2b5f1b1b4', 'bg_loc_ad_adm': '4de831ad58b4',
 'bg_loc_ad_central': 'e8082fce12ad', 'bg_loc_agency_ho': '330c2651751a',
 'bg_loc_cafe_cha': '55e62774d698', 'bg_loc_film_cotton': 'aeabc65ebe1a',
 'bg_loc_film_harbour': '648271810d59', 'bg_loc_film_lion': 'cbd6b3b8d464',
 'bg_loc_rec_hk': '8bd6f8a39286', 'bg_loc_rec_star': '07c59b102bff',
 'bg_loc_rec_wanchai': 'c49279626197', 'bg_loc_tvb_harbour': '2d828b1afeeb',
 'bg_loc_tvb_kowloon': '5fdf5cb66638', 'bg_loc_tvb_longmen': 'dc8132dc12c5',
 'bg_loc_gift_shop': '022d39114c11', 'bg_loc_hospital': '77d0837447fc',
}
for key in FILES16:
    f = root / 'assets' / 'story' / 'locs' / (key + '.jpg')
    ok(f'{key}.jpg 存在', f.exists())
    if not f.exists(): continue
    data = f.read_bytes()
    ok(f'{key}.jpg 尺寸 720×1280', jpeg_size(data) == (720, 1280))
    ok(f'{key}.jpg sha 對版', hashlib.sha256(data).hexdigest()[:12] == EXPECT_SHA[key])
w = root / 'assets' / 'story' / 'locs' / 'bg_loc_rec_wanchai.jpg'
if w.exists():
    ok('灣仔圖唔再係 v103 舊圖', hashlib.sha256(w.read_bytes()).hexdigest()[:12] != 'eedd38e1f9e6')

print('---')
print('SCENE104 STATIC: ' + ('ALL PASS' if not fails else f'{len(fails)} FAIL'))
sys.exit(1 if fails else 0)
