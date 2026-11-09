# NOTES V20A46 — StoryPlay 標題區（.sp-head）根因診斷＋修復

性質：soft 預覽換膚修復。唔改 SAVE key（starVolunteer_map_v19w）、softRev（s107）、產品 ?v=（v20a10）；唔改 content pack；唔改 StoryPlay 對話邏輯/模板結構。工作副本 `~/workspace/linji-work46/`（基線 v20a45，4,199,207 bytes）。

## 症狀（兩輪實機）

全屏分層版面下，`.sp-head` 場景標題字頂似被削平/裁、meta 行（主線 · 1988春）同 progress 行（對白 X/8 · 句 Y/Z）幾乎睇唔到（深色字、冇底色襯托、對比極低）；只有 `.sp-setting` 描述行清晰（有深色半透明底）。v20a44 改過排版（block 疊排、頂距 12px、line-height、不透明度、漸變略加深）——實機依然 FAIL。

## 根因（證據）

**主因：兩條通用 modal 排版規則以 `!important` 強制深色，本層淺色從來冇生效過。**

- 行 1755–1758：`#mask:not(.tut-on) .modal h3{ color:#1A1A2E !important; font-weight:800 !important }`——所有非教學 modal 嘅 h3 一律深海軍藍。特異度 (1,2,1)。
- 行 1759–1764：`#mask:not(.tut-on) .modal p, …{ color:#3a2e22 !important }`——所有 modal 內 `<p>` 一律深啡。特異度 (1,2,1)。
- `.sp-head` 嘅三行偏偏就係一個 h3（標題）＋兩個 p（`.sp-meta`、`.sp-progress`）；v20a41/44 皮膚層畀佢哋嘅淺色（`#f8efdb`／`rgba(245,234,210,.92/.95)`）**冇 !important**，按 cascade 規則，!important 宣告無條件壓過任何冇 !important 嘅宣告（特異度再高都冇用）。所以 v20a44 調不透明度/陰影注定冇效——改嘅根本唔係生效緊嗰條 color。
- **對照組**：`.sp-setting` 係 `<div>`，唔中 h3 規則、唔中 p 規則，皮膚層淺色＋`rgba(12,8,4,.32)` 底正常生效——正係實機「得描述行睇得清」嗰行。同一 head、四行入面三行死一行活，死活分野同元素種類（h3/p vs div）完全吻合，機制實錘。

**次因（加重睇唔清）：** head 漸變舊 stops 係 `.66 → .3(62%) → 0(100%)`，progress 行位於 head 底部、嗰處漸變已近乎全透明，深色字直接落喺場景圖最雜亂部分，零底色。

**「裁頂」部分嘅查證：** 逐層追盒鏈（#app 行 59：height:100dvh、overflow:hidden、position:relative → .mask 行 4304 區：position:absolute inset:0 → .modal → #modal-inner 行 1642 → .story-play 行 2268／3953 → .sp-head 行 3963）：祖先鏈冇 transform/filter（v20a41 NOTES 已核實，今輪複核 grep 冇新增）；.sp-head 冇 overflow/max-height/line-clamp；h3 冇負 margin、冇細過字體嘅 line-height（1.4）。以本機 headless Chromium（Playwright 156）載真 `<style>` 全文＋真模板 DOM 嘅 harness 截圖（修復前）複現：**標題字形完整、冇幾何裁切**，但係深海軍藍色、meta/progress 深啡低對比——同實機描述（深色字、冇底色）一致。實機所見「字頂平切」最合理嘅解釋係深色字頂部幼筆劃喺深色漸變/雜亂場景上溶咗，視覺上似被削平；無論如何，加大頂距緩衝＋淺色＋加厚底漸變三樣都已落，截圖覆核字頂完整兼有真緩衝。

## 修法（只改 v20a41 皮膚段內 .sp-head 四條規則，逐行 diff 只有 21 行）

1. **三條 color 加 `!important`**：h3 `#f8efdb !important`（本層特異度 (1,3,1) > 對方 (1,2,1)，同為 !important 時本層勝）；`.sp-meta`／`.sp-progress` `rgba(245,234,210,.92/.95) !important`（本層 (1,4,0) > 對方 (1,2,1)，勝）。作用域只限 `#mask.story-play-on` 內嘅 .sp-head，其他 modal 嘅深色排版（結算卡等米紙底深色字）完全唔受影響。
2. **漸變加深加厚**：`rgba(10,6,3,.84) 0% → .6 52% → .34 78% → 0 100%`——progress 行（head 底部）都有實底色，唔再跌落全透明區。
3. **頂距 12px → 18px**（保留 `+ env(safe-area-inset-top)`）：字頂有真緩衝。
4. 段首註解已加 v20a46 根因更正，指向本 NOTES。

對話版面同選擇版面共用同一組 .sp-head 規則（選擇版標題係「… — 選擇」），兩邊一齊修好，harness 兩款都截圖核實。

## 自我驗證（harness，證據存 `linji-work46/harness/`)

方法：抽 index 全份真 `<style>`（165KB 原樣）＋按真模板（行 21506–21510）砌嘅 .sp-head/.sp-stage DOM＋事務所場景圖做底，Playwright Chromium headless 截圖；幾何兩款：桌面框 468×960（視窗 1280×1000）同手機 390×844，DSF 2。

- 修復前 `head_before.png`：標題深海軍藍、meta/progress 深啡低對比、setting 行淺色清晰——同實機症狀逐項吻合（亦證明 harness 有效）。
- 修復後 `head_after_desktop.png`／`head_after_mobile.png`：三行全部米白清晰、標題字頂完整＋上方有緩衝、漸變成條托住成個 head。
- 選擇版 `head_after_choices.png`：標題連「— 選擇」完整、meta/setting 可讀。
- harness 入面企立圖係未去背原圖（白色長方形）——係 harness 素材代替品，同 head 無關，唔係遊戲缺陷（遊戲用 UI40_STAND 去背圖）。

## 驗證結果（工作副本 ~/workspace/linji-work46）

- repo tests：全套 32 檔（17 node 邏輯＋15 python 靜態，連 flow45）**全 PASS**。
- `node --check`：全檔 2 個 script 段逐個驗，syntax OK。
- 逐行 diff（vs v20a45）：只有 v20a41 皮膚段 .sp-head 註解＋4 條規則，共 21 行；模板／JS／素材／LOCS 零改動；大括號平衡（改版前後 style 段規則數不變）。
- 紅線 grep：`starVolunteer_map_v19w` 在位（10 處）；`softRev=s107` 在位；`"v20a10"` 在位（7 處）。
- 檔大小：4,199,207 → **4,200,089 bytes**（+882，主要是根因註解文字）。

## 已知限制

- 本機 harness 用 Playwright Chromium 156 渲染；實機（用戶手機/iOS app webview）字體度量或有輕微差異，但今次修復係 cascade 層面（顏色邊條生效）＋底色＋緩衝，唔依賴像素級度量，部署後仍建議主代理照慣例做一次實機覆驗。
- 通用規則行 1755／1759 本身唔郁：佢哋係其他米紙 modal 嘅對比保底（v17 年代），全域改佢哋風險大；今次以作用域 !important 在 StoryPlay 頭條局部勝出，係最小改動。
