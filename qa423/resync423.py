# -*- coding: utf-8 -*-
"""v423 resync: index.html 淨 +113 行（53420->53533）；行號釘按 difflib 映射重寫，內容逐字核實純漂移。"""
import difflib, re, subprocess, pathlib
ROOT = pathlib.Path('/home/hatch/workspace/linji-work423')
old = subprocess.check_output(['git','-C',str(ROOT),'show','HEAD:index.html']).decode('utf-8').split('\n')
new = (ROOT/'index.html').read_text(encoding='utf-8').split('\n')
print('old lines', len(old), 'new lines', len(new))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
old2new = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2-i1):
            old2new[i1+k+1] = j1+k+1  # 1-based
def m(n):
    if n not in old2new:
        raise SystemExit(f'pin {n} not in equal mapping')
    return old2new[n]
def m0(n):  # 0-based index pin
    return m(n+1)-1

def patch(path, pairs, note):
    p = ROOT/path
    s = p.read_text(encoding='utf-8')
    orig = s
    for a, b in pairs:
        if a not in s:
            raise SystemExit(f'{path}: anchor not found: {a[:80]}')
        s = s.replace(a, b, 1)
    s = note + s
    p.write_text(s, encoding='utf-8')
    print('patched', path)

NOTE = "# v423 resync：index.html 淨 +113 行（53420→53533）；行號釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa423/resync423.py。\n"

# rom159 line_has pins + 全佳 idx_lines
patch('tests/test_rom159_static.py', [
    ('line_has(30132,', f'line_has({m(30132)},'),
    ('line_has(10311,', f'line_has({m(10311)},'),
    ('line_has(31054,', f'line_has({m(31054)},'),
    ('line_has(12519,', f'line_has({m(12519)},'),
    ('line_has(17195,', f'line_has({m(17195)},'),
    ('line_has(30909,', f'line_has({m(30909)},'),
    ('idx_lines[30159]', f'idx_lines[{m0(30159)}]'),
], NOTE)

# rom176 line() pins
patch('tests/test_rom176_static.py', [
    ('line(8456)', f'line({m(8456)})'),
    ('line(17193)', f'line({m(17193)})'),
    ('line(45971)', f'line({m(45971)})'),
    ('line(46330)', f'line({m(46330)})'),
    ('line(48026)', f'line({m(48026)})'),
    ('line(48216)', f'line({m(48216)})'),
], NOTE)

# tang152 lines()[idx] pins (0-based)
patch('tests/test_tang152_static.py', [
    ('lines()[17122]', f'lines()[{m0(17122)}]'),
    ('lines()[17247]', f'lines()[{m0(17247)}]'),
], NOTE)

# text125 ls[idx] pins (0-based)
patch('tests/test_text125_static.py', [
    ('ls[13099]', f'ls[{m0(13099)}]'),
    ('ls[13241]', f'ls[{m0(13241)}]'),
    ('ls[19012]', f'ls[{m0(19012)}]'),
], NOTE)

# totals + openLoc DEF + L4872 (tang171/tang173/gift185)
openloc_new = m(45652)
fade_new = None
for i, l in enumerate(new, 1):
    if 'loc-acts-more171::after' in l and 'act-locked171' in l:
        fade_new = i; break
print('openLoc DEF', openloc_new, 'fade line', fade_new)
for path in ['tests/test_gift185_static.py', 'tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    p = ROOT/path
    s = p.read_text(encoding='utf-8')
    s = s.replace('總行數 53420', '總行數 53533')
    s = s.replace('v422C +29）', 'v422C +29＋v423 +113）')
    s = s.replace('openLoc DEF 行 45652', f'openLoc DEF 行 {openloc_new}')
    s = s.replace('v422C +29，travel114 釘行）', f'v422C +29＋v423 +{openloc_new-45652}，travel114 釘行）')
    p.write_text(NOTE + s, encoding='utf-8')
    print('patched total', path)
# tang173 L4872 pins (lines[5346] style + label)
p = ROOT/'tests/test_tang173_static.py'
s = p.read_text(encoding='utf-8')
s = s.replace('lines[5346]', f'lines[{fade_new-1}]')
s = s.replace('L4872', f'L{fade_new}')
p.write_text(s, encoding='utf-8')
print('patched tang173 fade pin ->', fade_new)

# travel114 FREE/COUNT/DEF/WRAPPER lists: map every pin number in assignment blocks
p = ROOT/'tests/test_travel114_static.py'
s = p.read_text(encoding='utf-8')
def map_block(mo):
    head, body = mo.group(1), mo.group(2)
    def rep(mm):
        n = int(mm.group(0))
        return str(m(n)) if n in old2new else mm.group(0)
    return head + re.sub(r'\b\d{4,5}\b', rep, body)
s2 = re.sub(r'((?:FREE|COUNT|DEF|WRAPPER)\w*\s*=\s*[\[{])(.*?)([\]}])', lambda mo: mo.group(1) + re.sub(r'\b\d{4,5}\b', lambda mm: str(m(int(mm.group(0)))) if int(mm.group(0)) in old2new else mm.group(0), mo.group(2)) + mo.group(3), s, flags=re.S)
if s2 == s:
    print('WARN travel114 no block matched; inspect manually')
else:
    p.write_text(NOTE + s2, encoding='utf-8')
    print('patched travel114')
print('RESYNC423 DONE')
