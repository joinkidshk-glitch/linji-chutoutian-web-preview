# -*- coding: utf-8 -*-
# v20a103 SCENE103 靜態測試：地點場景圖年代重製（14 張換新圖）＋載入指向改版（繞快取）。
# 反證：喺 v20a101 index 上行會 FAIL（LOC_SHEET_BG 大半指 UI40_SCENE、locs 版本參數仍係 20a8、
#       spBgImageCandidates 係 UI40 行先；14 張圖檔 sha 同舊版）。
# 用法：python3 tests/test_scene103_static.py [path-to-index.html]
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

LOCS13 = ['cafe_cha','agency_ho','film_lion','film_cotton','film_harbour','tvb_longmen',
          'tvb_kowloon','tvb_harbour','ad_central','ad_adm','rec_hk','rec_wanchai','rec_star']
FILES14 = ['bg_c1_tea_restaurant'] + ['bg_loc_' + x for x in LOCS13]

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

# --- (1) 14 張新圖齊、規格啱、唔係舊圖（sha 對重製留檔）---
EXPECT_SHA = {
 'bg_c1_tea_restaurant': 'f2e2b5f1b1b4', 'bg_loc_ad_adm': '4de831ad58b4',
 'bg_loc_ad_central': 'e8082fce12ad', 'bg_loc_agency_ho': '330c2651751a',
 'bg_loc_cafe_cha': '55e62774d698', 'bg_loc_film_cotton': 'aeabc65ebe1a',
 'bg_loc_film_harbour': '648271810d59', 'bg_loc_film_lion': 'cbd6b3b8d464',
 'bg_loc_rec_hk': '8bd6f8a39286', 'bg_loc_rec_star': '07c59b102bff',
 'bg_loc_rec_wanchai': 'eedd38e1f9e6', 'bg_loc_tvb_harbour': '2d828b1afeeb',
 'bg_loc_tvb_kowloon': '5fdf5cb66638', 'bg_loc_tvb_longmen': 'dc8132dc12c5',
}
for key in FILES14:
    f = root / 'assets' / 'story' / 'locs' / (key + '.jpg')
    ok(f'{key}.jpg 存在', f.exists())
    if not f.exists(): continue
    data = f.read_bytes()
    ok(f'{key}.jpg 係 JPEG', data[:2] == b'\xff\xd8')
    ok(f'{key}.jpg 尺寸 720×1280', jpeg_size(data) == (720, 1280))
    ok(f'{key}.jpg 係重製新圖（sha 對版）', hashlib.sha256(data).hexdigest()[:12] == EXPECT_SHA[key])

# --- (2) LOC_SHEET_BG：13 個 locId 全部改指新檔＋?v=20a103，冇 UI40 殘留 ---
m = re.search(r'const LOC_SHEET_BG = \{(.*?)\n\};', src, re.S)
ok('搵到 LOC_SHEET_BG', bool(m))
if m:
    block = m.group(1)
    ok('LOC_SHEET_BG 冇 UI40_SCENE 引用', 'UI40_SCENE' not in block)
    for loc in LOCS13:
        ok(f'LOC_SHEET_BG[{loc}] 指新檔 ?v=20a103',
           f'{loc}:"assets/story/locs/bg_loc_{loc}.jpg?v=20a103"' in block)

# --- (3) spBgImageCandidates：檔案鏈行先、locs 版本 20a103、UI40 退後備 ---
m2 = re.search(r'function spBgImageCandidates\(bgKey\)\{(.*?)\n  \}', src, re.S)
ok('搵到 spBgImageCandidates', bool(m2))
if m2:
    body = m2.group(1)
    ok('locs 候選用 ?v=20a103', '"assets/story/locs/"+key+"."+ext+"?v=20a103"' in body)
    ok('locs 候選唔再用 ?v=20a8', '?v=20a8' not in body)
    i_file = body.find('assets/story/locs/')
    i_ui40 = body.find('UI40_SCENE[sk40]')
    ok('檔案候選排喺 UI40 內嵌圖之前', 0 <= i_file < i_ui40)

print('---')
print('SCENE103 STATIC: ' + ('ALL PASS' if not fails else f'{len(fails)} FAIL'))
sys.exit(1 if fails else 0)
