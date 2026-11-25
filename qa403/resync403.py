#!/usr/bin/env python3
"""v403 resync：index.html 淨 +125 行（51771→51896；UI403 第十輪頭五項＋暗角 dismiss）。

改動點（相對 v402 main d1a46b5，difflib hunk 摘要）：
  CSS：v403 集中區塊（捲動安全區／固定抬頭／支票 memo 上移／教學舞台收窄／
       頒獎下接提示／推介場景圖／索引紙籤／合約紙詳情／結局紙／人情頁／
       資料卡手寫化／toast 唔擋暗角）；頒獎 26px mask rule 拆除（同行改寫區）。
  JS：MAP403_ANCHORS 靜態錨點＋map403CurTop／map403LabelsReady（地圖標籤錨點
       損毀修復）；positionMapLabels137 改靜態錨點；clamp／deCollide 改
       offsetTop 口徑＋venue99 納入；paintBar 定位前唔推撞；
       align403ScrollEdges＋awd403FoldAndHint（捲動邊界／頒獎摺位）；
       modal／syncHomeTabExit 掛鈎；推介卡場景圖＋總片酬 meta 首項；
       mask 暗角 dismiss（target #modal 亦算＋board-tall392 豁免教學阻擋）；
       何生事務所靜態錨 offset -52→-42（同維港電影近距對解開）。
影響：
  (a) 有意圖行為改動（唔係漂移，測試同步更新）：
      · v398 fade rule 拆除＋「下接」提示（第十輪裁決改 fade）——
        test_v398_static.py 期望同步更新（mask 不存在＋下接存在）。
      · 何生事務所錨 offset -52→-42——test_ui142_static.py／
        test_ux68_static.py 期望同步更新（近距對解開，調查報告 §6⑥）。
      · s30dedup：gigBoardTeaserHtml 註解縮短（行數不變），令 gt-meta
        返入 test 嘅 6000 字元抽取窗；test 本身唔使改。
      · v401 整理選單：v403 索引紙籤保留 rotate(-.6deg)＋透明文字行，
        v401 test 期望照過，唔使改。
  (b) 釘行全部按 difflib 映射重寫，內容逐字核實純漂移：
      travel114 FREE／COUNT＋DEF／WRAPPER；rom159 6 釘＋全佳行；
      rom176 6 釘；tang152 兩釘；text125 三錨點；tang171／tang173 DEF；
      tang173 lines[5412]（8 處）；gift185／tang171／tang173 總行數
      51771→51896，行數鏈尾加 ＋v403 +125。
紀律：travel114 兩個 set 用單次掃描 dict 查表（唔好逐對 re.sub——v162 教訓）；
其餘逐處 replace 全部 assert 恰好出現一次；ok() 名入面嘅 L 號係歷史標籤，
唔郁（總行數鏈同報錯字串行號例外，一併更新）。
用法：python3 qa403/resync403.py（OLD 攞 v402 main d1a46b5，assert 總行數
51771；每檔開頭有「v403 resync」註記就跳過）。
"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "d1a46b5:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 51771, len(OLD) - 1  # v402 main d1a46b5
assert len(NEW) - 1 == 51896, len(NEW) - 1


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note):
    src = read(path)
    if src.split("\n")[0].startswith(("# v403 resync", "// v403 resync")):
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
DEF_NEW = map_line(46522)
WRAP_NEW = map_line(32625)
print(f"travel114 DEF 46522->{DEF_NEW} WRAPPER 32625->{WRAP_NEW}")


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.split("\n")[0].startswith("# v403 resync"):
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
    for old, new, n in [("DEF_LINE = 46522", f"DEF_LINE = {DEF_NEW}", 1),
                        ("WRAPPER_LINE = 32625", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, "# v403 resync：index.html 淨 +125 行（51771→51896）；FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；openLoc( 呼叫點總數不變；見 qa403/resync403.py。")
    write(path, "\n".join(lines))
    print(f"patched {path}")


patch("tests/test_rom159_static.py",
      [(f'line_has(28753, "v20a159 ROM159 Phase 1")',
        f'line_has({map_line(28753)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(9750, "rom159GainAllowed(k)")',
        f'line_has({map_line(9750)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(29661, "COMMIT48_NODES.CMT_lan_commit")',
        f'line_has({map_line(29661)}, "COMMIT48_NODES.CMT_lan_commit")', 1),
       (f'line_has(11930, "rom159PrepareNode(node)")',
        f'line_has({map_line(11930)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(16562, "rom159ApplyGiftOverrides()")',
        f'line_has({map_line(16562)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(29516, "function rom159SoMeetGate")',
        f'line_has({map_line(29516)}, "function rom159SoMeetGate")', 1),
       ('"查實" in idx_lines[28780]', f'"查實" in idx_lines[{map_line(28781) - 1}]', 1)],
      "# v403 resync：index.html 淨 +125 行；6 個 line_has 釘行＋全佳行按 difflib 映射重寫，內容逐字核實純漂移；見 qa403/resync403.py。")
patch("tests/test_rom176_static.py",
      [(f"line(7876).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'",
        f"line({map_line(7876)}).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'", 1),
       ("line(16560)", f"line({map_line(16560)})", 2),
       (f"line(44480).startswith('/* ===== v20a176 ROM176'",
        f"line({map_line(44480)}).startswith('/* ===== v20a176 ROM176'", 1),
       (f"line(44839).startswith('function rom176ApplyGiftOverrides()')",
        f"line({map_line(44839)}).startswith('function rom176ApplyGiftOverrides()')", 1),
       (f"line(46405).startswith('function addLocTalkGiftActs(add, L, npcId)')",
        f"line({map_line(46405)}).startswith('function addLocTalkGiftActs(add, L, npcId)')", 1),
       (f"'rom176TryIntercept(id)' in line(46563)",
        f"'rom176TryIntercept(id)' in line({map_line(46563)})", 1)],
      "# v403 resync：index.html 淨 +125 行；6 個 line() 釘行按 difflib 映射重寫，內容逐字核實純漂移；見 qa403/resync403.py。")
patch("tests/test_tang152_static.py",
      [("lines()[16489].startswith('function normaliseTangStub152(pack){')",
        f"lines()[{map_line(16490) - 1}].startswith('function normaliseTangStub152(pack){{')", 1),
       ("lines()[16614].strip().startswith('try{ normaliseTangStub152(rom2);')",
        f"lines()[{map_line(16615) - 1}].strip().startswith('try{{ normaliseTangStub152(rom2);')", 1)],
      "# v403 resync：index.html 淨 +125 行；normaliseTangStub152 兩釘按 difflib 映射重寫，內容逐字核實純漂移；見 qa403/resync403.py。")
patch("tests/test_text125_static.py",
      [("if len(ls) < 12510 or FALLBACK not in ls[12509]:",
        f"if len(ls) < {map_line(12510)} or FALLBACK not in ls[{map_line(12510) - 1}]:", 1),
       ('probs.append("currentLine 第 12510 行冇 text fallback")',
        f'probs.append("currentLine 第 {map_line(12510)} 行冇 text fallback")', 1),
       ("v402 resync：12399→12510（difflib 對位核實純漂移，見 qa402/resync402.py）",
        f"v402 resync：12399→12510（difflib 對位核實純漂移，見 qa402/resync402.py）；v403 resync：12510→{map_line(12510)}（difflib 對位核實純漂移，見 qa403/resync403.py）", 1),
       ("if len(ls) < 12652 or FALLBACK not in ls[12651]:",
        f"if len(ls) < {map_line(12652)} or FALLBACK not in ls[{map_line(12652) - 1}]:", 1),
       ('probs.append("advance 第 12652 行冇 text fallback")',
        f'probs.append("advance 第 {map_line(12652)} 行冇 text fallback")', 1),
       ("v402 resync：12541→12652（difflib 對位核實純漂移，見 qa402/resync402.py）",
        f"v402 resync：12541→12652（difflib 對位核實純漂移，見 qa402/resync402.py）；v403 resync：12652→{map_line(12652)}（difflib 對位核實純漂移，見 qa403/resync403.py）", 1),
       ("if len(ls) < 18275 or 'if(typeof b.text === \"string\" && b.text){' not in ls[18274]:",
        f"if len(ls) < {map_line(18275)} or 'if(typeof b.text === \"string\" && b.text){{' not in ls[{map_line(18275) - 1}]:", 1),
       ('probs.append("applyFamilySafeToNode 第 18275 行冇 b.text 分支")',
        f'probs.append("applyFamilySafeToNode 第 {map_line(18275)} 行冇 b.text 分支")', 1),
       ("v402 resync：18164→18275（difflib 對位核實純漂移，見 qa402/resync402.py）",
        f"v402 resync：18164→18275（difflib 對位核實純漂移，見 qa402/resync402.py）；v403 resync：18275→{map_line(18275)}（difflib 對位核實純漂移，見 qa403/resync403.py）", 1)],
      "# v403 resync：index.html 淨 +125 行；三錨點按 difflib 映射重寫，內容逐字核實純漂移；見 qa403/resync403.py。")

patch("tests/test_gift185_static.py",
      [("總行數 51771（", "總行數 51896（", 1),
       ("== 51771)", "== 51896)", 1),
       ("＋v401 +192＋v402 +210）'", "＋v401 +192＋v402 +210＋v403 +125）'", 1)],
      "# v403 resync：index.html 淨 +125 行（51771→51896）；見 qa403/resync403.py。")
patch("tests/test_tang171_static.py",
      [("總行數 51771（", "總行數 51896（", 1),
       ("== 51771)", "== 51896)", 1),
       ("＋v401 +192＋v402 +210）'", "＋v401 +192＋v402 +210＋v403 +125）'", 1),
       ("len(lines) >= 46522 and 'function openLoc(id, opts){' in lines[46521]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1)],
      "# v403 resync：index.html 淨 +125 行（51771→51896）；openLoc DEF 46522→" + str(DEF_NEW) + "；見 qa403/resync403.py。")
patch("tests/test_tang173_static.py",
      [("總行數 51771（", "總行數 51896（", 1),
       ("== 51771)", "== 51896)", 1),
       ("＋v401 +192＋v402 +210）'", "＋v401 +192＋v402 +210＋v403 +125）'", 1),
       ("len(lines) >= 46522 and 'function openLoc(id, opts){' in lines[46521]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1),
       ("lines[5412]", f"lines[{map_line(5413) - 1}]", 8)],
      "# v403 resync：index.html 淨 +125 行（51771→51896）；openLoc DEF 46522→" + str(DEF_NEW) + "；L4872 釘 lines[5412]→[" + str(map_line(5413) - 1) + "]（8 處）；見 qa403/resync403.py。")

resync_travel114()
print("v403 resync done")
