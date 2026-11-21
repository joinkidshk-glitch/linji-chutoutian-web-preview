# -*- coding: utf-8 -*-
# v363 resync：index.html 淨 +437 行（UI363 CSS +332＠舊 L5965 前插入、JS block +99＠舊 L22105 前、
#   drawMap hooks +3、paintBar hook +1、stressScale hook +1、today sticker 1→2 行、層掣／壓力 hide 原地換值）。
#   用 difflib 將每條釘行由 base 10bb733 對位去現行 index.html，逐行核實內容逐字相同＝純漂移先改行號。
#   單次掃描 dict 查表一次過換，唔逐對 re.sub（AGENTS.md v160 教訓）。註解行唔郁（歷史數字）。
# 用法：python3 qa363/resync363.py [--apply]
import difflib, re, subprocess, sys

ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
APPLY = '--apply' in sys.argv

def git_lines(ref):
    out = subprocess.run(['git', 'show', '%s:index.html' % ref], cwd=ROOT, capture_output=True, text=True)
    assert out.returncode == 0, ref
    return out.stdout.split('\n')

base = git_lines('10bb733')
with open('%s/index.html' % ROOT, encoding='utf-8') as f:
    head_src = f.read()
head = head_src.split('\n')
NEW_TOTAL = head_src.count('\n')

sm = difflib.SequenceMatcher(None, base, head, autojunk=False)
MAP = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            MAP[i1 + 1 + k] = j1 + 1 + k

def map1(n):
    m = MAP.get(n)
    if m is None or base[n - 1] != head[m - 1]:
        return None
    return m

def map0(n):
    m = map1(n + 1)
    return None if m is None else m - 1

changes = []

def sub_code_lines(path, rules):
    """逐行處理，跳過註解行（strip 後以 # 開頭）。"""
    with open('%s/%s' % (ROOT, path), encoding='utf-8') as f:
        lines = f.read().split('\n')
    out = []
    for ln in lines:
        if ln.lstrip().startswith('#'):
            out.append(ln)
            continue
        for pat, fn in rules:
            def repl(mo, fn=fn):
                new = fn(mo)
                return new if new is not None else mo.group(0)
            ln = re.sub(pat, repl, ln)
        out.append(ln)
    src = '\n'.join(out)
    with open('%s/%s' % (ROOT, path), encoding='utf-8') as f:
        orig = f.read()
    if src != orig:
        changes.append(path)
        if APPLY:
            with open('%s/%s' % (ROOT, path), 'w', encoding='utf-8') as f:
                f.write(src)
    return src

# ---- rom159：line_has(NNN, ...) 1-based ----
def r_line_has(mo):
    n = int(mo.group(1)); m = map1(n)
    if m is None or m == n: return None
    print('rom159 line_has %d -> %d' % (n, m))
    return 'line_has(%d,' % m
sub_code_lines('tests/test_rom159_static.py', [(r'line_has\((\d+),', r_line_has)])

# ---- rom176：ok('釘...', line(NNN)...) 1-based，只限釘行 ----
def r_rom176(mo):
    n = int(mo.group(2)); m = map1(n)
    if m is None or m == n: return None
    print('rom176 line %d -> %d' % (n, m))
    return mo.group(1) + 'line(%d)' % m
sub_code_lines('tests/test_rom176_static.py',
         [(r"(ok\('釘[^']*',\s*(?:[^\n]*?\b)?)line\((\d+)\)", r_rom176),
          (r"('GIFT_REACT = giftReact' in )line\((\d+)\)", r_rom176),
          (r"('rom176ApplyGiftOverrides\(\)' in )line\((\d+)\)", r_rom176)])

# ---- tang152：lines()[NNN] 0-based（只 code 行）----
def r_lines_idx(mo):
    n = int(mo.group(2)); m = map0(n)
    if m is None or m == n: return None
    print('lines()[%d] -> [%d]' % (n, m))
    return mo.group(1) + '[%d]' % m
sub_code_lines('tests/test_tang152_static.py', [(r'(lines\(\)|lines)\[(\d+)\]', r_lines_idx)])

# ---- text125：len(ls) < NNN（1-based）＋ ls[NNN]（0-based）＋報錯字串行號 ----
def r_text125_len(mo):
    n = int(mo.group(1)); m = map1(n)
    if m is None or m == n: return None
    print('text125 len %d -> %d' % (n, m))
    return 'len(ls) < %d' % m
def r_text125_idx(mo):
    n = int(mo.group(1)); m = map0(n)
    if m is None or m == n: return None
    print('text125 ls[%d] -> [%d]' % (n, m))
    return 'ls[%d]' % m
def r_text125_msg(mo):
    n = int(mo.group(2)); m = map1(n)
    if m is None or m == n: return None
    return mo.group(1) + str(m) + mo.group(3)
sub_code_lines('tests/test_text125_static.py', [
    (r'len\(ls\) < (\d+)', r_text125_len),
    (r'\bls\[(\d+)\]', r_text125_idx),
    (r'(probs\.append\("(?:currentLine|advance|applyFamilySafeToNode) 第 )(\d+)( 行)', r_text125_msg),
])

# ---- tang171／tang173／gift185：總行數＋openLoc DEF＋標籤鏈尾 ----
def r_total(mo):
    n = int(mo.group(2))
    if n == NEW_TOTAL: return None
    print('total %d -> %d' % (n, NEW_TOTAL))
    return mo.group(1) + str(NEW_TOTAL)
def r_def(mo):
    n = int(mo.group(2)); m = map1(n)
    if m is None or m == n: return None
    print('openLoc DEF %d -> %d' % (n, m))
    return mo.group(1) + str(m)
def r_label_total(mo):
    return '總行數 %d（' % NEW_TOTAL
def r_label_def(mo):
    n = int(mo.group(1)); m = map1(n)
    if m is None: return None
    return 'openLoc DEF 行 %d（' % m
for t in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py', 'tests/test_gift185_static.py']:
    sub_code_lines(t, [
        (r"((?:src|html)\.count\('\\n'\) == )(\d+)", r_total),
        (r'(len\(lines\) >= )(\d+)', r_def),
        (r'(lines)\[(\d+)\]', r_lines_idx),
        (r'總行數 \d+（', r_label_total),
        (r'openLoc DEF 行 (\d+)（', r_label_def),
        (r'＋v362 \+267）', lambda mo: '＋v362 +267＋v363 +437）'),
        (r'＋v362 \+267，travel114', lambda mo: '＋v362 +267＋v363 +437，travel114'),
    ])

# ---- travel114：COUNT_LINES／FREE_LINES 集＋DEF_LINE／WRAPPER_LINE ----
def r_travel_set(mo):
    n = int(mo.group(1)); m = map1(n)
    if m is None:
        print('travel114 UNMAPPED %d' % n)
        return None
    if m == n: return None
    return '%d,' % m
def r_travel_def(mo):
    n = int(mo.group(2)); m = map1(n)
    if m is None or m == n: return None
    print('travel114 %s %d -> %d' % (mo.group(1), n, m))
    return mo.group(1) + str(m)
with open('%s/tests/test_travel114_static.py' % ROOT, encoding='utf-8') as f:
    tsrc = f.read()
torig = tsrc
for name in ['COUNT_LINES', 'FREE_LINES']:
    mm = re.search(name + r' = \{(.*?)\n\}', tsrc, re.S)
    assert mm, name
    block = mm.group(1)
    newblock = re.sub(r'(\d+),', r_travel_set, block)
    tsrc = tsrc[:mm.start(1)] + newblock + tsrc[mm.end(1):]
tsrc = re.sub(r'(DEF_LINE = )(\d+)', r_travel_def, tsrc)
tsrc = re.sub(r'(WRAPPER_LINE = )(\d+)', r_travel_def, tsrc)
if tsrc != torig:
    changes.append('tests/test_travel114_static.py')
    if APPLY:
        with open('%s/tests/test_travel114_static.py' % ROOT, 'w', encoding='utf-8') as f:
            f.write(tsrc)

print('---')
print('NEW_TOTAL =', NEW_TOTAL)
print('files changed:', changes)
print('APPLY' if APPLY else 'dry-run')
