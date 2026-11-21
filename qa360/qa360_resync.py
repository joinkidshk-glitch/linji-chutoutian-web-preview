#!/usr/bin/env python3
"""v360 resync：index.html 淨 +69 行（P0 三修），difflib 映射各測試行號釘，逐釘驗證內容相同。"""
import difflib, re, subprocess, sys

old = subprocess.run(['git', 'show', 'HEAD:index.html'], capture_output=True, text=True, cwd='.').stdout.split('\n')
new = open('index.html', encoding='utf-8').read().split('\n')
print(f"old lines={len(old)} new lines={len(new)}")

sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}  # old 1-indexed -> new 1-indexed
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1

def map_line(n, ctx=""):
    if n not in mapping:
        print(f"ABORT: line {n} ({ctx}) not in equal mapping"); sys.exit(1)
    m = mapping[n]
    if old[n - 1] != new[m - 1]:
        print(f"ABORT: content mismatch {n}->{m} ({ctx}):\n  old: {old[n-1][:90]}\n  new: {new[m-1][:90]}"); sys.exit(1)
    return m

def load(p):
    return open(p, encoding='utf-8').read()

def save(p, s):
    open(p, 'w', encoding='utf-8').write(s)

HDR = "# v20a360 resync：index.html 淨 +69 行（P0 三修：normalize 回填呼叫 +2／defaultWeekPlan 輪替 +7／enterHome 懶掃 +3／genre 標籤授予＋回填 +41／aud91PresentDue 自癒 +16）；釘行按 difflib 映射重寫，內容逐字核實純漂移（qa360_resync.py）。\n"

def add_hdr(s):
    lines = s.split('\n')
    # insert after shebang if present
    idx = 1 if lines and lines[0].startswith('#!') else 0
    lines.insert(idx, HDR.rstrip('\n'))
    return '\n'.join(lines)

# ---------- text125 ----------
p = 'tests/test_text125_static.py'
s = load(p)
for n in (10896, 11038, 15979):
    m = map_line(n, f'text125 {n}')
    print(f"text125 {n}->{m}")
    if m != n:
        s = s.replace(f'len(ls) < {n} or', f'len(ls) < {m} or')
        s = s.replace(f'ls[{n-1}]', f'ls[{m-1}]')
        s = s.replace(f'第 {n} 行', f'第 {m} 行')
save(p, add_hdr(s))

# ---------- rom159 ----------
p = 'tests/test_rom159_static.py'
s = load(p)
for n in (25100, 8173, 25994, 10316, 14421, 25849):
    m = map_line(n, f'rom159 {n}')
    print(f"rom159 {n}->{m}")
    if m != n:
        s = s.replace(f'line_has({n},', f'line_has({m},')
m = map_line(25128, 'rom159 全佳')
print(f"rom159 全佳 25128->{m}")
if m != 25128:
    s = s.replace('idx_lines[25128 - 1]', f'idx_lines[{m} - 1]')
save(p, add_hdr(s))

# ---------- rom176 ----------
p = 'tests/test_rom176_static.py'
s = load(p)
for n in (6325, 14419, 40463, 40813, 42116, 42277):
    m = map_line(n, f'rom176 {n}')
    print(f"rom176 {n}->{m}")
    if m != n:
        s = s.replace(f'line({n})', f'line({m})')
save(p, add_hdr(s))

# ---------- travel114 ----------
p = 'tests/test_travel114_static.py'
s = load(p)
def remap_set(s, name):
    m = re.search(name + r' = \{([^}]*)\}', s)
    assert m, name
    body = m.group(1)
    def sub(mm):
        n = int(mm.group(0))
        return str(map_line(n, f'travel114 {name} {n}'))
    newbody = re.sub(r'\b\d{4,5}\b', sub, body)
    return s[:m.start(1)] + newbody + s[m.end(1):]
s = remap_set(s, 'COUNT_LINES')
s = remap_set(s, 'FREE_LINES')
for name, n in (('DEF_LINE', 42236), ('WRAPPER_LINE', 28834)):
    m = map_line(n, f'travel114 {name}')
    print(f"travel114 {name} {n}->{m}")
    s = re.sub(name + r' = ' + str(n) + r'\b', f'{name} = {m}', s)
save(p, add_hdr(s))

# ---------- tang171 / tang173 / gift185 ----------
total_new = len(new) - 1  # split('\n') trailing empty
print("total_new (count \\n):", open('index.html', encoding='utf-8').read().count('\n'))
def_line_new = map_line(42236, 'openLoc DEF')
print(f"openLoc DEF 42236->{def_line_new}")
for p in ('tests/test_tang171_static.py', 'tests/test_tang173_static.py', 'tests/test_gift185_static.py'):
    s = load(p)
    s = s.replace("== 46999", "== 47068")
    s = s.replace("總行數 46999（", "總行數 47068（")
    s = s.replace("＋v358 −441）", "＋v358 −441＋v360 +69）")
    if '42236' in s:
        s = s.replace("openLoc DEF 行 42236（", f"openLoc DEF 行 {def_line_new}（")
        s = s.replace("＋v358 −424，travel114 釘行）", "＋v358 −424＋v360 +53，travel114 釘行）")
        s = s.replace("len(lines) >= 42236", f"len(lines) >= {def_line_new}")
        s = s.replace("lines[42235]", f"lines[{def_line_new - 1}]")
    save(p, add_hdr(s))
    print(f"{p} done")

print("ALL RESYNC DONE")
