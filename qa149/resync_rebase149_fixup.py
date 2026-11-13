#!/usr/bin/env python3
# qa149/resync_rebase149_fixup.py — 續 resync_rebase149.py＋part2。
# 原因：合併 reveal 行嗰陣由一行融合成兩行原文（v149 spawn＋v160 audio 各留原文，
# test_awards149.js 逐字檢查先 PASS），index.html 淨 ＋97→＋98；reveal 行（~46616）
# 之後嘅釘行要再 ＋1。更新用單次掃描 dict 查表（防撞值：57728→57729 同時
# 57729→57730、57764→57765 同時 57765→57766）。
# 用法：python3 qa149/resync_rebase149_fixup.py（在工作副本根目錄執行）
import difflib
import re
import sys

old = open("/tmp/main149_index.html", encoding="utf-8").read().split("\n")
new = open("index.html", encoding="utf-8").read().split("\n")
print("old %d new %d net %+d" % (len(old), len(new), len(new) - len(old)))
assert len(new) - len(old) == 98

sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1

# 受影響釘行（main 行號→新行號），逐行驗內容逐字相同
pins = {
    "travel114 DEF": 53690,
    "travel114 COUNT": [57738, 57905, 58048, 58069, 58519],
    "travel114 FREE": [52565, 52684, 53577, 53959, 53981, 54132, 55769, 57180,
                       57513, 57631, 57632, 57667, 57668, 57687, 57702],
    "tang171 DEF": 53690,
}
bad = 0
newvals = {}
for name, v in pins.items():
    vals = v if isinstance(v, list) else [v]
    for ln in vals:
        nl = mapping.get(ln)
        same = nl is not None and old[ln - 1] == new[nl - 1]
        if not same:
            bad += 1
        newvals[ln] = nl
        print("%-18s %5d -> %-5s %s" % (name, ln, nl, "SAME" if same else "MISMATCH"))
print("MISMATCH: %d" % bad)
assert bad == 0
# 當前檔內值（resync 後）→ 新值：current = newvals[main] - 1（reveal 拆行之前嗰版）
fix = {}
for main_ln, nl in newvals.items():
    fix[nl - 1] = nl
print("fix map (current->new):", fix)


def exact_line(path, old_line, new_line, tag):
    s = open(path, encoding="utf-8").read()
    assert s.count(old_line) == 1, "%s %s: found %d" % (path, tag, s.count(old_line))
    open(path, "w", encoding="utf-8").write(s.replace(old_line, new_line))
    print("%s: %s" % (path, tag))


# travel114：set 元素（行首 5 位數字＋逗號）單次掃描查表
s = open("tests/test_travel114_static.py", encoding="utf-8").read()
s2, n = re.subn(r"(?m)^(\s*)(\d{5})(,)",
                lambda m: m.group(1) + str(fix[int(m.group(2))]) + m.group(3)
                if int(m.group(2)) in fix else m.group(0), s)
open("tests/test_travel114_static.py", "w", encoding="utf-8").write(s2)
print("tests/test_travel114_static.py: set 元素 %d 處掃描（%d 處改動）" % (n, sum(1 for k in fix if str(k) in s)))
exact_line("tests/test_travel114_static.py",
           "DEF_LINE = 53787      # function openLoc(id, opts){",
           "DEF_LINE = 53788      # function openLoc(id, opts){", "DEF_LINE +1")
# 頭註數字更正（＋97→＋98、DEF →53788、JS ＋84→＋85）
exact_line("tests/test_travel114_static.py",
           "# v20a149 rebase 上 main 6d08c7c（v171）resync：淨 ＋97 行（CSS ＋13／JS ＋84；difflib 核實 40 個釘行內容逐行相同，純漂移；qa149/resync_rebase149.py）；COUNT 13／FREE 27 不變，DEF 53690→53787、WRAPPER 44172→44185。",
           "# v20a149 rebase 上 main 6d08c7c（v171）resync：淨 ＋98 行（CSS ＋13／JS ＋85；difflib 核實 40 個釘行內容逐行相同，純漂移；qa149/resync_rebase149.py＋fixup；reveal 行拆兩行原文令 ＋97→＋98）；COUNT 13／FREE 27 不變，DEF 53690→53788、WRAPPER 44172→44185。",
           "travel114 header note +1")

# tang171：總行數＋DEF
exact_line("tests/test_tang171_static.py",
           "# v20a149 rebase 上 main 6d08c7c resync：淨 ＋97 行（CSS ＋13／JS ＋84），總行數 59171→59268、DEF 53690→53787；其餘斷言唔郁。",
           "# v20a149 rebase 上 main 6d08c7c resync：淨 ＋98 行（CSS ＋13／JS ＋85），總行數 59171→59269、DEF 53690→53788；其餘斷言唔郁。",
           "tang171 header note +1")
exact_line("tests/test_tang171_static.py",
           "ok('零行數漂移：總行數 59268（v149 rebase ＋97）', src.count('\\n') == 59268)",
           "ok('零行數漂移：總行數 59269（v149 rebase ＋98）', src.count('\\n') == 59269)",
           "tang171 total check +1")
exact_line("tests/test_tang171_static.py",
           "ok('零行數漂移：openLoc DEF 行 53787（v149 rebase ＋97，travel114 釘行）',",
           "ok('零行數漂移：openLoc DEF 行 53788（v149 rebase ＋98，travel114 釘行）',",
           "tang171 DEF check name +1")
exact_line("tests/test_tang171_static.py",
           "   len(lines) >= 53787 and 'function openLoc(id, opts){' in lines[53786])",
           "   len(lines) >= 53788 and 'function openLoc(id, opts){' in lines[53787])",
           "tang171 DEF check body +1")
print("FIXUP DONE — net +98")
