# v20a136 結局閘搬去 1992 年 12 月 — 靜態鎖
#   閘欄位／評估器分支／文案（N17＋N16＋N12/N13/N14/N15＋提示表＋CHOICE47）／
#   邀請 modal 無「稍後」／G1 還原／gallery 桶／pack N17 唔郁。
# 反證：對 pristine main（未改）跑，必須 FAIL（唔係 crash）。
# 用法：python3 tests/test_gate136_static.py [path-to-index.html]
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "index.html")
src = open(HTML, encoding="utf-8").read()
fails = []
def ok(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)
def block(start_marker, end_marker):
    # marker 唔見就返空字串，等斷言 FAIL，唔好 raise（反證要乾淨 FAIL 唔 crash）。
    if start_marker not in src or end_marker not in src:
        return ""
    i = src.index(start_marker)
    j = src.index(end_marker, i)
    return src[i:j]
def strip_comments(s):
    return re.sub(r"/\*.*?\*/", "", s, flags=re.S)

# ---- A. 閘＋評估器 ----
gm = re.search(r"const STORY_GATE_3Y = \{(.*?)\n\};", src, re.S)
gate = gm.group(1) if gm else ""
ok("N17 閘有 weekMin: 153", "weekMin: 153" in gate)
ok("N17 閘有 awardResolved（award_singho_tv／1992）",
   'awardResolved: { ceremonyId: "award_singho_tv", year: 1992 }' in gate)
ok("N17 閘有 backstopDay: 1096", "backstopDay: 1096" in gate)
ev = block("function evalGate3Y(nodeOrId, opts)", "function rivalGao_onlyC3ChoiceFlags")
ok("evalGate3Y 有 backstopDay 早返（繞過全部條件）",
   "backstopDay" in ev and "backstopDay:" in ev)
ok("evalGate3Y 有 awardResolved 檢查（done／skipped 先計）",
   "awardResolved" in ev and '"done" || st==="skipped"' in ev)
ok("awardResolved 檢查 defensive（try/catch）", "awardResolved" in ev and "catch(_e)" in ev)
ok("awardResolved／backstopDay 冇撞名（閘表內各出現一次）",
   len(re.findall(r"awardResolved\s*:", gate)) == 1 and len(re.findall(r"backstopDay\s*:", gate)) == 1)
ok("進度頁 awardResolved 有玩家文案（唔漏工程術語）",
   "等冬台慶有結果" in src and "awardResolved" in block("function prog71GateItems", "function prog71StubItems"))

# ---- B. 評核 ----
ok("CONSEQ61_REVIEWS 有 1992 條目（155／195／156）",
   "1992: { floor: 155, warnLine: 195, boundaryWeek: 156 }" in src)

# ---- C. 文案 ----
# 語義關鍵（v20a136 實駕捉到）：JSON pack 主線節點／STORY_HINT_SOFT／CHOICE47_NODES
# 全部經 years66Walk 載入 +2（源頭寫舊曆 1990 → 玩家面顯示 1992）。
# 所以呢啲來源入面玩家面年份字串源頭必須係 1990，「1992」出現即係顯示 1994（錯）。
# v20a234：內嵌覆寫表已刪，N17／N12–N16 來源由內嵌表改做 JSON pack（同一批舊曆值，逐字同步）；
# pack 主線節點經 refreshCopyPacksFromDisk 嘅 [main, rom1, rom2, rival, ...] walk（L18562 一帶）。
# 唔經 walk 嘅 code 字串（結局總結 fallback、endingEveOptions410 note、閘表）先至直接寫 1992。
pack = json.load(open(os.path.join(ROOT, "content", "story_detail_n1_to_n17.json"), encoding="utf-8"))
pack_nodes = {n.get("id"): n for n in (pack.get("nodes") or [])}
c17 = json.dumps(pack_nodes.get("N17"), ensure_ascii=False)
ok("N17 節點「頒獎禮前夕」只剩對白否定句（v157：何生「唔係頒獎禮前夕——獎已經頒完」；舊 synopsis 第2段 DEV 註解已刪）",
   c17.count("頒獎禮前夕") == 1 and "唔係頒獎禮前夕" in c17)
ok("N17 節點玩家面年份係舊曆 1990（walk +2 → 顯示 1992），無「1992」",
   "1990" in c17 and "1992" not in c17)
ok("N17 節點係 1990 冬（源頭）＋台慶之後＋散場（v157：場景改會議室，台慶之後＝冬台慶啱啱完）",
   '"1990冬"' in c17 and "era_1990_winter_finale" in c17 and "冬台慶剛剛完" in c17
   and "台慶之後，何生在星河電視台會議室等你" in c17 and "頒獎禮散場" in c17)
ok("N17 節點無「試咪／開場之前」", "試咪" not in c17 and "開場之前" not in c17)
ok("N17 節點經 years66Walk（1990 源頭先會顯示 1992）：pack main 喺載入 walk 清單",
   "[main, rom1, rom2, rival, gateStub, dengMock, dengPushMock, dualMock].forEach" in src
   and "years66Walk(p, null)" in src)
ok("N17 pacing.weekMin＝153（章戳約第153週）", (pack_nodes.get("N17", {}).get("pacing") or {}).get("weekMin") == 153)
ok("結局總結 fallback 改做台慶之後嗰晚（唔經 walk，源頭寫 1992）",
   "台慶之後嗰晚，先係埋單嗰陣" in src and "頒獎禮前夕嗰晚，先係埋單嗰陣" not in src)
ok("動態重建選項 note 係散場（endingEveOptions410，唔經 walk）",
   "頒獎禮散場，他站回他站慣的那個位置。" in src)  # v233 RW-2：第二人稱廣東話→第三人稱書面語，「散場」事實不變
ok("全檔無「頒獎禮開場」", "頒獎禮開場" not in src)
n1990 = json.dumps([pack_nodes.get(k) for k in ("N12", "N13", "N14", "N15", "N16")], ensure_ascii=False)
ok("pack N12/N13/N14/N15/N16 玩家面年份係舊曆 1990，無「1992」",
   "1990" in n1990 and "1992" not in n1990)
ok("N16 節點係 1990 冬（源頭）＋era_1990_winter_newyear",
   '"1990冬"' in n1990 and "era_1990_winter_newyear" in n1990)
for cid, season in [("N12", "春"), ("N13", "夏"), ("N14", "秋"), ("N15", "秋末"), ("N16", "冬")]:
    m = re.search(r"^  " + cid + r": \{ playerHint:.*$", src, re.M)
    ok("提示表 %s 行玩家面年份係舊曆 1990，無 1992" % cid, bool(m) and "1990" in m.group(0) and "1992" not in m.group(0))
m17 = re.search(r"^  N17: \{ playerHint:.*$", src, re.M)
ok("提示表 N17 行係台慶之後＋1990 年冬（源頭）",
   bool(m17) and "台慶之後" in m17.group(0) and "1990 年冬" in m17.group(0) and "1992" not in m17.group(0))
f4 = block('F4_stay_mind: {', 'G4_family_job: {')
g4 = block('G4_family_job: {', '};\nconst CHOICE47_DEFS')
ok("CHOICE47 F4 玩家面年份係舊曆 1990（1990 秋）", "1992" not in f4 and "1990秋起" in f4 and "1990 年秋" in f4)
ok("CHOICE47 G4 玩家面年份係舊曆 1990（1990 冬）", "1992" not in g4 and "1990冬起" in g4 and "1990 年年尾" in g4)

# ---- D. 邀請流程 ----
inv = block("function presentAwardInvite(pack, thenFn)", "function presentPendingAward")
ok("邀請 modal 無「稍後」掣", "稍後" not in inv)
ok("邀請 modal 只有出席＋推辭", '"出席"' in inv and '"推辭"' in inv)
ok("邀請 dismiss 即推辭（onDismiss: skip）", "onDismiss: skip" in inv)
ok("全檔無 _awardSnoozed／_awardSnoozeDay 死碼", "_awardSnooz" not in src and "_awardSnoozeDay" not in src)
ok("推辭會入報紙（skip 呼叫 enqueueNewspaperFromAward）",
   "enqueueNewspaperFromAward" in inv and "declined:true" in inv)
ok("G1 還原函數在位＋queue 嗰陣呼叫",
   "function restorePendingAward136()" in src
   and "restorePendingAward136();" in block("function queueAwardsOnSeasonWindow", "function renderAwardInviteHtml"))
ok("pending pack 持久化（S.pendingAwardPack 寫入＋清走）",
   "S.pendingAwardPack = pack" in src and "S.pendingAwardPack = null" in src)
gal = block("const NEWSPAPER_AWARD_GALLERY_TEMPLATES_136", "function enqueueNewspaperFromAward")
ok("gallery 報紙模板 4 隻（film／tv／music／ad）",
   all(m in gal for m in ["award_gallery.film", "award_gallery.tv", "award_gallery.music", "award_gallery.ad"]))
ok("gallery 模板唔寫入圍／提名／得獎", not re.search(r"入圍|提名|得獎", gal))
ok("enqueueNewspaperFromAward 有 gallery 桶＋declined 路徑",
   '"award_gallery"' in src and "opts.declined" in src)

# ---- Pack 唔郁 ----
pack = json.load(open(os.path.join(ROOT, "content", "story_detail_n1_to_n17.json"), encoding="utf-8"))
nodes = pack.get("nodes") or pack.get("story") or []
c17p = None
for n in (nodes if isinstance(nodes, list) else []):
    if isinstance(n, dict) and n.get("id") == "N17":
        c17p = n
        break
if c17p is None and isinstance(pack, dict):
    c17p = (pack.get("N17") or {})
# v233 RW-2：JSON N17 已按內嵌表正本同步（取代死 pack 節點）——when 由舊 pack「1992收束 / W105-108」改做內嵌正本「1990冬」（舊曆，載入 +2 變 1992 冬），pacing.weekMin 由 105 改做 153（同內嵌 N17／STORY_GATE_3Y 一致），prevMain 由 N15 改做 N16。斷言跟正本，唔再釘死 pack 舊值。
ok("pack N17 when／pacing 跟內嵌正本（1990冬／weekMin 153／prevMain N16）",
   c17p is not None and "1990冬" in str(c17p.get("when", "")) and (c17p.get("pacing") or {}).get("weekMin") == 153 and (c17p.get("pacing") or {}).get("prevMain") == "N16")

if fails:
    print("FAILURES: " + " | ".join(fails))
    sys.exit(1)
print("ALL PASS (gate136 static)")
