# NOTES_V20A213 — 請柬提前 3 日＋典禮改晚上播

- 分支：`v20a213`（基底 main `f58f19c`，v208；唔落地，落地由統籌做）
- 拍板：用戶 2026-11-14 18:07「提前3日，典禮改晚上播」
- 落地次序（2026-11-14 晚更新）：v212 → v209 → v213 → v214（v211 已上線，遊戲 `7704ce3`＋NOTES `b1ca47a`）
- 唔郁：SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、`?v=`（`v20a10`）、
  content pack JSON、典禮內容（提名／得獎／計分／贏線 0.875）、報紙翌日規則（`publishDay: day+1`）、
  C10 anti-stack、獎項表、晨鏈其他環節。

## 1. 改咗乜

**請柬提前 3 日**：請柬日＝典禮日 − 3 日（金碟夜 6 月 1 號→請柬 5 月 29 號到；
台慶 12 月 1 號→11 月 28 號到）。`queueAwardsOnSeasonWindow` 改用窗口
`[ceremonyDay−3, ceremonyDay]` 做閘，唔再用 `awardsSeasonMatches`（請柬日仲係上一季，
舊季節配對會擋）；`awardsWeekOk` 照留做雙保險；`forceCeremonyId`（debug／自檢探針）
跳過窗口＋週數，同舊制一致。窗口過咗（從來冇排過）就嗰屆靜默錯過，唔寫旗標，
下一屆用唔同 year 鍵，唔會誤擋。

**決定＝預約，唔係即播**：請柬「出席／推辭」而家只係寫低決定，存入
`S.awardBooked213`（＋session 鏡 `FREEPLAY_FW._awardBooked213`）
`{ceremonyId, year, ceremonyDay, decision, pack}`，清 `_pendingAward`／`S.pendingAwardPack`；
旗標留返 `"invited"`（防重排）。`onDismiss`＝推辭預約。決定咗之後
`queueAwardInvite`／`restorePendingAward136` 唔會重建／重彈請柬。

**典禮改晚上播**：典禮日玩家照常返工／拍攝，收工之後先播（v208 逐格流程不變）。
兩個晚間掛點（one-shot，播之前清預約，防重入／雙掛點重播）：
- (a) `morningChain196` 開頭（行晨鏈之前）——覆蓋地圖／休息／病假／加速靜默日；
- (b) `resolvePlannedDay` 尾——`nextNb` 包咗 `awards213EveningThen`，殺青結算＋
  殺青日結板（＋殺青獎勵 sheet，經 `afterDayRes`）行先，之後先播典禮，再跑下一日／返地圖。
  呢個掛點亦覆蓋週末（典禮日係星期日嗰陣日結板係「回家結算」，一樣經 `nextNbReward` 入 hook）。
  到期條件係 `ceremonyDay < S.dayIndex`（典禮日已完）；已入 log（done／skipped）唔重播；
  典禮進行中唔重入。出席＝現場版（播完出結果卡）；推辭＝電視直播版（v165 行為原樣抽出，
  播完入 log＋第二日報紙 declined 版，唔出結果卡）。

**報紙**：`enqueueNewspaperFromAward` 用 `FREEPLAY_FW._awardCeremonyDay213`
（晚間播嗰陣設、播完清）做 `day`，所以 `publishDay = ceremonyDay+1`（唔係播出嗰刻
`dayIndex+1`）；冇 override 嗰陣照舊。報紙流程本身（`pullDueNewspaperEdition`／
`presentDueMorningPaper`／`newspaperDueItems`）一字唔郁。

**請柬文案加日期錨**：有 stamp 嘅 pack（`pack.ceremonyDay213`／`pack.inviteDay213`）
顯示 `典禮夜：6月1日（星期五）` 行，gallery 行寫 `6月1日獎項：…（觀禮）`，
閘句寫 `6月1日席位：觀禮。…`。冇 stamp 嘅 pack（合成／測試 pack，
直接經 `buildAwardResultPack` 起）跌返舊字 `今晚獎項：`／`今晚席位：觀禮。`——
刻意保留，令舊測試 `test_awards192_logic.js`／`test_awards200_logic.js`／
`test_awards200_static.py`（逐字期望 `今晚獎項：`）唔使郁。

**典禮日係關鍵日**：`isCriticalPlanDay` 喺 `awards213BookedForDay(S.dayIndex)` 嗰陣返 true，
週加速唔會靜默合併典禮日，日結板一定要停低出。

**其他**：`awardsDebugForceSeasonWindow` 而家一併清 `S.awardBooked213`（force 重排唔會俾預約擋住）；
`window.__awards` 加咗 `booked213`／`playEvening213`／`ceremonyDay213` 暴露。
`awards213CeremonyDay(ceremony, year)` 用月份表 春3／夏6／秋9／冬12 計季節首日；
1990–1992 典禮日（dayIndex）：春 59／424／790、夏 151／516／882、秋 243／608／974、
冬 334／699／1065。

## 2. 舊存檔遷移

已有存檔入面嘅舊制 pending 請柬（舊制當日彈出嗰種，`pack.dayIndex`＝典禮日），
經 `restorePendingAward136` 照舊還原，唔會唔見、唔會爛。玩家決定嗰陣，
`awards213CeremonyDayForPack` 由屆別（ceremonyId＋year）計返季節首日做典禮日，
再 clamp 到 `max(計出嚟嗰日，今日）`——過期 pack（典禮日已過）預約典禮日＝今日
（即係今晚），典禮照開，唔會開唔到。已預約嘅屆別唔會重排／重彈。
未知 `ceremonyId` 嘅 pack（例如頁內自檢 fake invite `award_test_invite`）保留舊制即播行為，
自檢唔郁。

## 3. 測試

### 新測試（全部 ALL PASS＋反證）
- `tests/test_awards213_logic.js`：**46 項 PASS**（典禮日數學 1990–1992 四季、
  預約 attend／decline／dismiss、合成 pack 即播舊路、queue／restore 已預約唔重排、
  `isCriticalPlanDay`、進行中／已入 log 唔重播、舊存檔還原＋過期 pack 預約今日、
  真 `enqueueNewspaperFromAward` publishDay 152 vs 153、有 stamp／冇 stamp 文案）。
  反證：pristine main **5 項 FAIL**（乾淨 FAIL，唔 crash）。
- `tests/test_awards213_static.py`：**36 項 PASS**（窗口、預約、兩個晚間掛點、報紙 override、
  文案、唔郁嘅嘢：贏線 0.875、SAVE key、softRev s107、`?v=v20a10`、C10 anti-stack）。
  反證：pristine main **5 項 FAIL**（乾淨 FAIL，唔 crash）。

### 舊測試更新（行為改動令舊斷言過時，唔係回歸）
- `tests/test_awards194_logic.js`：**29 項 PASS**（queue 日子搬入窗口：春 day 56、夏 148、
  冬 334；加太早 day 55→0、窗口過咗 day 60→0；force case 留喺 day 335 證明 bypass）。
  反證：pristine **3 行 FAIL**。附帶教訓：test 檔 IIFE 入面 `var` 唔會漏出去，
  const 抽取要用頂層直接 `eval`；`AWARDS213_SEASON_MONTH` 要同 `AWARDS213_LEAD_DAYS`
  一齊抽，唔係 `awards213CeremonyDay` 會經 try/catch 靜默返 null。
- `tests/test_awards78_edition.js`：**18 項 PASS**（端到端日子搬入窗口：冬 1990 day 334、
  冬 1991 day 699、春 1991 day 424；C10 deferral 重寫：窗口內 defer 照出同屆，
  窗口過咗 day 365 唔再遲開）。反證：pristine **1 項 FAIL**。
- 唔郁嘅舊 awards 測試照舊 PASS：`test_awards200_logic.js`、`test_awards192_logic.js`、
  `test_awards200_static.py`、`test_awards194_static.py`、`test_dayflow196_static.py`、
  `test_gate136_static.py` 全部 ALL PASS。

### 全套 A/B（`qa131/run_suite.sh`，兩個參數）
- A 基線（pristine main `f58f19c`，`qa213/suite_pristineA.txt`）：**TOTAL PASS 293 FAIL 13**
  （13 項全部 pre-existing：flash51／giglib36／pacing35／poster59／rumor49／slot50／
  soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38 static）。
- B 工作版（未 resync，`qa213/suite_workB.txt`）：**TOTAL PASS 288 FAIL 20**——
  新增 7 項全部係行號漂移／體積記帳（gift185／poster85／rom176／tang171／tang173／
  travel114／ux68），唔係行為回歸。
- Resync（`qa213/resync213.py`，difflib 對位 `/tmp/pristine213.html` vs 工作版 index.html）：
  index.html 淨 **+199 行**（61,714→61,913 行；5,478,389→5,491,267 bytes，+12,878），
  non-equal opcodes 全部喺已知改動區（晨鏈 ~L38277／resolvePlannedDay ~L38600／
  awards213 block ~L46800／presentAwardInvite ~L46991／gate 行 ~L47375／報紙 override ~L49131），
  全部釘行內容逐字相同（純漂移）。7 檔 resync：travel114 COUNT 12／FREE 33／DEF 56186→56385／
  WRAPPER 45180→45192；rom176 4 釘＋199；tang171／173 總行數 61714→61913、DEF 56385；
  gift185 總行數 61913；poster85 體積基線 5,448,954→5,491,267（＋40,000 slack 不變）；
  ux68 體積上限 5,490,000→5,500,000（有意增長附註）。
- C 工作版（resync 後，`qa213/suite_workC.txt`）：**TOTAL PASS 295 FAIL 13**——
  FAIL 清單同基線 A **逐項相同**（13 項 pre-existing），PASS 293→295（＋2＝兩個新測試）。
  **零回歸**（全套總數會波動，判斷用穩定 FAIL 清單＋受影響測試逐個直接覆驗）。

## 4. 實駕（Playwright，本地鏡像 port 8913，`qa213/drive213.py`，報告 `qa213/drive213_report.json`）

播種：經 new_game 正常開局 slot 3，真實 gigId 播種 wrapHistory（廣告×2／電視×3／綜藝×1／
唱片×2／電影×2，fame 30／credit 52）。**5 場全部 PASS，0 pageerror。**
實駕期間發現兩個 drive 流程問題（已修，唔係 game code 問題）：C1／C2 強制劇情會喺晨鏈
自動彈出擋住地圖掣（settle 要撳「跳至選項」＋抉擇先過到）；`#modal` 長駐 DOM，
modal 可見性要用有冇文字判，撳掣要限定 `#modal` 範圍（否則誤撳地圖「開始今日行程」）。

- **A. 請柬提前（金碟夜 1990）**：day 148（5 月 29）請柬彈出，寫
  「典禮夜：6月1日（星期五）」，席位入圍／提名，爭最佳新人獎＋最佳男歌手，
  憑《夜更和音》爭獎。撳出席 → 冇即播（stage 唔出），預約 attend、ceremonyDay 151，
  旗標 `1990/award_golddisc_music: invited`。截圖 `qa213/shots213/A_invite_148.png`。
- **B. 晚間出席（續 A）**：典禮日 6 月 1（day 151）休息日結卡「休息（週五）」先出，
  撳「開始今日行程」＋確認 → 典禮舞台先出（`.awd62-stage`，最佳新人獎格，跳過掣在場），
  跳過 → 結果卡「收下這晚」→ 翌日晨報（1990/6/2，頭條「星河金碟夜入圍名單出爐」）→
  地圖。終態 dayIndex 152（典禮唔耗日），預約已清，awardsLog 有
  `award_golddisc_music` dayIndex 151（skipped false），剪報 1。截圖 `B_stage.png`／
  `B_result.png`／`B_paper_152.png`。
- **C. 推辭 → 電視直播版**：請柬日推辭 → 預約 decline，唔即播；典禮日晚上播電視直播版
  （stage 出、跳過得），**唔出結果卡**，log skipped＝true，declined 報紙翌日出
  （頭條「駱家聲憑《熱浪之夏》奪獎」），day 152，剪報 1。
- **D. 撞殺青**：典禮日同時係電影《陰陽夜更》殺青日。殺青日結板
  「殺青：《陰陽夜更》動作替身」先出（settle trace 錄到），撳「開始今日行程」→
  殺青獎勵 sheet（「收下這份反響」）→ 典禮 → 結果卡 → 翌日晨報。終態 wraps 9→10、
  log dayIndex 151、獎報紙剪報 1、殺青報紙排咗 publishDay 153。兩樣冇互相吞、冇 modal 打架。
- **E. 窗口前＋全鏈請柬**：day 147（5 月 28）`present()` 返 false，冇請柬；
  day 149 經真 UI 鏈（地圖→開始今日行程→日結板→返回地圖→晨鏈）彈出請柬，
  寫「典禮夜：6月1日（星期五）」，撳出席 → 預約 attend、ceremonyDay 151。
- **F. 星期日報紙（台慶 1990）**：請柬 11 月 28（day 331），典禮 12 月 1（星期六，
  day 334）晚上播，結果卡後翌日 12 月 2（**星期日**）晨報即刻出
  （頭條「星河台慶夜 鍾楚凝憑《街角繁華夢》奪獎」，日期 1990/12/2），
  12 月 3 唔再重出。星期日晨報冇遲到。

### 星期日典禮（v192 C1）針對性對照（`qa213/drive213_sunday.py`，台慶 1991，典禮日 12 月 1 星期日 day 699）
- work：請柬 11 月 28（696，典禮夜：12月1日（星期日））→ 週末日結板「休息（週日）／
  一週完結 → 回家結算」→ 撳「回家結算」→ 晚間典禮播（stage 出）→ 結果卡 →
  log dayIndex 699、旗標 done；獎報紙已排 `publishDay 700`（週一）、`enqueuedDay 699`。
- pristine 對照：舊制請柬 699 當日朝早，撳出席即播（stage 即出），結果卡，獎報紙同樣已排
  `publishDay 700`、`enqueuedDay 699`。
- **報紙週一出街嗰刻，兩邊都未直接觀察到**：典禮日係週日，播完要經週結算（回家結算→
  新一週 planning，`homeEditable=true`、`todayPlan=null`、地圖冇「開始今日行程」掣），
  drive 停喺 planning 嗰步，未開到週一（`#home-back-map-tabs` 係純粹返地圖，
  `book70ExitHome` 唔行晨鏈，所以返地圖唔會出報紙）。兩邊終態完全一致：
  獎報紙仲喺 queue（publishDay 700）、剪報 3 張全部係 WF3 世界報紙（唔係獎報紙），
  **v192 C1 原封不動——冇惡化，亦冇（順便）修好**。報紙呈現本身（`pullDueNewspaperEdition`／
  `presentDueMorningPaper`／`publishDay` 計法）係 v213 完全冇郁嘅 code，
  排報數值兩邊相同，週一開日嗰陣晨鏈會照舊派返。跟進：落地後若要實證，補一場由
  planning 確認行程→開週一→睇報紙嘅實駕（drive 導航問題，唔係 game 問題）。
- 附帶：邀請文案入面「碟市」／「臨記席」等字眼係 pre-existing 模板字（v214 報紙重做範圍），
  唔係 v213 改出嚟嘅，呢票唔郁。

## 5. 落地注意（rebase 上最新 main）

- **基底係 v208（`f58f19c`）**：v211（舞台幾何 480×540，雙幾何 ×1.25；已上線
  `7704ce3`／NOTES `b1ca47a`）同 v212（逐格流程修復：glamour 收跳過掣、得主去重、
  格標題預淡入剪影＋`applyCatState208` 隱形根因、卡片字幕同步、光柱＋行前、walkup 讓路、
  兩位提名人置中；落地進行中）**唔喺呢個基底入面**。落地次序 v212 → v209 → v213 → v214。
- Rebase 嗰陣預期衝突區：`presentAwardInvite`／`queueAwardsOnSeasonWindow`／
  `morningChain196`／`resolvePlannedDay` 嘅 `nextNb`／`enqueueNewspaperFromAward`／
  `awards62GateLineHtml` 附近（v212 改逐格流程、v211 改舞台幾何）。
  落地後要對一次：slotCx／FLOOR／卡列幾何（v211 480×540）、逐格 beats 次序（v212）、
  典禮日關鍵日邏輯同加速互動。
- Rebase 後重跑：`test_awards213_logic.js`＋`test_awards213_static.js`＋
  `test_awards194_logic.js`＋`test_awards78_edition.js`＋全套（對 FAIL 清單，唔齋信總數）。
  靜態測試行號釘會再漂移，用 `qa213/resync213.py` 嘅 difflib 做法對位（唔好手估行號）。
- Pristine 對照 worktree `~/workspace/linji-pristine213`（基底 `f58f19c`）用完即刪
  （清機規則；呢票完咗先刪）。

## 6. 檔案

- `index.html`（淨 +199 行，61,714→61,913；5,478,389→5,491,267 bytes）
- `tests/test_awards213_logic.js`（新，46 項）、`tests/test_awards213_static.py`（新，36 項）
- `tests/test_awards194_logic.js`、`tests/test_awards78_edition.js`（更新）
- `tests/test_gift185_static.py`、`tests/test_poster85_static.py`、`tests/test_rom176_static.py`、
  `tests/test_tang171_static.py`、`tests/test_tang173_static.py`、`tests/test_travel114_static.py`、
  `tests/test_ux68_static.py`（resync 行號／體積上限）
- `qa213/resync213.py`、`qa213/drive213.py`、`qa213/drive213_sunday.py`、
  `qa213/drive213_sunday_diag.py`、`qa213/suite_pristineA.txt`、`qa213/suite_workB.txt`、
  `qa213/suite_workC.txt`、`qa213/drive213_report.json`、
  `qa213/drive213_sunday_report_work.json`、`qa213/drive213_sunday_report_pristine.json`、
  `qa213/drive213_sunday_diag.json`、`qa213/shots213/`（14 張截圖）

## 7. 落地紀錄（rebase＋重驗＋上線，2026-11-14）

- **Rebase**：分支 `v20a213` 由舊 main `f58f19c` rebase 上最新 main `17c6f69`
  （v211＋v212＋v209 已上線），新 HEAD `3f3be53`，47 檔改動。index.html 自動合併，
  零內容衝突；5 個 static 測試行號漂移（gift185／rom176／tang171／tang173／travel114）
  全部係純行號漂移，已用 difflib 對位解好（`qa213/resync213_rebase.py`、
  `qa213/resync213_rebase2.py`，amend 入 commit）。
- **Resync 過程捉到 4 隻腳本 bug（全部已修，證據在案）**：
  ① resync 衝突解析 regex 用 `^>>>>>>>.*\n` 配 `re.S`，貪婪 `.*` 吞到檔尾，
  截斷咗 4 檔（gift185 54 行／rom176 91 行／tang171 94 行／tang173 91 行）；
  用 `git checkout -m` 還原返衝突版，pattern 改做 `[^\n]*`＋接受 `ours`／`theirs` 標籤。
  ② `sub_pins()` 逐個 str 取代造成級聯（31005→31006 再被換成 31007，重複值）。
  ③ travel114 FREE 集因合併切分漏咗 30995 針（HEAD hunk 29 針、theirs hunk 28 針，
  合併後得 32 針）。
  ④ `sub_block` 用 keepends 丟失換行，整爛 FREE 區塊；已還原重做。
  教訓：resync 腳本唔好用 `"}"` 做 end marker（撞 FREE 註解 `{travelFree}` 嘅 `}`）；
  `git rebase --continue` 絕對唔好 pipe 去 head；用 `GIT_EDITOR=true`。
- **釘行地面真相（實測）**：`openLoc` DEF 行——f58f19c 56186／main 17c6f69 56267／
  e81027e 56385／rebased 56466（v211＋v212 共 +81、v213 +199）。留意：v212 留低嘅
  tang171／173 標籤文字話 DEF 56225 係 stale（assertion 本身用 56267，啱嘅）；
  travel114 HEAD 嘅 DEF 56267 係啱嘅。
- **第二輪 resync（`qa213/resync213_rebase2.py`）**：以 HEAD（:2:，main）33 針為準重建
  travel114——HEAD 映射同 theirs 映射**完全一致**（FREE 33 針唯一、COUNT 12 針唯一、
  DEF 56466、WRAP 45200）；rom176 標籤改返啱（L54896／L55264／L56403／L56497）。
- **ux68 體積上限（rebase 後新 FAIL，唔係行為回歸）**：rebased index.html 5,500,561 bytes，
  過咗 v213 設嘅 5,500,000 上限（v213 單獨 5,491,267；rebase 帶入 v211＋v212 嘅
  +9,294 bytes）。上限改 5,500,000→5,510,000（slack ~9,439，同 v213 原本 ~8,733 相若），
  附註加「v211＋v212 rebase 上 main 17c6f69 有意增長至 5,500,561」。
- **重驗（rebased 版 `3f3be53`＋ux68 修正）**：
  - 5 個 resync 檔全綠；213 logic 46＋static 36 全綠；194 logic、78 edition、200 logic、
    192 logic、200 static、194 static、dayflow196、gate136 全部 ALL PASS。
  - 關鍵錨點齊：HSC211×16、`cardsInnerHtmlFor208`×3、glamour-hide×4、`used212`×6、
    `preview212`×4、`awardBooked213`×10、`awards213EveningThen`×2、
    `awards213CeremonyDay`×8、`_awardCeremonyDay213`×5、`ceremonyDay213`×8、
    `queueAwardsOnSeasonWindow`×10。主 inline script 4,450,253 bytes，`node --check` 通過。
  - 全套 A/B：基線（pristine main `17c6f69`）**297／13**；工作版 **299／13**
    （＋2 新 213 檔；13 項 pre-existing FAIL 逐項相同：flash51、giglib36、pacing35、
    poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、
    wf5_87、wrap38）。零回歸。
  - 實駕重跑（`qa213/drive213_rebased.py`，報告 `qa213/drive213_rebased.json`，
    截圖 `qa213/shots213_rebased/` 13 張）：5 場全 PASS，0 pageerror、0 console error、
    0 http fail。A/B 金碟夜：day 148 請柬「典禮夜：6月1日（星期五）」→出席預約
    ceremonyDay 151→典禮日休息日結卡先出→晚上舞台→結果卡→翌日晨報 1990/6/2，
    終態 day 152 唔耗日。C 推辭：電視直播版、唔出結果卡、declined 報紙翌日出、
    flag `skipped`。D 撞殺青：殺青板＋獎勵 sheet 行先→典禮→結果卡→晨報，
    wraps 9→10，殺青報 publishDay 153（日＋2）。E day 147 無請柬、day 149 經真 UI 鏈
    彈出請柬。F 台慶 1990：典禮週六晚播、星期日晨報 1990/12/2 即刻出、12/3 唔重出。
    D 場 `wrapBoardSeen`／`wrapRewardSheet` 兩旗係探針時序假象（run_day_via_map 嘅
    settle 迴圈入面已經見到並撳咗殺青板＋「收下這份反響」，trace 有證；終態同
    rebase 前一致）。F 場 day 336 `settleOk: False` 係探針未行完當日故事（「回家結算」），
    唔係遊戲錯；關鍵斷言（335 出報、336 唔重出）已驗。
- **上線**：遊戲 commit `4183d77`；線上 5,500,561 bytes，
  sha256 `ef52d2fe7dcc45ac072c307e9b8104be03fae83e8243aa1e09602509eb35b342`，
  curl 核實同 repo HEAD 一致（push 後約 4 分鐘傳播到 Pages）。NOTES commit 見 git log。
- **落地後跟進**：星期日典禮 v192 C1——補一場由 planning 確認→開週一→睇報紙嘅實駕，
  驗證週一報紙出唔出到（見 §4／§5）。
