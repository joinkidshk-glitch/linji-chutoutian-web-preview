#!/usr/bin/env python3
"""v396 resync：index.html 淨 +129 行（50512→50641；改動散喺全檔，唔係淨加檔尾）。

改動點（相對 v395 main 9eaadfd）：
  CSS：act-sel396 ＋8＠~1477／日結漸變 !important＋註解 ＋5＠~2229／
       ui-hide-under396 ＋16＠~3238／awd-result396 ＋9＠~5044
  JS：日結日期 helper ＋20＠~17427／通告欄 exp＋pill ＋~30＠~19680／
       setUnderlyingInert ＋~15＠~21716／afterDayModal＋afterDayRes 日期行 ＋~6／
       頒獎 factbox 搬版 ＋~10＠~34107／40 號卡 day-res ＋~4＠~47302／
       禮品店單一購買 ＋~57＠~48919／買衫店單一購買 ＋~57＠~7651
影響：
  (a) 8 份 logic 測試抽出嘅函數（afterDayModal／afterDayRes／resolvePlannedDay／
      presentStartScheduleConfirm45／presentRestSleepDayEnd）而家 call
      dayResDateLine396——一併抽三個 helper（settledDateObj396／fmtShortDate396／
      dayResDateLine396）入沙盒，否則 ReferenceError。
  (b) 釘行全部按 difflib 映射重寫，內容逐字核實純漂移（4 處重複行：
      衣櫃／禮品店關閉＋dismiss 各兩行，內容相同，用函數範圍上下文定位）：
      travel114 FREE 42 處＋COUNT 13 處＋DEF 45489→45592＋WRAPPER 31679→31780；
      rom159 27807→27908／9289→9338／28715→28816；
      rom176 7428→7464／16099→16148／43484→43587；
      tang152 [16028]→[16077]／[16153]→[16202]（0-indexed）；
      tang173 L4872 lines[5233]→lines[5269]；
      text125 12049→12098／12191→12240／17766→17841。
  (c) 總行數鏈：50512→50641（＋v396 +129）；openLoc DEF 鏈 ＋v396 +103
      （DEF 行本身漂 +103，檔尾 ＋26 喺佢之後）。
紀律：travel114 兩個 set 用單次掃描 dict 查表（唔好逐對 re.sub——v162 教訓：
重疊 pair 會食錨點）；其餘逐處 replace 全部 assert 恰好出現一次；
ok() 名入面嘅 L 號係歷史標籤，唔郁（總行數鏈同報錯字串行號例外，一併更新）。
用法：python3 qa396/resync396.py（已跑過，冪等檢查：每處錨點必須恰好出現一次；
      註記行已存在就跳過該檔）。
"""
import difflib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(NEW) - 1 == 50641, len(NEW) - 1  # split 尾空行；count('\n') == 50641

NOTE = "# v396 resync：index.html 淨 +129 行（50512→50641）；見 qa396/resync396.py。"
NOTE_LOGIC = ("// v396 resync：afterDayRes／afterDayModal／休息卡靠 dayResDateLine396 等三 helper "
              "出日結日期行，沙盒一併抽入；見 qa396/resync396.py。")


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note, force=False):
    """subs：(old, new, expect_count)；逐處 replace，assert 出現次數。
    force=True 時唔理已註記（跟進補釘用）。"""
    src = read(path)
    if not force and "v396 resync" in src.split("\n")[0]:
        print(f"skip {path}（已註記）")
        return
    for old, new, n in subs:
        c = src.count(old)
        assert c == n, f"{path}: {old[:60]!r} count={c} expect={n}"
        src = src.replace(old, new)
    if not force:
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


# travel114：FREE 42＋COUNT 13——difflib 映射＋逐行內容核實。
# 4 處重複行（衣櫃／禮品店關閉＋dismiss）difflib 對唔到唯一位置，用函數範圍上下文定位。
FREE_CTX = {7638: 7695, 7639: 7696, 48826: 48964, 48827: 48965}
FREE_MAP = {}
COUNT_MAP = {}
_t = read("tests/test_travel114_static.py")


def _set(name):
    m = re.search(name + r" = \{(.*?)\n\}", _t, re.S)
    return sorted(int(x) for x in re.findall(r"^\s*(\d+),", m.group(1), re.M))


for _ln in _set("FREE_LINES"):
    _n = FREE_CTX[_ln] if _ln in FREE_CTX else map_line(_ln)
    assert OLD[_ln - 1] == NEW[_n - 1], f"FREE {_ln} content changed"
    FREE_MAP[_ln] = _n
for _ln in _set("COUNT_LINES"):
    _n = map_line(_ln)
    assert OLD[_ln - 1] == NEW[_n - 1], f"COUNT {_ln} content changed"
    COUNT_MAP[_ln] = _n
assert len(FREE_MAP) == 42 and len(COUNT_MAP) == 13
DEF_NEW = map_line(45489)   # 45592
WRAP_NEW = map_line(31679)  # 31780
assert DEF_NEW == 45592 and WRAP_NEW == 31780


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.startswith(NOTE):
        print(f"skip {path}（已註記）")
        return
    # 兩個 set：單次掃描 dict 查表，只喺 set 字面範圍內換數。
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
    for old, new, n in [(f"DEF_LINE = 45489", f"DEF_LINE = {DEF_NEW}", 1),
                        (f"WRAPPER_LINE = 31679", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, NOTE)
    write(path, "\n".join(lines))
    print(f"patched {path}")


# ---------- (a) logic 測試：沙盒一併抽三個 helper ----------
_FNS_TAIL = ("'esc202','nextDayLabel202','dayEndNextLine202','storyResultDestLine202']; "
             "/* v392：dayEndDismissNote202 已刪（dismiss 提示機制隨 v392 ① 廢止） */")
_FNS_TAIL_NEW = ("'esc202','nextDayLabel202','dayEndNextLine202','storyResultDestLine202',"
                 "'settledDateObj396','fmtShortDate396','dayResDateLine396']; "
                 "/* v396：afterDayRes／afterDayModal／休息卡靠呢三個 helper 出日結日期行 */ "
                 "/* v392：dayEndDismissNote202 已刪（dismiss 提示機制隨 v392 ① 廢止） */")
for _p in ["tests/test_aud91_logic.js", "tests/test_levels75_logic.js",
           "tests/test_rest58_logic.js", "tests/test_stamina58_logic.js"]:
    patch(_p, [(_FNS_TAIL, _FNS_TAIL_NEW, 1)], NOTE_LOGIC)
patch("tests/test_verify37_logic.js",
      [("'aud91PresentDue','aud91PresentOne'];",
        "'aud91PresentDue','aud91PresentOne','settledDateObj396','fmtShortDate396',"
        "'dayResDateLine396']; /* v396：resolvePlannedDay→afterDayRes 靠呢三個 helper 出日結日期行 */", 1)],
      NOTE_LOGIC)
_EVAL3 = ("eval(extractFn('settledDateObj396'));\n"
          "eval(extractFn('fmtShortDate396'));\n"
          "eval(extractFn('dayResDateLine396'));")
for _p in ["tests/test_dayend202_logic.js", "tests/test_dayflow196_logic.js",
           "tests/test_flow45_logic.js"]:
    patch(_p, [("eval(extractFn('presentRestSleepDayEnd'));",
                "eval(extractFn('presentRestSleepDayEnd'));\n/* v396：afterDayModal／afterDayRes／休息卡靠呢三個 helper 出日結日期行 */\n" + _EVAL3, 1)],
          NOTE_LOGIC)

# ---------- (b) 釘行 ----------
patch("tests/test_rom159_static.py",
      [(f'line_has(27807, "v20a159 ROM159 Phase 1")',
        f'line_has({map_line(27807)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(9289, "rom159GainAllowed(k)")',
        f'line_has({map_line(9289)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(28715, "COMMIT48_NODES.CMT_lan_commit")',
        f'line_has({map_line(28715)}, "COMMIT48_NODES.CMT_lan_commit")', 1)],
      "# v396 resync：index.html 淨 +129 行；3 個 line_has 釘行按 difflib 映射重寫（27807→27908、9289→9338、28715→28816），內容逐字核實純漂移；見 qa396/resync396.py。")
# 跟進：同一檔其餘 3 個 line_has＋全佳行（首輪 head 截斷未見）
patch("tests/test_rom159_static.py",
      [(f'line_has(11469, "rom159PrepareNode(node)")',
        f'line_has({map_line(11469)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(16101, "rom159ApplyGiftOverrides()")',
        f'line_has({map_line(16101)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(28570, "function rom159SoMeetGate")',
        f'line_has({map_line(28570)}, "function rom159SoMeetGate")', 1),
       ('"查實" in idx_lines[27835 - 1]', f'"查實" in idx_lines[{map_line(27835) - 1}]', 1)],
      "# v396 resync（跟進）：其餘釘行 11469→11518、16101→16150、28570→28671、全佳 27835→27936。", force=True)
patch("tests/test_rom176_static.py",
      [(f'line(7428).startswith(\'  lan:{{ id:"lan", name:"藍若曦"',
        f'line({map_line(7428)}).startswith(\'  lan:{{ id:"lan", name:"藍若曦"', 1),
       (f"'GIFT_REACT = giftReact' in line(16099) and 'rom176ApplyGiftOverrides()' in line(16099)",
        f"'GIFT_REACT = giftReact' in line({map_line(16099)}) and 'rom176ApplyGiftOverrides()' in line({map_line(16099)})", 1),
       (f"line(43484).startswith('/* ===== v20a176 ROM176')",
        f"line({map_line(43484)}).startswith('/* ===== v20a176 ROM176')", 1)],
      "# v396 resync：index.html 淨 +129 行；3 個釘行按 difflib 映射重寫（7428→7464、16099→16148、43484→43587），內容逐字核實純漂移；見 qa396/resync396.py。")
# 跟進：同一檔其餘 3 個釘（首輪 head 截斷未見）
patch("tests/test_rom176_static.py",
      [(f"line(43843).startswith('function rom176ApplyGiftOverrides()')",
        f"line({map_line(43843)}).startswith('function rom176ApplyGiftOverrides()')", 1),
       (f"line(45409).startswith('function addLocTalkGiftActs(add, L, npcId)')",
        f"line({map_line(45409)}).startswith('function addLocTalkGiftActs(add, L, npcId)')", 1),
       (f"'rom176TryIntercept(id)' in line(45530)",
        f"'rom176TryIntercept(id)' in line({map_line(45530)})", 1)],
      "# v396 resync（跟進）：其餘釘行 43843→43946、45409→45512、45530→45633。", force=True)
patch("tests/test_tang152_static.py",
      [("lines()[16028].startswith('function normaliseTangStub152(pack){')",
        f"lines()[{map_line(16029) - 1}].startswith('function normaliseTangStub152(pack){{')", 1),
       ("lines()[16153].strip().startswith('try{ normaliseTangStub152(rom2);')",
        f"lines()[{map_line(16154) - 1}].strip().startswith('try{{ normaliseTangStub152(rom2);')", 1)],
      "# v396 resync：index.html 淨 +129 行；normaliseTangStub152 兩釘按 difflib 映射重寫（lines()[16028]→[16077]、[16153]→[16202]），內容逐字核實純漂移；見 qa396/resync396.py。")
patch("tests/test_text125_static.py",
      [("if len(ls) < 12049 or FALLBACK not in ls[12048]:",
        f"if len(ls) < {map_line(12049)} or FALLBACK not in ls[{map_line(12049) - 1}]:", 1),
       ("currentLine 第 12049 行冇 text fallback",
        f"currentLine 第 {map_line(12049)} 行冇 text fallback", 1),
       ("if len(ls) < 12191 or FALLBACK not in ls[12190]:",
        f"if len(ls) < {map_line(12191)} or FALLBACK not in ls[{map_line(12191) - 1}]:", 1),
       ("advance 第 12191 行冇 text fallback",
        f"advance 第 {map_line(12191)} 行冇 text fallback", 1),
       ("if len(ls) < 17766 or 'if(typeof b.text === \"string\" && b.text){' not in ls[17765]:",
        f"if len(ls) < {map_line(17766)} or 'if(typeof b.text === \"string\" && b.text){{' not in ls[{map_line(17766) - 1}]:", 1),
       ("applyFamilySafeToNode 第 17766 行冇 b.text 分支",
        f"applyFamilySafeToNode 第 {map_line(17766)} 行冇 b.text 分支", 1)],
      "# v396 resync：index.html 淨 +129 行；三錨點按 difflib 映射重寫（currentLine 12049→12098、advance 12191→12240、applyFamilySafe 17766→17841），內容逐字核實純漂移；報錯字串行號一併更新；見 qa396/resync396.py。")

# ---------- (c) 總行數鏈＋openLoc DEF 鏈 ----------
_TOTAL = [("總行數 50512（", "總行數 50641（", 1),
          ("＋v395 +1）", "＋v395 +1＋v396 +129）", 1),
          ("== 50512)", "== 50641)", 1)]
patch("tests/test_gift185_static.py", _TOTAL, NOTE)
patch("tests/test_tang171_static.py",
      _TOTAL + [("len(lines) >= 45489 and 'function openLoc(id, opts){' in lines[45488]",
                f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1),
               ("＋v394 +5，travel114 釘行）", "＋v394 +5＋v396 +103，travel114 釘行）", 1)],
      NOTE)
patch("tests/test_tang173_static.py",
      [("src.count('\\n') == 50512)", "src.count('\\n') == 50641)", 1),
       ("＋v395 +1）", "＋v395 +1＋v396 +129）", 1),
       ("len(lines) >= 45489 and 'function openLoc(id, opts){' in lines[45488]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1),
       ("＋v394 +5，travel114 釘行）", "＋v394 +5＋v396 +103，travel114 釘行）", 1),
       ("lines[5233]", f"lines[{map_line(5234) - 1}]", 8)],
      NOTE)
resync_travel114()
print("done")
