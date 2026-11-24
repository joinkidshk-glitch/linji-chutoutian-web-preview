#!/usr/bin/env python3
"""v397 resync：index.html 淨 +338 行（50641→50979；改動散喺全檔，唔係淨加檔尾）。

改動點（相對 v396 main e92a457）：
  CSS：clampMapLabels397＋.dayres-scene397＋.dayres-stamp397＋.dayres-ledger397
       ＋awd-result396 報頭收緊＋.np214-sb-mark397＋.board-ctl397＋.board-calc397
       ＋#nb-q-tools397／#nb-tools397-menu＋.sp-lock-tag；刪 #nb-actions
       #btn-reset-plan 4 條規則＋.menu-sep。
  JS：clampMapLabels397 ＋板下拉掣 toggle wiring＋boardExpCalc397＋計法行
       ＋locked 摘要搬尾＋keepScene397（setUnderlyingInert scene 分支）
       ＋dayResLedger397（兩條日結路徑）＋40 號掣 reorder＋86c 印章 12 處
       ＋tut-stage397＋行程工具選單＋rom159 約會 who-picker。
  HTML：金禧錨點 top:24%→calc(24% + 30px)；選單刪「過一日」＋分隔線；
       未開放掣→span 紙標。
影響：
  (a) 行為改動（有意圖，唔係漂移）：金禧錨點新位（ui108／ui128a1／v155
      三份測試嘅 86%/24% 斷言跟新位）；「還原」搬入行程工具選單
      （buttons197 B2 :disabled 選擇器＋ui128a6 S-20 規則跟新位置；
      鎖定態嗰陣成個工具組連 #nb-quick 一齊隱藏，見下註）。
  (b) 釘行全部按 difflib 映射重寫，內容逐字核實純漂移：
      travel114 FREE 42 處＋COUNT 13 處＋DEF 45592→45873＋WRAPPER 31780→32005；
      rom159 6 釘＋全佳行；rom176 6 釘；tang152 兩釘；text125 三錨點；
      tang173 lines[5269]→[5333]（4 處）。
  (c) 總行數鏈：50641→50979（＋v397 +338）；openLoc DEF 鏈 ＋v397 +281
      （DEF 行本身漂 +281，檔尾 ＋57 喺佢之後）。
紀律：travel114 兩個 set 用單次掃描 dict 查表（唔好逐對 re.sub——v162 教訓：
重疊 pair 會食錨點）；其餘逐處 replace 全部 assert 恰好出現一次；
ok() 名入面嘅 L 號係歷史標籤，唔郁（總行數鏈同報錯字串行號例外，一併更新）。
用法：python3 qa397/resync397.py（喺 resync commit 之前跑一次；OLD 攞
HEAD~1＝v396 main e92a457，assert 總行數 50641，跑完再 commit 就唔會
重跑——每檔開頭有「v397 resync」註記就跳過）。
"""
import difflib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = subprocess.run(["git", "show", "HEAD~1:index.html"], cwd=ROOT,
                     capture_output=True, text=True).stdout.split("\n")
NEW = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read().split("\n")
assert len(OLD) - 1 == 50641, len(OLD) - 1  # v396 main e92a457
assert len(NEW) - 1 == 50979, len(NEW) - 1  # split 尾空行；count('\n') == 50979

NOTE = "# v397 resync：index.html 淨 +338 行（50641→50979）；見 qa397/resync397.py。"


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
    if not force and src.split("\n")[0].startswith("# v397 resync"):
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
# 4 處重複行（衣櫃 7695/7696／禮品店 48964/48965）額外用跟住嗰行核實：
# 衣櫃嗰對後面係 clothing-shop265-list，禮品店嗰對後面係 gift-shop-list。
FREE_MAP = {7695: 7770, 7696: 7771, 9314: 9389, 15598: 15673, 15599: 15674,
            15611: 15686, 15612: 15687, 15623: 15698, 15624: 15699, 15719: 15794,
            27160: 27385, 28504: 28729, 28505: 28730, 28593: 28818, 30942: 31167,
            30975: 31200, 43368: 43612, 43487: 43731, 43579: 43823, 43786: 44030,
            43830: 44074, 43836: 44080, 43903: 44147, 43905: 44149, 43908: 44152,
            43935: 44179, 44726: 44970, 44746: 44990, 45475: 45719, 45527: 45771,
            45860: 46141, 45882: 46163, 46039: 46320, 46044: 46325, 47097: 47381,
            48844: 49146, 48964: 49266, 48965: 49267, 49000: 49302, 49001: 49303,
            49030: 49332, 49931: 50235}
COUNT_MAP = {16725: 16800, 20371: 20505, 20470: 20610, 22768: 22926, 24078: 24240,
             24858: 25083, 24861: 25086, 24892: 25117, 31144: 31369, 49085: 49387,
             49293: 49595, 49460: 49762, 49481: 49783}
for _old, _new in list(FREE_MAP.items()) + list(COUNT_MAP.items()):
    assert map_line(_old) == _new, f"travel114 {_old} -> {map_line(_old)} != {_new}"
assert "clothing-shop265-list" in NEW[7771], "衣櫃重複行上下文唔啱"
assert "gift-shop-list" in NEW[49267], "禮品店重複行上下文唔啱"
DEF_NEW = map_line(45592)   # 45873
WRAP_NEW = map_line(31780)  # 32005
assert DEF_NEW == 45873 and WRAP_NEW == 32005


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
    for old, new, n in [(f"DEF_LINE = 45592", f"DEF_LINE = {DEF_NEW}", 1),
                        (f"WRAPPER_LINE = 31780", f"WRAPPER_LINE = {WRAP_NEW}", 1)]:
        assert src.count(old) == n, f"{path}: {old!r} count={src.count(old)}"
        src = src.replace(old, new)
    lines = src.split("\n")
    lines.insert(0, NOTE)
    write(path, "\n".join(lines))
    print(f"patched {path}")


# ---------- (a) 行為改動：金禧錨點新位（v397 UI397-1：top:24%→calc(24% + 30px)，淨距 ≥8px） ----------
patch("tests/test_ui108_static.py",
      [("ok('S-7 金禧新位 86%/24%（v366）', 'left:86%;top:24%\">金禧大酒店' in html)",
        "ok('S-7 金禧新位 86%/calc(24%+30px)（v397）', 'left:86%;top:calc(24% + 30px)\">金禧大酒店' in html)", 1)],
      "# v397 resync：金禧錨點 top:24%→calc(24% + 30px)（venue99 相疊修正）；見 qa397/resync397.py。")
patch("tests/test_ui128a1_static.py",
      [("'left:86%;top:24%\">金禧大酒店' in html",
        "'left:86%;top:calc(24% + 30px)\">金禧大酒店' in html", 1)],
      "# v397 resync：金禧錨點 top:24%→calc(24% + 30px)（venue99 相疊修正）；見 qa397/resync397.py。")
patch("tests/test_v155_static.py",
      [("ok('B3：會場標籤 HTML／位置（v366：left:86%;top:24%）'",
        "ok('B3：會場標籤 HTML／位置（v397：left:86%;top:calc(24% + 30px)）'", 1),
       ("'<div class=\"md97 md97-venue99\" style=\"left:86%;top:24%\">金禧大酒店</div>'",
        "'<div class=\"md97 md97-venue99\" style=\"left:86%;top:calc(24% + 30px)\">金禧大酒店</div>'", 1)],
      "# v397 resync：金禧錨點 top:24%→calc(24% + 30px)（venue99 相疊修正）；見 qa397/resync397.py。")

# ---------- (a) 行為改動：「還原」搬入行程工具選單（v397 UI397-5） ----------
# B2 鎖定態本身不變（inline-block＋disabled 灰態），只係選擇器由 #nb-actions
# 轉做 #nb-tools397-menu；鎖定態嗰陣成個工具組連 #nb-quick 一齊隱藏
# （33b 回顧預設唯讀收起編輯工具，同一意圖）。
patch("tests/test_buttons197_static.py",
      [("'#nb-actions #btn-reset-plan:disabled{ opacity:.35; cursor:not-allowed; }' in src",
        "'#nb-tools397-menu #btn-reset-plan:disabled{ opacity:.35; cursor:not-allowed; }' in src", 1)],
      "# v397 resync：「還原」搬入行程工具選單（v397 UI397-5），:disabled 選擇器跟新位置；見 qa397/resync397.py。")
patch("tests/test_ui128a6_static.py",
      [("ok('S-20 還原收細做次要掣', '#nb-actions #btn-reset-plan{ min-height:34px;' in html)",
        "ok('S-20 還原收埋入行程工具選單做次要掣（v397）', '#nb-tools397-menu #btn-reset-plan{ background:#fbf3df; border:1px solid #b99b62;' in html and '#nb-actions #btn-reset-plan' not in html)", 1)],
      "# v397 resync：「還原」搬入行程工具選單（v397 UI397-5），S-20 規則跟新位置；見 qa397/resync397.py。")

# ---------- (b) 釘行 ----------
patch("tests/test_rom159_static.py",
      [(f'line_has(27908, "v20a159 ROM159 Phase 1")',
        f'line_has({map_line(27908)}, "v20a159 ROM159 Phase 1")', 1),
       (f'line_has(9338, "rom159GainAllowed(k)")',
        f'line_has({map_line(9338)}, "rom159GainAllowed(k)")', 1),
       (f'line_has(28816, "COMMIT48_NODES.CMT_lan_commit")',
        f'line_has({map_line(28816)}, "COMMIT48_NODES.CMT_lan_commit")', 1),
       (f'line_has(11518, "rom159PrepareNode(node)")',
        f'line_has({map_line(11518)}, "rom159PrepareNode(node)")', 1),
       (f'line_has(16150, "rom159ApplyGiftOverrides()")',
        f'line_has({map_line(16150)}, "rom159ApplyGiftOverrides()")', 1),
       (f'line_has(28671, "function rom159SoMeetGate")',
        f'line_has({map_line(28671)}, "function rom159SoMeetGate")', 1),
       ('"查實" in idx_lines[27935]', f'"查實" in idx_lines[{map_line(27936) - 1}]', 1)],
      "# v397 resync：index.html 淨 +338 行；6 個 line_has 釘行＋全佳行按 difflib 映射重寫（27908→28133、9338→9413、28816→29041、11518→11593、16150→16225、28671→28896、全佳 27936→28161），內容逐字核實純漂移；見 qa397/resync397.py。")
patch("tests/test_rom176_static.py",
      [(f"line(7464).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'",
        f"line({map_line(7464)}).startswith('  lan:{{ id:\"lan\", name:\"藍若曦\"'", 1),
       (f"'GIFT_REACT = giftReact' in line(16148) and 'rom176ApplyGiftOverrides()' in line(16148)",
        f"'GIFT_REACT = giftReact' in line({map_line(16148)}) and 'rom176ApplyGiftOverrides()' in line({map_line(16148)})", 1),
       (f"line(43587).startswith('/* ===== v20a176 ROM176')",
        f"line({map_line(43587)}).startswith('/* ===== v20a176 ROM176')", 1),
       (f"line(43946).startswith('function rom176ApplyGiftOverrides()')",
        f"line({map_line(43946)}).startswith('function rom176ApplyGiftOverrides()')", 1),
       (f"line(45512).startswith('function addLocTalkGiftActs(add, L, npcId)')",
        f"line({map_line(45512)}).startswith('function addLocTalkGiftActs(add, L, npcId)')", 1),
       (f"'rom176TryIntercept(id)' in line(45633)",
        f"'rom176TryIntercept(id)' in line({map_line(45633)})", 1)],
      "# v397 resync：index.html 淨 +338 行；6 個釘行按 difflib 映射重寫（7464→7539、16148→16223、43587→43831、43946→44190、45512→45756、45633→45914），內容逐字核實純漂移；見 qa397/resync397.py。")
patch("tests/test_tang152_static.py",
      [("lines()[16077].startswith('function normaliseTangStub152(pack){')",
        f"lines()[{map_line(16078) - 1}].startswith('function normaliseTangStub152(pack){{')", 1),
       ("lines()[16202].strip().startswith('try{ normaliseTangStub152(rom2);')",
        f"lines()[{map_line(16203) - 1}].strip().startswith('try{{ normaliseTangStub152(rom2);')", 1)],
      "# v397 resync：index.html 淨 +338 行；normaliseTangStub152 兩釘按 difflib 映射重寫（lines()[16077]→[16152]、[16202]→[16277]），內容逐字核實純漂移；見 qa397/resync397.py。")
patch("tests/test_text125_static.py",
      [("if len(ls) < 12098 or FALLBACK not in ls[12097]:",
        f"if len(ls) < {map_line(12098)} or FALLBACK not in ls[{map_line(12098) - 1}]:", 1),
       ("currentLine 第 12098 行冇 text fallback",
        f"currentLine 第 {map_line(12098)} 行冇 text fallback", 1),
       ("if len(ls) < 12240 or FALLBACK not in ls[12239]:",
        f"if len(ls) < {map_line(12240)} or FALLBACK not in ls[{map_line(12240) - 1}]:", 1),
       ("advance 第 12240 行冇 text fallback",
        f"advance 第 {map_line(12240)} 行冇 text fallback", 1),
       ("if len(ls) < 17841 or 'if(typeof b.text === \"string\" && b.text){' not in ls[17840]:",
        f"if len(ls) < {map_line(17841)} or 'if(typeof b.text === \"string\" && b.text){{' not in ls[{map_line(17841) - 1}]:", 1),
       ("applyFamilySafeToNode 第 17841 行冇 b.text 分支",
        f"applyFamilySafeToNode 第 {map_line(17841)} 行冇 b.text 分支", 1)],
      "# v397 resync：index.html 淨 +338 行；三錨點按 difflib 映射重寫（currentLine 12098→12173、advance 12240→12315、applyFamilySafe 17841→17928），內容逐字核實純漂移；報錯字串行號一併更新；見 qa397/resync397.py。")

# ---------- (c) 總行數鏈＋openLoc DEF 鏈 ----------
_TOTAL = [("總行數 50641（", "總行數 50979（", 1),
          ("＋v396 +129）", "＋v396 +129＋v397 +338）", 1),
          ("== 50641)", "== 50979)", 1)]
patch("tests/test_gift185_static.py", _TOTAL, NOTE)
patch("tests/test_tang171_static.py",
      _TOTAL + [("len(lines) >= 45592 and 'function openLoc(id, opts){' in lines[45591]",
                f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1),
               ("＋v396 +103，travel114 釘行）", "＋v396 +103＋v397 +281，travel114 釘行）", 1)],
      NOTE)
patch("tests/test_tang173_static.py",
      [("src.count('\\n') == 50641)", "src.count('\\n') == 50979)", 1),
       ("＋v396 +129）", "＋v396 +129＋v397 +338）", 1),
       ("len(lines) >= 45592 and 'function openLoc(id, opts){' in lines[45591]",
        f"len(lines) >= {DEF_NEW} and 'function openLoc(id, opts){{' in lines[{DEF_NEW - 1}]", 1),
       ("＋v396 +103，travel114 釘行）", "＋v396 +103＋v397 +281，travel114 釘行）", 1),
       ("lines[5269]", f"lines[{map_line(5270) - 1}]", 8)],
      NOTE)
resync_travel114()

# ---------- 跟進：v397 新加兩個 forceRestore 呼叫點 ----------
# 首輪 suite 後 travel114 剩 1 項：rom159OpenDateWhoPicker 新加「返回」掣
# （45835）＋onDismiss（45836）兩個 openLoc(L.id, {forceRestore:true}) 呼叫點
# 未入 FREE_LINES——兩者都係 forceRestore 還原路徑（travel114IsFree 認呢個旗，
# 唔扣出行額度），入 FREE_LINES（42→44）。另有註解行 45810 含 "openLoc(" 字面，
# 誤觸呼叫點普查——註解改寫（唔含括號），唔入 FREE_LINES（唔係呼叫點）。
# 冪等：兩行已在 set 入面就跳過，只核實狀態。
_t = read("tests/test_travel114_static.py")
assert "45835,  # v397 約會揀人 modal「返回」掣（forceRestore，唔再扣額度）" in _t
assert "45836,  # v397 約會揀人 modal onDismiss（forceRestore，唔再扣額度）" in _t
assert len(re.findall(r"^\s*\d+,", re.search(r"FREE_LINES = \{(.*?)\n\}", _t, re.S).group(1), re.M)) == 44
assert 'openLoc(L.id, {forceRestore:true}) 返地點面板' not in read("index.html")
print("follow-up travel114 FREE 42->44 verified")
print("done")
