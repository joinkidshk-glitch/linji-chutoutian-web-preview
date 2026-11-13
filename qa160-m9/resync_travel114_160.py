#!/usr/bin/env python3
# qa160-m9/resync_travel114_160.py — v20a160 M9 後 travel114 行號再實量。
# 改動：index.html 喺 awards62PlayCeremony 之前插入 M9 helper（淨 +41 行；reveal 觸發行
# 1 行換 1 行，行數不變）。舊版＝pristine main e08a070，新版＝工作副本現版。
# 做法：difflib 對位，逐個釘行映射去新行號、驗內容逐字相同；44 個 openLoc( 呼叫點
# 序列逐字一致先算純漂移。只印映射，唔改測試檔——核實後人手更新測試檔釘行。
# 用法：在 ~/workspace/linji-work160-m9 執行：python3 qa160-m9/resync_travel114_160.py
import difflib
import re
import sys

OLD_PATH = "/home/hatch/workspace/pristine160-m9/index.html"
NEW_PATH = "index.html"
TEST_PATH = "tests/test_travel114_static.py"

old_src = open(OLD_PATH, encoding="utf-8").read()
new_src = open(NEW_PATH, encoding="utf-8").read()
old_lines = old_src.split("\n")
new_lines = new_src.split("\n")
print("old lines: %d  new lines: %d  net: %+d" % (len(old_lines), len(new_lines), len(new_lines) - len(old_lines)))

sm = difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based
    else:
        print("CHANGE %s old %d-%d -> new %d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))

test_src = open(TEST_PATH, encoding="utf-8").read()

def parse_set(name):
    m = re.search(name + r"\s*=\s*\{([^}]*)\}", test_src, re.S)
    return sorted(int(x) for x in re.findall(r"\d+", m.group(1)))

count_old = parse_set("COUNT_LINES")
free_old = parse_set("FREE_LINES")
def_old = int(re.search(r"DEF_LINE = (\d+)", test_src).group(1))
wrap_old = int(re.search(r"WRAPPER_LINE = (\d+)", test_src).group(1))

fail = 0
new_pins = {}
for label, pins in (("COUNT", count_old), ("FREE", free_old), ("DEF", [def_old]), ("WRAP", [wrap_old])):
    new_pins[label] = []
    for ln in pins:
        nl = mapping.get(ln)
        ok = nl is not None and old_lines[ln - 1] == new_lines[nl - 1]
        if not ok:
            fail += 1
        new_pins[label].append(nl)
        print("%s %d -> %s %s" % (label, ln, nl, "OK" if ok else "MISMATCH"))

def calls(lines):
    return [(i + 1, l.strip()) for i, l in enumerate(lines) if "openLoc(" in l]

oc, nc = calls(old_lines), calls(new_lines)
print("openLoc call sites: old %d new %d" % (len(oc), len(nc)))
seq_ok = len(oc) == len(nc) and all(a[1] == b[1] for a, b in zip(oc, nc))
print("call-site content sequence identical:", seq_ok)
if not seq_ok:
    fail += 1
print("NEW PINS COUNT=%s" % (new_pins["COUNT"],))
print("NEW PINS FREE=%s" % (new_pins["FREE"],))
print("NEW PINS DEF=%s WRAP=%s" % (new_pins["DEF"][0], new_pins["WRAP"][0]))
print("RESULT " + ("FAIL (%d)" % fail if fail else "PASS"))
sys.exit(1 if fail else 0)
