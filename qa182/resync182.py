# -*- coding: utf-8 -*-
"""v20a182 resync：七份釘行測試因 v182 插行漂移，全套初跑 237/19 由 suite 捉到
（pristine 243/12；12 項穩定 FAIL 兩邊共有，新增 7 項全部係釘行）。
v182 改動（index.html 淨 +17 行，difflib hunks）：
  (a) B1 CSS .awd62-fellows ＋1 行（L762 之後）；
  (b) C1 CSS 淨 ＋1 行（L799–809：新卡面 4 則＋刪 cssicon／cssname 2 則）；
  (c) 請柬 catsBit182 註解＋const ＋3 行（L45746 附近）＋模板 ＋1 行；
  (d) presentAwardInvite 落 story-play-on ＋6 行（L45827 附近）；
  (e) B1 JS 提名行換 class（同行，淨 0）；
  (f) C1 JS 淨 ＋5 行（L46447 附近：medLabel＋註解＋tint palette＋tint 行，刪 medName149）。
漂移段：＜762 ＋0；763–808 ＋1；809–45745 ＋2；45753–45826 ＋6；45827–46446 ＋12；其後 ＋17。
方法：跟 resync178——difflib 直接對 ece1fac index（pristine）同工作副本 index
逐行對位，舊行 → 新行 dict 查表，單次掃描改測試檔（唔逐對 re.sub，免撞值；
唔 blanket txt.replace 改 prose 數字，只改 code 行）。text125 行內歷史註解同
釘數字同行，唔行 dict，改用精確字串替換（逐項 assert 唯一）。只改測試檔釘行
數字＋每檔一行 resync 註解，唔郁遊戲檔。
用法：python3 qa182/resync182.py（喺工作副本跑；跑完逐檔跑返對應測試核實）。
"""
import difflib
import re
import subprocess
from pathlib import Path

ROOT = Path("/home/hatch/workspace/linji-work182")
OLD_TEXT = subprocess.check_output(
    ["git", "-C", str(ROOT), "show", "ece1fac:index.html"], text=True)
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
assert len(hunks) == 7, hunks
NEW_TOTAL = NEW_TEXT.count("\n")
print(f"new total (count newline) = {NEW_TOTAL}")
assert NEW_TOTAL == 60010, NEW_TOTAL

# --- 每檔釘行（ece1fac 行號） ---
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
    "tests/test_kwan151_static.py": [25615, 25956, 25959, 25960, 25961, 26004, 26223,
                                 27169, 27202, 30968, 30976, 30977, 31019],
    "tests/test_tang152_static.py": [25774, 25775, 31457, 31458, 31601, 31602],
    "tests/test_text125_static.py": [27693, 27694, 27822, 27823, 33515, 33516, 33517, 33518],
    "tests/test_travel114_static.py": count_lines + free_lines + [54493, 44335],
    "tests/test_rom176_static.py": [6028, 31531, 53033, 53398, 54430, 54524],
    "tests/test_tang171_static.py": [54493, 54492],
    "tests/test_tang173_static.py": [54493, 54492, 4845, 4844],
}

# 內容核實：每粒釘行舊行內容＝新行內容（逐字相同，純漂移）
for rel, pins in PINS.items():
    for p in pins:
        assert p in mapping, f"{rel}: 釘行 {p} 唔喺 equal block（內容俾 v182 改咗？）"
        assert old_lines[p - 1] == new_lines[mapping[p] - 1], (
            f"{rel}: 釘行 {p}->{mapping[p]} 內容唔同："
            f"{old_lines[p-1][:60]!r} vs {new_lines[mapping[p]-1][:60]!r}")
print("all pins content-verified")

MAPS = {}
for rel, pins in PINS.items():
    MAPS[rel] = {p: mapping[p] for p in pins}
MAPS["tests/test_tang171_static.py"][59993] = NEW_TOTAL
MAPS["tests/test_tang173_static.py"][59993] = NEW_TOTAL
for rel in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    assert 59993 not in MAPS[rel] or MAPS[rel][59993] == NEW_TOTAL

NUM = re.compile(r"(?<!\d)(\d{4,5})(?!\d)")  # v182：4 位釘都有（rom176 L6028、tang173 L4845），只換 map 入面嘅數
# 唔郁嘅行範圍（1-based）：歷史註解入面嘅舊行號
SKIP = {
    "tests/test_kwan151_static.py": [(1, 38)],
    "tests/test_tang152_static.py": [(1, 27)],
    "tests/test_travel114_static.py": [(1, 138), (193, 206)],
    "tests/test_rom176_static.py": [(1, 59)],
    "tests/test_tang171_static.py": [(1, 40)],
    "tests/test_tang173_static.py": [(1, 36)],
}
# 每檔加一行 resync 註解：插喺呢句錨之後
ANCHOR = {
    "tests/test_kwan151_static.py": "# v151 落地 resync：v156（9c850f9）先落地，main 行號 +15（L733 插入 15 行），錨點由 e08a070 版 +15。",
    "tests/test_tang152_static.py": "# v20a176 resync：NPCS ＋7 行（插入點 L6017 之後），三個錨點一律 ＋7（qa176/resync176.py 逐行核實內容逐字相同，純漂移）。",
    "tests/test_text125_static.py": "# 用法：python3 tests/test_text125_static.py [path-to-index.html]",
    "tests/test_travel114_static.py": "# v20a153 第三輪 rebase 上 main a500536（v149）resync：difflib 對位核實純漂移，COUNT/FREE/DEF/WRAPPER 行號按映射重寫（見 qa153/resync_rebase153c.py）。",
    "tests/test_rom176_static.py": "# v20a176 ROM176 全面隨機巧遇・靜態測試：接線標記／紅線／玩家面文案／行號釘。",
    "tests/test_tang171_static.py": "# v20a176 第三輪 rebase 上 main c682cc2（v178）resync：v178 淨 ＋21（fellows 特別名額＋21；註解＋sprite 來回 ＋4−4 抵消），總行數 59972→59993、DEF 54472→54493（qa176/resync176_rebase3.py difflib 對位核實純漂移；三檔 rebase 衝突後取 v176 嗰邊，v178 註解行補返）。",
    "tests/test_tang173_static.py": "# v20a176 第三輪 rebase 上 main c682cc2（v178）resync：v178 淨 ＋21（fellows 特別名額＋21；註解＋sprite 來回 ＋4−4 抵消），總行數 59972→59993、DEF 54472→54493（qa176/resync176_rebase3.py difflib 對位核實純漂移；三檔 rebase 衝突後取 v176 嗰邊，v178 註解行補返）。",
}
NOTE = {
    "tests/test_kwan151_static.py": "# v20a182 resync：v182 淨 ＋17 行（B1 CSS＋1／C1 CSS 淨＋1／請柬＋4／presentAwardInvite＋6／C1 JS＋5），十三錨點一律 ＋2（qa182/resync182.py difflib 對位核實純漂移；A8／B2–B5／C1／C3／C4／E1 嗰 7 粒 line() 釘喺第一輪 head -6 截斷睇漏，補核實後一併更新）。",
    "tests/test_tang152_static.py": "# v20a182 resync：v182 淨 ＋17 行全部喺錨點之前，三錨點一律 ＋2（qa182/resync182.py difflib 對位核實純漂移；ok() 名標籤一併更新）。",
    "tests/test_text125_static.py": "# v20a182 resync：v182 淨 ＋17 行全部喺錨點之前，三錨點一律 ＋2（qa182/resync182.py difflib 對位核實內容逐字相同，純漂移；報錯字串行號一併更新）。",
    "tests/test_travel114_static.py": "# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5）；＜45746 者 ＋2、其後者 ＋17，COUNT 13／FREE 33 不變，DEF 54493→54510、WRAPPER 44335→44337（qa182/resync182.py difflib 對位核實純漂移）。",
    "tests/test_rom176_static.py": "# v20a182 resync：v182 淨 ＋17 行，錨點按段 ＋2／＋12／＋17（NPCS 6028＋2、載入點 31531＋2、block 53033＋12、其後 ＋17；qa182/resync182.py difflib 對位核實純漂移）。",
    "tests/test_tang171_static.py": "# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5），總行數 59993→60010、DEF 54493→54510（qa182/resync182.py difflib 對位核實純漂移）。",
    "tests/test_tang173_static.py": "# v20a182 resync：v182 淨 ＋17 行（CSS＋2／請柬＋4／presentAwardInvite＋6／C1 JS＋5），總行數 59993→60010、DEF 54493→54510、CSS 同行 4845→4847（qa182/resync182.py difflib 對位核實純漂移）。",
}
EXPECTED_HITS = {
    "tests/test_kwan151_static.py": {25615: 3, 25956: 3, 25959: 3, 25960: 1, 25961: 1, 26004: 3,
                                 26223: 3, 27169: 1, 27202: 1, 30968: 4, 30976: 3, 30977: 2, 31019: 1},
    "tests/test_tang152_static.py": {25774: 1, 25775: 1, 31457: 1, 31458: 1, 31601: 1, 31602: 1},
    "tests/test_travel114_static.py": None,  # 每粒 1 次（set 內＋DEF／WRAPPER 各一）；下面逐項核實
    "tests/test_rom176_static.py": {6028: 2, 31531: 3, 53033: 2, 53398: 2, 54430: 2, 54524: 2},
    "tests/test_tang171_static.py": {59993: 2, 54493: 2, 54492: 1},
    "tests/test_tang173_static.py": {59993: 2, 54493: 2, 54492: 1, 4845: 3, 4844: 8},
}

# --- dict 單次掃描（text125 除外） ---
# 已完成嘅檔（上一輪寫入，唔重跑——舊釘號已唔喺檔入面）
DONE = {"tests/test_kwan151_static.py", "tests/test_tang152_static.py",
        "tests/test_travel114_static.py"}
for rel, mp in MAPS.items():
    if rel == "tests/test_text125_static.py" or rel in DONE:
        continue
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
    exp = EXPECTED_HITS.get(rel)
    if exp is not None:
        assert hits == exp, f"{rel}: 命中數唔符：{hits} vs 預期 {exp}"
    else:
        assert all(v == 1 for v in hits.values()), f"{rel}: 有釘行命中唔只一次：{hits}"
        assert len(hits) == len(mp), f"{rel}: 命中粒數唔符"
    anchor = ANCHOR[rel]
    assert anchor in out, f"{rel}: 錨句唔見咗"
    idx = out.index(anchor)
    out.insert(idx + 1, NOTE[rel])
    (ROOT / rel).write_text("\n".join(out), encoding="utf-8")
    print(f"{rel}: 改咗 {sum(hits.values())} 處")
    for k in sorted(hits):
        print(f"    {k} -> {mp[k]} x{hits[k]}")

# --- text125：精確字串替換（行內歷史數字唔郁） ---
rel = "tests/test_text125_static.py"
src = (ROOT / rel).read_text(encoding="utf-8")
TEXT125_REPL = [
    ("if len(ls) < 27694 or FALLBACK not in ls[27693]:",
     "if len(ls) < 27696 or FALLBACK not in ls[27695]:"),
    ('"currentLine 第 27694 行冇 text fallback"',
     '"currentLine 第 27696 行冇 text fallback"'),
    ("if len(ls) < 27823 or FALLBACK not in ls[27822]:",
     "if len(ls) < 27825 or FALLBACK not in ls[27824]:"),
    ('"advance 第 27823 行冇 text fallback"',
     '"advance 第 27825 行冇 text fallback"'),
    ("行號 33516–33518，rebase 重對",
     "行號 33518–33520，rebase 重對"),
    ("if len(ls) < 33518 or 'if(typeof b.text === \"string\" && b.text){' not in ls[33515]:",
     "if len(ls) < 33520 or 'if(typeof b.text === \"string\" && b.text){' not in ls[33517]:"),
    ('"applyFamilySafeToNode 第 33516 行冇 b.text 分支"',
     '"applyFamilySafeToNode 第 33518 行冇 b.text 分支"'),
]
for old, new in TEXT125_REPL:
    assert src.count(old) == 1, f"text125: {old[:40]!r} 出現 {src.count(old)} 次（預期 1）"
    src = src.replace(old, new)
out = src.split("\n")
anchor = ANCHOR[rel]
assert anchor in out, f"{rel}: 錨句唔見咗"
out.insert(out.index(anchor) + 1, NOTE[rel])
(ROOT / rel).write_text("\n".join(out), encoding="utf-8")
print(f"{rel}: 精確替換 {len(TEXT125_REPL)} 處")

# --- tang171／tang173 公式鏈＋tang173 L4845 括號 prose（dict 唔覆蓋） ---
# tang171：總行數名＋DEF 名各一（2 處）；tang173：得 DEF 名有鏈（1 處）
for rel, want in (("tests/test_tang171_static.py", 2), ("tests/test_tang173_static.py", 1)):
    src = (ROOT / rel).read_text(encoding="utf-8")
    old = "＋v178 ＋21）"
    assert src.count(old) == want, f"{rel}: 公式鏈 {old!r} 出現 {src.count(old)} 次（預期 {want}）"
    src = src.replace(old, "＋v178 ＋21＋v182 ＋17）")
    (ROOT / rel).write_text(src, encoding="utf-8")
    print(f"{rel}: 公式鏈 ＋v182 ＋17 x{want}")
rel = "tests/test_tang173_static.py"
src = (ROOT / rel).read_text(encoding="utf-8")
old = "（冇插行，kwan151／tang152 釘行唔使 resync）"
assert src.count(old) == 1, f"{rel}: L4845 括號出現 {src.count(old)} 次（預期 1）"
src = src.replace(old, "（v182 CSS 插 2 行，kwan151／tang152 釘行一併 resync）")
(ROOT / rel).write_text(src, encoding="utf-8")
print(f"{rel}: L4845 括號 prose 更新 x1")
print("RESYNC182 DONE")
