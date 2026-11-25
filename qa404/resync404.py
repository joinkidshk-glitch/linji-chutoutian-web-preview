#!/usr/bin/env python3
"""v404 resync：index.html 淨 +189 行（51896→52085；第十一輪頭五項＋掣量裁決）。

(a) 釘行按 difflib 映射重寫，內容逐字核實純漂移：
    rom159 6 釘＋全佳行；rom176 6 釘；tang152 兩釘；text125 三錨點；
    travel114 FREE／COUNT／DEF／WRAPPER；tang171／tang173／gift185 總行數＋DEF；
    tang173 lines[5410] 釘（8 處）。
(b) 有意圖行為改動（測試同步更新，唔係漂移）：
    · 確認閘刪除（用戶拍板）——flow45／v392／v397 改斷言閘已刪＋掣名。
    · 選單 6→3——menu72 改新清單。
    · 進度 chip 改靜態徽章——hub77／ui128a1／ui108／terms57 改斷言。
    · 推介卡片酬獨立行——s30dedup D3 改斷言。
    · 茶餐廳點菜紙早退條件——tang169 B2 改斷言。
    · 人情債過期便條插入——weave47 改組成斷言。
    · 日結 scene modal 計數——v398 改計數。
用法：python3 qa404/resync404.py（OLD 攞 v403 main ce3b547）。
"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "ce3b547:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 51896, len(OLD) - 1
assert len(NEW) - 1 == 52085, len(NEW) - 1


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note):
    src = read(path)
    if src.split("\n")[0].startswith(("# v404 resync", "// v404 resync")):
        print(f"skip {path}（已註記）")
        return
    for old, new, n in subs:
        c = src.count(old)
        assert c == n, f"{path}: {old[:70]!r} count={c} expect={n}"
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


def _current_set(src, name):
    m = re.search(name + r" = \{(.*?)\n\}", src, re.S)
    assert m, name
    return [int(x) for x in re.findall(r"^\s*(\d+),", m.group(1), flags=re.M)]


_travel_src = read("tests/test_travel114_static.py")
FREE_MAP = {o: map_line(o) for o in _current_set(_travel_src, "FREE_LINES")}
COUNT_MAP = {o: map_line(o) for o in _current_set(_travel_src, "COUNT_LINES")}
DEF_NEW = map_line(46647)
WRAP_NEW = map_line(32750)
print(f"travel114 FREE {len(FREE_MAP)} COUNT {len(COUNT_MAP)} DEF->{DEF_NEW} WRAP->{WRAP_NEW}")


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.split("\n")[0].startswith("# v404 resync"):
        print(f"skip {path}")
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
    for old, new, n in [("DEF_LINE = 46647", f"DEF_LINE = {DEF_NEW}", 1),
                        ("WRAPPER_LINE = 32750", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, "# v404 resync：index.html 淨 +189 行（51896→52085）；FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；見 qa404/resync404.py。")
    write(path, "\n".join(lines))
    print(f"patched {path}")


resync_travel114()

patch("tests/test_rom159_static.py",
      [(f'line_has(28877, "v20a159 ROM159 Phase 1")', f'line_has({map_line(28877)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(9796, "rom159GainAllowed(k)")', f'line_has({map_line(9796)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(29785, "COMMIT48_NODES.CMT_lan_commit")', f'line_has({map_line(29785)}, "COMMIT48_NODES.CMT_lan_commit")', 1),
       (f'line_has(11976, "rom159PrepareNode(node)")', f'line_has({map_line(11976)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(16608, "rom159ApplyGiftOverrides()")', f'line_has({map_line(16608)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(29640, "function rom159SoMeetGate")', f'line_has({map_line(29640)}, "function rom159SoMeetGate")', 1)],
      "# v404 resync：index.html 淨 +189 行；6 個 line_has 釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa404/resync404.py。")
# 全佳行（idx_lines）
_r159 = read("tests/test_rom159_static.py")
_m = re.search(r'"查實" in idx_lines\[(\d+)\]', _r159)
if _m:
    _old = int(_m.group(1))
    _new = map_line(_old + 1) - 1
    _r159 = _r159.replace(f'"查實" in idx_lines[{_old}]', f'"查實" in idx_lines[{_new}]', 1)
    write("tests/test_rom159_static.py", _r159)
    print("patched rom159 全佳行")

patch("tests/test_rom176_static.py",
      [(f"line(7922).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'", f"line({map_line(7922)}).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'", 1),
       ("line(16606)", f"line({map_line(16606)})", 2),
       (f"line(44605).startswith('/* ===== v20a176 ROM176'", f"line({map_line(44605)}).startswith('/* ===== v20a176 ROM176'", 1),
       (f"line(44964).startswith('function rom176ApplyGiftOverrides()')", f"line({map_line(44964)}).startswith('function rom176ApplyGiftOverrides()')", 1),
       (f"line(46530).startswith('function addLocTalkGiftActs(add, L, npcId)')", f"line({map_line(46530)}).startswith('function addLocTalkGiftActs(add, L, npcId)')", 1),
       (f"'rom176TryIntercept(id)' in line(46688)", f"'rom176TryIntercept(id)' in line({map_line(46688)})", 1)],
      "# v404 resync：index.html 淨 +189 行；6 個 line() 釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa404/resync404.py。")
patch("tests/test_tang152_static.py",
      [("lines()[16535].startswith('function normaliseTangStub152(pack){')", f"lines()[{map_line(16536) - 1}].startswith('function normaliseTangStub152(pack){{')", 1),
       ("lines()[16660].strip().startswith('try{ normaliseTangStub152(rom2);')", f"lines()[{map_line(16661) - 1}].strip().startswith('try{{ normaliseTangStub152(rom2);')", 1)],
      "# v404 resync：index.html 淨 +189 行；normaliseTangStub152 兩釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa404/resync404.py。")
patch("tests/test_text125_static.py",
      [("if len(ls) < 12556 or FALLBACK not in ls[12555]:", f"if len(ls) < {map_line(12556)} or FALLBACK not in ls[{map_line(12556) - 1}]:", 1),
       ('probs.append("currentLine 第 12556 行冇 text fallback")', f'probs.append("currentLine 第 {map_line(12556)} 行冇 text fallback")', 1),
       ("v403 resync：12510→12556（difflib 對位核實純漂移，見 qa403/resync403.py）", f"v403 resync：12510→12556（difflib 對位核實純漂移，見 qa403/resync403.py）；v404 resync：12556→{map_line(12556)}（difflib 對位核實純漂移，見 qa404/resync404.py）", 1),
       ("if len(ls) < 12698 or FALLBACK not in ls[12697]:", f"if len(ls) < {map_line(12698)} or FALLBACK not in ls[{map_line(12698) - 1}]:", 1),
       ('probs.append("advance 第 12698 行冇 text fallback")', f'probs.append("advance 第 {map_line(12698)} 行冇 text fallback")', 1),
       ("v403 resync：12652→12698（difflib 對位核實純漂移，見 qa403/resync403.py）", f"v403 resync：12652→12698（difflib 對位核實純漂移，見 qa403/resync403.py）；v404 resync：12698→{map_line(12698)}（difflib 對位核實純漂移，見 qa404/resync404.py）", 1),
       ("if len(ls) < 18321 or 'if(typeof b.text === \"string\" && b.text){' not in ls[18320]:", f"if len(ls) < {map_line(18321)} or 'if(typeof b.text === \"string\" && b.text){{' not in ls[{map_line(18321) - 1}]:", 1),
       ('probs.append("applyFamilySafeToNode 第 18321 行冇 b.text 分支")', f'probs.append("applyFamilySafeToNode 第 {map_line(18321)} 行冇 b.text 分支")', 1),
       ("v403 resync：18275→18321（difflib 對位核實純漂移，見 qa403/resync403.py）", f"v403 resync：18275→18321（difflib 對位核實純漂移，見 qa403/resync403.py）；v404 resync：18321→{map_line(18321)}（difflib 對位核實純漂移，見 qa404/resync404.py）", 1)],
      "# v404 resync：index.html 淨 +189 行；三錨點按 difflib 映射重寫，內容逐字核實純漂移；見 qa404/resync404.py。")

for _p in ["tests/test_gift185_static.py", "tests/test_tang171_static.py", "tests/test_tang173_static.py"]:
    _subs = [("總行數 51896（", "總行數 52085（", 1),
             ("＋v403 +125）", "＋v403 +125＋v404 +189）", 1)]
    if "gift185" in _p:
        _subs.append(("html.count('\\n') == 51896", "html.count('\\n') == 52085", 1))
    else:
        _subs.append(("src.count('\\n') == 51896", "src.count('\\n') == 52085", 1))
        _subs.append(("len(lines) >= 46647 and 'function openLoc(id, opts){' in lines[46646]",
                      f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1))
    patch(_p, _subs, "# v404 resync：index.html 淨 +189 行（51896→52085）；openLoc DEF 按 difflib 映射重寫；見 qa404/resync404.py。")

# tang173 lines[5410] 釘（8 處）
_t173 = read("tests/test_tang173_static.py")
_n5410 = map_line(5411) - 1
if _n5410 != 5410:
    _c = _t173.count("lines[5410]")
    _t173 = _t173.replace("lines[5410]", f"lines[{_n5410}]")
    write("tests/test_tang173_static.py", _t173)
    print(f"patched tang173 lines[5410]->[{_n5410}] x{_c}")

print("resync pins done")
