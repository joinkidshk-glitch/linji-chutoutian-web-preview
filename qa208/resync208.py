# v20a208 resync：頒獎禮逐格重設計（beats 多格化＋player 逐格重建＋__awards 暴露 2 行），
# index.html 淨 +223 行（插入點：__awards L47108 附近 ＋2；beats／night helpers L47510 附近 ＋~110；
# player 重構其後 ＋~111）。用法：python3 qa208/resync208.py
# 以 difflib 對位 pristine main a426947（/tmp/pristine208.html）同工作版 index.html，
# 逐個釘行核實內容逐字相同（純漂移）。
import difflib, sys

old = open('/tmp/pristine208.html', encoding='utf-8').read().split('\n')
new = open('/home/hatch/workspace/linji-work208/index.html', encoding='utf-8').read().split('\n')
print('old lines:', len(old), 'new lines:', len(new), 'net:', len(new) - len(old))
sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-indexed
print('non-equal opcodes:', [(t, i2 - i1, j2 - j1) for t, i1, i2, j1, j2 in sm.get_opcodes() if t != 'equal'])

pins = {
    'rom176': [54334, 54702, 55841, 55935],
    'tang171/173 DEF': [55904],
    'travel114 FREE': [24748, 30963, 30964, 30976, 30977, 30988, 30989, 31092, 41510, 44224, 44247,
                       54157, 54276, 54326, 54549, 54588, 54594, 54661, 54663, 54666, 54693,
                       55804, 56178, 56200, 56351, 57988, 59753, 59871, 59872, 59907, 59908, 59933, 60780],
    'travel114 COUNT': [32296, 35796, 37947, 39117, 39549, 39552, 39583, 44567, 59985, 60163, 60309, 60330],
    'travel114 DEF': [55904],
    'travel114 WRAPPER': [45136],
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
