#!/usr/bin/env python3
# qa160-m4/resync_travel114.py — v20a160-m4 行號再實量。
# 原因：index.html 淨 +35 行（CSS walkup 層 +5／beats walkup +8／PlayCeremony 其餘 +22），
# travel114＋text125 嘅死行號釘全部漂移，內容本身一字冇郁。
# 做法：pristine (e08a070) vs 工作版 difflib 對位，每個釘行由 equal-block 映射去新行號，
# 逐行驗內容逐字相同；只印映射，唔直接改測試檔（改檔用人手 edit，免重蹈 qa147 第一版 bug）。
# 用法：python3 qa160-m4/resync_travel114.py（在 ~/workspace/linji-work160-m4 執行）
import difflib
import re

OLD = "/home/hatch/workspace/pristine160m4/index.html"
NEW = "index.html"

old_lines = open(OLD, encoding="utf-8").read().split("\n")
new_lines = open(NEW, encoding="utf-8").read().split("\n")
print("old lines: %d  new lines: %d  net: %+d" % (len(old_lines), len(new_lines), len(new_lines) - len(old_lines)))

sm = difflib.SequenceMatcher(a=old_lines, b=new_lines, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based
    else:
        print("CHANGE %s old %d-%d -> new %d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))

test_src = open("/home/hatch/workspace/pristine160m4/tests/test_travel114_static.py", encoding="utf-8").read()

def parse_set(name):
    m = re.search(name + r"\s*=\s*\{([^}]*)\}", test_src, re.S)
    return sorted(int(x) for x in re.findall(r"\d+", m.group(1)))

def check_pins(label, pins):
    bad = 0
    for old in pins:
        new = mapping.get(old)
        same = new is not None and old_lines[old - 1] == new_lines[new - 1]
        print("%s %d -> %s %s" % (label, old, new, "SAME" if same else "MISMATCH!!"))
        if not same:
            bad += 1
    return bad

bad = 0
bad += check_pins("COUNT", parse_set("COUNT_LINES"))
bad += check_pins("FREE", parse_set("FREE_LINES"))
def_old = int(re.search(r"DEF_LINE = (\d+)", test_src).group(1))
wrap_old = int(re.search(r"WRAPPER_LINE = (\d+)", test_src).group(1))
bad += check_pins("DEF", [def_old])
bad += check_pins("WRAPPER", [wrap_old])

# text125 三個釘（pristine 原值，唔讀已更新嘅工作版測試檔）
t125 = [27800, 27913, 33516]
bad += check_pins("TEXT125", t125)

print("MISMATCHES: %d" % bad)
print("NEW COUNT:", sorted(mapping[p] for p in parse_set("COUNT_LINES")))
print("NEW FREE:", sorted(mapping[p] for p in parse_set("FREE_LINES")))
print("NEW DEF:", mapping[def_old], " NEW WRAPPER:", mapping[wrap_old])
print("NEW TEXT125:", {p: mapping[p] for p in t125})
