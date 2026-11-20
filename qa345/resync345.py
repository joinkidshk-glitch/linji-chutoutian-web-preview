#!/usr/bin/env python3
# v345 resync: index.html +52 lines net (47316 -> 47368).
# Insertion points (old line -> added lines after it):
#   after 13229: +3  (review1992 scene)
#   after 13625: +14 (F2 floor check)
#   after 13636: +2  (earlyEnd)
#   after 19827: +1  (cq61Clean345 const)
#   old 19849 replaced 1->8 lines: +7 (warnHtml block)
#   after 20446: +23 (presentSettleWarn345 helper)
#   after 20472: +2  (enterHome call)
# Cumulative delta for an old 1-based line L:
#   L<=13229: 0 | 13230-13625: +3 | 13626-13636: +17 | 13637-19827: +19
#   19828-19849: +20 | 19850-20446: +27 | 20447-20472: +50 | >=20473: +52
# Every replacement asserts exact occurrence count before writing.
import re

ROOT = "/home/hatch/workspace/linji-work345"

def load(p):
    return open(f"{ROOT}/{p}", encoding="utf8").read()

def save(p, s):
    open(f"{ROOT}/{p}", "w", encoding="utf8").write(s)

def rep(s, old, new, n, tag):
    c = s.count(old)
    assert c == n, f"{tag}: count({old!r})={c} != {n}"
    return s.replace(old, new)

def delta(L):
    if L <= 13229: return 0
    if L <= 13625: return 3
    if L <= 13636: return 17
    if L <= 19827: return 19
    if L <= 19849: return 20
    if L <= 20446: return 27
    if L <= 20472: return 50
    return 52

RESYNC = "# v20a345 resync：index.html 淨 +52 行（F1 警告呈現＋F2 floor 檢查；插入點舊 L13229 +3／L13625 +14／L13636 +2／L19827 +1／L19849 +7／L20446 +23／L20472 +2；總行數 47316→47368；釘行按段 shift，內容逐行核實純漂移，見 qa345/resync345.py）。\n"

# ---- test_gift185_static.py: total lines only ----
p = "tests/test_gift185_static.py"; s = load(p)
s = rep(s, "總行數 47316（", "總行數 47368（", 1, p)
s = rep(s, "＋v342 +20）", "＋v342 +20＋v345 +52）", 1, p)
s = rep(s, "== 47316)", "== 47368)", 1, p)
save(p, RESYNC + s); print("OK", p)

# ---- test_rom159_static.py ----
p = "tests/test_rom159_static.py"; s = load(p)
for old in (25453, 26301, 14798, 26202):
    s = rep(s, f"line_has({old},", f"line_has({old + delta(old)},", 1, p)
s = rep(s, "idx_lines[25481 - 1]", "idx_lines[25533 - 1]", 1, p)
save(p, RESYNC + s); print("OK", p)

# ---- test_rom176_static.py ----
p = "tests/test_rom176_static.py"; s = load(p)
s = rep(s, "line(14796)", "line(14815)", 2, p)
for old in (40763, 41113, 42416, 42577):
    s = rep(s, f"line({old})", f"line({old + delta(old)})", 1, p)
save(p, RESYNC + s); print("OK", p)

# ---- test_tang152_static.py (0-based indices into lines()) ----
p = "tests/test_tang152_static.py"; s = load(p)
s = rep(s, "lines()[14723]", "lines()[14742]", 1, p)
s = rep(s, "lines()[14850]", "lines()[14869]", 1, p)
save(p, RESYNC + s); print("OK", p)

# ---- test_tang171_static.py / test_tang173_static.py ----
for p in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    s = load(p)
    s = rep(s, "總行數 47316（", "總行數 47368（", 1, p)
    s = rep(s, "＋v342 +20）", "＋v342 +20＋v345 +52）", 1, p)
    s = rep(s, "== 47316)", "== 47368)", 1, p)
    s = rep(s, "openLoc DEF 行 42536（", "openLoc DEF 行 42588（", 1, p)
    s = rep(s, "＋v342 +20，travel114 釘行）", "＋v342 +20＋v345 +52，travel114 釘行）", 1, p)
    s = rep(s, "len(lines) >= 42536", "len(lines) >= 42588", 1, p)
    s = rep(s, "lines[42535]", "lines[42587]", 1, p)
    save(p, RESYNC + s); print("OK", p)

# ---- test_text125_static.py: only the 16365 pin moves (+19) ----
p = "tests/test_text125_static.py"; s = load(p)
s = rep(s, "len(ls) < 16365", "len(ls) < 16384", 1, p)
s = rep(s, "ls[16364]", "ls[16383]", 1, p)
s = rep(s, "applyFamilySafeToNode 第 16365 行冇 b.text 分支", "applyFamilySafeToNode 第 16384 行冇 b.text 分支", 1, p)
save(p, RESYNC + s); print("OK", p)

# ---- test_travel114_static.py: COUNT/FREE lists + DEF/WRAPPER ----
p = "tests/test_travel114_static.py"; s = load(p)
COUNT = [15378, 18659, 20869, 22072, 22512, 22515, 22546, 28567, 45801, 46009, 46167, 46188]
FREE = [6529, 6530, 8241, 14239, 14240, 14252, 14253, 14264, 14265, 14365, 24708,
        26052, 26053, 26129, 28375, 28408, 40561, 40680, 40755, 40955, 40999, 41005,
        41072, 41074, 41077, 41104, 42379, 42426, 42803, 42825, 42977, 42982, 43907,
        45581, 45678, 45679, 45723, 45724, 45749, 46638]
# single-pass dict scan over list-item lines to avoid overlapping replacements
pins = {n: n + delta(n) for n in COUNT + FREE if delta(n) != 0}
def sub_list(m):
    n = int(m.group(2))
    return m.group(1) + str(pins.get(n, n)) + m.group(3)
s2, cnt = re.subn(r"^(\s+)(\d{4,5})(,)", sub_list, s, flags=re.M)
assert cnt == len(COUNT) + len(FREE), f"{p}: list items matched {cnt} != {len(COUNT)+len(FREE)}"
s = s2
s = rep(s, "DEF_LINE = 42536", "DEF_LINE = 42588", 1, p)
s = rep(s, "WRAPPER_LINE = 29136", "WRAPPER_LINE = 29188", 1, p)
save(p, RESYNC + s); print("OK", p)

print("resync345 done")
