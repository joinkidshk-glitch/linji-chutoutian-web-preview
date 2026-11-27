# v20a393 十項修復票 — 靜態測試（釘字串／門檻／閘／接線）。
# 用法：python3 tests/test_v393_static.py [path-to-index.html]
import json, re, sys

src = open(sys.argv[1] if len(sys.argv) > 1 else "index.html", encoding="utf-8").read()
fails = []

def ok(cond, msg):
    if cond:
        print("PASS " + msg)
    else:
        fails.append(msg)
        print("FAIL " + msg)

def fn_body(name):
    i = src.find("function " + name + "(")
    if i < 0:
        return ""
    j = src.find("{", i)
    depth = 0
    for k in range(j, len(src)):
        if src[k] == "{":
            depth += 1
        elif src[k] == "}":
            depth -= 1
            if depth == 0:
                return src[i:k + 1]
    return ""

# ---- (1) 梯次序：v421 具體身份先判、SS 兜底（仍排 CR／E2 前） ----
lad = fn_body("resolveEnding410")
order = []
for code in ['"E1"', '"FK"', '"TK"', '"SK"', '"GH"', '"CK"', '"AK"', '"E3"', '"E5"', '"E4"', '"ID"', '"SS"', '"CR"', '"E2"']:
    idx = lad.find('career = ' + code)
    order.append((code, idx))
ok(all(idx >= 0 for _, idx in order), "梯分支全部在位（E1/FK/TK/SK/GH/CK/AK/E3/E5/E4/ID/SS/CR/E2）")
ok([c for c, _ in order] == [c for c, _ in sorted(order, key=lambda t: t[1])],
   "梯次序＝E1→FK→TK→SK→GH→CK→AK→E3→E5→E4→ID→SS→CR→E2（v421）")

# ---- 門檻表 ----
for frag in ["crFameHi: 110", "ghVarietyMin: 8",
             "e4ExposureMin: 6", "e4ExposureMonths: 3"]:
    ok(frag in src, "門檻在位：" + frag)
ok("e4NetCreditBelow" not in src, "v421：E4 net 欄 e4NetCreditBelow 已刪（曝光型）")
ok("e4CreditBelow" not in src, "舊 E4 窗 e4CreditBelow 已刪")
ok("e3BackstageTags:" not in src, "舊 E3 關鍵字欄 e3BackstageTags 已刪（註解提及除外）")

# ---- (2) GH：自選佔比＋板面保證 ----
gh = fn_body("resolveEnding410")
ok("selShare95" in gh and "ghVarietyMin" in gh, "GH 讀自選綜藝佔比＋8 宗下限")
ok("function variety392EnsureBoard" in src, "variety392EnsureBoard 在位")
ok("variety392EnsureBoard(locId, shown, curSeason)" in fn_body("gigsForLocSeasonBoard"),
   "通告板接 variety392EnsureBoard")
ok("tvb_longmen" in fn_body("variety392EnsureBoard") and "tvb_kowloon" in fn_body("variety392EnsureBoard")
   and "tvb_harbour" in fn_body("variety392EnsureBoard"), "板面保證只針對三個電視台板")

# ---- (4) E4：v421 曝光型（曝光＋影視擔正皆 0，唔讀 net） ----
ok("(lead229.byMedium.film||0)===0" in lad and "(lead229.byMedium.tv||0)===0" in lad,
   "E4 要電影／電視擔正皆 0（v421 曝光型）")
ok("expo392.count>=T95.e4ExposureMin" in lad and "expo392.months>=T95.e4ExposureMonths" in lad,
   "E4 要 ≥6 宗曝光＋橫跨 ≥3 個月")

# ---- (5) N12：閘＋次序＋預設 tick ----
gate = src[src.find("const STORY_GATE_3Y"):src.find("const STORY_GATE_3Y") + 3000]
n12 = re.search(r"N12: \{([^}]*)\}", gate)
ok(n12 is not None and "tagAny" not in n12.group(1), "N12 閘已刪動作標籤前置")
ok(n12 is not None and '"春", "夏"' in n12.group(1), "N12 閘季節擴至春／夏")
order165 = re.search(r"ORDER165 = \[([^\]]*)\]", src)
ok(order165 is not None and order165.group(1).index('"N12"') < order165.group(1).index('"N13"'),
   "ORDER165：N12 排喺 N13 之前")
ok("function story392N12DefaultTick" in src, "story392N12DefaultTick 在位")
ok("story392N12DefaultTick()" in fn_body("story165NextOpen"), "story165NextOpen 接預設 tick")
ok("flag_n12_auto_default" in src, "預設 tick 寫 flag_n12_auto_default")
pack = json.load(open("content/story_detail_n1_to_n17.json", encoding="utf-8"))
def find_n12(nodes):
    for n in nodes:
        if isinstance(n, dict):
            if n.get("id") == "N12":
                return n
            for v in n.values():
                if isinstance(v, list):
                    r = find_n12(v)
                    if r:
                        return r
    return None
n12j = find_n12(pack if isinstance(pack, list) else [pack])
note = (n12j or {}).get("openConditionsNote", "")
ok("1992 春／夏" in note and note.count("1992") == 1, "N12 JSON note：1992 春／夏（全文 1992 只出現一次）")

# ---- (5a/8) 幕後職務：通告表＋標籤＋判定 ----
ok("function mergeDuty392Gigs" in src, "mergeDuty392Gigs 在位")
ok("mergeDuty392Gigs()" in fn_body("gigsForLocSeasonBoard"), "通告板接 mergeDuty392Gigs")
for did in ["duty392_clapper_a", "duty392_ad_a", "duty392_editor_a",
            "duty392_clapper_b", "duty392_ad_b", "duty392_editor_b"]:
    ok('"' + did + '"' in src, "職務通告在位：" + did)
ok(src.count("duty392:true") == 6, "職務通告 6 張（每種 2 張）")
tags = json.load(open("content/STUB_CASTING_TAGS_v1.json", encoding="utf-8"))
tag_ids = [t["id"] for t in tags["tags"]]
for tid in ["tag_duty_clapper", "tag_duty_ad", "tag_duty_editor"]:
    ok(tid in tag_ids, "casting tag 註冊：" + tid)
    ok(tags["labelToId"].get({"tag_duty_clapper": "場記", "tag_duty_ad": "副導演助理", "tag_duty_editor": "剪接助理"}[tid]) == tid,
       "casting tag label 對照：" + tid)
ok("backstageDuties392Of" in fn_body("endingE3Eligible410"), "E3 判定讀職務類別（唔再讀關鍵字計數）")
ok("tagEntrance" in fn_body("backstageDuties392Of") and "relEntrance" in fn_body("backstageDuties392Of"),
   "職務入口：標籤入口＋關係入口")

# ---- (6) ID：對照信用 ----
ok("forcedCredit392CounterCredit" in lad and "idCredit392" in lad, "ID 讀對照信用")
ok("function forcedCredit392Backfill" in src, "forcedCredit392Backfill 在位（舊檔回填）")
ok("function forcedCredit392ReplayWraps" in src, "forcedCredit392ReplayWraps 在位（重播上限）")
ok("contractCredit361OnWrap" in fn_body("forcedCredit392ReplayWraps") or "4 - qCount" in fn_body("forcedCredit392ReplayWraps"),
   "對照重播用同一套季／生涯上限")

# ---- (7) E0：低投入分流 ----
ok("lowAct392" in lad, "E2／CR 分支有低投入豁免")
ok("function activity392Of" in src and "function isLowActivity392" in src, "活動量函數在位")
ok("fame <= 40" in fn_body("isLowActivity392") and "total <= 2" in fn_body("isLowActivity392"),
   "低投入＝fame≤40 且活動 ≤2 宗")

# ---- (9) E2／E1 文案：按紀錄插入獎項句 ----
ok("endingAward392TvSupport" in fn_body("endingCareerScene410"), "E2 文案讀 awardsLog 憑據")
ok("endingAward392WonLabel" in fn_body("endingCareerScene410"), "E1 文案讀得獎 label")
ok("function endingAward392TvSupport" in src and "cat_tv_support_m" in fn_body("endingAward392TvSupport"),
   "電視台最佳男配角類別 cat_tv_support_m")

# ---- (10) 錢：補班＋記欠 ----
ok('id:"pt_topup"' in src, "PLAN_ITEMS 有補班夜班")
ok("const pay392=185" in src, "補班 $185／班")
ok("S.ptTopup392" in src and "count>=2" in fn_body("resolvePlannedDay"),
   "補班每週上限 2 班（計數＋硬截）")
ok("pt_topup: 8" in src, "補班壓力預覽 8")
ok("moneyArrears: 0" in src, "新檔預設 moneyArrears: 0")
ok("S.moneyArrears" in fn_body("settleWeek") and "記欠" in fn_body("settleWeek"),
   "settleWeek 欠費記欠＋結算卡寫明")
ok("graceWeeks" not in src, "破產寬限欄已刪（CONSEQ61_CFG 無 graceWeeks）")

# ---- 存檔回填／新檔預設 ----
ok("careerStats392Sel: null" in src, "新檔預設 careerStats392Sel: null")
ok("forcedCredit392: null" in src, "新檔預設 forcedCredit392: null")
ok("backstageDuties392: []" in src, "新檔預設 backstageDuties392: []")
ok("n12_pending392" in fn_body("normalizeSaveObj"), "normalize 補掛 N12 待處理旗")
ok("end392SelDeriveStats" in fn_body("normalizeSaveObj"), "normalize 回填自選履歷計數器")
ok("forcedCredit392Backfill" in fn_body("normalizeSaveObj"), "normalize 回填對照信用帳")

# ---- 紀律 ----
ok("starVolunteer_map_v19w" in src, "SAVE key 冇郁")
ok("0.875" in src, "頒獎贏線 0.875 冇郁")

if fails:
    print("V393 STATIC FAILURES:")
    for f in fails:
        print("  ✗", f)
    sys.exit(1)
print("V393 STATIC: ALL PASS")
