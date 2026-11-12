# NOTES · v20a135 — 地圖底部卡收細（MAP135）

> **基底：** main `6395bad`（v133）｜**分支：** `v20a135`（工作副本 `~/workspace/linji-work135/`）
> **唔開 PR、唔用 GitHub connector、唔直推 main。** 落地前一刻已 `git fetch` 對過 origin/main：仍係 `6395bad`，**v134 未落 main，唔使 rebase**。
> SAVE `starVolunteer_map_v19w`、softRev `s107`、產品 `?v=` v20a10、HUD、地圖圖／地名標注／熱區、content pack JSON 全部唔郁。

## 用戶拍板內容（19:50 原 brief＋19:51 追加）

地圖主畫面底部 `#map-hint` 卡太高（~210pt，實測 234pt），食咗大地圖。追加指示：**「全部地點 ▸」掣都拎走**（地圖隱形熱區篤建築就入到，掣係多餘嘅）。

## 做咗咩（`index.html`，共 −14 行淨）

### 刪走（3 樣＋1 掣）

1. **灰色說明行**：`helpSoft`（兩版文案）＋`helpFirst128` block＋`seenMapHelp128` 旗標邏輯成組清走；靜態佔位文案（L5421）同步由舊灰字改做 `<b>載入中…</b>`（paintBar 一開即蓋過，純佔位）。
2. **藍色劇情卡**：paintBar 模板唔再計 `storyLine`、唔再串入 return；`refreshMapHintStory()` 改做**淨係移除殘留，永不再插入**（`insertAdjacentHTML` 刪走；`scheduleStoryMapRedraw` 等調用點唔郁，行為不變）。`storyMapHintHtml()` 本身**保留**（進度頁／其他地方用，另有 `test_progress71_static.py` 守住）。
3. **「全部地點 ▸」掣**：模板入面 `id="map-show-all-locs"` 成個掣拎走，頂行 `.map-hint-top128` flex 包裝一併刪（淨低日期 span）。掣嘅 JS 全部已係 null-safe，唔使改：`drawMap()` 嘅 `showAllBtn` 有 `if` 守衛、委派 `wireMapShowAllLocs` 淨係 `closest()` 唔中就 return、L52862／教學 spotlight 全部靜靜跳過。底層 toggle（`mapShowAllLocs`／toast 文案）留返，家下冇 UI 入口——按用戶決定（掣係多餘嘅）。

### 合併（計劃＋出行 → 一行）

- 舊：`今日計劃：到處逛逛` 一行＋`今日出行：仲可以去 1 個地方` 一行。
- 新（`planLine`）：`今日：<b>到處逛逛</b> · <span class="map-hint-travel">仲可以去 1 個地方</span>`；額度用完變體：`今日：到處逛逛 · 出行額度已用完，聽日再去`。兩個動態位（計劃名、`travel114Remain()` 數字）齊全；`stressHint`（壓力偏高／爆表）照跟呢行尾。
- 舊 `travelLine114` block（`rem114`）刪除，改由 `planLine` 入面 `rem135 = travel114Remain()` 計。

### 保留

- 日期＋週數行（`fmtDate()`：`1990年1月1日（一）· 第1週`）、大金掣「過一日」（`#map-end-day`／`#map-start-today` 行為一律唔變）、`audLine108`（有等緊試鏡回音先顯示，開局唔出）。
- 修後卡剩 3 行：日期／合併行／過一日。

### CSS（`#v-map` 段）

- 刪死規則：`.map-hint-top128`、`#v-map .map-hint #map-show-all-locs`、`#v-map .map-hint .map-hint-help`。
- 加：`#v-map .map-hint .map-hint-plan .map-hint-travel{ display:inline !important; … }`（出行 span 喺合併行入面行內顯示，唔再獨佔一行；金色＋粗體沿用舊 `.map-hint-travel` 規則）。
- **刻意留返**（死咗但無害，唔誤刪共用規則）：全域 `.map-hint-help`／`.map-hint-story` 規則（L1402／L2104／L2759／L3840 段；story 函數保留、v128 test 守住 2 行 clamp）、`.bar`／`#app` 區舊 `#map-show-all-locs` 規則（v128 搬掣入卡嗰陣已死，唔係今票生出嚟嘅）。

## 重要量度發現：地圖係闊度-bound，唔係流佈局

先量度再落手，發現同原 brief 假設唔同：

- 地圖圖 1376×1824（比例 0.7542），舞台高跟圖自然比例，v20a43 定案（`object-fit:contain`、`height:auto`），**唔改 cover**——cover 會裁圖邊，熱區百分比對位會走位。
- polaroid padding 已經係 `0`（v19z20 定案），圖已經係最闊（stage 384pt，wrap 390pt 減 2px 邊＋1px 框）。**中途試過加 `#app .map-polaroid{ padding:3.5% 2.5% … }` 收窄紙邊，實測圖反而由 509 縮到 483pt——即刻 revert 咗**（v17h 嘅 7.6% padding 早被 v19z20 `padding:0` 蓋過，唔係活規則）。
- 結論寫埋入 code 注釋：932 屏圖已完整顯示，卡縮細騰出嘅位變羊皮紙；700 短屏卡原本遮住圖底，卡縮細 1:1 轉化做可見圖高。想再放大就要改 cover 裁圖，會郁熱區對位，今票唔做（等拍板）。

## 修前修後量度對照（Playwright 實駕，開局 1990-01-01 第 1 週，`?softPreview=1`）

| 量度 | 430×932 修前 | 430×932 修後 | 430×700 修前 | 430×700 修後 |
|---|---:|---:|---:|---:|
| 卡高 `#map-hint` | 234pt | **121pt（−113，≤150 ✓）** | 234pt | **121pt（−113）** |
| 地圖圖高 `.map-img` | 509pt | 509pt | 509pt | 509pt |
| **可見圖高**（圖 ∩ polaroid 框） | 509pt | 509pt | 382pt | **495pt（+113）** |
| 可見圖佔屏 | 54.6% | 54.6% | 54.6% | **70.7%** |
| 卡底 → 屏底 | 816（餘 116pt 羊皮紙） | 703（餘 229pt 羊皮紙） | 688 | 688 |

- 修前卡 234pt（brief 話 ~210pt，實測 234——劇情卡副行令佢再高啲）。
- 932 屏：圖本身唔會再大（已係最闊，見上節）；卡佔屏由 25.1% → 13.0%。
- 700 屏：修前卡遮住圖底 127pt（可見得 382pt）；修後可見 495pt，+113pt，啱啱等於卡縮細嘅數。
- 實駕斷言（修後兩屏全 PASS）：卡 ≤150pt、「過一日」可見、「仲可以去 1 個地方」可見、冇 show-all／story／help、零 page error。
- 「過一日」可撳另有專項 probe：撳落去彈「確認過一日？」modal（確定過一日／取消），零 page error，行為不變。
- 變體 probe（`__dualHud.paintMap()` 重繪）：額度用完卡文案 `今日：到處逛逛 · 出行額度已用完，聽日再去` ✓；`pendingAud` 有 1 張嗰陣 `等緊 1 張試鏡回音…` 正常出現 ✓；`refreshMapHintStory()`＋`scheduleStoryMapRedraw()` 之後 `.map-hint-story` 唔會再插返入嚟 ✓。

## 測試

- **新** `tests/test_ui135_mapcard_static.py`（25 項）：灰字／旗標／掣／劇情卡唔喺模板、合併行字串在、舊分行寫法唔見、日期／aud／過一日保留、`refreshMapHintStory` 唔再插入、story 函數保留、死 CSS 清走、佔位灰字清走。**work 全 PASS；pristine main 乾淨 FAIL（17 項，唔 crash）**。
- **resync** `tests/test_ui128a1_static.py`：全部地點掣斷言反轉（v135 拎走）。work PASS；pristine 淨係呢項 FAIL（預期之內）。
- **resync** `tests/test_travel114_static.py`：① 合併行文案（`rem114`→`rem135`、`今日出行：`前綴隨分行刪走）；② 行號 allowlist 純漂移——`qa135/resync_travel114.py` 核實 44 個 `openLoc(` 呼叫點序列逐字一致、逐行內容相同（COUNT 13／FREE 27 不變；CSS 淨 +1、模板淨 −15）。work PASS；pristine 乾淨 FAIL。
- **resync** `tests/test_text125_static.py`：硬編行號純漂移（CSS 淨 +1）：currentLine 27557→27558、advance 27670→27671、familySafe 33268–33270→33269–33271，舊行內容逐行核實相同。work PASS；pristine FAIL（預期之內）。
- **全套**（`qa135/run_suite.sh`）：**work PASS 193 FAIL 12；新鮮 pristine baseline（`git worktree`，`~/workspace/linji-base135/`，origin/main `6395bad`）PASS 192 FAIL 12——FAIL 清單完全一致，零回歸**。12 個 FAIL 全部 pre-existing（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），baseline 一樣 FAIL。
- `node --check`：抽 2 段 inline script 驗語法，全部 OK（Node 24 拒 `.html`，故抽段驗）。

## 實駕證據

- `qa135/drive135.py`（新遊戲 → 跳過教學 → 返地圖量度；留意：地點 sheet 開緊嗰陣 `#map-hint` 會壓成 2.8em 緊湊態，量度前要先撳「返回地圖」閂 sheet；`text=過一日` locator 會撳到隱藏副本，要用 JS 搵可見掣先撳）
- 修前：`qa135/drive135_pre.json`、`qa135/shots/pre_430x932.png`、`qa135/shots/pre_430x700.png`
- 修後：`qa135/drive135_post.json`、`qa135/shots/post_430x932.png`、`qa135/shots/post_430x700.png`
- 全套：`qa135/suite_work135.txt`（work）、`qa135/suite_baseline135.txt`（pristine）
- resync 工具：`qa135/resync_travel114.py`
- 變體／撳掣 probe：`/tmp/probe135c.py`、`/tmp/probe135d.py`（結果見上節；probe 本身唔入 repo）
