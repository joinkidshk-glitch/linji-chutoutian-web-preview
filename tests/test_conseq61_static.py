# -*- coding: utf-8 -*-
"""v20a61 CONSEQ61 後果包 — 靜態鎖
鎖住：CONSEQ61 主 блок 在位＋參數、全部接線點（advanceDay/settleWeek/enterHome/
resolvePlannedDay/goToMapForBrowse/endBrowseDayGoHome/normalizeSaveObj/planMeta/
updateMapStressTip）、E7 結局呈現接入、SAVE key/softRev 紀律、
resolveEnding410 判定表冇 E7（E7 只准由強制收場路徑寫入）。
用法：python3 tests/test_conseq61_static.py [path-to-index.html]
"""
import re
import sys

src = open(sys.argv[1] if len(sys.argv) > 1 else "index.html", encoding="utf-8").read()
fails = []


def ok(cond, msg):
    if not cond:
        fails.append(msg)


def fn_body(name, src_text):
    i = src_text.find("function " + name + "(")
    if i < 0:
        return ""
    j = src_text.find("{", i)
    depth, k = 0, j
    while k < len(src_text):
        ch = src_text[k]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return src_text[j:k + 1]
        k += 1
    return ""


# --- 主 блок ＋參數 ---
ok("v20a61 CONSEQ61" in src, "CONSEQ61 主 блок 註頭在位")
ok("CONSEQ61_REVIEWS" in src, "CONSEQ61_REVIEWS 在位")
m = re.search(r"1988:\s*\{\s*floor:\s*45,\s*warnLine:\s*65,\s*boundaryWeek:\s*43\s*\}", src)
ok(m is not None, "1988 評核參數 floor 45／warnLine 65／邊界週 43")
m = re.search(r"1989:\s*\{\s*floor:\s*100,\s*warnLine:\s*130,\s*boundaryWeek:\s*95\s*\}", src)
ok(m is not None, "1989 評核參數 floor 100／warnLine 130／邊界週 95")
for key, val in (("graceWeeks", 4), ("sickStreak", 2), ("sickWarnStreak", 2),
                 ("sickRelief", 35), ("sickCooldownDays", 14),
                 ("sickCreditPerDay", 2), ("sickCreditCap", 6)):
    ok(re.search(key + r":\s*" + str(val) + r"\b", src) is not None,
       "CFG 參數 " + key + "=" + str(val))

# --- 接線點 ---
adv = fn_body("advanceDay", src)
ok("conseq61DailyTick" in adv, "advanceDay 接 conseq61DailyTick（翻日計收市壓力 streak）")
stw = fn_body("settleWeek", src)
ok("conseq61SettleEval" in stw, "settleWeek 接 conseq61SettleEval（評核／寬限）")
ok("身體警號" in stw, "settleWeek 有 ≥80 身體警號旁白（警告層）")
eh = fn_body("enterHome", src)
ok("conseq61PresentForcedEnding" in eh, "enterHome 接強制收場呈現 hook")
rpd = fn_body("resolvePlannedDay", src)
head = rpd[:600]
ok("conseq61ResolveSickDay" in head, "resolvePlannedDay 開頭有病日守衛")
gm = fn_body("goToMapForBrowse", src)
ok("conseq61ResolveSickDay" in gm, "goToMapForBrowse 有病日守衛（唔准入地圖避病）")
eb = fn_body("endBrowseDayGoHome", src)
ok("conseq61ResolveSickDay" in eb, "endBrowseDayGoHome 有病日守衛（唔准扮休息避病）")
nso = fn_body("normalizeSaveObj", src)
ok("conseq61LegacyMark" in nso, "normalizeSaveObj 接舊檔評核標記")
pm = fn_body("planMeta", src)
ok('"sick61"' in pm and "病假" in pm, "planMeta 有 sick61 病假格")
ust = fn_body("updateMapStressTip", src)
ok("身體警號" in ust and "streak80" in ust, "updateMapStressTip 有連續高壓身體警號分支")

# --- E7 呈現接入 ---
ok('E7: "未紅先收"' in src, "ENDING410_CAREER_NAMES 有 E7 未紅先收")
scene = fn_body("endingCareerScene410", src)
ok('case "E7"' in scene, "endingCareerScene410 有 E7 場景")
for word in ("bankrupt", "review1989"):
    ok(word in scene, "E7 場景有 variant：" + word)
summ = fn_body("endingSummaryHtml410", src)
ok("提早收科" in summ, "總結頁有 E7 提早收科標題分支")
ok("renderClippingsPane" in src and "提早收場" in src, "剪報卡有 E7 日期分支")

# --- 紀律：E7 唔入判定表、E6 規則冇郁 ---
res = fn_body("resolveEnding410", src)
ok('"E7"' not in res and "E7" not in res.split("career")[0], "resolveEnding410 判定表冇 E7（head）")
ok("E7" not in res, "resolveEnding410 全函數冇 E7（強制收場只經 conseq61 路徑）")
ok('career = "E6"' in res or 'career="E6"' in res or '"E6"' in res, "E6 自願退圈判定仍在（冇畀 E7 頂替）")

# --- 硬規則字串冇變 ---
ok("starVolunteer_map_v19w" in src, "SAVE key 冇變")
ok("s107" in src, "softRev s107 仍在")

if fails:
    print("conseq61 static: FAIL")
    for f in fails:
        print("  ✗", f)
    sys.exit(1)
print("conseq61 static: PASS")
