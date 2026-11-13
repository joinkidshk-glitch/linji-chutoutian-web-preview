#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v20a153 第二輪 rebase（上 main e8c3a73／v170）resync：
#   old = main e8c3a73:index.html，new = rebased 工作版 index.html（main＋v153 hunks）。
#   difflib 對位建 old→new 行號映射（equal 段先至映射；非 equal 段嘅錨點即刻報錯）。
#   只改 code 行嘅行號，header 歷史註解原封不動，另加一條新 resync 記錄行。
import difflib, re, subprocess

WORK = '/home/hatch/workspace/linji-work153'

def git_show(rev, path):
    r = subprocess.run(['git', 'show', '%s:%s' % (rev, path)],
                       capture_output=True, text=True, cwd=WORK)
    assert r.returncode == 0, r.stderr
    return r.stdout.split('\n')

old = git_show('e8c3a73', 'index.html')
new = open(WORK + '/index.html', encoding='utf-8').read().split('\n')
sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
print('opcodes: %d, mapped old lines: %d of %d' % (len(sm.get_opcodes()), len(mapping), len(old)))
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        print('  %s old %d-%d new %d-%d' % (tag, i1 + 1, i2, j1 + 1, j2))

def need(n):
    assert n in mapping, '錨點行 %d 唔喺 equal 段，唔可以靜默映射' % n
    return mapping[n]

# ---------- test_tang171_static.py ----------
p = 'tests/test_tang171_static.py'
txt = '\n'.join(git_show('HEAD', p))
new_total = open(WORK + '/index.html', encoding='utf-8').read().count('\n')
# 搵 HEAD 版嘅舊總行數／DEF 行
m_total = re.search(r"src\.count\('\\n'\) == (\d+)", txt)
m_def = re.search(r"len\(lines\) >= (\d+) and 'function openLoc\(id, opts\)\{' in lines\[(\d+)\]", txt)
old_total = int(m_total.group(1))
old_def = int(m_def.group(1))
assert int(m_def.group(2)) == old_def - 1
new_def = need(old_def)
print('tang171 total %d -> %d, DEF %d -> %d' % (old_total, new_total, old_def, new_def))
txt = txt.replace("src.count('\\n') == %d" % old_total,
                  "src.count('\\n') == %d" % new_total)
txt = txt.replace("len(lines) >= %d and 'function openLoc(id, opts){' in lines[%d]"
                  % (old_def, old_def - 1),
                  "len(lines) >= %d and 'function openLoc(id, opts){' in lines[%d]"
                  % (new_def, new_def - 1))
# 測試名＋header 註解嘅數字一併更新（只限呢兩個錨點數字）
txt = txt.replace('總行數 %d' % old_total, '總行數 %d' % new_total)
txt = txt.replace('DEF 行 %d' % old_def, 'DEF 行 %d' % new_def)
txt = txt.replace('DEF %d' % old_def, 'DEF %d' % new_def)
note = ('# v20a153 第二輪 rebase 上 main e8c3a73（v170）resync：總行數 %d→%d、'
        'DEF %d→%d（difflib 對位核實純漂移，見 qa153/resync_rebase153b.py）。'
        % (old_total, new_total, old_def, new_def))
assert note not in txt
txt = txt.replace("# 反證：喺 pristine main（56141a3／v169）index 上行，新行為斷言會乾淨 FAIL，",
                  note + "\n# 反證：喺 pristine main（56141a3／v169）index 上行，新行為斷言會乾淨 FAIL，")
open(WORK + '/' + p, 'w', encoding='utf-8').write(txt)
print('tang171 寫好')

# ---------- test_travel114_static.py ----------
p = 'tests/test_travel114_static.py'
txt = '\n'.join(git_show('HEAD', p))
lines = txt.split('\n')
in_count = in_free = False
n_mapped = 0
for i, ln in enumerate(lines):
    if ln.startswith('COUNT_LINES'):
        in_count = True
    elif ln.startswith('FREE_LINES'):
        in_free = True
    elif in_count and ln.startswith('}'):
        in_count = False
    elif in_free and ln.startswith('}'):
        in_free = False
    if ln.lstrip().startswith('#'):
        continue
    if in_count or in_free:
        lines[i], n = re.subn(r'\b(\d+)\b', lambda m: str(need(int(m.group(1)))), ln, count=1)
        n_mapped += n
    elif ln.startswith('DEF_LINE'):
        lines[i] = re.sub(r'DEF_LINE = (\d+)', lambda m: 'DEF_LINE = %d' % need(int(m.group(1))), ln)
        n_mapped += 1
    elif ln.startswith('WRAPPER_LINE'):
        lines[i] = re.sub(r'WRAPPER_LINE = (\d+)', lambda m: 'WRAPPER_LINE = %d' % need(int(m.group(1))), ln)
        n_mapped += 1
txt = '\n'.join(lines)
print('travel114 mapped numbers:', n_mapped)
note = ('# v20a153 第二輪 rebase 上 main e8c3a73（v170）resync：difflib 對位核實純漂移，'
        'COUNT/FREE/DEF/WRAPPER 行號按映射重寫（見 qa153/resync_rebase153b.py）。')
txt = txt.replace("# 頁內測試區：runSoftP0Checks 函數範圍（brace-match 實量，唔靠死行號）",
                  note + "\n# 頁內測試區：runSoftP0Checks 函數範圍（brace-match 實量，唔靠死行號）")
open(WORK + '/' + p, 'w', encoding='utf-8').write(txt)
print('travel114 寫好')
print('全部完成')
