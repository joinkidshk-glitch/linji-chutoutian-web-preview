#!/usr/bin/env python3
"""v20a279 resync：index.html 淨 +99 行（numstat 106 add／7 del）。
插入點（base 行號）：26418 +1、26426 +1、26569 +7、26621 +1、27419 +35、27432 +12、
35491 +33、38815 +1、38873 +2、38937 +4、42526 +2。
漂移分段：<26418 0；26418–26568 +1；26569–26620 +9；26621–27418 +10；27419–27431 +45；
27432–35490 +57；35491–38814 +90；38815–38872 +91；38873–38936 +93；38937–42525 +97；>=42526 +99。
方法：difflib 對位 base(4ba3078) vs 現行 index.html，逐粒釘核實內容逐字相同先改寫（純漂移）。
鏈式（gift185／tang171／tang173）：總行數 +99、openLoc DEF +97（DEF 喺 42526 插入點之前）。
"""
import difflib, re, subprocess, sys

ROOT = '/home/hatch/workspace/linji-work279'
base = subprocess.run(['git', 'show', '4ba3078:index.html'], cwd=ROOT,
                      capture_output=True, text=True, check=True).stdout.splitlines()
cur = open(ROOT + '/index.html', encoding='utf-8').read().splitlines()
print('base lines:', len(base), 'cur lines:', len(cur), 'net:', len(cur) - len(base))

sm = difflib.SequenceMatcher(a=base, b=cur, autojunk=False)
mapping = {}  # old 1-based -> new 1-based
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
    elif tag == 'replace':
        # 對齊 block 內相同嘅行
        old_block, new_block = base[i1:i2], cur[j1:j2]
        used = set()
        for k, ln in enumerate(old_block):
            for m, ln2 in enumerate(new_block):
                if m not in used and ln == ln2:
                    mapping[i1 + 1 + k] = j1 + 1 + m
                    used.add(m)
                    break

def remap(old_ln):
    assert old_ln in mapping, f'line {old_ln} unmapped (deleted/replaced?)'
    new_ln = mapping[old_ln]
    assert base[old_ln - 1] == cur[new_ln - 1], (
        f'line {old_ln}->{new_ln} content mismatch:\n  base: {base[old_ln-1][:80]!r}\n  cur:  {cur[new_ln-1][:80]!r}')
    return new_ln

# ---------- rom176：4 粒絕對釘 ----------
p = ROOT + '/tests/test_rom176_static.py'
s = open(p, encoding='utf-8').read()
pins = {'39635': '/* ===== v20a176 ROM176', '39993': 'function rom176ApplyGiftOverrides()',
        '41165': 'function addLocTalkGiftActs(add, L, npcId)',
        '41321': 'rom176TryIntercept(id)'}
newpins = {}
for old, anchor in pins.items():
    n = remap(int(old))
    assert anchor in cur[n - 1], f'rom176 {old}->{n}: anchor {anchor!r} not in {cur[n-1][:80]!r}'
    newpins[old] = str(n)
    print(f'rom176 {old} -> {n}  {anchor[:40]}')
for old, new in newpins.items():
    assert s.count(f'line({old})') == 1, f'rom176 line({old}) count != 1'
    s = s.replace(f'line({old})', f'line({new})')
open(p, 'w', encoding='utf-8').write(s)
print('rom176 written')

# ---------- travel114：COUNT 12＋FREE 40＋DEF＋WRAPPER ----------
p = ROOT + '/tests/test_travel114_static.py'
s = open(p, encoding='utf-8').read()
# 搵 COUNT_LINES／FREE_LINES 兩個 set 嘅行範圍
lines = s.splitlines()
def block_range(start_marker):
    start = next(i for i, l in enumerate(lines) if l.startswith(start_marker))
    end = next(i for i in range(start, len(lines)) if lines[i].strip() == '}')
    return start, end
cs, ce = block_range('COUNT_LINES = {')
fs, fe = block_range('FREE_LINES = {')
nums = {}
for i in list(range(cs + 1, ce)) + list(range(fs + 1, fe)):
    m = re.match(r'\s*(\d+),', lines[i])
    assert m, f'travel114 line {i+1} not a number: {lines[i]!r}'
    nums[int(m.group(1))] = i
remapped = {}
for old, i in sorted(nums.items()):
    n = remap(old)
    assert 'openLoc(' in cur[n - 1], f'travel114 {old}->{n}: no openLoc( in {cur[n-1][:80]!r}'
    remapped[old] = n
    print(f'travel114 {old} -> {n}')
# 單次掃描：只喺兩個 set 區間內換數字（唔掂註解／其他行）
def rescan_region(text_lines, start, end, mapping_dict):
    out = []
    for i, l in enumerate(text_lines):
        if start <= i < end:
            m = re.match(r'(\s*)(\d+)(,.*)$', l)
            assert m, f'region line {i+1}: {l!r}'
            old = int(m.group(2))
            l = m.group(1) + str(mapping_dict[old]) + m.group(3)
        out.append(l)
    return out
lines = rescan_region(lines, cs + 1, ce, remapped)
lines = rescan_region(lines, fs + 1, fe, remapped)
# DEF／WRAPPER（賦值行，唔掂註解）
for i, l in enumerate(lines):
    if l.startswith('DEF_LINE = '):
        n = remap(41280)
        assert 'function openLoc(id, opts){' in cur[n - 1]
        lines[i] = f'DEF_LINE = {n}      # function openLoc(id, opts){{'
        print(f'travel114 DEF 41280 -> {n}')
    if l.startswith('WRAPPER_LINE = '):
        n = remap(28636)
        assert 'openLoc' in cur[n - 1], f'WRAPPER {n}: {cur[n-1][:80]!r}'
        lines[i] = f'WRAPPER_LINE = {n}  # window.__phase2.openLoc：轉發 opts'
        print(f'travel114 WRAPPER 28636 -> {n}')
open(p, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('travel114 written')

# ---------- 鏈式：gift185／tang171／tang173 ----------
def chain_file(path, has_def):
    s = open(path, encoding='utf-8').read()
    # 總行數：標籤＋鏈尾＋檢查值
    assert s.count("總行數 46030（") == 1
    s = s.replace("總行數 46030（", "總行數 46129（")
    old_tail = "＋v278 +527）', "
    assert s.count(old_tail) == 1, f'{path}: total tail count {s.count(old_tail)}'
    s = s.replace(old_tail, "＋v278 +527＋v279 +99）', ")
    assert "count('\\n') == 46030" in s
    s = s.replace("count('\\n') == 46030", "count('\\n') == 46129")
    if has_def:
        assert s.count("openLoc DEF 行 41280（") == 1
        s = s.replace("openLoc DEF 行 41280（", "openLoc DEF 行 41377（")
        old_def = "＋v278 +527，travel114 釘行）"
        assert s.count(old_def) == 1
        s = s.replace(old_def, "＋v278 +527＋v279 +97，travel114 釘行）")
        assert "len(lines) >= 41286 and 'function openLoc(id, opts){' in lines[41279]" in s
        s = s.replace("len(lines) >= 41286 and 'function openLoc(id, opts){' in lines[41279]",
                      "len(lines) >= 41383 and 'function openLoc(id, opts){' in lines[41376]")
    open(path, 'w', encoding='utf-8').write(s)
    print('chain written:', path)

chain_file(ROOT + '/tests/test_gift185_static.py', False)
chain_file(ROOT + '/tests/test_tang171_static.py', True)
chain_file(ROOT + '/tests/test_tang173_static.py', True)
print('ALL RESYNC DONE')
