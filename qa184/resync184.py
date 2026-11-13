# -*- coding: utf-8 -*-
"""v20a184 resync：四份釘行測試因 v184 插行漂移，全套初跑工作版 241/16
（pristine 244/12；12 項穩定 FAIL 兩邊共有，新增 4 項全部係釘行）。
v184 改動（index.html 淨 +16 行，difflib hunks）：
  (a) C2 helper awardsCatsSorted184 ＋9 行（L45748 附近，renderAwardInviteHtml 之前）；
  (b) 請柬 catsBit182 註解＋1 行（L45761 附近）；
  (c) 結果卡註解＋1 行（L45778 附近）；
  (d) C1 DEEPS184 註解＋palette ＋4 行（L46479 附近）；
  (e) C1 deep184 取值＋漸變改用 deep ＋1 行淨（L46485 附近，2 行代 1 行）。
漂移段：＜45748 ＋0；其後 ＋16（全部插入點都喺 openLoc DEF 54510 之前）。
方法：跟 resync182——difflib 直接對 6ed68f8 index（pristine）同工作副本 index
逐行對位，舊行 → 新行 dict 查表，單次掃描改測試檔（唔逐對 re.sub，免撞值；
唔 blanket txt.replace 改 prose 數字，只改 code 行／釘行數字；歷史註解行用精確
字串替換，逐項 assert 唯一）。只改測試檔釘行數字＋每檔一行 resync 註解，唔郁遊戲檔。
用法：python3 qa184/resync184.py（喺工作副本跑；跑完逐檔跑返對應測試核實）。
"""
import difflib
import re
import subprocess
from pathlib import Path

ROOT = Path("/home/hatch/workspace/linji-work184")
OLD_TEXT = subprocess.check_output(
    ["git", "-C", str(ROOT), "show", "6ed68f8:index.html"], text=True)
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
# 全部非 equal hunk 都要落喺 v184 插入段 [45747, 46490] 內，唔准有其他改動
for tag, a, b, c, d in hunks:
    assert 45747 <= a <= 46490 and 45747 <= c <= 46490, (tag, a, b, c, d)
NEW_TOTAL = NEW_TEXT.count("\n")
print(f"new total (count newline) = {NEW_TOTAL}")
assert NEW_TOTAL == 60026, NEW_TOTAL
assert OLD_TEXT.count("\n") == 60010

# --- 每檔釘行（6ed68f8 行號） ---
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
assert len(count_lines) == 13 and len(free_lines) == 33

PINS = {
    "tests/test_rom176_static.py": [53050, 53415, 54447, 54541],
    "tests/test_tang171_static.py": [54510],
    "tests/test_tang173_static.py": [54510],
    "tests/test_travel114_static.py": count_lines + free_lines + [54510, 44337],
}
# 內容核實：每粒釘行舊行內容＝新行內容（逐字相同，純漂移）
for rel, pins in PINS.items():
    for p in pins:
        assert p in mapping, f"{rel}: 釘行 {p} 唔喺 equal block（內容俾 v184 改咗？）"
        assert old_lines[p - 1] == new_lines[mapping[p] - 1], (
            f"{rel}: 釘行 {p} 內容唔同：{old_lines[p-1][:60]!r} vs {new_lines[mapping[p]-1][:60]!r}")
        print(f"  pin {rel} {p} -> {mapping[p]} ok")
# 插入點之前嘅行唔郁
assert mapping[44337] == 44337 and mapping[31533] == 31533 and mapping[4847] == 4847
print("pre-insert pins unchanged: 44337/31533/4847 ok")


def replace_once(text, old, new, label):
    n = text.count(old)
    assert n == 1, f"{label}: {old!r} 出現 {n} 次（預期 1）"
    return text.replace(old, new)


RESYNC_NOTE_184 = "# v20a184 resync：v184 淨 ＋16 行（C2 helper＋9／請柬＋1／結果卡＋1／C1 DEEPS＋4／漸變＋1 淨）；＜45748 者唔郁、其後者 ＋16（qa184/resync184.py difflib 對位核實純漂移）。"

# --- rom176：四粒釘 ＋16 ---
p = ROOT / "tests/test_rom176_static.py"
t = p.read_text(encoding="utf-8")
for old in (53050, 53415, 54447, 54541):
    new = mapping[old]
    assert new == old + 16, (old, new)
    t = replace_once(t, f"L{old}", f"L{new}", f"rom176 L{old}")
    t = replace_once(t, f"line({old})", f"line({new})", f"rom176 line({old})")
t = replace_once(t,
                 "# v20a182 resync：v182 淨 ＋17 行，錨點按段 ＋2／＋12／＋17（NPCS 6028＋2、載入點 31531＋2、block 53033＋12、其後 ＋17；qa182/resync182.py difflib 對位核實純漂移）。",
                 "# v20a182 resync：v182 淨 ＋17 行，錨點按段 ＋2／＋12／＋17（NPCS 6028＋2、載入點 31531＋2、block 53033＋12、其後 ＋17；qa182/resync182.py difflib 對位核實純漂移）。\n" + RESYNC_NOTE_184,
                 "rom176 resync note")
p.write_text(t, encoding="utf-8")
print("rom176 resynced")

# --- tang171：總行數＋DEF ---
p = ROOT / "tests/test_tang171_static.py"
t = p.read_text(encoding="utf-8")
t = replace_once(t,
                 "總行數 60010（v170 59173＋v149 ＋97＋v153 ＋71＋v172 ＋15＋v175 ＋78＋v176 ＋538＋v178 ＋21＋v182 ＋17）",
                 "總行數 60026（v170 59173＋v149 ＋97＋v153 ＋71＋v172 ＋15＋v175 ＋78＋v176 ＋538＋v178 ＋21＋v182 ＋17＋v184 ＋16）",
                 "tang171 total prose")
t = replace_once(t, "src.count('\\n') == 60010", "src.count('\\n') == 60026", "tang171 total code")
t = replace_once(t,
                 "openLoc DEF 行 54510（v175 ＋78＋v176 ＋519＋v178 ＋21＋v182 ＋17）",
                 "openLoc DEF 行 54526（v175 ＋78＋v176 ＋519＋v178 ＋21＋v182 ＋17＋v184 ＋16）",
                 "tang171 def prose")
t = replace_once(t, "len(lines) >= 54510", "len(lines) >= 54526", "tang171 def guard")
t = replace_once(t, "lines[54509]", "lines[54525]", "tang171 def index")
t = replace_once(t,
                 "# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5），總行數 59993→60010、DEF 54493→54510（qa182/resync182.py difflib 對位核實純漂移）。",
                 "# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5），總行數 59993→60010、DEF 54493→54510（qa182/resync182.py difflib 對位核實純漂移）。\n" + RESYNC_NOTE_184,
                 "tang171 resync note")
p.write_text(t, encoding="utf-8")
print("tang171 resynced")

# --- tang173：總行數＋DEF（CSS L4847 喺插入點之前，唔郁） ---
p = ROOT / "tests/test_tang173_static.py"
t = p.read_text(encoding="utf-8")
t = replace_once(t, "ok('零行數漂移：總行數 60010', src.count('\\n') == 60010)",
                 "ok('零行數漂移：總行數 60026', src.count('\\n') == 60026)", "tang173 total")
t = replace_once(t,
                 "openLoc DEF 行 54510（v175 ＋78＋v176 ＋519＋v178 ＋21＋v182 ＋17）",
                 "openLoc DEF 行 54526（v175 ＋78＋v176 ＋519＋v178 ＋21＋v182 ＋17＋v184 ＋16）",
                 "tang173 def prose")
t = replace_once(t, "len(lines) >= 54510", "len(lines) >= 54526", "tang173 def guard")
t = replace_once(t, "lines[54509]", "lines[54525]", "tang173 def index")
t = replace_once(t,
                 "# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5），總行數 59993→60010、DEF 54493→54510、CSS 同行 4845→4847（qa182/resync182.py difflib 對位核實純漂移）。",
                 "# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5），總行數 59993→60010、DEF 54493→54510、CSS 同行 4845→4847（qa182/resync182.py difflib 對位核實純漂移）。\n" + RESYNC_NOTE_184,
                 "tang173 resync note")
p.write_text(t, encoding="utf-8")
print("tang173 resynced")

# --- travel114：COUNT／FREE sets 單次掃描 dict 查表＋DEF 54510→54526 ---
p = ROOT / "tests/test_travel114_static.py"
t = p.read_text(encoding="utf-8")
for name in ("COUNT_LINES", "FREE_LINES"):
    m = re.search(name + r"\s*=\s*\{([^}]*)\}", t, re.S)
    assert m, name
    block = m.group(0)
    def _sub(mm, _map=mapping):
        old = int(mm.group(2))
        return mm.group(1) + str(_map[old]) + mm.group(3)
    new_block = re.sub(r"(?m)^(\s*)(\d+)(,?)", _sub, block)
    assert new_block != block or all(mapping[v] == v for v in parse_set(t, name))
    t = t[:m.start()] + new_block + t[m.end():]
t = replace_once(t, "DEF_LINE = 54510", "DEF_LINE = 54526", "travel114 DEF_LINE")
assert "WRAPPER_LINE = 44337" in t  # 插入點之前，唔郁
t = replace_once(t,
                 "# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5）；＜45746 者 ＋2、其後者 ＋17，COUNT 13／FREE 33 不變，DEF 54493→54510、WRAPPER 44335→44337（qa182/resync182.py difflib 對位核實純漂移）。",
                 "# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5）；＜45746 者 ＋2、其後者 ＋17，COUNT 13／FREE 33 不變，DEF 54493→54510、WRAPPER 44335→44337（qa182/resync182.py difflib 對位核實純漂移）。\n" + RESYNC_NOTE_184,
                 "travel114 resync note")
p.write_text(t, encoding="utf-8")
print("travel114 resynced")
print("DONE")
