# v385 resync: index.html net +20 lines (SCHED385 CSS block @~L6658).
# Pins updated by difflib mapping (old -> new), single-pass dict lookup.
import json, re

mapping = {int(k): v for k, v in json.load(open('/tmp/linemap385.json')).items()}

def remap(text, nums, label):
    pat = re.compile(r'\b(' + '|'.join(str(n) for n in nums) + r')\b')
    def sub(m):
        old = int(m.group(1))
        new = mapping.get(old)
        if new is None:
            print(f'  !! {label}: {old} UNMAPPED')
            return m.group(1)
        return str(new)
    out, n = pat.subn(sub, text)
    print(f'{label}: {n} replacements')
    return out

def load(p): return open(p, encoding='utf-8').read()
def save(p, t): open(p, 'w', encoding='utf-8').write(t)

# --- rom159: line_has pins + 全佳行 ---
p = 'tests/test_rom159_static.py'
t = load(p)
t = remap(t, [26839, 9040, 27747, 11210, 15479, 27602], 'rom159')
# 全佳行 idx_lines[N - 1]
m = re.search(r'idx_lines\[(\d+) - 1\]', t)
if m:
    old = int(m.group(1)); new = mapping[old]
    t = t.replace(f'idx_lines[{old} - 1]', f'idx_lines[{new} - 1]')
    print(f'rom159: 全佳行 {old} -> {new}')
save(p, t)

# --- rom176: line() pins (labels L6152 etc are historical, numbers in line() only) ---
p = 'tests/test_rom176_static.py'
t = load(p)
# only remap inside line(N) calls to avoid touching labels/comments
def sub_line(m):
    old = int(m.group(1)); new = mapping.get(old, old)
    return f'line({new})'
t2, n = re.subn(r'line\((\d+)\)', sub_line, t)
print(f'rom176: {n} line() remapped')
save(p, t2)

# --- tang152: lines()[idx] 0-based ---
p = 'tests/test_tang152_static.py'
t = load(p)
for idx in [15406, 15531]:
    new_idx = mapping[idx + 1] - 1
    t = t.replace(f'lines()[{idx}]', f'lines()[{new_idx}]')
    print(f'tang152: lines()[{idx}] -> lines()[{new_idx}]')
save(p, t)

# --- text125: len(ls) < N and ls[N-1] pairs ---
p = 'tests/test_text125_static.py'
t = load(p)
for m in list(re.finditer(r'len\(ls\) < (\d+) or', t)):
    ln = int(m.group(1)); new_ln = mapping.get(ln)
    if new_ln and new_ln != ln:
        t = t.replace(f'len(ls) < {ln} or', f'len(ls) < {new_ln} or')
        t = t.replace(f'ls[{ln - 1}]', f'ls[{new_ln - 1}]')
        print(f'text125: {ln} -> {new_ln}')
save(p, t)

# --- travel114: list entries + DEF/WRAPPER ---
p = 'tests/test_travel114_static.py'
lines = load(p).split('\n')
out = []
cnt = 0
for ln in lines:
    m = re.match(r'^(\s*)(\d{4,5})(,.*)$', ln)
    if m:
        new = mapping.get(int(m.group(2)))
        if new:
            out.append(m.group(1) + str(new) + m.group(3)); cnt += 1; continue
    m2 = re.match(r'^(DEF_LINE = )(\d{5})(\s.*)$', ln) or re.match(r'^(WRAPPER_LINE = )(\d{5})(\s.*)$', ln)
    if m2:
        out.append(m2.group(1) + str(mapping[int(m2.group(2))]) + m2.group(3)); cnt += 1; continue
    out.append(ln)
save(p, '\n'.join(out))
print(f'travel114: {cnt} remapped')

# --- gift185/tang171/tang173: total 49322 -> 49342, openLoc 44458 -> 44478 ---
for p in ['tests/test_gift185_static.py', 'tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    t = load(p)
    t = t.replace("＋v384 +40）', src.count('\\n') == 49322)", "＋v384 +40＋v385 +20）', src.count('\\n') == 49342)")
    t = t.replace("＋v384 +40）', html.count('\\n') == 49322)", "＋v384 +40＋v385 +20）', html.count('\\n') == 49342)")
    t = t.replace('總行數 49322（', '總行數 49342（')
    t = t.replace("＋v384 +40，travel114 釘行）',\n   len(lines) >= 44458 and 'function openLoc(id, opts){' in lines[44457])",
                  "＋v384 +40＋v385 +20，travel114 釘行）',\n   len(lines) >= 44478 and 'function openLoc(id, opts){' in lines[44477])")
    t = t.replace('openLoc DEF 行 44458（', 'openLoc DEF 行 44478（')
    save(p, t)
    print(f'{p}: total/openLoc updated')
