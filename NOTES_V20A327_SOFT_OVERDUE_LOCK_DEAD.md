# NOTES_V20A327_SOFT_OVERDUE_LOCK_DEAD

版本：v20a327（暫定，順序號；若期間有其他票先落地，順延）
Base：main `fd90cd3`（v326，通告庫 322 張，index.html 47,280 行）
Brief：`~/workspace/linji-brief-soft-overdue-lock-v327.md`（偵察 2026-11-19，唯讀）
Suite 基線：385／9（九項已知 pre-existing FAIL）

## 一、改動（完美做法 (b)：成把鎖刪走，唔係接返寫入路徑）

偵察結論（parent 已逐項對 live 核實）：鎖自 v20a1 起從未有路徑可以觸發——雙重死因：
① preview flag 預設 off（實玩永遠行 live path）；② 就算 flag 開，都無已逾期債畀佢鎖
（`\.status = "已逾期"` 全檔 0 命中；全部到期 tick 一律 filter 移除，唔改 status）。
接返寫入路徑要逆轉 v20a17＋v20a298 兩個 deliberate 設計決定（「永不設已逾期」——死鎖：
幫忙通告本身就係還債路徑，債一標逾期，鎖會擋住玩家去做嗰張幫忙通告），係設計變更唔係 bug 修復。
到期後果已經存在（作廢＋rel −3／信用 −2／收割過期），唔缺一個鎖。

### index.html（淨 −36 行：47,280 → 47,244）
| # | 舊行號 | 改法 |
|---|---|---|
| 1 | L17426–17450 | 刪 `function softOverdueFavorDebtLock(gig){...}` 整個函數（25 行） |
| 2 | L17510–17513 | 刪 `canAudition` 內 try block（4 行） |
| 3 | L17559–17562 | 刪 `gateShortReason` 內 try block（4 行） |
| 4 | L35370 | 刪 `__freeplay` export 行（1 行） |
| 5 | L35450 | 刪自檢行 `fails.push("debt_lock")`（1 行） |
| 6 | L35484 | 刪回傳欄位行 `debtLock: ...`（1 行） |

註解三處改寫（唔留 dangling 引用，語義保留，行數不變）：
- L22737 FAVOR_DUE 註解：「避免 soft 逾期鎖誤鎖幫忙通告本身。」→「到期＝作廢（唔設逾期狀態）。」
- L22931 RIPPLE 註解：「永不設「已逾期」status（跟 F1），免 soft 逾期鎖誤鎖幫忙通告本身。」→「永不設「已逾期」status（跟 F1，到期＝作廢）。」
- L23380–23381 屋企債註解：「favorPressure 同 soft 逾期鎖兩處計算都明確排除」→「favorPressure 計算明確排除」。

### tests（3 檔，邏輯刪除）
- `tests/test_weave43_logic.js`：刪 L174 eval 行；刪 L189–L192 四行（兩個 lock 控制斷言＋專餵佢哋嘅兩個 S 賦值；同段 favorPressure 斷言保留）。
- `tests/test_weave47_logic.js`：刪 L476 eval 行。
- `tests/test_r300_pang_stage_half.js`：刪 L44 local stub 行。

### docs（2 處）
- `content/SCHEMA_FREEPLAY_FRAMEWORK_v1.json:93`：刪 `"overdueSoftLock"` 一行；上一行（`singleSource`）尾逗號一併刪走，JSON 仍有效。
- `docs/CONTENT_CONTRACT.md:152`：刪示範行 `__freeplay.softOverdueFavorDebtLock({});`。

### 絕對唔郁（已核實）
- 「已逾期」顯示系：`SEASON_COLLECT` 夏卡 `card_biao_summer`、`debtStatusLabel`、`DEBT_FUZZY`、`.debt-status[data-tone="已逾期"]` CSS、`favorPressure`、`seasonCollectToast`、`allDebtsForRepay`、`renderDebtPane`——全部 live UI。
- 同系其餘兩個 soft 閘 `softCastingTagGate`、`softIndustryCreditGate`；`ensureWeakSeals`／`castingTagsEarnedLabels`／`ENDING_NEG_TAGS410`。
- FAVOR_DUE／RIPPLE／grudge／fen／family 全部到期機制；dated 歷史 `NOTES_V20A*.md`；SAVE key／softRev／產品 `?v=`。

## 二、驗收（工作副本實測）
- `grep -rn "softOverdueFavorDebtLock" index.html tests/ content/ docs/` ＝ **0 命中**（NOTES 歷史提及＋brief 檔除外；測試檔頭 resync 註解刻意唔寫函數名，等驗收 grep 保持 0 命中，同 v326 做法）。
- `grep -rn "debt_lock\|debtLock" index.html tests/ content/ docs/` ＝ 0；`\.status = "已逾期"`（雙引號／單引號）＝ 0 命中維持。
- `grep -n "已逾期" index.html` 只剩 10 處顯示系（CSS、FAVOR_DUE／RIPPLE 註解、夏卡、DEBT_FUZZY、`debtStatusLabel`、`favorPressure`、seasonCollectToast、`mapFreeplayDebtStatus`）。
- `canAudition`／`gateShortReason` 其餘閘（tag／credit）行為不變；`__freeplay.check()` 自檢只剩 `soft_tag_gate`／`credit_gate`，其餘自檢不變。
- 總行數 **47,244**。

## 三、測試同步
- `qa327/resync327.py`：difflib 核實 9 個 hunk（3 deletes zone A＋3 comment replaces＋3 deletes `__freeplay`），淨 −36；漂移分區＜17426 唔郁、17563–35369 −33、35371–35449 −34、35451–35483 −35、≥35485 −36。同步 5 檔：gift185／tang171／tang173（總行數＋openLoc DEF 42489→42453）／rom176（4 釘行各 −36）／travel114（FREE 40＋COUNT 12 逐個內容核實＋DEF 42489→42453＋WRAPPER 29098→29065）。
- `qa327/resync327b.py`（suite 兜底）：第一跑 381／13，多出 4 項——rom159 四釘行各 −33（25457→25424、26305→26272、26206→26173、全佳 25485→25452）；aud91fix122／124／newspaper214 三檔 content JSON 守門——本包有意刪 schema 一行，按慣例加 `_v327_allowed` 豁免（ok 名加 v327；newspaper214 嘅 X05 名無版本表，唔郁）。
- 八檔受影響測試逐個直接跑全部 PASS（gift185／tang171 22／22／tang173 22／22／rom176／travel114／weave43_logic／weave47_logic／r300；rom159 156 checks 0 FAIL）。
- 全套 suite 第二跑：**385／9＝基線**，9 項 FAIL 同基線逐項一致（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），零回歸。結果見 `~/workspace/suite327.txt`（第二跑）。

## 四、備註（兩處同 brief 有出入，已按實測處理）
1. Brief §5 寫 `test_tang171_static.py:171` guard 係 `len(lines) >= 42496 … lines[42489]`，實際 v326 base 已經係 `42495`／`lines[42488]`（v326 resync 已改；brief 引用嘅係 v325 數字）。已按實際值改（42495→42459、lines[42488]→lines[42452]），tang173 同理。
2. weave43 刪 L190／L192 兩個 lock 斷言嗰陣，一併刪埋專餵佢哋嘅兩個 S 賦值行（L189／L191）＋分隔空行——佢哋只為嗰兩個斷言而存在，留低係死 code。
3. `muse.write` 寫入層會將非 `\n` 嘅反斜線加倍（`\\s`、`\\{`、`\\\\n` 全部中招，`\n` 本身唔受影響）——resync327.py 初版因此喺 counter 字串斷言失敗。修法：`BS = chr(92)` 拼字串、regex 改用 `[0-9]`／空格類、exec 核實改用 index 定位，檔案入面零多餘反斜線。教訓：以後寫含 regex／`\n` 字面嘅 Python 腳本，寫完先 grep 核實反斜線數量，唔好假設寫入原樣。

## 五、合併＋部署
- 內容 commit `99654f5` → 常駐 clone squash merge → **main `52ee0f4`**，已 push；ls-remote 核實一致。
- Pages 核實：curl 比對 byte-identical，index.html md5 `a7e80c804f4790f2eed9d69b79d690ce`／4,699,290 bytes；schema JSON HTTP 200。
- 工作副本已刪；`qa296/derive296.json` 乾淨（suite 喺工作副本跑，衍生檔無入版）。
