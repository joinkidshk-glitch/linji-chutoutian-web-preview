# v388 resync: index.html net +18 lines (lockShootsIntoDraft 填位唔跨限期 +18 @~old L20250;
# CSS L807/L5235 同殺青結算四處查 gig 係同行改，零行數變化).
# Pins updated by difflib mapping (old -> new), single-pass dict lookup.
import json, re

mapping = {int(k): v for k, v in json.load(open('/tmp/linemap388.json')).items()}

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
t = remap(t, [26899, 27807, 27662, 26927], 'rom159')
save(p, t)

# --- rom176: line() pins ---
p = 'tests/test_rom176_static.py'
t = load(p)
t = remap(t, [42477, 42836, 44402, 44563], 'rom176')
save(p, t)

# --- travel114: COUNT/FREE set literals + DEF/WRAPPER ---
p = 'tests/test_travel114_static.py'
t = load(p)
for setname in ['COUNT_LINES', 'FREE_LINES']:
    m = re.search(setname + r' = \{.*?\n\}', t, re.S)
    assert m, setname
    span = m.group(0)
    nums = sorted({int(x) for x in re.findall(r'\b\d{4,5}\b', span)})
    newspan = remap(span, nums, 'travel114 ' + setname)
    t = t[:m.start()] + newspan + t[m.end():]
t = remap(t, [44522, 30710], 'travel114 DEF/WRAPPER')
save(p, t)

# --- gift185: 總行數鏈 ---
p = 'tests/test_gift185_static.py'
t = load(p)
assert t.count('49386') == 2, t.count('49386')
t = t.replace('49386', '49404')
assert '＋v387 +4）' in t
t = t.replace('＋v387 +4）', '＋v387 +4＋v388 +18）')
save(p, t)
print('gift185: count chain done')

# --- tang171 / tang173: 總行數鏈 + openLoc DEF ---
for p in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    t = load(p)
    assert t.count('49386') == 2, (p, t.count('49386'))
    t = t.replace('49386', '49404')
    assert '＋v387 +4）' in t, p
    t = t.replace('＋v387 +4）', '＋v387 +4＋v388 +18）')
    assert '＋v387 +4，travel114 釘行）' in t, p
    t = t.replace('＋v387 +4，travel114 釘行）', '＋v387 +4＋v388 +18，travel114 釘行）')
    t = remap(t, [44522, 44521], p + ' DEF')
    save(p, t)
    print(p + ': done')

print('resync388 complete')
