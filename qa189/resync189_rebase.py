# v20a189 rebase 上 main 0c29f03（v188）resync：由分支舊 index（e1f8f5b，60189 行）
# 對位到 rebase 後 index（60443 行），逐個錨點核實內容逐字相同（純漂移）先更新測試檔。
# 用法：python3 qa189/resync189_rebase.py
import difflib, re, subprocess, sys

old = subprocess.check_output(['git', 'show', 'e1f8f5b:index.html'], text=True).split('\n')
new = open('index.html', encoding='utf-8').read().split('\n')
print('old newlines %d / new newlines %d (net %+d)' % (len(old) - 1, len(new) - 1, len(new) - len(old)))

mapping = {}
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1
print('mapped lines: %d / %d' % (len(mapping), len(old)))

bad = 0
def check(test, o, needle):
    global bad
    n = mapping.get(o)
    if n is None:
        print('FAIL %-8s old %6d -> (changed/deleted)' % (test, o)); bad += 1; return None
    hit = needle in new[n - 1]
    print('%s %-8s old %6d -> new %6d (delta %+d) needle %s :: %s' % (
        'PASS' if hit else 'FAIL', test, o, n, n - o, 'found' if hit else 'NOT FOUND', new[n - 1].strip()[:70]))
    if not hit:
        bad += 1
    return n

# rom176 (6) — 舊行號取自分支版（e1f8f5b）測試檔
rom = {}
rom['lan'] = check('rom176', 6070, 'lan:{ id:"lan", name:"藍若曦"')
rom['load'] = check('rom176', 31574, 'GIFT_REACT = giftReact')
rom['block'] = check('rom176', 53115, '/* ===== v20a176 ROM176')
rom['over'] = check('rom176', 53483, 'function rom176ApplyGiftOverrides()')
rom['addloc'] = check('rom176', 54622, 'function addLocTalkGiftActs(add, L, npcId)')
rom['intercept'] = check('rom176', 54716, 'rom176TryIntercept(id)')
# tang171 / tang173 DEF
defn = check('tang171', 54685, 'function openLoc(id, opts){')
check('tang173', 54685, 'function openLoc(id, opts){')
# tang173 L4862 anchor (分支版 assert lines[4886] 即 4887 行)
check('tang173', 4887, 'loc-acts-more171::after')

# travel114：分支版 COUNT／FREE／DEF／WRAPPER 逐行對位（附原註解）
branch = subprocess.check_output(['git', 'show', 'e1f8f5b:tests/test_travel114_static.py'], text=True)
def parse_set(name):
    m = re.search(name + r' = \{(.*?)\n\}', branch, re.S)
    out = []
    for ln in m.group(1).split('\n'):
        mm = re.match(r'\s*(\d+),\s*(#.*)?$', ln)
        if mm:
            out.append((int(mm.group(1)), (mm.group(2) or '').strip()))
    return out
for kind in ('COUNT_LINES', 'FREE_LINES'):
    mapped = []
    for o, cmt in parse_set(kind):
        n = mapping.get(o)
        if n is None:
            print('FAIL travel114 %s old %d -> (changed)' % (kind, o)); bad += 1; continue
        okc = 'openLoc(' in new[n - 1]
        if not okc:
            print('FAIL travel114 %s old %d -> new %d :: no openLoc(: %s' % (kind, o, n, new[n - 1].strip()[:70])); bad += 1
        mapped.append((n, cmt))
    print('travel114 %s mapped:' % kind)
    for n, cmt in mapped:
        print('    %d,%s %s' % (n, ' ' if cmt else '', cmt))
    globals()['M_' + kind] = mapped
for name, o in (('DEF_LINE', 54685), ('WRAPPER_LINE', 44387)):
    n = mapping.get(o)
    okc = n is not None and 'openLoc(' in new[n - 1]
    print('%s travel114 %s old %d -> new %s :: %s' % ('PASS' if okc else 'FAIL', name, o, n, (new[n-1].strip()[:70] if n else '')))
    if not okc:
        bad += 1
    globals()['M_' + name] = n
print('---')
print('rom176 mapped:', rom)
print('DEF mapped:', defn)
print('FAILURES: %d' % bad if bad else 'ALL PINS VERIFIED (pure drift)')
sys.exit(1 if bad else 0)
