# NOTES_V20A202 — 修 v196 設計 review B1＋B2＋C1＋C2

分支 `v20a202`，基底 main `860e790`（v201）。**只做實作＋驗證，唔落地。**
index.html 淨 **+88 行**（60900→60988；95 insertions，7 deletions，12 個 hunk）。
問題來源：`~/workspace/linji-design-review-v196/REVIEW.md`——四項全部係「承諾制之後，
畫面冇講清楚承諾係乜／點樣反悔」，功能本身 live 行得通。**v196 承諾制流程本身一啲都冇郁**
（自動連跑、故事鎖死、晨鏈次序、`dismissFn`／`dismissNb`／confirm dismiss 全部原封不動；
靜態測試有守衛檢查，見 §5）。

## 1. 修法逐項

### B1 — 日結板＋劇情結算唔講下一站去邊
掣前加一行去向（`.dayend-next202`，放 `<h3>` 之後，第一屏見，唔使碌）：
- 排程日：`聽日：街頭表演（自動行程）`（行程名＋「自動行程」）
- 逛逛日：`聽日：到處逛逛（返地圖自由行）`
- 劇情結算（`showResult`）：`關閉之後：繼續跑今日行程「街頭表演」（自動行程）`／
  `關閉之後：返地圖（今日：到處逛逛）`——showResult 嗰陣 dayIndex 已經係入緊嗰日，
  所以用「關閉之後」＋今日 framing，唔係「聽日」。

落點（4 處）：`afterDayModal`（L37104）、`resolvePlannedDay` 兩個 modal 分支（L38340；
兩個分支共用 `btns`）、`presentRestSleepDayEnd` 休息卡（L57764）、`showResult`（L28083）。
去向行字由新 helpers 計出嚟（L38141–38190，`dayEndContinueButtons` 前面）：
`esc202`（頂層冇 `esc`，佢只喺 StoryPlay IIFE 入面）、`nextDayLabel202`、
`dayEndNextLine202(ended)`、`dayEndDismissNote202(ended)`、`storyResultDestLine202()`。

`nextDayLabel202` 跟 `nextDayIsMap()` 同一判定：冇計劃／地圖日／`wrap:`／`audition:` 歷史標記
＝逛逛日。`rest` 特別標「休息」，唔用 PLAN_ITEMS 嘅「休息睡覺」；逛逛日一律硬碼「到處逛逛」，
唔用 `planLabel`（`scout_nt` 等 `planMeta` 得返 raw id）。

### B2 — 日結板 dismiss 零提示、零掣
**揀咗加提示文案，唔加 ✕。** 原因：✕ 本身唔講規則——玩家見到 ✕ 唔知佢係「繼續跑聽日」
定「取消返地圖」，仲要再加文案解釋先講得清；一句文案直接講埋規則，唔使多一個掣。
提示放掣列尾（`.modal-note202`，`role:"note"` 純文字，唔係掣、唔可撳、唔接 `onDismiss`、
唔影響 firstBtn focus；落喺 sticky `#modal-btns` 入面，長期可見）：
- 排程日：`撳出面＝繼續跑聽日行程`
- 逛逛日：`撳出面＝返地圖`
- 週結：`撳出面＝回家結算`

落點：`afterDayModal`、`resolvePlannedDay`（兩分支共用 `btns`，加一次）、
`presentRestSleepDayEnd`。`modal()`（L39609）加 `role:"note"` 分支（L39633–39642）。
**dismiss 行為一啲都冇變**——排程日 dismiss 照跑聽日，逛逛日照返地圖（實駕實撳驗證，見 §6）。

### C1 — 休息卡確認 modal 得一粒掣、無取消
**揀咗加「取消（返去休息卡）」掣，唔係改直述句。** 原因：標題問句「開始今日行程？」
本身冇錯，錯在得一個答案；家下有真選擇，問句合理。改直述句（例如「開始今日行程」）
只係換個寫法，依然冇得返轉頭。
- `presentStartScheduleConfirm45`（L57728）簽名變三參 `(onStart, onMap, onCancel)`；
  有 `onCancel` 先出取消掣（role g，defensive）。
- 確認 modal 另加 dismiss note：逛逛日 `撳出面＝返地圖`／排程日 `撳出面＝開始今日行程`。
  dismiss 照跟 D1 繼續，同取消唔衝突。
- 接線：`presentRestSleepDayEnd` 內 `goScheduleAsk` 傳 `onCancel`，用同一份 `opts`
  重開 `presentRestSleepDayEnd(opts)`——返去休息卡本身（唔係返地圖）；
  `finish()` 已清 day-res／停 FX，重開嗰陣重新加上；dayIndex／存檔唔郁。

### C2 — 故事鎖死零提示，似死機
StoryPlay `render()`（L28210）喺 beats／choices if-else 之後、D4 註解之前 push
`{ label:"劇情進行中，播完先可以離開", role:"note" }`——對白步＋抉擇步都有。
**enc79 巧遇 overlay 唔加**（L53710）：佢本身有「點頭離開」出口（重遇）／
播完收尾掣（初遇），唔係鎖死，寫呢句會係錯話。靜態測試有守衛檢查 enc79 唔加提示。

## 2. 邊界情況（寫入 helper 註解）

- `ended`（週結）：唔出聽日行（週結之後係回家結算，唔係聽日行程）。
- `rest`／`home_chore`／訓練／`shoot:`／`job:`：用 `planLabel` 實名＋「（自動行程）」。
- `sick61`→「病假」：朝早行 conseq61 病假結算，一樣自動。
- 週末：週六板讀週日計劃、週日板係 ended，已覆蓋。
- 週加速摘要板（`flushWeekAccelSummary`）唔係日結板，唔加（範圍外）。
- `storyResultDestLine202()`：slot **只 peek 唔消費**（讀 `FREEPLAY_FW._story165AfterCont`，
  消費留返「關閉」／dismiss 本身）；冇 slot→「關閉：返地圖」。
- 唔掂 v197 B3 嗰條線（跳過掣／典禮 frame）。

## 3. CSS

L1863–1865：`.dayend-next202`（.85rem 粗體啡字）、`.modal-note202`
（flex 1 1 100%、置中、.78rem 啡字）、`#mask.story-play-on .modal-note202`
（淺金字，故事深色掣欄用）。

## 4. 新測試（`tests/`）

- `tests/test_dayend202_logic.js`：**47/47 PASS**（node eval 真函數；stub modal capture）。
  覆蓋：`nextDayLabel202` 10 種（street／scout_all／scout_nt／rest／sick61／train／shoot／
  wrap:／audition:／null）、B1/B2 文案＋ended 邊界、結算 dest line＋peek 不消費 slot、
  afterDayModal（去向行喺 `<h3>` 之後、note 喺掣列尾、note 冇 on、dismiss 照跑行程／返地圖）、
  休息卡＋確認 modal（取消重開休息卡、取消後再入確認 dismiss 照跟 D1）、
  直接呼叫 confirm45（冇 onCancel 就唔出取消掣）。
  註：逛逛日休息卡根本冇「開始今日行程」掣（v196 行為），去唔到確認 modal——
  逛逛日確認 modal 改用直接呼叫覆蓋（測試本身嘅錯誤假設已修正）。
- `tests/test_dayend202_static.py`：**30/30 PASS**。覆蓋落點逐字核對＋enc79 唔加提示＋
  流程唔郁守衛（初版有 1 項檢查寫錯方向——C2 push 喺 if/else 之後、D4 註解之前，已修正檢查本身）。
- **反證**（對 pristine main `860e790`）：靜態 25 項新檢查全 FAIL（5 項「流程唔郁」守衛
  喺 pristine 本來就啱，預期之內）；logic 直接 throw `fn not found: esc202`。乾淨 FAIL，唔 crash。

## 5. 舊測試 harness 耦合（修 harness，唔係產品加 defensive guard）

多個舊 logic test 用 eval 抽真函數（`afterDayModal`／`resolvePlannedDay`／`showResult`／
`presentRestSleepDayEnd`／`presentStartScheduleConfirm45`），而家呢啲函數靠 v202 helpers，
harness 冇抽就會 `ReferenceError: dayEndNextLine202 is not defined`。修法係 harness 補抽 helpers：
- `test_dayflow196_logic.js`、`test_flow45_logic.js`：eval 加入 5 個 helper 名。
- `test_aud91_logic.js`、`test_levels75_logic.js`、`test_rest58_logic.js`、
  `test_stamina58_logic.js`、`test_verify37_logic.js`：FNS list／模組層一次過 eval 5 個 helpers。
覆驗（逐個直接跑，全部 PASS）：`test_dayflow196_logic.js`、`test_flow45_logic.js`、
`test_dayend189_logic.js`、`test_dayend202_logic.js`、`test_dayflow196_static.py`、
`test_flow45_static.py`、`test_dayend189_static.py`、`test_dayend202_static.py`。

### 8 個.py 靜態測試 resync（淨 +88 行漂移，唔係行為回歸）

`qa202/resync202.py`（跟 `qa196/resync_travel114_196.py` 模式）：由 `git diff -U0` hunk
計映射，**每粒釘先核實 pristine 行內容 == 工作版行內容（逐字相同，純漂移）先改**，
內容唔啱就停手。75 粒釘全部核實，零 BAD。
- `test_gift185_static.py`：總行數 60900→60988。
- `test_kwan151_static.py`：13 個 `line()` 參數（＋7／＋12；名入面嘅舊 L 號係歷史標籤，留返）。
- `test_tang152_static.py`：3 個 0-based index（25873→25880、31609→31621、31753→31765）。
- `test_rom176_static.py`：6 個 `line()` 參數＋名一併改（呢檔名同參數一向同步）。
- `test_tang171_static.py`：總行數＋openLoc DEF 55384→55460。
- `test_tang173_static.py`：總行數＋DEF 55384→55460＋L4862 錨點 4935→**4942**（＋7，
  唔係 ＋12——初版手寫錯數，verify 用 mapping() 計啱咗，write 嗰段寫死錯數，已修正）。
- `test_text125_static.py`：3 個 `ls[]` index＋訊息行號（27840→27847、27969→27976、33671→33683）。
- `test_travel114_static.py`：COUNT 12 個＋FREE 33 個＋DEF 55384→55460＋WRAPPER 44647→44723。
  教訓：逐個順序替換會撞號（30952→30964 之後再搵 30964 搵到兩行）——改用單次 regex
  掃描一併替換；中途死過一次，`git checkout` 還原再跑先過。

## 6. 全套 A/B（`qa131/run_suite.sh`）

- 基線（pristine `860e790`，`qa202/suite_pristine.txt`）：**280 PASS／12 FAIL**。
  12 項全部係舊靜態.py：`test_flash51_static`、`test_giglib36_static`、`test_pacing35_static`、
  `test_poster59_static`、`test_rumor49_static`、`test_slot50_static`、`test_soft_tip_111_restore`、
  `test_start53_static`、`test_weave43_static`、`test_weave44_static`、`test_weave49_static`、
  `test_wrap38_static`。
- 工作版（`qa202/suite_work.txt`）：**282 PASS／12 FAIL，FAIL 清單同基線完全相同**
  （多 2 分係兩個新測試 PASS）。零回歸。

## 7. 實駕（`qa202/drive202.py`，本地鏡像 port 8977，LIVE 裸 URL，932／700）

**15/15 PASS**（`qa202/report202.json`），截圖 17 張喺 `qa202/shots/`。
JS pageerror **0**；console error 324 個，**全部係已知 pre-existing `bg_loc_home_airport` 404**
（jpg/png/webp 各 90 次＋`?v=20a104` 版各 18 次；b1c/b1d 各 162 次係因為 Fen 送別戲
本身喺機場場景重複載入呢張缺圖）。證實 pre-existing：`git diff 860e790 -- index.html`
零提及 airport（背景 key 係 `bg_loc_`＋locId 動態砌，`assets/` 根本冇呢張圖）；v196 review 殘留，
唔係 v202 引入。

| case | 驗證結果（DOM 量度） |
|---|---|
| b1a-932／700 | 日結板「聽日：街頭表演（自動行程）」；932 top 246／bottom 266，可見窗 216–752；700 top 188／208，可見窗 158–516——第一屏見，scrollTop 0 |
| b1b-932／700 | 日結板「聽日：到處逛逛（返地圖自由行）」；932 top 246／266，窗 216–804；700 top 188／208，窗 158–568 |
| b2a-932／700 | 板底「撳出面＝繼續跑聽日行程」；**實撳 mask** → Tue 街頭表演照跑，Tue 板 day 2（events：reward／paper／dayend:街頭表演（週二）） |
| b2b-932／700 | 板底「撳出面＝返地圖」；**實撳 mask** → 落地圖，day 1 |
| c1a-932 | 休息卡去向行＋note 齊；確認 modal 標題「開始今日行程？」，掣［開始今日行程，取消（返去休息卡）］，note「撳出面＝開始今日行程」；**撳取消真係返去休息卡**（標題「休息（週一）」＋day 1 唔郁）；再入確認撳出面 → Tue 街頭表演照跑，Tue 板 day 2 |
| c1b-700 | 同 c1a 取消路徑（700） |
| c2a-932／700 | C1 播放期間掣列見到「劇情進行中，播完先可以離開」；播完＋settle 正常 |
| c2b-932 | enc79 overlay 全程**冇**鎖死細字；初遇路徑播到尾，收尾掣「（返去睇下呢度有咩做）」關閉 overlay（見下文限制） |
| b1c-932 | Fen 送別結算「關閉之後：繼續跑今日行程「街頭表演」（自動行程）」；關閉後 Tue 街頭表演照跑 |
| b1d-932 | Fen 送別結算「關閉之後：返地圖（今日：到處逛逛）」；關閉後落地圖，day 1 |

### c2b 兩次測試本身嘅錯誤（已修正，唔係產品問題）

1. 初版假設「點頭離開」由第一句就有——錯。源碼 L53732：`(built.first ? "" : skip)`，
   初遇（`enc79BuildScript` 返 `{steps, first:true}`，`forceFirst || !st.met`）根本唔渲染
   點頭離開，要播完先走得；重遇先由第一句就有。
2. 修正版想播種全部星 `met=true` 攞重遇——唔生效。Probe 證實 `S.stars` 係 lazy init，
   settle 嗰陣 `S.stars===undefined`，播種無嘢可設；同一粒星同日有冷卻
   （`ENC79_COOLDOWN`），唔可以即日再撞同一粒星。
   所以 live 驗初遇路徑（播到尾＋收尾掣＋全程無鎖死細字）；重遇路徑（點頭離開）
   以源碼核實（`built.first` 閘＋`enc79BuildScript` first:true/false 分支）。
   另 `saveQ()` 唔係 global（主 script 係 IIFE）——播種嗰陣唔可以直接叫佢。

## 8. 殘留／跟進

- v197 B3（跳過掣／典禮 frame）唔喺呢票，冇掂。
- `bg_loc_home_airport` 404（v196 review 殘留）：b1c/b1d 每次 Fen 送別戲觸發幾十次，
  另開票處理，唔喺呢票。
- c2b 重遇路徑（點頭離開）只以源碼核實，未 live 驗——要 live 驗要隔日再撞同一粒星，
  另開票先做。
- `~/workspace/tmp-pristine202/`（基線用嘅 pristine 樹）用完可刪。

## 9. 落地紀錄（統籌補）

- 遊戲 commit `1a4a249`（squash merge `v20a202`，基底 main `860e790`），2026-11-14 04:53 HKT 推上 GitHub main。統籌親自核實：新測試 logic 47/47＋static 30/30（反證對 pristine 乾淨 FAIL）、相關 7 邏輯＋8 靜態測試逐個重跑 PASS、全套 A/B 基線 280/12 → 工作版 282/12（FAIL 清單完全相同）、實駕報告 15 runs／0 pageerror／324 個 http fail 全部係已知 pre-existing `bg_loc_home_airport` 404。
- Push：全包連續斷 3 次（Broken pipe／remote hung up，pack 約 21MB）後改拆細推——分三程 fast-forward 全部一次成功：`ef3673a`（v201 證據 sup）→ `860e790`（v201 證據 shots，兩粒 v201 證據 commit 至此先上 GitHub）→ `1a4a249`（v202）。教訓：大 pack 斷線唔好死重試，拆做逐粒 commit 推。
- 線上核實：初次 curl 仲係舊版 v201（Pages 部署 lag，約 90 秒後追上），之後線上 5,377,918 bytes sha `04b0f2ed…` 同 repo `HEAD:index.html` 逐字一致。
- 設計 review 已派（見 `~/workspace/linji-design-review-v202/`）。
