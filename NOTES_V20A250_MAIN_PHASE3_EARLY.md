# NOTES_V20A250_MAIN_PHASE3_EARLY

主線實裝票 v250 早期批（N1–N6＋N6F＋N18）。基底 main `def65af`（v249）。
分支 `v20a250`。Suite **314／10**（FAIL 10 項同基線逐項一致，見 §6）。

## §1 改動總覽

| 檔案 | 改動 |
|---|---|
| `index.html` | 44,392 → **44,205 行（淨 −187）**：GRANT229 加 11 entry、刪 `N5:*`（淨 +10）；刪 BR89 內嵌表 197 行＋soft N6F 條目 1 行；scrub 祖父條款註解＋1；其餘開閘／lockedHint／selfCheck 同行改 |
| `content/story_detail_n1_to_n17.json` | 19 → **20 節點**（N6F 搬入）；N1–N6／N6F／N18 標題統一新短詞；N5 weekMin 9→36、when W36；N6 lockedHint 補「先完成采兒小訪」；對白層面 (b) 2 處修正 |
| `content/gigs_new.json` | 241 → **251 張**（10 張即派新通告，純加法 +310 行／−0 行） |
| `content/SANDBOX_BEHAVIOR_GATE_N1_N5_SOFT_STUB_v1.json` | N5 trigger weekMin 9→36（其餘唔郁） |
| `content/STUB_STORY_BEATS_FREEPLAY_SLOTS_v1.json` | N3_b ripple 一句第二人稱修正（freeplay 會讀呢檔） |
| 測試 | 38 檔（見 §5；resync＋計數更新） |

## §2 逐章改動（live JSON 原文做底，唔照抄施工單引文）

- **標題統一**：N1 通告板、N2 後巷、N3 正中央、N4 記數簿、N5 筆記本、N6 角落那張枱、N6F 角落那張枱、N18 將來。N6 `setting` 內嵌舊標籤「角落那張桌子」→「角落那張枱」。其餘舊標題出現處（N3 傳聞引用、N18 對白短語、N6 敘事「桌子」普通名詞）唔改。
- **N5（D10）**：`pacing.weekMin` 9→36；`openConditions` `week_min:9`→36；`when`／`pacing.when` `1988秋 / W9-10`→`1988秋 / W36`（`1988秋` 無改，YEARS66 source 年份唔手改）。
- **對白層面 (b) 修正 2 處**：N1_a `effects.notes`「張子駿肯教你，是你好彩」→「張子駿肯教他，是他好彩」；N3_b `effects.ripple.rivalAttitude`「高俊傑覺得你好蝦，變本加厲」→「高俊傑覺得他好欺負，變本加厲」。N1_a 嗰句喺 freeplay stub 搵唔到，唔使改；N3_b 嗰句 freeplay stub 同步改咗。
- **對白重抽覆蓋**：N1–N6、N18 全部 beats＋全部 choices resultBeats 已逐字對照施工單 §2–§8。旁白全部 RW-2 漂移（live 啱，唔改）；對白句逐字一致，例外只有「等住睇」「笑住帶過」「留下一條後路」三句（live 已改好）同 N18_b label 書面語化。詳見 `~/workspace/linji-main-phase3/V250_DIALOGUE_DELTA.md`。
- **留低**：N6F 第二人稱轉換（beats B6／B7、兩邊 notes、4 個系統 resultBeats）——搬遷任務明文一字不改，逐句提案喺 delta §3.4，**等拍板先做**。N6 唔接邊派唔派散工要拍板（盤點 §13 第 4 項）。N1 頒獎禮場地一句唔喺 N1–N6／N18 JSON 入面。`thresholds.rel_choi_threshold_note`「夏 OR 保留」舊註留低唔改（metadata 註腳，唔係玩家面）。

## §3 即派接線（GRANT229，17 key，無 wildcard）

新增 11 個 entry，現有 5 個主線 entry＋2 個 W3 entry 一字不改：

| 鍵 | gig | 備註 |
|---|---|---|
| `N1:N1_a` | `gig_1990_tv_124`《跟組雜務》 | NEW |
| `N1:N1_b` | `gig_1990_film_124`《賀歲片場》 | NEW |
| `N2:N2_a` | `gig_1990_film_125`《陰陽夜更》 | NEW |
| `N2:N2_b` | `gig_1990_tv_125`《街景臨記》 | NEW |
| `N3:N3_a` | `gig_1990_tv_127`《幽林魅影夜追逐》 | NEW |
| `N3:N3_b` | `gig_1990_tv_128`《靈異屋邨夜話》 | NEW |
| `N4:N4_a` | `gig_1990_ad_117`《便利店短片》 | NEW |
| `N5:N5_a` | `gig_1990_tv_130`《記者會外景》 | NEW（N5_a／N5_b 共享） |
| `N5:N5_b` | `gig_1990_tv_130`《記者會外景》 | NEW（共享） |
| `N5:N5_c` | `gig_1990_tv_131`《天星碼頭》 | NEW |
| `N18:N18_b` | `gig_1990_tv_129`《冬日單元劇》 | NEW（唯一作品類） |

`gig_1990_tv_126`《電視城街景》**唔建**（N6_b／N6F_b 唔派，揀「唔接」固定位就唔派）。`gig_1990_tv_122`《記者會現場》仍然喺庫入面（板面通告，唔刪除；去留留後批定）。reason 係何生傳呼口吻廣東話對白，按施工單「派通告嗰句」草稿改寫。新 gig 全部 `storyKeys` 唔加（live code 唔讀 gig 嘅 `storyKeys`；verify Q11 `total_echo` 硬編 35，加任何一個即 FAIL）。

## §4 新通告 10 張（241→251）

| id | 標題 | 日數／片酬 | 季節 | 來源 |
|---|---|---|---|---|
| `gig_1990_tv_124` | 《跟組雜務》 | 3日 [1800,2700] | 1990春 | N1_a |
| `gig_1990_film_124` | 《賀歲片場》 | 3日 [1800,2700] | 1990春 | N1_b |
| `gig_1990_film_125` | 《陰陽夜更》 | 2日 [1200,1800] | 1990春 | N2_a |
| `gig_1990_tv_125` | 《街景臨記》 | 2日 [1200,1800] | 1990春 | N2_b |
| `gig_1990_tv_127` | 《幽林魅影夜追逐》 | 2日 [1200,1800] | 1990春 | N3_a |
| `gig_1990_tv_128` | 《靈異屋邨夜話》 | 2日 [1200,1800] | 1990春 | N3_b |
| `gig_1990_ad_117` | 《便利店短片》 | 1日 [500,900] | 1990春 | N4_a |
| `gig_1990_tv_130` | 《記者會外景》 | 3日 [1800,2700] | 1990秋 | N5_a＋N5_b 共享 |
| `gig_1990_tv_131` | 《天星碼頭》 | 3日 [1800,2700] | 1990秋 | N5_c |
| `gig_1990_tv_129` | 《冬日單元劇》 | 4日 [2450,2950] | 1990冬 | N18_b（唯一作品類，posterBrief 有，leadStarId 未定） |

`year` 寫顯示年 1990（D-6；loader 跳過 YEARS66，三重證據見工人 B 報告）。`posterBrief` 只有 129 有（全庫作品 142 張，141 張有；臨記 0／103 有）。`leadStarId` 10 張全部 null。文案全部香港式書面語，synopsis 每張 3–4 句；簡體 0 命中、禁詞 0 命中。詳見 `~/workspace/linji-main-phase3/V250_B_REPORT.md`。

## §5 開閘＋N6F 搬遷＋scrub 祖父條款

- **Stub**：N5 trigger `weekMin` 9→36；其他 N5 trigger 欄位唔郁（`needDone: ["N4"]`、`seasonAny: ["autumn", "winter"]`）；`legacyWeekMin: 9` 保留；`stubRev` 維持 `v1.3.0-full-literal-or`。連帶 `BehaviorGate.selfCheck` c5base 樣本 `week:9`→36、`dayIndex:50`→250、`lastMainDoneDay:40`→240。
- **GATE N6／N6F**：加 `needDone: ["N5"]`（weekMin 15 唔郁）。N18 註解「N5 自身 weekMin 9」→36。STORY_HINT_SOFT N6／N6F `lockedHint` 改寫（先完成 N5）；N6F 注入節點 `lockedHint` 改寫（呢句先至係玩家面真正顯示嗰句）。JSON N6 `lockedHint` →「時候未到。先完成采兒小訪那一幕，等處境劇班底那邊開口，收工去星河電視台飯堂那邊看一下。」
- **N5 lockedHint 清理**：STORY_HINT_SOFT N5 `lockedHint`「約第9週起」→「約第36週起、秋天」，「初夏台慶籌備季」刪走。注意：soft 表 lockedHint 喺正常遊玩係被 JSON 遮住嘅（`storyHintPack` 永遠優先讀 JSON node 欄位）；N5 JSON lockedHint 無提週數／台慶，無誤導，可保留；N6 JSON lockedHint 已按上行改。
- **N6F 搬遷**：由 `index.html` 內嵌表 `STORY_SPINE_NODES_BR89` 搬入 JSON `nodes[6]`（N6 之後），`id`／`beats`／`choices`／`effects`／`flags_written`／`openConditions`／`openConditionsNote` 一字不改（node 抽取，逐欄對照 0 差異）；補 JSON 獨有欄位（`artId: null`、`aftermathHint`／`journalCandidate` 照 N6 pattern 寫電影線對應版、`redStarHook: null`、`nodeRipple: null`、`thresholds: {}`、`pacing` N6 鏡像）；頂層 `coverage`：`have` 加 N6F、`count` 19→20。**內嵌表已刪**：`STORY_SPINE_NODES_BR89`＋`applyStoryBr89Nodes89()`＋呼叫點（改做 v20a250 註解一行）＋soft 表 N6F 條目。殘留只得新註解一行提到個名（跟 v20a242 刪 LAN 表寫法一致）。`playerHint` 差異已核實：JSON 用 node 版「留一個固定跟班」（soft 表係「簽一個固定跟班」；`storyHintPack()` node 優先，顯示唔會變）。
- **⚠️ scrub 祖父條款（新）**：`storyGate113Scrub` 每次載入都行，`needDone` 任一未做就 `delete done[id]`。v249 規則下 N6／N6F 第 15 週開、N5 要第 36 週先開，合法舊檔必然有 done.N6／N6F 而無 done.N5——唔加豁免會靜默刪除舊檔完成紀錄，過咗 1990 年冬更會隨即被 `calib60MissedScan` 登記做「錯過咗一幕」。已加祖父條款：`if(bad && !((id==="N6" || id==="N6F") && week >= Number(e.weekMin)))`——第 15 週起先豁免，第 11 週 done.N6 照清（週數違規唔包）。新檔唔受影響（`evalGate` 開閘仍然要 N5）。實測核實（載入模擬 §7）。
- **刻意留低、無改嘅同類殘留（display-dead）**：N4／N5 `nextHint` 殘留「約第9週起／夏季台慶籌備季／第15週起」——`storyHintPack` 強制 `pack.nextHint = ""`（v19z12 M4），玩家面唔顯示，留低畀將來清理批。`prog71GateItems` 會顯示舊 soft 標籤「先完成第 5 幕〈采兒小訪題〉」而唔係新短詞「筆記本」，要等標題批對齊。`c5SeasonLockLine` 寫死咗「采兒小訪題」，標題批要一併對齊。

## §6 測試 resync＋計數更新（38 檔）

- **gig229 四檔**：grant（T0 27 張 id 齊＋17 鍵；T1 主線 15 映射；刪走舊「N4_a 唔派」「N5→tv_122」「N18_b 唔派」）、pack（251；初級 76／84／51／17／23；作品 142、臨記 103；每年 104／80／67）、years（1990 年 104、總數 251）、press94（251；named 142／base 109）。
- **br89／story157／story191／story198／weave48**：改讀 JSON pack N6F（唔再抽內嵌表）；N6／N6F 標題「角落那張枱」；閘斷言加 needDone N5；`test_story157_pack_static.py` nodes 19→20、N5 weekMin／when W36、nodes[5:] sha 重算 `d8473989…`。
- **gate113**：靜態斷言→v250（N5:* 已拆做 N5_a／b／c）；邏輯加 4 個祖父條款個案（第 21 週 N6／N6F 照保、第 15 週照保、第 11 週照清）。
- **weave45**：N6 fixture 加 `withDone('N5')`；新增反例（N5 未做→鎖）；same-day 段加 `withDone('N5')`。
- **fixtures**：`behavior_gate_n1_n5.json` N5 weekMin 9→36；`story_detail_n1_to_n17.json` N5 when／week_min／pacing W36。
- **釘行 resync（difflib 映射，內容逐字核實純漂移；淨 −187 行）**：kwan151 13 釘（−198）、rom176 5 釘（6360 唔郁，其餘 −198／−187）、tang152 3 釘（9219→9021、14725→14527、14847→14649）、tang171／tang173（openLoc DEF 39793→39606；css 5163 唔郁）、gift185／tang171／tang173 總行數 44392→44205、travel114 49 處（COUNT 12＋FREE 35＋DEF 39793→39606＋WRAPPER 27816→27629）、text125 3 錨點（currentLine 11193→10995、advance 11330→11132、applyFamilySafe 16442→16245）。tang152 係 resync 途中補捉到嘅（唔喺原清單入面，`lines()[9218]` 等三處）。
- **計數／語義更新（期望值真係變咗，唔係漂移）**：
  - dur90 A4：241→251（＋B1／B4 名）。
  - fix88：A1 241→251；B2 入口池 94→104；D1 作品 141→142，**除 129 外**全部有 leadStarId（129 例外寫明，等選角拍板）。
  - nat92：F2 錯峰合資格 229→239（251－12）；**D2 反轉**：九龍電視台第一週 0 可接嘅分佈缺口由 v250 即派新通告填咗（6 張落喺 tvb_kowloon，1990 春低門檻），badLoc 而家係空，斷言改做 `badLoc.length === 0`。
  - wf1_80_logic：pack nodes 19→20（N6F）。wf1_80_static：N18 pack 標題斷言「上岸路」→「將來」（CALIB60 fallback 表「上岸路」唔郁）。
  - terms57 B3：舊「（關係約到2）」只存在於 soft 表 N5 lockedHint，隨 P-01／D10 刪替代閘一併清走；改驗新鎖文「約第36週起」。
- **全套 suite**：`bash qa131/run_suite.sh` → **TOTAL PASS 314 FAIL 10**。FAIL 10 項同 v249 基線逐項一致：flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38（全部已知 pre-existing）。
- **中途發現**：第一輪 suite 306／18，多咗 8 項新 FAIL（dur90／fix88／nat92／wf1_80_logic／terms57／text125／travel114／wf1_80_static）——全部係上列計數／釘行／語義更新，已逐項修好，第二輪 314／10。

## §7 載入模擬（`/tmp/v250_sim.js`，23 項，ALL PASS）

GRANT229 17 key、無 wildcard、全部 gigId 喺 251 張庫入面；N5_a／N5_b 共享 tv_130；無 N6_b／N6F_b。JSON N6F 恰好 1 個、緊貼 N6 之後、beats 8／choices 2、標題「角落那張枱」。內嵌表＋注入器＋soft N6F 條目已無。stub N5 weekMin 36。GATE N6／N6F needDone N5＋weekMin 15。**scrub 實測（真函數＋真 GATE）**：舊檔第 20 週 done.N6 無 N5 照保；done.N6F 照保；第 11 週 done.N6 照清；N18 舉報個案照清。標題 N1–N6／N18 係新短詞；N6 lockedHint 提及先做 N5；N5 weekMin 36＋when W36。`node --check` 兩塊 inline script 全部 PASS。

## §8 verify_gigs.py（`~/workspace/linji-gig-redesign/gigs/verify_gigs.py`，已更新矩陣）

Q0 241→251；WORKS tv 1990 `[2,8,2,0,0]`→`[2,9,2,0,0]`；EXTRAS film 1990 `[9,1,0,0,0]`→`[9,3,0,0,0]`；EXTRAS tv 1990 `[9,1,0,0,0]`→`[9,7,0,0,0]`；EXTRAS ad 1990 `[7,1,0,0,0]`→`[7,2,0,0,0]`；Q8 作品 141→142、臨記通告 94→103；檔頭註解同步。重跑全量：**16 項 ERROR／0 WARNING**，全部係三類已知接受項：

1. **Q2 ×1**：129《冬日單元劇》作品缺 leadStarId——無來源指明主演，唔憑空指派；等選角拍板（見 §9）。
2. **Q6 ×9**：9 張新通告片酬帶 hi ≤ lo×1.25 唔過（[1800,2700]／[1200,1800]＝1.50×，[500,900]＝1.80×）——任務表指定帶同 SPEC §2.10 衝突；保留任務表指定帶（改帶會改玩家實得片酬，係設計改動）；日薪中位數全部喺初級帶內（$750／$750／$700 每日）。SPEC §2.10／verify Q6 修訂留跟進。
3. **Q17 ×6**：6 張標題＋角色名同已刪舊庫字串完全一致（film_125／tv_124／tv_125／tv_127／tv_128／ad_117）——名係施工單／V249 對照表嘅劇本定名（寫單嗰陣對住舊庫寫），唔係抄舊庫文案；blurb／synopsis 全部新寫，Q17 只係標題字串撞舊庫。接受為已知偏差，唔改名（改名會偏離已批劇本名）。

其餘 Q2–Q18 全部 PASS（包括 Q11 回響、Q12、Q13、Q15）。gig229 JS 測試計數漂移已喺 §6 同步。

## §9 已知限制／等拍板（留後批，唔係呢票）

1. **129《冬日單元劇》主演未定**（Q2 ×1＋fix88 D1 例外）：1990 冬六位合理電視主演 Q13 計數已滿 3 張，抄模板星都會撞 Q13；其餘未滿嘅星定位唔夾。等 parent／用戶指派主演，或接受呢一項 FAIL。
2. **9 張片酬帶 vs SPEC §2.10／verify Q6**：收窄片酬帶定係修 SPEC／verify，留跟進決定。
3. **N6F 第二人稱轉換**：A delta §3.4 有逐句提案，等拍板先做。
4. **N6 唔接邊派唔派散工**：盤點 §13 第 4 項，等拍板。
5. **`gig_1990_tv_122`《記者會現場》去留**：N5_a／N5_b 改 NEW 130 之後要定。
6. **`thresholds.rel_choi_threshold_note`「夏 OR 保留」**：留低唔改（metadata 註腳）。
7. **D3 F1 幫忙通告**：留 v253。**D7 N16 跟進通告計一個作品**：留 v252。**D4 closeup39**：留 v251。**D11／D12**：留 v252。
8. **人情 F2／F3／F5／F6／F7／F8／F9／F10 兌現**：留 v253。
9. **CALIB60_NODE_TITLES／STORY_TITLE_SOFT**：唔郁（fallback／摘要標籤表，JSON 標題運行時優先；全部對齊係另一個標題批嘅工作）。

## §10 實機抽檢清單（瀏覽器已死，全部押後，唔好扮驗過）

- N1–N3／N4_a／N5_a／b／c／N18_b 即派實機（第二朝何生電話派、跳過試鏡）。
- N6／N6F needDone N5 開閘實機：新檔第 15 週前鎖、第 36 週 N5 之後開；舊檔 done.N6／N6F 祖父條款係咪如預期保留、calib60Missed 有無誤報。
- N6F 由 JSON 直出後進度頁／StoryPlay 顯示（標題「角落那張枱」、beats／choices 完整）。
- N5 第 36 週秋開實機（lockedHint「約第36週起、秋天」）。
- 10 張新通告板面顯示（片酬／季節／地點）＋《冬日單元劇》殺青畫面（作品類，posterBrief 有，主演名未定）。

## §11 工人交付

- A 主線 JSON：`~/workspace/linji-main-phase3/V250_A_REPORT.md`＋`V250_DIALOGUE_DELTA.md`。
- B 新通告 10 張：`~/workspace/linji-main-phase3/V250_B_REPORT.md`。
- C index.html 接線＋開閘：`~/workspace/linji-main-phase3/V250_C_REPORT.md`。
- 整合 resync 腳本：`/tmp/v250_resync.py`（kwan151／rom176／tang171／tang173／gift185）、`/tmp/v250_resync2.py`（travel114／text125）、載入模擬 `/tmp/v250_sim.js`。
