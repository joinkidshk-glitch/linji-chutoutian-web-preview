# v404 修復筆記（第十一輪報告頭五項＋掣量裁決）

Base：main `ce3b547`（v403）。唔改 SAVE key／softRev／產品 `?v=`。

## 1. 地圖回圖標籤避碰
- 根因：`deCollideLabels363` 喺 toggle 高亮 class（`mn68-here` font-weight 800 等）之後，
  pair pass 用 toggle 前量嘅 rect 計位；回圖嗰陣高亮籤展開遮鄰籤。
- 修法：先套最終高亮尺寸（here／tip／dim）→ 強制 reflow → 先量 rect；收尾加可見帶感知
  pair pass（推落出帶就推上面嗰張上）＋迭代 pair→clamp→障礙推撞；最後橫向分離收尾
  （障礙推撞推完再撞鄰籤嗰陣橫移，唔俾 clamp 夾返）。v403 靜態錨點（`map403AnchorFor`）唔郁。
- 實駕（讀檔路徑，播種 1990-01-11／聲望 19／信用 22／$955／壓力 46）：
  390×844 片場入場前 0 對、約會 0 對、入何生事務所返出嚟 0 對；
  430×707 三態全 0 對（證據 `linji-drive404/drive404d.json`）。

## 2. 折位殘留
- 頒獎：`awd403FoldAndHint` 改逐行量度（Range 行盒），折位收喺完整一行之後；
  `np214ShowPage` 切頁後重新對齊（第二版之前從未對齊，切一行 23px）。
  實駕：第一版／第二版 foldCut 均 []。
- 通告詳情：`notice_sheet_body` 底預留 56px＋安全區，尾行完整露出（實駕捲到底 lastGap 404.9px，scrollH 892）。

## 3. 里程碑首屏
- 結局總結：收緊段距（組距 8→4、紙頂距、段落距，唔縮字）；實駕尾段 hiddenBelow −50px（首屏完整）。
- 人情債：過期提示改佔位便條（`.debt-overdue404`，債卡之前佔版面位）；「去還」掣 44px 捲到底完整（lastGap 139.3px）。

## 4. 刪走「開始今日行程？」確認閘（用戶 2026-11-25 拍板）
- `presentStartScheduleConfirm45` 成個刪走，`confirmStartSchedule` 旗標四處呼叫一併刪；
  `presentRestSleepDayEnd` 執行掣直接行 `goSchedule`。
- 掣名講明後果：休息日「休息並過日」、自動行程「執行今日行程」、拍攝「開始拍攝」、工作「開始工作」
  （`dayEndContinueButtons`＋地圖開始掣＋行程頁狀態掣一致改名）。
- 測試同步（唔靜默拆）：`test_dayend202_static` N1 改斷言閘已刪＋掣名；
  `test_dayend202_logic`／`test_dayflow196_logic` 改直接執行斷言；
  `test_dayend189_*`／`test_dayflow196_static`／`test_book70_static` 掣名同步；
  `test_flow45_static`／`test_flow45_logic`／`test_v392_ui_static`／`test_v397_static`
  改斷言閘已刪＋新掣名；`test_v398_static` scene 計數 11→10（確認函數已刪）。
- 實駕連續休息日：撳「休息並過日」dayIndex 12→13（只過一日），下一張卡
  「休息（週六）」日期行「結算：1月13日（六）· 下一日：1月14日（日）行程」，冇確認 modal。

## 5. 通告欄最後一里
- 推介卡：場景底＋阿偉人物合成劇照（`gt-still404-fig`，唔出成品海報／主演名）；
  片酬獨立大字行（`.gt-pay404`「總片酬 $378」首屏可見，17 張板實駕確認）。
- 整理選單：索引紙籤（左紅邊＋選中紅筆「✓」）。
- 紅印：印章圖檔墨色加深（R×0.58／G,B×0.26）＋輕 filter；像素實量最深 7.38:1、
  強墨中位（R−G>50）4.86:1（≥4.5:1）。

## 6. 掣量裁決
- 24_menu 6→3（☰＋返回／設定／存檔管理；存檔管理共用槽位清單＋新遊戲；重看教學入設定）。
- 地圖刪「進度」掣（改靜態徽章；手帳行程頁頂部直接顯示主線進度行）：
  地圖 baseline 23→21。
- 茶餐廳：三個指定打聽合成「向霞姐打聽」點菜紙（$15 飲茶八卦／執漏獨立）；
  「未開放」展開掣真刪，改靜態標題＋直接列出。
- 08_tv：面板首屏五掣（播劇情／通告欄／報名／歇陣／返回）維持；報名後原位換訓練 CTA
  （`enrolledCourseCta` 現行行為，唔並排）；地圖 chrome 因刪進度掣同步 −1。
- 逐屏數掣：地圖 23→21、選單 6→4（含 ☰ 本身；選單項目 5→3）、茶餐廳面板打聽 3 掣→1 張點菜紙（3 行）。

- 茶餐廳覆驗（drive404g）：點菜紙內恰好三題（打聽電視城規矩／打聽高俊傑搶鏡事／
  打聽曉晴近況），$15「大堂飲茶聽八卦」同「幫手執漏」喺紙外獨立。
- 掣量相關測試同步：`test_menu72_static`（選單新清單）、`test_hub77_static`／
  `test_ui128a1_static`／`test_ui108_static`／`test_terms57_static`（chip 靜態徽章）、
  `test_s30dedup117_static`（片酬獨立行）、`test_tang169_static`（早退條件加 cafeSlip404）、
  `test_weave47_static`（債頁組成加 overdueNote404）。
- 行數釘 resync：`qa404/resync404.py`（difflib 映射，index.html 51896→52085，淨 +189）。

## 驗收證據
`~/workspace/linji-drive404/`（drive404d/e/f/g.json＋截圖＋紅印裁切）。
