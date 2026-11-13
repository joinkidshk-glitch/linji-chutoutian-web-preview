# -*- coding: utf-8 -*-
"""v20a195 resync：difflib 對位 pristine main (f2a6b0c) → work index.html，
核實漂移純粹係 v195 插入（5 處），再映射全部受影響靜態測試嘅行號釘。
v195 插入點（淨 +87 行：93 增 −6 刪）：
  (1) dlg106AweiStem 改讀最高紀錄（~L26800，淨 +4）
  (2) normalizeSaveObj 加 backfill 呼叫（~L33440，淨 +3）
  (3) resolvePlannedDay 殺青寫入點加 record 呼叫（~L38170，淨 +2）
  (4) enc79PlayerTier 之後加 enc195 四函數（~L52550，淨 +75）
  (5) failShootOverdue 寫入點加 record 呼叫（~L59290，淨 +3）
用法：python3 qa195/resync195.py
"""
import difflib, subprocess

def git_show(rev, path):
    return subprocess.check_output(["git", "show", "%s:%s" % (rev, path)],
                                   cwd="/home/hatch/workspace/linji-work195",
                                   text=True).split("\n")

old = git_show("f2a6b0c", "index.html")
new = open("/home/hatch/workspace/linji-work195/index.html", encoding="utf-8").read().split("\n")
print("old lines:", len(old) - 1, "new lines:", len(new) - 1, "net:", (len(new) - 1) - (len(old) - 1))

sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
# old(1-based) -> new(1-based)，只限 equal 區
mapping = {}
hunks = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1
    else:
        hunks.append((tag, i1 + 1, i2, j1 + 1, j2))
print("change hunks (old 1-based range -> new 1-based range):")
for tag, a1, a2, b1, b2 in hunks:
    print("  %s old L%d-%d -> new L%d-%d" % (tag, a1, a2, b1, b2))

ANCHORS = {
    "rom176": [6072, 31583, 53416, 53784, 54923, 55017],
    "tang152_1based": [31510, 31654, 25819],
    "tang171_173_DEF": [53961],
    "travel114_COUNT": [32184, 35680, 37807, 38888, 39322, 39325, 39356, 43911, 59046, 59224, 59367, 59388],
    "travel114_FREE": [24686, 28228, 30851, 30852, 30864, 30865, 30876, 30877, 30980, 40866, 43568, 43591,
                       53239, 53358, 53408, 53631, 53670, 53676, 53743, 53745, 53748, 53775, 54886, 55260,
                       55282, 55433, 57070, 58814, 58932, 58933, 58968, 58969, 58994, 59838],
    "travel114_DEF_WRAPPER": [54986, 44434],
    "kwan151": [31029, 31020, 27246, 31071, 31028, 27213],
    "text125": [27738, 27867, 33568],
}
print("\nanchor mapping (old -> new, content must match verbatim):")
bad = 0
for group, lines in ANCHORS.items():
    for ln in lines:
        nl = mapping.get(ln)
        if nl is None:
            print("  %s L%d -> ??? (line itself changed!)" % (group, ln))
            bad += 1
            continue
        same = old[ln - 1] == new[nl - 1]
        if not same:
            bad += 1
        print("  %s L%d -> L%d %s :: %s" % (group, ln, nl, "OK" if same else "CONTENT DIFF!",
              old[ln - 1].strip()[:100]))
print("\nBAD:", bad)
raise SystemExit(1 if bad else 0)
