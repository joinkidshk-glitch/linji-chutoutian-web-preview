# v20a146 NOTES — WF4 舞台 modal 間歇性標題被切（A1）＋街市 banner 空白招牌（B2）

分支 `v20a146`，基底 main `f0ae995`（v136）。唔開 PR、唔落地（落地由統籌做）。

## 改動一覽（index.html，淨 +15 行）

### A1 — `.mask` 改 viewport 錨定（引擎層）
- `.mask{position:absolute;inset:0}` → `position:fixed;top:0;bottom:0;left:50%;width:min(390px,100%);transform:translateX(-50%)`（L427 起，連註解）。
  橫向繼續跟 `#app` 框（390px 置中），唔做 full-viewport 闊；`≥480px` 上下貼齊 `#app` 框（`top/bottom:14px`），
  `≥900px` 跟 468px 框＋desktop-rail 偏移（`left:calc(50% + (min(220px,22vw) + 22px)/2)`，rail 喺 `#app` 之前）。
  `align-items:flex-end` 唔郁，全部 modal 繼續行 bottom-sheet；`#mask.tut-on` 置中、`day-res` 規則唔郁。
- modal 高帽加 `svh` 後備（`#mask:not(.tut-on) .modal` 78svh、矮屏 media 88svh、`#mask.tut-on .modal` 88svh）：
  dvh 誤報偏大嗰陣 modal 唔會高過細 viewport。基底 `.modal` 嘅 `min(78dvh,720px)` 原封不動做 fallback；
  `#mask.story-play-on .modal` 刻意唔郁（ui133 釘死 `min(78dvh,720px)`，且呢句冇 `!important`，實際由上面高帽管）。
- `WF4_SCENE_OVERRIDE134` 唔郁；SAVE key／softRev s107／產品 `?v=` v20a10 唔郁；`content/` JSON 唔郁。

### 機制（已證實，修正 v134 review 嘅 dvh 猜測）
- 盤點：得一個 mask 元素（`<div class="mask" id="mask">` L5689），全部 modal（約 80 個 `modal()` 呼叫點：
  WF4 舞台＋卡片、主線／巧遇 StoryPlay、報紙、頒獎、殺青、試鏡、教學、存檔／設定、日結、通告欄、人情／醫院／傳聞等）
  共用同一個 mask，經單一 choke point `modal()`（L39152）開關。手帳係 view、loc-sheet 係 `.sheet`，唔經 mask。
- 根源唔係 dvh：`#app` 係 `overflow:hidden` 但 `scrollHeight` 超高（實量 916 vs client 700），
  `openLoc` 嘅 `scrollIntoView`＋`modal()` 嘅 `focus()` 會將 `#app.scrollTop` 推到 0–537（視流程而定）；
  absolute mask 喺 `#app` 入面，bottom-aligned modal 跟住上移。`scrollTop=216` 嗰陣 modal y=149→-67、h3 y=-53，
  同 v134 review 壞例數字逐 px 吻合（`qa146/probe146_scroll.py` 喺 pristine 上重現到；修好版同一操作 modal 唔郁，y=149）。
- v142（main 落地嗰陣先至知，見 MEMORY 00:30 更新）喺 S-30 A1 證實同一機制，嗰邊用防禦性歸零 `scrollTop`；
  呢度結構性改 `fixed`，同 v142 互補唔衝突。合併嗰陣兩邊可以共存；fixed 令歸零對 modal 定位變得多餘但無害。

### B2 — 街市 banner 偏向檔口帶
- `wf4PlayEvent` 生成 `sceneHtml105` 嗰度按圖分流（L40529 起）：得 `bg_wf4_market.jpg` 先加
  `background-position:center 75%`（inline style）；set08（`bg_loc_film_lion`）／st04（`bg_loc_cafe_cha`）唔加，
  共用 `.wf4-scene105` 嘅 `background-position:center` 唔郁；舞台版 `sp-bg-layer` 唔郁。
- 75% 係實測甜點：圖 720×1280，banner 342×150 橫裁；50%（現狀）裁到招牌帶＋檔口頂，75% 裁到原圖 y 723–1038
  （簷篷＋菜／魚檔），85% 冇咗簷篷、65% 仲見招牌角。五單 market 事件（st06／st07／st11／day03／day04）
  全部行卡片版（無阿偉 beat，唔行舞台），所以舞台版街市圖唔存在，無變差可言。

### B1 — st05／st08 補圖（統籌接入，v146 第二部分）
- 新圖 2 張（美術工人出，參照＋QC 見 `~/workspace/linji-wf4scenes-refs/SOURCES.md` v146 一節）：
  `assets/story/locs/bg_wf4_karaoke.jpg`（159,930 bytes，卡拉OK包廂：CRT 空白畫面、鐳射影碟機、有線咪、紅皮梳化）＋
  `assets/story/locs/bg_wf4_taxi.jpg`（121,125 bytes，的士車廂夜景：後座視角、右軚、模擬咪錶、木珠椅套，窗外啟德跑道燈＋低飛 747）。
  兩張 720×1280、無字無人無水印、時代啱 1990–92；落選版留喺 `qa146/`（唔入 assets）。
- 接入：`WF4_SCENE_OVERRIDE134` 加 2 行（`wf4_ev_st05 → bg_wf4_karaoke.jpg?v=20a146`、
  `wf4_ev_st08 → bg_wf4_taxi.jpg?v=20a146`）；覆寫表註解更新（16／18 → 18／18，無留灰）。
  行號影響：覆寫表 ＋2 行（約行 40463 後）；travel114 錨點 ≥40463 者 ＋2（`qa146/resync_b1_146.py` difflib 對位核實純漂移，
  DEF 53417→53419、WRAPPER 44102→44104）；text125 三錨點全部喺表之前，＋0 不變。
- 測試：`tests/test_ui134_wf4scene_static.py` 更新（覆寫表 18 單、留灰 0、新圖格式檢查加 2 張）。
  反證：更新版喺 pristine main `79defe3` 上乾淨 FAIL 5 項（表 16 單、留灰斷言、st05／st08 入表、2 張新圖唔存在）；工作版 TOTAL PASS。

## 統籌補記（rebase 上 79defe3，B1 接線後）
- 全套：baseline（pristine `79defe3`，`git archive` 抽出）PASS 207／FAIL 12；工作版 PASS 208／FAIL 12——
  只加 mask146 一個 PASS，FAIL 清單逐項對過完全一致（12 項全部 pre-existing，同上）。
- main 其後再行前（v145 落地，main `57d4081`＋NOTES `f45e766`）：v145 加咗 2 個新測試（test_book145_*）
  ＋index.html ＋69 行（手帳 B1／B2／B3），所以要第二次 rebase 上 `f45e766` 先至落地；行號測試要再 resync 一次。
- 第二次 rebase 已完成（統籌核實）：兩個 v146 commit 喺 `f45e766` 之上（`5a276ab`＋`3f2df37`＋補腳本 `3135ccf`）；
  index.html diff 核實同原本 v146 diff 逐字相同；travel114／text125 再 resync（零非漂移錨點，DEF 53484→53486、WRAPPER 44169→44171）；
  五個關鍵測試（travel114／text125／mask146／ui134／book145）喺最終樹上全部 PASS。
  **數字糾正**：f45e766 新鮮 baseline 係 209／12（統籌親自量過），工作版應為 210／12（209＋mask146）；
  之前工人話 baseline 209 係誤讀 v145 NOTES（嗰個 209 係 v145 分支數，佢哋當時 pristine 79defe3 係 207／12）。

## 統籌補記（終驗＋落地受阻，環境故障）
- **環境寫入故障**（2026-11-13 ~17:07 起持續）：VM 寫入間歇性 `Operation not permitted`（EPERM），時好時壞——
  `git archive`、`tar` 解壓、`git commit`（loose object）全部失敗過；新鮮 baseline 全套因此量唔到。
  替代證據：v145 NOTES（pristine 79defe3 207／12）＋統籌親量 f45e766 baseline 209／12＋工作版全套 203／19（7 個額外全部係 tempfile 寫入錯誤，環境問題，唔係斷言失敗；12 個已知 FAIL 同 v145 清單逐項一致）。
- **終驗實駕跑唔到**：呢個 cell 嘅 Chromium 壞咗（兩個 binary 任何頁面都 SIGTRAP／SIGILL，連 `about:blank` 都死；`playwright install` 亦 EPERM）。
  終驗工人做到嘅唯讀驗證全部 PASS：mask146 24/24、ui134 TOTAL PASS、diff 核對三項齊晒、兩段 inline script Node `vm.Script` SYNTAX-OK、
  兩張新圖 PIL 視覺 QC 一致、街市圖 75% 帶視覺上確實係檔口帶。工人抽查開發者先前 QA 記錄（17:02，rebase 前）：
  A1 5×700 次次 modal y=149／h3 y=163、932 2×、scroll 探針穩定、tour 大致 PASS（唯一 T5 S-30 首次 `board:false`、retry PASS，似已知間歇性靜默吞點擊，唔似 v146 回歸）。
- **缺口**：B1 st05／st08 卡片 live-run 記錄未有（分支入面冇量度 JSON／截圖）；st08 有 `cond:{yearMin:1991}`，重跑要處理播種年份。
- **未落地**：git 寫入仍 EPERM（`git commit` loose object 失敗），兩支第二次 rebase 腳本（`qa146/resync_rebase146b.py`、`qa146/resync_b1_146b.py`）仍未追蹤入 commit。
  恢復後跟手做：commit 兩支腳本 → 重跑實駕（probe146_a1 5×700＋2×932、scroll 探針、cards＋B1 兩單兩 viewport、tour146）→ squash 合併 → curl 線上核實。
- 新測試 `tests/test_mask146_static.py`（23 斷言）：基線不變＋A1（fixed／desktop 對位／svh 帽／行為保留）＋B2（分流＋75% 唯一＋共用規則唔郁）。
  反證：喺 pristine main `f0ae995` 上行，14 項新斷言乾淨 FAIL（exit 1，唔 crash）；修好版 ALL PASS。
- 行號敏感測試 resync（我嘅插入淨 +15 行：MASK146 段 ＋8、modal 高帽註解 ＋2、B2 ＋5）：
  `tests/test_travel114_static.py` 經 `qa146/resync_travel114.py` 重算（44 個 `openLoc(` 呼叫點序列逐字一致、
  內容逐行相同，純漂移；COUNT 13／FREE 27 不變，DEF 53369→53384、WRAPPER 44054→44069；＜40529 者 +10、≥40529 者 +15）；
  `tests/test_text125_static.py` 釘行號重對（currentLine 27709→27719、advance 27822→27832、familySafe 33423→33433，實量核實）。
  `tests/test_ui133_wf4clip_static.py` 曾經 FAIL（我初版郁咗 `#mask.story-play-on .modal` 嗰句死規則）——已還原，PASS。
- 全套：baseline（pristine f0ae995）PASS 204／FAIL 12；修好版 PASS 205／FAIL 12——只加 mask146 一個 PASS，
  FAIL 清單逐項對過，同 baseline 完全一致（12 項全部 pre-existing：flash51／giglib36／pacing35／poster59／
  rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38）。

## 實駕驗證（Playwright，本地鏡像＋`?softPreview=1`，0 pageerror／0 failed request 全部環節）
- A1：day02 舞台流程 430×700 跑 5 次，次次 modal y=149、h=541、h3 y=163、bottom=185、mask y=0 h=700（修前同流程 5 次亦全好，
  壞態約 1/3 機率，修前未重現；決定性證據係上面 scrollTop 探針：pristine 設 scrollTop=216 即重現 y=-67／h3=-53，
  修好版同一操作完全唔郁）。430×932 跑 2 次，次次 modal y=269、h=653、h3 y=283。
- 其他 modal 抽查（全部 modal y ≥ 0、標題完整）：
  教學卡 430×700（modal y=226）＋1200×900（mask rect＝app rect，487,18,468×864，rail 偏移計啱）；
  「確認過一日？」y=493；日結「小休（週一）」y=355（`day-res` class 正常）；
  S-30 通告欄「通告欄 · 星河電視台」y=144、h=546（高帽 78dvh 生效，頂部照見）；
  地點板（事務所 sheet 正常開）、手帳（正常開）。WF4 舞台入場攔截嗰次（「飛紙仔殺到埋身」y=305）亦正常。
  未直接觸發：試鏡結果、殺青、報紙、巧遇對話——四者全部經同一個 `modal()`＋同一個 `#mask`，
  上面 6 種 modal 幾何已證，轉移成立；報紙（paper-on）喺日結流程未撞到，留待全弧驗證。
- B2：st06 卡片 banner 兩 viewport 計算值 `50% 75%`，截圖見菜／魚檔（唔再係空白招牌）；set08／st04 計算值 `50% 50%`，
  同 pristine 截圖 banner 區逐 px 對照：set08 差 106/51300 px（最大色差 9/255）、st04 差 78/51300 px（最大 7/255），
  屬渲染噪聲，實質無變；st06 同區差 50290/51300 px（預期之內，位置真係郁咗）。
- 機制探針：`qa146/probe146_scroll.py`（pristine vs 修好版，scrollTop=216 前後對照）。

## 檔案
- `index.html`（淨 +15 行：mask fixed＋desktop 對位、svh 高帽、B2 分流；再 ＋2 行：B1 覆寫表 st05／st08）
- `tests/test_mask146_static.py`（新）、`tests/test_travel114_static.py`（行號 resync ×2）、
  `tests/test_text125_static.py`（行號 resync）、`tests/test_ui134_wf4scene_static.py`（18／18 更新）
- `assets/story/locs/bg_wf4_karaoke.jpg`、`bg_wf4_taxi.jpg`（新，B1）
- `qa146/`：`probe146_a1.py`、`probe146_scroll.py`、`probe146_t5.py`、`probe146_cards.py`、`tour146.py`、
  `resync_travel114.py`、`resync_rebase146.py`、`resync_b1_146.py`、量度 JSON（`a1_*`、`scroll_*`、`tour146.json`、`t5_retry.json`）、截圖 `shots146/`
- 本 NOTES：`NOTES_V20A146.md`

## 未解決／要統籌決定
- 工作副本入面有唔屬於我嘅檔案（B1 並行工作）：`assets/story/locs/bg_wf4_karaoke.jpg`、
  `assets/story/locs/bg_wf4_taxi.jpg` 及 `qa146/gen_bg-wf4-*.jpg`／`media-generation-*.json`——
  係另一邊 B1 出圖嗰陣寫入嚟嘅，我冇掂過，**今次 commit 唔包佢哋**，落地嗰陣由統籌處理。
- main 喺我開工期間行前咗（v138／v142 已落地，v142 嘅 scrollTop 歸零同呢版 fixed 互補）；
  合併嗰陣要 rebase 上新 main，留意行號 resync（travel114／text125 釘行號要再對一次）。
- 試鏡結果／殺青／報紙／巧遇對話四種 modal 未喺今次實駕直接觸發（見上文），留待全弧驗證。

## 恢復嘗試受阻（2026-11-13 01:38，恢復統籌）
- 恢復統籌接手嗰陣環境檢查表面健康：git log／status 正常、identity 同 core.sshCommand 齊、Chromium 156.0.8078.4 正常出 version、touch 寫入 /tmp＋workspace OK、磁碟有 115G 空位。
- 但第一步 commit 兩支 resync 腳本即刻撞返同一故障：`git add` 後 `git commit` 報 `fatal: unable to write loose object file: Operation not permitted`（exit 128）；5 秒後重試，`git add` 寫入嘅 staged 狀態竟然消失咗——兩支腳本變返 untracked，`git commit` 報 `no changes added to commit`。即係話寫入故障唔止係大聲失敗，仲有靜默丟失（staged index 寫完唔見咗）。
- 結論：故障唔係上一手統籌個 cell 獨有，恢復統籌個 cell 一樣中招，而且係間歇性＋靜默丟失——喺呢個狀態下做 squash 合併／push 唔安全（就算 commit 表面成功都唔敢信佢真係落咗盤）。按指示停低，唔死 loop，等主 agent 決定（等 VM 恢復再試，或換個 cell／換條路落地）。
- 未做：重跑實駕（probe146_a1.py 5×700＋2×932、scroll 探針、probe146_cards.py、tour146.py）、新鮮 baseline 全套 vs 工作版全套、squash 合併＋push＋curl 核實。分支現況：`v20a146` 停喺 `3135ccf`，3 個 commit ahead of origin/main；兩支 resync 腳本（`qa146/resync_rebase146b.py`、`qa146/resync_b1_146b.py`）仍未入 commit；NOTES 呢個修改亦未 commit。
