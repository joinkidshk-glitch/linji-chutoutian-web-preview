# v20a203 resync：WF4 區插入淨 +233 行（迎新期 CFG＋helpers＋41 新事件＋7 覆寫行＋C3 閘＋測試更新），
# 5 個行號釘測試純漂移。用法：python3 qa203/resync203.py
# 以 difflib 對位 pristine main 6e45cdb（/tmp/pristine203.html）同工作版 index.html，
# 逐個釘行核實內容逐字相同。
import difflib, sys

old = open('/tmp/pristine203.html', encoding='utf-8').read().split('\n')
new = open('/home/hatch/workspace/linji-work203/index.html', encoding='utf-8').read().split('\n')
print('old lines:', len(old), 'new lines:', len(new), 'net:', len(new) - len(old))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-indexed
print('opcodes:', [(t, i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal'])

pins = {
    'rom176': [6134, 31695, 54069, 54437, 55576, 55670],
    'tang171/173 DEF': [55639],
    'travel114 COUNT': [32296, 35795, 37946, 39100, 39532, 39535, 39566, 44333, 59720, 59898, 60044, 60065],
    'travel114 FREE': [24748, 30963, 30964, 30976, 30977, 30988, 30989, 31092, 41276, 43990, 44013, 53892,
                       54011, 54061, 54284, 54323, 54329, 54396, 54398, 54401, 54428, 55539, 55913,
                       55935, 56086, 57723, 59488, 59606, 59607, 59642, 59643, 59668, 60515],
    'travel114 DEF': [55639],
    'travel114 WRAPPER': [44902],
}
bad = []
for group, nums in pins.items():
    for n in nums:
        m = mapping.get(n)
        same = (m is not None and old[n - 1] == new[m - 1])
        print(f'{group:20s} old {n} -> new {m} {"SAME" if same else "DIFF!!"}  {old[n-1].strip()[:70]}')
        if not same:
            bad.append((group, n, m))
print('BAD:', bad if bad else 'none — 全部純漂移')
sys.exit(1 if bad else 0)
