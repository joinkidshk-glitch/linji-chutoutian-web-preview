# -*- coding: utf-8 -*-
"""v20a178 第二次 rebase（上 main 91f264a／v175）resync。
背景：rebase 第一 commit 2d58c35 時 tang171／tang173／travel114 三檔衝突——
v175 同 v178 各自 resync 過同一批斷言（總行數／DEF／COUNT／FREE）。
解法：三檔先取 v175（ours）版為底，再用 difflib 對位重算：
  OLD = origin/main:index.html（59434 行，v175 落地版）
  NEW = 工作副本 index.html（v178 +25 行已合併：註解+1／ko sprite+3／fellows+21）
方法：舊行 -> 新行 dict 查表，單次掃描改測試檔（唔逐對 re.sub，免撞值；
唔 blanket txt.replace 改 prose 數字，只改 code 行——純註解行 skip）。
用法：python3 qa178/resync178b.py（喺工作副本跑；跑完逐檔跑返對應測試核實）。
"""
import difflib
import re
import subprocess
from pathlib import Path

ROOT = Path("/home/hatch/workspace/linji-work178")
OLD_TEXT = subprocess.check_output(
    ["git", "-C", str(ROOT), "show", "origin/main:index.html"], text=True)
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
# 淨 v178 三段：註解 insert 1 行／yip 行 replace 1→4 行／fellows insert 21 行
assert len(hunks) == 3, hunks
assert sorted(h[0] for h in hunks) == ["insert", "insert", "replace"], hunks

NEW_TOTAL = NEW_TEXT.count("\n")
print(f"new total (count newline) = {NEW_TOTAL}")
assert NEW_TOTAL == 59459, NEW_TOTAL  # 59434 + 25

# --- 每檔釘行（v175 版行號；travel114 兩組由測試檔本身 parse，唔手抄） ---
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
    "tests/test_tang171_static.py": [59434, 53953, 53952],
    "tests/test_tang173_static.py": [59434, 53953, 53952],
    "tests/test_travel114_static.py": count_lines + free_lines + [53953, 44328],
}

# 內容核實：每粒釘行舊行內容＝新行內容（逐字相同，純漂移）
for rel, pins in PINS.items():
    for p in pins:
        if p == 59434:
            continue
        assert p in mapping, f"{rel}: 釘行 {p} 唔喺 equal block（內容俾 v178 改咗？）"
        assert old_lines[p - 1] == new_lines[mapping[p] - 1], (
            f"{rel}: 釘行 {p}->{mapping[p]} 內容唔同："
            f"{old_lines[p-1][:60]!r} vs {new_lines[mapping[p]-1][:60]!r}")
print("all pins content-verified")

MAPS = {}
for rel, pins in PINS.items():
    MAPS[rel] = {p: mapping[p] for p in pins if p != 59434}
MAPS["tests/test_tang171_static.py"][59434] = NEW_TOTAL
MAPS["tests/test_tang173_static.py"][59434] = NEW_TOTAL

NUM = re.compile(r"(?<!\d)(\d{5})(?!\d)")
# 每檔加一行 resync 註解：插喺 v175 註解行之後（以開頭匹配，唔靠全行）
ANCHOR_START = {
    "tests/test_tang171_static.py": "# v20a175 rebase 上 main f09fa1b",
    "tests/test_tang173_static.py": "# v20a175 rebase 上 main f09fa1b",
    "tests/test_travel114_static.py": "# v20a175 rebase 上 main f09fa1b",
}
NOTE = {
    "tests/test_tang171_static.py": "# v20a178 第二次 rebase 上 main 91f264a（v175）resync：v178 ＋25 行（AWARDS64 註解＋1／ko sprite＋3／fellows 特別名額＋21）疊喺 v175 ＋78 之上，總行數 59434→59459、DEF 53953→53978（qa178/resync178b.py difflib 對位核實純漂移；三檔 rebase 衝突後以 v175 版為底重算）。",
    "tests/test_tang173_static.py": "# v20a178 第二次 rebase 上 main 91f264a（v175）resync：v178 ＋25 行（AWARDS64 註解＋1／ko sprite＋3／fellows 特別名額＋21）疊喺 v175 ＋78 之上，總行數 59434→59459、DEF 53953→53978（qa178/resync178b.py difflib 對位核實純漂移；三檔 rebase 衝突後以 v175 版為底重算）。",
    "tests/test_travel114_static.py": "# v20a178 第二次 rebase 上 main 91f264a（v175）resync：v178 ＋25 行（註解＋1／sprite＋3／fellows＋21，插入點新行號 46812／46847／46991；其後者 ＋25、之前者唔郁）；COUNT 13／FREE 27 不變，DEF 53953→53978、WRAPPER 44328 唔郁（qa178/resync178b.py difflib 對位核實純漂移；三檔 rebase 衝突後以 v175 版為底重算）。",
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
print("RESYNC178B DONE")
