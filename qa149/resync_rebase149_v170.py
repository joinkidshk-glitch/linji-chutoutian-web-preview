#!/usr/bin/env python3
"""Resolve v149 rebase-onto-v170 conflicts in travel114 / tang171.
Rule (verified): v170's index.html change is net +2 (fallback comment+geometry,
insertion at main line 46098 == v149-numbering 46116; FLOOR 194->193 net 0).
So every v149 pin >= 46116 shifts +2; pins < 46116 stay. DEF 53788->53790
(verified by grep in merged index.html), total 59173+98=59271 (wc -l)."""
import re, sys

THRESH = 46116

def shift_nums_in_line(line):
    # shift standalone integers >= THRESH by +2 (only in data lines, not comments)
    def rep(m):
        n = int(m.group(0))
        return str(n + 2) if n >= THRESH else str(n)
    return re.sub(r'\d+', rep, line)

def resolve(path, regions):
    lines = open(path, encoding='utf-8').read().split('\n')
    out = []
    i = 0
    ri = 0
    while i < len(lines):
        if lines[i].startswith('<<<<<<< HEAD'):
            # collect head part and theirs part
            j = i + 1
            head = []
            while not lines[j].startswith('======='):
                head.append(lines[j]); j += 1
            j += 1
            theirs = []
            while not lines[j].startswith('>>>>>>>'):
                theirs.append(lines[j]); j += 1
            j += 1  # skip >>>>>>> line
            out.extend(regions[ri](head, theirs))
            ri += 1
            i = j
        else:
            out.append(lines[i]); i += 1
    assert ri == len(regions), f"{path}: resolved {ri} of {len(regions)} regions"
    open(path, 'w', encoding='utf-8').write('\n'.join(out))
    print(f"{path}: resolved {ri} regions")

# ---- travel114 ----
def t114_count(head, theirs):
    # head: [v170 comment x2, '# 計清單', 'COUNT_LINES = {', 13 number lines]
    # theirs: [v149 comment, '# 計清單', 'COUNT_LINES = {', 13 number lines]
    nums = [shift_nums_in_line(l) for l in theirs[3:]]
    return [
        head[0],
        head[1],
        "# v20a149 rebase 上 main e8c3a73（v170）resync：淨 ＋98 行（CSS ＋13／JS ＋85；v170 fallback +2 之上；difflib 核實 40 個釘行內容逐行相同，純漂移；reveal 行拆兩行原文令 ＋97→＋98）；COUNT 13／FREE 27 不變，DEF 53692→53790、WRAPPER 44172→44185。",
        "# 計清單（玩家主動導航，預設計數，唔加旗）：13 處",
        "COUNT_LINES = {",
    ] + nums

def t114_free(head, theirs):
    # theirs: 27 FREE number lines + '}' + FREE_FLAGS + DEF_LINE + WRAPPER_LINE
    data = [shift_nums_in_line(l) for l in theirs[:27]]
    return data + [
        "}",
        'FREE_FLAGS = ("travelFree:true", "encDone:true", "forceRestore:true", "wf4Done:true")',
        "DEF_LINE = 53790      # function openLoc(id, opts){",
        "WRAPPER_LINE = 44185  # window.__phase2.openLoc：轉發 opts",
    ]

resolve('/home/hatch/workspace/linji-work149/tests/test_travel114_static.py',
        [t114_count, t114_free])

# ---- tang171 ----
def tang_head(head, theirs):
    return [
        head[0],
        "# v20a149 rebase 上 main e8c3a73（v170）resync：淨 ＋98 行（CSS ＋13／JS ＋85），總行數 59173→59271、DEF 53692→53790；其餘斷言唔郁。",
    ]

def tang_assert(head, theirs):
    return [
        "ok('零行數漂移：總行數 59271（v170 59173＋v149 ＋98）', src.count('\\n') == 59271)",
        "ok('零行數漂移：openLoc DEF 行 53790 不變（travel114 釘行）',",
        "   len(lines) >= 53790 and 'function openLoc(id, opts){' in lines[53789])",
    ]

resolve('/home/hatch/workspace/linji-work149/tests/test_tang171_static.py',
        [tang_head, tang_assert])
print("done")
