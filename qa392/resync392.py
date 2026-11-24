#!/usr/bin/env python3
"""v392 resync：index.html 淨 +146 行（UI392 頭五項：日結／休息卡 dismiss、39 拍攝排程、
通告欄分層＋高版 modal、拍攝簿截字、頒獎快進提示＋雙焦；另 TDZ 修正＋片酬前綴＋
closest34 還原；插入點散佈 CSS／JS，全檔行號漂移）。
行號釘按 difflib 對位映射重寫，逐行核實內容相同（純漂移）。
覆蓋：travel114（COUNT／FREE／DEF／WRAPPER）、rom159（6 釘）、rom176（6 釘）、
tang152（2 釘，0-indexed）、text125（3 錨點）、gift185／tang171／tang173（總行數＋openLoc DEF）。"""
import difflib
import re
import subprocess

ROOT = "/home/hatch/workspace/linji-work392-ui"
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
note = ("# v392 resync：index.html 淨 +146 行（UI392 頭五項＋TDZ 修正）；"
        "COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移，見 qa392/resync392.py。")
lines.insert(0, note)
open(path, "w", encoding="utf-8").write("\n".join(lines))
print("travel114 done")

# ---------- rom159 ----------
path = f"{ROOT}/tests/test_rom159_static.py"
src = open(path, encoding="utf-8").read()
pins159 = [
    (27197, "v20a159 ROM159 Phase 1"),
    (9251, "rom159GainAllowed(k)"),
    (28105, "COMMIT48_NODES.CMT_lan_commit"),
    (11421, "rom159PrepareNode(node)"),
    (15701, "rom159ApplyGiftOverrides()"),
    (27960, "function rom159SoMeetGate"),
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
src = "# v392 resync：index.html 淨 +146 行（UI392 頭五項＋TDZ 修正）；6 個 line_has 釘行按 difflib 映射重寫，內容逐字核實純漂移，見 qa392/resync392.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("rom159 done")

# ---------- rom176 ----------
path = f"{ROOT}/tests/test_rom176_static.py"
src = open(path, encoding="utf-8").read()
pins176 = [
    (7390, "startswith", '  lan:{ id:"lan", name:"藍若曦"'),
    (15699, "contains", "GIFT_REACT = giftReact"),
    (42842, "startswith", "/* ===== v20a176 ROM176"),
    (43201, "startswith", "function rom176ApplyGiftOverrides()"),
    (44767, "startswith", "function addLocTalkGiftActs(add, L, npcId)"),
    (44888, "contains", "rom176TryIntercept(id)"),
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
src = "# v392 resync：index.html 淨 +146 行（UI392 頭五項＋TDZ 修正）；6 個釘行按 difflib 映射重寫，內容逐字核實純漂移，見 qa392/resync392.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("rom176 done")

# ---------- tang152 (0-indexed lines()[N]) ----------
path = f"{ROOT}/tests/test_tang152_static.py"
src = open(path, encoding="utf-8").read()
for n0, frag in [(15628, "function normaliseTangStub152(pack){"), (15753, "try{ normaliseTangStub152(rom2);")]:
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
src = "# v392 resync：index.html 淨 +146 行（UI392 頭五項＋TDZ 修正）；normaliseTangStub152 兩釘按 difflib 映射重寫，內容逐字核實純漂移，見 qa392/resync392.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("tang152 done")

# ---------- text125 (3 anchors: currentLine / advance / applyFamilySafe) ----------
path = f"{ROOT}/tests/test_text125_static.py"
src = open(path, encoding="utf-8").read()
FALLBACK = '(typeof b.text === "string" && b.text ? [b.text] : [])'
pins125 = [
    (12001, FALLBACK, "currentLine", "第 12001 行"),
    (12143, FALLBACK, "advance", "第 12143 行"),
    (17324, 'if(typeof b.text === "string" && b.text){', "applyFamilySafeToNode", "第 17324 行"),
]
for n, frag, label, msg_old in pins125:
    assert frag in old[n - 1], f"text125 old pin {n} frag mismatch: {old[n-1][:80]!r}"
    m = map_line(n, f"text125 {label} {n}")
    if m is None:
        m = find_line(frag, f"text125 {label} {n}")
    assert m is not None, label
    a1, b1 = f"len(ls) < {n} or", f"len(ls) < {m} or"
    a2, b2 = f"ls[{n - 1}]", f"ls[{m - 1}]"
    assert src.count(a1) == 1, (label, a1)
    assert src.count(a2) == 1, (label, a2)
    assert src.count(msg_old) == 1, (label, msg_old)
    src = src.replace(a1, b1).replace(a2, b2).replace(msg_old, f"第 {m} 行")
    print(f"text125 {label} {n} -> {m}")
src = "# v392 resync：index.html 淨 +146 行（UI392 頭五項＋TDZ 修正）；三錨點按 difflib 映射重寫，內容逐字核實純漂移，報錯字串行號一併更新，見 qa392/resync392.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("text125 done")

# ---------- rom159 全佳註解釘（resync392 補：27225 -> 27284，difflib 對位＋內容逐字核實純漂移） ----------
# 已於本腳本外獨立處理（見 tests/test_rom159_static.py L201 註解鏈）。

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
    src = src.replace("＋v391 +243", f"＋v391 +243＋v392 +{delta}")
    if f"openLoc DEF 行 {def_line_old}" in src:
        src = src.replace(f"openLoc DEF 行 {def_line_old}", f"openLoc DEF 行 {def_line_new}")
        src = src.replace(f"len(lines) >= {def_line_old}", f"len(lines) >= {def_line_new}")
        src = src.replace(f"lines[{def_line_old - 1}]", f"lines[{def_line_new - 1}]")
    open(path, "w", encoding="utf-8").write(src)
    print(fname, "done")
print("ALL DONE")
