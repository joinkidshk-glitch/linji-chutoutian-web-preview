# v411 第十五輪 UI 修復（第一階段：S1 進度抽屜折位）

基線：main `860cc38`（v410）。本票分階段：第一階段只修第十五輪校正嚴重項 S1，修好重截後停低回報；頭五項修復（第二階段）喺同一工作副本 `linji-work411`、分支 `v411-ui15` 繼續。

## S1. 進度抽屜落點折位切字

- 證據（CALIBRATION.md S1）：390×844 進度抽屜 scrollTop=0 落點，捲動區 fold=733.0px，文字行「○ 時窗：1991 年春」top 726.1／bottom 744.1 跨 fold 被切，落點見半行字。
- 根源：抽屜捲動器係內層 `#progress-list`（max-height 62vh），而 v408 折位家族 `fold408Align`／`align403ScrollEdges` 只套咗外層 `#modal-inner` 同 `.notice_sheet_body`；外層內容唔溢出即早退，內層從未對齊。v409 抽屜改版（完成幕摺疊紙條＋底 padding 28px）改變內容高度後，fold 落入卡內文字行。
- 修法（只改 index.html，唔縮字、唔刪內容、唔隱藏內容）：
  1. modal 嘅 `_al403` 對齊排程納入 `#progress-list`（fold408Align＋align403ScrollEdges，rAF＋250／700／1200／2000ms＋fonts.ready 重跑，同其他捲動器同一節奏）。
  2. `fold408Align` 嘅 block 選擇補進度卡口徑：卡頂行（`.prog71-top` 內）被切嗰陣推成張 `.prog71-row`，折位落卡與卡之間；完成紙條 summary 被切推成條 `.prog409-done`；其餘維持行級推（li／p），折位落行與行之間（推成張卡會連上一行一齊推落去再切上一行）。
  3. `openProgressDrawer389` 喺完成紙條 toggle 後重跑對齊（只喺 scrollTop≤2 嗰陣推折位，捲走咗唔郁玩家位置；底邊對齊照跑）。
- 量度（Playwright 實駕，校正同一播種狀態：N1–N5 完成、已完成 5 幕紙條；FOLD 口徑同 probe409n）：
  - 390×844：fold=733.0、clientH=523，cutBottom／cutTop 空；fold 上最後一行「○ 到第 61 週」bottom 726.2，fold 下第一行「○ 時窗：1991 年春」top 736.0，fold 落行間（推幅 9.9px）。
  - 430×707：fold=597.9、clientH=438，切字空；上行 bottom 581.1、下行 top 600.9。
  - 430×932：fold=821.0、clientH=578，切字空；上行 bottom 811.4、下行 top 823.4。
  - 展開完成紙條後三視口切字仍空；捲到底三視口 cutTop／cutBottom 空、最後一行完整可見；關閉掣可達（hit-test 中、三視口撳關閉後 mask 熄）。
- 玩家視角判斷（合理）：落點最後一行完整、卡身喺抽屜底邊自然延續落去，玩家一眼知下面仲有內容可捲，唔再見半截字形；推幅最多約 20px（行距微增），畫面唔覺異樣，冇大片空白；捲動、展開紙條、關閉操作不變，冇副作用。副作用只有被推嗰行上方行距略闊，屬正常排版呼吸位。
- 相關測試逐個直接跑全過：test_progress71_static、test_progress71_logic、test_prog175_static、test_v403_static、test_story198_static／logic、test_story191_logic、test_hub77_static、test_v400_static／logic、test_v401_static／logic。
- 唔郁：SAVE key、softRev、?v=、source 年份、抽屜文案同幕次序。

## 第二階段：頭五項必修（GPT-6.2-sol 加強方案，2026-11-26）

方案經 88API 第二條 key 分兩段取得（第 1–3 項／第 4–5 項），brief 寫明終極目標原生 iOS app 上架＋六項檢視標準；方案落到 CSS 數值（紙色 #F6EBD6／線色 #CDBFA9／印色 #823F35／下一幕底 #EDDFC2、44pt 命中、折位落行間），實裝只加 v411 覆寫層（`/* v20a411 UI411 */`，喺 v409 塊之後），唔改 DOM 結構、唔改邏輯。

1. **彈窗／資料卡報表感**：合約卡逐行虛線拆除（row border-bottom 0px），末行改 1px 細線分組＋字級提升作便箋抬頭；算式 `.board-calc397` 退註腳（12px、#5C4D3D）；`.cn-kv` 行距 1.45、值字重 700；資料卡逐行分隔線拆除（border-bottom 0）；詳情彈窗主掣 flex 1.4／次掣 1（實量 191px／143px、高 52px）。判斷（合理）：合約一眼先見金額、算式退後唔搶焦，資訊量不變；掣層級分明但兩掣都 ≥44pt 好撳。
2. **行程頁首屏密度**：頁首 padding-top 2px、日期 margin-bottom 2px、日格 min-height 88px（≤740 高 80px）、gap 4px；進度徽章加 2px 印色左邊作書籤角（實量 2px）。實量日格 top 93.7、首屏完整入鏡、無切字（建議／成本列喺此播種態 hidden，屬無建議狀態，非入鏡失敗）。判斷（合理）：日期下留白收窄後週格上移，排程操作不變，冇為密度犧牲可讀性。
3. **進度抽屜層級**：四卡改一張通告紙（row border-top 1px、radius 0px、背景透明）；下一幕 `.open` 底 #EDDFC2＋2px 左邊＋標題 1rem；狀態膠囊改印章（radius 2px）；完成紙條收薄（padding-top 0）。實量 cutBottom 空、關閉掣高 48px hit-test 中。判斷（合理）：幕次以幼線分隔似手帳紙，下一幕底色突出，完成紙條唔再搶焦；S1 折位對齊照常運作（cutBottom 空）。
4. **約會場景套框**：對白內框拆除（bubble border 0px、背景透明，正文直排紙上）；肖像改相片貼角（3px 紙邊＋1px 外框）；約會期間背景地圖標籤 visibility hidden；提示 margin-bottom 8px；雙掣 min-height 48px 同款同尺寸維持。判斷（合理）：場景少一重框似貼相紙頁，背景唔再搶焦；選項同權重不變。
5. **旁白正文對比覆量＋完成卡**：computed 定斷——旁白正文色 #484640 對紙底 #f7f1e6／#f5e7c6 對比 8.39:1／7.70:1，≥4.5:1，穩定態合格；像素法 1.94–2.09 屬打字動畫（charFade opacity 過渡）／取底環跨邊假陽性，唔改墨色。完成卡收細（max-width 38%、字 .75rem、padding 5px 10px），旁白舞台底 padding 4px、操作欄頂 padding 4px 收窄間距。判斷（合理）：正文即時可讀，唔為假陽性亂改色；完成卡唔再壓住標題區。

- 實駕：Playwright（capture_j rich_seed 520，390×844）重截 progress／schedule／detail，量度見上；PAGEERR 零。
- 唔郁：SAVE key、softRev、?v=、source 年份、文案與流程。
