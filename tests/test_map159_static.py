# -*- coding: utf-8 -*-
# v20a407（約會層收起）靜態測試（原 v20a159 MAP159 測試改寫）：
# 一、地圖只有一層：LOCS 17 個、冇 layer 欄、冇切層掣／層過濾／層標籤渲染。
# 二、六個約會場景保留：DATE_SCENES407 六場＋LOC_SHEET_BG bg_159_* 六行＋約會場景顯示背景；
#     場景唔係地圖 pin／標籤／可入地點（openLoc 非 LOCS id 直接 return）。
# 三、約會入口保留：地點面板約人（hub＋非 hub 兩分支）／傾談後約／手帳 Call 機約；
#     揀場嗰陣先去到場景（picker 認 DATE_SCENES407 名＋圖標）。
# 四、第三出沒點改返地圖日常地點；p／share／上限／冷卻數字零改動，20% roll 不變。
# 五、出行額度不變（唔加新豁免）。
# 用法：python3 tests/test_map159_static.py [path-to-index.html]
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

# --- (1) 地圖只有一層：LOCS 17 個 ---
m = re.search(r'const LOCS = \[(.*?)\n\];', src, re.S)
ok('搵到 LOCS', bool(m))
locs_seg = m.group(1) if m else ''
entries = re.findall(r'\{ id:"(\w+)",(.*?)\},', locs_seg, re.S)
ids = [e[0] for e in entries]
ok('LOCS 17 個', len(ids) == 17)
EXP17 = {
    'film_lion': (56, 19), 'rec_hk': (40, 40), 'tvb_longmen': (23, 34), 'tvb_kowloon': (42, 30),
    'tvb_harbour': (51, 37), 'film_cotton': (70, 17), 'film_harbour': (10, 81), 'ad_central': (40, 63),
    'ad_adm': (17, 89), 'rec_wanchai': (56, 83), 'rec_star': (70, 81), 'cafe_cha': (29, 27),
    'agency_ho': (29, 84), 'gift_shop': (24, 16), 'hospital': (86, 78),
    'clothing_shop': (78, 7), 'home': (13, 8)}
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
ok('17 個地點 id 齊', all(k in by_id for k in EXP17))
ok('17 個地點座標不變', all(by_id.get(k, {}).get('x') == v[0] and by_id.get(k, {}).get('y') == v[1]
                            for k, v in EXP17.items()))
ok('LOCS 冇 layer 欄', all('layer' not in f for f in by_id.values()))
ok('LOCS 冇 date_* 地點', not any(i.startswith('date_') for i in ids))
ok('茶餐廳／廟街保留地圖日常用途', 'cafe_cha' in by_id and 'gift_shop' in by_id)
ok('切層邏輯已刪（map159／map-layer159／共享表零殘留）',
   'map159' not in src and 'map-layer159' not in src and 'MAP159_DATE_LAYER_SHARED' not in src)
ok('drawMap 全畫 17 個地點', 'const visible = LOCS.slice();' in src)
ok('層標籤渲染已刪（visNames 顯示切換零殘留）', 'visNames' not in src)
mn = re.findall(r'<div class="mn68[^"]*"[^>]*>([^<]+)</div>', src)
ok('墨字地名 17 個', len(mn) == 17)
ok('墨字地名冇約會場景名', not any(n in mn for n in ('尖沙咀海傍', '山頂', '酒廊唱歌', '旺角戲院', '淺水灣', '啟德機場')))
ok('openLoc 非 LOCS id 直接 return（約會場景唔可入、唔扣額度）',
   'if(!LOCS.some(x=>x && x.id===id)) return;' in src)

# --- (2) 約會場景保留 ---
msc = re.search(r'const DATE_SCENES407 = \[(.*?)\n\];', src, re.S)
ok('搵到 DATE_SCENES407', bool(msc))
scenes = {a: b for a, b, _c in re.findall(r'\{ id:"(date_\w+)", name:"([^"]+)", emoji:"([^"]+)" \}', msc.group(1))} if msc else {}
EXP_SCENES = {'date_harbour': '尖沙咀海傍', 'date_peak': '山頂', 'date_lounge': '酒廊唱歌',
              'date_cinema': '旺角戲院', 'date_beach': '淺水灣', 'date_airport': '啟德機場'}
ok('六個約會場景齊（id＋名）', scenes == EXP_SCENES)
ok('場景查詢 helper 在位', 'function dateScene407ById(id)' in src)
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
ok('場景背景對照表 6 行檔名啱', all(f'{k}:"{v}"' in bg for k, v in EXP_BG.items()))
ok('約會場景顯示背景（rom159DateScene 讀 LOC_SHEET_BG）',
   'LOC_SHEET_BG[spot.locId]' in src and 'date-scene-bg407' in src)

# --- (3) 約會入口保留 ---
ok('約會對象 helper rom159WomenAtLoc 在位', 'function rom159WomenAtLoc(locId)' in src)
ok('helper 認直接 locId 寫法', 'if(sp===locId) return true;' in src)
ok('helper 認 ROM159_DATES key 間接寫法', 'ROM159_DATES[sp]' in src and 'd.locId===locId' in src)
ok('約人掣經現成 rom159DateGate／rom159OpenDatePicker',
   'rom159DateGate(rk, null)' in src and 'rom159OpenDatePicker(rk, L)' in src)
ok('約人掣加喺 hub＋非 hub 兩個分支', src.count('addRom159DateActs(add, L);') == 2)
ok('傾談後約入口在位', 'rom159OpenDatePicker(rk, L)' in src and 'function rom159TalkButtons' in src)
ok('手帳 Call 機約入口在位', 'Call 機約佢出街' in src and 'rom159OpenDatePicker(who, null)' in src)
ok('揀場認場景名＋圖標（DATE_SCENES407）',
   'dateScene407ById(sp.locId)' in src and 'iconHtml112(_sc407.emoji' in src)
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
ok('茶記約人：六人齊', sorted(women_at.get('cafe_cha', [])) == ['choi', 'hiu', 'lan', 'so', 'xu', 'yip'])
ok('廟街約人：曉晴', women_at.get('gift_shop', []) == ['hiu'])
ok('約會場次六場景仍可揀（15 場用 date_* 場景）',
   sum(1 for _, loc in dates.values() if loc.startswith('date_')) == 15)
ok('ROM159 終態：六人、37 場、無 vera',
   'yip' in (mw.group(1) if mw else '') and 'so' in (mw.group(1) if mw else '')
   and 'vera' not in (mw.group(1) if mw else '').lower() and len(dates) == 37)

# --- (4) 第三出沒點改返地圖日常地點 ---
ms = re.search(r'const ENC79_STARS = \[(.*?)\n\];', src, re.S)
enc_seg = ms.group(1) if ms else ''
ok('ENC79 葉敏芝 tertiary→天星音樂、蘇芷茵 tertiary→海港廣播',
   'tertiary:"rec_star"' in enc_seg and 'tertiary:"tvb_harbour"' in enc_seg)
mr = re.search(r'const ROM176_WOMEN = \[(.*?)\n\];', src, re.S)
rom_seg = mr.group(1) if mr else ''
ok('ROM176 第三點：曉晴→茶記、采兒→海港、藍→香江、徐→紅棉、葉→香江、蘇→天星',
   all(x in rom_seg for x in ['tertiary:"cafe_cha"', 'tertiary:"tvb_harbour"', 'tertiary:"rec_hk"',
                               'tertiary:"film_cotton"', 'tertiary:"rec_star"']))
ok('兩表 tertiary 冇 date_* 殘留', 'tertiary:"date_' not in src)
ok('兩邊出沒 roll 都讀 tertiary（20% 不變）', src.count('":tert") < 0.20') == 2)
ok('出沒率／上限／冷卻數字零改動',
   'const ROM176_P = 0.50, ROM176_SHARE = 0.65, ROM176_DAILY_CAP = 1, ROM176_WEEKLY_CAP = 3, ROM176_COOLDOWN = 2, ROM176_PITY_DAYS = 5' in src
   and 'ENC79_COOLDOWN = 3' in src and 'ENC79_DAILY_CAP = 1' in src and 'ENC79_WEEKLY_CAP = 2' in src)

# --- (5) 出行額度 ---
ok('出行額度閘口不變（唔加新豁免）', 'travel114TrySpend(opts, id)' in src and 'id==="home"' in src)
ok('travel114IsFree 冇新豁免', 'date_' not in src[src.find('function travel114IsFree'):src.find('function travel114IsFree') + 400])

print('FAILURES: ' + ' | '.join(fails) if fails else 'ALL PASS')
sys.exit(1 if fails else 0)
