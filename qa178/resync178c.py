# -*- coding: utf-8 -*-
"""v20a178 第二次 rebase（strip commit 上 91f264a）resync。
背景：cherry-pick 69f8f63（strip）時 tang171／tang173／travel114 三檔衝突——
strip 嗰 −4 行（AWARDS64 註解＋3 條 ko sprite key）要疊喺已 rebase 嘅
59459 行之上；三檔先取 ours（resync178b 版，59459／DEF 53978）為底，再用
difflib 對位重算：
  OLD = HEAD:index.html（59459 行，rebase 後未 strip）
  NEW = 工作副本 index.html（59455 行，strip 已合併）
方法：舊行 -> 新行 dict 查表，單次掃描改測試檔（唔逐對 re.sub，免撞值；
唔 blanket txt.replace 改 prose 數字，只改 code 行——純註解行 skip）。
用法：python3 qa178/resync178c.py（喺工作副本跑；跑完逐檔跑返對應測試核實）。
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
# 淨 strip 兩段：註解 delete 1 行／3 條 sprite key delete 3 行
assert len(hunks) == 2, hunks
assert sorted(h[0] for h in hunks) == ["delete", "delete"], hunks

NEW_TOTAL = NEW_TEXT.count("\n")
print(f"new total (count newline) = {NEW_TOTAL}")
assert NEW_TOTAL == 59455, NEW_TOTAL  # 59459 - 4

# --- 每檔釘行（resync178b 版行號；travel114 兩組由測試檔本身 parse，唔手抄） ---
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
    "tests/test_tang171_static.py": [59459, 53978, 53977],
    "tests/test_tang173_static.py": [59459, 53978, 53977],
    "tests/test_travel114_static.py": count_lines + free_lines + [53978, 44328],
}

# 內容核實：每粒釘行舊行內容＝新行內容（逐字相同，純漂移）
for rel, pins in PINS.items():
    for p in pins:
        if p == 59459:
            continue
        assert p in mapping, f"{rel}: 釘行 {p} 唔喺 equal block（內容俾 strip 改咗？）"
        assert old_lines[p - 1] == new_lines[mapping[p] - 1], (
            f"{rel}: 釘行 {p}->{mapping[p]} 內容唔同："
            f"{old_lines[p-1][:60]!r} vs {new_lines[mapping[p]-1][:60]!r}")
print("all pins content-verified")

MAPS = {}
for rel, pins in PINS.items():
    MAPS[rel] = {p: mapping[p] for p in pins if p != 59459}
MAPS["tests/test_tang171_static.py"][59459] = NEW_TOTAL
MAPS["tests/test_tang173_static.py"][59459] = NEW_TOTAL

NUM = re.compile(r"(?<!\d)(\d{5})(?!\d)")
# 每檔加一行 resync 註解：插喺 resync178b 註解行之後（以開頭匹配，唔靠全行）
ANCHOR_START = {
    "tests/test_tang171_static.py": "# v20a178 第二次 rebase 上 main 91f264a",
    "tests/test_tang173_static.py": "# v20a178 第二次 rebase 上 main 91f264a",
    "tests/test_travel114_static.py": "# v20a178 第二次 rebase 上 main 91f264a",
}
NOTE = {
    "tests/test_tang171_static.py": "# v20a178 strip 上 91f264a resync：strip 淨 −4 行（AWARDS64 註解＋1／ko sprite＋3），總行數 59459→59455、DEF 53978→53974（qa178/resync178c.py difflib 對位核實純漂移）。",
    "tests/test_tang173_static.py": "# v20a178 strip 上 91f264a resync：strip 淨 −4 行（AWARDS64 註解＋1／ko sprite＋3），總行數 59459→59455、DEF 53978→53974（qa178/resync178c.py difflib 對位核實純漂移）。",
    "tests/test_travel114_static.py": "# v20a178 strip 上 91f264a resync：strip 淨 −4 行（註解＋1／sprite＋3，刪除點新行號 46812／46848；其後者 −4、之前者唔郁）；COUNT 13／FREE 27 不變，DEF 53978→53974、WRAPPER 44328 唔郁（qa178/resync178c.py difflib 對位核實純漂移）。",
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

    out = []
    for ln_text in src.split("\n"):
        # 純註解行 skip（歷史行號 prose 唔郁）；code 行先改數
        if ln_text.lstrip().startswith("#"):
            out.append(ln_text)
        else:
            out.append(NUM.sub(repl, ln_text))
    missing = [k for k in mp if k not in hits]
    assert not missing, f"{rel}: 搵唔到 {missing}"
    anchor = next(i for i, l in enumerate(out)
                  if l.startswith(ANCHOR_START[rel]))
    out.insert(anchor + 1, NOTE[rel])
    (ROOT / rel).write_text("\n".join(out), encoding="utf-8")
    print(f"{rel}: 改咗 {sum(hits.values())} 處")
    for k in sorted(hits):
        print(f"    {k} -> {mp[k]} x{hits[k]}")
print("RESYNC178C DONE")
