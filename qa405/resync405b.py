#!/usr/bin/env python3
"""v405 resync 第二段：P1-7 在場盤改進令 index.html 再 +13 行（52214→52227）。
OLD=e93ff24（rebase 後第一段 resync 完成態），釘行按 difflib 映射重寫。"""
import difflib, os, re, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "e93ff24:index.html"], cwd=ROOT, capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 52214, len(OLD) - 1
assert len(NEW) - 1 == 52227, len(NEW) - 1

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

def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f: return f.read()
def write(p, s):
    with open(os.path.join(ROOT, p), "w", encoding="utf-8") as f: f.write(s)

def patch(path, subs):
    src = read(path)
    for old, new, n in subs:
        c = src.count(old)
        assert c == n, f"{path}: {old[:50]!r} count={c} expect={n}"
        src = src.replace(old, new)
    write(path, src)
    print(f"patched {path}")

DEF_NEW = map_line(46987)
print("DEF 46987->", DEF_NEW)
patch("tests/test_rom176_static.py",
      [("'rom176TryIntercept(id)' in line(47028)", f"'rom176TryIntercept(id)' in line({map_line(47028)})", 1)])
for t in ("tests/test_gift185_static.py", "tests/test_tang171_static.py", "tests/test_tang173_static.py"):
    subs = [("總行數 52214（", "總行數 52227（", 1), ("== 52214)", "== 52227)", 1),
            ("＋v404 +189＋v405 +129）'", "＋v404 +189＋v405 +142）'", 1)]
    if "tang" in t:
        subs.append(("len(lines) >= 46987 and 'function openLoc(id, opts){' in lines[46986]",
                     f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1))
    patch(t, subs)

# travel114 sets
path = "tests/test_travel114_static.py"
src = read(path)
def _set(name):
    m = re.search(name + r" = \{(.*?)\n\}", src, re.S)
    assert m, name
    return [int(x) for x in re.findall(r"^\s*(\d+),", m.group(1), flags=re.M)]
for name in ("FREE_LINES", "COUNT_LINES"):
    d = {o: map_line(o) for o in _set(name)}
    m = re.search(name + r" = \{(.*?)\n\}", src, re.S)
    span = m.group(1)
    def _rep(mm):
        old = int(mm.group(1))
        assert old in d, f"{name}: {old}"
        return mm.group(0).replace(str(old), str(d[old]), 1)
    src = src[:m.start(1)] + re.sub(r"^\s*(\d+),", _rep, span, flags=re.M) + src[m.end(1):]
assert src.count("DEF_LINE = 46987") == 1
src = src.replace("DEF_LINE = 46987", f"DEF_LINE = {DEF_NEW}")
write(path, src)
print("patched travel114")
print("resync405b done")
