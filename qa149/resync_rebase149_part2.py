#!/usr/bin/env python3
# qa149/resync_rebase149_part2.py — 續 resync_rebase149.py（該腳本喺 travel114 頭註
# anchor 斷言停咗；text125＋travel114 set／DEF／WRAPPER 已寫入）。只做餘下四項：
# travel114 頭註、kwan151、tang152、tang171。錨點映射同 part1（MISMATCH 0 已驗）。
import re
import sys


def exact_line(path, old_line, new_line, tag):
    s = open(path, encoding="utf-8").read()
    assert s.count(old_line) == 1, "%s %s: found %d" % (path, tag, s.count(old_line))
    open(path, "w", encoding="utf-8").write(s.replace(old_line, new_line))
    print("%s: %s" % (path, tag))


# travel114 頭註加 v149 resync 紀錄（接喺 v165 (c) 行之後）
s = open("tests/test_travel114_static.py", encoding="utf-8").read()
anchor = "# v20a165 (c) resync：(c) 3 hunks 淨 ＋31 行（story165ModalOpen helper ＋15／book70ExitHome 掛點 ＋7／#loc-close 包裝 −1＋10；modal 閘由 CanPlay 移出，見 NOTES §9）；qa165/resync_travel114_165c.py 核實：difflib 對 HEAD 只得 3 個 hunks，其餘純漂移；COUNT 13／FREE 27 不變，openLoc( 呼叫點總數 44 不變，DEF 53668→53690、WRAPPER 44150→44172。\n"
assert s.count(anchor) == 1, "travel114 anchor"
note = "# v20a149 rebase 上 main 6d08c7c（v171）resync：淨 ＋97 行（CSS ＋13／JS ＋84；difflib 核實 40 個釘行內容逐行相同，純漂移；qa149/resync_rebase149.py）；COUNT 13／FREE 27 不變，DEF 53690→53787、WRAPPER 44172→44185。\n"
open("tests/test_travel114_static.py", "w", encoding="utf-8").write(s.replace(anchor, anchor + note))
print("tests/test_travel114_static.py: 頭註加 v149 resync 紀錄")

# kwan151：13 個錨點＋13（只改非註解行嘅 line(N)／L(N)）
k151 = {25569: 25582, 25906: 25919, 25909: 25922, 25910: 25923, 25911: 25924,
        25954: 25967, 26173: 26186, 27114: 27127, 27147: 27160, 30897: 30910,
        30905: 30918, 30906: 30919, 30948: 30961}
lines = open("tests/test_kwan151_static.py", encoding="utf-8").read().split("\n")
n1 = n2 = 0
for i, ln in enumerate(lines):
    if ln.lstrip().startswith("#"):
        continue
    ln2, c1 = re.subn(r"line\((\d+)\)",
                      lambda m: "line(%d)" % k151[int(m.group(1))] if int(m.group(1)) in k151 else m.group(0), ln)
    ln2, c2 = re.subn(r"L(\d{5})",
                      lambda m: "L%d" % k151[int(m.group(1))] if int(m.group(1)) in k151 else m.group(0), ln2)
    n1 += c1
    n2 += c2
    lines[i] = ln2
open("tests/test_kwan151_static.py", "w", encoding="utf-8").write("\n".join(lines))
print("tests/test_kwan151_static.py: line() %d 處／L 標籤 %d 處" % (n1, n2))
s = open("tests/test_kwan151_static.py", encoding="utf-8").read()
anchor = "# v20a157 rebase 上 main 60b0a8f resync：splice 插入令錨點漂移（＜30831 者 ＋24、≥30831 者 ＋66；qa131/resync_rebase157.py difflib 對位核實：13 個錨點內容逐字相同，純漂移）。\n"
assert s.count(anchor) == 1, "kwan151 anchor"
note = "# v20a149 rebase 上 main 6d08c7c（v171）resync：CSS ＋13，13 個錨點一律 ＋13（qa149/resync_rebase149.py difflib 對位核實內容逐字相同，純漂移）。\n"
open("tests/test_kwan151_static.py", "w", encoding="utf-8").write(s.replace(anchor, anchor + note))
print("tests/test_kwan151_static.py: 頭註加 v149 resync 紀錄")

# tang152：3 個錨點＋13（lines()[idx] 0-based；ok() 名 L 行號一併更新）
t152 = {25725: 25738, 31387: 31400, 31531: 31544}
lines = open("tests/test_tang152_static.py", encoding="utf-8").read().split("\n")
n1 = n2 = 0
for i, ln in enumerate(lines):
    if ln.lstrip().startswith("#"):
        continue
    ln2, c1 = re.subn(r"lines\(\)\[(\d+)\]",
                      lambda m: "lines()[%d]" % (t152[int(m.group(1)) + 1] - 1) if (int(m.group(1)) + 1) in t152 else m.group(0), ln)
    ln2, c2 = re.subn(r"L(\d{5})",
                      lambda m: "L%d" % t152[int(m.group(1))] if int(m.group(1)) in t152 else m.group(0), ln2)
    n1 += c1
    n2 += c2
    lines[i] = ln2
open("tests/test_tang152_static.py", "w", encoding="utf-8").write("\n".join(lines))
print("tests/test_tang152_static.py: lines()[] %d 處／L 標籤 %d 處" % (n1, n2))
s = open("tests/test_tang152_static.py", encoding="utf-8").read()
anchor = "# v20a157 rebase 上 main 60b0a8f resync：splice 插入令三個錨點漂移（HELD ＋24、normaliser／loader ＋66；qa131/resync_rebase157.py difflib 對位核實內容逐字相同，純漂移；ok() 名全形括號標籤一併更新）。\n"
assert s.count(anchor) == 1, "tang152 anchor"
note = "# v20a149 rebase 上 main 6d08c7c（v171）resync：CSS ＋13，三個錨點一律 ＋13（qa149/resync_rebase149.py difflib 對位核實內容逐字相同，純漂移；ok() 名標籤一併更新）。\n"
open("tests/test_tang152_static.py", "w", encoding="utf-8").write(s.replace(anchor, anchor + note))
print("tests/test_tang152_static.py: 頭註加 v149 resync 紀錄")

# tang171：總行數 59171→59268、DEF 53690→53787（零漂移斷言跟新 main）
exact_line("tests/test_tang171_static.py",
           "#      同行加呼叫），總行數 59171 不變，openLoc DEF 行 53690 不變——",
           "#      同行加呼叫），總行數 59171 不變，openLoc DEF 行 53690 不變——\n# v20a149 rebase 上 main 6d08c7c resync：淨 ＋97 行（CSS ＋13／JS ＋84），總行數 59171→59268、DEF 53690→53787；其餘斷言唔郁。",
           "tang171 header note")
exact_line("tests/test_tang171_static.py",
           "ok('零行數漂移：總行數 59171', src.count('\\n') == 59171)",
           "ok('零行數漂移：總行數 59268（v149 rebase ＋97）', src.count('\\n') == 59268)",
           "tang171 total check")
exact_line("tests/test_tang171_static.py",
           "ok('零行數漂移：openLoc DEF 行 53690 不變（travel114 釘行）',",
           "ok('零行數漂移：openLoc DEF 行 53787（v149 rebase ＋97，travel114 釘行）',",
           "tang171 DEF check name")
exact_line("tests/test_tang171_static.py",
           "   len(lines) >= 53690 and 'function openLoc(id, opts){' in lines[53689])",
           "   len(lines) >= 53787 and 'function openLoc(id, opts){' in lines[53786])",
           "tang171 DEF check body")
print("PART2 DONE")
