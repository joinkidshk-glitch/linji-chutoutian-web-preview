"""Re-sync test_travel114_static.py + test_text125_static.py line numbers for v20a146 2nd rebase.
基底：f45e766（v145 main）版測試檔＋index.html；目標：rebase 後工作區 index.html
（f45e766 ＋ v146 commit 1：A1 .mask fixed＋svh 高帽、B2 market 分流）。
做法（按慣例：difflib 對位核實純漂移先改行號）：
- difflib.SequenceMatcher(OLD, NEW) 建 equal-block 行號映射；每個釘行必須落喺 equal block，
  內容逐字相同，且前後 3 行 context 相同，先至接受新行號。
- travel114 另加 openLoc( 全序列逐字一致檢查（同 v122/v128/v144 做法）；DEF／WRAPPER 直接搜尋核對。
- text125 三錨點由 f45e766 版解析（唔 hardcode 79defe3 舊數）：currentLine 27790、advance 27903、
  familySafe 33506（上界 33508）。
- B2 分界線：OLD 入面 'const sceneHtml105 = scene105 ?' 嗰行；釘行 ＜分界 ＋10、≥分界 ＋15；
  每個釘行嘅實量 shift 必須同呢個預期一致，否則停低。
用法：python3 qa146/resync_rebase146b.py [--apply]
無 --apply：只印對位結果。--apply：由 f45e766 版測試檔出發，寫新行號入工作區兩個測試檔。
"""
import difflib, re, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work146"
BASE = "f45e766"
OLD = subprocess.run(["git", "show", BASE + ":index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
print("OLD (%s index.html) lines: %d  NEW (rebased worktree) lines: %d  net: %+d"
      % (BASE, len(OLD), len(NEW), len(NEW) - len(OLD)))

sm = difflib.SequenceMatcher(None, OLD, NEW, autojunk=False)
mapping = {}
non_equal = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1
    else:
        non_equal.append((tag, i1 + 1, i2, j1 + 1, j2))
print("non-equal opcodes (tag, old_start, old_end, new_start, new_end):")
for op in non_equal:
    print("  ", op)
# 預期 5 個非 equal 區：.mask 段、tut-on svh、modal 高帽註解＋行、88dvh svh、B2 段。


def remap(old_line, label, expect_sub=None):
    assert old_line in mapping, "%s: old line %d not in an equal block!" % (label, old_line)
    new_line = mapping[old_line]
    assert OLD[old_line - 1] == NEW[new_line - 1], \
        "%s: content differs old %d vs new %d" % (label, old_line, new_line)
    assert OLD[old_line - 4:old_line + 3] == NEW[new_line - 4:new_line + 3], \
        "%s: context differs around old %d" % (label, old_line)
    if expect_sub is not None:
        assert expect_sub in NEW[new_line - 1], \
            "%s: new line %d lacks expected substring" % (label, new_line)
    print("  %-28s %6d -> %6d  (+%d)  %s"
          % (label, old_line, new_line, new_line - old_line, OLD[old_line - 1].strip()[:70]))
    return new_line


# B2 分界線：OLD 入面 sceneHtml105 原行（B2 註解＋分流插喺佢前面，呢行本身被改寫）。
split_candidates = [i + 1 for i, l in enumerate(OLD)
                    if "const sceneHtml105 = scene105 ?" in l]
assert len(split_candidates) == 1, "sceneHtml105 line not unique: %s" % split_candidates
SPLIT = split_candidates[0]
print("B2 split (OLD line of sceneHtml105): %d" % SPLIT)


def check_shift(old_line, new_line, label):
    want = 10 if old_line < SPLIT else 15
    assert new_line - old_line == want, \
        "%s: shift %d != expected %+d (split %d)" % (label, new_line - old_line, want, SPLIT)


# ---------- travel114 ----------
TEST114 = subprocess.run(["git", "show", BASE + ":tests/test_travel114_static.py"], cwd=ROOT,
                         capture_output=True, text=True).stdout

def parse_set(name):
    m = re.search(name + r" = \{([^}]*)\}", TEST114, re.S)
    nums, comments = [], {}
    for line in m.group(1).split("\n"):
        code = line.split("#", 1)[0]
        found = [int(x) for x in re.findall(r"\d+", code)]
        if not found:
            continue
        nums.extend(found)
        if "#" in line:
            comments[found[-1]] = line.split("#", 1)[1].strip()
    return nums, comments

count_nums, count_c = parse_set("COUNT_LINES")
free_nums, free_c = parse_set("FREE_LINES")
def_old = int(re.search(r"DEF_LINE = (\d+)", TEST114).group(1))
wrap_old = int(re.search(r"WRAPPER_LINE = (\d+)", TEST114).group(1))
print("\nbase anchors: COUNT %d FREE %d DEF %d WRAPPER %d"
      % (len(count_nums), len(free_nums), def_old, wrap_old))

old_hits = [(i + 1, l.strip()) for i, l in enumerate(OLD) if "openLoc(" in l]
new_hits = [(i + 1, l.strip()) for i, l in enumerate(NEW) if "openLoc(" in l]
print("openLoc( lines: old %d new %d" % (len(old_hits), len(new_hits)))
assert [s for _, s in old_hits] == [s for _, s in new_hits], \
    "openLoc( SEQUENCE DIFFERS — not a pure shift, stop!"
print("openLoc( sequence identical: pure line shift confirmed")
seq_pos = {o: n for (o, _), (n, _) in zip(old_hits, new_hits)}

print("\nCOUNT_LINES remap:")
count_new = {}
for n in sorted(count_nums):
    nn = remap(n, "COUNT %d" % n)
    assert seq_pos[n] == nn, "COUNT %d: difflib %d != sequence %d" % (n, nn, seq_pos[n])
    check_shift(n, nn, "COUNT %d" % n)
    count_new[n] = nn
print("FREE_LINES remap:")
free_new = {}
for n in sorted(free_nums):
    nn = remap(n, "FREE %d" % n)
    assert seq_pos[n] == nn, "FREE %d: difflib %d != sequence %d" % (n, nn, seq_pos[n])
    check_shift(n, nn, "FREE %d" % n)
    free_new[n] = nn
def_new = remap(def_old, "DEF_LINE", "function openLoc(id, opts){")
check_shift(def_old, def_new, "DEF_LINE")
wrap_new = remap(wrap_old, "WRAPPER_LINE", "openLoc: function(id, opts){ openLoc(id, opts); }")
check_shift(wrap_old, wrap_new, "WRAPPER_LINE")
d = [i + 1 for i, l in enumerate(NEW) if "function openLoc(id, opts){" in l]
w = [i + 1 for i, l in enumerate(NEW) if "openLoc: function(id, opts){ openLoc(id, opts); }" in l]
print("direct-search DEF_LINE:", d, " WRAPPER_LINE:", w)
assert d == [def_new] and w == [wrap_new]
print("travel114: COUNT %d FREE %d, all pure drift, shifts +10/＋15 split at %d"
      % (len(count_nums), len(free_nums), SPLIT))

# ---------- text125 ----------
TEST125 = subprocess.run(["git", "show", BASE + ":tests/test_text125_static.py"], cwd=ROOT,
                         capture_output=True, text=True).stdout
t125_lines = TEST125.split("\n")
cur_old = adv_old = fam_old = fam_hi_old = None
for i, l in enumerate(t125_lines):
    if "FALLBACK not in ls[" in l:
        n = int(re.search(r"if len\(ls\) < (\d+)", l).group(1))
        if cur_old is None:
            cur_old = n
        else:
            adv_old = n
    if "if(typeof b.text" in l and "not in ls[" in l:
        fam_hi_old = int(re.search(r"if len\(ls\) < (\d+)", l).group(1))
        fam_old = int(re.search(r"not in ls\[(\d+)\]", l).group(1)) + 1
assert None not in (cur_old, adv_old, fam_old, fam_hi_old), \
    "text125 anchors not parsed: %s %s %s %s" % (cur_old, adv_old, fam_old, fam_hi_old)
print("\ntext125 base anchors: currentLine %d advance %d familySafe %d (bound %d)"
      % (cur_old, adv_old, fam_old, fam_hi_old))
print("text125 anchors remap:")
FALLBACK = '(typeof b.text === "string" && b.text ? [b.text] : [])'
cur_new = remap(cur_old, "currentLine", FALLBACK)
check_shift(cur_old, cur_new, "currentLine")
adv_new = remap(adv_old, "advance", FALLBACK)
check_shift(adv_old, adv_new, "advance")
fam_new = remap(fam_old, "familySafe", 'if(typeof b.text === "string" && b.text){')
check_shift(fam_old, fam_new, "familySafe")
fam_hi_new = remap(fam_hi_old, "familySafe bound", None)
assert fam_hi_new - fam_new == 2
print("text125: all three anchors pure drift (+10, B2 split %d is after all three)" % SPLIT)

# ---------- apply ----------
if "--apply" not in sys.argv:
    print("\nDRY RUN only — pass --apply to rewrite the two test files.")
    sys.exit(0)

out114 = TEST114
out114 = re.sub(r"COUNT_LINES = \{[^}]*\}",
                "COUNT_LINES = {\n" + "\n".join(
                    "    %d,%s" % (count_new[n], ("  # " + count_c[n]) if n in count_c else "")
                    for n in sorted(count_nums)) + "\n}",
                out114, count=1, flags=re.S)
out114 = re.sub(r"FREE_LINES = \{[^}]*\}",
                "FREE_LINES = {\n" + "\n".join(
                    "    %d,%s" % (free_new[n], ("  # " + free_c[n]) if n in free_c else "")
                    for n in sorted(free_nums)) + "\n}",
                out114, count=1, flags=re.S)
out114 = re.sub(r"DEF_LINE = \d+", "DEF_LINE = %d" % def_new, out114, count=1)
out114 = re.sub(r"WRAPPER_LINE = \d+", "WRAPPER_LINE = %d" % wrap_new, out114, count=1)
# allowlist 頭註加 v146 rebase 紀錄
old_tail = "；v20a145 BOOK145 ＋67 行（CSS 段，全部錨點再 ＋67） ----------"
assert old_tail in out114
out114 = out114.replace(old_tail,
    "；v20a145 BOOK145 ＋67 行（CSS 段，全部錨點再 ＋67）；v20a146 rebase：行號 ＜%d 者 ＋10、≥%d 者 ＋15（MASK146 CSS ＋8／modal 高帽 ＋2／B2 ＋5） ----------"
    % (SPLIT, SPLIT), 1)
# 頭註加 v146 rebase 紀錄（接喺 v142 行之後）
anchor142 = "# 行號按 difflib 對位逐行實量（COUNT 13／FREE 27 不變，DEF 53369→53402、WRAPPER 44054→44087）。\n"
assert anchor142 in out114
out114 = out114.replace(anchor142, anchor142 +
    "# v20a146 rebase 上 v145（f45e766）：MASK146 淨 ＋10 行（.mask CSS 段 ＋8／modal 高帽註解 ＋2）＋B2 淨 ＋5 行\n"
    "# （wf4PlayEvent 註解＋分流，約行 %d 後）；行號 ＜%d 者 ＋10、≥%d 者 ＋15。\n"
    "# qa146/resync_rebase146b.py 核實：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，\n"
    "# 純漂移（COUNT 13／FREE 27 不變，DEF %d→%d、WRAPPER %d→%d）。\n"
    % (SPLIT, SPLIT, SPLIT, def_old, def_new, wrap_old, wrap_new), 1)
open(ROOT + "/tests/test_travel114_static.py", "w", encoding="utf-8").write(out114)
print("\nAPPLIED: test_travel114_static.py resynced from %s base" % BASE)

# text125：逐行改（註解行號＋檢查行＋prob 字串），唔用全檔 replace。
def edit125(lines):
    out = []
    for l in lines:
        if "# ① currentLine fallback（行號 " in l:
            assert "v145 ＋67：BOOK145 CSS 段）" in l
            l = l.replace("行號 %d，" % cur_old, "行號 %d，" % cur_new)
            l = l.replace("；v145 ＋67：BOOK145 CSS 段）",
                          "；v145 ＋67：BOOK145 CSS 段；v146 rebase ＋10：MASK146 CSS 段 ＋8／modal 高帽註解 ＋2，B2 喺 %d 後唔影響呢行）" % SPLIT)
        elif "# ① advance fallback（行號 " in l:
            assert "；v145 ＋67，同上）" in l
            l = l.replace("行號 %d，" % adv_old, "行號 %d，" % adv_new)
            l = l.replace("；v145 ＋67，同上）", "；v145 ＋67，同上；v146 rebase ＋10，同 currentLine）")
        elif "# ② applyFamilySafeToNode 處理 b.text（行號 " in l:
            assert "；v145 ＋67，同上）" in l
            l = l.replace("行號 %d–%d，" % (fam_old, fam_hi_old),
                          "行號 %d–%d，" % (fam_new, fam_hi_new))
            l = l.replace("；v145 ＋67，同上）", "；v145 ＋67，同上；v146 rebase ＋10，同 currentLine）")
        elif "FALLBACK not in ls[" in l:
            m = re.search(r"if len\(ls\) < (\d+) or FALLBACK not in ls\[(\d+)\]", l)
            assert m, "unexpected FALLBACK check line: %s" % l
            old_n, old_i = int(m.group(1)), int(m.group(2))
            if old_n == cur_old:
                l = l.replace("len(ls) < %d" % cur_old, "len(ls) < %d" % cur_new)
                l = l.replace("ls[%d]" % (cur_old - 1), "ls[%d]" % (cur_new - 1))
            elif old_n == adv_old:
                l = l.replace("len(ls) < %d" % adv_old, "len(ls) < %d" % adv_new)
                l = l.replace("ls[%d]" % (adv_old - 1), "ls[%d]" % (adv_new - 1))
            else:
                raise AssertionError("FALLBACK check line with unexpected number %d" % old_n)
        elif 'if(typeof b.text === "string" && b.text){' in l and "not in ls[" in l:
            m = re.search(r"if len\(ls\) < (\d+) or 'if\(typeof b\.text.*not in ls\[(\d+)\]", l)
            assert m and int(m.group(1)) == fam_hi_old, "unexpected familySafe check line: %s" % l
            l = l.replace("len(ls) < %d" % fam_hi_old, "len(ls) < %d" % fam_hi_new)
            l = l.replace("ls[%d]" % (fam_old - 1), "ls[%d]" % (fam_new - 1))
        elif 'probs.append("currentLine 第 ' in l:
            l = re.sub(r'currentLine 第 \d+ 行', "currentLine 第 %d 行" % cur_new, l)
        elif 'probs.append("advance 第 ' in l:
            l = re.sub(r'advance 第 \d+ 行', "advance 第 %d 行" % adv_new, l)
        elif 'probs.append("applyFamilySafeToNode 第 ' in l:
            l = re.sub(r'applyFamilySafeToNode 第 \d+ 行',
                       "applyFamilySafeToNode 第 %d 行" % fam_new, l)
        out.append(l)
    return out

out125 = "\n".join(edit125(TEST125.split("\n")))
open(ROOT + "/tests/test_text125_static.py", "w", encoding="utf-8").write(out125)
print("APPLIED: test_text125_static.py resynced from %s base" % BASE)
print("  currentLine %d->%d, advance %d->%d, familySafe %d->%d (bound %d->%d)"
      % (cur_old, cur_new, adv_old, adv_new, fam_old, fam_new, fam_hi_old, fam_hi_new))
