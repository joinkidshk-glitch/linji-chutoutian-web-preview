# -*- coding: utf-8 -*-
"""v20a178 resync：五份測試因 v178 插行漂移，全套初跑 232/17 由 suite 捉到。
v178 改動（index.html 淨 +25 行，全部喺 openLoc DEF 之前）：
  (a) AWARDS64 註解 +1 行（L46738 附近）；
  (b) AWARDS64_SPRITES 加 ko 3 張（yip_manji_walkB 行加逗號＋3 行新 key）；
  (c) awards63Fellows 加第三步特別名額 +21 行（L46917 附近）。
方法：difflib 直接對 HEAD index（pristine）同工作副本 index 逐行對位，舊行 → 新行
dict 查表，單次掃描改測試檔（唔逐對 re.sub，免撞值；唔 blanket txt.replace 改
prose 數字，只改 code 行）。只改測試檔釘行數字＋每檔一行 resync 註解，唔郁遊戲檔。
另外兩份 sprite 數目測試（test_awards63_static／test_awards64_chibi_static）唔係釘行，
係 34→37 張基線更新，唔喺呢個腳本入面，獨立改。
用法：python3 qa178/resync178.py（喺工作副本跑；跑完逐檔跑返對應測試核實）。
"""
import difflib
import re
import subprocess
from pathlib import Path

ROOT = Path("/home/hatch/workspace/linji-work178")
OLD_TEXT = subprocess.check_output(
    ["git", "-C", str(ROOT), "show", "HEAD:index.html"], text=True)
NEW_TEXT = (ROOT / "index.html").read_text(encoding="utf-8")
old_lines = OLD_TEXT.split("\n")
new_lines = NEW_TEXT.split("\n")
print(f"old {len(old_lines)} split-lines, new {len(new_lines)} split-lines")
print(f"old count(chr(10))={OLD_TEXT.count(chr(10))}, "
      f"new count(chr(10))={NEW_TEXT.count(chr(10))}")

mapping = {}
hunks = []
sm = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
    else:
        hunks.append((tag, i1 + 1, i2, j1 + 1, j2))
print(f"mapped {len(mapping)} equal lines; non-equal hunks: {hunks}")
# 只得 v178 三段：註解 insert 1 行／yip 行 replace 1→4 行／fellows insert 21 行
assert len(hunks) == 3, hunks
assert sorted(h[0] for h in hunks) == ["insert", "insert", "replace"], hunks

NEW_TOTAL = NEW_TEXT.count("\n")
print(f"new total (count newline) = {NEW_TOTAL}")

# --- 每檔釘行（HEAD 行號；travel114 兩組由測試檔本身 parse，唔手抄） ---
def parse_set(text, name):
    m = re.search(name + r"\s*=\s*\{([^}]*)\}", text, re.S)
    assert m, name
    vals = []
    for ln in m.group(1).split("\n"):
        mm = re.match(r"\s*(\d+)\s*,?\s*(#.*)?$", ln)
        if mm:
            vals.append(int(mm.group(1)))
    return sorted(vals)

t114 = (ROOT / "tests/test_travel114_static.py").read_text(encoding="utf-8")
count_lines = parse_set(t114, "COUNT_LINES")
free_lines = parse_set(t114, "FREE_LINES")
print(f"travel114 COUNT {len(count_lines)} FREE {len(free_lines)}")
assert len(count_lines) == 13 and len(free_lines) == 27

PINS = {
    "tests/test_tang171_static.py": [59356, 53875, 53874],
    "tests/test_tang173_static.py": [59356, 53875, 53874],
    "tests/test_travel114_static.py": count_lines + free_lines + [53875, 44250],
}

# 內容核實：每粒釘行舊行內容＝新行內容（逐字相同，純漂移）；總行數另外處理
for rel, pins in PINS.items():
    for p in pins:
        if p == 59356:
            continue
        assert p in mapping, f"{rel}: 釘行 {p} 唔喺 equal block（內容俾 v178 改咗？）"
        assert old_lines[p - 1] == new_lines[mapping[p] - 1], (
            f"{rel}: 釘行 {p}->{mapping[p]} 內容唔同："
            f"{old_lines[p-1][:60]!r} vs {new_lines[mapping[p]-1][:60]!r}")
print("all pins content-verified")

MAPS = {}
for rel, pins in PINS.items():
    MAPS[rel] = {p: mapping[p] for p in pins if p != 59356}
MAPS["tests/test_tang171_static.py"][59356] = NEW_TOTAL
MAPS["tests/test_tang173_static.py"][59356] = NEW_TOTAL

NUM = re.compile(r"(?<!\d)(\d{5})(?!\d)")
# 唔郁嘅行範圍（1-based）：歷史註解入面嘅舊行號
SKIP = {
    "tests/test_tang171_static.py": [(1, 31)],
    "tests/test_tang173_static.py": [(1, 40)],
    "tests/test_travel114_static.py": [(1, 138)],
}
# 每檔加一行 resync 註解：插喺呢句錨之後
ANCHOR = {
    "tests/test_tang171_static.py": "# v20a173 rebase 上 main 0ecaeb3（v153）：同行改動，總行數 59341、DEF 53860 不變。",
    "tests/test_tang173_static.py": "# v20a173 rebase 上 main 0ecaeb3（v153）resync：總行數 59173→59341、DEF 53692→53860、CSS 同行 4832→4845、舊 rule L2016→L2024／L2040→L2048（逐項 grep＋git show 核實純漂移，單次掃描 dict 查表，見 NOTES_V20A173 §9）。",
    "tests/test_travel114_static.py": "# v20a153 第三輪 rebase 上 main a500536（v149）resync：difflib 對位核實純漂移，COUNT/FREE/DEF/WRAPPER 行號按映射重寫（見 qa153/resync_rebase153c.py）。",
}
NOTE = {
    "tests/test_tang171_static.py": "# v20a178 resync：v178 淨 ＋25 行（AWARDS64 註解＋1／ko sprite＋3／fellows 特別名額＋21），總行數 59356→59381、DEF 53875→53900（qa178/resync178.py difflib 對位核實純漂移）。",
    "tests/test_tang173_static.py": "# v20a178 resync：v178 淨 ＋25 行（AWARDS64 註解＋1／ko sprite＋3／fellows 特別名額＋21），總行數 59356→59381、DEF 53875→53900（qa178/resync178.py difflib 對位核實純漂移；全套初跑由 suite 捉到）。",
    "tests/test_travel114_static.py": "# v20a178 resync：v178 淨 ＋25 行全部喺釘行之前（AWARDS64 註解＋1／ko sprite＋3／fellows 特別名額＋21）；＜46738 者 ＋0、其後者 ＋25，COUNT 13／FREE 27 不變，DEF 53875→53900、WRAPPER 44250 唔郁（qa178/resync178.py difflib 對位核實純漂移）。",
}

for rel, mp in MAPS.items():
    src = (ROOT / rel).read_text(encoding="utf-8")
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
    missing = [k for k in mp if k not in hits]
    assert not missing, f"{rel}: 搵唔到 {missing}"
    anchor = ANCHOR[rel]
    assert anchor in out, f"{rel}: 錨句唔見咗"
    idx = out.index(anchor)
    out.insert(idx + 1, NOTE[rel])
    (ROOT / rel).write_text("\n".join(out), encoding="utf-8")
    print(f"{rel}: 改咗 {sum(hits.values())} 處")
    for k in sorted(hits):
        print(f"    {k} -> {mp[k]} x{hits[k]}")
print("RESYNC178 DONE")
