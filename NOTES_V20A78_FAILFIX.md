# v20a78 驗證 FAIL 修復包（結局鎖定＋台慶年界去重）

用戶 2026-11-10 20:31 定調「先穩定劇情比較緊要」：本包只修全弧驗證第三輪
（`~/workspace/linji-fullarc3-report.md`）兩個實證問題，唔加新內容、唔郁任何
數值門檻／結局判定條件。基底 v20a77（4,697,539 bytes，tests 84/84）。
SAVE key（`starVolunteer_map_v19w`）／softRev（`s107`）／產品 `?v=`（`v20a10`）不變。

## 修復一 [中] 結局後仍可繼續遊玩（LOCK78）

現象（第三輪實證，v65 第一輪起跨輪重現）：E1 自然結局（day 746）同 E7 破產
結局（day 98）出完結局總結之後，遊戲返回可玩狀態——日子繼續行、數值繼續變
（正常弧結局後 +10 日 fame 181→190；高壓弧 +42 日、credit 67→84、再病倒 1 次）。

根因：結局寫入點有兩個——C17 前夕抉擇經 `ending410AfterEveChoice` 寫
`S.ending410`（E0–E6，含 E6 自願退圈）、E7 經 `conseq61PresentForcedEnding` 寫
`S.ending410`——兩者呈現完總結（page1→page2→`showEndingSummary410`）之後，
主循環冇任何「已結局」狀態：總結頁得一個「關閉」掣，文案仲明文寫住唔會鎖檔
（E7 版「遊戲唔鎖檔：你可以繼續過日子…」／通常版「收科之後，你照樣可以
繼續跑通告過日子」）。關閉 modal 之後玩家返到地圖／手帳，`advanceDay` 照翻日、
地點 sheet 照開、行程照行。

修法（判定條件本身一概唔郁）：
- 新增 `ending78Locked(st)`：`S.ending410` 存在＝已結局（單一事實來源，
  兩個寫入點都經佢）；`ending78Gate()`：已結局時停週加速殘留並改出結局總結。
- 硬閘：`advanceDay()` 開頭已結局即 return false（全檔唯一 `dayIndex += 1`
  喺呢度）；`tickDay()` 開頭同閘，return `{ended:false, summary:null}`。
- 入口閘：`goToMapForBrowse`／`resolvePlannedDay`／`endBrowseDayGoHome`／
  `commitPlanAndGo`／`openLoc`（含 forceRestore 還原路徑——結局係終局狀態，
  冇合法流程要喺結局後還原 sheet）／`StoryPlay.start`（C17 本身喺寫入
  ending410 之前已經 start，唔受閘影響；閘只擋結局之後嘅新 start）。
  實駕覆核額外捉到一條漏網路：手帳恆常出口 `book70ExitHome`（及 fallback
  `leaveHomeFromNotebook`）係直出 `show("v-map")`、唔經 `goToMapForBrowse`，
  兩者已同樣加閘——其餘 `show("v-map")` 位點經普查係 debug／教學／開局流，
  結局後唔可達。
- 手帳：`enterHome` 已結局時強制 `editable=false`——作品牆／回憶／剪報等
  唯讀回顧照用，唔准再編排行程。
- 總結頁：`showEndingSummary410` 已結局時出口改為「回顧手帳／開新一局／
  讀檔」三掣（未收科嗰陣維持單掣「關閉」）；兩句舊文案改寫做收科語氣
  （全檔「遊戲唔鎖檔」「照樣可以繼續跑通告過日子」清零）。
- 剪報頁「重睇結局總結」係既有唯讀回顧入口，保留不變。

舊存檔判斷（載入處理）：判斷基準＝存檔入面有冇結局記錄旗標 `S.ending410`。
- 未結局嘅舊檔：冇旗標，完全唔受影響，照常行 `contFromSlot` 原路徑。
- 已結局嘅舊檔（包括喺 v77 或之前結局後被繼續玩落去嗰啲——佢哋嘅
  `S.ending410` 喺結局嗰刻已經寫入並 saveQ）：`contFromSlot` 載入即入已
  結局狀態——落手帳唯讀回顧＋出結局總結，唔行 `runScheduleFromToday`。
  結局後多行咗嘅日子／數值**唔追溯回滾**（存檔冇留結局嗰刻嘅完整快照可
  靠還原，硬回滾風險大過收益）；由載入嗰刻起鎖死，唔再變。

## 修復二 [低] 台慶頒獎年界雙觸發（AWARDS78）

現象：day 364（1990-12-31・冬1990・入圍）同 day 365（1991-01-01・冬1991・
旁聽）連續兩日舉行兩屆年度台慶。

根因：`queueAwardsOnSeasonWindow` 用「今日曆法年」（`awardsCalendarYear()`）
做 `S.awardsFlags` 去重鍵兼 pack 年份；而冬季定義係 12–2 月（`calendarSeason`），
橫跨公曆年界——同一季冬喺 12 月尾以曆法年 Y 開一屆，1 月頭旗標鍵變成 Y+1
（空）又開一屆。連帶傷害：1 月嗰屆食埋 Y+1 年嘅旗標，嗰年 12 月嗰屆俾
done 旗標壓住唔開，典禮自此永久漂移去 1 月（第三輪 day 742 冬1992 喺
1 月中舉行就係呢個漂移嘅延續）。已用抽函數沙盒對 day 363–365 實測重現。

修法：新增 `awardsEditionYear(ceremony, dayIndex)` 做「屆別年」——冬季屆別
歸開季嗰年（12 月＝當年、1–2 月＝上一年），其餘季節屆別年＝曆法年。
`queueAwardsOnSeasonWindow` 旗標鍵同 pack 年份改用屆別年；`awards62SeasonHints`
今季嗰台嘅旗標／作品計數同步改用屆別年（唔改的話 1–2 月提示會用錯年旗標
誤報「仲差 N 部」）。持久化去重照舊行 `S.awardsFlags`（鍵格式
`"year/ceremonyId"` 不變）。作品本身嘅曆法年（`awardsYearFromDay`）唔郁——
1990 屆計返 1990 年曆法年內殺青嘅作品，語義正確。

C10 讓路延期唔誤殺：`buildAwardResultPack` 喺 C10 窗口對台慶回 null 嗰陣
唔寫旗標、翌日重試；延期跨年界（12 月尾→1 月頭）屆別年不變，仍然開得返
同一屆（測試 (3) 覆蓋）。

其他三台年界風險檢查（schema 真值：廣告 春 wk≥6／金碟 夏 wk≥16／影藝
秋 wk≥28／台慶 冬 wk≥40）：春（3–5 月）、夏（6–8 月）、秋（9–11 月）成季
都喺單一曆法年內，冇跨年界，屆別年恆等於曆法年，冇雙觸發風險，唔使改。

舊檔：已雙觸發過嘅檔唔追溯——旗標入面嗰個錯位年份鍵（例如
`"1991/award_singho_tv": "done"` 係 1 月假屆寫嘅）會令嗰年 12 月嗰屆喺
舊檔入面俾壓住唔開（等於嗰年台慶已「舉行過」），唔做遷移硬改；新檔同
未雙觸發過嘅檔由生效日起每屆只開一次。

## 測試

- 新增 `tests/test_lock78_ending.js`（35 項）：ending78Locked 判定、
  advanceDay 已結局唔翻日（行為）、gate 行為、各入口接線（靜態，含
  book70ExitHome／leaveHomeFromNotebook）、總結頁三出口、舊文案清零、
  紀律不變。對 v77 index 行 → 16+ 項 FAIL（反證）。
- 新增 `tests/test_awards78_edition.js`（16 項）：屆別年單元、跨年界端到端
  只開一屆、延期唔誤殺、非冬季對照。對 v77 index 行 → FAIL（反證）。
- 既有全套 tests 照跑（見交付報告總數）；全檔主 script `node --check` 過。
- 真 UI 實駕（`verify78/drive78.py`，可棄用槽 3，證據 `verify78/`）：
  收割真存檔改植（money<0＋寬限 weeksLeft=1＋全週休息）→ 真 UI 行一週
  （day 1→7，未結局對照：日子正常推進）→ 週結觸發 E7 三頁至總結
  （三出口＋新文案）→ 探針：回顧手帳唯讀（homeEditable=false）、手帳
  「事業」分頁照開、恆常出口「返回地圖」俾閘擋返出總結、選單「提早
  休息／+1日」＋確定俾閘擋（日／聲望／錢唔變）、reload 已結局檔即入
  鎖定態出總結。全程 pageerror 0；截圖 shot1–shot4 存 `verify78/`。

## 不在本包範圍

- 覆蓋缺口「寬限入帳解除」正面驗證：唔喺本包，留待下輪驗證弧設計
  「寬限期內大額入帳」弧線補驗（第三輪兩條寬限弧收入都結構性低於門檻，
  未構成故障證據）。
- BUG-5（電視桶提示時機）、第三年頒獎俾結局閘截斷、E1／E5 門檻：全部唔郁。
