# NOTES_V20A189 — 日結板三粒掣：返回地圖真返地圖／加速降級做細連結／版面唔裁字

- 版本：v20a189（分支 `v20a189`，基底 main `dcf1b72`）
- 用戶拍板：2026-11-13 19:18「照你建議修：返回地圖真係返地圖，加速降級做細連結」
- 範圍：只改 `index.html`＋新測試；唔落地（唔做 squash merge、唔 push main、唔做設計 review）

## 1. 問題（修前已查 code 核實，實駕重現）

日結板（殺青／日結 modal）三粒掣由 `dayEndContinueButtons()`（`index.html`）出：

1. **「返回地圖」同「開始今日行程」係同一粒掣**：soft 分支兩粒都 call 同一個
   `goRunSchedule` → `nextNb` → `runScheduleFromToday()`。註解話明原意係「預設返地圖，
   另可開始今日」，但 code 冇做到。實駕（pristine）：soft 板撳「返回地圖」→
   殺青獎勵 modal → 街頭日結板，dayIndex +1——即係直接開咗今日行程，完全冇落地圖。
2. **「加速本週剩餘」係週級動作**（`confirmWeekAccel`：連續結算本週剩餘日子、跳過地圖
   自由操作），唔應該同兩粒日級掣平排同一行（仲要佔兩行掣欄：3 粒掣排兩行）。
3. **版面溢出**：wrap 板內容 ~768–865px vs `#modal-inner` 可見 383–617px，
   fold 位裁斷內容。700 高實測重現用戶截圖：綠色殺青行（`《陰陽夜更》動作替身完工。
   片酬$ 6,000，聲望+5，人氣+5。`）top 504／bottom 545，fold 喺 541——俾掣欄裁咗一半。
   932 高嗰陣 fold 裁嘅係支票圖（676–918），綠行喺 fold 之下（要捲先見到）。
   `#modal-inner` 本身捲得郁（scrollTop 0→max，尾行全部見得返），問題係首屏 fold 位裁字。

### 修前核實：`runScheduleFromToday()` 喺 soft 日係咪真係直接開行程

係。`runScheduleFromToday()`：`mapish`（無計劃／逛逛／wrap:／audition:）先至
`goToMapForBrowse()`；否則（街頭／訓練／休息／拍攝／試鏡）直接 `resolvePlannedDay(id)`。
`kickScheduleIfNeeded()` 亦只 kick 強制日（shoot:／job:），soft 日返地圖唔會自動開行程。
所以兩粒修好後真係分流：返回地圖 → 地圖自由行（toast 提今日行程，要過日先撳開始今日行程）；
開始今日行程 → 直接結算今日。邏輯測試 (f)(g)(h) 將呢個分流釘死。

## 2. 修法

### (a) 返回地圖真係返地圖（`dayEndContinueButtons` soft 分支）

soft 分支（聽日係街頭／訓練／休息等非強制非地圖日）嘅「返回地圖」改行
`()=>{ try{ goToMapForBrowse(); }catch(_e){} }`，唔再行 `goRunSchedule`。
「開始今日行程」唔郁，繼續行 `goRunSchedule`。

注意：`resolvePlannedDay` 嘅 `L38364` wrapper 會將每粒掣嘅 `on` 包多一層 `afterDayRes`
（殺青獎勵 sheet 先出），所以 handler 本身淨係做返地圖就得，唔好重複包獎勵。
soft 日 `shootFinished` 係 false，`afterDayRes` 直通；殺青日（聽日 soft）撳返地圖，
獎勵 sheet 照樣先出，撳完先落地圖——獎勵流程唔會漏。

唔郁：`nextForced` 分支（淨係「開始今日行程」）、`nextIsMap` 分支（淨係「返回地圖」行
`goRunSchedule`，v20a4 註解話明要經獎勵流程先返地圖）、`ended` 分支（回家結算）、
`confirmWeekAccel` 確認流程。

另外兩個 `dayEndContinueButtons` 呼叫點核查：
- `afterDayModal`：掣直接入 `modal()`，冇 wrapper——返回地圖直行 `goToMapForBrowse`；
  呢條路同佢個 `onDismiss`（一樣係 `goToMapForBrowse`）一致，`closeModal()` 會清
  `day-res`／`day-res-open`，唔會留殘 class。
- `presentRestSleepDayEnd`：掣按 label 重新映射——「返回地圖」→ `goMap`、
  「開始今日行程」→ `goScheduleAsk`（確認閘）、「加速」→ 停 FX＋清 `day-res` 再行原 handler。
  新加速連結 label 照有「加速」二字，`indexOf("加速")>=0` 嗰支仍然命中，唔使改呢度。
  （舊 `test_flow45_logic.js` 覆蓋呢條路，見 §4。）

### (b) 加速降級做細連結

`dayEndContinueButtons` 唔再推 role `"g"` 大掣，改推一粒 role `"link"` 條目
（label「想跳過本週剩餘日子？加速 →」，放掣列最後，等主掣先渲染），`on` 照行現有
`confirmWeekAccel(()=>goRunSchedule())`，確認 modal（列出將跳過日子＋後果）唔郁。
`modal()` 識得 `role==="link"` → class `day-end-accel-link`；CSS（`#modal-btns`
`button.day-end-accel-link`）：`flex: 1 1 100%` 全行一列喺掣列下方、44px 高、
`.85rem`＋底線＋`#6b4e2e`——夠顯眼撳得到，唔係細到撳唔中。
其餘兩處（`afterDayModal`、`presentRestSleepDayEnd`）經同一函數出掣，自動跟埋降級；
三個呼叫點嘅 wrapper／label 映射照舊行（`resolvePlannedDay` 嘅 `afterDayRes` 包裝、
`presentRestSleepDayEnd` 嘅「加速」分支）。

### (c) 版面：唔再裁字

三樣加埋：
1. 加速離開主掣列：3 粒掣兩行（掣欄 ~123–127px）→ 2 粒主掣一行＋連結一行
   （掣欄 ~119–123px，連結行 44px＋gap 8px 抵消咗大半；實測 932 inner 只係
   561→565px，+4px）。所以呢項唔係放寬主力，真正放寬靠第 3 項 92dvh；
   呢項嘅價值係語義降級（週級動作唔再同日級掣平排）同埋主掣列得返一行。
2. 兩處日結板 body 嘅 `.week-accel-hint` 段落拎走（加速需二次確認嗰句）——連結本身＋
   確認 modal 已經講清楚，唔使重複；慳返 ~20px 內容高。CSS rule 留返（死 rule 一行，唔郁）。
3. **根因**：矮屏保底死咗——v19z12 N7 嘅 `@media (max-height: 820px)` 88dvh 本來要畀矮屏
   modal 高啲，免底部 CTA 被裁；但後來居上嗰條 `#mask:not(.tut-on) .modal`
   `max-height: min(78dvh, 720px) !important`（同一 specificity、更後）壓死咗佢。
   實測：700 高嗰陣 computed max-height 係 546px（=78dvh），唔係 616px（=88dvh）。
   修法：`resolvePlannedDay` 非休息分支一律幫 `#mask` 加 `day-res` class
   （休息卡／`afterDayModal` 本來已經有；唔加 `body.day-res-open`，唔改 dim／HUD 樣，
   `closeModal` 本來就會清 mask `day-res`），再加一條只認 `day-res` 嘅矮屏規則：
   `@media (max-height: 820px){ #mask.day-res:not(.tut-on) .modal{ max-height: min(92dvh,92svh,720px) !important; } }`。
   只放寬日結板，其餘 modal 唔郁；932 高唔受影響（media query 唔命中）。
   92dvh 唔係一次過揀啱：初版 88dvh（modal 616px／inner 457px）實駕第三輪，700
   最長內容嗰版綠色結算行 508–548 vs fold 545，仲差 3px 先過到；92dvh（modal 644px／
   inner ~485px）先至清晒。modal 係底錨（top = vh − h − 10），放寬只會向上伸，
   掣列唔會跌出屏（700：modal top 46、掣列底 676，屏底 700）。

   註：內容最豐富嘅殺青板（片＋支票＋海報＋notes）本身 ~760–860px，就算放寬都唔可以
   成版唔捲（932 內高上限 ~617px、700 係 ~485–537px）。驗收準則係：首屏 fold 位唔裁綠色
   notes 行＋全部內容捲得到（scrollTop 到底，尾行齊見）。支票／片等圖喺 fold 位半現
   係正常捲動內容，唔係裁字；要支票成張首屏見晒就要縮圖，嗰個係 v20a101／v20a105
   定咗嘅設計，唔喺呢票郁，留待設計決定。

## 3. 改動清單（`index.html`）

- `dayEndContinueButtons()`：soft「返回地圖」→ `goToMapForBrowse()`；加速改 role `"link"`
  細連結，放主掣之後。
- `modal()`：`role==="link"` → class `day-end-accel-link`。
- CSS：`#modal-btns button.day-end-accel-link`（全行、44px、底線）。
- `afterDayModal`／`resolvePlannedDay` modal body：刪 `.week-accel-hint` 段落。
- `resolvePlannedDay` 非休息分支：`#mask` 加 `day-res` class。
- CSS：矮屏 `@media (max-height: 820px)` 下 `#mask.day-res` modal 放寬到 92dvh
  （初版 88dvh，實駕見最長內容版仲差 3px，見 §4）。
- 唔郁：SAVE key（`starVolunteer_map_v19w`）、softRev（s107）、`?v=`（v20a10）、content pack JSON。

## 4. 驗證

### 新測試（fixed 版全 PASS）

- `tests/test_dayend189_static.py`（23 項）：soft 分流／forced／map／ended 唔郁／加速係 link／
  modal render link／連結 CSS／hint 已刪／day-res＋92dvh／confirm 流程唔郁／紅線。
  連結色 `#6b4e2e` on `#F2EBD8` 對比度實算 6.41:1（WCAG AA 以上）。
- `tests/test_dayend189_logic.js`（17 項）：真 `dayEndContinueButtons` 三種分支＋ended、
  真 `countRemainingAutoDays`（有剩餘先出連結）、真 `runScheduleFromToday` 分流核實。

### 反證（pristine main，`git stash push index.html` 兩輪，乾淨 FAIL 唔 crash）

- static：11 FAIL／12 PASS，exit 1，零 traceback。FAIL 嘅正正係 v189 嗰 11 項
  （soft 地圖掣／加速大掣已清／link／連結 CSS×4／hint 已刪／92dvh 規則）；
  PASS 嘅係「唔郁」守門（forced／map／ended 分支、confirm 流程、紅線、NOTES 存在）。
- logic：5 FAIL／12 PASS，exit 1，零 crash。FAIL 嘅正正係 v189 行為 5 項
  （soft 三粒掣結構／地圖掣唔行程／地圖掣落地圖／加速係 link／加速確認後行程）。
- 期間捉到 static test 本身一個脆弱位：`fn.index('想跳過本週剩餘日子？加速')` 喺
  pristine 會掟 `ValueError` 令成檔 crash（第一輪反證見到）。已硬化
  （`seg()` 搵唔到返 `''`、`idx()` 返 -1、CSS 段 guard），硬化後 fixed 版照樣 23/23，
  第二輪反證乾淨 FAIL。
- 註：static 入面「day-res class ≥3 次」嗰項係守門唔係判別項——pristine 都 PASS，
  因為休息卡路徑本身已經有 day-res；真正判別 92dvh 規則嗰項喺 pristine 係 FAIL。

### 實駕（`qa189/drive189.py`，live 模式，Playwright，port 8975）

pristine 基線（第一輪，完整矩陣兩次）：bug 全部重現——soft 板撳「返回地圖」→
殺青獎勵 modal → 街頭日結板，dayIndex +1（932：day 0→2，即直接開咗今日行程，
完全冇落地圖）；700 高 forced／soft case 綠色殺青行俾掣欄裁一半（`greenCut=1`，
行 top 504–574／bottom 545–614，fold 541–597）；932 高 fold 裁支票圖，綠行喺 fold 之下。

fixed 最終輪（92dvh，第四輪；中間兩輪用嚟修 probe：見下）：12/12 case 全部
`settled=True`、0 pageerror、0 http_fail。`greenCut=0` 全部 case。

| case | 結果 | day | scroll（內容／可見） | greenCut | anyCut |
|---|---|---|---|---|---|
| wrap-soft-返回地圖-932 | map ✓ | 0→1 | 833/565 | 0 | 2（支票圖） |
| wrap-soft-開始今日行程-932 | new-dayend ✓ | 1→3 | 833/565 | 0 | 2（支票圖） |
| wrap-map-返回地圖-932 | map ✓ | 3→4 | 833/617 | 0 | 2（支票圖） |
| wrap-forced-開始今日行程-932 | new-dayend ✓ | 4→6 | 833/565 | 0 | 2（支票圖） |
| accel-932（撳連結→確認加速） | home ✓（加速跑到週尾摘要→回家結算） | 8→14 | 813/565 | 0 | 2（支票圖） |
| rest-soft-map-932 | map ✓ | 14→15 | 228/228（冇溢出） | 0 | 0 |
| wrap-soft-返回地圖-700 | map ✓ | 15→16 | 764/485 | 0 | 2（支票圖） |
| wrap-soft-開始今日行程-700 | new-dayend ✓ | 16→18 | 785/485 | 0 | 2（支票圖） |
| wrap-map-返回地圖-700 | map ✓ | 18→19 | 760/537 | 0 | 2（支票圖） |
| wrap-forced-開始今日行程-700 | new-dayend ✓ | 19→21 | 838/537 | 0 | 2（支票圖） |
| accel-700（撳連結→確認加速） | home ✓（加速跑到週尾摘要→回家結算） | 22→28 | 809/485 | 0 | 2（支票圖） |
| rest-soft-map-700 | map ✓ | 28→29 | 228/228（冇溢出） | 0 | 0 |

- 700 幾何：modal 644px（top 46／bottom 690）、inner 485px（soft，2 行掣）／537px
  （map／forced，1 行掣）；最長內容版綠色結算行 451–492，fold 545，margin 53px。
  932 幾何唔變（modal 720／inner 565 或 617），綠色結算行 margin 84px。
- accel 連結實測：class `day-end-accel-link`、13.6px（.85rem）、底線、44px 高、全行；
  撳落去出確認 modal（取消→落地圖，day 唔郁；確認加速→連續結算到週尾摘要，
  再撳「回家結算」→屋企，day 推進 6 日）。
- wrap-forced-700 冇加速連結係啱嘅：嗰日係星期六，星期日計劃係 rest（唔係自動日），
  剩餘自動日＝0，連結唔出（logic test (e) 同款）。
- 休息卡（rest-soft-map）掣列一樣係三粒（返回地圖／開始今日行程／加速連結），
  撳返回地圖落地圖，day 唔郁（只係休息日結算本身推咗一日）。
- 中間兩輪 probe 修補（遊戲 code 冇郁過，淨係修 probe）：
  ① 種子要 reset 壓力＋清病假狀態（`hosp96TreatGate` 會攔路）、`S.homeEditable=false`
  （週結算後返規劃模式會令 `kickScheduleIfNeeded`／`#map-start-today` 失效，
  成個 700 腿開唔到板）；② chain 要識撳劇情抉擇 modal 第一粒掣
  （「傳呼台嘅一課」／「LD舖租碟夜」兩選一）同「回家結算」；③ 88dvh→92dvh
  （第三輪 wrap-soft-開始今日行程-700 `greenCut=1`，結算行 508–548 vs fold 545，
  差 3px——呢個係遊戲修法唔夠，唔係 probe 問題）。
- 報告：`qa189/drive189_report_fixed.json`（最終輪）、
  `qa189/drive189_report_pristine.json`（基線）；截圖 `qa189/shots189/`。

### 全套 suite（A/B 對照）

- pristine 基線（`main dcf1b72` 乾淨 clone，`qa189/suite_baseline_pristine.txt`）：
  **TOTAL PASS 255 FAIL 12**。
- work 樹第一跑：**TOTAL PASS 249 FAIL 20**——多出 8 項 FAIL，全部係行號釘靜態測試
  （gift185／kwan151／rom176／tang152／tang171／tang173／text125／travel114），
  根源係 v189 index.html 淨 +34 行令釘行漂移，唔係功能回歸。
  用 difflib 對位 pristine vs 現行逐個錨點核實內容逐字相同（純漂移），
  腳本 `qa189/resync189.py` 全部 PASS；8 檔測試釘行按映射更新＋加 v20a189 resync 註解。
  其中 travel114 COUNT 38844／39278／39281／39312 係 +33 唔係 +34（逐行內容核實過，
  唔係心算 shift，見 resync 腳本）。
- work 樹 resync 後第二跑：**TOTAL PASS 257 FAIL 12**——FAIL 清單同 pristine 基線
  **逐項相同**（`diff` 零差異）；PASS 多 2 項正正係兩檔新測試。
  相關測試逐個直接覆驗：`test_flow45_logic.js`（休息卡路徑）PASS，
  8 檔 resync 測試逐檔 PASS（kwan151 全 PASS、rom176 全 PASS、tang152 全 PASS、
  tang171 22/22、tang173 21/21、text125 PASS、travel114 PASS、gift185 全 PASS）。

## 5. 殘留

- **支票／片圖喺 fold 位半現（`anyCut=2`，12 個 wrap case 全部係支票圖）**：
  係正常捲動內容，唔係裁字——圖本身 ~242px，唔縮圖就唔可能成張首屏見晒。
  要成張見晒就要縮圖，係 v20a101／v20a105 定咗嘅設計，唔喺呢票郁，留待設計決定。
- **尾綠行喺 fold 之下（by design）**：「殺青獎勵：傳媒／街外／成績反響已整理——
  下一頁揭曉。」係板底最後一行，永遠要捲先見；scrollTest 證明捲到底全部尾行齊見
  （包括呢行綠色獎勵提示），唔係裁字。
- **700 極長內容版仍有理論裁字風險**：92dvh 下觀測到嘅最長版 margin 係 53px；
  再多一條 stat 行（~24px）或一行描述（~21px）都仲清得到，兩樣一齊多先至有機會
  再裁幾 px。觀測過三輪共 12 個 700 wrap case，只喺 88dvh 見過一次 3px 裁切，
  92dvh 未見過。要「任何內容都零裁」就要縮媒體，唔喺呢票。
- **加速流程終點係屋企唔係地圖**：確認加速跑到週尾會出「本週加速摘要」→撳
  「回家結算」→屋企（week settle），唔係直接返地圖；呢個係既有流程，唔係 v189 改出嚟。
  實駕 probe 嘅 settle 會再撳返地圖，唔影響驗證。
- **`.week-accel-hint` CSS rule 留返一行死 rule**：body 段落已刪晒（全檔只剩 CSS rule
  一處），留返係為咗唔郁其他可能引用佢嘅位；要清可以一併清埋 rule。
- **`day-res` static 檢查係守門唔係判別項**（見 §4 反證註）。
- **probe 學到嘅遊戲行為**（留返畀下一票實駕用）：`S.homeEditable=true` 會閂
  `kickScheduleIfNeeded`＋`#map-start-today`；去地圖途中會撞隨機劇情事件
  （WF4／傳呼台／LD舖）同病假閘，chain 要識撳埋佢哋先到地圖。

## 6. Rebase 上最新 main（2026-11-13 20:15–21:00，工人重驗）

- 舊基底 `dcf1b72`（v187）→ 新基底 main **`0c29f03`**（v188；期間 v190 `4283862`＋v188 落咗地）。
  Rebase 前 `git fetch origin` 核實 main 最新 HEAD 係 `0c29f03`。
- Rebase 結果：兩 commit 順利重播（`9834396`→`7e266be`、`e1f8f5b`→`4a6eee9`），
  遊戲改動（index.html 日結板掣＋modal CSS＋dayEndContinueButtons）零衝突——
  v188 改獎項類別、v190 改 glamour panel，同 v189 改區唔撞。
- 衝突：只得 5 檔靜態測試（gift185／rom176／tang171／tang173／travel114）嘅
  **行號 resync 註解＋斷言**撞區——兩邊各自 resync（v188 淨 +254、v189 淨 +34）。
  解法：註解兩邊保留；數字先取 main 版，再用 difflib 由分支舊 index（`e1f8f5b`，
  60189 行）對位到 rebase 後 index（60443 行）重算，**唔靠心算 shift**。
  腳本 `qa189/resync189_rebase.py` 全部錨點核實純漂移（內容逐字相同）：
  rom176 6 釘（6070／31574 唔郁、53115→53369、53483→53737、54622→54876、
  54716→54970）、DEF 54685→54939（tang171／tang173／travel114 共用）、
  travel114 COUNT 12／FREE 34 逐行映射（DEF 54939、WRAPPER 44387 唔郁）、
  tang173 L4862 錨點 4887 唔郁；總行數 60409＋34＝60443。
  其餘 3 檔（kwan151／tang152／text125）auto-merge 無衝突，逐檔直接覆驗全 PASS；
  tang152／text125 唔用硬行號錨點（內容搜尋），唔使改。
  附註：main 版 travel114 FREE 醫院區係 30817／30818／30830／30831／30842／30843，
  分支版係 +25 後嘅 30842／30843／30855／30856／30867／30868——同一批行，
  唔係漏咗／多咗，difflib 映射已核實。
- 新測試重驗：`test_dayend189_static.py` **23/23 PASS**、
  `test_dayend189_logic.js` **17/17 PASS**。反證唔使重做（測試本身冇改）。
- 全套 suite（`qa131/run_suite.sh`）：
  - pristine 基線（main `0c29f03` 乾淨 archive，`qa189/suite_baseline_main188.txt`）：
    **TOTAL PASS 259 FAIL 12**。
  - work 樹（`qa189/suite_work_rebase.txt`）：**TOTAL PASS 261 FAIL 12**——
    FAIL 清單同基線**逐項相同**（`diff` 零差異）；PASS 多 2 項正正係兩檔新測試。
    零回歸。相關測試逐個直接覆驗：8 檔 resync 測試＋dayend189 全部 PASS。
  - 中途插曲：第一跑 work 樹出咗 153／120——係 `/tmp`（512M tmpfs）俾
    pristine 解壓（463M）塞滿，suite redirect 寫唔到造成嘅假 FAIL；
    清走 `/tmp/pristine189-main` 後重跑即回復正常。教訓：pristine 唔好解去 `/tmp`，
    改解去 workspace（今次用 `~/workspace/linji-pristine189`，驗完即刪）。
    另：`run_suite.sh` 會 `cd` 入 repo root，outfile 要用**絕對路徑**，
    否則相對路徑寫唔到、成個 baseline 假 FAIL（第一個 baseline 嘗試就係咁死咗，
    要 kill 重跑）。
- 實駕重跑（`qa189/drive189.py --mode fixed`，Playwright live，port 8975，
  報告 `qa189/drive189_report_fixed.json`，截圖 `qa189/shots189/`）：
  **12/12 case，逐項同工人原報告一致**——wrap-soft 返回地圖→地圖／開始今日行程→
  新日結板、wrap-map 返回地圖→地圖、wrap-forced 開始今日行程→新日結板
  （932＋700 各 6 case）；加速確認 modal 出現→取消落返地圖且日唔郁
  （cancel_ok 兩 viewport 都 True）→確認加速行流程（day 8→14／22→28）；
  rest 卡返回地圖→地圖；綠色 notes 行 greenCut 全 0；**0 pageerror、0 http_fail**。
  （anyCut=1 vs 工人原報告 2 喺 accel-700 一項：fold 位半現嘅非綠行數目，
  係可捲內容，唔係裁字；greenCut 判據係 0，唔變。）
- 交貨：本 NOTES＋5 檔 resync 測試＋`qa189/resync189_rebase.py`＋
  suite 兩份＋drive 重跑報告／截圖一併 commit＋push 分支（force-with-lease，
  只推常駐 clone，唔上 GitHub）。**唔落地**——squash merge／push main／設計 review
  由統籌做。

## 落地紀錄
- 遊戲 commit `b7ca827`，線上親自 curl 核實 5,331,999 bytes、sha256 `bbca684a…`，同 repo `HEAD:index.html` 一致。
