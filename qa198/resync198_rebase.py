#!/usr/bin/env python3
# v20a198 rebase resync（報告模式）：difflib 對位 v198 tip index.html (60483) → 合併後 index.html (60602)，
# 掃描分支改動過嘅測試檔，列出每個行號釘舊→新＋內容逐字對照。唔寫檔。
import difflib, re, subprocess, sys

OLD = subprocess.check_output(['git', 'show', 'v20a198:index.html'], text=True).split('\n')
NEW = open('index.html', encoding='utf-8').read().split('\n')
print('old lines: %d, new lines: %d, net: %+d' % (len(OLD) - 1, len(NEW) - 1, (len(NEW) - 1) - (len(OLD) - 1)))

sm = difflib.SequenceMatcher(None, OLD, NEW, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
print('equal-mapped lines: %d' % len(mapping))
print('change hunks (old 1-based -> new 1-based):')
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        print('  %s old L%d-%d -> new L%d-%d' % (tag, i1 + 1, i2, j1 + 1, j2))

FILES = ['tests/test_story198_logic.js', 'tests/test_story198_static.py',
         'tests/test_progress71_logic.js', 'tests/test_progress71_static.py',
         'tests/test_story191_logic.js', 'tests/test_story191_static.py',
         'tests/test_ui135_mapcard_static.py', 'tests/test_verify37_static.py',
         'tests/test_story165_static.py', 'tests/test_text108_static.py',
         'tests/test_text125_static.py', 'tests/test_kwan151_static.py',
         'tests/test_tang152_static.py', 'tests/test_rom176_static.py',
         'tests/test_tang171_static.py', 'tests/test_tang173_static.py',
         'tests/test_travel114_static.py', 'tests/test_gift185_static.py']

def in_string(line, pos):
    # 粗略判斷：match 之前單引號／雙引號數目係咪奇數（喺字串入面）
    before = line[:pos]
    return (before.count("'") % 2 == 1) or (before.count('"') % 2 == 1)

bad = 0
total = 0
for f in FILES:
    try:
        lines = open(f, encoding='utf-8').read().split('\n')
    except FileNotFoundError:
        print('SKIP (no file):', f)
        continue
    for li, txt in enumerate(lines, 1):
        if txt.lstrip().startswith('#'):
            continue
        # 1-based line(N)
        for m in re.finditer(r'line\((\d+)\)', txt):
            if in_string(txt, m.start()):
                continue
            old = int(m.group(1))
            new = mapping.get(old)
            total += 1
            if new is None:
                print('%-38s L%-4d line(%d) -> ??? CHANGED REGION: %s' % (f, li, old, OLD[old - 1][:70] if 1 <= old <= len(OLD) else '?'))
                bad += 1
                continue
            same = OLD[old - 1] == NEW[new - 1]
            flag = 'SAME' if same else 'DIFF!'
            if not same or old != new:
                print('%-38s L%-4d line(%d) -> line(%d) %s :: %s' % (f, li, old, new, flag, OLD[old - 1].strip()[:70]))
            if not same:
                bad += 1
                print('      NEW: %s' % NEW[new - 1].strip()[:100])
        # 0-based lines()[N] / lines[N] / ls[N]
        for m in re.finditer(r'(?:lines\(\)|lines|ls)\[(\d+)\]', txt):
            if in_string(txt, m.start()):
                continue
            idx = int(m.group(1))
            old = idx + 1
            new = mapping.get(old)
            total += 1
            if new is None:
                print('%-38s L%-4d [%d] -> ??? CHANGED REGION' % (f, li, idx))
                bad += 1
                continue
            same = OLD[old - 1] == NEW[new - 1]
            if not same or old != new:
                print('%-38s L%-4d [%d] (line %d) -> [%d] (line %d) %s :: %s' % (f, li, idx, old, new - 1, new, 'SAME' if same else 'DIFF!', OLD[old - 1].strip()[:70]))
            if not same:
                bad += 1
        # len(ls) < N / len(lines) < N
        for m in re.finditer(r'len\((?:ls|lines)\) < (\d+)', txt):
            old = int(m.group(1))
            new = mapping.get(old)
            total += 1
            if new is None:
                print('%-38s L%-4d len< %d -> ??? CHANGED REGION' % (f, li, old))
                bad += 1
                continue
            same = OLD[old - 1] == NEW[new - 1]
            if not same or old != new:
                print('%-38s L%-4d len< %d -> len< %d %s :: %s' % (f, li, old, new, 'SAME' if same else 'DIFF!', OLD[old - 1].strip()[:70]))
            if not same:
                bad += 1
        # total lines
        for m in re.finditer(r"count\(['\"]\\n['\"]\) == (\d+)", txt):
            old = int(m.group(1))
            print('%-38s L%-4d TOTAL %d -> %d' % (f, li, old, len(NEW) - 1))
            total += 1
        # DEF_LINE / WRAPPER_LINE
        for m in re.finditer(r'(?:DEF_LINE|WRAPPER_LINE) = (\d+)', txt):
            old = int(m.group(1))
            new = mapping.get(old)
            total += 1
            if new is None:
                print('%-38s L%-4d %s %d -> ??? CHANGED REGION' % (f, li, m.group(0).split('=')[0].strip(), old))
                bad += 1
                continue
            same = OLD[old - 1] == NEW[new - 1]
            if not same or old != new:
                print('%-38s L%-4d %s %d -> %d %s :: %s' % (f, li, m.group(0).split('=')[0].strip(), old, new, 'SAME' if same else 'DIFF!', OLD[old - 1].strip()[:70]))
            if not same:
                bad += 1

# travel114 COUNT_LINES / FREE_LINES set members (1-based)
f = 'tests/test_travel114_static.py'
lines = open(f, encoding='utf-8').read().split('\n')
for setname in ('COUNT_LINES', 'FREE_LINES'):
    start = next(i for i, t in enumerate(lines) if t.startswith(setname + ' = {'))
    end = next(i for i in range(start, len(lines)) if lines[i].strip() == '}')
    for i in range(start + 1, end):
        m = re.match(r'\s*(\d+),', lines[i])
        if not m:
            continue
        old = int(m.group(1))
        new = mapping.get(old)
        total += 1
        if new is None:
            print('%-38s L%-4d %s %d -> ??? CHANGED REGION' % (f, i + 1, setname, old))
            bad += 1
            continue
        same = OLD[old - 1] == NEW[new - 1]
        if not same or old != new:
            print('%-38s L%-4d %s %d -> %d %s :: %s' % (f, i + 1, setname, old, new, 'SAME' if same else 'DIFF!', OLD[old - 1].strip()[:70]))
        if not same:
            bad += 1

print()
print('pins scanned: %d, content DIFF / unmapped: %d' % (total, bad))
sys.exit(1 if bad else 0)
