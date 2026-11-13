# -*- coding: utf-8 -*-
"""v20a181 第二次 rebase 上 main 77603b3（v184）resync 驗證。
用法：python3 qa181/resync181_rebase2.py（喺工作副本跑，須已 rebase＋解衝突）。
做乜：difflib 對位 v181 舊合併態 index.html（a684522，60135 行）同 main
index.html（77603b3，60143 行）各自對合併後 index.html（60151 行），逐行核實
全部釘行內容逐字相同先認做純漂移；兩個基底映射必須一致；再掃描全部 52 個
openLoc( 呼叫點分類覆蓋。
輸出：每組錨點 old->new＋內容相同與否；最後 TOTAL。
"""
import difflib, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read().split('\n')

def mapping(old_lines):
    sm = difflib.SequenceMatcher(a=old_lines, b=NEW, autojunk=False)
    m = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                m[i1 + k + 1] = j1 + k + 1
    return m

def check(label, old_lines, m, pins):
    bad = 0
    out = []
    for p in pins:
        q = m.get(p)
        same = q is not None and old_lines[p - 1] == NEW[q - 1]
        out.append('%d->%s%s' % (p, q, '' if same else ' MISMATCH'))
        if not same:
            bad += 1
    print('%-26s %s' % (label, ' '.join(out)))
    return bad

def git_show(rev):
    return subprocess.check_output(['git', 'show', rev + ':index.html'],
                                   cwd=ROOT, text=True).split('\n')

old181 = git_show('a684522')
oldmain = git_show('77603b3')
m181 = mapping(old181)
mmain = mapping(oldmain)
print('lines: v181-old %d / main %d / merged %d (newlines %d)' %
      (len(old181), len(oldmain), len(NEW),
       open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read().count('\n')))
fails = 0
fails += check('kwan151 (old181)', old181, m181,
               [25621, 25962, 25965, 25966, 25967, 26010, 26229, 27175, 27208,
                30974, 30982, 30983, 31025])
fails += check('tang152 (old181)', old181, m181, [25792, 31476, 31620])
fails += check('tang173 L (old181)', old181, m181, [4862])
fails += check('text125 (old181)', old181, m181, [27711, 27840, 33534])
fails += check('DEF (old181)', old181, m181, [54631])
fails += check('WRAPPER (old181)', old181, m181, [44353])
fails += check('rom176 (old181)', old181, m181,
               [6045, 31549, 53061, 53429, 54568, 54662])
fails += check('rom176 (oldmain)', oldmain, mmain,
               [6032, 31536, 53069, 53437, 54576, 54670])
fails += check('travel114 COUNT (old181)', old181, m181,
               [32150, 35646, 37773, 38844, 39278, 39281, 39312, 43866,
                58691, 58869, 59012, 59033])
fails += check('travel114 COUNT (oldmain)', oldmain, mmain,
               [32137, 35633, 37760, 38831, 39265, 39268, 39299, 43853,
                58699, 58877, 59020, 59041])
fails += check('travel114 FREE (old181)', old181, m181,
               [24659, 28194, 30817, 30818, 30830, 30831, 30842, 30843, 30946,
                40821, 43523, 43546, 52884, 53003, 53053, 53276, 53315, 53321,
                53388, 53390, 53393, 53420, 54531, 54905, 54927, 55078, 56715,
                58459, 58577, 58578, 58613, 58614, 58639, 59483])
fails += check('travel114 FREE (oldmain)', oldmain, mmain,
               [24646, 28181, 30804, 30805, 30817, 30818, 30829, 30830, 30933,
                40808, 43510, 43533, 52892, 53011, 53061, 53284, 53323, 53329,
                53396, 53398, 53401, 53428, 54539, 54913, 54935, 55086, 56723,
                58467, 58585, 58586, 58621, 58622, 58647, 59491])
# --- 雙基底一致性：同一內容行，兩個映射必須指向同一新行 ---
for a, b in zip([6045, 31549, 53061, 53429, 54568, 54662],
                [6032, 31536, 53069, 53437, 54576, 54670]):
    if m181.get(a) != mmain.get(b):
        print('CROSS-MISMATCH rom176 %d->%s vs %d->%s' % (a, m181.get(a), b, mmain.get(b)))
        fails += 1
for a, b in zip([32150, 35646, 37773, 38844, 39278, 39281, 39312, 43866,
                 58691, 58869, 59012, 59033],
                [32137, 35633, 37760, 38831, 39265, 39268, 39299, 43853,
                 58699, 58877, 59020, 59041]):
    if m181.get(a) != mmain.get(b):
        print('CROSS-MISMATCH COUNT %d->%s vs %d->%s' % (a, m181.get(a), b, mmain.get(b)))
        fails += 1
for a, b in zip([24659, 28194, 30817, 30818, 30830, 30831, 30842, 30843, 30946,
                 40821, 43523, 43546, 52884, 53003, 53053, 53276, 53315, 53321,
                 53388, 53390, 53393, 53420, 54531, 54905, 54927, 55078, 56715,
                 58459, 58577, 58578, 58613, 58614, 58639, 59483],
                [24646, 28181, 30804, 30805, 30817, 30818, 30829, 30830, 30933,
                 40808, 43510, 43533, 52892, 53011, 53061, 53284, 53323, 53329,
                 53396, 53398, 53401, 53428, 54539, 54913, 54935, 55086, 56723,
                 58467, 58585, 58586, 58621, 58622, 58647, 59491]):
    if m181.get(a) != mmain.get(b):
        print('CROSS-MISMATCH FREE %d->%s vs %d->%s' % (a, m181.get(a), b, mmain.get(b)))
        fails += 1
# --- travel114 全掃描：52 個 openLoc( 呼叫點分類 ---
FREE_FLAGS = ("travelFree:true", "encDone:true", "forceRestore:true", "wf4Done:true")
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
s = src.find("function runSoftP0Checks(){")
d, j = 0, src.find("{", s)
for k in range(j, len(src)):
    if src[k] == "{":
        d += 1
    elif src[k] == "}":
        d -= 1
        if d == 0:
            j = k
            break
TS, TE = src[:s].count("\n") + 1, src[:j].count("\n") + 1
DEF = src[:src.find("function openLoc(id, opts){")].count("\n") + 1
n_free = n_count = n_other = 0
for ln, line in enumerate(NEW, 1):
    if "openLoc(" not in line:
        continue
    if ln == DEF or TS <= ln <= TE or "back176" in line:
        continue
    if "openLoc: function(id, opts){ openLoc(id, opts); }" in line:
        continue
    if any(f in line for f in FREE_FLAGS):
        n_free += 1
    else:
        n_count += 1
print('travel114 scan: FREE %d COUNT %d DEF %d (expect 34/12/54647)' % (n_free, n_count, DEF))
if (n_free, n_count, DEF) != (34, 12, 54647):
    fails += 1
print('TOTAL ' + ('FAIL (%d)' % fails if fails else 'PASS'))
sys.exit(1 if fails else 0)
