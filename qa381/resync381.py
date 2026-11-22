# v381 resync: index.html net +164 lines (INTEL381 CSS +8 @~4212, home button +1 @~6906,
# wireHome265 +8, normalizeSaveObj +2, MOCK_ASK def +2, mockAskDefs +10, applyMockAsk +2,
# advanceDay tick +2, board exemption +3, card labels +4, INTEL381 module ~+122 @~43174;
# same-line edits elsewhere). Pins updated by difflib mapping (old -> new), single-pass dict lookup.
import json, re

mapping = {int(k): v for k, v in json.load(open('/tmp/linemap381.json')).items()}

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

def remap0(text, idxs, label):
    """0-based index pins: old idx i (line i+1) -> mapping[i+1]-1."""
    pat = re.compile(r'\b(' + '|'.join(str(n) for n in idxs) + r')\b')
    def sub(m):
        old = int(m.group(1))
        new = mapping.get(old + 1)
        if new is None:
            print(f'  !! {label}: idx {old} UNMAPPED')
            return m.group(1)
        return str(new - 1)
    out, n = pat.subn(sub, text)
    print(f'{label}: {n} replacements')
    return out

def load(p): return open(p, encoding='utf-8').read()
def save(p, t): open(p, 'w', encoding='utf-8').write(t)

# --- rom159: line_has pins (1-based) ---
p = 'tests/test_rom159_static.py'
t = load(p)
t = remap(t, [26675, 9014, 27583, 11184, 15453, 27438, 26703], 'rom159')
save(p, t)

# --- rom176: line() pins (1-based) ---
p = 'tests/test_rom176_static.py'
t = load(p)
t = remap(t, [7153, 15451, 42221, 42580, 43898, 44059], 'rom176')
save(p, t)

# --- text125: ls[idx] 0-based + len thresholds (1-based line numbers) ---
p = 'tests/test_text125_static.py'
t = load(p)
t = remap0(t, [11763, 11905, 17063], 'text125 idx')
t = remap(t, [11764, 11906, 17064], 'text125 len')
save(p, t)

# --- tang152: lines()[idx] 0-based ---
p = 'tests/test_tang152_static.py'
t = load(p)
t = remap0(t, [15380, 15505], 'tang152')
save(p, t)

# --- travel114: list entries + DEF/WRAPPER ---
p = 'tests/test_travel114_static.py'
lines = load(p).split('\n')
out = []
for ln in lines:
    m = re.match(r'^(\s*)(\d{4,5})(,.*)$', ln)
    if m:
        new = mapping.get(int(m.group(2)))
        out.append(m.group(1) + str(new) + m.group(3) if new else ln)
        continue
    m2 = re.match(r'^(DEF_LINE = )(\d{4,5})(\s.*)$', ln) or re.match(r'^(WRAPPER_LINE = )(\d{4,5})(\s.*)$', ln)
    if m2:
        out.append(m2.group(1) + str(mapping[int(m2.group(2))]) + m2.group(3))
        continue
    out.append(ln)
save(p, '\n'.join(out))
print('travel114: list entries + DEF/WRAPPER remapped')

# --- tang171/tang173/gift185: total 48856 -> 49020 (+164) ---
for p in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py', 'tests/test_gift185_static.py']:
    t = load(p)
    t = t.replace("count('\\n') == 48856", "count('\\n') == 49020")
    t = t.replace("總行數 48856（", "總行數 49020（")
    t = t.replace("＋v379 +50）", "＋v379 +50＋v381 +164）")
    save(p, t)
    print(p, 'total updated')
# openLoc DEF 44018 -> 44180 (+162 before openLoc)
for p in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    t = load(p)
    t = remap(t, [44018], p + ' openLoc len/label')
    t = remap0(t, [44017], p + ' openLoc idx')
    t = t.replace("＋v379 +46，travel114 釘行）", "＋v379 +46＋v381 +162，travel114 釘行）")
    save(p, t)
    print(p, 'openLoc updated')
# tang173 L4872 rule line idx 5212 (0-based)
p = 'tests/test_tang173_static.py'
t = load(p)
t = remap0(t, [5212], 'tang173 L4872 idx')
save(p, t)

print('done')
