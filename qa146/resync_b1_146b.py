"""Re-sync test_travel114_static.py line numbers for v20a146 2nd rebase, commit 2 (B1 wiring).
基底：HEAD (5a276ab，commit 1 已 rebase 上 f45e766) 版 index.html＋travel114；
目標：工作區 index.html（＋B1 接線：覆寫表 st05／st08 ＋2 行＋兩段註解改寫）。
做法（按慣例：difflib 對位核實純漂移先改行號）：
- difflib.SequenceMatcher(OLD, NEW) 建行號映射；每個釘行必須落喺 equal block，
  內容逐字一致，且前後 3 行 context 相同，先至接受新行號。
- B1 分界線：OLD 入面覆寫表 `wf4_ev_set08:` 嗰行（即 day04 行之後第一行，新行插喺佢前面）；
  釘行 ≥分界 ＋2、＜分界 ＋0；每個釘行嘅實量 shift 必須同預期一致。
- travel114 另加 openLoc( 全序列逐字一致檢查；DEF／WRAPPER 直接搜尋核對。
- 獨立交叉核對：新行號必須 ＝735f284（原 B1 commit）對應行號 ＋67（v145 BOOK145 全域 ＋67）。
- text125 三錨點全部喺覆寫表之前，預期行號不變——核實後唔郁個檔。
用法：python3 qa146/resync_b1_146b.py [--apply]
無 --apply：只印對位結果。--apply：由 HEAD 版 travel114 出發，寫新行號入工作區測試檔。
"""
import difflib, re, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work146"
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
print("OLD (HEAD index.html) lines: %d  NEW (worktree) lines: %d  net: %+d"
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
# 預期 3 個非 equal 區：覆寫表上註解改寫、表頭註解改寫、st05／st08 ＋2 行插入。

# B2 分界線：覆寫表 set08 行（新行插喺 day04 行之後、呢行之前）。
split_candidates = [i + 1 for i, l in enumerate(OLD)
                    if 'wf4_ev_set08:"assets/story/locs/bg_loc_film_lion.jpg' in l]
assert len(split_candidates) == 1, "set08 override row not unique: %s" % split_candidates
SPLIT = split_candidates[0]
print("B1 split (OLD line of set08 override row): %d" % SPLIT)


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


def check_shift(old_line, new_line, label):
    want = 2 if old_line >= SPLIT else 0
    assert new_line - old_line == want, \
        "%s: shift %d != expected %+d (split %d)" % (label, new_line - old_line, want, SPLIT)


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
print("travel114: COUNT %d FREE %d, all pure drift, shifts +0/＋2 split at %d"
      % (len(count_nums), len(free_nums), SPLIT))

# ---------- cross-check vs original B1 commit (735f284): new == orig + 67 ----------
ORIG114 = subprocess.run(["git", "show", "735f284:tests/test_travel114_static.py"], cwd=ROOT,
                         capture_output=True, text=True).stdout
def parse_set_txt(txt, name):
    m = re.search(name + r" = \{([^}]*)\}", txt, re.S)
    nums = []
    for line in m.group(1).split("\n"):
        nums.extend(int(x) for x in re.findall(r"\d+", line.split("#", 1)[0]))
    return nums
orig_count = parse_set_txt(ORIG114, "COUNT_LINES")
orig_free = parse_set_txt(ORIG114, "FREE_LINES")
orig_def = int(re.search(r"DEF_LINE = (\d+)", ORIG114).group(1))
orig_wrap = int(re.search(r"WRAPPER_LINE = (\d+)", ORIG114).group(1))
assert sorted(count_new.values()) == sorted(x + 67 for x in orig_count), "COUNT cross-check vs 735f284+67 FAILED"
assert sorted(free_new.values()) == sorted(x + 67 for x in orig_free), "FREE cross-check vs 735f284+67 FAILED"
assert def_new == orig_def + 67 and wrap_new == orig_wrap + 67, "DEF/WRAPPER cross-check vs 735f284+67 FAILED"
print("cross-check: all remapped anchors == 735f284 anchors + 67 (v145 BOOK145)")

# ---------- text125 (expect unchanged) ----------
TEST125 = subprocess.run(["git", "show", "HEAD:tests/test_text125_static.py"], cwd=ROOT,
                         capture_output=True, text=True).stdout
t125_lines = TEST125.split("\n")
cur_old = adv_old = fam_old = fam_hi_old = None
for l in t125_lines:
    if "FALLBACK not in ls[" in l:
        n = int(re.search(r"if len\(ls\) < (\d+)", l).group(1))
        if cur_old is None:
            cur_old = n
        else:
            adv_old = n
    if "if(typeof b.text" in l and "not in ls[" in l:
        fam_hi_old = int(re.search(r"if len\(ls\) < (\d+)", l).group(1))
        fam_old = int(re.search(r"not in ls\[(\d+)\]", l).group(1)) + 1
print("\ntext125 anchors remap (expect +0: all before the override table):")
FALLBACK = '(typeof b.text === "string" && b.text ? [b.text] : [])'
cur_new = remap(cur_old, "currentLine", FALLBACK)
assert cur_new == cur_old
adv_new = remap(adv_old, "advance", FALLBACK)
assert adv_new == adv_old
fam_new = remap(fam_old, "familySafe", 'if(typeof b.text === "string" && b.text){')
assert fam_new == fam_old
fam_hi_new = remap(fam_hi_old, "familySafe bound", None)
assert fam_hi_new == fam_hi_old
print("text125: all three anchors unchanged — file needs no change")

# ---------- apply ----------
if "--apply" not in sys.argv:
    print("\nDRY RUN only — pass --apply to rewrite test_travel114_static.py.")
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
# allowlist 頭註加 B1 紀錄
old_tail = "；v20a146 rebase：行號 ＜40613 者 ＋10、≥40613 者 ＋15（MASK146 CSS ＋8／modal 高帽 ＋2／B2 ＋5） ----------"
assert old_tail in out114
out114 = out114.replace(old_tail,
    "；v20a146 rebase：行號 ＜40613 者 ＋10、≥40613 者 ＋15（MASK146 CSS ＋8／modal 高帽 ＋2／B2 ＋5）；B1 ＋2（覆寫表 st05／st08，行號 ≥%d 者再 ＋2） ----------"
    % SPLIT, 1)
# 頭註加 B1 紀錄（接喺 rebase 純漂移行之後；該行寫 DEF／WRAPPER 由 f45e766 到 HEAD 嘅 ＋15）
anchor = "# 純漂移（COUNT 13／FREE 27 不變，DEF %d→%d、WRAPPER %d→%d）。\n" % (def_old - 15, def_old, wrap_old - 15, wrap_old)
assert anchor in out114
out114 = out114.replace(anchor, anchor +
    "# v20a146 B1 接線（rebase 版）：覆寫表 ＋2 行（st05／st08，約行 %d 後）；行號 ≥%d 者 ＋2。\n"
    "# qa146/resync_b1_146b.py 核實：44 個 openLoc( 呼叫點序列逐字一致，純漂移（DEF %d→%d、WRAPPER %d→%d）。\n"
    % (SPLIT - 1, SPLIT, def_old, def_new, wrap_old, wrap_new), 1)
open(ROOT + "/tests/test_travel114_static.py", "w", encoding="utf-8").write(out114)
print("\nAPPLIED: test_travel114_static.py resynced for B1 wiring (HEAD base)")
print("  DEF %d->%d, WRAPPER %d->%d" % (def_old, def_new, wrap_old, wrap_new))
