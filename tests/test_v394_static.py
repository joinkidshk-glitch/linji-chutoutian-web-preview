# v20a394：E0 浮沉未定加入 1992 floor 豁免 — 靜態測試（釘字串／門檻／接線）。
# 用法：python3 tests/test_v394_static.py [path-to-index.html]
import sys

src = open(sys.argv[1] if len(sys.argv) > 1 else "index.html", encoding="utf-8").read()
fails = []

def ok(msg, cond):
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

# ---- (1) 豁免名單有 E0，舊成員齊全 ----
ex = fn_body("ending361FloorExempt")
ok("v394 ending361FloorExempt 豁免 E0",
   '"E0"' in ex)
ok("v394 ending361FloorExempt 舊成員 E6/E4/E3/E5 齊全",
   all(x in ex for x in ['"E6"', '"E4"', '"E3"', '"E5"']))
ok("v394 ending361FloorExempt 唔豁免 E2/E1/SS",
   all(x not in ex for x in ['"E2"', '"E1"', '"SS"']))

# ---- (2) 1992 floor 數字不變，F2 覆寫照行豁免 helper ----
ok("v394 CONSEQ61_REVIEWS 1992 floor 140／warnLine 180 不變",
   "1992: { floor: 140, warnLine: 180, boundaryWeek: 156 }" in src)
ok("v394 F2 覆寫改行 ending361FloorExempt",
   "!ending361FloorExempt(res.career)" in src)
ok("v394 F2 改判目標仍係 E7 review1992",
   'res.career = "E7"; res.careerVariant = "review1992";' in src)

# ---- (3) E0 判定本身唔郁（預設格＋低投入守門） ----
ok("v394 E0 仍係預設 fallback（career 起始值）",
   'let career = "E0", variant = "";' in src)
ok("v394 低投入定義不變（fame≤40 且活動 ≤2 宗）",
   "const lowAct392 = fame <= 40 && act392.total <= 2;" in src)
ok("v394 CR/E2 仍有 !lowAct392 閘，低投入跌落 E0",
   src.count("!lowAct392") >= 2)

# ---- (4) 註解有 v20a394 交代 ----
ok("v394 豁免註解有 v20a394 交代",
   "v20a394" in src and "E0" in src)

print("ALL PASS" if not fails else f"{len(fails)} FAILED: {fails}")
sys.exit(1 if fails else 0)
