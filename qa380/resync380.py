# v380 resync: index.html net +33 lines (ending410-scene CSS +5 @~4106,
# NPCS yip/so +5 @~7150, ROM176 yip/so +5 @~42220, NL176 yip/so +16 @~42700,
# PORTRAITS +2; same-line edits elsewhere).
# Pins updated by difflib mapping (old -> new), single-pass dict lookup.
import json, re, hashlib

mapping = {int(k): v for k, v in json.load(open('/tmp/linemap380.json')).items()}

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

# --- rom159: line_has pins + 全佳 idx_lines[26692-1] ---
p = 'tests/test_rom159_static.py'
t = load(p)
t = remap(t, [26664, 9004, 27572, 11174, 15443, 27427, 26692], 'rom159')
# WOMEN npcId assertion: yip/so now have npcId (v380 P1-2)
t = t.replace(
    'ok("WOMEN yip／so npcId null", \'"yip"\' in _women and "yip" in _women and _women.count("npcId:null") >= 2)',
    'ok("WOMEN yip／so npcId 已補（v380 P1-2）", \'npcId:"yip"\' in _women and \'npcId:"so"\' in _women and "npcId:null" not in _women)')
save(p, t)

# --- rom176: line() pins ---
p = 'tests/test_rom176_static.py'
t = load(p)
t = remap(t, [7148, 15441, 42210, 42562, 43865, 44026], 'rom176')
save(p, t)

# --- tang152: lines()[N] 0-indexed pins ---
p = 'tests/test_tang152_static.py'
t = load(p)
for old0 in [15370, 15495]:
    new0 = mapping[old0 + 1] - 1
    t = t.replace(f'lines()[{old0}]', f'lines()[{new0}]')
    print(f'tang152: lines()[{old0}] -> lines()[{new0}]')
save(p, t)

# --- text125: 1-indexed line pins in checker messages + lookups ---
p = 'tests/test_text125_static.py'
t = load(p)
t = remap(t, [11609, 11751, 16597], 'text125')
save(p, t)

# --- tang173: lines[5207] pin (0-indexed -> line 5208) ---
p = 'tests/test_tang173_static.py'
t = load(p)
new5207 = mapping[5208] - 1
t = t.replace('lines[5207]', f'lines[{new5207}]')
print(f'tang173: lines[5207] -> lines[{new5207}]')
save(p, t)

# --- tang171/tang173/gift185: total 48823 -> 48856, openLoc 43985 -> mapped ---
new_total = 48856
new_openloc = mapping[43985]
for p in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py', 'tests/test_gift185_static.py']:
    t = load(p)
    t = t.replace('48823', str(new_total))
    t = t.replace('43985', str(new_openloc))
    t = t.replace('lines[43984]', f'lines[{new_openloc - 1}]')
    save(p, t)
    print(f'{p}: total->{new_total} openLoc->{new_openloc}')

# --- travel114: list entries + DEF/WRAPPER (v379 approach) ---
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

# --- text55: rail copy changed ---
p = 'tests/test_text55_static.py'
t = load(p)
t = t.replace("'不計日子（茶錢另計）' in src", "'耗用一日（茶錢另計）' in src")
save(p, t)
print('text55: A6 copy updated')

# --- story157: nodes[5:] sha recompute (only N17_410_b notes changed, verified by git diff) ---
d = json.load(open('content/story_detail_n1_to_n17.json'))
nodes = d if isinstance(d, list) else d.get('nodes', d)
if isinstance(nodes, dict): nodes = list(nodes.values())
tail = json.dumps(nodes[5:], sort_keys=True, ensure_ascii=False)
new_sha = hashlib.sha256(tail.encode('utf-8')).hexdigest()
p = 'tests/test_story157_pack_static.py'
t = load(p)
t = t.replace('d3c47bb9481d76a5369ad51b61ffd8f34716e7499889af27c77336215696327b', new_sha)
save(p, t)
print('story157: sha ->', new_sha)

# --- wf1_80 fixture: N17_410_b notes sync (v354 precedent) ---
p = 'tests/fixtures/spine_n6_n17_v136.json'
t = load(p)
old_note = '先說清楚：選這個，今晚之後他就不再是這一行的人。（退圈・安穩）'
new_note = '先說清楚：選這個，今晚之後他就不再是這一行的人。此選擇不可逆轉，結局會按退圈計算。（退圈・安穩）'
assert old_note in t, 'fixture note not found'
t = t.replace(old_note, new_note)
save(p, t)
print('wf1_80 fixture: N17_410_b notes synced')
