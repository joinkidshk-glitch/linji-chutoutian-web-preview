# NOTES_V20A145 — v143 review B1＋B2＋B3（手帳紙面化收尾）

用戶 2026-11-13 00:04 拍板修 v143 review 頭三項。基底 main `c881530`（v134）；分支 `v20a145`。**只實作＋測試＋實駕，唔合併入 main、唔 push main、唔開 PR**，等 parent 核實＋落地。

## Rebase＋重驗（2026-11-13 統籌核實，落地前）

- main 其間行前咗（v136／v138／v142 落地，HEAD `79defe3`）：分支 rebase 到 `79defe3`，新 commit `728cbaa`。`index.html` 自動合併，difflib 核實淨係 +67 行 BOOK145 插入；測試檔行號衝突已解（取 main 版＋67，逐個錨點實量核實：text125 三個 fallback 行、travel114 13 個 COUNT＋27 個 FREE 全部對位）。
- 全套重跑（rebase 後分支＋新鮮 pristine baseline 對照）：**分支 PASS 209／FAIL 12；pristine PASS 207／FAIL 12；FAIL 清單完全一致**（12 個全部 pre-existing：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111／start53／weave43／weave44／weave49／wrap38）＝零回歸。+2 係本票新測試。註：第一次 `run_suite.sh` 背景跑報 113／108 係該次運行本身嘅假象（同一個 loop 人手重跑即係 209／12；個別跑亦全部 PASS），已用逐 loop 重跑＋pristine 對照排除。
- 實駕重跑（`drive145.py`，rebase 後）：**0 pageerror／0 HTTP404**；B1 700 鎖定態 7/7（週日 593–635，footer 頂 639）；B2 pane 全部 `rgb(243,230,200)`、紅墨圈跟 active；B3 chips 紙面；932 印章 24px／footer 84px／標題列照舊。7 張截圖重出（同景重渲染）。

## 改咗邊幾處（index.html，淨 +67 行；唔郁 content pack JSON）

- **CSS 段**（`</style>` 前，`/* === v20a145 BOOK145 === */`，L5394–5460）：全部三項樣式。手寫字體棧／紅墨 `#c0452c`／紙面 `#f5eddc`／`#fbf3df`／事業頁紙 `#f3e6c8` 跟 v141／v143。掣嘅 id／class／onclick 綁定零改動。
- **B1 — 700px 鎖定態 7/7 行全見（揀咗做法②＋細微收窄）**：
  - **量度糾正**：任務寫法話「仲差 17px」，pre-fix probe 量到 700 鎖定態 5/7——週六頂 612／底 654、footer 頂 637（17px 只夠週六成行＝6/7）；**週日底 699——要 7/7 全見其實差 62px，唔係 17px**（標題行 22px＋提示列 27px＋間距 ≈ 61px）。所以揀做法②：`@media (max-height:780px)`＋`:has(#btn-confirm-plan.is-locked)` 限定，收起鎖定態「本週行程」標題行＋「行程已定」提示列（`display:none!important`，慳 61px）；`.nb-range` 底 margin 6px→2px（`!important` 蓋 1655 行）；`#nb-actions` padding 6px→5px。合共慳 **67px**。印章維持 20px（唔再縮，唔失印章味）。
  - **932 唔變**：唔入 media query，印章 24px／3px double／斜 -4.5°／footer 84px／七日 7/7 原封不動。標題行／提示列本身仲喺 HTML，淨係 CSS 收起（DOM／文字唔郁）。
- **B2 — 其餘 8 組 pane 換紙面**：
  - Pre-fix probe 核實：works／awards／memory 三組 journal-scroll 已經係紙色；其餘 **8 組仲係透明**（透出 `#v-home` 深色底）：ledger、inv、rumor、clippings、debt、people、tags、progress。plan pane 本身係 notebook 紙面，唔使郁；事業三頁（v142 範圍）同 plan pane 一律唔郁。
  - 8 組 `.journal-scroll` 換紙面，跟 v131 B2 事業三頁同一套（`#f3e6c8`＋金邊 `#c4a574`＋圓角 14px＋padding 12px 10px 16px）。內容面板本身唔郁，淨係換底。剪報／庫存空狀態細紙卡浮喺深色上面——pane 換紙面之後一併解決，實駕驗埋。
  - 附帶三處深底淺字覆寫還原墨色：`ledger-enroll`／`people-next` → `#6b4e2e`，debt `.pane-intro` → `#5a4328`。
  - **續（實駕目視捉到，見「實駕」節）**：v76 為深底加嘅淺字覆寫仲有三處喺新紙面頁——`.jobs72-h`（庫存／人脈標題，4979 行 `#ecdfc2` 喺紙面淡到睇唔到）同進度頁 `.prog71-h`／`.prog71-intro`；喺紙面頁範圍內還原返墨色（`#43301c`／`#8a755a`）。傳聞頁 `.weak-whisper` 係故意淡化嘅鬼影字（v76 判斷清單保留），唔郁；記數簿 h3 繼承 pane 墨色、debt／rumor 無 h3，唔使郁。
- **B3 — 訓練選擇器紙面語言**：
  - **更正**：屬性 chips 其實係 **`.guide68-chip`**（`train71PickerHtml` 出，兩個 host 共用：全日填滿 `#train71-picker`＋逐日 `.train71-host`），**唔係 `.train71-pick`**——嗰個係課程卡上面「全日排呢堂／排入呢一日」金掣。兩個一齊換紙面語言：chips 紙 `#fbf3df`＋金邊 `#b99b62`＋radius 3px＋手寫字，選中紅墨（`#c0452c`＋淡紅底，跟複製 chip `.on`）；`.train71-pick` 同套紙標籤。課程卡本身（`.guide68-row`／`.t70-mini`）已經係米紙卡，唔郁；已揀卡綠框（`.t70-card.picked`）照舊。功能一個都唔少。
  - **舊規則搶贏一鑊（實駕量度捉到）**：1887／2116 行 `.nb-quick button`（0,1,1 後代選擇器，底 `#efe6cf`＋8px 圓角＋`font-family:inherit`）蓋走 0,1,0 嘅 base rule——chips 同排入掣全部係 `.nb-quick` 後代（全日 host）；選中態 0,2,0 先贏到，所以第一輪 drive 得選中啱。修法：選擇器升到 0,2,0（`.guide68-chips .guide68-chip`／`.train71-acts .train71-pick`，親層；逐日 host 唔喺 `.nb-quick` 入面，同一選擇器照樣啱用）。2116 行 font-size／min-height／padding 係 `!important`，唔郁（chips 維持 .72rem 密度）。

## 測試

- 新：`tests/test_book145_static.py`（32 斷言）＋`tests/test_book145_logic.js`（11 斷言，接線唔郁）。
- 反證（pristine main `c881530`，`git show` 出嚟嘅 index → `/tmp/pristine145_index.html`）：static **20 FAIL**／logic **1 FAIL**（淨 gate，同 v143 模式一致——接線斷言本身喺 pristine 都 PASS，因為接線冇郁過）；工作副本 **ALL PASS**。
- 全套（`qa131/run_suite.sh`）：基線 **PASS 201／FAIL 12**；本票 **PASS 203／FAIL 12**（FAIL 清單完全一致，12 個係 pristine 已有；+2 係新測試）＝零回歸。
- 舊測試 rebase（純行號漂移，`qa145/resync_travel114.py` 用 difflib 核實：單一 replace 舊行 5393→新行 5393–5460，淨 +67；全部錨點內容對位一致）：
  - `test_map54_static.py`：allowlist 加 `v20a145`（寬容式，同 v141／v143 做法一樣；pristine 照舊 PASS，預期之內）。
  - `test_text125_static.py`：錨點 +67（27674→27741、27787→27854、33385→33452）。
  - `test_travel114_static.py`：COUNT 13＋FREE 27＋DEF 53222→53289＋WRAPPER 44009→44076，全部 +67。
  - Pristine 反證：text125 FAIL(1)、travel114 FAIL(27)。

## 實駕（`qa145/drive145.py`，port 8966，`?softPreview=1`，0 pageerror／0 HTTP404）

430×932＋430×700，三輪（第一輪捉到 B3 競爭規則問題；第二輪驗 B3 修正；第三輪驗標題修正）。流程：新遊戲（槽 3）→ 手帳 → B3 → B1 編輯功能 → B2 逐組切換 → 確定行程 → 鎖定量度 → 吊牌返地圖。截圖 `qa145/shots/`，量度 `qa145/drive145.json`。

- **B1 PASS**：700 鎖定態 **7/7**——週日頂 593／底 635，footer 頂 639（4px clearance）；標題／提示列 `display:none`；range margin 2px；footer 高 61px；印章 20px／54px 高／3px double 紅框。932 鎖定態 7/7，印章 24px／67px 高／footer 84px，標題／提示列照舊可見。
- **B2 PASS**：10 組 pane（含事業三組對照＋progress）journal-scroll computed bg 全部 `rgb(243,230,200)`；PIL 抽色核實 14 個 pane 抽色點（7 組×2 屏×2 點）全部準確 `(243,230,200)`；四組 subtab＋plan 組逐個切換，紅墨圈跟 active 郁（全部 `circleFollows=True`）；淺字覆寫已落地（ledger-enroll／people-next `rgb(107,78,46)`、debt pane-intro `rgb(90,67,40)`、rumor pane-intro 深字＋米紙底）。
  - **目視捉到一鑊（第二輪後補修）**：庫存 pane 頂「庫存」h3 淡到幾乎睇唔到——放大 crop 核實＋grep 確診係 4979 行 v76 `.jobs72-h{ color:#ecdfc2; }` 蓋走 4915 行深色，v131 只修返 works 一頁。補修後第三輪 drive：inv／people `.jobs72-h`＝`rgb(67,48,28)`（#43301c）、progress `.prog71-h`＝#43301c、`.prog71-intro`＝`rgb(138,117,90)`（#8a755a），全部墨色。
  - 剪報／庫存空狀態截圖目視：細紙卡坐喺成片紙面上面，唔再浮喺深色上面。
- **B3 PASS**（第二輪後）：未選 chips bg `rgb(251,243,223)`（#fbf3df）＋字 `#3a2e22`＋radius 3px＋邊 `#b99b62`＋Kaiti 字體；選中 bg `#fdf6e0`＋字／邊 `#c0452c`＋inset 紅影；排入掣同套。picker 開合正常；撳「台風」chip，`.on` 跟住郁；未報名提示句（`train73-zero`）在場；經 live `S` 掛 `S.enrolled={train_stage:true}` 後重開 picker，出「全日排呢堂」掣，撳落去七日全部變「台風訓練」，還原返原狀。
- **回歸 PASS**：五大 tab 58×38／58×32；備忘紙 live（銀包 `$12,000`／聲望 5／信用 10）；吊牌返地圖；全日休息／清空／還原全部正常；鎖定態還原隱藏。

## 唔郁嘅位

- SAVE key／softRev／產品 `?v=`／content pack JSON 零改動；C1–C2（頂部 HUD、地圖熱區描邊）留返原生版；事業組回憶 pane（v142 範圍）唔郁；v143 review「已證實唔係問題」一節嘅誤讀項一律冇修。
- 取捨：chips 字體維持 .72rem（2116 行 `!important` 唔郁，密度不變）；`.weak-whisper` 鬼影字故意保留淡化。

## 落地（2026-11-13 統籌）

- Squash 合併入 main：`57d4081`（分支 `v20a145` 337ac8c，基底 79defe3，零衝突；唔開 PR，git 直接合併）。
- 線上核實：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/index.html — **5,223,215 bytes、sha256 `2bf503a2…`，同 repo 一致**（部署約 2 分鐘後覆核，首查仍係舊版 5,217,690 bytes）。
- 設計 review 待派（新常規）：v145 落地後做一次設計 review，只出報告唔改 code。
