# NOTES — v20a112 圖標組全量製作・審計＋接入

- **版本**：v20a112（原編 v111，2026-11-12 07:04 更正：v111 已畀 S-30 套用包）
- **分支**：`v112-icons`（工作目錄 `~/workspace/linji-work111/`，基底 main `546007d`）
- **風格**（用戶 2026-11-12 06:59 批核「ok」）：細線條手繪風，深啡墨線 `#3a2e22`、無填色、透明底 PNG 256×256
- **範圍**：審計 S-17／S-22／S-38／S-46 四個受影響畫面＋全庫 emoji；26 隻圖標接入；S-46 人脈頁 ♥/♡ 改 CSS 進度格
- **唔推 repo**（parent 指示）；**唔改** SAVE key／softRev／`?v=`（見測試紅線）

## 1. 圖標清單（26 隻，`assets/icons/`）

樣本 12 隻（由 `~/workspace/linji-icon-sample/icon_*.png` 複製原檔）：
`icon_map`（地圖）／`icon_sleep`（休息）／`icon_mic`（唱歌）／`icon_tea`（飲茶）／
`icon_clapper`（拍戲）／`icon_fitness`（健身）／`icon_home`（屋企）／`icon_news`（報紙）／
`icon_gift`（禮物店）／`icon_hospital`（醫院）／`icon_music`（音樂）／`icon_people`（人脈）

新圖 14 隻（生成工人出，QC 14/14 PASS，`qa111/qc111_icons.png`）：
`icon_tv`（電視）／`icon_radio`（電台／廣播）／`icon_lion`（獅子山製片）／
`icon_briefcase`（廣告／公事包）／`icon_building`（大廈／公司）／`icon_mask`（戲劇面譜）／
`icon_book`（書／學業）／`icon_martial`（武術）／`icon_broom`（打掃）／`icon_sick`（生病）／
`icon_phone`（電話／等消息）／`icon_mood`（心情）／`icon_star`（紅星）／`icon_sparkle`（閃爍／特別）

24px 下獅子／面譜／武術／病只剩輪廓＋主特徵，同已批核樣本喺 24px 嘅退化程度一致，按已批核標準收貨；
獅子係最弱一隻，實機後若覺得唔夠清楚先再簡化（今次實駕未見問題）。

## 2. 接入方式（中央 resolver，欄位值唔改）

- 欄位值（`icon:`／`emoji:`／`channel.icon`／LOCS emoji）**保留原 emoji**：舊存檔相容，舊測試唔使改。
- 渲染統一經中央 helper（加喺 `uiIcon()` 之後，約 L33847）：
  - `EMOJI_ICON112`：31 個 emoji 值 → 26 個圖檔 stem（🗺️ key 係 U+1F5FA＋VS16，已逐 byte 核實；
    查找先精確、再去 VS16、再補 VS16）。
  - `iconHtml112(v)`：有對應 → `<img class="ic112" src="assets/icons/icon_<stem>.png" …>`；
    ✅ → `<span class="ic-check112">✓</span>`（綠色 CSS 勾）；`·` → 原樣；未對應 → escape 後原樣 passthrough。
  - `favDots112(n)`：S-46 人脈頁 5 格進度點（`<span class="fav-dots112">`＋5 個 `<i>`，0–5 clamp，`.on`＝實心金）。
  - CSS（加喺 `.psr-icon` 之後，約 L3845）：`.ic112` 按容器調尺寸（行程列 1.2em／分類 tab 1.4em／
    活動列 1.25em／psr 1.15em／地點板標題 1.1em）、`.ic-check112` 綠色粗體、`.fav-dots112` 9px 金色圓點。
- 改咗 **20 個渲染位**（grep：`iconHtml112(` 呼叫位 20 處＋定義＋1 處註釋＝22 命中；`favDots112(` 定義＋2 呼叫）：
  週行程 `.ic`／分類 tab `.ci`／活動列 `.ai`／日結結果行（`resolvePlannedDay` body）／
  EXEC105 `nbRowMeta105`／訓練指南（`COURSE_DEFS`）／地圖底欄 `#map-area-list`（見 §6：CSS 隱藏中）／
  地點板標題（`textContent`→`innerHTML`＋`esc59`）／S-38 psr kicker（`channel.icon`＋3 處 hardcode：
  ✨／📰／📻；🏆 嗰行留低）／拍攝簿 5 處（📞／✅📞／🎥／🎬／✅）／S-46 人脈頁 2 處（`enc79PeopleHtml`＋`people72Html`）／
  禮物渲染 3 處（`iconHtml112(item.emoji||"🎁")`，象形字 passthrough）。
- `index.html` diff：56 insertions／22 deletions。兩個 script block 都過 `node --check`。

## 3. 對照表（階段一審計）

完整表見 [`notes_icon_audit.md`](notes_icon_audit.md)。

- README 話「33 個不同 emoji 值」**核實為 32 個 emoji 值＋♥**：`icon:` 欄位 23 個不同值（含非 emoji `·`×2）、
  `emoji:` 欄位 15 個不同值，union（唔計 `·`）＝32；README 嘅 33 係連 ♥ 一齊計（♥/♡ 只喺 S-46 心形字串出現）。
  全檔掃描：44 個不同 emoji／符號序列、123 次出現。
- 31 個 emoji 值 → 26 隻圖（見 §1）；✅ → CSS 綠勾。
- **留返 emoji（有原因，唔係漏咗）**：
  - 🏆 ×7（頒獎／成就）：未 commission 圖標——殘留缺口，建議跟進 `icon_trophy.png`。
  - 🔒 ×4（鎖定狀態）、💡 ×4（情報提示，含地圖 fallback，極少命中）：語義係狀態標誌，唔係類別圖標。
  - 📋 ×1／👤 ×1：地圖 fallback only，圖例圖已存在。
  - 禮物象形 🍍🧁🧴📎📝📼🍬🌸 ×8（`content/items_gifts.json` 10 件禮物；☕📰 已有圖）：逐件象形，要多 8 隻圖先換得晒。
  - 已係 CSS 文字元號：✓／✗／○、★／☆、☰、`·`。
- README 偏差（審計發現）：手帳頂部 5 tabs＋全部 sub-tabs 本身**純文字、無 emoji**，無嘢可換（加圖標係新設計，唔喺範圍）；
  通告卡本身無類型 emoji（★/☆ 係評分、✓/✗ 係要求格、💡 係情報）；📡（海港廣播）同 📻 共用 `icon_radio.png`；
  九龍電視台用 📻 係舊數據，唔喺呢包改。

## 4. 測試結果

### 新測試（2 檔＋menu72 追加斷言）
- `tests/test_icons112_static.py`：helper／對照／圖檔／CSS／渲染位／舊片段已消失／保留 emoji／紅線 —— **ALL PASS**
- `tests/test_icons112_logic.js`：31 個對應（含逐個 `<img>` 字串）、✅ CSS、欄位值枚舉（33＝32 emoji＋`·`）、
  passthrough、favDots clamp —— **ALL PASS（90 斷言）**
- `tests/test_menu72_logic.js` 追加 5 斷言（拍攝簿數據驅動）：拍攝中 🎥→`icon_clapper.png`、履歷 ✅→`ic-check112`、
  等消息 📞→`icon_phone.png`、試鏡消息 ✅/📞→綠勾＋電話圖、待試鏡散工 🎬→`icon_clapper.png`，
  全部附「無對應 emoji 字面」斷言 —— **ALL PASS**
- **反證**：對 pristine 基線（`git show 546007d:index.html`）——static 65 FAIL／9 PASS（9 PASS 係保留 emoji＋紅線斷言，兩邊都真）；
  logic 乾淨 FAIL（exit 1，helper 抽唔到）；menu72 喺基線載入即 throw（`EMOJI_ICON112` 不存在）。
- 紅線斷言：SAVE `starVolunteer_map_v19w`、softRev `s107`、`?v=20a10`——全部無郁。

### 全套 A/B
- 基線（改前）：**142 PASS／12 FAIL**（`qa112/suite_baseline112.txt`）
- 改後：**144 PASS／12 FAIL**（`qa112/suite_work112.txt`）——＋2＝兩隻新測試檔；12 FAIL 同基線 byte-identical，
  全部係已知環境性 static FAIL：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、
  start53、weave43、weave44、weave49、wrap38。**零新增回歸。**
- 10 隻舊測試因新 helper 要補沙盒載入（harness only，零行為改動）：
  `test_aud91_logic.js`、`test_enc84_logic.js`、`test_levels75_logic.js`、`test_menu72_logic.js`、
  `test_progress71_logic.js`、`test_rest58_logic.js`、`test_stamina58_logic.js`、`test_verify37_logic.js`（三個沙盒）、
  `test_weave47_logic.js`、`test_ux68_static.py`（地點板標題新 `innerHTML`＋`esc59` 形式）。

## 5. 實駕結果（Playwright headless shell，390×844，dsf=2）

- 驅動：`qa112/drive112.py`（伺服 `python3 -m http.server 8932`）；日誌 `qa112/drive112_pre.json`／`qa112/drive112_post.json`；
  截圖 `qa112/shots/`（`pre_*`／`post_*`）。
- 路線：新遊戲 → 跳過教學 → 寫手帳 → 確定出發 → 地圖 → 全部地點 → 金龍茶餐廳（巧遇自動撳過，13 撳）→
  地點板 → ☰ → 手帳（行程／人情→人脈／事業／近況／消息）→ 返回地圖 → 過一日（週一逛逛日，小休）→
  開始今日行程（週二休息日）→ 過一日（週三／週四逛逛日）→ 開始今日行程（週五街頭表演→週六咖啡店駐場，日結板）。

| 畫面 | 改前 ic112 | 改後 ic112 | 損壞圖 | 備註 |
|---|---|---|---|---|
| 地圖 | 0 | 26 | 0 | 13 手帳隱藏 DOM＋13 地點底欄 DOM（CSS 隱藏，見 §6） |
| 全部地點 | 0 | 28 | 0 | 底欄 15 隻全出 |
| 地點板（金龍茶餐廳） | 0 | 27 | 0 | 標題前有茶杯圖：` 金龍茶餐廳 · 油麻地`，locImg=1 |
| 手帳・行程 | 0（emoji：🗺️😴🎤☕） | 26 | 0 | 日 `.ic` 7/7 `<img>`、分類 `.ci` 5/5、活動 `.ai` 1/1 |
| 手帳・人脈 | 0（♥/♡ ×39） | 26 | 0 | fav-dots 7 組（1 格實心）、♥/♡ 字面 0 |
| 手帳・事業／近況／消息 | 0 | 26 | 0 | 同上（人脈格留喺 DOM） |
| 日結（週一小休） | — | 26 | 0 | 小休 modal 本身無 icon 位（by design，見 §6） |
| 日結（週二休息） | — | 26 | 0 | 休息動畫 modal，無 icon 位（by design） |
| 日結（週六咖啡店駐場） | — | 27 | 0 | **日結板 icon 實駕驗證：`icon_tea.png`×1**（`resolvePlannedDay` body 行） |

- **0 pageerror、0 損壞圖片**（全程）。
- 語義核對（目視截圖）：地圖＝到處逛逛、月亮＝休息睡覺、咪＝街頭表演、茶杯＝咖啡店駐場——全部同原 emoji 一致。
- 改前／改後對照截圖：行程編輯頁 `pre_nb_plan.png`／`post_nb_plan.png`、地圖頁 `pre_map.png`／`post_map.png`、
  手帳人脈 `pre_nb_people.png`／`post_nb_people.png`、地點板 `pre_locsheet.png`／`post_locsheet.png`、
  日結板 `post_dayres_fri.png`（改前無對應畫面——首週行程未行到嗰度）。

### 實駕期間查明嘅事（唔係 bug，記低免後人重查）
- `window.iconHtml112` 係 `undefined` 係**預期**：成個遊戲 JS 包喺 IIFE 入面（L17 `(function(){`），helper 正確地只喺作用域內。
- 實駕初期 hearts 計數（39→2）係量度假象：`document.body.textContent` 包含 `<script>` 內文——
  pre 嘅 39 係隱藏手帳 DOM 入面嘅 S-46 心形字串；post 嘅 2 係我自己寫喺 S-46 註釋入面嘅 ♥/♡ 字面。
  註釋已改寫做「好感心形字串」（無 emoji 字面），最終 hearts=0。
- `click_first` 驅動器改用 JS dispatch 撳掣＋3 次重試：Playwright 嘅 actionability check 喺呢個 app 重新渲染嘅
  modal 度會 timeout（縱使 handler 已經觸發）；地圖提示喺 modal 閂咗之後要一陣先重新渲染出掣。
- 過日流程：逛逛日無「開始今日行程」掣，要撳「過一日」→二次確認「確定過一日」→小休 modal；
  有排程嘅日子先有「開始今日行程」→確認 modal→執行→日結板。休息日行 `presentRestSleepDayEnd` 動畫 modal，
  唔行 `resolvePlannedDay` 嘅 body 行。

## 6. 唔換／換咗都睇唔到嘅位（刻意，唔係漏網）

- **`#map-area-list`（地圖底欄地點快捷列）換咗都睇唔到**：v20a43 起 `#app #map-area-list{ display:none !important; }`
  （用戶 2026-11-09 決定刪走底欄快捷列、地圖放大；JS 照生成＋綁定，DOM 入面 15 隻圖齊出、0 損壞）。
  呢包照換（萬一日後重開返條列，圖已經喺度），但**可見效果＝零**；實駕只量 DOM，唔截元素圖（display:none 元素截唔到）。
- **地圖底部提示（`#map-hint`「今日計劃：…」）無 icon**：本身純文字，冇 emoji 可換。加圖標係新設計，唔喺呢包做。
- **小休／休息 modal 無 icon 位**：`presentRestSleepDayEnd` 動畫 modal（週一小休、週二休息）本身無 icon 槽，
  唔係 `resolvePlannedDay` body 行；日結板 icon 位只喺非休息執行日出現（週六咖啡店駐場已實駕驗證）。
- **地圖提示文案同掣名唔一致（舊問題，唔喺呢包改）**：提示寫「要過日請撳「開始今日行程」」，但逛逛日實際掣名係「過一日」。
  實駕證實掣本身運作正常，只係文案過時。

## 7. 殘留缺口（跟進用）

1. **🏆 無圖**（頒獎／成就 ×7）：建議跟進 `icon_trophy.png`，接入點同其他 26 隻一樣。
2. **禮物象形 8 隻**（🍍🧁🧴📎📝📼🍬🌸）：要逐件出圖先換得晒；現時 passthrough。
3. **九龍電視台 📻 舊數據**：`channel.icon` 寫錯台徽（應用 📺 類），唔喺呢包改數據。
4. **獅子 24px 最弱**：實駕未見問題；真機檢查後若覺得唔夠清楚先簡化。
5. **S-38 psr kicker 未實駕**：靜態＋邏輯測試覆蓋咗（`channel.icon`＋✨／📰／📻 hardcode 換圖、🏆 留低）；
   首週行程未觸發傳聞推送，實駕無緣見到。
6. **拍攝簿 5 個 icon 位未實駕**：首週無拍攝／試鏡紀錄；已補數據驅動斷言（`test_menu72_logic.js`，見 §4），
   靜態＋邏輯測試覆蓋。

## 8. 檔案清單

- `NOTES_V20A112_ICONS.md`（本檔）
- [`notes_icon_audit.md`](notes_icon_audit.md)（階段一對照表）
- `assets/icons/icon_*.png`（26 隻）
- `tests/test_icons112_static.py`、`tests/test_icons112_logic.js`（新守門測試）
- `tests/test_menu72_logic.js`（追加 5 斷言＋`aud91Ensure` stub）
- `qa112/drive112.py`、`qa112/drive112_pre.json`、`qa112/drive112_post.json`、`qa112/shots/`（實駕）
- `qa112/suite_baseline112.txt`、`qa112/suite_work112.txt`（全套 A/B，v108 基線 142／12）
- `index.html`（56 insertions／22 deletions；另 10 隻舊測試 harness-only 修補）

## 9. 合併前 rebase 補記（統籌）

分支原基於 v108（`546007d`），合併前 rebase 到最新 main `41e4be8`（已含 v109、v111），**零衝突**。Rebase 後重跑全套：

- Pristine main 基線（`qa112/suite_baseline_main.txt`）：**147 PASS／12 FAIL**
- Rebase 後工作版（`qa112/suite_work112_rebased.txt`）：**149 PASS／12 FAIL**（＋2＝兩隻新測試；12 FAIL 同基線逐字相同，全部已知環境性 static FAIL）——**零新增回歸**
- `node --check`（抽 inline script）通過；紅線 SAVE／softRev／`?v=` 無郁；兩隻新測試單獨重跑 PASS。

合併方式：squash 入 main；`qa111/`（生成工人 QC 工作目錄）留喺工作區，唔入 main。
