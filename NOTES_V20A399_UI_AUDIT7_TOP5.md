# NOTES_V20A399_UI_AUDIT7_TOP5

第七輪 UI 檢視（`~/workspace/linji-ui-audit-2026-11-24f/REPORT.md`：GPT A 0／B 4／C 169，
Gemini A 0／B 167／C 6，173 張截圖）頭五項修復（REPORT.md §四，只做 GPT 頭五，唔擴大範圍）。
基線 v398（main `070eae7`，suite 421／9）。實駕證據 `~/workspace/linji-drive399/`
（`drive399.py`，五個 probe：settings／audition／tut／awards／board）。

## 修復一覽

### 1. 設定深啡條對比度 9 項 fail（UI399-1）
- `.settings-row` 由深啡底 `var(--panel2)`（#4a433c）配近黑字，改淺紙底 `#fbf4dd` 配深墨字
  `#1a1410`，hint 改 `#5c4a1f`；已選速度 pill「快」由 cream on gold（3.03）改深底白字
  `#fff8e8 on #5c4a1f`。
- 實駕量度（`settings399.json`，CONTRAST_JS 同 f 輪同一口徑）：14 項 **0 fail**（之前 9 fail）；
  最低 7.78（副文／速度掣），「快」8.09，lab 16.58。截圖 `settings399.png` 睇圖確認全部可讀。

### 2. 43b／43c 黑背底 bottom-sheet（UI399-2）
- `doAudition` 試鏡等消息卡加 `keepScene397:true`（`modal()` 掛 `scene398`＋`dayres-scene397`，
  同休息／訓練／病倒卡同一套 v396 日結漸變 dim 頂 .10／底 .42）；標題由「試鏡完畢」改
  「試鏡完畢・等消息」，唔再令人誤解為已出結果。流程（掣「繼續」＋`cont` 路）一字唔郁。
- 實駕量度（`audition399.json`）：maskCls `mask on scene398`，maskBg 同休息／訓練卡同一條漸變，
  `vmapVisible true`（mapImg 384×576），h3「試鏡完畢・等消息 《冬日鄰里情》鄰里配角」。
  截圖 `audition399_43b.png`：地圖清晰可見，唔再上半純黑。
- 唔郁：手帳排程試鏡日嘅日結標題 `試鏡完畢：${gig.title}`（resolvePlannedDay 入面，日結卡本身
  已經係 scene 模式，內文有「等消息」句）——嗰個唔係 43b／43c 卡，留待下一批先一併改名。

### 3. 教學聚光燈圈埋鄰居（UI399-3）
- `refreshTutSpotlight398()` 定位金圈之後調 `updateTutLabels399()`：逐張 `.mn68` 同金圈 rect
  求交集，撞圈嘅非目標標籤加 `.tut-label-hide399`（visibility 隱藏）；目標「星河電視台」
  原標籤同樣隱藏，改由 `#app` 直屬浮貼 `#tut-target-label399`（z 521）喺遮罩上層顯示，
  上移 12px 同圈頂留空。金圈繼續跟 pin 中心（59.3, 252.9, 64×64），唔靠移偏避字。
  離開 step 1（`!on` 分支／`clearTutSpotlight()`）即 `restoreTutLabels399()` 還原。
- 點解要浮貼：`.map-well`（z-index 1）困住標籤層，標籤本身升 z-index 逃唔出遮罩（z 50）；
  浮貼係唯一唔郁地圖結構嘅做法。
- **補丁（實駕捉到）**：第一版浮貼上移 8px＋無 line-height，浮貼高 21px、底掂圈頂 −1.4px；
  加 `line-height:1.2`（同原標籤一致，高 18px）＋上移 12px，圈頂空隙 **+5.1px**。
- 實駕量度（`tut399.json`）：step 1 撞圈兩張（星河電視台 64×6.5、金龍茶餐廳 46.9×32.1）
  全部隱藏，浮貼 (53.7, 229.8, 77×18) display block、zIndex 521；step 2 隱藏 0、浮貼收起。
  截圖 `tut399_step1.png` 睇圖確認：圈內只得電視台大樓，「星河電視台」紙籤光亮喺圈頂，
  金龍茶餐廳標籤唔見咗。

### 4. 35c 右欄直排淡出截半行（UI399-4）
- `renderAwardResultHtml` 右欄 `sidebar214` 只留 outlet＋行首 6 字（共 13 字＋❦），
  唔再全文直排；全文仍喺第二版主欄（`${esc214(news.line)}</p>` 唔郁），唔失內容。
  晨報渲染器唔郁（`.np214-filler-v` 保留）。
- 實駕量度（`awards399.json`）：P1 右欄 p 底比 fade 起點低 **83.4px**（之前 +144.6，即伸出 fade 區
  144.6px，「大禮堂」三字橫跨 fade 起點 727），P2 低 102.3px；p 文「晚間娛樂快訊：街招年賞散場」。
  截圖 `awards399_p1.png`／`awards399_p2.png` 睇圖確認：右欄收尾＋❦ 喺 fade 區之上，無半截字。

### 5. 通告欄底部漸隱洗字＋頂部報表感（UI399-5）
- **底漸隱刪咗，唔係縮短**：量度第 6 張 chips 行 733–758 橫跨摺位 745，26px 漸隱（719 起）
  將成行洗到 46%→0% 不透明；縮到 8px 仍洗走字下半（字高 ~12px，fade 起點 737 蓋住字身）。
  摺位乾切係正常捲動行為，底墊 26px 已保捲到底最後一張完整。`#mask.board-tall392 #modal-inner`
  規則刪除，`test_v398_static.py` 兩條相關斷言按先例更新（v398 更新 v397 嗰陣同一做法）。
- 統計列改剪報標籤：虛線裁邊＋米紙漸變底＋微斜 −1deg＋紙影，同一句唔改數。
  「整理」縮成側邊紙籤：靠右自動闊（53.8px，之前 338px 全寬），選單展開嗰陣 200px 靠右掛喺籤下，
  6 個選項齊全（預期日薪／總片酬／成功率／全部／電視劇／綜藝）。展開嗰陣掣本身會撐闊做選單頂欄，
  係下拉掣正常形態。
- 附帶小修（圖釘掂標題）：卡頂圖釘 `::before` 由 `top:5px` 改 `top:-4px`（半出卡頂，釘住紙邊），
  釘底同標題字頂留 **+6px**（之前 −3px）。唔郁標題——標題下移會逐張墊高卡身，第 6 張跌出摺位
  （第一版 margin-top:8px 實測：第 6 張頂由 697 跌到 739，chips 行完全睇唔到，已 revert）。
- 實駕量度（`board399.json`）：fadeLen null，第 6 張 chips 行 735.2–760.2（摺位 745 之上部分
  全不透明），pinWorst「冬日鄰里情推介」clearance +6。截圖 `board399_peak.png` 睇圖確認：
  第 6 張「一屋人」chips 行（電視劇／可接通告）實色可讀，唔再淡白；`board399_organize.png`
  選單 200px 靠右，6 項齊全。

## 測試
- 新增 `tests/test_v399_static.py`：20 項，全部 PASS（五項斷言＋WCAG 對比度實算：
  lab #1a1410／hint #5c4a1f on #fbf4dd、on 態 #fff8e8 on #5c4a1f 全部 ≥4.5:1）。
- `tests/test_v398_static.py`：38/38 PASS（三處按先例更新：底漸隱規則刪除、統計列虛線邊、
  `keepScene397:true` 計數 10→11——試鏡卡加入 scene 家族）。
- **resync（`qa399/resync399.py`，照 v398 先例如常）**：`index.html` 淨 +72 行（51111→51183），
  10 個行號釘測試要跟住漂移，全部按 difflib 映射重寫、內容逐字核實純漂移：travel114
  FREE 42＋COUNT 13＋DEF 45945→45973＋WRAPPER 32074→32098；rom159 6 釘＋全佳行 28230→28254；
  rom176 6 釘；tang152 兩釘；text125 三錨點；tang171／tang173 DEF 45945→45973＋總行數
  51111→51183；tang173 lines[5361]→[5382]（8 處）；gift185 總行數 51111→51183。
  另兩處有意圖行為改動：ui128a6 已選速度 pill 金底 #c97f1f→深啡底 #5c4a1f（對比度修復本身）；
  設定頁註解「即將推出 1.35」令 `html.count('即將推出')` 變 2，改寫做「未推出行 1.35」，
  測試（ui105）唔郁。resync 後 10 檔逐個直跑全部 PASS。
- 全套 suite：**422 PASS／9 FAIL**（基線 421／9＋新測試檔 test_v399_static.py 1 項；9 個 FAIL
  全部係 pre-existing，同基線同一批：flash51、slot50、soft_tip_111_restore、start53、
  weave43、weave44、weave49、wf5_87、wrap38——逐檔喺 pristine v398 對照過，本身已 fail）。
  第一輪 suite 曾出 412／19，原因係 index.html +72 行令 10 個行號釘測試漂移（未 resync），
  resync 後重跑回復 422／9。

## 唔做（下一批）
- 21_debt 文字重疊＋掣截半、33 結局總結、11c、88 資料卡、08b 紅字 4.21、病倒卡綠字 4.42、
  掣量背景卸載八項（tut step2／tut_01 收 pin、35b 卸載地圖層等）。全部唔喺呢票。

## 唔郁嘅嘢
- SAVE key（`starVolunteer_map_v19w`）／softRev（s107）／產品 `?v=`（v=20a10）唔郁（v398 測試釘死，suite 驗）。
- 靜態 `<button` 總數 111 唔變。
