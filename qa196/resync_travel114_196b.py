# v20a196 第二次 rebase 上 main 2c1a680（v199）：travel114 COUNT／FREE 清單重算。
# 方法同上：base（bc7f234，第一次 rebase 後 60750 行）對 merged（60794 行），difflib 對位。
# 方法：base（bc7f234）同 merged 兩版 index.html 各自列舉全部含 'openLoc(' 嘅行，
# 用 difflib SequenceMatcher 按內容＋次序對位（純漂移＋v196 刪走 leaveStory 嗰行），
# 將 v196 版清單（bc7f234）嘅 base 行號映射去 rebased 行號。
# 驗證：印出嚟嘅清單直接跑 tests/test_travel114_static.py——佢自己會重列舉全部呼叫點對清單，
# 漏／錯都會 FAIL 兼印 UNACCOUNTED。
import re, subprocess, difflib

WORK = '/home/hatch/workspace/linji-work196'

def show(rev, path):
    out = subprocess.run(['git', '-C', WORK, 'show', f'{rev}:{path}'],
                         capture_output=True, text=True)
    assert out.returncode == 0, (rev, path, out.stderr[:200])
    return out.stdout.split('\n')

def sites(lines):
    # 全部含 openLoc( 嘅行（連定義／wrapper／測試區／back176 一併列舉，對位先準）
    return [(i + 1, l) for i, l in enumerate(lines) if 'openLoc(' in l]

def parse_list(src_text, name):
    m = re.search(name + r'\s*=\s*\{(.*?)\n\}', src_text, re.S)
    assert m, name
    body = m.group(1)
    out = []  # (number, comment)
    for ln in body.split('\n'):
        mm = re.match(r'\s*(\d+)\s*,?\s*(#.*)?$', ln)
        if mm:
            out.append((int(mm.group(1)), (mm.group(2) or '').strip()))
    return out

base_lines = show('bc7f234', 'index.html')  # v196 版 index.html（清單行號以呢版為準）
reb_lines = open(WORK + '/index.html', encoding='utf-8').read().split('\n')
base_sites = sites(base_lines)
reb_sites = sites(reb_lines)
print(f'base call sites: {len(base_sites)}, rebased call sites: {len(reb_sites)}')

base_seq = [l.strip() for _, l in base_sites]
reb_seq = [l.strip() for _, l in reb_sites]
sm = difflib.SequenceMatcher(a=base_seq, b=reb_seq, autojunk=False)
mapping = {}  # base line -> rebased line
deleted = []
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

t196 = show('bc7f234', 'tests/test_travel114_static.py')
t196_text = '\n'.join(t196)
count196 = parse_list(t196_text, 'COUNT_LINES')
free196 = parse_list(t196_text, 'FREE_LINES')
print(f'v196 COUNT: {len(count196)}, FREE: {len(free196)}')

def remap(lst, name):
    out = []
    missing = []
    for num, comment in lst:
        if num in mapping:
            out.append((mapping[num], comment))
        else:
            missing.append((num, comment))
    print(f'{name}: mapped {len(out)}, missing {len(missing)}')
    for num, comment in missing:
        print(f'  MISSING base L{num} {comment}')
    return out

count_new = remap(count196, 'COUNT')
free_new = remap(free196, 'FREE')

# 逐行核實：FREE 嘅行實要有旗，COUNT 嘅行實要冇旗（同測試本身同一邏輯）
FREE_FLAGS = ("travelFree:true", "encDone:true", "forceRestore:true", "wf4Done:true")
bad = []
for num, comment in free_new:
    if not any(f in reb_lines[num - 1] for f in FREE_FLAGS):
        bad.append(('FREE no flag', num, reb_lines[num - 1].strip()[:90]))
for num, comment in count_new:
    if any(f in reb_lines[num - 1] for f in FREE_FLAGS):
        bad.append(('COUNT has flag', num, reb_lines[num - 1].strip()[:90]))
print('flag check bad:', len(bad))
for b in bad:
    print('  ', b)

# 防重複／防漏：rebase 後全部呼叫點（扣定義／wrapper／測試區／back176）應該全部喺兩清單入面
print()
print('COUNT_LINES = {')
for num, comment in count_new:
    print(f'    {num},  {comment}')
print('}')
print()
print('FREE_LINES = {')
for num, comment in free_new:
    print(f'    {num},  {comment}')
print('}')
print()
print('DEF_LINE =', [n for n, l in reb_sites if 'function openLoc(id, opts){' in l])
print('WRAPPER_LINE =', [n for n, l in reb_sites if 'openLoc: function(id, opts){ openLoc(id, opts); }' in l])
