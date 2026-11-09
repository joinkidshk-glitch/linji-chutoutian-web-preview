# v20a50 存檔槽顯示診斷：首次載入 vs 重載不一致——查無 code 缺陷，不作修改

## 任務與症狀

v20a39 實機驗收附帶發現（只觀察到一次）：首次載入遊戲時，開始畫面／讀檔位嘅
「新遊戲」槽位顯示，同重新載入之後嘅顯示不一致；重載之後兩邊一致、之後一直正常。
當時假設：舊存檔遷移同槽位渲染時序問題——第一次 render 喺遷移完成／寫回之前，
顯示遷移前狀態；重載讀到已遷移檔就正常。

**結論：假設根因唔成立（有行號＋實測證據，見下）。index.html 零改動**
（同 v20a49 byte-identical，4,210,205 bytes）。本期交付＝診斷報告＋兩套守護測試，
鎖死已驗證嘅不變量，防日後改版真係引入時序問題。

## 證據一：槽位顯示係 localStorage 嘅純函數，渲染嗰刻即時讀，冇快取狀態

槽位顯示只有兩個出口，兩者都喺渲染嗰一刻先讀檔：

- 標題畫面「繼續／讀檔」掣：boot 尾段 `(function paintTitleSaveBtns(){...})()`
  （行 38799 起）呼叫 `hasSave()`（行 24245）→ `listSaveSlots()`（行 24232）。
- 揀槽 modal（新遊戲／讀檔／存檔共用）：`openSaveSlotsModal(mode)`（行 24271）
  喺開 modal 嗰刻先行 `const slots=listSaveSlots();`（行 24275）砌行文。

`listSaveSlots()` 對每槽行 `readSlotRaw(i)`（行 24224）：直接
`localStorage.getItem(saveKeyForSlot(slot))` + `JSON.parse`，再由
`saveSummaryFrom`（行 24214）計摘要。冇任何一處將槽位狀態喺 boot 時快取落嚟
之後重用——唔存在「第一次 render 攞舊狀態、之後冇 re-render」嘅結構。

## 證據二：存檔遷移只喺記憶體行、從不寫回；boot 期間存檔 key 零寫入

- 遷移／正規化函數係 `normalizeSaveObj(o)`（行 24203），唯一呼叫點係
  `loadFromSlot(slot)`（行 24260）——即玩家真係㩒「繼續／讀檔」載入嗰陣。
  標題畫面階段 S=null，boot 路徑唔會呼叫佢。
- `loadFromSlot` 全函數冇 `localStorage.setItem`（靜態測試鎖死）：
  遷移結果只回傳記憶體物件，唔寫回。存檔寫入只經 `saveToSlot`（行 24246）／
  `saveQ`（行 24257），兩者都要有進行中嘅 S，標題階段唔會觸發。
- boot 期間唯一嘅 localStorage 寫入係 **prefs** 一次性遷移：`loadPrefs`
  （行 24166）發現舊 prefs 嘅 `familySafeContent===false` 且未顯式設定時，
  升為 null 並即時寫回 prefs key 一次（行 24174–24177）。唔掂存檔 key、
  唔改 activeSlot／lastSlot，對槽位顯示零影響（邏輯測試 D 段鎖死）。

## 證據三：就算遷移行先，摘要都唔會變——摘要欄位對遷移係不變量

槽位摘要得三欄，全部嚟自遷移唔會掂嘅欄位：

- 週數：`Math.floor(dayIndex/7)+1`（行 24216–24217）——normalize 唔改 dayIndex。
- 存款：`Number(o.money)||0`（行 24218）——normalize 唔改 money。
- 聲望（stage）：`saveSummaryFrom` 經 `readDualTracks`（行 24625）→
  `dualTrackNumbers`（行 24613），`stageVolume = fame`（行 24620）——normalize 唔改 fame。

`normalizeSaveObj` 實際做嘅嘢：補缺失容器（inventory／giftMeta／wrapHistory／
castingTags／postShootRewards／awardsLog／awardsFlags／newspaperQueue／
newspaperClippings，行 24205–24211）、vocal 缺失補 14（行 24207）、
stress 超過 STRESS_MAX 夾落上限（行 24209）、`syncDualTracks`（行 24211，
只寫 stageVolume／industryCredit 兩個衍生欄，唔入摘要）。冇一樣入槽位摘要。
邏輯測試 B／C 段以舊格式 fixture 實證：遷移前後 `listSaveSlots()` 輸出
逐字節相同；遷移結果本身（補欄、夾 stress、核心欄不動）亦逐項驗明，
同現行（修復前）行為一致——舊存檔相容冇變。

## 證據四：真頁面實測（Playwright，舊檔種子＋setItem 全程監察）

實驗環境：本機 HTTP serve 現行 index.html＋線上 content 檔 40 個；
種入舊格式存檔（槽 1：缺 normalize 會補嘅全部欄位、stress=130；
槽 3：另一舊檔；槽 2：空）＋舊 prefs（觸發一次性遷移嗰款）；
以 init script 包住 `Storage.prototype.setItem` 記錄所有寫入。

結果：首次載入、等 async 內容包 settle 後再開槽、重載、三載——四次嘅
槽位行文（「槽 1 · 第 5 週 · 存款 $23,456 · 幕前聲望 42 · 使用中」等）同
標題掣狀態完全一致；全程 setItem 日誌只有 prefs 遷移嗰一次寫入，
存檔 key 由頭到尾冇被寫過。

## 證據五：槽位渲染 code 跨版本冇變過

`listSaveSlots`／`saveSummaryFrom`／`openSaveSlotsModal`／`paintTitleSaveBtns`
四段喺本地所有歷史工作副本（v20a11 原始副本、v20a37、現行 v20a49）md5 完全
相同。就算首次載入食到舊版文件，槽位邏輯同文案都唔會唔同。

## 咁嗰次觀察到嘅係咩？（最合理推斷，無法再現）

無法以現行 code 再現。最脗合「只此一次、重載即正常」嘅解釋係部署直後嘅
文件快取：index.html 自己嘅頭注（行 10–16）記錄咗呢個已知陷阱——
GitHub Pages 對 HTML 設 max-age=600，試玩盒又有按完整 URL 嘅持久快取，
曾令部署後首次載入繼續執行舊文件、重載先攞到新文件。v20a39 驗收正值
部署直後，首次載入好可能跑緊上一版文件（開始畫面周邊狀態有別），
重載後一致。屬環境／快取因素，唔係槽位或遷移 code 嘅缺陷。

## 本期產出

- `index.html`：**零改動**（4,210,205 bytes，同 v20a49 byte-identical）。
  按任務守則：根因唔成立，唔亂改。
- `tests/test_slot50_logic.js`（27 斷言，全 PASS）：抽真函數驗舊檔摘要、
  遷移不變量、loadFromSlot 零寫回、normalize 結果逐項、prefs 遷移只寫一次
  唔掂存檔、壞檔／非物件檔顯示空白唔爆。
- `tests/test_slot50_static.py`（15 斷言，全 PASS）：結構鎖死
  （loadFromSlot 冇 setItem、開 modal 即時 listSaveSlots、標題掣源自 hasSave、
  遷移規則原樣）＋紅線（SAVE key／?v=／softRev／style 大括號平衡）。
- 全套 repo tests：**37/37 檔案 PASS**（原 35＋新 2）；兩段 script
  `node --check` OK。

## 紅線確認

唔改 SAVE key（`starVolunteer_map_v19w`）、唔改存檔格式／遷移規則、
唔改 softRev（s107）／產品 ?v=（v20a10）。冇推 repo（留畀主代理決定：
本期只有測試＋NOTES，如要入 repo 可有可無；index 本身冇嘢要部署）。

## 日後備註（畀原生移植）

- 遷移唔寫回係現行設計：舊檔每次載入都重新 normalize 一次（純函數、平價），
  唔係 bug；原生版可保留同一語義（load 時 normalize、save 時先落盤新格式）。
- 若日後真係想連 prefs 嗰次 boot 寫入都消除，要注意嗰個寫回係
  familySafeContent 語義升級嘅一部分，郁之前要先確認內容過濾預設行為唔變。
