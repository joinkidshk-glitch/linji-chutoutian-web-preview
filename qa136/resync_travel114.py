"""Re-sync test_travel114_static.py line allowlists after v136 endgate move
(pure line shift from gate comment + evalGate3Y backstop/awardResolved +
prog71 mapping + scrub guard + CONSEQ61 1992 entry + copy edits;
OLD = rebase base bcac846 (v137, origin/main), NEW = work136).
Rebase note: branch originally based on 673df0d (v135); after rebase onto
bcac846, OLD is origin/main so the v137 shift is already in the base.
No openLoc( line content touched.
Method (same as v122/v128/v135): for every old-listed line, take its content from
the base index.html and find the identical stripped line in the work
index.html. Positional sequence alignment of ALL openLoc( lines must be
identical (no call site added/removed/edited); only then is a pure
line-shift re-sync valid.
Usage: python3 qa136/resync_travel114.py [--apply]
Without --apply: print only. With --apply: rewrite the test file's sets.
"""
import re, subprocess, sys

ROOT = "/home/hatch/workspace/linji-work136"
OLD = subprocess.run(["git", "show", "origin/main:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(ROOT + "/index.html", encoding="utf-8").read().split("\n")
TEST = open(ROOT + "/tests/test_travel114_static.py", encoding="utf-8").read()

def parse_set(name):
    m = re.search(name + r" = \{([^}]*)\}", TEST, re.S)
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
def_line_old = int(re.search(r"DEF_LINE = (\d+)", TEST).group(1))
wrap_line_old = int(re.search(r"WRAPPER_LINE = (\d+)", TEST).group(1))

old_hits = [(i + 1, l.strip()) for i, l in enumerate(OLD) if "openLoc(" in l]
new_hits = [(i + 1, l.strip()) for i, l in enumerate(NEW) if "openLoc(" in l]
print("old openLoc( lines:", len(old_hits), " new:", len(new_hits))
old_seq = [s for _, s in old_hits]
new_seq = [s for _, s in new_hits]
assert old_seq == new_seq, "SEQUENCE DIFFERS — not a pure shift, stop!"
print("sequence identical: pure line shift confirmed")
pos = {o: n for (o, _), (n, _) in zip(old_hits, new_hits)}

def show(name, nums, comments):
    print("\n%s = {" % name)
    for n in sorted(nums):
        nn = pos[n]
        c = comments.get(n, "")
        print("    %d,%s" % (nn, ("  # " + c) if c else ""))
    print("}")
    for n in nums:
        assert OLD[n - 1].strip() == NEW[pos[n] - 1].strip(), "content mismatch at old %d" % n
    print("  (content verified identical for all %d lines)" % len(nums))

show("COUNT_LINES", count_nums, count_c)
show("FREE_LINES", free_nums, free_c)
print("\nDEF_LINE =", pos[def_line_old], " #", OLD[def_line_old - 1].strip()[:60])
print("WRAPPER_LINE =", pos[wrap_line_old], " #", OLD[wrap_line_old - 1].strip()[:60])
d = [i + 1 for i, l in enumerate(NEW) if "function openLoc(id, opts){" in l]
w = [i + 1 for i, l in enumerate(NEW) if "openLoc: function(id, opts){ openLoc(id, opts); }" in l]
print("direct-search DEF_LINE:", d, " WRAPPER_LINE:", w)
assert d == [pos[def_line_old]] and w == [pos[wrap_line_old]]
print("counts: free %d count %d" % (len(free_nums), len(count_nums)))

if "--apply" in sys.argv:
    out = TEST
    out = re.sub(r"COUNT_LINES = \{[^}]*\}",
                 "COUNT_LINES = {\n" + "\n".join("    %d,%s" % (pos[n], ("  # " + count_c[n]) if n in count_c else "") for n in sorted(count_nums)) + "\n}",
                 out, count=1, flags=re.S)
    out = re.sub(r"FREE_LINES = \{[^}]*\}",
                 "FREE_LINES = {\n" + "\n".join("    %d,%s" % (pos[n], ("  # " + free_c[n]) if n in free_c else "") for n in sorted(free_nums)) + "\n}",
                 out, count=1, flags=re.S)
    out = re.sub(r"DEF_LINE = \d+", "DEF_LINE = %d" % pos[def_line_old], out, count=1)
    out = re.sub(r"WRAPPER_LINE = \d+", "WRAPPER_LINE = %d" % pos[wrap_line_old], out, count=1)
    # 註頭加 v136 resync 一行（放喺 v135 resync 註之後）
    out = out.replace(
        "# v20a135 resync：MAP135 淨 −14 行（CSS 死規則清理淨 +1 行喺 5162 附近、paintBar 模板合併淨 −15 行喺 38396–38612；\n# 行號 ≥5162 者 +1、≥38396 者再 −15，逐行內容經 difflib 對位核實純漂移）。qa135/resync_travel114.py 核實：",
        "# v20a135 resync：MAP135 淨 −14 行（CSS 死規則清理淨 +1 行喺 5162 附近、paintBar 模板合併淨 −15 行喺 38396–38612；\n# 行號 ≥5162 者 +1、≥38396 者再 −15，逐行內容經 difflib 對位核實純漂移）。qa135/resync_travel114.py 核實：\n# v20a136 resync：ENDGATE136 淨行數見 qa136/resync_travel114.py 輸出（閘＋評估器＋評核＋文案）；\n# 44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移（COUNT 13／FREE 27 不變）。")
    open(ROOT + "/tests/test_travel114_static.py", "w", encoding="utf-8").write(out)
    print("\nAPPLIED: test_travel114_static.py resynced")
