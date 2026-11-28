# v425 resync：index.html 淨 +38 行（53721→53759）；行號釘按 difflib 映射重寫，逐錨核實內容相同（純漂移）。
import difflib, re, subprocess, sys

old = subprocess.run(['git', 'show', 'HEAD:index.html'], capture_output=True, text=True).stdout.splitlines()
new = open('index.html', encoding='utf-8').read().splitlines()
sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
mp = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mp[i1 + k + 1] = j1 + k + 1
    elif tag == 'replace' and (i2 - i1) == (j2 - j1):
        for k in range(i2 - i1):
            mp[i1 + k + 1] = j1 + k + 1

def m(n):
    r = mp.get(n)
    assert r is not None, f'no map for {n}'
    assert old[n - 1] == new[r - 1], f'content mismatch {n}->{r}: {old[n-1][:60]!r} vs {new[r-1][:60]!r}'
    return r

def patch(path, pairs, note):
    s = open(path, encoding='utf-8').read()
    for a, b in pairs:
        assert a in s, f'{path}: anchor missing {a[:60]}'
        s = s.replace(a, b, 1)
    s = note + s
    open(path, 'w', encoding='utf-8').write(s)
    print('patched', path, pairs)

NOTE = '# v425 resync：index.html 淨 +38 行（53721→53759）；行號釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa424/resync425.py。\n'

patch('tests/test_rom159_static.py',
      [(f'line_has({n},', f'line_has({m(n)},') for n in (30380, 10393, 31306, 12655, 17351, 31161) if m(n) != n], NOTE)
patch('tests/test_rom176_static.py',
      [(f'line({n})', f'line({m(n)})') for n in (8538, 17349, 46242, 46601, 48299, 48489) if m(n) != n], NOTE)
patch('tests/test_tang152_static.py',
      [(f'lines()[{n}]', f'lines()[{m(n + 1) - 1}]') for n in (17278, 17403)], NOTE)
patch('tests/test_text125_static.py',
      [(f'ls[{n}]', f'ls[{m(n + 1) - 1}]') for n in (13242, 13384, 19168)], NOTE)

# travel114：COUNT/FREE 集合逐數映射（舊行含 openLoc( 先郁）＋DEF/WRAPPER
p = 'tests/test_travel114_static.py'
s = open(p, encoding='utf-8').read()
def map_block(s, start_marker):
    i = s.index(start_marker)
    j = s.index('}', i)
    blk = s[i:j]
    def rep(mm):
        n = int(mm.group(0))
        if 1 <= n <= len(old) and 'openLoc(' in old[n - 1]:
            return str(m(n))
        return mm.group(0)
    return s[:i] + re.sub(r'\b\d{4,5}\b', rep, blk) + s[j:]
s = map_block(s, 'COUNT_LINES = {')
s = map_block(s, 'FREE_LINES = {')
s = s.replace('DEF_LINE = 48446', f'DEF_LINE = {m(48446)}')
s = s.replace('WRAPPER_LINE = 34337', f'WRAPPER_LINE = {m(34337)}')
open(p, 'w', encoding='utf-8').write(NOTE + s)
print('patched travel114 DEF', m(48446), 'WRAPPER', m(34337))

for p in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py', 'tests/test_gift185_static.py'):
    s = open(p, encoding='utf-8').read()
    s = s.replace("== 53721", "== 53759").replace("總行數 53721", "總行數 53759").replace("＋v424 +187）", "＋v424 +187＋v425 +38）")
    s = s.replace('lines[48445]', f'lines[{m(48446) - 1}]')
    if 'tang173' in p:
        s = s.replace('lines[5389]', f'lines[{m(5390) - 1}]')
    open(p, 'w', encoding='utf-8').write(NOTE + s)
    print('patched', p)
print('DONE')
