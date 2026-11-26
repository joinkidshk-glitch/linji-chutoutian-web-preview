#!/usr/bin/env python3
"""v408 resync：index.html 淨 +63 行（52253→52316；第十三輪頭五項＋裁決修復）。
釘行全部按 difflib 映射重寫，內容逐字核實純漂移；有意圖行為改動嘅測試
（hub77／progress71／terms57／ui108／ui128a1 chip 刪除）已喺各自 test 直接更新，唔經呢度。
紀律：travel114 兩個 set 用單次掃描 dict 查表；其餘逐處 replace assert 恰好一次；
ok() 名入面嘅 L 號係歷史標籤，唔郁（總行數鏈同報錯字串行號例外，一併更新）。
用法：python3 qa408/resync408.py（OLD 攞 v407 main 6af55f1，assert 總行數 52253）。
"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "6af55f1:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 52253, len(OLD) - 1
assert len(NEW) - 1 == 52316, len(NEW) - 1


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note):
    src = read(path)
    if src.split("\n")[0].startswith(("# v408 resync", "// v408 resync")):
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


NOTE = "# v408 resync：index.html 淨 +63 行（52253→52316）；釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa408/resync408.py。"

# --- 總行數鏈＋DEF／L4872 釘（gift185／tang171／tang173，同一 patch 內做齊） ---
_def_new = map_line(47037) - 1
_l4872_new = map_line(5405) - 1
_n173 = read("tests/test_tang173_static.py").count("lines[5404]")
patch("tests/test_gift185_static.py", [
    ("總行數 52253（", "總行數 52316（", 1),
    ("v407 −120）", "v407 −120＋v408 +63）", 1),
    ("== 52253", "== 52316", 1),
], NOTE)
patch("tests/test_tang171_static.py", [
    ("總行數 52253（", "總行數 52316（", 1),
    ("v407 −120）", "v407 −120＋v408 +63）", 1),
    ("== 52253", "== 52316", 1),
    ("lines[47036]", f"lines[{_def_new}]", 1),
], NOTE)
patch("tests/test_tang173_static.py", [
    ("總行數 52253（", "總行數 52316（", 1),
    ("v407 −120）", "v407 −120＋v408 +63）", 1),
    ("== 52253", "== 52316", 1),
    ("lines[47036]", f"lines[{_def_new}]", 1),
    ("lines[5404]", f"lines[{_l4872_new}]", _n173),
], NOTE)

# --- rom159 line_has 釘＋全佳行 ---
_subs159 = []
for _old in (29218, 9852, 30130, 12060, 16696, 29985):
    _subs159.append((f"line_has({_old},", f"line_has({map_line(_old)},", 1))
_subs159.append(("idx_lines[29245]", f"idx_lines[{map_line(29246) - 1}]", 1))
patch("tests/test_rom159_static.py", _subs159, NOTE)

# --- rom176 line() 釘 ---
_subs176 = []
for _old in (7998, 16694, 44965, 45324, 46890, 47080):
    _subs176.append((f"line({_old})", f"line({map_line(_old)})", 2 if _old == 16694 else 1))
patch("tests/test_rom176_static.py", _subs176, NOTE)

# --- tang152 lines()[] 釘（0-based） ---
patch("tests/test_tang152_static.py", [
    ("lines()[16623]", f"lines()[{map_line(16624) - 1}]", 1),
    ("lines()[16748]", f"lines()[{map_line(16749) - 1}]", 1),
], NOTE)

# --- text125 三錨（ls[] 0-based＋報錯字串行號） ---
_cl = map_line(12640)
_adv = map_line(12782)
_fs = map_line(18496)
patch("tests/test_text125_static.py", [
    ("ls[12639]", f"ls[{_cl - 1}]", 1),
    ("currentLine 第 12640 行", f"currentLine 第 {_cl} 行", 1),
    ("ls[12781]", f"ls[{_adv - 1}]", 1),
    ("advance 第 12782 行", f"advance 第 {_adv} 行", 1),
    ("ls[18495]", f"ls[{_fs - 1}]", 1),
    ("applyFamilySafeToNode 第 18496 行", f"applyFamilySafeToNode 第 {_fs} 行", 1),
], NOTE)

# --- travel114：COUNT／FREE 兩 set 單次掃描 dict 查表＋DEF／WRAPPER ---
_p114 = "tests/test_travel114_static.py"
_src114 = read(_p114)
assert not _src114.split("\n")[0].startswith("# v408 resync")
for _setname in ("COUNT_LINES", "FREE_LINES"):
    _m = re.search(_setname + r" = \{(.*?)\n\}", _src114, re.S)
    assert _m, _setname
    _body = _m.group(1)
    _nums = [int(x) for x in re.findall(r"^\s*(\d+),", _body, re.M)]
    _table = {str(n): str(map_line(n)) for n in _nums}
    _newbody = re.sub(r"^(\s*)(\d+),", lambda mm: mm.group(1) + _table[mm.group(2)] + ",", _body, flags=re.M)
    _src114 = _src114[:_m.start(1)] + _newbody + _src114[_m.end(1):]
    print(f"{_setname}: {len(_nums)} 錨點映射完成")
_src114 = _src114.replace("DEF_LINE = 47037", f"DEF_LINE = {map_line(47037)}", 1)
_src114 = _src114.replace("WRAPPER_LINE = 33103", f"WRAPPER_LINE = {map_line(33103)}", 1)
_lines114 = _src114.split("\n")
_lines114.insert(0, NOTE)
write(_p114, "\n".join(_lines114))
print(f"patched {_p114}")

print("RESYNC408 DONE")
