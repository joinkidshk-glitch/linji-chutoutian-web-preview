# v170 Phase 2 調查報告：舞台-only 重構可行性＋v149 衝突

- 日期：2026-11-13（HKT）
- 範圍：只調查，冇實作、冇 commit、冇落地。冇改任何 repo 檔案；只寫呢份報告。
- 用戶方向（2026-11-13 11:59）：典禮場景只需要舞台（紅幕布＋平台＋講台＋人物），唔要台下部分（白色觀眾椅／紅地毯）。
- 現況：v170 Phase 1（分支 `v20a170`，基底 `fc1a1aa`）企位修正已 commit `69a3553`（FLOOR 194→155）；main 已郁到 `56141a3`（v169，線上 5,251,706 bytes sha `c0bbc07d…`）；卡片路向待用戶決定，呢份調查唔做卡片。
- 方法：code 閱讀＋PIL 量度為主，冇跑實駕（stale frame 前科；寫入探針 `/tmp/probe170p2.txt` 正常）。

---

## (a) 舞台-only 重構做法：裁切唔夠，要新底圖

### 底圖實測（`assets/story/awards/bg_awards_ballroom.jpg`，424×240，39,211 bytes）

PIL 行掃描＋逐欄量度（系統 `python3`＋PIL 10.2.0），對照目視：

| 元素 | 位置（底圖座標） | 證據 |
|---|---|---|
| 天花＋水晶吊燈 | y0–約 60（吊燈頂部本身已裁一半，M1 驗收已知小瑕） | 行平均亮度 y0–60 約 150–190 |
| 紅幕布 | y約 64–155 | x=140／300 紅像素行 y72–155；行亮度 y64–156 約 22–60 |
| 講台（金色） | 中央 x約 195–230，y約 136–160 | 中央欄 x=212：y136–158 淺木色 (202,158,109)→(255,219,149) |
| **舞台頂邊（平台前緣）** | **y156** | x250–350 帶平均亮度 y156 跌到 99.0（全段最暗行），y157 起回升 191→330 |
| 白椅椅頂 | y約 160–167（左右兩排） | x=40／60／90／340／380 首個亮像素 y160–167 |
| 紅地毯（中央走道） | y約 162 起向下 | 中央欄 x=212：y170 起紅色調 (49,13,0)→(178,86,61)，y180–238 持續紅地毯 |
| 底部 | y232–236 暗邊 | 行亮度跌到 71–82 |

舞台-only 裁切即係 **y0–157（保留舞台頂邊）→ 424×157，比例 2.70:1**（canvas 而家 424×240，1.77:1）。

### 三個做法比較

**A. 裁切＋cover 填滿現有 424×240 canvas——唔得。**
- 縮放 240/157 ≈ 1.53×；可見闊度得 424/1.53 ≈ 277px，即左右各裁 ~73px——側牆／木門／幕布邊全部出框，只剩中央一截。
- 1.53× 放大一張 424px 闊 JPG 會明顯矇（canvas 行 `imageSmoothingEnabled=false`＋pixelated，插畫平塗風格稍為頂得住，但唔係冇代價）。
- FLOOR 映射：舞台邊 y156 → canvas y≈239（貼底）；人物腳底要改到 ~237，頭頂（燕尾服 dispH 64）去到 y~173，企喺講台前面遮住講台——構圖爛。

**B. 裁切＋canvas 改短做 424×157——技術上得，但視覺縮水。**
- 1:1，唔矇、唔裁側邊；FLOOR 155 原封唔動（見 (d)）。
- 代價：canvas 顯示高度由 760×240/424 ≈ 430px 跌到 ≈ 281px（932 viewport）；人物顯示高由 ~115px 跌到 ~86px。成個典禮畫面變成一條闊扁帶，上下留白更大——而 v147 B1 嘅投訴正正就係「舞台細、上下大片黑帶」。呢個做法唔會整返黑帶出嚟（frame 居中、底色 `#14101f`），但同 B1「做大做實」嘅方向背道而馳。
- 要改嘅 code 見 (b) 清單。

**C. 生成一張新嘅舞台-only 底圖，424×240 原生——建議做法。**
- 零 code 改動（只換 asset 檔；`AWARDS62_STAGE_BG` 路徑不變，`index.html:44940`），canvas 幾何、FLOOR 基準、slots、glamour、walkup、pan 全部唔郁；唯一變數係新圖舞台頂邊位置，要 PIL 重新量度再定 FLOOR（見 (d)）。
- 構圖要求：低機位／收緊取景，紅幕布＋講台＋平台填滿 424×240，吊燈頂部可留；**唔准有白椅、紅地毯走道、觀眾**。
- 場景圖硬規矩（必須跟）：
  1. 先搵真實香港相做參照再重新生成，齋文字描述唔合格。參照相現成：`~/workspace/linji-work147/samples147/m1_ref_island_shangrila.webp`（港島香格里拉大酒店大禮堂，1080×700，來源頁 islandshangrila.hotelsofhongkong.com；M1 嗰陣已用過，紀錄喺 `~/workspace/linji-work147/samples147/SAMPLES147_REPORT.md` L37–40）。
  2. 相入面文字／真人樣唔抄——無字、一般化、無人、無 logo（M1 驗收標準照舊）。
  3. **唔准用成品場景圖做參照**——即係唔可以用而家呢張 `bg_awards_ballroom.jpg` 或者 `m1_ballroom.png` 做參照圖餵生成；只可以用真實相 `m1_ref_island_shangrila.webp`＋文字 prompt。M1 原 prompt 存喺 `m1_ballroom_body.json`（pixflux 400×224，1 次成功），新 prompt 要改做舞台填滿取景、刪走白椅／地毯描述。
  4. 生成限制（SAMPLES147 報告 L40）：pixflux 闊度上限 400px、闊高要被 4 整除；M1 係 400×224 再放大／重裁到 424×240（約 1.06×，輕微）。如果 v149 先落地（canvas backing 636×360，見 (c)），同一張 400×224 源圖要放大 1.59× 先填滿 backing——會軟啲；到時要評估係咪接受，或者生成後再升頻／直接出 424×240 後放大。呢個係 v149 落地次序決定嘅細節，唔係分叉。
- 成本預算：M1 用咗 1 次；新圖預算 1–3 次（Pixellab 餘額 2026-11-13 v170 Phase 1 後約 4,573 次，足夠）。唔好喺調查階段生成——等統籌批。

**結論 (a)：裁切唔夠（A 爛、B 縮水），要一張新嘅舞台-only 底圖（C）。**

---

## (b) 佈局影響清單（work170 `index.html`，行號實測）

Canvas 而家：`<canvas class="awd62-canvas" width="424" height="240">`（`index.html:46199`），CSS `width:100%;height:auto`（L781）。`draw()` 邏輯座標 `W=424, H=240`（L46357–46358）。以下分「方案 C（新圖 424×240）」同「方案 B（裁切＋canvas 424×157）」兩欄。

### 方案 C（建議）：全部唔郁，只換圖＋重定 FLOOR

| 元素 | 行號／函數 | 影響 |
|---|---|---|
| `AWARDS62_STAGE_BG` 常數 | L44940（註解 L44931–44939） | 路徑不變；註解要更新（新圖＋新量度數字） |
| canvas backing 424×240 | L46199 | 唔郁 |
| `draw()` 背景繪製 | L46362–46363（pan：`drawImage(bgImg,-8+off,0,440,H)`；其餘 `drawImage(bgImg,0,0,W,H)`） | 唔郁（新圖同尺寸，pan ±6px 搖擺照行） |
| `FLOOR` | L46248 | **要重定**：新圖舞台頂邊 PIL 量度後設 `FLOOR = 邊 − 1`（見 (d)）；唔可以假設 155 |
| `slotCx` | L46249（`202 + (i-(n-1)/2)*72`） | 唔郁（x 向，唔關底圖事） |
| `drawFigure`／`dispH`（player 50／fellow 48／燕尾服 64） | L46284–46303 | 唔郁（腳底跟 FLOOR 行） |
| `lightPool`（`F-66`） | L46305–46310 | 唔郁（FLOOR 相對） |
| glamour overlay＋panel | CSS L798–801（`aspect-ratio:424/240`，右邊 44% panel） | 唔郁（canvas 比例不變；燕尾服並置佈局照舊） |
| 卡列 `.awd63-cards`（v168 glamour-hide） | CSS L788–789；JS `syncGlamour`（L46350 附近） | 唔郁（DOM 層，喺 frame 入面 canvas 下面） |
| 字幕框 `.awd62-caption`（v166 C1 空字隱藏） | CSS L782；`setCaption` | 唔郁 |
| 跳過掣 `.awd62-skip` | CSS L785（`top:-10px;right:-4px`，相對 frame） | 唔郁 |
| walkup GIF 層 `.awd62-walkup160` | CSS L803–806（`position:absolute;inset:0`，掛喺 stage 全幅） | 唔郁（唔係 canvas 尺寸，係成個 stage overlay） |
| 後備舞台 `awards62FallbackStage` | L46015–46036（平台頂 `H-85=155`） | 唔郁（佢本身已經跟 FLOOR=155；新圖載入失敗先用佢，畫面係程式舞台，冇觀眾席可言） |
| 彩紙／星光（names `fy 150+…%80`、confetti `y>244`） | `draw()` L46390 附近、loop | 唔郁（H=240 不變） |
| 文案 | gallery pan beat caption「今晚你坐喺觀禮席」（`awards62CeremonyBeats`，L46037 起） | **輕微注意**：畫面唔再見到觀眾椅，但旁白講玩家坐喺觀禮席（鏡頭外）——敍事上仍然成立，唔使改；實作嗰陣順手核對一次即可，唔係 blocker |

### 方案 B（裁切＋canvas 424×157，唔建議但列出嚟對照）

| 元素 | 要改咩 |
|---|---|
| canvas backing | `width="424" height="240"` → `height="157"`（L46199） |
| `draw()` | `H=240` → `H=157`（L46358） |
| glamour overlay | `aspect-ratio:424/240` → `424/157`（CSS L798）；panel 內海報 `max-height:60%` 要重驗（panel 矮咗，海報＋cap 會唔會逼爆） |
| 後備舞台 | 平台頂 `H-85` → `H-2`（=155，L46021–46022 註解＋數值）；金線 `H-89` → `H-6`；底部 `H-22` 區要成組重算 |
| names 星光 | `fy = 150 + ((…)%80)` 上限 229 → 夾死喺 157 以下（L46390 附近） |
| confetti | loop 重置條件 `p.y > 244` → `> H`（L46460 附近） |
| `FLOOR`／`slotCx`／`drawFigure`／`lightPool` | 唔郁（FLOOR 155 照成立，見 (d)） |
| 卡列／字幕／跳過／walkup | 唔郁（DOM 層；成個 frame 矮咗 83 logical px，932 顯示矮約 150px，畫面更細——見 (a) B 項） |
| 測試 | `tests/test_awards160_m1_static.py`（釘 BG 尺寸／路徑，L50–55）、`tests/test_awards170_static.py`（釘 FLOOR 155）、`test_awards62_static.py`、travel114／text125 resync 全部要重對 |

---

## (c) v149 衝突：真實存在，衝突點唯一且明確

### v149 現況（只讀 `git diff`／`git status`，冇掂過佢任何檔案）

- 工作副本 `~/workspace/linji-work149/`，分支 `v20a149`，基底 `da90957`（v146 時代），未落地。
- 未 commit 改動：`M index.html`（+171／−約 80 行，淨約 +113 行）、`M tests/test_text125_static.py`、`M tests/test_travel114_static.py`、`?? assets/fx/awd_confetti_m5.gif`、`?? qa149/`。

### v149 B1 實際改咗咩（逐項，`git diff index.html` 全文已讀）

| 改動 | 係咪觀眾席 | 檔案／位置 |
|---|---|---|
| **`.awd62-aud149` 上下觀眾席帶（CSS 畫，唔使新圖）**：`flex:1` 吸晒 frame 上下剩餘空間；8 個 `radial-gradient` 深色橢圓（人頭剪影）＋深紫漸變底；`.bot` 用 `scaleY(-1)` 反轉 | **係——直接衝突** | CSS 段（diff hunk 1，`.awd62-stage` 改 `flex-direction:column`＋`.awd62-frame{flex:none}`＋新增 `.awd62-aud149`／`.bot`）；`stage.innerHTML` 加 `<div class="awd62-aud149 top">`（frame 上）＋`<div class="awd62-aud149 bot">`（frame 下） |
| `.awd62-stage` 改 `flex-direction:column`（為咗上下疊三件：上帶／frame／下帶） | 係——只為咗裝觀眾帶 | 同上 CSS hunk |
| canvas backing 424×240 → **636×360**，`draw()` 入面 `ctx.setTransform(1.5,0,0,1.5,0,0)`，邏輯座標維持 424×240；註解寫明「FLOOR／slotCx／confetti／fallback 舞台全部照舊」 | 唔係（純解像度） | `stage.innerHTML` canvas 行＋`draw()` 開頭 |
| `.awd62-canvaswrap` 包裝＋M5 彩紙 GIF 疊加（`.awd62-m5fx149` ×2，一張 `scaleX(-1)` 鏡像，reveal／comfort／out 期間顯示，`syncConfetti149`） | 唔係（彩紙，唔係觀眾） | CSS 新增＋`stage.innerHTML`＋`syncConfetti149` |
| 彩紙加密：46 → 90 粒；非贏 reveal／comfort 期間都 spawn／飄落 | 唔係 | `spawnConfetti`、loop、reveal／comfort 分支 |
| 跳過掣移位 `top:-10px;right:-4px` → `top:8px;right:8px`（v147 review B1 附帶：唔再半出框壓住舞台框） | 唔係 | CSS `.awd62-skip` |

v149 其他部分（B2／B3／B4）同舞台-only **零衝突**：B2 得主報紙文案（`awardWinner149`／`awardWinLine149`／`awardGalleryCopy149`＋`renderAwardResultHtml` metricLine＋`awards63FellowsHtml`＋推辭／旁聽報紙動態得主）、B3 卡片 win 🏆角標＋csscard 改媒介圖標＋典禮名、B4 短屏報紙 `padding-bottom:76px`（`@media (max-height:800px)`）。

### 衝突判定

**真實存在，但範圍好窄：唯一衝突點係 `.awd62-aud149` 上下兩條觀眾席帶＋為佢而設嘅 `.awd62-stage{flex-direction:column}`。**

釐清兩點，免得誤判：
1. v149 冇加白色觀眾椅——佢加嘅係 CSS 畫嘅**深色人頭剪影帶**（抽象暗景），唔係將底圖嘅白椅放大。但用戶方向係「唔需要台下嘅部分」，剪影帶正正就係「台下」裝飾，方向上直接對撞，唔係「冇椅就冇事」。
2. v149 冇郁過 FLOOR／slotCx／底圖 `drawImage`（diff 全文 grep：零 `FLOOR`／`slotCx` 命中；`W=424,H=240` 邏輯座標原封不動）。所以 v149 同 Phase 1 企位修正（FLOOR 155）本身冇衝突；衝突只喺 B1 嘅觀眾帶。

### 兩個處理方向（唔做決定，等統籌／家長拍板）

**方向 1：v149 B1 剔走觀眾席嗰截先落地。**
- v149 工人喺自己分支刪走 `.awd62-aud149` CSS＋兩行 innerHTML＋stage `flex-direction:column`（還原單 frame 居中，`.awd62-frame` 唔使 `flex:none`），保留 B1 其餘部分（636×360 backing、M5 彩紙、彩紙加密、跳過掣移位）＋B2／B3／B4 原樣落地。
- 優點：main 永遠唔出現用戶已否決嘅觀眾帶；v170 Phase 2 之後接手乾淨。
- 成本：v149 分支約 30 行回退＋重跑佢嘅測試／resync／實駕（qa149 現成）；B1 驗收要改寫——「上下唔再留大片純黑空帶」呢個驗收目標要重新定義（冇咗觀眾帶，上下剩餘空間係 `#14101f` 底色；要唔要接受，定係等舞台-only 新圖填滿 frame，係跟住要拍板嘅細節）。
- 注意：v147 B1 原投訴（舞台細、上下大片黑帶）如果靠觀眾帶來填，剔走之後嗰個投訴會原狀保留，直到舞台-only 新圖（方案 C）或者其他填法落地。

**方向 2：v149 B1 照原樣落地，舞台-only 喺 v170 Phase 2 覆蓋佢。**
- v149 唔郁，照現有 diff 落地；v170 Phase 2 實作嗰陣一併刪走 `.awd62-aud149`＋還原 stage flex（約 30 行，計入 v170 diff），再換舞台-only 底圖。
- 優點：v149 工人零返工，即刻可以落地；v149 嘅 B2／B3／B4 同彩紙部分唔使等。
- 成本：觀眾帶會短暫上 main（v149 落地到 v170 Phase 2 落地之間），而用戶已經話唔要——呢段時間 live 會有用戶否決咗嘅元素；v149 嘅 B1 實駕截圖會影住啲之後要刪嘅嘢，驗證工夫部分白費；v170 diff 變大（要包埋刪帶＋resync）。

**調查員意見（僅供參考，唔係決定）：** v149 未落地，方向 1 乾淨啲；但如果 v149 急住要 B2／B3／B4（報紙講賽果＋卡片角標）先行，方向 2 都行得通，條件係 v170 Phase 2 緊接其後，唔好等觀眾帶喺 main 留太耐。

### 附加：合併次序注意（唔係衝突，係工序）

- v149（基底 `da90957`）同 v170 Phase 1（基底 `fc1a1aa`）都掂過頒獎禮區：v149 改 `index.html` 約 +113 行淨（集中 `awards62PlayCeremony`＋CSS），v170 Phase 1 改 12 行（FLOOR 一行＋fallback 幾行＋註解）。v149 diff 冇掂 FLOOR，所以內容上唔會打架；但兩個分支都要 rebase 上而家 main `56141a3`（v169），`test_travel114_static.py`／`test_text125_static.py` 行號 resync 會疊加（v149：CSS +27／JS +86，註解寫明；v170：淨 +2 行，DEF 53610→53612）。後落地嗰個要重跑自己嘅 resync script（`qa149/resync149.py`／`qa170/resync_travel114_170.py` 現成）。
- v170 工作副本入面完全冇 v149 code（grep `awd62-aud149`／`awd62-m5fx149` 零命中），Phase 1 實駕結果唔受 v149 影響。

---

## (d) FLOOR 155 係咪仲成立：方案 C 要重定，方案 B 照成立

Phase 1 嘅 FLOOR 155 係噉嚟：底圖舞台頂邊 y156（y156 全行暗線，y157 起急亮），腳底設喺 155＝邊 −1。對照數字（今次重驗，一致）：

| 對照點 | 底圖 y | 來源 |
|---|---|---|
| 紅幕布底 | 155 | x=140／300 紅像素最後一行 |
| 舞台頂邊暗線 | 156 | x250–350 帶最暗行（亮度 99.0） |
| FLOOR | **155** | = 邊 − 1（Phase 1 實駕：reveal 行前 162／燕尾服 162.5、glamour 155.5，誤差係 fwd／bob 偏移，唔係 FLOOR 錯） |
| 白椅椅頂 | 160–167 | 各欄首個亮像素 |
| 紅地毯（中央） | 約 162 起 | 中央欄紅色調起始 |
| 舊 FLOOR 194 | — | 低過舞台頂 39px，腳底同白椅椅面齊高＝企觀眾席（Phase 1 已證實） |

- **方案 C（新底圖 424×240）：FLOOR 155 唔可以直接沿用。** 新圖舞台頂邊位置由生成結果決定（取景唔同，邊可以喺 y140–200 任何位置）。實作步驟：新圖落 repo 後，PIL 行掃描搵舞台頂邊（暗線／亮度躍變），設 `FLOOR = 邊 − 1`，更新 `index.html:46248` 註解＋`tests/test_awards170_static.py` 釘值＋fallback 舞台 `H-85` 對應值（而家 H-85=155，FLOOR 變咗就要跟住變：平台頂 = `H-(240-FLOOR)`）。slotCx、dispH、lightPool 全部 FLOOR 相對，唔使郁。
- **方案 B（裁切＋canvas 424×157）：FLOOR 155 照成立。** 裁切係 1:1，舞台邊仍然喺 canvas y156，腳底 155＝邊 −1 不變。人物頭頂 y91–107（dispH 48–64），喺幕布範圍內，唔撞講台頂（講台頂 y136，中央 slot 人物會遮講台一半——同而家 Phase 1 實駕接受咗嘅狀態一樣）。
- **方案 A（cover）：FLOOR 要改到 ~237，構圖爛，唔建議。**
- **v149 因素：** v149 嘅 636×360 backing＋1.5× transform 唔改變邏輯座標，FLOOR 155 喺 v149 落地後仍然成立（佢自己註解都寫明）。所以 FLOOR 問題只取決於舞台-only 用邊個方案，唔取決於 v149。

---

## 建議實作方案（步驟清單，等批先做）

**前置決定（要家長／統籌拍板，唔係調查員決定）：**
1. 舞台-only 用方案 C（新底圖）定方案 B（裁切＋改短 canvas）——調查建議 C。
2. v149 衝突行方向 1（剔走觀眾帶先落地）定方向 2（照落地、v170 覆蓋）——調查傾向 1（v149 未落地）。
3. 卡片路向（bust 裁切／Pixellab 像素／留返深色字卡）——呢票唔做，但要留意 v170 Phase 2 實作嗰陣唔好同卡片改動撞 code（卡列結構 `awd63-cards` 喺 B3 已改過一次）。

**實作步驟（方案 C ＋ 方向 1 假設下）：**
1. v149 工人：分支內刪 `.awd62-aud149` CSS＋兩行 innerHTML＋stage `flex-direction:column` 還原；保留 636×360／M5／彩紙／跳過掣／B2／B3／B4；重跑測試＋resync＋實駕；落地。
2. v170 Phase 2 工人：rebase 上當時 main（留意 v149 落地後嘅行號漂移，重跑 `qa170/resync_travel114_170.py`）。
3. 生成新舞台-only 底圖：參照相用現成 `~/workspace/linji-work147/samples147/m1_ref_island_shangrila.webp`（唔准用成品 M1 圖做參照）；prompt 以 `m1_ballroom_body.json` 為底，改做舞台填滿取景、刪白椅／紅地毯／觀眾、保留紅幕布＋金講台＋吊燈＋暖金暗木配色、無人無字無 logo；pixflux 400×224（闊高被 4 整除），再放大／裁到 424×240（如果 v149 已落地，評估 636×360 backing 下 1.59× 放大係咪接受，唔接受就升頻或重出大圖）。預算 1–3 次。
4. 新圖驗收（PIL＋目視）：無字無人無 logo；舞台頂邊清晰可量；講台唔好俾裁走；左右幕布邊完整。舊圖 `bg_awards_ballroom.jpg` 留檔唔刪（samples170），新圖同名覆蓋或者新檔名＋改 `AWARDS62_STAGE_BG`——揀同名覆蓋最少改動，但要留意 `?v=` 紀律（唔郁產品 `?v=`；asset 檔本身換內容唔使改版本參數，瀏覽器快取由部署流程處理——呢點實作嗰陣要同部署對口徑）。
5. PIL 量新圖舞台頂邊 → 定 FLOOR（= 邊 − 1）→ 改 `index.html:46248`＋註解；fallback 舞台平台頂跟住改（`H-(240-FLOOR)`）；更新 `tests/test_awards170_static.py` 釘值＋`test_awards160_m1_static.py`（如有尺寸斷言）。
6. 全套測試＋實駕（won_932／won_700／gallery_932／nominated_932，Phase 1 嘅 `qa170/drive170.py` 模式）：逐 beat 腳底＝FLOOR、slot x、glamour 並置、walkup、彩紙、卡列隱藏，0 pageerror。
7. 設計 review（按慣例每版一次）。
8. 落地：squash merge → push main → 線上核實（bytes＋sha＋curl）。

**真正分叉（除咗 v149 之外）：**
- **F1：v147 B1「舞台細、上下黑帶」點收科。** v149 原本靠觀眾帶填上下空位；用戶而家唔要台下部分，咁上下空位點算？方案 C（新圖填滿 424×240 frame）本身唔會令 frame 變大——frame 上下空位依然係 `#14101f` 底色。係咪接受、定係要另外諗填法（例如舞台圖本身拉高／frame 加闊），要設計決定。呢個唔係調查可以代答。
- **F2：gallery 旁聽 beat 嘅「觀眾席」敍事。** 畫面冇咗觀眾席之後，pan beat 文案「今晚你坐喺觀禮席」＋報紙文案「阿偉坐喺台下／坐滿全場」係咪仲順——調查判斷敍事成立（玩家喺鏡頭外），但如果用戶覺得畫面同文案唔夾，要另開文案票。
- **F3（輕微）：新圖生成尺寸 vs v149 636×360 backing。** 如果 v149 先落地，新圖 400×224 源圖放大 1.59× 會軟；接受、升頻、定係生成更大源圖，三揀一，實作嗰陣先有實圖可以判斷。
