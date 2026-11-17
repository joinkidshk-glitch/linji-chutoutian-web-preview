# NOTES_V20A254 — 主線實裝收尾批（統籌記錄）

- 基線 main `f8e486a`（v256）；分支 `v20a254`；工作副本 `linji-work254`（clone 式，origin＝常駐 clone 本地路徑）。
- 範圍：`linji-main-phase3/INVENTORY.md` 分批計劃「收尾批」（文件寫 v253，編號順延一格即 v254）＋ `linji-favor-audit/FAVOR_AUDIT.md` ＋ `linji-favor-table-workorder.md`。兩份文件都舊（INVENTORY 基線 v248、FAVOR_AUDIT 基線 v206），行號／總數／結論全部對 live 重核，唔信原文。
- 工人：A 通告／BR89、 B 主線 JSON／引文、 C index.html 機制／死碼／農場洞；三人全部完成，統籌抽查核實＋整合。
- 唔改：SAVE key、softRev `s107`、產品 `?v=` `v20a10`；`gigs_new.json` 282 張零改動；romance／rival JSON 零改動；結局計數口徑唔改；唔成個刪人情系統。
- 實機驗證押後（瀏覽器死，2026-11-15 起）。

## A — 人情兌現（BR89＋F1）

BR89_PATRON_OF_GIG 13 對，全部 REUSE 新庫，0 張新開（`content/gigs_new.json` 0 改動，282 張不變；舊 code-side 4 張 `gig_br89_*` 新庫 0 命中，已刪）：

| 債權人 | 債權 id | 新庫 gig | 作品 |
|---|---|---|---|
| 陸柏言 | credit_enc83_luk_patron | gig_1991_film_101 | 《江河歲月》 |
| 彭少祺 | credit_enc84_pang_patron | gig_1991_variety_203 | 《台慶大騷》 |
| 程天諾 | credit_enc84_ching_patron | gig_1992_rec_106 | 《夜場匯演》 |
| 廖炳星（優先） | credit_enc79_liu_priority | gig_1991_film_103 | 《笑住過肥年・外傳》 |
| 廖炳星（引薦） | credit_enc83_liu_patron | gig_1992_film_103 | 《吉星笑哈哈》 |
| 麥震東 | credit_enc83_mak_patron | gig_1991_film_110 | 《鐵拳王》 |
| 葉敏芝 | credit_enc83_yip_patron | gig_1992_tv_105 | 《摩登一家人》 |
| 顧明輝 | credit_enc83_gu_patron | gig_1992_rec_105 | 《當年情懷》 |
| 蘇芷茵 | credit_enc84_so_patron | gig_1991_ad_102 | 《秀髮如瀑》 |
| 鍾楚凝 | credit_enc84_chung_patron | gig_1991_tv_108 | 《深秋情緣》 |
| 駱家聲 | credit_enc83_lok_patron | gig_1992_rec_102 | 《硬漢柔情》 |
| 魏詠男 | credit_enc83_ngai_patron | gig_1991_film_111 | 《雪山雙劍傳》 |
| 齊鎮海 | credit_enc83_chai_patron | gig_1992_tv_104 | 《滬上往事》 |

- 統籌獨立抽查：13 個 gig id 全部在庫，trigger.creditId 同映射債權逐對啱，creditOwner 啱星名。R-4 雙觸發硬編碼由舊 `gig_1991_rec_102`（新庫已改做無 trigger 嘅《鄉謠》）搬去 `gig_1992_rec_105`，還錢路重新接通。
- F1 幫忙通告（D3 補）已恢復：**恢復 v20a17 原裝 special gig 接線，唔入庫存**（新庫版幫忙通告無 trigger kind 可接，入庫會郁 282 張計數／六批驗證）。`gig_favor_ho_errand`《晨光劇場》臨時人手、事務所板、`payExact: 500`、`pay: [450, 550]`、1 日工、4 日窗不變；tier 舊「初」→新五級「臨記」、補 `category: "臨記通告"`、刪死 data `favorDelta`、唔寫 `era_*` id。`FAVOR_DUE_CFG gigId` 填返、`FAVOR_DUE_GIGS` 恢復。新測試 `tests/test_br89_favor_due.js` 26 項全過（到期叫數→上板、做完清債＋何生 rel +2、過期作廢唔計 settled＋rel −3、到期前現金還款兜底）。**留意**：$500 定額高過 SPEC §7.1 庫存臨記帶（$250–400），保留原裝；要跟 §7.1 改 pay 係一行，見「要拍板」。
- 驗證（唔重做）：F2 未兌現（`debt_c4_ho_ripple` 真入帳可還，無到期循環／叫數場面）；F3 部分兌現（「捱得」tag 真入 `S.castingTags`，無指定動作組優先通告）；F6／F7／F8 未兌現（`choi_spin` 零 gameplay 讀者；昌叔／根叔旗只喺結局頁回望文案讀，無跟進通告）。credits 三筆通過：c7→`gig_1991_tv_204`《通宵追捕》、c9→`gig_1991_film_108`《月夜酒廊》、c15→`gig_1992_film_203`《江湖復仇》。`credit_c13_newyear` 通過（結局頁兌現喺位，標 `redeemedBy="ending_c13_newyear"`）。
- 偏離：① A 嘅 index.html 改動淨 +61 行，令 5 個行數漂移測試 FAIL（gift185／rom176／tang171／tang173／travel114），按慣例機械 resync 咗 5 檔（逐支釘核實啱位先改）。② 廖炳星引薦有兩張新庫 gig（`gig_1991_film_109`＋`gig_1992_film_103`），表只取後者做 canonical；先殺青前者嗰陣殺青鉤唔標 `redeemedBy`（同 c7／c9／c15 一樣嘅通用-credit 限制，靠 `done_` 旗落板），留另票統一。③ 工作記錄 `NOTES_V20A254_BR89_FAVOR.md` 在工作副本內。

## B — 標題／年份／引文對齊（主線 JSON）

- 對齊：全部已啱，JSON 淨改 1 行：21 個新標題全部已在 JSON（N6F 同 N6 一樣係「角落那張枱」）；`when` 全部 source 舊曆無手改 +2；N5 `when: 1988秋 / W36`＋`week_min: 36`＋note「秋|冬；禁夏台慶開主線」＋stub `seasonAny:[autumn,winter]`＋攻略 ch-meta「約第 36 週起」——D10 秋，四方一致；F4 DEFS `year:1992, season:秋`，node `when:"1990秋起"`，顯示 1992 秋（D6）；N14 `when: 1990春末`（D5）；N12 note 已係「（動作標籤＋1992 春）」（v251 改咗）；N19 artId 已係 `story_c19`（v251 補咗）。
- 唯一 JSON 改動（B）：N1 beats[3].lines[0] 何生對白，live 係書面語（RW-2 誤改對白），同一 beat 下一句即係廣東話；施工單 L62＋攻略兩邊都係廣東話版，語言規則話對白留廣東話——改返廣東話版。12 個相關 story 測試全 PASS，唔使重算 hash（`nodes[5:]` 一字未郁）。
- 全量引文重對（B）：攻略來源釐清——`~/workspace/linji-story-guide/index.html` 係 2026-11-14 舊快照（唔用）；用咗最新本地快照 `space-versions/.../v101/tree/index.html`（＝live，`live` 指向 v101，建於 2026-11-17 06:15 HKT）。方法：抽每章 `<blockquote>` 每行＋choice label＋outcome 格內引文，對 live JSON＋CHOICE47 逐段比。**總數 629 段**：DRAFT 設計草稿 158（明言未實裝，唔計分）＋ARTIFACT 非引文 16＋**非草稿引文 455 段：EXACT 237、NEAR／SUB 60、MISS 158**——啱 297 段（65.3%），唔啱 158 段（34.7%）。158 MISS 入面 154 段係同一成因：RW-2 旁白漂移（攻略引舊廣東話旁白，live 係書面語）；真正對白出入只得 3 段 MISS（N6 昌叔句攻略多咗一句；N17 兩句 v235 改寫後攻略仲係舊「揀路」版）＋8 段 NEAR／SUB 對白。逐段對照表喺工作副本 `QUOTE_RECHECK_V254.md`（untracked，275 行，唔 commit）。攻略側改動由 parent 經 artifact 做，唔喺工人範圍。
- D9：N6F 已搬入 JSON（v250，8 beats／13 行／2 抉擇）；F4／G4 照 D9.2 留 `CHOICE47_NODES`，無郁。
- `nodeRipple` 核實（B）：INVENTORY K9 話「七章全部 null」係舊／唔準。Live：**N1–N5 有值（5 個），其餘 17 個節點全部 null**（C 已清零，見下）。
- 新發現（B，見「要拍板」）：① **N4 季節張力**：JSON `when: 1988春 / W8-9`，但 beats[0]＋施工單 §4＋攻略 scene cap 三邊都係「夏」（live `1988年夏…`）；攻略同一章「遊戲原文」blockquote 反而寫「1990 年春」——攻略側手民之誤。邊邊為準要定，B 無改。② **`coverage.count: 21` vs 22 節點**：`coverage.have` 列 21 章，N17_epi（v253 加嘅 4 拍湯場尾聲）唔喺入面（C 已補，見下）。③ **N6F `artId: null`**：D9.1 話跟 N18／N19 前例，但 N19 而家已有 `story_c19`，理據半過時；無對應 asset，唔捏造；等場面圖批定。④ **`STORY_TITLE_SOFT`（index.html）11 處同 JSON 新標題唔一致**（C 已處理，見下）。

## C — 機制／死碼／農場洞（index.html）

- **SOFT 對齊**：核實 SOFT 唔係純 fallback——`storyMainProgressLine`、`prog71Title`（進度頁）、`playerReasonFrom`（「先完成上一幕〈…〉」）、`markDone` 週 highlight 都係 **SOFT 優先於 node.title** 顯示；`storyHintPack.mapTipTitle` 同首頁提示就係 node.title 優先、SOFT 只做後備。所以 SOFT 值係會當標題顯示，唔對齊就會半遮新標題（v20a253 註解本身都承認）。C 改咗 N7–N12（暴雨救場→暴雨、選美後台→化妝間、茶餐廳度橋→卡座、年尾追數→酒廊、戲路定型→黑西裝與舊風褸、高危替身→墊）；N13–N17 本來已啱。測試同步：`test_weave46_static.py`（5 項）、`test_weave48_static.py`（N12 一項）、`test_progress71_logic.js` B3 mock＋斷言。
- **`nodeRipple` 清理**：`.nodeRipple` 屬性讀取全 repo **0 處**（index.html 0 處——v20a222 已刪 code 側讀者；tests 0 處）。剩低嘅只係 data：JSON 5 個有值＋17 個 null、測試 fixture `behavior_gate_n1_n5.json` 5 個值、tang171／173 註解提及 v20a222 刪除。支線交接靠 `flags_written`＋synopsis（index.html 內 `flags_written` 讀者多處在位），唔靠 nodeRipple，符合 INVENTORY 講法。已做：JSON N1–N5 五個值 → `null`（同其餘 17 個一致，唔刪 key）；fixture 同樣 5 個 → `null`。唔使 hash resync（`test_story157_pack_static.py` 只 hash `nodes[5:]`，N1–N5 唔喺入面）。
- **死碼清理（逐項驗證）**：
  - (a) `favorDelta` — 已刪最後一處 live 出現：`nat92Gig()` `favorDelta: []` 空陣列預設值（`.favorDelta` 讀者全 repo 0 處；`content/gigs_new.json` 0 處、story JSON 0 處；A 恢復嘅 FAVOR_DUE gig 本身已無此欄）。`gigs_new.json` 零郁、設計庫 `regen-v2/gigs_new_v2.json` 本身都係 0 處，唔使同步、唔使重跑六批驗證。殘留：A 註解一句「刪死 data favorDelta」（歷史註解，留返）、`qa149/pristine_index.html`（173 處舊快照）同 `qa200/drive200.json`（7 處 QA drive 數據）——兩者都唔係 live，唔郁。統籌核實：index.html 只剩 1 處 `favorDelta`，就係 A 嗰句註解。
  - (b) `softOverdueFavorDebtLock` — **留返，唔硬刪**（有讀者＋測試釘死，符合停手規則）。永不觸發已對 live 證明：① 函數本身 soft-only（`?softBehaviorGate=1`／`?softPreview=1`／localStorage 先行，預設 off）；② 就算 flag 開，佢只掃 `S.mockDebts` 入面 `status == "已逾期"`——全檔冇任何 code 將 mockDebt status 設做「已逾期」（創建全部係「未到期」／「就嚟到期」；mutation 得兩處：L22962「就嚟到期」、L23334「絕響」；唯一「已逾期」字面值係季節卡 `card_biao_summer`，唔係 mockDebt，鎖掃唔到）。**但讀者存在**：live `canAudition()`（L17511）同 `gateShortReason()`（L17560）直接 call 佢；`window.__freeplay` export＋self-check（L34287／34368／34401–34402，刪咗會報 `debt_lock` fail）；測試 `test_weave43_logic.js` §3（手造已逾期債 control case，斷言會鎖）同 `test_weave47_logic.js`（extract＋經 `canAudition` 行）。刪佢要郁核心 gating＋self-check＋兩個測試檔，屬另票範圍。建議另票：刪函數＋兩個 call 位＋export／self-check＋改寫 weave43 §3／weave47（行為零變，因觸發條件本身唔存在）。
  - (c) `creditGate`／`debtGate` — 冇獨立人工製品可刪。全 repo 冇呢兩個名嘅獨立函數／測試 id；佢哋只係 `canAudition`／`gateShortReason` 入面嘅 local 變數名（`softIndustryCreditGate`／`softOverdueFavorDebtLock` 嘅回傳）。self-check 入面嘅 `"credit_gate"`／`"debt_lock"` 只係 fail label 字串。隨 (b) 刪鎖嗰陣 `debtGate` local 自然消失；`creditGate`（業內信用閘）係真 soft 閘，留返。
  - (d) 「何生忠誠帳」— live 已經冇嘢可改。`index.html`＋story JSON 入面「忠誠」**0 命中**：N10 nodeRipple 而家係 null（B 話 notes 已改寫，核實屬實——N10 節點全文無「忠誠」）；「呢份忠誠，佢之後會還」嗰句只留喺兩個舊測試 fixture（`spine_c6_c17_v79.json`、`spine_n6_n17_v136.json`，歷史快照，唔係 live）。其餘「忠誠」命中同忠誠帳無關（`cast_main.json` 角色特質標籤、`story_detail_rival_mentor.json`「忠誠同利益對撞」衝突描述）。唔使改寫。
- **`coverage.count`**：`coverage` 係 JSON 入面嘅純 metadata——`index.html` 同全部 tests **零讀取**。`have` 21 項、`count: 21`，但 `nodes` 有 22 個，漏咗 v253 加嘅 `N17_epi`。已補：`have` 喺 `N17` 之後插入 `N17_epi`（跟節點次序），`count` 21→22，`missing` 維持 `[]`；`python3 -m json.tool` 驗證通過，story 測試全過。附帶發現：`qa.beat_counts` 仲寫 `N17: 19`，但 v253 已將 N17 由 19 拍搬 4 拍去 N17_epi（家下 15 拍）——統籌已順手改做 15（見「統籌整合」）。
- **農場洞分析（只分析＋提案，零經濟改動）**：現行門檻數字（live 抽查）：`endingFavor410()`／`favorLedgerCounts()`——`creditsHeld` ＝ `S.mockCredits` 入面 `status !== "絕響"` 嘅筆數，**唔分來源、唔讀 `redeemedBy`**；`settled` ＝ `S.favorLedger.settled`。E4：聲望 ≥50＋信用 ＜30＋`creditsHeld ≥ 2`（`ENDING410_T.e4RescueCredits: 2`）；E5：`(settled + creditsHeld) ≥ 6`＋何生 rel ≥60（`e5FavorTotal: 6`、`e5AgentRel: 60`）；E3 製片老闆變體：`(settled + creditsHeld) ≥ 5`（`ENDING95_T.e3BossFavor: 5`）。
  - 洞 (a) 茶餐廳債權無上限 — 仍然成立，數字不變：`enc79HelpClear`：每日最多 1 次（`enc79HelpDay` 旗）、當日機率 55%（`enc79Rand < 0.55`）、id 按日生成 `credit_enc79_cafe_help_<dayIndex>`、`enc79GrantCredit` 只按 id 去重、**無總量上限**；唯一會變「絕響」嘅債權係芬姐移民嗰筆（`EXODUS_FEN_CREDIT`），霞姐債權永不過期。刷穿成本：E4 要 2 筆 ≈ 期望 4 日探訪（每次 1 次出行額度、$0）；E5／E3 要 6／5 筆 ≈ 期望 11／9 日、$0。何生 rel ≥60 嗰邊唔係農場瓶頸（事務所打聽每次 +3~+5）。
  - 洞 (b) 還季節卡刷 settled — 成立，但有上限，唔係無限：現金還款一律劃一 `$200`；季節卡得 **8 張固定 id**（`SEASON_COLLECT`：何／張／標／美兒 × 春／夏／秋／冬），`favorLedgerNoteSettled` 按 id 冪等，所以季節卡最多貢獻 **+8 settled、合共 $1,600**，唔係無限刷。開局最快：1990 春兩張卡 $400 → settled 2；加教學債 $200／禮物／幫忙通告還 → settled 3。季節卡本身唔係大洞；大洞係佢同 (a) 相加：`settled + creditsHeld` 兩個池都可以用低成本填滿。
  - 現況已變：新庫 282 張入面有 **22 個 distinct `trigger.creditId`**（13 張 BR89 引薦債權經 A 重對後全部 REUSE 新庫 trigger gig；另有 c7／c9／c15 主線債權、WF3 三筆、芬姐、顧借錢雙觸發等）。兌現後 `redeemedBy` 會標記、trigger 通告落板，但結局計數照計（`endingFavor410`／`favorLedgerCounts` 唔讀 `redeemedBy`）——兌現咗嘅人情仲係結局燃料，呢個係 R2 要處理嘅口徑問題。`credit_c13_newyear` 例外：冇 trigger gig，喺結局頁兌現。
  - 修補提案（全部要拍板先改，C 冇改任何口徑／門檻）：**R1**（改計數口徑）：`endingFavor410`／`favorLedgerCounts` 計 `creditsHeld` 嗰陣排除 `credit_enc79_cafe_help_*`。一行 filter；E4／E5／E3 即刻唔再畀茶餐廳刷穿。副作用：霞姐債權變得「結局零價值」，要配返兌現先唔會令玩家覺得白做。**R2**（改計數口徑）：已兌現債權（有 `redeemedBy`）唔再計 `creditsHeld`。令「兌現」有實質代價／意義，配合而家 22 個 trigger 兌現路一齊先成立。**R3**（語義統一）：`settled` 語義而家混雜（還錢／還季節卡／移民勾銷 `exodus_writeoff` 都計 settled——芬姐債勾銷嗰陣 `favorLedgerNoteSettled(EXODUS_FEN_DEBT.id, "exodus_writeoff")` 都 +1）。要定：移民勾銷計唔計？教學債 `closed_other` 計唔計？定咗先至改。**R4**（純顯示，唔使拍板可做）：人情頁／結局頁分開顯示「故事債權」vs「茶餐廳幫手」vs「已兌現」，等玩家睇得出邊啲係真人情。零玩法影響。**R5**（另開兌現工作，唔係計數修補）：霞姐債權改做情報貨幣（審核 §9.2 建議：每持有 1 筆，茶餐廳聽八卦多一個選項），唔再入 `S.mockCredits`／結局計數。連同其餘未兌現債權逐筆加兌現（主線 4 筆＋WF3＋一次性嗰批），要另開票排期。**唔建議**：淨係加總量上限（例如霞姐債權上限 5 筆）——治標，唔解決「門檻量度緊去茶餐廳次數」嘅本質問題；亦唔建議郁門檻數字（E4 ≥2／E5 ≥6／E3 ≥5 係用戶拍板數字）。

## 統籌整合（C 完成後，統籌親手做）

1. **SOFT N1–N6／N6F 摘要 → 新標題（統籌決定，選項 a）**：C 留返等統籌定嘅 7 處——N1「先學做動作戲／先賺」、N2「留人脈／趕通告」、N3「對對手硬／忍」、N4「何生拒單」、N5「采兒小訪題」、N6「飯堂閒角」、N6F「片場跟班」。統籌核實 `prog71Title()` 讀 SOFT 優先、**永不跌返 node.title**（`STORY_TITLE_SOFT[id]` 有值即回，否則 `calib60NodeTitle`，最後先係 id 本身），所以呢 7 個摘要字會經進度頁／「先完成上一幕〈…〉」／地圖提示當標題顯示——同已拍板新短詞標題（N1 通告板／N2 後巷／N3 正中央／N4 記數簿／N5 筆記本／N6 角落那張枱／N6F 角落那張枱）衝突。決定一併改做新標題；摘要資訊本身留喺 JSON 抉擇／label，唔會唔見。測試同步：progress71（A2／A3／段二／A4／B1×4／B2×2，含 B1 防劇透改驗「第 6 幕・電視線〈角落那張枱〉」行唔見——N6／N6F 同標題，改驗路線行）、story191（N6F 開放行／合併行／地圖提示／新遊戲 N6 電視線行唔見）、story198（N18 鎖行）、verify37（N6 進度行）、weave48（SOFT 釘表 N6）。verify37 picker 錨點維持 fixture 舊標題「留人脈／趕通告」——picker 讀 frozen fixture（17 節點舊快照，見下），唔係 live 標題，改錨點係錯。
2. **N6F lockedHint 標題引用（統籌發現＋修）**：全 JSON 掃舊標題，唯一 live 顯示嘅標題引用係 N6F `lockedHint`「先完成「采兒小訪題」那一幕」→改「筆記本」。其餘命中唔係標題，唔郁：N8 playerHint／journalCandidate／redStarHook「選美後台」（場景描述，唔係標題）、N12 choice label「做高危替身」（動作，唔係標題）、N17 beats「高危替身那一躍」（回憶事件，唔係標題）、N6 openConditionsNote「飯堂閒角」（DEV legacy 對照，`TEXTFIX55_SKIP_KEYS` 註明唔顯示）、JSON openConditionsNote 入面「1989 夏／秋／冬」（同樣 legacy 對照，唔顯示）。改 N6F lockedHint 郁咗 `nodes[5:]`，`test_story157_pack_static.py` hash 重算：舊 `e2580c74…` → 新 `6e2f307b9e3023281e87012ca4ae89f59e7184f3169577a85dda267ca9f8a63c`，註解加 v20a254 一行。個別跑過 ALL PASS。
3. **`qa.beat_counts` N17 19→15（統籌順手修）**：`/qa/phase5/beat_counts` 仲寫 `N17: 19`，v253 已將 N17 由 19 拍搬 4 拍去 N17_epi（家下 15 拍）；`index.html`＋tests 零讀者（純 metadata），改數字唔影響 hash（唔喺 `nodes[5:]`）。
4. **行數漂移教訓（統籌親身中招）**：統籌第一版 SOFT 改動加咗 1 行註解（插入點 L6515），kwan151 即刻 FAIL（13 錨點全部喺插入點之後）。修法：刪返嗰行註解（理據併入下面已存在嘅 v20a254 註解），行數回復 C 驗過嘅 44640 行，kwan151／tang152／text125／progress71／story191 全部 ALL PASS。**以後喺 L6515 附近加行，一定要預 resync。**
5. **HINT／CALIB60 舊名（統籌核實，刻意留返，見「跟進」）**：`STORY_HINT_SOFT` lockedHint／nextHint 入面仲有舊章名＋字面「1989 年夏／秋／冬」。核實：`storyHintPack` 優先讀 JSON node 嘅 lockedHint（21／22 個節點有，N17_epi 兩邊都冇→空字串），SOFT lockedHint／nextHint 喺 live 唔顯示（nextHint C 已證永不顯示）；`CALIB60_NODE_TITLES` 後備表舊名亦只喺 pack 未載入先跌落去（live pack 已載入，顯示行優先讀 JSON 標題）。三處全部 dormant，唔喺今次範圍，列入跟進，唔順手改（CALIB60 牽涉 mock 環境斷言 `test_calib60_logic.js:200`「暴雨救場」＋progress71 B1「上岸路／賭枱邊」，要另票判斷）。
6. **Fixture 說明**：`tests/fixtures/story_detail_n1_to_n17.json` 係 17 節點 frozen 舊快照（N6「首次正式約會對象」等 pre-v250 標題，缺 N6F／closeup39／N17_epi／N18／N19），kwan151 用佢做「walk 原樣輸出」回歸數據——**唔係 live 鏡像，唔好同步佢**。

## 測試

- 全套 `qa131/run_suite.sh`（工作副本，2026-11-17 00:04–00:07）：**TOTAL PASS 316 FAIL 10**。10 項 FAIL 同基線 main `f8e486a` 實測（315／10）**完全一致**，全部 pre-existing（7 項係 softRev 期望 `s111` 但 live 係 `s107`：flash51／rumor49／slot50／start53／wrap38／weave43／44／49；另 soft_tip_111_restore、wf5_87 亦係基線已有）。唯一差別係 A 新加嘅 `test_br89_favor_due.js` PASS（＋1）。
- 個別跑過全部 PASS：progress71／story191／story198／verify37／story157 pack＋index／weave46／48／br89 邏輯／靜態／favor_due／gig229 全系列／nat92／calib60／travel114／gift185／rom176／weave42–45／47／49／410／lock78_ending。
- C 嘅改動一度令 3 個新 FAIL 出現（kwan151／tang152／text125），已全部 resync 修復（根因：加咗 2 行 SOFT 註解，插入點之後嘅絕對行號釘全部 +2：kwan151 13 個釘、tang152 3 個釘、text125 3 個釘，逐個錨點核實內容再 +2）。其餘 C 郁過行數嘅測試檔一併 resync：tang171／173（總行數斷言 44638→44640、標籤 44649→44651、openLoc DEF 40039→40041）、gift185、rom176（5 個釘各 +2，NPCS 6360 喺插入點之前唔郁）、travel114（49 個錨點各 +2）、progress71 B3（mock＋斷言「高危替身」→「墊」）。
- `node --check index.html` 唔適用（.html 副檔名，Node 24 報 ERR_UNKNOWN_FILE_EXTENSION）；JS 語法由 suite 內靜態測試覆蓋。
- `index.html` 淨行數變化：A +61、C +2、統籌 +0（SOFT 值同行改、註解行刪一加零、N6F 係 JSON），合共 +63；`git diff HEAD --numstat` index.html：84 增／21 刪（A＋C＋統籌）。

## 落地

- 工作副本 `git push origin v20a254` → 常駐 clone checkout main → `git merge --squash v20a254` → commit → push main（deploy key，唔開 PR）。落地後 main 新 HEAD＋Pages 核實由統籌做，記入 parent 回報；本檔只記工作副本內容。

## 要拍板嘅嘢（逐項，交 parent 問用戶）

1. **N4 季節張力**：JSON `when: 1988春 / W8-9` vs beats[0]＋施工單 §4＋攻略 scene cap 三邊「夏」（live `1988年夏…`）；攻略同一章 blockquote 寫「1990 年春」係手民之誤。邊邊為準？（改 `when` 去夏，定改 beats／施工單去春？）
2. **農場洞修補方案 R1／R2／R3**（見 C 節）：R1 排除茶餐廳債權出 `creditsHeld`；R2 已兌現債權唔再計 `creditsHeld`；R3 定 `settled` 語義（移民勾銷／教學債計唔計）。三項都改計數口徑，要用戶拍板。R4 純顯示可直接做；R5 另開兌現票。
3. **計數口徑（另一票）**：兌現後扣唔扣數（`creditsHeld` 唔讀 `redeemedBy` 係已知出入，v253 已記錄）——同 R2 重疊，等用戶一併定。
4. **F1 $500 定額 vs SPEC §7.1 臨記帶（$250–400）**：保留 v20a17 原裝 $500，定改做帶內（改 pay 係一行）？
5. **攻略 N6F_a／N6F_b notes 逐字引用**：用戶未答，**唔好主動再問**，留待用戶話先補（2026-11-17 朝早簡報已指明）。

## 跟進（唔使拍板，另票／順手）

- `softOverdueFavorDebtLock` 另票刪（函數＋`canAudition`／`gateShortReason` call 位＋export／self-check＋改寫 weave43 §3／weave47；行為零變）。
- HINT nextHint 舊章名＋CALIB60 後備表舊名＋SOFT lockedHint 舊名／1989 字面值——三處 dormant 文字，另票判斷係咪順手清（注意 calib60 mock 斷言）。
- 廖炳星引薦雙 gig：先殺青 `gig_1991_film_109` 唔標 `redeemedBy`，留另票統一（通用-credit 限制，同 c7／c9／c15 一樣）。
- v254 落地跟進（未修）：F2／F6／F7／F8 缺口維持；劣評分支新庫下死咗（fame 最低 [5,10]，`sh.fame ≤ 1` 永不成立）；殺青海報 caption D-12；唱片 9 張 singer 語義含糊；5 位名冊外女星殺青唔加好感；1990 冬板面薄；高俊傑同場顯示段刪唔刪（產品決定）；N6F `artId: null`（等場面圖批）；攻略引文 158 段 MISS（154 段 RW-2 旁白漂移＋3 段對白＋8 段 NEAR／SUB 對白）由 parent 經 artifact 改。
- 實機驗證（瀏覽器恢復後）：BR89 13 對兌現＋F1 幫忙通告到期流程＋死碼清理後全程＋SOFT 新標題顯示（進度頁／地圖提示／「先完成上一幕」）。
