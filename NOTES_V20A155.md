# NOTES_V20A155 — v142 design review B1＋B2＋B3 修復

分支 `v20a155`，由常駐 clone main `e08a070`（v20a148）開出。
**注意 main 已郁**：開分支後 v156（`0c7ebbb`）同 v151（`86e391d`，現 HEAD）先後落地，
rebase 嗰陣要留意；v151 訊息話「行號 resync +15 跟 v156」，呢票改動嘅行號（v20a41 註解約 L4193、
prog71 CSS 約 L4878、.md97 約 L5151）rebase 後要核對。
**Rebase 已完成（統籌，2026-11-13）**：rebase 上 main `9346a8e`（v151 NOTES，含 v156＋v151），新 commit `9b74967`；
index.html diff 同原本逐段一致（B1／B2／B3 三段，淨 ＋17 行）；`test_text125_static.py`／`test_travel114_static.py`
衝突（兩版都 resync 過行號），取 main 版再全部錨點 ＋17（text125：27815→27832、27928→27945、33550→33567；
travel114：DEF 53601→53618、WRAPPER 44205→44222，COUNT 13／FREE 27 不變），三份測試重跑全 PASS；
行號對照：B1 註解 L4226、mask rule L4232（舊 L4211）、modal-inner L4239（舊 L4218）；B2 註解 L4899、
prog71-row L4910；B3 註解 L5180、venue99 rule L5182、.md97 光暈 rule L5178–5179（舊 L5151）。
全套重跑見 §4 補充。
工作副本 `~/workspace/linji-work155/`；pristine 對照 `~/workspace/linji-pristine155/`（e08a070 detached）。
本票只改 `index.html`（CSS＋一處註解），唔改 SAVE key／softRev／`?v=`／content pack JSON／文案／幕次序。

## 0. 實駕重現（pristine，開工前）

驅動 `probe155.py`（`shots155/`、`probe155.json`；Playwright＋本地鏡像，430×932／430×700，`?softPreview=1`）：
新遊戲 → 何生事務所 → 返回地圖 → 進度頁 → 播呢幕（C1）→ 行到中段量度。0 pageerror／0 404。

### B1 根因（實測，唔係估）
- `.sp-stage` x30 y10 w370 h900，底緣 910；`.modal` x30 y10 w370 h912，底緣 922；
  `#mask` x20 y0 w390 h932，底緣 932。罅＝舞台底 910 → viewport 底 932，共 22px。
- 逐層計得 `#mask` padding:10px、background `rgba(0,0,0,0.72)`；`#modal-inner` padding-bottom:12px；
  `.story-play` height:100% → 900（＝modal-inner 內容高 912−12）。
- 底帶像素（2x 截圖，pristine）：y910–920 深色約 (10,7,3)；**y922–930 暖灰 (71,69,63)**——
  半透明 mask（0.72 黑）下面透出淺色寄語卡，正係 review 嗰條罅。
- CDP `getMatchedStylesForNode` 證實：`#mask.story-play-on{padding:0;align-items:stretch;background:#0a0705 !important}`
  （L4232）**完全唔喺 matched rules 入面**，但同段嘅 `#mask.story-play-on .modal`／`#modal-inner` 有入。
  根源係 v20a41 大註解提早閂咗：`/* === v20a41 …` 開咗之後，「已申報）。」句後多咗個閂標記，
  後面十行散文跌出註解、併入下一條 rule 嘅 prelude，成條 L4232 rule 靜默失效。
  佐證：style 區塊 `/*` 431 個、`*/` 432 個——多一個閂標記。v20a42 以為加 `!important` 修好咗，
  其實條 rule 從來冇生效過。
- 第二個根源：L3506 `#mask:not(.casting-sheet-on):not(.tut-on) #modal-inner{padding-bottom:12px;}`
  specificity (2,2,0) 贏 L4239 `#mask.story-play-on #modal-inner{padding:0}` (2,1,0)，
  12px 令 `.story-play`／舞台矮咗 12px。

### B2 實量（932，pristine）
- 捲動器 `#progress-list.journal-scroll`：scrollH 772／clientH 642（在場態）／724（唔在場態），可視底 930。
- 寄語卡 `.prog71-next142`：在場態 y921–1038（底超 108px）、唔在場態 y867–984（底超 54px）。
  在場態開局行高 117px（含「播呢幕」掣 40px＋margin 8px），唔在場態 69px——差 48px。
  每行實量：在場 open 117／locked C2 171（5 條件項，其中一項兩行）／locked C3 151／far 68；
  intro 40px（兩行）＋margin 10px；`.prog71-top` 高 24px。

### B3 實量（pristine）
- 會場標籤計得 color `rgb(122,92,51)`（#7a5c33）、opacity .88、光暈係 L5178 嗰條 4px／3px 版；
  15 張地點標籤 `.mn68` 係 #43301c／opacity 1。`.md97` 元素全檔只得會場標籤一個（12 個地區名已刪）。

## 1. B1 — 舞台底罅（修法 a：舞台加高冚罅）
- 刪走 v20a41 註解「已申報」句後多餘嘅閂標記，等成段散文返入註解，L4232 rule 恢復生效
  （mask padding:0、background #0a0705 不透明）。註解平衡返 432／432。
- L4239 `#mask.story-play-on #modal-inner` padding 加 `!important`（贏 L3506），
  故事作用域內 modal-inner 底 padding 歸零；L3506 通用 rule 唔郁，其他 modal 嘅 12px 照舊。
- 量度後（932）：stage／modal／mask 全部 x20 y0 w390 h932，底緣 932＝viewport 底，罅清零。
  mask 計得 background `rgb(10,7,5)`、padding 0；modal-inner padding-bottom 0px。
  elementFromPoint（215, y915／921／928／931）全部返 `.btnrow`「下一句」（modal 內掣），
  再冇 mask／下層元素。底帶像素：y912–928 平均 (15–20, 10–12, 5–7)，max brightness ≤22——
  舊 (71,69,63) 暖灰帶消失。
- 700 核實：stage h700＝viewport，唔頂穿；plate y516 h118 bottom 634；行文零溢出；0 pageerror。
- 對話框遮腿比例：plate 底永遠＝舞台底 −66px（`sp-stage-inner` 底 padding 唔郁），
  企立圖（`.dlg106-char`）遮蓋像素 932：94→91px、700：117→114px；
  佔企立高比例 932：19.1%→17.4%、700：29.2%→27.1%——企立圖隨舞台加高咗，腳繼續匿喺牌後面，
  視覺上同之前一樣（截圖 `155_b1_story_932.png`／`155_b1_story_700.png` 目視確認）。
  實量對照（同一句中段）：

  | | 舞台 | plate | 企立圖（左／右） |
  |---|---|---|---|
  | 932 pristine | y10 h900 底 910 | y726 h118 底 844 | y329 h491 底 820 |
  | 932 工作版 | y0 h932 底 932 | y748 h118 底 866 | y317 h522 底 839 |
  | 700 pristine | y10 h668 底 678 | y494 h118 底 612 | y210 h401 底 611 |
  | 700 工作版 | y0 h700 底 700 | y516 h118 底 634 | y210 h420 底 630 |

## 2. B2 — 進度頁寄語橫跨摺線（上面收窄，唔碌）
- 十處小收窄（只改 `.prog71-*`／捲動器 padding，文案／幕次序／寄語卡本身一字唔郁）：
  行 padding 9→4px、行距 8→5px、intro margin 10→6px＋行高 1.6→1.5、
  條件 ul margin 8→6px、li 行高 1.55→1.4、note 行高 1.55→1.45＋margin 6→5px、
  播掣 min-height 40→36px＋margin-top 8→6px、標題 margin 4→2px、
  捲動器頂 padding 4→2px、wrap 頂 padding 2→0、幕頂行高 1.3。
  預算約 110–116px（在場態要 108px、唔在場態要 54px）。
- 量度後（932）：在場態寄語卡 y810–928（底緣 928，可視底 930，餘量 2px——兩次獨立跑都係 928）；
  唔在場態 y766–883（餘量 47px，scrollH 642＝clientH 642，成頁唔使碌）。
  行高：在場 open 97／locked 144／126／far 53（之前 117／171／151／68）。
- 700：寄語卡 y810–928（摺下，同之前一樣要碌；scrollH 772→661，碌少咗，冇變差）。
- 截圖 `155_b2_progress_932.png`（在場態）目視：寄語卡成塊見晒，兩段文完整，行距唔覺迫。
  （註：在場態餘量得 2px，係逐像素計嘅最緊態；如果之後開局行再加內容，會第一個跌穿。）

## 3. B3 — 會場標籤對比弱
- L5178 嗰條 `.md97` 光暈 rule 後面加 `.md97-venue99` 專用規則：
  color #43301c、opacity 1、text-shadow 跟 `.mn68` 同級（0 0 3px ×2＋1px 2px 四向）。
  字體大細／字距／位置唔郁；`positionMapLabels137` 位置邏輯唔郁；base `.md97` 唔郁。
- 量度後：932 標籤 x25 y326、700 標籤 x32 y217（同 pristine 一模一樣）；計得 color `rgb(67,48,28)`、opacity 1。
- 對比度（WCAG luminance）：#43301c on #f3e7c8 光暈 **10.17:1**（舊 #7a5c33 係 5.01:1）；
  冇光暈直接印喺地圖中間色上面：5.37 vs 2.65。截圖 zoom 目視：深啡字＋米紙光暈，同隔籬標籤同級。
- 15 地點逐針實撳：932 15/15、700 15/15（獨立 fresh session，`case_pins`）。

## 4. 測試
- 新測試 `tests/test_v155_static.py`：27 項，工作版 **27/27 ALL PASS**；
  對 pristine（e08a070）13 項修復斷言乾淨 FAIL（B1×3、B2×8、B3×2），其餘基線斷言 PASS，唔 crash。
  斷言全部用字串匹配，冇寫死行號（rebase 唔使 resync；但 B1 嗰兩條 rule 嘅行號郁咗要人手核對見 §0）。
- 行號 resync（本票淨加 17 行引起，唔係內容回歸）：`resync155.py` difflib 對位核實——
  新舊 index.html 只差 B1／B2／B3 三段，硬計行號錨點全部純漂移、內容逐行相同、劃一 ＋17。
  跟住 resync 咗兩份舊測試（跟返 v146／v147 嘅做法，行號＋註解歷史一齊改）：
  `tests/test_text125_static.py`（currentLine 27800→27817、advance 27913→27930、
  familySafe 33516→33533）同 `tests/test_travel114_static.py`（FREE 27 處／COUNT 13 處／
  DEF 53562→53579／WRAPPER 44171→44188）。兩份 resync 後各自直接跑 RESULT PASS。
- 全套 `qa131/run_suite.sh`（A＝pristine `linji-pristine155`，B＝工作版）：
  A：**211 PASS／12 FAIL**（12 項全部 pre-existing，見 `suite155_pristine.txt`）。
  B：初跑 **210 PASS／14 FAIL**——多出嚟嗰兩項就係上面未 resync 嘅 text125／travel114
  （同一版工作版跑兩次都係呢兩項，唔係波動；舊版 /tmp 跑亦一樣）。
  resync 後重跑 B：**212 PASS／12 FAIL**（`suite155_work2.txt`）。
  FAIL 清單同 A 逐項一致（flash51、giglib36、pacing35、poster59、rumor49、slot50、
  soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38——全部 pre-existing），
  淨差異係多咗 `PASS tests/test_v155_static.py` 一行。零回歸。
- **Rebase 後重跑（統籌，基於 main 9346a8e）**：JS loop **97 PASS／0 FAIL**；PY loop **118 PASS／12 FAIL**——
  多出嚟嗰第 13 項 `test_kwan151_static.py` 係 v151 測試行號未 resync（錨點全部喺 v155 插入點之後，純漂移），
  resync ＋17 後 ALL PASS；其餘 12 項 FAIL 同上面 pristine 清單逐項一致。合共 **215 PASS／12 FAIL，零回歸**。
  （注意：第一次全套誤用 `bash qa131/run_suite.sh` 唔帶參數，OUT 寫唔到，得 190/37，作廢；另有一次 service
  restart 期間 SIGTERM 中斷，之後分 JS／PY 兩段重跑。分段 OUT：`suite155_js2.txt`／`suite155_py2.txt`，留喺工作副本未入 commit。）

## 5. 實駕證據（本地鏡像＋Playwright，0 pageerror／0 404）
- `shots155/155_b1_story_932.png`、`155_b1_story_700.png`：舞台冚全屏，對白完整，底帶全深色。
- `shots155/155_b2_progress_932.png`（在場態）、`155_b2_nothere_932.png`（唔在場態）：寄語卡成塊見晒。
- `shots155/155_b3_map_932.png`、`155_b3_map_700.png`：會場標籤深啡可讀，其餘 14 張標籤唔受影響。
- `probe155.json`（B1／B2／B3 量度）、`probe_b2.py`（兩態行高）、`probe_css4.py`（CDP matched rules）、
  `probe_pristine_b1.py`（pristine 對照）留喺工作副本，未入 commit。

## 6. 已知／留畀 parent
- B2 在場態餘量得 2px（見 §2）。
- main 郁咗兩版（見頂部），rebase 後要重跑靜態測試＋抽驗實駕。
- 18080 隧道已死：工作副本 `core.sshCommand` 已改行 `~/workspace/gh_tunnel.py`（跟常駐 clone 同款）。
