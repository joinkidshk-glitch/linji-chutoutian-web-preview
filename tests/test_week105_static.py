# -*- coding: utf-8 -*-
"""v20a105 WEEK105 週界狀態組 — 靜態鎖
鎖住：S-12 週界旗接線（settleWeek 寫旗、enterHome 清旗、contFromSlot 補呈現且
唔再行 settleWeek）、S-13 剔已完成標記（scrubInherited105／todayPlanId／paintBar
保底過一日掣）、S-14 實際執行紀錄接線（各耗日路徑記名＋回顧渲染優先用紀錄）、
SAVE key／softRev／?v= 紀律、存檔新欄位向後兼容（fresh＋normalizeSaveObj）。
反證：對 v20a104 index 行——WEEK105 標記同全部接線唔存在 → FAIL。
用法：python3 tests/test_week105_static.py [path-to-index.html]
"""
import sys

src = open(sys.argv[1] if len(sys.argv) > 1 else "index.html", encoding="utf-8").read()
fails = []


def ok(cond, msg):
    if not cond:
        fails.append(msg)


def fn_body(name):
    i = src.find("function " + name + "(")
    if i < 0:
        return ""
    j = src.find("{", i)
    depth, k = 0, j
    while k < len(src):
        ch = src[k]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return src[j:k + 1]
        k += 1
    return ""


def seg(a, b):
    i = src.find(a)
    j = src.find(b, i + 1) if i >= 0 else -1
    return src[i:j] if (i >= 0 and j > i) else ""


# --- 紀律：SAVE／softRev／?v= 冇郁 ---
ok('const SAVE = "starVolunteer_map_v19w"' in src, "SAVE key 冇郁")
ok(src.count("starVolunteer_map_v19w") == 10, "SAVE 字面出現次數維持 10（冇新增引用）")
ok('var SOFT_REV = "s107"' in src or 'SOFT_REV = "s107"' in src, "softRev s107 冇郁")
ok("WEEK105" in src, "WEEK105 標記在位")

# --- S-12：週界旗寫入／清旗／補呈現 ---
sw = fn_body("settleWeek")
ok("weekBoundary105" in sw and "html: settleBlock + flavorHtml" in sw,
   "settleWeek 扣完錢寫週界旗（存結算 html）")
ok(sw.count("apply({money:-paid})") == 1, "settleWeek 扣生活費仍然只得一處")
eh = fn_body("enterHome")
ok("weekBoundary105 = null" in eh and "editable" in eh, "enterHome 編排步清週界旗")
cf = seg("function contFromSlot(", "function cont(){")
ok("week105Pending()" in cf, "contFromSlot 載入檢查週界旗")
ok("enterHome(" in cf and "wp105.html" in cf, "contFromSlot 補呈現結算 html＋入編排步")
ok("settleWeek(" not in cf, "contFromSlot 唔會重行 settleWeek（防雙重扣錢）")
wp = fn_body("week105Pending")
ok("wk*7" in wp, "week105Pending 以 dayIndex == week*7 判旗有效（過咗週一即殘旗）")

# --- S-13：剔已完成標記＋保底入口 ---
sc = fn_body("scrubInherited105")
ok('startsWith("wrap:")' in sc and 'startsWith("audition:")' in sc and 'startsWith("shoot:")' in sc,
   "scrubInherited105 剔 wrap:/audition:/死 shoot:")
ok("scrubInherited105(S.weekPlan)" in cf, "contFromSlot 繼承時行 scrubInherited105")
tp = fn_body("todayPlanId")
ok('startsWith("wrap:")' in tp and '"scout_all"' in tp, "todayPlanId 已完成標記改返自由日")
pb = seg("function paintBar(){", "let __storyMapRedrawT")
ok("WEEK105 S-13 保底" in pb and pb.count('id="map-end-day"') >= 2,
   "paintBar 保底：任何非強制日子有「過一日」")

# --- S-14：實際執行紀錄 ---
ok("execLog105:{}" in src.replace(" ", "") or "execLog105: {}" in src, "fresh() 有 execLog105 欄")
ns = fn_body("normalizeSaveObj")
ok("execLog105" in ns and "weekBoundary105" in ns, "normalizeSaveObj 補舊檔新欄（向後兼容）")
ok('recordExec105Day("audition"' in src, "試鏡路徑記名 audition")
ok('recordExec105Day("early_rest")' in src, "提早休息記名 early_rest")
ok('recordExec105Day("story"' in src, "劇情完成記名 story")
ok('recordExec105Day("sick")' in src, "病假記名 sick")
ok('recordExec105Day(k105, det105)' in src, "resolvePlannedDay 按實際分支記名")
tk = fn_body("tickDay")
ok("recordExec105Day" in tk and "exec105KindForSlot" in tk, "tickDay 有執行紀錄兜底")
rn = seg("function renderNotebook(){", "function enterHome(")
ok("nbRowMeta105" in rn, "手帳回顧渲染優先用實際執行紀錄")

if fails:
    print("week105_static: FAIL")
    for f in fails:
        print("  ✗", f)
    sys.exit(1)
print("week105_static: PASS")
