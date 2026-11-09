# NOTES v20a47 — 新 UI 接入第三期：報紙實物化＋剪報／開始畫面／手帳收尾

基線：v20a46（線上 4,200,089 bytes）。本期只改呈現層，零內容邏輯改動、零新增內嵌素材。

## 改動清單（逐行 diff vs v20a46：145 行，當中只有 1 行係改寫，其餘全新增）

### JS 接駁（3 處，跟檔案既有 `casting-sheet-on` 情境 class 慣例）
1. `modal()`：新增一行 `maskEl.classList.toggle("paper-on", !!opts.paperSheet)`。
2. `closeModal()`：新增一行清除 `paper-on`（同 `casting-sheet-on` 並列），確保唔污染其他彈窗。
3. `presentDueMorningPaper`：`modal(...)` 嘅 opts 加 `paperSheet: true`——**該函數簽名、回傳語義（true=已呈現／false=冇到期報紙）、`done`/`onDismiss` 綁定一律原封不動**；按鈕「收下這份剪報」綁定冇改。
   - `renderMorningPaperHtml` 模板、`commitMorningPaper`、edition 機制、`newspaperCheck` 自檢涉及嘅字串一律冇掂。

### CSS 皮膚層（主 style 段尾新增一段 `v20a47`，約 140 行）
作用域 `#mask.paper-on` 內將 `.paper-sheet` 變實物報紙：
- **情境**：遮罩 `rgba(0,0,0,.72)` → `rgba(24,15,6,.48)`，背後地圖／場景透出；`.modal` 牌面透明化（背景／邊框／陰影全清），`#modal-btns` 列透明化——報紙本體做主角，掣浮喺紙下。
- **紙本體**：斜放 `rotate(-1.1deg)`；紙紋全 CSS（兩層 repeating-linear-gradient 纖維紋＋radial 漸變紙色）；第二張紙邊用兩層硬偏移 box-shadow（`5px 7px 0 -1px／0`）喺右下露出，另加雙層柔影＋內側暈影。**唔用 `::before`+負 z-index**：`.paper-sheet` 有 transform（stacking context），負 z 偽元素會畫喺紙面背景之上遮紙紋，次序陷阱已避開並註明喺 code。
- **報頭版式**：報名大字（1.45rem/900）置中、字距 .32em、頂 3px 粗線＋底 4px double 雙線；日期行置中＋幼線收尾；標題 1.5rem 置中、dek 置中；短訊欄頂 2px 粗線開欄，`@media (min-width:430px)` 行雙欄＋column-rule 欄線（窄屏單欄）；聲望行＋附註置中、幼線分隔。內容結構同原文案排序完全保留，文字續由 HTML 排。
- **剪報頁**（`.clip-card`，只用喺手帳 clippings 分頁＋結局卡）：同款紙紋／紙邊／投影，加頂部膠紙貼（`::before` 半透明米色＋虛線邊）＋奇偶卡交錯輕斜（∓0.55°），`margin-top` 畀膠紙留位；似黐喺剪報簿上面。
- **收尾統一**：開始畫面 `.start` 加紙紋底（覆寫舊 `var(--cream)` 純色）、`.start-brand` 加 drop-shadow；手帳 `.home-card` 換同款米紙面＋金啡邊＋`h3` 深金啡字。全部只換外觀，冇郁結構／佈局／DOM。

## 體積帳
- 4,200,089 → **4,205,962 bytes**（+5,873，全係 CSS/JS 文字；**新增內嵌圖像：0**）。
- 距 4.35MB 紀律線仲有約 144KB 餘量；報紙底圖（p1/system newspaper-base）冇採用——CSS 紙紋已達效果，唔使燒體積。

## 驗證
- `node --check`：全檔 2 個 script 段 syntax OK。
- **repo tests 全套 32/32 PASS**（17 node 邏輯＋15 python 靜態，含 newspaper 自檢路徑相關嘅 weave 系列）。
- 紅線 grep：SAVE key `starVolunteer_map_v19w` 10 處在位；`"v20a10"` 7 處在位；softRev 相關在位，同 v20a46 一致。
- CSS 大括號平衡（全 style 段＋v47 段均為 0 差）。

## Harness 截圖自查（證據存 `linji-work47/harness/`）
方法同 v20a46：抽 index 全份真 `<style>` 原樣＋按真模板（`renderMorningPaperHtml` 輸出結構／真 #mask>.modal>#modal-inner+#modal-btns 骨架／`renderClippingsPane` clip-card 結構）砌 DOM，Playwright Chromium headless 截圖（390×844 手機＋468×960 框，DSF 2）。Playwright 瀏覽器今次裝喺 `/home/hatch/pw-browsers`（/tmp 係 512MB tmpfs 裝唔落——v20a46 嗰次下載失敗嘅真因亦係 ENOSPC）。
- `paper_desktop.png`：報頭雙線、大標置中、雙欄短訊連欄線、聲望頁腳、背後場景透出、右邊露第二張紙邊、掣浮喺紙下——實物感成立。
- `paper_mobile.png`：單欄版式成立；內容高過 modal 上限嗰陣沿用既有 `#modal-inner` 捲動（同改版前行為一致，掣列保持可見）。
- `clippings_mobile.png`：膠紙貼＋交錯輕斜＋紙紋，剪報簿語言成立。
- `start_mobile.png`：紙紋底＋標題卡投影（harness 入面標題卡係色塊代替品，真遊戲用返 start_title_card.png 實圖）。

## 已知限制
- harness 標題（h3）顏色受檔案既有通用 modal 規則影響呈深藍墨色——喺紙面上對比充足、近報紙油墨色，未另行覆寫（避免再開 specificity 戰線）。
- 雙欄只喺 ≥430px 視窗寬觸發；真機框闊 468px 以內多數情境係單欄／臨界雙欄，兩者都已截圖核實可讀。
- 部署後仍建議主代理照慣例做一次實機覆驗（真 edition 內容長短不一，長版面靠 modal 捲動，已屬既有行為）。
