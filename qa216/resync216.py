# v20a216 resync：index.html 淨 +263 行（工作副本 vs pristine main v215），
# 8 個靜態測試嘅釘行按 difflib 映射重寫（單次掃描 dict 查表，唔逐對 re.sub）。
# 用法：python3 qa216/resync216.py
# 對位基底 main HEAD（v215，git show HEAD:index.html）同工作版 index.html，
# 逐個釘行核實內容逐字相同（純漂移），輸出 old->new 對照（寫入 qa216/resync216_map.json）。
# 插入點（git diff --numstat：+322／-59，淨 +263）：CSS headline4／factbox-wide（~L4760-4900）、
# renderMorningPaperHtml R1-R3 跟進（~L50500-50630）、newspaperCheck R1／R3（~L51030-51120）、
# R0 隊列三層閘、R5 口語重寫（原位替換，淨 0 行，唔產生漂移）。
import difflib
import json
import re
import subprocess
import sys

ROOT = '/home/hatch/workspace/linji-work216'
old = subprocess.check_output(['git', 'show', 'HEAD:index.html'], cwd=ROOT).decode('utf-8').split('\n')
new = open(f'{ROOT}/index.html', encoding='utf-8').read().split('\n')
print('old lines:', len(old) - 1, 'new lines:', len(new) - 1, 'net:', (len(new) - 1) - (len(old) - 1))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-indexed
print('non-equal opcodes (1-based start, old_len -> new_len):',
      [(t, i1 + 1, i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal'])


def head_test(fname):
    return subprocess.check_output(['git', 'show', f'HEAD:tests/{fname}'], cwd=ROOT).decode('utf-8')


def line_calls(fname):
    txt = head_test(fname)
    code = '\n'.join(ln.split('#', 1)[0] for ln in txt.split('\n'))
    return sorted(set(int(x) for x in re.findall(r'\bline\((\d+)\)', code)))


def set_ints(fname, var):
    txt = head_test(fname)
    i = txt.index(var + ' = {')
    j = txt.index('\n}', i)
    seg = txt[i:j]
    seg = '\n'.join(ln.split('#', 1)[0] for ln in seg.split('\n'))
    return sorted(set(int(x) for x in re.findall(r'\b\d+\b', seg)))


def idx_calls(fname, pat):
    txt = head_test(fname)
    code = '\n'.join(ln.split('#', 1)[0] for ln in txt.split('\n'))
    return sorted(set(int(x) for x in re.findall(pat, code)))


# 釘行清單（全部 1-based 行號；0-based 索引喺呢度先轉返 1-based）。
pins = {
    'kwan151': line_calls('test_kwan151_static.py'),
    'rom176': line_calls('test_rom176_static.py'),
    # tang152：lines()[N] 係 0-based，1-based 行 = N+1。
    'tang152': [n + 1 for n in idx_calls('test_tang152_static.py', r'lines\(\)\[(\d+)\]')],
    # tang171／173：lines[N] 0-based；DEF lines[56963] = 行 56964。
    'tang171 DEF': [56964],
    'tang173 DEF': [56964],
    # tang173：L4862 錨點 lines[5124] = 行 5125。
    'tang173 L4862': [5125],
    # text125：ls[N] 0-based。
    'text125': [n + 1 for n in idx_calls('test_text125_static.py', r'\bls\[(\d+)\]')],
    'travel114 COUNT': set_ints('test_travel114_static.py', 'COUNT_LINES'),
    'travel114 FREE': set_ints('test_travel114_static.py', 'FREE_LINES'),
    'travel114 DEF/WRAPPER': [56964, 45392],
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
with open(f'{ROOT}/qa216/resync216_map.json', 'w', encoding='utf-8') as f:
    json.dump(out_map, f, ensure_ascii=False, indent=1)
sys.exit(1 if bad else 0)
