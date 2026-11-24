#!/usr/bin/env python3
"""v393-endings resync（rebase 上 cfd8b2b 之後）：index.html 淨 +607 行
（結局梯十項修復；底係 cfd8b2b「v392 第三輪 UI 檢視」，佢本身 +146 行）。
行號釘按 difflib 對位映射重寫，逐行核實內容相同（純漂移）。
覆蓋：travel114（COUNT／FREE／DEF／WRAPPER）、rom159（6 釘＋全佳行）、rom176（6 釘）、
tang152（2 釘，0-indexed）、text125（3 錨點）、gift185／tang171／tang173（總行數＋openLoc DEF）。
舊釘值＝cfd8b2b 版（UI 工人 resync 完嘅數），唔係 v391 版。
"""
import difflib
import re
import subprocess

ROOT = "/home/hatch/workspace/linji-work392"
old = subprocess.run(["git", "-C", ROOT, "show", "HEAD:index.html"],
                     capture_output=True, text=True, check=True).stdout.split("\n")
new = open(f"{ROOT}/index.html", encoding="utf-8").read().split("\n")
print(f"old lines={len(old)} new lines={len(new)} delta={len(new)-len(old)}")

sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-indexed

def map_line(n, label):
    if n not in mapping:
        print(f"  !! {label}: old line {n} not in equal block (changed/deleted): {old[n-1][:90]!r}")
        return None
    m = mapping[n]
    if new[m - 1] != old[n - 1]:
        print(f"  !! {label}: content mismatch old {n} -> new {m}")
        return None
    return m

def find_line(frag, label, startswith=False):
    hits = [i + 1 for i, l in enumerate(new) if (l.startswith(frag) if startswith else frag in l)]
    if len(hits) != 1:
        print(f"  !! {label}: frag {frag[:50]!r} hits={hits}")
        return None
    return hits[0]

# ---------- travel114 ----------
path = f"{ROOT}/tests/test_travel114_static.py"
src = open(path, encoding="utf-8").read()
lines = src.split("\n")

def remap_set(lines, start_marker):
    si = next(i for i, l in enumerate(lines) if l.startswith(start_marker))
    ei = next(i for i in range(si + 1, len(lines)) if lines[i] == "}")
    out, removed = [], []
    for i in range(si + 1, ei):
        m = re.match(r"^(\s*)(\d+),(.*)$", lines[i])
        if not m:
            out.append(lines[i])
            continue
        n = int(m.group(2))
        mapped = map_line(n, f"{start_marker} {n}")
        if mapped is None:
            removed.append((n, lines[i].strip()))
            continue
        out.append(f"{m.group(1)}{mapped},{m.group(3)}")
    lines[si + 1:ei] = out
    return removed

rem_c = remap_set(lines, "COUNT_LINES = {")
rem_f = remap_set(lines, "FREE_LINES = {")
print("travel114 removed COUNT:", rem_c)
print("travel114 removed FREE:", rem_f)
for name in ("DEF_LINE", "WRAPPER_LINE"):
    for i, l in enumerate(lines):
        m = re.match(rf"^{name} = (\d+)(.*)$", l)
        if m:
            mapped = map_line(int(m.group(1)), name)
            lines[i] = f"{name} = {mapped}{m.group(2)}"
            print(f"{name}: {m.group(1)} -> {mapped}")
            break
note = ("# v393-endings resync：index.html 淨 +607 行（結局梯十項修復，底係 cfd8b2b）；"
        "COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移，見 qa392/resync393_endings.py。")
lines.insert(0, note)
open(path, "w", encoding="utf-8").write("\n".join(lines))
print("travel114 done")

# ---------- rom159 ----------
path = f"{ROOT}/tests/test_rom159_static.py"
src = open(path, encoding="utf-8").read()
pins159 = [
    (27256, "v20a159 ROM159 Phase 1"),
    (9289, "rom159GainAllowed(k)"),
    (28164, "COMMIT48_NODES.CMT_lan_commit"),
    (11459, "rom159PrepareNode(node)"),
    (15739, "rom159ApplyGiftOverrides()"),
    (28019, "function rom159SoMeetGate"),
]
repl = {}
for n, frag in pins159:
    assert frag in old[n - 1], f"rom159 old pin {n} frag mismatch: {old[n-1][:80]!r}"
    m = map_line(n, f"rom159 {n}")
    if m is None:
        m = find_line(frag, f"rom159 {n}")
    repl[f"line_has({n},"] = f"line_has({m},"
    print(f"rom159 {n} -> {m} ({frag[:40]})")
for a, b in repl.items():
    assert src.count(a) == 1, a
    src = src.replace(a, b)
# 全佳行：舊 27284（cfd8b2b 值）→ difflib 映射
assert "查實" in old[27284 - 1], f"rom159 全佳 old line mismatch: {old[27283][:80]!r}"
m_full = map_line(27284, "rom159 全佳")
if m_full is None:
    m_full = find_line("查實", "rom159 全佳")
assert m_full is not None
a = "idx_lines[27284 - 1]"
b = f"idx_lines[{m_full} - 1]"
assert src.count(a) == 1, a
src = src.replace(a, b)
src = src.replace("# v391 resync（26982→27225，difflib 核實）",
                  f"# v393-endings resync（27284→{m_full}，difflib 核實）  # v391 resync（26982→27225，difflib 核實）")
src = "# v393-endings resync：index.html 淨 +607 行（結局梯十項修復，底係 cfd8b2b）；6 個 line_has 釘行＋全佳行按 difflib 映射重寫，內容逐字核實純漂移，見 qa392/resync393_endings.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print(f"rom159 done (全佳 27284 -> {m_full})")

# ---------- rom176 ----------
path = f"{ROOT}/tests/test_rom176_static.py"
src = open(path, encoding="utf-8").read()
pins176 = [
    (7428, "startswith", '  lan:{ id:"lan", name:"藍若曦"'),
    (15737, "contains", "GIFT_REACT = giftReact"),
    (42933, "startswith", "/* ===== v20a176 ROM176"),
    (43292, "startswith", "function rom176ApplyGiftOverrides()"),
    (44858, "startswith", "function addLocTalkGiftActs(add, L, npcId)"),
    (44979, "contains", "rom176TryIntercept(id)"),
]
repl = {}
for n, kind, frag in pins176:
    assert frag in old[n - 1], f"rom176 old pin {n} frag mismatch: {old[n-1][:80]!r}"
    m = map_line(n, f"rom176 {n}")
    if m is None:
        m = find_line(frag, f"rom176 {n}", startswith=(kind == "startswith"))
    repl[f"line({n})"] = f"line({m})"
    print(f"rom176 {n} -> {m} ({frag[:40]})")
for a, b in repl.items():
    assert src.count(a) >= 1, a
    src = src.replace(a, b)
src = "# v393-endings resync：index.html 淨 +607 行（結局梯十項修復，底係 cfd8b2b）；6 個釘行按 difflib 映射重寫，內容逐字核實純漂移，見 qa392/resync393_endings.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("rom176 done")

# ---------- tang152 (0-indexed lines()[N]) ----------
path = f"{ROOT}/tests/test_tang152_static.py"
src = open(path, encoding="utf-8").read()
for n0, frag in [(15666, "function normaliseTangStub152(pack){"), (15791, "try{ normaliseTangStub152(rom2);")]:
    n = n0 + 1  # to 1-indexed
    assert frag in old[n - 1], f"tang152 old pin {n0} frag mismatch: {old[n-1][:80]!r}"
    m = map_line(n, f"tang152 {n0}")
    if m is None:
        m = find_line(frag, f"tang152 {n0}")
    a = f"lines()[{n0}]"
    b = f"lines()[{m - 1}]"
    assert src.count(a) == 1, a
    src = src.replace(a, b)
    print(f"tang152 lines()[{n0}] -> lines()[{m - 1}] ({frag[:40]})")
src = "# v393-endings resync：index.html 淨 +607 行（結局梯十項修復，底係 cfd8b2b）；normaliseTangStub152 兩釘按 difflib 映射重寫，內容逐字核實純漂移，見 qa392/resync393_endings.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("tang152 done")

# ---------- text125 (3 anchors: currentLine / advance / applyFamilySafe) ----------
path = f"{ROOT}/tests/test_text125_static.py"
src = open(path, encoding="utf-8").read()
FALLBACK = '(typeof b.text === "string" && b.text ? [b.text] : [])'
pins125 = [
    (12039, FALLBACK, "currentLine"),
    (12181, FALLBACK, "advance"),
    (17383, 'if(typeof b.text === "string" && b.text){', "applyFamilySafeToNode"),
]
for n, frag, label in pins125:
    assert frag in old[n - 1], f"text125 old pin {n} frag mismatch: {old[n-1][:80]!r}"
    m = map_line(n, f"text125 {label} {n}")
    if m is None:
        m = find_line(frag, f"text125 {label} {n}")
    assert m is not None, label
    a1, b1 = f"len(ls) < {n} or", f"len(ls) < {m} or"
    a2, b2 = f"ls[{n - 1}]", f"ls[{m - 1}]"
    a3, b3 = f"第 {n} 行", f"第 {m} 行"
    assert src.count(a1) == 1, (label, a1)
    assert src.count(a2) == 1, (label, a2)
    assert src.count(a3) == 1, (label, a3)
    src = src.replace(a1, b1).replace(a2, b2).replace(a3, b3)
    print(f"text125 {label} {n} -> {m}")
src = "# v393-endings resync：index.html 淨 +607 行（結局梯十項修復，底係 cfd8b2b）；三錨點按 difflib 映射重寫，內容逐字核實純漂移，報錯字串行號一併更新，見 qa392/resync393_endings.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("text125 done")

# ---------- gift185 / tang171 / tang173 totals ----------
new_total = len(new) - 1
old_total = len(old) - 1
delta = new_total - old_total
def_line_new = find_line("function openLoc(id, opts){", "openLoc DEF", startswith=True)
def_line_old = [i + 1 for i, l in enumerate(old) if l.startswith("function openLoc(id, opts){")][0]
print(f"total {old_total} -> {new_total} (delta {delta}); openLoc DEF {def_line_old} -> {def_line_new}")
for fname in ("test_gift185_static.py", "test_tang171_static.py", "test_tang173_static.py"):
    path = f"{ROOT}/tests/{fname}"
    src = open(path, encoding="utf-8").read()
    assert f"總行數 {old_total}" in src, fname
    src = src.replace(f"總行數 {old_total}", f"總行數 {new_total}")
    src = src.replace(f"== {old_total}", f"== {new_total}")
    src = src.replace("＋v392 +146）", f"＋v392 +146＋v393-endings +{delta}）")
    if f"openLoc DEF 行 {def_line_old}" in src:
        src = src.replace(f"openLoc DEF 行 {def_line_old}", f"openLoc DEF 行 {def_line_new}")
        src = src.replace(f"len(lines) >= {def_line_old}", f"len(lines) >= {def_line_new}")
        src = src.replace(f"lines[{def_line_old - 1}]", f"lines[{def_line_new - 1}]")
        src = src.replace("，travel114 釘行）", f"＋v393-endings +{def_line_new - def_line_old}，travel114 釘行）")
    open(path, "w", encoding="utf-8").write(src)
    print(fname, "done")

print("ALL DONE")
