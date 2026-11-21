# v369 — 動畫 P1 補完＋系統回饋黑箱修復

評估報告（`linji-playtest-eval-2026-11-21/REPORT.md`）P2 ⑨⑩。UI 方案先經 GPT-6.2-sol 諮詢（原稿 `linji-drive369/gpt_consult_v369.md`），跟方向二紙本手帳風實裝。只改 UI／回饋，唔改數值玩法；唔改 SAVE key／softRev／產品 `?v=`。

## 現況核實（唔重做已有嘅）

已有（v362/v363）：掣按壓（`#app button:active`）、HUD 浮字（money/fame/credit/stress）、結算雙軌滾動、手帳貼紙、confirm 蓋章、傾談／約會／送禮 modal 好感數字、債權卡「可以換：」行（`creditRedeemLine283`，只喺人情頁內）、trigger 通告一次性 toast。

真缺口（本版補）：通告卡按壓、訓練／結算增量浮字、殺青蓋章、地圖 pin 彈跳、劇情關係變化視覺強調、送禮結果分級、人情兌現常駐入口提示、情報入口引導。

## 改動（index.html，淨 +181 行）

共通原則（GPT 方案）：先更新結果再播動畫；裝飾層 `pointer-events:none`；唔等 `animationend` 先畀操作；`prefers-reduced-motion` 停位移／縮放，保留高亮同數值差。

1. **卡按壓**：`.gig-teaser:active` 內層壓低（translateY 2px＋scale .99，外框唔郁），`:focus-visible` 金框。
2. **數值浮字**：`.result-line .good/.bad` 原位彈起（`statPop369`，唔複製文字、唔改行高；`formatResultNotes` 輸出不變）。
3. **殺青蓋章**：日結算 modal 標題旁紅印「已殺青」（`wrapStamp369`），只喺 `shootFinished` 嗰日出；DOM 注入（唔改 `test_dayend202` 釘住嘅模板字串）；週加速摘要（`flushWeekAccelSummary`）同樣蓋章。
4. **pin 輕跳＋可打聽**：有提示（storyTip／tip／board）嘅 pin 首次見到輕跳一次（`pinBounce369`，session 去重、每版地圖最多一個）；有打聽嘅地點（`mockAskDefs`：茶餐廳／事務所）pin 旁加「可打聽」細字。
5. **劇情 rel 強調**：StoryPlay 結果頁關係變化行（「同X的人情 ±N」／「人情有變」）加 `sp-rel369` 手寫旁註式強調（手寫字體＋金色左邊＋淡金閃）；`playerNotes` 文字輸出不變。
6. **送禮分級**：兩條送禮路徑（`doGiveGift`／`rom176DoGiveStarGift`）結果 modal 加「收禮反應：最愛／喜歡／普通／唔鍾意」一行（只顯示今次一級，唔預告全表）；鄧麗萍公事心意唔出（免誤會關係有變）。
7. **人情兌現入口**：手帳「人情」tab 常駐「可兌現」票角（`paintFavorBadge369` 掛 `paintBar`，判定 `creditRedeemable369` 同債權卡「可以換」行同源：BR89 反查＋`CREDIT_REDEEM_GIG283`＋`CREDIT_REDEEM_TEXT283`＋`triggerGigOn`）；人情頁可兌現卡紅框高亮＋故事債權組內排前（stable sort，其餘次序不變）。
8. **情報入口**：地圖頂欄常駐「打聽」掣（`openAskPicker369`：1 個地點直入、多個出 modal 揀，入地點照計出行額度）；地點面板打聽行動加左金邊高亮（`act-ask` 本有 class）。GPT 方案原建議面板行動排前——改動風險高（行動次序有測試同玩家習慣），改做高亮代替。

## 測試 resync

行號釘漂移（difflib 對位、逐行核實內容逐字相同先改）：rom159／rom176／tang152／text125／tang171／tang173／gift185／travel114，腳本 `qa369/resync369.py`＋`resync369b.py`（+2 行 delta）＋`resync369c_travel.py`（369b 嘅 `r_travel_set` 喺 m==n 時 return None 被 re.sub 食數，修復重做）。book141／book70：人情 tab 斷言字串更新（掣內加票角 span）。travel114 新增 2 處 `openLoc(` 呼叫點歸 COUNT（入地點計出行）。

## 驗證

- Suite：400 PASS／9 FAIL（九項 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），零回歸。
- Playwright 實駕（`linji-drive369/`）：地圖打聽掣＋可打聽 pin＋揀場 modal；人情頁可兌現卡排前＋高亮＋票角；殺青印＋數值浮字＋動畫唔鎖操作抽查；送禮分級行；劇情 rel CSS 實測。
