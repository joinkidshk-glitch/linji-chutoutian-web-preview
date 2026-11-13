#!/usr/bin/env python3
# qa149/resync_rebase149_fixup2.py — 續 fixup。
# 原因：reveal 行由兩行拆分改返一行融合（同時滿足 awards149＋m9 兩檔逐字檢查），
# index.html 淨 ＋98→＋97；reveal 行（~46616）之後嘅釘行要再 −1，返去 resync
# 原值。更新用單次掃描 dict 查表（防撞值：57729→57728 同時 57730→57729、
# 57765→57764 同時 57766→57765）。
# 用法：python3 qa149/resync_rebase149_fixup2.py（在工作副本根目錄執行）
import difflib
import re
import sys

old = open("/tmp/main149_index.html", encoding="utf-8").read().split("\n")
new = open("index.html", encoding="utf-8").read().split("\n")
print("old %d new %d net %+d" % (len(old), len(new), len(new) - len(old)))
assert len(new) - len(old) == 97

sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1

# 全部釘行（main 行號→期望新行號，即 resync 原值），逐行驗內容逐字相同
pins = {
    "text125 currentLine": (27639, 27652),
    "text125 advance": (27752, 27765),
    "text125 familySafe": (33445, 33458),
    "travel114 DEF": (53690, 53787),
    "travel114 WRAPPER": (44172, 44185),
    "travel114 COUNT": [(32061, 32074), (35542, 35555), (37669, 37682), (38735, 38748),
                        (39169, 39182), (39172, 39185), (39203, 39216), (43753, 43766),
                        (57738, 57835), (57905, 58002), (58048, 58145), (58069, 58166),
                        (58519, 58616)],
    "travel114 FREE": [(24612, 24625), (28106, 28119), (30728, 30741), (30729, 30742),
                       (30741, 30754), (30742, 30755), (30753, 30766), (30754, 30767),
                       (30857, 30870), (40708, 40721), (43410, 43423), (43433, 43446),
                       (52565, 52662), (52684, 52781), (53577, 53674), (53959, 54056),
                       (53981, 54078), (54132, 54229), (55769, 55866), (57180, 57277),
                       (57513, 57610), (57631, 57728), (57632, 57729), (57667, 57764),
                       (57668, 57765), (57687, 57784), (57702, 57799)],
    "kwan151": [(25569, 25582), (25906, 25919), (25909, 25922), (25910, 25923),
                (25911, 25924), (25954, 25967), (26173, 26186), (27114, 27127),
                (27147, 27160), (30897, 30910), (30905, 30918), (30906, 30919),
                (30948, 30961)],
    "tang152": [(25725, 25738), (31387, 31400), (31531, 31544)],
    "tang171 DEF": (53690, 53787),
}
bad = 0
for name, v in pins.items():
    pairs = v if isinstance(v, list) else [v]
    for main_ln, want in pairs:
        nl = mapping.get(main_ln)
        same = nl == want and old[main_ln - 1] == new[nl - 1]
        if not same:
            bad += 1
            print("MISMATCH %-18s %5d -> %-5s want %-5s" % (name, main_ln, nl, want))
print("pins checked, MISMATCH: %d" % bad)
assert bad == 0
print("total newlines:", open("index.html", encoding="utf-8").read().count("\n"), "(want 59268)")


def exact_line(path, old_line, new_line, tag):
    s = open(path, encoding="utf-8").read()
    assert s.count(old_line) == 1, "%s %s: found %d" % (path, tag, s.count(old_line))
    open(path, "w", encoding="utf-8").write(s.replace(old_line, new_line))
    print("%s: %s" % (path, tag))


# travel114：reveal 行之後嘅 set 元素 −1（當前值＝期望＋1）→期望
fix = {}
for main_ln, want in pins["travel114 COUNT"] + pins["travel114 FREE"]:
    if want >= 52662:  # reveal 行（~46616）之後嘅先受影響（＋98 版值＝want＋1）
        fix[want + 1] = want
fix[53788] = 53787  # DEF
s = open("tests/test_travel114_static.py", encoding="utf-8").read()
s2, n = re.subn(r"(?m)^(\s*)(\d{5})(,)",
                lambda m: m.group(1) + str(fix[int(m.group(2))]) + m.group(3)
                if int(m.group(2)) in fix else m.group(0), s)
open("tests/test_travel114_static.py", "w", encoding="utf-8").write(s2)
print("tests/test_travel114_static.py: set 元素 %d 處掃描" % n)
exact_line("tests/test_travel114_static.py",
           "DEF_LINE = 53788      # function openLoc(id, opts){",
           "DEF_LINE = 53787      # function openLoc(id, opts){", "DEF_LINE -1")
exact_line("tests/test_travel114_static.py",
           "# v20a149 rebase 上 main 6d08c7c（v171）resync：淨 ＋98 行（CSS ＋13／JS ＋85；difflib 核實 40 個釘行內容逐行相同，純漂移；qa149/resync_rebase149.py＋fixup；reveal 行拆兩行原文令 ＋97→＋98）；COUNT 13／FREE 27 不變，DEF 53690→53788、WRAPPER 44172→44185。",
           "# v20a149 rebase 上 main 6d08c7c（v171）resync：淨 ＋97 行（CSS ＋13／JS ＋84；difflib 核實 40 個釘行內容逐行相同，純漂移；qa149/resync_rebase149.py＋fixup＋fixup2；reveal 行先拆兩行再融返一行，淨數返去 ＋97）；COUNT 13／FREE 27 不變，DEF 53690→53787、WRAPPER 44172→44185。",
           "travel114 header note -1")

# tang171：總行數＋DEF 返去 ＋97 版
exact_line("tests/test_tang171_static.py",
           "# v20a149 rebase 上 main 6d08c7c resync：淨 ＋98 行（CSS ＋13／JS ＋85），總行數 59171→59269、DEF 53690→53788；其餘斷言唔郁。",
           "# v20a149 rebase 上 main 6d08c7c resync：淨 ＋97 行（CSS ＋13／JS ＋84），總行數 59171→59268、DEF 53690→53787；其餘斷言唔郁。",
           "tang171 header note -1")
exact_line("tests/test_tang171_static.py",
           "ok('零行數漂移：總行數 59269（v149 rebase ＋98）', src.count('\\n') == 59269)",
           "ok('零行數漂移：總行數 59268（v149 rebase ＋97）', src.count('\\n') == 59268)",
           "tang171 total check -1")
exact_line("tests/test_tang171_static.py",
           "ok('零行數漂移：openLoc DEF 行 53788（v149 rebase ＋98，travel114 釘行）',",
           "ok('零行數漂移：openLoc DEF 行 53787（v149 rebase ＋97，travel114 釘行）',",
           "tang171 DEF check name -1")
exact_line("tests/test_tang171_static.py",
           "   len(lines) >= 53788 and 'function openLoc(id, opts){' in lines[53787])",
           "   len(lines) >= 53787 and 'function openLoc(id, opts){' in lines[53786])",
           "tang171 DEF check body -1")
print("FIXUP2 DONE — net +97, all pins back to resync values")
