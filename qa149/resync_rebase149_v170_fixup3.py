#!/usr/bin/env python3
"""Resolve v149 commit-2 (17637f4) rebase conflicts on top of v170.
The fuse (2 reveal lines -> 1) is at merged index.html line 46602 (verified);
total 59271->59270, DEF 53790->53789 (verified by wc/grep).
Rule: HEAD-side pins > 46602 shift -1; pins <= 46602 stay."""
import re

FUSE_LINE = 46602

def shift_down(line):
    def rep(m):
        n = int(m.group(0))
        return str(n - 1) if n > FUSE_LINE else str(n)
    return re.sub(r'\d+', rep, line)

def resolve(path, regions):
    lines = open(path, encoding='utf-8').read().split('\n')
    out = []
    i = 0
    ri = 0
    while i < len(lines):
        if lines[i].startswith('<<<<<<< HEAD'):
            j = i + 1
            head = []
            while not lines[j].startswith('======='):
                head.append(lines[j]); j += 1
            j += 1
            theirs = []
            while not lines[j].startswith('>>>>>>>'):
                theirs.append(lines[j]); j += 1
            j += 1
            out.extend(regions[ri](head, theirs))
            ri += 1
            i = j
        else:
            out.append(lines[i]); i += 1
    assert ri == len(regions), f"{path}: resolved {ri} of {len(regions)} regions"
    open(path, 'w', encoding='utf-8').write('\n'.join(out))
    print(f"{path}: resolved {ri} regions")

# ---- travel114: 3 regions (comment, COUNT tail, FREE tail+DEF) ----
def t114_comment(head, theirs):
    return head + [
        "# v20a149 fixup3（rebase 上 e8c3a73）：reveal 行融返一行（−1，插入點 L46602），淨 ＋98→＋97；COUNT 13／FREE 27 不變，DEF 53790→53789、WRAPPER 44185 唔郁。",
    ]

def t114_count_tail(head, theirs):
    return [shift_down(l) for l in head]

def t114_free_tail(head, theirs):
    return [shift_down(l) for l in head]

resolve('/home/hatch/workspace/linji-work149/tests/test_travel114_static.py',
        [t114_comment, t114_count_tail, t114_free_tail])

# ---- tang171: 2 regions (comment, assertions) ----
def tang_head(head, theirs):
    return head + [
        "# v20a149 fixup3（rebase 上 e8c3a73）：reveal 行融返一行（−1），總行數 59271→59270、DEF 53790→53789。",
    ]

def tang_assert(head, theirs):
    return [
        "ok('零行數漂移：總行數 59270（v170 59173＋v149 ＋97）', src.count('\\n') == 59270)",
        "ok('零行數漂移：openLoc DEF 行 53789 不變（travel114 釘行）',",
        "   len(lines) >= 53789 and 'function openLoc(id, opts){' in lines[53788])",
    ]

resolve('/home/hatch/workspace/linji-work149/tests/test_tang171_static.py',
        [tang_head, tang_assert])
print("done")
