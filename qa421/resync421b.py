#!/usr/bin/env python3
"""v421 resync 增量：E0 浮沉收尾喺 L15258 插入 6 行（53093→53099）。
舊釘（53093 座標）≥15258 者 +6；0-based idx ≥15257 者 +6。單次掃描逐 pattern 處理。"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(NEW) - 1 == 53099, len(NEW) - 1
INS = 15258  # 舊座標插入點（1-based）


def shift1(n):  # 1-based pin
    return n + 6 if n >= INS else n


def shift0(n):  # 0-based idx pin
    return n + 6 if n + 1 >= INS else n


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def bump_note(src):
    src = src.replace("淨 +23 行（53070→53093）", "淨 +29 行（53070→53099）")
    src = src.replace("淨 +23 行；", "淨 +29 行；")
    src = src.replace("53093", "53099")
    src = src.replace("+23）", "+29）")
    return src


# travel114 sets + DEF/WRAPPER
p = "tests/test_travel114_static.py"
src = read(p)


def sub_set(src, name):
    m = re.search(name + r" = \{(.*?)\n\}", src, re.S)
    assert m, name
    span = m.group(1)
    new_span, c = re.subn(r"^(\s*)(\d+),", lambda mm: f"{mm.group(1)}{shift1(int(mm.group(2)))},", span, flags=re.M)
    assert c > 0, name
    return src[:m.start(1)] + new_span + src[m.end(1):]


src = sub_set(src, "FREE_LINES")
src = sub_set(src, "COUNT_LINES")
for name in ("DEF_LINE", "WRAPPER_LINE"):
    src, c = re.subn(name + r" = (\d+)", lambda mm: f"{name} = {shift1(int(mm.group(1)))}", src)
    assert c == 1, name
write(p, bump_note(src))
print("patched", p)

PATS = [
    (r"line_has\((\d+),", lambda n: f"line_has({shift1(n)},"),
    (r"idx_lines\[(\d+)\]", lambda n: f"idx_lines[{shift0(n)}]"),
    (r"lines\(\)\[(\d+)\]", lambda n: f"lines()[{shift0(n)}]"),
    (r"lines\[(\d+)\]", lambda n: f"lines[{shift0(n)}]"),
    (r"line\((\d+)\)", lambda n: f"line({shift1(n)})"),
    (r"ls\[(\d+)\]", lambda n: f"ls[{shift0(n)}]"),
]

for p in ["tests/test_rom176_static.py", "tests/test_tang152_static.py",
          "tests/test_text125_static.py", "tests/test_rom159_static.py",
          "tests/test_gift185_static.py", "tests/test_tang171_static.py",
          "tests/test_tang173_static.py"]:
    src = read(p)
    total = 0
    for pat, fn in PATS:
        src, c = re.subn(pat, lambda mm, fn=fn: fn(int(mm.group(1))), src)
        total += c
    src = bump_note(src)
    write(p, src)
    print("patched", p, total, "pins")

print("RESYNC421B DONE")
