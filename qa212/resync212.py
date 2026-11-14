# v20a212 resync：index.html 淨 +39 行（見下文插入點），
# 10 個靜態測試嘅釘行按 difflib 映射重寫（單次掃描 dict 查表，唔逐對 re.sub）。
# 用法：python3 qa212/resync212.py
# 對位 pristine main f58f19c（~/workspace/linji-pristine212/index.html）同工作版 index.html，
# 逐個釘行核實內容逐字相同（純漂移），輸出 old->new 對照（寫入 qa212/resync212_map.json）。
import difflib
import json
import re
import sys

OLD = '/home/hatch/workspace/linji-pristine212/index.html'
NEW = '/home/hatch/workspace/linji-work212/index.html'
TESTS = '/home/hatch/workspace/linji-work212/tests'

old = open(OLD, encoding='utf-8').read().split('\n')
new = open(NEW, encoding='utf-8').read().split('\n')
print('old lines:', len(old), 'new lines:', len(new), 'net:', len(new) - len(old))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-indexed
print('non-equal opcodes:', [(t, i1 + 1, i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal'])


def set_ints(fname, var):
    txt = open(f'{TESTS}/{fname}', encoding='utf-8').read()
    i = txt.index(var + ' = {')
    j = txt.index('\n}', i)
    seg = txt[i:j]
    seg = '\n'.join(ln.split('#', 1)[0] for ln in seg.split('\n'))
    return sorted(set(int(x) for x in re.findall(r'\b\d+\b', seg)))


def line_calls(fname):
    txt = open(f'{TESTS}/{fname}', encoding='utf-8').read()
    return sorted(set(int(x) for x in re.findall(r'\bline\((\d+)\)', txt)))


def idx_calls(fname, var):
    # 0-based index 用法（lines()[N]／ls[N]）→ 轉 1-based 行號
    txt = open(f'{TESTS}/{fname}', encoding='utf-8').read()
    return sorted(set(int(x) + 1 for x in re.findall(var + r'\[(\d+)\]', txt)))


pins = {
    'rom176': line_calls('test_rom176_static.py'),
    'tang152': idx_calls('test_tang152_static.py', r'lines\(\)'),
    'kwan151': line_calls('test_kwan151_static.py'),
    'text125': idx_calls('test_text125_static.py', r'ls'),
    'travel114 COUNT': set_ints('test_travel114_static.py', 'COUNT_LINES'),
    'travel114 FREE': set_ints('test_travel114_static.py', 'FREE_LINES'),
    'travel114 DEF/WRAPPER': [56186, 45180],
    'tang171 DEF': [56186],
    'tang173 DEF/L4862': [56186, 4954],
}
out_map = {}
bad = []
for group, nums in pins.items():
    for n in nums:
        m = mapping.get(n)
        same = (m is not None and old[n - 1] == new[m - 1])
        print(f'{group:22s} old {n} -> new {m} {"SAME" if same else "DIFF!!"}  {old[n-1].strip()[:70]}')
        if not same:
            bad.append((group, n, m))
        else:
            out_map.setdefault(group, {})[n] = m
print('BAD:', bad if bad else 'none — 全部純漂移')
with open('/home/hatch/workspace/linji-work212/qa212/resync212_map.json', 'w', encoding='utf-8') as f:
    json.dump(out_map, f, ensure_ascii=False, indent=1)
sys.exit(1 if bad else 0)
