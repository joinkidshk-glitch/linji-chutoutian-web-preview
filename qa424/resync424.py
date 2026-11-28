# -*- coding: utf-8 -*-
"""v424 resync: index.html 淨 +187 行（53534->53721）；行號釘按 difflib 映射重寫，
單次掃描 dict 查表，內容逐字核實純漂移（改動行按內容錨點重對）。"""
import difflib, re, subprocess, pathlib

ROOT = pathlib.Path('/home/hatch/workspace/linji-work424')
old = subprocess.check_output(['git', '-C', str(ROOT), 'show', 'HEAD:index.html']).decode('utf-8').split('\n')
new = (ROOT / 'index.html').read_text(encoding='utf-8').split('\n')
print('old lines', len(old), 'new lines', len(new))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
old2new = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            old2new[i1 + k + 1] = j1 + k + 1  # 1-based

def m(n):
    if n in old2new:
        return old2new[n]
    # 改動行：按舊行內容喺新檔搵唯一行
    frag = old[n - 1].strip()
    hits = [i + 1 for i, l in enumerate(new) if l.strip() == frag]
    if len(hits) == 1:
        return hits[0]
    raise SystemExit(f'pin {n} not in equal mapping and content hits={hits}: {frag[:80]}')

def m0(n):  # 0-based index pin
    return m(n + 1) - 1

def patch(path, pairs, note):
    p = ROOT / path
    s = p.read_text(encoding='utf-8')
    for a, b in pairs:
        if a not in s:
            raise SystemExit(f'{path}: anchor not found: {a[:80]}')
        s = s.replace(a, b, 1)
    s = note + s
    p.write_text(s, encoding='utf-8')
    print('patched', path)

NOTE = "# v424 resync：index.html 淨 +187 行（53534→53721）；行號釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa424/resync424.py。\n"

# rom159 line_has pins + 全佳 idx_lines
patch('tests/test_rom159_static.py', [
    ('line_has(30194,', f'line_has({m(30194)},'),
    ('line_has(10332,', f'line_has({m(10332)},'),
    ('line_has(31120,', f'line_has({m(31120)},'),
    ('line_has(12540,', f'line_has({m(12540)},'),
    ('line_has(17232,', f'line_has({m(17232)},'),
    ('line_has(30975,', f'line_has({m(30975)},'),
    ('idx_lines[30221]', f'idx_lines[{m0(30221)}]'),
], NOTE)

# rom176 line() pins（由現行檔掃描，單次 dict 查表）
p = ROOT / 'tests/test_rom176_static.py'
s = p.read_text(encoding='utf-8')
pins176 = sorted({int(x) for x in re.findall(r'line\((\d+)\)', s)})
print('rom176 pins', pins176)
s = re.sub(r'line\((\d+)\)', lambda mo: f'line({m(int(mo.group(1)))})', s)
p.write_text(NOTE + s, encoding='utf-8')
print('patched tests/test_rom176_static.py')

# tang152 lines()[idx] pins (0-based)
p = ROOT / 'tests/test_tang152_static.py'
s = p.read_text(encoding='utf-8')
pins152 = sorted({int(x) for x in re.findall(r'lines\(\)\[(\d+)\]', s)})
print('tang152 pins', pins152)
s = re.sub(r'lines\(\)\[(\d+)\]', lambda mo: f'lines()[{m0(int(mo.group(1)))}]', s)
p.write_text(NOTE + s, encoding='utf-8')
print('patched tests/test_tang152_static.py')

# text125 ls[idx] pins (0-based) + len guards
p = ROOT / 'tests/test_text125_static.py'
s = p.read_text(encoding='utf-8')
pins125 = sorted({int(x) for x in re.findall(r'ls\[(\d+)\]', s)})
print('text125 pins', pins125)
s = re.sub(r'ls\[(\d+)\]', lambda mo: f'ls[{m0(int(mo.group(1)))}]', s)
p.write_text(NOTE + s, encoding='utf-8')
print('patched tests/test_text125_static.py')

# travel114 COUNT/FREE 集合行釘＋DEF/WRAPPER（單次掃描 dict 查表）
p = ROOT / 'tests/test_travel114_static.py'
s = p.read_text(encoding='utf-8')
s = re.sub(r'^(\s+)(\d{4,5}),(.*)$', lambda mo: f"{mo.group(1)}{m(int(mo.group(2)))},{mo.group(3)}", s, flags=re.M)
s = s.replace('DEF_LINE = 48260', f'DEF_LINE = {m(48260)}', 1)
s = s.replace('WRAPPER_LINE = 34151', f'WRAPPER_LINE = {m(34151)}', 1)
p.write_text(NOTE + s, encoding='utf-8')
print('patched tests/test_travel114_static.py')

# totals + openLoc DEF + L5356 (tang171/tang173/gift185)
openloc_new = m0(48259)
fade_new = None
for i, l in enumerate(new):
    if 'loc-acts-more171::after' in l and 'act-locked171' in l:
        fade_new = i
        break
print('openLoc DEF idx', openloc_new, 'fade idx', fade_new)
for path in ['tests/test_gift185_static.py', 'tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    p = ROOT / path
    s = p.read_text(encoding='utf-8')
    s = s.replace('總行數 53534', '總行數 53721')
    s = s.replace("== 53534", "== 53721")
    s = s.replace('＋v423 +114）', '＋v423 +114＋v424 +187）')
    s = s.replace('＋v423 +72，travel114 釘行）', '＋v423 +72＋v424 +187，travel114 釘行）')
    s = s.replace('lines[48259]', f'lines[{openloc_new}]')
    s = s.replace('lines[5355]', f'lines[{fade_new}]')
    p.write_text(NOTE + s, encoding='utf-8')
    print('patched', path)
