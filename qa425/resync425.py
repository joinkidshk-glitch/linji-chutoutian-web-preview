#!/usr/bin/env python3
"""v425 UI27 resync：index.html 淨 +64 行（53759→53823；篩選狀態行／合約分層／試鏡語意呈現層改動）。
行號釘按 difflib 映射重寫，內容逐字核實純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。
用法：python3 qa425/resync425.py（OLD 攞 HEAD=v424，assert 總行數 53759）。"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 53759, len(OLD) - 1
assert len(NEW) - 1 == 53823, len(NEW) - 1

_sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
_map = {}
for _tag, _i1, _i2, _j1, _j2 in _sm.get_opcodes():
    if _tag == "equal":
        for _k in range(_i2 - _i1):
            _map[_i1 + _k] = _j1 + _k

def map0(i):
    """0-based index map with content verification."""
    assert i in _map, f"index {i} not in equal map"
    j = _map[i]
    assert OLD[i] == NEW[j], f"content mismatch {i}->{j}"
    return j

def map1(n):
    return map0(n - 1) + 1

def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()

def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)

NOTE = "# v425 UI27 resync：index.html 淨 +64 行（53759→53823）；行號釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa425/resync425.py。"

def patch(path, subs):
    src = read(path)
    seen = set()
    for old, new, n in subs:
        if old in seen:
            continue
        seen.add(old)
        c = src.count(old)
        if c == 0 and new in src:
            continue  # 已 patch 過（重跑）
        assert c == n, f"{path}: {old[:60]!r} count={c} expect={n}"
        src = src.replace(old, new)
    if not src.split("\n")[0].startswith("# v425 UI27 resync"):
        lines = src.split("\n")
        lines.insert(0, NOTE)
        src = "\n".join(lines)
    write(path, src)
    print(f"patched {path}")

# 總行數鏈：53759→53823，鏈尾加 UI27 +64
for p in ["tests/test_gift185_static.py", "tests/test_tang171_static.py", "tests/test_tang173_static.py"]:
    src = read(p)
    subs = [("53759", "53823", src.count("53759")),
            ("＋v425 +38）", "＋v425 +38＋UI27 +64）", src.count("＋v425 +38）"))]
    patch(p, subs)

# openLoc DEF：lines[48483]（0-based）＋標籤 45724
for p in ["tests/test_tang171_static.py", "tests/test_tang173_static.py"]:
    src = read(p)
    subs = []
    if "lines[48483]" in src:
        subs.append(("lines[48483]", f"lines[{map0(48483)}]", src.count("lines[48483]")))
    if "45724" in src:
        subs.append(("45724", str(map1(45724)), src.count("45724")))
    if subs:
        patch(p, subs)

# tang173 L5356 釘：lines[5405]
src = read("tests/test_tang173_static.py")
if "lines[5405]" in src:
    patch("tests/test_tang173_static.py", [("lines[5405]", f"lines[{map0(5405)}]", src.count("lines[5405]"))])

# tang152：lines()[17300]、lines()[17425]
patch("tests/test_tang152_static.py", [
    ("lines()[17300]", f"lines()[{map0(17300)}]", 1),
    ("lines()[17425]", f"lines()[{map0(17425)}]", 1),
])

# rom159：line_has(N, ...) 1-based
src = read("tests/test_rom159_static.py")
subs = []
for m in re.finditer(r"line_has\((\d+),", src):
    n = int(m.group(1))
    subs.append((f"line_has({n},", f"line_has({map1(n)},", 1))
patch("tests/test_rom159_static.py", subs)

# rom176：line(N) 1-based（只改 body 釘，唔改 def line(n)）
src = read("tests/test_rom176_static.py")
subs = []
for m in re.finditer(r"(?<![\w])line\((\d+)\)", src):
    n = int(m.group(1))
    subs.append((f"line({n})", f"line({map1(n)})", src.count(f"line({n})")))
patch("tests/test_rom176_static.py", subs)

# travel114：FREE_LINES 等行號集合（1-based 數字行）
src = read("tests/test_travel114_static.py")
subs = []
for m in re.finditer(r"^    (\d+),", src, re.M):
    n = int(m.group(1))
    subs.append((f"    {n},", f"    {map1(n)},", 1))
for m in re.finditer(r"^    (\d+)$", src, re.M):
    n = int(m.group(1))
    subs.append((f"    {n}\n", f"    {map1(n)}\n", 1))
patch("tests/test_travel114_static.py", subs)

# text125：ls[N] 三錨（0-based）
patch("tests/test_text125_static.py", [
    ("ls[13264]", f"ls[{map0(13264)}]", 1),
    ("ls[13406]", f"ls[{map0(13406)}]", 1),
    ("ls[19190]", f"ls[{map0(19190)}]", 1),
    ("第 12761 行", f"第 {map0(13264)+1} 行", 1),
    ("第 12903 行", f"第 {map0(13406)+1} 行", 1),
    ("第 18619 行", f"第 {map0(19190)+1} 行", 1),
])

print("resync425 done")
