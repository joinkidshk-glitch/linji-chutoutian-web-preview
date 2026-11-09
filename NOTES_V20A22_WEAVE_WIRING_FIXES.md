# NOTES v20a22 — 串聯系統接線修復批次（試玩斷鏈）

背景：Phase 1–3 實機試玩（新檔玩到第 5 週）發現 2 項實機斷鏈＋多項部分通過。
單元測試全過但實機唔見——根因集中喺「接線／渲染路徑」：功能寫咗、測咗，
但玩家實際行嘅 UI 路徑無經過佢。今票按診斷一次過修 7 項。

## 共同根因（第 1、4 項源頭）
`openLoc(id)` 大 if/else：有 MOCK_ASK 嘅 hub 地點（agency_ho、cafe_cha）行 if 分支，
只渲染 MOCK_ASK 掣；通告板入口（doScout／逐 gig 試鏡掣）同傾談掣（doTalk）全部喺
else 分支，hub 永遠行唔到（v19u 設計）。

## 修復清單
1. **hub 分支開板＋傾談掣**：抽三個共用 helper——`addLocTalkGiftActs`（傾談＋送禮）、
   `addLocBridgeActs`（soft 橋接試鏡入口）、`addLocGigActs`（逐 gig 試鏡／查看檔期＋
   進行中拍攝）；else 分支改行 helper（行為不變），hub 分支喺 MOCK_ASK loop 後呼叫
   傾談 helper，並用 `gigsForLocSeasonBoard(L.id, calendarSeason())` 判斷：有 gig 先加
   「只查看通告欄」掣＋橋接＋逐 gig 入口，唔 hardcode 地點名（cafe_cha 無 gig 自動唔顯示）。
   → 人情幫忙通告《晨光劇場》喺事務所終於有板開；事務所／茶餐廳傾談行返 doTalk
   （pickNpcLine＋階梯提示結果頁）。
2. **人情補種守衛＋還款落紀錄**：`renderDebtPane` 補種教學債條件加守衛——
   `S.favorDueSettled` 有 `FAVOR_DUE_CFG.debtId` 紀錄就唔補種（修「作廢後債行復活」）；
   `applyMockAsk` 現金／禮物還清教學債嗰陣即刻寫入 settled `{result:"closed_other"}`，
   唔再單靠 favorDueTick 第二日兜底。
3. **favor toast 唔好被斬**：到期／作廢兩句長 toast 改 `toast(msg, {sub})` 兩段式
   （主句 ≤40 字、指示入 sub），避開 `toast()` 無 sub 時嘅 40 字截斷。
4. **情報行補玩家模板**：`castingNoticeDetailHtml` 摘要區加同 gigCardHtml 一樣嘅
   `intelLineForGig` 情報行（有值先出）；`gigBoardTeaserHtml` 加輕量「💡 有情報」
   標記（只標記、唔塞成句入短卡）。
5. **角度穿透淡紙**：`newspaperWrapFadeLines(subject, angle)` 加參數並傳入兩處
   FaceLines 呼叫；`enqueueNewspaperFromWrap` 淡紙分支改傳 `wrapAngle`。淡紙本意
   （fameDelta=0、匿名）保留。有意推翻 1-2/3-1 當時「淡紙唔傳角度」嘅舊斷言。
6. **人脈頁顯示統一**：`showPeople` 通用池全開後改顯示情報階梯下一級
   （`npcNextTierHint`：內幕情報 60 解鎖），過晒階梯先寫全開；`affProgressHtml`
   「對白池已全開」改「通用對白池已開晒」，唔再同階梯提示打架。只改顯示，唔改 gates。
7. **階梯權重微調**：`pickNpcLine` 階梯權重 daily 1.6→2.5、insider 2.2→3.5
   （wantIntel 時 4／5），過階後抽得到、有感；唔加跨階保證旗（留下一票）。

## 測試
- 新增路徑級測試（今票重點，唔只測單函數）：
  - `tests/test_weave34_logic.js`（45 項）：假 DOM 行**真 openLoc**——favor called 時
    事務所斷言通告入口＋《晨光劇場》逐 gig 掣＋傾談掣同時出現，未 called 時通告入口
    唔出現，cafe_cha 無 gig 自動唔顯示；真 `enqueueNewspaperFromWrap`（fame=5＋街坊卡
    stageVolumeDelta:1）斷言 dek 搶眼句＋tone="spotlight"＋fameDelta=0＋匿名，對照組
    steady；真 `castingNoticeDetailHtml`／`gigBoardTeaserHtml` 置旗／未置旗情報行有／無；
    真 `renderDebtPane` 三種 settled 結果下斷言唔補種（＋無紀錄對照照補）；
    真 `favorDueTick` 斷言 toast 主句 ≤42 字＋sub 有指示；真 `applyMockAsk` 現金還款
    斷言即刻寫 settled；真 `pickNpcLine` rel=65 抽樣斷言 insider 句出現得到、rel=30/10 唔洩漏。
  - `tests/test_weave34_static.py`（32 項）：靜態斷言鎖死入口函數體接線（openLoc hub 段
    含 doScout／doTalk helper／gigsForLocSeasonBoard、FadeLines 簽名含 angle 且兩處傳入、
    detail/teaser 體內有 intelLineForGig 等）。
- 舊測試更新（3 處，均為今票有意更改嘅行為，非回歸）：
  - `test_weave22_logic.js`：toast stub 改收 opts 拼 sub（驗全文指示內容）。
  - `test_weave12_static.py`／`test_weave31_static.py`：fade 斷言由「唔傳角度」改為「傳 angle」。
- 其餘舊測試全套（P0、P0-3、Weave 1-1～3-3）無改動、全過；全檔 script `node --check` 通過。
- 遊戲內建自檢（runSoftP0Checks ferry／fade／hi 段）逐項人手核對：嗰啲 pack 全部無
  反響卡 → angle=steady，淡紙輸出同改前一致，唔受影響。

## 無改
SAVE key、softRev、?v= 不變；反響包隨機分佈不變（fans 卡必入建議另開一票）；
story／award 模板 {playerName} 稱呼統一（試玩第 7 項）唔喺今票範圍。
