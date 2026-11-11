# -*- coding: utf-8 -*-
# v20a105 ENC105 靜態測試：巧遇資產組 D-2（12 星企立接入＋剪影兜底）＋D-3（巧遇背景改行逐地點新場景）。
# 反證：喺 v20a104 index 上行會 FAIL（冇 stand 檔、enc79SceneSrc 冇 LOC_SHEET_BG、候補第一位唔係企立）。
# 用法：python3 tests/test_enc105_static.py [path-to-index.html]
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
ok('SAVE key／softRev／產品 ?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

STARS12 = ['luk_baakyin','liu_bingxing','ngai_wingnaam','yip_manji','mak_zhendong','lok_gasing',
           'pang_siuki','chung_choning','gu_mingfai','so_jiyan','chai_zanhoi','ching_tinlok']
# 審計點名冇圖嗰 6 星（修復前兩邊候補全缺）
MISSING6 = ['mak_zhendong','pang_siuki','chung_choning','gu_mingfai','chai_zanhoi','ching_tinlok']

def png_size_mode(data):
    if data[:8] != b'\x89PNG\r\n\x1a\n': return None
    w, h = struct.unpack('>II', data[16:24])
    return w, h, data[25]  # color type: 6=RGBA, 2=RGB

# --- (1) D-2：12 星企立檔入庫（864×1152，跟 bust pipeline 同規格） ---
for sid in STARS12:
    f = root / 'assets' / 'story' / 'era_stars' / (sid + '_stand_default.png')
    ok(f'{sid} 企立檔存在', f.exists())
    if f.exists():
        info = png_size_mode(f.read_bytes())
        ok(f'{sid} 企立檔 864×1152 PNG', info is not None and info[0] == 864 and info[1] == 1152)
for sid in MISSING6:
    ok(f'原本冇圖星 {sid} 已補企立', (root / 'assets' / 'story' / 'era_stars' / (sid + '_stand_default.png')).exists())
sil = root / 'assets' / 'story' / 'era_stars' / 'enc105_stand_silhouette.png'
ok('中性剪影兜底檔存在', sil.exists())
if sil.exists():
    info = png_size_mode(sil.read_bytes())
    ok('剪影檔 864×1152 RGBA PNG', info is not None and info[0] == 864 and info[1] == 1152 and info[2] == 6)

# --- (2) D-2：候補次序（企立第一、bust 後備、剪影＋data URI 兜底） ---
m = re.search(r'function enc79StandCandidates\(starId\)\{(.*?)\n\}', src, re.S)
ok('搵到 enc79StandCandidates', bool(m))
if m:
    body = m.group(1)
    i_stand = body.find('_stand_default.png?v=20a105')
    i_bust = body.find('_bust_default.png?v=20a8')
    ok('候補含企立路徑 ?v=20a105', i_stand >= 0)
    ok('企立排喺 bust 之前', 0 <= i_stand < i_bust)
    ok('候補尾段有入庫剪影檔', 'ENC105_STAND_SILHOUETTE' in body)
    ok('候補最尾有 data URI 兜底', 'ENC105_STAND_FALLBACK' in body)
ok('兜底常數係內嵌 SVG data URI', 'const ENC105_STAND_FALLBACK = "data:image/svg+xml' in src)
ok('入庫剪影常數指向真檔', 'const ENC105_STAND_SILHOUETTE = "assets/story/era_stars/enc105_stand_silhouette.png?v=20a105"' in src)
_pi = src.index('function enc79PlayEncounter')
seg = src[src.index('const tryNext', _pi):src.index('const tryNext', _pi) + 300] if 'const tryNext' in src[_pi:] else ''
ok('候補行晒改落剪影兜底（唔再 display:none 隱藏）',
   'ENC105_STAND_FALLBACK' in seg and 'display="none"' not in seg)

# --- (3) D-3：場景函數來源次序（LOC_SHEET_BG 行先、UI40 退兜底） ---
m2 = re.search(r'function enc79SceneSrc\(locId\)\{(.*?)\n\}', src, re.S)
ok('搵到 enc79SceneSrc', bool(m2))
if m2:
    body = m2.group(1)
    i_loc = body.find('LOC_SHEET_BG[locId]')
    i_ui40 = body.find('UI40_BG_BY_KEY')
    ok('場景函數查 LOC_SHEET_BG', i_loc >= 0)
    ok('LOC_SHEET_BG 排喺 UI40 類別圖之前', 0 <= i_loc < i_ui40)
    ok('UI40 studio 保留做最後兜底', 'UI40_SCENE.studio' in body)

# --- (4) LOC_SHEET_BG 本體冇被今包改爛（13 地點仍指 v104 逐地點檔） ---
LOCS13 = ['cafe_cha','agency_ho','film_lion','film_cotton','film_harbour','tvb_longmen',
          'tvb_kowloon','tvb_harbour','ad_central','ad_adm','rec_hk','rec_wanchai','rec_star']
m3 = re.search(r'const LOC_SHEET_BG = \{(.*?)\n\};', src, re.S)
ok('搵到 LOC_SHEET_BG', bool(m3))
if m3:
    block = m3.group(1)
    for loc in LOCS13:
        ok(f'LOC_SHEET_BG[{loc}] 仍指逐地點檔', f'{loc}:"assets/story/locs/bg_loc_{loc}.jpg?v=20a104"' in block)
        ok(f'bg_loc_{loc}.jpg 實檔存在', (root / 'assets' / 'story' / 'locs' / f'bg_loc_{loc}.jpg').exists())

print('---')
print('ENC105 STATIC: ' + ('ALL PASS' if not fails else f'{len(fails)} FAIL'))
sys.exit(1 if fails else 0)
