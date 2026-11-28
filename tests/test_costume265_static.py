# v416：店舖提示收去衣櫃頁首、未合要求改 span，斷言跟新寫法。
# -*- coding: utf-8 -*-
# v20a265 COSTUME265（服裝＋屋企系統 P1）靜態測試：
# 一、服裝表 12 件：價錢／加成／解鎖同設計檔 §1.2 一致，全套 $6,270
# 二、v20a293 Q6：店賣 12 件（全數 shop:true；v265 P1 只賣 4 件 #1／#4／#10／#8 已成歷史）
# 三、有效數值：加成函數在位、每圍上限 +4、永遠唔寫入 S.*（靜態掃描：成個 COSTUME265 塊
#     入面唔准出現 S.<七圍／聲望> 賦值；錢只准喺 buyCostume265 入面扣）
# 四、門檻檢查＋卡面顯示行有效數值（reqGap／gigMissingReqGaps／reqGridHtml 衫貢獻）
# 五、買衫流程標記齊（查擁有→查解鎖→查錢→扣錢→入 owned→saveQ；買嘢唔耗日）
# 六、瞓覺掣／衣櫃入口標記齊（瞓覺＝全日休息同一條數＋zzz 呈現，唔用 fx_rest.mp4）
# 七、地點數：片場層 15→17、LOCS 總數 21→23；屋企免費／服裝店計 1 次
# 八、舊檔相容（normalizeSaveObj／fresh 補 S.wardrobe 預設）＋紅線三項不變
# 反證：喺 v162 基底（120c683）上行會 FAIL（COSTUME265／新地點／瞓覺／衣櫃全部唔存在）。
# 唔斷言衫圖檔案存在（圖由另一工人平行生成，免次序耦合；統籌最後統一驗）。
# 用法：python3 tests/test_costume265_static.py [path-to-index.html]
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "index.html")
ROOT = os.path.dirname(IDX)
with open(IDX, encoding="utf-8") as f:
    src = f.read()

fails = []
def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond: fails.append(name)

def extract_fn(name):
    i = src.find("function %s(" % name)
    assert i >= 0, "fn not found: " + name
    depth, j = 0, src.find("{", i)
    for k in range(j, len(src)):
        if src[k] == "{": depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0: j = k; break
    return src[i:j + 1]

def block_between(start_marker, end_marker):
    i = src.find(start_marker)
    j = src.find(end_marker, i)
    assert i >= 0 and j > i, "block not found: " + start_marker
    return src[i:j]

# ---------- 0. 紅線 ----------
ok("SAVE key 不變", "starVolunteer_map_v19w" in src)
ok("softRev 不變", "s107" in src)
ok("產品 ?v= 不變", "v20a10" in src)

# ---------- 1. 服裝表 12 件（設計 §1.2） ----------
m = re.search(r"const COSTUME265 = \[(.*?)\n\];", src, re.S)
ok("搵到 COSTUME265", bool(m))
tab = m.group(1) if m else ""
EXP = {
    # id: (name, cat, price, bonus dict, unlock dict-or-None, stem, shop)
    "c1":  ("乾淨白恤衫＋牛仔褲", "日常", 120,  {"looks": 1, "charm": 1}, None, "awi_c1", True),
    "c2":  ("街坊波鞋套裝", "日常", 150,  {"stamina": 1, "looks": 1}, None, "awi_c2", True),
    "c3":  ("黑皮褸", "日常", 300,  {"looks": 2, "charm": 1}, {"fame": 15}, "awi_c3", True),
    "c4":  ("合身深藍西裝", "正式", 600,  {"looks": 2, "charm": 2}, {"fame": 25}, "awi_c4", True),
    "c5":  ("灰色三件頭", "正式", 900,  {"looks": 3, "charm": 2, "stage": 1}, {"tier": 1}, "awi_c5", True),
    "c6":  ("晚宴禮服", "正式", 1500, {"looks": 3, "charm": 3, "stage": 1}, {"tier": 2, "fame": 40}, "awi_c6", True),
    "c7":  ("牛仔舞台服", "舞台", 250,  {"stage": 2, "vocal": 2}, {"vocal": 20}, "awi_c7", True),
    "c8":  ("亮片舞台裝", "舞台", 500,  {"stage": 3, "charm": 1}, {"vocal": 25}, "awi_c8", True),
    "c9":  ("閃粉舞衣", "舞台", 800,  {"stage": 3, "charm": 2, "vocal": 1}, {"tier": 2}, "awi_c9", True),
    "c10": ("武師練功服", "戲行", 150,  {"stamina": 2, "acting": 1}, None, "awi_c10", True),
    "c11": ("民初長衫", "戲行", 400,  {"acting": 3, "stage": 1}, {"acting": 35}, "awi_c11", True),
    "c12": ("古裝戲服", "戲行", 600,  {"acting": 2, "looks": 2}, {"acting": 30}, "awi_c12", True),
}
def parse_bonus(s):
    out = {}
    for k, v in re.findall(r"(\w+):(\d+)", s or ""):
        out[k] = int(v)
    return out
def parse_unlock(s):
    s = (s or "").strip()
    if s == "null": return None
    return parse_bonus(s)
rows = {}
for mm in re.finditer(
        r'\{ id:"(\w+)",\s*name:"([^"]+)",\s*cat:"([^"]+)",\s*price:(\d+),\s*bonus:\{([^}]*)\},\s*unlock:(\{[^}]*\}|null),\s*stem:"([^"]+)",\s*shop:(true|false)\s*\}',
        tab):
    rows[mm.group(1)] = (mm.group(2), mm.group(3), int(mm.group(4)),
                         parse_bonus(mm.group(5)), parse_unlock(mm.group(6)),
                         mm.group(7), mm.group(8) == "true")
ok("12 件齊", len(rows) == 12 and set(rows) == set(EXP))
tab_ok = all(rows.get(k) == v for k, v in EXP.items())
ok("12 件價錢／加成／解鎖／stem／shop 同設計 §1.2 一致", tab_ok)
if not tab_ok:
    for k, v in EXP.items():
        if rows.get(k) != v:
            print("  MISMATCH %s: got %r want %r" % (k, rows.get(k), v))
ok("全套 $6,270", sum(v[2] for v in EXP.values()) == 6270)
ok("加成唔掂聲望／人氣／信用／智商（衫唔令人變聰明）",
   all(set(v[3]) <= {"acting", "stage", "vocal", "looks", "charm", "stamina"} for v in EXP.values()))
ok("單件最高 +3", all(n <= 3 for v in EXP.values() for n in v[3].values()))

# ---------- 2. v293 店賣 12 件 ----------
shop = sorted(k for k, v in rows.items() if v[6])
ok("v293 店賣 12 件（全數 shop:true）", shop == ["c1", "c10", "c11", "c12", "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9"])
ok("再無入表唔賣嘅衫（P2 清零）", len(rows) - len(shop) == 0)
ok("12 件衫 stem 約定：awi_c1～awi_c12",
   all(rows.get("c%d" % n, (None,) * 7)[5] == "awi_c%d" % n for n in range(1, 13)))
ok("表情組 8 個（base／angry／sad／serious／shy／smile／surprise／think）",
   'const COSTUME265_EXPRS = ["base","angry","sad","serious","shy","smile","surprise","think"]' in src)

# ---------- 3. 有效數值：函數在位＋上限 +4＋唔寫入 S.* ----------
for fn in ("costume265ById", "costume265EnsureWardrobe", "costume265EquippedDef",
           "costume265BonusMap", "costume265EffStat", "costume265UnlockReason",
           "costume265Unlocked", "costume265Tier", "buyCostume265", "costume265Equip"):
    ok("函數 %s 在位" % fn, ("function %s(" % fn) in src)
ok("每圍上限 +4（常數＋BonusMap 用 Math.min 夾）",
   "const COSTUME265_MAX_PER_STAT = 4" in src
   and "Math.min(COSTUME265_MAX_PER_STAT, n)" in extract_fn("costume265BonusMap"))
ok("costume265EffStat＝底數＋衫加成",
   "costume265BonusMap()[key]" in extract_fn("costume265EffStat"))
# 靜態反證：成個 COSTUME265 塊（表＋helpers＋店／瞓覺／衣櫃 UI）唔准寫入任何一圍／聲望；
# 錢只准喺 buyCostume265 入面扣（買衫本身）；S.wardrobe 只准寫 owned／equipped。
blk = block_between("/* ===== v20a265 COSTUME265", "const STAT_LABEL")
STAT_KEYS = ["acting", "stage", "vocal", "looks", "charm", "stamina", "iq", "fame", "popularity", "stress"]
bad_writes = []
for key in STAT_KEYS:
    for mm in re.finditer(r"S\." + key + r"\s*=(?!=)", blk):
        bad_writes.append("S.%s=" % key)
ok("COSTUME265 塊唔寫入任何一圍／聲望／壓力（有效數值，唔入 S.*）", not bad_writes)
buy_src = extract_fn("buyCostume265")
money_writes = re.findall(r"S\.money\s*=(?!=)", blk)
ok("錢只喺 buyCostume265 入面扣（其餘 helpers／UI 唔掂錢）",
   len(money_writes) == 1 and "S.money = (S.money||0) - price;" in buy_src)
ok("wardrobe 寫入只限 owned／equipped（唔寫其他 S 欄）",
   "w.owned.push(id)" in buy_src and "w.equipped = id" in extract_fn("costume265Equip")
   and not re.search(r"S\.(?!wardrobe\b|money\b|weekRestDone370\b)\w+\s*=(?!=)", blk.replace(buy_src, "")) )  # v20a370 P3-11：weekRestDone370 係休息計數，唔係數值寫入
ok("解鎖級數用 max(即時, 最高紀錄)，唔用即時 tier（跨年唔會鎖返）",
   "Math.max(live, mx)" in extract_fn("costume265Tier"))

# ---------- 4. 門檻檢查＋卡面顯示行有效數值 ----------
ok("reqGap 用 costume265EffStat（通告接取／試鏡門檻）",
   "costume265EffStat(k)" in extract_fn("reqGap"))
ok("gigMissingReqGaps 用 costume265EffStat（差距顯示同門檻一致）",
   "costume265EffStat(k)" in extract_fn("gigMissingReqGaps"))
ok("reqGridHtml 卡面標明衫貢獻（衫+N；v425 數值詞組唔拆行）",
   "衫+${bonus265}" in src and "costume265BonusMap()[key]" in src)
ok("canAudition 經 reqGap 行（唔繞過有效數值）",
   "reqGap(gig)" in extract_fn("canAudition"))

# ---------- 5. 買衫流程標記齊 ----------
ok("buyCostume265：查擁有（已經擁有）", '"已經擁有"' in buy_src)
ok("buyCostume265：查解鎖（未合要求）", "costume265UnlockReason(c)" in buy_src)
ok("buyCostume265：查錢（不夠錢）", "(S.money||0) < price" in buy_src)
ok("buyCostume265：扣錢＋入 owned＋saveQ", "S.money = (S.money||0) - price;" in buy_src
   and "w.owned.push(id)" in buy_src and "saveQ();" in buy_src)
ok("buyCostume265：買嘢唔耗日（冇 tickDay／confirmSpendDay）",
   "tickDay" not in buy_src and "confirmSpendDay" not in buy_src)
ok("buyCostume265：未有售嘅衫買唔到（P2 衫守門）", '"這件衫暫未有售"' in buy_src)
shop_src = extract_fn("openClothingShop265")
ok("openClothingShop265：在位＋先確認後扣錢（confirmChoice236＋buyCostume265）",
   "confirmChoice236({" in shop_src and "buyCostume265(id)" in shop_src)
ok("openClothingShop265：鎖住寫明要求", '未合要求：' in shop_src)
ok("openClothingShop265：已擁有顯示，唔可以重複買", '"已擁有"' in shop_src)
ok("openLoc 服裝店出「買衫」掣",
   'if(L.id==="clothing_shop") add("買衫", "花園街成衣店","免費", ()=>openClothingShop265(L), "act-priority");' in src)

# ---------- 6. 瞓覺掣／衣櫃入口 ----------
ok("HTML 有 #btn-sleep265（瞓覺掣）", 'id="btn-sleep265"' in src)
ok("衣櫃子頁入口在位（v389：#htab-wardrobe＋#home-pane-wardrobe，舊 #btn-wardrobe265 已刪）", 'id="htab-wardrobe"' in src and 'id="home-pane-wardrobe"' in src and 'id="btn-wardrobe265"' not in src)
ok("HTML 有 #wardrobe265（衣櫃區容器）", 'id="wardrobe265"' in src)
ok("renderNotebook 尾段接線瞓覺／衣櫃＋渲染衣櫃區",
   "wireHome265();" in extract_fn("renderNotebook")
   and "renderWardrobe265();" in extract_fn("renderNotebook"))
sleep_src = extract_fn("costume265Sleep")
ok("costume265Sleep：在位＋確認講明「今日就咁完咗，聽朝見」",
   "今日就咁完咗，聽朝見" in sleep_src)
ok("瞓覺＝全日休息同一條數（壓力清零 apply({stress:-S.stress})）",
   "apply({stress:-S.stress})" in sleep_src)
ok("瞓覺耗一日（tickDay＋writeTodayPlan rest）",
   "tickDay()" in sleep_src and 'writeTodayPlan("rest")' in sleep_src)
ok("瞓覺唔用 fx_rest.mp4（costume265Sleep 塊冇 fx_rest；日結卡行 sleep265ZzzHtml）",
   "fx_rest" not in sleep_src and "sleep265: true" in sleep_src)
ok("sleep265ZzzHtml 在位（zzz 浮字，唔畫瞓低身體）",
   "function sleep265ZzzHtml()" in src and "<span>z</span><span>z</span><span>z</span>" in src)
ok("presentRestSleepDayEnd：sleep265 行 zzz 唔行 restSleepFxHtml",
   "(opts.sleep265 ? sleep265ZzzHtml() : restSleepFxHtml())" in src)
gate_src = extract_fn("costume265SleepAvailable")
ok("瞓覺 gate：強制日唔出掣（todayIsForcedDay）＋編排行程嗰陣唔出（homeEditable）",
   "todayIsForcedDay()" in gate_src and "S.homeEditable" in gate_src)
ok("瞓覺 gate：結局鎖／劇情進行中唔出掣",
   "ending78Locked" in gate_src and "isStoryPlayActive" in gate_src)
ok("CSS 有 .sleep265-zzz 浮字動畫", ".sleep265-zzz" in src and "@keyframes sleep265float" in src)
ok("CSS 有 .wardrobe265 衣櫃區", ".wardrobe265" in src and ".wardrobe265-row" in src)
ward_src = extract_fn("renderWardrobe265")
ok("衣櫃區：著緊邊套／擁有／換衫（著上／除低）",
   "而家著緊" in ward_src and 'data-equip265' in ward_src and 'data-unequip265' in ward_src)
ok("衣櫃區：未擁有寫明去向（店有售／稍後推出）",
   "未購入嘅衫可以去花園街成衣店買" in ward_src)
ok("換衫免費即時（costume265Equip：寫 equipped＋saveQ，冇 tickDay／冇扣錢）",
   "w.equipped = id" in extract_fn("costume265Equip")
   and "tickDay" not in extract_fn("costume265Equip")
   and "S.money" not in extract_fn("costume265Equip"))

# ---------- 7. 地點數 15→17／23；出行額度 ----------
lm = re.search(r"const LOCS = \[(.*?)\n\];", src, re.S)
locs_seg = lm.group(1) if lm else ""
ids = re.findall(r'\{ id:"(\w+)",', locs_seg)
ok("LOCS 總數 17 個（v407 約會場景收起，23→17）", len(ids) == 17)
set_layer = [i for i in ids if not i.startswith("date_")]
ok("片場層 17 個（15 舊＋服裝店／屋企）", len(set_layer) == 17)
ok("LOCS 有 clothing_shop（花園街成衣店／旺角／shop／78,7）",
   '{ id:"clothing_shop", name:"花園街成衣店", area:"旺角", type:"shop", region:"kln", x:78, y:7' in locs_seg)
ok("LOCS 有 home（阿偉屋企／深水埗／home／13,8）",
   '{ id:"home", name:"阿偉屋企", area:"深水埗", type:"home", region:"kln", x:13, y:8' in locs_seg)
ok("新點唔加 layer 欄（預設片場層）",
   'layer' not in locs_seg.split('id:"clothing_shop"')[1].split('id:"home"')[0]
   and 'layer' not in locs_seg.split('id:"home"')[1].split('},')[0])
mn = re.findall(r'<div class="mn68[^"]*"[^>]*>([^<]+)</div>', src)  # v20a373：容許額外 class（mn68-ask373）
ok("墨字地名 17 個，包花園街成衣店／阿偉屋企", len(mn) == 17
   and "花園街成衣店" in mn and "阿偉屋企" in mn)
ok("LOC_SHEET_BG：服裝店＋屋企（屋企用現成 bg_wf4_home.jpg）",
   'clothing_shop:"assets/story/locs/bg_loc_clothing_shop.jpg"' in src
   and 'home:"assets/story/locs/bg_wf4_home.jpg"' in src)
ok("屋企場景圖檔實存（bg_wf4_home.jpg 已入庫）",
   os.path.isfile(os.path.join(ROOT, "assets", "story", "locs", "bg_wf4_home.jpg")))
ok("屋企唔計出行額度（travel114IsFree 守衛 id===\"home\" 仲在）",
   'id==="home"' in extract_fn("travel114IsFree"))
ok("服裝店照計 1 次（travel114IsFree 冇 clothing_shop 豁免）",
   "clothing_shop" not in extract_fn("travel114IsFree"))
ok("openLoc：屋企行 enterHome 手帳（唔開地點 sheet、唔擲巧遇）",
   'if(id==="home"){' in src and "enterHome(null, false);" in src)
ok("返地圖行 book70ExitHome 恆常出口（唔加新出口）",
   "function book70ExitHome()" in src and src.count("book70ExitHome()") >= 3)  # 定義 1＋呼叫 2
def _coords(seg):
    return {mm.group(1): (int(mm.group(2)), int(mm.group(3))) for mm in
            re.finditer(r'\{ id:"(\w+)",[^}]*?x:(\d+), y:(\d+)', seg)}
def _dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
_by = _coords(locs_seg)
_new_min = 999.0
for _a in ("clothing_shop", "home"):
    for _b, _xy in _by.items():
        if _b == _a or _b.startswith("date_"):
            continue  # 跨層唔計：兩層永不同時顯示
        _new_min = min(_new_min, _dist(_by[_a], _xy))
ok("新點同最近同層舊點 ≥7.5%（唔撞針／唔觸發 fan-out）", _new_min >= 7.5)

# ---------- 8. 衫圖接線（路徑，唔斷言檔案存在） ----------
ok("dlg106AweiStem：著衫行衫嘅 stem（冇衫跌返階段 stem）",
   "costume265EquippedDef()" in extract_fn("dlg106AweiStem"))
ok("bust109HeroSrc：著衫行衫嘅 base 全身圖",
   '"assets/story/fullbody/"+cd.stem+"_base.webp"' in extract_fn("bust109HeroSrc"))
ok("頁頭 bust 缺圖有 onerror 跌返階段 bust（唔出破圖）",
   "img.onerror=function()" in src and "PORTRAITS.hero_awi" in src)
ok("頒獎禮燕尾服唔郁（COSTUME265 塊冇掂 NP214／燕尾服）",
   "NP214" not in blk and "燕尾服" not in blk)

# ---------- 9. 舊檔相容 ----------
ok("normalizeSaveObj 補 S.wardrobe 預設（owned:[]／equipped:null）",
   "o.wardrobe={ owned:[], equipped:null }" in extract_fn("normalizeSaveObj"))
ok("fresh() 有 S.wardrobe 預設", "wardrobe:{ owned:[], equipped:null }" in extract_fn("fresh"))

# ---------- 10. 唔做（P2／P3，唔好偷渡） ----------
ok("唔郁 N11（COSTUME265 塊冇 N11 掛鈎）", "N11" not in blk)
ok("唔開耐久度／混搭／場合加成／套裝效果",
   all(w not in blk for w in ("耐久", "混搭", "場合加成", "套裝效果")))
ok("唔開第二間店／衫送禮／感情線掛鈎",
   "第二間店" not in blk and "送禮" not in blk)
ok("瞓覺只清壓力（costume265Sleep 冇回體能／其他數值）",
   "stamina" not in sleep_src and "S.money" not in sleep_src)

print("FAILURES: " + " | ".join(fails) if fails else "ALL PASS")
sys.exit(1 if fails else 0)
