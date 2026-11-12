#!/usr/bin/env python3
# v20a119 travel114 行號 resync：DLG119 剪影模組令 index.html 淨 +152 行
# （CSS 4877 起 +15、GAZE／DLG119 模組／LEGACY／REG／pair 去重／chars 25979–27386
# 起累積至 +152），test_travel114_static.py 寫死嘅 FREE／COUNT／DEF／WRAPPER
# 行號要跟住漂移。本腳本用 difflib 對位舊 main 同新版逐行核實：全部 44 個
# openLoc( 呼叫點內容逐字一致、次序一致（純漂移），COUNT 13／FREE 27 不變，
# 再印出新行號畀測試檔用。
# 用法：python3 qa119/resync_travel114.py [old-index.html] [new-index.html]
# 預設 old＝pristine main（git show origin/main:index.html 抽出），new＝工作副本 index.html。
import difflib, subprocess, sys, tempfile, os

def read_old(path):
    if path:
        return open(path, encoding="utf-8").read().split("\n")
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        tmp = f.name
    subprocess.run(["git", "show", "origin/main:index.html"],
                   stdout=open(tmp, "w", encoding="utf-8"), check=True)
    lines = open(tmp, encoding="utf-8").read().split("\n")
    os.remove(tmp)
    return lines

old = read_old(sys.argv[1] if len(sys.argv) > 1 else None)
new = open(sys.argv[2] if len(sys.argv) > 2 else "index.html",
           encoding="utf-8").read().split("\n")
print("old lines: %d  new lines: %d  delta: %+d" % (len(old), len(new), len(new) - len(old)))

sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1
    else:
        print("  %s: old %d-%d -> new %d-%d" % (tag, i1 + 1, i2, j1 + 1, j2))

FREE = [24282, 27602, 30202, 30203, 30215, 30216, 30227, 30228, 30331, 39891,
        42589, 42612, 51400, 51488, 52379, 52764, 52786, 52921, 54550, 55960,
        56287, 56405, 56406, 56441, 56442, 56461, 56476]
COUNT = [31481, 34932, 37046, 38044, 38400, 38403, 38434, 42932, 56510, 56677,
         56820, 56841, 57291]
DEF, WRAP = 52492, 43344

bad = 0
def remap(name, lines):
    global bad
    out = []
    for ln in lines:
        nl = mapping.get(ln)
        ok = nl is not None and old[ln - 1] == new[nl - 1]
        if not ok:
            bad += 1
            print("  !! %s %d -> %s 內容唔一致" % (name, ln, nl))
        out.append(nl)
    return out

free_new = remap("FREE", FREE)
count_new = remap("COUNT", COUNT)
def_new = remap("DEF", [DEF])[0]
wrap_new = remap("WRAP", [WRAP])[0]

oc = [l.strip() for l in old if "openLoc(" in l]
nc = [l.strip() for l in new if "openLoc(" in l]
print("openLoc( 行數 old=%d new=%d；內容次序逐字一致：%s" % (len(oc), len(nc), oc == nc))
if oc != nc:
    bad += 1
print("FREE new  =", sorted(free_new))
print("COUNT new =", sorted(count_new))
print("DEF new   =", def_new, " WRAP new =", wrap_new)
print("RESULT " + ("FAIL" if bad else "PASS"))
sys.exit(1 if bad else 0)
