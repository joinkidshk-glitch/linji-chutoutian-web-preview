# v20a193 resync：WF4 區插入淨 +179 行（36 新事件＋18 覆寫行＋註解／once 改動），
# 5 個行號釘測試純漂移。用法：python3 qa193/resync193.py
# 以 difflib 對位 pristine main b3db32f 同工作版 index.html，逐個釘行核實內容逐字相同。
import difflib, subprocess, sys

old = subprocess.check_output(['git', 'show', 'b3db32f:index.html'], cwd='/home/hatch/workspace/linji-work193').decode('utf-8').split('\n')
new = open('/home/hatch/workspace/linji-work193/index.html', encoding='utf-8').read().split('\n')
print('old lines:', len(old), 'new lines:', len(new), 'net:', len(new) - len(old))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-indexed
print('opcodes:', [(t, i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal'])

pins = {
    'rom176': [6070, 31574, 53369, 53737, 54876, 54970],
    'tang171/173 DEF': [54939],
    'tang173 L4862': [4887],
    'travel114 COUNT': [32175, 35671, 37798, 38877, 39311, 39314, 39345, 43900, 58999, 59177, 59320, 59341],
    'travel114 FREE': [24684, 28219, 30842, 30843, 30855, 30856, 30867, 30868, 30971, 40855, 43557, 43580,
                       53192, 53311, 53361, 53584, 53623, 53629, 53696, 53698, 53701, 53728, 54839, 55213,
                       55235, 55386, 57023, 58767, 58885, 58886, 58921, 58922, 58947, 59791],
    'travel114 DEF': [54939],
    'travel114 WRAPPER': [44387],
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
