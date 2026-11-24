#!/usr/bin/env python3
"""v394 resync：index.html 淨 +5 行（E0 加入 1992 floor 豁免：豁免函數前註解 +4 行
@舊 L14897–14901，CONSEQ61_REVIEWS 1992 註解 +1 行 @舊 L18516；其餘 1 對 1 替換，行數不變）。
行號釘按 difflib 對位映射重寫，逐行核實內容相同（純漂移）。舊釘值＝171f9c3（v393）版，
由現行測試檔動態抽出，唔係 cfd8b2b 版。
覆蓋：travel114（COUNT／FREE／DEF／WRAPPER）、rom159（6 釘＋全佳行）、rom176（6 釘）、
tang152（2 釘，0-indexed）、text125（3 錨點）、gift185／tang171／tang173（總行數＋openLoc DEF）。
單次掃描 dict 查表式替換（逐對 re.sub 會撞值，見 v162 教訓）；每對替換前 assert 出現次數＝1。
"""
import difflib
import re
import subprocess

ROOT = "/home/hatch/workspace/linji-work394"
old = subprocess.run(["git", "-C", ROOT, "show", "171f9c3:index.html"],
                     capture_output=True, text=True, check=True).stdout.split("\n")
new = open(f"{ROOT}/index.html", encoding="utf-8").read().split("\n")
print(f"old lines={len(old)} new lines={len(new)} delta={len(new)-len(old)}")
assert len(new) - len(old) == 5, "v394 預期淨 +5 行"
assert old[14901 - 1].startswith("function ending361FloorExempt"), old[14900][:80]
assert "E0" not in old[14901 - 1]

sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-indexed

errors = []
def map_line(n, label):
    if n not in mapping:
        errors.append(f"{label}: old line {n} not in equal block: {old[n-1][:90]!r}")
        print(f"  !! {label}: old line {n} not in equal block")
        return None
    m = mapping[n]
    if new[m - 1] != old[n - 1]:
        errors.append(f"{label}: content mismatch old {n} -> new {m}")
        print(f"  !! {label}: content mismatch old {n} -> new {m}")
        return None
    return m

def find_line(frag, label, startswith=False):
    hits = [i + 1 for i, l in enumerate(new) if (l.startswith(frag) if startswith else frag in l)]
    if len(hits) != 1:
        errors.append(f"{label}: frag {frag[:50]!r} hits={hits}")
        print(f"  !! {label}: frag hits={hits}")
        return None
    return hits[0]

def replace_once(src, a, b, label):
    assert src.count(a) == 1, f"{label}: {a!r} count={src.count(a)}"
    return src.replace(a, b)

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
note = ("# v394 resync：index.html 淨 +5 行（E0 豁免註解 ＋4＠舊 L14897／＋1＠舊 L18516）；"
        "COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移，見 qa394/resync394.py。")
lines.insert(0, note)
open(path, "w", encoding="utf-8").write("\n".join(lines))
print("travel114 done")

# ---------- rom159 ----------
path = f"{ROOT}/tests/test_rom159_static.py"
src = open(path, encoding="utf-8").read()
pins159 = sorted(set(int(x) for x in re.findall(r"line_has\((\d+),", src)))
print("rom159 pins:", pins159)
repl = {}
for n in pins159:
    m = map_line(n, f"rom159 {n}")
    if m is None:
        raise SystemExit("rom159 mapping failed")
    repl[f"line_has({n},"] = f"line_has({m},"
    print(f"rom159 {n} -> {m} ({old[n-1][:40].strip()})")
for a, b in repl.items():
    src = replace_once(src, a, b, "rom159")
m_full_old = int(re.search(r"idx_lines\[(\d+) - 1\]", src).group(1))  # 括號內數字本身就係 1-indexed 行號
assert "查實" in old[m_full_old - 1], f"rom159 全佳 old line mismatch: {old[m_full_old-1][:80]!r}"
m_full = map_line(m_full_old, "rom159 全佳")
a = f"idx_lines[{m_full_old} - 1]"
b = f"idx_lines[{m_full} - 1]"
src = replace_once(src, a, b, "rom159 全佳")
print(f"rom159 全佳 {m_full_old} -> {m_full}")
src = "# v394 resync：index.html 淨 +5 行（E0 豁免註解）；6 個 line_has 釘行＋全佳行按 difflib 映射重寫，內容逐字核實純漂移，見 qa394/resync394.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("rom159 done")

# ---------- rom176 ----------
path = f"{ROOT}/tests/test_rom176_static.py"
src = open(path, encoding="utf-8").read()
pins176 = sorted(set(int(x) for x in re.findall(r"line\((\d+)\)", src)))
print("rom176 pins:", pins176)
repl = {}
for n in pins176:
    m = map_line(n, f"rom176 {n}")
    if m is None:
        raise SystemExit("rom176 mapping failed")
    repl[f"line({n})"] = f"line({m})"
    print(f"rom176 {n} -> {m} ({old[n-1][:40].strip()})")
for a, b in repl.items():
    assert src.count(a) >= 1, a
    src = src.replace(a, b)
src = "# v394 resync：index.html 淨 +5 行（E0 豁免註解）；6 個釘行按 difflib 映射重寫，內容逐字核實純漂移，見 qa394/resync394.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("rom176 done")

# ---------- tang152 (0-indexed lines()[N]) ----------
path = f"{ROOT}/tests/test_tang152_static.py"
src = open(path, encoding="utf-8").read()
# 只取現行斷言兩行（ok() 行，非歷史註解）
op_lines = [l for l in src.split("\n") if l.startswith("ok(") and "lines()[" in l]
pins152 = sorted(set(int(x) for l in op_lines for x in re.findall(r"lines\(\)\[(\d+)\]", l)))
print("tang152 pins (0-indexed):", pins152)
for n0 in pins152:
    n = n0 + 1
    m = map_line(n, f"tang152 {n0}")
    if m is None:
        raise SystemExit("tang152 mapping failed")
    a = f"lines()[{n0}]"
    b = f"lines()[{m - 1}]"
    src = replace_once(src, a, b, "tang152")
    print(f"tang152 lines()[{n0}] -> lines()[{m - 1}] ({old[n-1][:40].strip()})")
src = "# v394 resync：index.html 淨 +5 行（E0 豁免註解）；normaliseTangStub152 兩釘按 difflib 映射重寫，內容逐字核實純漂移，見 qa394/resync394.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("tang152 done")

# ---------- text125 (3 anchors) ----------
path = f"{ROOT}/tests/test_text125_static.py"
src = open(path, encoding="utf-8").read()
pins125 = sorted(set(int(x) for x in re.findall(r"len\(ls\) < (\d+) or", src)))
print("text125 pins:", pins125)
for n in pins125:
    m = map_line(n, f"text125 {n}")
    if m is None:
        raise SystemExit("text125 mapping failed")
    a1, b1 = f"len(ls) < {n} or", f"len(ls) < {m} or"
    a2, b2 = f"ls[{n - 1}]", f"ls[{m - 1}]"
    a3, b3 = f"第 {n} 行", f"第 {m} 行"
    src = replace_once(src, a1, b1, f"text125 {n} a1")
    src = replace_once(src, a2, b2, f"text125 {n} a2")
    src = replace_once(src, a3, b3, f"text125 {n} a3")
    print(f"text125 {n} -> {m} ({old[n-1][:40].strip()})")
src = "# v394 resync：index.html 淨 +5 行（E0 豁免註解）；三錨點按 difflib 映射重寫，內容逐字核實純漂移，報錯字串行號一併更新，見 qa394/resync394.py。\n" + src
open(path, "w", encoding="utf-8").write(src)
print("text125 done")

# ---------- gift185 / tang171 / tang173 totals + openLoc DEF ----------
new_total = len(new) - 1  # src.count('\n')
old_total = len(old) - 1
delta = new_total - old_total
def_line_new = find_line("function openLoc(id, opts){", "openLoc DEF", startswith=True)
def_line_old = [i + 1 for i, l in enumerate(old) if l.startswith("function openLoc(id, opts){")][0]
print(f"total {old_total} -> {new_total} (delta {delta}); openLoc DEF {def_line_old} -> {def_line_new}")
assert delta == 5
for fname in ("test_gift185_static.py", "test_tang171_static.py", "test_tang173_static.py"):
    path = f"{ROOT}/tests/{fname}"
    lines = open(path, encoding="utf-8").read().split("\n")
    # 現行斷言行＝ok('總行數／ok('零行數漂移 開頭嗰行＋佢嘅下一行（DEF 檢查喺 continuation 行）；歷史註解唔郁
    op_idx = set()
    for i, l in enumerate(lines):
        if l.startswith("ok('總行數") or l.startswith("ok('零行數漂移"):
            op_idx.add(i)
            if i + 1 < len(lines):
                op_idx.add(i + 1)
    changed = []
    for i in sorted(op_idx):
        l = lines[i]
        nl = l
        if f"總行數 {old_total}" in nl:
            nl = nl.replace(f"總行數 {old_total}", f"總行數 {new_total}")
            nl = nl.replace(f"== {old_total}", f"== {new_total}")
            changed.append("total")
        if f"openLoc DEF 行 {def_line_old}" in nl:
            nl = nl.replace(f"openLoc DEF 行 {def_line_old}", f"openLoc DEF 行 {def_line_new}")
            changed.append("def-label")
        if f"len(lines) >= {def_line_old}" in nl:
            nl = nl.replace(f"len(lines) >= {def_line_old}", f"len(lines) >= {def_line_new}")
            changed.append("def-check")
        if f"lines[{def_line_old - 1}]" in nl:
            nl = nl.replace(f"lines[{def_line_old - 1}]", f"lines[{def_line_new - 1}]")
            changed.append("def-index")
        if "＋v393-endings" in nl and "＋v394" not in nl:
            # 喺 chain 尾加 ＋v394 +5（喺 ）或 ，travel114 之前）
            nl = nl.replace("＋v393-endings +607）", "＋v393-endings +607＋v394 +5）")
            nl = nl.replace("＋v393-endings +546，travel114", "＋v393-endings +546＋v394 +5，travel114")
            changed.append("chain")
        if nl != l:
            lines[i] = nl
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    print(fname, "done", changed)

if errors:
    print(f"ERRORS: {len(errors)}")
    for e in errors:
        print("  !!", e)
    raise SystemExit(1)
print("ALL DONE")
