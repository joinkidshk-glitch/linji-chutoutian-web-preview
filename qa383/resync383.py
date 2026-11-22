# v383 resync: index.html net +155 lines (TAPE383 CSS +6 @~4220, normalize +1,
# gigCard/teaser labels +6, costume382 exclusion +1, MOCK_ASK def +2, mockAskDefs +14,
# applyMockAsk guard +2, advanceDay tick +1, board exemption +3, add() hooks +6,
# TAPE383 module +113 @~43437). Pins updated by difflib mapping (old -> new), single-pass dict lookup.
import json, re

mapping = {int(k): v for k, v in json.load(open('/tmp/linemap383.json')).items()}

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
t = remap(t, [26799, 9032, 27707, 11202, 15471, 27562], 'rom159')
assert mapping[26827] == 26849, mapping[26827]
t = t.replace('idx_lines[26827 - 1]', 'idx_lines[26849 - 1]')
print('rom159: 全佳行 26827 -> 26849')
save(p, t)

# --- rom176: line() pins ---
p = 'tests/test_rom176_static.py'
t = load(p)
t = remap(t, [7163, 15469, 42360, 42719, 44159, 44320], 'rom176')
save(p, t)

# --- tang152: lines()[idx] 0-based -> line idx+1 mapped, back to idx ---
p = 'tests/test_tang152_static.py'
t = load(p)
for idx in [15398, 15523]:
    new_idx = mapping[idx + 1] - 1
    t = t.replace(f'lines()[{idx}]', f'lines()[{new_idx}]')
    print(f'tang152: lines()[{idx}] -> lines()[{new_idx}]')
save(p, t)

# --- text125: len(ls) < N and ls[N-1] pairs ---
p = 'tests/test_text125_static.py'
t = load(p)
for ln in [11782, 11924, 17084]:
    new_ln = mapping[ln]
    t = t.replace(f'len(ls) < {ln} or', f'len(ls) < {new_ln} or')
    t = t.replace(f'ls[{ln - 1}]', f'ls[{new_ln - 1}]')
    print(f'text125: {ln} -> {new_ln}')
save(p, t)

# --- travel114: list entries + DEF/WRAPPER + 2 new FREE call sites (43525/43545, new-file lines) ---
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
# add the two new FREE call sites right after FREE_LINES opening brace line
t = t.replace('FREE_LINES = {\n', 'FREE_LINES = {\n    43533,  # v383 tape383OpenPicker 取消／完成返去而家身處地點（travelFree，唔計額度）\n    43553,  # v383 tape383Confirm 完成返去而家身處地點（travelFree，唔計額度）\n', 1)
save(p, t)
print(f'travel114: {cnt} remapped + 2 new FREE')

# --- reconfirm236: confirmChoice236 call sites 12 -> 13 (+def = 14) ---
p = 'tests/test_reconfirm236_static.py'
t = load(p)
t = t.replace("ok('A 呼叫點齊 12 處（＋定義＝13）', html.count('confirmChoice236(') == 13)",
              "ok('A 呼叫點齊 13 處（＋定義＝14）', html.count('confirmChoice236(') == 14)")
save(p, t)
print('reconfirm236: 13 -> 14')

# --- gift185/tang171/tang173: total 49119 -> 49282, openLoc 44279 -> 44427, chain append ---
for p in ['tests/test_gift185_static.py', 'tests/test_tang171_static.py', 'tests/test_tang173_static.py']:
    t = load(p)
    t = t.replace("＋v381 +164＋v382 +99）', src.count('\\n') == 49119)", "＋v381 +164＋v382 +99＋v383 +163）', src.count('\\n') == 49282)")
    t = t.replace("＋v381 +164＋v382 +99）', html.count('\\n') == 49119)", "＋v381 +164＋v382 +99＋v383 +163）', html.count('\\n') == 49282)")
    t = t.replace('總行數 49119（', '總行數 49282（')
    t = t.replace("＋v381 +162＋v382 +99，travel114 釘行）',\n   len(lines) >= 44279 and 'function openLoc(id, opts){' in lines[44278])",
                  "＋v381 +162＋v382 +99＋v383 +163，travel114 釘行）',\n   len(lines) >= 44435 and 'function openLoc(id, opts){' in lines[44434])")
    t = t.replace('openLoc DEF 行 44279（', 'openLoc DEF 行 44435（')
    save(p, t)
    print(f'{p}: total/openLoc updated')

# --- tang173 L4872 label: actual pin lines[5221] (0-based, line 5222) + len>=5208; CSS +6 before it ---
p = 'tests/test_tang173_static.py'
t = load(p)
assert mapping[5222] == 5228, mapping[5222]
t = t.replace('lines[5221]', 'lines[5227]')
t = t.replace('len(lines) >= 5208', 'len(lines) >= 5214')
save(p, t)
print('tang173: lines[5221] -> lines[5227], len 5208 -> 5214')
