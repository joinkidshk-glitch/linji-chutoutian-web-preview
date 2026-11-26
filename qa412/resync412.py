#!/usr/bin/env python3
"""v412 resync：index.html 淨 +99 行（52448→52547；UI412 呈現層修復）。
釘行按 difflib 映射重寫，內容逐字核實純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。
用法：python3 qa412/resync412.py（OLD 攞 HEAD=v411，assert 總行數 52448）。
"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 52448, len(OLD) - 1
assert len(NEW) - 1 == 52547, len(NEW) - 1


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note):
    src = read(path)
    if src.split("\n")[0].startswith(("# v412 resync", "// v412 resync")):
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


def _current_set(src, name):
    m = re.search(name + r" = \{(.*?)\n\}", src, re.S)
    assert m, name
    return [int(x) for x in re.findall(r"^\s*(\d+),", m.group(1), flags=re.M)]


_travel_src = read("tests/test_travel114_static.py")
FREE_MAP = {o: map_line(o) for o in _current_set(_travel_src, "FREE_LINES")}
COUNT_MAP = {o: map_line(o) for o in _current_set(_travel_src, "COUNT_LINES")}
print(f"travel114 FREE {len(FREE_MAP)} 處 COUNT {len(COUNT_MAP)} 處")
DEF_NEW = map_line(47232)
WRAP_NEW = map_line(33296)
print(f"travel114 DEF 47232->{DEF_NEW} WRAPPER 33296->{WRAP_NEW}")


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.split("\n")[0].startswith("# v412 resync"):
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
    for old, new, n in [("DEF_LINE = 47232", f"DEF_LINE = {DEF_NEW}", 1),
                        ("WRAPPER_LINE = 33296", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, "# v412 resync：index.html 淨 +99 行（52448→52547）；FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；見 qa412/resync412.py。")
    write(path, "\n".join(lines))
    print(f"patched {path}")


patch("tests/test_rom159_static.py",
      [(f'line_has(29396, "v20a159 ROM159 Phase 1")',
        f'line_has({map_line(29396)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(9915, "rom159GainAllowed(k)")',
        f'line_has({map_line(9915)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(30308, "COMMIT48_NODES.CMT_lan_commit")',
        f'line_has({map_line(30308)}, "COMMIT48_NODES.CMT_lan_commit")', 1),
       (f'line_has(12123, "rom159PrepareNode(node)")',
        f'line_has({map_line(12123)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(16760, "rom159ApplyGiftOverrides()")',
        f'line_has({map_line(16760)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(30163, "function rom159SoMeetGate")',
        f'line_has({map_line(30163)}, "function rom159SoMeetGate")', 1),
       ('"查實" in idx_lines[29423]', f'"查實" in idx_lines[{map_line(29424) - 1}]', 1)],
      "# v412 resync：index.html 淨 +99 行；6 個 line_has 釘行＋全佳行按 difflib 映射重寫，內容逐字核實純漂移；見 qa412/resync412.py。")
patch("tests/test_rom176_static.py",
      [(f"line(8061).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'",
        f"line({map_line(8061)}).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'", 1),
       ("line(16758)", f"line({map_line(16758)})", 2),
       (f"line(45160).startswith('/* ===== v20a176 ROM176'",
        f"line({map_line(45160)}).startswith('/* ===== v20a176 ROM176'", 1),
       (f"line(45519).startswith('function rom176ApplyGiftOverrides()')",
        f"line({map_line(45519)}).startswith('function rom176ApplyGiftOverrides()')", 1),
       (f"line(47085).startswith('function addLocTalkGiftActs(add, L, npcId)')",
        f"line({map_line(47085)}).startswith('function addLocTalkGiftActs(add, L, npcId)')", 1),
       (f"'rom176TryIntercept(id)' in line(47275)",
        f"'rom176TryIntercept(id)' in line({map_line(47275)})", 1)],
      "# v412 resync：index.html 淨 +99 行；6 個 line() 釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa412/resync412.py。")
patch("tests/test_gift185_static.py",
      [("總行數 52448（", "總行數 52547（", 1),
       ("== 52448)", "== 52547)", 1),
       ("＋v411 +64）'", "＋v411 +64＋v412 +99）'", 1)],
      "# v412 resync：index.html 淨 +99 行（52448→52547）；見 qa412/resync412.py。")

patch("tests/test_tang152_static.py",
      [("lines()[16687].startswith('function normaliseTangStub152(pack){')",
        f"lines()[{map_line(16688) - 1}].startswith('function normaliseTangStub152(pack){{')", 1),
       ("lines()[16812].strip().startswith('try{ normaliseTangStub152(rom2);')",
        f"lines()[{map_line(16813) - 1}].strip().startswith('try{{ normaliseTangStub152(rom2);')", 1)],
      "# v412 resync：index.html 淨 +99 行；normaliseTangStub152 兩釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa412/resync412.py。")
patch("tests/test_text125_static.py",
      [("if len(ls) < 12640 or FALLBACK not in ls[12703]:",
        f"if len(ls) < {map_line(12704)} or FALLBACK not in ls[{map_line(12704) - 1}]:", 1),
       ('probs.append("currentLine 第 12704 行冇 text fallback")',
        f'probs.append("currentLine 第 {map_line(12704)} 行冇 text fallback")', 1),
       ("if len(ls) < 12782 or FALLBACK not in ls[12845]:",
        f"if len(ls) < {map_line(12846)} or FALLBACK not in ls[{map_line(12846) - 1}]:", 1),
       ('probs.append("advance 第 12846 行冇 text fallback")',
        f'probs.append("advance 第 {map_line(12846)} 行冇 text fallback")', 1),
       ("if len(ls) < 18496 or 'if(typeof b.text === \"string\" && b.text){' not in ls[18561]:",
        f"if len(ls) < {map_line(18562)} or 'if(typeof b.text === \"string\" && b.text){{' not in ls[{map_line(18562) - 1}]:", 1),
       ('probs.append("applyFamilySafeToNode 第 18562 行冇 b.text 分支")',
        f'probs.append("applyFamilySafeToNode 第 {map_line(18562)} 行冇 b.text 分支")', 1)],
      "# v412 resync：index.html 淨 +99 行；三錨點按 difflib 映射重寫，內容逐字核實純漂移；見 qa412/resync412.py。")

resync_travel114()
print("v412 resync done")
