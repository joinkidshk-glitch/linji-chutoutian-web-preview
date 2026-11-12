# v20a110：通告級別與要求脫節（OVR110）

- **分支**：`v110-gigreq`（由 main `8e9e773` 開）；**未合併、未推 main**。
- **審計**：`~/workspace/linji-work110/audit110.md`（667 行）；改動表 `req_overrides110.json`（246 張）＋`tier_overrides110.json`（96 張）；判處書＋實作細節見 `NOTES_V20A110_IMPLEMENT.md`。
- **改動**：`index.html` 只加 16 行——`TIER110`／`REQ110` 兩張 id 對照表＋`ovr110Apply(o)` 貼入 `normalizeGigRecord` 之前，喺 NAME93 呼叫之後加一行呼叫。唔改 content pack JSON、唔改 SAVE key／softRev／`?v=`。
- **結果**：全池去重 469 張，套用後 A／B／C 脫節全清零；開局 day-0 可接 14→**20**（底線 ≥12 保住）；第 2 週 rec_hk 板零訓練 2／8、歌藝 1 堂後 3／8、歌藝 2 堂＋魅力 1 堂＋台風 1 堂後 4／8；每級中位最高要求全部落帶（1990 初 20／中 70／高 130；1991 18／65／147.5；1992 18／66.5／172.5）。
- **升 tier 27 張**（初→中 23、初→高 1、中→高 3）：唔再係臨記，唔再喺臨記板出現，要聲望 ≥16／≥32 先報得。清單見 IMPLEMENT NOTES §6。
- **重要更正**：見報分類器跟角色文字，唔跟 tier——升 tier 唔會自動除「臨」印；只有《櫥窗》過場模特例外（標題有「過場」二字，升中後「臨」印不變，唔係 bug）。
- **測試**：新測試 `tests/test_gigreq110_logic.js`（45 項）＋`tests/test_gigreq110_static.py`（22 項）全 PASS；全套 A/B：基線 146 PASS／12 FAIL → 分支 **148 PASS／12 FAIL**（＋2＝兩隻新測試檔），FAIL 清單逐字相同，零新增回歸；主 script `node --check` OK；sim110.js 重跑數字同審計一致。
- **殘留缺口**（另票，唔喺呢包）：內嵌 fallback 11 張 req 差異未處理；片酬／工期異常 9 項；「特約男主」文案；死內容 103 張（改動表有佢哋 37 張，等加年先生效）；聲望第二閘（中 ≥16／高 ≥32）係設計原意。另：審計 §1「觸及 281 張」係筆誤，實數 273 張（96＋246−重疊 69），詳見 IMPLEMENT NOTES §8。
- **合併後待補**：線上核實（實駕：開局可接數、第 2 週 rec_hk 板、升 tier 通告板位）。
