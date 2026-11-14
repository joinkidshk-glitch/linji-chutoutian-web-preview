# v20a204 補女星入獎池＋提名人性別分流 static tests：
# (1) 入池：POSTER59_STAR_IDS 加 3 名；AWARDS63_POOL music＋2、film＋1；權重三位 ×3。
# (2) 性別分流：AWARDS204_FEMALE_STARS 7 位；awards63Fellows 第三參數 gender＋逐類別 seed；
#     第一輪／第二輪／高俊傑三處有性別閘。
# (3) buildAwardResultPack 逐類別計 fellows（c.gender／c.id），唔再全 pack 共用同一份；
#     類別物件帶 gender。
# (4) 舞台 px：新星 9 檔齊（3 人 × south／east／west），128×128、腳底 y115、高 102px。
# (5) 硬規則：SAVE key 不變；softRev／?v= 不變；LEADSTAR59 唔加新星；唔改 content pack JSON。
# 反證：對 pristine main 行 → v204 條款唔存在 → 乾淨 FAIL（exit 1，唔 crash）。
import sys, os
from PIL import Image

idx_path = sys.argv[1] if len(sys.argv) > 1 else 'index.html'
src = open(idx_path, encoding='utf-8').read()
fails = []

def chk(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond:
        fails.append(name)

def slice_fn(name):
    i = src.find('function ' + name + '(')
    if i < 0: return ''
    depth = 0
    j = src.find('{', i)
    for k in range(j, len(src)):
        if src[k] == '{': depth += 1
        elif src[k] == '}':
            depth -= 1
            if depth == 0: return src[i:k+1]
    return ''

def slice_const(name):
    i = src.find('const ' + name + ' =')
    if i < 0: return ''
    depth = 0
    started = False
    for k in range(i, len(src)):
        ch = src[k]
        if ch in '{[': depth += 1; started = True
        elif ch in '}]':
            depth -= 1
            if started and depth == 0: return src[i:k+1]
        elif ch == ';' and not started:
            return src[i:k+1]
    return ''

fellows_fn = slice_fn('awards63Fellows')
build_fn = slice_fn('buildAwardResultPack')
pool = slice_const('AWARDS63_POOL')
weights = slice_const('AWARDS63_TIER_WEIGHT')
star_ids = slice_const('POSTER59_STAR_IDS')
female = slice_const('AWARDS204_FEMALE_STARS')
leadstar = slice_const('LEADSTAR59')

# --- (1) 入池 ---
chk('v204 標記喺 awards63Fellows／pool 附近', 'v20a204' in src)
chk('POSTER59_STAR_IDS 加藍若曦／沈映雪／江詩盈', all(x in star_ids for x in
    ['"藍若曦": "lan_ruoxi"', '"沈映雪": "shum_yingsuet"', '"江詩盈": "kong_siying"']))
chk('音樂池加 lan_ruoxi＋shum_yingsuet', 'lan_ruoxi' in pool and 'shum_yingsuet' in pool)
chk('電影池加 kong_siying', 'kong_siying' in pool)
chk('權重三位都係 ×3', all(x in weights for x in ['lan_ruoxi: 3', 'shum_yingsuet: 3', 'kong_siying: 3']))

# --- (2) 性別分流 ---
chk('AWARDS204_FEMALE_STARS 在位', 'const AWARDS204_FEMALE_STARS' in src)
chk('女性集齊 7 位 id', all(x in female for x in
    ['so_jiyan', 'chung_choning', 'ngai_wingnaam', 'yip_manji', 'lan_ruoxi', 'shum_yingsuet', 'kong_siying']))
chk('awards63Fellows 簽名加 gender＋catId（舊 2 參呼叫兼容）',
    'function awards63Fellows(ceremony, year, gender, catId)' in src)
chk('第一輪有性別閘', 'genderOk204(c.starId)' in fellows_fn)
chk('第二輪池先按性別過濾', 'poolAll.filter' in fellows_fn and 'awards204StarGender' in fellows_fn)
chk('高俊傑唔入女獎（gender !== "f" 閘）', 'gender !== "f"' in fellows_fn)
chk('seed 加 gender／catId（每類別獨立）', 'seedParts204' in fellows_fn and 'catId' in fellows_fn)

# --- (3) build pack 逐類別計 ---
chk('類別物件帶 gender', 'gender: cat.gender' in build_fn)
chk('逐類別計 fellows（唔再共用同一份）',
    'awards63Fellows(ceremony, year, c.gender || "", c.id)' in build_fn)
chk('冇全 pack 共用一份嘅舊寫法', 'const fl63 = ' not in build_fn)

# --- (4) 舞台 px：新星 9 檔齊，錨尺寸 ---
PX_DIR = os.path.join(os.path.dirname(os.path.abspath(idx_path)), 'assets', 'story', 'awards')
missing, bad_geo = [], []
for sid in ['lan_ruoxi', 'shum_yingsuet', 'kong_siying']:
    for d in ('south', 'east', 'west'):
        p = os.path.join(PX_DIR, 'px_%s_%s.png' % (sid, d))
        if not os.path.isfile(p):
            missing.append(p); continue
        im = Image.open(p).convert('RGBA')
        bb = im.getchannel('A').getbbox()
        if im.size != (128, 128) or not bb or bb[3] != 115 or bb[3] - bb[1] != 102:
            bad_geo.append((os.path.basename(p), im.size, bb))
chk('新星 px 9 檔齊（3 人 × south／east／west）', not missing)
if missing: print('  missing:', missing)
chk('新星 px 全部 128×128、腳底 y115、高 102px', not bad_geo)
if bad_geo: print('  bad_geo:', bad_geo)

# --- (5) 硬規則 ---
chk('SAVE key 不變', 'starVolunteer_map_v19w' in src)
chk('LEADSTAR59 唔加新星（只經第二輪入 fellows）',
    'lan_ruoxi' not in leadstar and 'shum_yingsuet' not in leadstar and 'kong_siying' not in leadstar)
chk('softRev 不變（s107）', 's107' in src)
chk('?v= 不變（v20a10）', 'v20a10' in src)

print('')
print('FAILED: %d' % len(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
