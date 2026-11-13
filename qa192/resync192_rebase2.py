# -*- coding: utf-8 -*-
"""v20a192 rebase 上 f2a6b0c（v191）resync — 第 2 輪（travel114 已喺第 1 輪改好，今輪唔再郁佢）。
逐個錨點 difflib 核實純漂移先改數。用法（喺 ~/workspace/linji-work192 行）：
python3 /tmp/resync192_rebase2.py
"""
import difflib
import re
import sys

OLD = open('/tmp/pristine191.html', encoding='utf-8').read().splitlines()
NEW = open('index.html', encoding='utf-8').read().splitlines()
print(f"f2a6b0c {len(OLD)} 行，工作版 {len(NEW)} 行，淨 {len(NEW) - len(OLD):+d}")
assert len(NEW) - len(OLD) == 32

mapping = {}
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k

fails = []


def check(name, old_ln, expect_sub):
    cur = mapping.get(old_ln)
    if cur is None:
        print(f"FAIL {name}: 舊 L{old_ln} 唔喺 equal 區")
        fails.append(name)
        return None
    o, n = OLD[old_ln - 1], NEW[cur - 1]
    ok = (o == n) and (expect_sub in n)
    print(f"{'PASS' if ok else 'FAIL'} {name}: 舊 L{old_ln} -> 新 L{cur} (shift {cur - old_ln:+d}) 內容相同={o == n} 含標記={expect_sub in n}")
    if not ok:
        fails.append(name)
        print(f"   舊: {o[:120]}")
        print(f"   新: {n[:120]}")
    return cur


def sub(path, old, new, count=1):
    s = open(path, encoding='utf-8').read()
    n = s.count(old)
    assert n == count, f"{path}: {old!r} 出現 {n} 次，預期 {count} 次"
    open(path, 'w', encoding='utf-8').write(s.replace(old, new))
    print(f"  fix {path}: {old.strip()[:70]!r} -> {new.strip()[:70]!r}")


# ---- rom176：淨係 4 個 ROM176 錨點（6072／31583 喺插入點前，唔郁） ----
p = 'tests/test_rom176_static.py'
rom = [(53416, "/* ===== v20a176 ROM176"),
       (53784, "function rom176ApplyGiftOverrides()"),
       (54923, "function addLocTalkGiftActs(add, L, npcId)"),
       (55017, "rom176TryIntercept(id)")]
new_rom = {}
for n, ssub in rom:
    new_rom[n] = check(f"rom176 錨 L{n}", n, ssub)
if not fails:
    for old_n, new_n in new_rom.items():
        sub(p, f"line({old_n})", f"line({new_n})")

# ---- tang171 / tang173：DEF 1-based = group(1)；總行數 60490 -> 60522 ----
for f in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    s = open(f, encoding='utf-8').read()
    m = re.search(r"len\(lines\) >= (\d+) and 'function openLoc\(id, opts\)\{' in lines\[(\d+)\]", s)
    def1 = int(m.group(1))  # 1-based DEF 行（lines[group2)] 0-based = 同一行）
    assert int(m.group(2)) == def1 - 1, f"{f}: DEF 斷言內外唔一致"
    new_def = check(f"{f} DEF", def1, "function openLoc(id, opts){")
    tot = int(re.search(r"src\.count\('\\n'\) == (\d+)", s).group(1))
    print(f"{'PASS' if len(NEW) == tot + 32 else 'FAIL'} {f} 總行數：工作版 {len(NEW)} 行（測試期望 {tot}，須改 {tot + 32}）")
    if len(NEW) != tot + 32:
        fails.append(f + " total")
    if not fails:
        sub(f, f"src.count('\\n') == {tot}", f"src.count('\\n') == {len(NEW)}")
        sub(f, f"len(lines) >= {def1} and 'function openLoc(id, opts){{' in lines[{def1 - 1}])",
            f"len(lines) >= {new_def} and 'function openLoc(id, opts){{' in lines[{new_def - 1}])")

# ---- tang173 CSS：lines[4888] 0-based = 1-based L4889，插入點前，唔郁 ----
check("tang173 CSS 同行", 4889, "loc-acts-more171::after")

# ---- gift185：總行數 60490 -> 60522 ----
p = 'tests/test_gift185_static.py'
s = open(p, encoding='utf-8').read()
tot = int(re.search(r"html\.count\('\\n'\) == (\d+)", s).group(1))
print(f"{'PASS' if len(NEW) == tot + 32 else 'FAIL'} gift185 總行數：工作版 {len(NEW)} 行（測試期望 {tot}，須改 {tot + 32}）")
if len(NEW) != tot + 32:
    fails.append("gift185 total")
if not fails:
    sub(p, f"html.count('\\n') == {tot}", f"html.count('\\n') == {len(NEW)}")

print()
print("FAILED: %d" % len(fails) if fails else "ALL ANCHORS VERIFIED PURE DRIFT + FIXED")
sys.exit(1 if fails else 0)
