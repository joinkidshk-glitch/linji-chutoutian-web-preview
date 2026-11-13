#!/usr/bin/env python3
# v20a198 rebase resync（寫入模式）：同 /tmp/resync198_rebase.py 同一個 mapping，
# 將 8 檔衝突測試嘅行號釘改為合併後 index.html 嘅新行號。只改 code 數字，唔改 prose 標籤。
import difflib, re, subprocess, sys

OLD = subprocess.check_output(['git', 'show', 'v20a198:index.html'], text=True).split('\n')
NEW = open('index.html', encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(None, OLD, NEW, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k

FILES = ['tests/test_text125_static.py', 'tests/test_kwan151_static.py',
         'tests/test_tang152_static.py', 'tests/test_rom176_static.py',
         'tests/test_tang171_static.py', 'tests/test_tang173_static.py',
         'tests/test_travel114_static.py', 'tests/test_gift185_static.py']

def in_string(line, pos):
    before = line[:pos]
    return (before.count("'") % 2 == 1) or (before.count('"') % 2 == 1)

changed = 0
for f in FILES:
    lines = open(f, encoding='utf-8').read().split('\n')
    out = []
    for txt in lines:
        if txt.lstrip().startswith('#'):
            out.append(txt)
            continue
        # line(N) — 1-based；跳過字串入面嘅
        def sub_line(m):
            global changed
            old = int(m.group(1))
            new = mapping.get(old)
            assert new is not None and OLD[old - 1] == NEW[new - 1], (f, old)
            if new != old:
                changed += 1
            return 'line(%d)' % new
        txt = re.sub(r'line\((\d+)\)', lambda m: m.group(0) if in_string(txt, m.start()) else sub_line(m), txt)
        # 0-based [N]
        def sub_idx(m):
            global changed
            idx = int(m.group(1))
            old = idx + 1
            new = mapping.get(old)
            assert new is not None and OLD[old - 1] == NEW[new - 1], (f, old)
            if new - 1 != idx:
                changed += 1
            return m.group(0).replace(str(idx), str(new - 1))
        txt = re.sub(r'(?:lines\(\)|lines|ls)\[(\d+)\]', lambda m: m.group(0) if in_string(txt, m.start()) else sub_idx(m), txt)
        # len(...) < N
        def sub_len(m):
            global changed
            old = int(m.group(1))
            new = mapping.get(old)
            assert new is not None and OLD[old - 1] == NEW[new - 1], (f, old)
            if new != old:
                changed += 1
            return m.group(0).replace(str(old), str(new))
        txt = re.sub(r'len\((?:ls|lines)\) < (\d+)', sub_len, txt)
        # total lines
        def sub_total(m):
            global changed
            changed += 1
            return m.group(0).replace(m.group(1), str(len(NEW) - 1))
        txt = re.sub(r"count\(['\"]\\n['\"]\) == (\d+)", sub_total, txt)
        # DEF_LINE / WRAPPER_LINE
        def sub_def(m):
            global changed
            old = int(m.group(1))
            new = mapping.get(old)
            assert new is not None and OLD[old - 1] == NEW[new - 1], (f, old)
            if new != old:
                changed += 1
            return m.group(0).replace(str(old), str(new))
        txt = re.sub(r'(?:DEF_LINE|WRAPPER_LINE) = (\d+)', sub_def, txt)
        out.append(txt)
    # travel114 set members
    if f == 'tests/test_travel114_static.py':
        for setname in ('COUNT_LINES', 'FREE_LINES'):
            start = next(i for i, t in enumerate(out) if t.startswith(setname + ' = {'))
            end = next(i for i in range(start, len(out)) if out[i].strip() == '}')
            for i in range(start + 1, end):
                m = re.match(r'(\s*)(\d+),(.*)$', out[i])
                if not m:
                    continue
                old = int(m.group(2))
                new = mapping.get(old)
                assert new is not None and OLD[old - 1] == NEW[new - 1], (f, old)
                if new != old:
                    changed += 1
                out[i] = '%s%d,%s' % (m.group(1), new, m.group(3))
    open(f, 'w', encoding='utf-8').write('\n'.join(out))
    print(f, 'done')

print('total numeric pins rewritten:', changed)
