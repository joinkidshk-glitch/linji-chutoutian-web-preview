# NOTES V20A11 — P0 試玩修復（基於 s107 / commit 93914a8）

> 對應試玩報告 `linji-chutoutian-playtest-improvements.md` 第 2 章 P0-1 至 P0-5。
> 原則：外科手術式改動；**無改 SAVE／localStorage 版本 key（仍 `starVolunteer_map_v19w`）、無改 softRev（仍 s107）、無改 `?v=` 參數**；金額計法同經濟平衡不變，只改「一致性、解釋、次序、遮擋」。
> 目標 branch：`fix/p0-playtest-fixes`（本筆記隨改動一齊入 repo 根目錄）。

## P0-1 薪酬矛盾（$550 vs $450–$650 vs 實收 $747）

**根因**：`rollAuditionPay()`（舊 L31553）喺 soft 模式對 `entryTier` 通告靜靜將擲出嘅牌面酬（`R(pay[0], pay[1])`，街景臨記係 $450–$650）乘 1.35，553×1.35≈747，超出公布上限又無任何解釋；同時通告欄／詳情用 `gigPayExactText()` 只顯示 `payExact` 單一數（$550），三處各講各的。

**改法**（金額計法不變）：
- `rollAuditionPay()` 回傳多 `basePay／bonusPay／bonusLabel`（入門加成 +35%；softBridge 補場 $800 亦計負差額），並為入門加成補返 `note`。
- `payContractNote(gig, lockedPay, roll)`：有加成時拆開列明「區間；牌面擲出 $X + 加成 $Y ＝ 合約 $Z」。
- `scheduleShoot(..., payBreak)` 將拆數存入 shoot（`payBase／payBonus／payBonusLabel`，新增欄位、舊檔兼容）；`payWrapNote(sh)` 殺青結算用同一拆法，加總對得返。兩個獲聘入口（即場試鏡／手帳約試鏡）都已接線。
- `gigPayExactText()`：有約酬區間嗰陣同框顯示「$550（約酬 $450–$650）」，列表同詳情共用同一函數。

**驗證**：`tests/test_p0_logic.js` 以擲出 553 重現試玩嗰單：pay=747、553+194=747、合約句同殺青句都含完整拆數；softBridge 補場分支拆數同樣對得返。

## P0-2 報紙重複派發

**根因**：殺青報版面（標題／內文）只由通告本身決定，但去重 key 係 `wrap:<gigId>:<拍攝日>`（`enqueueNewspaperFromWrap`）。同一通告換日再殺青，版面一模一樣但 key 唔同，`newspaperEventSeen()` exact-key 檢查放行，當新報再派；第二次 fameDelta 多數係 0，就出埋「這則未再改聲望」呢句系統話。

**改法**（跟返現有 np_／enqueue 機制，無另起爐灶）：
- `newspaperEventSeen()` 加一層：`wrap:` 開頭嘅 key 以 gigId 為準，queue／剪報（clippings）／待出（pendingMorningPaper）之中有同 gigId 嘅 wrap 紀錄即當已派發。
- 刪走系統話術：報紙淡紙行改「聲望未有變動。」；剪報頁 fameBit 同步改；檔案內建 `newspaperCheck` 兩處斷言（fade_html／story_c5_modal）同步更新至新字串。

**驗證**：邏輯測試證實同 gig 不同日嘅 wrap key 被擋、其他 gig／story key 唔受影響；靜態測試證實舊字串已清零。

## P0-3 傳聞卡文字重疊

**根因**：`.rumor-card` 無文件流排版保證；「有頭緒」印章（`.rumor-stamp`，68×68 絕對定位右下）無預留空間，長內文會寫到印章底；來源／標題無行數上限。另外拼合卡用詞同碎片唔一致（碎片「半夜喺蘭桂坊飲到爛醉」vs 拼合卡「夜晚又去買醉」）。

**改法**（無推翻 s107 對 tut-fx 高亮框嘅尺寸修復）：
- `.rumor-card` 加 `display:flex; flex-direction:column`；`.rumor-src` 單行省略號；`.rumor-title` 最多 2 行截斷；`.rumor-card.is-stamped` 加 `padding-right:86px` 畀印章留位。
- `MERGE_PAIRS` 陸柏言拼合文案改用返碎片原句：「半夜又喺蘭桂坊飲到爛醉」。

**驗證**：靜態測試檢查上述 CSS 規則齊全、傳聞文字元素無絕對定位、舊拼合文案已消失。

## P0-4 提示／教學遮擋

**根因（教學）**：`mergePickedRumors()` 舊順序係先 `renderRumorPane()` 後 `markRumorTutorialDone("merge")`——render 嗰刻教學未標完成，Step-5 拖曳教學（手指＋虛線箭咀 `tutorialPhase2DragGuideHtml`）同目標卡高亮重新掛上，之後無人再 render，殘留遮卡。
**改法**：調換次序，先標記完成、先至重繪；完成狀態本身已入存檔（`S.flags.rumorTutorialDone`），讀檔唔會重置。

**根因（提示）**：`toast()` 本身有 1.8 秒自動消失同 `pointer-events:none`，但同一句提示重複觸發會重置計時器，連環入地圖／過日時睇落久久唔散；而且無 sheet 嗰陣 toast 喺 `bottom:42px`，連同 `#app.toast-up::after` 嗰塊 88px 暗影壓住地圖底部快捷列。
**改法**：`toast()` 加去重——同一訊息＋副題喺顯示期間重複觸發直接返回，唔重置計時；CSS 將地圖上（無 sheet）嘅 toast 改去頂 `top:64px`（同 keep-sheet 既有規則對齊），並喺地圖上隱藏底部暗影 slab。

**驗證**：靜態測試檢查拼合流程次序、toast 去重守衛、1800ms 逾時保留、地圖 toast 新規則齊全。

## P0-5 結算次序＋生活費

**根因（次序）**：`endBrowseDayGoHome()`（提早休息）喺 `tickDay()` 之後刻意「先彈翌日報紙、先至出休息結算」（舊註解寫明），同正常日程（先結算、後喺 `runScheduleFromToday`／`goToMapForBrowse` 出報紙）唔一致，玩家見到 3/11 報紙早過 3/10 結算。
**改法**：刪走提早休息入面嗰段先行派報，改為直接出休息結算；報紙由結算後嘅既有路徑喺恰當時機派返，唔會漏派（兩條收尾路徑本來就會出報紙）。

**根因（生活費）**：`livingCostRoll()` 舊版喺費帶內隨機擲（第一週 $1,400–$1,800，擲出 $1,420），但預覽／日結提示寫中位數 $1,600，兩個數打架。
**改法**：`livingCostRoll()` 改用費帶中位數，同 `livingCostEstimate()` 同一數——預告幾多、實扣幾多；期望值同舊隨機區間中點一致，唔改平衡。週預覽同日結提示文案改為「定額，週結算照此數扣」；`settleWeek()` 補一行：存款唔夠畀足嗰陣，卡面講明只扣到幾多、餘額未扣（唔會扣到負數）。

**無做嘅部分（有意保留）**：報告建議「生活費改到週結算確認嗰刻先扣」需要新嘅 pending 結算狀態，會改變存檔時序同 `enterHome(summary)` 既有流程，風險高。今次以「金額提早明確預告＋預告等於實扣＋卡面逐項列明」達成同一透明度目標；如要做真・確認先扣，建議另開一票連存檔遷移一齊做。

**驗證**：邏輯測試證實 w=1..12 `livingCostRoll(w) === livingCostEstimate(w)`；靜態測試證實提早休息函數唔再先行派報。

## 整體驗證

- 改前／改後抽出全部 inline `<script>` 用 `node --check`：兩者皆 OK。
- `tests/test_p0_logic.js`：17 項全 PASS。
- `tests/test_p0_static.py`：27 項全 PASS（含 SAVE key／s107／v20a10 字串出現次數同原版一致）。
- 未能跑：檔案內建嘅瀏覽器 self-check（如 `newspaperCheck`）需要 DOM，本地無 jsdom，只更新咗佢哋引用嘅字串斷言，建議入 repo 後喺瀏覽器行一次 `__newspaper.check()` 等檢查確認。
- Diff（對原版 s107）：+105 行／−27 行，淨 +78 行（33,262 → 33,340 行）。
