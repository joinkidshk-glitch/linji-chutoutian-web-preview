# NOTES_V20A283 — R5 人情兌現票：A 通用標記＋H 逐卡兌現說明

- 版號：v283（已核實未有人用）。Base main `af7c704`（v282，suite 346／9，通告庫 288 張）。
- 範圍：只做 R5 研究簡報嘅 A＋H。B／C／D／E／F／G 全部等拍板——拍板後已定 B＋C＋D＋E＋F＋G 入 v284，唔喺本票。
- 唔做儀表板（用戶 2026-11-18 06:32 明確停做）。

## A. 通用 credit-trigger 通告殺青標 `redeemedBy`（機制修復）

行號核實（v282 base，brief 嗰啲行號全部啱，BR89 map 實際喺 L26422–26431、函數 L26472）：
- 殺青鉤唯一呼叫點 L21489（`resolvePlannedDay`，`br89OnGigComplete(sh.gigId)`）。
- `br89OnGigComplete` 只認 BR89 map 14 張；`redeemedBy` 寫入全檔只得 3 處（L13400 c13、L26481 BR89、L44372 v158 渠道）。
- 9 張通用 trigger 通告逐張對過 `content/gigs_new.json`：全部 kind:"credit"，creditId 如下——
  `gig_1991_tv_204`《通宵追捕》→`credit_c7_rain`／`gig_1991_film_108`《月夜酒廊》→`credit_c9_crew`／
  `gig_1992_film_203`《江湖復仇》→`credit_c15_stunt`／`gig_1991_film_112`《夜半無人聲》→`credit_wf3_lu_team`／
  `gig_1992_tv_106`《冬日情書》→`credit_wf3_yip_manager`／`gig_1991_tv_106`《鬼馬經理人》→`credit_enc79_yip_manager`／
  `gig_1992_tv_201`《芬姐茶檔》→`credit_fen_rescue`／`gig_1992_film_101`《武館風波》→`credit_enc83_ngai_meal`／
  `gig_1991_film_109`《笑聲震天響》→`credit_enc83_liu_patron`。
- 通告庫 kind:"credit" 合共 23 張＝14 BR89＋9 通用，吻合研究簡報。

改動（index.html 淨 +77 行）：
- L21491：殺青鉤 br89 呼叫之後加通用分支呼叫 `genericCreditOnGigComplete283(sh.gigId)`（try/catch 包住，同 br89 一樣）。
- L26494 `gigRecordById283(gigId)`：按 gig id 反查通告記錄——先查當年 GIGS，再查 `STORY_WIRE.gigsByYear` 三年全庫（GIGS 只得當年，跨年殺青／跨年債權卡唔可以跌返去搵唔到）。
- L26511 `gigTitleById283(gigId)`：經上者反查通告名，查唔到跌返 gig id。
- L26517 `genericCreditOnGigComplete283(gigId)`：讀 gig 嘅 `trigger.creditId` 標記，模式照抄 `br89OnGigComplete`（`redeemedBy`＋line 附加「已兌現：…，呢份提攜真係落咗袋。」＋`syncNotebookMirror`）；BR89 map 有嗰張即跳過；冪等（已標唔重標）。
- 9 張無一補入 BR89 map（BR89 維持 14 對，測試釘死）。
- `gig_1992_film_202` 雖有 `trigger.creditId=credit_wf3_comedy_crew`，但佢喺 BR89 map 入面，通用分支跳過，唔重複標（測試釘死）。

效果：9 張殺青後 `redeemedBy` 在位 → `favorCreditCountsAsHeld`（L12611）返 false，`creditsHeld` 唔再計已兌現；手帳「已兌現」組（L28072，`!!c.redeemedBy`）＋結局頁「提攜兌現」句（L13407，同 filter）自動見到佢哋，唔使另改嗰兩處。
附帶清零已知跟進項「廖引薦雙 gig `redeemedBy` 缺口」：`credit_enc83_liu_patron` 雙 gig（BR89 `gig_1992_film_103`《吉星笑哈哈》＋通用 `gig_1991_film_109`《笑聲震天響》）——邊張先殺青就標邊張，另一張嘅開閘（`triggerGigOn` L26572／`br89GigOn`）讀 `redeemedBy` 唔再開，一筆債權只兌現一次。

## H. R4 逐卡兌現說明（純顯示）

改動：
- L26535 `CREDIT_REDEEM_GIG283`：通用 9 張 creditId→gigId 對照。
- L26541 `CREDIT_REDEEM_TEXT283`：v158 兩條免試鏡渠道類別名——`credit_enc79_mak_wuzhi`→「武打通告免試鏡」、`credit_enc84_pang_charity`→「司儀通告免試鏡」（渠道兌現係類別，唔係單一通告）。
- L26546 `creditRedeemLine283(c)`：未兌現先出 `<p class="debt-redeem">可以換：…</p>`——BR89 14 張由 `BR89_PATRON_OF_GIG` 反查（唔另抄表，免漂移）＋通用 9 張由上表＋v158 兩條寫類別；通告名經 `gigTitleById283` 反查（跨年都搵到）；已兌現卡返空字串（c.line 已有「已兌現：…」一句＋狀態「已兌現」）；無兌現／茶餐廳幫手／null 返空字串。
- `creditCardHtml`（L28060 一帶）：collect-line 之後插入 `${creditRedeemLine283(c)}`。純顯示，唔改計數邏輯。
- 例：`credit_enc83_liu_patron` 雙 gig 一行出晒兩張名——「可以換：《吉星笑哈哈》男配角／《笑聲震天響》男配角」。

## 測試

新檔 `tests/test_r5_283_logic.js`：**82 項斷言，全部 PASS**（單獨跑過兩次）。
- (0) 靜態 8 項：殺青鉤呼叫次序、BR89 維持 14 對、9 張唔喺 BR89 map、兩張對照表數目、creditCardHtml 呼叫、通告庫 kind:credit 仍 23 張。
- (1) A 功能 36 項：9 張逐張 redeemedBy＋line＋creditsHeld 排除＋mirror 呼叫（36 項入面 9×4）；冪等；film_202／film_101 跳過；無 trigger／未知 id／null 唔掟錯；跨年兜底（GIGS 只得 1992 年，1991 年通告照標＋照出名）；film_109 雙 gig 清口。
- (2) H 功能 38 項：BR89 14 張逐張標題、通用 9 張逐張標題、廖雙 gig 兩名一併出、v158 兩條類別名、無兌現／茶餐廳／已兌現／null 返空、跨年標題。

## 留畀 v284 嘅互動（唔喺本票做）

- **C film_112**：v284 會拆 `gig_1991_film_112`《夜半無人聲》嘅死 trigger（`credit_wf3_lu_team`），改做普通板通告。拆完之後通用分支讀唔到 trigger，自然唔再標——同本票一致，唔使另改 A。`CREDIT_REDEEM_GIG283` 入面 `credit_wf3_lu_team` 嗰行到時變死對照（債權卡唔會再出，因為 trigger 拆咗就唔會再授出／持有？——唔係，舊存檔持有嘅債權卡仍會顯示「可以換：《夜半無人聲》」；v284 嗰陣要決定留唔留呢行，建議一併清走）。
- **F 新 1992 年陸引薦**：v284 加一張 1992 年陸引薦通告（通告庫 288→289 張）。如果佢入 BR89 map，H 會自動經反查出名，唔使改本票；如果佢係通用 credit-trigger，要補 `CREDIT_REDEEM_GIG283` 一行。
- **B 芬姐**：`gig_1992_tv_201`《芬姐茶檔》v284 改 1991 春＋中級——改 gig 年份／級數唔影響 A／H（對照用 gig id，唔用年份）。
- **E 霞姐情報貨幣**：唔關 A／H 事。
- **G 還錢授引薦債權**：新授出嘅債權如果有對應兌現通告，H 要視乎佢入唔入 BR89／通用表再決定補唔補行。

## 釘行 resync（6 個靜態測試，本票 +76 行引起）

index.html 淨 **+76 行**（殺青鉤通用分支 ＋2＠舊 L21490 之後／R5-A＋H 新函數＋對照表 ＋74＠舊 L26493 之後；creditCardHtml 原地改，行數不變）。總行數 46167→**46243**。
段規則：舊行 ＜21490 唔郁、21490–26492 ＋2、≥26493 ＋76。全部逐行對內容核實，純漂移：
- `test_travel114_static.py`：FREE 30 處＋COUNT 9 處＋DEF 41415→41491＋WRAPPER 28693→28769（WRAPPER 舊 28693 ≥26493，係 ＋76 唔係 ＋2，內容核實捉到）。腳本 `qa283/resync283_travel114.py`（單次掃描 dict 查表，只換 dict 區行首 key 數字；可重跑，冪等）。初版漏咗 COUNT 22197（≥21490，＋2→22199），測試捉到 `UNACCOUNTED line 22199`，補返後 PASS。
- `test_rom159_static.py`：3 個釘行＋全佳行各 ＋2（25202→25204、26036→26038、25951→25953、全佳 25230→25232）。
- `test_rom176_static.py`：4 個釘行各 ＋76（39770→39846、40128→40204、41300→41376、41456→41532）。
- `test_gift185_static.py`：總行數鏈尾加 ＋v283 +76（46167→46243）。
- `test_tang171_static.py`／`test_tang173_static.py`：總行數＋openLoc DEF 鏈尾各加 ＋v283 +76（DEF 41415→41491，lines[] guard 41414→41490／41421→41497）。
- 六檔重跑全部 PASS；新測試 `test_r5_283_logic.js` 82 項全部 PASS。

## 合併

- 工作副本 `linji-work283`（clone 式），分支 `v20a283`。
- （落地後補：squash merge commit、main HEAD、suite TOTAL、Pages 核實。）
