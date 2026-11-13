# v20a196 落地 squash merge 上 main 2de5026（v197）：travel114 COUNT／FREE 清單重算。
# base（ced807e，第三次 rebase 後 60806 行）對 merged（60900 行），difflib 對位。
import re, subprocess, difflib
REPO = '/home/hatch/workspace/linji-repo'
def show(rev, path):
    out = subprocess.run(['git', '-C', REPO, 'show', f'{rev}:{path}'], capture_output=True, text=True)
    assert out.returncode == 0, (rev, path, out.stderr[:200])
    return out.stdout.split('\n')
def sites(lines):
    return [(i + 1, l) for i, l in enumerate(lines) if 'openLoc(' in l]
def parse_list(src_text, name):
    m = re.search(name + r'\s*=\s*\{(.*?)\n\}', src_text, re.S)
    assert m, name
    out = []
    for ln in m.group(1).split('\n'):
        mm = re.match(r'\s*(\d+)\s*,?\s*(#.*)?$', ln)
        if mm:
            out.append((int(mm.group(1)), (mm.group(2) or '').strip()))
    return out
base_lines = show('ced807e', 'index.html')
reb_lines = open(REPO + '/index.html', encoding='utf-8').read().split('\n')
base_sites = sites(base_lines); reb_sites = sites(reb_lines)
print(f'base call sites: {len(base_sites)}, merged call sites: {len(reb_sites)}')
base_seq = [l.strip() for _, l in base_sites]
reb_seq = [l.strip() for _, l in reb_sites]
sm = difflib.SequenceMatcher(a=base_seq, b=reb_seq, autojunk=False)
mapping = {}; deleted = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag in ('equal', 'replace'):
        for k in range(min(i2 - i1, j2 - j1)):
            mapping[base_sites[i1 + k][0]] = reb_sites[j1 + k][0]
        if tag == 'replace' and (i2 - i1) != (j2 - j1):
            print(f'WARN replace block base[{i1}:{i2}] reb[{j1}:{j2}] (lengths differ)')
    elif tag == 'delete':
        for k in range(i1, i2):
            deleted.append((base_sites[k][0], base_sites[k][1].strip()[:100]))
print(f'mapped: {len(mapping)}, deleted base sites: {len(deleted)}')
for ln, txt in deleted:
    print(f'  DELETED base L{ln}: {txt}')
t = show('ced807e', 'tests/test_travel114_static.py')
ttext = '\n'.join(t)
count = parse_list(ttext, 'COUNT_LINES')
free = parse_list(ttext, 'FREE_LINES')
print(f'base COUNT: {len(count)}, FREE: {len(free)}')
def emit(name, lst):
    print(f'\n{name} = {{')
    miss = 0
    for num, cmt in lst:
        if num in mapping:
            print(f'    {mapping[num]},  {cmt}')
        else:
            print(f'    MISSING {num},  {cmt}'); miss += 1
    print('}')
    print(f'{name}: mapped {len(lst)-miss}, missing {miss}')
    return miss
m1 = emit('COUNT_LINES', count)
m2 = emit('FREE_LINES', free)
# flag check: every FREE line must contain a FREE flag
bad = 0
for num, cmt in free:
    if num in mapping:
        ln = reb_lines[mapping[num]-1]
        if not any(f in ln for f in ('travelFree:true', 'encDone:true', 'forceRestore:true', 'wf4Done:true')):
            print(f'FLAG BAD at merged L{mapping[num]}: {ln.strip()[:100]}'); bad += 1
print(f'flag check bad: {bad}')
# DEF / WRAPPER
for pat, label in [('function openLoc(id, opts){', 'DEF_LINE'), ('openLoc: function(id, opts){ openLoc(id, opts); }', 'WRAPPER_LINE')]:
    hits = [i+1 for i, l in enumerate(reb_lines) if pat in l]
    print(f'{label} = {hits}')
