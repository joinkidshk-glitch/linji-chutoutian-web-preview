# v384 resync: index.html net +40 lines (EVAL6 P2: CSS +2 @~4225, lockShoots sort +3,
# defaultWeekPlan peak +5, detail row +7, teaser pill same-line, intel381DeadlineText +1,
# tape383DeadlineShortText +4, openLoc note +16, HE notes same-line). Pins updated by
# difflib mapping (old -> new), single-pass dict lookup.
import json, re

mapping = {int(k): v for k, v in json.load(open('/tmp/linemap384.json')).items()}

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
t = remap(t, [26821, 9038, 27729, 11208, 15477, 27584], 'rom159')
assert mapping[26849] == 26867, mapping[26849]
t = t.replace('idx_lines[26849 - 1]', 'idx_lines[26867 - 1]')
print('rom159: 全佳行 26849 -> 26867')
save(p, t)

# --- rom176: line() pins ---
p = 'tests/test_rom176_static.py'
t = load(p)
t = remap(t, [7169, 15475, 42399, 42758, 44315, 44476], 'rom176')
save(p, t)

# --- tang152: lines()[idx] 0-based -> line idx+1 mapped, back to idx ---
p = 'tests/test_tang152_static.py'
t = load(p)
for idx in [15404, 15529]:
    new_idx = mapping[idx + 1] - 1
    t = t.replace(f'lines()[{idx}]', f'lines()[{new_idx}]')
    print(f'tang152: lines()[{idx}] -> lines()[{new_idx}]')
save(p, t)

# --- text125: len(ls) < N and ls[N-1] pairs ---
p = 'tests/test_text125_static.py'
t = load(p)
for ln in [11788, 11930, 17091]:
    new_ln = mapping[ln]
    t = t.replace(f'len(ls) < {ln} or', f'len(ls) < {new_ln} or')
    t = t.replace(f'ls[{ln - 1}]', f'ls[{new_ln - 1}]')
    print(f'text125: {ln} -> {new_ln}')
save(p, t)

# --- travel114: list entries + DEF/WRAPPER (no new openLoc call sites in v384) ---
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
t = '\n'.join(out)
save(p, t)
print(f'travel114: {cnt} remapped')

# --- gift185/tang171/tang173: total 49282 -> 49322, openLoc 44435 -> 44458, chain append ---
for p in ['tests/test_gift185_static.py', 'tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    t = load(p)
    t = t.replace("＋v382 +99＋v383 +163）', src.count('\\n') == 49282)", "＋v382 +99＋v383 +163＋v384 +40）', src.count('\\n') == 49322)")
    t = t.replace("＋v382 +99＋v383 +163）', html.count('\\n') == 49282)", "＋v382 +99＋v383 +163＋v384 +40）', html.count('\\n') == 49322)")
    t = t.replace('總行數 49282（', '總行數 49322（')
    t = t.replace("＋v382 +99＋v383 +163，travel114 釘行）',\n   len(lines) >= 44435 and 'function openLoc(id, opts){' in lines[44434])",
                  "＋v382 +99＋v383 +163＋v384 +40，travel114 釘行）',\n   len(lines) >= 44458 and 'function openLoc(id, opts){' in lines[44457])")
    t = t.replace('openLoc DEF 行 44435（', 'openLoc DEF 行 44458（')
    save(p, t)
    print(f'{p}: total/openLoc updated')

# --- tang173 L4872 label: actual pin lines[5227] (0-based, line 5228) + len>=5214; CSS +2 before it ---
p = 'tests/test_tang173_static.py'
t = load(p)
assert mapping[5228] == 5230, mapping[5228]
t = t.replace('lines[5227]', 'lines[5229]')
t = t.replace('len(lines) >= 5214', 'len(lines) >= 5216')
save(p, t)
print('tang173: lines[5227] -> lines[5229], len 5214 -> 5216')
