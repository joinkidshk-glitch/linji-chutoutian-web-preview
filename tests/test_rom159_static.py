# v20a276 resync：index.html 淨 +1 行（#loc-title 米紙圓底 chip 新規則，插入點舊 L4010）；本檔釘行／鏈尾一律 +1，內容逐字核實純漂移。
# v20a272 resync：index.html 淨 +3 行（enterHome setHomeTab 加防禦，插入點新 L20675；其後錨點各 +3，之前唔郁；difflib 對位核實內容逐字相同，純漂移；rebase 上 v271 f25df08 後重做）。
# v20a271 resync：index.html 淨 +91 行（支線第二批：交心旗＋陸頂一晚新機制＋初遇好感差異；插入點舊 L19690–39960；awei195 S4 wrap hook 改一行寫法保 3 行窗）；釘行按 difflib 映射重寫，內容逐字核實純漂移，見 qa271/resync271.py。
# v20a268 resync：index.html 淨 −236 行（WF2 Vera 覆寫 −233／MEET_SOFT −1／SCENE_OVERRIDE154 −1／CONTRA98 R_tang 行 −1）；
# 7 個釘行按 difflib 映射重寫（25431→25195、8480→8246、26265→26029、10950→10716、15050→14814、26180→25944、全佳註解 25459→25223；
# 內容逐字相同，純漂移，見 qa268/resync268.py；ok() 名內歷史行號標籤不變）。
# v20a267 resync：傳聞系統刪除，淨 −1399 行；7 個釘行按內容重對（26135→25431、8623→8480、26969→26265、11171→10950、15495→15050、26884→26180、全佳註解 26163→25459；內容逐字相同，ok() 名內歷史行號標籤不變）。
# v20a266 resync：index.html 淨 +328 行（V158 block ＋284／StoryPlay hook ＋1／載入呼叫 ＋1／enc158 hook ＋42）；釘行按 difflib 映射重寫，內容逐字相同，純漂移。
# v20a265 resync：index.html 淨 +378 行；6 個釘行＋全佳行按 difflib 映射重寫（25499→25849、8020→8339、26333→26683、10553→10886、14877→15210、26248→26598、全佳 25527→25877），內容逐字相同，純漂移；ok() 名入面嘅 L 號係歷史標籤，唔郁。
# v20a139 resync：pristine 改由 git show 846e952（v154 main HEAD，v159 落地前最後一個 main）讀，唔再用 ~/workspace/linji-repo（佢個 main 而家已經係 v159，唔再係 pristine）；反證＋pack 對照不變。
# v20a159 ROM159 Phase 1＋v159 感情線重排 static 測試：紀律釘（SAVE/softRev/?v=、pack JSON 冇直改）
# ＋修復標記在場＋pristine 反證（同一批斷言對 pristine main 乾淨 FAIL，唔 crash）。
# 用法：python3 tests/test_rom159_static.py
# 反證行法：ROM159_PRISTINE=<dir> python3 tests/test_rom159_static.py
#   （<dir> 係一個 v159 之前嘅 index.html 副本；會 FAIL，符合預期）。
# 預設：pristine 由 git show 846e952（v154 main HEAD）讀，唔再用 ~/workspace/linji-repo。
# 注意：行號釘 2026-11-17 重新量度（舊值喺基底已經唔啱——量度值同舊釘差成萬行，
#   舊釘大概係更舊佈局；改動移位要同步更新呢度）。
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
# pristine 來源：環境變數 ROM159_PRISTINE 指定目錄優先；否則由 git 讀 846e952
#（v154 main HEAD，v159 落地前最後一個 main——resident clone 個 main 而家已經係 v159 之後）。
_PRISTINE_COMMIT = "846e952"
_PRISTINE_DIR = os.environ.get("ROM159_PRISTINE")


def _read_pristine_bytes(rel):
    if _PRISTINE_DIR:
        return open(os.path.join(os.path.expanduser(_PRISTINE_DIR), rel), "rb").read()
    r = subprocess.run(["git", "-C", ROOT, "show", _PRISTINE_COMMIT + ":" + rel],
                       capture_output=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError("pristine git show 失敗：" + r.stderr.decode("utf8", "replace").strip())
    return r.stdout


def _read_pristine(rel):
    return _read_pristine_bytes(rel).decode("utf8")
idx = open(os.path.join(ROOT, "index.html"), encoding="utf8").read()
idx_lines = idx.split("\n")
pris = _read_pristine("index.html")
fails = []
skipped = []
total = [0]


def ok(name, cond):
    total[0] += 1
    if not cond:
        fails.append(name)


def skip(name):
    skipped.append(name)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# 紀律：SAVE key / softRev / ?v= 不變
ok("SAVE key", "starVolunteer_map_v19w" in idx)
ok("softRev s107", '"s107"' in idx or "'s107'" in idx or "s107" in idx)
ok("?v= v20a10", "v20a10" in idx)

# ROM159 標記在場（work）
markers = [
    "v20a159 ROM159 Phase 1",
    "const ROM159_LOCK_REL = 5",
    "const ROM159_ENC_CAP = 3",
    "const ROM159_DATE_PER_WEEK = 1",
    "const ROM159_WOMEN = {",
    "const ROM159_DATES = {",
    "const ROM159_XU_PRICES = { ad_central:150, ad_adm:140, film_cotton:120, rec_star:100, cafe_cha:35 }",
    "const ROM159_GIFT_OVERRIDES = {",
    "function rom159RelKeyWho(",
    "function rom159EnsureLock(",
    "function rom159LockedWho(",
    "function rom159SetLock(",
    "function rom159GainAllowed(",
    "function rom159CheckLock(",
    "function rom159FlushNotices(",
    "function rom159GiftBlocked(",
    "function rom159ApplyGiftOverrides(",
    "function rom159TalkCapped(",
    "function rom159RecordTalk(",
    "function rom159DateGate(",
    "function rom159OpenDatePicker(",
    "function rom159TodayConflict(",
    "function rom159ConfirmDate(",
    "function rom159RunDate(",
    "function rom159DateScene(",
    "function rom159PeopleHtml(",
    "function rom159PrepareNode(",
    "function rom159SoMeetGate(",
    "COMMIT48_NODES.CMT_lan_commit = {",
    "COMMIT48_NODES.CMT_xu_commit = {",
    "COMMIT48_NODES.CMT_yip_commit = {",
    "COMMIT48_NODES.CMT_so_commit = {",
    "COMMIT48_DEFS.CMT_lan_commit = {",
    "COMMIT48_DEFS.CMT_xu_commit = {",
    "COMMIT48_DEFS.CMT_yip_commit = {",
    "COMMIT48_DEFS.CMT_so_commit = {",
    "get(\"story_detail_romance_yip_so.json\")",
    "STORY_WIRE.romance.yipSo = rom3",
    "rom159PrepareNode(node)",
    "rom159ApplyGiftOverrides()",
    "rom159TalkButtons(npcId, L)",
    "rom159PeopleHtml()",
    "rom159OpenDatePicker(rk, L)",
    "rom159OpenDatePicker(who, null)",
    "rom159FlushNotices()",
    "rom159DateButtonInfo(rk)",
]
for m in markers:
    ok("標記在場: " + m, m in idx)

# Vera 感情線已出局：CMT 定義唔可以再有佢（註解提到舊名唔計，只驗 code 定義）
ok("CMT_vera 已刪", "COMMIT48_NODES.CMT_vera_commit" not in idx and "COMMIT48_DEFS.CMT_vera_commit" not in idx)
ok("WOMEN 冇 vera", '"vera"' not in idx.split("const ROM159_WOMEN")[1].split("};")[0] if "const ROM159_WOMEN" in idx else False)
ok("WOMEN 冇 mei", '"mei"' not in idx.split("const ROM159_WOMEN")[1].split("};")[0] if "const ROM159_WOMEN" in idx else False)
_rom176_block = idx.split("const ROM176_WOMEN")[1].split("];")[0] if "const ROM176_WOMEN" in idx else ""
ok("ROM176_WOMEN 冇 vera／mei", 'key:"vera"' not in _rom176_block and 'key:"mei"' not in _rom176_block)

# 接線點：bumpRel 凍結鉤＋commit 閘鎖條件＋送禮分層＋送禮拒收
ok("bumpRel 凍結鉤", 'if(typeof rom159GainAllowed==="function" && !rom159GainAllowed(k))' in idx)
ok("bumpRel 鎖觸發鉤", 'if(typeof rom159CheckLock==="function") rom159CheckLock(k, next);' in idx)
ok("commit48Available 鎖條件", "rom159LockedWho()" in idx and "只可以 commit 鎖定嗰位" in idx)
ok("prefKind 最愛分層", 'if((pref.favorites||[]).indexOf(itemId)>=0) return "favorite";' in idx)
ok("calcDelta 最愛 +2", '(kind==="liked" || kind==="favorite") ? (Number(dr.liked)||2)' in idx)  # v20a183 B2：最愛同喜歡同數，舊斷言字面已過時
ok("canGive 鎖拒收", "rom159GiftBlocked(npcKey)" in idx)
ok("送禮標籤最愛", 'kind==="favorite"?"★ 最愛"' in idx)  # ★ 號後加，舊斷言字面已過時
ok("手帳 Call 機掣", 'class="rom159-call"' in idx)
ok("撞期 shoot 偵測", 'slot.indexOf("shoot:")===0' in idx)
ok("撞期 job 試鏡偵測", 'slot.indexOf("job:")===0' in idx)
ok("采兒公開／低調拆分", "C_choi_ending_he_public" in idx and "C_choi_ending_he_quiet" in idx)
ok("采兒公開 fame 代價", '"flag_choi_public"' in idx)
ok("蘇層級閘接 rom176BeatOpen", 'if(key==="so" && typeof rom159SoMeetGate==="function"' in idx)
ok("蘇層級閘接 rom159PrepareNode", 'node.id==="R_so_meet"' in idx and "R_so_meet_gate" in idx)
ok("鏈 D yip_choice 有 R_yip_push1 guard", 'StoryOC.isDone("R_yip_push1")' in idx)
ok("ending commit 分支六人", 'rom.lan.committed' in idx and 'rom.yip.committed' in idx and 'rom.so.committed' in idx)

# 行號釘（靜態寫死；2026-11-17 整合重測：B1＋B2 cherry-pick 後移位，改動移位要同步更新呢度）
# v20a158 resync：釘行各 ＋15（插入點全部喺釘行之前：gigCardHtml＋4／詳情頁＋11；GRANT229_ENC79 喺釘行之後，唔計）；difflib 對位核實內容逐字相同，純漂移。
def line_has(n, frag):
    return 1 <= n <= len(idx_lines) and frag in idx_lines[n - 1]

ok("行號釘 ROM159 block 頭 25499", line_has(25202, "v20a159 ROM159 Phase 1"))
ok("行號釘 bumpRel 凍結鉤 8020", line_has(8247, "rom159GainAllowed(k)"))
ok("行號釘 CMT_lan_commit 26333", line_has(26036, "COMMIT48_NODES.CMT_lan_commit"))
ok("行號釘 StoryPlay 預備鉤 10553", line_has(10717, "rom159PrepareNode(node)"))
ok("行號釘載入覆寫呼叫 14877", line_has(14815, "rom159ApplyGiftOverrides()"))
ok("行號釘 rom159SoMeetGate 26248", line_has(25951, "function rom159SoMeetGate"))

# costsDay:true 殘留已拎走（code 值；註解提到舊值唔計）
ok("giveGift 回傳冇 costsDay:true", "before, after, costsDay:true" not in idx)
ok("全檔冇 after, costsDay:true", "after, costsDay:true" not in idx)

# 「全佳 7 分」查實：code 入面從來冇「全佳」閘門——唯一一次出現係 ROM159 註解嘅查實說明
ok("全佳只出現喺 ROM159 查實註解", idx.count("全佳") == 1 and "查實" in idx_lines[25230 - 1])  # v20a159 整合：B1＋B2 後行號 +86
ok("rel 上限 7 校準說明在場", "理論最高 7" in idx)

# ROM159_WOMEN：最終六人，37 場（spots 順序照任務表）
_m = re.search(r"const ROM159_WOMEN = \{(.*?)\n\};", idx, re.S)
_women = _m.group(1) if _m else ""
_keys = re.findall(r"^\s*(\w+):\s*\{", _women, re.M)
ok("WOMEN 六人", _keys == ["hiu", "choi", "lan", "xu", "yip", "so"])
_spots = re.findall(r"spots:\[([^\]]*)\]", _women)
_spot_lists = [[s.strip().strip('"') for s in grp.split(",") if s.strip()] for grp in _spots]
ok("WOMEN spots 總數 37", sum(len(x) for x in _spot_lists) == 37)
ok("WOMEN hiu 7 場", len(_spot_lists[0]) == 7 if len(_spot_lists) > 0 else False)
ok("WOMEN choi 5 場", len(_spot_lists[1]) == 5 if len(_spot_lists) > 1 else False)
ok("WOMEN lan 6 場", len(_spot_lists[2]) == 6 if len(_spot_lists) > 2 else False)
ok("WOMEN xu 7 場", len(_spot_lists[3]) == 7 if len(_spot_lists) > 3 else False)
ok("WOMEN yip 6 場", len(_spot_lists[4]) == 6 if len(_spot_lists) > 4 else False)
ok("WOMEN so 6 場", len(_spot_lists[5]) == 6 if len(_spot_lists) > 5 else False)
ok("WOMEN yip／so npcId null", '"yip"' in _women and "yip" in _women and _women.count("npcId:null") >= 2)
_flat_spots = [s for grp in _spot_lists for s in grp]
ok("WOMEN spots 無重複", len(_flat_spots) == len(set(_flat_spots)))

# 約會價錢定值表（B1 工人同一張）：散步類 $4、海傍／山頂／淺水灣／啟德 $6、廟街 $20、
# 茶記 $45、戲院／首映 $58、酒廊唱歌 $50（酒廊係推算，NOTES 標明待確認）。
# DATES 係 B1 範圍——呢個分支未齊 37 場嗰陣成段 skip，唔紅；齊晒先驗終態。
_dates_m = re.search(r"const ROM159_DATES = \{(.*?)\n\};", idx, re.S)
_dates_body = _dates_m.group(1) if _dates_m else ""
_costs = {k: int(v) for k, v in re.findall(r"^\s*(\w+):\s*\{[^}]*?cost:(\d+)", _dates_body, re.M)}  # v20a159 整合：findall 回字串，轉 int 先同定值表比
_SUFFIX_PRICE = {"harbour": 6, "beach": 6, "airport": 6, "peak": 6,
                 "market": 20, "cafe": 45, "cinema": 58, "premiere": 58, "lounge": 50}
_ALLOWED = {4, 6, 20, 45, 58, 50}
_missing = [s for s in _flat_spots if s not in _costs]
if not _flat_spots or _missing:
    skip("約會價錢表：DATES 未齊 37 場（欠 %d 場），合併 B1 之後先驗" % len(_missing))
else:
    for s in _flat_spots:
        suf = s.split("_", 1)[1] if "_" in s else s
        if suf in _SUFFIX_PRICE:
            ok("約會價錢 %s $%d" % (s, _SUFFIX_PRICE[suf]), _costs.get(s) == _SUFFIX_PRICE[suf])
    ok("約會價錢全部喺定值表入面", all(int(c) in _ALLOWED for c in _costs.values()))

# 藍 crisis 重寫（針對性斷言；lan_xu pack 已改，唔再入下面 sha 清單）
_lanxu = json.load(open(os.path.join(ROOT, "content", "story_detail_romance_lan_xu.json"), encoding="utf8"))
_crisis = [n for n in _lanxu["nodes"] if n["id"] == "R_lan_crisis"]
ok("藍 crisis 搵到唯一節點", len(_crisis) == 1)
if _crisis:
    _c = _crisis[0]
    _blob = json.dumps(_c, ensure_ascii=False)
    ok("藍 crisis 無 flag_family_marriage", "flag_family_marriage" not in _blob)
    ok("藍 crisis 無豪門／聯姻字眼", "豪門" not in _blob and "聯姻" not in _blob)
    ok("藍 crisis 有阿爸壓力", "阿爸" in _blob)
    ok("藍 crisis flags_written 已同步", _c.get("flags_written") == ["flag_family_help", "flag_lan_help", "flag_lan_stepback"])
    ok("藍 crisis 抉擇 id 不變", [ch["id"] for ch in _c["choices"]] == ["C_lan_crisis_help", "C_lan_crisis_stepback"])
    ok("藍 crisis help rel+2／fame-1 不變",
       _c["choices"][0]["effects"]["stats"] == {"rel_lan": 2, "fame": -1})

# pack JSON 冇直改（同 pristine main 逐檔 sha 對照；lan_xu 已改唔入清單，見上面針對性斷言；
# v20a268：vera_hiu_choi.json＋romance_tang.json 唔入清單——vera 檔已減 5 個 R_vera_* 節點，tang 檔已刪；見下面精確替代斷言）
packs = [
    "content/story_detail_n1_to_n17.json",
    "content/story_detail_rival_mentor.json",
    "content/gift_prefs.json",
    "content/gift_react_copy.json",
    "content/items_gifts.json",
    "content/shops.json",
    "content/cast_main.json",
]
for p in packs:
    ok("pack 冇直改: " + p, sha(os.path.join(ROOT, p)) == hashlib.sha256(_read_pristine_bytes(p)).hexdigest())

# v20a268 精確替代斷言：vera_hiu_choi.json ＝ pristine 版減 5 個 R_vera_* 節點（metadata 清零另行講明）；tang 檔唔存在
_vhc_now = json.load(open(os.path.join(ROOT, "content", "story_detail_romance_vera_hiu_choi.json"), encoding="utf8"))
_vhc_pris = json.loads(_read_pristine("content/story_detail_romance_vera_hiu_choi.json"))
_vhc_now_ids = [n["id"] for n in _vhc_now.get("nodes", [])]
_vhc_pris_ids = [n["id"] for n in _vhc_pris.get("nodes", [])]
ok("v268 vera_hiu_choi：nodes 15→10（hiu／choi 各 5 條留返）",
   len(_vhc_now_ids) == 10 and len(_vhc_pris_ids) == 15
   and _vhc_now_ids == [i for i in _vhc_pris_ids if not i.startswith("R_vera_")])
ok("v268 vera_hiu_choi：檔內 vera／Vera 零殘留",
   "vera" not in json.dumps(_vhc_now, ensure_ascii=False).lower())
ok("v268 vera_hiu_choi：metadata version 1.3.2", _vhc_now.get("version") == "1.3.2")
ok("v268 romance_tang.json 檔已刪", not os.path.exists(os.path.join(ROOT, "content", "story_detail_romance_tang.json")))

# ---- pristine 反證：同一批標記對 pristine main 應該全部唔存在（乾淨 FAIL，唔 crash） ----
pris_missing = [m for m in markers if m in pris]
ok("反證 pristine 冇 ROM159 標記", not pris_missing)
ok("反證 pristine 冇 CMT_vera", "COMMIT48_NODES.CMT_vera_commit" not in pris)
ok("反證 pristine commit 閘冇鎖條件", "只可以 commit 鎖定嗰位" not in pris)
# costsDay 反證已失效：main 早已拎走 costsDay（唔係 Phase 1 先拎），唔再斷言。
# 最愛分層反證已失效：pref.favorites 係 ROM176 星層（v176，已入 main），唔係 ROM159 獨有，唔再斷言。

print("ROM159 static: %d checks, %d FAIL, %d SKIP" % (total[0], len(fails), len(skipped)))
for s in skipped:
    print("SKIP: " + s)
if fails:
    for f in fails:
        print("FAIL: " + f)
    sys.exit(1)
print("PASS")
