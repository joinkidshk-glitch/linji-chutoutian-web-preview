# NOTES v20a105 WEEK105 — 週界狀態組（UI 審計 S-12／S-13／S-14）

分支 `v20a105-week`（施工員 B，只做呢三項；冇掂 main、冇合併）。
SAVE key `starVolunteer_map_v19w`／softRev `s107`／產品 `?v=` `v20a10` 全部冇郁。
存檔只加兩欄（向後兼容）：`S.weekBoundary105`、`S.execLog105`；舊檔由
`normalizeSaveObj` 補空值，載入唔炸。

## S-12（A）週界流程唔跨 session
- 根源：`tickDay()` 喺翻日嗰刻即刻行 `settleWeek()`——扣生活費＋`saveQ()` 已完成，
  但結算畫面同「編排下週行程」嗰步只靠記憶體將 `summary` 傳落 `enterHome`。
  玩家喺週日日結板（「回家結算」掣）嗰陣重開，`contFromSlot` 只會
  `runScheduleFromToday()` 沿用上週 `weekPlan` 行落去，嗰步永久消失。
- 修法：`settleWeek` 扣完錢嗰刻將 `{week, day, html}` 寫入 `S.weekBoundary105`
  再 `saveQ()`；`enterHome(editable=true)`（入編排步）先清旗；
  `contFromSlot` 載入時用 `week105Pending()` 驗旗（只喺 `dayIndex === week*7`、
  即嗰週之後嘅週一有效，過咗就當殘旗清走）——有效就強制先入編排步再補呈現
  存低嘅結算卡（modal「回家結算 · 第 N 週」＋講明金額已入帳唔會重扣）。
- 防雙重扣錢：補呈現只讀旗入面嘅 `html`，成條恢復路徑冇 `settleWeek(` 呼叫
  （靜態測試釘死）；實駕驗證 reload 前後金額同為 $12,798（$13,898 − $1,100 只扣一次）。

## S-13（A）已殺青通告變下週「今日計劃」卡死嗰日
- 根源：`scrubStaleJobs` 只剔 `job:`（未 booked）同舊 district scout，
  `wrap:`／`audition:`／已唔存在嘅 `shoot:` 標記原樣留喺 `weekPlan`；
  跨週做「今日計劃」嗰陣，嗰日既唔係 map 日（冇「逛完・過一日」）、又唔係
  soft 行程（冇「開始今日行程」）、又唔係強制日，三種入口全缺。
- 修法：新增 `scrubInherited105`（剔 wrap:/audition:/死 shoot: → `scout_all`，
  活 shoot: 保留），`contFromSlot` 繼承時行；`todayPlanId` 見今日格係已完成
  標記即時改返 `scout_all` 兼回寫；`paintBar` 保底——任何非強制、非編輯、
  未有掣嘅日子補「逛完・過一日」（行既有 `confirmEarlyRestFromMenu`）。
  已完成標記嘅歷史改由 execLog105 回顧承載（見 S-14）。

## S-14（A）「上週行程」回顧同實際經歷對唔上
- 根源：回顧直接攞 `weekPlan` 槽位 label，但槽位會被之後嘅寫入覆蓋
  （`endBrowseDayGoHome` 寫 rest、殺青寫 wrap:、試鏡／劇情嗰日最後變其他標籤），
  冇任何實際執行紀錄可攞。
- 修法：新增 `S.execLog105 = { [dayIndex]: {kinds:[], detail} }`。
  記名路徑（全部喺 `tickDay` 之前）：`resolvePlannedDay` 按實際分支記
  shoot/wrap/audition(train job)/train/rest/chore/perform/sick；
  `doAudition` 記 audition；`StoryOC.applyChoice` 完成記 story；
  `endBrowseDayGoHome` 記 early_rest（同全日 rest 分名）；`doRest` 記 rest；
  `doEnrollRun` 記 train；病假結算記 sick；傾談／送禮耗日記 social。
  同一日多種合併顯示（如「劇情・試鏡：《賀歲特輯》…」、「到處逛逛・提早休息」），上限 3 種、只留最近 21 日。
  `tickDay` 兜底：冇記名嗰日按當日槽位記一次（`exec105KindForSlot`）。
  渲染：`renderNotebook` 對已過去嘅日子（`nbRowMeta105`，按 plan 週一絕對日計）
  優先用紀錄；冇紀錄（舊檔）退返槽位標籤，唔 crash。

## 測試
- 新守門：`tests/test_week105_logic.js`（30 項全過：真 `settleWeek` 只扣一次＋
  旗落存檔＋重載唯讀唔重扣＋殘旗/舊檔唔觸發；scrub/todayPlanId；exec 合併/回顧選源）
  ＋ `tests/test_week105_static.py`（接線＋紀律）。對 v20a104 基線行 → 兩者皆 FAIL（反證）。
- 既有全套測試：新版 FAIL 集合同 v20a104 基線逐個一致（7 JS＋8 PY 皆為改動前已存在），零新增回歸。
- 實駕（Playwright 本地鏡像，`qa105/drive105.py`，截圖 `qa105/shots/`）：16 項全過——
  週日日結板 reload → 補呈現結算卡＋入編排步＋金額只扣一次；
  下週週三已殺青標記消失、今日計劃變到處逛逛＋有「逛完・過一日」；
  手帳上週行程週一＝劇情・試鏡、週四＝到處逛逛・提早休息。
