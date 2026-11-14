# -*- coding: utf-8 -*-
"""v20a206 C2 resync 核實：index.html 淨 +3 行（WF4 覆寫表頭註解）＋9 行原位換圖，係純漂移。
插入點（舊行號，基底 b25c6d0＝C1 commit）：表頭註解＋3（舊 L41271 之後）；
9 行重映射原位替換（淨 0，舊 L41293–41315 一帶）。其餘全部 equal。
核實兩樣：① difflib opcodes 除咗呢兩段之外全部 equal，淨變 +3；
② 全部釘位（舊行號 → 舊＋3 若舊行＞41271，否則唔郁）內容逐字相同。
釘位來源：C1 resync206.py 53 處（60f16b5 座標，先按 C1 規則＋22 換算做 b25c6d0 座標）
＋5 份受影響測試嘅釘行（gift185 總行數／rom176 4 處／tang171・173 DEF／travel114 COUNT＋FREE＋DEF＋WRAPPER）。
用法：python3 qa206/resync206c2.py
"""
import difflib, subprocess

ROOT = '/home/hatch/workspace/linji-work206'
OLD = subprocess.check_output(['git', 'show', 'b25c6d0:index.html'], cwd=ROOT, text=True).split('\n')
NEW = open(ROOT + '/index.html', encoding='utf-8').read().split('\n')
print('舊總行數（\\n 計）：%d；新總行數：%d；淨變：%+d' % (len(OLD) - 1, len(NEW) - 1, len(NEW) - len(OLD)))
assert len(OLD) - 1 == 61422, '舊總行數唔係 61422'
assert len(NEW) - 1 == 61425, '新總行數唔係 61425'

sm = difflib.SequenceMatcher(None, OLD, NEW, autojunk=False)
ops = sm.get_opcodes()
net = 0
bad = []
for tag, i1, i2, j1, j2 in ops:
    if tag == 'equal':
        continue
    net += (j2 - j1) - (i2 - i1)
    # 全部非 equal 段都要喺舊 L41269–41322 之內（表頭註解＋覆寫表）
    if i1 + 1 < 41269 or i2 > 41322:
        bad.append((tag, i1 + 1, i2, j1 + 1, j2))
    print('  %s 舊 L%d–%d → 新 L%d–%d（淨 %+d）' % (tag, i1 + 1, i2, j1 + 1, j2, (j2 - j1) - (i2 - i1)))
print('淨變（opcodes）：%+d' % net)
assert net == 3, '淨變唔係 +3'
assert not bad, '有改動喺表頭／覆寫表範圍之外：%r' % bad

# 釘位對位：舊行號 → 新行號（舊行 ≤41271 唔郁，其餘 +3），內容逐字相同
PINS_60F = [6134, 31695, 32296, 35795, 37946, 39116, 39548, 39551, 39582, 24748,
            30963, 30964, 30976, 30977, 30988, 30989, 31092,
            41509, 44223, 44246, 44566, 45135, 54125, 54244, 54294, 54302, 54517,
            54556, 54562, 54629, 54631, 54634, 54661, 54670, 55772, 55809, 55872,
            55903, 56146, 56168, 56319, 57956, 59721, 59839, 59840, 59875, 59876,
            59901, 59953, 60131, 60277, 60298, 60748]
PINS_B25 = [p + (22 if p >= 41126 else 0) for p in PINS_60F]
PINS_B25 += [54324, 54692, 55831, 55925, 55894, 45157,  # rom176 4 處＋tang DEF＋travel WRAPPER
             44588, 59975, 60153, 60299, 60320,        # travel114 COUNT_LINES（＞41271 者）
             41531, 44245, 44268, 54147, 54266, 54316, 54539, 54578, 54584,
             54651, 54653, 54656, 54683, 55794, 56168, 56190, 56341, 57978,
             59743, 59861, 59862, 59897, 59898, 59923, 60770]  # travel114 FREE_LINES（＞41271 者）
PINS_B25 = sorted(set(PINS_B25))
fails = []
for old_ln in PINS_B25:
    shift = 0 if old_ln <= 41271 else 3
    new_ln = old_ln + shift
    o, n = OLD[old_ln - 1], NEW[new_ln - 1]
    if o != n:
        fails.append((old_ln, new_ln, o[:60], n[:60]))
print('釘位核實：%d 處，%d 處內容唔同' % (len(PINS_B25), len(fails)))
for f in fails:
    print('  MISMATCH 舊 L%d → 新 L%d：%r vs %r' % f)
assert not fails

# scene104 計數核實：?v=20a104 26→29（WF4 覆寫表重用 10→13）
old_n = sum(1 for ln in OLD if '?v=20a104' in ln)
new_n = sum(1 for ln in NEW if '?v=20a104' in ln)
print('?v=20a104：舊 %d 處 → 新 %d 處' % (old_n, new_n))
assert (old_n, new_n) == (26, 29), '20a104 計數唔係 26→29'
print('RESYNC206C2 PASS：全部釘位純漂移，+3')
