# v20a218 resync：index.html 淨 +136 行（工作副本 vs main v217，e54d9a1），
# 總行數 62758→62894、openLoc DEF 57230→57350（＋120；其餘 +16 行加喺 DEF 之後：
# chk101 1→11 @60975（+10）、＋6 @62356（+6））。
# 用法：python3 qa218/resync218.py
# difflib 對位核實純漂移：插入 235 行、刪除 99 行、淨 +136；
# DEF 之前各 hunk 淨加總和 +120，啱啱等於 DEF 行位移（57350-57230），
# DEF 之後淨加 +16，120+16=136。DEF 行內容逐字相同。
import difflib
import json
import subprocess
import sys

ROOT = '/home/hatch/workspace/linji-repo'
old = subprocess.check_output(['git', 'show', 'main:index.html'], cwd=ROOT).decode('utf-8').splitlines()
new = open(f'{ROOT}/index.html', encoding='utf-8').read().splitlines()
print('old lines:', len(old), 'new lines:', len(new), 'net:', len(new) - len(old))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
adds = dels = 0
before_def = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'insert':
        adds += (j2 - j1)
        if i1 < 57230:
            before_def += (j2 - j1)
    elif tag == 'delete':
        dels += (i2 - i1)
        if i1 < 57230:
            before_def -= (i2 - i1)
    elif tag == 'replace':
        adds += (j2 - j1)
        dels += (i2 - i1)
        if i1 < 57230:
            before_def += (j2 - j1) - (i2 - i1)
print('inserted:', adds, 'deleted:', dels, 'net check:', adds - dels)
print('net before openLoc DEF (old L57230):', before_def)

def find(lines, pat):
    for i, l in enumerate(lines, 1):
        if pat in l:
            return i
    return None

o = find(old, 'function openLoc(id, opts){')
n = find(new, 'function openLoc(id, opts){')
print('openLoc old:', o, 'new:', n, 'shift:', n - o)
assert len(old) == 62758 and len(new) == 62894, '總行數唔啱'
assert o == 57230 and n == 57350, 'DEF 行唔啱'
assert before_def == n - o, 'DEF 之前淨加唔等於 DEF 位移'
assert old[o - 1] == new[n - 1], 'DEF 行內容唔同'
assert adds - dels == 136, '淨加唔係 +136'
mapping = {'total_lines': [62758, 62894], 'openLoc_def': [57230, 57350]}
with open(f'{ROOT}/qa218/resync218_map.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, ensure_ascii=False, indent=2)
print('RESYNC218 OK — 純漂移核實通過')
