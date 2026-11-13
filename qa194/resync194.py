# -*- coding: utf-8 -*-
"""v20a194 resync：difflib 對位 pristine main (2374637) → work index.html，
核實漂移純粹係 v194 插入（4 處），再映射全部受影響靜態測試嘅行號釘。
v194 插入點（淨 +65 行：68 增 −3 刪）：
  (1) awards194ApplyMetaTip 函數＋註解（awards188ApplyNpOverlay 之後，舊 ~L45754，淨 +25）
  (2) queueAwardsOnSeasonWindow 拆閘（舊 L46070，閘行 → 3 行註解，淨 +2）
  (3) awardsCheck live_queue 探針＋meta_tip 核實（舊 ~L46305，淨 +37）
  (4) loadFreeplayFramework 加 meta tip 呼叫（舊 ~L49384，淨 +1）
分段漂移：舊行 ＜45755 者 +0；45755–46069 者 +25；46070–46304 者 +27；
          46305–49383 者 +64；≥49384 者 +65。
用法：python3 qa194/resync194.py
"""
import difflib
import re
import subprocess

ROOT = "/home/hatch/workspace/linji-work194"


def git_show(rev, path):
    return subprocess.check_output(["git", "show", "%s:%s" % (rev, path)],
                                   cwd=ROOT, text=True).split("\n")


old = git_show("2374637", "index.html")
new = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
print("old lines:", len(old) - 1, "new lines:", len(new) - 1,
      "net:", (len(new) - 1) - (len(old) - 1))

sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
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


def ints_from_test(path, var):
    txt = open(ROOT + "/" + path, encoding="utf-8").read()
    m = re.search(re.escape(var) + r"\s*=\s*\{([^}]*)\}", txt, re.S)
    if not m:
        raise SystemExit("var not found: %s in %s" % (var, path))
    return sorted(int(x) for x in re.findall(r"\b\d+\b", m.group(1)))


ANCHORS = {
    "rom176": [31587, 53532, 53900, 55039, 55133],
    "tang_DEF": [55102],
    "travel114_COUNT": ints_from_test("tests/test_travel114_static.py", "COUNT_LINES"),
    "travel114_FREE": ints_from_test("tests/test_travel114_static.py", "FREE_LINES"),
    "travel114_DEF_WRAPPER": [55102, 44443],
}
print("\nanchor mapping (old -> new, content must match verbatim):")
bad = 0
newnums = {}
for group, lines in ANCHORS.items():
    newnums[group] = []
    for ln in lines:
        nl = mapping.get(ln)
        if nl is None:
            print("  %s L%d -> ??? (line itself changed!)" % (group, ln))
            bad += 1
            continue
        same = old[ln - 1] == new[nl - 1]
        if not same:
            bad += 1
        newnums[group].append(nl)
        print("  %s L%d -> L%d %s :: %s" % (group, ln, nl, "OK" if same else "CONTENT DIFF!",
              old[ln - 1].strip()[:100]))
print("\nnew numbers:")
for group, lines in newnums.items():
    print("  %s: %s" % (group, lines))
print("\nBAD:", bad)
raise SystemExit(1 if bad else 0)
