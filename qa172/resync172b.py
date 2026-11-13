# -*- coding: utf-8 -*-
"""v20a172 rebase 上 v149 main (a500536) resync：五份釘行測試再漂移。
v149 index.html 淨 +97 行（CSS L778/L794 附近 ＋8、L4457 ＋5、典禮區 45594-47476
淨 ＋84），全部釘行都要再對一次。方法：difflib 直接對舊 index（e8c3a73＋v172
hunks，/tmp/index_pre_rebase149.html）同合併後 index（工作副本）逐行對位，
舊行 → 新行 dict 查表，單次掃描改測試檔（唔逐對 re.sub，免撞值）。
釘行表用 my-side（分支 v20a172）嘅值——即係舊 index 行號。
用法：python3 /tmp/resync172b.py（喺工作副本跑；跑完逐檔跑返對應測試核實）。
只改測試檔釘行數字，唔郁遊戲檔。
"""
import difflib
import re
import subprocess
from pathlib import Path

ROOT = Path("/home/hatch/workspace/linji-work172")
OLD = Path("/tmp/index_pre_rebase149.html")
NEW = ROOT / "index.html"

old_lines = OLD.read_text(encoding="utf-8").split("\n")
new_lines = NEW.read_text(encoding="utf-8").split("\n")
print(f"old {len(old_lines)} lines, new {len(new_lines)} lines")

# 舊行號（1-based）→ 新行號（1-based），只限 equal block
mapping = {}
sm = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
print(f"mapped {len(mapping)} equal lines")

# 每檔釘行（舊 index 行號；總行數另外處理）
PINS = {
    "tests/test_tang171_static.py": [53707, 53706],  # openLoc DEF（名＋0-based 索引）
    "tests/test_tang152_static.py": [25725, 25724, 31392, 31391, 31536, 31535],
    "tests/test_text125_static.py": [27644, 27643, 27757, 27756, 33452, 33449, 33450],
    "tests/test_travel114_static.py": [
        32066, 35547, 37674, 38745, 39179, 39182, 39213, 43763,
        57755, 57922, 58065, 58086, 58536,
        24612, 28111, 30733, 30734, 30746, 30747, 30758, 30759,
        30862, 40718, 43420, 43443, 52582, 52701, 53594, 53976,
        53998, 54149, 55786, 57197, 57530, 57648, 57649, 57684,
        57685, 57704, 57719,
        53707, 44187,
    ],
    "tests/test_kwan151_static.py": [
        25569, 25906, 25954, 26173, 25911, 25909, 25910,
        30911, 30902, 27152, 30953, 30910, 27119,
    ],
}
# 總行數：直接用新檔行數（wc -l 核實）
NEW_TOTAL = len(new_lines) - (1 if new_lines and new_lines[-1] == "" else 0)
print(f"new total lines (wc-style): {NEW_TOTAL}")

# 內容核實：每粒釘行舊行內容＝新行內容（逐字相同，純漂移）
for rel, pins in PINS.items():
    for p in pins:
        assert p in mapping, f"{rel}: 釘行 {p} 唔喺 equal block（內容俾 v149 改咗？）"
        assert old_lines[p - 1] == new_lines[mapping[p] - 1], (
            f"{rel}: 釘行 {p}→{mapping[p]} 內容唔同：{old_lines[p-1][:60]!r} vs {new_lines[mapping[p]-1][:60]!r}")
print("all pins content-verified")

# 每檔 {舊：新}（tang171 總行數 59188→NEW_TOTAL 另外加）
MAPS = {}
for rel, pins in PINS.items():
    MAPS[rel] = {p: mapping[p] for p in pins}
MAPS["tests/test_tang171_static.py"][59188] = NEW_TOTAL

NUM = re.compile(r"\b(\d{5})\b")
# 唔郁嘅行範圍（1-based）：歷史註解入面嘅舊行號
SKIP = {
    "tests/test_tang171_static.py": [(1, 27)],
    "tests/test_text125_static.py": [(10, 12)],
    "tests/test_travel114_static.py": [(1, 140)],
    "tests/test_kwan151_static.py": [(1, 27)],
    # tang152：頭註 L14 係現況說明要跟住改；其餘頭註數字唔喺 map 入面
}

for rel, mp in MAPS.items():
    src = subprocess.run(["git", "show", f"v20a172:tests/{Path(rel).name}"],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    hits = {}

    def repl(m, _mp=mp, _hits=hits):
        old = int(m.group(1))
        if old in _mp:
            _hits[old] = _hits.get(old, 0) + 1
            return str(_mp[old])
        return m.group(1)

    def skipped(ln, _sk=SKIP.get(rel, [])):
        return any(a <= ln <= b for a, b in _sk)

    out = []
    for i, ln_text in enumerate(src.split("\n"), 1):
        out.append(ln_text if skipped(i) else NUM.sub(repl, ln_text))
    new_text = "\n".join(out)
    missing = [k for k in mp if k not in hits]
    assert not missing, f"{rel}: 搵唔到 {missing}"
    (ROOT / rel).write_text(new_text, encoding="utf-8")
    print(f"{rel}: 改咗 {sum(hits.values())} 處")
    for k in sorted(mp):
        print(f"    {k} -> {mp[k]}")
print("RESYNC172B DONE")
