#!/usr/bin/env python3
"""v213 rebase resync, part 2 — fix travel114 FREE set + verify COUNT.

Two bugs found in part 1 (resync213_rebase.py):
1. sub_pins() did sequential str replacement: 31005->31006 was then
   re-replaced 31006->31007 (cascade), giving a duplicate 31007.
2. The git merge split the FREE list so neither conflict side alone is
   complete: HEAD hunk2 has 29 pins, theirs hunk2 has 28; the merged file
   ended with 32 pins, missing the 30995 anchor (base 30994 + v211 +1).

Authoritative source: HEAD's (:2:, main 17c6f69) pin sets, which passed
on main. Map them main-index -> rebased-index via difflib with content
verification, and rebuild the travel114 sets from those. Cross-check
against the theirs-mapped values from part 1; any disagreement is
reported with content at both positions.

Also fixes rom176 stale ok() labels (L54815 etc. kept the old number
while line() moved) and the wrong "6152/31713" remark in the appended
rebase comment.
"""
import difflib
import re
import subprocess
import sys

REPO = "/home/hatch/workspace/linji-work213"


def sh(cmd):
    return subprocess.check_output(cmd, shell=True, text=True, cwd=REPO)


main = sh("git show 17c6f69:index.html").splitlines()
new = open(f"{REPO}/index.html", encoding="utf-8").read().splitlines()
print(f"main index: {len(main)} lines; new index: {len(new)} lines")
assert len(main) == 61795 and len(new) == 61994

sm = difflib.SequenceMatcher(None, main, new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1


def map_pins(pins, label):
    out, bad = [], 0
    for p in pins:
        q = mapping.get(p)
        if q is None or main[p - 1] != new[q - 1]:
            print(f"UNMAPPED/MISMATCH {label} {p} -> {q}")
            print(f"  main: {main[p-1][:110]!r}" if p <= len(main) else "  (out of range)")
            if q:
                print(f"  new:  {new[q-1][:110]!r}")
            bad += 1
            continue
        out.append(q)
    if bad:
        print(f"{label}: {bad} failed")
        sys.exit(1)
    return out


def get_set(spec, name):
    txt = sh(f"git show {spec}tests/test_travel114_static.py")
    m = re.search(rf"{name} = \{{(.*?)\n\}}", txt, re.S)
    return [int(x) for x in re.findall(r"^\s+(\d+),", m.group(1), re.M)]


def get_scalar(spec, name):
    txt = sh(f"git show {spec}tests/test_travel114_static.py")
    m = re.search(rf"^{name} = (\d+)", txt, re.M)
    return int(m.group(1))


head_free = get_set(":2:", "FREE_LINES")
head_count = get_set(":2:", "COUNT_LINES")
head_def = get_scalar(":2:", "DEF_LINE")
head_wrap = get_scalar(":2:", "WRAPPER_LINE")
print(f"HEAD FREE {len(head_free)} COUNT {len(head_count)} DEF {head_def} WRAP {head_wrap}")

mapped_free = map_pins(head_free, "FREE")
mapped_count = map_pins(head_count, "COUNT")
mapped_def = map_pins([head_def], "DEF")[0]
mapped_wrap = map_pins([head_wrap], "WRAP")[0]
print(f"mapped FREE {len(mapped_free)} (unique {len(set(mapped_free))})")
print(f"mapped COUNT {mapped_count}")
print(f"mapped DEF {mapped_def} WRAP {mapped_wrap}")

# cross-check vs theirs-mapped values from part 1 (recompute quickly)
old213 = sh("git show e81027e:index.html").splitlines()
sm2 = difflib.SequenceMatcher(None, old213, new, autojunk=False)
map2 = {}
for tag, i1, i2, j1, j2 in sm2.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            map2[i1 + k + 1] = j1 + k + 1
theirs_free = get_set(":3:", "FREE_LINES")
theirs_count = get_set(":3:", "COUNT_LINES")
tm_free = sorted(map2[p] for p in theirs_free)
tm_count = sorted(map2[p] for p in theirs_count)
print("FREE: HEAD-mapped == theirs-mapped ?", mapped_free == tm_free)
if mapped_free != tm_free:
    print("  only HEAD-mapped:", sorted(set(mapped_free) - set(tm_free)))
    print("  only theirs-mapped:", sorted(set(tm_free) - set(mapped_free)))
print("COUNT: HEAD-mapped == theirs-mapped ?", mapped_count == tm_count)
if mapped_count != tm_count:
    print("  HEAD-mapped:", mapped_count)
    print("  theirs-mapped:", tm_count)
    for a, b in zip(mapped_count, tm_count):
        if a != b:
            print(f"  disagree {a} vs {b}: new[{a}]={new[a-1][:90]!r} new[{b}]={new[b-1][:90]!r}")

if mapped_free != tm_free or mapped_count != tm_count:
    print("DISAGREEMENT — stop, inspect manually")
    sys.exit(1)

# ---- rebuild travel114 sets from HEAD-mapped values ----
path = f"{REPO}/tests/test_travel114_static.py"
txt = open(path, encoding="utf-8").read()

# single-pass number substitution inside a block, preserving comments
def sub_block(block, old_new):
    # splitlines() (no keepends) + "\n".join: the previous keepends version
    # dropped newlines (group(3) never captured the trailing "\n")
    out = []
    for ln in block.splitlines():
        m = re.match(r"^(\s+)(\d+),(.*)$", ln)
        if m and int(m.group(2)) in old_new:
            out.append(f"{m.group(1)}{old_new[int(m.group(2))]},{m.group(3)}")
        else:
            out.append(ln)
    return "\n".join(out)


def replace_set(txt, name, head_pins, mapped_pins):
    m = re.search(rf"({name} = \{{)(.*?)(\n\}})", txt, re.S)
    assert m, name
    old_new = dict(zip(head_pins, mapped_pins))
    new_block = sub_block(m.group(2), old_new)
    # the block in the current file is the theirs-mapped version, not HEAD's;
    # rebuild it from HEAD's block text instead (keeps HEAD comments)
    head_txt = sh("git show :2:tests/test_travel114_static.py")
    hm = re.search(rf"({name} = \{{)(.*?)(\n\}})", head_txt, re.S)
    new_block = sub_block(hm.group(2), old_new)
    return txt[:m.start(2)] + new_block + txt[m.end(2):]


txt = replace_set(txt, "COUNT_LINES", head_count, mapped_count)
txt = replace_set(txt, "FREE_LINES", head_free, mapped_free)
txt = re.sub(r"^DEF_LINE = \d+", f"DEF_LINE = {mapped_def}", txt, flags=re.M)
txt = re.sub(r"^WRAPPER_LINE = \d+", f"WRAPPER_LINE = {mapped_wrap}",
             txt, flags=re.M)
# refresh the rebase comment with the full mapping note
txt = re.sub(
    r"# v20a213 rebase 上 main 17c6f69 resync：COUNT／FREE／DEF／WRAPPER 按 difflib 映射重寫.*\n",
    f"# v20a213 rebase 上 main 17c6f69 resync：COUNT／FREE／DEF／WRAPPER 按 "
    f"difflib 映射重寫（以 HEAD :2: 33 針為準，補返合併漏咗嘅 30995；"
    f"DEF {mapped_def}／WRAPPER {mapped_wrap}），"
    f"qa213/resync213_rebase2.py 核實純漂移。\n", txt)
open(path, "w", encoding="utf-8").write(txt)

# verify final file
m = re.search(r"FREE_LINES = \{(.*?)\n\}", txt, re.S)
final_free = [int(x) for x in re.findall(r"^\s+(\d+),", m.group(1), re.M)]
m = re.search(r"COUNT_LINES = \{(.*?)\n\}", txt, re.S)
final_count = [int(x) for x in re.findall(r"^\s+(\d+),", m.group(1), re.M)]
assert len(final_free) == 33 and len(set(final_free)) == 33, final_free
assert len(final_count) == 12 and len(set(final_count)) == 12, final_count
assert final_free == mapped_free and final_count == mapped_count
assert "<<<<<<<" not in txt
print(f"travel114 rebuilt: FREE {len(final_free)} unique, COUNT "
      f"{len(final_count)} unique, DEF {mapped_def}, WRAP {mapped_wrap}")

# ---- rom176: fix stale labels + wrong remark ----
rpath = f"{REPO}/tests/test_rom176_static.py"
rt = open(rpath, encoding="utf-8").read()
for old_pin, new_pin in ((54815, 54896), (55183, 55264), (56322, 56403),
                         (56416, 56497)):
    rt = rt.replace(f"起點 L{old_pin}", f"起點 L{new_pin}")
    rt = rt.replace(f"定義 L{old_pin}", f"定義 L{new_pin}")
    rt = rt.replace(f"addLocTalkGiftActs L{old_pin}",
                    f"addLocTalkGiftActs L{new_pin}")
    rt = rt.replace(f"openLoc rom176 攔截 L{old_pin}",
                    f"openLoc rom176 攔截 L{new_pin}")
rt = rt.replace("；6152／31713 唔郁", "；6152 唔郁")
open(rpath, "w", encoding="utf-8").write(rt)
assert "L54815" not in rt and "L55183" not in rt
assert "6152／31713" not in rt
print("rom176 labels + remark fixed")
print("PART 2 DONE")
