#!/usr/bin/env python3
# v342 resync: index.html +20 lines inserted after old L6758 (STORY_LOC_SOFT R_ locIds).
# Pins > 6758 shift +20; pins <= 6758 unchanged. Total lines 47296 -> 47316.
# Every replacement asserts exact occurrence count before writing.
import re, sys

ROOT = "/home/hatch/workspace/linji-work342"

def load(p):
    return open(f"{ROOT}/{p}", encoding="utf8").read()

def save(p, s):
    open(f"{ROOT}/{p}", "w", encoding="utf8").write(s)

def rep(s, old, new, n, tag):
    c = s.count(old)
    assert c == n, f"{tag}: count({old!r})={c} != {n}"
    return s.replace(old, new)

RESYNC = "# v20a342 resync：index.html 淨 +20 行（STORY_LOC_SOFT 派 R_ 節點 locId ＋20＠舊 L6758 後；總行數 47296→47316；其後錨點一律 +20，內容逐行核實純漂移，見 qa342/resync342.py）。\n"
RESYNC176 = "# v20a342 resync：index.html 淨 +20 行（STORY_LOC_SOFT 派 R_ 節點 locId ＋20＠舊 L6758 後；總行數 47296→47316；6325 喺插入點之前唔郁，其後錨點一律 +20，內容逐行核實純漂移，見 qa342/resync342.py）。\n"
RESYNC114 = "# v20a342 resync：index.html 淨 +20 行（STORY_LOC_SOFT 派 R_ 節點 locId ＋20＠舊 L6758 後；總行數 47296→47316；FREE 6529／6530 喺插入點之前唔郁，COUNT／FREE 其餘＋DEF 42516→42536＋WRAPPER 29116→29136 一律 +20，內容逐行核實純漂移，見 qa342/resync342.py）。\n"

# ---- test_rom159_static.py ----
p = "tests/test_rom159_static.py"; s = load(p)
s = rep(s, "line_has(25433,", "line_has(25453,", 1, p)
s = rep(s, "line_has(8245,", "line_has(8265,", 1, p)
s = rep(s, "line_has(26281,", "line_has(26301,", 1, p)
s = rep(s, "line_has(10703,", "line_has(10723,", 1, p)
s = rep(s, "line_has(14778,", "line_has(14798,", 1, p)
s = rep(s, "line_has(26182,", "line_has(26202,", 1, p)
s = rep(s, "idx_lines[25461 - 1]", "idx_lines[25481 - 1]", 1, p)
save(p, RESYNC + s); print("OK", p)

# ---- test_rom176_static.py ----
p = "tests/test_rom176_static.py"; s = load(p)
s = rep(s, "line(14776)", "line(14796)", 2, p)
s = rep(s, "line(40743)", "line(40763)", 1, p)
s = rep(s, "line(41093)", "line(41113)", 1, p)
s = rep(s, "line(42396)", "line(42416)", 1, p)
s = rep(s, "line(42557)", "line(42577)", 1, p)
save(p, RESYNC176 + s); print("OK", p)

# ---- test_tang152_static.py ----
p = "tests/test_tang152_static.py"; s = load(p)
s = rep(s, "lines()[9286]", "lines()[9306]", 1, p)
s = rep(s, "lines()[14703]", "lines()[14723]", 1, p)
s = rep(s, "lines()[14830]", "lines()[14850]", 1, p)
save(p, RESYNC + s); print("OK", p)

# ---- test_tang171_static.py / test_tang173_static.py ----
for p in ["tests/test_tang171_static.py", "tests/test_tang173_static.py"]:
    s = load(p)
    s = rep(s, "總行數 47296", "總行數 47316", 1, p)
    s = rep(s, "＋v336 +24）", "＋v336 +24＋v342 +20）", 1, p)
    s = rep(s, "== 47296", "== 47316", 1, p)
    s = rep(s, "openLoc DEF 行 42516", "openLoc DEF 行 42536", 1, p)
    s = rep(s, "＋v336 +24，travel114 釘行）", "＋v336 +24＋v342 +20，travel114 釘行）", 1, p)
    s = rep(s, "len(lines) >= 42516", "len(lines) >= 42536", 1, p)
    s = rep(s, "lines[42515]", "lines[42535]", 1, p)
    save(p, RESYNC + s); print("OK", p)

# ---- test_gift185_static.py ----
p = "tests/test_gift185_static.py"; s = load(p)
s = rep(s, "總行數 47296", "總行數 47316", 1, p)
s = rep(s, "＋v336 +24）", "＋v336 +24＋v342 +20）", 1, p)
s = rep(s, "== 47296", "== 47316", 1, p)
save(p, RESYNC + s); print("OK", p)

# ---- test_travel114_static.py ----
p = "tests/test_travel114_static.py"; s = load(p)
lines = s.split("\n")
in_block = False
shifted = 0
for i, ln in enumerate(lines):
    if ln.startswith("COUNT_LINES = {") or ln.startswith("FREE_LINES = {"):
        in_block = True; continue
    if in_block and ln.startswith("}"):
        in_block = False; continue
    if in_block:
        m = re.match(r"^(\s*)(\d+)(,.*)$", ln)
        if m:
            v = int(m.group(2))
            if v > 6758:
                lines[i] = f"{m.group(1)}{v+20}{m.group(3)}"
                shifted += 1
s = "\n".join(lines)
s = rep(s, "DEF_LINE = 42516", "DEF_LINE = 42536", 1, p)
s = rep(s, "WRAPPER_LINE = 29116", "WRAPPER_LINE = 29136", 1, p)
save(p, RESYNC114 + s); print("OK", p, "shifted", shifted)

# ---- test_text125_static.py ----
p = "tests/test_text125_static.py"; s = load(p)
s = rep(s, "len(ls) < 11283 or FALLBACK not in ls[11282]", "len(ls) < 11303 or FALLBACK not in ls[11302]", 1, p)
s = rep(s, "currentLine 第 11283 行", "currentLine 第 11303 行", 1, p)
s = rep(s, "len(ls) < 11425 or FALLBACK not in ls[11424]", "len(ls) < 11445 or FALLBACK not in ls[11444]", 1, p)
s = rep(s, "advance 第 11425 行", "advance 第 11445 行", 1, p)
s = rep(s, "len(ls) < 16345 or", "len(ls) < 16365 or", 1, p)
s = rep(s, "ls[16344]", "ls[16364]", 1, p)
s = rep(s, "applyFamilySafeToNode 第 16345 行", "applyFamilySafeToNode 第 16365 行", 1, p)
save(p, RESYNC + s); print("OK", p)

# ---- test_weave48_static.py (playerOffer assertion) ----
p = "tests/test_weave48_static.py"; s = load(p)
s = rep(s, "ok('lan JSON playerOffer 全部 false', all(lan_nodes[n].get('playerOffer') is False for n in lan_nodes))",
        "ok('lan JSON playerOffer 全部非 false（v342：行 offer 機制）', all(lan_nodes[n].get('playerOffer') is not False for n in lan_nodes))", 1, p)
save(p, s); print("OK", p)

# ---- test_weave48_logic.js (playerOffer assertion) ----
p = "tests/test_weave48_logic.js"; s = load(p)
s = rep(s, "if(n.playerOffer !== false) structOk = false;", "if(n.playerOffer === false) structOk = false;", 1, p)
s = rep(s, "playerOffer false、結構層齊", "playerOffer 非 false（v342）、結構層齊", 1, p)
save(p, s); print("OK", p)

# ---- content exemption: aud91fix122 / aud91fix124 ----
V342_BLOCK = """    # v342 豁免（R_ 節點 locId 修復，已拍板）：三個 romance pack 刪 playerOffer:false＋crisis when 1991→1990。
    _v342_allowed = {'content/story_detail_romance_lan_xu.json',
        'content/story_detail_romance_vera_hiu_choi.json',
        'content/story_detail_romance_yip_so.json'}
"""
for p in ["tests/test_aud91fix122_static.py", "tests/test_aud91fix124_static.py"]:
    s = load(p)
    anchor = "    _v327_allowed = {'content/SCHEMA_FREEPLAY_FRAMEWORK_v1.json'}\n"
    s = rep(s, anchor, anchor + V342_BLOCK, 1, p)
    s = rep(s, "| _v327_allowed for p in touched", "| _v327_allowed | _v342_allowed for p in touched", 1, p)
    s = rep(s, "＋v327 豁免", "＋v327＋v342 豁免", 1, p)
    save(p, s); print("OK", p)

# ---- content exemption: newspaper214 ----
p = "tests/test_newspaper214_award_static.py"; s = load(p)
anchor = "        'content/story_detail_romance_lan_xu.json', 'content/PLAN_STORY_UI_BEAT_SCHEMA_v1.md'}\n"
s = rep(s, anchor, anchor + V342_BLOCK, 1, p)
s = rep(s, "| _v297_allowed for l in touched", "| _v297_allowed | _v342_allowed for l in touched", 1, p)
save(p, s); print("OK", p)

print("ALL RESYNC DONE")
