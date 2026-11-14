# v20a215 resync：index.html 淨 +140 行（插入點：advanceDay +2／enqueue 註解 +1／
# RELEASE215 block +130／buildNewspaperEdition 排序 +4／pullDue 懶掃 +3；見下文），
# 7 個靜態測試嘅釘行按 difflib 映射重寫（單次掃描 dict 查表，唔逐對 re.sub）。
# 用法：python3 qa215/resync215.py
# 對位基底 main eed04dc（git show）同工作版 index.html，
# 逐個釘行核實內容逐字相同（純漂移），輸出 old->new 對照（寫入 qa215/resync215_map.json）。
# 附帶發現：tang171／tang173 嘅 DEF 名公式漏咗 v211 +42——真 DEF 喺 56267（lines[56266]），
# 名寫嘅 56225 係錯數；apply 嗰陣補返 +42（56267→56407），唔係跟錯數 56225→56365。
import difflib
import json
import re
import subprocess
import sys

ROOT = '/home/hatch/workspace/linji-work215'
old = subprocess.check_output(['git', 'show', 'eed04dc:index.html'], cwd=ROOT).decode('utf-8').split('\n')
new = open(f'{ROOT}/index.html', encoding='utf-8').read().split('\n')
print('old lines:', len(old), 'new lines:', len(new), 'net:', len(new) - len(old))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-indexed
print('non-equal opcodes:', [(t, i1 + 1, i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal'])


def set_ints(fname, var):
    txt = open(f'{ROOT}/tests/{fname}', encoding='utf-8').read()
    i = txt.index(var + ' = {')
    j = txt.index('\n}', i)
    seg = txt[i:j]
    seg = '\n'.join(ln.split('#', 1)[0] for ln in seg.split('\n'))
    return sorted(set(int(x) for x in re.findall(r'\b\d+\b', seg)))


def line_calls(fname):
    txt = open(f'{ROOT}/tests/{fname}', encoding='utf-8').read()
    return sorted(set(int(x) for x in re.findall(r'\bline\((\d+)\)', txt)))


pins = {
    'rom176': line_calls('test_rom176_static.py'),
    'tang171 DEF(check)': [56267],
    'tang173 DEF(check)': [56267],
    'travel114 COUNT': set_ints('test_travel114_static.py', 'COUNT_LINES'),
    'travel114 FREE': set_ints('test_travel114_static.py', 'FREE_LINES'),
    'travel114 DEF/WRAPPER': [56267, 45188],
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
with open(f'{ROOT}/qa215/resync215_map.json', 'w', encoding='utf-8') as f:
    json.dump(out_map, f, ensure_ascii=False, indent=1)
sys.exit(1 if bad else 0)
