# v361 resync 套用：difflib 映射舊行號→新行號，逐行核實內容逐字相同先改釘（純漂移）
# 對象：travel114／tang152／tang171／tang173／gift185／rom159／rom176／text125
import difflib, re, subprocess, sys

old = subprocess.check_output(['git', 'show', 'HEAD:index.html']).decode('utf-8').splitlines()
new = open('index.html', encoding='utf-8').read().splitlines()
sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
MAP = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            MAP[i1 + k + 1] = j1 + k + 1

def m(o):  # 1-based -> 1-based, verify content
    n = MAP.get(o)
    assert n is not None, f'UNMAPPED old line {o}: {old[o-1][:80]}'
    assert old[o - 1] == new[n - 1], f'DIFF at {o}->{n}'
    return n

def edit(path, fn):
    s = open(path, encoding='utf-8').read()
    s2 = fn(s)
    assert s2 != s, f'no change in {path}'
    open(path, 'w', encoding='utf-8').write(s2)
    print('resynced', path)

TOTAL_OLD, TOTAL_NEW = 47068, len(new)
print(f'total {TOTAL_OLD} -> {TOTAL_NEW} (net {TOTAL_NEW-TOTAL_OLD:+d})')
DEF_OLD = 42289
DEF_NEW = m(DEF_OLD)
print(f'openLoc DEF {DEF_OLD} -> {DEF_NEW}')

# ---- travel114：COUNT_LINES／FREE_LINES／DEF_LINE／WRAPPER_LINE ----
def travel(s):
    def repl_block(s, name):
        mm = re.search(name + r' = \{(.*?)\n\}', s, re.S)
        assert mm, name
        blk = mm.group(1)
        def rn(x):
            o = int(x.group(0))
            return str(m(o))
        blk2 = re.sub(r'(?<![\w.])\d{4,5}(?=,)', rn, blk)
        return s[:mm.start(1)] + blk2 + s[mm.end(1):]
    s = repl_block(s, 'COUNT_LINES')
    s = repl_block(s, 'FREE_LINES')
    s = s.replace('DEF_LINE = 42289', f'DEF_LINE = {DEF_NEW}')
    w = re.search(r'WRAPPER_LINE = (\d+)', s)
    s = s.replace(f'WRAPPER_LINE = {w.group(1)}', f'WRAPPER_LINE = {m(int(w.group(1)))}')
    s = s.replace('# v20a358 resync', '# v20a361 resync：index.html 淨 +93 行（P1 平衡修復：合約信用／結局次序／負標籤預警／頒獎 q 表）；COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；openLoc( 呼叫點總數不變。\n# v20a358 resync', 1)
    return s
edit('tests/test_travel114_static.py', travel)

# ---- tang152：lines()[14348]／[14473]（0-based） ----
def tang152(s):
    for idx in (14348, 14473):
        s = s.replace(f'lines()[{idx}]', f'lines()[{m(idx + 1) - 1}]')
    s = s.replace('# v20a358 resync', '# v20a361 resync：index.html 淨 +93 行（P1 平衡修復）；2 個釘索引按 difflib 映射重寫，內容逐字核實純漂移。\n# v20a358 resync', 1)
    return s
edit('tests/test_tang152_static.py', tang152)

# ---- tang171／tang173／gift185：總行數＋openLoc DEF ----
def chain(s):
    s = s.replace('總行數 47068', f'總行數 {TOTAL_NEW}')
    s = s.replace('＋v360 +69）', '＋v360 +69＋v361 +93）')
    s = s.replace('== 47068', f'== {TOTAL_NEW}')
    s = s.replace('openLoc DEF 行 42289', f'openLoc DEF 行 {DEF_NEW}')
    s = s.replace('＋v360 +53，travel114', f'＋v360 +53＋v361 +{DEF_NEW - DEF_OLD}，travel114')
    s = s.replace('len(lines) >= 42289', f'len(lines) >= {DEF_NEW}')
    s = s.replace('lines[42288]', f'lines[{DEF_NEW - 1}]')
    return s
for p in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py', 'tests/test_gift185_static.py'):
    edit(p, chain)

# ---- rom159：line_has 4 釘 ----
def rom159(s):
    for o in (25112, 26006, 14421, 25861):
        s = s.replace(f'line_has({o},', f'line_has({m(o)},')
    return s
edit('tests/test_rom159_static.py', rom159)

# ---- rom176：line() 6 釘 ----
def rom176(s):
    for o in (6325, 14419, 40516, 40866, 42169, 42330):
        s = s.replace(f'line({o})', f'line({m(o)})')
    s = s.replace('# v20a355 resync', '# v20a361 resync：index.html 淨 +93 行（P1 平衡修復）；釘行按 difflib 映射重寫，錨點內容逐字相同，純漂移。\n# v20a355 resync', 1)
    return s
edit('tests/test_rom176_static.py', rom176)

# ---- text125：ls[15980]（0-based） ----
def text125(s):
    n1 = m(15981)
    s = s.replace('ls[15980]', f'ls[{n1 - 1}]')
    s = s.replace('len(ls) < 15981', f'len(ls) < {n1}')
    s = s.replace('第 15981 行冇 b.text 分支', f'第 {n1} 行冇 b.text 分支')
    return s
edit('tests/test_text125_static.py', text125)

print('ALL RESYNC DONE')
