# -*- coding: utf-8 -*-
"""v20a181 rebase 上 main 9640c6f（v183）resync 驗證。
用法：python3 qa181/resync181_rebase.py（喺工作副本跑，須已 rebase＋解衝突）。
做乜：difflib 對位 v181 基底 index.html（4c6f868，59442 行）同 main index.html
（9640c6f，60127 行）各自對合併後 index.html（60135 行），逐行核實全部釘行
內容逐字相同先認做純漂移；再掃描全部 52 個 openLoc( 呼叫點分類覆蓋。
輸出：每組錨點 old->new＋內容相同與否；最後 TOTAL。
"""
import difflib, json, os, sys

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
    for p in pins:
        q = m.get(p)
        same = q is not None and old_lines[p - 1] == NEW[q - 1]
        print('%-28s %6d -> %-6s same=%s' % (label, p, q, same))
        if not same:
            bad += 1
    return bad

fails = 0
# --- 基底對照：用 git show 抽出嚟嘅檔（開工嗰陣已存 /tmp/idx181.html、/tmp/idxmain.html；呢度直接讀 git） ---
import subprocess
def git_show(rev):
    return subprocess.check_output(['git', 'show', rev + ':index.html'],
                                   cwd=ROOT, text=True).split('\n')
old181 = git_show('4c6f868')
oldmain = git_show('9640c6f')
m181 = mapping(old181)
mmain = mapping(oldmain)
print('lines: v181 %d / main %d / merged %d (newlines %d)' %
      (len(old181), len(oldmain), len(NEW),
       open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read().count('\n')))
fails += check('kwan151', old181, m181,
               [25621, 25962, 25965, 25966, 25967, 26010, 26229, 27175, 27208,
                30974, 30982, 30983, 31025])
fails += check('tang152', old181, m181, [25781, 31464, 31608])
fails += check('tang173', old181, m181, [4858])
fails += check('text125', old181, m181, [27700, 27829, 33522])
fails += check('DEF', old181, m181, [53961])
fails += check('WRAPPER', old181, m181, [44341])
fails += check('travel114 COUNT/FREE (main)', oldmain, mmain,
               [32137, 35633, 37760, 38831, 39265, 39268, 39299, 43853,
                58683, 58861, 59004, 59025,
                24646, 28181, 30804, 30805, 30817, 30818, 30829, 30830, 30933,
                40808, 43510, 43533, 52876, 52995, 53045, 53268, 53307, 53313,
                53380, 53382, 53385, 53412, 54523, 54897, 54919, 55070, 56707,
                58451, 58569, 58570, 58605, 58606, 58631, 59475])
fails += check('rom176 pins (main)', oldmain, mmain,
               [6032, 31536, 53053, 53421, 54560, 54654])
# --- travel114 全掃描：52 個 openLoc( 呼叫點分類 ---
FREE_FLAGS = ("travelFree:true", "encDone:true", "forceRestore:true", "wf4Done:true")
src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
s = src.find("function runSoftP0Checks(){")
d, j = 0, src.find("{", s)
for k in range(j, len(src)):
    if src[k] == "{": d += 1
    elif src[k] == "}":
        d -= 1
        if d == 0: j = k; break
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
print('travel114 scan: FREE %d COUNT %d DEF %d (expect 34/12/54631)' % (n_free, n_count, DEF))
if (n_free, n_count, DEF) != (34, 12, 54631):
    fails += 1
print('TOTAL ' + ('FAIL (%d)' % fails if fails else 'PASS'))
sys.exit(1 if fails else 0)
