# v382 resync: index.html net +99 lines (COSTUME382 CSS +1 @~4221, costume382 functions +65 @~18285,
# canAudition/gateShortReason gates +8, gigCardHtml/teaser/detail rows +4).
# Pins updated by difflib mapping (old -> new), single-pass dict lookup.
import json, re

mapping = {int(k): v for k, v in json.load(open('/tmp/linemap382.json')).items()}

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

# --- rom159 ---
p = 'tests/test_rom159_static.py'
t = load(p)
t = remap(t, [26700, 9031, 27608, 11201, 15470, 27463, 26728], 'rom159')
save(p, t)

# --- rom176 ---
p = 'tests/test_rom176_static.py'
t = load(p)
t = remap(t, [7162, 15468, 42261, 42620, 44060, 44221], 'rom176')
save(p, t)

# --- tang152: lines()[idx] 0-based -> line idx+1 mapped, back to idx ---
p = 'tests/test_tang152_static.py'
t = load(p)
for idx in [15397, 15522]:
    new_idx = mapping[idx + 1] - 1
    t = t.replace(f'lines()[{idx}]', f'lines()[{new_idx}]')
    print(f'tang152: lines()[{idx}] -> lines()[{new_idx}]')
save(p, t)

# --- text125: len(ls) < N and ls[N-1] pairs ---
p = 'tests/test_text125_static.py'
t = load(p)
for ln in [11781, 11923, 17083]:
    new_ln = mapping[ln]
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

# --- gift185/tang171/tang173: total 49020 -> 49119, openLoc 44180 -> 44279, chain append ---
for p in ['tests/test_gift185_static.py', 'tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    t = load(p)
    t = t.replace("＋v381 +164）', src.count('\\n') == 49020)", "＋v381 +164＋v382 +99）', src.count('\\n') == 49119)")
    t = t.replace("＋v381 +164）', html.count('\\n') == 49020)", "＋v381 +164＋v382 +99）', html.count('\\n') == 49119)")
    t = t.replace('總行數 49020（', '總行數 49119（')
    t = t.replace("＋v381 +162，travel114 釘行）',\n   len(lines) >= 44180 and 'function openLoc(id, opts){' in lines[44179])",
                  "＋v381 +162＋v382 +99，travel114 釘行）',\n   len(lines) >= 44279 and 'function openLoc(id, opts){' in lines[44278])")
    t = t.replace('openLoc DEF 行 44180（', 'openLoc DEF 行 44279（')
    save(p, t)
    print(f'{p}: total/openLoc updated')

# --- tang173 L4872: lines[5220] -> lines[5221] (line 5221 -> 5222) ---
p = 'tests/test_tang173_static.py'
t = load(p)
assert mapping[5221] == 5222, mapping[5221]
t = t.replace('lines[5220]', 'lines[5221]')
save(p, t)
print('tang173: lines[5220] -> lines[5221]')
