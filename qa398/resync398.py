#!/usr/bin/env python3
"""v398 resync：index.html 淨 +132 行（50979→51111；改動散喺全檔，唔係淨加檔尾）。

改動點（相對 v397 main 9fae41f，difflib opcode 摘要）：
  CSS：tut-step-map 教學卡貼底 ＋2／#mask.scene398 日結家族 dim ＋5／
       .tut-spotlight-ring398 金圈 ＋7／np214 cropbanner＋fade ＋14／
       board-head392／board-sum392 紙章化＋整理選單組名 ＋1＋10。
  JS：keepScene397:true 加 7 處（設定／43／日結兩路／rom159 兩處／
       35_invite；同行改動，淨 0）；teaser 約 ％／詳情精確值註（同行，淨 0）；
       入地圖「今日」toast 兩處刪除（5 行→2 行註解，淨 −3）；
       clampMapLabels397 改可見帶（＋17＋8，deCollide 尾 ＋3）；
       drawMap 尾聚光重定位 ＋2；modal() scene398 掛／closeModal 拆 ＋2＋1；
       np214 cropBanner ＋3；board 整理選單重組（sortLabel392 刪 −1、
       ctl 重組 ＋1−1）；rom183 TUT_MAP 重複句（同行，淨 0）；
       applyTutSpotlight 尾 refresh ＋1／alignTutSurface ＋1／
       showTutMainStep ＋1／finishTutorial ＋2；聚光環函數 ＋52。
影響：
  (a) 行為改動（有意圖，唔係漂移）：
      - 入地圖「今日」toast 刪除（UI398-2：蓋住地圖頂部地點牌；日卡
        #map-hint 本身已經寫住同一資訊，過日指引留喺「過一日」掣
        title）。r295 'day toast' 斷言改釘刪除＋日卡替代。
      - 35_invite 請柬加 keepScene397:true（UI398-5 日結家族統一場景
        背圖）；reconfirm236 C5 字面跟新值，onDismiss=skip 唔郁。
      - 排序＋媒介合成一個「整理」掣（UI398-4），靜態 <button
        112→111；v396/v397 button 總數斷言跟新值。
  (b) 釘行全部按 difflib 映射重寫，內容逐字核實純漂移：
      travel114 FREE 42 處＋COUNT 13 處＋DEF 45873→45945＋WRAPPER
      32005→32074；rom159 6 釘＋全佳行 28161→28230；rom176 6 釘；
      tang152 兩釘；text125 三錨點；tang171／tang173 DEF 45873→45945；
      tang173 lines[5333]→[5361]（8 處）。
  (c) 總行數鏈：50979→51111（＋v398 +132，含 showTutMainStep 延遲 refresh 補丁 ＋4：註解 3＋setTimeout 1）；openLoc DEF 鏈 ＋v398 +72。
紀律：travel114 兩個 set 用單次掃描 dict 查表（唔好逐對 re.sub——v162 教訓：
重疊 pair 會食錨點）；其餘逐處 replace 全部 assert 恰好出現一次；
ok() 名入面嘅 L 號係歷史標籤，唔郁（總行數鏈同報錯字串行號例外，一併更新）。
用法：python3 qa398/resync398.py（喺 resync commit 之前跑一次；OLD 攞
HEAD＝v397 main 9fae41f，assert 總行數 50979，跑完再 commit 就唔會
重跑——每檔開頭有「v398 resync」註記就跳過）。
"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "HEAD:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 50979, len(OLD) - 1  # v397 main 9fae41f
assert len(NEW) - 1 == 51111, len(NEW) - 1  # split 尾空行；count('\n') == 51111

NOTE = "# v398 resync：index.html 淨 +132 行（50979→51111）；見 qa398/resync398.py。"


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note):
    """subs：(old, new, expect_count)；逐處 replace，assert 出現次數。"""
    src = read(path)
    if src.split("\n")[0].startswith(("# v398 resync", "// v398 resync")):
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


# travel114：FREE 42＋COUNT 13——difflib 映射＋逐行內容核實。
# 2 處重複行（衣櫃 7770/7771／禮品店 49266/49267）額外用跟住嗰行核實：
# 衣櫃嗰對後面係 clothing-shop265-list，禮品店嗰對後面係 gift-shop-list。
FREE_MAP = {44970: 45042, 44990: 45062, 7770: 7809, 7771: 7810, 9389: 9428,
            15673: 15712, 15674: 15713, 15686: 15725, 15687: 15726,
            15698: 15737, 15699: 15738, 15794: 15833, 27385: 27454,
            28729: 28798, 28730: 28799, 28818: 28887, 31167: 31236,
            31200: 31269, 43612: 43684, 43731: 43803, 43823: 43895,
            44030: 44102, 44074: 44146, 44080: 44152, 44147: 44219,
            44149: 44221, 44152: 44224, 44179: 44251, 45719: 45791,
            45771: 45843, 45835: 45907, 45836: 45908, 46141: 46213,
            46163: 46235, 46320: 46392, 46325: 46397, 47381: 47452,
            49146: 49217, 49266: 49337, 49267: 49338, 49302: 49373,
            49303: 49374, 49332: 49403, 50235: 50366}
COUNT_MAP = {20610: 20649, 16800: 16839, 20505: 20544, 22926: 22965,
             24240: 24276, 25083: 25147, 25086: 25150, 25117: 25181,
             31369: 31438, 49387: 49458, 49595: 49666, 49762: 49833,
             49783: 49854}
for _old, _new in list(FREE_MAP.items()) + list(COUNT_MAP.items()):
    assert map_line(_old) == _new, f"travel114 {_old} -> {map_line(_old)} != {_new}"
assert "clothing-shop265-list" in NEW[7810], "衣櫃重複行上下文唔啱"
assert "gift-shop-list" in NEW[49338], "禮品店重複行上下文唔啱"
DEF_NEW = map_line(45873)   # 45945
WRAP_NEW = map_line(32005)  # 32074
assert DEF_NEW == 45945 and WRAP_NEW == 32074


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.split("\n")[0].startswith("# v398 resync"):
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
    for old, new, n in [(f"DEF_LINE = 45873", f"DEF_LINE = {DEF_NEW}", 1),
                        (f"WRAPPER_LINE = 32005", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, "# v398 resync：index.html 淨 +132 行（50979→51111）；FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；openLoc( 呼叫點總數不變；見 qa398/resync398.py。")
    write(path, "\n".join(lines))
    print(f"patched {path}")


# ---------- (a) 行為改動：入地圖「今日」toast 刪除（v398 UI398-2） ----------
# r295 'day toast' 斷言改釘：toast 唔再存在，今日資訊由日卡常駐顯示
# （planLine `今日：<b>${planName135}</b>`），過日指引留喺「過一日」掣 title
# （'free-day titles' 斷言已覆蓋嗰句「逛完點擊這個掣…」）。
patch("tests/test_r295_click_not_gam.js",
      [("chk('day toast', s.indexOf('要過日請點擊「開始今日行程」') >= 0);",
        "chk('day toast gone (v398: 今日資訊改由日卡常駐顯示)', s.indexOf('toast(`今日：${meta.name}`') < 0 && s.indexOf('今日：<b>${planName135}</b>') >= 0);", 1)],
      "// v398 resync：入地圖「今日」toast 已刪（蓋住地圖頂部地點牌，審計 UI398-2；.js 檔用 // 註解）；今日資訊改由日卡常駐顯示（planLine），過日指引留喺「過一日」掣 title；見 qa398/resync398.py。")

# ---------- (a) 行為改動：35_invite 請柬加 keepScene397:true（v398 UI398-5） ----------
patch("tests/test_reconfirm236_static.py",
      [("'{ onDismiss: skip, keepSheetContent:true }' in html",
        "'{ onDismiss: skip, keepSheetContent:true, keepScene397:true }' in html", 1)],
      "# v398 resync：35_invite 請柬加 keepScene397:true（日結卡家族統一場景背圖），onDismiss=skip 唔郁；見 qa398/resync398.py。")

# ---------- (a) 行為改動：排序＋媒介合成一個「整理」掣（v398 UI398-4） ----------
patch("tests/test_v396_static.py",
      [('ok("v397 靜態 <button 總數 112（v396：110）",',
        'ok("v398 靜態 <button 總數 111（v397：112）",', 1),
       ('src.count("<button") == 112)', 'src.count("<button") == 111)', 1)],
      "# v398 resync：排序＋媒介合成一個「整理」掣，靜態 <button −1（112→111）；見 qa398/resync398.py。")

# ---------- (b) 釘行 ----------
patch("tests/test_rom159_static.py",
      [(f'line_has(28133, "v20a159 ROM159 Phase 1")',
        f'line_has({map_line(28133)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(9413, "rom159GainAllowed(k)")',
        f'line_has({map_line(9413)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(29041, "COMMIT48_NODES.CMT_lan_commit")',
        f'line_has({map_line(29041)}, "COMMIT48_NODES.CMT_lan_commit")', 1),
       (f'line_has(11593, "rom159PrepareNode(node)")',
        f'line_has({map_line(11593)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(16225, "rom159ApplyGiftOverrides()")',
        f'line_has({map_line(16225)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(28896, "function rom159SoMeetGate")',
        f'line_has({map_line(28896)}, "function rom159SoMeetGate")', 1),
       ('"查實" in idx_lines[28160]', f'"查實" in idx_lines[{map_line(28161) - 1}]', 1)],
      "# v398 resync：index.html 淨 +128 行；6 個 line_has 釘行＋全佳行按 difflib 映射重寫（28133→28202、9413→9452、29041→29110、11593→11632、16225→16264、28896→28965、全佳 28161→28230），內容逐字核實純漂移；見 qa398/resync398.py。")
patch("tests/test_rom176_static.py",
      [(f"line(7539).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'",
        f"line({map_line(7539)}).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'", 1),
       ("line(16223)", f"line({map_line(16223)})", 2),
       (f"line(43831).startswith('/* ===== v20a176 ROM176'",
        f"line({map_line(43831)}).startswith('/* ===== v20a176 ROM176'", 1),
       (f"line(44190).startswith('function rom176ApplyGiftOverrides()')",
        f"line({map_line(44190)}).startswith('function rom176ApplyGiftOverrides()')", 1),
       (f"line(45756).startswith('function addLocTalkGiftActs(add, L, npcId)')",
        f"line({map_line(45756)}).startswith('function addLocTalkGiftActs(add, L, npcId)')", 1),
       (f"'rom176TryIntercept(id)' in line(45914)",
        f"'rom176TryIntercept(id)' in line({map_line(45914)})", 1)],
      "# v398 resync：index.html 淨 +128 行；6 個 line() 釘行按 difflib 映射重寫（7539→7578、16223→16262、43831→43903、44190→44262、45756→45828、45914→45986），內容逐字核實純漂移；見 qa398/resync398.py。")
patch("tests/test_tang152_static.py",
      [("lines()[16152].startswith('function normaliseTangStub152(pack){')",
        f"lines()[{map_line(16153) - 1}].startswith('function normaliseTangStub152(pack){{')", 1),
       ("lines()[16277].strip().startswith('try{ normaliseTangStub152(rom2);')",
        f"lines()[{map_line(16278) - 1}].strip().startswith('try{{ normaliseTangStub152(rom2);')", 1)],
      "# v398 resync：index.html 淨 +128 行；normaliseTangStub152 兩釘按 difflib 映射重寫（lines()[16152]→[16191]、[16277]→[16316]），內容逐字核實純漂移；見 qa398/resync398.py。")
patch("tests/test_text125_static.py",
      [("if len(ls) < 12173 or FALLBACK not in ls[12172]:",
        f"if len(ls) < {map_line(12173)} or FALLBACK not in ls[{map_line(12173) - 1}]:", 1),
       ('probs.append("currentLine 第 12173 行冇 text fallback")',
        f'probs.append("currentLine 第 {map_line(12173)} 行冇 text fallback")', 1),
       ("v20a297 resync：11299→11278",
        "v20a297 resync：11299→11278；v398 resync：12173→12212（difflib 對位核實純漂移，見 qa398/resync398.py）", 1),
       ("if len(ls) < 12315 or FALLBACK not in ls[12314]:",
        f"if len(ls) < {map_line(12315)} or FALLBACK not in ls[{map_line(12315) - 1}]:", 1),
       ('probs.append("advance 第 12315 行冇 text fallback")',
        f'probs.append("advance 第 {map_line(12315)} 行冇 text fallback")', 1),
       ("v20a297 resync：11441→11420",
        "v20a297 resync：11441→11420；v398 resync：12315→12354（difflib 對位核實純漂移，見 qa398/resync398.py）", 1),
       ("if len(ls) < 17928 or 'if(typeof b.text === \"string\" && b.text){' not in ls[17927]:",
        f"if len(ls) < {map_line(17928)} or 'if(typeof b.text === \"string\" && b.text){{' not in ls[{map_line(17928) - 1}]:", 1),
       ('probs.append("applyFamilySafeToNode 第 17928 行冇 b.text 分支")',
        f'probs.append("applyFamilySafeToNode 第 {map_line(17928)} 行冇 b.text 分支")', 1),
       ("v20a297 resync：16385→16349",
        "v20a297 resync：16385→16349；v398 resync：17928→17967（difflib 對位核實純漂移，見 qa398/resync398.py）", 1)],
      "# v398 resync：index.html 淨 +128 行；三錨點按 difflib 映射重寫（12173→12212、12315→12354、17928→17967），內容逐字核實純漂移；見 qa398/resync398.py。")

# ---------- (b) 釘行＋總行數鏈 ----------
patch("tests/test_gift185_static.py",
      [("html.count('\\n') == 50979", "html.count('\\n') == 51107", 1),
       ("總行數 50979（", "總行數 51107（", 1),
       ("＋v397 +338）'", "＋v397 +338＋v398 +128）'", 1)],
      "# v398 resync：index.html 淨 +128 行（50979→51107）；見 qa398/resync398.py。")
patch("tests/test_tang171_static.py",
      [("src.count('\\n') == 50979", "src.count('\\n') == 51107", 1),
       ("總行數 50979（", "總行數 51107（", 1),
       ("＋v397 +338）'", "＋v397 +338＋v398 +128）'", 1),
       ("len(lines) >= 45873 and 'function openLoc(id, opts){' in lines[45872]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1)],
      "# v398 resync：index.html 淨 +128 行（50979→51107）；openLoc DEF 45873→45945；見 qa398/resync398.py。")
patch("tests/test_tang173_static.py",
      [("src.count('\\n') == 50979", "src.count('\\n') == 51107", 1),
       ("總行數 50512（", "總行數 51107（", 1),
       ("＋v397 +338）'", "＋v397 +338＋v398 +128）'", 1),
       ("len(lines) >= 45873 and 'function openLoc(id, opts){' in lines[45872]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1),
       ("lines[5333]", f"lines[{map_line(5334) - 1}]", 8)],
      "# v398 resync：index.html 淨 +128 行（50979→51107）；openLoc DEF 45873→45945；L4872 釘 lines[5333]→[5361]（8 處）；見 qa398/resync398.py。")

resync_travel114()
print("v398 resync done")
