#!/usr/bin/env python3
"""v420 resync：index.html 淨 +14 行（53056→53070；UI420 呈現層修復）。
釘行按 difflib 映射重寫，內容逐字核實純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。
用法：python3 qa420/resync420.py（OLD 攞 HEAD=v419，assert 總行數 53056）。"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 53056, len(OLD) - 1
assert len(NEW) - 1 == 53070, len(NEW) - 1

_sm = difflib.SequenceMatcher(a=OLD, b=NEW, autojunk=False)
_map = {}
for _tag, _i1, _i2, _j1, _j2 in _sm.get_opcodes():
    if _tag == "equal":
        for _k in range(_i2 - _i1):
            _map[_i1 + _k] = _j1 + _k


def map_line(old_1based):
    n = _map.get(old_1based - 1)
    assert n is not None, f"line {old_1based} not in equal blocks"
    assert OLD[old_1based - 1] == NEW[n], f"line {old_1based} content changed"
    return n + 1


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note):
    src = read(path)
    if src.split("\n")[0].startswith(("# v420 resync", "// v420 resync")):
        print(f"skip {path}（已註記）")
        return
    for old, new, n in subs:
        c = src.count(old)
        assert c == n, f"{path}: {old[:60]!r} count={c} expect={n}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, note)
    write(path, "\n".join(lines))
    print(f"patched {path}")


def _current_set(src, name):
    m = re.search(name + r" = \{(.*?)\n\}", src, re.S)
    assert m, name
    return [int(x) for x in re.findall(r"^\s*(\d+),", m.group(1), flags=re.M)]


# travel114
_travel_src = read("tests/test_travel114_static.py")
FREE_MAP = {o: map_line(o) for o in _current_set(_travel_src, "FREE_LINES")}
COUNT_MAP = {o: map_line(o) for o in _current_set(_travel_src, "COUNT_LINES")}
_def_m = re.search(r"DEF_LINE = (\d+)", _travel_src); _wrap_m = re.search(r"WRAPPER_LINE = (\d+)", _travel_src)
DEF_OLD, WRAP_OLD = int(_def_m.group(1)), int(_wrap_m.group(1))
DEF_NEW, WRAP_NEW = map_line(DEF_OLD), map_line(WRAP_OLD)
print(f"travel114 FREE {len(FREE_MAP)} COUNT {len(COUNT_MAP)} DEF {DEF_OLD}->{DEF_NEW} WRAPPER {WRAP_OLD}->{WRAP_NEW}")


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.split("\n")[0].startswith("# v420 resync"):
        print(f"skip {path}（已註記）")
        return

    def _sub_set(src, name, d):
        m = re.search(name + r" = \{(.*?)\n\}", src, re.S)
        assert m, name
        span = m.group(1)
        used = set()

        def _rep(mm):
            old = int(mm.group(1))
            assert old in d, f"{name}: {old} not in map"
            used.add(old)
            return mm.group(0).replace(str(old), str(d[old]), 1)

        new_span = re.sub(r"^\s*(\d+),", _rep, span, flags=re.M)
        assert used == set(d), f"{name}: unused {set(d) - used}"
        return src[:m.start(1)] + new_span + src[m.end(1):]

    src = _sub_set(src, "FREE_LINES", FREE_MAP)
    src = _sub_set(src, "COUNT_LINES", COUNT_MAP)
    for old, new, n in [(f"DEF_LINE = {DEF_OLD}", f"DEF_LINE = {DEF_NEW}", 1),
                        (f"WRAPPER_LINE = {WRAP_OLD}", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, "# v420 resync：index.html 淨 +14 行（53056→53070）；FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；見 qa420/resync420.py。")
    write(path, "\n".join(lines))
    print(f"patched {path}")


resync_travel114()


def remap_pins(path, note):
    src = read(path)
    if src.split("\n")[0].startswith(("# v420 resync", "// v420 resync")):
        print(f"skip {path}（已註記）")
        return
    pats = [
        (r"line_has\((\d+),", lambda n: f"line_has({map_line(n)},"),
        (r"idx_lines\[(\d+)\]", lambda n: f"idx_lines[{map_line(n + 1) - 1}]"),
        (r"lines\(\)\[(\d+)\]", lambda n: f"lines()[{map_line(n + 1) - 1}]"),
        (r"lines\[(\d+)\]", lambda n: f"lines[{map_line(n + 1) - 1}]"),
        (r"line\((\d+)\)", lambda n: f"line({map_line(n)})"),
        (r"len\(ls\) < (\d+)", lambda n: f"len(ls) < {map_line(n)}"),
        (r"ls\[(\d+)\]", lambda n: f"ls[{map_line(n + 1) - 1}]"),
    ]
    total = 0
    for pat, fn in pats:
        def _rep(mm, fn=fn):
            return fn(int(mm.group(1)))
        src, c = re.subn(pat, _rep, src)
        total += c
    assert total > 0, f"{path}: no pins remapped"
    lines = src.split("\n")
    lines.insert(0, note)
    write(path, "\n".join(lines))
    print(f"patched {path} ({total} pins)")


for _p in ["tests/test_rom176_static.py",
           "tests/test_tang152_static.py", "tests/test_text125_static.py"]:
    remap_pins(_p, "# v420 resync：index.html 淨 +14 行；釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa420/resync420.py。")

# rom159：逐項明確替換
patch("tests/test_rom159_static.py",
      [(f'line_has(29947, "v20a159 ROM159 Phase 1")', f'line_has({map_line(29947)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(10305, "rom159GainAllowed(k)")', f'line_has({map_line(10305)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(30860, "COMMIT48_NODES.CMT_lan_commit")', f'line_has({map_line(30860)}, "COMMIT48_NODES.CMT_lan_commit")', 1),
       (f'line_has(12513, "rom159PrepareNode(node)")', f'line_has({map_line(12513)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(17150, "rom159ApplyGiftOverrides()")', f'line_has({map_line(17150)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(30715, "function rom159SoMeetGate")', f'line_has({map_line(30715)}, "function rom159SoMeetGate")', 1),
       ('"查實" in idx_lines[29974]', f'"查實" in idx_lines[{map_line(29975) - 1}]', 1)],
      "# v420 resync：index.html 淨 +14 行；6 個 line_has 釘行＋全佳行按 difflib 映射重寫，內容逐字核實純漂移；見 qa420/resync420.py。")

# total-count files
for _p in ["tests/test_gift185_static.py", "tests/test_tang171_static.py", "tests/test_tang173_static.py"]:
    subs = [("總行數 53056（", "總行數 53070（", 1),
            ("== 53056)", "== 53070)", 1),
            ("＋v419 +61）'", "＋v419 +61＋v420 +14）'", 1)]
    src = read(_p)
    if "＋v419 +61，travel114 釘行）'" in src:
        subs.append(("＋v419 +61，travel114 釘行）'", "＋v419 +61＋v420 +14，travel114 釘行）'", 1))
    if "lines[47209]" in src:
        subs.append(("lines[47209]", f"lines[{map_line(47210) - 1}]", src.count("lines[47209]")))
    if "lines[5410]" in src:
        subs.append(("lines[5410]", f"lines[{map_line(5411) - 1}]", src.count("lines[5410]")))
    patch(_p, subs, "# v420 resync：index.html 淨 +14 行（53056→53070）；總行數＋openLoc DEF 釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa420/resync420.py。")

print("RESYNC420 DONE")
