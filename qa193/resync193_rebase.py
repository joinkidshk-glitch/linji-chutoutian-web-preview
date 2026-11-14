#!/usr/bin/env python3
"""v20a193 rebase 上 main b104f85 之後的行號 resync。

原理：b104f85:index.html（HEAD 版）→ 工作樹 index.html（已合併 v193 改動）
之間只係 v193 插入（淨 +179），被釘嘅行本身內容唔變。用 difflib 對位，
將 HEAD 版測試入面嘅行號逐個映射去而家嘅行號，唔靠心算。

用法：python3 qa193/resync193_rebase.py           # 只印對照表
      python3 qa193/resync193_rebase.py --apply   # 以 HEAD 版做底寫入解析檔
"""
import difflib
import re
import subprocess
import sys

REPO = "/home/hatch/workspace/linji-work193"


def sh(*args):
    return subprocess.check_output(args, cwd=REPO, text=True)


def build_map():
    base = sh("git", "show", "b104f85:index.html").split("\n")
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


def main():
    mapping, base, cur = build_map()
    total_newlines = open(f"{REPO}/index.html", encoding="utf-8").read().count("\n")
    print(f"current total newlines: {total_newlines}")

    pins = {
        "tests/test_rom176_static.py": [
            (31583, "GIFT_REACT = giftReact"),
            (53448, "v20a176 ROM176"),
            (53816, "function rom176ApplyGiftOverrides()"),
            (54955, "function addLocTalkGiftActs(add, L, npcId)"),
            (55049, "rom176TryIntercept(id)"),
        ],
        "tests/test_tang171_static.py": [(55018, "function openLoc(id, opts){")],
        "tests/test_tang173_static.py": [(55018, "function openLoc(id, opts){")],
    }
    for path, plist in pins.items():
        print(f"\n== {path} ==")
        for n, sub in plist:
            old, new, content = check(mapping, base, cur, n, sub)
            print(f"  HEAD {old} -> {new} : {content}")

    print("\n== tests/test_travel114_static.py ==")
    head = sh("git", "show", ":2:tests/test_travel114_static.py")
    hlines = head.split("\n")
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
    # 衝突檔一律以 HEAD 版（stage 2，新 main b104f85）做底，再套映射。
    p = f"{REPO}/tests/test_gift185_static.py"
    s = sh("git", "show", ":2:tests/test_gift185_static.py")
    s = re.sub(r"ok\('總行數 [^']*', html\.count\('\\n'\) == \d+\)",
               lambda m: f"ok('總行數 {total_newlines}（v20a193 淨 ＋179 上 main b104f85，行號釘唔漂移）', html.count('\\n') == {total_newlines})", s)
    open(p, "w", encoding="utf-8").write(s)
    print("  gift185 done")

    p = f"{REPO}/tests/test_rom176_static.py"
    s = sh("git", "show", ":2:tests/test_rom176_static.py")
    rom_map = {31583: mapping[31583], 53448: mapping[53448],
               53816: mapping[53816], 54955: mapping[54955],
               55049: mapping[55049]}
    for old, new in rom_map.items():
        s = s.replace(f"line({old})", f"line({new})")
    s = s.replace("釘：ROM176 block 起點 L53050", f"釘：ROM176 block 起點 L{rom_map[53448]}")
    s = s.replace("釘：rom176ApplyGiftOverrides 定義 L53415", f"釘：rom176ApplyGiftOverrides 定義 L{rom_map[53816]}")
    s = s.replace("addLocTalkGiftActs L54447", f"addLocTalkGiftActs L{rom_map[54955]}")
    s = s.replace("openLoc rom176 攔截 L54541", f"openLoc rom176 攔截 L{rom_map[55049]}")
    open(p, "w", encoding="utf-8").write(s)
    print("  rom176 done")

    for fname in ("tests/test_tang171_static.py", "tests/test_tang173_static.py"):
        p = f"{REPO}/{fname}"
        s = sh("git", "show", f":2:{fname}")
        s = re.sub(r"src\.count\('\\n'\) == \d+",
                   lambda m: f"src.count('\\n') == {total_newlines}", s)
        new_def = mapping[55018]
        s = re.sub(r"len\(lines\) >= \d+ and 'function openLoc\(id, opts\)\{' in lines\[\d+\]",
                   f"len(lines) >= {new_def} and 'function openLoc(id, opts){{' in lines[{new_def - 1}]", s)
        open(p, "w", encoding="utf-8").write(s)
        print(f"  {fname} done (openLoc DEF -> {new_def})")

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
