# v409 UI 第十四輪修復

## S1 資料卡對比（校正閘嚴重項，已修）
- 根因：`.stat .l/.v` 用 `var(--cream)` 淺色字，資料卡紙底 #fbf4dd 上對比 1.08:1；帳本頁有深色覆寫，資料卡頁漏咗。
- 修法：`#home-pane-stats389 .stats-grid .stat .l{color:#6b4e2e}`、`.v{color:#1A1410}`（同帳本頁一致）。
- 實測：標籤 6.93:1、數字 16.58:1（~/workspace/linji-drive409/drive409_s1.json），零 page error。
- 合理性判斷：玩家即刻讀得返七圍數值，畫面維持紙卡手寫感，零副作用。合理。

## S2 地點面板底部透明（用戶實機新捉，校正閘嚴重項，已修）
- 根因：v391「頁角吊牌」將 `#app #loc-sheet.sheet .btnrow` 設 `background:transparent`，場景透出、返回掣浮喺場景上面。
- 修法：btnrow 回復紙底 #F2EBD8＋虛線頂邊＋安全區底 padding，面板延伸到底。
- 實測：sheetBottom=844=視口高、rowBg rgb(242,235,216)、零 page error（~/workspace/linji-drive409/drive409_s2.json）。
- 合理性判斷：面板成塊紙貼底，返回掣喺面板內，唔再有透明截口。合理。

## 第十四輪頭五項（GPT 方案 ~/workspace/linji-drive409/gpt_plan409.md）
1. 旁白底欄對比：g 掣改 #33241C／#F7EEDF、note 改 #F3E8D5 實色、詳情 ✓ 改 #14532D。實測（drive409_verify2.json）：「跳至選項」12.94:1、「劇情進行中」15.53:1、✓ 8.28:1。合理：只加深墨色，玩家讀字變易，主掣層級不變。
2. 彈窗報表感：modal 卡拆浮影改 1px #CDBFA9 細線、資料卡統計改底線短欄、刪重複「幕前聲望」行（格內已有聲望，實測聲望提及 1 次、業內信用保留、卡陰影 none）。合理：資料齊全只刪同義重複，紙面分組仍清楚。
3. 進度抽屜：刪外層重複「主線進度」標題（實測標題數 1）、已完成幕摺疊「已完成 5 幕 ✓」紙條（預設收合、可展開查原資料）、第 6 幕兩線首屏主焦、捲動底 padding 28px。合理：完成紀錄無消失，一撳可查。
4. 行程頁：建議／成本移週格前（實測 suggestBeforeDays=true）、進度掣書籤化（高 44）、格距／內距收窄＋fold 改收格高優先。實測 390×844：第二排底 712 ≤ 手帳底 715、第三排頂 721，折位落完整兩排之間，margin 只剩 16.6px。合理：兩排日卡完整入鏡，字號不縮。
5. 約會場景：拆深藍套框改紙底場記紙條（stageBg rgb(247,238,223)）、天台圖 170px 主景、肖像貼相 90px、兩回應同寬同色（167×72 兩粒一致）取消金底預設。合理：選項無正解暗示，對白字清晰。
- 證據：~/workspace/linji-drive409/drive409_verify.json、drive409_verify2.json、drive409_date.json、v409-*.png。零 page error。
