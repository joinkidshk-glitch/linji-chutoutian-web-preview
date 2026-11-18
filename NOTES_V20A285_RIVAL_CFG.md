# NOTES_V20A285 — RIVAL_CFG 錯配修正

- 版本：v20a285（main HEAD 0ac7668，v284 之後）
- 問題：`RIVAL_CFG.gigId` 寫咗 `gig_1991_film_109`，但註解話係《霓虹夜影》男主角。
  查 live `content/gigs_new.json`：film_109＝《笑聲震天響》男配角（初級，trigger
  credit_enc83_liu_patron，廖炳星引薦）；真正《霓虹夜影》男主角係
  `gig_1991_film_102`（高級，1991 秋，trigger kind rival，rivalScoreMin 3）。
  後果：`rivalryGigForRound` 喺 GIGS 搵錯 id，對手線決戰會開出《笑聲震天響》男配角
  （仲要係要廖引薦債權先上板嘅通告），唔係《霓虹夜影》男主角；fallback
  `r.gigId = (gig && gig.id) || RIVAL_CFG.gigId` 會將錯 id 一路傳到決戰 offer。
  （test_gig229_trigger.js 早已當 film_102 係 rival gig；只有 RIVAL_CFG 同
  test_rival_board_r2.js 釘錯 id。）

## 改動（index.html，2 處）

1. L24636：`RIVAL_CFG.gigId` 由 `"gig_1991_film_109"` 改做 `"gig_1991_film_102"`；
   註解加 v20a285 修正說明（舊 id 係廖引薦，唔係決戰通告）。
2. L24868：mergeRivalGigs 註解 `(RIVAL_CFG.gigId＝gig_1991_film_109)` 改做 film_102。

唔郁：film_109 本身嘅廖引薦接駁（BR89 map L26543、beat:liu_repay L26821、
L26412／L26813 註解）、`rivalryGigForRound` 邏輯、第 2／3 輪重用同一張 id 嘅
isGigConsumed 閘（殺青後回 null，rematch 邏輯到時重寫覆蓋——維持原設計）。

## 測試

- 新 `tests/test_r285_rival_cfg.js`：12 項 ALL PASS
  （R1 CFG 指向 film_102；R2 film_102 數據正確；R3 film_109 唔郁；
  R4／R5 靜態註解已改；R6–R8 第 1／2／3 輪都回 film_102；
  R9 已消費回 null；R10 GIGS 只有 film_109 回 null——對手線唔會再開出
  《笑聲震天響》；R11 ensureRivalry 預設 gigId film_102；
  R12 第 1 輪 rivalryTick 開局出 film_102《霓虹夜影》）。
- 舊 `tests/test_rival_board_r2.js` 同步改 3 處（header 註解／seed gig id／
  gigId 斷言由 film_109 改 film_102）：9 項 ALL PASS。
  註：呢檔測試 B5 本身係按錯 id 寫成，係 bug 釘死咗喺測試入面，今次一併修正。

## Suite

`bash qa131/run_suite.sh`：**TOTAL PASS 349 FAIL 9**（基線 348／9，＋1 係新測試）。
九項 FAIL 同基線名單一模一樣，零回歸：
flash51／slot50／soft_tip_111_restore／start53／weave43_static／
weave44_static／weave49_static／wf5_87／wrap38。

## 實駕

（統籌為 generic 子代理，無 live browser 權限，未能實駕；node 層 R12 已驗
第 1 輪開局出 film_102。瀏覽器實駕——決戰 offer 真係出《霓虹夜影》男主角——
留 parent 實駕補驗。）

## 落地

- 分支 v285-rival-cfg（work commit 7a8a10d）→ main squash merge，main commit
  `3e65487`（2026-11-18）；`git ls-remote origin HEAD` 核實一致。
- Pages 核實：curl 200，4,687,712 bytes，sha256
  `abd05009fda949d6eb1dfa3316ea9172ea572e399a34dbad371b57e8b56c00b9`，
  同 main index.html byte-identical。
- 工作副本 linji-work285 已刪。
