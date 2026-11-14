#!/usr/bin/env python3
"""v213 rebase resync: map static-test pins from v213-branch index (e81027e,
61,913 lines) to the rebased index (working tree, 61,994 lines = 61,714
+ v211 +42 + v212 +39 + v213 +199; v209 added 0 lines).

Method: difflib opcodes (autojunk=False) between the two index.html files.
Every pin must land in an 'equal' block AND the line content at the new
position must be byte-identical to the old line (pure drift). Any pin that
fails either check is reported UNMAPPED/MISMATCH and the script exits 1.

Also resolves the 5 conflicted static test files: keeps merged common
segments, takes the theirs (v213) side of each conflict hunk, maps its pins,
keeps the audit-trail resync comments from both sides, appends a new
v213-rebase comment. Never uses "}" as an end marker (v212 lesson).
"""
import difflib
import re
import subprocess
import sys

REPO = "/home/hatch/workspace/linji-work213"


def sh(cmd):
    return subprocess.check_output(cmd, shell=True, text=True, cwd=REPO)


old = sh("git show e81027e:index.html").splitlines()
new = open(f"{REPO}/index.html", encoding="utf-8").read().splitlines()
print(f"old index: {len(old)} lines; new index: {len(new)} lines")
assert len(old) == 61913, len(old)
assert len(new) == 61994, len(new)

sm = difflib.SequenceMatcher(None, old, new, autojunk=False)
mapping = {}
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            mapping[i1 + k + 1] = j1 + k + 1  # 1-based

# pins to map: name -> old line (1-based)
PINS = {
    # rom176
    "rom176_gift_react": 31712,
    "rom176_block": 54815,
    "rom176_apply": 55183,
    "rom176_addloc": 56322,
    "rom176_intercept": 56416,
    # tang171 / tang173 openLoc DEF
    "openloc_def": 56385,
    # travel114 COUNT_LINES (theirs side)
    "t114_count": [32313, 35813, 37964, 39146, 39578, 39581, 39612, 44623,
                   60466, 60644, 60790, 60811],
    # travel114 FREE_LINES, hunk2 theirs side
    "t114_free2": [31005, 31006, 31109, 41566, 44280, 44303, 54638, 54757,
                   54807, 55030, 55069, 55075, 55142, 55144, 55147, 55174,
                   56285, 56659, 56681, 56832, 58469, 60234, 60352, 60353,
                   60388, 60389, 60414, 61261],
    # travel114 DEF / WRAPPER (theirs side)
    "t114_def": 56385,
    "t114_wrapper": 45192,
}

flat = {}
for k, v in PINS.items():
    if isinstance(v, list):
        for i, p in enumerate(v):
            flat[f"{k}[{i}]={p}"] = p
    else:
        flat[f"{k}={v}"] = v

bad = 0
mapped = {}
for label, p in sorted(flat.items(), key=lambda kv: kv[1]):
    q = mapping.get(p)
    if q is None:
        print(f"UNMAPPED  old {p} ({label}): not in an equal block")
        print(f"  old content: {old[p-1][:120]!r}")
        bad += 1
        continue
    if old[p - 1] != new[q - 1]:
        print(f"MISMATCH  old {p} -> new {q} ({label})")
        print(f"  old: {old[p-1][:120]!r}")
        print(f"  new: {new[q-1][:120]!r}")
        bad += 1
        continue
    mapped[p] = q
    print(f"OK  {p} -> {q}  ({label})  :: {old[p-1][:90]}")

if bad:
    print(f"\n{bad} pin(s) failed; NOT resolving files")
    sys.exit(1)

# ---- resolve conflicted files ----
NEW_TOTAL = 61994
NEW_TOTAL_COMMENT = ("v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋v206 C2 +3＋"
                     "v207 +34＋v208 +223＋v211 +42＋v212 +39＋v213 +199")
REBASE_COMMENT_213 = ("# v20a213 rebase 上 main 17c6f69 resync：釘行按 difflib 映射重寫，"
                      "qa213/resync213_rebase.py 核實純漂移（v211 +42／v212 +39／v213 +199）。")


def parse_conflicts(text):
    """Split text into segments: ('common', s) or ('hunk', head, theirs)."""
    pat = re.compile(r"^<<<<<<< [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n",
                     re.M | re.S)
    segs, pos = [], 0
    for m in pat.finditer(text):
        segs.append(("common", text[pos:m.start()]))
        segs.append(("hunk", m.group(1), m.group(2)))
        pos = m.end()
    segs.append(("common", text[pos:]))
    return segs


def sub_pins(text, pinmap):
    """Replace standalone integers listed in pinmap (old->new), word-bounded."""
    for o, n in sorted(pinmap.items(), key=lambda kv: -len(str(kv[0]))):
        text = re.sub(rf"\b{o}\b", str(n), text)
    return text


def resolve(path, hunk_fns):
    text = open(f"{REPO}/{path}", encoding="utf-8").read()
    segs = parse_conflicts(text)
    hunks = [s for s in segs if s[0] == "hunk"]
    assert len(hunks) == len(hunk_fns), (path, len(hunks), len(hunk_fns))
    out = []
    hi = 0
    for kind, *rest in segs:
        if kind == "common":
            out.append(rest[0])
        else:
            head, theirs = rest
            out.append(hunk_fns[hi](head, theirs))
            hi += 1
    resolved = "".join(out)
    assert "<<<<<<<" not in resolved and ">>>>>>>" not in resolved, path
    open(f"{REPO}/{path}", "w", encoding="utf-8").write(resolved)
    print(f"resolved {path}")


# --- gift185: 1 hunk, total-lines only ---
def gift185_hunk(head, theirs):
    t = theirs
    t = t.replace("總行數 61913（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋"
                  "v206 C2 +3＋v207 +34＋v208 +223＋v213 +199）",
                  f"總行數 {NEW_TOTAL}（{NEW_TOTAL_COMMENT}）")
    t = t.replace("html.count('\\n') == 61913",
                  f"html.count('\\n') == {NEW_TOTAL}")
    t += REBASE_COMMENT_213 + "\n"
    return t


# --- rom176: 1 hunk, 5 pins + keep audit comments from both sides ---
def rom176_hunk(head, theirs):
    pinmap = {p: mapped[p] for p in (31712, 54815, 55183, 56322, 56416)}
    ok_lines = [ln for ln in theirs.splitlines(keepends=True)
                if ln.strip() and not ln.lstrip().startswith("#")]
    body = sub_pins("".join(ok_lines), pinmap)
    comments = []
    for ln in theirs.splitlines(keepends=True):
        if ln.lstrip().startswith("#"):
            comments.append(ln)
    for ln in head.splitlines(keepends=True):
        if ln.lstrip().startswith("#") and ln not in comments:
            comments.append(ln)
    mapping_txt = "、".join(f"{o}→{mapped[o]}" for o in
                            (31712, 54815, 55183, 56322, 56416))
    comments.append(
        f"# v20a213 rebase 上 main 17c6f69 resync：釘行按 difflib 映射重寫"
        f"（{mapping_txt}；6152／31713 唔郁），"
        f"qa213/resync213_rebase.py 核實純漂移。\n")
    return body + "".join(comments)


# --- tang171 / tang173: 1 hunk each, total + openLoc DEF ---
def tang_hunk(head, theirs):
    d = mapped[56385]
    t = theirs
    t = t.replace("總行數 61913（v193 61167＋v203 +233＋v204 +32＋v206 C1 +22＋"
                  "v206 C2 +3＋v207 +34＋v208 +223＋v213 +199）",
                  f"總行數 {NEW_TOTAL}（{NEW_TOTAL_COMMENT}）")
    t = t.replace("src.count('\\n') == 61913",
                  f"src.count('\\n') == {NEW_TOTAL}")
    t = t.replace(f"openLoc DEF 行 56385（v193 55639＋v203 +233＋v204 +32＋"
                  f"v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v213 +199，"
                  f"travel114 釘行）",
                  f"openLoc DEF 行 {d}（v193 55639＋v203 +233＋v204 +32＋"
                  f"v206 C1 +22＋v206 C2 +3＋v207 +34＋v208 +223＋v211 +42＋"
                  f"v212 +39＋v213 +199，travel114 釘行）")
    t = t.replace("len(lines) >= 56385", f"len(lines) >= {d}")
    t = t.replace("lines[56384]", f"lines[{d - 1}]")
    t += REBASE_COMMENT_213 + "\n"
    return t


# --- travel114: hunk1 COUNT set, hunk2 FREE set + DEF/WRAPPER ---
def t114_hunk1(head, theirs):
    pinmap = {p: mapped[p] for p in PINS["t114_count"]}
    return sub_pins(theirs, pinmap)


def t114_hunk2(head, theirs):
    pinmap = {p: mapped[p] for p in PINS["t114_free2"]}
    pinmap[56385] = mapped[56385]
    pinmap[45192] = mapped[45192]
    body = sub_pins(theirs, pinmap)
    # keep both sides' resync comments, append new one
    comments = []
    for ln in theirs.splitlines(keepends=True):
        if ln.lstrip().startswith("# v20a213 resync"):
            comments.append(ln)
    for ln in head.splitlines(keepends=True):
        if ln.lstrip().startswith("# v20a212 rebase"):
            comments.append(ln)
    # strip the old trailing resync comments from body (they sit at the end)
    body_lines = body.splitlines(keepends=True)
    body_lines = [ln for ln in body_lines
                  if not ln.lstrip().startswith("# v20a213 resync")]
    body = "".join(body_lines)
    d = mapped[56385]
    w = mapped[45192]
    comments.append(
        f"# v20a213 rebase 上 main 17c6f69 resync：COUNT／FREE／DEF／WRAPPER 按 "
        f"difflib 映射重寫（DEF {d}／WRAPPER {w}），"
        f"qa213/resync213_rebase.py 核實純漂移。\n")
    return body + "".join(comments)


resolve("tests/test_gift185_static.py", [gift185_hunk])
resolve("tests/test_rom176_static.py", [rom176_hunk])
resolve("tests/test_tang171_static.py", [tang_hunk])
resolve("tests/test_tang173_static.py", [tang_hunk])
resolve("tests/test_travel114_static.py", [t114_hunk1, t114_hunk2])
print("ALL PINS MAPPED + FILES RESOLVED")
