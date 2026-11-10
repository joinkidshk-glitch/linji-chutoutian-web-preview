# NOTES V20A74 — TARGET74 攞走主攻目標功能

用戶 2026-11-10 16:06 拍板：問「設 XX 為主攻目標有什麼用的」後，揀「攞走成個
主攻目標功能」。parent 查實嗰個功能（v68 年代嘅目標數值，prefs 鍵
`ux68TargetStat`，唔入存檔）全部效果只有三樣純導航嘢，冇數值／解鎖／劇情
效果，用戶決定成個攞走。

## 改動（只刪功能，唔掂課程／判定／數值）
- **刪掣**：選擇器（`train71PickerHtml`）入面「設「X」為主攻目標／✓ 已設為
  主攻目標」成段移除；數值 chips 上面嘅「目標」標記一併移除；
  `train71HandleClick` 嘅 `data-gtgt` handler 分支成段刪除。
- **刪預設邏輯**：`train71Stat()` 攞走目標分支——選擇器預設改用今個
  session 上次睇開嗰組（`ux68GuideStat`，UI 狀態變量保留），未揀過就開
  演技組。
- **刪標示**：`ux68ApplyTargetBadges` 成個函數刪除，`ux68OrganizeLocSheet`
  入面嘅呼叫一併移除；地點 sheet 選項唔再產生 `.ux68-tgt`「▲數值名」標。
  organizer 其餘行為（意圖分組／要事置頂／未開放摺疊）冇郁。
- **刪存取**：`ux68TargetStat`／`ux68SetTargetStat` 刪除；全檔 grep 證實
  冇其他地方讀寫 prefs 鍵 `ux68TargetStat`。玩家舊 prefs 留低嘅殘值冇
  程式再讀、自然失效，冇為清佢改 prefs／存檔結構。
- **CSS 清孤兒**：`.ux68-tgt`、`.guide68-chip .gt`、`.guide68-tgtrow`、
  `.guide68-tgtbtn` 規則成批移除。
- 玩家面文字清掃：全檔「主攻」字樣歸零（教學／說明／picker intro 本來
  冇提及呢個功能，唯一出處就係已刪嘅掣面文字）。

## 冇掂
- 課程數據／增益／解鎖判定；選擇器 v73 三分流行為（未開放隱藏、未報名
  一句純文字、已報名出卡）；地點 organizer 其餘行為；進度頁；`ux68GoLoc`
  本體（picker 以外用）。
- SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=v20a10`／
  content pack JSON。

## 測試
- 基線 79 檔全過＋新增 `tests/test_target74_static.py`＝80/80。
- 原位改版（註明 v74 用戶拍板原因）：`test_ux68_logic.js`（4）目標 prefs
  往返斷言→函數不存在斷言；`test_ux68_static.py` 兩條（存 prefs／▲ 標示
  →全清斷言）；`test_progress71_logic.js` P1（目標入口→冇掣）＋P3（目標
  預設開組→session 記住上次組＋冇掣冇 chip 標記）；`test_picker73_static.py`
  「保留目標設定入口」→「冇目標設定入口」。
- 反證：新／改版斷言行落 v73 index 分別 FAIL（target74 靜態 11 項／
  ux68 靜態 2 項／ux68 邏輯 2 項／picker73 靜態 1 項／progress71 邏輯
  P1・P3(v74) 2 項——嗰檔測試讀自己目錄嘅 index，反證要用 v73 index
  做同目錄副本先行到，已照做）。

## 實機驗證（verify74/，Playwright、槽 3、本地鏡像 sha 核對、零 pageerror）
- 新 session 開 picker：冇主攻掣、版面正常、預設開演技組；撳去歌藝組、
  關 picker、重開——記住歌藝組（session 行為）。
- 開星河電視台地點 sheet（有訓練／休息／接工選項）：organizer 分組照常、
  全頁 `.ux68-tgt` 元素＝0。
- v73 存檔（verify73/base_save73.json）喺 v74 繼續載入正常。
