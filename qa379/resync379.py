# v379 resync: index.html net +50 lines (defaultWeekPlan stress +7 @~20058,
# deCollideLabels363 tag obstacle +19 @~23154, rom159DateScene portrait +13 @~27324,
# awards379GapBand +10 @~33163, gift cap line +4 @~47178; same-line edits elsewhere).
# Pins updated by difflib mapping (old -> new), single-pass dict lookup.
import json, re

mapping = {int(k): v for k, v in json.load(open('/tmp/linemap379.json')).items()}

def remap(text, nums, label):
    """Replace each number in nums (as standalone token) with mapped value, single pass."""
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

# --- rom176: line(42164), line(42516), line(43819), line(43980) ---
p = 'tests/test_rom176_static.py'
t = load(p)
t = remap(t, [42164, 42516, 43819, 43980], 'rom176')
save(p, t)

# --- rom159: line_has(26639), line_has(27535), line_has(27390), idx_lines[26667-1] ---
p = 'tests/test_rom159_static.py'
t = load(p)
t = remap(t, [26639, 27535, 27390, 26667], 'rom159')
save(p, t)

# --- travel114: all COUNT/FREE list entries + DEF/WRAPPER constants ---
# (run on the pristine v378 copy of the file; list-entry lines only, so chain
#  deltas like -15612 in comments are untouched)
p = 'tests/test_travel114_static.py'
lines = load(p).split('\n')
out = []
for ln in lines:
    m = re.match(r'^(\s*)(\d{5})(,.*)$', ln)
    if m:
        new = mapping.get(int(m.group(2)))
        out.append(m.group(1) + str(new) + m.group(3) if new else ln)
        continue
    m2 = re.match(r'^(DEF_LINE = )(\d{5})(\s.*)$', ln) or re.match(r'^(WRAPPER_LINE = )(\d{5})(\s.*)$', ln)
    if m2:
        out.append(m2.group(1) + str(mapping[int(m2.group(2))]) + m2.group(3))
        continue
    out.append(ln)
save(p, '\n'.join(out))
print('travel114: list entries + DEF/WRAPPER remapped')

# --- tang171/tang173/gift185: total 48773 -> 48823 (count('\n')), openLoc 43939 -> 43985 ---
for p in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py', 'tests/test_gift185_static.py']:
    t = load(p)
    t = t.replace("count('\\n') == 48773", "count('\\n') == 48823")
    t = t.replace("總行數 48773（", "總行數 48823（")
    t = t.replace("＋v378 +134）", "＋v378 +134＋v379 +50）")
    save(p, t)
    print(p, 'total updated')
for p in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    t = load(p)
    t = remap(t, [43939, 43938], p + ' openLoc')
    t = t.replace("＋v378 +98，travel114 釘行）", "＋v378 +98＋v379 +46，travel114 釘行）")
    save(p, t)
    print(p, 'openLoc updated')

# --- awards212: preview opacity pin .22 -> .38 ---
p = 'tests/test_awards212_static.py'
t = load(p)
t = t.replace("'opacity:.22' in src", "'opacity:.38' in src")
t = t.replace("dimmed 0.22", "dimmed 0.38")
save(p, t)
print(p, 'opacity pin updated')

# --- stamina58: WEEK_LOW_STA fallback sentence now mentions fame drop ---
p = 'tests/test_stamina58_static.py'
t = load(p)
t = t.replace("'體能見底，宜減輕通告。' in src", "'體能見底，聲望下跌，宜減輕通告。' in src")
save(p, t)
print(p, 'low-sta sentence pin updated')

print('done')
