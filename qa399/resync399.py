#!/usr/bin/env python3
"""v399 resync：index.html 淨 +72 行（51111→51183；改動散喺全檔，唔係淨加檔尾）。

改動點（相對 v398 main 070eae7，git diff hunk 摘要）：
  CSS：設定深啡條改淺紙底＋hint 深啡字 ＋3／#tut-target-label399 浮貼 ＋15／
       board-sum392 剪報標籤化 ＋3／board-ctl397 側邊紙籤 ＋1／
       board pin 上移＋menu 收窄 ＋2。
  JS：35c 右欄直排只留行首 6 字 ＋4／doAudition 標題＋keepScene397 ＋2＋0／
       tutBodyHtml 註解 ＋1／ensureTutSpotlightRing398 浮貼 helpers ＋39／
       refreshTutSpotlight398 接線 ＋0＋2。
影響：
  (a) 行為改動（有意圖，唔係漂移）：
      - 已選速度 pill「快」由金底 #c97f1f 改深啡底 #5c4a1f 配 #fff8e8 白字
        （UI399-1：cream on gold 3.03，低過 4.5:1；改後實量 8.09）。
        test_ui128a6_static.py 斷言跟新值（ok 名「選中金底」→「選中深啡底」）。
      - 設定頁註解本來寫「即將推出 1.35」令 html.count('即將推出') 變 2，
        test_ui105_static.py（S-48：只得一行「即將推出」）fail；註解改寫做
        「未推出行 1.35」，index.html 入面「即將推出」回復 1 次，測試唔郁。
  (b) 釘行全部按 difflib 映射重寫，內容逐字核實純漂移：
      travel114 FREE 42 處＋COUNT 13 處＋DEF 45945→45973＋WRAPPER
      32074→32098；rom159 6 釘＋全佳行 28230→28254；rom176 6 釘；
      tang152 兩釘；text125 三錨點；tang171／tang173 DEF 45945→45973；
      tang173 lines[5361]→[5382]（8 處）；gift185／tang171／tang173
      總行數 51111→51183，行數鏈尾加 ＋v399 +72。
  (c) 總行數鏈：51111→51183（＋v399 +72）；openLoc DEF 鏈 ＋v399 +28。
紀律：travel114 兩個 set 用單次掃描 dict 查表（唔好逐對 re.sub——v162 教訓：
重疊 pair 會食錨點）；其餘逐處 replace 全部 assert 恰好出現一次；
ok() 名入面嘅 L 號係歷史標籤，唔郁（總行數鏈同報錯字串行號例外，一併更新）。
用法：python3 qa399/resync399.py（喺 resync commit 之前跑一次；OLD 攞
v398 main 070eae7（唔係 HEAD——HEAD 已經係 v399 commit），assert 總行數
51111，跑完再 commit 就唔會重跑——每檔開頭有「v399 resync」註記就跳過）。
"""
import difflib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "070eae7:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 51111, len(OLD) - 1  # v398 main 070eae7
assert len(NEW) - 1 == 51183, len(NEW) - 1  # split 尾空行；count('\n') == 51183

NOTE = "# v399 resync：index.html 淨 +72 行（51111→51183）；見 qa399/resync399.py。"


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, src):
    with open(os.path.join(ROOT, path), "w", encoding="utf-8") as f:
        f.write(src)


def patch(path, subs, note):
    """subs：(old, new, expect_count)；逐處 replace，assert 出現次數。"""
    src = read(path)
    if src.split("\n")[0].startswith(("# v399 resync", "// v399 resync")):
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
# 2 處重複行（衣櫃 7809/7810／禮品店 49337/49338）額外用跟住嗰行核實：
# 衣櫃嗰對後面係 clothing-shop265-list，禮品店嗰對後面係 gift-shop-list。
FREE_MAP = {45042: 45070, 45062: 45090, 7809: 7833, 7810: 7834, 9428: 9452,
            15712: 15736, 15713: 15737, 15725: 15749, 15726: 15750,
            15737: 15761, 15738: 15762, 15833: 15857, 27454: 27478,
            28798: 28822, 28799: 28823, 28887: 28911, 31236: 31260,
            31269: 31293, 43684: 43712, 43803: 43831, 43895: 43923,
            44102: 44130, 44146: 44174, 44152: 44180, 44219: 44247,
            44221: 44249, 44224: 44252, 44251: 44279, 45791: 45819,
            45843: 45871, 45907: 45935, 45908: 45936, 46213: 46241,
            46235: 46263, 46392: 46420, 46397: 46425, 47452: 47480,
            49217: 49245, 49337: 49367, 49338: 49368, 49373: 49403,
            49374: 49404, 49403: 49433, 50367: 50439}
COUNT_MAP = {20649: 20673, 16839: 16863, 20544: 20568, 22965: 22989,
             24276: 24300, 25147: 25171, 25150: 25174, 25181: 25205,
             31438: 31462, 49458: 49488, 49666: 49696, 49833: 49863,
             49854: 49884}
for _old, _new in list(FREE_MAP.items()) + list(COUNT_MAP.items()):
    assert map_line(_old) == _new, f"travel114 {_old} -> {map_line(_old)} != {_new}"
assert "clothing-shop265-list" in NEW[7834], "衣櫃重複行上下文唔啱"
assert "gift-shop-list" in NEW[49368], "禮品店重複行上下文唔啱"
DEF_NEW = map_line(45945)   # 45973
WRAP_NEW = map_line(32074)  # 32098
assert DEF_NEW == 45973 and WRAP_NEW == 32098


def resync_travel114():
    path = "tests/test_travel114_static.py"
    src = read(path)
    if src.split("\n")[0].startswith("# v399 resync"):
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
    for old, new, n in [(f"DEF_LINE = 45945", f"DEF_LINE = {DEF_NEW}", 1),
                        (f"WRAPPER_LINE = 32074", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, "# v399 resync：index.html 淨 +72 行（51111→51183）；FREE／COUNT／DEF／WRAPPER 按 difflib 映射重寫，內容逐行核實純漂移；openLoc( 呼叫點總數不變；見 qa399/resync399.py。")
    write(path, "\n".join(lines))
    print(f"patched {path}")


# ---------- (a) 行為改動：已選速度 pill 金底改深啡底（UI399-1） ----------
patch("tests/test_ui128a6_static.py",
      [("ok('速度 紙掣 CSS 在（米紙底＋金邊＋選中金底）', '.set-speed128 .set-speed-btn.on{ background:#c97f1f' in html)",
        "ok('速度 紙掣 CSS 在（米紙底＋金邊＋選中深啡底）', '.set-speed128 .set-speed-btn.on{ background:#5c4a1f' in html)", 1)],
      "# v399 resync：已選速度 pill「快」由金底 #c97f1f 改深啡底 #5c4a1f 配 #fff8e8 白字（UI399-1：cream on gold 3.03 低過 4.5:1，改後實量 8.09；見 qa399/resync399.py）。")

# ---------- (b) 釘行 ----------
patch("tests/test_rom159_static.py",
      [(f'line_has(28202, "v20a159 ROM159 Phase 1")',
        f'line_has({map_line(28202)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(9452, "rom159GainAllowed(k)")',
        f'line_has({map_line(9452)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(29110, "COMMIT48_NODES.CMT_lan_commit")',
        f'line_has({map_line(29110)}, "COMMIT48_NODES.CMT_lan_commit")', 1),
       (f'line_has(11632, "rom159PrepareNode(node)")',
        f'line_has({map_line(11632)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(16264, "rom159ApplyGiftOverrides()")',
        f'line_has({map_line(16264)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(28965, "function rom159SoMeetGate")',
        f'line_has({map_line(28965)}, "function rom159SoMeetGate")', 1),
       ('"查實" in idx_lines[28229]', f'"查實" in idx_lines[{map_line(28230) - 1}]', 1)],
      "# v399 resync：index.html 淨 +72 行；6 個 line_has 釘行＋全佳行按 difflib 映射重寫（28202→28226、9452→9476、29110→29134、11632→11656、16264→16288、28965→28989、全佳 28230→28254），內容逐字核實純漂移；見 qa399/resync399.py。")
patch("tests/test_rom176_static.py",
      [(f"line(7578).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'",
        f"line({map_line(7578)}).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'", 1),
       ("line(16262)", f"line({map_line(16262)})", 2),
       (f"line(43903).startswith('/* ===== v20a176 ROM176'",
        f"line({map_line(43903)}).startswith('/* ===== v20a176 ROM176'", 1),
       (f"line(44262).startswith('function rom176ApplyGiftOverrides()')",
        f"line({map_line(44262)}).startswith('function rom176ApplyGiftOverrides()')", 1),
       (f"line(45828).startswith('function addLocTalkGiftActs(add, L, npcId)')",
        f"line({map_line(45828)}).startswith('function addLocTalkGiftActs(add, L, npcId)')", 1),
       (f"'rom176TryIntercept(id)' in line(45986)",
        f"'rom176TryIntercept(id)' in line({map_line(45986)})", 1)],
      "# v399 resync：index.html 淨 +72 行；6 個 line() 釘行按 difflib 映射重寫（7578→7602、16262→16286、43903→43931、44262→44290、45828→45856、45986→46014），內容逐字核實純漂移；見 qa399/resync399.py。")
patch("tests/test_tang152_static.py",
      [("lines()[16191].startswith('function normaliseTangStub152(pack){')",
        f"lines()[{map_line(16192) - 1}].startswith('function normaliseTangStub152(pack){{')", 1),
       ("lines()[16316].strip().startswith('try{ normaliseTangStub152(rom2);')",
        f"lines()[{map_line(16317) - 1}].strip().startswith('try{{ normaliseTangStub152(rom2);')", 1)],
      "# v399 resync：index.html 淨 +72 行；normaliseTangStub152 兩釘按 difflib 映射重寫（lines()[16191]→[16215]、[16316]→[16340]），內容逐字核實純漂移；見 qa399/resync399.py。")
patch("tests/test_text125_static.py",
      [("if len(ls) < 12212 or FALLBACK not in ls[12211]:",
        f"if len(ls) < {map_line(12212)} or FALLBACK not in ls[{map_line(12212) - 1}]:", 1),
       ('probs.append("currentLine 第 12212 行冇 text fallback")',
        f'probs.append("currentLine 第 {map_line(12212)} 行冇 text fallback")', 1),
       ("v398 resync：12173→12212（difflib 對位核實純漂移，見 qa398/resync398.py）",
        "v398 resync：12173→12212（difflib 對位核實純漂移，見 qa398/resync398.py）；v399 resync：12212→12236（difflib 對位核實純漂移，見 qa399/resync399.py）", 1),
       ("if len(ls) < 12354 or FALLBACK not in ls[12353]:",
        f"if len(ls) < {map_line(12354)} or FALLBACK not in ls[{map_line(12354) - 1}]:", 1),
       ('probs.append("advance 第 12354 行冇 text fallback")',
        f'probs.append("advance 第 {map_line(12354)} 行冇 text fallback")', 1),
       ("v398 resync：12315→12354（difflib 對位核實純漂移，見 qa398/resync398.py）",
        "v398 resync：12315→12354（difflib 對位核實純漂移，見 qa398/resync398.py）；v399 resync：12354→12378（difflib 對位核實純漂移，見 qa399/resync399.py）", 1),
       ("if len(ls) < 17967 or 'if(typeof b.text === \"string\" && b.text){' not in ls[17966]:",
        f"if len(ls) < {map_line(17967)} or 'if(typeof b.text === \"string\" && b.text){{' not in ls[{map_line(17967) - 1}]:", 1),
       ('probs.append("applyFamilySafeToNode 第 17967 行冇 b.text 分支")',
        f'probs.append("applyFamilySafeToNode 第 {map_line(17967)} 行冇 b.text 分支")', 1),
       ("v398 resync：17928→17967（difflib 對位核實純漂移，見 qa398/resync398.py）",
        "v398 resync：17928→17967（difflib 對位核實純漂移，見 qa398/resync398.py）；v399 resync：17967→17991（difflib 對位核實純漂移，見 qa399/resync399.py）", 1)],
      "# v399 resync：index.html 淨 +72 行；三錨點按 difflib 映射重寫（12212→12236、12354→12378、17967→17991），內容逐字核實純漂移；見 qa399/resync399.py。")

# ---------- (b) 釘行＋總行數鏈 ----------
patch("tests/test_gift185_static.py",
      [("總行數 51111（", "總行數 51183（", 1),
       ("== 51111)", "== 51183)", 1),
       ("＋v398 +132）'", "＋v398 +132＋v399 +72）'", 1)],
      "# v399 resync：index.html 淨 +72 行（51111→51183）；見 qa399/resync399.py。")
patch("tests/test_tang171_static.py",
      [("總行數 51111（", "總行數 51183（", 1),
       ("== 51111)", "== 51183)", 1),
       ("＋v398 +132）'", "＋v398 +132＋v399 +72）'", 1),
       ("len(lines) >= 45945 and 'function openLoc(id, opts){' in lines[45944]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1)],
      "# v399 resync：index.html 淨 +72 行（51111→51183）；openLoc DEF 45945→45973；見 qa399/resync399.py。")
patch("tests/test_tang173_static.py",
      [("總行數 51111（", "總行數 51183（", 1),
       ("== 51111)", "== 51183)", 1),
       ("＋v398 +132）'", "＋v398 +132＋v399 +72）'", 1),
       ("len(lines) >= 45945 and 'function openLoc(id, opts){' in lines[45944]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1),
       ("lines[5361]", f"lines[{map_line(5362) - 1}]", 8)],
      "# v399 resync：index.html 淨 +72 行（51111→51183）；openLoc DEF 45945→45973；L4872 釘 lines[5361]→[5382]（8 處）；見 qa399/resync399.py。")

resync_travel114()
print("v399 resync done")
