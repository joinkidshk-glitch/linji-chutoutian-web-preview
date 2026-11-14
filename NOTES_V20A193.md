# NOTES_V20A193 — WF4 隨機事件改 once 硬規則（見過就永遠唔再出）

- 分支：`v20a193`（基底 main `b104f85`＝v192；由 `b3db32f`＝v189 rebase 上嚟，見 §6.7；**唔落地**，落地由統籌做）
- **第二次重驗（2026-11-13）：分支由統籌 rebase 上最新 main `707ff66`＝v194，見 §6.9；HEAD `6314dfc`（Case C fix，rebased），工作樹乾淨，index.html 60846 行。**
- 用戶拍板：2026-11-13 20:36「遇過就一定唔可以再遇」（硬規則，唔係拉長冷卻、唔係降機率）
- 調查報告：`~/workspace/linji-work-rand-repeat/INVESTIGATION.md`（舊制：36 單、每 3.2 日一單、一年 113 單 76% 重複、三年 358 單 91% 重複；電視線玩家見 set03《飛紙仔殺到埋身》21 次）

## 1. once 機制點改（`index.html`，WF4 區 L40214 起，行號以本分支為準）

- `wf4PickEvent`：舊過濾 `ev.once && seen>0`（得 boss01–03 三單）＋45 日冷卻（`evDay`＋`WF4_CFG.repeatDays`），改做**全部事件見過即剔**：`(st.seen[ev.id]||0) > 0 → return false`，唔分 `once` 旗。合資格池空 → 回 `null`，嗰日／嗰次入場就冇事件（`wf4DailyTick`／`wf4TryLocEvent` 本來就接受 null，唔出空卡、唔 crash——見 §6 抽乾測試）。
- `WF4_CFG`：`{ pDay:0.03, pLoc:0.03, gapDays:3, locTriesPerDay:3, pendingMaxAge:2 }`（舊 `{ pDay:0.30, pLoc:0.20, gapDays:2, repeatDays:45, ... }`）。`repeatDays` **成個刪除**（唔係留低唔用）；seeded 隨機 `wf4Rand`（FNV-1a）唔郁，`gapDays` 保留（2→3，見 §3）。
- `wf4Fire`：唔再寫 `evDay[id]`；`seen[id]++`＋`saveQ()` 即寫不變（seen 係 once 封印本身）。
- `wf4Ensure`：`evDay:{}` 初始化**保留**（舊 save 有此欄，唔讀唔寫，純相容；註解寫明）。其餘欄位不變。
- `wf4PresentPending`：pending 嗰單如果已經見過（`seen[pending]>0`，舊 save 遷移邊緣情況）→ 清 pending、唔彈、回 false。正常流程 pending 本來就係 pick 嗰陣未見過嘅，呢個守衛只防舊 save／異常狀態。**Case C 修法（見 §6.6）：呢條守衛由 baseOk 之後搬到函數開頭（`wf4Ensure`＋pending-null check 之後、ending／強制日／病日／芬姐／baseOk 之前）——清 stale pending 唔靠 base 條件；另外同一條規則加埋另外兩個 WF4 入口：`wf4DailyTick`（過期或見過都清）＋`wf4TryLocEvent`（見過即清，唔閘住入場擲骰）。三處都係淨零行數改動（index.html 總行數 60701 不變，行號釘測試唔使再 resync）。**
- `ev.once` 旗本身保留（boss01–03 仲標住，語義不變——而家全部事件都係 once 效果）。

## 2. 遷移處理

- `S.wf4.seen` 已經經 `saveQ()` 持久化，規則一改即刻生效：舊 save 嘅 seen 紀錄（例如 set03 見過 21 次）繼續封，唔洗走、唔重置。
- `S.wf4` 成個唔存在嘅舊 save（或新局）：`wf4Ensure` 照常初始化，唔 crash（測試覆蓋）。
- 舊 save pending 指向已見過事件：見 §1 守衛，清走唔彈（實駕 Case C 驗證）。
- 紀律不變：SAVE key `starVolunteer_map_v19w`、softRev `s107`、`?v=` `v20a10` 全部冇改。

## 3. 擴池＋頻率（計數做）

### 3.1 點解頻率一定要大跌

once 之後，三年抽獎次數唔可以超過可達池。舊頻率三年約 358 次抽獎，池得 36 單——就算擴池到 72 單都頂唔住。模擬器（`qa193/sim_wf4.js`，由調查員嗰支改，用遊戲本身 WF4 code eval，唔係重寫邏輯）掃咗六組參數：

| pDay／pLoc／gap | 一年事件（A 均衡） | 三年事件（A） | A day 池抽乾日 | A 全部抽乾日 |
|---|---|---|---|---|
| 0.30／0.20／2（舊） | 58 | 68 | day 732 | day 751 |
| 0.15／0.10／3 | 56 | 68 | day 736 | day 751 |
| 0.10／0.08／3 | 57 | 68 | day 736 | day 765 |
| 0.08／0.06／3 | 49 | 69 | day 757 | day 769 |
| 0.06／0.05／4 | 37 | 67 | day 758 | day 977 |
| 0.05／0.04／3 | 37 | 64 | day 758 | day 905 |
| **0.03／0.03／3（採用）** | **28** | **62** | **day 915** | **day 965** |
| 0.02／0.02／3 | 16 | 45 | 未抽乾（但只見 24／33 單 day 事件） | 未抽乾 |

- 0.02 太疏：一年得 16 單，而且 day 池有 9 單三年都見唔到（內容嘥咗）。
- 0.03 是甜點：day 池捱到 1992 年中後期（day 915，約 1992-07），均衡路線三年見 62／68 單可達事件；一年約 28 單（平均每 13 日一單，舊制係每 3.2 日一單）。
- 代價講清楚：**隨機事件密度跌咗約 4 倍**。呢個係 once 硬規則嘅數學代價，唔係 bug——每一單而家都係一次性內容，唔可以再用重複頂數。

### 3.2 擴池：36 → 72 單（Phase 1）

- day 池 18 → **36**（新 day05–16、st12–17，共 18 單）。
- loc 池 18 → **36**：film_lion 3→5、film_cotton 2→4、film_harbour 2→4、**tvb_longmen／tvb_harbour／tvb_kowloon 各 1→4**（新 set11–25，共 15 單）、cafe_cha 8→11（新 cha05–07，共 3 單；boss01–03 一次性鏈不變）。
- 新事件清單（id／地點／觸發條件）：

| id | 標題 | trig／地點 | 條件 |
|---|---|---|---|
| wf4_ev_day05 | 冰室門口嗰張櫈 | day | — |
| wf4_ev_day06 | 大排檔嗰煲及第粥 | day | tierMin 1 |
| wf4_ev_day07 | 電車上面嗰段戲 | day | — |
| wf4_ev_day08 | 天台晾衫嗰陣風 | day | 夏／秋 |
| wf4_ev_day09 | 唱片舖試聽嗰首歌 | day | — |
| wf4_ev_day10 | 巴士上層望住個海 | day | — |
| wf4_ev_day11 | 茶樓飲早茶聽到消息 | day | 1991 年起 |
| wf4_ev_day12 | 街市買餸撞到熟人 | day | tierMin 1 |
| wf4_ev_day13 | 電話亭入面嗰個長途 | day | 壓力 ≥45 |
| wf4_ev_day14 | Call機密碼簿唔見咗 | day | 1991 年起 |
| wf4_ev_day15 | 銀包得返幾蚊 | day | 銀包 ≤$1000 |
| wf4_ev_day16 | 瞓唔着嗰晚數星 | day | 壓力 ≥45 |
| wf4_ev_st12 | 廟街夜市嗰檔煲仔飯 | day | 秋／冬 |
| wf4_ev_st13 | 渡輪上面嗰陣海風 | day | — |
| wf4_ev_st14 | 卡拉OK嗰晚有人點錯歌 | day | 1991 年起 |
| wf4_ev_st15 | 的士上面聽到嘅電台 | day | tierMax 1 |
| wf4_ev_st16 | 返屋企樓下撞到細佬 | day | 1991 年起 |
| wf4_ev_st17 | 涼茶舖嗰碗廿四味 | day | 壓力 ≥45 |
| wf4_ev_set11 | 廠房門口嗰班車 | loc／film_lion | — |
| wf4_ev_set12 | 道具房嗰把遮 | loc／film_lion | 夏／秋 |
| wf4_ev_set13 | 化妝間嗰面鏡 | loc／film_cotton | — |
| wf4_ev_set14 | 收工嗰陣嗰句說話 | loc／film_cotton | — |
| wf4_ev_set15 | 碼頭邊嗰場夜戲 | loc／film_harbour | — |
| wf4_ev_set16 | 道具船上面嗰陣風 | loc／film_harbour | 春／夏 |
| wf4_ev_set17 | 錄影廠門口嗰班粉絲 | loc／tvb_longmen | tierMin 1 |
| wf4_ev_set18 | 新聞部嗰陣騷動 | loc／tvb_longmen | — |
| wf4_ev_set19 | 化妝間借粉底 | loc／tvb_longmen | — |
| wf4_ev_set20 | 清水灣嗰陣海風 | loc／tvb_harbour | — |
| wf4_ev_set21 | 廣播室嗰個電話 | loc／tvb_harbour | — |
| wf4_ev_set22 | 飯堂嗰碟叉燒 | loc／tvb_harbour | — |
| wf4_ev_set23 | 外景車上面嗰程 | loc／tvb_kowloon | — |
| wf4_ev_set24 | 紅磡碼頭嗰場戲 | loc／tvb_kowloon | — |
| wf4_ev_set25 | 道具部嗰個電話 | loc／tvb_kowloon | — |
| wf4_ev_cha05 | 茶餐廳嗰張舊枱 | loc／cafe_cha | — |
| wf4_ev_cha06 | 老闆娘嗰煲湯 | loc／cafe_cha | — |
| wf4_ev_cha07 | 隔籬枱嗰份報紙 | loc／cafe_cha | 1992 年起 |

- 寫法紀律：全部廣東話、1990–92 年代質地、真地名／年代片種／工種（冰室／大排檔／廟街／天星小輪／傳呼／Call機／卡拉OK／錄影廠／廣播室）；**冇真人名、冇禁詞**（VCD／互聯網／狗仔隊／1989 年）；文案唔寫數字承諾（效果只喺 `fx` 欄位，跟原有 36 單同一形狀，fx 範圍合測試 schema）；講者避開「阿偉」（DLG108 盤點表 NEW108 維持 8 單唔變）；新 day 事件 18 單全部入埋 `WF4_SCENE_OVERRIDE134`（覆寫表 18→36 行，用現成場景圖，唔留灰；loc 事件用 `LOC_SHEET_BG`，唔使覆寫）。
- 條件閘放寬（穩陣玩家都見到，但唔係成日出）：day03 銀包 ≤$300→**≤$1000**、home01 壓力 ≥55→**≥45**、day04 壓力 ≥75→**≥60**。新事件嘅壓力閘一律用 ≥45（唔用 ≥75），銀包閘用 ≤$1000。

### 3.3 Phase 1 仲爭幾多單＋下一批點排

老實講：**Phase 1 未做到「三年全程零抽乾」**，只做到重複率 0%＋抽乾推遲到三年尾段。最終模擬（`qa193/sim_output.txt`，pDay／pLoc 0.03、gap 3）：

| 路線（1095 日） | 事件總數 | 唔同事件 | 重複率 | day 池抽乾日 | 全部抽乾日 |
|---|---|---|---|---|---|
| A 均衡跑圖 | 62 | 62 | **0%** | day 915（33／36 單；day03／day04／day15 係銀包／壓力閘，穩陣玩家見唔到） | day 965 |
| B 電視線 | 47 | 47 | **0%** | day 990（32 單） | day 990 |
| C 電影線 | 41 | 41 | **0%** | （見 sim_output.txt） | — |
| D 茶餐廳常客 | 42 | 42 | **0%** | （見 sim_output.txt） | — |

- 結構性限制（唔係頻率問題）：**單一地點常客一定會抽乾嗰個地點嘅 loc 池**——tvb_longmen 池得 4 單，電視線玩家日日去，day 125 就抽乾；cafe_cha 11 單捱到 day 771。任何可玩嘅 pLoc 都改變唔到呢點（池 4 單、日日去，預期幾個月內抽乾）。抽乾之後嗰個地點只係唔再出 loc 事件，day 事件照出，唔 crash（見 §6）。
- 要做到「三年全程零抽乾」，下一批（Phase 2）要補嘅量：
  - **loc 池優先**：每個地點補到 **8–10 單**（現時 4–5 單，cafe_cha 11 單除外）。即係再寫約 **30 單 loc 事件**（film_lion ＋4、film_cotton ＋5、film_harbour ＋5、三個電視台／廣播各 ＋5）。再加年份／季節變體（例如同一地點 1990／1991／1992 版）係最慳位嘅擴池法——變體要寫到真係唔同場景，唔准淨換年份數字。
  - **day 池**：補到 **45–50 單**（現時 36 單，可達 33 單；再寫約 10–14 單，優先 1992 年限定＋高壓／見底玩家先見到嘅變體，等尾段都有新嘢）。
  - 補完之後頻率可以酌量調返高少少（例如 pDay 0.03→0.05），但每次調頻率都要用模擬器重掃，唔好憑感覺。
  - 唔建議為咗頂數降低新事件質素（通用事件、重複場景換皮）——Phase 1 寧願認仲爭數，都唔寫水數。

## 4. 舊 `repeatDays` 點處置

- `WF4_CFG.repeatDays` 刪除；`wf4PickEvent` 嘅 `evDay` 冷卻讀取刪除；`wf4Fire` 嘅 `evDay` 寫入刪除。
- `S.wf4.evDay` 欄位只留初始化做舊 save 相容（見 §1），唔再讀寫；舊 save 入面嘅 `evDay` 紀錄會留喺 save 度，唔影響 once 判斷（測試覆蓋：舊 save `evDay` 有紀錄、seen 有紀錄，pick 照封）。
- 全檔 `repeatDays` 只剩區塊頭註解一句提及（講明已刪除），唔係 code。

## 5. 附帶：`eventLine` 一句式文案

- 查過 `content/events_zh_HK.json`：78 句入面有 **3 句跨池重複**（`SHOOT_DAY[2]`＝`SHOOT_DAY_BY_TYPE/廣告[0]`「廣告通告：{title}完成{done}/{total}場，導演收貨。」；`SHOOT_DAY[3]`＝`SHOOT_DAY_BY_TYPE/電視劇[1]`；`SHOOT_DAY[4]`＝`SHOOT_DAY_BY_TYPE/電視劇[2]`）。
- **今票冇改**：pack JSON 紀律係唔直改（要用覆寫表／merge 注入／載入正規化），而 `eventLine` 暫時冇現成覆寫機制（live pack 載入後成個蓋過內嵌 `EVENTS_ZH_HK`，齋改內嵌常數會俾 live pack 蓋返）。WF4 事件本身一次過封咗，呢 3 句重複唔會經 WF4 再出現；要清就要另開一票做 eventLine 載入覆寫（3 句改寫＋測試），唔喺呢票順手直改 pack。
- 其餘 eventLine 池內文案（SHOOT_DAY 6 句等）係一句式狀態文案，唔係完整事件，今票唔郁。

## 6. 驗證

### 6.1 新測試（`tests/test_wf4_193_logic.js`、`tests/test_wf4_193_static.py`）

- logic：CFG 值＋冇 repeatDays；池 72／day 36／loc 36、每地點 ≥4；**72 單逐單見過即封**（兩輪環境：1990 冬／tier 0／銀包見底／低壓＋1992 夏／tier 2／高壓，快進 1000 日後都唔漏）；全池見晒 pick 回 null、tick／入場／present 唔 crash；pending 已見過→清走唔彈、未見過照彈；舊 save 遷移（seen set03:21 照封、冇 S.wf4 唔 crash）；**三年模擬四路線（用遊戲本身 WF4 code eval）重複率 0%、每單最多見 1 次**；新事件文案紀律（冇阿偉講者、冇真人名／禁詞、fx 鍵合規、全部有香港質地關鍵詞）。
  - **Case C 新斷言（§6.6 修法，`tests/test_wf4_193_logic.js` (4b)–(4d)，9 項）**：(4b) `wf4PresentPending` 喺報紙日（day 385，NEWS82 日）／強制日／病日／gap 內（lastDay＝尋日）四種 baseOk 攔住嘅情況下，stale pending（set03 見過 21 次）照清唔彈，seen 保持 21；對照：新鮮 pending 喺強制日唔彈但保留（唔可以一併清走）。(4c) `wf4DailyTick`：pendingDay＝尋日（age 1 ≤ pendingMaxAge 2，唔係過期）、gap 內（唔會順手擲新單）嗰陣 stale pending 即清；對照新鮮 pending 保留。(4d) `wf4TryLocEvent`：stale pending 即清（lastDay＝今日，清完回 false 唔擲新單）；對照新鮮 pending 照閘住＋保留。
- static：SAVE／softRev／?v= 不變；CFG 新值＋冇 repeatDays；pick／fire／presentPending once 寫法；池數＋每地點數；條件閘放寬值；覆寫表 36 行；WF4 區塊冇真人名／時代錯誤詞。**Case C 新斷言 3 項**：守衛排喺 baseOk／強制／病假之前（行號次序斷言）；`wf4DailyTick`／`wf4TryLocEvent` 體內有見過即清寫法。
- **反證**：兩個新測試＋更新咗嘅舊測試對 pristine main `b3db32f` 乾淨 FAIL（193 logic：三年模擬舊制 358 單／33 唔同等 20+ 項 FAIL；193 static TOTAL FAIL 27；86 logic 6 項、86 static 2 項、ui134 3 項、dlg108 static 2 項、dlg108 logic 2 項——全部係 v193 改動點，唔 crash）。

### 6.2 舊測試更新（結論變咗，唔係純漂移）

- `test_wf4_86_logic.js`：總數 36→72、day／loc 各 36；gap 測試 2→3 日；第 (4) 節「45 日冷卻」成段改寫做 once（見過唔再揀、100 日後都唔出、未見過照揀）；day03 斷言跟放寬（$5000 唔出／$800 出）。
- `test_wf4_86_static.py`：總數 36→72；CFG 斷言改新值＋repeatDays 已刪。
- `test_ui134_wf4scene_static.py`：總數 36→72、覆寫表 18→36、無 loc 事件 18→36。
- `test_wf4dlg108_static.py`／`test_wf4dlg108_logic.js`：總數 36→72、舊路徑 28→64（新事件唔用阿偉做講者，NEW108 維持 8 單）。
- 附帶發現：陣列入面嘅 block comment 會整爛 dlg108_static 嘅 naive JS→JSON 轉換——新事件段嘅說明註解已拎走（說明留喺 `qa193/new_events193.js.txt`＋本 NOTES）。

### 6.3 行號 resync（純漂移，difflib 對位核實）

- 本票 index.html 淨 **＋179 行**（新事件 162 行＋覆寫表 18 行＋once 改動淨 −1／＋1 等）。5 個行號釘測試受影響，全部純漂移（`qa193/resync193.py`：44 個 openLoc 呼叫點內容逐行相同）：
  - `test_travel114_static.py`：COUNT 12／FREE 34 不變，DEF 54939→55118、WRAPPER 44387→44566；40855→41033 係 ＋178（pending 守衛 ＋1 行喺佢之後），其餘 ＋179。
  - `test_rom176_static.py`：53369→53548、53737→53916、54876→55055、54970→55149；6070／31574 喺插入點之前唔郁。
  - `test_tang171_static.py`／`test_tang173_static.py`：總行數 60443→60622、openLoc DEF 54939→55118；L4862 釘行唔郁。
  - `test_gift185_static.py`：總行數 60443→60622。

### 6.4 全套 A/B（`qa131/run_suite.sh`）

- 基線（pristine `b3db32f`，`qa193/suite_pristine193.txt`）：**261 PASS／12 FAIL**（FAIL：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38——全部 static）。
- 工作版（`qa193/suite_work193b.txt`）：**263 PASS／12 FAIL，FAIL 清單同基線完全相同，零回歸**（＋2 係新嘅 wf4_193 兩個測試）。
- 中間曾經 258／17（5 個行號漂移 FAIL），resync 後回復 263／12。
- **Rebase 後重驗（基底 `b104f85`＝v192，接手工人重跑，`qa193/suite_pristine193b.txt`／`qa193/suite_work193c.txt`）**：基線（pristine `b104f85`，自己跑，唔係信 v192 落地數字）：**265 PASS／12 FAIL**（FAIL：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38——同 v192 落地話嘅 265/12 一致，FAIL 清單亦同舊基線完全相同）。工作版（Case C 修法後最終樹）：**267 PASS／12 FAIL，FAIL 清單同基線完全相同，零回歸**（＋2 係新嘅 wf4_193 兩個測試；行號淨零，5 個行號釘測試零改動照 PASS）。

### 6.5 三年模擬（`qa193/sim_wf4.js`＋`qa193/sim_output.txt`，遊戲本身 WF4 code eval）

- 四條路線（A 均衡／B 電視／C 電影／D 茶餐廳常客）×1095 日：**重複率全部 0%**，每單最多見 1 次（A 62 單／62 唔同、B 47／47、C 41／41、D 42／42）。
- 抽乾時間見 §3.3（A day 池 day 915、全部 day 965；B tvb_longmen loc 池 day 125、cafe_cha day 771、day 池 day 990）。模擬假設：每日入 2 個地點、壓力 50、銀包 $12,000（穩陣玩家；壓力爆／銀包見底嘅玩家會多見 day03／day04／day15 三單）、報紙日為空、冇主線／巧遇／病假干擾。

### 6.6 實駕（`qa193/drive193.py`，本地鏡像＋`python3 -m http.server`，LIVE 模式，932／700）

- **最終樹重跑全綠（`qa193/drive193_report.json`，`qa193/drive193_final.log`）**：A／B／**C**／D＋700 smoke 全部 ok，0 pageerror、0 http fail。
  - A 事件正常彈出＋見過唔再出：37 日行完，3 單唔同標題——「化妝間借粉底」（day 10，星河電視台）、「冰室門口嗰張櫈」（day 59，茶餐廳）、「茶客講睇場費」（day 68，茶餐廳）；seeded 4 單（set03／st04／cha03／day02）一次都冇出；截圖 `qa193/shots193/A_map_start.png`、`A_d10_tvb_longmen_wf4_1.png`、`A_d59_cafe_cha_wf4_2.png`、`A_d68_cafe_cha_wf4_3.png`。
  - B reload 後 seen-set 仲喺度：7→7。
  - **C 舊 save 遷移：ok**——state：day 70、seen set03:21／st04:7／cha03:2（__n 30）、**pending `null`**、lastDay 64。即係 pending 清走咗、set03 冇再彈、seen 保留 21。C 冇截圖（正確：冇 WF4 modal 彈出，斷言本身就係證據）。
  - D 抽乾優雅：全池 72 單見晒，行 2 日＋入兩個地點，零 WF4 modal、0 pageerror、地圖正常（state day 72）；截圖 `D_map_end.png`。
  - 700 smoke：ok，0 pageerror。
- **修法前 C 係 FAIL**（同一 drive，`qa193/drive193_report.json` 舊版已覆蓋，見 `qa193/drive193.log` 舊記錄／`qa193/probe193d.json` 重現）：state day 70、pending 仲係 `wf4_ev_set03`、lastDay 64。

#### 6.6.1 Case C 根因（實證，統籌假設唔成立）

- 統籌假設：守衛排喺 `wf4PresentFenFarewell()`＋`wf4BaseOk()` 之後，day 70 嗰陣 baseOk 回 false（報紙日／強制日／病假／gap）攔住咗。**逐個核實：全部唔成立**——`wf4NewsDay(70)`＝false（NEWS82 報紙日只有 385／532／658／744／750／1015／1092）；gap＝70−64＝6 ≥ 3；`todayIsForcedDay()`／`conseq61IsSickToday()` 喺嗰個 state 下亦唔係攔截原因——因為 **`wf4PresentPending()` 根本一次都冇被叫到**，連 baseOk 都未行到。
- 證據（source-level instrumentation probe，`qa193/probe193e.py`＋`qa193/build_probe193e.py`，instrumented copy 喺 `/tmp/wf4probe193/`，**唔入 repo**；C-load 之後成條 trace 得 9 個 entry，見 `qa193/probe193e.json`）：
  1. `contFromSlot` → `runScheduleFromToday`（day 69，plan `rest`）→ `presentDueMorningPaper`／`aud91PresentDue`（day 69，冇嘢到期，同步回返）→ `resolvePlannedDay`（day 69，`rest`）→ `wf4DailyTick`（day 70，pending set03、pendingDay 69）。
  2. 之後 **18 秒內零 `goToMapForBrowse`、零 `wf4PresentPending`、零 `presentPendingAward`**——load 嗰陣補跑嘅 rest 日經 `presentRestSleepDayEnd` 出咗休息瞓覺日結板，等玩家撳掣先行 `onMap → afterDayRes → goToMapForBrowse()`；drive 嘅 `settle()`（15 秒）撳唔到呢塊非標準 modal 嘅掣，超時回 `('timeout', None)`、地圖唔可見；之後 `go_map` 強制撳「返回地圖」先至見返地圖。
  3. 之後唯一兩個 WF4 觸發點：`wf4TryLocEvent`（入茶餐廳，pending set03 → `if(st.pending) return false`，唔清）同 `story165TryForcedPlay`（兩次，唔關 WF4 事）。
- 附帶發現（probe 過程，唔係今票範圍）：遊戲主 script 頂層函數**唔喺 `window`**——`page.evaluate` 入面 `typeof wf4PresentPending`／`saveQ`／`goToMapForBrowse` 全部 `undefined`，得 `window.S`（`window.S = S` 顯式寫出）先讀到。第一版 probe（`qa193/probe193c.py`，window wrap）因此零記錄；改用 source-level 注入（`build_probe193e.py`，喺 16 個函數入口插 `window.__probe193` 記錄）先追到。`probe193d.py`（忠實重跑＋window wrap）都係零記錄，但成功重現 C FAIL（A 三單＋37 日同原 drive 一字不差）。
- day-0 對照（`probe193c.py`，即使 wrap 失效，結果本身有意義）：day 0 嗰陣 load 唔使補跑 rest 日（`todayPlanId`＝`scout_all` → mapish → 直接 `goToMapForBrowse`），晨鏈行到 WF4 嗰步，舊守衛都清到 pending——所以 C 嘅失敗係 day-69／70「load 補跑 rest 日」呢條路徑獨有，唔係守衛本身喺所有情況都唔 work。
- **結論**：Case C 係兩個問題疊加——(i) 守衛次序確實有 latent bug（排喺 baseOk 之後，base 條件一攔就清唔到）；(ii) 更重要係 **Case C 條路根本行唔到 `wf4PresentPending`**（晨鏈喺 rest 日結板嗰度斷咗）。淨係修 (i)（統籌方向 (a)）唔會令 C 變綠；唔使修 drive（方向 (b) 唔成立——settle 超時係 rest 板等真人撳掣嘅正常行為，唔係 probe 寫錯；斷言本身亦冇放寬）。

#### 6.6.2 修法：三個 WF4 入口一齊清 stale pending（淨零行數）

- 同一條規則——「pending 指向已見過事件就係死 state，邊個 WF4 入口掂到邊個即刻清」——落喺三處（`index.html`，淨 **+4／−4 行，總行數 60701 不變**，5 個行號釘測試零改動）：
  1. `wf4PresentPending`（P1，統籌方向 (a)）：守衛搬到函數開頭（`wf4Ensure`＋pending-null check 之後、ending／強制日／病日／芬姐／baseOk 之前）。治 latent 次序 bug，覆蓋「無論 base 條件」嘅要求。
  2. `wf4DailyTick`（P2）：過期條件併埋見過即清——`day - pendingDay > pendingMaxAge || (seen[pending]||0) > 0`。Case C 真正清走 pending 嗰位：load 補跑 rest 日嗰陣 `advanceDay` tick（day 70、pendingDay 69、age 1 ≤ 2，舊制唔會過期清）。
  3. `wf4TryLocEvent`（P3）：`if(st.pending) return false;` 之前先清見過嘅 pending，唔好一路閘住入場擲骰。Case C 最後一個觸發點（入茶餐廳）。
- 唔郁嘅嘢：once 規則／池 72／頻率 0.03／gap 3／pendingMaxAge 2 全部唔郁；新鮮 pending（未見過）三處都保留（邏輯測試對照覆蓋）；`wf4Fire`／`wf4PickEvent` 唔郁；SAVE key／softRev／`?v=` 唔郁；斷言一個字都冇放寬。
- 驗證：新邏輯斷言 (4b)–(4d) 9 項＋新靜態斷言 3 項全綠（見 §6.1）；三年模擬重跑數字同修法前一字不差（A 62／62、B 47／47、C 41／41、D 42／42，全部 0%——sim 入面 pending 永遠係新鮮，修法零影響）；全套 267／12 零回歸（見 §6.4）；實駕 C 由 FAIL 變 ok（見 §6.6 上文）；反證見 §6.8。

### 6.7 Rebase 紀錄（b3db32f → b104f85，統籌做，接手工人核實）

- 半成品（WIP commit `eb3f0e9`，基底 main `b3db32f`＝v189）由統籌 rebase 上最新 main `b104f85`＝v192；接手嗰陣工作樹乾淨、HEAD 已經係 rebase 後嘅 `eb3f0e9`。
- Rebase 衝突 5 檔行號釘測試（gift185／rom176／tang171／tang173／travel114）由統籌用 difflib 對位解咗（腳本 `qa193/resync193_rebase.py`，映射＋178／＋179 逐個錨點核實，5 檔全部 PASS，冪等驗證通過）。
- 接手工人核實：WF4 池 72 單唯一（day 36／loc 36）、CFG `{pDay:0.03, pLoc:0.03, gapDays:3, locTriesPerDay:3, pendingMaxAge:2}`、`repeatDays` 只剩區塊頭註解一句、seen 守衛在位、新事件 36 單；新測試＋舊測試喺 rebase 後樹上全部 PASS（193 logic／193 static／86 logic／86 static／ui134／dlg108 logic＋static）——即係話 rebase 本身零回歸，唯一缺口就係實駕 Case C（見 §6.6）。
- 本票 Case C 修法淨零行數，rebase 後嘅行號映射唔使再郁。

### 6.8 反證（新／改過嘅測試對 pristine main `b104f85`）

- `test_wf4_193_logic.js`：exit 1，**30 項 FAIL**（唔 crash）——包括 6 項新 Case C 斷言（報紙日／強制日／病日／gap／DailyTick／TryLocEvent stale-clear）＋舊 193 項（CFG／池／once／三年模擬舊制 358 單等）。
- `test_wf4_193_static.js`：exit 1，**TOTAL FAIL 30**（唔 crash）——包括 3 項新 Case C 靜態斷言。
- `test_wf4_86_logic.js`：exit 1，7 項 FAIL；`test_wf4_86_static.py`：exit 1，3 項 FAIL；`test_ui134_wf4scene_static.py`：exit 1，3 項 FAIL；`test_wf4dlg108_static.py`：exit 1，2 項 FAIL；`test_wf4dlg108_logic.js`：exit 1，3 項 FAIL——全部係 v193 改動點，唔 crash。

### 6.9 第二次重驗（基底 b104f85 → 707ff66，2026-11-13 第二次重驗工人）

- **Rebase**：統籌將分支 rebase 上最新 main `707ff66`（v194）；中間落地 v195（`4f47077`）／v198（`22382b2`）／v194（`707ff66`）。第二次 rebase 衝突 5 檔行號釘測試（gift185／rom176／tang171／tang173／travel114），由統籌用 difflib 對位解咗（`qa193/resync193_rebase2.py`，＋178／＋179 逐個錨點核實，5 檔全部 PASS）。Rebase 後 WF4 測試全部 PASS（193 logic ALL PASS、193 static TOTAL PASS、86 logic／86 static、ui134、dlg108 logic＋static）。index.html 總行數 60846（707ff66 係 60667，＋179 係 v193 淨增）。
- **v198×v193 互動（唯一互動點，`wf4TryLocEvent`）**：
  - Code 讀：v193 清 stale pending（L40996）排喺 v198 defer 守衛（L41014，`story165CanPlay`）之前，中間隔住新鮮 pending 閘（L40996 後半）、lastDay（L40997）、baseOk（L40998）、A1（L41002）。**次序正確，唔使調動**——清 stale 係狀態清理，喺任何 early return 之前。
  - 新斷言（(4e)，5 項 logic＋1 項 static，全綠）：強制播 pending＋stale pending 同時存在，入場嗰次 stale pending 清走＋loc 事件照 defer（locTries 仲係 0）；對照：新鮮 pending 保留＋defer；淨強制播 defer 唔計數（v198 行為不變）；冇強制播，stale 清完照擲骰（locTries＝1）。
  - **真打架喺測試唔係 code**：v198 嘅 B1 對照寫死舊頻率／舊池——static「WF4_CFG 機率唔郁」（`pDay:0.30, pLoc:0.20`）＋logic 根因對照（roll 0.1535＜pLoc 0.20、pick 落 boss01、「boss01 之後照出」）。v193 拍板改咗頻率（0.03）＋cafe_cha 池 4→11 單，呢 4 項斷言喺重驗全套嗰陣 FAIL（工作版首次全套 271/14，多咗嘅 2 項正正係 story198 兩個測試；見 `qa193/suite_work193d.txt`）。修法：**唔郁 defer 主修斷言**；對照改寫做頻率／池無關（池收窄到得 boss01 照出；seeded roll 值仲係 0.1535、RNG 冇變；用 day 127 roll 0.0256＜0.03 做確定性例子；static 釘死 v193 新值 pDay／pLoc 0.03）。改完 story198 兩個測試全綠。跟進：drive198 嘅 boss01-after 實駕步驟喺 v193 頻率下同樣唔再確定性出（同一粒 roll），drive193 case E 刻意唔再斷言嗰步（見 §6.6.3）。
- **全套 A/B（新基線自己跑，唔係信數字）**：
  - 基線 pristine `707ff66`（`git archive` 解去 `~/workspace/linji-pristine707ff66`，唔經 /tmp）：**271 PASS／12 FAIL**（FAIL：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38——同 v194 落地話嘅 271/12 一致，`qa193/suite_pristine707ff66.txt`）。
  - 工作版：**273 PASS／12 FAIL，FAIL 清單同基線完全相同，零回歸**（＋2 係新嘅 wf4_193 兩個測試；`qa193/suite_work193e.txt`）。
  - **環境事故（EPERM 風暴）**：全套重跑期間撞正間歇性寫入 EPERM（已知環境問題，MEMORY.md v146 教訓有記）——4 次連續假失敗 119/166（測試 redirect 失敗→未跑就 FAIL，OUT 寫入都 EPERM），另加一次 runtime restart 打斷背景全套（`proc_13a1419c50aa`，做到 `test_name93_logic.js`，全部 PASS）。最後用 stdout 版 runner（`qa193/run_suite193_stdout.sh`，結果印 stdout 唔寫 OUT 檔，背景跑）先攞到真數 273/12，結果存 `qa193/suite_work193e.txt`。教訓：EPERM 風暴期間，測試執行本身多數行得通，死嘅係結果寫入；全套要經 stdout／分塊＋覆跑先攞到真數，唔好信一次 119/166。分塊／重試腳本留檔（`qa193/run_suite193_chunked.sh`、`qa193/run_suite193_retry.sh`），今次最終數字唔係靠佢哋。
- **Sim 重跑**：`node qa193/sim_wf4.js` → `qa193/sim_output_rerun2.txt`，同修法前 `sim_output.txt` **byte-identical**（四路線重複率全部 0%；v198 改動唔影響 sim，因為 sim 冇強制播 pending）。
- **實駕重跑**（`qa193/drive193.py`，本地鏡像 port 8993，LIVE，932／700，約 19 分鐘）：A／B／C／D＋700 smoke 全部 ok，0 pageerror（`qa193/drive193_report.json`；A 三單標題同上次一樣——「化妝間借粉底」day 10、「冰室門口嗰張櫈」day 61、「茶客講睇場費」；C pending null＋seen set03:21；D 零 WF4 modal）。新 case E 見 §6.6.3。
- **反證（新／改過嘅測試對 pristine `707ff66`，乾淨 FAIL 唔 crash；計數係實 FAIL 行，唔計 `FAILURES:` 匯總行）**：193 logic 31 項（包括 2 項新 (4e) 判別斷言；其餘 3 項 (4e) 對照喺 pristine 都 PASS）、193 static 31 項（TOTAL FAIL 31）；86 logic 6、86 static 2、ui134 3、dlg108 static 2、dlg108 logic 2；story198 logic 3 項（原檔寫死 `../index.html` 路徑，直接傳 argv 唔生效——經 scratch copy `qa193/antiproof198/` 真跑 pristine，跑完已刪除）、story198 static 1 項（WF4_CFG v193 新值）。全部係 v193／v198×v193 改動點。

### 6.6.3 實駕 case E（v198×v193 互動，新增）

- 設計：獨立新局 slot 3，C1 電影線 → day 98（第 15 週）＋舊 save 式 stale pending（seen set03:21、pending 指 set03）→ 首次入茶餐廳。
- 首次全 drive 嗰次 E FAIL 係 **drive bug 唔係 game bug**：`run_case_e` 喺入場嗰刻讀故事狀態，但強制播係閂 sheet（`#loc-close` onclick：closeSheet → `story165TryForcedPlay`，L60466）先觸發，入場嗰陣故事未開。WF4 半邊嗰次已經全啱（pending null、locTries 0、冇霞姐 modal）。修正：入場讀 WF4 狀態 → 閂 sheet（加 `close_loc_sheet()`；drive198 都係 open → close_loc → 讀故事）→ 再讀故事。修正後用 `qa193/drive193e.py` 單獨重跑，全綠。
- 重跑結果（`qa193/drive193e_report.json`，截圖 `qa193/shots193/E_story_open.png`）：seed 開 C6F（open `["C6F"]`）；入場 pending null（stale 清走）、locTries 0、wf4title null（boss01 冇打尖）；閂 sheet 後故事 active、act191「第 6 幕・電影線：片場跟班」、nodeTitle「角落嗰張枱」；播完 C6F mark done（c6f: true）；0 pageerror。主報告 `qa193/drive193_report.json` 嘅 E 項已換成重跑結果（附註寫明首次 FAIL 原因）。
- 刻意唔斷言：播完 C6F 再入茶餐廳 boss01 即出——v193 pLoc 0.03 之下，v198 嗰粒 seeded roll 0.1535 過唔到，boss01 唔出係頻率所致，唔係 defer 爛咗（同 story198 logic 改寫同一原因）。

## 7. 檔案清單

- 改：`index.html`（WF4 引擎＋36 新事件＋覆寫表 18 行＋放寬 3 個條件閘；對 `b3db32f` 淨 ＋179 行；Case C 修法淨零行數，見 §6.6.2）
- 改：`tests/test_wf4_86_logic.js`、`tests/test_wf4_86_static.py`、`tests/test_ui134_wf4scene_static.py`、`tests/test_wf4dlg108_static.py`、`tests/test_wf4dlg108_logic.js`（見 §6.2）、`tests/test_travel114_static.py`、`tests/test_rom176_static.py`、`tests/test_tang171_static.py`、`tests/test_tang173_static.py`、`tests/test_gift185_static.py`（resync，見 §6.3）
- 新：`tests/test_wf4_193_logic.js`、`tests/test_wf4_193_static.py`
- QA：`qa193/sim_wf4.js`、`qa193/sim_output.txt`、`qa193/sim_output_pristine_ref.txt`（調查員原輸出，供對照）、`qa193/new_events193.js.txt`（36 新事件原文）、`qa193/resync193.py`、`qa193/resync193_rebase.py`（rebase 5 檔 difflib 對位，見 §6.7）、`qa193/drive193.py`、`qa193/drive193_report.json`、`qa193/drive193.log`（修法前舊 drive 記錄）＋`qa193/drive193_final.log`（修法後最終 drive 全綠記錄）、`qa193/shots193/`、`qa193/suite_pristine193.txt`、`qa193/suite_work193b.txt`（rebase 前）、`qa193/suite_pristine193b.txt`＋`qa193/suite_pristine193b.log`（rebase 後基線 265/12，見 §6.4）、`qa193/suite_work193c.txt`＋`qa193/suite_work193c.log`（最終樹 267/12）、`qa193/probe193.py`（開局流程探測，唔係正式驗證）、`qa193/probe193c.py`＋`qa193/probe193c.json`（Case C 初探：window wrap 失效，見 §6.6.1）、`qa193/probe193d.py`＋`qa193/probe193d.json`＋`qa193/probe193d.log`（忠實重跑重現 C FAIL）、`qa193/probe193e.py`＋`qa193/probe193e.json`＋`qa193/probe193e.log`＋`qa193/build_probe193e.py`（source-level instrumentation，根因鐵證；instrumented copy 喺 `/tmp/wf4probe193/`，唔入 repo）
- **第二次重驗新增（見 §6.9／§6.6.3）**：`qa193/resync193_rebase2.py`（第二次 rebase 5 檔 difflib 對位）、`qa193/suite_pristine707ff66.txt`（新基線 271/12）、`qa193/suite_work193d.txt`（工作版首次全套 271/14，story198 兩項 FAIL——v198×v193 測試衝突證據）、`qa193/suite_work193e.txt`（工作版最終全套 273/12）、`qa193/sim_output_rerun2.txt`（sim 重跑，byte-identical）、`qa193/run_suite193_retry.sh`／`qa193/run_suite193_chunked.sh`／`qa193/run_suite193_stdout.sh`（EPERM 風暴期間嘅全套 runner；最終數字靠 stdout 版）、`qa193/drive193e.py`＋`qa193/drive193e_report.json`（case E 單獨重跑，全綠）、`qa193/shots193/E_story_open.png`（E 故事開場截圖）、`qa193/shots193/A_d61_cafe_cha_wf4_2.png`（重跑 A 第二單）
- 改：`tests/test_story198_logic.js`、`tests/test_story198_static.py`（v198×v193 測試衝突改寫，見 §6.9——B1 defer 主修斷言唔郁）

## 8. 殘留／跟進（唔喺本票）

1. Phase 2 擴池（見 §3.3）：loc 每地點 8–10 單（約 ＋30 單）＋day 45–50 單（約 ＋10–14 單），之後頻率可酌量調返高＋模擬重掃。
2. eventLine 3 句跨池重複（見 §5）：要另開一票做載入覆寫，唔直改 pack JSON。
3. 頻率代價：事件密度由每 3.2 日一單跌到約每 13–19 日一單（一年 A 路線 28 單）。如果用戶覺得太疏，唔好齋調返高頻率——要連 Phase 2 擴池一齊做，否則抽乾會提早。

## 9. 接手統籌第三次重驗＋落地前核實（2026-11-14，基底 6c207a6＝v202）

上一手統籌 `f2efa98b` 07:27 中斷（rebase 完、跑緊測試嗰陣斷；08:30 resume 返唔到，transcript 停喺 07:13），改派接手統籌。半成品：分支 `v20a193` 已經 rebase 上 `6c207a6`（舊 hash `2d6c1dd`／`6314dfc` → 新 hash `15f81bd`／`304eaf4`，commit 訊息一樣），工作副本有未 commit `M index.html`（07:13）。

### 9.1 未 commit 改動逐行核實（保留，行為零改動）
- 四處 `st.seen &&` 守衛（`wf4PickEvent`／`wf4DailyTick`／`wf4TryLocEvent`／`wf4PresentPending`）：`wf4Ensure()` 保證 seen 恒為物件（無就補 `{}`），四處呼叫點都先行 `wf4Ensure()` 且 null 即返——守衛係防禦性 no-op，行為唔變。
- `wf4PresentPending` 刪去 Fen farewell 之後嗰行 `if(!st.pending) return false;`：`wf4PresentFenFarewell` 從來唔掂 `st.pending`（只寫 `fenFarewellDone`＋`S.wf4FenFarewell`），函數頂部已驗過 pending 非空，呢行係 dead code；就算 `StoryPlay.start` 間接清咗 pending，之後 `find(ev)` 回 undefined 一樣會清走＋return false。行為不變。
- 已獨立 commit：`d9a9bce`「v20a193 硬化：seen 守衛＋刪 dead pending re-check（行為零改動）」。

### 9.2 「19 FAIL」調查結論：假警報，全套零回歸
- `qa193/suite_work193f.txt`（07:11）寫 TOTAL PASS 277 FAIL 19，比 v202 基線 282/12 多 7 個 FAIL；同一時間嘅 pristine `suite_pristine193d.txt`（07:09）係 281/13。
- 19 個 FAIL 入面 13 個同 pristine 完全一致（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38——全部 pre-existing）。
- 其餘 6 個（dayflow196_logic.js／gift185／rom176／tang171／tang173／travel114）逐個直接跑**全部 PASS**。根因：07:11 全套跑緊嗰陣，上一手統籌同時改緊 `index.html`（07:13 改完），suite 讀到半寫緊嘅檔案——同 v151 教訓同一類環境波動，唔係回歸。
- **重跑全套（`qa193/run_suite193_chunked.sh`，最終樹連硬化 commit）：TOTAL PASS 283 FAIL 13（`qa193/suite_work193g.txt`），FAIL 清單同 pristine 逐項一致，零回歸。**＋2 PASS 係新 wf4_193 測試；pristine 本身 281/13 vs v202 嗰陣 282/12，基線自己都浮動 ±1（v151 教訓）。

### 9.3 頻率模擬獨立重跑
- `node qa193/sim_wf4.js`（遊戲本身 WF4 code eval，唔係重寫邏輯）：重複率 **0.0%**，每單最多見 1 次；day 池 36／loc 池 36＝72 單；day 池抽乾日 990、loc 抽獎 15 次；tvb_longmen 4 單 day 125 抽乾（單一地點常客結構性限制，見 §3.3，Phase 2 先補）。數字同工人 `sim_output_rerun2.txt` 一致。

### 9.4 v198×v193 互動獨立核實（code＋實駕）
- code 次序（最終樹）：`wf4TryLocEvent` 入面 Case C 清 stale pending 行喺最前，之後先係 v153 A1 守衛（`enc79StoryPendingAt`）同 v198 B1 守衛（`story165CanPlay()`），兩守衛 defer 都唔計 `locTries`。次序正確，唔使調動。
- `test_dayflow196_logic.js` (h) 段（forced 日／allowForced／Fen afterCont）單獨重跑 ALL PASS。

### 9.5 實駕（接手統籌親自跑，`qa193/drive193.py`，最終樹，LIVE 模式，932／700）
- 瀏覽器執行檔舊路徑失蹤（`/home/hatch/pw-browsers/chromium_headless_shell-1248/...` 得返支援檔、無 binary），`playwright install chromium-headless-shell` 重新下載同一版本 v1248 到 `~/.cache/ms-playwright/`，drive193.py 嘅 EXE 路徑已改過去（qa 工具改動，唔入遊戲）。
- **A–E＋700 smoke 全部 PASS，errors／http_fail／errors_932／errors_700 全部空**（`qa193/drive193_report.json`，2026-11-14 02:32 UTC）：
  - A：34 日，3 單唔同事件（電話亭長龍／唱片舖試聽嗰首歌／鄰居借電話），seeded 見過嗰 4 單 0 漏出。
  - B：reload 後 seen 8 → 8。
  - C：舊 save（seen set03:21、evDay 舊紀錄、pending 指 set03）遷移 0 pageerror，pending 清走（null），seen 保留。
  - D：seed seen＝全部 72 單，行 2 日＋入兩個地點，零 WF4 modal、0 pageerror。
  - E：day 98／第 15 週，stale pending（set03:21）清走，C6F「第 6 幕・電影線：片場跟班」即播完成，boss01 唔打尖（wf4title null），locTries 仲係 0。
