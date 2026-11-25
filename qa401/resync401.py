#!/usr/bin/env python3
"""v401 resync：index.html 淨 +192 行（51369→51561；UI401 頭五項）。

改動點（相對 v400 main dcae7a1，difflib hunk 摘要）：
  CSS：v401 集中區塊 ＋~150 ＠舊 L7078（</style>）前——scene-paper401 紙卡、
       教學遮罩挖空／窄紙條、35c 小檔案旁註＋小標、通告欄索引紙／合約紙／手寫備註／捲底留白。
  CSS：共用金掣 button.p 規則 ＋4 ＠舊 L993（實色金＋清陰影／浮雕）。
  JS：modal()／closeModal() scenePaper401 opt ＋5；refreshTutSpotlight398 遮罩挖空 ＋~20；
       renderPostShootRewardHtml／renderAwardResultHtml dual 組裝各 ＋6；
       metricHead401／metricSub401 ＋5；P2 小標行 ＋1；詳情合約紙包裝 ＋2；
       其餘呼叫點（電話／醫院／B01／病假路徑）係同行註解／opt，行數唔變。
影響：
  (a) 行為改動（有意圖，唔係漂移）：35c dual 行缺值省略（雙值輸出逐字不變，見
      tests/test_v401_logic.js）；35c P2 主標「陳偉翔散場」＋奪獎行降小標（只限
      入圍＋他人奪獎嗰案；玩家奪獎／旁聽沿用舊主標）；金掣實色金；教學遮罩挖空。
      舊斷言受影響嘅已核實：test_awards186_logic.js:88／
      test_newspaper214_award_logic.js:153 嘅 b7（雙值逐字）照舊通過——
      test_v401_logic.js a／d3 覆蓋同一輸出；test_newspaper214_award_logic c1–c3
      （winLine 字串在位）照舊通過——小標保留字串。v401 新測試另立兩檔。
      四個舊逐字釘因有意圖改動而更新（意圖保留，見各檔 v401 註記）：
      test_v391_ui_static.py（金漸變→實色金，改釘 background:#C9A227）；
      test_v397_static.py（setUnderlyingInert 加 scene401 或項）；
      test_v398_static.py（scene398 toggle 加 scene401 或項）；
      test_v399_static.py（43b 加 scenePaper401 opt；refresh !on 分支加清挖空）。
  (b) 釘行全部按 difflib 映射重寫，內容逐字核實純漂移：
      travel114 FREE／COUNT／DEF 46159→?／WRAPPER 32284→?；
      rom159 6 釘＋全佳行 28440→?；rom176 6 釘；tang152 兩釘；
      text125 三錨點；tang171／tang173 DEF 46159→?；tang173 lines[5389]→?（8 處）；
      gift185／tang171／tang173 總行數 51369→51561，行數鏈尾加 ＋v401 +192。
  (c) 總行數鏈：51369→51561（＋v401 +192）；openLoc DEF 鏈唔郁（ok 名係歷史標籤，
      只有 executable check 數字更新，同 v398／v399／v400 做法一致）。
紀律：travel114 兩個 set 用單次掃描 dict 查表（唔好逐對 re.sub——v162 教訓：
重疊 pair 會食錨點）；其餘逐處 replace 全部 assert 恰好出現一次；
ok() 名入面嘅 L 號係歷史標籤，唔郁（總行數鏈同報錯字串行號例外，一併更新）。
用法：python3 qa401/resync401.py（喺 resync commit 之前跑一次；OLD 攞
v400 main dcae7a1，assert 總行數 51369，跑完再 commit 就唔會重跑——每檔開頭有
「v401 resync」註記就跳過）。
"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "dcae7a1:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 51369, len(OLD) - 1  # v400 main dcae7a1
assert len(NEW) - 1 == 51561, len(NEW) - 1  # split 尾空行；count('\n') == 51561

NOTE = "# v401 resync：index.html 淨 +192 行（51369→51561）；見 qa401/resync401.py。"


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note):
    """subs：(old, new, expect_count)；逐處 replace，assert 出現次數。"""
    src = read(path)
    if src.split("\n")[0].startswith(("# v401 resync", "// v401 resync")):
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
DEF_NEW = map_line(46159)
WRAP_NEW = map_line(32284)
print(f"travel114 DEF 46159->{DEF_NEW} WRAPPER 32284->{WRAP_NEW}")


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.split("\n")[0].startswith("# v401 resync"):
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
    for old, new, n in [(f"DEF_LINE = 46159", f"DEF_LINE = {DEF_NEW}", 1),
                        (f"WRAPPER_LINE = 32284", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, "# v401 resync：index.html 淨 +192 行（51369→51561）；FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；openLoc( 呼叫點總數不變；見 qa401/resync401.py。")
    write(path, "\n".join(lines))
    print(f"patched {path}")


# ---------- (b) 釘行 ----------
patch("tests/test_rom159_static.py",
      [(f'line_has(28412, "v20a159 ROM159 Phase 1")',
        f'line_has({map_line(28412)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(9487, "rom159GainAllowed(k)")',
        f'line_has({map_line(9487)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(29320, "COMMIT48_NODES.CMT_lan_commit")',
        f'line_has({map_line(29320)}, "COMMIT48_NODES.CMT_lan_commit")', 1),
       (f'line_has(11667, "rom159PrepareNode(node)")',
        f'line_has({map_line(11667)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(16299, "rom159ApplyGiftOverrides()")',
        f'line_has({map_line(16299)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(29175, "function rom159SoMeetGate")',
        f'line_has({map_line(29175)}, "function rom159SoMeetGate")', 1),
       ('"查實" in idx_lines[28439]', f'"查實" in idx_lines[{map_line(28440) - 1}]', 1)],
      "# v401 resync：index.html 淨 +192 行；6 個 line_has 釘行＋全佳行按 difflib 映射重寫，內容逐字核實純漂移；見 qa401/resync401.py。")
patch("tests/test_rom176_static.py",
      [(f"line(7613).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'",
        f"line({map_line(7613)}).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'", 1),
       ("line(16297)", f"line({map_line(16297)})", 2),
       (f"line(44117).startswith('/* ===== v20a176 ROM176'",
        f"line({map_line(44117)}).startswith('/* ===== v20a176 ROM176'", 1),
       (f"line(44476).startswith('function rom176ApplyGiftOverrides()')",
        f"line({map_line(44476)}).startswith('function rom176ApplyGiftOverrides()')", 1),
       (f"line(46042).startswith('function addLocTalkGiftActs(add, L, npcId)')",
        f"line({map_line(46042)}).startswith('function addLocTalkGiftActs(add, L, npcId)')", 1),
       (f"'rom176TryIntercept(id)' in line(46200)",
        f"'rom176TryIntercept(id)' in line({map_line(46200)})", 1)],
      "# v401 resync：index.html 淨 +192 行；6 個 line() 釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa401/resync401.py。")
patch("tests/test_tang152_static.py",
      [("lines()[16226].startswith('function normaliseTangStub152(pack){')",
        f"lines()[{map_line(16227) - 1}].startswith('function normaliseTangStub152(pack){{')", 1),
       ("lines()[16351].strip().startswith('try{ normaliseTangStub152(rom2);')",
        f"lines()[{map_line(16352) - 1}].strip().startswith('try{{ normaliseTangStub152(rom2);')", 1)],
      "# v401 resync：index.html 淨 +192 行；normaliseTangStub152 兩釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa401/resync401.py。")
patch("tests/test_text125_static.py",
      [("if len(ls) < 12247 or FALLBACK not in ls[12246]:",
        f"if len(ls) < {map_line(12247)} or FALLBACK not in ls[{map_line(12247) - 1}]:", 1),
       ('probs.append("currentLine 第 12247 行冇 text fallback")',
        f'probs.append("currentLine 第 {map_line(12247)} 行冇 text fallback")', 1),
       ("v400 resync：12236→12247（difflib 對位核實純漂移，見 qa400/resync400.py）",
        f"v400 resync：12236→12247（difflib 對位核實純漂移，見 qa400/resync400.py）；v401 resync：12247→{map_line(12247)}（difflib 對位核實純漂移，見 qa401/resync401.py）", 1),
       ("if len(ls) < 12389 or FALLBACK not in ls[12388]:",
        f"if len(ls) < {map_line(12389)} or FALLBACK not in ls[{map_line(12389) - 1}]:", 1),
       ('probs.append("advance 第 12389 行冇 text fallback")',
        f'probs.append("advance 第 {map_line(12389)} 行冇 text fallback")', 1),
       ("v400 resync：12378→12389（difflib 對位核實純漂移，見 qa400/resync400.py）",
        f"v400 resync：12378→12389（difflib 對位核實純漂移，見 qa400/resync400.py）；v401 resync：12389→{map_line(12389)}（difflib 對位核實純漂移，見 qa401/resync401.py）", 1),
       ("if len(ls) < 18012 or 'if(typeof b.text === \"string\" && b.text){' not in ls[18011]:",
        f"if len(ls) < {map_line(18012)} or 'if(typeof b.text === \"string\" && b.text){{' not in ls[{map_line(18012) - 1}]:", 1),
       ('probs.append("applyFamilySafeToNode 第 18012 行冇 b.text 分支")',
        f'probs.append("applyFamilySafeToNode 第 {map_line(18012)} 行冇 b.text 分支")', 1),
       ("v400 resync：17991→18012（difflib 對位核實純漂移，見 qa400/resync400.py）",
        f"v400 resync：17991→18012（difflib 對位核實純漂移，見 qa400/resync400.py）；v401 resync：18012→{map_line(18012)}（difflib 對位核實純漂移，見 qa401/resync401.py）", 1)],
      "# v401 resync：index.html 淨 +192 行；三錨點按 difflib 映射重寫，內容逐字核實純漂移；見 qa401/resync401.py。")

# ---------- (b) 釘行＋總行數鏈 ----------
patch("tests/test_gift185_static.py",
      [("總行數 51369（", "總行數 51561（", 1),
       ("== 51369)", "== 51561)", 1),
       ("＋v399 +72＋v400 +186）'", "＋v399 +72＋v400 +186＋v401 +192）'", 1)],
      "# v401 resync：index.html 淨 +192 行（51369→51561）；見 qa401/resync401.py。")
patch("tests/test_tang171_static.py",
      [("總行數 51369（", "總行數 51561（", 1),
       ("== 51369)", "== 51561)", 1),
       ("＋v399 +72＋v400 +186）'", "＋v399 +72＋v400 +186＋v401 +192）'", 1),
       ("len(lines) >= 46159 and 'function openLoc(id, opts){' in lines[46158]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1)],
      "# v401 resync：index.html 淨 +192 行（51369→51561）；openLoc DEF 46159→" + str(DEF_NEW) + "；見 qa401/resync401.py。")
patch("tests/test_tang173_static.py",
      [("總行數 51369（", "總行數 51561（", 1),
       ("== 51369)", "== 51561)", 1),
       ("＋v399 +72＋v400 +186）'", "＋v399 +72＋v400 +186＋v401 +192）'", 1),
       ("len(lines) >= 46159 and 'function openLoc(id, opts){' in lines[46158]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1),
       ("lines[5389]", f"lines[{map_line(5390) - 1}]", 8)],
      "# v401 resync：index.html 淨 +192 行（51369→51561）；openLoc DEF 46159→" + str(DEF_NEW) + "；L4872 釘 lines[5389]→[" + str(map_line(5390) - 1) + "]（8 處）；見 qa401/resync401.py。")

resync_travel114()
print("v401 resync done")
