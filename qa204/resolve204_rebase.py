#!/usr/bin/env python3
"""Resolve the 5 rebase conflict files: take the v204 (theirs) side of each
hunk and apply the difflib-verified new line numbers (see /tmp/resync204.py)."""
import re

def resolve(path, subs):
    txt = open(path, encoding='utf-8').read()
    # split into segments; for each conflict block keep theirs side, apply subs
    out = []
    i = 0
    while True:
        m = re.search(r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> [^\n]*\n', txt[i:], re.S)
        if not m:
            out.append(txt[i:])
            break
        out.append(txt[i:i + m.start()])
        theirs = m.group(2)
        for old, new in subs:
            theirs = theirs.replace(old, new)
        out.append(theirs + '\n')
        i += m.end()
    open(path, 'w', encoding='utf-8').write(''.join(out))
    print('resolved', path)

# gift185: total 61199 -> 61432
resolve('tests/test_gift185_static.py', [
    ('61199（v193 61167＋v204 淨 +32）', '61432（v193 61167＋v203 +233＋v204 +32）'),
    ("== 61199", "== 61432"),
])

# rom176 pegs
resolve('tests/test_rom176_static.py', [
    ('L54101', 'L54334'), ('line(54101)', 'line(54334)'),
    ('L54469', 'L54702'), ('line(54469)', 'line(54702)'),
    ('L55608', 'L55841'), ('line(55608)', 'line(55841)'),
    ('L55702', 'L55935'), ('line(55702)', 'line(55935)'),
])

# tang171 / tang173: total + openLoc DEF
for f in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    resolve(f, [
        ('61199（v193 61167＋v204 淨 +32）', '61432（v193 61167＋v203 +233＋v204 +32）'),
        ("== 61199", "== 61432"),
        ('55872（v193 55639＋v203 +233，travel114 釘行）', '55904（v193 55639＋v203 +233＋v204 +32，travel114 釘行）'),
        ('55671（v193 55639＋v204 淨 +32，travel114 釘行）', '55904（v193 55639＋v203 +233＋v204 +32，travel114 釘行）'),
        ('lines[55670]', 'lines[55903]'),
        ('>= 55671', '>= 55904'),
        ('>= 55872', '>= 55904'),
        ('lines[55871]', 'lines[55903]'),
    ])

# travel114: apply the difflib mapping in one simultaneous pass
mapping = {
    35796: 35796, 37947: 37947, 39101: 39117, 39533: 39549, 39536: 39552,
    39567: 39583, 44334: 44567, 59752: 59985, 59930: 60163, 60076: 60309,
    60097: 60330, 41277: 41510, 43991: 44224, 44014: 44247, 53924: 54157,
    54043: 54276, 54093: 54326, 54316: 54549, 54355: 54588, 54361: 54594,
    54428: 54661, 54430: 54663, 54433: 54666, 54460: 54693, 55571: 55804,
    55945: 56178, 55967: 56200, 56118: 56351, 57755: 57988, 59520: 59753,
    59638: 59871, 59639: 59872, 59674: 59907, 59675: 59908, 59700: 59933,
    60547: 60780, 55671: 55904, 44903: 45136,
}
txt = open('tests/test_travel114_static.py', encoding='utf-8').read()
out = []
i = 0
while True:
    m = re.search(r'<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> [^\n]*\n', txt[i:], re.S)
    if not m:
        out.append(txt[i:])
        break
    out.append(txt[i:i + m.start()])
    theirs = m.group(2)
    theirs = re.sub(r'\b(\d{5})\b', lambda mm: str(mapping.get(int(mm.group(1)), int(mm.group(1)))), theirs)
    out.append(theirs + '\n')
    i += m.end()
open('tests/test_travel114_static.py', 'w', encoding='utf-8').write(''.join(out))
print('resolved tests/test_travel114_static.py')
