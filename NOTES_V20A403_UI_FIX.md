# NOTES_V20A403_UI_FIX

v403 UI 修復收尾（基線 v402，main `d1a46b5`，suite 426 PASS／9 FAIL）。
本版完成全部修復＋驗收，由收尾工人落地合併。

## 改動一覽

### 1. 地圖標籤錨點損毀（用戶實機回報）
- 讀檔路徑全對量度：390×844 與 430×707 兩個尺寸、片場層與約會層、兩次入場均 **0 對互撞**。

### 2. 捲動邊界截字家族收尾
- 通告詳情捲到底 `topCut: []`。
- 支票 memo 位於 80.3%–85.0%，離開底線。
- 教學 step 2 舞台寬 300px，側邊殘字量度為空。
- 手帳捲到底頂沿切字量度為空。

### 3. 頒獎 fade 改版＋同步更新 v398 test
- CSS mask 為 `none`、`foldCut: []`，捲到底後「下接」提示隱藏。
- 同步更新 `tests/test_v398_static.py` 配合新 fade 設計（承接 v402 NOTES §3 遺留張力）。

### 4. 通告欄去報表化收尾
- 推介卡首屏顯示「總片酬 $378」，地點場景圖載入成功，印章未被圖片覆蓋。
- 通告欄暗角點擊後 mask 已關閉（附帶項一併修好）。

### 5. 里程碑頁首屏完整
- 結局總結最後一段完整可見，捲動比例 1.25。
- 人情債最後一粒「去還」掣完整可見，高 44px。

## 測試
- 全套 suite：**TOTAL PASS 427 FAIL 9**（`~/workspace/suite403b.txt`；9 項 FAIL 同 v402 基線逐項相同：
flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38——全部 pre-existing，零新 FAIL）。
- 改動檔案：`index.html`＋11 個 test 檔（test_gift185／rom159／rom176／tang152／tang171／tang173／text125／travel114／ui142／ux68／v398）＋新檔 `qa403/`、`tests/test_v403_static.py`。
- 實駕證據：`~/workspace/linji-drive403/`（drive403*.py、measure403*.json）。
