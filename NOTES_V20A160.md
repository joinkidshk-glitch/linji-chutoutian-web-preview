# NOTES_V20A160 — v147 頒獎禮樣本四項接入（M6＋M4＋M1＋M9）

- 目的：將 v147 樣本五項入面剩低嗰四項接入遊戲。M5 彩紙唔喺呢票（v149 接入緊）。
- 用戶拍板：2026-11-13 07:16 全部接入；M9 fanfare 用戶 07:15 試聽後揀 **take 1**。
- Base：main `e08a070`（v148）。分支 `v20a160`（工作副本 `~/workspace/linji-work160/`）。
- 來源：`~/workspace/linji-work147/samples147/SAMPLES147_REPORT.md`（含 07:14 M4 殘影補記）；零新生成（Pixellab 餘額 4601／5000 嗰陣，M6 export-spritesheet 免費攞返，balance 驗過 4576／5000，差嗰 25 次係其他工用咗）。
- 紀律：唔直改 content pack JSON；SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`（`v20a10`）冇郁。

## 四項落點（詳見各工人 NOTES）

### M1 會場場景圖 — `assets/story/awards/bg_awards_ballroom.jpg`
- 來源 `m1_ballroom.png` 400×224，兩側各裁 2px → 396×224 → 等比放大 424×240（JPEG q88，39,211 bytes）；吊燈／紅幕／講台／白椅／紅地毯全入鏡。
- `index.html` 淨 ＋7 行：舊 v62 內嵌像素舞台 data URI（`AWARDS62_STAGE_PX`，24,872 字元）成個撤走，改行 `AWARDS62_STAGE_BG` 常數＋`im.src`；其餘典禮 code 一字唔郁。
- 四場典禮＋贏／落選／旁聽三分支共用同一張（`awards62PlayCeremony` 得一個 `bgImg`）。
- 新目錄 `assets/story/awards/`（會場唔係 15 個地圖地點，唔入 `locs/`）。
- 工人 NOTES：`NOTES_V20A160_M1.md`；分支 `v20a160-m1`，commit `f572f11`。

### M4 上台領獎動畫 — `assets/fx/awd_walkup_m4.gif`
- **一定要修好版 `m4_walkup_fixed.gif`**（原檔入庫，sha256 `3d446609…0603` 一致；9 幀全幅＋disposal=2）。原版差分幀＋disposal=0，播起嚟有殘影，唔准用。獎盃第 5→6 幀轉手跳位係已知、用戶接受，冇重抽。
- 落點：贏分支加新 beat `walkup` 2200ms（≈GIF 一圈 1080ms 播兩圈），插喺 `reveal` 之後、`glamour`／`out` 之前；贏全長 9350→11550ms。唔直接疊喺 reveal——嗰陣 canvas 已經畫緊行前＋捧杯，疊 GIF 會兩個阿偉打架；獨立 beat、canvas 壓暗、GIF 做主角（同 v147 comfort 加 beat 同一模式）。gallery／nominated 唔行。
- 呈現：簡單 `<img>` overlay（`.awd62-walkup160`，跟 glamour 同款層，`pointer-events:none`，GIF 300px 像素渲染＋金框）；文案「阿偉行上台，接過獎盃，高高舉起。」淨放 overlay `.cap`，beat caption 係 `""`（第一版兩邊都放，截圖見到金字＋台下暗字重複，已改）。
- `index.html` 淨 ＋37 行。
- 工人 NOTES：`NOTES_V20A160_M4.md`；分支 `v20a160-m4`，commit `ad2fcbc`。

### M6 燕尾服阿偉 — `assets/story/awards/awei_tuxedo.png`
- 來源 Pixellab state `7577440c…`（job `dcbd831c…`，8 方向齊），helper `export-spritesheet` 免費攞返；**無更高清來源**（spritesheet 每格 144×144，格內原畫只係 128×128，同樣本檔逐像素一致，128px 上限）。檔案 5,090 bytes，同樣本檔 byte-identical。
- 落點：只喺贏分支 `reveal`（2100ms，行前已經係燕尾服）＋`glamour`（1800ms）畫燕尾服；企定嗰陣頭頂加金獎盃 glyph（燕尾服原圖無獎盃，沿用對手得主嗰套標記）。`enter`／`names`／`suspense`／`out`／`gallery`／`nominated`／`comfort` 全部無郁。載唔到跌返 Q 版阿偉，唔穿崩。人物高 51px，同 Q 版玩家 50px 齊高，腳底對齊地板線。
- `index.html` 淨 ＋30 行。
- 工人 NOTES：`NOTES_V20A160_M6.md`；分支 `v20a160-m6`，commit `6449a1e`。

### M9 音樂／音效 — `assets/audio/awards_fanfare.mp3`＋`assets/audio/awards_applause.mp3`
- Fanfare **take 1** 原檔（462,979 bytes，約 20 秒，120 BPM；take 2 唔用，冇入 repo）。掌聲 WAV 557KB → MP3 74,973 bytes（音量對照相同）。
- 範圍嚴限頒獎禮贏分支。index.html 本來零 audio 機制，加咗一個典禮專用最小 helper `awards160PlayWinAudio()`（`index.html` 淨 ＋41 行）：揭曉 beat 且 `best === "won"` 嗰陣起 fanfare，900ms 後疊掌聲；按需建 `Audio` 元素，音量跟 `prefs.volume`，靜音跟 `bgmMuted`／`sfxMuted`；全部 `play()` 有 `.catch` 靜默吞＋call site 雙重 try/catch，絕對唔拖垮典禮。觸發點係 `awards62PlayCeremony` 嘅 `advance()` 入面 reveal beat 同 `spawnConfetti()` 同一行；Skip 行 `finish()` 唔經 `advance()`，所以每場贏典禮只觸發一次；gallery／提名唔觸發。
- `play()` 自動播放政策：揭曉係計時器觸發，未必喺用戶手勢入面，`play()` 有機會被拒——已 catch 靜默失敗，典禮唔會報錯／停低。
- 工人 NOTES：`NOTES_V20A160_M9.md`；分支 `v20a160-m9`，commit `ccb3e66`。

## 合併過程（統籌，`~/workspace/linji-work160/`，分支 `v20a160`）

合併次序 M1 → M4 → M6 → M9，base 全部係 `e08a070`。`index.html` 淨 ＋115 行（7＋37＋30＋41）。

### travel114 三次衝突
四個工人各自 resync 過 `tests/test_travel114_static.py`（釘行測試），合併必撞。用 difflib 對位（pristine `e08a070` vs 合併緊嘅 `index.html`）逐次重算，工具 `qa160-merge/resync_travel114.py`：
- M1＋M4：淨 ＋44，12 個 change 段，COUNT 13／FREE 27／DEF／WRAPPER 內容逐行相同，0 mismatch；DEF 53562→53606、WRAPPER 44171→44176。
- ＋M6：淨 ＋74，18 個 change 段，0 mismatch；DEF →53636、WRAPPER 44171→44176。
- ＋M9：淨 ＋115，20 個 change 段，0 mismatch；DEF →53677、WRAPPER 44171→44176。
- `test_text125_static.py`／`test_awards62_static.py`／62／63 logic 驗過唔使郁（M1 ＋7 喺佢哋釘行之下；M4 數值窗唔受 M1 影響）。
- 教訓：parse 釘值一定要用「每行首個數字」——註解入面嘅數字（ux68、inv72 等）唔係釘，第一版全數字 parse 撈埋咗 68／72／4 入去。

### M6 測試切片修正（game code 冇錯）
M4 喺同一個 play 函數加咗另一個 `if(best === "won"){`（walkup GIF），M6 測試 `find` 撞到佢，3 項 FAIL。修法：測試改為搵有 `tuxedo: true` 嗰個 won 區（17 項，全 PASS）。第一版用 `next()` 喺 pristine 反證嗰陣 crash（StopIteration），已改 defensive pick，反證 14 FAIL 乾淨、無 crash。

### 資產目錄統一
M6 用咗 `assets/awards/`，M1 用咗 `assets/story/awards/`——合併嗰陣搬 M6 嗰張去 `assets/story/awards/awei_tuxedo.png`，常數＋測試同步改，M6 測試重跑全 PASS＋反證乾淨。工人 NOTES_V20A160_M6.md 入面寫嘅舊路徑以呢度為準。

## 測試

- 新測試四檔，全部 PASS＋反證乾淨（對 pristine `e08a070` FAIL、唔 crash）：
  - `tests/test_awards160_m1_static.py` 19/19（反證 9 FAIL）
  - `tests/test_awards160_m4_static.py` 26/26（反證 17 FAIL／5 PASS；PIL 逐幀斷言全幅＋disposal=2＋120ms，殘影回歸防線）
  - `tests/test_awards160_m6_static.py` 17/17（合併修正後 17 項；反證 14 FAIL／3 PASS）
  - `tests/test_awards160_m9_static.py` 34/34（反證 29 FAIL）
- 相關測試逐個直接覆驗全部 PASS：travel114、text125、awards62、62／63 logic。
- 全套 A/B（`qa131/run_suite.sh`，`qa160-merge/suite_work160.txt`）：pristine **211／12**（三個工人獨立核實）vs 合併版跑出 **214／13**。多出嗰 1 項係 `test_wrap38_logic.js`——**suite 波動，唔係回歸**：直接跑 3/3 ALL PASS（按 v151 教訓：同一 repo 連續跑出唔同總數，判斷回歸睇 12 項穩定 FAIL 清單）。其餘 12 項 FAIL 同基線逐項相同。**實效 215／12，零回歸。**

## 合併實駕（`qa160-merge/drive160merge.py`，port 8985，證據 `qa160-merge/drive160merge.json`＋`qa160-merge/shots/`）

**3/3 PASS，0 pageerror**（一次過全跑）：
- `won_932` 13/13：真海報 gig 種子（`gig_1988_film_lion_autumn_high`，有 glamour），pack won；會場底圖載入（39,511 bytes）、燕尾服繪製、walkup GIF 郁、**glamour 喺 walkup 之後**、fanfare 揭曉嗰刻 attempted＋掌聲跟住 attempted、兩隻 mp3 成隻攞咗、結果卡。
- `gallery_932` 13/13（對照組）：底圖照載；燕尾服繪製 0 次、walkup 唔出、fanfare／掌聲零 attempted、零 audio 資源請求。
- `won_700` 13/13：同一組驗證喺 700。
- **M4 遺留窿補返**：walkup→glamour 順序喺有海報嗰陣實駕驗過（walkup 先、glamour 後），M4 工人嗰陣用假 gigId 所以冇 glamour beat。
- 目視確認：walkup 截圖（燕尾服阿偉企樓梯、金框、文案「阿偉行上台，接過獎盃，高高舉起。」、台下壓暗）＋glamour 截圖（《幻彩舞影》海報＋彩紙＋「得獎」）。頭像 emoji 🏆 喺 headless 截圖顯示做豆腐格，係 headless 欠 emoji 字體，唔係 game 問題。
- Harness 教訓（已修入 drive）：① ceremony id 係 `award_harbour_film`，唔係 `award_singho_film`（錯 id 會 `debugForceSeasonWindow` 回 null）；② 舞台播完會拆走，`final` snapshot 冇資源／音頻——stage_state 改為資源／音頻／繪製次數唔依賴舞台元素；③ walkup GIF loop 1080ms，兩張截圖隔 700ms 會撞返同一幀（byte-identical 假陰性）——改 3 張、350ms 間隔、任兩張唔同即算郁。

## 資產清單（新增 binary，合共約 601KB）
- `assets/story/awards/bg_awards_ballroom.jpg` 39,211 bytes
- `assets/story/awards/awei_tuxedo.png` 5,090 bytes
- `assets/fx/awd_walkup_m4.gif` 19,128 bytes
- `assets/audio/awards_fanfare.mp3` 462,979 bytes
- `assets/audio/awards_applause.mp3` 74,973 bytes

## 未解決事項／落地須知
- **main 已郁，落地要 rebase**：四個分支 base 係 `e08a070`；其後 v151（`86e391d`）、v156（`9c850f9`）已落地，落地嗰陣 rebase 上最新 main，`test_travel114_static.py` 釘行要再 resync（呢票嘅 resync 只對 `e08a070` 有效）。v149（舞台放大＋M5 彩紙）未落地——佢落地後舞台幾何／canvas 尺寸可能變，底圖照樣 work 但會再粒狀啲（M1 原圖上限 400px 闊），重驗 canvas 幾何。
- **M6 glamour beat 肉眼見唔到燕尾服**：海報全幅 DOM overlay 遮住成個 canvas——燕尾服喺海報下面有畫（draw 記錄 31–32 次），但玩家睇唔到。設計取捨；想 glamour 都見到要改版式，另開票。
- **獎盃 glyph 偏淡**：細金色 glyph 喺光池亮底上面對比弱；想明顯啲可加深色描邊，另開票。
- **掌聲 MP3 未經人耳試聽**（只做咗客觀對照）；fanfare take 1 用戶已試聽。最終上線前建議用戶實機聽一次揭曉嗰段。
- **headless 驗唔到聲**：實駕驗到嘅係觸發邏輯＋`play()` resolve＋檔案攞取，唔扮驗到聲。
- `test_poster59_static.py` 嘅 webp count pin 早已過時（pristine 已經 FAIL），M1 令實數 42→41，一樣 FAIL，失敗集合同 pristine 相同，呢票刻意唔郁。
- 隧道：工作副本 `core.sshCommand` 已改行 `~/workspace/gh_tunnel.py`（18080 已死，見 AGENTS.md）。
