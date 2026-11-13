#!/usr/bin/env python3
"""v20a160 M1 resync 核實：比對 pristine（e08a070）同工作版 index.html，
確認 M1 改動只係 L44997–45005 一段 replace（舊像素 data URI 1 行 → 新常數註解＋常數 6 行，
淨 ＋7 行；B 註解＋loader 原地改，行數不變），其後全部行號純漂移 ＋7。
核實：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同；COUNT 13／FREE 27 不變；
DEF 53562→53569、WRAPPER 44171 不變（佢喺改動點之前）。"""
import difflib, re, sys

OLD = "/home/hatch/workspace/pristine160/index.html"
NEW = "/home/hatch/workspace/linji-work160-m1/index.html"
a = open(OLD, encoding="utf-8").read().splitlines()
b = open(NEW, encoding="utf-8").read().splitlines()
print("pristine lines:", len(a), "work lines:", len(b), "delta:", len(b) - len(a))

sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
ops = [op for op in sm.get_opcodes() if op[0] != "equal"]
print("non-equal opcodes:", len(ops))
for tag, i1, i2, j1, j2 in ops:
    print(f"  {tag} old[{i1+1}..{i2}] new[{j1+1}..{j2}]")
    for ln in a[i1:i2][:2]:
        print("    - " + ln[:100])
    for ln in b[j1:j2][:8]:
        print("    + " + ln[:100])

# 44 個 openLoc( 呼叫點：新舊序列逐字一致（漂移後對位）
def calls(lines):
    return [ln for ln in lines if "openLoc(" in ln]
ca, cb = calls(a), calls(b)
print("openLoc call lines: pristine", len(ca), "work", len(cb), "identical:", ca == cb)

# 釘行內容對位：舊行號 +7（改動點之後）＝新行號內容逐行相同
pins_old = [32132, 35613, 37740, 38734, 39168, 39171, 39202, 43748,
            57592, 57759, 57902, 57923, 58373,
            24772, 28267, 30853, 30854, 30866, 30867, 30878, 30879, 30982,
            40707, 43405, 43428, 52437, 52556, 53449, 53831, 53853, 53988,
            55625, 57036, 57369, 57487, 57488, 57523, 57524, 57543, 57558,
            53562]
EDIT_AT = 45005  # M1 改動段尾行（新檔行號）；舊檔對應約 44998
bad = []
for ln in pins_old:
    shift = 7 if ln >= 44998 else 0
    new_ln = ln + shift
    if a[ln - 1] != b[new_ln - 1]:
        bad.append((ln, new_ln, a[ln - 1][:60], b[new_ln - 1][:60]))
print("pinned lines checked:", len(pins_old), "mismatched:", len(bad))
for x in bad:
    print("  MISMATCH", x)
print("DEF old 53562 -> new", 53562 + 7, ":", b[53562 + 7 - 1][:60])
print("WRAPPER old 44171 (before edit) ->", b[44171 - 1][:60])
ok = (len(b) - len(a) == 7
      and all(op[0] == "replace" for op in ops)
      and sum((op[4] - op[3]) - (op[2] - op[1]) for op in ops) == 7
      and ca == cb and not bad)
print("RESYNC-OK" if ok else "RESYNC-FAIL")
sys.exit(0 if ok else 1)
