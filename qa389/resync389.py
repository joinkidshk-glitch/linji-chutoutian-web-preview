#!/usr/bin/env python3
"""v389 resync：index.html 淨 +80 行（UI389：手帳 4 組 7 子＋拉柄＋傾談貼紙＋鎖定標籤；
刪 openAskPicker369／addLocGigActs／addLocBridgeActs／act_ho_tvb_rules）。
行號釘按 difflib 對位映射重寫，逐行核實內容相同（純漂移）；openAskPicker369 兩處
openLoc 呼叫點隨函數刪除，由 travel114 COUNT 清單移除（呼叫點總數 −2）。
覆蓋：travel114（COUNT／FREE／DEF／WRAPPER）、rom159（6 釘）、rom176（6 釘）、
gift185／tang171／tang173（總行數＋openLoc DEF）。
"""
import difflib
import re
import subprocess
import sys

ROOT = "/home/hatch/workspace/linji-work389"
old = subprocess.run(["git", "-C", ROOT, "show", "0447dfe:index.html"],
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
# DEF / WRAPPER
for name in ("DEF_LINE", "WRAPPER_LINE"):
    for i, l in enumerate(lines):
        m = re.match(rf"^{name} = (\d+)(.*)$", l)
        if m:
            mapped = map_line(int(m.group(1)), name)
            lines[i] = f"{name} = {mapped}{m.group(2)}"
            print(f"{name}: {m.group(1)} -> {mapped}")
            break
# resync 註解插喺檔案最頂
note = ("# v389 resync：index.html 淨 +80 行（UI389 手帳 4 組 7 子＋拉柄＋傾談貼紙＋鎖定標籤；"
        "刪 openAskPicker369／addLocGigActs／addLocBridgeActs／act_ho_tvb_rules）；"
        "COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移，見 qa389/resync389.py；"
        "openAskPicker369 兩處 COUNT 呼叫點隨函數刪除，呼叫點總數 −2。")
lines.insert(0, note)
open(path, "w", encoding="utf-8").write("\n".join(lines))
print("travel114 done")

# ---------- rom159 ----------
path = f"{ROOT}/tests/test_rom159_static.py"
src = open(path, encoding="utf-8").read()
pins159 = [
    (26917, "v20a159 ROM159 Phase 1"),
    (9064, "rom159GainAllowed(k)"),
    (27825, "COMMIT48_NODES.CMT_lan_commit"),
    (11234, "rom159PrepareNode(node)"),
    (15506, "rom159ApplyGiftOverrides()"),
    (27680, "function rom159SoMeetGate"),
]
repl = {}
for n, frag in pins159:
    # 先核實舊釘啱
    assert frag in old[n - 1], f"rom159 old pin {n} frag mismatch: {old[n-1][:80]!r}"
    m = map_line(n, f"rom159 {n}")
    if m is None:
        m = find_line(frag, f"rom159 {n}")
    repl[f"line_has({n},"] = f"line_has({m},"
    print(f"rom159 {n} -> {m} ({frag[:40]})")
for a, b in repl.items():
    assert src.count(a) == 1, a
    src = src.replace(a, b)
src = "# v389 resync：index.html 淨 +80 行（UI389）；6 個 line_has 釘行按 difflib 映射重寫，內容逐字核實純漂移，見 qa389/resync389.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("rom159 done")

# ---------- rom176 ----------
path = f"{ROOT}/tests/test_rom176_static.py"
src = open(path, encoding="utf-8").read()
pins176 = [
    (7195, "startswith", '  lan:{ id:"lan", name:"藍若曦"'),
    (15504, "contains", "GIFT_REACT = giftReact"),
    (42495, "startswith", "/* ===== v20a176 ROM176"),
    (42854, "startswith", "function rom176ApplyGiftOverrides()"),
    (44420, "startswith", "function addLocTalkGiftActs(add, L, npcId)"),
    (44581, "contains", "rom176TryIntercept(id)"),
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
src = "# v389 resync：index.html 淨 +80 行（UI389）；6 個釘行按 difflib 映射重寫，內容逐字核實純漂移，見 qa389/resync389.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("rom176 done")

# ---------- gift185 / tang171 / tang173 totals ----------
new_total = len(new) - 1  # html.count('\n') = split lines - 1
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
    # 喺總行數標籤尾（＋v388 +18）後加 ＋v389 +80
    src = src.replace("＋v388 +18）", f"＋v388 +18＋v389 +{delta}）")
    if f"openLoc DEF 行 {def_line_old}" in src:
        src = src.replace(f"openLoc DEF 行 {def_line_old}", f"openLoc DEF 行 {def_line_new}")
        src = src.replace(f"len(lines) >= {def_line_old}", f"len(lines) >= {def_line_new}")
        src = src.replace(f"lines[{def_line_old - 1}]", f"lines[{def_line_new - 1}]")
        src = src.replace("，travel114 釘行）", f"＋v389 +{def_line_new - def_line_old}，travel114 釘行）")
    open(path, "w", encoding="utf-8").write(src)
    print(fname, "done")
print("ALL DONE")
