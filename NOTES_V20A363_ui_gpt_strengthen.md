# v363 NOTES — UI 加強：GPT-6.2-sol 方案＋方向二「紙本手帳 · 實物劇組」全面整合

## 背景
用戶睇完 v362（四屏可用性修復）話效果不好，要求 UI 改動要 GPT 幫手加強。
本票先經 88api2 中轉分屏諮詢 GPT-6.2-sol（五次：主畫面／手帳／故事／結算／共通動畫，
原稿存 `~/workspace/linji-drive363/gpt_ui_strengthen.md`），再按方案實裝。
只做 UI，唔改平衡數值；唔改 SAVE key／softRev／產品 `?v=`；年份 source 冇手改。

## 改動（index.html 淨 +437 行：CSS +332、JS +105）
- **共通**：動畫 tokens（`--m-paper363`／`--m-settle363`／`--m-hit363`／`--m-tear363` easing）、
  keyframes（stampHit363／settle363／floatUp363／pageIn363）、`.view.on` 入頁動畫、
  `prefers-reduced-motion` 停新動畫。真資產入 `assets/ui363/`（paper 紙紋、像素貼紙 7 張）。
- **主畫面**：成頁開工簿——紙面底＋裝訂孔、帳本式頁眉（阿偉＋級數印＋銀包＋撕頁日曆
  `paintPageHead363()` 讀 `dateObj()`／`calendarSeason()`／`enc79PlayerTier()`）、
  紙標籤地點名（`.mn68` 改紙籤＋`deCollideLabels363()` 縱向避撞，熱區座標唔郁）、
  像素人「我喺呢度」位置指示（`mapMe363()`，讀 `drawMap._pinPos`／`atLoc`）、
  今日像素貼紙（`todaySticker363()`，由 `nbStickerKind362(todayPlanId())` 映射）、
  票根「過一日」掣、層切換掣兩行（`map159LayerBtnHtml()` 改兩 span，保留 `id="map-layer159"`）、
  toast 跟新頁眉高度落位（top 98px，唔遮帳本第二行）。
  釘維持隱形熱區（v20a43 用戶決定），GPT 方案嘅圖釘唔採用。
- **手帳**：索引紙舌分頁、日列 grid（42px 日期／活動／52px 貼紙位，`grid-row:1` 防錯行）、
  貼紙 44px 白邊、`#plan-teach105` 改邊註樣式（元素保留，test_text108／test_ui105 斷言）、
  壓力刻度（`stressScale363(pv)`，`updateLiveStressStrip()` 掛鈎，start／end 點＋peak 標）。
  確定蓋章沿用 v20a197 鎖定態印章（`stampIn362`），唔另加元素。
- **故事**：撕邊便條 plate、旁白白條／對白分工、場記籤（`.sp-head` 票根籤）、
  進度紙角（`.sp-prog362`）、選項紙；modal 註腳加深（`#mask .modal-note202`）。
  對白字級維持 1.12rem/1.5（v20a154 plate 170px 固定高，唔再加大）。
- **結算**：票根憑據（ticket_stub 圖推走撕線＋CSS dashed 左邊）、雙軌兩欄 1.9rem 大數、
  完成印延遲 .42s 落印；「關閉」掣保留全寬 52px（唔改名，drive 腳本靠標籤撳掣）。

## 驗證
- 實駕（Playwright 390×844，`~/workspace/linji-drive363/`）：全流程行通
  （晨鏈→手帳→故事→抉擇→結算→地圖→過一日）；量度：HUD 字體維持 12.48/15.68px、
  細目標 0（過一日 340×55、層掣 77×46、☰／進度 chip 44×44）、地點標籤 17 個零重疊、
  日曆／級數印／像素人／壓力刻度齊、故事跳至選項 1 步。
- Suite：**400 PASS／9 FAIL**，同 v362 基線完全一致（九項 pre-existing：
  flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。
- 行號釘 resync（`qa363/resync363.py`，difflib 對位＋內容逐字核實）：gift185／rom159／
  rom176／tang152／tang171／tang173／text125／travel114 八檔重釘，逐檔覆驗 PASS。

## 備註
- 今日貼紙只喺拍攝／試鏡／訓練／休息日出現（「到處逛逛」冇貼紙，屬設計）。
- 壓力刻度喺數值低嗰陣點位集中左邊，係真實數值反映，唔係 bug。
