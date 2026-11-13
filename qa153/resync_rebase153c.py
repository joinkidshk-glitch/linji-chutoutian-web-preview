#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# v20a153 第三輪 rebase（上 main a500536／v149）resync：
#   old = main a500536:index.html，new = rebased 工作版 index.html（main＋v153 hunks）。
#   difflib 對位建 old→new 行號映射（equal 段先至映射；非 equal 段錨點即刻報錯）。
#   只改 code 行嘅行號（# 註解行原封不動——第二輪教訓：blanket replace 誤改咗 v170 歷史註解）。
#   每檔另加一條新 resync 記錄行。
import difflib, re, subprocess

WORK = '/home/hatch/workspace/linji-work153'

def git_show(rev, path):
    r = subprocess.run(['git', 'show', '%s:%s' % (rev, path)],
                       capture_output=True, text=True, cwd=WORK)
    assert r.returncode == 0, r.stderr
    return r.stdout.split('\n')

old = git_show('a500536', 'index.html')
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

def add_note(txt, note, anchor):
    assert note not in txt, 'note 已存在'
    assert anchor in txt, 'anchor 唔見咗：%s' % anchor
    return txt.replace(anchor, note + '\n' + anchor, 1)

# ---------- test_kwan151_static.py ----------
p = 'tests/test_kwan151_static.py'
txt = '\n'.join(git_show('HEAD', p))
out = []
for ln in txt.split('\n'):
    if ln.lstrip().startswith('#'):
        out.append(ln)
        continue
    ln = re.sub(r'line\((\d+)\)', lambda m: 'line(%d)' % need(int(m.group(1))), ln)
    ln = re.sub(r'\bL(\d+)\b', lambda m: 'L%d' % need(int(m.group(1))), ln)
    out.append(ln)
txt = '\n'.join(out)
note = ('# v20a153 第三輪 rebase 上 main a500536（v149）resync：difflib 對位核實純漂移，'
        'code 行錨點按映射重寫（見 qa153/resync_rebase153c.py）。')
txt = add_note(txt, note, "# 用法：python3 tests/test_kwan151_static.py [path-to-index.html]")
open(WORK + '/' + p, 'w', encoding='utf-8').write(txt)
print('kwan151 寫好')

# ---------- test_text125_static.py ----------
p = 'tests/test_text125_static.py'
txt = '\n'.join(git_show('HEAD', p))
out = []
for ln in txt.split('\n'):
    if ln.lstrip().startswith('#'):
        out.append(ln)
        continue
    ln = re.sub(r'ls\[(\d+)\]', lambda m: 'ls[%d]' % (need(int(m.group(1)) + 1) - 1), ln)
    ln = re.sub(r'len\(ls\) < (\d+)', lambda m: 'len(ls) < %d' % need(int(m.group(1))), ln)
    ln = re.sub(r'第 (\d+) 行', lambda m: '第 %d 行' % need(int(m.group(1))), ln)
    out.append(ln)
txt = '\n'.join(out)
note = ('# v20a153 第三輪 rebase 上 main a500536（v149）resync：錨點 difflib 對位核實純漂移，'
        '行號按映射重寫（見 qa153/resync_rebase153c.py）。')
txt = add_note(txt, note, "# 用法：python3 tests/test_text125_static.py [path-to-index.html]")
open(WORK + '/' + p, 'w', encoding='utf-8').write(txt)
print('text125 寫好')

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
note = ('# v20a153 第三輪 rebase 上 main a500536（v149）resync：difflib 對位核實純漂移，'
        'COUNT/FREE/DEF/WRAPPER 行號按映射重寫（見 qa153/resync_rebase153c.py）。')
txt = add_note(txt, note, "# 頁內測試區：runSoftP0Checks 函數範圍（brace-match 實量，唔靠死行號）")
open(WORK + '/' + p, 'w', encoding='utf-8').write(txt)
print('travel114 寫好')

# ---------- test_tang152_static.py ----------
p = 'tests/test_tang152_static.py'
txt = '\n'.join(git_show('HEAD', p))
out = []
for ln in txt.split('\n'):
    if ln.lstrip().startswith('#'):
        out.append(ln)
        continue
    ln = re.sub(r'lines\(\)\[(\d+)\]', lambda m: 'lines()[%d]' % (need(int(m.group(1)) + 1) - 1), ln)
    ln = re.sub(r'\bL(\d+)\b', lambda m: 'L%d' % need(int(m.group(1))), ln)
    out.append(ln)
txt = '\n'.join(out)
note = ('# v20a153 第三輪 rebase 上 main a500536（v149）resync：HELD／normaliser／loader 三錨點 '
        'difflib 對位核實純漂移（見 qa153/resync_rebase153c.py）。')
txt = add_note(txt, note, "# 用法：python3 tests/test_tang152_static.py [path-to-index.html]")
open(WORK + '/' + p, 'w', encoding='utf-8').write(txt)
print('tang152 寫好')

# ---------- test_tang171_static.py ----------
p = 'tests/test_tang171_static.py'
txt = '\n'.join(git_show('HEAD', p))
# total 唔係行號，唔用 mapping——直接用新總行數；DEF 用 mapping
new_total = open(WORK + '/index.html', encoding='utf-8').read().count('\n')
m_total = re.search(r"src\.count\('\\n'\) == (\d+)", txt)
old_total = int(m_total.group(1))
m_def = re.search(r"len\(lines\) >= (\d+) and 'function openLoc\(id, opts\)\{' in lines\[(\d+)\]", txt)
old_def = int(m_def.group(1))
new_def = need(old_def)
print('tang171 total %d -> %d, DEF %d -> %d' % (old_total, new_total, old_def, new_def))
txt = txt.replace("src.count('\\n') == %d" % old_total,
                  "src.count('\\n') == %d" % new_total)
txt = txt.replace("len(lines) >= %d and 'function openLoc(id, opts){' in lines[%d]"
                  % (old_def, old_def - 1),
                  "len(lines) >= %d and 'function openLoc(id, opts){' in lines[%d]"
                  % (new_def, new_def - 1))
# ok() 名入面嘅數字（code 行，唔係註解）：總行數／DEF 行
txt = re.sub(r"(ok\('零行數漂移：總行數 )\d+(')", r"\g<1>%d\g<2>" % new_total, txt)
txt = re.sub(r"(ok\('零行數漂移：openLoc DEF 行 )\d+( 不變)", r"\g<1>%d\g<2>" % new_def, txt)
note = ('# v20a153 第三輪 rebase 上 main a500536（v149）resync：總行數 %d→%d、'
        'DEF %d→%d（difflib 對位核實純漂移，見 qa153/resync_rebase153c.py）。'
        % (old_total, new_total, old_def, new_def))
txt = add_note(txt, note, "# 反證：喺 pristine main（56141a3／v169）index 上行，新行為斷言會乾淨 FAIL，")
open(WORK + '/' + p, 'w', encoding='utf-8').write(txt)
print('tang171 寫好')
print('全部完成')
