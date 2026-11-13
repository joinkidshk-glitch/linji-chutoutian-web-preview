# -*- coding: utf-8 -*-
"""v20a188 resync 驗證（第二輪）：上一手 resync188.py 用 +225，但 index.html 其後
再加咗 +29 行（NP_WIN 覆寫＋load 呼叫＋gate 行＋debug 入口），總淨變 +254。
呢個腳本用 difflib 對位逐個錨點核實：pristine（main fc76b9e）舊行內容逐字等於
工作版新行內容（純漂移），先至准改測試檔行號。唔信盲改。
用法：python3 qa188/resync188_verify.py
"""
import difflib
import re
import sys

OLD = open('/tmp/pristine188.html', encoding='utf-8').read().splitlines()
NEW = open('index.html', encoding='utf-8').read().splitlines()
print(f"pristine {len(OLD)} 行，工作版 {len(NEW)} 行，淨 {len(NEW) - len(OLD):+d}")

# difflib 映射：pristine 行號（1-based）-> 工作版行號（1-based），只限 equal 區
mapping = {}
sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        for k in range(i2 - i1):
            mapping[i1 + 1 + k] = j1 + 1 + k
print(f"equal 映射覆蓋 {len(mapping)} / {len(OLD)} 舊行")

fails = []


def check_anchor(name, pristine_ln, expect_sub):
    """核實：pristine 行 pristine_ln 嘅內容，喺工作版 mapping 行逐字相同，並含 expect_sub。"""
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


# ---- travel114：COUNT／FREE／DEF（測試檔現有數字係 +225 中間態；pristine 號＝現有－225）----
src114 = open('tests/test_travel114_static.py', encoding='utf-8').read()
def _set_nums(block):
    return [int(x) for x in re.findall(r"^\s*(\d+),", block, re.M)]
count_lines = _set_nums(re.search(r"COUNT_LINES = \{([^}]*)\}", src114, re.S).group(1))
free_lines = _set_nums(re.search(r"FREE_LINES = \{([^}]*)\}", src114, re.S).group(1))
print(f"travel114 錨點：COUNT {len(count_lines)} 個，FREE {len(free_lines)} 個")
def_line = int(re.search(r"DEF_LINE = (\d+)", src114).group(1))
wrap_line = int(re.search(r"WRAPPER_LINE = (\d+)", src114).group(1))
for n in count_lines + free_lines:
    p = n - 225 if n > 46000 else n  # 插入區之後者先減 225 還原 pristine 號
    check_anchor(f"travel114 openLoc L{n}", p, "openLoc(")
check_anchor("travel114 DEF", def_line - 225, "function openLoc(id, opts){")
check_anchor("travel114 WRAPPER", wrap_line, "openLoc")

# ---- rom176：4 個失敗錨點 ----
for n, sub in [(53306, "/* ===== v20a176 ROM176"),
               (53674, "function rom176ApplyGiftOverrides()"),
               (54813, "function addLocTalkGiftActs(add, L, npcId)"),
               (54907, "rom176TryIntercept(id)")]:
    check_anchor(f"rom176 錨 L{n}", n - 225, sub)

# ---- tang171／tang173：DEF 行 ----
for f in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    s = open(f, encoding='utf-8').read()
    m = re.search(r"len\(lines\) >= (\d+) and 'function openLoc\(id, opts\)\{' in lines\[(\d+)\]", s)
    n = int(m.group(1))
    check_anchor(f"{f} DEF", n - 225, "function openLoc(id, opts){")

# ---- gift185：總行數 ----
print(f"{'PASS' if len(NEW) == 60409 else 'FAIL'} gift185 總行數：工作版 {len(NEW)} 行（測試期望 60380，須改 60409）")
if len(NEW) != 60409:
    fails.append("gift185 total")

print()
print("FAILURES:", len(fails), fails if fails else "全部錨點純漂移，准改行號")
sys.exit(1 if fails else 0)
