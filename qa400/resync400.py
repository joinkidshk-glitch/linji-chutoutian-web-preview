#!/usr/bin/env python3
"""v400 resync：index.html 淨 +186 行（51183→51369；細改 1–3）。

改動點（相對 v399 main 137036e，difflib hunk 摘要）：
  CSS：.nb-suggest400／.nb-cost400 ＋7 ＠舊 L2081 後／.t70-mprog ＋1 ＠舊 L5445 後。
  HTML：#nb-suggest400＋#nb-cost400 ＋3 ＠舊 L7333 後。
  JS：train71CourseMini 進度行 ＋3＋1／train71HandleClick 記 lastTrain＋成本行 ＋2＋2／
       defaultWeekPlan 重寫＋v400 helpers（lowestStatTrain400／weekStressPeak400／
       freeDays400／nbDayHint400／cost*／showCost400／renderSuggest400）淨 ＋~120／
       renderNotebook hint＋建議列＋通用改格 ＋1＋2＋2＋2／enterHome 清成本行 ＋2。
影響：
  (a) 行為改動（有意圖，唔係漂移）：defaultWeekPlan 唔再自動揀課／唔再因壓力靜靜換休息；
      舊斷言已喺 test_calib60_logic.js／test_calib60_static.py／test_p360_static.py／
      test_eval6_384_logic.js／test_eval7_386_logic.js 更新，見該檔 v400 註記。
  (b) 釘行全部按 difflib 映射重寫，內容逐字核實純漂移：
      travel114 FREE／COUNT／DEF 45973→46159／WRAPPER 32098→32284；
      rom159 6 釘＋全佳行 28254→28440；rom176 6 釘；tang152 兩釘；
      text125 三錨點；tang171／tang173 DEF 45973→46159；tang173 lines[5382]→[5389]（8 處）；
      gift185／tang171／tang173 總行數 51183→51369，行數鏈尾加 ＋v400 +186。
  (c) 總行數鏈：51183→51369（＋v400 +186）；openLoc DEF 鏈唔郁（ok 名係歷史標籤，
      只有 executable check 數字更新，同 v398／v399 做法一致）。
紀律：travel114 兩個 set 用單次掃描 dict 查表（唔好逐對 re.sub——v162 教訓：
重疊 pair 會食錨點）；其餘逐處 replace 全部 assert 恰好出現一次；
ok() 名入面嘅 L 號係歷史標籤，唔郁（總行數鏈同報錯字串行號例外，一併更新）。
用法：python3 qa400/resync400.py（喺 resync commit 之前跑一次；OLD 攞
v399 main 137036e，assert 總行數 51183，跑完再 commit 就唔會重跑——每檔開頭有
「v400 resync」註記就跳過）。
"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "137036e:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 51183, len(OLD) - 1  # v399 main 137036e
assert len(NEW) - 1 == 51369, len(NEW) - 1  # split 尾空行；count('\n') == 51369

NOTE = "# v400 resync：index.html 淨 +186 行（51183→51369）；見 qa400/resync400.py。"


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note):
    """subs：(old, new, expect_count)；逐處 replace，assert 出現次數。"""
    src = read(path)
    if src.split("\n")[0].startswith(("# v400 resync", "// v400 resync")):
        print(f"skip {path}（已註記）")
        return
    for old, new, n in subs:
        c = src.count(old)
        assert c == n, f"{path}: {old[:60]!r} count={c} expect={n}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, note)
    src = "\n".join(lines)
    write(path, src)
    print(f"patched {path}")


# ---------- difflib 映射：舊行 → 新行（內容逐字相同先算數） ----------
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


# ---------- travel114：FREE／COUNT 由檔內現有 set 動態建表，再逐行內容核實 ----------
def _current_set(src, name):
    m = re.search(name + r" = \{(.*?)\n\}", src, re.S)
    assert m, name
    # 只抽行首釘數字（同 _sub_set 口徑一致），唔好食註解入面嘅裸數字
    return [int(x) for x in re.findall(r"^\s*(\d+),", m.group(1), flags=re.M)]


_travel_src = read("tests/test_travel114_static.py")
FREE_MAP = {o: map_line(o) for o in _current_set(_travel_src, "FREE_LINES")}
COUNT_MAP = {o: map_line(o) for o in _current_set(_travel_src, "COUNT_LINES")}
print(f"travel114 FREE {len(FREE_MAP)} 處 COUNT {len(COUNT_MAP)} 處")
DEF_NEW = map_line(45973)
WRAP_NEW = map_line(32098)
assert DEF_NEW == 46159 and WRAP_NEW == 32284, (DEF_NEW, WRAP_NEW)


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.split("\n")[0].startswith("# v400 resync"):
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
    for old, new, n in [(f"DEF_LINE = 45973", f"DEF_LINE = {DEF_NEW}", 1),
                        (f"WRAPPER_LINE = 32098", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, "# v400 resync：index.html 淨 +186 行（51183→51369）；FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；openLoc( 呼叫點總數不變；見 qa400/resync400.py。")
    write(path, "\n".join(lines))
    print(f"patched {path}")


# ---------- (b) 釘行 ----------
patch("tests/test_rom159_static.py",
      [(f'line_has(28226, "v20a159 ROM159 Phase 1")',
        f'line_has({map_line(28226)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(9476, "rom159GainAllowed(k)")',
        f'line_has({map_line(9476)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(29134, "COMMIT48_NODES.CMT_lan_commit")',
        f'line_has({map_line(29134)}, "COMMIT48_NODES.CMT_lan_commit")', 1),
       (f'line_has(11656, "rom159PrepareNode(node)")',
        f'line_has({map_line(11656)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(16288, "rom159ApplyGiftOverrides()")',
        f'line_has({map_line(16288)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(28989, "function rom159SoMeetGate")',
        f'line_has({map_line(28989)}, "function rom159SoMeetGate")', 1),
       ('"查實" in idx_lines[28253]', f'"查實" in idx_lines[{map_line(28254) - 1}]', 1)],
      "# v400 resync：index.html 淨 +186 行；6 個 line_has 釘行＋全佳行按 difflib 映射重寫（28226→28412、9476→9487、29134→29320、11656→11667、16288→16299、28989→29175、全佳 28254→28440），內容逐字核實純漂移；見 qa400/resync400.py。")
patch("tests/test_rom176_static.py",
      [(f"line(7602).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'",
        f"line({map_line(7602)}).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'", 1),
       ("line(16286)", f"line({map_line(16286)})", 2),
       (f"line(43931).startswith('/* ===== v20a176 ROM176'",
        f"line({map_line(43931)}).startswith('/* ===== v20a176 ROM176'", 1),
       (f"line(44290).startswith('function rom176ApplyGiftOverrides()')",
        f"line({map_line(44290)}).startswith('function rom176ApplyGiftOverrides()')", 1),
       (f"line(45856).startswith('function addLocTalkGiftActs(add, L, npcId)')",
        f"line({map_line(45856)}).startswith('function addLocTalkGiftActs(add, L, npcId)')", 1),
       (f"'rom176TryIntercept(id)' in line(46014)",
        f"'rom176TryIntercept(id)' in line({map_line(46014)})", 1)],
      "# v400 resync：index.html 淨 +186 行；6 個 line() 釘行按 difflib 映射重寫（7602→7613、16286→16297、43931→44117、44290→44476、45856→46042、46014→46200），內容逐字核實純漂移；見 qa400/resync400.py。")
patch("tests/test_tang152_static.py",
      [("lines()[16215].startswith('function normaliseTangStub152(pack){')",
        f"lines()[{map_line(16216) - 1}].startswith('function normaliseTangStub152(pack){{')", 1),
       ("lines()[16340].strip().startswith('try{ normaliseTangStub152(rom2);')",
        f"lines()[{map_line(16341) - 1}].strip().startswith('try{{ normaliseTangStub152(rom2);')", 1)],
      "# v400 resync：index.html 淨 +186 行；normaliseTangStub152 兩釘按 difflib 映射重寫（lines()[16215]→[16226]、[16340]→[16351]），內容逐字核實純漂移；見 qa400/resync400.py。")
patch("tests/test_text125_static.py",
      [("if len(ls) < 12236 or FALLBACK not in ls[12235]:",
        f"if len(ls) < {map_line(12236)} or FALLBACK not in ls[{map_line(12236) - 1}]:", 1),
       ('probs.append("currentLine 第 12236 行冇 text fallback")',
        f'probs.append("currentLine 第 {map_line(12236)} 行冇 text fallback")', 1),
       ("v399 resync：12212→12236（difflib 對位核實純漂移，見 qa399/resync399.py）",
        "v399 resync：12212→12236（difflib 對位核實純漂移，見 qa399/resync399.py）；v400 resync：12236→12247（difflib 對位核實純漂移，見 qa400/resync400.py）", 1),
       ("if len(ls) < 12378 or FALLBACK not in ls[12377]:",
        f"if len(ls) < {map_line(12378)} or FALLBACK not in ls[{map_line(12378) - 1}]:", 1),
       ('probs.append("advance 第 12378 行冇 text fallback")',
        f'probs.append("advance 第 {map_line(12378)} 行冇 text fallback")', 1),
       ("v399 resync：12354→12378（difflib 對位核實純漂移，見 qa399/resync399.py）",
        "v399 resync：12354→12378（difflib 對位核實純漂移，見 qa399/resync399.py）；v400 resync：12378→12389（difflib 對位核實純漂移，見 qa400/resync400.py）", 1),
       ("if len(ls) < 17991 or 'if(typeof b.text === \"string\" && b.text){' not in ls[17990]:",
        f"if len(ls) < {map_line(17991)} or 'if(typeof b.text === \"string\" && b.text){{' not in ls[{map_line(17991) - 1}]:", 1),
       ('probs.append("applyFamilySafeToNode 第 17991 行冇 b.text 分支")',
        f'probs.append("applyFamilySafeToNode 第 {map_line(17991)} 行冇 b.text 分支")', 1),
       ("v399 resync：17967→17991（difflib 對位核實純漂移，見 qa399/resync399.py）",
        "v399 resync：17967→17991（difflib 對位核實純漂移，見 qa399/resync399.py）；v400 resync：17991→18012（difflib 對位核實純漂移，見 qa400/resync400.py）", 1)],
      "# v400 resync：index.html 淨 +186 行；三錨點按 difflib 映射重寫（12236→12247、12378→12389、17991→18012），內容逐字核實純漂移；見 qa400/resync400.py。")

# ---------- (b) 釘行＋總行數鏈 ----------
patch("tests/test_gift185_static.py",
      [("總行數 51183（", "總行數 51369（", 1),
       ("== 51183)", "== 51369)", 1),
       ("＋v398 +132＋v399 +72）'", "＋v398 +132＋v399 +72＋v400 +186）'", 1)],
      "# v400 resync：index.html 淨 +186 行（51183→51369）；見 qa400/resync400.py。")
patch("tests/test_tang171_static.py",
      [("總行數 51183（", "總行數 51369（", 1),
       ("== 51183)", "== 51369)", 1),
       ("＋v398 +132＋v399 +72）'", "＋v398 +132＋v399 +72＋v400 +186）'", 1),
       ("len(lines) >= 45973 and 'function openLoc(id, opts){' in lines[45972]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1)],
      "# v400 resync：index.html 淨 +186 行（51183→51369）；openLoc DEF 45973→46159；見 qa400/resync400.py。")
patch("tests/test_tang173_static.py",
      [("總行數 51183（", "總行數 51369（", 1),
       ("== 51183)", "== 51369)", 1),
       ("＋v398 +132＋v399 +72）'", "＋v398 +132＋v399 +72＋v400 +186）'", 1),
       ("len(lines) >= 45973 and 'function openLoc(id, opts){' in lines[45972]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1),
       ("lines[5382]", f"lines[{map_line(5383) - 1}]", 8)],
      "# v400 resync：index.html 淨 +186 行（51183→51369）；openLoc DEF 45973→46159；L4872 釘 lines[5382]→[5389]（8 處）；見 qa400/resync400.py。")

resync_travel114()
print("v400 resync done")
