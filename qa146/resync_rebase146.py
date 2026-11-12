"""Re-sync test_travel114_static.py + test_text125_static.py line numbers for v20a146 rebase.
基底：HEAD (new main 79defe3, v138+v142) 版測試檔＋index.html；目標：rebase 後工作區 index.html。
做法（按慣例：difflib 對位核實純漂移先改行號）：
- difflib.SequenceMatcher(OLD, NEW) 建 equal-block 行號映射；每個釘行必須落喺 equal block，
  內容逐字相同，且前後 3 行 context 相同，先至接受新行號。
- travel114 另加 openLoc( 全序列逐字一致檢查（同 v122/v128/v144 做法）；DEF／WRAPPER 直接搜尋核對。
- text125 三錨點：currentLine 27723、advance 27836、familySafe 33439（上界 33441）。
- v146 對 HEAD index.html 淨 +15 行（.mask CSS 段＋8／modal 高帽註解＋2／B2 註解＋分流＋5，
  另有 3 行原地改內容：.mask 行、兩條 max-height 行、sceneHtml105 行——全部唔係錨點）。
用法：python3 qa146/resync_rebase146.py [--apply]
無 --apply：只印對位結果。--apply：由 HEAD 版測試檔出發，寫新行號入工作區兩個測試檔。
"""
import difflib, re, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work146"
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
print("OLD (HEAD index.html) lines: %d  NEW (rebased) lines: %d  net: %+d"
      % (len(OLD), len(NEW), len(NEW) - len(OLD)))

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
# 預期只有 4 個非 equal 區：.mask 段、modal 高帽註解、max-height 原地改、B2 段。
# （max-height 88dvh 行同 sceneHtml105 行係 replace 區一部分。）


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


# ---------- travel114 ----------
TEST114 = subprocess.run(["git", "show", "HEAD:tests/test_travel114_static.py"], cwd=ROOT,
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

old_hits = [(i + 1, l.strip()) for i, l in enumerate(OLD) if "openLoc(" in l]
new_hits = [(i + 1, l.strip()) for i, l in enumerate(NEW) if "openLoc(" in l]
print("\nopenLoc( lines: old %d new %d" % (len(old_hits), len(new_hits)))
assert [s for _, s in old_hits] == [s for _, s in new_hits], \
    "openLoc( SEQUENCE DIFFERS — not a pure shift, stop!"
print("openLoc( sequence identical: pure line shift confirmed")
seq_pos = {o: n for (o, _), (n, _) in zip(old_hits, new_hits)}

print("\nCOUNT_LINES remap:")
count_new = {}
for n in sorted(count_nums):
    nn = remap(n, "COUNT %d" % n)
    assert seq_pos[n] == nn, "COUNT %d: difflib %d != sequence %d" % (n, nn, seq_pos[n])
    count_new[n] = nn
print("FREE_LINES remap:")
free_new = {}
for n in sorted(free_nums):
    nn = remap(n, "FREE %d" % n)
    assert seq_pos[n] == nn, "FREE %d: difflib %d != sequence %d" % (n, nn, seq_pos[n])
    free_new[n] = nn
def_new = remap(def_old, "DEF_LINE", "function openLoc(id, opts){")
wrap_new = remap(wrap_old, "WRAPPER_LINE", "openLoc: function(id, opts){ openLoc(id, opts); }")
d = [i + 1 for i, l in enumerate(NEW) if "function openLoc(id, opts){" in l]
w = [i + 1 for i, l in enumerate(NEW) if "openLoc: function(id, opts){ openLoc(id, opts); }" in l]
print("direct-search DEF_LINE:", d, " WRAPPER_LINE:", w)
assert d == [def_new] and w == [wrap_new]
print("travel114: COUNT %d FREE %d, all pure drift" % (len(count_nums), len(free_nums)))

# ---------- text125 ----------
print("\ntext125 anchors remap:")
FALLBACK = '(typeof b.text === "string" && b.text ? [b.text] : [])'
cur_new = remap(27723, "currentLine", FALLBACK)
adv_new = remap(27836, "advance", FALLBACK)
fam_new = remap(33439, "familySafe", 'if(typeof b.text === "string" && b.text){')
fam_hi_new = remap(33441, "familySafe bound", None)
assert fam_hi_new - fam_new == 2
print("text125: all three anchors pure drift")

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
# 頭註加 v146 resync 紀錄（接喺 v142 行之後）
anchor142 = "# 行號按 difflib 對位逐行實量（COUNT 13／FREE 27 不變，DEF 53369→53402、WRAPPER 44054→44087）。\n"
assert anchor142 in out114
out114 = out114.replace(anchor142, anchor142 +
    "# v20a146 resync：MASK146 淨 ＋10 行（.mask CSS 段 ＋8／modal 高帽註解 ＋2）＋B2 淨 ＋5 行\n"
    "# （wf4PlayEvent 註解＋分流，約行 40543 後）；行號 ＜40543 者 ＋10、≥40543 者 ＋15。\n"
    "# qa146/resync_rebase146.py 核實：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，\n"
    "# 純漂移（COUNT 13／FREE 27 不變，DEF %d→%d、WRAPPER %d→%d）。\n"
    % (def_old, def_new, wrap_old, wrap_new), 1)
open(ROOT + "/tests/test_travel114_static.py", "w", encoding="utf-8").write(out114)
print("\nAPPLIED: test_travel114_static.py resynced from HEAD base")

TEST125 = subprocess.run(["git", "show", "HEAD:tests/test_text125_static.py"], cwd=ROOT,
                         capture_output=True, text=True).stdout
out125 = TEST125
out125 = out125.replace(
    "v142 ＋14：A2b CSS ＋4／A2a CSS ＋6／B1 註釋 ＋4）",
    "v142 ＋14：A2b CSS ＋4／A2a CSS ＋6／B1 註釋 ＋4；v146 ＋10：MASK146 CSS 段 ＋8／modal 高帽註解 ＋2，B2 喺 40543 後唔影響呢行）", 1)
out125 = out125.replace("27723", str(cur_new)).replace("27722", str(cur_new - 1))
out125 = out125.replace(
    "v142 ＋14，同 currentLine 一樣）",
    "v142 ＋14，同 currentLine 一樣；v146 ＋10，同 currentLine）", 1)
out125 = out125.replace("27836", str(adv_new)).replace("27835", str(adv_new - 1))
out125 = out125.replace(
    "v142 ＋16，實量）",
    "v142 ＋16，實量；v146 ＋10，同 currentLine）", 1)
out125 = out125.replace("33439", str(fam_new)).replace("33441", str(fam_hi_new)).replace("33438", str(fam_new - 1))
open(ROOT + "/tests/test_text125_static.py", "w", encoding="utf-8").write(out125)
print("APPLIED: test_text125_static.py resynced from HEAD base")
print("  currentLine %d->%d, advance %d->%d, familySafe %d->%d (bound %d->%d)"
      % (27723, cur_new, 27836, adv_new, 33439, fam_new, 33441, fam_hi_new))
