# NOTES_V20A198 — v191 設計 review B1＋C1–C3 一次過修復

- 分支：`v20a198`；基底 main `2760680`（v191 NOTES）；工作副本 `~/workspace/linji-work198/`
- 用戶 2026-11-13 21:13 拍板一次過修晒。落地由統籌做（本票只 push 分支去常駐 clone 本地 origin，唔上 GitHub）。
- 改動總覽：`index.html` 60490 → 60483 行（淨 −7）；`git diff` 61 insertions／68 deletions。
  新測試 2 檔；更新舊測試 10 檔（見 §6）；resync 行號釘 73 個錨點＋text125 1 行＋text108 1 行。

---

## §1 B1 根因——強制播第一觸發必定先出霞姐（WF4 boss01）

### 現象（review 報告）
首次入茶餐廳，WF4 `boss01`（`trig:"loc"`、`loc:"cafe_cha"`、`once:true`）必定打尖，
目標主線幕要等下一次觸發（晨鏈）先出；review 員 4 次 sheet-close 0 次即出主線幕。

### 根因（實測證實，唔係估）
1. **v153 A1 守衛係地點範圍，強制播唔係。**`wf4TryLocEvent` 入口調 `enc79StoryPendingAt(locId)`，
   只會喺主線節點 pending **喺入緊嗰個地點**嗰陣先壓住 WF4 地點事件
   （經 `S.mapTips[locId]` kind story，或 open 節點嘅 `storyNodeLocId(n) === locId`）。
   強制播候選係跨地點嘅：C6F → `film_lion`、C6 → 電視台飯堂、C18 → `agency_ho`。
   入 `cafe_cha`（C1 觸發地點，兩邊 drive 都用佢觸發強制播）永遠唔會觸發呢個守衛。
2. **pristine WF4 狀態下，day 98 首次入茶餐廳 boss01 係確定性觸發。**
   節點內計數＋實駕確認（probe2 R1＋R2，2/2）：
   seeded roll `wf4loc:98:cafe_cha:1` ＝ 0.1535 ＜ `pLoc` 0.20 通過；
   當時 pool（tier 0／1990 春／boss 未見）＝ {cha03, cha04, boss01, st10}，
   pick `wf4pick:loc:cafe_cha:98:0` ＝ 0.6895 → pool index 2 → `boss01`
   （`wf4_ev_boss01`，index.html 約 L40389，`once:true`，`setFlag:"boss_met"`）。
   真入場後 `S.wf4` ＝ `lastDay: 98, seen: {wf4_ev_boss01: 1, __n: 1}, flags: {boss_met: true},
   evDay: {wf4_ev_boss01: 98}, locDay: 98, locTries: 1`；modal 文本係 boss01（「老闆娘叫霞姐…」）。
   播種嗰陣 `S.wf4` 完全 pristine（`lastDay: -99, seen: {}, pending: null, locDay: -99, locTries: 0`）。
3. **點解 qa191 第一擊即出目標幕：係 drive artifact，唔係遊戲。**
   `drive191.py` 嘅 `open_loc_sheet` 喺撳地圖掣之前，無條件先 `js_click_text("返回地圖")`。
   唯一可見嘅匹配係 `#loc-sheet` 入面嘅 `#loc-close`（`sheetOn === false` 但 `offsetParent !== null`，
   閂咗嘅 sheet 個掣仲係 JS-clickable）。撳佢會行 `loc-close` onclick（`closeSheet()` ＋
   `story165TryForcedPlay()`），所以強制播喺入茶餐廳之前已經播緊；`S.wf4` 完全冇郁
   （probe P1／P2 `locTries` 0）。真玩家撳唔到嗰粒掣。review 員嘅路徑（地圖掣直接入）先係真玩家路徑。
4. **review 員第二次經晨鏈先出，解釋到：** 佢哋嘅 drive 留低咗 WF4 結果 modal 未閂，
   sheet-close 嗰陣強制播俾 `story165ModalOpen()` 擋住；晨鏈（`goToMapForBrowse`）先播到 C6F。
   另註：boss01 消耗咗之後（`once:true`），一次普通 sheet-close 都會 work
   （冇嘢再打尖；同日 `lastDay === day` 守衛亦擋住第二次 WF4 地點事件）。
5. **晨鏈次序刻意唔郁：** `goToMapForBrowse` 先行 `wf4PresentPending()` 後行 `story165TryForcedPlay()`，
   但嗰個只關 *pending day 事件*；boss01 係 `trig:"loc"`，永遠唔會係 pending，同 B1 無關。記為刻意非改動。
6. 附註：`story165CanPlay`／`enc79StoryPendingAt`／`todayIsForcedDay`／`wf4TryLocEvent`
   全部 IIFE-scoped，頁面 context `typeof` 係 `"undefined"`，唔係 window global。
   `wf4DailyTick` 只喺 `advanceDay()`（真過日）入面行；播種直接寫 `S.dayIndex`，中間唔行 daily tick。

### 修法（B1）
`wf4TryLocEvent` 入面，v153 A1 守衛之後、`locTries` 計數之前，加：
有強制播 pending（`story165CanPlay()` 非 null）嗰陣 return false——**defer，唔消耗額度**。
- 唔掂 boss01 定義（`once:true`、pool、機率、`WF4_CFG` 全部唔郁）；`wf4Fire`／`wf4PickEvent` 唔郁。
- 效果：強制播嗰次入場，WF4 完全唔擲（`locTries` 唔加，roll／pick 唔變）；強制播播完之後，
  **下一次入茶餐廳 boss01 照出**——同一日，因為 defer 嗰次冇計數，roll／pick 同 pristine 一樣
  （0.1535／0.6895 → boss01）。實駕證實（§9）。

### boss01 之後去向（實駕證實）
播完目標主線幕 → 再入茶餐廳 → boss01 modal 即出（「老闆娘叫霞姐…」），
`S.wf4.seen.wf4_ev_boss01 = 1`、`flags.boss_met = true`、`locTries = 1`。
即係話：boss01 冇消失、冇改期，只係由「強制播之前」搬去「強制播之後嘅下一次入場」。
玩家一日內仍然撞到霞姐（同一日，defer 唔計數）。

---

## §2 C1——死 code：拎走（唔係接返玩家面）

**揀咗：刪除 `storyMapHintHtml()`＋`refreshMapHintStory()`＋`window.refreshMapHintStory` export
＋`scheduleStoryMapRedraw` 入面 2 個呼叫點。**原址留低 v198 註解交代。

**點解唔係接返玩家面：**
- 接返即係喺地圖加返一張劇情卡，等於推翻 v135 已拍板嘅移除（「進度提示進度頁已有」）。
- `storyMapHintHtml()` 零呼叫者（v135 之後淨低嘅只係佢自己＋refresh 入口）；
  佢嘅內容（「下一幕」句式）已經有玩家面載體——進度頁逐行前置句＋`storyMainProgressLine()` 規格。
- `storyMainProgressLine()` **保留**：佢係已測試嘅「下一幕」句式規格（logic 測試＋頁內
  `runSoftP0Checks` 覆蓋，window 有 dev 自檢入口），唔係死 code；`storyActLabel` 註解由
  「三處共用」更正為兩處玩家面見到嘅地方。
- `.map-hint-story` CSS 規則**刻意留返**（inert，冇元素再用呢個 class）：成段刪 CSS 會令
  幾千行釘死行號嘅測試漂移，零玩家收益；留畀 stylesheet 清理票。
- 跟進：`progShort105`（副行截第一句）只係已刪 `storyMapHintHtml` 入面嘅局部變量，一併消失；
  `tests/test_text108_static.py` S-10 斷言跟住改為 v198 語義（見 §6）。

驗證：`storyMapHintHtml`／`refreshMapHintStory` 宣告＋export＋呼叫點 grep 零殘留
（新 static 測試用確切語法斷言，因為 v198 註解本身仲有呢啲名）；
實駕 FRESH：地圖卡 `.map-hint-story` 元素 null，合併行（計劃＋出行）仲喺度，頂欄進度 chip 仲喺度。

---

## §3 C2——鎖住插入幕出獨立鎖定行；遠幕合併改為按段計

### 改動（`renderProgressPane71`）
- 鎖住插入行經 detail 分支出獨立行：條件由 `detailSet71[r.id]` 改為
  `detailSet71[r.id] || storyActIsInsert(r.id)`，帶 `prog71-insert` class＋同 detail 行一樣嘅
  gate items（解鎖條件逐項列出）。C6F／C18／C19 鎖住嗰陣全部見到。
- 遠幕合併改為**按段計**：預先計 `segOf198`（段以鎖住插入行分隔）；
  合併行只收同段嘅遠主幹，區間用該段實際首末 `loN–hiN`（`farLbl198`）；
  得返一幕嗰陣印「第 N 幕」，唔印「第 17–17 幕」。插入行截斷遠幕段（`farMerged105 = false`）。
- 例：新遊戲 → 「第 4–6 幕」＋插入行＋「第 7–17 幕」；film 第 15 週（C6F 已開放）→
  插入行之後 「第 8–17 幕」不變；播完 C18 → 「第 9–17 幕」（C7／C8 係 detail，far 由 C9 起）。
- **紅線守住：** 進度頁一路數到 17，全頁無「第 18／19／20 幕」；插入幕標籤跟 v191
  （「第 6 幕・電影線」／「番外・1990 冬」／「番外・1991 春」）；C19 前置句
  「先完成番外・1990 冬〈上岸路〉」玩家面終於驗到。
- **附帶 bug 修咗：** `prog71GateItems` 將所有 `route:` token 寫死做「行電視線」，
  C6F（`route_film`）鎖行會講錯條件。改為跟 token 分（`route_film` →「行電影線」）。
  之前睇唔到，因為 C6F 鎖行係隱形嘅；家下行見到，文字必須啱。
- 註：`detailSet71` 入面「為插入幕計 detail」嘅舊邏輯（v153 血統）留返原位，渲染已經唔再讀佢；
  唔郁佢，避免無謂 churn——下次掂呢段嗰陣可以一併清理。

---

## §4 C3——場景頂路線名只寫一次

- C6／C6F 兩個節點嘅 `setting` 先至有「電視線：」／「電影線：」（index.html L21833／L22554；
  運行時年份 remap 1988→1990）。其他節點冇路線名。
- 新 global helper `storySettingStripRoute198(setting)`（放 `storyActLabel` 隔籬）：
  剝走「電影線：」／「電視線：」，保留冒號後面嘅地點細節。
  StoryPlay head `.sp-setting` 經佢出（`typeof` guard，同現有 `storyActLabel` 呼叫同一寫法）。
- **節點 setting 資料本身唔郁**（原字仲有路線名）；幕號行（`.sp-act191`）唔郁。
- 例：C6F 場景行由「獅子山製片廠 · 1990 年 · 電影線：佈景板後面嗰個位」變
  「獅子山製片廠 · 1990 年 · 佈景板後面嗰個位」；幕號行仲有「第 6 幕・電影線」——全 head 只出現一次。

---

## §5 測試

### 新測試
- `tests/test_story198_logic.js`（47 項）：B1 獨立 harness（StoryOC stub；`wf4TryLocEvent`／
  `wf4PickEvent`／`wf4Fire`＋`story165CanPlay`／`enc79StoryPendingAt` 實抽）——
  defer 唔計數、boss01 之後照出、A1 守衛獨立有效、seeded roll／pick 對照；
  C2＋C3 用 v191 harness（真 StoryOC／BehaviorGate＋fixture＋插入節點）——鎖行／按段合併／
  單一遠幕／主線行晒；C1 字串斷言。**ALL PASS。**
- `tests/test_story198_static.py`（31 項）：B1 守衛位置（CanPlay 喺 locTries／roll 之前）、
  boss01 定義唔郁、晨鏈次序唔郁；C1 缺席斷言（確切語法）＋`storyMainProgressLine` 保留；
  C2（`prog71-insert`／`segOf198`／`farLbl198`／舊 guard 冇晒／路線條件跟 token）；
  C3（head 經 helper、helper 剝兩個路線名、setting 資料唔郁）。**ALL PASS。**

### 更新舊測試（配合新語義）
- `test_progress71_logic.js`：B1 兩條斷言改 v198 語義（遠幕按段合併兩行；鎖住插入行見到；
  C6F 鎖行講「行電影線」）。**ALL PASS。**
- `test_story191_logic.js`：10 條斷言改 v198 語義（鎖行見到＋`prog71-insert`＋按段合併＋路線條件）。**ALL PASS。**
- `test_story191_static.py`：guard 斷言改為 v198 C2（舊 skip guard 拎走＋按段合併）。**ALL PASS。**
- `test_progress71_static.py`：段界改用 `wireHomeStoryHint`（C1 刪除）；「地圖 hint 行可撳」一節改為
  v198 C1 缺席斷言＋進度入口（頂欄 chip＋手帳進度子頁；v128 起地圖浮掣已取消）。**ALL PASS。**
- `test_ui135_mapcard_static.py` §6／§7：改為斷言 `refreshMapHintStory`／`storyMapHintHtml` 已拎走
  ＋`storyMainProgressLine` 保留。**ALL PASS。**
- `test_verify37_static.py:72`：段界改用 `wireHomeStoryHint`。**ALL PASS。**
- `test_story165_static.py`：兩處註解（§7 頭＋§7 段）更新，反映 storyMapHintHtml 已拎走；無 code 斷言改動。**ALL PASS。**
- `test_verify37_logic.js`：唔郁。**ALL PASS。**

### 行號 resync（`/tmp/resync198.py`，difflib 單次掃描，舊 HEAD → 新工作版）
- 淨漂移 −7 行（60490 → 60483；C1 死 code 刪 −43／B1 守衛 ＋12／C2＋C3 ＋24，逐段唔係均勻）。
- **73 個錨點全部純漂移**（新行內容逐字等於舊行）：kwan151（31020→31019、31028→31027、
  31029→31028、31071→31070；其餘唔郁）、tang152（31509→31508、31653→31652 index）、
  rom176（31583→31582、53416→53409、53784→53777、54923→54916、55017→55010）、
  tang171／173（DEF 54986→54979；總行數 60490→60483）、travel114（COUNT 12／FREE 34／
  DEF 54986→54979／WRAPPER 44434→44427）、gift185（總行數 60490→60483）。
  只改數字釘，ok() 名入面嘅舊標籤（例「A1 L25608」）跟 v182 慣例留返。
- 全套 B 跑完先發現多兩項 FAIL（唔係 12 項穩定 FAIL 入面）：`text125` 係同一類漂移
  （`applyFamilySafeToNode` b.text 分支 33568→33567，`30413` export −1 所致；內容逐字相同）——
  已 resync；`text108` 係 C1 刪除嘅直接後果（`progShort105` 只係已刪 renderer 入面嘅局部變量）——
  S-10 斷言改為 v198 語義。兩檔直接重跑 PASS（見 §7）。

---

## §6 反證（pristine＝HEAD／v191，臨時目錄實體複製，唔用 symlink）

- 新 logic：**18 FAIL／29 PASS，exit 1，唔 crash**——18 項全部係新功能斷言（B1 defer、C1 缺席、
  C2 鎖行／按段合併、C3 剝路線名）；29 項對照／基線 PASS（B1 根因 roll／pick、A1 守衛、
  `storyMainProgressLine` 保留、C3 no-op、無壞幕號）。
  修復：初版 `buildSrc()` 喺 pristine crash（`extractFn('function storySettingStripRoute198')`
  拋錯，未行到 stub guard）——已將條件移入 `buildSrc()` 入面，pristine 乾淨 FAIL，工作版 ALL PASS。
- 新 static：**17 FAIL（全部新斷言），基線 PASS，exit 1，唔 crash。**
- 更新舊測試喺 pristine：progress71_logic 3 FAIL（正正 3 條更新斷言）、story191_logic 10 FAIL
  （正正 10 條）、progress71_static 2 FAIL（C1 缺席）、story191_static 1 FAIL（guard）、
  ui135 3 FAIL（C1 缺席）；verify37_static 1 FAIL 係臨時目錄冇 NOTES 檔造成（同改動無關）；
  story165_static ALL PASS（只改註解）。全部 exit 1，唔 crash。

---

## §7 全套 A/B（`qa131/run_suite.sh`）

- Run A（誤用：冇傳 `<repo-root> <outfile>`，逐檔結果寫失，只剩計數）：263 PASS／14 FAIL。
- Run B（正確參數）：**263 PASS／14 FAIL**——12 項穩定 FAIL 齊晒
  （flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、
  weave43、weave44、weave49、wrap38）＋多出 text108／text125。
  直接覆驗：text125 係行號漂移（§5 resync）、text108 係 C1 刪除後果（§5）——兩者都唔係回歸，
  更新後直接重跑 PASS。
- Run C（text108／text125 更新後）：**265 PASS／12 FAIL**——正正 12 項穩定 FAIL，零回歸。

---

## §8 實駕（`qa198/drive198.py`，本地鏡像＋`python3 -m http.server` port 8988，LIVE 模式）

- 5 cases：FRESH（932）＋A_film（932）＋B_tv（932）＋C_c18（932）＋D_old（700）。
  **71 PASS／0 FAIL、0 pageerror、0 http_fail。**報告 `qa198/drive198_report.json`，截圖 `qa198/shots/`。
- **B1（A_film，實證）：** 播種後 WF4 pristine（`locTries 0`）；首次入茶餐廳嗰刻 modal 唔係霞姐、
  `locTries` 仲係 0；閂 sheet 即出「第 6 幕・電影線：片場跟班」；播完 C6F 再入茶餐廳，
  boss01 即出——modal「老闆娘叫霞姐金龍茶餐廳，下晝三點幾，落場冇乜人嗰下，你會點做？」、
  `locTries 1`、`seen.wf4_ev_boss01 = 1`、`flags.boss_met = true`。
  B_tv／C_c18 同樣首次觸發即出目標幕（C6／C18），入場嗰刻無打尖。
- **C1（FRESH）：** 地圖卡 `.map-hint-story` 元素 null；合併行（計劃＋出行）仲喺度；頂欄進度 chip 仲喺度。
- **C2：** FRESH 進度頁 acts＝`['第 1 幕','第 2 幕','第 3 幕','第 4–6 幕','第 6 幕・電影線',
  '番外・1990 冬','番外・1991 春','第 7–17 幕']`——插入行帶 `prog71-insert`，C6F 講「行電影線」，
  C19 有「先完成番外・1990 冬〈上岸路〉」；A_film 次序 C6＜C6F＜C7；C_c18 播完後
  `['第 1 幕'…'第 6 幕・電視線','第 6 幕・電影線','番外・1990 冬','番外・1991 春','第 7 幕','第 8 幕','第 9–17 幕']`，
  第 7 幕緊貼插入行之後；D_old 700 闊 C6F ✓ 已完成＋C18／C19 鎖行見到；全頁無「第 18／19／20 幕」。
- **C3：** A_film 場景行＝「獅子山製片廠 · 1990 年 · 佈景板後面嗰個位」（「電影線」全 head 一次）；
  B_tv 場景行＝「星河電視台飯堂 · 1990 年 · 角落嗰張枱」（「電視線」全 head 一次）；
  C_c18 場景頂冇「電影線／電視線」。
- 註：第一輪 drive 有 2 FAIL，全部係 drive 斷言寫錯（唔係遊戲）：FRESH 預期「第 5–6 幕」錯，
  實際「第 4–6 幕」啱（C2／C3 係鎖住 detail，far 由 C4 起）；C_c18 預期「第 8–17 幕」錯，
  實際「第 9–17 幕」啱（C7／C8 係 detail，far 由 C9 起）。修正斷言後重跑 ALL PASS。

---

## §9 改動檔案

- `index.html`（唯一遊戲改動）
- 新測試：`tests/test_story198_logic.js`、`tests/test_story198_static.py`
- 更新測試：`tests/test_progress71_logic.js`、`tests/test_progress71_static.js`、
  `tests/test_story191_logic.js`、`tests/test_story191_static.js`、
  `tests/test_ui135_mapcard_static.py`、`tests/test_verify37_static.py`、
  `tests/test_story165_static.py`、`tests/test_text108_static.py`、
  `tests/test_text125_static.py`、`tests/test_kwan151_static.py`、
  `tests/test_tang152_static.py`、`tests/test_rom176_static.py`、
  `tests/test_tang171_static.py`、`tests/test_tang173_static.py`、
  `tests/test_travel114_static.py`、`tests/test_gift185_static.py`
- 實駕：`qa198/drive198.py`、`qa198/drive198_report.json`、`qa198/shots/`（＋probe `qa198/dbg_b1.py`、`qa198/dbg_b1b.py`）
- 本 NOTES：`NOTES_V20A198_B1_C1_C2_C3.md`

## §10 落地狀態

- 工作分支 commits：`a81d96e`（v20a198 本體，33 files）＋`22405ac`（NOTES 補落地紀錄）。
- 已 push 去 origin（常駐 clone 本地路徑）分支 `v20a198`；落地（squash merge 上 main＋部署＋覆檢）由統籌做。

## §11 統籌 rebase 上 main `2374637`（v195 NOTES）＋resync

- main 喺工人開工之後郁咗：v192（`6cfcfbf`，index ＋32 行）＋v195（`4f47077`，index ＋87 行）已落地。
  分支由 `2760680` rebase 上 `2374637`，index.html 60483 → 60602 行（淨 ＋119）。
- rebase 衝突 8 檔，全部係 static test 行號釘（index.html 本身自動合併）。解衝突取 v198 側；
  **教訓**：第一版 regex 解衝突跨咗 travel114 兩個 hunk（syntax error），還原後改用狀態機逐行解先啱——
  regex 唔好用嚟解 git conflict。
- resync（`qa198/resync198_rebase.py` 報告＋`resync198_rebase_apply.py` 寫入，difflib 單次掃描
  v198 tip → 合併後 index）：101 個釘全部純漂移，改咗 78 個數字釘；
  其餘測試檔（story198／progress71／story191／ui135／verify37／story165／text108）用函數體抽取＋內容斷言，
  唔釘行號，唔受漂移影響。
- **resync 捉到嘅陷阱**：合併後測試檔入面嘅釘有兩種來源——main 已經 resync 啱咗嘅（kwan151 C1／E1、
  text125 currentLine／advance），同 v198 側嘅。第一版 apply 腳本當晒全部係 v198 底，
  將 main 啱咗嘅 4 粒（kwan151 27250→27254、27217→27221；text125 27742→27746、27871→27875）改錯咗，
  逐個直接跑嗰陣 text125／kwan151 FAIL 先捉到。修法：`qa198` 內容驗證（斷言搜尋字串喺合併後 index
  搵真行）——COUNT／FREE 全部啱、DEF 55095／WRAPPER 44436 啱、b.text 分支 33574 啱；
  4 粒改返 main 數字後 18 檔全 PASS。verifier 剩低 1 項係誤報（kwan151 L47 係 regex 針，字面搜尋搵唔到，
  實際行 25659 有嗰個 pattern）。
- rebase 後全套：**269 PASS／12 FAIL**——正正 12 項穩定 FAIL，零回歸（267→269 係新加 2 檔 v198 測試）。
- rebase 後分支 commits：`06c942f`（本體）＋`11bffcf`＋`7f29530`；另加本節 commit（resync 腳本＋4 粒修正）。
