#!/usr/bin/env python3
# qa149/resync_rebase149.py — v20a149 rebase 上 main 6d08c7c（v171）行號 resync。
# 做法：main index.html（/tmp/main149_index.html，git show HEAD:index.html）vs 合併後
# index.html difflib 對位；每個釘行由 equal-block 映射去新行號，逐行驗內容逐字相同
# （純漂移先改行號）。更新用單次掃描 dict 查表，唔逐對 re.sub（防撞值：例如
# FREE 30728＋13＝30741 本身係另一個舊釘行）。
# 用法：python3 qa149/resync_rebase149.py（在工作副本根目錄執行）
import difflib
import re
import sys

old_raw = open("/tmp/main149_index.html", encoding="utf-8").read()
new_raw = open("index.html", encoding="utf-8").read()
old = old_raw.split("\n")
new = new_raw.split("\n")
print("old lines: %d  new lines: %d  net: %+d" % (len(old), len(new), len(new) - len(old)))

sm = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1

# 全部釘行（1-based）：由各測試檔抽出
pins = {
    "text125 currentLine": 27639,
    "text125 advance": 27752,
    "text125 familySafe": 33445,
    "travel114 DEF": 53690,
    "travel114 WRAPPER": 44172,
    "travel114 COUNT": [32061, 35542, 37669, 38735, 39169, 39172, 39203, 43753,
                        57738, 57905, 58048, 58069, 58519],
    "travel114 FREE": [24612, 28106, 30728, 30729, 30741, 30742, 30753, 30754,
                       30857, 40708, 43410, 43433, 52565, 52684, 53577, 53959,
                       53981, 54132, 55769, 57180, 57513, 57631, 57632, 57667,
                       57668, 57687, 57702],
    "kwan151": [25569, 25906, 25909, 25910, 25911, 25954, 26173, 27114, 27147,
                30897, 30905, 30906, 30948],
    "tang152": [25725, 31387, 31531],
    "tang171 total": 59171,  # 總行數（檔尾計數，非釘行；驗 net ＋97）
    "tang171 DEF": 53690,
}
bad = 0
mapped = {}
for name, v in pins.items():
    vals = v if isinstance(v, list) else [v]
    for ln in vals:
        if name == "tang171 total":
            nl = new_raw.count("\n")  # 總行數＝換行符數（同測試 src.count('\n')）
            same = (new_raw.count("\n") - old_raw.count("\n") == 97)
            print("%-22s total %5d -> %-5d %s" % (name, ln, nl, "NET+97" if same else "MISMATCH"))
            if not same:
                bad += 1
            continue
        nl = mapping.get(ln)
        same = nl is not None and old[ln - 1] == new[nl - 1]
        if not same:
            bad += 1
        mapped[ln] = nl
        print("%-22s %5d -> %-5s %s | %s" % (name, ln, nl, "SAME" if same else "MISMATCH",
              old[ln - 1][:60] if ln <= len(old) else ""))
print("MISMATCH: %d" % bad)
if bad:
    sys.exit(1)

# ---- 單次掃描更新（每檔一次 regex pass，dict 查表） ----
def sub_once(path, pattern, fn, count_note):
    s = open(path, encoding="utf-8").read()
    s2, n = re.subn(pattern, fn, s)
    assert n > 0, path + ": no match for " + count_note
    open(path, "w", encoding="utf-8").write(s2)
    print("%s: %d 處 %s" % (path, n, count_note))
    return s2

def exact_line(path, old_line, new_line, tag):
    s = open(path, encoding="utf-8").read()
    assert s.count(old_line) == 1, "%s %s: found %d" % (path, tag, s.count(old_line))
    open(path, "w", encoding="utf-8").write(s.replace(old_line, new_line))
    print("%s: %s" % (path, tag))

# text125：三個錨點＋13（check 行逐行精確替換；歷史註解唔郁，錨點註解尾加 v149 註）
t125 = {
    27639: 27652, 27752: 27765, 33445: 33458,
    27638: 27651, 27751: 27764, 33444: 33457, 33447: 33460,
}
exact_line("tests/test_text125_static.py",
           "    if len(ls) < 27639 or FALLBACK not in ls[27638]:",
           "    if len(ls) < 27652 or FALLBACK not in ls[27651]:", "currentLine check")
exact_line("tests/test_text125_static.py",
           '        probs.append("currentLine 第 27639 行冇 text fallback")  # v157 resync：27800→27824（splice ＋24）',
           '        probs.append("currentLine 第 27652 行冇 text fallback")  # v157 resync：27800→27824（splice ＋24）；v149 rebase ＋13：27639→27652', "currentLine msg")
exact_line("tests/test_text125_static.py",
           "    if len(ls) < 27752 or FALLBACK not in ls[27751]:",
           "    if len(ls) < 27765 or FALLBACK not in ls[27764]:", "advance check")
exact_line("tests/test_text125_static.py",
           '        probs.append("advance 第 27752 行冇 text fallback")  # v157 resync：27913→27937（splice ＋24）',
           '        probs.append("advance 第 27765 行冇 text fallback")  # v157 resync：27913→27937（splice ＋24）；v149 rebase ＋13：27752→27765', "advance msg")
exact_line("tests/test_text125_static.py",
           "    if len(ls) < 33447 or 'if(typeof b.text === \"string\" && b.text){' not in ls[33444]:",
           "    if len(ls) < 33460 or 'if(typeof b.text === \"string\" && b.text){' not in ls[33457]:", "familySafe check")
exact_line("tests/test_text125_static.py",
           '        probs.append("applyFamilySafeToNode 第 33445 行冇 b.text 分支")  # v157 resync：33516→33582（splice ＋66）',
           '        probs.append("applyFamilySafeToNode 第 33458 行冇 b.text 分支")  # v157 resync：33516→33582（splice ＋66）；v149 rebase ＋13：33445→33458', "familySafe msg")

# travel114：COUNT／FREE set 元素（行首 5 位數字＋逗號）單次掃描查表
t114 = {ln: mapped[ln] for ln in pins["travel114 COUNT"] + pins["travel114 FREE"]}
t114[53690] = 53787
t114[44172] = 44185
sub_once("tests/test_travel114_static.py", r"(?m)^(\s*)(\d{5})(,)",
         lambda m: m.group(1) + str(t114[int(m.group(2))]) + m.group(3)
         if int(m.group(2)) in t114 else m.group(0), "set 元素行號")
exact_line("tests/test_travel114_static.py",
           "DEF_LINE = 53690      # function openLoc(id, opts){",
           "DEF_LINE = 53787      # function openLoc(id, opts){", "DEF_LINE")
exact_line("tests/test_travel114_static.py",
           "WRAPPER_LINE = 44172  # window.__phase2.openLoc：轉發 opts",
           "WRAPPER_LINE = 44185  # window.__phase2.openLoc：轉發 opts", "WRAPPER_LINE")
# 頭註加 v149 resync 紀錄（接喺 v165 (c) 行之後）
s = open("tests/test_travel114_static.py", encoding="utf-8").read()
anchor = "# v20a165 (c) resync：(c) 3 hunks 淨 ＋31 行（story165ModalOpen helper ＋15／book70ExitHome 掛點 ＋7／#loc-close 包裝 −1＋10；modal 閘由 CanPlay 移出，見 NOTES §9）；qa165/resync_travel114_165c.py 核實：difflib 對 HEAD 只得 3 個 hunks，其餘純漂移；COUNT 13／FREE 27 不變，openLoc( 呼叫點總數 44 不變，DEF 53668→53690、WRAPPER 44150→44172。\n"
assert s.count(anchor) == 1, "travel114 anchor"
note = "# v20a149 rebase 上 main 6d08c7c（v171）resync：淨 ＋97 行（CSS ＋13／JS ＋84；difflib 核實 40 個釘行內容逐行相同，純漂移；qa149/resync_rebase149.py）；COUNT 13／FREE 27 不變，DEF 53690→53787、WRAPPER 44172→44185。\n"
open("tests/test_travel114_static.py", "w", encoding="utf-8").write(s.replace(anchor, anchor + note))
print("tests/test_travel114_static.py: 頭註加 v149 resync 紀錄")

# kwan151：13 個錨點＋13（只改非註解行嘅 line(N)／L(N)）
k151 = {ln: mapped[ln] for ln in pins["kwan151"]}
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
t152 = {ln: mapped[ln] for ln in pins["tang152"]}
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
print("tests/test_tang152_static.py: lines()[%d] %d 處／L 標籤 %d 處" % (0, n1, n2))
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
print("ALL RESYNC DONE — MISMATCH 0")
