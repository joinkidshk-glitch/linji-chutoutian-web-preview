# NOTES_V20A196 — 日流程自動連跑＋故事播放鎖死返地圖

> 基底：main `2760680`（v191 NOTES，遊戲 `f2a6b0c`），調查日 2026-11-13。
> 用戶硬規則兩條（2026-11-13 21:03／21:05 親自拍板）：
> 1. **如果當日安排咗行程，跑完就自動去下一日安排咗嘅行程；如果下個行程係逛逛，咁先去大地圖。**
> 2. **交代劇情嗰陣，更加唔可以無故返地圖**（故事播放期間鎖死所有返地圖路徑，只可以經場景本身流程完結先離開；「跳至選項」唔計，唔郁佢）。
>
> 落地次序注意：v192／v193／v195 進行緊，實作前先 rebase 上最新 main；行號以基底為準，實作嗰陣動態定位。

## §0 設計決定（統籌拍板，工人照做唔好重問）

- **D1 日結板過渡**：結果板照出（唔可以靜靜吞咗結果）。下一日有排程 → 板上只留一粒主掣（沿用現有文案：「開始今日行程」forced／soft 日；休息卡沿用休息卡掣），dismiss（撳走 modal）＝同一去向（繼續跑下一日）。下一日係逛逛 → 「返回地圖」照出，dismiss＝返地圖。**唔做定時自動跳頁**（玩家要睇結果，唔可以未睇就跳走）。week-accel 緩衝合併維持 opt-in，唔做預設流程。
- **D2 晨鏈搬位**：`runScheduleFromToday()` 非 mapish 分支改行**全晨鏈**（而家只行報紙＋試鏡消息），continuation＝跑當日行程；`goToMapForBrowse()` 保留全鏈，continuation＝落地圖。晨鏈項目：朝早報紙 → 試鏡消息 → 頒獎請柬 → WF4 → 病假前置（病假頭閘已喺 `resolvePlannedDay` 頭，唔使搬）。WF4 要加 continuation 參數（預設 `goToMapForBrowse` 保舊行為）。
- **D3 強制播續鏈**：強制播（`story165TryForcedPlay`）喺晨鏈尾跑；播之前記低「播完續鏈」slot（例如 `FREEPLAY_FW._story165AfterCont`＝跑下一日／落地圖，按新規則計），`showResult` 嘅「關閉」／onDismiss 消費呢個 slot；「下一節」會播下一幕，slot 要留到成條鏈播完先消費，唔好第一幕完就消費咗。
- **D4 故事鎖死**：`render()` 唔再按 `lockedForced` 分流——**所有故事播放期間一律唔出「先返回」，onDismiss 一律重開畫面**（即係而家 lockedForced 嗰條路）。「跳至選項」唔郁（`stay:true`，場景內跳前）。`spSoftSeedCanDismiss()` 嘅 dismiss 能力喺播放期間同樣鎖死（offer 階段先可以拒絕，播咗就唔可以中途走）。
- **D5 手帳出口唔郁**：`book70ExitHome`／`#home-back-map-tabs`／`leaveHomeFromNotebook` 唔郁——手帳只喺逛逛日／週末先入到（排程日自動連跑，玩家唔會喺排程日中途入手帳）。`#home-back-map` 喺地圖模式下 `display:none`，bypass 係潛在唔係現實，今次唔郁（v165 NOTES §9.4 殘留照舊，等用戶決定）。`#loc-close` 唔郁（地點 sheet 內部，已經喺地圖）。
- **D6 週末／病假／accel／save 唔郁**：`ended` → `enterHome(summary, true)` 照舊；病假頭閘（`hosp96TreatGate`／`conseq61ResolveSickDay`）照舊，但病假日結板（行 `afterDayModal` 預設）嘅 dismiss／掣要跟新規則；week-accel 流程照舊（佢已經係自動連跑，critical 日停低）；每步 `saveQ()` 照舊；`S.awardsFlags`／頒獎請柬數據／C17 結局閘唔郁。
- **D7 「逛逛日」判定**：沿用現有 `nextIsMap` 邏輯（`dayEndContinueButtons` L38020–38025）：`!nextId || isMapDay(nextId) || wrap: || audition:`。抽成共用 helper（例如 `nextDayIsMap()`）畀三處（`dayEndContinueButtons`、`afterDayModal` dismiss、休息卡）共用，唔好三份複製。注意 `wrap:`／`audition:` 係歷史標記（`todayPlanId()` 即時改返 `scout_all`），但判定要保留佢哋做 mapish（防禦性）。

## §1 調查結論：逛逛日係乜（全部對住基底核實）

- `isMapDay(id)`（L36220）：`scout_all`／`scout_nt`／`scout_kln`／`scout_island` 先係逛逛日。
- `todayPlanId()`（L37654）：返 `S.weekPlan[weekdayIdx]`；`wrap:`／`audition:` 即時改返 `scout_all`；已死嘅 `shoot:` 殘留都改返 `scout_all`。返 `null`＝冇計劃＝地圖日。
- `todayIsForcedDay()`（L37699 附近）：`shoot:`／`job:` 先係強制日。
- `todayHasSoftSchedule()`：訓練／休息／街頭／`cafe_gig` 等 soft 日（唔係地圖日、唔係 shoot/job/wrap/audition）。
- 預設週計劃：`["scout_all","rest","scout_all","scout_all","street","cafe_gig","rest"]`。
- `runScheduleFromToday()`（L38072）：mapish（冇計劃／地圖日／wrap:／audition:）→ `goToMapForBrowse()`，否則跑 `resolvePlannedDay`。**注意：佢用「今日」個 plan 判斷，唔係「下一日」**——日結板撳「繼續」嗰陣，`tickDay()` 已經將 `dayIndex` 推去下一日，所以 `todayPlanId()` 嗰陣已經係下一日嘅 plan。工人唔好搞亂呢個時序。
- `startTodayScheduleFromMap()`（L37706）：地圖日／wrap:／audition: → `goToMapForBrowse()`，否則 `resolvePlannedDay(id)`。唔郁。

## §2 日流程骨架（基底行號）

- `resolvePlannedDay(id)`（L38105）：頭閘（`ending78Gate` → `hosp96TreatGate` → 病假 `conseq61ResolveSickDay`）→ 分支（`shoot:` 殺青／拍攝中、`TRAIN75_SPEC` 訓練、`rest`／`home_chore`／`street`／`cafe_gig`／`job:` 試鏡）→ `tickDay()` → 尾段（L38355–38460）：`nextNb`（`ended` → `enterHome`，否則 `runScheduleFromToday()`）、試鏡落選結算、week-accel 分流（非 critical 日靜默合併＋`setTimeout(runScheduleFromToday)`；critical／ended 日 `flushWeekAccelSummary`）、正常路 `dayEndContinueButtons(ended, nextNbReward)`＋`dismissNb`（見 §3）、`rest` 日行 `presentRestSleepDayEnd` 其餘行 `modal()` 日結板。
- `afterDayModal(resultHtml, title, L, ended, summary, opts)`（L36996）：共用日結板 builder。`go`＝`ended ? enterHome : runScheduleFromToday()`；掣＝`dayEndContinueButtons(ended, go)`；**`dismissFn = ended ? go : ()=>goToMapForBrowse()`**（L37035 附近）。呼叫方：`conseq61ResolveSickDay`（L34529，病假板）、`doEnrollRun`（L57206，訓練板）、`doRest`（L57489，休息板）、`endBrowseDayGoHome` fallback（L37748，小休板）。
- `tickDay()`（L36966）：記名兜底 → `closeSheet()`＋`atLoc=null` → `advanceDay()`（L36551：dayIndex+1、換年通告庫、ticks：favorDue／news82／wf3／`wf4DailyTick`／enc83／rivalry／exodus／story46／48／family debt／conseq61 病倒；回傳係咪新一週）→ `processOverdueShoots` → 週末 `settleWeek()`。
- `enterHome(summary, editable, initialTab)`（L37409）：週末回家結算＋計劃下週（editable 嗰陣重設 planDraft、清 audition:/wrap: 殘留）。唔郁。
- `commitPlanAndGo()`（L37563）：確認週計劃 → `runScheduleFromToday()`。已經跟新規則兼容（第一日係排程就即跑，係逛逛就落地圖），唔郁。
- `endBrowseDayGoHome()`（L37714）：地圖日「過一日」（提早休息）：story guard → hosp96 → 病假 → 寫今日做 `rest` → `tickDay()` → 休息卡（`presentRestSleepDayEnd`，`confirmStartSchedule:true`）。地圖日路徑，掣跟新規則（§3），流程唔郁。

## §3 返地圖路徑清單（改／唔郁，逐項核實）

### 要改（跟新規則：下一日有排程 → 唔出／唔返；逛逛 → 出／返）

| # | 位置 | 現況 | 改法 |
|---|---|---|---|
| 1 | `dayEndContinueButtons(ended, goRunSchedule, opts)`（L38008） | `ended` → 「回家結算」；下一日 forced → 「開始今日行程」；下一日 map → 「返回地圖」（行 goRunSchedule 經獎勵流程）；soft 日 → 兩粒（「返回地圖」→ `goToMapForBrowse()`，v189 改；「開始今日行程」→ goRunSchedule）＋加速細連結（`countRemainingAutoDays()>0` 先出） | soft 分支：下一日有排程 → **唔出「返回地圖」**，只留「開始今日行程」；下一日逛逛 → 照出兩粒。forced／map 分支唔郁。加速細連結唔郁（佢本身就係「跳過剩餘日子」，同新規則一致） |
| 2 | `afterDayModal` 嘅 `dismissFn`（L37035） | 非 ended → `goToMapForBrowse()` | 跟 D7 helper：下一日有排程 → `go`（＝`runScheduleFromToday()`）；逛逛 → 返地圖 |
| 3 | `resolvePlannedDay` 尾段 `dismissNb`（L38430 附近） | `ended ? nextNbReward : ()=>afterDayRes(()=>goToMapForBrowse())` | 同上：下一日有排程 → `nextNbReward`；逛逛 → 返地圖。注意 `afterDayRes`（殺青獎勵 sheet）要保留喺兩條路之前 |
| 4 | `presentRestSleepDayEnd(opts)`（L57280）休息卡 | 掣由 `dayEndContinueButtons(ended, goSchedule)` 嚟，再按 label 重映射（「返回地圖」→ goMap、「開始今日」→ `goScheduleAsk` 經 `presentStartScheduleConfirm45` 確認 modal、「加速」→ 原 handler、「回家結算」→ goSchedule）；`dismissFn = ended ? goSchedule : goMap` | 掣：跟 #1（`dayEndContinueButtons` 改咗之後，label 重映射嘅「返回地圖」分支喺排程日自然唔會匹配到——但 fallback `finish(orig \|\| goMap)` 一定要改：未識別掣喺排程日唔可以預設 goMap）。dismiss：跟 D7。`presentStartScheduleConfirm45`（L57254）確認 modal：排程日 → 唔出「返回地圖」掣，dismiss＝`proceedSchedule`（玩家已經撳咗「開始」，dismiss 唔可以走佬返地圖）；逛逛日 → 照舊 |
| 5 | `flushWeekAccelSummary`（L38073 附近） | 摘要 modal 掣「繼續」／「回家結算」＋`onDismiss: contFn` | 唔郁（accel 流程本身已經自動連跑，contFn 跟返 accel 續鏈）——但工人要核實 accel 完結嗰陣嘅去向跟新規則（critical 日停低出摘要，撳「繼續」→ `nextNb` → `runScheduleFromToday()`，已經啱） |

### 唔郁（已核實唔係走佬路／已經跟新規則）

- `goToMapForBrowse()`（L37810）：返地圖 hub 本體。晨鏈（見 §4）＋`kickScheduleIfNeeded()`（強制日即跑）＋`story165TryForcedPlay()`＋顯示地圖＋soft 日 toast。只喺逛逛日／週末／明確地圖操作先入到，唔郁。
- `book70ExitHome()`（L43990）：手帳恆常出口（關 sheet → `show("v-map")` → 強制播嘗試）。手帳只喺逛逛日／週末入到，唔郁。
- `leaveHomeFromNotebook(mode)`（L60077）＋`#home-back-map`（L60088）＋`#home-back-map-tabs`（L60092）：手帳內部出口。`#home-back-map` 喺地圖模式下 `display:none`（L37379），bypass 係潛在唔係現實；今次唔郁（v165 NOTES §9.4 殘留照舊，等用戶決定）。
- `#loc-close`（L60110）：地點 sheet「返回地圖」→ `closeSheet()`＋強制播嘗試。地點 sheet 內部，已經喺地圖，唔郁。
- `commitPlanAndGo()`（L37563）：見 §2，已經兼容，唔郁。
- `endBrowseDayGoHome()` 流程本身：見 §2，唔郁（只係佢出嗰張休息卡跟 #4）。
- 週末 `enterHome`／`settleWeek()`：唔郁。

## §4 晨鏈＋強制播喺自動連跑之下（重點，唔可以漏派）

### 晨鏈現況（`goToMapForBrowse` L37810–37860，early-return＋callback 模式）

次序：殺青獎勵 `presentPendingPostShootReward` → 頒獎排期＋請柬 `presentPendingAward` → 朝早報紙 `presentDueMorningPaper` → 試鏡消息 `aud91PresentDue` → WF4 `wf4PresentPending` → 醫院 `hosp96TreatGate` → 病假 `conseq61ResolveSickDay` → `kickScheduleIfNeeded()` → `story165TryForcedPlay()` → 顯示地圖。

### 自動連跑之下邊啲會漏（已核實）

- **朝早報紙＋試鏡消息：唔會漏。**`runScheduleFromToday()` 非 mapish 分支已經會先出呢兩樣再跑行程（`presentDueMorningPaper(thenFn)` L48706、`aud91PresentDue(continueFn)` L58643，兩個都食 continuation）。
- **殺青獎勵：唔會漏。**日結板續鏈（`afterDayRes`／`nextNbReward`）已經會喺跑下一日之前出 `presentPendingPostShootReward`。
- **頒獎請柬：會漏／會遲。**`presentPendingAward`（L46230）只喺 `goToMapForBrowse` 呼叫（另一處 L49197 係靜態測試，唔係 live 流程）。排咗成週行程、成週唔落地圖，請柬會一直等到下一個逛逛日先出。請柬本身冇過期（flag `invited`／`pending` 會留住，`restorePendingAward136` 處理 reload），但季候 fiction 會走樣；C17 要求 1992 台慶有結果，遲出唔會爛閘，但唔應該拖成週。**修法：跟 D2，搬入 `runScheduleFromToday` 全鏈。**注意：成個派柬 pipeline 而家仲鎖喺 soft 閘後面（`queueAwardsOnSeasonWindow` 第一行 `awardsSoftOn()`，v194 待開）；v196 唔郁個閘，淨係搬呈現位。
- **WF4 日常事件：會漏（最傷）。**`wf4PresentPending()`（L40870）只喺 `goToMapForBrowse` 呼叫；`wf4DailyTick()`（L40837）每日播種 pending，但 `WF4_CFG.pendingMaxAge = 2`（L40544）——pending 超過 2 日未呈現就靜默丟失。自動連跑之下，一單星期一播種嘅事件，等到星期四逛逛日已經唔見咗。**修法：跟 D2，搬入全鏈；`wf4PresentPending` 加可選 continuation 參數（預設 `goToMapForBrowse` 保舊行為，鏈入面傳續鏈）。**另外 `wf4PresentPending` 而家喺 forced 日直接回 false（唔呈現）——晨鏈喺日頭未開工前跑，事件唔會中斷拍攝；**建議鏈入面放寬呢個 forced 拒絕**（即係鏈用嘅呈現路徑唔理 `todayIsForcedDay()`），但工人必須實駕證實 `wf4Fire` 嘅 doneCb 接續正確、事件播完照跑當日行程；如果證實唔到，寧願寫明邊界（連續 forced 日會丟失，pendingMaxAge=2），唔好靜默改。
- **芬姐送別戲（一次性，exodus 線）：同 WF4 同一條路**（`wf4PresentPending` 入面 `wf4PresentFenFarewell()` 優先）。跟 WF4 一齊搬，唔可以漏。
- **強制播（v165）：會遲，唔會漏。**`story165NextOpen()`（L38482）返下一幕可播主線（C1–C17 次序，C6F 計在內），**冇過期**——未播嘅幕會一直等。但掛點只得三個：`goToMapForBrowse` 尾段、`book70ExitHome`、地點 sheet 返回（`#loc-close`）。自動連跑之下，主線幕要等到下一個逛逛日先播。**修法：跟 D2＋D3——晨鏈尾（`story165TryForcedPlay`）喺 `runScheduleFromToday` 全鏈入面都跑；播之前記低續鏈 slot（D3），播完經 `showResult` 續鏈。**`story165CanPlay()`（L38497）本身已經守住（`homeEditable`／結局／故事進行中／`_storyPlayLocked` → null），唔使再加閘。`story165ModalOpen()`（L38509）只供 `book70ExitHome`／`#loc-close` 兩條掛點用，唔可以擺入 `CanPlay`（晨鏈續鏈嗰陣 modal 技術上仲開緊，擺入去會誤擋——見該函數註解）。
- **病假：唔會漏。**頭閘喺 `resolvePlannedDay` 頭（`hosp96TreatGate`／`conseq61ResolveSickDay`），自動連跑每朝都會行一次。`conseq61ResolveSickDay` 嘅病假板行 `afterDayModal` 預設（L34529），掣／dismiss 跟 §3 #2。
- **週末：唔會漏。**`tickDay()` → `settleWeek()` → `ended` → `enterHome`，唔經地圖，唔郁。

## §5 故事播放期間返地圖路徑（追加硬規則，全部核實）

### StoryPlay 呈現（`render()`，L28215 附近）

- 每 render 加 `story-play-on`＋`setStoryPlayLock(true)`（全檔唯一 `true` 寫入點）。
- `forcedChrome = spIsForcedStory(n, _sess.pack, _sess.label)`（L27491：只得 C1 或 `_sess.forced`）；`seedDismiss = forcedChrome && spSoftSeedCanDismiss()`（L27499：soft-seed 自動開＋非 C1＋soft behavior gate 先可以 dismiss）；`lockedForced = forcedChrome && !seedDismiss`。
- `leaveStory()`（L28219）：`abort()`＋除 `story-play-on`＋解鎖＋`refreshLocAfterStory()`（重開地點 sheet）／重開地點。
- 掣列：beats 模式「下一句」（`stay:true`）＋非強制先有「跳至選項」（`stay:true`，場景內跳前，**唔郁**）；抉擇模式無選項嗰陣「完成這一節」；**非 lockedForced 先有「先返回」掣（`leaveStory`，L28255）**——即係而家除咗 C1／forced 之外，所有主線／支線／巧遇故事都有明確嘅「先返回」掣。
- `dismissOpts`：lockedForced → onDismiss 重開畫面（走唔到）；非 locked → onDismiss 只係 `abort()`＋除 `story-play-on`（`closeModal` 本身會解鎖）。
- **修法（D4）**：唔再按 `lockedForced` 分流——所有故事一律唔出「先返回」，onDismiss 一律重開畫面。`spSoftSeedCanDismiss()` 唔使刪（其他地方／offer 邏輯可能用到），但播放期間唔可以再靠佢開 dismiss 口。
- 巧遇（ENC79）行同一條路：`playMeet()`（L25904）／`playPush(id)`（L25975）／`play(id)`（L26234）全部經 `StoryPlay.start` → 同一個 `render()`，一次修晒。WF4 故事節點（`choice47Play` L41635／`commit48Play` L41759／芬姐 intro／farewell）同樣經 `StoryPlay.start`，一樣覆蓋。

### 故事結算 modal（`showResult`，L28040 附近）

- 播完先出，掣有「下一節」（播下一幕）／「進度」（入手帳進度頁）／「關閉」（`show("v-map")` 直返地圖）＋ onDismiss（畫 hints／drawMap／`refreshLocAfterStory()`，**冇 `show("v-map")`**——即係撳走結算 modal 係留喺原地／重開地點，唔係返地圖）。
- **修法**：「關閉」唔可以一律 `show("v-map")`——要跟 D3 續鏈 slot（排程日 → 跑下一日，逛逛日 → 地圖）。onDismiss 照舊（留原地／重開地點，唔係返地圖，已經啱）。「下一節」／「進度」唔郁（「進度」入手帳係玩家主動選擇，唔係無故返地圖；但工人要核實由進度頁返出嚟嗰陣唔會跌咗續鏈 slot——slot 消費時機寫明）。
- `refreshLocAfterStory()`（L54878）：`atLoc` 先重開地點 sheet（`travelFree`），`atLoc` null 就乜都唔做（留喺當下畫面）。唔郁。

### 已經鎖死／已經有 guard，唔使郁（工人核實，唔好重做）

- **Mask 撳外面**（L60159）：`e.target.id==="mask"` → `closeModal()`＋跑 `_modalDismiss`（教學 blocking 嗰陣唔郁）。故事播放期間 `_modalDismiss` 就係 `render()` 傳入嘅 `dismissOpts.onDismiss`——D4 改咗佢之後，mask click 會重開畫面，唔會返地圖。注意次序：`closeModal()`（L39464）會先清 `story-play-on`＋解鎖，然後 `fn()` 重開畫面嗰陣 `render()` 再加返——C1 lockedForced 而家已經行同一條路，工人核實冇閃爍／冇狀態丟失就得。
- **頂欄／選單**：`.mask` z-index 50 蓋住成個 390px 欄，`.menu` z-index 45、`.bar` z-index 5 全部喺 mask 下面——故事 modal 開緊嗰陣撳唔到。`setUnderlyingInert()`（L36889）另外蓋 v-map／v-home／v-start／menubar／menu／loc-sheet／`btn-confirm-plan`＋`app.ui-inert`。唔郁。
- **地點／地點行動**：`openLoc()`（L54885）：故事進行中 → toast「劇情進行中，完成對白先可以繼續。」＋return（`forceRestore` 除外）；forced 日 → `kickScheduleIfNeeded()`。`applyMockAsk()`（L43367）／地點行動 handler（L54991／L55422）／`ensureLocSheetInteractive()`（L58240）：同樣 story guard＋toast。唔郁。
- **選單「過一日」／地圖日「提早休息」**：`confirmEarlyRestFromMenu()`／`endBrowseDayGoHome()`（L37714）開頭都有 story guard（toast＋return）。唔郁。
- **頒獎禮典禮**：`awards62PlayCeremony()`（L46812）`div.awd62-stage` 直接掛 `document.body`，唔經 `modal()`；CSS `.awd62-stage{position:fixed;inset:0;z-index:9990}`（L780）冚晒成個 viewport（menu 45／mask 50／頂欄 5 全部喺下面），得「跳過 ⏩」掣（`finish()`→`done()`→結果卡）＋「撳畫面可以快進」。**已經鎖死，唔使郁。**典禮後結果卡 `presentAwardResult`：modal「收下這晚」＋onDismiss＝cont（晨鏈續鏈），唔係返地圖，唔郁——但工人要核實 cont 喺自動連跑鏈入面跟 D2 續鏈，唔好硬返地圖。
- **頒獎請柬 modal**：`presentAwardInvite()`（L46183）：「出席」／「推辭」兩粒掣，**onDismiss＝skip（推辭）**，唔係返地圖。但佢開 modal 之前會 `remove("story-play-on")`＋`setStoryPlayLock(false)`（L46191 上下文，針對 N1 開場故事 modal 殘留，唔郁請柬邏輯）。工人要核實：請柬只喺晨鏈出，晨鏈唔會喺故事播緊嗰陣跑（`story165CanPlay`／`isStoryPlayActive` 守住），所以呢句 unlock 唔會成為故事期間嘅走佬路；寫明原因喺 NOTES §4 殘留。
- **系統 modal（病假／報紙）唔可以鎖死**：晨鏈項目本身係故事之前／之後嘅嘢，D4 只鎖 StoryPlay `render()` 嘅 dismiss／「先返回」，唔郁 `modal()` 本體、唔郁晨鏈 modal 嘅 dismiss（請柬 dismiss＝推辭、報紙 dismiss＝續鏈，全部有定義好嘅續鏈，唔係返地圖）。

## §6 實作清單（工人照單執藥）

1. 抽 D7 helper `nextDayIsMap()`（讀 `todayPlanId()`——注意時序：日結板嗰陣 `dayIndex` 已經係下一日），三處共用。
2. `dayEndContinueButtons`：soft 分支按 D7 決定「返回地圖」出唔出；其餘分支唔郁；加速細連結唔郁。
3. `afterDayModal` dismissFn、`resolvePlannedDay` 尾段 dismissNb、休息卡 dismissFn：全部跟 D7（排程日＝繼續，逛逛日＝返地圖）。休息卡 fallback `finish(orig || goMap)` 一定要改（唔可以預設 goMap）。
4. `presentStartScheduleConfirm45`：排程日唔出「返回地圖」，dismiss＝`proceedSchedule`；逛逛日照舊。
5. `runScheduleFromToday` 非 mapish 分支：行全晨鏈（報紙→試鏡消息→請柬→WF4→強制播），continuation＝跑當日行程；`goToMapForBrowse` 全鏈保留，continuation＝落地圖。兩邊共用同一條鏈 runner，唔好複製兩份。
6. `wf4PresentPending`：加可選 continuation 參數；鏈入面放寬 forced 拒絕（見 §4，實駕證實）。
7. 強制播續鏈 slot（D3）：`story165TryForcedPlay` 播之前寫 slot；`showResult`「關閉」／onDismiss 消費 slot；「下一節」鏈完之後先消費。
8. StoryPlay `render()`：所有故事一律唔出「先返回」，onDismiss 一律重開畫面（D4）。
9. `showResult`「關閉」：跟 D3 slot，唔一律 `show("v-map")`。
10. 唔郁清單（§3／§5）：手帳出口、`#loc-close`、週末、week-accel、save key、softRev、`?v=`、content pack JSON（唔直改，用覆寫／注入）、`S.awardsFlags`／C17 閘、頒獎 soft 閘（v194 嗰票先郁）。

## §7 驗證

- 新測試＋反證（對 pristine 乾淨 FAIL，唔好 crash）；全套 A/B（基線 12 項穩定 FAIL，判斷準則：FAIL 清單相同＋相關測試逐個直接覆驗）。
- 實駕 932／700（本地鏡像＋http.server，live 模式——**唔好用 `?softPreview=1`**，強制播喺 softPreview 下全滅，見 v165 review B1）：
  1. 連續 3 日排程（train／rest／shoot 混合）：日結板撳「繼續」自動跑下一日，全程唔經地圖（`v-map` 唔現、唔見 map toast、`dayIndex` 遞增）。
  2. 下一日逛逛：日結板出「返回地圖」，撳落去落地圖＋toast＋「開始今日行程」正常。
  3. dismiss（mask click）：排程日＝繼續跑下一日；逛逛日＝返地圖。
  4. 晨鏈：播種 due 報紙＋試鏡消息＋請柬（soft mode 先有請柬，live 模式請柬未開——請柬 case 用 soft 播種但行 live 斷言要分開寫）＋WF4 pending，連續排程日自動跑，全部照出、次序啱、唔漏。
  5. 強制播：播種一幕可播主線，自動連跑嗰陣照觸發；播完「關閉」跟新規則（排程日→跑下一日，逛逛日→地圖）。
  6. 故事鎖死：播一段主線幕，逐個試——「先返回」掣唔存在、mask click、頂欄／選單撳唔到、地點掣撳唔到——全部唔返地圖；播完經結算 modal 正常離開。
  7. 週末照常：`ended` → `enterHome` → 計劃下週 → `commitPlanAndGo` → 跑新週第一日／落地圖（按第一日係咪逛逛）。
  8. 病假日照常：播種病假，病假結算板出，掣／dismiss 跟新規則。
  9. 休息卡：rest 日結卡，排程下一日→「開始今日行程」＋確認 modal 冇返地圖路；逛逛下一日→「返回地圖」。
  10. 殺青獎勵：shoot wrap 日，獎勵 sheet 照出，之後跟新規則。
  11. Week-accel 照舊（opt-in 加速流程唔爛；critical 日停低出摘要）。
  12. 頒獎禮典禮期間撳唔到地圖（stage 冚晒，跳過掣正常）；請柬 dismiss＝推辭，唔係返地圖。
- 落地由統籌做（checkout main → `git merge --squash v20a196` → commit → push main，唔開 PR）。落地前核對常駐 clone 分支 HEAD 係咪最新；檢查常駐 clone 工作樹有冇其他人嘅 staged 改動；落地後統籌親自 curl 核實線上 bytes／sha 同 repo HEAD 一致。Push 斷線嗰陣拆細推（v183 教訓）。

## §8 風險／殘留

- **WF4 邊界**（§4）：如果鏈入面放寬 forced 拒絕證實唔到，連續 forced 日嘅 WF4 pending 會喺 pendingMaxAge=2 之後靜默丟失——工人要喺實作 NOTES 寫明揀咗邊條路＋實駕證據，唔好靜默。
- **獎項 soft 閘**（已解決）：v194 已落地（main `a1a6681`，遊戲 `707ff66`），派柬 pipeline 拆咗 soft 閘；v196 嘅請柬鏈搬位已喺 **live 模式**驗到——rebase 後實駕 c12a／c12b（§10 932 重跑）請柬照出、典禮照播。
- **掣位 review B4／B5**（報告 `~/workspace/linji-design-review-buttons/REVIEW.md`，A 0／B 7／C 7）：B4 日結三粒掣跟內容郁 70px、B5「返回地圖」三個位三種大細——review 明言「B4／B5 日結『返回地圖』可能喺 v196 之後消失，修之前先對 v196 落地点」。v196 落地後，B4／B5 要重新對一次（「返回地圖」喺排程日消失之後，剩低嗰粒掣嘅位置／大細仲有冇問題）。
- **C17 結局閘**：`awardResolved: {ceremonyId: "award_singho_tv", year: 1992}`＋`backstopDay: 1096` 唔郁；請柬遲出唔會爛閘（backstop 兜底），但 D2 搬鏈之後遲出問題已經解決。
- **行號漂移**：上面行號全部對住基底 `2760680`；rebase 上 main `a1a6681`（v192／v194／v195／v198 已落地）之後行號已漂移，見 §11。

## §9 實作報告（工人，2026-11-13）

- **實作基底**：main `2760680`（v191）。開工 `git fetch origin` 後 origin/main 仍係 `2760680`，v192 分支存在但未合併——rebase 係 no-op，分支本身已喺最新 main。基底行號同 §2／§6 完全一致。
- **改動**：`index.html` 唯一遊戲檔改動，`+182/−99`（淨 `+83` 行；總行數 `60490→60573` 個 `\n`）。`node --check` 兩段 inline script 全部 PASS。`lockedForced`／`leaveStory`／`seedDismiss` 殘留命中全部係註解。「唔複製兩份」字樣完好（`U+FFFD count: 0`）。
- **§6 十項全部落地**（`nextDayIsMap()`／`dayEndContinueButtons`／三處 dismiss／`presentStartScheduleConfirm45`／`morningChain196`／`wf4PresentPending(cont, opts)`／D3 slot 三 helper／`render()` 鎖死／`showResult` 跟 slot／唔郁清單）。**偏離 §0 決定：零。**
- **新測試**：
  - `tests/test_dayflow196_logic.js`：**55/55 ALL PASS**（D7 判定／日結四分支／晨鏈次序＋續鏈＋病假截停／兩邊分流／D3 slot 一次性／dismiss 兩向／休息卡＋確認 modal／真 WF4／真 Fen 送別）。
  - `tests/test_dayflow196_static.py`：**ALL PASS**（D7／slot／晨鏈次序／兩邊呼叫點／日結掣＋dismiss／WF4／showResult／render 鎖死／休息卡＋確認 modal／紅線）。
  - 教訓（已寫入測試註解）：鏈環 stub 只可以捕捉續鏈，唔可以同步叫 `cont()`（會重入無限遞歸）；stub 必須 one-shot；測試用 `driveChain()`（guard 上限 50）逐個續鏈驅動。
- **反證**（`git show HEAD:index.html` → `/tmp/pristine196_index.html`）：logic throw（`nextDayIsMap` 唔存在），exit 1；static 31 項 FAIL，exit 1——乾淨 FAIL，唔 crash。
- **舊測試更新**（全部因 v196 刻意改行為，已加 v196 註解）：`test_dayend189_static.py`＋`test_dayend189_logic.js`（soft 分支唔再出「返回地圖」）、`test_flow45_logic.js`（case B 改排程下一日、case F 改逛逛日；另修咗個 `const c2` 重名 SyntaxError）、`test_story165_static.py`（掛點改跟 `morningChain196`＋slot 寫入）、`test_wf4_86_static.py`（掛點改跟新 call form）。全部 **ALL PASS**。
- **全套 A/B**（`qa131/run_suite.sh`）：
  - 基線（改之前）：**263 PASS／12 FAIL**（12 項穩定 FAIL，見 `qa196/suite_baseline.txt`）。
  - 工作版 A：**253／24**——12 項新 FAIL，逐個 triage 全部唔係行為回歸：
    - **釘行／總行數漂移 8 檔**（淨 +83 行所致）：`kwan151`（4 錨點各 −1）、`rom176`（5 錨點 −1／+74）、`tang152`（2 錨點各 −1）、`tang171`／`tang173`（總行數＋DEF）、`gift185`（總行數）、`text125`（familySafe 錨點 −1）、`travel114`（COUNT／FREE／DEF／WRAPPER 成組重對）。全部經 difflib 對位核實內容逐字相同，純漂移；測試檔本身有 per-version resync 慣例，照慣例更新錨點＋加 v196 resync 註解。
    - **travel114 另有一行刻意刪除**：舊 28228 行（`leaveStory` 嗰行 `openLoc(atLoc,{travelFree})`）隨 D4「先返回」拎走而消失，openLoc 呼叫點 52→51——係 v196 刻意改動，唔係漂移；FREE 清單 34→33。
    - **掛點搬位 4 檔**（行為經共用晨鏈保留，斷言改跟新掛點）：`aud91`（公佈 hook 由 `runScheduleFromToday` 搬入 `morningChain196`）、`conseq61`（病日守衛由 `goToMapForBrowse` 搬入 `morningChain196`，守衛本身唔郁）、`hub77`（強制播掛點搬入 `morningChain196`；另 `story165TryForcedPlay` 簽名加 `afterCont`）、`story172`（B1(b) seg 起點改跟新簽名；`{ ignoreSheetLoc:true }` 本身仲喺度）。
  - 工作版 B（更新 12 檔舊測試後）：**265／12**——FAIL 清單同基線 12 項穩定 FAIL 完全一致，**零回歸**（見 `qa196/suite_workB.txt`；工作版 A 見 `qa196/suite_workA.txt`）。
- **WF4 邊界**：揀咗「鏈入面放寬 forced 拒絕」嗰條路（§4 建議）。實駕證據見 §10 c4（`wf4_ev_set01` 經排程鏈播完，`S.wf4.pending` 清空、`seen` 計數 +1，之後 Tue street 照跑）。

## §10 實駕結果（工人，2026-11-13）

實駕腳本 `qa196/drive196.py`（本地鏡像 port 8976，live 模式，Playwright venv `/home/hatch/pwenv49/bin/python`，headless_shell 瀏覽器；報告 `qa196/report196.json`，截圖 `qa196/shots196/`）。每 case 新 page → 正常開局（slot 3）→ `settle_opening` 播完開局 C1 → 播種 localStorage（key `starVolunteer_map_v19w`，slot 1）→ UI 路徑觸發 → 行為斷言。

### 932：17/17 PASS（約 11 分鐘，0 pageerror 以外嘅錯誤）

| case | 內容 | 關鍵證據 |
|---|---|---|
| c1 | 連續排程日自動連跑 | Mon wrap 板只得「開始今日行程」（Tue street）→ Tue 街頭板只得「開始今日行程」（Wed rest）→ Wed 休息卡只得「返回地圖」（Thu scout_all 逛逛日）→ Thu 落地圖，day 3 |
| c2 | 逛逛日準確落地圖 | Mon 板「返回地圖」（Tue scout_all）→ Tue 鏈 [reward, paper, map]，day 1 |
| c3a／c3b | 日結板 dismiss 兩向 | mask dismiss＝同一去向（排程日繼續／逛逛日返地圖），兩向 PASS |
| c4 | 晨鏈一個唔漏 | phase1 [reward, invite:街招年賞請柬] → 典禮 → 結果卡；phase2 [paper, aud:何生來電， WF4「開鏡拜神企前排」4 beats, dayend 街頭表演（週二）]；`S.wf4` 事後 `{pending: null, seen: 1, audLeft: 0}` |
| c5a | 強制播續鏈 slot=map | Mon 街頭板 →「返回地圖」→ 晨鏈 → 芬姐送別戲「啟德送芬姐」→ 結果 modal（內文含芬姐／啟德）→「關閉」→ 落地圖，日唔郁（day 1） |
| c5b | 強制播續鏈 slot=schedule | Mon wrap 板 →「開始今日行程」→ 晨鏈 [reward, paper, story:啟德送芬姐， story-done, result-modal] →「關閉」→ Tue 街頭板，day 2 |
| c6 | 故事鎖死 | 開局 C1：無「先返回」掣；mask click 後故事照播；地圖位真滑鼠撳完故事照播、map false；關閉後 map true |
| c7 | 週末照常 | Sun wrap 板「回家結算」→ 獎勵 sheet 行先（撳穿）→ 回家成功 → 確認下週計劃 → 出發即跑 Monday（已排定嘅 probe196f 拍攝日）→ 拍攝中板，day 13→15 |
| c8a／c8b | 病假照常＋掣／dismiss 跟新規則 | 病假板「病倒休養（第 1 日）」；(a) Tue street：只得「開始今日行程」，mask dismiss → Tue 街頭板；(b) Tue scout_all：有「返回地圖」，mask dismiss → 落地圖 |
| c9a／c9b | 休息卡 | (a) Tue street：休息卡「休息（週一）」[開始今日行程]，mask dismiss → Tue 街頭板；(b) Tue scout_all：休息卡只得「返回地圖」，撳佢 → 落地圖 |
| c10 | 殺青獎勵 | 晨鏈 [reward, paper, dayend:街頭表演（週二）] |
| c11 | week-accel 照舊 | 加速連結 → 獎勵 sheet 行先（afterDayRes 包裝，pre-existing）→ 撳穿 →「加速本週剩餘？」確認 [取消， 確認加速] → 加速 →「本週加速完成」[返回地圖] → 落地圖（day 4；途中 WF4 故事「傳呼台嘅一課」照播） |
| c12a | 請柬 dismiss＝推辭 | Mon 街頭板 →「返回地圖」→ 晨鏈 → 請柬「街招年賞請柬」[出席， 推辭] → mask 閂＝推辭 → 典禮照播（gallery）→ 落地圖；award log 尾段有 skipped |
| c12b | 出席＋典禮鎖死 | 請柬 →「出席」→ 典禮舞台；elementFromPoint 三點全部命中 `.awd62-stage`；舞台上撳極唔走；典禮播完 →「收下這晚」→ 落地圖 |

- **WF4 邊界（§9 嗰條路）實駕證實**：c4 嘅 `wf4_ev_set01` 經排程鏈播完，`S.wf4.pending` 清空、`seen`＋1，之後 Tue street 照跑——鏈入面放寬 forced 拒絕（`allowForced:true`，doneCb＝續鏈 step）可行，事件播完照跑當日行程。c11 途中 WF4 故事「傳呼台嘅一課」經地圖鏈播完亦同證。
- **console.error 404（共 324 個，全部同一原因）**：全部係缺失資產 `bg_loc_home_airport`（芬姐送別戲背景）——圖像 resolver 每播一次探 18 條候選路徑（6 目錄 × jpg／png／webp），Fen 播 18 次共 324 個 404。已核實 worktree 入面完全冇呢個檔。**pre-existing，唔係 v196 回歸**（v196 冇郁過資產／resolver）；留返另開票補圖。
- **實駕腳本修正（test-only，零遊戲 code 改動）**：(1) `is_dayend` 收緊——要埋繼續掣（報紙 modal 標題都含「殺青」但得「收下這份剪報」）；(2) `mask_click` 成功定義＝原本嗰個 modal 唔見咗（dismiss 後即出新 modal 都計）；(3) `trigger_map_chain` 原假設錯——查明 `#loc-close` 只係 `closeSheet()＋story165TryForcedPlay()`，唔行晨鏈；`openLoc` 只喺 forced 日（shoot:／job:）先 kick 行程。改行正確觸發：新增 `start_today_from_map()`（地圖 `#map-start-today`，settle 後 hint 係開局 plan 渲染、掣可能唔存在，後備行 menu→手帳→行程頁 `#home-back-map「開始今日行程」`）畀 c8／c9；c5a／c12 改行 Mon 街頭板 →「返回地圖」→ 晨鏈（真實玩家路徑）；(4) c1 嘅 Wed 休息卡斷言本身寫錯——Thu 係 scout_all 逛逛日，按 D7 應該出「返回地圖」，已改跟 D1；(5) c7 home loop 要先撳穿獎勵 sheet（回家結算掣包咗 `afterDayRes`，獎勵行先）；(6) c9b 改跟 v196 D1——逛逛日休息卡只出「返回地圖」，唔再經確認 modal（確認 modal 兩向由 `test_dayflow196_logic.js` 覆蓋）；(7) c11 加速確認之前要先撳穿獎勵 sheet（同 (5) 一個機制）；(8) c7 嘅 Monday 唔係 street——seed 嘅 probe196f（三日拍攝）自動排入新一週 Mon–Wed（「拍攝檔期已定」），Monday 跑拍攝、day 13→15 係正確行為，斷言已改跟實際流程。

### 932 重跑（rebase 後，統籌，2026-11-13）

`qa196/drive196.py --vp 932`，同一腳本、同一種子，報告覆寫 `qa196/report196.json`（log `qa196/drive_rebased_932.log`，截圖不變 `qa196/shots196/`）。**17/17 PASS**，total pageerrors=324——同 pre-rebase 一模一樣嘅 324 個 `bg_loc_home_airport` 404（pre-existing，§10 上文）。c12a／c12b 今次行 **live 模式**（drive 本身唔用 `?softPreview=1`；v194 已拆 soft 閘）：c12a 請柬「街招年賞請柬」照出、mask 閂＝推辭、典禮照播、award log 有 skipped；c12b 出席後 elementFromPoint 三點全部命中 `.awd62-stage`，典禮鎖死，播完 → 報紙 → 落地圖。

### 700：17/17 PASS（統籌，rebase 後補；逐單 `--only ${k}-700 --vp 700`，各寫獨立報告 `qa196/report196_${k}-700_700.json`，log `qa196/drive_rebased_700.log`）

17 單全部 PASS，內容同 932 一致（c1 連跑、c2 逛逛日、c3a／c3b dismiss 兩向、c4 晨鏈、c5a／c5b 強制播續鏈、c6 鎖死、c7 週末、c8a／c8b 病假、c9a／c9b 休息卡、c10 殺青獎勵、c11 week-accel、c12a 推辭、c12b 出席＋典禮鎖死）。pageerrors 合共 324 個——同 932 一模一樣嘅 `bg_loc_home_airport` 404（c5a／c5b 各 162），其餘 15 單 0 個。

- **c12b-700 曾經 FAIL 一次（drive 探點 bug，唔係遊戲問題）**：第一輪 `elementFromPoint` 返 `["awd62-stage", "awd62-stage", null]`。根因：drive 寫死探點 `[[195,200],[195,400],[195,700]]`，但 700 viewport 係 390×700——y=700 啱啱喺 viewport 底邊之外，`elementFromPoint` 返 null。典禮本身正常（`ceremony: true, map: false`，頭兩點命中舞台）。已修正 drive：探點改跟舞台本身嘅 bounding rect（橫向中央、25／50／75% 高），重跑 c12b-700 **PASS**（3/3 命中），c12b-932 重跑亦 PASS——探點改動冇放寬 932 檢查。

## §11 Rebase 上 main `a1a6681`（統籌，2026-11-13）

- **基底**：工作 commit `9bee88f`（基底 main `2760680`，v191）→ rebase 上 main `a1a6681`（v194 NOTES，遊戲 `707ff66`）。`GIT_EDITOR=true git rebase origin/main`：**index.html 乾淨合併，零衝突**（main 37 hunks vs work 32 hunks，0 重疊，最近 gap 11 行）。
- **衝突：8 個測試檔，11 hunks，全部係行號 resync**（兩邊各自更新同一批 hardcoded 行號）。逐個錨點對住 rebased index.html 核實後解晒（`muse.edit` 套入，唔用 `git checkout --ours/--theirs`）：
  - gift185：總行數 60750。kwan151：PHRASES 31031、EXACT C13 31022、relMap 31073、NOTE_EXACT 31030。rom176：GIFT_REACT 31585、ROM176 block 53664、rom176ApplyGiftOverrides 54032、addLocTalkGiftActs 55171、rom176TryIntercept 55265。
  - tang152：HEAD 側正確（`lines()[31511]`／`lines()[31655]`，0-based 索引——第一次照 HEAD 寫 `lines()[31512]`／`lines()[31656]` 錯咗 off-by-one，跑測試即捉到，已更正）。tang171／tang173：總行數 60750、openLoc DEF 55234。text125：b.text 分支 33573。
  - travel114：用 `qa196/resync_travel114_196.py`（base→rebased 兩版 index.html 各自列舉全部 `openLoc(` 行，difflib SequenceMatcher 按內容＋次序對位）核實——**51 個呼叫點兩邊一致，全部對上**；COUNT 12/12、FREE 33/33、flag check 0 bad；DEF 55234、WRAPPER 44510；leaveStory 嗰行已刪，呼叫點總數 52→51。travel114 測試本身係自我驗證（重列舉全部呼叫點對清單），套入後 PASS 即係啱。
- **Rebase 尾段故障**：第一次 `git rebase --continue` 造好 commit `bc7f234` 並更新咗 branch ref，但 rebase state 未清（懷疑 EPERM 故障打斷咗 ref 更新）；第二次 `--continue` 報 `update_ref failed ... is at bc7f234 but expected 9bee88f`。核實咗工作樹乾淨、`git diff HEAD` 空、HEAD＝branch＝`bc7f234`（parent `a1a6681`）、`git fsck` 只有 dangling commits（rebase 後正常，零損壞）之後，**手動 `rm -rf .git/rebase-merge` 清走殘留 state**（`git rebase --abort` 會錯手退返 `9bee88f`，唔用）。之後 `git status` 乾淨、on branch v20a196。
- **語義覆核（v198 × v196）**：v198 B1 改咗 `wf4TryLocEvent`（地點入場事件）：有強制播 pending 嗰陣 defer；v196 改咗 `wf4PresentPending`（晨鏈 pending day 事件）。兩者唔同函數、唔同觸發（loc vs day），v198 註解明言晨鏈次序唔郁——**零語義衝突**。rebase 後合併樹同時滿足兩邊：強制播優先於 WF4 地點事件（c5a／c5b＋c6 驗到）＋晨鏈 WF4 day 事件一個唔漏（c4 驗到）。
- **全套 A/B（rebase 後，新基線＝pristine main `a1a6681`）**：
  - 基線：**271／12**（`qa196/suite_rebased_baseline.txt`；12 項＝穩定 FAIL 清單：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38——同 v194 落地數字一致）。
  - 工作版：**272／13**（`qa196/suite_rebased_work.txt`）。唯一新 FAIL 係 `tests/test_story198_static.py` 單一 assertion——v198 測試假設晨鏈仲行舊式無參呼叫 `wf4PresentPending()`，v196 D2 已刻意改做帶續鏈 `wf4PresentPending(step, { allowForced:true, afterCont:afterKind })`（晨鏈搬入共用 runner）。行為本身冇變（pending day 事件仍然喺鏈入面、仍然喺強制播之前，boss01 仍然唔關事），已更新測試斷言跟新 call form＋加次序檢查（`src.index` wf4 喺強制播之前），**更新後 ALL PASS**。其餘 8 檔 resync＋2 檔新測試逐個覆驗全部 PASS。**零回歸。**
- **實駕**：932 重跑 17/17（見 §10 上文）；700 17/17（見 §10 700 節；c12b 探點 bug 已修，唔係遊戲問題）。
- **第二次 rebase**：v199 落地後 main 行前去 `2c1a680`，分支再 rebase 一次，見 §12。

## §12 第二次 rebase 上 main `2c1a680`（統籌，2026-11-13）

- **原因**：第一次 rebase 完成後、落地之前，main 行前咗——v199 落地（main `5f5be18`：修 v195 review B1＋C1–C3，阿偉三 tier 渲染高度正規化）＋v195 NOTES（main `2c1a680`）。落地基底必須係最新 main，所以再 rebase 一次。
- **v199 改動範圍**：index.html 只得 4 處（CSS／PORTRAITS L5906／5927、對話舞台 fit `dlg108FitApply` L26977–27078、WF4 對話 L40712；淨 ＋44 行，60750→60794），全部唔喺 v196 嘅改動區（showResult／晨鏈／WF4 pending／StoryPlay render／日結板），**index.html 乾淨合併，零衝突**。v199 另改 7 檔測試（同第一次 rebase 嗰 7 檔）＋加 2 檔新測試（全套 273／12）。
- **衝突：8 個測試檔，11 hunks，全部係行號 resync**（同第一次一樣，連 gift185 都撞埋）。解法同第一次：逐個錨點對住 merged index.html（60794 行）核實——v199 嘅 ＋44 拆做 DLG199 ＋30（L26977）／fitApply ＋13（L27001–27036）／WF4 onload ＋1（L40712）；錨點喺 27078–40712 之間者 ＋43，其後者 ＋44；v196 嘅 showResult −1 令 HEAD 側永遠大 1。travel114 用 `qa196/resync_travel114_196b.py`（bc7f234→merged difflib 對位）：**51 個呼叫點全部對上，0 刪除；COUNT 12/12、FREE 33/33、flag check 0 bad；DEF 55278、WRAPPER 44554**。解完 8 檔＋2 檔新測試逐個跑，全部 PASS。
- **Rebase 尾段故障（第二次）**：`git rebase --continue` 造好第一個 pick 嘅 commit `6e80c76` 之後停喺 "editing" 狀態，`done` 檔寫住兩個 pick 做完，但第二個 pick（`9afc7d7`）根本未套入——工作樹冇佢嘅內容（story198 fix／NOTES §11／drive 探點 fix 全部 0 命中）。再跑 `--continue` 顯示 "Successfully rebased"，但分支只得 `6e80c76`，第二個 pick 靜默丟失。修法：`git cherry-pick 9afc7d7` 補返，乾淨套入，成 `be622a8`。教訓：**rebase 完一定要逐項核實第二個 pick 之後嘅 commit 內容有冇入樹，唔好信 "done"／"Successfully rebased"**（同第一次 rebase 尾段 `update_ref failed` 係同一類 EPERM／狀態故障）。
- **全套 A/B（第二次 rebase 後，新基線＝pristine main `2c1a680`）**：
  - 基線：**273／12**（`qa196/suite_rebased2_baseline.txt`）。第一次喺常駐 clone 直接跑嗰陣出咗 249／36——假陽性：另一手（v200）同一時間喺常駐 clone 嘅 tests/ 入面郁緊（16:16 寫入 `test_awards200_*` 兩檔＋改咗 5 檔），基線樹俾人途中改咗；逐個重跑嗰 8 檔全部 PASS、v200 自己喺 16:14 嘅乾淨基線亦係 273／12，證實樹本身冇事。教訓：**以後基線唔好喺共用嘅常駐 clone 跑，要用獨立 worktree**（今次用 `git worktree add ~/workspace/pristine196b 2c1a680`，820M，跑完可刪；`git archive` 淨抽 index.html＋tests 唔夠——好多測試要讀 `content/`，嗰次出咗 179／106，唔作準）。
  - 工作版：**275／12**（`qa196/suite_rebased2_work.txt`）。＋2 係 v196 兩檔新測試，雙雙 PASS；FAIL 清單同基線 12 項穩定 FAIL 完全一致，**零回歸**。
- **實駕（第二次 rebase 後）**：針對性重跑 c1／c6／c12b（932，各寫獨立報告 `qa196/report196_c1-932_932.json`／`c6-932`／`c12b-932`）：**3/3 PASS，0 pageerror**——c1 連跑鏈完整（Mon 拍攝→Tue 街頭→Wed 休息→Thu 落地圖）、c6 故事鎖死（無「先返回」掣、mask／地圖撳極唔走、關閉返地圖）、c12b 典禮鎖死（elementFromPoint 3/3 舞台）。v199 淨改對話人像 fit，唔郁日流程；全套 932／700 證據（第一次 rebase 後，§10）仍然有效。
- **Rebased commits**：`6e80c76`（第一次 pick＋8 檔 resync）＋`be622a8`（cherry-pick 補返第二個 pick），parent `2c1a680`。
- **Rebased commit**：`bc7f234`（37 files，5706 insertions／218 deletions；原 `9bee88f` 36 files＋resync 腳本 `qa196/resync_travel114_196.py` 新加入）。
- **第三次 rebase**：v200 落地後 main 行前去 `4e841e5`，分支再 rebase 一次，見 §13。

## §13 第三次 rebase 上 main `4e841e5`（統籌，2026-11-13）

- **原因**：第二次 rebase 驗證完成、準備落地嗰陣，main 又行前咗——v200 落地（main `4e841e5`：修 v194 review C1＋C2，請柬 gap 句加「今年」／旁聽 rep 行改「入場觀禮」／nominee 行改「你爭嘅獎項」；全套 275／12 vs 基線 273／12）。
- **v200 改動範圍**：index.html 只得 5 處，全部喺頒獎請柬區（L46184–47612：`renderAwardInviteHtml` ＋3／`awards62GateLineHtml` ＋2／`awards62SeasonHints` ＋1／`awards63InviteBitHtml` ＋6；淨 ＋12 行），全部唔喺 v196 嘅改動區，**index.html 乾淨合併，零衝突**。v200 另改 5 檔測試（gift185／rom176／tang171／tang173／travel114）＋加 2 檔新測試（`test_awards200_*`）。
- **`git rebase` 機械故障（第三次）**：`git rebase origin/main` 一開始就死咗——`error: Your local changes to the following files would be overwritten by merge`（列出 15 檔），reflog 證實 `rebase (start): checkout origin/main` 之後乜都冇發生過（第一個 pick 未套入、零 commit），工作樹停喺 main `4e841e5` 內容，但 `done` 檔照樣寫住第一個 pick 做完（同第二次 rebase 尾段一樣：state 檔講嘅進度唔可信）。`git rebase --abort` 乾淨返去 `dda0a36`（v196 內容完整返晒，`morningChain196` 4 命中）。
- **改行手動 cherry-pick rebase**：開新分支 `v20a196-r3` 企喺 `4e841e5`，逐個 `git cherry-pick` 返 4 個 commit（`6e80c76`→`be622a8`→`3d73e1e`→`dda0a36`），全部乾淨套入。第一個 pick 衝突 5 檔（gift185／rom176／tang171／tang173／travel114；kwan151／tang152／text125／story198 乾淨合併），解法同前兩次：逐個錨點對住 merged index.html（60806 行）核實——v200 嘅 ＋12 全部喺 L46184 之後，L46184 之前錨點唔郁，其後者 ＋12（DEF 55278→55290、WRAPPER 44554 唔郁、總行數 60806）。travel114 用 `qa196/resync_travel114_196c.py`（6e80c76→merged difflib 對位）：**51 個呼叫點全部對上，0 刪除；COUNT 12/12、FREE 33/33、flag check 0 bad；DEF 55290、WRAPPER 44554**。解完 10 檔測試＋logic 逐個跑，全部 PASS；`node --check` 兩段 inline script PASS；`git fsck` 乾淨。
- **全套 A/B（第三次 rebase 後，新基線＝pristine main `4e841e5`）**：
  - 基線：**275／12**（`qa196/suite_rebased3_baseline.txt`，獨立 worktree `~/workspace/pristine196b` 重建喺 `4e841e5` 之上跑；同 v200 落地數字一致）。
  - 工作版：**277／12**（`qa196/suite_rebased3_work.txt`）。＋2 係 v196 兩檔新測試，雙雙 PASS；FAIL 清單同基線 12 項穩定 FAIL 完全一致，**零回歸**。
- **實駕（第三次 rebase 後）**：針對性重跑 c1／c6／c12a／c12b（932，各寫獨立報告 `qa196/report196_c1-932_932.json`／`c6-932`／`c12a-932`／`c12b-932`）：**4/4 PASS，0 pageerror**——c1 連跑鏈完整、c6 故事鎖死、c12a 請柬推辭→典禮照播→落地圖、c12b 出席→典禮鎖死 3/3 舞台。v200 改咗請柬文案（gap 句「今年」／旁聽「入場觀禮」／nominee「你爭嘅獎項」），請柬標題＋「出席／推辭」掣唔受影響，流程照行；全套 932／700 證據（第一次 rebase 後，§10）仍然有效。
- **Rebased commits（分支 `v20a196-r3`）**：`e666a50`→`81885c5`→`e2141b1`→`25ca688`，parent `4e841e5`。落地嗰陣將 `v20a196` 指去呢個 tip 再推。

## §14 落地合併上 main `2de5026`（v197）（統籌，2026-11-14）

- **原因**：第三次 rebase 驗證完成、準備落地嗰陣，main 又行前咗——v197 已半落地，squash commit `2de5026` 喺本地 main（全站掣位修復 B1–B7＋C1–C7＋D1；新測試 33 項＋全套 276/12；但 push 連續 3 次斷線，pack 約 26MB，截圖 21MB，未上 GitHub）。
- **撞車處理（上級通知）**：v196 嘅 squash merge 建喺 `2de5026` 之上，**唔好 reset／rebase 冧咗佢**，commit 嘅 parent 一定要留返 `2de5026`，等 v197 搭同一程 push 上 GitHub。解衝突嗰陣只解 v196 嗰批，唔好掂 v197 標記。
- **Squash merge**：`git checkout main && git merge --squash v20a196`。**index.html 乾淨合併（＋182／−99，v196 原 diff，一字不差）**；**8 份測試檔衝突**（gift185／kwan151／rom176／tang152／tang171／tang173／text125／travel114），全部係行號 resync（v197 淨 ＋94 行，總行數 60817→合併後 **60900**）。v197 嘅 index.html hunks 唔喺 v196 改動區（CSS／掣位／手帳／day-res 等，L119–37684 一帶）。
- **合併樹錨點（已量好，60900 行）**：kwan PHRASES **31129**、EXACT C13 **31120**、relMap **31171**、NOTE_EXACT **31128**；rom GIFT_REACT **31683**、ROM176 block **53814**、rom176ApplyGiftOverrides **54182**、addLocTalkGiftActs **55321**、rom176TryIntercept **55415**、NPCS lan **6127**；tang def **31610**（0-based idx 31609）、tang call **31754**（idx 31753）；openLoc DEF **55384**、WRAPPER **44647**；text125 b.text **33671**；gift185／tang171／tang173 總行數 **60900**、DEF **55384**。
- **travel114 合併 resync**：腳本 `qa196/resync_travel114_196d.py`，base `ced807e`（60806 行）→ merged（60900 行）difflib 對位：**51 個呼叫點全部對上，0 刪除；COUNT 12/12、FREE 33/33、flag check 0 bad；DEF 55384、WRAPPER 44647**。新 COUNT：32284、35783、37931、39033、39465、39468、39499、44078、59453、59631、59777、59798；新 FREE：24741、30951、30952、30964、30965、30976、30977、31080、41022、43735、43758、53637、53756、53806、54029、54068、54074、54141、54143、54146、54173、55284、55658、55680、55831、57468、59221、59339、59340、59375、59376、59401、60248（leaveStory 嗰行已刪，HEAD 側 28330 唔要）。
- **解衝突教訓**：8 檔用 `muse.edit` 套入真值之後，**要再 `git add` 先算解決**——工作樹啱、測試 PASS 都唔等於 index 解決咗（`git ls-files -u` 仲列出 8 檔，`git diff --cached` 顯示 Unmerged）；已補 `git add` 八檔，`ls-files -u` 歸零。gift185／tang171 各有兩個 hunk（頭註解 hunk一開始漏咗，跑測試 SyntaxError 即捉到，已補解）。v197 標記零郁動：`syncConfirmPlanStamp197`／`revealCatTabs197` 喺 index.html 仲有 7 處，staged diff 入面零 "197" 行。
- **解完驗證（合併樹）**：零殘留衝突標記；10 檔測試逐個跑全部 PASS（gift185／kwan151／rom176／tang152／tang171／tang173／text125／travel114／dayflow196_static／story198_static＋`test_dayflow196_logic.js`）。
- **針對性實駕（合併樹，`/tmp/drive196_merge.py`，ROOT 改去常駐 clone）**：c1／c6／c12a／c12b（932）**4/4 PASS，0 pageerror**——c1 連跑鏈完整（Mon 拍攝→Tue 街頭→Wed 休息→Thu 落地圖）、c6 故事鎖死（冇「先返回」掣、撳外面／地圖都唔走佬、播完先返地圖）、c12a 請柬推辭→典禮照播→落地圖、c12b 出席→典禮鎖死 3/3 舞台。v197 改咗掣位 CSS＋日結板，呢四 case 尤其要睇，全部照行。
- **全套 A/B（合併樹 vs pristine main `2de5026`，獨立 worktree `~/workspace/pristine196c`）**：
  - 基線：**276／12**（`qa196/suite_merge_baseline.txt`，同 v197 落地數字一致）。
  - 工作版：**278／12**（`qa196/suite_merge_work.txt`）。＋2 係 v196 兩檔新測試，雙雙 PASS；FAIL 清單同基線 12 項穩定 FAIL 完全一致，**零回歸**。
- **落地**：squash commit parent `2de5026`（v197 搭同一程）；push 後親自 curl 核實線上 bytes／sha；落地後派 v196 設計 review。
