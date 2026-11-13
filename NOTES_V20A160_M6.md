# NOTES — v20a160 M6 燕尾服阿偉（典禮贏分支限定）

- 分支：`v20a160-m6`（工作副本 `~/workspace/linji-work160-m6`，基底 main `e08a070`＝v148）
- 狀態：code＋測試＋實駕已完成並驗證。**唔落地、唔開 PR**（落地由統籌做）。SAVE key／softRev／`?v=` 一律無郁；無直改 content pack JSON；M4／M1／M9／M5 一律無掂。
- index.html：58,904 → **58,934 行（淨 ＋30 行）**

## 1. 落點決定——贏分支揭曉＋glamour，先至著燕尾服

- 錨點（`awards62PlayCeremony`，v147 狀態）：舞台 canvas 424×240、FLOOR=194、slotCx 置中 202／間距 72、玩家 Q 版高 50。
- **顯示 beats**：`reveal`（won 分支，2100ms 全程——行前 500ms 已經係燕尾服，唔等企定先換衫，免得中途爆衫）＋`glamour`（won＋有海報先有，1800ms）。合共約 3.9 秒台上時間。
- **唔著 beats**：`open`／`enter`／`names`／`suspense`（行入場＋唱名＋懸念嗰陣仲係 Q 版日常衫，等揭曉嗰刻先「上台」）；`out`（得個 fade，無人仔）；`gallery`（玩家根本唔上台，無 player slot）；`nominated`／`comfort`（落選，維持原樣）。
- **獎盃**：燕尾服原圖手臂垂低、本身無獎盃；企定捧杯嗰陣頭頂加 `drawTrophyGlyph`（沿用對手得主嗰套標記，金色獎盃 glyph，`FLOOR + fp.y - 64`）。行前嗰 500ms 無 glyph（行緊路）。
- **降級**：圖載唔到（`tuxRec.ok=false`）就跌返 Q 版 `awei`／`awei_hold`，唔穿崩；同 v64 剪影降級同一哲學。

## 2. 資產來源／解像度

- 來源：Pixellab state `7577440c-565f-4b64-9d2e-8b21d505ead3`（state 名「燕尾服頒獎」，由 v2 character `49907fa9-077f-4f59-aaba-45d3a06958fb` 開，job `dcbd831c-0d56-4be2-8c3d-12efb5de6190`，8 方向齊；樣本報告 `~/workspace/linji-work147/samples147/SAMPLES147_REPORT.md` M6 一節 PASS）。
- **唔准新生成，零花費**：先用 helper `export-spritesheet` 免費攞返成個 state（`qa160-m6/scratch/m6_export.zip`＋解開咗嘅 manifest；前後 `balance` 全部係 **4576／5000**，一毫子都無扣）。注意：samples147 嗰陣餘額係 4601，家下 4576——差嗰 25 次係其他工用咗，唔係我。
- **無更高清來源**：spritesheet 1296×288、每格 144×144，但格內原畫只係 128×128（south 格中央 128px 同 `m6_tuxedo_south.png` **逐像素一致**，已驗）。原生就係 128×128，**128px 上限**。
- 入 repo 檔案：`assets/awards/awei_tuxedo.png`（5,090 bytes，PNG 128×128，同樣本檔 byte-identical）。位置決定：新開 `assets/awards/`——佢唔係全身立繪（`assets/story/fullbody/`），唔係 fx 片（`assets/fx/`），係典禮舞台專用 sprite；檔名望落知係典禮燕尾服阿偉。
- 渲染幾何（`drawTuxedo`）：原圖人物佔框 x42–87／y13–115（45×102），腳底喺 y115。`dispH` 係成張圖顯示高度 64，腳底對齊 `floorY`（`top = floorY - dispH×115/128`），人物高 ≈ 51px，同 Q 版玩家 50px 齊高；影闊跟返 dispH 64。

## 3. 改動一覽（index.html，全部喺 awards62 區內）

- `AWARDS160_TUXEDO_AWEI = "assets/awards/awei_tuxedo.png"`（AWARDS64_SPRITES 之前，連來源註解）。
- `awards62PlayCeremony`：`tuxRec` 預載（`new Image()`，onload／onerror）；`drawTuxedo(cx, floorY, dispH)`；`drawFigure` 加 `o.dispH`＋`o.tuxedo` 分流（燕尾服成功先 return，失敗跌返 `drawSpr`）。
- `draw()` reveal won 區：玩家行前＋企定兩處加 `tuxedo: true, dispH: 64`；企定加 `drawTrophyGlyph`。
- `draw()` glamour 區：玩家加 `tuxedo: true, dispH: 64`（同揭曉同一套衫）。
- 其餘 beats／分支一字無郁。

## 4. 附帶：test_travel114_static.py resync（＋30 行漂移）

- M6 淨 ＋30 行全部喺 L46232–46501 之間，`test_travel114_static.py` 硬計行號要跟：行號 ≥46232 者 ＋30（DEF 53562→**53592**；WRAPPER 44171 不變；COUNT 5 處＋FREE 15 處＋30）。
- 核實 `qa160-m6/resync_travel114.py`（difflib 對位）：只得插入＋3 個 M6 區內改寫段（dispH 行改寫、reveal won 重組、glamour 行改寫），44 個 `openLoc(` 呼叫點逐字一致，42 個釘行內容逐行相同（6 個重複行按預期位置對位），純漂移。

## 5. 測試

- 新測試 `tests/test_awards160_m6_static.py`：**16/16 PASS**（資產在場＋PNG 128×128、常量指向、tuxRec 預載、drawTuxedo 腳底對齊、drawFigure 分流＋跌返 Q 版、reveal won 區＋glamour 區有 `tuxedo: true`、全 play 共 3 處、comfort 區／nominated reveal else 區／beats 定義無 tuxedo）。
- **反證**：同一測試對 pristine main（`~/workspace/pristine160m6`，`git archive e08a070`）：**13 FAIL／3 PASS**，exit 1，唔 crash。3 個 PASS 係三個輸分支負向斷言（pristine 本來就無 tuxedo，啱）。
- 全套 A/B（`qa131/run_suite.sh`）：
  - pristine：**200 PASS／23 FAIL**；工作版：**212 PASS／12 FAIL**（`qa160-m6/suite_pristine160.txt`／`suite_work160.txt`）。
  - **數字要咁讀**（AGENTS.md v151 教訓：同一 repo 連續跑出 211/12、137/86、200/23，失敗項每次唔同、全部係 .py，逐個直接跑全部 PASS）：pristine 嗰 23 項入面，12 項係穩定 pre-existing FAIL（同 v147／v148 基線逐項相同），其餘 11 項（aud91／aud91fix122／aud91fix124／awards62／awards63／awards64_chibi／awards64／book141／book143／book145／book70）**逐個直接重跑全部 PASS**——證實係環境波動，唔係回歸。
  - 工作版 FAIL 清單 **exactly 12 項穩定 pre-existing**（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），**零回歸**。另：相關測試逐個直接覆驗全部 PASS（awards62／63／64 static＋logic、travel114、m6）。
  - 注意：第一次 A/B 嘗試用相對路徑 OUT 失敗（run_suite.sh 會 `cd` 去 ROOT，OUT 搵唔到），已改用絕對路徑重跑；之前嗰個中途混合跑數（210/13）作廢，唔好引用。

## 6. 實駕——2/2 PASS（`qa160-m6/drive160m6.py`，port 8972，430×932）

- 腳本：沿用 `qa147/drive147.py` 模式＋三樣新嘢：① 強檔 seed（fame 200／credit 210／4 部電影＋2 部電視，base 0.90）＋`debugForceSeasonWindow` 重骰到 `bestOutcome==="won"` ② `drawImage` 監測（patch 原型，只記 `src` 含 `awei_tuxedo` 嘅呼叫，連落點＋尺寸）③ 截圖 key 由「得獎」改「得獎！」（「得獎者是……」都會 match「得獎」，第一版截錯 suspense）。
- **won_932：13/13 PASS**（`qa160-m6/drive160m6.json`）：pack won（score 0.924，一嘢中）、請柬＋出席、舞台出現（canvas x12／y295／406×233，同 v147 review 932 frame top 295 一致）、reveal 字幕「🏆 得獎！影壇新面孔（臨記組）：《幻彩舞影》」、glamour beat 出現（repGigId63＝有海報嘅 `gig_1988_film_lion_autumn_high`）、總長 **10,912ms**（約 11 秒：open 1200＋enter 1750＋names 2400＋suspense 1400＋reveal 2100＋glamour 1800＋out 500＝11,150ms，吻合）、結果卡講得獎、**tuxedo draw 32 次、全部 64×64**（dx 136→144、dy 139→144——行前移位＋企定，幾何同 §2 一致）、**0 pageerror／0 failed request**。
  - 截圖 `qa160-m6/shots/won_reveal_430x932.png`＋3x 放大 `won_reveal_canvas_3x.png`：台中央光池入面，阿偉著黑燕尾服（黑褸＋白恤衫＋黑領結＋黑褲）、同面同髮型、企喺同一個地板線，頭頂有細金獎盃 glyph；左右三個 Q 版對手暗 0.7；彩紙落緊。glamour 截圖 `won_glamour_430x932.png` 係海報全幅一擊（見 §7）。
  - 附帶：呢輪 won 第一 attempt 曾經 `total_about_11s` FAIL（>14s，harness 計時敏感——截圖＋polling 拖慢咗），內容檢查全部 PASS，第二 attempt 全 PASS。第一輪全跑嗰陣 won 亦因 http.server 喺 case 之間無故死咗＋「新遊戲」click timeout 而 ERROR，drive 已加 `ensure_server()`（每 attempt 探測＋重開）同 click timeout 5000→15000ms；之後三輪全過。第一輪 nominated 嗰陣見過幾單 icon REQFAIL（檔案本身存在，係 server  hiccup），之後兩輪 0 REQFAIL。
- **nominated_932：7/7 PASS**（對照組）：pack nominated、comfort beat 正常出現、結果卡正常、**tuxedo draw 0 次**——輸分支全程無畫過燕尾服；0 pageerror。
- 贏分支 seed 詳見 `drive160m6.py` `won_wraps()`：4 部電影全部用 `gig_1988_film_lion_autumn_high`（gig roleScale `film_support_main`→q 0.78；`poster59Path` 回 `assets/posters/poster-1988_film_lion_autumn_high.webp`，repGigId63 係佢先有 glamour beat；wsum 0.78×2.1＝1.64→worksScore 1.0）＋2 部電視假 lead（q 1.0，跨媒介借分＋repPower 0.08）。`awardsEvalTier` 只認 forceTier `gallery`／`nominee`，「won」無得直接 force，要靠 score 過贏線 0.875＋重骰（taste ±0.05）。

## 7. 未解決事項

- **main 已郁，落地要 rebase**：分支基底係 v148 `e08a070`；其後 v151（關海媚禁名拎走）、v156（手帳 B1＋B3）已落地，最新 main 唔係 e08a070。落地嗰陣要 rebase 上最新 main，`test_travel114_static.py` 釘行要再 resync（呢票嘅 resync 只對 e08a070 有效）。
- **glamour beat 肉眼見唔到燕尾服**：glamour 係海報全幅 DOM overlay，遮住晒成個 canvas——燕尾服喺海報下面有畫（draw 記錄：reveal 約 17 次＋glamour 約 14 次＝31–32 次），但玩家睇唔到。設計取捨：glamour 本來就係「海報一擊」；想 glamour 都見到燕尾服，要改 glamour 版式（另開票，唔喺呢票改）。
- **獎盃 glyph 偏淡**：細金色 glyph 喺光池亮底上面對比弱，勉強見到（見 3x 放大圖）。接受現狀；想明顯啲可以加深色描邊（另開票）。
- **實駕總長計時有波動**：`total_about_11s` 曾經一 attempt 超 14s（harness polling＋截圖開銷），唔係 game code 問題；重跑即過。

## 8. 檔案

- 改動：`index.html`（淨 ＋30 行）、`tests/test_travel114_static.py`（釘行 resync＋註解行）
- 新增：`assets/awards/awei_tuxedo.png`、`tests/test_awards160_m6_static.py`、`NOTES_V20A160_M6.md`（本檔）、`qa160-m6/`（`drive160m6.py`、`drive160m6.json`、`resync_travel114.py`、`suite_pristine160.txt`、`suite_work160.txt`、`suite_baseline160.txt`（作廢混合跑數，見 §5）、`shots/` 7 張）
- 另存：`qa160-m6/scratch/`（免費 export 證據：`m6_export.zip`＋解開嘅 spritesheet／manifest；`south_cell144.png` 對照用）
- `~/workspace/pristine160m6/` 係 `git archive e08a070` 抽出嚟嘅反證／基線樹，唔係本分支嘅一部分。
