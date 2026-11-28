# v423 UI 第二十五輪修復（NOTES_V20A423_UI25）

基線 v422 `0ae3bd2`（Pages byte-identical 已核實，SHA-256 `3d3dbd2a17ba9e6bdb495d67c69ad2f76bafd7cad9e7da2004c28b28ec3e7d2f`）。
範圍：只改 UI／呈現層同文案連貫；玩法、數值、結局條件、SAVE key `starVolunteer_map_v19w`、softRev、產品 `?v=`、頒獎贏線 0.875 全部不變。

## 第二十四輪餘下 C×2

- **`11_suggest_cost_row`**：主因擷取假象（舊擷取未入編輯態）；真瑕疵兩項已修——「本週外出機會剩 N 日」由第一個外出格移去週標題日期行（`nbMapTotal400`／`nbRangeWithTotal400`，計數邏輯不變）；建議掣 `min-height` 36→44px。真路徑重擷取（週一結算入編輯態）影到成本行「失去一日外出機會；得到演技 +1 堂（再 4 堂升二級）· 學費 $20 · 壓力 +10」。`test_v400_logic` 5C／5C2、`test_v400_static` ⑤ 同步。
- **`37b_encounter_choice_hiu`**：真問題已修——`spResolveBgKey` 加 `storyNodeLocId` 後備（31 個 R_ 節點背景一併接上實景相）；抉擇屏加瘦身語境行 `.sp-choice-ctx423`（標題＋場景，唔出 meta／進度，守 v128 原意）。重截見廠景休息角實景＋「廠景休息角初遇 · 廠景休息角」語境行。

## v419 試玩轉交 UI 八項

1. **剪報 modal 後手帳卡死（真問題，間歇競態）**：`presentDueMorningPaper` done() 加 once-guard；晨鏈收尾 self-heal（mask 已關強制 `setUnderlyingInert(false)`，`S.homeEditable` 真且手帳顯示中重繪可編輯手帳）。真玩重演週界結算：回家結算→收下剪報→手帳可編輯、確定掣可撳、零 inert。
2. **頒獎揭曉層次（harness 假象為主）**：典禮 mount 時底層 view／地點面板入 inert，cleanup 一致還原（層次衛生）。
3. **idle-break（歸因假象＋真弱點）**：同地第二段開放劇情出第二張卡（探針：tvb_longmen 雙卡「廠景休息角初遇」＋「週刊小訪」）。
4. **「約人出街」卡被底部截（真問題，輕微）**：`#loc-acts` padding-bottom 22→34px、scroll-padding 24→36px、淡出 10→18px；捲到底量度尾卡完整可見。
5. **已定行程 pin 失效（harness 假象）**：遊戲側不改；手動路徑（返回地圖→pin）一直通。
6. **約會／送禮 ±0 落差**：v422 已修結果解釋；本輪補花費前警告——約會選人 hint 同選地點頁在 capped 時先講明「關係已達目前劇情階段上限，本次約會不會再增加好感」。
7. **同日迴圈 reload（harness 假象）**：不改。
8. **手帳頂部擠迫（真問題，輕微）**：≤430px 收窄 plan 組 gap／左 padding、進度徽章可縮省略、紅圈 inset 收窄；390 量度標籤全在紙邊內、觸控 ≥44px。
9. **缺立繪後備（真問題）**：`ENC423_NO_ART` 登記四星（沈映雪／江詩盈／胡美琳／韓秀婷）——巧遇直接用藝員資料卡並上移至對話框之上完整可見；在場頭像用中性剪影；人物頁縮圖鏈只留剪影＋SVG。實駕巧遇 `era_stars` 零 404、無破圖。補圖屬美術票另開。

## v422 新增呈現面覆核

感情 crisis／commit 線索（mapTips 斷言 ad_adm=R_choi_crisis、cafe_cha=CMT_choi_commit；人脈「下一步」兩態齊）、何生信任三態、武師班 3/5 堂、負標籤 pane、E1 進度行已入盤點截圖。引薦詳情「14 日內」改出實際到期日期（與補位／試鏡帶口徑一致）。

## 測試

- Suite：422 PASS／17 FAIL（未 resync 前）→ resync 後 8 項行號釘修復（`qa423/resync423.py`，difflib 映射，index.html 淨 +113 行 53420→53533）；最終數字見出貨回報。
- 相關測試逐個覆驗：v400 logic/static、ui128a3、story191、enc105、gift185、rom159、rom176、tang152/171/173、text125、travel114 全過。
- 截圖：197 張（全屏 192／裁切 5）；第十八輪 388 映射 direct 196／state-equivalent 136／md5-alias 44／manual-equivalent 12，missing 0。像素旗標 0。
