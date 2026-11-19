# v20a336 跨年即派修復（G-NGAI-3 實駕 BUG-1）

## 問題

runtime `GIGS` 按日曆年載入（`syncGigsForCalendarYear`，1991 年只載 1991 庫），但
`grant229GigById`（舊 L27148）淨查當年 `GIGS`；`grant229Record` 搵唔到就靜默
`return false`——唔入 queue、唔設 flag，玩家面零提示。Beats 係一次性，派唔出即永久冇咗。

實駕證實三例（`~/workspace/linji-drive-ngai3/CHECKLIST.md` BUG-1 節）：

1. Beat 3「下次先」→ `gig_1990_film_210`《茶餐廳早市熟手臨記》喺 1991 播 → 永遠派唔出
2. heart「認真記低」→ `gig_1992_film_108`《劍客傳》喺 1991 播 → 無入 queue
3. patron「講大話」→ `gig_1991_film_114`《刀光劍影錄》喺 1992 播 → 無入 queue

GRANT229_ENC79 全表 74 行多處跨年配對（1990 gig 25 行、1991 gig 28 行、1992 gig 21 行），
唔限魏線；GRANT229_CHOICE 44 行同理。

## 改動（index.html 淨 +24 行，47272→47296）

1. **`grant229GigById`（L27148）查全庫**：先查當年 runtime `GIGS`（快路徑不變），搵唔到再查
   `STORY_WIRE.gigsByYear` 三年全庫（同 `gigRecordById283` L26744 同一查法）；全庫命中係
   raw 記錄，經 `normalizeGigRecord` 先返（shootDaysHint 等引擎欄位同入池版一致）。
   只有兩個呼叫點（record L27170／deliver L27274），語義不變；真係全庫都冇嘅 id 先返 null
   （保留「唔好派空頭支票」）。`grant229Record` 註解同步改「全庫都無呢張」。
2. **`grant229DeliverOne` 派發後補入 GIGS**（scheduleShoot 之後）：跨年 gig 唔喺當年
   runtime `GIGS`，派發成功後補入，令拍攝／殺青路徑嘅 `GIGS` 反查（end95／end229 計數、
   wrapHistory 欄位、shootDeadlineHud）照常 resolve。補入嗰刻 shoot 已建立，
   `isGigConsumed`＝true，板面 pool（`gigsForLocSeasonBoard`）唔會貼返出嚟，唔污染板；
   下次 `syncGigsForCalendarYear` 換年庫自然清走（同普通通告跨年一樣，殺青路徑容忍缺失）。
   record 嗰陣唔補入（未派發前 GIGS 不變）。
3. **唔郁**：GRANT229_ENC79／GRANT229_CHOICE／GRANT229_DRAFT 任何一行配對、一生一次
   flag 語義、板面 pool、syncGigsForCalendarYear。

行號漂移：qa336/resync336.py（difflib 核實 4 處 hunk：註解 ＋5＠舊 L27148 後、查表體
1→13 行＠舊 L27151、註解改字 1→1＠舊 L27171、補入 ＋7＠舊 L27282 後；錨點按段
shift：≤27148 唔郁、27149–27151 ＋5、27152–27282 ＋17、≥27283 ＋24）。resync 5 檔：
gift185／tang171／tang173（總行數＋openLoc DEF 42492→42516）、rom176（4 釘行 ＋24）、
travel114（集合 31 錨 ＋24＋DEF 42516＋WRAPPER 29116，逐錨內容核實）。

## 驗證

- **新測試** `tests/test_r336_grant229_cross_year.js`：21 項 ALL PASS。沙盒同
  test_gig229_grant.js 同模式，但 `GIGS` 改做當年年庫（normalize 後）、
  `STORY_WIRE.gigsByYear` 係三年 raw 全庫——同 runtime 一致（舊 test 用全庫做 GIGS
  遮住咗呢個 bug）。覆蓋：三實例錯年份 record 成功；全表掃描 ENC79 74 行＋CHOICE
  44 行＋DRAFT 2 行＋直接呼叫 2 張（luk_tease tv_203／pang_finale variety_203）逐行
  喺「最唔利年份」GIGS 下 record 成功；跨年 dispatch 全程（何生來電 modal＋shoot
  建立＋簽約金三成入帳＋gig 補入 GIGS 一次且 normalized＋isGigConsumed true）；同年
  dispatch 唔重複補入；冇嘅 id 仍然 return false；一生一次 flag；record 唔補入 GIGS。
- **全套 suite：389／9**（v335 基線 388／9＋新測試檔 1 項；9 FAIL 同基線逐項一致，
  零回歸）。第一跑 384／14 係行號釘未 resync（gift185／rom176／tang171／tang173／
  travel114），resync 後回 389／9。
- **實駕覆驗**（`~/workspace/linji-drive336/`）：本地 serve 工作副本（md5
  `ea4681febfe062d984962ca57b5d763f` 對版），用 ngai3 harness 改指本地重播 S4a2
  （Beat 3「下次先」）：6 項 CHECK 全 PASS——grant-queued（film_210 入 queue，
  dueDay 522）、翌朝何生來電直接獲聘（shoot 建立、pay $203、簽約金 $61＝三成、
  totalDays 3、delivered=True）、call text 在位。截圖
  `s4a2-morning-hit.png`（1991 年何生來電派 1990 年《茶餐廳早市熟手臨記》＋支票
  $61）。v158／ngai3 原本 FAIL 嘅 S4a2 而家全 PASS。

## 跟進

- BUG-2（魏 patron 債權 1992 年無兌現通告）唔喺本票範圍，排隊 v337 補 1992 張。
- MEMORY.md 按 brief 無直接改——版本進度行要 parent 更新做 v336（suite 389／9、
  通告庫 322 張不變、index.html 47,296 行）。
