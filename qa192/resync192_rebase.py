# -*- coding: utf-8 -*-
"""v20a192 rebase 上 f2a6b0c（v191）resync：5 檔舊測試行號重新對位。
方法：difflib 對位 f2a6b0c index.html -> 工作版 index.html（淨 +32，應只係
6 個 v192 hunks）；逐個錨點核實純漂移（舊行內容逐字等於新行內容），先至改數。
用法（喺 ~/workspace/linji-work192 行）：python3 /tmp/resync192_rebase.py
"""
import difflib
import re
import sys

OLD = open('/tmp/pristine191.html', encoding='utf-8').read().splitlines()
NEW = open('index.html', encoding='utf-8').read().splitlines()
print(f"f2a6b0c {len(OLD)} 行，工作版 {len(NEW)} 行，淨 {len(NEW) - len(OLD):+d}")
assert len(NEW) - len(OLD) == 32, "淨行數唔係 +32，停低檢查"

mapping = {}
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
print(f"equal 映射覆蓋 {len(mapping)} / {len(OLD)} 舊行")
print("非 equal 區（應只係 6 個 v192 hunks）：")
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        print(f"  {tag} 舊 L{i1+1}–L{i2} -> 新 L{j1+1}–L{j2}")

fails = []


def check(name, old_ln, expect_sub):
    cur = mapping.get(old_ln)
    if cur is None:
        print(f"FAIL {name}: 舊 L{old_ln} 唔喺 equal 區（被改過，非純漂移）")
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


# ---- travel114 ----
p = 'tests/test_travel114_static.py'
s = open(p, encoding='utf-8').read()
count_lines = [int(x) for x in re.findall(r"^\s*(\d+),", re.search(r"COUNT_LINES = \{([^}]*)\}", s, re.S).group(1), re.M)]
free_lines = [int(x) for x in re.findall(r"^\s*(\d+),", re.search(r"FREE_LINES = \{([^}]*)\}", s, re.S).group(1), re.M)]
print(f"travel114 錨點：COUNT {len(count_lines)} 個，FREE {len(free_lines)} 個")
new_map = {}
for n in count_lines + free_lines:
    new_map[n] = check(f"travel114 openLoc L{n}", n, "openLoc(")
def_line = int(re.search(r"DEF_LINE = (\d+)", s).group(1))
wrap_line = int(re.search(r"WRAPPER_LINE = (\d+)", s).group(1))
new_def = check("travel114 DEF", def_line, "function openLoc(id, opts){")
new_wrap = check("travel114 WRAPPER", wrap_line, "openLoc")


def bump_block(src, block_re):
    m = re.search(block_re, src, re.S)
    blk = m.group(1)
    new_blk, n = re.subn(r"^(\s*)(\d+),",
                         lambda mm: mm.group(1) + str(new_map[int(mm.group(2))]) + ",",
                         blk, flags=re.M)
    return src[:m.start(1)] + new_blk + src[m.end(1):], n


if not fails:
    s, _ = bump_block(s, r"COUNT_LINES = \{([^}]*)\}")
    s, _ = bump_block(s, r"FREE_LINES = \{([^}]*)\}")
    open(p, 'w', encoding='utf-8').write(s)
    print(f"  {p}: COUNT/FREE dicts 已按映射改")
    sub(p, f"DEF_LINE = {def_line}", f"DEF_LINE = {new_def}")
    assert f"WRAPPER_LINE = {wrap_line}" in open(p, encoding='utf-8').read() and new_wrap == wrap_line, "WRAPPER 應該唔郁"
    print(f"  travel114 WRAPPER {wrap_line} 保持不變")

# ---- rom176 ----
p = 'tests/test_rom176_static.py'
s = open(p, encoding='utf-8').read()
rom_anchors = [(r"line\((\d+)\)", None)]
nums = sorted(set(int(x) for x in re.findall(r"line\((\d+)\)", s)))
subs = ["/* ===== v20a176 ROM176", "function rom176ApplyGiftOverrides()",
        "function addLocTalkGiftActs(add, L, npcId)", "rom176TryIntercept(id)"]
print(f"rom176 line() 錨點：{nums}")
new_nums = {}
for n, sub_s in zip(nums, subs):
    new_nums[n] = check(f"rom176 錨 L{n}", n, sub_s)
if not fails:
    for old_n, new_n in new_nums.items():
        if old_n != new_n:
            sub(p, f"line({old_n})", f"line({new_n})")
        else:
            print(f"  rom176 line({old_n}) 唔郁")

# ---- tang171 / tang173 ----
for f in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    s = open(f, encoding='utf-8').read()
    m = re.search(r"len\(lines\) >= (\d+) and 'function openLoc\(id, opts\)\{' in lines\[(\d+)\]", s)
    n = int(m.group(1))
    new_n = check(f"{f} DEF", n - 1, "function openLoc(id, opts){")
    tot = int(re.search(r"src\.count\('\\n'\) == (\d+)", s).group(1))
    print(f"{'PASS' if len(NEW) == tot + 32 else 'FAIL'} {f} 總行數：工作版 {len(NEW)} 行（測試期望 {tot}，須改 {tot + 32}）")
    if len(NEW) != tot + 32:
        fails.append(f + " total")
    if not fails:
        sub(f, f"src.count('\\n') == {tot}", f"src.count('\\n') == {len(NEW)}")
        sub(f, f"len(lines) >= {n} and 'function openLoc(id, opts){{' in lines[{int(m.group(2))}])",
            f"len(lines) >= {new_n + 1} and 'function openLoc(id, opts){{' in lines[{new_n}])")

# ---- tang173 CSS ----
check("tang173 CSS 同行", 4887, "loc-acts-more171::after")

# ---- gift185 ----
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
