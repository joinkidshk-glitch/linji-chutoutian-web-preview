# NOTES — v20a165 劇情強制播放（STORY165）

- 分支：`v20a165`（工作副本 `~/workspace/linji-work165/`，基底 main `276ffa1`＝v160 落地後）
- 用戶拍板：2026-11-13 09:24（針對 v155 review B1）——**主線劇情（尤其頒獎禮）一定要播出嚟，唔畀玩家自己決定播定唔播；符合條件就硬性規定播劇情；目的係減少不穩因素**。取代 B1 舊 A／B 兩方向。
- 範圍：主線劇情節點（N1–N17／C1–C19＋F4）＋頒獎禮典禮場面。12 星巧遇、隨機事件 WF4、支線、約會等可選內容唔喺呢票，維持現狀，一行都唔好郁。
- 本票工人唔落地（落地由統籌做）。唔開 PR、唔 merge、唔 push 去 main。

## §1 觸發架構調查（實證，全部 grep＋讀 code＋探針核實）

### 1.1 條件判定（live 路徑，無地點檢查）
- `StoryOC.evalNode`（L24272 起）live 路徑只驗 weekMin／days_after_prev／needDone／fame／credit／dual／tag／season／year 等 token（`evalToken` L24199）；C6–C17 行 `STORY_GATE_3Y`（L19600 起）經 `evalGate3Y`（L25369），同樣無地點檢查。
- C17 結局閘：`{ needDone: ["C13"], weekMin: 153, yearEq: 1992, seasonIn: ["冬"], awardResolved: { ceremonyId: "award_singho_tv", year: 1992}, backstopDay: 1096}`（1992-12-01＝dayIndex 1065＝第 153 週；backstop 1993-01-01＝dayIndex 1096 過後無條件開，繞過全部條件）。C18：`{ needDone: ["C5"], weekMin: 48, yearMin: 1990, seasonIn: ["冬"]}`；C19：`{ needDone: ["C18"], weekMin: 61, yearMin: 1991, seasonIn: ["春"]}`；C6：`{ route: "route_tv", weekMin: 15}`；C6F：`{ route: "route_film", weekMin: 15}`。
- **同日禁**：`evalNode` 內 `sameDayBlock`——同一日已播完任一 C*，其他 C* 唔入可播（`lastMainDoneDay === day`）；`markDone` 寫 `lastMainDoneDay`。即強制播每日最多一幕主線；多幕同時就緒要排隊，按 N 次序一日一幕。
- **soft 路徑（opt-in dev preview，預設關）**：`BehaviorGate.gatePath()` 返 "soft" 只喺 `?softBehaviorGate=1`／`?softPreview=1` 或 localStorage `starVolunteer_softBehaviorGatePreview==="1"`；soft 下 `evalTrigger_AND_softRumor` 的 `stepLoc`／`stepFavor` 驗 `ctx.atLoc` 對 `locIdAny`。`storyNodeLocId`（L23955）：soft 下先問 `softLocId`，否則 `node.locId`，否則 `STORY_LOC_SOFT` 後備表。`STORY_LOC_SOFT`：C1 agency_ho、C2 tvb_longmen、C3 tvb_longmen、C4 agency_ho、C5 tvb_longmen、C6 tvb_longmen、C6F film_lion、C7 film_harbour、C8 cafe_cha、C9 tvb_harbour、C10 tvb_longmen、C11 tvb_longmen、C12 rec_star、C13 film_cotton、C14 tvb_longmen、C15 film_harbour、C16 rec_star、C17 tvb_longmen。
  - 注意 C17 路由分裂（v136 review A1，v153 在途）：全套文案叫玩家去星河電視台後台，但引擎路由去事務所＋茶餐廳（`BehaviorGate.locIdAny(C17)`＝`[agency_ho, cafe_cha]`，`storyNodeLocId`＝`agency_ho`）——呢個係 v153 範圍，本票唔修，只記低。強制播之後 C17 唔再經地點路由，分裂對播出無影響；v153 落地後路由歸一亦唔會同本票打架（本票唔讀 locId）。
- **playerOffer**：`listOpen({player:true})` 要求 `hasPlayerOffer`。C1–C5 有字串 offer；C6–C10 `playerOffer: true`；C11–C17 `playerOffer: None`（omit），要 `openMeetOffer` 寫入先入玩家列表——openLoc 嘅 script-lock 迴圈會喺入場嗰陣（節點 loc＋ev.ok）寫 offer。C18（`STORY_SPINE_NODES_WF1` L22074，locId agency_ho，playerOffer 字串）、C19（L22257，locId film_lion，playerOffer 字串）、C6F（`STORY_SPINE_NODES_BR89`，locId film_lion，playerOffer 字串）三者本身有 offer。C11–C17 喺 `content/story_detail_c1_to_c17.json` 入面 `locId: None`，靠 `STORY_LOC_SOFT` 後備。
- **StoryPlay.start 守門**（L26968 起）：homeEditable（手帳未確定）→ 拒播（除非 `opts.allowDuringPlanner`／`force`）；`ending78Locked()` → 拒播；stub／已完成／無 playerOffer → 拒播；`evalNode` 唔 ok → 拒播。`opts.force` 會繞過晒呢啲檢查——強制播**唔應該用 force**，要用普通 `StoryPlay.start(id)` 等佢自己再驗。播完出「劇情結算」modal，掣有「下一節」（播下一已開放幕）、「進度」（入進度頁）、「關閉」（`show("v-map")` 直接返地圖，唔經 goToMapForBrowse）。
- **現行三個播劇情入口**（本票前）：(1) 地點 sheet「播劇情：…」act 掣（tip path 或 open list，入地點先見到）；(2) 進度頁「播呢幕」掣（`data-prog77-play`，render 時 `here77 = evalNode(node, {checkNodePhase:true, player:true}).ok` 先出；委派掛喺 `#progress-list`，L58426 一帶）；(3) 舊 picker `playOpenPicker` 已無玩家入口（HUB77：頂欄 chip、選單「劇情」掣已移除，改指進度頁）。
- **HUB77「唔畀隔空播」設計意圖**：註解話進度頁掣要用 picker 同一套 evalNode，唔在場維持「去 X 就會觸發」文字。但 live 路徑 evalNode 根本唔驗地點，所以呢個意圖實際上只喺 soft 路徑先執行到；live 下掣一早已經可以遙距播（見 1.5 探針 P5）。
- **enc79 主線待播優先守門**：`enc79TryIntercept`（openLoc 掛點）有 `enc79StoryPendingAt(locId)`——嗰地點有主線待播就唔觸發巧遇（留返同日下次入場）。巧遇上限：每日 1 次、每週 2 次（星期一重置），冷卻 3 日。
- **出行額度**：`TRAVEL114_DAILY_CAP = 2`，狀態 `S.travel114 = { day, used}` 跟 save 走；計數只喺 `openLoc` 閘口 `travel114TrySpend` 發生（全檔只一處呼叫）；`travel114IsFree` 只認 `forceRestore`／`encDone`／`wf4Done`／`travelFree`（屋企 `home` 免費）。強制播唔經 openLoc → 唔食額度（見 §5）。
- **既有自動推先例**：`autoPushC1IfNeeded(opts)`（L38229）：C1 可播時 ensure offer；`opts.play` 先至 `StoryPlay.start("C1")`，且 homeEditable 時只 ensure offer、唔播。現時無任何 caller 用 `play:true`（`postTutorialEntry` 用 `play:false`，因 v19z12 M3：教學後唔喺手帳未確認時全屏播 C1；`paintStoryEntryHints` 無 opts）。`ensureWeekPlanCommittedForStory` 會靜默提交週計劃（將 planDraft 寫入 `S.weekPlan`、清 `homeEditable`）——地點 sheet／進度頁掣／home-story-hint 撳掣前都用佢；但自動強制播唔應該靜默提交，應該 defer。
- **地圖提示（實時）**：`storyMapHintHtml`（L38530 起）——地圖提示行「有劇情 · {label}」＋下一幕進度句首句，成行係掣（`data-prog71="1"`）撳入進度頁；唔寫「到現場先可播」，唔跳地點，**唔使改**。`paintStoryEntryHints` 頂欄 chip 標題：「主線進度 · 有 N 幕可播」／「主線進度（暫無可播）」。`refreshStoryMapTips` 將 open 主線寫入 `S.mapTips`（地圖「劇」針）。
- **home-story-hint 係死碼（v20a71 PART3C 起停用）**：`storyHomeHintHtml`（L38580 起）自 v71 起無任何呼叫方——enterHome 唔再填充卡面內容，「劇情」提示一併停用（劇情進度改由地圖提示行＋手帳「進度」頁承載）；`wireHomeStoryHint`（L38631 起）嘅掣 `#home-story-open` 永遠唔存在，handler 永遠唔會跑。本票初稿改過呢兩處，實駕核實係死碼後**已全部還原**（見 §7），唔做無謂 churn；測試 `test_story165_static.py` §七只斷言死碼留返原樣。
- **C17 前夕**：`StoryPlay.start` 內 C17 會經 `ending410EveNode` 重建節點；抉擇後 `ending410AfterEveChoice` 直接入結局呈現（寫 `S.ending410`）。

### 1.2 `goToMapForBrowse` 晨鏈（L37606 起，順序重要）
`ending78Gate` → 殺青獎勵 pending（`presentPendingPostShootReward`，callback 重入）→ 頒獎請柬（`queueAwardsOnSeasonWindow`＋`presentPendingAward`，callback 重入）→ 次日朝早報紙（`presentDueMorningPaper`，callback 重入）→ 試鏡消息（`aud91PresentDue`，callback 重入）→ WF4 待播（`wf4PresentPending()`，**無 callback**——`wf4Fire(ev, ()=>goToMapForBrowse())` 由 WF4 自己重入）→ 病日閘（`hosp96TreatGate`／`conseq61ResolveSickDay`，劇情進行中唔截）→ `kickScheduleIfNeeded()` → `nudgeRegionForToday()` → `closeSheet()` → `atLoc=null` → `show("v-map")`＋`paintBar()`＋`drawMap()`＋行程 toast。
- `kickScheduleIfNeeded`（L37578）：只喺 `todayIsForcedDay()` 先 `resolvePlannedDay(id)`（今日已排定行程，繼續進行），否則返 false。`resolvePlannedDay` 會將當日行程行落去，完咗經重入返返嚟。
- `wf4PresentPending`（L40574）：已結局／forced day／病日 → 唔播；芬姐送別戲優先；否則 `wf4Fire(ev, ()=>goToMapForBrowse())`。
- 晨鏈每一步都係「有 pending 先截住、跑完 callback 重入」——強制播掛喺鏈尾係唯一唔會打斷任何 modal 嘅位（見 §2）。

### 1.3 頒獎禮三條路徑（現行，本票前）
- 觸發：`goToMapForBrowse` 內 `queueAwardsOnSeasonWindow()`＋`presentPendingAward()`（請柬彈出先截住）；邀請 modal 掣「出席」／「推辭」，`onDismiss`＝推辭（v136：「稍後」已拎走，dismiss 即推辭）。一年四場：廣告賞春／金碟夜夏／影藝獎秋／台慶冬。C10 anti-stack：每年第 49–52 週 TV 典禮讓路畀 C10。
- (1) 出席：`awards62PlayCeremony(pack, ()=>presentAwardResult(pack, cont))`——典禮 6 beats 約 9.6 秒（v147：gallery 宣佈弧 open 1200＋pan 2000＋names 2400＋suspense 1400＋reveal 2100＋out 500＝9600ms；won 分支 v160 後全長 11550ms，因 M4 walkup beat 2200ms），跟住結果卡。典禮有「跳過 ⏩」掣＋撳畫面快進。
- (2) 旁聽（gallery tier）：同一 ceremony，`bestOutcome==="gallery"`——玩家唔上台、無 "me" 卡、唱名只列 fellows、得主＝fellows[0]、無 comfort beat、無 glamour。結果卡照出（badge「觀禮」）。
- (3) 推辭：**無典禮、無結果卡**；只係第二日報紙講結果（declined 專用文案：`enqueueNewspaperFromAward({...pack, skipped:false}, {declined:true})`，行典禮級 press 文案，fameDelta 0，唔派聲望，**唔可以寫阿偉贏獎／出席**——self-check `declined_copy` 會 FAIL 如果 headline+dek 含「阿偉」）；`commitAwardToLog` 寫 `skipped:true`、rewards 歸零、`awardsSetFlag(year, ceremonyId, "skipped")`——所以 C17 `awardResolved` 計推辭（「去現場／旁聽／推辭都計」）。
- 典禮內部得主規則（v147／v149，**唔准寫死得主**）：`best = pack.bestOutcome || "gallery"`；`winFellow = focus.winner63 || fellows63[0]`；`winner63` 只喺 outcome==="nominated" 嗰陣設做 `fellows63[0]`，gallery 嗰陣係 null；won 嗰陣得主係玩家本人。gallery beats 入面 `gWin = fellows[0]`。`awards62CeremonyBeats`：gallery 分支（pan 2000「今晚你坐喺觀禮席…」＋names＋suspense＋reveal＋out，無 comfort）；非 gallery 分支有 enter／names（含阿偉）／suspense／reveal（won 嗰陣「得獎！」＋glamour 條件、nominated 嗰陣 reveal 後加 comfort beat 2600ms「何生拍拍你膊頭：『差少少啫…』」）。

### 1.4 玩家可以 skip／唔播劇情嘅所有路徑（本票前）
1. 唔去地點：主線只經地點 sheet／進度頁掣觸發，唔去現場就永遠唔播（最主要嘅漏播路徑）。
2. 進度頁掣三態（v155 B1）：掣有無取決於入場路線，soft 路徑下經手帳入就無掣（見 1.5）。
3. 推辭頒獎禮：典禮場面完全唔播，只剩第二日報紙。
4. 典禮「跳過 ⏩」掣＋撳畫面快進：場面可以跳過——呢個係場面內嘅快進，唔係「唔播劇情」，本票保留（見 §4）。
5. 結算 modal「關閉」：播完先可以關，唔係 skip。
6. C1 教學後：`postTutorialEntry` 用 `play:false`，C1 唔會自動播，要玩家自己去事務所。

### 1.5 v155 B1 三態根因（探針證實）
- 探針：`~/workspace/linji-probe165/probe165.py`（mirror `~/workspace/linji-probe165/`，HEAD 276ffa1，port 8997），結果 `probe165.json`，全程 0 pageerror／0 failed request。關鍵發現：**review 驅動行 `?softPreview=1`**（`drive142r_base.py` L13–14），即 review 環境行 soft 路徑。
- soft 下：fresh map 時 `evalNode(C1).ok === false`（reasons `['locIdAny']`，atLoc=null）；探訪事務所後 `ok === true`；`ignoreSheetLoc:true` 版永遠 ok。`listOpen` openIds 全程 `['C1']`（因用 ignoreSheetLoc）。`atLoc` 由 `openLoc(agency_ho)` 設定，由 `enterHome`／`goToMapForBrowse` 清零（`atLoc=null`）。diag2.py 流程證實：A（探訪事務所後 chip 入）atLoc=agency_ho → 有掣；B（先「返回地圖」再 `open_notebook` → `enterHome` → atLoc=null）→ 無掣；C（chip 再入，atLoc 仍 null）→ 依然無掣。
- live 下（無參數）：fresh map `evalNode(C1).ok === true`，A／B／C 三態全部有「播呢幕」掣（97px 行，文案「你而家喺何生事務所，可以即刻播呢幕。」）。即 **B1 三態喺出貨 live 版重現唔到**，係 softPreview review 環境先有嘅現象；但背後矛盾係真：HUB77「唔畀隔空播」意圖只喺 soft 路徑執行，live 下進度頁掣一早可以遙距播。
- 探針 P5：live 下由地圖直接 `StoryPlay.start("C1")` 成功（started:true，`#mask.story-play-on` 出現）；soft 下同樣呼叫失敗（started:false，因 atLoc 已清零、soft stepLoc 唔過）。附帶觀察：probe 入面 `typeof atLoc` 讀做 UNDEF（`let` 頂層變數經 evaluate 讀唔到），但 `S` 讀得到；機制結論以 evC1 翻轉為準，atLoc 讀數問題唔影響結論，唔使再追。

### 1.6 v149 衝突檢查（`~/workspace/linji-work149/`，未落地工作目錄）
- v149 diff（相對舊底）：index.html 171 行改動，集中 CSS（~L761–797、~L4431–4453）、`renderAwardResultHtml`（~L45586）、`renderAwardsPane62`（~L46000，B2 得主標記 `w149 = c.winner63 || (gallery 時 fellows63[0])`）、`awards62PlayCeremony` 內部（~L46175 起：cardsData `win` 旗、M5 彩紙 GIF `syncConfetti149` 喺 reveal／comfort／out 顯示）、`awards63FocusFellows`（~L46674 起：`winRaw = c.winner63 || (gallery 時 fl[0])`，新增 `awardWinner149`／`awardWinLine149` helper）；另 `tests/test_text125_static.py`、`tests/test_travel114_static.py` resync；新檔 `assets/fx/awd_confetti_m5.gif`、`qa149/`。v149 無分支喺 origin（`git branch -r` 無 v20a149／v20a156／v20a158）。
- 本票掂嘅位置（新底行號）：`presentAwardInvite` 嘅 `skip()`（L45502 起）、`awards62CeremonyBeats` 嘅 gallery 分支（L45960 起）——**同 v149 hunks 無重疊**（v149 唔掂 invite modal 掣行為，亦唔掂 beats 函數）。本票 diff 8 個 hunks（見 §7），全部喺 v149 hunks 之外。v149 落地嗰陣 rebase 可能漂移行號，要對位核實。v160 已落地，佢改嘅典禮內部（walkup／M1 底圖／M6／M9）本票唔掂。

## §2 觸發時機決定

- **決定：`goToMapForBrowse` 尾段，病日閘之後、`kickScheduleIfNeeded()` 之前。**新增 `story165NextForced()`／`story165TryForcedPlay()`（放 `autoPushC1IfNeeded` 附近），由 `storyOpenSnapshot()`／`listOpen({checkNodePhase:true, player:true, ignoreSheetLoc:true})` 取第一幕未播主線（C1–C19＋C6F，按 N 次序：prog71 `order71` 嗰套——C1–C6、C6F、C18、C19、C7–C17），只播一幕（同日禁保證）。
- **擺位理由**：晨鏈早段（請柬→報紙→試鏡→WF4→病日）已串行跑完，強制播唔會打斷任何 modal。掛點喺 `if(kickScheduleIfNeeded()) return;` 嗰行**之後**、地圖顯示之前——呢個擺位同時滿足「唔打斷 modal」同「唔搶拍攝日」：forced day（拍攝日）嗰陣 `kickScheduleIfNeeded()` 返 true 會直接 `return`，強制播掛點根本行唔到，故事自動順延到下次返地圖；free day kick 返 false，掛點即刻試播。考慮過嘅替代擺位：(a) kick 之前——拍攝日故事會搶先播，結算「關閉」直返地圖，行程未 kick，玩家要手動撳「開始今日行程」先開始拍攝日，有 miss 拍攝日風險，否決；(b) 朝早結算後即時中斷——會撞請柬／報紙／試鏡 modal，否決；(c) 入地點嗰陣——要食出行額度，同 §5 衝突，否決。
- **守門**（`story165CanPlay`）：`!S.homeEditable`（唔靜默提交週計劃，defer 到下次返地圖）、未結局（`ending78Locked`／`ending78Gate`）、故事未進行中（`isStoryPlayActive()`／`_storyPlayLocked`）、節點存在且 eval ok。C11–C17 等 omit 節點先 `StoryOC.openMeetOffer(id, "forced165")` 寫 offer，再用普通 `StoryPlay.start(id)`（唔用 `force`，等 start 自己再驗 eval＋offer＋homeEditable＋結局鎖）。start 返 false 就跌返地圖，唔重試、唔 loop。掛點有 try/catch 跌返地圖（`catch(_s165){}`），強制播出事唔阻返地圖。
- **排隊**：多幕同時就緒按 N 次序，一日一幕；時窗已過（missed）嘅幕唔會入 open，唔會播。
- **中途變 open**（例如喺地點入面攞到 tag 達標）：等下次返地圖先播；地點 sheet「播劇情」掣保留做後備路徑。
- **C1 開局**：fresh game「確定出發」後首次返地圖即播 C1（開局條件滿足即硬播，係用戶拍板嘅字面要求；舊 `autoPushC1IfNeeded({play:true})` 機制本身就係為呢個而設，只係一直無 caller 用 `play:true`）。
- **純粹返地圖 bypass（實駕核實）**：`book70ExitHome`（手帳「返回地圖」）同 `#loc-close`（地點 sheet「返回地圖」＝`closeSheet`）都係純粹返地圖，**唔經 `goToMapForBrowse`**，所以唔會觸發強制播——玩家喺呢兩條路返地圖嗰陣，有待播主線都唔會即刻播。故事唔會無限期唔播：下一次行晨鏈嗰陣一定播——「開始今日行程」（`startTodayScheduleFromMap` → map 日直行 `goToMapForBrowse`）、確認行程（`commitPlanAndGo` → `runScheduleFromToday`）、下一日朝早晨鏈、WF4 完成重入。最壞情況係順延到聽朝。呢個係設計分叉，見 §8 第 7 項（本票唔自作主張擴範圍）。
  - **(c) 更新（2026-11-13 11:11 用戶拍板，見 §9）**：兩條路而家都掛咗強制播——`book70ExitHome` 本體＋`#loc-close` 撳掣包裝；`closeSheet()` 本體**無掛**（調查結論：~30 個 call sites，`modal()` 每次開 modal 都 call 佢）。第三條純返地圖路 `#home-back-map` → `leaveHomeFromNotebook("map")` 仍然係 bypass，留返統籌決定（見 §9）。
- **homeEditable 順延嘅觀察條件**：`enterHome(summary, editable, ...)` 用 `editable` 參數決定 `S.homeEditable`——選單入手帳永遠係唯讀（editable=false），會改寫之前播種嘅 true；homeEditable=true 只喺編排入口存在（週一／教學後 planner）。所以靜態測試覆蓋順延守門，實駕唔硬測呢態（case A 教學後確認流程已覆蓋：確認前唔播，確認後即播）。

## §3 掣處置

- **進度頁「播呢幕」掣：拎走（首播不再經掣觸發）。**open 行文案改做「已經開放——返地圖嗰陣就會播出。」＋場景資料「（場景：X）」（地點留返做場景資料，唔係觸發條件，唔寫「去 X 就會觸發」——`test_progress71_logic.js` B1 斷言要求已開放行照樣講明地點，場景 framing 兩邊兼顧）；`data-prog77-play` 掣＋`#progress-list` 委派一併拎走；HUB77 註解更新。B1 三態根除：掣本身唔再存在，唔可以再有「有時有、有時冇」。
  - `.prog71-play` CSS 留返（死規則，v155 測試 `test_v155_static.py:51` 照過；刪 CSS 無謂，只會多改一檔測試）。
  - `prog71LocName`／`r.locName` 留返（rows 仍計 locName，無其他讀者；刪佢無謂）。
  - 保留：地點 sheet「播劇情」掣（後備路徑）、結算 modal「下一節」（玩家主動接續）、`enc79TryIntercept` 主線待播優先守門、舊 picker 繼續無玩家入口。
- **`storyHomeHintHtml`／`wireHomeStoryHint`：唔郁（死碼，見 §1）。**實時提示係地圖提示行（`storyMapHintHtml`，掣入進度頁，唔寫「到現場先可播」），唔使改；進度頁文案已承載新規則。
- **頂欄 chip 標題唔郁**：「主線進度 · 有 N 幕可播」／「主線進度（暫無可播）」保留——「可播」而家意思係「返地圖就會播出」，進度頁文案承載新規則；改 chip 會多改 `test_hub77_static.py` 一處斷言，無必要。
- **測試影響**：`tests/test_hub77_static.py` §4 按 v165 新規格改寫（掣拎走＋委派拎走＋掛點在位）；`tests/test_v155_static.py` 唔受影響（CSS 留返）。

## §4 頒獎禮各路徑決定

- **推辭都播典禮——電視直播版（gallery 觀察者路徑重用）。**`presentAwardInvite` 嘅 `skip()` 改做：先 `awards62PlayCeremony({...pack, bestOutcome:"gallery", declined165:true}, done)`，播完先行原有 skip bookkeeping（`pack.skipped=true`、rewards 歸零、`commitAwardToLog`→flag skipped、declined 報紙第二日出、toast「已推辭席位」），再 `cont()`。try/catch 跌返舊 skip 路徑（跟 attend 嗰套寫法）。
  - reload 風險同 attend 一致：播典禮期間 reload，請柬已清（`_pendingAward`／`S.pendingAwardPack` 已清）但 log 未入（flag 仲係 invited）→ `restorePendingAward136` 會按 flag 重建請柬（category 可能唔同）。attend 路徑本身就有同一窗口，本票唔引入新類別嘅風險。
- **`awards62CeremonyBeats`**：`pack.declined165` 嗰陣只換 gallery 分支嘅 pan 字幕做電視直播 framing（「今晚你喺屋企睇電視轉播\n台上群星逐一亮相，記住呢晚。」代替「今晚你坐喺觀禮席…」）；names／suspense／reveal 照舊（只列 fellows，得主＝fellows[0]，動態讀 `winner63 || fellows63[0]`，**唔寫死得主**）。無 comfort beat、無 glamour、無玩家上台、無 "me" 卡——全部係 gallery 分支本身已有嘅行為。播完唔出結果卡（維持現狀：declined 報紙第二日先講結果）。
  - 舞台視覺維持會場圖（v160 M1 底圖）：字幕承載「電視轉播」fiction，畫面本身唔改——v149 落地後舞台幾何可能變，嗰陣再重驗。
  - Declined 嗰陣「forfeit 贏獎」fiction 同現有規則一致：rewards 歸零、declined 報紙唔提阿偉贏獎（self-check `declined_copy` 守住）。
- **出席／旁聽路徑唔郁。**邀請 modal「出席／推辭」選擇保留；`onDismiss`＝推辭 → 同樣播直播版典禮。典禮本身「跳過 ⏩」掣保留（場面跳過≠劇情唔播；用戶拍板係「一定要播出嚟」，唔係「唔畀跳過」）。
- v149／v160 無重疊（見 §1.6），但要喺 NOTES 記低對位行號（見 §7）。

## §5 額度問題結論

- **強制播唔食出行額度。**計數只喺 `openLoc` 閘口 `travel114TrySpend` 發生（全檔只一處呼叫，L53596）；強制播唔經 `openLoc` → 唔經 `travel114TrySpend` → 唔食額度。實駕 case A 證實：C1 播完 `travel114.used` 仍係 0。
- 正常入地點照舊計數（每日 2 次上限唔變，`TRAVEL114_DAILY_CAP = 2`）。
- 強制播亦唔經 `enc79TryIntercept`（嗰個係 openLoc 掛點）——但 enc79 守門嘅目的係「有主線待播嗰陣唔好畀巧遇搶先」；強制播本身就係播嗰幕主線，守門無嘢要守。

## §6 測試＋實駕結果

### 靜態測試（逐個直接跑，全部 PASS）

- `tests/test_story165_static.py`：**29/29 ALL PASS**（強制播三函數、掛點、守門、選幕、普通 start、唔經 openLoc、進度頁掣拎走、死碼留原樣、推辭直播版、得主規則、C17／C18／C19 閘、額度 cap 2、SAVE key 等）。
- `tests/test_hub77_static.py`：**ALL PASS**。
- `tests/test_travel114_static.py`：**RESULT PASS**（免費 27 處＋計數 13 處＋定義／wrapper／測試區 4 處）。
- `tests/test_progress71_logic.js`：**87 PASS**（node 直接跑，0 FAIL）。
- JS 語法：兩個 inline script block `node --check` 全部 OK。

### 反證（對 pristine main `276ffa1`，`/tmp/index165_pristine.html`，5,213,030 bytes）

- story165：20 FAIL／9 PASS，exit 1，唔 crash。9 項 PASS 係唔變嘅斷言（強制播唔經 openLoc、推辭 bookkeeping、得主規則、C17／C18／C19 閘、額度、SAVE key、巧遇／WF4、CSS）。
- hub77：對 pristine 6 FAIL（5 項 v165 新規格＋1 項 NOTES_V20A77 路徑 artifact——`/tmp` 檔嘅 parent 唔係工作副本，唔係真回歸）。

### 全套 A/B（`qa131/run_suite.sh`，帶參數跑）

- 舊底基線（v152，`40702c7`）：**217 PASS／12 FAIL**（`/tmp/suite165_base.out`）。
- 新底基線（v160，`276ffa1`）：**221 PASS／12 FAIL**（`/tmp/suite165_base160.out`）。
- 工作版第二輪（home hint 還原前）：222／12。
- **276ffa1 底最終樹：`TOTAL PASS 222 FAIL 12`**（`/tmp/suite165_final.out`，正確參數重跑確認）。＋1＝新 `test_story165` 檔；12 項 FAIL 同新底基線**完全一致**（flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38），**零回歸**。
- 註：中途有一次無參數跑 suite（ROOT／OUT 空），TOTAL 同樣 222／12 但逐檔明細冇寫入檔；已用正確參數（`run_suite.sh <repo-root> <outfile>`）重跑確認，明細同基線一致。教訓：suite 一定要帶參數跑。
- **rebase 上 da05b32（v164＋v166）後最終樹：`TOTAL PASS 224 FAIL 12`**（`/tmp/suite165_final166b.out`，第二輪；新底基線 pristine `da05b32` 係 **223／12**，`/tmp/suite165_base166.out`，經 `git worktree` 喺 `~/workspace/linji-base166` 跑）。＋1＝新 `test_story165` 檔；12 項 FAIL 同新底基線**完全一致**，**零回歸**。
  - 第一輪 rebase 後跑出 207／29（`/tmp/suite165_final166.out`），多出 17 項 FAIL 全部係 .py（aud91／aud91fix122／aud91fix124、awards160_m1／m4／m6／m9、awards166、awards62／63、awards64／awards64_chibi、book70／141／143／145、br89）——**逐個直接跑全部 PASS**，證實係已知批量波動（見 AGENTS.md：同一 repo 連續跑出唔同總數，失敗項每次唔同、全部係 .py），唔係回歸。第二輪即刻返到 224／12。
  - 註：基線嗰陣 /tmp（512M tmpfs）爆滿過一次（`git archive` 解出成個 repo 323M）——教訓：唔好將成個 repo 解去 /tmp，用 `git worktree` 喺 workspace 下面做基線。

### 實駕（`drive165.py`，live 模式唔用 softPreview，mirror 工作副本，port 8998，430×932，槽 3）

結果檔 `drive165/drive165.json`；截圖 `drive165/shots/`（20 張，未入 commit，工作目錄留檔）。四 case 全部 PASS，0 pageerror。**rebase 上 da05b32 後重跑一次，同樣 4 case 全部 PASS**（A 8/8、B 17/17、C 28/28、D 10/10；decline 總長 10880ms、attend 10582ms；0 pageerror）：

- **Case A fresh_c1：PASS 8/8**。新遊戲→跳過教學→確定出發→C1 即播（maskOn，標題「先學做動作戲／先賺」，何生事務所），travelUsed 0，C1 未做完；pump 20 次「下一句」／抉擇播完，結算 modal（「進度」／「關閉」，抉擇「跟張子駿班底學動作戲」），C1 done，返地圖，travelUsed 仍 0。
- **Case B progress_3states：PASS 17/17**。播種 day 21（第 4 週）、C1 done、gigCount 3、rumors `["tvb_rules_gossip"]` → C2 open、eval ok。B態（手帳入）／A態（探訪事務所後 chip 入）／C態（再 chip 入）三態全部無「播呢幕」掣、有「返地圖嗰陣就會播出」＋「場景：星河電視台」、無舊「就會觸發」文案；手帳「返回地圖」純粹返地圖，故事暫唔播（預期，bypass）；撳「過一日」去到下一日朝早，晨鏈行到 C2 即播，播完 C2 done，返地圖。
- **Case C decline：PASS 28/28**。seed day 657（1991-10-20）、done C1–C5＋C18＋C19，`__awards.debugForceSeasonWindow`＋`present()` 強制 gallery 典禮（`award_harbour_film`）。請柬有「推辭」、無「稍後」；推辭後典禮即播（「跳過」掣可見），beats open／pan／names／suspense／reveal／out，pan 字幕係「今晚你喺屋企睇電視轉播\n台上群星逐一亮相，記住呢晚。」（唔係「觀禮席」），無 comfort beat，reveal 得主廖炳星憑《離岸的信》得獎（唔係阿偉），總長 9381ms ≈ 9.6 秒，舞台播完消失，無結果卡，返地圖，flag `1991/award_harbour_film`＝skipped，pending 清零，報紙已排隊；第二日報紙 declined 版（template `award_declined.film`，fameDelta 0，headline+dek 無「阿偉」；文案：「影藝獎夜，銀幕外多一行／維港影藝獎散場。金禧大酒店門外，票房話題以外，亦有新人入圍消息。」）。
  - 過一日嗰朝：先出咗 C1 路線報紙（`story:C1:route_tv`），之後晨鏈行到掛點，**C6 即播**（「飯堂閒角」），播完 C6 done，返地圖。declined 報紙嗰朝未出——仍喺 queue（publishDay 658），一日一報紙嘅現行排隊，唔係 v165 改動；v147 已驗過 declined 報紙本身會出。
  - **debug165b 懸案已解（唔係 bug）**：decline 典禮後 C6 唔即刻播，原因係 drive 經 `__awards.present()` debug 路徑彈請柬，佢嘅 cont 係 no-op（`presentPendingAward(undefined)` → `cont = function(){}`），典禮後唔會重入晨鏈，掛點自然唔會行。真實路徑（晨鏈出請柬，L37620）嘅 cont 係 `()=>goToMapForBrowse()`，典禮後即刻重入，掛點即刻播。`debug165c.py` 亦證實 `StoryPlay.start("C6")` 喺 seed 態直接返 true，C6 播得郁（24 句播完，抉擇「熬日子：接固定閒角」）。
- **Case D attend：PASS 10/10**（對照組）。seed 同 decline；出席路徑 pan 字幕「今晚你坐喺觀禮席\n睇住台上群星，記住呢晚。」（無電視轉播文案），無 comfort beat，總長 10613ms，結果卡照出（badge「觀禮」，同屆提名三人齊），返地圖。

## §7 rebase 紀錄

- 開工基底：main 遊戲 `40702c7`／NOTES `222a984`（v152 落地後），基線全套 **217／12**（`/tmp/suite165_base.out`；12 項穩定 FAIL：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38）。
- 工作期間 v160 落地（2026-11-13 09:30 核實，main 變成遊戲 `109422b`／NOTES `276ffa1`）：M1 會場底圖、M4 修好版 GIF＋walkup beat 2200ms、M6 燕尾服、M9 fanfare take 1＋掌聲 MP3；全套 rebase 後最終樹 221／12。
- 已 rebase 上新 main：`git rebase origin/main` 乾淨完成，HEAD `276ffa1`。新底基線全套 **221／12**（`/tmp/suite165_base160.out`，核實：`TOTAL PASS 221 FAIL 12`）。
- 本票 diff（相對 `276ffa1`）：index.html 6 個 hunks，85 insertions(+)、43 deletions(-)（淨 ＋42 行）：
  1. `goToMapForBrowse` 尾段 L37641：＋8 行（強制播掛點＋註解）。
  2. `autoPushC1IfNeeded` 之後 L38263：＋49 行（`story165NextOpen`／`story165CanPlay`／`story165TryForcedPlay` 三函數）。
  3. `renderProgressPane71` L43999：−11 行淨（here77／播掣拎走＋文案改＋場景後綴）。
  4. `presentAwardInvite.skip` L45560：＋9 行淨（先播直播版典禮，播完先 finishSkip）。
  5. `awards62CeremonyBeats` gallery pan L46023：＋3 行（declined165 電視 framing＋註解）。
  6. prog77 委派 L58589：−16 行淨（委派拎走＋註解）。
  - home hint 兩處（`storyHomeHintHtml`／`wireHomeStoryHint`）初稿改過，實駕核實係死碼（v71 起停用）後**已全部還原**，唔計入 diff；`qa165/resync_travel114.py` 兩次運行都核實 difflib 只得本票 hunks（第一次 8 個，含 home hint；還原後 6 個）。
  - v149 對位（見 §1.6）：零重疊。`renderAwardResultHtml`（新底 L45468，v149 hunk 區）／`renderAwardsPane62`（L45887）／`awards62PlayCeremony` 內部（L46108 起）／`awards63FocusFellows`（L46687）／CSS hunks 全部唔掂。
- 測試檔：新 `tests/test_story165_static.py`（29 項斷言，§七改為死碼留原樣斷言）；`tests/test_hub77_static.py` §4 按 v165 新規格改寫（6 項斷言改寫＋1 項新增掛點斷言，`w` 段錨點改用 v165 註解）；`tests/test_progress71_logic.js` B1 斷言按新規格改寫（已開放行「返地圖嗰陣就會播出」＋「場景：何生事務所」，唔再斷言「去何生事務所就會觸發」）；`tests/test_travel114_static.py` resync（`qa165/resync_travel114.py`：difflib 只得 6 個 hunks，其餘純漂移；COUNT 13／FREE 27 不變，DEF 53540→53598、WRAPPER 44034→44080）。
- 行號漂移監察：全套 A/B 證實其餘釘行測試（kwan151／tang152／text125 等）唔受影響，唔使 resync。
- **rebase 上 da05b32（v164＋v166），2026-11-13 10:xx**：工作期間 v164（`3973d4a`，鄧麗萍送禮補完）＋v166（`da05b32`，glamour 海報縮細並置＋空字幕框隱藏）相繼落地，main 由 `276ffa1` 變成 `da05b32`（NOTES `60b0a8f`）。先 commit（`69d1ad8`，276ffa1 底）再 `git rebase origin/main`：index.html 自動合併，**只有 `tests/test_travel114_static.py` 衝突**（兩邊都 resync 過同一批行號）。解決：拎上游版（`git show origin/main:...`），`qa165/resync_travel114.py` 改對位 pristine `da05b32`（`/tmp/index166_pristine.html`）重跑——difflib **只得 6 個 STORY165 hunks**，其餘純漂移；新數字同 rebase 前完全一致（COUNT 13／FREE 27、DEF 53540→53598、WRAPPER 44034→44080、openLoc( 44 不變），因為 v164／v166 淨增值全部喺 DEF 之後（送禮掣 ＋16 喺 53879）或淨零（CSS／PlayCeremony 替換）。`GIT_EDITOR=true git rebase --continue`（EDITOR 未設，唔好用預設 --continue）。rebase 後 HEAD `a5d77f0`，index.html diff 仍係 6 hunks、＋85／−43。
  - v166 對位：v166 改嘅典禮區係 glamour overlay CSS＋`awards62PlayCeremony` 內部（`setCaption` 空字幕隱藏，L46254）＋won 分支；本票掂嘅係 `presentAwardInvite.skip`＋`awards62CeremonyBeats` gallery pan 字幕，**無重疊**。rebase 後實駕 4 case 全部 PASS（decline 總長 10880ms、attend 10582ms，v166 C1 無影響）。
  - 新底基線：pristine `da05b32` 全套 **223／12**（`/tmp/suite165_base166.out`）；rebase 後工作版第二輪 **224／12**，FAIL 集同基線一致，零回歸（見 §6）。
  - 注意：v168 已開工（用戶 10:23 拍板修 v166 review C1：glamour 期間壓暗／隱藏提名卡列），改緊同一典禮檔但係 glamour beat，同本票 hunks 無重疊；佢落地嗰陣要留意唔好撞。
  - 附帶：v166 commit message 話全套 223／12，MEMORY 嗰陣寫 222／12——suite 總數會波動，以 FAIL 集為準（兩邊都係同一批 12 項）。
- **rebase 上 807440f（v157），2026-11-13 統籌**：工作期間 v157 落地（`807440f`，C1–C17 全幕重寫＋F4／G4 新寫＋C18／C19 輕微潤色；機制唔郁；全套 rebase 後 225／12）。`git rebase origin/main`：index.html 自動合併，**只有 `tests/test_travel114_static.py` 衝突**（兩邊都 resync 過同一批錨點）。解決：拎上游版（`git show origin/main:...`），新寫 `qa165/resync_travel114_157.py` 對位 pristine `807440f`（`/tmp/index157_pristine.html`）重跑——difflib **只得 6 個 STORY165 hunks**（＋8／＋49／16→5／8→17／1→4／18→2，淨 ＋42），其餘純漂移；42 個錨點內容逐行相同（COUNT 13／FREE 27，openLoc( 44 不變，FREE 唔帶旗 0 處、COUNT 帶旗 0 處）；DEF 53610→53668、WRAPPER 44104→44150。數字替換用單次掃描 dict 查表（AGENTS.md v160 教訓，唔用逐對 re.sub）。rebase 後四檔逐個重跑全部 PASS（story165 29/29、hub77、travel114 RESULT PASS、progress71 87 PASS）。
- **(c) rebase 上 fc1a1aa（v167＋v168 落地後），2026-11-13**：工作期間 v167（`280af68`，鄧麗萍咖啡豆 liked 句）＋v168（`5e6a6b0`，glamour 卡列隱藏）相繼落地，main 由 `807440f` 變成 `fc1a1aa`（NOTES `fc1a1aa`）。先 commit (c)（`801ef0c`）再 `git rebase origin/main`：**乾淨完成，零衝突**（兩 commit 一併 rebase：`ba81165`＋`5e8df57`）。difflib 對 pristine `fc1a1aa`（`/tmp/index165_main.html`）核實：只得 **8 個 opcodes**（原 6 hunks＋(c) 3 hunks，其中新函數＋49 同 helper＋15 相鄰合併做一個 ＋64 insert；淨 ＋73＝＋42＋＋31），其餘純漂移；`openLoc(` 44 不變。直接受影響測試逐個重跑全部 PASS（story165 39/39、hub77、travel114 RESULT PASS、progress71 87 PASS、book70、book141、lock78、ux68）。全套 A/B（`qa165/run_suite165.sh`，workspace 寫入版）：基線 pristine `fc1a1aa`（worktree `~/workspace/linji-base165c`）**227／12**，工作版最終樹 **228／12**（＋1＝新 `test_story165` 檔；12 項 FAIL 同基線完全一致——flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38，**零回歸**）。實駕 `drive165.py all` 喺最終樹重跑（見 §9.5）。v170 已開工（用戶 11:23 追加：提名人 Pixellab character＋移上舞台），佢落地嗰陣典禮區要重驗。

## §8 設計分叉

調查期間遇到嘅分叉，大部分已按用戶拍板原則／現行規則決定；但有一項係真正要拍板嘅分叉，留返畀統籌問用戶（本票唔自作主張擴範圍）：

**未決分叉（交統籌問用戶）：**
7. **純粹返地圖 bypass——要唔要將強制播掛埋去 `closeSheet`／`book70ExitHome`？**~~現狀：強制播只掛喺 `goToMapForBrowse` 尾段；手帳「返回地圖」（`book70ExitHome`）同地點 sheet「返回地圖」（`closeSheet`）係純粹返地圖，唔經晨鏈，故事唔會即刻播，最壞順延到聽朝晨鏈。選項：(a) 接受現狀（本票決定）——故事永遠唔會無限期唔播（聽朝晨鏈一定播），改動最細，唔掂兩條「純粹返地圖」路徑嘅契約；(b) 掛埋去 `book70ExitHome`（手帳出口，較安全——嗰刻無 modal 開緊）＋唔郁 `closeSheet`；(c) 兩條都掛——「返地圖就會播出」字面成立，但 `closeSheet` 喺好多 modal 流程入面都會跑（開 sheet 前、結算後、encounter 後），故事 stage 疊喺 modal 上面嘅風險要另外調查，唔係本票可以順手做嘅。~~
    **已拍板 (c)（用戶 2026-11-13 11:11）＋已實作（見 §9）**：兩條都掛。調查結論：`closeSheet()` 本體唔掛（~30 個 call sites，`modal()` 每次開 modal 都先 call 佢，掛本體會喺每個 modal 之前誤播）；掛嘅係兩個真正「返回地圖」嘅用戶動作——`book70ExitHome` 本體＋`#loc-close` 撳掣包裝；modal 閘做咗 helper `story165ModalOpen()`，只供兩條新掛點用（唔可以放喺 `story165CanPlay`——晨鏈續鏈嗰陣 modal 技術上仲開緊，擺嗰度會誤擋聽朝強制播，實駕 case C 捉到）。**殘留第三條路**：`#home-back-map` → `leaveHomeFromNotebook("map")`（行程頁「返回地圖」掣，free day mode="map" 嗰陣純粹返地圖，唔經晨鏈）仍然係 bypass——(c) 拍板嗰陣 §8.7 只列明兩條路，呢條唔喺範圍內，**留返統籌決定**掛唔掛（掛法同 book70 一樣：kick 檢查之後、地圖顯示嗰陣試播；"start-today"／"continue" mode 唔可以掛）。

**已決定（唔使問）：**
1. **推辭路徑播咩版**——決定：電視直播版（gallery 旁聽弧重用，只換 pan 字幕）。否決：(a) 原樣 gallery（字幕話「坐喺觀禮席」，fiction 錯——推辭咗嘅人唔喺現場）；(b) 報紙＋場面（報紙已經有，場面就係典禮本身，唔使另開一套）；(c) 全新「屋企睇電視」舞台（新機制，違反「改動盡量細」；字幕已承載 fiction）。
2. **強制播時機**——決定：`goToMapForBrowse` 尾段（kick 之後、地圖顯示之前）。否決：(a) 朝早結算後即時中斷（會撞請柬／報紙／試鏡 modal）；(b) 入地點嗰陣（要食額度，同 §5 衝突）；(c) kick 之前（會搶拍攝日，見 §2）。
3. **進度頁掣處置**——決定：拎走。否決：(a) 留做重播（重播機制唔存在——StoryPlay 拒播已完成節點，留掣只會係死掣；而且 B1 要求掣唔可以「有時有、有時冇」）；(b) 永遠出掣（同「首播不再經掣觸發」矛盾，掣會變成第二個觸發點）。
4. **強制播用唔用 `opts.force`**——決定：唔用，普通 `StoryPlay.start(id)`。`force` 會繞過 homeEditable／結局鎖／eval 檢查，係為 debug 而設；強制播嘅「強制」係指「玩家唔可以選擇唔播」，唔係指「繞過閘」。
5. **chip 標題改唔改**——決定：唔改（見 §3）。進度頁文案承載新規則就夠。
6. **典禮「跳過 ⏩」掣留唔留**——決定：留。用戶拍板係「一定要播出嚟」，唔係「唔畀跳過」；場面內快進同「唔播」係兩回事，拎走跳過掣會令玩家覺得俾 game 挾持。
8. **home-story-hint 郁唔郁**——決定：唔郁（死碼，v71 起停用；實時提示係地圖提示行，唔使改）。初稿改過，實駕核實係死碼後已還原。

## §9 設計分叉 (c) 實作（用戶 2026-11-13 11:11 拍板：兩條返回路徑都掛）

### 9.1 `closeSheet` 調查結論（先調查，唔准跳過——全部 grep＋讀 code＋實駕核實）

- **`closeSheet()` 本體絕對唔可以掛。**全檔 ~30 個 call sites，分類如下（行號係 (c) 前）：
  - 真正「返回地圖」用戶動作：**只有一處**——`#loc-close` 撳掣直綁 `document.getElementById("loc-close").onclick=closeSheet;`（L58760）。
  - 內部關面板（掛本體會誤播）：`modal()` L39237–38——**每次開 modal 都會先 call `closeSheet()`**；`openLoc` L53675（強制日路徑＋開 sheet 前清理）；`enterHome` L37274、`goJournalFromMenu` L37620、`endBrowseDayGoHome` L37590（入屋／過日流程）；`k105` L36845（過日 `advanceDay()` 之前）；enc79 巧遇 overlay L52545；地點播劇情掣 L53940（本身就係播劇情）；訓練 L55858／休息 L56154／傾談 L57088／試鏡 L57545（之後 `tickDay()`＋出 modal）；禮品店 L57604／送禮 L57641（關 sheet 即開 modal）；教學 L58251／L58357；`startNewFresh` L58513；`toast(opts.closeSheet)` L33647；menu 開合 L58765。
  - `book70ExitHome` L43823 嗰個係佢自己函數入面嘅內部呼叫（hook 目標本身，唔係問題）；`goToMapForBrowse` L37719 嗰個喺已有掛點之後。
- **疊 stage 風險係真，而且係結構性嘅**：StoryPlay `render()`（L27975 起）經 `modal(inner, modalBtns, ...)` 行——故事 stage 同普通 modal **共用同一個 `#mask`／`#modal-inner`**（`#mask > #modal > #modal-inner`）。`StoryPlay.start` 本身**無 modal-open guard、無重入 guard**（只驗 homeEditable／結局鎖／stub／done／offer／eval）；重入保護只靠 `story165CanPlay` 嘅 `isStoryPlayActive()`／`_storyPlayLocked`（`render()` 入面 `setStoryPlayLock(true)`，`start()` 同步設定）。所以任何新掛點都必須經 `story165TryForcedPlay()`（唔可以直接 call `StoryPlay.start`），而 `closeSheet()` 本體掛點會喺每個 modal 開之前誤播——`modal()` 會先 `closeSheet()`，故事一開即刻冚咗嗰 modal 嘅內容（`modal()` 寫 `#modal-inner`，`render()` 同樣寫 `#modal-inner`）。
- **設計選擇**：只掛兩個真正「返回地圖」嘅用戶動作，唔掛函數本體：
  1. `book70ExitHome()` 本體（手帳恆常出口，`#home-back-map-tabs` 掣＋`ux68GoLoc`「前往」都經呢度）——`show("v-map"); paintBar(); drawMap();` 之後試播，播到就 return。
  2. `#loc-close` 撳掣包裝——`closeSheet()` 之後試播。`atLoc` 唔郁（`goToMapForBrowse` 掛點嗰陣 `atLoc` 都未清，兩條路一致；播唔到就照原樣留喺地圖，`atLoc` 殘留同現狀一樣）。
- **modal 閘擺位（實駕捉到嘅教訓，見 9.3）**：新 helper `story165ModalOpen()`——`#mask` 有 `on` 但無 `story-play-on` 先算 modal 開緊。**只供兩條新掛點用，唔可以放喺 `story165CanPlay`**（共用 choke point 嗰個諗法係錯嘅——見 9.3）。

### 9.2 實作（相對 HEAD `bfd8f5d`，index.html 淨 ＋31 行，3 hunks）

1. `story165ModalOpen()`（`story165CanPlay` 之後，＋15 行）：modal-open 偵測 helper（見 9.1）。
2. `book70ExitHome()`（＋7 行）：返地圖之後先問 `story165ModalOpen()`，無 modal 先 `story165TryForcedPlay()`，播到 return；try/catch 跌返地圖（`catch(_s165b){}`）。結局閘（`ending78Gate`）留返喺函數頭，唔經呢度繞過。
3. `#loc-close`（−1＋10 行）：舊直綁 `onclick=closeSheet` 改做包裝——`closeSheet()` → 問 `story165ModalOpen()` → `story165TryForcedPlay()`，try/catch（`catch(_s165c){}`）。
- 唔變：進度頁「播呢幕」掣繼續拎走；推辭播電視直播版典禮唔變；12 星巧遇／WF4／支線等可選內容唔郁；`story165CanPlay` 守門（homeEditable／結局鎖／劇情進行中）唔變；`leaveHomeFromNotebook` 唔郁（見 9.4）。
- 已知互動（寫低，唔係 bug）：`ux68GoLoc`（手帳「前往」）call `book70ExitHome` 之後 60ms 就 `openLoc(locId)`——如果嗰刻有待播主線，故事會先播，`openLoc` 嗰陣 `isStoryPlayActive()` 會拒（toast「劇情進行中」），玩家播完故事要再撳一次「前往」。故事優先係拍板原意，導航只係順延，接受。
- `test_travel114_static.py` resync：`qa165/resync_travel114_165c.py`（difflib 對 HEAD `bfd8f5d`）——只得 3 個 (c) hunks，其餘純漂移；COUNT 13／FREE 27 不變，`openLoc(` 44 不變，DEF 53668→53690、WRAPPER 44150→44172。教訓：resync 腳本假設測試檔入面係 pristine 行號——HEAD 版測試檔入面已經係工作版行號（157 resync 嗰陣映射咗），第一次跑錯將工作版行號當 pristine 行號，19 FAIL；修正：每次跑之前先將測試檔還原返 HEAD 版再跑（見腳本頭註解）。

### 9.3 modal 閘擺錯位 → 實駕捉到 → 修正（重要教訓）

- **初版錯法**：將 modal 閘放喺 `story165CanPlay()`（諗住三條掛點共用一個 choke point）。靜態測試 39/39 全 PASS，drive A／B／E 全 PASS。
- **實駕 case C 捉到**：`c6_forced_next_morning: false`（其餘 23/24 PASS）。根因：晨鏈報紙／試鏡／請柬 modal 係用掣 `on()` → `cont()` → `goToMapForBrowse()` 續鏈，而 modal 掣 `onclick` 係 `on()` 行先、`closeModal()` 行後——`goToMapForBrowse` 掛點行到嗰陣，嗰 modal 喺技術上仲係開緊（`#mask` 仲有 `on`）。`StoryPlay.render()` 經 `modal()` 行，會直接重用同一個 `#mask`，根本唔會冚 modal；擺閘喺 `CanPlay` 會令每次晨鏈續鏈嗰陣都誤判「modal 開緊」，強制播永遠唔會喺聽朝晨鏈行到（C6 順延唔到——唔係順延到下次，係每次續鏈都撞同一閘）。
- **修正**：modal 閘由 `story165CanPlay` 移出，做咗獨立 helper `story165ModalOpen()`，只供兩條新掛點用；`goToMapForBrowse` 掛點唔使閘（鏈尾嗰陣要麼無 modal、要麼就係續鏈緊嘅 modal，`render()` 重用 `#mask` 係正確行為）。
- **修正後重驗**：靜態 39/39、travel114 PASS、drive C 28/28（`c6_forced_next_morning: true`，C6 播完 done）。教訓寫入測試：`test_story165_static.py` §十有「modal 閘唔喺 CanPlay」斷言（連埋原因），防止之後有人「順手」搬返入去。

### 9.4 殘留（等統籌決定，唔喺 (c) 範圍）

- **第三條返地圖路**：`#home-back-map` → `leaveHomeFromNotebook("map")`（行程頁「返回地圖」掣，free day `mode="map"` 嗰陣純粹返地圖，唔經晨鏈）。掛法同 book70 一樣（kick 檢查之後、地圖顯示嗰陣試播），但 "start-today"／"continue" mode 唔可以掛——要分開處理，唔係順手加一行就得。等統籌決定。
- **v149／v168／v170 衝突監察**：v149（頒獎禮 B1–B4）仲未落地，改緊同一典禮區——本票掂嘅係 `presentAwardInvite.skip`＋`awards62CeremonyBeats` gallery pan 字幕，同 v149 hunks 無重疊（§1.6），(c) 完全唔掂典禮區；v168 已落地（main `5e6a6b0`，glamour 卡列隱藏）——推辭路徑播 gallery 典禮，drive C／D 重跑照行（D 10/10、C 28/28）；v170 已開工（用戶 11:23 追加：提名人 Pixellab character＋移上舞台，Phase 1 調查＋樣本先行）——未落地，舞台幾何可能變，佢落地嗰陣典禮區要重驗。
- **drive B 附註**：`map_ready()`（要「過一日／開始今日行程」掣可見）喺 `homeEditable=true` 嗰陣唔適用——地圖底欄嗰陣係 planner CTA；deferral 檢查改用 `on_map_view()`（v-map on＋無非故事 modal）。唔係 (c) bug，係 drive helper 嘅假設問題。

### 9.5 測試＋實駕結果（(c) 後半段）

- **靜態**：`tests/test_story165_static.py` **39/39 ALL PASS**（原 29 項＋(c) 新 10 項：book70 掛點、loc-close 包裝、舊直綁清零、closeSheet 本體唔掛、modal helper 在位、modal 閘唔喺 CanPlay、兩掛點 try/catch、唔經 openLoc／唔用 force、leaveHome 唔喺呢票、book70 結局閘留返）。
- **反證**（對 pristine HEAD `bfd8f5d`，`/tmp/index165_head.html`）：**6 FAIL／33 PASS**，唔 crash——6 項 FAIL 全部係 (c) 新斷言（book70 掛點、loc-close 包裝×2、modal helper、try/catch、book70 modal 閘）；其餘 4 項 (c) 斷言喺 pristine 照 PASS（全部係否定式／缺席斷言：結局閘留返、closeSheet 本體唔掛、唔經 openLoc、leaveHome 唔喺呢票——pristine 根本無掛點，自然成立）。
- **直接受影響測試逐個重跑**：hub77 ALL PASS、travel114 RESULT PASS、progress71 87 PASS、book70 ALL PASS、book141 ALL PASS、lock78 ALL PASS、ux68 ALL PASS；JS 語法兩個 inline script block `node --check` 全部 OK。
- **實駕**（`drive165.py`，live 模式，port 8998，430×932，槽 3；結果 `drive165/drive165.json`＋截圖 `drive165/shots/`，工作目錄留檔，唔入 commit）：**5 case 全部 PASS，0 pageerror**——
  - **A fresh_c1：8/8**。C1 即播，標題 v157 新版「第一日：冇價」（舊「先學做動作戲／先賺」已改，斷言兩邊都收；首句「何生事務所嘅冷氣夠凍…」）；travelUsed 0，播完 C1 done，返地圖。
  - **B progress_3states：18/18**。三態全部無「播呢幕」掣＋「返地圖嗰陣就會播出」＋「場景：星河電視台」；頭兩次返地圖用 homeEditable=true defer（驗新掛點守門），第三次撳 `#home-back-map-tabs` 即刻播 C2「後巷聽古」（v157 新標題，舊「留人脈／趕通告」係進度頁列名，仲喺度），播完 C2 done，返地圖。
  - **C decline：28/28**。推辭→電視直播版典禮（pan「今晚你喺屋企睇電視轉播…」，得主廖炳星《離岸的信》，總長 9484ms≈9.6 秒，無 comfort、無結果卡，flag skipped，declined 報紙 template `award_declined.film`、fameDelta 0、無「阿偉」）；過一日嗰朝 C1 報紙先出，之後晨鏈掛點 C6 即播——v157 C6 新標題「角落嗰張枱」（星河電視台飯堂，舊「飯堂閒角」已改；抉擇「A · 電視線：接固定閒角，日日有工開」），播完 C6 done，返地圖。
  - **D attend：10/10**（對照組）。pan「觀禮席」，結果卡照出，總長 9511ms。
  - **E loc_close（新）：11/11**。入何生事務所（travelUsed 0→1）→ 撳 `#loc-close` → C2「後巷聽古」即播；單一 stage（`#story-play-root` 1 個、sheet 已關、無 `.awd62-stage`、mask story-play-on）；強制播唔食額度（travelUsed 停 1）；播完 C2 done，返地圖。

### 9.6 清理 scratch（落地前做，見 §7；main 入面同類檔案先例）

- `git ls-tree -r fc1a1aa`：main 入面有 **1058** 個同類 tracked scratch（例如 `qa102/debug_fx.py`、`qa102/drive_fx.py`、`qa102/drive_log.txt`）——舊版有將 qa／drive／debug 檔帶入 main 嘅先例。但本票按任務指示做：未引用嘅 scratch 用 `git rm` 由分支拎走，唔帶入 main。
- 查引用：`debug165.py`／`debug165b.py`／`debug165c.py`、`drive165.py`、`qa165/resync_travel114.py`／`resync_travel114_157.py`／`resync_travel114_165c.py`——無任何測試／suite／drive 引用佢哋（grep `tests/`＋`qa131/run_suite.sh`：只有舊版 `qaXXX/resync_travel114.py` 喺 `test_travel114_static.py` 註解入面提及，唔係引用）。`drive165/`、`qa165/probe*.txt`、suite 輸出係 untracked，唔入 merge，唔使理。
- 執行時機：rebase＋最終驗證之後先 `git rm`（rebase 嗰陣仲要 resync 腳本；drive 重跑仲要 `drive165.py`）。詳見 §7。
