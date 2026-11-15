# v20a218 resync：rom176／tang152／travel114 三檔釘行按 difflib 映射重寫。
# 用法：python3 qa218/resync218_pins.py
# 對位基底 main HEAD（v217，e54d9a1）同工作版 index.html；每個錨點內容逐字核實純漂移。
# 替換只改 code 位（line(N)／lines()[N]／COUNT/FREE 集合／DEF_LINE／WRAPPER_LINE），
# 註解入面嘅歷史 L 號唔郁。單次掃描 dict 查表，唔逐對 re.sub。
import difflib
import re
import subprocess
import sys

ROOT = '/home/hatch/workspace/linji-repo'
old = subprocess.check_output(['git', 'show', 'main:index.html'], cwd=ROOT).decode('utf-8').splitlines()
new = open(f'{ROOT}/index.html', encoding='utf-8').read().splitlines()
print('old lines:', len(old), 'new lines:', len(new), 'net:', len(new) - len(old))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based


def mapped(a):
    n = mapping.get(a)
    assert n is not None, f'行 {a} 唔喺 equal 段（內容改過，唔係純漂移）'
    assert old[a - 1] == new[n - 1], f'行 {a}→{n} 內容唔同：{old[a-1][:60]!r} vs {new[n-1][:60]!r}'
    return n


def rewrite(path, pat, fmt):
    s = open(f'{ROOT}/{path}', encoding='utf-8').read()
    found = {}

    def sub(m):
        a = int(m.group(1))
        if a not in found:
            found[a] = mapped(a)
        return fmt(found[a])

    s2, n = re.subn(pat, sub, s)
    assert n > 0, f'{path}：搵唔到錨點'
    open(f'{ROOT}/{path}', 'w', encoding='utf-8').write(s2)
    print(f'{path}: {len(found)} 個錨點 {sorted(found.items())}')
    return found


# --- rom176：line(N)（1-based） ---
rewrite('tests/test_rom176_static.py', re.compile(r'line\((\d+)\)'),
        lambda n: f'line({n})')
# --- tang152：lines()[N]（0-based index → 行 N+1） ---
s = open(f'{ROOT}/tests/test_tang152_static.py', encoding='utf-8').read()
found = {}

def sub_tang(m):
    idx = int(m.group(1))
    a = idx + 1
    if a not in found:
        found[a] = mapped(a)
    return f'lines()[{found[a] - 1}]'

s2, n = re.subn(r'lines\(\)\[(\d+)\]', sub_tang, s)
assert n > 0
open(f'{ROOT}/tests/test_tang152_static.py', 'w', encoding='utf-8').write(s2)
print(f'tests/test_tang152_static.py: {len(found)} 個錨點 {sorted(found.items())}（0-based index 已換算）')

# --- travel114：COUNT_LINES／FREE_LINES 集合＋DEF_LINE／WRAPPER_LINE ---
p = 'tests/test_travel114_static.py'
s = open(f'{ROOT}/{p}', encoding='utf-8').read()
found = {}
for m in re.finditer(r'^(DEF_LINE|WRAPPER_LINE) = (\d+)', s, re.M):
    a = int(m.group(2))
    found[a] = mapped(a)
for m in re.finditer(r'(COUNT_LINES|FREE_LINES) = \{(.*?)\n\}', s, re.S):
    for a in (int(x) for x in re.findall(r'^\s+(\d+),', m.group(2), re.M)):
        found[a] = mapped(a)
print(f'{p}: {len(found)} 個錨點')
# 只喺兩個集合 block＋兩行賦值入面換（註解唔郁）
def sub_block(m):
    head, body, tail = m.group(1), m.group(2), m.group(3)
    body = re.sub(r'^(\s+)(\d+),', lambda mm: mm.group(1) + str(found[int(mm.group(2))]) + ',', body, flags=re.M)
    return head + body + tail
s = re.sub(r'((?:COUNT_LINES|FREE_LINES) = \{)(.*?)(\n\})', sub_block, s, flags=re.S)
s = re.sub(r'^(DEF_LINE|WRAPPER_LINE) = (\d+)', lambda m: f'{m.group(1)} = {found[int(m.group(2))]}', s, flags=re.M)
open(f'{ROOT}/{p}', 'w', encoding='utf-8').write(s)
print(f'{p}: 重寫完成，DEF {found.get(57230)}／WRAPPER {found.get(45430)}')
print('RESYNC218_PINS OK')
