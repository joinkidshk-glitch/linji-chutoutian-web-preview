# v266 resync: index.html net +328 (V158 block +284 @~7523 / StoryPlay hook +1 @10883 /
# load call +1 @15255 / enc158 hook +42 @27960). All pinned lines in 9 test files
# remapped via difflib (main 60f0d12 -> work266); every anchor verified verbatim
# (pure drift, zero content change). Ledger tests get "+v266 +328" appended.
import difflib, re, sys

MAIN = '/home/hatch/workspace/linji-repo/index.html'
WORK = '/home/hatch/workspace/linji-work266/index.html'
W266 = '/home/hatch/workspace/linji-work266/tests/'

main_lines = open(MAIN, encoding='utf-8').read().split('\n')
work_lines = open(WORK, encoding='utf-8').read().split('\n')
print('main lines:', len(main_lines), 'work lines:', len(work_lines),
      'delta:', len(work_lines) - len(main_lines))
assert len(work_lines) - len(main_lines) == 328

sm = difflib.SequenceMatcher(None, main_lines, work_lines, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based
    elif tag != 'insert':
        print('NON-EQUAL opcode (not pure insertion):', tag, i1, i2, j1, j2)
        sys.exit(1)
print('opcodes all equal/insert; mapped lines:', len(mapping))

def check_pin(old1):
    """1-based main line -> mapped work line; assert content identical."""
    new1 = mapping.get(old1)
    assert new1 is not None, f'line {old1} not mapped (in insert region?)'
    assert main_lines[old1 - 1] == work_lines[new1 - 1], \
        f'content mismatch main:{old1} vs work:{new1}\nMAIN: {main_lines[old1-1]!r}\nWORK: {work_lines[new1-1]!r}'
    return new1

def replace_code(path, old, new, label, expect):
    """Replace every occurrence of a code anchor (same pin may appear twice
    on one ok() line, e.g. line(9299) twice in A1); assert exact count."""
    txt = open(path, encoding='utf-8').read()
    n = txt.count(old)
    assert n == expect, f'{path} {label}: expected {expect} occurrence(s) of {old!r}, found {n}'
    open(path, 'w', encoding='utf-8').write(txt.replace(old, new))
    print(f'  {path.split("/")[-1]}: {label} (x{n})')

def replace_once(path, old, new, label):
    txt = open(path, encoding='utf-8').read()
    n = txt.count(old)
    assert n == 1, f'{path} {label}: expected 1 occurrence of {old!r}, found {n}'
    open(path, 'w', encoding='utf-8').write(txt.replace(old, new, 1))
    print(f'  {path.split("/")[-1]}: {label}')

def header(path, note):
    txt = open(path, encoding='utf-8').read()
    open(path, 'w', encoding='utf-8').write(note + '\n' + txt)

# ---- pin specs: (test file, 1-based main lines to remap, replacement style) ----
# style 'line(N)' / 'lines()[N-1]' / 'ls[N-1]' handled by caller-supplied lambdas
specs = {
    'test_text125_static.py': ([11469, 11611, 16871], 'ls'),
    'test_kwan151_static.py': ([9299, 9640, 9643, 9644, 9645, 9688, 9907, 10932, 10965, 14697, 14706, 14813, 14814, 14849], 'line'),
    'test_tang152_static.py': ([9459, 15136, 15262], 'bracket'),
    'test_rom159_static.py': ([25849, 8339, 26683, 10886, 15210, 26598, 25877], 'line_has'),
    'test_rom176_static.py': ([15208, 40147, 40522, 41682, 41838], 'line'),
    'test_travel114_static.py': ([8315, 14634, 14635, 14647, 14648, 14659, 14660, 14763, 25037, 26448, 26449, 26525, 28621, 28654, 39947, 40066, 40139, 40364, 40408, 40414, 40481, 40483, 40486, 40513, 41645, 41692, 42081, 42103, 42255, 42260, 43202, 44697, 44970, 44971, 45015, 45016, 45041, 45934,
                                 15792, 19204, 21400, 22606, 23046, 23049, 23080, 28983, 45093, 45305, 45463, 45484], 'setnum'),
}
for fname, (pins, style) in specs.items():
    path = W266 + fname
    print(f'== {fname} ==')
    for old1 in pins:
        new1 = check_pin(old1)
        if new1 == old1:
            print(f'  {old1} unchanged (before all insertions)')
            continue
        if style == 'line':
            txt0 = open(path, encoding='utf-8').read()
            n0 = txt0.count(f'line({old1})')
            assert n0 >= 1, f'{path} line({old1}): unexpected count {n0}'
            replace_code(path, f'line({old1})', f'line({new1})', f'{old1}->{new1}', n0)
        elif style == 'line_has':
            if old1 == 25877:
                replace_once(path, 'idx_lines[25877 - 1]', f'idx_lines[{new1} - 1]', f'full佳 {old1}->{new1}')
            else:
                replace_once(path, f'line_has({old1},', f'line_has({new1},', f'{old1}->{new1}')
        elif style == 'bracket':
            replace_once(path, f'lines()[{old1 - 1}]', f'lines()[{new1 - 1}]', f'{old1}->{new1}')
        elif style == 'ls':
            replace_once(path, f'ls[{old1 - 1}]', f'ls[{new1 - 1}]', f'{old1}->{new1}')
            replace_once(path, f'len(ls) < {old1}', f'len(ls) < {new1}', f'guard {old1}->{new1}')
        elif style == 'setnum':
            txt = open(path, encoding='utf-8').read()
            # bare number inside a set literal: match '    <n>,' or '    <n>  #'
            pat = re.compile(r'(?m)^(\s+)' + str(old1) + r'(,.*)$')
            ms = pat.findall(txt)
            assert len(ms) == 1, f'{fname} setnum {old1}: found {len(ms)} matches'
            txt = pat.sub(lambda m: m.group(1) + str(new1) + m.group(2), txt, count=1)
            open(path, 'w', encoding='utf-8').write(txt)
            print(f'  {fname}: {old1}->{new1}')
    header(path, '# v20a266 resync：index.html 淨 +328 行（V158 block ＋284／StoryPlay hook ＋1／載入呼叫 ＋1／enc158 hook ＋42）；釘行按 difflib 映射重寫，內容逐字相同，純漂移。')

# ---- travel114 DEF / WRAPPER (not set literals) ----
path = W266 + 'test_travel114_static.py'
for old1, new1 in [(41797, 42125), (29554, 29882)]:
    assert check_pin(old1) == new1, f'travel114 anchor {old1}->{new1} mapping mismatch'
replace_once(path, 'DEF_LINE = 41797', 'DEF_LINE = 42125', 'DEF_LINE')
replace_once(path, 'WRAPPER_LINE = 29554', 'WRAPPER_LINE = 29882', 'WRAPPER_LINE')

# ---- ledgers: gift185 / tang171 / tang173 ----
for fname in ['test_gift185_static.py', 'test_tang171_static.py', 'test_tang173_static.py']:
    path = W266 + fname
    print(f'== {fname} (ledger) ==')
    replace_once(path, '總行數 46625（v193', '總行數 46953（v193', 'total label')
    replace_once(path, '＋v265 +378）', '＋v265 +378＋v266 +328）', 'total ledger tail')
    cnt = open(path, encoding='utf-8').read().count("== 46614")
    assert cnt == 1, f'{fname}: == 46614 count {cnt}'
    replace_once(path, '== 46614', '== 46942', 'total count')
    header(path, '# v20a266 resync：index.html 淨 +328 行；總行數帳本鏈尾加 ＋v266 +328（總行數 46625→46953）。')
for fname in ['test_tang171_static.py', 'test_tang173_static.py']:
    path = W266 + fname
    replace_once(path, 'openLoc DEF 行 41797（', 'openLoc DEF 行 42125（', 'DEF label')
    replace_once(path, '＋v265 +350，travel114 釘行', '＋v265 +350＋v266 +328，travel114 釘行', 'DEF ledger tail')
    replace_once(path, 'len(lines) >= 41803', 'len(lines) >= 42131', 'DEF guard')
    replace_once(path, 'lines[41796]', 'lines[42124]', 'DEF index')
    print(f'== {fname} DEF done ==')

print('RESYNC DONE')
