# NOTES_V20A284_R5_BCDEFG.md — v284：R5 人情兌現票餘下六項（B＋C＋D＋E＋F＋G）

基線：main `61e5d4f`（v283 已落地，suite 347／9，九項 pre-existing FAIL）。
工作副本：`linji-work284`（clone 式，分支 `v284`）。index.html 46243→46301 行（淨 +58）；通告庫 288→289 張。

用戶拍板：2026-11-18 07:04–07:06 逐題揀（B／D／E／C／F／G）。R5 A＋H 已於 v283 落地。

## B — 芬姐《芬姐茶檔》改 1991 春＋中級（`content/gigs_new.json`，`gig_1992_tv_201`，id 不變）

- 年份 1992 春→**1991 春**，tier 高級→**中級**，pay [510,630]→**[270,330]**（中級電視 3 日 peer-exact：90–110／日；SPEC §7.1 中級帶 90–160／日，同級 peers 全部 90–110／日）。
- 其餘不變：3 日、req 演技 65、fame [5,14]、cast 廖 leadM＋胡 leadF＋陸 supportM＋鍾 supportF、trigger `credit_fen_rescue`。
- 窗口核實：`GIG_SEASON_LEAD88 = 60`（index.html L12214），1991 春可見 1990-12-31–1991-05-31；`exodusFenTick` 絕響最早 1991-06-01（1991 夏或 year≥1992），窗口全程喺絕響之前。芬債權由 `seedExodusFenPair` 經 `ensureMockJournal`（L27705）早期種下。
- v283 H 對照唔受影響（id 不變）。

## C — film_112《夜半無人聲》拆死 trigger → 普通板通告

- `content/gigs_new.json` `gig_1991_film_112`：刪 trigger＋刪 discoverNote；blurb「憑陸柏言團隊引薦入組」句改做「在渡假屋走廊與山路之間查探真相」。storyKeys 留返（v274 de-triggered rec_105 precedent）。tier 初級／pay [1100,1320] 不變。
- `index.html` L26537：`CREDIT_REDEEM_GIG283` 刪 `credit_wf3_lu_team:"gig_1991_film_112"` 一行＋加 v284 註解。舊存檔持有嗰筆債權嘅卡唔再出「可以換」行（測試斷言舊存檔卡無死行）。結局讀取 L12913 保留（永不觸發，無害）。
- 依據：`credit_wf3_lu_team` 全 repo 授出位 0 處；test_wf3_82_logic.js L161–165 明文釘死「鏈 A 休眠」。

## D — 葉守口《鬼馬經理人》改 1992 春（`content/gigs_new.json`，`gig_1991_tv_106`，id 不變）

- 年份 1991 夏→**1992 春**；tier 初級／pay [245,295]／trigger `credit_enc79_yip_manager` 不變。
- 窗口核實：1992 春可見 1991-12-31–1992-05-31；授出閘 `yip_choice`（index.html L38960）要 1991 年起＋tier ≥2（fav ≥25，`enc79TierOf` L38652）；葉 1991 夏先見面（N8 後台），授出多數 1991 秋後，窗口開嗰陣債權已在手。

## E — 霞姐情報貨幣（新機制，index.html）

用戶拍板：每筆一次，用完消耗，情報用現成池。v259 R1（cafe_help 唔計結局數）維持唔郁；授出路（`enc79HelpClear`）唔郁。

- 新 helper（L40584–40603）：`enc79CafeHelpHeld284()`（讀未兌現＋未絕響嘅 `credit_enc79_cafe_help_*`，L40589）＋`enc79ConsumeCafeHelp284()`（標 `redeemedBy:"cafe_help_intel"`＋line 加「已兌現：霞姐情報，茶餐廳多打聽一次。」句，寫法照抄 `br89OnGigComplete`，冪等，L40595）。
- `enc79TeaListen` 改三處（L40606 起）：
  1. 每日上限 2 次用晒之後，持有霞姐人情就多打聽一次（每筆一次，用完消耗；無人情就擋返 cap reason；L40606–40612）。
  2. 有霞姐人情嗰陣強制星風聲（現成風聲池 `ENC79_STARS` 過濾無 active whisper＋unlockYear，隨機揀一粒，星名＋地點＋3 日有效；無目標就早退「霞姐話：今日行內靜靜哋，冇咩大風聲，呢筆人情留返第日用。」——唔消耗，唔收茶錢；L40617–40627）。
  3. 風聲分支授出後消耗一筆，toast 加「霞姐人情已用一筆（尚餘 N 筆）。」（L40664–40668）。
- `mockAskDefs`（L27683 起，＋10 行）：持人情嗰陣飲茶掣 hint 加「霞姐人情 ×N：今日可多打聽 N 次（每次消耗一筆）。」。

## F — 新陸引薦《海角歸人》1992 春（通告庫 288→289）

- 新 gig `gig_1992_film_114`《海角歸人》男配角（插喺 film_113 之後；`content/gigs_new.json`）：1992 春／中級／電影／文藝／12 日／pay [1210,1430]／fame [28,45]／req 演技 75／roleScale film_support_main／hard 0.5／loc film_harbour／cast 陸 leadM＋鍾 leadF＋玩家 supportM＋江詩盈 supportF／trigger `credit_enc83_luk_patron`／discoverNote／storyKeys luk_baakyin。標題無年份數字；blurb／synopsis／posterBrief 全新寫（漁村碼頭歸人故事，唔抄 film_101）。
- 揀 BR89 路唔係通用路：BR89 係引薦語義；H 經反查自動出兩張名＋殺青標記自動，唔使改 v283；`br89GigOn` 讀同一筆債權嘅 `redeemedBy`，殺青邊張另一張自動落板。
- `index.html`：`BR89_PATRON_OF_GIG` 加第 15 對 `gig_1992_film_114:"credit_enc83_luk_patron"`（L26435）＋行內註解；map 頭註解加 v284 一行（L26425）。
- 窗口核實：film_114 1992 春可見 1991-12-31–1992-05-31；film_101（1991 秋）窗口約 1991-07-01–11-30；授出要 fav ≥70。

## G — 還錢授引薦債權（index.html `enc83GuLoanTick`，L40800 起）

- 還錢分支（`repay` 真嗰陣）加 `enc79GrantCredit({id:"credit_enc83_gu_patron", debtor:"顧明輝", title:"登台引薦", line:"顧明輝寫咗張卡片畀你：嗰位登台班主係佢舊相識，你攞住張卡去搵佢，佢會畀個機會你。", status:"未收"})`（L40802），try/catch 包住；`granted284` 真嗰陣 toast 副句加「佢寫咗張登台引薦卡片畀你，話班主係佢舊相識。」。
- 冪等：`enc79GrantCredit` 去重——`gu_patron` beat（L40893）已經會授同一筆，已有嗰筆唔重複授。
- OR 閘（L26441）**留返**：v284 之前已還錢嘅舊存檔 tick 唔會重跑，靠 OR 閘開通告，係遷移路。

## 測試

- 新檔 `tests/test_r5_284_logic.js`：**54 項 ALL PASS**（B 窗口＋級別／C trigger 已拆＋對照已清＋舊存檔卡無死行／D 窗口／E 授出→選項→消耗＋無目標唔消耗＋hint／F 新 gig 上板＋BR89 雙向落板＋H 兩張名／G 還錢授卡＋冪等＋壞帳唔授＋OR 閘留返）。
- 已更新並逐檔 PASS（18 檔）：test_r5_283_logic.js（BR89 14→15、通用 9→8、film_112 移除、kind:credit 維持 23＝15＋8）、test_br89_logic.js（15 對）、test_gig229_trigger.js（T8 15 對＋match 15）、test_enc83_logic.js（G 三斷言）、test_dur90_logic.js（A4 289）、test_gig229_grant.js（T0 289）、test_gig229_pack.js（P0 289、P1 27／152／70／19／21、P2 作品 165、每年 111／99／79、P8 233 張有 cast／影視廣告作品 116 張）、test_gig229_press94_advice.js（A10 289、named 156／base 133）、test_gig229_years.js（C0 289、A6 1992 年 79 張、C1 111／99／79）、test_sideline274_logic.js（A1 289、D1／D2 15）、test_sideline280_logic.js（總數 289）、test_sideline158_logic.js（T8 15）、test_sideline273_logic.js（15）、test_enc79_logic.js、test_favor259_counts.js、test_cast252_logic.js、test_awards63_logic.js、test_wf3_279_logic.js、test_wf3_82_logic.js。
- JS 語法：抽兩個 inline script 塊去 /tmp/check284.js 做 node --check，通過。

## Resync（v284 釘行漂移，腳本 `qa284/resync284.py`，冪等）

- Suite 首跑 TOTAL 342／15：9 項基線＋6 項新 FAIL（nat92 邏輯 1 項＋5 檔靜態）。
- nat92 F2：庫 288→289，錯峰合資格 276→**277**（289－12 入門）。
- 5 檔靜態（index.html 淨 +58 行；段規則：＜26425 ＋0、26425–26433 ＋1、26434–26534 ＋2、26535–27679 ＋3、27680–40570 ＋13、40571–40573 ＋33、40574–40577 ＋39、40578–40613 ＋50、40614–40745 ＋55、≥40746 ＋58；由 git diff hunk 頭逐段核實）：
  - travel114：FREE 40＋COUNT 12＋DEF 41491→**41549**＋WRAPPER 28769→**28782**（單次掃描 set 查表）。
  - rom176：4 釘 39846→39859、40204→40217（各 ＋13）、41376→41434、41532→41590（各 ＋58）；6325／14813 唔郁。
  - tang171／tang173：總行數 46243→**46301**、openLoc DEF 41491→**41549**、guard lines[41490]→[41548]。
  - gift185：總行數 46243→**46301**。
- 內容核實：腳本逐行對內容（openLoc／旗／DEF／WRAPPER／pin 片段），MISMATCHES: none；6 檔重跑全部 PASS。

## 全套 suite

- 全套 suite（2026-11-18 約 07:55，`bash qa131/run_suite.sh`，`/tmp/suite284b.txt`）：**TOTAL PASS 348 FAIL 9**——目標達成（347 基線＋新測試檔 1 項，總數 356→357）。9 項 FAIL 同基線名單一模一樣（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），**零回歸**。

## 合併＋Pages

- 合併 commit：`c53aa38`（main，2026-11-18，squash merge 自工作分支 `v284` 兩 commits `7c5c17b`＋`ce654ed`；26 檔，+886／−134）。`git push origin main`：61e5d4f..c53aa38，ls-remote 一致。
- Pages 核實（推 main 後約 4 分鐘）：HTTP 200，線上 index.html 同本地 byte-identical（4,687,484 bytes；sha256 `963205fe21c431a0b16b09107a55f70c02f8c7f7711e99b1d73ffa715bd70222`）；線上檔含 `gig_1992_film_114`（2 處）＋`enc79CafeHelpHeld284`（5 處）。
- 工作副本 `linji-work284` 已刪。

## 留畀下一版

- R5 最後一題 I（G-C2 鍾忠告卡機制）：DECISIONS Q6 已批「開新機制：憑卡下一次文藝片試鏡多一句提示」，未實裝；要定授卡位置＋提示文案＋入 R5 定另開引擎票，等 parent 定。
- 攻略 gig id 同步票（`gig_br89_patron_pang`→`gig_1991_variety_203`、$900→pay [200,240]、「電視劇」→綜藝；`gig_wf3_liao_harvest`→`gig_1991_film_214`；`g36_90_aut_adcentral_preshow` 係草稿 id，live 係 `gig_1992_ad_109`）。
- RIVAL_CFG 錯配另開票（`RIVAL_CFG.gigId` 話 film_109 係《霓虹夜影》男主角，live film_109 係《笑聲震天響》；真正《霓虹夜影》係 film_102）。
- Beat 5 冷版接 `liaoChoice`（v279 跟進）。
- v284 新測試檔計入 suite 總數：基線 347／9 → 目標 348／9（總數 356→357）。
