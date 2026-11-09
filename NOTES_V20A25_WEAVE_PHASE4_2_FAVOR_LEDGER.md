# v20a25 — Weave Phase 4-2：人情帳本 favorLedger＋鏈 F 第 2 拍（芬姐離港／人情絕響）

Phase 4 第二步：補返結局判定要用嘅人情總帳，再用帳本承載鏈 F 第 2 拍「次要角色離港」嘅兩個後果（勾銷＋絕響）。

## 1. 人情帳本 `S.favorLedger`（新欄，optional、舊檔安全）

形狀：`{ settled, credits, exodus:[], counted:{} }`（另有一次性回填標記 `__bf`）。

- `settled`：已清債總數。
- `credits`：曾獲債權（人哋欠玩家）總數。
- `exodus`：變絕響嘅債權 id 清單。
- `counted{}`：冪等登記（id → {kind, source, day}）——每筆只計一次，任何結清路徑重行都唔會雙計。
- 讀取口 `favorLedgerCounts()` → `{ settled, credits, creditsHeld, openDebts, exodus }`，畀日後結局判定（E4 債權 ≥2、E5 清債＋債權 ≥6）直接用；`creditsHeld`／`openDebts` 由 `S.mockCredits`／`S.mockDebts` 即場數（絕響唔計）。

### 結清路徑掛點（全部行 `favorLedgerNoteSettled`／`favorLedgerNoteCredit`）

| 路徑 | 入口 | 計入 | source |
| :--- | :--- | :--- | :--- |
| 一般還款（現金） | `applyMockAsk` repay 清債後 | settled +1 | `repay_cash` |
| 一般還款（禮物） | 同上 | settled +1 | `repay_gift` |
| 教學債經還款清 | 同上（兼寫 favorDueSettled） | settled +1 | `closed_other` |
| 季節卡還清 | 同上（`_seasonCard`／SEASON_COLLECT 分支） | settled +1 | `repay_season` |
| 教學債幫忙通告結清 | `favorDueTick` repaid_help | settled +1 | `repaid_help` |
| 教學債 tick 兜底記帳 | `favorDueTick`（債已唔見＋armed） | settled +1 | `closed_other` |
| 芬姐離港勾銷 | `exodusFenTick` | settled +1 | `exodus_writeoff` |
| 芬姐債權播種 | `seedExodusFenPair` | credits +1 | `seed_fen_pair` |

### 設計決定（講明）

1. **作廢（void_expired）唔計 settled。** 過期無人做＝失約，唔係「清」；計入會令結局判定以為玩家還咗債。程式喺 void 分支留咗註解講明，測試亦有斷言。
2. **季節卡計 settled，唔計 credits。** 簡報原假設 SEASON_COLLECT 係「人哋欠玩家」，但程式實際語義相反：卡面原文係債主講「你欠我嗰筆數」，仲款掣係玩家畀 $200／禮物，清除係「還清」。跟簡報「以 SEASON_COLLECT 實際語義為準」——計 settled。
3. **債權（credits）今票唯一來源係芬姐債權種子。** 遊戲本身之前無任何「人欠玩家」嘅持久結構；今票新加 `S.mockCredits` 清單承載（手帳人情頁獨立一段渲染）。日後其他債權來源照 `favorLedgerNoteCredit` 入帳即可，E4/E5 門檻靠後續內容補來源，今票唔硬造。
4. **舊檔回填只行一次**（ledger 首次建立、`__bf` 未置時）：`favorDueSettled` 嘅 `repaid_help`／`closed_other` → settled、`void_expired` 跳過；`mockSeasonCleared` 為 true 嘅 id → settled；全部同步寫入 `counted{}`（source 前綴 `backfill_`）防雙計。推斷唔到嘅（例如回填前已經用舊版清咗、又無任何紀錄嘅債）由 0 起，無得追。
5. **回填／真結清撞車處理**：若結清寫入（favorDueSettled／mockSeasonCleared）早過該 session 第一次 ensure（回填），回填會先計數；其後真路徑嘅 note 唔加數，但會將 `counted` 來源由 `backfill_*` 升級返真 source，唔留推斷來源誤導日後查帳。

## 2. 鏈 F 第 2 拍：副導演芬姐離港（1989 夏）

離港者：副導演芬姐（`extra_ad_fen`，LIVE 演講者表 display 用字；唔喺 NPCS，屬次要角色，符合拍板）。查過現有內容：無任何芬姐債／季節卡，所以新播種一對。

### 播種（1989 年起，`seedExodusFenPair`，ensureMockJournal＋事件 tick 雙入口，固定 id＋旗冪等）

- 債（玩家欠佢）：`debt_fen_standin`「芬姐頂更人情」——阿偉病到面青嗰晚，芬姐幫佢頂咗嗰更，保住嗰日人工同印象，記一筆細人情。入 `S.mockDebts`，跟一般債渲染／還款。
- 債權（佢欠你）：`credit_fen_rescue`「芬姐欠你嗰次救場」——清水灣外景你落手幫佢頂到收工。入新清單 `S.mockCredits`，播種即 `credits +1`。
- 兩項都守「已結清唔重種」：帳本 `counted{}` 有紀錄就唔好再種返（旗遺失都守得住）。
- 1988 年完全唔種；1989 春開局存檔自然喺春種齊，兩條分支都可達。

### 事件（`exodusFenTick`，掛 `advanceDay` 尾、跟 favorDueTick 同模式，一次性旗 `S.exodusFenFired`）

- 觸發：`yearSeasonNow()` 係 1989 夏；**catch-up**：存檔若喺更新前已跨到 1990（year≥1990 未觸發過），tick 會先補種再即時觸發，唔靜默錯過。
- 效果：
  (a) 芬姐債未清 → 喺 mockDebts 移除、帳本計 settled（`exodus_writeoff`）——離港勾銷；
  (b) 芬姐債權未收 → status 轉「絕響」，id 入 `ledger.exodus`；手帳渲染加灰階 class `debt-exodus`（opacity .55＋grayscale）＋「人已不在香港」文案＋絕響 status 色；
  (c) 情報：固定 id 傳聞碎片 `rumor_fen_exodus_tip` 入池（芬姐臨走口風：清水灣新廠唔夠人、有經驗臨記唔愁無工開、睇實通告板——指向現有通告系統，唔新開情報線、唔入 MERGE_PAIRS）；
  (d) 兩邊都無（已還清／已處理）→ 事件照觸發：toast 講芬姐離港＋情報碎片照入，唔靜默。
- Toast 兩段式（主句＋sub），跟邊條分支在場揀文案（勾銷／絕響／送機）。
- 絕響排除：`allDebtsForRepay()`（還款入口來源）跳過 `status==="絕響"` 嘅債行；`favorPressure()` 計數排除絕響；`renderDebtPane` 絕響債行無「去還」掣、絕響債權直情無掣。`debtStatusLabel` 新增「絕響」直通＋`DEBT_FUZZY["絕響"]` 文案。

## 測試

- 新增 `tests/test_weave42_logic.js`（62/62 PASS）：一段回填＋冪等（作廢唔計）；二段行真 `applyMockAsk` 四條還款路徑（現金／禮物／季節卡／教學債）各 +1 且來源正確；三段行真 `favorDueTick`（repaid_help 計、void 唔計、closed_other 兜底只計一次）；四段行真 `ensureMockJournal`＋真日曆（1988 唔種、1989 春種一對、冪等、已結清唔重種）；五段離港事件（兩分支齊、只觸發一次、還清後唔雙計、兩邊都無仍有 toast＋情報、春唔觸發、1990 catch-up）；六段行真 `renderDebtPane`（絕響灰階 class／「人已不在香港」／無還款掣）＋`favorPressure`／`allDebtsForRepay` 排除絕響；七段 `favorLedgerCounts`。
- 新增 `tests/test_weave42_static.py`（37/37 PASS）：帳本形狀／掛點／種子 id／觸發閘／絕響接線／MERGE_PAIRS 無新碎片／SAVE key、softRev 不變／新文案無真藝名。
- 全套回歸：tests/ 共 30 檔（15 邏輯＋15 靜態）全部 PASS；全檔 inline script `node --check` OK。
- 慣例不變：無改 SAVE key（`starVolunteer_map_v19w`）、softRev（s107）、`?v=`（v20a10）。

## 未做（分票）

- 債權嘅「使用／收取」互動（E4「未用債權」要等結局系統票先定義點用）；今票債權只入帳＋顯示＋絕響。
- 鏈 F 第 4 拍（何生「走定留」對白＋旗）、第 5 拍（移民潮通告）、第 6 拍（結局回收）留待後續 Phase 4 分票。
- 帳本數字暫時唔喺玩家面顯示（結局判定專用）；要唔要喺手帳加一頁總帳，等結局票再決定。
