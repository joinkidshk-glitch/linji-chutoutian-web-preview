# v361 resync：difflib 映射舊行號→新行號，逐行核實內容逐字相同（純漂移先准改釘）
# 用法：python3 qa361/resync361.py <old_line_1based> [<old_line> ...]
# 輸出：old -> new（內容核實 OK/DIFF）
import difflib, subprocess, sys

old = subprocess.check_output(['git', 'show', 'HEAD:index.html']).decode('utf-8').splitlines()
new = open('index.html', encoding='utf-8').read().splitlines()
print(f'old lines={len(old)} new lines={len(new)} net={len(new)-len(old):+d}')

sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based

for arg in sys.argv[1:]:
    o = int(arg)
    n = mapping.get(o)
    if n is None:
        print(f'{o} -> UNMAPPED (line changed/deleted)')
    else:
        same = old[o - 1] == new[n - 1]
        print(f'{o} -> {n} ({"OK" if same else "DIFF"}) | {old[o-1][:80]}')
