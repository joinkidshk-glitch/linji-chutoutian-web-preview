#!/usr/bin/env python3
# 驗證合併後測試檔嘅行號釘：每個釘用斷言本身嘅搜尋字串喺合併後 index.html 搵真行，
# 同檔案寫嘅行號對一次。唔啱就印出正確行號。唔寫檔。
import re

NEW = open('index.html', encoding='utf-8').read().split('\n')

FILES = ['tests/test_text125_static.py', 'tests/test_kwan151_static.py',
         'tests/test_tang152_static.py', 'tests/test_rom176_static.py',
         'tests/test_tang171_static.py', 'tests/test_tang173_static.py',
         'tests/test_travel114_static.py', 'tests/test_gift185_static.py']

def find_unique(needle):
    hits = [i + 1 for i, t in enumerate(NEW) if needle in t]
    return hits

wrong = 0
checked = 0
for f in FILES:
    lines = open(f, encoding='utf-8').read().split('\n')
    for li, txt in enumerate(lines, 1):
        if txt.lstrip().startswith('#'):
            continue
        # 'needle' in line(N)
        for m in re.finditer(r"'([^']{8,120})' in line\((\d+)\)", txt):
            needle, n = m.group(1), int(m.group(2))
            if needle.startswith('第 ') or '行' in needle[-6:]:
                continue
            checked += 1
            hits = find_unique(needle)
            if n not in hits:
                wrong += 1
                print('%-38s L%-4d line(%d) WRONG :: %s... -> hits %s' % (f, li, n, needle[:50], hits[:5]))
        # "..." in line(N)
        for m in re.finditer(r'"([^"]{8,120})" in line\((\d+)\)', txt):
            needle, n = m.group(1), int(m.group(2))
            checked += 1
            hits = find_unique(needle)
            if n not in hits:
                wrong += 1
                print('%-38s L%-4d line(%d) WRONG :: %s... -> hits %s' % (f, li, n, needle[:50], hits[:5]))
        # lines()[N].startswith('...') / lines[N].startswith / '...' in lines[N]
        for m in re.finditer(r"(?:lines\(\)|lines|ls)\[(\d+)\]", txt):
            idx = int(m.group(1))
            n = idx + 1
            # 搵同一行嘅搜尋字串
            sm = re.search(r"startswith\('([^']{8,120})'\)", txt) or re.search(r"'([^']{8,120})' in (?:lines\(\)|lines|ls)\[", txt) or re.search(r'"([^"]{8,120})" in (?:lines\(\)|lines|ls)\[', txt)
            if not sm:
                continue
            needle = sm.group(1)
            checked += 1
            hits = find_unique(needle)
            if n not in hits:
                wrong += 1
                print('%-38s L%-4d [%d] line %d WRONG :: %s... -> hits %s' % (f, li, idx, n, needle[:50], hits[:5]))
        # len(...) < N guards — 唔驗內容，只驗 N 行存在（guard 本身唔係斷言）
print()
print('checked: %d, wrong: %d' % (checked, wrong))
