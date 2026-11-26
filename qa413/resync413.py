#!/usr/bin/env python3
"""v413 resync：index.html 淨 +60 行（52547→52607；UI413 呈現層修復）。
釘行按 difflib 映射重寫，內容逐字核實純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。
另更新刻意改動嘅呈現期望：進度「時窗：」→「時間條件相符／未到：」（P4）。
用法：python3 qa413/resync413.py（OLD 攞 HEAD=v412，assert 總行數 52547）。"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 52547, len(OLD) - 1
assert len(NEW) - 1 == 52607, len(NEW) - 1


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note):
    src = read(path)
    if src.split("\n")[0].startswith(("# v413 resync", "// v413 resync")):
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
DEF_NEW = map_line(47331)
WRAP_NEW = map_line(33395)
print(f"travel114 DEF 47331->{DEF_NEW} WRAPPER 33395->{WRAP_NEW}")


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.split("\n")[0].startswith("# v413 resync"):
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
    for old, new, n in [("DEF_LINE = 47331", f"DEF_LINE = {DEF_NEW}", 1),
                        ("WRAPPER_LINE = 33395", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, "# v413 resync：index.html 淨 +60 行（52547→52607）；FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；見 qa413/resync413.py。")
    write(path, "\n".join(lines))
    print(f"patched {path}")


resync_travel114()

patch("tests/test_rom159_static.py",
      [(f'line_has(29492, "v20a159 ROM159 Phase 1")',
        f'line_has({map_line(29492)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(9972, "rom159GainAllowed(k)")',
        f'line_has({map_line(9972)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(30405, "COMMIT48_NODES.CMT_lan_commit")',
        f'line_has({map_line(30405)}, "COMMIT48_NODES.CMT_lan_commit")', 1),
       (f'line_has(12180, "rom159PrepareNode(node)")',
        f'line_has({map_line(12180)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(16817, "rom159ApplyGiftOverrides()")',
        f'line_has({map_line(16817)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(30260, "function rom159SoMeetGate")',
        f'line_has({map_line(30260)}, "function rom159SoMeetGate")', 1),
       ('"查實" in idx_lines[29519]', f'"查實" in idx_lines[{map_line(29520) - 1}]', 1)],
      "# v413 resync：index.html 淨 +60 行；6 個 line_has 釘行＋全佳行按 difflib 映射重寫，內容逐字核實純漂移；見 qa413/resync413.py。")

patch("tests/test_rom176_static.py",
      [(f"line(8118).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'",
        f"line({map_line(8118)}).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'", 1),
       ("line(16815)", f"line({map_line(16815)})", 2),
       (f"line(45259).startswith('/* ===== v20a176 ROM176'",
        f"line({map_line(45259)}).startswith('/* ===== v20a176 ROM176'", 1),
       (f"line(45618).startswith('function rom176ApplyGiftOverrides()')",
        f"line({map_line(45618)}).startswith('function rom176ApplyGiftOverrides()')", 1),
       (f"line(47184).startswith('function addLocTalkGiftActs(add, L, npcId)')",
        f"line({map_line(47184)}).startswith('function addLocTalkGiftActs(add, L, npcId)')", 1),
       (f"'rom176TryIntercept(id)' in line(47374)",
        f"'rom176TryIntercept(id)' in line({map_line(47374)})", 1)],
      "# v413 resync：index.html 淨 +60 行；6 個 line() 釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa413/resync413.py。")

patch("tests/test_gift185_static.py",
      [("總行數 52547（", "總行數 52607（", 1),
       ("== 52547)", "== 52607)", 1),
       ("＋v412 +99）'", "＋v412 +99＋v413 +60）'", 1)],
      "# v413 resync：index.html 淨 +60 行（52547→52607）；見 qa413/resync413.py。")

patch("tests/test_tang152_static.py",
      [("lines()[16744].startswith('function normaliseTangStub152(pack){')",
        f"lines()[{map_line(16745) - 1}].startswith('function normaliseTangStub152(pack){{')", 1),
       ("lines()[16869].strip().startswith('try{ normaliseTangStub152(rom2);')",
        f"lines()[{map_line(16870) - 1}].strip().startswith('try{{ normaliseTangStub152(rom2);')", 1)],
      "# v413 resync：index.html 淨 +60 行；normaliseTangStub152 兩釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa413/resync413.py。")

for _tang in ["tests/test_tang171_static.py", "tests/test_tang173_static.py"]:
    patch(_tang,
          [("總行數 52547（", "總行數 52607（", 1),
           ("== 52547)", "== 52607)", 1),
           ("＋v412 +99）'", "＋v412 +99＋v413 +60）'", 1),
           ("＋v412 +99，travel114 釘行）'", "＋v412 +99＋v413 +60，travel114 釘行）'", 1),
           ("'function openLoc(id, opts){' in lines[47330]", f"'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1)],
          "# v413 resync：index.html 淨 +60 行（52547→52607）；總行數＋openLoc DEF 釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa413/resync413.py。")

patch("tests/test_text125_static.py",
      [("if len(ls) < 12761 or FALLBACK not in ls[12760]:",
        f"if len(ls) < {map_line(12761)} or FALLBACK not in ls[{map_line(12761) - 1}]:", 1),
       ("if len(ls) < 12903 or FALLBACK not in ls[12902]:",
        f"if len(ls) < {map_line(12903)} or FALLBACK not in ls[{map_line(12903) - 1}]:", 1),
       ("if len(ls) < 18619 or 'if(typeof b.text === \"string\" && b.text){' not in ls[18618]:",
        f"if len(ls) < {map_line(18619)} or 'if(typeof b.text === \"string\" && b.text){{' not in ls[{map_line(18619) - 1}]:", 1)],
      "# v413 resync：index.html 淨 +60 行；3 個 fallback 釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa413/resync413.py。")

patch("tests/test_progress71_static.py",
      [("seg71 = src[i71:j71 + 7000]", "seg71 = src[i71:j71 + 7600]", 1)],
      "# v413 resync：renderProgressPane71 加分岔組呈現（P3），seg71 窗 7000→7600 先覆蓋全函數；見 qa413/resync413.py。")

patch("tests/test_progress71_logic.js",
      [("ok('B2：第 7 幕逐項——時窗未到（1991 年夏）', b2.indexOf('時窗：1991 年夏') >= 0);",
        "ok('B2：第 7 幕逐項——時間條件未到（1991 年夏）', b2.indexOf('時間條件未到：1991 年夏') >= 0);", 1)],
      "// v413 resync：進度時間條件措辭改「時間條件相符／未到」（P4 呈現修復，判定不變）；見 qa413/resync413.py。")

patch("tests/test_story198_logic.js",
      [("paneA.indexOf('時窗：1990 年冬') >= 0", "paneA.indexOf('時間條件未到：1990 年冬') >= 0", 1)],
      "// v413 resync：進度時間條件措辭改「時間條件相符／未到」（P4 呈現修復，判定不變）；見 qa413/resync413.py。")

print("RESYNC413 DONE")
