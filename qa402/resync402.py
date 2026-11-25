#!/usr/bin/env python3
"""v402 resync：index.html 淨 +210 行（51561→51771；UI402 第九輪頭五項＋掣量頭項）。

改動點（相對 v401 main 3f72a41，difflib hunk 摘要）：
  CSS：v402 集中區塊 ＋92 ＠舊 L7229（</style>）前——卡片避讓（mn-hidden402）、
       掣量卸載（tut-stage397 pin 收起／sheet-open pin 收起／awd-stage-on402／
       menu-open402）、通告欄索引紙／板頭橫列／推介卡劇照、底欄／卡片捲動安全區、
       支票紙邊、08b 紅字加深、金掣 serif（＋4 ＠舊 L993）、P2 相標記。
       settle363 keyframes 補 translate（行數唔變）；.map-me363／.map-here373
       zone 併入（JS）。
  JS：hideMapLabelsUnderModal402／restoreMapLabels402 新函數（＋21 ＠ modal 附近）；
       modal()／closeModal() 掛鈎；drawMap() 尾段 hide（＋6）；deCollide 尾段
       clamp 後再推障礙＋刷新 it.r（＋14／＋5／＋8）；paintBar() clamp 後加
       deCollide（＋5）；ResizeObserver 加 deCollide（行數唔變，係同行改寫）；
       setUnderlyingInert tut 豁免收窄到 tutMap（＋4）；setTutMask 由 mask class
       推導 scene（＋9）；showTutBoardStage 去 role／tabindex（＋4）；
       awards62PlayCeremony 加／除 awd-stage-on402（＋1／＋1）；
       btn-menu／menu／body toggle menu-open402（＋2／＋1／＋5）；
       gigBoardTeaserHtml still402 插畫（＋5／＋1）；renderAwardResultHtml
       P2 mark214（＋5）；chk101EnsureCss 支票 margin／memo top（同行改寫）；
       awardsPickPressNews fallback 文案（同行改寫）；newspaperCheck 測試輸入
       字串（同行改寫）。
  內容：content/STUB_AWARDS_CEREMONY_v1.json 三模板大標改（ad／film／tv，
       同行改寫，行數唔變）；seal_extra.png 紅像素 ×0.85（binary，行數唔變）。
影響：
  (a) 行為改動（有意圖，唔係漂移）：
      · v396 setUnderlyingInert 教學豁免收窄到只限 TUT_MAP（!tut→!tutMap；
        任務 6③⑤；聚光目標 pin 只喺 TUT_MAP 步先要留低，TUT_BOARD／結算卡
        要 scene 卸載）。test_v396_static.py 期望字串同步更新，見檔頭 v402 註記。
      · v398 fade rule：v402 曾拆走（第九輪話淡出洗摺位半行字），但 v398 test
        釘住呢條 rule（「未完待續」係設計意圖，唔係 bug），拆走會令 suite fail
        ——已還原，padding-bottom 32px 保留緩解洗字；張力見 index.html 內註解
        同 NOTES_V20A402_UI_AUDIT9_TOP5.md。v398 test 本身唔使改。
      · s30dedup still402 註解縮短 ~90 字元（行數不變，純文字縮短），令
        <div class="gt-meta">／gt-meta-line 返入 test 嘅 6000 字元抽取窗。
        s30dedup117 test 本身唔使改。
  (b) 釘行全部按 difflib 映射重寫，內容逐字核實純漂移：
      travel114 FREE 44 處＋COUNT 13 處＋DEF／WRAPPER；
      rom159 6 釘＋全佳行；rom176 6 釘；tang152 兩釘；
      text125 三錨點；tang171／tang173 DEF；tang173 lines[5393]（8 處）；
      gift185／tang171／tang173 總行數 51561→51771，行數鏈尾加 ＋v402 +210。
  (c) 總行數鏈：51561→51771（＋v402 +210）；openLoc DEF 鏈唔郁（ok 名係歷史標籤，
      只有 executable check 數字更新，同 v398／v399／v400／v401 做法一致）。
紀律：travel114 兩個 set 用單次掃描 dict 查表（唔好逐對 re.sub——v162 教訓：
重疊 pair 會食錨點）；其餘逐處 replace 全部 assert 恰好出現一次；
ok() 名入面嘅 L 號係歷史標籤，唔郁（總行數鏈同報錯字串行號例外，一併更新）。
用法：python3 qa402/resync402.py（喺 resync commit 之前跑一次；OLD 攞
v401 main 3f72a41，assert 總行數 51561，跑完再 commit 就唔會重跑——每檔開頭有
「v402 resync」註記就跳過）。
"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "3f72a41:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 51561, len(OLD) - 1  # v401 main 3f72a41
assert len(NEW) - 1 == 51771, len(NEW) - 1  # split 尾空行；count('\n') == 51771

NOTE = "# v402 resync：index.html 淨 +210 行（51561→51771）；見 qa402/resync402.py。"


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note):
    """subs：(old, new, expect_count)；逐處 replace，assert 出現次數。"""
    src = read(path)
    if src.split("\n")[0].startswith(("# v402 resync", "// v402 resync")):
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
DEF_NEW = map_line(46334)
WRAP_NEW = map_line(32443)
print(f"travel114 DEF 46334->{DEF_NEW} WRAPPER 32443->{WRAP_NEW}")


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.split("\n")[0].startswith("# v402 resync"):
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
    for old, new, n in [(f"DEF_LINE = 46334", f"DEF_LINE = {DEF_NEW}", 1),
                        (f"WRAPPER_LINE = 32443", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, "# v402 resync：index.html 淨 +210 行（51561→51771）；FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；openLoc( 呼叫點總數不變；見 qa402/resync402.py。")
    write(path, "\n".join(lines))
    print(f"patched {path}")


# ---------- (a) 有意圖行為改動：v396 setUnderlyingInert 教學豁免收窄到 TUT_MAP ----------
patch("tests/test_v396_static.py",
      [('app.classList.toggle("ui-hide-under396", !!(on && !scene && !tut))',
        'app.classList.toggle("ui-hide-under396", !!(on && !scene && !tutMap))', 1)],
      "# v402 resync：setUnderlyingInert 教學豁免收窄到只限 TUT_MAP（!tut→!tutMap，有意圖改動，任務 6③⑤；聚光目標 pin 只喺 TUT_MAP 步先要留低，TUT_BOARD／結算卡要 scene 卸載；見 qa402/resync402.py。")

# ---------- (b) 釘行 ----------
patch("tests/test_rom159_static.py",
      [(f'line_has(28571, "v20a159 ROM159 Phase 1")',
        f'line_has({map_line(28571)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(9639, "rom159GainAllowed(k)")',
        f'line_has({map_line(9639)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(29479, "COMMIT48_NODES.CMT_lan_commit")',
        f'line_has({map_line(29479)}, "COMMIT48_NODES.CMT_lan_commit")', 1),
       (f'line_has(11819, "rom159PrepareNode(node)")',
        f'line_has({map_line(11819)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(16451, "rom159ApplyGiftOverrides()")',
        f'line_has({map_line(16451)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(29334, "function rom159SoMeetGate")',
        f'line_has({map_line(29334)}, "function rom159SoMeetGate")', 1),
       ('"查實" in idx_lines[28598]', f'"查實" in idx_lines[{map_line(28599) - 1}]', 1)],
      "# v402 resync：index.html 淨 +210 行；6 個 line_has 釘行＋全佳行按 difflib 映射重寫，內容逐字核實純漂移；見 qa402/resync402.py。")
patch("tests/test_rom176_static.py",
      [(f"line(7765).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'",
        f"line({map_line(7765)}).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'", 1),
       ("line(16449)", f"line({map_line(16449)})", 2),
       (f"line(44292).startswith('/* ===== v20a176 ROM176'",
        f"line({map_line(44292)}).startswith('/* ===== v20a176 ROM176'", 1),
       (f"line(44651).startswith('function rom176ApplyGiftOverrides()')",
        f"line({map_line(44651)}).startswith('function rom176ApplyGiftOverrides()')", 1),
       (f"line(46217).startswith('function addLocTalkGiftActs(add, L, npcId)')",
        f"line({map_line(46217)}).startswith('function addLocTalkGiftActs(add, L, npcId)')", 1),
       (f"'rom176TryIntercept(id)' in line(46375)",
        f"'rom176TryIntercept(id)' in line({map_line(46375)})", 1)],
      "# v402 resync：index.html 淨 +210 行；6 個 line() 釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa402/resync402.py。")
patch("tests/test_tang152_static.py",
      [("lines()[16378].startswith('function normaliseTangStub152(pack){')",
        f"lines()[{map_line(16379) - 1}].startswith('function normaliseTangStub152(pack){{')", 1),
       ("lines()[16503].strip().startswith('try{ normaliseTangStub152(rom2);')",
        f"lines()[{map_line(16504) - 1}].strip().startswith('try{{ normaliseTangStub152(rom2);')", 1)],
      "# v402 resync：index.html 淨 +210 行；normaliseTangStub152 兩釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa402/resync402.py。")
patch("tests/test_text125_static.py",
      [("if len(ls) < 12399 or FALLBACK not in ls[12398]:",
        f"if len(ls) < {map_line(12399)} or FALLBACK not in ls[{map_line(12399) - 1}]:", 1),
       ('probs.append("currentLine 第 12399 行冇 text fallback")',
        f'probs.append("currentLine 第 {map_line(12399)} 行冇 text fallback")', 1),
       ("v401 resync：12247→12399（difflib 對位核實純漂移，見 qa401/resync401.py）",
        f"v401 resync：12247→12399（difflib 對位核實純漂移，見 qa401/resync401.py）；v402 resync：12399→{map_line(12399)}（difflib 對位核實純漂移，見 qa402/resync402.py）", 1),
       ("if len(ls) < 12541 or FALLBACK not in ls[12540]:",
        f"if len(ls) < {map_line(12541)} or FALLBACK not in ls[{map_line(12541) - 1}]:", 1),
       ('probs.append("advance 第 12541 行冇 text fallback")',
        f'probs.append("advance 第 {map_line(12541)} 行冇 text fallback")', 1),
       ("v401 resync：12389→12541（difflib 對位核實純漂移，見 qa401/resync401.py）",
        f"v401 resync：12389→12541（difflib 對位核實純漂移，見 qa401/resync401.py）；v402 resync：12541→{map_line(12541)}（difflib 對位核實純漂移，見 qa402/resync402.py）", 1),
       ("if len(ls) < 18164 or 'if(typeof b.text === \"string\" && b.text){' not in ls[18163]:",
        f"if len(ls) < {map_line(18164)} or 'if(typeof b.text === \"string\" && b.text){{' not in ls[{map_line(18164) - 1}]:", 1),
       ('probs.append("applyFamilySafeToNode 第 18164 行冇 b.text 分支")',
        f'probs.append("applyFamilySafeToNode 第 {map_line(18164)} 行冇 b.text 分支")', 1),
       ("v401 resync：18012→18164（difflib 對位核實純漂移，見 qa401/resync401.py）",
        f"v401 resync：18012→18164（difflib 對位核實純漂移，見 qa401/resync401.py）；v402 resync：18164→{map_line(18164)}（difflib 對位核實純漂移，見 qa402/resync402.py）", 1)],
      "# v402 resync：index.html 淨 +210 行；三錨點按 difflib 映射重寫，內容逐字核實純漂移；見 qa402/resync402.py。")

# ---------- (b) 釘行＋總行數鏈 ----------
patch("tests/test_gift185_static.py",
      [("總行數 51561（", "總行數 51771（", 1),
       ("== 51561)", "== 51771)", 1),
       ("＋v400 +186＋v401 +192）'", "＋v400 +186＋v401 +192＋v402 +210）'", 1)],
      "# v402 resync：index.html 淨 +210 行（51561→51771）；見 qa402/resync402.py。")
patch("tests/test_tang171_static.py",
      [("總行數 51561（", "總行數 51771（", 1),
       ("== 51561)", "== 51771)", 1),
       ("＋v400 +186＋v401 +192）'", "＋v400 +186＋v401 +192＋v402 +210）'", 1),
       ("len(lines) >= 46334 and 'function openLoc(id, opts){' in lines[46333]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1)],
      "# v402 resync：index.html 淨 +210 行（51561→51771）；openLoc DEF 46334→" + str(DEF_NEW) + "；見 qa402/resync402.py。")
patch("tests/test_tang173_static.py",
      [("總行數 51561（", "總行數 51771（", 1),
       ("== 51561)", "== 51771)", 1),
       ("＋v400 +186＋v401 +192）'", "＋v400 +186＋v401 +192＋v402 +210）'", 1),
       ("len(lines) >= 46334 and 'function openLoc(id, opts){' in lines[46333]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1),
       ("lines[5393]", f"lines[{map_line(5394) - 1}]", 8)],
      "# v402 resync：index.html 淨 +210 行（51561→51771）；openLoc DEF 46334→" + str(DEF_NEW) + "；L4872 釘 lines[5393]→[" + str(map_line(5394) - 1) + "]（8 處）；見 qa402/resync402.py。")

resync_travel114()
print("v402 resync done")
