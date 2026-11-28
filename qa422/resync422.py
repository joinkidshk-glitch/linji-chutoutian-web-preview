#!/usr/bin/env python3
"""v422 resync：index.html 淨 +113 行（53099→53212；感情尾段入口＋好感上限文案）。
釘行按 difflib 映射重寫，內容逐字核實純漂移；story172／tang167 兩處係 v422 新呼叫點／新回傳欄嘅斷言同步。
用法：python3 qa422/resync422.py（OLD 攞 HEAD=v421，assert 總行數 53099）。"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 53099, len(OLD) - 1
assert len(NEW) - 1 == 53212, len(NEW) - 1

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


def one_pass(src, repl):
    """單次掃描 dict 查表替換，避免逐對 replace 撞值。"""
    out = []
    i = 0
    keys = sorted(repl, key=len, reverse=True)
    while i < len(src):
        hit = None
        for old in keys:
            if src.startswith(old, i):
                hit = old
                break
        if hit:
            out.append(repl[hit])
            i += len(hit)
        else:
            out.append(src[i])
            i += 1
    return "".join(out)


def patch(path, repl, note):
    src = read(path)
    if src.split("\n")[0].startswith("# v422 resync"):
        print(f"skip {path}（已註記）")
        return
    for old in repl:
        assert old in src, f"{path}: missing {old[:80]!r}"
    src = one_pass(src, repl)
    lines = src.split("\n")
    lines.insert(0, note)
    write(path, "\n".join(lines))
    print(f"patched {path}")


def _current_set(src, name):
    m = re.search(name + r" = \{(.*?)\n\}", src, re.S)
    assert m, name
    return [int(x) for x in re.findall(r"^\s*(\d+),", m.group(1), flags=re.M)]


# travel114：FREE／COUNT／DEF／WRAPPER 按 difflib 映射
_travel_src = read("tests/test_travel114_static.py")
FREE_MAP = {o: map_line(o) for o in _current_set(_travel_src, "FREE_LINES")}
COUNT_MAP = {o: map_line(o) for o in _current_set(_travel_src, "COUNT_LINES")}
_def_m = re.search(r"DEF_LINE = (\d+)", _travel_src)
_wrap_m = re.search(r"WRAPPER_LINE = (\d+)", _travel_src)
DEF_OLD, WRAP_OLD = int(_def_m.group(1)), int(_wrap_m.group(1))
DEF_NEW, WRAP_NEW = map_line(DEF_OLD), map_line(WRAP_OLD)
print(f"travel114 FREE {len(FREE_MAP)} COUNT {len(COUNT_MAP)} DEF {DEF_OLD}->{DEF_NEW} WRAPPER {WRAP_OLD}->{WRAP_NEW}")


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.split("\n")[0].startswith("# v422 resync"):
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
    src = one_pass(src, {f"DEF_LINE = {DEF_OLD}": f"DEF_LINE = {DEF_NEW}",
                         f"WRAPPER_LINE = {WRAP_OLD}": f"WRAPPER_LINE = {WRAP_NEW}"})
    lines = src.split("\n")
    lines.insert(0, "# v422 resync：index.html 淨 +113 行（53099→53212）；FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；見 qa422/resync422.py。")
    write(path, "\n".join(lines))
    print(f"patched {path}")


resync_travel114()

# rom176：line(n) 釘行
_rom176 = read("tests/test_rom176_static.py")
_rom176_pins = sorted({int(x) for x in re.findall(r"line\((\d+)\)", _rom176)})
patch("tests/test_rom176_static.py",
      {f"line({n})": f"line({map_line(n)})" for n in _rom176_pins},
      "# v422 resync：index.html 淨 +113 行；line() 釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa422/resync422.py。")

# total-count files：總行數＋lines[] 釘
for _p in ["tests/test_gift185_static.py", "tests/test_tang171_static.py", "tests/test_tang173_static.py"]:
    _src = read(_p)
    _repl = {"總行數 53099（": "總行數 53212（", "== 53099)": "== 53212)"}
    if "＋v421 +29）'" in _src:
        _repl["＋v421 +29）'"] = "＋v421 +29＋v422 +113）'"
    if "＋v421 +23，travel114 釘行）'" in _src:
        _repl["＋v421 +23，travel114 釘行）'"] = "＋v421 +23＋v422 +111，travel114 釘行）'"
    for _n in sorted({int(_m) for _m in re.findall(r"lines\[(\d+)\]", _src)}):
        _repl[f"lines[{_n}]"] = f"lines[{map_line(_n + 1) - 1}]"
    patch(_p, _repl, "# v422 resync：index.html 淨 +113 行（53099→53212）；總行數＋釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa422/resync422.py。")

# story172：v422 新增普通 eval offer 寫入點（romance422SyncTailOffers），斷言同步
patch("tests/test_story172_static.py",
      {"ok('範圍：普通 eval 只剩 enterLoc／doTalk 兩處寫 offer（start 已轉交 ignoreSheetLoc，見 §四）',\n   src.count('StoryOC.evalNode(node, { checkNodePhase:true })') == 2)":
       "ok('範圍：普通 eval 只剩 enterLoc／doTalk／v422 感情尾段同步／v422 線索讀取四處（start 已轉交 ignoreSheetLoc，見 §四）',\n   src.count('StoryOC.evalNode(node, { checkNodePhase:true })') == 4)"},
      "# v422 resync：普通 eval 呼叫點由 2 處增至 4 處（新增 romance422SyncTailOffers 主動同步＋romance422TailClue 線索讀取）；見 qa422/resync422.py。")

# tang167：giveGift 回傳新增 paceCapped 欄，斷言同步
patch("tests/test_tang167_static.py",
      {"'kind, delta:applied378, softcap, line, relKey, before, after' in src":
       "'kind, delta:applied378, softcap, paceCapped:(applied>0 && applied378<applied), line, relKey, before, after' in src"},
      "# v422 resync：giveGift 回傳新增 paceCapped 欄，斷言同步；見 qa422/resync422.py。")

print("RESYNC422 DONE")
