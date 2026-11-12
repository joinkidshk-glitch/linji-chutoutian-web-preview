# NOTES_V20A141 — 手帳去網頁感（B 式文件夾 tab＋備忘紙＋吊牌＋印章）

用戶 2026-11-12 22:10 拍板揀 B（文件夾式標籤）。樣本 `~/workspace/linji-handbook-sample/sample_v2b.html` 照抄數值搬入遊戲。

## 改咗邊幾處（index.html，基底 main bcac846）
- **SVG defs**（`<body>` 後，約 L5353–5365）：`ink141`／`inkSoft141`（feTurbulence＋displacement，樣本參數原封）。檔內本無 feTurbulence／`id="ink"`，無撞名。
- **CSS 段**（`</style>` 前，約 L5308–5351，`/* === v20a141 BOOK141 === */`）：全部五點樣式。手寫字體棧 `"Kaiti TC","STKaiti","KaiTi","Noto Serif CJK TC",serif`。
- **HTML**（約 L5523–5533）：`.home-top` 入面 `#home-stats` `<p>` 刪除，改做 `.memo141-row`（`.memo141#home-stats`＋`.tagwrap141#home-tab-exit` 吊牌 `#home-back-map-tabs`）。id／`book70ExitHome` handler／`data-hgroup`／`role=tab`／`aria-selected` 不變。
- **JS enterHome**（約 L37218，`hs.innerHTML`）：三行備忘紙，同一數據源（`S.money`／`syncDualTracks(S)`），保留 `.home-money`（`refreshMoneyHud` 刷錢）＋`h-stage-volume`／`h-industry-credit` id。唔寫死樣本數字。
- **JS 其餘**：無改動。`syncHomeTabExit` 唔使郁——吊牌窿用 `::before`，`textContent = "返回地圖"` 清唔走佢。

## 五點對照
1. **B 式 tab**：`#home-tabs` 紙面 strip（`#f5eddc`，margin 歸零貼住 pane 頂）；tab 58px 闊、未選 32px 高 manila `#e9dcbc`、選中 38px 高同紙面色、底部伸出 1.5px 截斷分隔線（`#home-tabs::after`）；舊金底線 `.on::after` 蓋走。tab 列＋subtab 列共用一張紙面，量度：memo 底 200／tabs 199–250／subtabs 250–288／notebook 頂 288——零深色間隙。
2. **進度／行程手寫行**：只限 `data-hsubgroup="plan"`——17px 手寫字，「進度」褪色 `#a08a68`，紅墨圈係 `.on::after` SVG 背景，圈跟 `.on` 郁（實駕：行程→進度→行程，圈跟住郁）。其餘四組維持 pill。
3. **備忘紙**：和紙膠帶＋微斜＋三行手寫（銀包 `$` 紅波浪底線、幕前聲望、業內信用）＋右下角「偉」字紅印。實駕新遊戲：銀包 `$ 12,000`＝`S.money`，聲望 5／信用 10（live 值，唔係樣本 $12,927／5／11）。
4. **吊牌**：`#home-back-map-tabs` 102×38（computed 102×38；rect 104×42 係 parent 斜 2.5° 嘅 AABB）、`#c9a876`、clip-path 吊牌形、繩圈＋窿（`::before`）。撳落去返地圖正常。
5. **印章**：`#btn-confirm-plan.is-locked` 先變印章（`#c0452c` 3px double、斜 -4.5°、24px、letter-spacing .32em、紙面底 `#nb-actions:has(.is-locked)` 轉 `#f5eddc`）。未定嗰陣係原有金色「確定本週行程」掣，唔出印章；「還原」鎖定態照舊隱藏（editable 先見到）。

## 舊規則搶贏兩鑊（實駕 probe141 捉到，已修）
- 吊牌闊：舊 5143 行 `width:auto !important` 蓋走 102px → 闊加 `!important`。
- 印章框：舊 904 行 grouped 規則 `border:2px solid var(--ink) !important`（連 radius／shadow 都係 `!important`）蓋走 3px double 紅框 → border／radius／shadow 一併加 `!important`。修前實駕見深色幼線框，修後量度 `borderTop: 3px double rgb(192,69,44)`。

## 測試
- 新：`tests/test_book141_static.py`（27 斷言）＋`tests/test_book141_logic.js`（7 斷言，兩組唔同 S／dual 值驗 live）。反證：pristine main（bcac846）跑，static 11 FAIL／logic 1 FAIL。
- 全套（`qa131/run_suite.sh`）：基線 **PASS 194／FAIL 12**；本票 **PASS 196／FAIL 12**（FAIL 清單完全一致，12 個係 pristine 已有；+2 係新測試）。中途有一次套件跑出 `test_wrap38_logic.js` FAIL，單獨重跑 4 次全 PASS＋全套重跑回復 196／12，判定 flaky（同本票改動無關——該檔直接跑＋重跑全套都 PASS）。
- 舊測試 rebase（純行號漂移，內容對位核實，唔改語義）：`test_map54_static.py`（allowlist 加 v20a141）、`test_text125_static.py`（三個錨點 +60：27631／27744／33342）、`test_travel114_static.py`（釘行 +60／+62 兩段：CSS ＋42／SVG ＋13／HTML ＋5／enterHome 註解 ＋2；FREE 27＋COUNT 13＋DEF 53143＋WRAPPER 43938）。

## 實駕（`qa141/drive141.py`，port 8962，`?softPreview=1`，0 pageerror／0 HTTP404）
- 430×932：五 tab 58×38／58×32 量度啱；五 tab 逐個撳→plan／works／ledger／rumor／debt pane 啱；進度／行程切換圈跟住郁；備忘紙數字啱；吊牌返地圖啱；editable 無印章＋還原可用；locked 有印章（y 858–925，一屏內）＋還原隱藏；七日全見。
- 430×700：同上全 PASS；editable 見三日全＋週四頭（要捲先見其餘；樣本 v2b 話三日全＋週四半，遊戲日行高啲，少半日，合理）。
- 截圖 `qa141/shots/`：`141_932_editable.png`、`141_932_locked.png`、`141_700_editable.png`、`141_700_locked.png`、`141_932_progress.png`、`141_700_progress.png`、`141_932_map.png`、`141_700_map.png`；量度 `qa141/drive141.json`；probe `qa141/probe141.py`。

## 同樣本唔同而取捨嘅地方
- 樣本 tab 喺書入面有左右 inset（54／40px）；遊戲 tab 列貼齊 `.home` 左右邊（10px padding），五隻 58px 置中——選中 tab 照樣駁住下面紙面＋notebook，視覺已連續。
- 其餘分類 pane（近況／消息／人情）嘅 journal-scroll 底仍係舊底（v131 只將事業三頁改做筆記紙）；tab 紙面 strip 同 pane 之間 margin 歸零直接駁住，無深色間隙，但 pane 內容本身唔係紙面——同「內容面板本身唔郁」一致。
- 印章喺 locked 態先出嗰陣，`#nb-actions` 底轉紙面色；editable 態底部保持原有深色 bar＋金色確定掣。
- 手寫字喺 Linux 截圖用 Noto Serif 渲染（已知限制，iPhone 出楷體），唔當 bug。

## 紅線
SAVE key／softRev s107／產品 `?v=` v20a10 不變；content pack JSON 唔郁；index.html 註解無其他測試硬計嘅版本字串。

## 落地紀錄
- main `4667ae0`（git 直接合併，冇開 PR），基底 bcac846。
- 線上核實：index.html 5,193,778 bytes、sha256 `5b5aabbc0a29c5d1378a7bbf3339976ffbff6b034805a8bb98241dabcb6cdba9`，同 repo HEAD 一致；`memo141` 12 處。
- 測試：全套基線 194／12 → 本票 196／12，FAIL 清單完全一致，零回歸；新測試反證：pristine static 11 FAIL／logic 1 FAIL。
- 實駕：430×932＋430×700 五點全驗（B 式 tab、備忘紙 live 數字、吊牌、印章只喺鎖定態、五 tab 切換、進度／行程圈跟住郁），見 `qa141/drive141.json`。
