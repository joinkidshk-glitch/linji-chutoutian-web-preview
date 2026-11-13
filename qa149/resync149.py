#!/usr/bin/env python3
# qa149/resync149.py — v20a149 行號 resync（text125／travel114 寫死行號）。
# 做法：pristine（qa149/pristine_index.html，da90957）vs 工作版 index.html difflib 對位；
# 每個釘行由 equal-block 映射去新行號，逐行驗內容逐字相同（純漂移先改行號）。
# 用法：python3 qa149/resync149.py（在工作副本根目錄執行）
import difflib

old = open("qa149/pristine_index.html", encoding="utf-8").read().split("\n")
new = open("index.html", encoding="utf-8").read().split("\n")
print("old lines: %d  new lines: %d  net: %+d" % (len(old), len(new), len(new) - len(old)))

sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based
    else:
        print("  DIFF %s old %d-%d -> new %d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))

pinned = {
    "text125 currentLine": [27800],
    "text125 advance": [27913],
    "text125 familySafe": [33516, 33517, 33518],
    "travel114 COUNT": [32132, 35613, 37740, 38734, 39168, 39171, 39202, 43748, 57592, 57759, 57902, 57923, 58373],
    "travel114 FREE": [24772, 28267, 30853, 30854, 30866, 30867, 30878, 30879, 30982, 40707, 43405, 43428, 52437, 52556, 53449, 53831, 53853, 53988, 55625, 57036, 57369, 57487, 57488, 57523, 57524, 57543, 57558],
    "travel114 DEF": [53562],
    "travel114 WRAPPER": [44171],
}
bad = 0
for group, lines in pinned.items():
    for ln in lines:
        nl = mapping.get(ln)
        same = (nl is not None and old[ln - 1] == new[nl - 1])
        if not same:
            bad += 1
        print("%-20s %5d -> %-5s %s | %s" % (group, ln, nl, "SAME" if same else "MISMATCH",
              (old[ln - 1][:60] if ln <= len(old) else "")))
print("MISMATCH: %d" % bad)
