# NOTES_V20A259 — 農場洞修補 R1＋R2＋R3（＋R4 顯示）

- **基線**：main `5d59dfb`（v258）→ 本票落地後 main 新 HEAD 見回報。
- **拍板**：用戶 2026-11-17 08:44 揀「做晒 R1＋R2＋R3」；R4 純顯示一併做；R5 另開票。
- **依據**：`~/workspace/linji-favor-audit/FAVOR_AUDIT.md` §5.3／§5.4／§9.3＋本 repo `NOTES_V20A254_COORDINATOR.md` C 節（R1–R5 提案原文）。

## 改動（index.html）

### R1＋R2：creditsHeld 新口徑
- 新增共用 filter `favorCreditCountsAsHeld(c)`：只計「故事債權、未兌現、未絕響」。
  排除兩類：(a) `credit_enc79_cafe_help_*`（茶餐廳幫手債權）；(b) 有 `redeemedBy`（已兌現）。
- `endingFavor410()`（結局判定用）＋`favorLedgerCounts()`（live 讀取口）一齊改用佢；`heldList` 同步只含故事未兌現債權。
- `creditsTotal`（曾獲總數）唔郁；門檻數字唔郁（E4 ≥2／E5 ≥6／E3 ≥5）。

### R3：settled 語義統一——只計真係還清
- **定義（v259）**：settled 只計真係還清——還錢／還季節卡／幫忙結清（repaid_help）／提早還（closed_other，現金／禮物還教學債）／收割做完（wf3_harvest）。勾銷／作廢／過期唔做一律唔計。
- **逐個呼叫點核實（6 個，全部對過）**：
  - 計：`repaid_help`（幫忙通告結清）、`wf3_harvest`（收割做完）、`repay_season`／`repay_*`（現金／禮物還款）、`closed_other`（教學債現金／禮物還清——兩處：favorDueTick 兜底＋通用還款路徑；審核 §5.4.1「教學債過期作廢就唔計」指嘅係 `void_expired`，嗰條路本來就唔 call 入帳本）。
  - 唔計：`exodus_writeoff`（芬姐移民勾銷）——刪咗 L23329 嗰 call；`wf3_harvest_expired`（廖面子債收割過期）——刪咗 L26482 嗰 call；`void_expired`（教學債過期作廢）——本來就唔 call。
  - 另加 `favorLedgerNoteSettled` 內守衛：三個非還款來源（exodus_writeoff／wf3_harvest_expired／void_expired）直接拒絕，唔登記、唔計數（等日後同一筆債真係還清嗰陣先計，唔會鎖死）。
- **舊檔回填唔郁**：`ensureFavorLedger` backfill 計 `repaid_help`／`closed_other`＋季節卡——兩者按 code 都係真還款，定義一致。
- **定義註解同步**：`ensureFavorLedger` 頭註解嘅 settled 定義刪走「芬姐離港勾銷」，寫明三類唔計（v259 R3）。
- **c13 註解同步**：結局頁兌現註解舊句「endingFavor410／favorLedgerCounts 唔讀 redeemedBy」＋「已兌現債權仍計入 creditsHeld」已改——c13 例外只係因為標示遲過快照（快照計好嗰陣 c13 未兌現），唔係口徑例外。

### R4：分組顯示（純顯示，零玩法影響）
- **人情頁 `renderDebtPane`**：債權段分三組——故事債權 → 茶餐廳幫手 → 已兌現；每組非空先出標題行；已兌現卡狀態寫「已兌現」；絕響債權歸故事債權組，灰階＋「人已不在香港」不變。卡面 HTML／class／次序（組內）不變。
- **結局頁 `endingSummaryHtml410`**：人情總帳行之下加分佈行「人情債權分佈：故事債權 X 份 · 茶餐廳幫手 Y 份 · 已兌現 Z 份」（live 讀 S.mockCredits；絕響唔入三組；三組全空唔出呢行）。

## 測試

- **新檔 `tests/test_favor259_counts.js`（27 項，全過）**：R1（兩讀取口＋creditsTotal 不變）、R2（兩讀取口＋heldList）、R1＋R2 混合（故事 1＋茶餐廳 2＋已兌現 1＋絕響 1 → 1）、R3（拒絕三來源＋拒絕後真還清照計＋六種還款來源計＋冪等）、R4 人情頁真渲染（三組標題＋次序＋已兌現狀態＋絕響灰階）、R4 結局頁靜態（分佈行＋守衛字串在位）。
- **改動嘅舊測試（期望按新口徑更新，附歷史註解）**：
  - `test_weave42_logic.js`：exodus 寫入唔計 settled（3 處：write-off／fires only once／catch-up）；LEDGER_SRC 加 `favorCreditCountsAsHeld`（否則 favorLedgerCounts 抽出嚟行嗰陣 ReferenceError，held 計 0）。
  - `test_weave42_static.py`：唔使改——`"exodus_writeoff"` 字串留喺守衛集，靜態檢查照過。
  - `test_weave410_logic.js`：c13 註解同步；SRC 加 `favorCreditCountsAsHeld`（否則 crash）。
  - `test_conseq61_logic.js`／`test_gig229_counts.js`／`test_ladder95_logic.js`／`test_qa101_logic.js`：各加 `favorCreditCountsAsHeld` 抽取（endingFavor410 依賴佢）。
- **全套 suite**：見回報（工作副本跑）。

## Resync（v259 淨 +41 行引致嘅釘行漂移）
- index.html 淨 +41 行（`git diff` +55／−14；`count('\n')` 44640→44681）令 8 檔靜態測試釘行漂移，第一次全套跑出 TOTAL PASS 309 FAIL 18（8 個新 FAIL：gift185／kwan151／rom176／tang152／tang171／tang173／text125／travel114；其餘 10 項係已知 pre-existing）。
- **核實方法**：`/tmp/v259_resync.py` difflib 對位——67 個錨點（kwan151 3＋tang152 3＋rom176 6＋travel114 COUNT 12＋FREE 35＋DEF／WRAPPER 2＋text125 3＋tang173 1＋總行數）**零 mismatch，內容逐字相同，純漂移**。插入點分佈：舊 L12516＋9／L13288＋1／L13401＋15／L13418＋1／L23033＋1／L23073＋4／L23101＋1／L27364＋9；兩處呼叫改註解行數不變。釘行按段重算：＋0（L12516 之前）／＋26（L13418–L23032）／＋32（L23101–L27363）／＋41（L27364 之後）。
- **套用方法**：`/tmp/v259_resync_apply.py`＋`_apply2.py`——單次掃描 dict 查表（唔逐對 re.sub，防 14113→14139 同 14139→14165 撞值）；每個替換斷言出現次數（rom176 `line(14686)` 同一行用兩次，expect=2；kwan151 B3／B4／B5 共用 `line(14283)` 一併跟到 14309）。8 檔逐個重跑全過，再跑全套。
- 改動：gift185／tang171／tang173 總行數斷言 44640→44681、標籤 44651→44692（標籤＝斷言＋11，沿慣例）、鏈尾加 `＋v259 +41`；tang171／tang173 openLoc DEF 40041→40082（`lines[40040]`→`[40081]`、guard 40047→40088）；travel114 COUNT 12＋FREE 34 行＋DEF 40082＋WRAPPER 28034；rom176 五釘＋26／＋41；kwan151 四釘＋26；tang152 兩索引＋26；text125 `ls[16337]`→`ls[16363]`、訊息 16338→16364（11003／11140 唔郁）。標籤 Lxxxxx 歷史名唔郁（沿 v251 慣例）。

## R1 副作用（記低，等 R5 票）
- 霞姐債權變「結局零價值」（唔計 creditsHeld）。按審核 §9.2／R5 提案，R5 票將佢改做情報貨幣（每持有 1 筆，茶餐廳聽八卦多一個選項）＋其餘未兌現債權逐筆加兌現。呢票唔順手加兌現。

## 未修／留低
- 季節卡刷 settled（最多 +8，$1,600）維持現狀——有上限、要畀錢，審核定性為「成立但有上限」，R1–R3 唔郁佢。
- `softOverdueFavorDebtLock` 等死碼清理另票（v254 已記）。
- 實機驗證押後（瀏覽器死）：人情頁三組顯示、結局頁分佈行、E4／E5 門檻新口徑實玩。
