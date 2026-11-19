# NOTES_V20A329 — A2：`promptAudition` 死函數刪除＋TUT_AUD_LOCK 搬入 `doAudition`

## §一 改動（index.html，淨 −13 行：47,262 → 47,249）

1. **刪 `function promptAudition(gig, L)` 成個函數**（舊 L45312–45330，19 行）：v19i 註解明言試鏡預約紙本卡已廢，入口一律直走即場 `doAudition`；全檔 0 呼叫（只得定義行＋L17682 註解一句）。
2. **先搬，後刪**：`sawTutAudLock`／`TUT_AUD_LOCK` 首次教學 toast 由 promptAudition fail branch 搬入 `doAudition` fail branch（舊 L45531 `if(!gate.ok){` 之後，`toast` 之前），6 行，同原寫法（`back` 用 `()=> L ? openLoc(L.id, {travelFree:true}) : null`；首次鎖住嗰陣出教學 toast 並 return，之後先出通用 `toast(gate.reason||"未能試鏡")`）。
3. **L17682 註解改寫**：「掛喺 promptAudition 附近」→「掛喺 doAudition 附近」。
4. **唔郁**：`gigCardHtml` 剩返手帳 call 位（`S.booked` 非空先出），v325 殘留「新玩家只會喺板上短卡見到稀印」維持原狀；SAVE key／softRev／產品 `?v=` 唔郁。

### ⚠️ 算術更正（brief 寫錯數，按實測處理）
- Brief（任務＋triage A2）寫「淨 −18 行、總行數 47244」係算錯數：死函數實為 **19 行**（舊 L45312–45330，連埋閉括號行；brief 計漏咗 `}` 行），搬入 doAudition 嘅教學 toast 係 **6 行**，淨 −19＋6＝**−13**，總行數 **47,249**。
- 漂移分段：＜45312 唔郁；45331–45531 −19；≥45532 −13（插入＋6、刪除 −19）。

## §二 測試同步（`qa329/resync329.py`，difflib 對位核實純漂移）

- **difflib**：只得 3 個非 equal hunk（L17682 註解 replace／舊 L45312–45330 delete／舊 L45531 之後 insert 6 行），其餘全 equal。
- **`tests/test_aud91_static.py:73`**：seg 終點 `function promptAudition` → `function chungAdviceCardHeld229`（緊貼其後嘅函數；**triage brief 漏咗呢處，parent 補**——唔改，seg fallback 會抽 30000 字元，doAudition 入面 `pending` 字面會令文案檢查 FAIL）。Chunk 只多 B7 註解＋`CHUNG_ADVICE_TEXT229` 常數行，文案檢查不變。逐個跑 ALL PASS。
- **`tests/test_travel114_static.py`**：FREE 刪舊錨 45317（行已無），**原位加新錨 45514**（搬入咗嘅 back 行，`openLoc(L.id, {travelFree:true})`，排序 43840＜45514＜45611）；COUNT 4 處（45747／45955／46113／46134）＋FREE 6 處（45624／45625／45669／45670／45695／46584）各 −13；DEF 42471／WRAPPER 29083 唔郁；FREE 總數維持 40 處（刪 1 加 1）。逐個跑 PASS。
- **`tests/test_gift185_static.py`／`test_tang171_static.py`／`test_tang173_static.py`**：總行數 47262→47249，ok() 名歷史鏈加 `＋v329 −13`；openLoc DEF 42471／guard 42477／index 42470 喺刪除點之前，唔郁。逐個跑全部 PASS（tang171／tang173 各 22／22）。
- **計數不變／有變**：`openLoc(` 全檔 58 處不變（back 行由死函數搬入 doAudition，一出一入）；`gigCardHtml(` 3→2、`confirmSpendDay(` 5→4（刪死函數嘅 modal／confirm 呼叫，無測試斷言呢兩個數）。
- **`tests/test_rom176_static.py`**：錨點全部喺刪除點之前，唔郁；逐個跑 ALL PASS。

## §三 全套 suite

- **第一跑（工作副本，已 commit 樹）：TOTAL PASS 386 FAIL 9＝基線**（v328 基線：385＋新檔 r328 1 項），9 項 FAIL 同基線逐項一致（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），零回歸。**第一跑即達基線，唔使第二跑。**
- 六檔逐個直接跑全部 PASS（aud91 ALL PASS、travel114 PASS、gift185 ALL PASS、tang171 22／22、tang173 22／22、rom176 ALL PASS）。

## §四 教訓

1. **Brief 算術／行號要喺副本再核實，唔好照抄**：triage A2 寫 promptAudition 18 行（實為 19 行）、travel114 錨點行號 274（實為 275）、tang171 guard 值係 v327 數字（v328 已改）；今次三處都係開工前喺副本重新 grep 核實先發現。
2. **死函數刪除要查埋測試嘅 seg／抽取錨點**：triage 只列咗 travel114 錨點，漏咗 aud91 嘅 seg 終點——`seg()` 搵唔到 end marker 會 fallback 抽 30000 字元，靜默擴大 chunk，文案檢查會誤 FAIL。刪函數嗰陣要 grep 埋函數名喺 tests/ 全部出現處（今次 4 處：index.html 定義＋註解、aud91 seg、travel114 錨點）。
3. **搬入嘅行可能要入返測試清單**：搬入 doAudition 嘅 back 行帶 `travelFree:true`，travel114 掃描會要求佢喺 FREE_LINES 入面——唔係淨刪舊錨，要加新錨，否則「帶免費旗但唔喺 FREE_LINES」FAIL。

## §五 合併＋部署（待填）

- 內容 commit：（待填）
- main HEAD：（待填）
- Pages index.html md5／bytes：（待填）
