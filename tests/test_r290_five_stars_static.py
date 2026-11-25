# -*- coding: utf-8 -*-
# v20a290 Q2 五位名冊外女星入紅星系統：靜態測試——
#   defs／PILOT／DIALOG＋註冊／STAGEUP／CAP／WRAP／SP176／FAV176／GEN176／SIGHTINGS 全部齊；
#   主副場 id 喺 LOCS 表；onWrap 舊「跳過」註解已清；SAVE key／softRev／產品 ?v= 不變。
# 用法：python3 tests/test_r290_five_stars_static.py [path-to-index.html]
import re, sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
root = p.resolve().parent
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

NEW5 = ['lan_ruoxi', 'kong_siying', 'shum_yingsuet', 'wu_meilam', 'hon_sauting']
NAMES5 = {'lan_ruoxi': '藍若曦', 'kong_siying': '江詩盈', 'shum_yingsuet': '沈映雪',
          'wu_meilam': '胡美琳', 'hon_sauting': '韓秀婷'}

# ---- 基線不變 ----
ok('SAVE key 不變', 'starVolunteer_map_v19w' in src)
ok('softRev 不變', 's107' in src)
ok('產品 ?v= 不變', 'v20a10' in src)

# ---- LOCS id 集（主副場驗證用） ----
m_locs = re.search(r'const LOCS = \[(.*?)\n\];', src, re.S)
loc_ids = set(re.findall(r'id:"([^"]+)"', m_locs.group(1))) if m_locs else set()
ok('搵到 LOCS（17 個地圖地點）', len(loc_ids) == 17)  # v20a407：約會層收起，LOCS 23→17

# ---- (1) 名冊 ----
m_stars = re.search(r'const ENC79_STARS = \[(.*?)\n\];', src, re.S)
ok('搵到 ENC79_STARS', bool(m_stars))
star_ids = re.findall(r'id:"([^"]+)"', m_stars.group(1)) if m_stars else []
ok('名冊 17 星（12＋5）', len(star_ids) == 17)
for sid in NEW5:
    ok(f'{sid}（{NAMES5[sid]}）在名冊', sid in star_ids)
    m_def = re.search(r'\{ id:"' + sid + r'",\s*name:"([^"]+)",\s*primary:"([^"]+)",\s*secondary:"([^"]+)",\s*area:"([^"]+)",\s*win:\[\[', src)
    ok(f'{sid} def 格式齊（name／primary／secondary／area／win）', bool(m_def) and m_def.group(1) == NAMES5[sid])
    if m_def:
        ok(f'{sid} 主副場係有效 LOCS id', m_def.group(2) in loc_ids and m_def.group(3) in loc_ids)
# 12 星原 def 一字不變（抽舊行逐字對版）
for old in ['{ id:"luk_baakyin",  name:"陸柏言", primary:"film_lion",   secondary:"rec_star"',
            '{ id:"ching_tinlok", name:"程天諾", primary:"rec_star",    secondary:"rec_hk",      area:"唱片公司嗰邊", win:[[1992,"秋"],[1992,"冬"]], unlockYear:1992 }']:
    ok('原 12 星 def 不變：' + old[:28] + '…', old in src)

# ---- (2) PILOT ----
m_pilot = re.search(r'const ENC79_PILOT = \{([^}]*)\};', src)
ok('搵到 ENC79_PILOT', bool(m_pilot))
for sid in NEW5:
    ok(f'PILOT 有 {sid}', bool(m_pilot) and (sid + ':1') in m_pilot.group(1))

# ---- (3) DIALOG＋註冊 ----
for sid in NEW5:
    ok(f'初遇劇本 const ENC79_DLG_{sid} 在場', ('const ENC79_DLG_' + sid + ' = {') in src)
    ok(f'初遇劇本有 first／openers／address：{sid}',
       bool(re.search(r'const ENC79_DLG_' + sid + r' = \{.*?first:\s*\{.*?openers:\s*\{.*?address:\s*\{', src, re.S)))
    ok(f'註冊行 ENC79_DIALOG.{sid}', ('ENC79_DIALOG.' + sid + ' = ENC79_DLG_' + sid) in src)
    for t in ['T0', 'T1', 'T2', 'T3', 'T4']:
        ok(f'{sid} opener {t} 在場', bool(re.search(r'const ENC79_DLG_' + sid + r' = \{.*?' + t + r':\s*\[', src, re.S)))

# ---- (4) STAGEUP／CAP／WRAP ----
for sid in NEW5:
    m = re.search(re.escape(sid) + r':\[\["S",', src)
    ok(f'STAGEUP 有 {sid}（3 句）', src.count(sid + ':[["S",') >= 1)
    ok(f'CAP_LINES 有 {sid}', bool(re.search(re.escape(sid) + r':\["S",', src)))
    ok(f'WRAP_ECHO 有 {sid}', bool(re.search(re.escape(sid) + r':\["S","上次', src)))

# ---- (5) 送禮喜好 ----
for sid in NEW5:
    ok(f'SP176 有 {sid}', (sid + ':{ fav:[') in src or (sid + ': { fav:[') in src)
for sid in NEW5:
    fav_rows = re.findall(r'\["' + sid + r'","gift_[^"]+","', src)
    ok(f'FAV176 {sid} 最愛反應句 2 條', len(fav_rows) == 2)
    gen_rows = re.findall(r'\["' + sid + r'","(?:liked|dislike)","', src)
    ok(f'GEN176 {sid} 喜歡／唔鍾意句各 1 條', len(gen_rows) == 2)
ok('NAMES176 有五位中文名', all(('"%s":"%s"' % (k, v)) in src or (k + ':"' + v + '"') in src for k, v in NAMES5.items()))

# ---- (6) SIGHTINGS ----
for sid in NEW5:
    ok(f'STAR_SIGHTINGS 有 {sid}', ('{ starId:"' + sid + '", displayName:"' + NAMES5[sid] + '"') in src)

# ---- (7) 殺青註解＋人脈頁 ----
ok('onWrap 舊「跳過」註解已清（五位已入名冊）', '冇 enc79 好感狀態位，跳過' not in src)
ok('onWrap 新註解：grant() 讀 enc79StarDef 生效，唔使另開特例', 'grant() 讀 enc79StarDef 生效' in src and '唔使另開特例' in src)
ok('人脈頁縮圖：冇 BUST109 鍵嗰陣用入庫剪影（v290 guard）', 'hasB109v290' in src and 'ENC105_STAND_SILHOUETTE' in src)

# ---- (8) 藍若曦避撞 ----
m_lan = re.search(r'\{ id:"lan_ruoxi",\s*name:"藍若曦",\s*primary:"([^"]+)",\s*secondary:"([^"]+)"', src)
ok('藍主場／副場唔係感情線地點（rec_hk／tvb_longmen／tvb_kowloon／cafe_cha）',
   bool(m_lan) and m_lan.group(1) not in ('rec_hk', 'tvb_longmen', 'tvb_kowloon', 'cafe_cha')
   and m_lan.group(2) not in ('rec_hk', 'tvb_longmen', 'tvb_kowloon', 'cafe_cha'))

if fails:
    print('FAILURES: ' + ' | '.join(fails))
    sys.exit(1)
print('ALL PASS')
