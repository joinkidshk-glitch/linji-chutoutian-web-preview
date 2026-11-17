# -*- coding: utf-8 -*-
# v20a159 MAP159（B2：約會層＋6 新地點）靜態測試：
# 一、LOCS 23 個（15 原有零改動＋6 新點欄位齊全＋v265 服裝店／屋企 2 新點）
# v20a265 COSTUME265 resync：地點 21→23（片場層 15→17：花園街成衣店／阿偉屋企）；
# 墨字地名 21→23；新點同最近同層舊點距離 ≥7.5%（跨層唔計——兩層永不同時顯示）。
# 二、地圖層切換（片場層 17／約會層 6 新＋茶記＋廟街；切換唔耗額度）
# 三、地點 sheet（bg 對照表 6 行＋404 漸變 fallback＋約會對象列讀 ROM159_WOMEN spots）
# 四、日常用途（tertiary 第三出沒點；p／share／上限／冷卻數字零改動）
# 五、出行額度（入新地點計 1 次；層切換唔計；唔加新豁免）
# 反證：喺 v159 Phase 1 基底（6cc403c）上行會 FAIL（LOCS 仲係 15 個、冇層切換、冇新 bg 行）。
# 用法：python3 tests/test_map159_static.py [path-to-index.html]
import math
import re
import sys
from pathlib import Path
p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / 'index.html'
src = p.read_text(encoding='utf-8')
fails = []
def ok(name, cond):
    print(('PASS ' if cond else 'FAIL ') + name)
    if not cond: fails.append(name)

# --- 基線不變 ---
ok('SAVE key／softRev／?v= 不變', 'starVolunteer_map_v19w' in src and 's107' in src and 'v20a10' in src)

# --- (1) LOCS 23 個：15 原有＋6 新點＋v265 2 新點 ---
m = re.search(r'const LOCS = \[(.*?)\n\];', src, re.S)
ok('搵到 LOCS', bool(m))
locs_seg = m.group(1) if m else ''
entries = re.findall(r'\{ id:"(\w+)",(.*?)\},', locs_seg, re.S)
ids = [e[0] for e in entries]
ok('LOCS 23 個（15＋6＋2）', len(ids) == 23)
EXP15 = {
    'film_lion': (52, 12), 'rec_hk': (30, 24), 'tvb_longmen': (41, 14), 'tvb_kowloon': (37, 45),
    'tvb_harbour': (90, 15), 'film_cotton': (68, 11), 'film_harbour': (80, 18), 'ad_central': (64, 57),
    'ad_adm': (85, 60), 'rec_wanchai': (72, 77), 'rec_star': (81, 82), 'cafe_cha': (15, 16),
    'agency_ho': (24, 86), 'gift_shop': (43, 35), 'hospital': (43, 73)}
def fields(block):
    out = {}
    for k in ('name', 'area', 'type', 'region', 'desc', 'layer'):
        mm = re.search(k + r':"([^"]*)"', block)
        if mm: out[k] = mm.group(1)
    for k in ('x', 'y'):
        mm = re.search(k + r':(\d+)', block)
        if mm: out[k] = int(mm.group(1))
    return out
by_id = {e[0]: fields(e[1]) for e in entries}
ok('15 個原有地點 id 齊', all(k in by_id for k in EXP15))
locs15_ok = all(by_id.get(k, {}).get('x') == v[0] and by_id.get(k, {}).get('y') == v[1]
                for k, v in EXP15.items())
ok('15 個原有地點座標零改動', locs15_ok)
ok('15 個原有地點唔加 layer 欄（預設片場層）',
   all('layer' not in by_id.get(k, {}) for k in EXP15))
EXP6 = {
    'date_harbour': ('尖沙咀海傍', '尖沙咀', 'kln', 58, 40),
    'date_peak': ('山頂', '山頂', 'island', 52, 63),
    'date_lounge': ('酒廊唱歌', '中環', 'island', 74, 60),
    'date_cinema': ('旺角戲院', '旺角', 'kln', 22, 32),
    'date_beach': ('淺水灣', '淺水灣', 'island', 55, 92),
    'date_airport': ('啟德機場', '九龍城', 'kln', 78, 38)}
ok('6 個新點齊', all(k in by_id for k in EXP6))
new_ok = True
for k, (nm, area, region, x, y) in EXP6.items():
    f = by_id.get(k, {})
    if not (f.get('name') == nm and f.get('area') == area and f.get('type') == 'date'
            and f.get('region') == region and f.get('x') == x and f.get('y') == y
            and f.get('desc') and f.get('layer') == 'date'):
        new_ok = False
ok('6 新點欄位齊全（id／name／area／type／region／x／y／desc／layer）', new_ok)
# 新點唔撞舊點／唔入 CLUSTER 7.5% fan-out 圈（基底冇新點嗰陣直接 FAIL，唔 crash）
# v20a265：只計同層——片場層新點同約會層舊點永不同時顯示（drawMap 只畫當前層），
# 跨層距離唔入呢個斷言（成衣店 (24,30) 同約會層戲院 (22,32) 只差 2.8%，同層先至撞）。
mind = 999.0
if all(k in by_id for k in EXP6):
    for k in EXP6:
        for o, f in by_id.items():
            if o == k: continue
            # v20a265：跨層唔計——date 點只同 date 層點＋約會層共享點（茶記／廟街）比較
            # （片場層新點唔入；共享點冇 layer 欄，要顯式認 id）
            if f.get('layer') != 'date' and o not in ('cafe_cha', 'gift_shop'): continue
            d = math.hypot(by_id[k]['x'] - f['x'], by_id[k]['y'] - f['y'])
            mind = min(mind, d)
ok('新點同最近同層舊點距離 ≥7.5%（唔撞針／唔觸發 fan-out）', mind >= 7.5)
_lounge_seg = locs_seg.split('date_lounge')[1].split('date_cinema')[0] if 'date_lounge' in locs_seg else ''
ok('酒廊唔係卡拉OK（1990 年未有多房式 K 場；文案唔寫卡拉OK／K 房）',
   'date_lounge' in locs_seg and '卡拉OK' not in _lounge_seg
   and 'K房' not in locs_seg and 'K 房' not in locs_seg)

# --- (2) 地圖層切換 ---
ok('層狀態 map159Layer 預設片場層', 'let map159Layer="set"' in src)
ok('約會層共享點：茶記＋廟街', 'MAP159_DATE_LAYER_SHARED=["cafe_cha","gift_shop"]' in src)
ok('層過濾 map159LocVisible 在位', 'function map159LocVisible(L)' in src)
ok('drawMap 只畫當前層（唔再 LOCS.slice() 全畫）',
   'const visible = LOCS.filter(map159LocVisible);' in src)
ok('層切換掣生喺 #map-hint（paintBar 渲染）', 'map159LayerBtnHtml()' in src and 'id="map-layer159"' in src)
ok('層切換掣委派掛喺 #map-hint（跟 wireMapShowAllLocs 同一寫法）',
   'function wireMapLayer159' in src and 'closest("#map-layer159")' in src)
ok('切換唔耗出行額度（handler 入面冇 travel114TrySpend）',
   'travel114TrySpend' not in src[src.find('function wireMapLayer159'):src.find('function wireMapLayer159') + 800])
ok('約會層唔包事務所／醫院',
   'agency_ho' not in src[src.find('MAP159_DATE_LAYER_SHARED'):src.find('MAP159_DATE_LAYER_SHARED') + 80]
   and 'hospital' not in src[src.find('MAP159_DATE_LAYER_SHARED'):src.find('MAP159_DATE_LAYER_SHARED') + 80])
# 墨字地名 23 個（15 舊＋6 新＋v265 2 新）
mn = re.findall(r'<div class="mn68"[^>]*>([^<]+)</div>', src)
ok('墨字地名 23 個（15＋6＋2）', len(mn) == 23)
ok('6 新點墨字地名齊', all(k in by_id and by_id[k]['name'] in mn for k in EXP6))
ok('v265 2 新點墨字地名齊（花園街成衣店／阿偉屋企）',
   '花園街成衣店' in mn and '阿偉屋企' in mn)

# --- (3) 地點 sheet：bg 對照表＋404 fallback＋約會對象列 ---
mb = re.search(r'const LOC_SHEET_BG = \{(.*?)\n\};', src, re.S)
ok('搵到 LOC_SHEET_BG', bool(mb))
bg = mb.group(1) if mb else ''
EXP_BG = {
    'date_harbour': 'assets/story/locs/bg_159_harbour.jpg',
    'date_peak': 'assets/story/locs/bg_159_peak.jpg',
    'date_lounge': 'assets/story/locs/bg_159_lounge.jpg',
    'date_cinema': 'assets/story/locs/bg_159_cinema.jpg',
    'date_beach': 'assets/story/locs/bg_159_beach.jpg',
    'date_airport': 'assets/story/locs/bg_159_airport.jpg'}
ok('bg 對照表 6 行檔名啱', all(f'{k}:"{v}"' in bg for k, v in EXP_BG.items()))
ok('bg fallback：bg_159_ 圖 404 用中性漸變底（唔用第二個地點嘅圖頂住）',
   'bg_159_' in src[src.find('function applyLocSheetBg'):src.find('function applyLocSheetBg') + 1600]
   and 'linear-gradient(160deg,#ebe2d4' in src[src.find('function applyLocSheetBg'):src.find('function applyLocSheetBg') + 1600]
   and 'loc-bg-missing159' in src)
ok('約會對象 helper rom159WomenAtLoc 在位', 'function rom159WomenAtLoc(locId)' in src)
ok('helper 認直接 locId 寫法', 'if(sp===locId) return true;' in src)
ok('helper 認 ROM159_DATES key 間接寫法（Phase 1 spots）',
   'ROM159_DATES[sp]' in src and 'd.locId===locId' in src)
ok('sheet 約會掣經現成 rom159DateGate／rom159OpenDatePicker（唔改嗰兩個函數）',
   'rom159DateGate(rk, null)' in src and 'rom159OpenDatePicker(rk, L)' in src)
ok('約會掣唔靜默消失（gate 唔啱都出掣，hint 講原因）',
   'gate.ok ? "act-priority" : ""' in src)
ok('約會掣加喺 hub＋非 hub 兩個分支（茶記＋廟街＋6 新點都食到）',
   src.count('addRom159DateActs(add, L);') == 2)
# 用 source 數據驗證 helper 嘅 resolution：茶記→六人齊（Vera 出局後，六位女角都有茶記場）；廟街→曉晴
mw = re.search(r'const ROM159_WOMEN = \{(.*?)\n\};', src, re.S)
md = re.search(r'const ROM159_DATES = \{(.*?)\n\};', src, re.S)
ok('搵到 ROM159_WOMEN／ROM159_DATES', bool(mw) and bool(md))
dates = {}
if md:
    for dkey, who, loc in re.findall(r'(\w+):\s*\{ who:"(\w+)", locId:"(\w+)"', md.group(1)):
        dates[dkey] = (who, loc)
women_at = {}
if mw:
    for key, spots in re.findall(r'(\w+):\s*\{ key:"\w+".*?spots:\[(.*?)\]', mw.group(1), re.S):
        for sp in re.findall(r'"([^"]+)"', spots):
            loc = sp if sp in ('cafe_cha', 'gift_shop') or sp.startswith('date_') else (dates.get(sp, (None, None))[1])
            if loc: women_at.setdefault(loc, []).append(key)
ok('茶記約會對象：六人齊（讀 ROM159_WOMEN spots 經 ROM159_DATES）',
   sorted(women_at.get('cafe_cha', [])) == ['choi', 'hiu', 'lan', 'so', 'xu', 'yip'])
ok('廟街約會對象：曉晴', women_at.get('gift_shop', []) == ['hiu'])
ok('ROM159_WOMEN／ROM159_DATES 終態：六人、37 場、無 vera（A＋B1 整合後）',
   'yip' in (mw.group(1) if mw else '') and 'so' in (mw.group(1) if mw else '')
   and 'vera' not in (mw.group(1) if mw else '').lower() and len(dates) == 37)

# --- (4) 日常用途：tertiary 第三出沒點 ---
ms = re.search(r'const ENC79_STARS = \[(.*?)\n\];', src, re.S)
ok('ENC79 葉敏芝 tertiary→酒廊、蘇芷茵 tertiary→海傍',
   'yip_manji' in src and 'tertiary:"date_lounge"' in (ms.group(1) if ms else '')
   and 'tertiary:"date_harbour"' in (ms.group(1) if ms else ''))
mr = re.search(r'const ROM176_WOMEN = \[(.*?)\n\];', src, re.S)
ok('ROM176 曉晴→啟德、采兒→戲院、藍若曦→淺水灣、徐寶珊→山頂',
   all(x in (mr.group(1) if mr else '') for x in
       ['tertiary:"date_airport"', 'tertiary:"date_cinema"', 'tertiary:"date_beach"', 'tertiary:"date_peak"']))
ok('兩邊出沒 roll 都讀 tertiary（唔出沒嘅日子先去第三點）',
   src.count('":tert") < 0.20') == 2)
ok('出沒率／上限／冷卻數字零改動',
   'const ROM176_P = 0.50, ROM176_SHARE = 0.65, ROM176_DAILY_CAP = 1, ROM176_WEEKLY_CAP = 3, ROM176_COOLDOWN = 2, ROM176_PITY_DAYS = 5' in src
   and 'ENC79_COOLDOWN = 3' in src and 'ENC79_DAILY_CAP = 1' in src and 'ENC79_WEEKLY_CAP = 2' in src)
ok('唔加免費減壓（新點冇減壓行動）',
   'date_harbour' not in src[src.find('function doRest'):src.find('function doRest') + 600] if 'function doRest' in src else True)

# --- (5) 出行額度 ---
ok('入新地點照計 1 次（openLoc 閘口唔變；唔加新豁免）',
   'travel114TrySpend(opts, id)' in src and 'id==="home"' in src)
ok('travel114IsFree 冇新豁免（只認 home／forceRestore／encDone／wf4Done／travelFree）',
   'date_' not in src[src.find('function travel114IsFree'):src.find('function travel114IsFree') + 400])

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
