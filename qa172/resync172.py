# -*- coding: utf-8 -*-
"""v20a172 resync：index.html 淨 +15 行令五份釘行測試漂移，逐檔 dict 查表一次過 resync。
插入點（pristine 行號）＋淨增：
  L27080 後 ＋5（StoryPlay.start 註解＋ignoreSheetLoc 轉交）
  L38390-38391 後 ＋5（story165TryForcedPlay 註解＋ignoreSheetLoc:true）
  L44028 後 ＋3（C1 鎖行「（場景：X）」註解）
  L44032 後 ＋2（C1 OR 項註解）
漂移規則（pristine 行 L → 新行）：
  L<=27080：+0；27080<L<=38391：+5；38391<L<=44028：+10；
  44028<L<=44032：+13；L>44032：+15。
方法：每檔一次 re.sub 單掃描、dict 查表——唔逐對 re.sub，免撞值（例：travel114
FREE 同時有 57687→57702 同 57702→57717，逐對寫會撞）。
用法：python3 qa172/resync172.py（喺工作副本跑；跑完逐檔跑返對應測試核實）。
只改測試檔釘行數字，唔郁遊戲檔；內容本身 difflib 核實純漂移（見 NOTES §5.5）。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 每檔 {舊行號: 新行號}（索引值＝行號-1 嗰啲都列埋，例：ls[27638]→ls[27643]）
MAPS = {
    "tests/test_tang171_static.py": {
        59171: 59186,  # 總行數
        53690: 53705, 53689: 53704,  # openLoc DEF（名＋len 判斷＋0-based 索引）
    },
    "tests/test_tang152_static.py": {
        31387: 31392, 31386: 31391,  # normaliseTangStub152 函數在位
        31531: 31536, 31530: 31535,  # stub 正規化喺 TEXTFIX 之前
    },
    "tests/test_text125_static.py": {
        27639: 27644, 27638: 27643,  # currentLine fallback
        27752: 27757, 27751: 27756,  # advance fallback
        33445: 33450, 33447: 33452, 33444: 33449,  # applyFamilySafeToNode b.text
    },
    "tests/test_travel114_static.py": {
        # COUNT_LINES（13）
        32061: 32066, 35542: 35547, 37669: 37674, 38735: 38745,
        39169: 39179, 39172: 39182, 39203: 39213, 43753: 43763,
        57738: 57753, 57905: 57920, 58048: 58063, 58069: 58084, 58519: 58534,
        # FREE_LINES（26；24612 喺插入點之前唔郁）
        28106: 28111, 30728: 30733, 30729: 30734, 30741: 30746,
        30742: 30747, 30753: 30758, 30754: 30759, 30857: 30862,
        40708: 40718, 43410: 43420, 43433: 43443, 52565: 52580,
        52684: 52699, 53577: 53592, 53959: 53974, 53981: 53996,
        54132: 54147, 55769: 55784, 57180: 57195, 57513: 57528,
        57631: 57646, 57632: 57647, 57667: 57682, 57668: 57683,
        57687: 57702, 57702: 57717,
        # DEF／WRAPPER
        53690: 53705, 44172: 44187,
    },
    "tests/test_kwan151_static.py": {
        30906: 30911,  # B2 PHRASES
        30897: 30902,  # B3／B4／B5 EXACT C13
        27147: 27152,  # C1 speaker display
        30948: 30953,  # C3 relMap rel_mei
        30905: 30910,  # C4／C5 NOTE_EXACT
        27114: 27119,  # E1 speaker registry
        # A 系列（25569／25906／25954／26173／25909／25910／25911）喺插入點之前唔郁
    },
}

NUM = re.compile(r"\b(\d{5})\b")

# 唔郁嘅行範圍（1-based，含首尾）：歷史註解入面嘅舊行號唔可以跟住改
# （例：travel114 頭註「DEF 53668→53690」係 v165 (c) 嘅歷史，改咗就失真）。
SKIP = {
    "tests/test_tang171_static.py": [(1, 27)],   # 頭註（L20「總行數 59171 不變」係 v171 狀態，留返做歷史）
    "tests/test_text125_static.py": [(10, 10)],  # L10 長註：v157 resync 歷史（「27824→27639」等）
    "tests/test_travel114_static.py": [(1, 133)],  # 頭註全部係歷次 resync 歷史
}

for rel, mapping in MAPS.items():
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    hits = {}
    skips = SKIP.get(rel, [])

    def repl(m):
        old = int(m.group(1))
        if old in mapping:
            hits[old] = hits.get(old, 0) + 1
            return str(mapping[old])
        return m.group(1)

    def skipped(ln):
        return any(a <= ln <= b for a, b in skips)

    out = []
    for i, ln_text in enumerate(text.split("\n"), 1):
        out.append(ln_text if skipped(i) else NUM.sub(repl, ln_text))
    new = "\n".join(out)
    missing = [k for k in mapping if k not in hits]
    assert not missing, f"{rel}: 搵唔到 {missing}（可能已 resync 過／行號唔啱）"
    p.write_text(new, encoding="utf-8")
    print(f"{rel}: 改咗 {sum(hits.values())} 處，{sorted(hits)}")
print("RESYNC DONE")
