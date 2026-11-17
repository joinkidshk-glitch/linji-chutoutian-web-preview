# v266 resync part 2: ledgers for tang171 / tang173 only
# (part 1 already resynced text125/kwan151/tang152/rom159/rom176/travel114/gift185).
W266 = '/home/hatch/workspace/linji-work266/tests/'

def replace_once(path, old, new, label):
    txt = open(path, encoding='utf-8').read()
    n = txt.count(old)
    assert n == 1, f'{path} {label}: expected 1 occurrence of {old!r}, found {n}'
    open(path, 'w', encoding='utf-8').write(txt.replace(old, new, 1))
    print(f'  {path.split("/")[-1]}: {label}')

for fname in ['test_tang171_static.py', 'test_tang173_static.py']:
    path = W266 + fname
    replace_once(path, '總行數 46625（v193', '總行數 46953（v193', 'total label')
    replace_once(path, '＋v265 +378）\', src.count', '＋v265 +378＋v266 +328）\', src.count', 'total ledger tail')
    replace_once(path, '== 46614', '== 46942', 'total count')
    replace_once(path, 'openLoc DEF 行 41797（', 'openLoc DEF 行 42125（', 'DEF label')
    replace_once(path, '＋v265 +350，travel114 釘行', '＋v265 +350＋v266 +328，travel114 釘行', 'DEF ledger tail')
    replace_once(path, 'len(lines) >= 41803', 'len(lines) >= 42131', 'DEF guard')
    replace_once(path, 'lines[41796]', 'lines[42124]', 'DEF index')
    txt = open(path, encoding='utf-8').read()
    open(path, 'w', encoding='utf-8').write(
        '# v20a266 resync：index.html 淨 +328 行；總行數帳本鏈尾加 ＋v266 +328（總行數 46625→46953）；openLoc DEF 41797→42125。\n' + txt)
    print(f'== {fname} done ==')
print('LEDGER RESYNC DONE')
