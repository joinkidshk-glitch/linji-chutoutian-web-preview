# v386 resync: index.html net +40 lines (EVAL7 fixes: endingRomance410 BE-override +4,
# ux68OrganizeLocSheet keep-notes +5, costume382 static-trigger +6, placeShootOnPlan rest-last +7,
# previewShootPlacement sort +2, defaultWeekPlan locked-preview +12, endingRomanceState48 +1,
# intel381 expiredFrom +4 (tick 2 same-line + openBook +3 -1), 餘為同行改寫).
# Pins updated by difflib mapping (old -> new), single-pass dict lookup.
import json, re

mapping = {int(k): v for k, v in json.load(open('/tmp/linemap386.json')).items()}

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
t = remap(t, [26859, 27767, 15499, 27622], 'rom159')
assert mapping[26887] == 26923, mapping[26887]
t = t.replace('idx_lines[26887 - 1]', 'idx_lines[26923 - 1]')
print('rom159: 全佳行 26887 -> 26923')
save(p, t)

# --- rom176: line() pins ---
p = 'tests/test_rom176_static.py'
t = load(p)
t = remap(t, [15497, 42437, 42796, 44358, 44519], 'rom176')
save(p, t)

# --- tang152: lines()[idx] 0-based -> line idx+1 mapped, back to idx ---
p = 'tests/test_tang152_static.py'
t = load(p)
for idx in [15426, 15551]:
    new_idx = mapping[idx + 1] - 1
    t = t.replace(f'lines()[{idx}]', f'lines()[{new_idx}]')
    print(f'tang152: lines()[{idx}] -> lines()[{new_idx}]')
save(p, t)

# --- text125: len(ls) < N and ls[N-1] pairs ---
p = 'tests/test_text125_static.py'
t = load(p)
for ln in [17113]:
    new_ln = mapping[ln]
    t = t.replace(f'len(ls) < {ln} or', f'len(ls) < {new_ln} or')
    t = t.replace(f'ls[{ln - 1}]', f'ls[{new_ln - 1}]')
    print(f'text125: {ln} -> {new_ln}')
save(p, t)

# --- gift185 / tang171 / tang173: 總行數 ledger + openLoc DEF ---
for p in ['tests/test_gift185_static.py', 'tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    t = load(p)
    t = t.replace('49342', '49382')
    t = t.replace('v385 +20）', 'v385 +20＋v386 +40）')
    t = t.replace('v385 +20，travel114 釘行）', 'v385 +20＋v386 +40，travel114 釘行）')
    save(p, t)
    print(p + ': ledger 49342->49382 +v386 +40')
for p in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    t = load(p)
    assert mapping[44478] == 44518, mapping[44478]
    t = t.replace('openLoc DEF 行 44478', 'openLoc DEF 行 44518')
    save(p, t)
    print(p + ': openLoc DEF 44478 -> 44518')

# --- travel114: COUNT_LINES / FREE_LINES sets + DEF/WRAPPER ---
p = 'tests/test_travel114_static.py'
t = load(p)
def remap_block(text, start_marker, end_marker, label):
    i = text.index(start_marker)
    j = text.index(end_marker, i)
    block = text[i:j]
    def sub(m):
        old = int(m.group(1))
        new = mapping.get(old)
        if new is None:
            print(f'  !! {label}: {old} UNMAPPED')
            return m.group(1)
        return str(new)
    new_block, n = re.subn(r'\b(\d{4,5})\b', sub, block)
    print(f'{label}: {n} replacements')
    return text[:i] + new_block + text[j:]
t = remap_block(t, 'COUNT_LINES = {', '}\n', 'travel114 COUNT')
t = remap_block(t, 'FREE_LINES = {', '}\n', 'travel114 FREE')
t = t.replace('DEF_LINE = 44478', 'DEF_LINE = 44518')
t = t.replace('WRAPPER_LINE = 30670', 'WRAPPER_LINE = 30706')
print('travel114: DEF 44478->44518 WRAPPER 30670->30706')
save(p, t)

print('resync386 done')
