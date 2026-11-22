# v387 resync: index.html net +4 lines (EVAL8 P2: awd62 stage scale/overflow +3 @~L806,
# np214-switch min-height +1). Pins updated by difflib mapping (old -> new), single-pass dict lookup.
# Content pins for intentional changes: fix65 shoot preview 10->12, wrapHistory cap 90->240,
# buttons197 summary display:block->flex.
import json, re

mapping = {int(k): v for k, v in json.load(open('/tmp/linemap387.json')).items()}

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
t = remap(t, [26895, 9060, 27803, 11230, 15502], 'rom159')
new_qj = mapping[26923]
t = t.replace('idx_lines[26923 - 1]', f'idx_lines[{new_qj} - 1]')
print(f'rom159: 全佳行 26923 -> {new_qj}')
save(p, t)

# --- rom176: line() pins ---
p = 'tests/test_rom176_static.py'
t = load(p)
t = remap(t, [7191, 15500, 42473, 42832, 44398, 44559], 'rom176')
save(p, t)

# --- tang152: lines()[idx] 0-based ---
p = 'tests/test_tang152_static.py'
t = load(p)
for idx in [15429, 15554]:
    new_idx = mapping[idx + 1] - 1
    t = t.replace(f'lines()[{idx}]', f'lines()[{new_idx}]')
    print(f'tang152: lines()[{idx}] -> lines()[{new_idx}]')
save(p, t)

# --- tang173: lines[idx] 0-based (openLoc + L4872 同行) ---
p = 'tests/test_tang173_static.py'
t = load(p)
for idx in [44517, 5229]:
    new_idx = mapping[idx + 1] - 1
    t = t.replace(f'lines[{idx}]', f'lines[{new_idx}]')
    print(f'tang173: lines[{idx}] -> lines[{new_idx}]')
t = t.replace('len(lines) >= 44518', f'len(lines) >= {mapping[44518]}')
save(p, t)

# --- text125: len(ls) < N and ls[N-1] pairs ---
p = 'tests/test_text125_static.py'
t = load(p)
for ln in [11810, 11952, 17121]:
    new_ln = mapping[ln]
    t = t.replace(f'len(ls) < {ln} or', f'len(ls) < {new_ln} or')
    t = t.replace(f'ls[{ln - 1}]', f'ls[{new_ln - 1}]')
    print(f'text125: {ln} -> {new_ln}')
save(p, t)

# --- gift185 / tang171 / tang173: 總行數 ledger + openLoc DEF ---
for p in ['tests/test_gift185_static.py', 'tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    t = load(p)
    t = t.replace('49382', '49386')
    t = t.replace('v386 +40）', 'v386 +40＋v387 +4）')
    t = t.replace('v386 +40，travel114 釘行）', 'v386 +40＋v387 +4，travel114 釘行）')
    save(p, t)
    print(p + ': ledger 49382->49386 +v387 +4')
for p in ['tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    t = load(p)
    assert mapping[44518] == 44522, mapping[44518]
    t = t.replace('openLoc DEF 行 44518', 'openLoc DEF 行 44522')
    save(p, t)
    print(p + ': openLoc DEF 44518 -> 44522')

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
t = t.replace('DEF_LINE = 44518', 'DEF_LINE = 44522')
t = t.replace('WRAPPER_LINE = 30706', f'WRAPPER_LINE = {mapping[30706]}')
print(f'travel114: DEF 44518->44522 WRAPPER 30706->{mapping[30706]}')
save(p, t)

# --- fix65 logic: shoot preview 10 -> 12 (intentional v387 calibration) ---
p = 'tests/test_fix65_logic.js'
t = load(p)
t = t.replace('stressDeltaForAct("shoot:gig_x") === 10, "預覽入水維持原值（train/shoot = 10）"',
              'stressDeltaForAct("shoot:gig_x") === 12, "預覽入水：train = 10、shoot = 12（v387 校準到實際 8+R(2,6) 平均）"')
save(p, t)
print('fix65_logic: shoot 10 -> 12')

# --- fix65 static + release215: wrapHistory cap 90 -> 240 (intentional v387) ---
p = 'tests/test_fix65_static.py'
t = load(p)
t = t.replace('ok("S.wrapHistory.length>90" in src.replace(" ", "") or "wrapHistory.length>90" in src,\n   "wrapHistory 上限 90（舊 30；全弧單年最多 79 部，30 條冚唔晒一年）")',
              'ok("S.wrapHistory.length>240" in src.replace(" ", "") or "wrapHistory.length>240" in src,\n   "wrapHistory 上限 240（v387：同 careerStats95 全史口徑對齊，冚得晒三年全弧；舊 90 只冚一年）")')
save(p, t)
print('fix65_static: cap 90 -> 240')

p = 'tests/test_release215_static.py'
t = load(p)
t = t.replace("chk('唔郁：wrapHistory 上限 90 照舊',\n    'if(S.wrapHistory.length>90) S.wrapHistory.length=90;' in src)",
              "chk('wrapHistory 上限 240（v387 改：同 careerStats95 全史口徑對齊）',\n    'if(S.wrapHistory.length>240) S.wrapHistory.length=240;' in src)")
save(p, t)
print('release215: cap 90 -> 240')

# --- buttons197: summary display:block -> flex (intentional v387 touch height) ---
p = 'tests/test_buttons197_static.py'
t = load(p)
t = t.replace("and '.gig-locked108 summary{ display:block;' in src",
              "and '.gig-locked108 summary{ display:flex; align-items:center; min-height:44px;' in src")
save(p, t)
print('buttons197: summary display flex + 44px')

# --- 補：rom159 SoMeetGate 釘 + tang171 lines[44517]（首跑漏咗，逐個覆驗時補） ---
p = 'tests/test_rom159_static.py'
t = load(p)
t = t.replace('line_has(27658, "function rom159SoMeetGate")', f'line_has({mapping[27658]}, "function rom159SoMeetGate")')
save(p, t)
print(f'rom159 SoMeetGate 27658 -> {mapping[27658]}')

p = 'tests/test_tang171_static.py'
t = load(p)
t = t.replace('lines[44517]', f'lines[{mapping[44518]-1}]')
t = t.replace('len(lines) >= 44518', f'len(lines) >= {mapping[44518]}')
save(p, t)
print('tang171 lines[44517] fixed')

print('resync387 done')
