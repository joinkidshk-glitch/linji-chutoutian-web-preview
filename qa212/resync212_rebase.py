"""v20a212 rebase resync: map pins from v212 index.html (30d07fb, 61753 lines)
to rebased index.html (v211 main b1ca47a + v212, 61795 lines) via difflib.

Usage: python3 qa212/resync212_rebase.py [--apply]
Without --apply: report only. With --apply: rewrite the 5 conflicted test
files' pins (from their v212-side versions) and print a verification table.
"""
import difflib
import re
import subprocess
import sys

REPO = "/home/hatch/workspace/linji-work212"
OLD_HTML = "/tmp/resync212r/index_v212.html"
NEW_HTML = REPO + "/index.html"
APPLY = "--apply" in sys.argv


def show(rev, path):
    return subprocess.check_output(["git", "show", f"{rev}:{path}"],
                                   cwd=REPO, text=True)


def build_mapping(old_lines, new_lines):
    sm = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
    mapping = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                mapping[i1 + k + 1] = j1 + k + 1  # 1-based line numbers
    return mapping, sm.get_opcodes()


old = open(OLD_HTML).read().split("\n")
new = open(NEW_HTML).read().split("\n")
mapping, opcodes = build_mapping(old, new)
print(f"old lines={len(old)} new lines={len(new)} mapped={len(mapping)}")
print("non-equal opcodes:")
for tag, i1, i2, j1, j2 in opcodes:
    if tag != "equal":
        print(f"  {tag} old[{i1+1}..{i2}] -> new[{j1+1}..{j2}]")


def mapped(n):
    """Map a 1-based old line number to new; None if inside a changed block."""
    return mapping.get(n)


def check(n, expect_frag=None):
    m = mapped(n)
    ok = m is not None
    content_ok = None
    if ok and expect_frag:
        content_ok = expect_frag in new[m - 1]
    return m, ok, content_ok


# ---- inventory of pins in the v212-side versions of the 14 touched files ----
# (line, N) pairs are 1-based line numbers in the v212 index.html.
PINS = {
    "tests/test_gift185_static.py": {"total": [61753]},
    "tests/test_tang171_static.py": {"total": [61753],
                                     "lines_idx": [56224]},  # 0-based -> line 56225
    "tests/test_tang173_static.py": {"total": [61753],
                                     "lines_idx": [56224, 4954]},
    "tests/test_rom176_static.py": {"line": [6152, 31713, 54655, 55023, 56162, 56256]},
    "tests/test_travel114_static.py": {
        "count": [32314, 35814, 37965, 39135, 39567, 39570, 39601, 44612,
                  60306, 60484, 60630, 60651],
        "free": [24766, 30981, 30982, 30994, 30995, 31006, 31007, 31110,
                 41555, 44269, 44292, 54478, 54597, 54647, 54870, 54909,
                 54915, 54982, 54984, 54987, 55014, 56125, 56499, 56521,
                 56672, 58309, 60074, 60192, 60193, 60228, 60229, 60254,
                 61101],
        "def": [56225], "wrapper": [45181]},
    "tests/test_kwan151_static.py": {"line": None},  # scanned below
    "tests/test_tang152_static.py": {"lines_idx": [25898, 31639, 31783]},
}

# scan kwan151 for all line(N) uses in the v212 version
kwan = show("30d07fb", "tests/test_kwan151_static.py")
kwan_pins = sorted({int(x) for x in re.findall(r"line\((\d+)\)", kwan)})
PINS["tests/test_kwan151_static.py"]["line"] = kwan_pins

print("\n== pin mapping (old -> new) ==")
all_ok = True
for path, groups in PINS.items():
    for kind, nums in groups.items():
        if nums is None:
            continue
        for n in nums:
            ln = n + 1 if kind == "lines_idx" else n
            m, ok, _ = check(ln)
            flag = "" if ok else "  <-- UNMAPPED (inside changed block!)"
            if not ok:
                all_ok = False
            print(f"  {path.split('/')[-1]:32s} {kind:9s} {ln:6d} -> {m}{flag}")
print("\nall pins in equal blocks:", all_ok)

# verify content identity for a few anchors
anchors = [
    (31713, "GIFT_REACT = giftReact"),
    (54655, "v20a176 ROM176"),
    (56225, "function openLoc(id, opts){"),
    (45181, "window.__phase2.openLoc"),
    (6152, 'lan:{ id:"lan"'),
]
print("\n== anchor content check ==")
for n, frag in anchors:
    m, ok, cok = check(n, frag)
    print(f"  old L{n} -> new L{m}: content_match={cok} (new line: {new[m-1][:80] if m else '?'})")
