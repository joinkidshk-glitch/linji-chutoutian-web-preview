# -*- coding: utf-8 -*-
"""v20a206 C1 resync 核實：index.html 淨 +22 行（WF4 保底）係純漂移。
插入點（舊行號）：WF4 區頭註解＋3（L41126–41133 一帶）、wf4SeenAny ＋10
（wf4DailyTick 之前）、wf4DailyTick 內保底檢查 ＋9——全部喺舊 L41497 之前。
核實兩樣：① difflib opcodes 除咗呢三段之外全部 equal，淨變 +22；
② 全部釘位（舊行號 → 舊＋22，＜41126 者唔郁）內容逐字相同。
用法：python3 qa206/resync206.py
"""
import difflib, subprocess, sys

OLD = subprocess.check_output(['git', 'show', '60f16b5:index.html'],
                              cwd='/home/hatch/workspace/linji-work206',
                              text=True).split('\n')
NEW = open('/home/hatch/workspace/linji-work206/index.html', encoding='utf-8').read().split('\n')
print('舊總行數（\\n 計）：%d；新總行數：%d；淨變：%+d' % (len(OLD) - 1, len(NEW) - 1, len(NEW) - len(OLD)))
assert len(OLD) - 1 == 61400, '舊總行數唔係 61400'
assert len(NEW) - 1 == 61422, '新總行數唔係 61422'

sm = difflib.SequenceMatcher(None, OLD, NEW, autojunk=False)
ops = sm.get_opcodes()
net = 0
bad = []
for tag, i1, i2, j1, j2 in ops:
    if tag == 'equal':
        continue
    net += (j2 - j1) - (i2 - i1)
    # 全部非 equal 段都要喺舊 L41497 之前（插入點上限）
    if i2 > 41497:
        bad.append((tag, i1 + 1, i2, j1 + 1, j2))
    print('  %s 舊 L%d–%d → 新 L%d–%d（淨 %+d）' % (tag, i1 + 1, i2, j1 + 1, j2, (j2 - j1) - (i2 - i1)))
print('淨變（opcodes）：%+d' % net)
assert net == 22, '淨變唔係 +22'
assert not bad, '有改動喺 L41497 之後：%r' % bad

# 釘位對位：舊行號 → 新行號（＜41126 唔郁，其餘 +22），內容逐字相同
PINS = [6134, 31695, 32296, 35795, 37946, 39116, 39548, 39551, 39582, 24748,
        30963, 30964, 30976, 30977, 30988, 30989, 31092,
        41509, 44223, 44246, 44566, 45135, 54125, 54244, 54294, 54302, 54517,
        54556, 54562, 54629, 54631, 54634, 54661, 54670, 55772, 55809, 55872,
        55903, 56146, 56168, 56319, 57956, 59721, 59839, 59840, 59875, 59876,
        59901, 59953, 60131, 60277, 60298, 60748]
fails = []
for old_ln in PINS:
    shift = 0 if old_ln < 41126 else 22
    new_ln = old_ln + shift
    o, n = OLD[old_ln - 1], NEW[new_ln - 1]
    if o != n:
        fails.append((old_ln, new_ln, o[:60], n[:60]))
print('釘位核實：%d 處，%d 處內容唔同' % (len(PINS), len(fails)))
for f in fails:
    print('  MISMATCH 舊 L%d → 新 L%d：%r vs %r' % f)
assert not fails
print('RESYNC206 PASS：全部釘位純漂移，+22')
