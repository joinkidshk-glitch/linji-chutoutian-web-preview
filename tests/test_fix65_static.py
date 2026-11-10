# -*- coding: utf-8 -*-
"""v20a65 FIX65 修復包 — 靜態鎖
鎖住：四項修復嘅接線點同新值、病倒規則冇郁（門檻/ relief/冷卻）、評核地板冇郁、
SAVE key／softRev／?v= 紀律、wrapHistory 上限 30。
反證：對 v20a64 index 行——FIX65 標記同新值全部唔存在 → FAIL。
用法：python3 tests/test_fix65_static.py [path-to-index.html]
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


# --- FIX65-1 用戶拍板規則（2026-11-10）：全日休息清零、入水原值 ---
ok("FIX65-1" in src, "FIX65-1 標記在位")
ok(src.count("apply({stress:-S.stress})") == 2, "兩條全日休息路徑清零（排程 rest＋doRest）")
ok("-(18+R(0,8))" not in src, "舊排程休息公式 −(18+R(0,8)) 已被清零取代")
ok("-(14+R(0,8))" not in src, "舊 doRest 公式 −(14+R(0,8)) 已被清零取代")
ok("stress:-(4+R(0,4))" in src, "部分休息（提早返屋企）保留")
ok("stress:-(6+R(0,4))" in src, "部分休息（家務）保留")
sd = fn_body("shootDailyDelta")
ok("stress: 8+R(2,6)" in sd, "拍攝日入水維持原值 8+R(2,6)")
ok(src.count("stress:8+R(0,4)") >= 8, "訓練入水維持原值（兩路徑多課）")
sdfa = fn_body("stressDeltaForAct")
ok("rest:-100" in sdfa, "預覽表 rest = −100（清零標示）")
ok('if(id==="rest") d=-s;' in src, "週預覽 rest 顯示實際清走量")

# --- 病倒規則冇郁（brief 紅線） ---
i = src.find("CONSEQ61_CFG = {")
cfg = src[i:i + 900]
ok("sickStreak: 2" in cfg, "病倒觸發連續 2 日（冇郁）")
ok("sickRelief: 35" in cfg, "病癒 −35（冇郁）")
ok("sickCooldownDays: 14" in cfg, "病癒冷卻 14 日（冇郁）")
ok("sickCreditPerDay: 2" in cfg and "sickCreditCap: 6" in cfg, "告假扣信用 −2/日封頂 6（冇郁）")
ok("graceWeeks: 4" in cfg, "寬限 4 週（冇郁）")

# --- FIX65-2 生活費緩坡＋寬限解除 ---
ok("FIX65-2" in src, "FIX65-2 標記在位")
lcb = fn_body("livingCostBand")
for m in ("mid:1100", "mid:1300", "mid:1500", "mid:1700", "mid:2400"):
    ok(m in lcb, "生活費帶含 " + m)
ok("yr>=1992" in lcb and "f>=250" in lcb, "CALIB60 年份/聲望加級保留")
se = fn_body("conseq61SettleEval")
ok("weekEarnIn" in se, "conseq61SettleEval 收 weekEarnIn（入帳解除）")
ok("conseq61SettleEval(S, w, earned)" in src, "settleWeek 傳 earned 入評核")
ok("floor: 45" in src and "warnLine: 65" in src and "floor: 100" in src and "warnLine: 130" in src,
   "評核地板/警告線 45/65、100/130 冇郁")

# --- FIX65-3 跨媒介補分＋wrapHistory 上限 ---
ok("FIX65-3" in src, "FIX65-3 標記在位")
sp = fn_body("awards62ScoreParts")
ok("borrowW65" in sp and "0.55 * 0.35 * crossQ65" in sp, "借分 0.55×0.35×crossQ 在位")
ok("repPower65" in sp and "0.08 * crossQ65" in sp, "跨桶星勢 0.08×crossQ 在位")
ok("AWARDS62_WIN_LINE = 0.82" in src, "贏線 0.82 冇郁（唔靠降線）")
ok("S.wrapHistory.length>30" in src.replace(" ", "") or "wrapHistory.length>30" in src,
   "wrapHistory 上限 30（舊 20）")

# --- FIX65-4 提示認級數 ---
ok("FIX65-4" in src, "FIX65-4 標記在位")
ok("function awards65IsLeadWork(" in src, "awards65IsLeadWork 在位")
ok("AWARDS65_LEAD_SCALES" in src, "擔正級數表在位")
wh = fn_body("awards62WeakHint")
ok("repIsLead65" in wh and "深度" in wh, "WeakHint 按擔正揀句（深度句在位）")

# --- 紀律 ---
ok('starVolunteer_map_v19w' in src, "SAVE key 冇郁")
ok('s107' in src, "softRev 冇郁")

if fails:
    print("FIX65 STATIC FAILURES:")
    for f in fails:
        print("  ✗", f)
    sys.exit(1)
print("FIX65 STATIC: ALL PASS")
