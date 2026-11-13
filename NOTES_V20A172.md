# NOTES_V20A172 — v165 review B1＋C1 修復

- 分支 `v20a172`，基底 main `6d08c7c`（v171 已落地，全套基線 230／12）；**工作期間 v170 落地，main 移到 `e8c3a73`（遊戲 `59fdf54`），分支已 rebase 上新 main（見 §7）**；**其後 v149 又落地，main 再移到 `a500536`（遊戲 `461dc87`），分支再 rebase 上新 main（見 §7）**，最終基線維持 231／12。
- 用戶 2026-11-13 12:33 拍板：修晒 v165 review B1＋C1。
- Review 報告：`~/workspace/linji-design-review-v165/REVIEW.md`。
- 工作副本 `~/workspace/linji-work172/`；本票只做分支 commit＋push 分支去常駐 clone，**唔落地**（落地由統籌做）。

## §1 任務範圍

1. **B1**——`?softPreview=1` 之下強制播全滅（`StoryPlay.start('C1')` 返 false；live 唔受影響）。
   (a) 即時寫明驗強制播必須行 live 模式（耐久記錄，見 §2）；
   (b) 評估 `start()` 帶 `ignoreSheetLoc` 係咪可行（見 §3）——改得先改。
2. **C1**——進度頁鎖行殘留舊觸發框架「去星河電視台先播到呢幕」，改做場景資料 framing（見 §4）。

### 唔郁
- 第三條返地圖路 `#home-back-map` → `leaveHomeFromNotebook("map")` 仍然係 bypass（v165 NOTES §9.4，等用戶決定掛唔掛，呢票唔掂；新測試 §六守衛斷言佢冇被掛上）。
- v170／v149 典禮工作、v171 範圍。
- SAVE key（`starVolunteer_map_v19w`）、softRev、產品 `?v=`；唔直改 content pack JSON；index.html 註解唔寫其他測試硬計嘅版本字串。

## §2 B1(a)：驗強制播必須行 live 模式（耐久記錄）

**規則：強制播（story165 機制）嘅 pass/fail 一律以 live 模式（無 `?softPreview=1`、無 `?softBehaviorGate=1`、無 localStorage `starVolunteer_softBehaviorGatePreview=1`）實駕為準。soft 模式只驗文案／靜態，唔可以作強制播 pass/fail 依據。**

原因（v165 review B1 證據）：soft 路徑之下，`StoryPlay.start('C1')` 直接返 false（`BehaviorGate.gatePath()==="soft"`，地圖上 `atLoc=null`，soft `stepLoc` 唔過）；同一流程 live 模式 C1 即播。呢個係驗證環境同出貨行為分叉，唔係玩家面缺陷——但 gate-on 慣例係 `?softPreview=1`，照跟會誤判功能失效。

v172 起 code 上已修（§3：強制播帶 `ignoreSheetLoc`，soft 下都播到），但呢條規則仍然有效，理由：
- 強制播嘅出貨行為係 live 行為；soft 係一個 preview／test gate，佢嘅 loc 條件喺玩家路徑（掣／直接 `start()`）仍然生效，soft 下嘅強制播成功唔等於 live 下成功，反之亦然；
- 之後任何改動 story165／StoryPlay.start／BehaviorGate 嘅票，實駕驗收都要行 live 模式先算數。

呢條規則同時寫喺：
- 本 NOTES §2（呢度）；
- `tests/test_story172_static.py` 檔頭註解＋§三斷言（斷言 NOTES 有呢段記錄）。

## §3 B1(b)：`start()` 帶 `ignoreSheetLoc` 評估——可行，已改

### §3.1 評估結論：改得，改咗

根因（review B1＋v165 NOTES §1.5 探針 P5 早已記錄）：`story165NextOpen()` 選幕嗰陣用 `StoryOC.listOpen({ checkNodePhase:true, player:true, ignoreSheetLoc:true })`（唔驗地點），但 `story165TryForcedPlay()` 交去普通 `StoryPlay.start(next.id)` 嗰陣，`start()` 內部再驗 `StoryOC.evalNode(node, { checkNodePhase:true })`——唔帶 `ignoreSheetLoc`。soft 路徑 `evalNode` 行 `BehaviorGate.evalTrigger_AND_softRumor`，地圖上 `atLoc=null` 俾 `stepLoc` 擋返。選幕話「開」，播出話「唔開」——同一個機制入面自相矛盾。

### §3.2 點解可行：鏈已經全程打通，只差 `start()` 嗰一格

逐格核實（行號係基底 `6d08c7c`）：
1. `stepLoc(trig, ctx, opts)`（L25249）：`if(opts && opts.ignoreSheetLoc) return true;`——早已識呢個 opts。
2. `stepFavor(trig, ctx, opts)`（L25260，OR／AND 人情＋地點）：`locOk = (opts && opts.ignoreSheetLoc) || …`——同樣早已識。
3. `evalTrigger_AND_softRumor(nodeOrId, opts)`（L25347）：`fn(trig, ctx, opts||{})`——opts 原樣傳入每一步。
4. `evalNode(node, opts)` soft 支路（L24328）：`return BehaviorGate.evalTrigger_AND_softRumor(node, opts);`——opts 原樣轉交。
5. 唯一斷口：`StoryPlay.start()`（L27080）寫死 `StoryOC.evalNode(node, { checkNodePhase:true })`，唔傳 opts。
6. C6–C17 唔受影響：`evalGate3Y`（L25399）根本冇地點一步；soft loc 問題只關 C1–C5 事。
7. `coversNode`（L24922）覆蓋 C1–C17（有 stub 先計），C1 在內。

所以唔使改 `start()` 簽名、唔使改 eval 選項結構、唔使掂 BehaviorGate——只係將一個已經存在、已經有人用（`listOpen`）嘅 opt-in 語義，由 `start()` 原樣轉交落去。

### §3.3 改動（兩處，index.html）

1. `StoryPlay.start()`：`StoryOC.evalNode(node, { checkNodePhase:true, ignoreSheetLoc: !!opts.ignoreSheetLoc })`。
   - `!!opts.ignoreSheetLoc`：唔傳嗰陣係 `false`，同以前「冇呢個 key」等價——全部現有 call sites 行為同以前完全一樣。
2. `story165TryForcedPlay()`：`StoryPlay.start(next.id, { ignoreSheetLoc:true })`（取代無 opts 嘅 `StoryPlay.start(next.id)`）。
   - 仍然唔用 `opts.force`／`allowDuringPlanner`——start 自己再驗 eval＋offer＋homeEditable＋結局鎖。

### §3.4 風險評估：soft 語義有冇被靜靜雞改咗？冇

- **只繞地點一步**：其餘 soft 條件（前置完成／隔日／週數／通告數／傳聞／聲望／季節／人情債）全部照驗。強制播唔會令未夠條件嘅幕提早播。
- **只限強制播一路**：全檔只有 `story165TryForcedPlay` 傳 `ignoreSheetLoc` 入 `StoryPlay.start`（新測試 §四斷言 `StoryPlay.start(...ignoreSheetLoc...)` 全檔只得 1 處）。普通玩家路徑——進度頁掣（已拎走）、`autoPushC1IfNeeded` 嘅 `StoryPlay.start("C1")`、console 直接 `start()`——全部唔帶呢個 opt，soft loc 閘對佢哋原封不動。
- **同 v165 設計決定一致**：v165 已拍板「地點係場景資料，唔係觸發條件；live 根本唔跟地點」。live eval 本來就唔驗地點，強制播喺 live 已經係「返地圖就播」；呢改只係令 soft 嘅強制播同 live 嘅強制播行為一致，唔係放寬 soft 閘本身。
- **三條掛點行為統一**：`goToMapForBrowse` 尾段／`book70ExitHome`／`#loc-close` 三條返地圖路都經 `story165TryForcedPlay`，改完三條喺 soft 下都一致（之前 `#loc-close` 嗰陣 `atLoc` 可能仲係某地點，視乎邊幕 loc 啱唔啱，行為飄忽）。
- **唔掂嘅地方**：`enterLoc`／`doTalk` 寫 offer 嗰兩處 `evalNode(node, { checkNodePhase:true })`（L53848／L57168）刻意留返普通 eval——佢哋係「入到某地先寫 offer」嘅 script-lock，本身就係地點閘，唔跟住放寬（新測試 §六斷言佢哋仲係 2 處普通 eval）。

### §3.5 唔改嘅替代方案（考慮過，唔用）

- 只改流程（B1(a) 耐久記錄）而唔改 code：做到「唔誤判」，但留返機制內自相矛盾（選幕話開、播出話唔開），下次有人喺 soft 下驗強制播依然會撞牆。既然鏈已打通、風險局限喺一條 opt-in 路徑，改埋 code 係啱。
- `story165TryForcedPlay` 改用 `opts.force`：唔用——force 會跳過全部 eval（包括前置／週數／傳聞），放寬過頭，違背 v165「普通 start，等佢自己再驗」嘅設計。

## §4 C1：進度頁鎖行改做場景資料 framing

### §4.1 改動（`prog71StubItems`，C1–C5 鎖行 checklist）

1. 主項（review 證據：C3 鎖行，行號基底不變，仍係 L44028）：
   - 舊：`"到"+names.join("或")+"播"`（`BehaviorGate.progressToward` remain）→ `"去"+lm[1]+"先播到呢幕"`。
   - 新：`"（場景："+lm[1]+"）"`——同已開放行「已經開放——返地圖嗰陣就會播出。（場景：X）」同一寫法。
   - 例：C3 鎖行舊句「去星河電視台先播到呢幕」→ 新句「（場景：星河電視台）」。
2. 掃埋 OR 條件項（同一 checklist，`s.indexOf("或到")>=0` 支路）：
   - 舊：`"以下任一達標："+s`，s 入面留「或到 X」（例：「以下任一達標：人情債 0／2／或到星河電視台」）。
   - 新：`"以下任一達標："+s.replace(/或到([^／]+)/g, "或（場景：$1）")`。
   - 邊幕行 OR：C4（`softLogic==="OR"`，人情債／何生人情／地點三揀一；2026-11-08 用戶 full_literal_including_gates 拍板 C4 用 OR）。

### §4.2 掃埋結果：其餘 remain 項無同類觸發句

逐項核對 `prog71StubItems` 全部 remain 映射：
- 「先完成第 N 幕〈…〉」——前置條件，留。
- 「到第 N 週（而家第 M 週）」——時間條件，留。
- 「接通告 n／m 張」——數量條件，留。
- 「同上一幕隔一日」——時間條件，留。
- 「聽到傳聞：〈…〉（去金龍茶餐廳打聽）」——**刻意保留**：佢講嘅係點滿足「聽到傳聞」呢個條件（去邊度打聽），唔係講去邊度觸發呢幕；v20a34 P0-3 刻意將「打聽傳聞嘅地點」同「播幕地點」分開寫，刪走會令玩家唔知去邊度聽傳聞。傳聞本身係真前置（soft＋live 都驗），唔係場景資料。
- 「要到秋或冬」／「等到啱嘅季節」——時間條件，留。
- 「聲望要多於 15（而家 5）」——數值條件，留。
- `prog71GateItems`（C6–C17）：token 只有 needDone／route／weekMin／fameGt／creditGt／dualGt／tagAny／awardResolved／year／season——**本身無地點項**，唔使改。

### §4.3 唔喺呢票範圍（查過，唔郁）

- `softLockPlayerLine`（L25026）「先到 X，先可以播這幕」：`progressToward` 回傳 `lockLine` 欄位，但全檔無任何 consumer 讀 `lockLine`（只得生產嗰一處）——死輸出，唔上玩家面，唔喺呢票。
- 地圖提示行 `storyMainProgressLine()`「去 X 就會觸發」：唯一玩家面出口 `storyMapHintHtml()` 自 v135 起無 caller（review「已證實唔係問題」第 1 項），死碼，唔郁。
- 舊 picker `sp-row locked`「（開咗之後，去 X 就會觸發）」（L28330）：舊 picker 已無玩家入口（HUB77），唔郁。
- `home-story-hint`「（到現場先可播）」：v20a71 PART3C 起停用嘅死碼（v165 測試 §七已斷言留返原樣），唔郁。

## §5 測試

### §5.1 新測試 `tests/test_story172_static.py`（22 項，ALL PASS）

斷言覆蓋：
- C1：舊觸發句全檔清零；「到 X 播」→「（場景：X）」；已開放行寫法唔變；OR 項「或到 X」→「或（場景：X）」；兩條 checklist 無觸發句殘留；傳聞提示刻意保留；其餘條件句唔變。
- B1(a)：NOTES 有 live 模式驗證要求＋soft 只驗文案／靜態。
- B1(b)：`start()` 轉交 `ignoreSheetLoc`；強制播帶 `{ ignoreSheetLoc:true }`；唔用 force／allowDuringPlanner；全檔只有強制播一路傳呢個 opt 入 `start()`；`autoPushC1IfNeeded` 普通路徑唔帶；eval 鏈前提（stepLoc／stepFavor／evalNode 轉交／listOpen 已用）在位。
- 範圍守衛：`#home-back-map` 仍然 bypass；`closeSheet()` 本體唔掛；普通 eval 只剩 enterLoc／doTalk 兩處；SAVE key／softRev／`?v=` 不變。
- 結果：**22/22 ALL PASS**（工作副本）。

### §5.2 v165 測試更新（`tests/test_story165_static.py`，兩處）

v165 測試 §五＋§十(c) 原本斷言 `StoryPlay.start(next.id, {` 唔出現（即係「普通 start，唔用 opts」）。v172 起強制播帶 `{ ignoreSheetLoc:true }`，兩處斷言更新為：**准許且只准 `{ ignoreSheetLoc:true }`，仍然禁止 `force:true`／`allowDuringPlanner`**。意圖不變（普通 start，等 start 自己再驗），只係將新 opt 白名單化。更新後 **ALL PASS**。

### §5.3 反證

- 新測試喺 pristine `6d08c7c` index.html 上行：**8 FAIL／14 PASS，exit 1，唔 crash**。8 項 FAIL 正正係 v172 改動斷言（C1 4 項＋B1(b) 3 項＋範圍守衛 1 項「普通 eval 只剩兩處」——pristine 嗰陣 `start()` 仲係第三處普通 eval）；其餘 14 項（前提／守衛／SAVE key 等）喺 pristine 都 PASS，符合預期。
- 更新後嘅 v165 測試喺 pristine 上行：**恰好 1 FAIL**——§五嗰句（而家釘咗 `{ ignoreSheetLoc:true }`，pristine 未有）；其餘全部 PASS。預期之內：呢句而家釘嘅係 v172 行為。

### §5.4 全套 A/B

- Pristine A（`6d08c7c`，`qa172/suite_pristineA.txt`）：**230／12**——同 task brief 講嘅 v171 基線一致。
- 工作版 A（第一次，`qa172/suite_workA.txt`）：**226／17**——多咗 5 項 FAIL，全部係 index.html 淨 ＋15 行令釘行測試漂移（見 §5.5），唔係回歸。
- 工作版 B（resync 後，`qa172/suite_workB.txt`）：**231／12，FAIL 清單同 pristine A 逐項相同**——零回歸；＋1 正好係新測試 `test_story172_static.py`。
- 相關測試逐個直接覆驗：§5.1／§5.2 七檔（story172／story165／kwan151／tang152／tang171／text125／travel114）全部個別 PASS。

**Rebase 後再驗（新基底 `e8c3a73`，見 §7）**：pristine（`qa172/suite_pristineB_newbase.txt`）**231／12**——同 v170 落地訊息講嘅 231／12 一致；工作版（`qa172/suite_workC_rebased.txt`）**232／12，FAIL 清單同新 pristine 逐項相同**——零回歸；＋1 正好係新測試 `test_story172_static.py`。12 項 FAIL 同舊基底 pristine A 嗰 12 項亦完全相同（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38——全部係穩定 FAIL）。七檔逐個直接跑 rebase 後全部 PASS。

**第二次 rebase 再驗（新基底 `a500536`，v149，見 §7）**：pristine（`qa172/suite_pristineC_v149base.txt`）**231／12**——同 v149 落地訊息講嘅 231／12 一致；工作版（`qa172/suite_workD_v149base.txt`）**232／12，FAIL 清單同新 pristine 逐項相同**——零回歸；＋1 正好係新測試。12 項 FAIL 同 v170 基底嗰 12 項完全相同（同一組穩定 FAIL）。七檔逐個直接跑全部 PASS。附註：中途 runtime restart 打斷咗第一次 A/B（pristine 跑到 216 項停咗，/tmp log 俾 restart 清走咗；工作版未開始），重跑後數字如上。

**第三次 rebase 再驗（新基底 `e2add29`，v174，見 §7）**：pristine（`qa172/suite_pristineD_v174base.txt`）**234／12**——同 v174 落地訊息講嘅 234／12 一致；工作版初跑（`qa172/suite_workE_v174base.txt` 第一版）**234／13**——多出嚟嗰 1 項係 `test_tang173_static.py`（佢都釘總行數＋openLoc DEF，見 §5.5 第六檔），其餘 12 項 FAIL 同新 pristine 逐項相同。補 resync tang173 後工作版重跑（同一 `suite_workE_v174base.txt`）**235／12，FAIL 清單同新 pristine 逐項相同**——零回歸；＋1 正好係新測試 `test_story172_static.py`。12 項 FAIL 同之前基底嗰 12 項完全相同（同一組穩定 FAIL）。八檔逐個直接跑全部 PASS（story172 22／22、story165、kwan151、tang152、tang171 22／22、tang173 21／21、text125、travel114）。

### §5.5 釘行 resync（五檔）

index.html 淨 ＋15 行（§3.3 兩處 B1＋§4.1 兩處 C1，全部係註解＋改行，difflib 核實**只得 4 個 replace hunks，其餘逐行相同**），插入點（pristine 行號）：L27080 後 ＋5、L38390–38391 後 ＋5、L44028 後 ＋3、L44032 後 ＋2。漂移規則：L≤27080 ＋0；27080<L≤38391 ＋5；38391<L≤44028 ＋10；44028<L≤44032 ＋13；L>44032 ＋15。

Resync 腳本 `qa172/resync172.py`：**單次掃描 dict 查表**（唔逐對 re.sub——travel114 FREE 同時有 57687→57702 同 57702→57717，逐對寫會撞值）；歷史註解行號跳過唔改（例：travel114 頭註「DEF 53668→53690」係 v165 (c) 歷史）；每檔加一行 v172 resync 註解。改動：
- `test_tang171_static.py`：總行數 59171→59186、openLoc DEF 53690→53705（5 處）。
- `test_tang152_static.py`：31387→31392、31531→31536（4 處，斷言名 L 號一併更新）。
- `test_text125_static.py`：27639→27644、27752→27757、33445→33450（9 處，含索引／len 判斷／報錯字串）。
- `test_travel114_static.py`：COUNT 13＋FREE 26＋DEF 53690→53705＋WRAPPER 44172→44187（41 處；FREE 24612 喺插入點之前唔郁）。
- `test_kwan151_static.py`：B／C／E 錨點全部 ＋5（12 處；A 系列喺插入點之前唔郁）。
- Resync 後五檔逐個直接跑全部 PASS；全套 B 231／12（見 §5.4）。

**Rebase resync（v170 嗰 +2 疊加）**：v170 index.html 淨 ＋2 行（FallbackStage 註解 2 行，插入點 6d08c7c L46098；FLOOR 原地改，淨 0）。rebase 嗰陣 `test_tang171_static.py` 同 `test_travel114_static.py` 有內容衝突（v170 自己都 resync 過呢兩檔），`index.html` 同其餘三檔自動合併。解法：合併後 index.html 實量——總行數 **59188**、openLoc DEF **53707**（`grep` 核實）；v170 插入點之後嘅釘行再 ＋2（即我嘅 ＋15 之上再 ＋2，合計 ＋17）：tang171 總行數 59173→59188、DEF 53692→53707；travel114 COUNT ≥46098 者 57753→57755、57920→57922、58063→58065、58084→58086、58534→58536，FREE ≥46098 者 52580→52582、52699→52701、53592→53594、53974→53976、53996→53998、54147→54149、55784→55786、57195→57197、57528→57530、57646→57648、57647→57649、57682→57684、57683→57685、57702→57704、57717→57719，DEF 53692→53707、WRAPPER 44187 唔郁（<46098）。kwan151／tang152／text125 錨點全部 <46098，v170 唔影響，唔使再郁。教訓：第一次 rebase 試行用咗 `| tail -15` pipe，訊息含混（報「local changes」而唔係衝突）；重試改用 output 寫檔先見到真衝突——**rebase 唔好 pipe**。另：解衝突嗰陣 regex `<<< HEAD` 誤食 `<<<<<<<` 頭 4 個 `<`，留低 `<<<<` 殘件（tang171／travel114 各一處），之後逐行清走並以測試 PASS 作實。rebase 後七檔逐個 PASS＋全套 232／12（見 §5.4）。

**第二次 rebase resync（v149 嗰 +97 疊加，`qa172/resync172b.py`）**：v149 index.html 淨 ＋97 行（CSS L778／L794 ＋8、L4457 ＋5、典禮區 45594–47476 淨 ＋84）。`git rebase` 兩次都報假「local changes would be overwritten by merge」（樹係乾淨嘅）兼停喺半完成狀態——改行手動 cherry-pick（`git checkout -b v172r2 origin/main`＋`git cherry-pick a360b47`）先見到真衝突：五檔全部內容衝突，index.html 自動合併。解法：difflib 直接對舊 index（e8c3a73＋v172 hunks，59188 行，`/tmp/index_pre_rebase149.html`）同合併後 index（59285 行）逐行對位，舊行→新行 dict 查表，單掃描改檔；每粒釘行內容逐字核實（舊行內容＝新行內容）。結果：＜45594 者 ＋13、典禮區後者 ＋97——總行數 59188→59285、openLoc DEF 53707→53804（`grep` 核實）；tang152 三錨點 ＋13（25738／31405／31549）；text125 三錨點 ＋13（27657／27770／33463）；travel114 COUNT／FREE 按段 ＋13／＋97（DEF 53804、WRAPPER 44200）；kwan151 13 個錨點一律 ＋13（A 系列之前唔郁，今次都要郁——v149 插入點喺佢哋之前）。v149 對五檔嘅改動本身純係 resync（釘行數字＋頭註一行），無新斷言——所以直接用 my-side 內容＋新釘行覆蓋，唔會丟嘢；v149 頭註行用一行新註補返歷史鏈。教訓：**`git rebase` 喺呢個環境有假報「local changes」嘅前科，rebase 失敗先試 cherry-pick，唔好死磕**；output 一律寫檔，唔 pipe。

**第三次 rebase resync（v153＋v173＋v174 疊加，`qa172/resync172c.py`）**：main 由 `a500536`（59270 行）到 `e2add29`（59341 行，淨 ＋71：v153 ＋71、v173 ＋1、v174 淨 −1）。`git rebase` 今次直接行到真衝突（無假 local changes）：index.html 自動合併，五檔取 main 版（`--ours`）。difflib 直接對 main index（59341 行）同合併後 index（59356 行）逐行對位——**只得 4 個 replace hunks，全部係 v172**（start ＋5／強制播 ＋5／C1 framing ＋3＋2），其餘逐行相同；舊行→新行 dict 查表，單掃描改檔；每粒釘行內容逐字核實（舊行內容＝新行內容）。結果：總行數 59341→59356、openLoc DEF 53860→53875（`grep` 核實）；tang171 總行數／DEF 一併 ＋15（v173 兩條斷言更新 78%→60%／`.h` `!important` 原封保留）；tang152 HELD 唔郁（＜27080）、normaliser／loader ＋5；text125 三錨點一律 ＋5；travel114 COUNT／FREE 按段 ＋0／＋5／＋10／＋15（DEF 53875、WRAPPER 44235→44250）；kwan151 A 系列唔郁（＜27080）、C1／E1／B／C3／C4／C5 ＋5。story165／story172 無釘行，唔使郁。教訓：resync regex 唔可以用 `\b(\d{5})\b`——`L25758` 入面 L 同數字之間冇 word boundary，會漏咗 ok() 名標籤；改用 `(?<!\d)(\d{5})(?!\d)`。另：第二個 commit `1eeeaef` 本身都郁過五檔（每檔一行 v149 resync 頭註），rebase 嗰陣要逐行補返，唔好淨係取 `--ours` 就算（見 §7）。**第六檔（suite 捉到）**：原先五檔之外，`test_tang173_static.py` 都釘總行數＋openLoc DEF（59341／53860）——全套初跑工作版 234／13，多出嚟嗰 1 項正正係佢（2 項 FAIL：總行數＋DEF），其餘 12 項同 pristine 逐項相同。補 resync（同一 mapping，總行數／DEF 一併 ＋15，L4845 釘行喺插入點之前唔郁），之後 21／21 PASS；`resync172c.py` 已補埋呢檔作紀錄。

## §6 實駕

本地鏡像＋Playwright（venv `/home/hatch/pwenv49/bin/python`，`chrome-headless-shell`）。live 模式為主（§2 規則）；softPreview 按 §3 改動驗新行為。932＋700。證據 `~/workspace/linji-work172/qa172/`（`drive172.py`＋`drive172.json`＋`shots/` 7 張）。

**Rebase 後重跑**：rebase 上 `e8c3a73` 後原樣重跑一次（`qa172/drive172_rebased.log`，舊結果留喺 `drive172_pre_rebase.json`＋`shots_pre_rebase/`）：**同樣 6/6 PASS，0 pageerror**——E 決定性對照（普通 eval 只敗 `locIdAny`、ignore 後 ok、普通 start false、book70 強制播 C2 11 句 done）同 F 700 鎖行（場景 framing）逐項一致。

**第二次 rebase 後又重跑**：rebase 上 `a500536`（v149）後原樣重跑一次（`qa172/drive172_v149base.log`，v170 基底結果留喺 `drive172_v170base.json`＋`shots_v170base/`）：**同樣 6/6 PASS，0 pageerror**。

**第三次 rebase 後又重跑**：rebase 上 `e2add29`（v174）後原樣重跑一次（`qa172/drive172_v174base.log`，v149 基底結果留喺 `drive172_v149base.json`＋`shots_v149base/`）：**同樣 6/6 PASS，0 pageerror**——A live C1 16 句、B C3 鎖行場景 framing、C #loc-close C2 11 句、D soft C1 16 句、E 決定性對照（普通 eval 只敗 `locIdAny`、ignore 後 ok、普通 start false、book70 強制播 C2 11 句 done）、F 700 鎖行逐項一致。

### §6.1 最終結果：6/6 PASS，0 pageerror

| Case | 內容 | 結果 |
|---|---|---|
| A live fresh C1（932） | 新遊戲→C1 即播 | ✅ PASS——16 句（節點數據 8 beats／16 lines）、標題「第一日：冇價」、首句「何生事務所嘅冷氣夠凍，檯面攤開兩份通告。」、travel 0→0、播完 done、返地圖 |
| B 進度頁鎖行 C3（932） | 種 day 21 → 手帳進度頁 | ✅ PASS——C3 鎖行：「○ 先完成第 2 幕〈留人脈／趕通告〉／○ 到第 6 週（而家第 4 週）／○ 聽到傳聞：「高仔片場搶鏡」（去金龍茶餐廳打聽）／○ **（場景：星河電視台）**／○ 聲望要多於 15（而家 5）」；無「先播到呢幕」／「去 X 先播到」／「就會觸發」；C2 已開放行「已經開放——返地圖嗰陣就會播出。（場景：星河電視台）」＋無掣 |
| C #loc-close live C2（932） | 種 day 21 → 事務所 → `#loc-close` | ✅ PASS——C2「後巷聽古」即播，11 句、done；單一 stage（`#story-play-root` 1 個、sheet 已關、無 `.awd62-stage`）、travel 1→1 |
| D soft fresh C1（932，`?softPreview=1`） | 新遊戲→C1 即播（**B1 新行為**） | ✅ PASS——gatePath soft，C1 即播、16 句、done、返地圖（v165 嗰陣呢個 case 係全滅） |
| E soft 普通 start vs 強制播（932） | 種 day 21 → 地圖上直接 `start('C2')` vs 手帳「返回地圖」強制播 | ✅ PASS——見 §6.2 |
| F 700 綜合（430×700） | live fresh C1 即播＋進度頁 C3 鎖行 | ✅ PASS——C1 即播；C3 鎖行同 B 一致（場景 framing、無觸發句） |

### §6.2 Case E：B1 修法嘅決定性對照（同一 session，同一 C2）

- `StoryOC.evalNode(C2, {checkNodePhase:true})` → `ok:false`，reasons **只得 `['locIdAny']`**——普通 eval 喺 soft 下只係俾地點一步擋住。
- `StoryOC.evalNode(C2, {checkNodePhase:true, ignoreSheetLoc:true})` → `ok:true`，reasons `[]`。
- 普通 `StoryPlay.start('C2')` → **`false`**，播完乜都冇發生——soft 閘對玩家路徑原封不動。
- 手帳「返回地圖」（`book70ExitHome`）→ C2「後巷聽古」即播，11 句、done、返地圖。
- 四點一齊成立，先至證明修法只繞地點一步、無放寬 soft 閘。

### §6.3 探針教訓（兩次失敗都係 probe 問題，唔係遊戲問題）

1. **C1 句數 16 vs 18–22**：第一輪 A 數到 18、D 數到 22。根因係 `.sp-line` 逐字打出（打字機效果）——未停定嗰陣 poll 到半句會當多咗一句。探針 `qa172/probe_c1_lines.py` 證實：節點數據 C1 係 8 beats／16 lines；DOM dump 入面同一句會出現「半句→全句」兩個狀態（例：「阿偉，你入行第一單嘢，我幫你睇咗」→「…睇咗兩條路。」）。修法：`play_story` 計句前等 500ms、兩次讀數相同先計——之後 A／D 穩定 16 句。**以後數對白句數一定要等打字機停定。**
2. **種子 field 寫錯（v165 review 嘅種子同病）**：第一輪 E 嘅 `evalNode(ignoreSheetLoc)` 返 `gigCountMin` 失敗，第二輪返 `rumorSoftPriority` 失敗。根因：`liveGigCount()` 讀嘅係 `S.story.gigCount`（＋`S.flags done_*`），唔係 `S.gigCount`；`liveRumors()` 讀嘅係 `S.mockRumors`／`S.notebook.rumors`／`S.story.rumors`／flags，唔係 `S.rumors`。v165 review 嘅種子（`S.gigCount = 3; S.rumors = [...]`）兩個 field 都錯——live 模式下唔覺（live eval 唔用 soft trigger），soft 下先爆出嚟。修法：種子改寫 `S.story.gigCount = 3`＋`S.story.rumors = ['tvb_rules_gossip']`（舊寫法留返無害）。第三輪 E 即 PASS。

### §6.4 探針方法備註

- 截圖前先清 `enc79` overlay（v167 教訓）；「過一日」掣喺 modal 下面都讀到 visible，唔可當作「已返地圖」信號——`play_story` 回地圖判斷加咗 mask 檢查。
- Chromium 全程無死過；寫入正常，無 EPERM；server 無 `ERR_EMPTY_RESPONSE`。

## §7 rebase 紀錄

- 開工嗰陣核實 main HEAD 係 `6d08c7c`（v171），同 task brief 一致；分支 `v20a172` 由 `6d08c7c` 開出。
- **工作期間 main 郁咗兩次**：① v170 落地，main 移到 `e8c3a73`（NOTES commit；遊戲 `59fdf54`「頒獎禮舞台-only 底圖＋提名人物企上舞台」，全套 231／12）。② v149 落地，main 再移到 `a500536`（NOTES commit；遊戲 `461dc87`「剔走典禮舞台觀眾席剪影帶」，全套 231／12）。§7 第一版寫「工作期間 main 無再郁，唔使 rebase」係錯嘅，已更正。
- 第一次 rebase（上 `e8c3a73`）：`git fetch origin` 後 `GIT_EDITOR=true git rebase origin/main`（output 寫檔，唔 pipe——見 §5.5 教訓）。第一次試行 pipe 咗 `| tail -15`，訊息含混兼中途停咗；`git rebase --abort` 後重試，先見到真衝突：`test_tang171_static.py`＋`test_travel114_static.py`（v170 自己都 resync 過呢兩檔）；`index.html` 同其餘測試檔自動合併。衝突解法見 §5.5（實量 59188／53707，≥46098 釘行再 ＋2）。Rebase 後 HEAD：遊戲＋測試 `a360b47`、NOTES `1312e7f`（rebase 前係 `8730f80`／`d131bb4`）。再驗：七檔逐個 PASS、全套 pristine 231／12 vs 工作版 232／12（FAIL 清單逐項相同）、實駕重跑 6/6 PASS 0 pageerror（見 §5.4／§6）。
- 第二次 rebase（上 `a500536`）：`git rebase` 兩次都報假「local changes would be overwritten by merge」（樹係乾淨嘅）兼停喺半完成狀態——改行手動 cherry-pick：`git checkout -b v172r2 origin/main`，`git cherry-pick a360b47`（五檔內容衝突，index.html 自動合併；解法見 §5.5，`qa172/resync172b.py` difflib 對位），再 `git cherry-pick 2b01f94`（NOTES＋qa，乾淨）。之後分支 `v20a172` 指去新 HEAD，`v172r2` 刪除。第二次 rebase 後 HEAD：遊戲＋測試 `d9806c0`、NOTES `67ac88f`（再加頭註＋NOTES 修訂後 amend，見下）。再驗：七檔逐個 PASS、全套 pristine 231／12 vs 工作版 232／12（FAIL 清單逐項相同）、實駕重跑 6/6 PASS 0 pageerror（見 §5.4／§6）。另：中途 runtime restart 打斷咗第一次 A/B（見 §5.4 附註），重跑後數字如上。
- 第三次 rebase（上 `e2add29`，v174）：工作期間 main 再郁三次——v153（C17 路由＋何生企台＋進度頁幕次序，index ＋80／−9）、v173（淡出 stop＋`.h` `!important`，淨 ＋1）、v174（獎盃 chip／舞台放大等，86 行改動）。開工核實 main HEAD 係 `e2add29`，同 task brief 一致。`GIT_EDITOR=true git rebase origin/main`（output 寫檔，唔 pipe）**今次冇假「local changes」**，直接行到真衝突：第一個 commit `d9806c0` 嗰陣 index.html 自動合併，五檔釘行測試內容衝突（v153／v173 都 resync 過呢五檔）。解法：五檔取 main 版（`--ours`——main 對呢五檔嘅改動本身純係 resync，tang171 另有 v173 兩條斷言更新 78%→60%／`.h` `!important`，必須保留），再用 `qa172/resync172c.py` difflib 對位（main index 59341 行 → 合併後 59356 行，只得 4 個 v172 replace hunks，其餘逐行相同；每粒釘行內容逐字核實），單次掃描改檔。resync 期間撞到一個 regex 問題：`\b(\d{5})\b` 唔 match `L25758`（L 同數字之間冇 word boundary），改用 `(?<!\d)(\d{5})(?!\d)` 先掂。解法見 §5.5。第一個 commit 落地 `3704883`。第二個 commit `1eeeaef` 嗰陣五檔又衝突——原因係 `1eeeaef` 本身都郁過呢五檔（只係每檔加咗一行 v149 resync 頭註；kwan151 另有兩行頭註舊行號，main 版已經更新過，唔跟）；解法同樣取 `--ours`，再將 `1eeeaef` 嗰五行頭註逐行補返（插喺 resync172c 註解之前，保歷史鏈）。第二個 commit 落地 `445493b`。第三次 rebase 後 HEAD：遊戲＋測試 `3704883`、NOTES `445493b`（再加 NOTES 修訂後 amend，見下）。再驗：七檔逐個 PASS、全套 pristine 234／12 vs 工作版 235／12（FAIL 清單逐項相同）、實駕重跑 6/6 PASS 0 pageerror（見 §5.4／§6）。
- 分支 `v20a172` 由 `6d08c7c` 開出；工作副本 `~/workspace/linji-work172/`（clone 自常駐 clone，origin 係本地路徑；core.sshCommand＋git identity 已按 AGENTS.md 補返）。
- Commit：遊戲＋測試一個 commit、NOTES＋qa 證據一個 commit；push 分支去常駐 clone（`git push origin v20a172`，rebase 後用 force-with-lease）。**唔落地**——落地由統籌做。

## §8 落地紀錄（統籌填）

- 落地：分支最終 HEAD `ff071cf`（遊戲＋測試 `3704883`，基底 `e2add29`／v174），squash merge → main 遊戲 commit **`9eea029`**，push main 一次成功（`a618a5d..9eea029`），`git fsck` 乾淨。
- 線上核實（統籌親自 curl，兩次）：第一次仲係舊版（v174，5,269,914 bytes sha `3af45a51…`，Pages 部署滯後）；等 90 秒後重 curl，**5,271,408 bytes、sha256 `eb594747bdb7e38e1e6174565600b969ce2bcff17965355e7230803a01bb798c`**，同 repo `HEAD:index.html` 完全一致。
- 落地後全套數字以 rebase 工人重驗為準（見 §5.4／§6）：新測試 22/22，全套 pristine 234／12 vs 工作版 235／12 零回歸，實駕 6/6 PASS 0 pageerror。
