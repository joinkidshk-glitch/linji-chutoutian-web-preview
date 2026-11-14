#!/usr/bin/env python3
"""v20a193 第二次 rebase（上 main 707ff66＝v194）之後的行號 resync。

原理同 qa193/resync193_rebase.py：707ff66:index.html（HEAD 版）→ 工作樹
index.html（已合併 v193 改動）之間只係 v193 插入（淨 +179），被釘嘅行
本身內容唔變。用 difflib 對位，將 HEAD 版測試入面嘅行號逐個映射。

用法：python3 qa193/resync193_rebase2.py [--apply]
只印對照表；--apply 先以 HEAD 版（stage 2）做底寫入解析檔。
"""
import difflib
import re
import subprocess
import sys

REPO = "/home/hatch/workspace/linji-work193"
BASE = "707ff66"


def sh(*args):
    return subprocess.check_output(args, cwd=REPO, text=True)


def build_map():
    base = sh("git", "show", f"{BASE}:index.html").split("\n")
    cur = open(f"{REPO}/index.html", encoding="utf-8").read().split("\n")
    print(f"base lines: {len(base)}, cur lines: {len(cur)}")
    sm = difflib.SequenceMatcher(None, base, cur, autojunk=False)
    mapping = {}
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                mapping[i1 + k + 1] = j1 + k + 1  # 1-based
    return mapping, base, cur


def check(mapping, base, cur, n, expect_sub=None):
    m = mapping.get(n)
    if m is None:
        return (n, None, f"行 {n} 唔喺 equal 區（被 v193 改過？）")
    content = cur[m - 1] if m - 1 < len(cur) else "<EOF>"
    base_content = base[n - 1] if n - 1 < len(base) else "<EOF>"
    flag = ""
    if base_content != content:
        flag = f"  !! 內容唔同：base={base_content.strip()[:80]!r}"
    if expect_sub and expect_sub not in content:
        flag += f"  !! 預期含 {expect_sub!r} 但冇"
    return (n, m, content.strip()[:110] + flag)


def travel_numbers(head_text):
    hlines = head_text.split("\n")
    in_count = in_free = False
    count_ns, free_ns = [], []
    def_line = wrapper_line = None
    for ln in hlines:
        if ln.startswith("COUNT_LINES"):
            in_count = True
            continue
        if ln.startswith("FREE_LINES"):
            in_free = True
            in_count = False
            continue
        if ln.startswith("FREE_FLAGS"):
            in_free = False
            continue
        m = re.match(r"^\s*(\d+),", ln)
        if m and in_count:
            count_ns.append(int(m.group(1)))
        if m and in_free:
            free_ns.append(int(m.group(1)))
        m2 = re.match(r"^DEF_LINE = (\d+)", ln)
        if m2:
            def_line = int(m2.group(1))
        m3 = re.match(r"^WRAPPER_LINE = (\d+)", ln)
        if m3:
            wrapper_line = int(m3.group(1))
    return count_ns, free_ns, def_line, wrapper_line


def main():
    mapping, base, cur = build_map()
    total_newlines = open(f"{REPO}/index.html", encoding="utf-8").read().count("\n")
    print(f"current total newlines: {total_newlines}")

    for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
        head = sh("git", "show", f":2:{fname}")
        m = re.search(r"'function openLoc\(id, opts\)\{' in lines\[(\d+)\]", head)
        head_def = int(m.group(1)) + 1  # 1-based
        print(f"\n== {fname} ==")
        old, new, content = check(mapping, base, cur, head_def,
                                  "function openLoc(id, opts){")
        print(f"  HEAD {old} -> {new} : {content}")

    print("\n== tests/test_travel114_static.py ==")
    head = sh("git", "show", ":2:tests/test_travel114_static.py")
    count_ns, free_ns, def_line, wrapper_line = travel_numbers(head)
    print(f"  COUNT ({len(count_ns)}):")
    for n in count_ns:
        old, new, content = check(mapping, base, cur, n)
        print(f"    HEAD {old} -> {new} : {content}")
    print(f"  FREE ({len(free_ns)}):")
    for n in free_ns:
        old, new, content = check(mapping, base, cur, n)
        print(f"    HEAD {old} -> {new} : {content}")
    for label, n in (("DEF", def_line), ("WRAPPER", wrapper_line)):
        old, new, content = check(mapping, base, cur, n)
        print(f"  {label}: HEAD {old} -> {new} : {content}")

    if "--apply" in sys.argv:
        print("\n--apply：寫入解析檔…")
        apply_all(mapping, total_newlines)


def apply_all(mapping, total_newlines):
    # 用 lambda 做 re.sub replacement，避免 \n 被當換行（第一次 rebase 教訓）。
    for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
        p = f"{REPO}/{fname}"
        s = sh("git", "show", f":2:{fname}")
        m = re.search(r"'function openLoc\(id, opts\)\{' in lines\[(\d+)\]", s)
        head_def = int(m.group(1)) + 1
        new_def = mapping[head_def]
        s = re.sub(r"src\.count\('\\n'\) == \d+",
                   lambda _: f"src.count('\\n') == {total_newlines}", s)
        s = re.sub(r"len\(lines\) >= \d+ and 'function openLoc\(id, opts\)\{' in lines\[\d+\]",
                   lambda _: f"len(lines) >= {new_def} and 'function openLoc(id, opts){{' in lines[{new_def - 1}]", s)
        open(p, "w", encoding="utf-8").write(s)
        print(f"  {fname} done (openLoc DEF -> {new_def}, total -> {total_newlines})")

    p = f"{REPO}/tests/test_travel114_static.py"
    head = sh("git", "show", ":2:tests/test_travel114_static.py")
    hlines = head.split("\n")
    out = []
    in_count = in_free = False
    for ln in hlines:
        if ln.startswith("COUNT_LINES"):
            in_count = True
            out.append(ln)
            continue
        if ln.startswith("FREE_LINES"):
            in_free = True
            in_count = False
            out.append(ln)
            continue
        if ln.startswith("FREE_FLAGS"):
            in_free = False
            out.append(ln)
            continue
        m = re.match(r"^(\s*)(\d+),(.*)$", ln)
        if m and (in_count or in_free):
            old = int(m.group(2))
            new = mapping.get(old)
            assert new is not None, f"travel114 行 {old} 映射唔到"
            out.append(f"{m.group(1)}{new},{m.group(3)}")
            continue
        m2 = re.match(r"^(DEF_LINE = )(\d+)(.*)$", ln)
        if m2:
            out.append(f"{m2.group(1)}{mapping[int(m2.group(2))]}{m2.group(3)}")
            continue
        m3 = re.match(r"^(WRAPPER_LINE = )(\d+)(.*)$", ln)
        if m3:
            out.append(f"{m3.group(1)}{mapping[int(m3.group(2))]}{m3.group(3)}")
            continue
        out.append(ln)
    open(p, "w", encoding="utf-8").write("\n".join(out))
    print("  travel114 done")


if __name__ == "__main__":
    main()
