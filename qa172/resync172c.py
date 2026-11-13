# -*- coding: utf-8 -*-
"""v20a172 rebase 上 main e2add29（v174）resync：五份釘行測試再漂移。
合併後 index.html = main e2add29（59341 行）＋ v172 4 hunks 淨 ＋15 行
（start() ignoreSheetLoc ＋5／強制播 ＋5／C1 framing ＋3＋2）。
方法：difflib 直接對 main index（/tmp/index_main_e2add29.html）同合併後
index（工作副本）逐行對位，舊行 → 新行 dict 查表，單次掃描改測試檔
（唔逐對 re.sub，免撞值；唔 blanket txt.replace 改 prose 數字，只改 code 行）。
來源檔係工作副本現況（rebase 衝突解法：五檔取 main 版 --ours——main 對呢
五檔嘅改動本身純係 resync，tang171 另有 v173 兩條斷言更新 78%→60%／.h
!important，必須保留；my-side 只有 resync，唔會丟嘢）。
用法：python3 qa172/resync172c.py（喺工作副本跑；跑完逐檔跑返對應測試核實）。
只改測試檔釘行數字＋每檔一行 resync 註解，唔郁遊戲檔。
附註：test_tang173_static.py 唔喺原先五檔之內——全套初跑 234／13 由 suite 捉到
（佢都釘總行數＋openLoc DEF），之後用同一 mapping 補 resync（總行數／DEF 一併
＋15，見 NOTES §5.5）；下面 PINS 已補埋佢，作紀錄。
"""
import difflib
import re
from pathlib import Path

ROOT = Path("/home/hatch/workspace/linji-work172")
OLD = Path("/tmp/index_main_e2add29.html")
NEW = ROOT / "index.html"

old_lines = OLD.read_text(encoding="utf-8").split("\n")
new_lines = NEW.read_text(encoding="utf-8").split("\n")
print(f"old {len(old_lines)} lines, new {len(new_lines)} lines")

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
# 合併後 index 只差 v172 4 個 replace hunks，其餘逐行相同
assert len(hunks) == 4 and all(h[0] == "replace" for h in hunks), hunks

# 每檔釘行（main e2add29 行號；總行數另外處理）
PINS = {
    "tests/test_tang171_static.py": [59341, 53860, 53859],
    "tests/test_tang152_static.py": [25758, 25757, 31436, 31435, 31580, 31579],
    "tests/test_text125_static.py": [27672, 27671, 27801, 27800, 33496, 33493, 33494],
    "tests/test_travel114_static.py": [
        32110, 35591, 37718, 38784, 39218, 39221, 39252, 43806,
        57908, 58075, 58218, 58239, 58689,
        24625, 28155, 30777, 30778, 30790, 30791, 30802, 30803,
        30906, 40761, 43463, 43486, 52735, 52854, 53747, 54129,
        54151, 54302, 55939, 57350, 57683, 57801, 57802, 57837,
        57838, 57857, 57872,
        53860, 44235,
    ],
    "tests/test_kwan151_static.py": [
        25598, 25939, 25987, 26206, 25944, 25942, 25943,
        30955, 30946, 30997, 30954, 27180, 27147,
    ],
    # suite 捉到後補：同樣釘總行數＋openLoc DEF
    "tests/test_tang173_static.py": [59341, 53860, 53859],
}
NEW_TOTAL = len(new_lines) - (1 if new_lines and new_lines[-1] == "" else 0)
print(f"new total lines (wc-style): {NEW_TOTAL}")

# 內容核實：每粒釘行舊行內容＝新行內容（逐字相同，純漂移）
for rel, pins in PINS.items():
    for p in pins:
        assert p in mapping, f"{rel}: 釘行 {p} 唔喺 equal block（內容俾 v172 改咗？）"
        assert old_lines[p - 1] == new_lines[mapping[p] - 1], (
            f"{rel}: 釘行 {p}->{mapping[p]} 內容唔同：{old_lines[p-1][:60]!r} vs {new_lines[mapping[p]-1][:60]!r}")
print("all pins content-verified")

MAPS = {}
for rel, pins in PINS.items():
    MAPS[rel] = {p: mapping[p] for p in pins}
MAPS["tests/test_tang171_static.py"][59341] = NEW_TOTAL

NUM = re.compile(r"(?<!\d)(\d{5})(?!\d)")
# 唔郁嘅行範圍（1-based）：歷史註解入面嘅舊行號
SKIP = {
    "tests/test_tang171_static.py": [(1, 31)],
    "tests/test_tang152_static.py": [(1, 12)],
    "tests/test_text125_static.py": [(1, 11)],
    "tests/test_travel114_static.py": [(1, 138)],
    "tests/test_kwan151_static.py": [(1, 19)],
    "tests/test_tang173_static.py": [(1, 40)],
}
# 每檔加一行 resync 註解：插喺呢句錨之後
ANCHOR = {
    "tests/test_tang171_static.py": "# v20a173 rebase 上 main 0ecaeb3（v153）：同行改動，總行數 59341、DEF 53860 不變。",
    "tests/test_tang152_static.py": "# v20a153 第三輪 rebase 上 main a500536（v149）resync：HELD／normaliser／loader 三錨點 difflib 對位核實純漂移（見 qa153/resync_rebase153c.py）。",
    "tests/test_text125_static.py": "# v20a153 第三輪 rebase 上 main a500536（v149）resync：錨點 difflib 對位核實純漂移，行號按映射重寫（見 qa153/resync_rebase153c.py）。",
    "tests/test_travel114_static.py": "# v20a153 第三輪 rebase 上 main a500536（v149）resync：difflib 對位核實純漂移，COUNT/FREE/DEF/WRAPPER 行號按映射重寫（見 qa153/resync_rebase153c.py）。",
    "tests/test_kwan151_static.py": "# v20a153 第三輪 rebase 上 main a500536（v149）resync：difflib 對位核實純漂移，code 行錨點按映射重寫（見 qa153/resync_rebase153c.py）。",
    "tests/test_tang173_static.py": "# v20a173 rebase 上 main 0ecaeb3（v153）resync：總行數 59173→59341、DEF 53692→53860、CSS 同行 4832→4845、舊 rule L2016→L2024／L2040→L2048（逐項 grep＋git show 核實純漂移，單次掃描 dict 查表，見 NOTES_V20A173 §9）。",
}
NOTE = {
    "tests/test_tang171_static.py": "# v20a172 rebase 上 main e2add29（v174）resync：v172 4 hunks 淨 ＋15，總行數 59341→59356、DEF 53860→53875（qa172/resync172c.py difflib 對位核實純漂移）。",
    "tests/test_tang152_static.py": "# v20a172 rebase 上 main e2add29（v174）resync：HELD 唔郁（＜27080）、normaliser／loader ＋5（qa172/resync172c.py difflib 對位核實純漂移）。",
    "tests/test_text125_static.py": "# v20a172 rebase 上 main e2add29（v174）resync：三錨點一律 ＋5（qa172/resync172c.py difflib 對位核實純漂移）。",
    "tests/test_travel114_static.py": "# v20a172 rebase 上 main e2add29（v174）resync：COUNT／FREE 按段 ＋0／＋5／＋10／＋15，DEF 53860→53875、WRAPPER 44235→44250（qa172/resync172c.py difflib 對位核實純漂移）。",
    "tests/test_kwan151_static.py": "# v20a172 rebase 上 main e2add29（v174）resync：A 系列唔郁（＜27080）、C1／E1 ＋5、B／C3／C4／C5 ＋5（qa172/resync172c.py difflib 對位核實純漂移）。",
    "tests/test_tang173_static.py": "# v20a172 rebase 上 main e2add29（v174）resync：v172 4 hunks 淨 ＋15，總行數 59341→59356、DEF 53860→53875（qa172/resync172c.py difflib 對位核實純漂移；全套初跑由 suite 捉到，見 NOTES §5.5）。",
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
    # 加 resync 註解行（插喺錨句之後）
    anchor = ANCHOR[rel]
    assert anchor in out, f"{rel}: 錨句唔見咗"
    idx = out.index(anchor)
    out.insert(idx + 1, NOTE[rel])
    (ROOT / rel).write_text("\n".join(out), encoding="utf-8")
    print(f"{rel}: 改咗 {sum(hits.values())} 處")
    for k in sorted(mp):
        if mp[k] != k:
            print(f"    {k} -> {mp[k]}")
print("RESYNC172C DONE")
