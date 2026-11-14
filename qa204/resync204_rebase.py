#!/usr/bin/env python3
"""v204 rebase resync: map anchor line numbers from pre-rebase v204
(a3355d2:index.html) to the merged working-tree index.html (v203+v204)
via difflib, and verify each mapped line is byte-identical (pure drift)."""
import difflib, subprocess, sys

old = subprocess.check_output(['git', 'show', 'a3355d2:index.html'], text=True).split('\n')
new = open('index.html', encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
# build old->new mapping for equal blocks
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based

def check(old_no, label):
    if old_no not in mapping:
        print(f'MISS {label}: old L{old_no} not in an equal block')
        return None
    new_no = mapping[old_no]
    same = old[old_no - 1] == new[new_no - 1]
    print(f'{label}: old L{old_no} -> new L{new_no}  identical={same}  | {old[old_no-1][:70]}')
    return new_no

# anchors from the v204 side of each conflict (ffa1cef numbers)
results = {}
results['total_newlines'] = None
results['openLoc_DEF'] = check(55671, 'openLoc DEF')
results['rom176_block'] = check(54101, 'ROM176 block')
results['rom176ApplyGiftOverrides'] = check(54469, 'rom176ApplyGiftOverrides')
results['addLocTalkGiftActs'] = check(55608, 'addLocTalkGiftActs')
results['rom176_intercept'] = check(55702, 'openLoc rom176 intercept')

# travel114 COUNT lines (v204 side)
for n in [35796, 37947, 39101, 39533, 39536, 39567, 44334, 59752, 59930, 60076, 60097]:
    check(n, f'COUNT L{n}')
# travel114 FREE lines (v204 side)
for n in [41277, 43991, 44014, 53924, 54043, 54093, 54316, 54355, 54361, 54428, 54430, 54433, 54460, 55571, 55945, 55967, 56118, 57755, 59520, 59638, 59639, 59674, 59675, 59700, 60547]:
    check(n, f'FREE L{n}')
results['travel_DEF'] = check(55671, 'travel DEF (same as openLoc)')
results['travel_WRAPPER'] = check(44903, 'travel WRAPPER')
print('new total newlines:', open('index.html', encoding='utf-8').read().count('\n'))
