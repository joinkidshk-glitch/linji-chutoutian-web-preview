# v20a213 resync：請柬提前 3 日＋典禮改晚上播（awards213 block＋晨鏈勾＋
# resolvePlannedDay nextNb 包裝＋presentAwardInvite 預約分流＋報紙 override＋
# 閘句日期化＋__awards 暴露），index.html 淨 +199 行（插入點：晨鏈 ~L38277／
# resolvePlannedDay ~L38600／v213 block ~L46800／presentAwardInvite ~L46991／
# gate 行 ~L47375／enqueueNewspaperFromAward ~L49131）。用法：python3 qa213/resync213.py
# 以 difflib 對位 pristine main f58f19c（/tmp/pristine213.html）同工作版 index.html，
# 逐個釘行核實內容逐字相同（純漂移）。
import difflib, sys

old = open('/tmp/pristine213.html', encoding='utf-8').read().split('\n')
new = open('/home/hatch/workspace/linji-work213/index.html', encoding='utf-8').read().split('\n')
print('old lines:', len(old), 'new lines:', len(new), 'net:', len(new) - len(old))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-indexed
print('non-equal opcodes:', [(t, i1 + 1, i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal'])

pins = {
    'travel114 COUNT': [32313, 35813, 37964, 39134, 39566, 39569, 39600, 44611, 60267, 60445, 60591, 60612],
    'travel114 FREE': [24765, 30980, 30981, 30993, 30994, 31005, 31006, 31109, 41554, 44268, 44291,
                       54439, 54558, 54608, 54831, 54870, 54876, 54943, 54945, 54948, 54975,
                       56086, 56460, 56482, 56633, 58270, 60035, 60153, 60154, 60189, 60190,
                       60215, 61062],
    'travel114 DEF': [56186],
    'travel114 WRAPPER': [45180],
    'rom176': [54616, 54984, 56123, 56217],
    'tang DEF': [56186],
}
bad = []
for group, nums in pins.items():
    for n in nums:
        m = mapping.get(n)
        same = (m is not None and old[n - 1] == new[m - 1])
        print(f'{group:18s} old {n} -> new {m} {"SAME" if same else "DIFF!!"}  {old[n-1].strip()[:70]}')
        if not same:
            bad.append((group, n, m))
print('BAD:', bad if bad else 'none — 全部純漂移')
sys.exit(1 if bad else 0)
