#!/usr/bin/env python3
"""v20a176 第三輪 rebase 上 main c682cc2 (v178) resync：
difflib 對位舊樹 -> 合併後 index.html，逐檔重寫釘行。
用法：python3 qa176/resync176_rebase3.py [--check]
  預設改寫；--check 只印報告唔改檔。
映射：
  map1：1367de3:index.html（第三輪 rebase 前 v176 HEAD 樹，含 699 fix）-> 工作版 index.html
       用於 v176 嗰邊嘅檔（12 檔 resync 舊測試＋rom176 兩個新測試）。
  map2：c682cc2:index.html（v178 main）-> 工作版 index.html
       用於 v178 嗰邊嘅檔（prog175／story179 等 v176 冇郁過嘅測試）。
  v178 新測試 awards178 兩個檔係內容斷言，冇釘行，唔入 TARGETS（直接跑驗證）。
  三檔 rebase 衝突（tang171／tang173／travel114）取 v176 嗰邊（theirs），v178 註解行事後手補。
規則：純漂移先改行號——每個釘行舊內容同新內容逐字相同先改，唔同就印 DIFF 停手等人工對。
唔 blanket txt.replace 改 prose 數字（v153 教訓）。"""
import difflib
import re
import subprocess
import sys

CHECK = '--check' in sys.argv
NEW = open('index.html', encoding='utf-8').read().split('\n')
NEW_TOTAL = open('index.html', encoding='utf-8').read().count('\n')


def load_tree(rev):
    txt = subprocess.check_output(['git', 'show', f'{rev}:index.html'], text=True)
    return txt.split('\n')


def build_map(old):
    sm = difflib.SequenceMatcher(None, old, NEW, autojunk=False)
    m = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            for k in range(i2 - i1):
                m[i1 + 1 + k] = j1 + 1 + k
    return m


MAP1 = build_map(load_tree('1367de3'))
MAP2 = build_map(load_tree('c682cc2'))
print(f'舊樹行數 1367de3={len(load_tree("1367de3"))} c682cc2={len(load_tree("c682cc2"))} '
      f'新樹={len(NEW)} (count newline={NEW_TOTAL}) map1={len(MAP1)} map2={len(MAP2)}')

# (檔, 用邊個 map)：1 = 1367de3，2 = c682cc2
TARGETS = [
    ('tests/test_rom176_static.py', 1),
    ('tests/test_kwan151_static.py', 1),
    ('tests/test_tang152_static.py', 1),
    ('tests/test_tang171_static.py', 1),
    ('tests/test_tang173_static.py', 1),
    ('tests/test_text125_static.py', 1),
    ('tests/test_travel114_static.py', 1),
    ('tests/test_bust109_static.py', 1),
    ('tests/test_enc79_static.py', 1),
    ('tests/test_tang164_static.py', 1),
    ('tests/test_tang167_static.py', 1),
    ('tests/test_text55_static.py', 1),
    ('tests/test_weave46_static.py', 1),
    ('tests/test_prog175_static.py', 2),
    ('tests/test_story179_static.py', 2),
]

# 1-based 釘行 pattern：(regex, group index)
PIN1 = [
    (re.compile(r'\bline\((\d+)\)'), 1),
    (re.compile(r'\blen\(ls\)\s*<\s*(\d+)'), 1),
    (re.compile(r'\blen\(lines\)\s*>=\s*(\d+)'), 1),
    (re.compile(r'\bDEF_LINE\s*=\s*(\d+)'), 1),
    (re.compile(r'\bWRAPPER_LINE\s*=\s*(\d+)'), 1),
]
# 0-based 釘行 pattern -> 1-based 行號 = N+1
PIN0 = [
    (re.compile(r'\blines\(\)\[(\d+)\]'), 1),
    (re.compile(r'\blines\[(\d+)\]'), 1),
    (re.compile(r'\bls\[(\d+)\]'), 1),
]
TOTAL_RE = re.compile(r"""count\(['"]\\n['"]\)\s*==\s*(\d+)""")
SETNUM_RE = re.compile(r'^(\s+)(\d+),(\s+#.*)?$')


def remap(old_line, mapping, old_lines):
    """舊 1-based 行號 -> 新 1-based 行號；內容唔同回 None。"""
    new_line = mapping.get(old_line)
    if new_line is None:
        return None
    if old_lines[old_line - 1] != NEW[new_line - 1]:
        return None
    return new_line


def process(path, which):
    mapping = MAP1 if which == 1 else MAP2
    old_lines = load_tree('1367de3' if which == 1 else 'c682cc2')
    lines = open(path, encoding='utf-8').read().split('\n')
    out = []
    remaps = {}  # old 1-based -> new 1-based（呢檔）
    problems = []
    in_set = False
    for ln, text in enumerate(lines, 1):
        orig = text
        if 'COUNT_LINES = {' in text or 'FREE_LINES = {' in text:
            in_set = True
        if in_set and text.strip() == '}':
            in_set = False
        if in_set:
            m = SETNUM_RE.match(text)
            if m:
                old_n = int(m.group(2))
                new_n = remap(old_n, mapping, old_lines)
                if new_n is None:
                    problems.append(f'{path}:{ln} SET {old_n} 對唔到（內容唔同／入咗取代區）')
                elif new_n != old_n:
                    remaps[old_n] = new_n
                    text = f'{m.group(1)}{new_n},{m.group(3) or ""}'
                out.append(text)
                continue
        # 總行數
        m = TOTAL_RE.search(text)
        if m:
            old_n = int(m.group(1))
            if old_n != NEW_TOTAL:
                remaps[old_n] = NEW_TOTAL
                text = text[:m.start(1)] + str(NEW_TOTAL) + text[m.end(1):]
            out.append(text)
            continue
        # 1-based pins
        for rx, g in PIN1:
            for m in list(rx.finditer(text)):
                old_n = int(m.group(g))
                new_n = remap(old_n, mapping, old_lines)
                if new_n is None:
                    problems.append(f'{path}:{ln} line({old_n}) 對唔到：舊={old_lines[old_n-1][:60]!r}')
                elif new_n != old_n:
                    remaps[old_n] = new_n
        # 0-based pins
        for rx, g in PIN0:
            for m in list(rx.finditer(text)):
                old_idx = int(m.group(g))
                new_n = remap(old_idx + 1, mapping, old_lines)
                if new_n is None:
                    problems.append(f'{path}:{ln} idx[{old_idx}] 對唔到')
                elif new_n != old_idx + 1:
                    remaps[old_idx + 1] = new_n
        out.append(text)
    # 第二步：按 remaps 重寫數字（由大到細，避免 5 位數撞位）
    def rewrite(text):
        for rx, g, base in [(r'\bline\((\d+)\)', 1, 1),
                            (r'\blen\(ls\)\s*<\s*(\d+)', 1, 1),
                            (r'\blen\(lines\)\s*>=\s*(\d+)', 1, 1),
                            (r'\bDEF_LINE\s*=\s*(\d+)', 1, 1),
                            (r'\bWRAPPER_LINE\s*=\s*(\d+)', 1, 1),
                            (r'\blines\(\)\[(\d+)\]', 1, 0),
                            (r'\blines\[(\d+)\]', 1, 0),
                            (r'\bls\[(\d+)\]', 1, 0)]:
            def sub(m):
                n = int(m.group(1))
                old_line = n if base == 1 else n + 1
                if old_line in remaps:
                    new_line = remaps[old_line]
                    new_n = new_line if base == 1 else new_line - 1
                    return m.group(0)[:m.start(1) - m.start(0)] + str(new_n) + m.group(0)[m.end(1) - m.start(0):]
                return m.group(0)
            text = re.sub(rx, sub, text)
        return text
    out2 = [rewrite(t) for t in out]
    # 標籤：同檔內 L<舊>／第 <舊> 行 -> L<新>／第 <新> 行（只改 remaps 入面嘅數）
    label_changes = []
    for old_n, new_n in sorted(remaps.items()):
        for pat in (f'L{old_n}', f'第 {old_n} 行'):
            for i, t in enumerate(out2):
                if pat in t:
                    out2[i] = t.replace(pat, pat.replace(str(old_n), str(new_n)))
                    label_changes.append(f'{path}:{i+1} {pat!r} -> {pat.replace(str(old_n), str(new_n))!r}')
    changed = out2 != lines
    for old_n, new_n in sorted(remaps.items()):
        print(f'  OK {path}: L{old_n} -> L{new_n}')
    for p in problems:
        print(f'  DIFF {p}')
    for c in label_changes:
        print(f'  LABEL {c}')
    if not remaps and not problems:
        print(f'  -- {path}：唔使改')
    if changed and not CHECK:
        open(path, 'w', encoding='utf-8').write('\n'.join(out2))
        print(f'  WROTE {path}')
    return problems


all_problems = []
for path, which in TARGETS:
    print(f'== {path} (map{which})')
    try:
        all_problems += process(path, which)
    except FileNotFoundError:
        print(f'  SKIP {path}：冇呢個檔')
print()
if all_problems:
    print(f'有 {len(all_problems)} 個釘行對唔到，要人工對：')
    for p in all_problems:
        print(' ', p)
else:
    print('全部釘行內容逐字相同，純漂移。')
