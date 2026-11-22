# v20a376 — 第三輪評估第一波修正（U4／U3／U5／U2／U1）

來源：`linji-playtest-eval3-2026-11-22/REPORT.md` P1 第 4–8 項（工人測 v373）。
證據：`~/workspace/linji-drive376/`（probe376b／verify376 數據＋截圖＋GPT 原稿 `gpt_u3.txt`）。

## 1. U4 對白被「下一句」掣遮 11px — 核實已修，唔使改 code

v375c（`e302f6c`）聲稱已修。Playwright 實駕 live v375 N1 逐句量度（8 句）：
plate padding-bottom = 96px，對白文字底邊 748.9、掣頂 792，間距 **+43.1px**，零遮擋。
證據：`u4_n1_first.png`／`u4_n1_later.png`＋`probe376b.json`。本版零改動。

## 2. U3 modal 冇紙底 — 已修（FIX376-2）

根因（實駕 DOM 量度證實）：紙底規則寫成 `#mask:not(.tut-on) .modal{background:#F2EBD8 !important}`，
教學態 `#mask.tut-on .modal{background:transparent}` 本意畀教學卡（`.tut-card` 自帶紙底）浮起，
但 tut-on 期間開嘅通用 modal（日結／請柬／作品詳情）全部食晒透明底，深色標題壓喺變暗地圖上。
W3 三種 modal 實測 `rgba(0,0,0,0)` 全部係 tut-on 態。

修法（GPT-6.2-sol 諮詢後，方向二紙本手帳；原稿 `gpt_u3.txt`）：
- L457 透明規則收窄做 `#mask.tut-on .modal:has(.tut-card)`（只限教學卡 modal）。
- 紙底規則加第二選擇器 `#mask.tut-on:not(.story-play-on):not(.paper-on) .modal:not(:has(.tut-card)):not(:has(.sp-result))`——story-play 深底／報紙實物／sp-result 票根各有專屬底，唔搶。
- `#modal-btns` 喺 tut-on 係透明，modal 補紙底後透出嚟就係紙色，唔使另改（GPT 同意共用同一張紙）。
- 定位唔郁（day-res 底錨係 v197 拍板，唔跟 GPT 置中建議改）。

驗證（本地 build 實駕）：plain／tutOn／dayResTutOn = `rgb(242,235,216)`；tutStory = `rgb(10,7,5)`（深底保留）；tutCard = 透明（教學卡保留）。

## 3. U5 黑剪影卡出唔到 — 已修（FIX376-3）

`enc79StandCandidates`：ENC105 黑剪影檔排喺藝員資料卡之前，剪影檔真係存在（Pages 200）會載入成功，卡永遠輪唔到。
修法：卡 push 搬到剪影之前（卡係 data URI 必載入；剪影保留做卡之後兜底；淨 −1 行）。

同查另外兩條鏈：
- StoryPlay `spDlgCharsHtml`（dlg106Candidates＋bust）：無圖星 bust 404 走盡候補經 `__dlg106Err` 出卡，路徑本身通，唔使改。
- WF4 `wf4DlgExtraCands108` 只補 awi，WF4 事件以阿偉為主，唔使改。
- `__dlg106Err` 卡兜底（dataset 守衛）維持不變。

驗證（本地 build，抽 live 函數 eval＋真網絡 img 鏈行）：五位無圖星（胡美琳／韓秀婷／江詩盈／沈映雪／藍若曦）cardIdx=2 < silIdx=3；
胡美琳鏈行實測：stand/bust 404 → 第 3 個候補 data URI 卡載入成功（idx=2）。

## 4. U2 CMT commit 閘唔查 BE 旗 — 已修（FIX376-4）

BE 記錄口徑：`flag_<line>_be`（BR89 六線）＋葉敏芝 crisis 路線旗 `flag_yip_be_route`。
`commit48Available` 補 BE 檢查（crisis 檢查之後）：BE 旗有就唔出 commit offer，六線全覆蓋（relKey→line 推導）。
舊版只查 commit 旗，BE 後約會刷 rel 可繞道 HE，違反「BE 唔解鎖」拍板。

驗證（本地 build 抽 live 函數 eval，crisis done＋rel 6＋鎖定本人＋1992 秋 stub）：六線 noBE=true、BE=false 全中。

## 5. U1 結局感情場景缺四條線 — 已修（FIX376-5）

`endingRomanceScene410` 舊版只有曉晴／采兒 commit＋藍／徐／曉晴／采兒 almost；
藍／徐／葉／蘇 commit＋葉／蘇 almost 跌返單身文案，同 v371 總結行（六線全映射）自相矛盾。
補 6 場：commit 藍（錄音室企出嚟）／徐（中環廣告大堂）／葉（選美後台企你嗰邊）／蘇（灣仔唱片大堂），
almost 葉／蘇（he/be 分版跟 BR89 口徑）。旁白香港書面語、對白廣東話；HE 明寫「正式成為情侶」。

驗證（本地 build 抽 live 函數 eval）：四 commit 場景 couple=true／solo=false；兩 almost solo=false；單身／曉晴 sanity 不變。

## 釘 resync

index.html 淨 +23 行（48601→48624）：U1 +22（L13833 起）、U2 +2（L26520 起）、U5 −1（L41816 起）；U3 同行改寫零漂移。
9 檔釘 resync（difflib 映射＋內容逐字核實，腳本 `linji-drive376/resync376.py`／`resync376b.py`）：
gift185／tang171／tang173 總行數鏈（＋v376 +23）、tang171／173 openLoc DEF 43803→43826、
rom159 4 釘＋全佳 26580→26604、rom176 5 釘、tang152 2 釘、text125 ls[17009]→ls[17031]、
travel114 COUNT 14＋FREE 40＋DEF 43803→43826＋WRAPPER 30303→30327、mask146 選擇器字串。
逐個直接跑全部 PASS。

## 紀律

唔改玩法結構；SAVE key／softRev／產品 ?v=／贏線 0.875／floor 140／warnLine 180 一概唔郁。
