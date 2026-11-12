"""Re-sync test_travel114_static.py + test_text125_static.py line numbers for v20a146 B1 wiring.
基底：分支 HEAD (9fe05d9，rebase 後 v146，A1＋B2) 版 index.html；目標：工作區 index.html（＋B1 接線）。
做法（按慣例：difflib 對位核實純漂移先改行號）：
- difflib.SequenceMatcher(OLD, NEW) 建行號映射；每個釘行必須落喺 equal block，
  內容逐字相同，且前後 3 行 context 相同，先至接受新行號。
- B1 接線只係覆寫表 ＋2 行（約行 40463，st05／st08），註解行數不變；預期只有 1 個
  非 equal 區（＋2 行插入），其餘全部 equal。
- travel114 另加 openLoc( 全序列逐字一致檢查；DEF／WRAPPER 直接搜尋核對。
- text125 三錨點（currentLine／advance／familySafe）全部喺表之前，預期行號不變。
用法：python3 qa146/resync_b1_146.py [--apply]
無 --apply：只印對位結果。--apply：由工作區現版測試檔出發，寫新行號。
"""
import difflib, re, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work146"
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
print("OLD (HEAD index.html) lines: %d  NEW (work) lines: %d  net: %+d"
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
TEST114 = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read()

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
TEST125 = open(ROOT + "/tests/test_text125_static.py", encoding="utf-8").read()
FALLBACK = '(typeof b.text === "string" && b.text ? [b.text] : [])'
cur_old = int(re.search(r"len\(ls\) < (\d+) or FALLBACK not in ls\[(\d+)\]", TEST125).group(1))
adv_old = int(re.search(r"advance 第 (\d+) 行", TEST125).group(1))
fam_old = int(re.search(r"applyFamilySafeToNode 第 (\d+) 行", TEST125).group(1))
fam_hi_old = int(re.search(r"len\(ls\) < (\d+) or 'if\(typeof b\.text", TEST125).group(1))
print("\ntext125 anchors remap:")
cur_new = remap(cur_old, "currentLine", FALLBACK)
adv_new = remap(adv_old, "advance", FALLBACK)
fam_new = remap(fam_old, "familySafe", 'if(typeof b.text === "string" && b.text){')
fam_hi_new = remap(fam_hi_old, "familySafe bound", None)
assert fam_hi_new - fam_new == 2
print("text125: old %d/%d/%d-%d -> new %d/%d/%d-%d"
      % (cur_old, adv_old, fam_old, fam_hi_old, cur_new, adv_new, fam_new, fam_hi_new))

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
anchor146 = "# qa146/resync_rebase146.py 核實：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，\n"
assert anchor146 in out114
out114 = out114.replace(anchor146, anchor146 +
    "# v20a146 B1 接線：覆寫表 ＋2 行（st05／st08，約行 40463 後）；行號 ≥40463 者 ＋2。\n"
    "# qa146/resync_b1_146.py 核實：44 個 openLoc( 呼叫點序列逐字一致，純漂移（DEF %d→%d、WRAPPER %d→%d）。\n"
    % (def_old, def_new, wrap_old, wrap_new), 1)
open(ROOT + "/tests/test_travel114_static.py", "w", encoding="utf-8").write(out114)
print("\nAPPLIED: test_travel114_static.py resynced for B1 wiring")

if (cur_new, adv_new, fam_new, fam_hi_new) != (cur_old, adv_old, fam_old, fam_hi_old):
    print("NOTE: text125 anchors moved — updating file")
    out125 = TEST125
    out125 = out125.replace("行號 %d" % cur_old, "行號 %d" % cur_new)
    out125 = out125.replace("第 %d 行冇 text fallback" % cur_old, "第 %d 行冇 text fallback" % cur_new)
    out125 = out125.replace("ls[%d]" % (cur_old - 1), "ls[%d]" % (cur_new - 1))
    out125 = out125.replace("len(ls) < %d" % cur_old, "len(ls) < %d" % cur_new)
    out125 = out125.replace("行號 %d" % adv_old, "行號 %d" % adv_new)
    out125 = out125.replace("第 %d 行冇 text fallback" % adv_old, "第 %d 行冇 text fallback" % adv_new)
    out125 = out125.replace("ls[%d]" % (adv_old - 1), "ls[%d]" % (adv_new - 1))
    out125 = out125.replace("len(ls) < %d" % adv_old, "len(ls) < %d" % adv_new)
    out125 = out125.replace("行號 %d–%d" % (fam_old, fam_hi_old), "行號 %d–%d" % (fam_new, fam_hi_new))
    out125 = out125.replace("第 %d 行冇 b.text 分支" % fam_old, "第 %d 行冇 b.text 分支" % fam_new)
    out125 = out125.replace("ls[%d]" % (fam_old - 1), "ls[%d]" % (fam_new - 1))
    out125 = out125.replace("len(ls) < %d" % fam_hi_old, "len(ls) < %d" % fam_hi_new)
    open(ROOT + "/tests/test_text125_static.py", "w", encoding="utf-8").write(out125)
    print("APPLIED: test_text125_static.py resynced for B1 wiring")
else:
    print("text125 anchors unchanged (all before the table) — no file change needed")
