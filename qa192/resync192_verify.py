# -*- coding: utf-8 -*-
"""v20a192 resync 驗證：index.html 淨 +32 行（6 個 hunks，全部喺 L45296–46530 之間：
VENUE99 dek 0／C1 0／NP_WIN 註解 +7／C4 請柬 +11／C3 結果卡 +11／C2 閘句 +3）。
呢個腳本用 difflib 對位逐個錨點核實：pristine（main b7ca827）舊行內容逐字等於
工作版新行內容（純漂移），先至准改測試檔行號。唔信盲改。
用法：python3 qa192/resync192_verify.py
"""
import difflib
import re
import sys

OLD = open('/home/hatch/workspace/linji-pristine192/index.html', encoding='utf-8').read().splitlines()
NEW = open('index.html', encoding='utf-8').read().splitlines()
print(f"pristine {len(OLD)} 行，工作版 {len(NEW)} 行，淨 {len(NEW) - len(OLD):+d}")

mapping = {}
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
print(f"equal 映射覆蓋 {len(mapping)} / {len(OLD)} 舊行")
print("非 equal 區（應只係 6 個 v192 hunks，L45296–46530）：")
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal':
        print(f"  {tag} 舊 L{i1+1}–L{i2} -> 新 L{j1+1}–L{j2}")

fails = []


def check_anchor(name, pristine_ln, expect_sub):
    cur_ln = mapping.get(pristine_ln)
    if cur_ln is None:
        print(f"FAIL {name}: pristine L{pristine_ln} 唔喺 equal 區（被改過，非純漂移）")
        fails.append(name)
        return None
    o, n = OLD[pristine_ln - 1], NEW[cur_ln - 1]
    ok = (o == n) and (expect_sub in n)
    print(f"{'PASS' if ok else 'FAIL'} {name}: pristine L{pristine_ln} -> 工作版 L{cur_ln} "
          f"(shift {cur_ln - pristine_ln:+d}) 內容相同={o == n} 含標記={expect_sub in n}")
    if not ok:
        fails.append(name)
        print(f"   舊: {o[:120]}")
        print(f"   新: {n[:120]}")
    return cur_ln


# ---- travel114：COUNT／FREE／DEF／WRAPPER ----
src114 = open('tests/test_travel114_static.py', encoding='utf-8').read()
count_lines = [int(x) for x in re.findall(r"^\s*(\d+),", re.search(r"COUNT_LINES = \{([^}]*)\}", src114, re.S).group(1), re.M)]
free_lines = [int(x) for x in re.findall(r"^\s*(\d+),", re.search(r"FREE_LINES = \{([^}]*)\}", src114, re.S).group(1), re.M)]
print(f"travel114 錨點：COUNT {len(count_lines)} 個，FREE {len(free_lines)} 個")
for n in count_lines + free_lines:
    check_anchor(f"travel114 openLoc L{n}", n, "openLoc(")
def_line = int(re.search(r"DEF_LINE = (\d+)", src114).group(1))
wrap_line = int(re.search(r"WRAPPER_LINE = (\d+)", src114).group(1))
check_anchor("travel114 DEF", def_line, "function openLoc(id, opts){")
check_anchor("travel114 WRAPPER", wrap_line, "openLoc")

# ---- rom176：4 個錨點 ----
for n, sub in [(53369, "/* ===== v20a176 ROM176"),
               (53737, "function rom176ApplyGiftOverrides()"),
               (54876, "function addLocTalkGiftActs(add, L, npcId)"),
               (54970, "rom176TryIntercept(id)")]:
    check_anchor(f"rom176 錨 L{n}", n, sub)

# ---- tang171／tang173：總行數＋DEF 行 ----
for f in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    s = open(f, encoding='utf-8').read()
    m = re.search(r"len\(lines\) >= (\d+) and 'function openLoc\(id, opts\)\{' in lines\[(\d+)\]", s)
    n = int(m.group(1))
    check_anchor(f"{f} DEF", n - 1, "function openLoc(id, opts){")
    tot = int(re.search(r"src\.count\('\\n'\) == (\d+)", s).group(1))
    print(f"{'PASS' if len(NEW) == tot + 32 else 'FAIL'} {f} 總行數：工作版 {len(NEW)} 行（測試期望 {tot}，須改 {tot + 32}）")
    if len(NEW) != tot + 32:
        fails.append(f + " total")

# ---- tang173：CSS 同行錨點 ----
check_anchor("tang173 CSS 同行", 4887, "loc-acts-more171::after")

# ---- gift185：總行數 ----
print(f"{'PASS' if len(NEW) == 60475 else 'FAIL'} gift185 總行數：工作版 {len(NEW)} 行（測試期望 60443，須改 60475）")
if len(NEW) != 60475:
    fails.append("gift185 total")

print()
print("FAILED: %d" % len(fails) if fails else "ALL ANCHORS VERIFIED PURE DRIFT")
sys.exit(1 if fails else 0)
