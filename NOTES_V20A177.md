# NOTES_V20A177 — 頒獎禮舞台加闊（FLOOR 加深＋企位拉開）

工作副本 `~/workspace/linji-work177/`，分支 `v20a177`，基底 main `7801a72`（v172 已落地；遊戲 `9eea029`，線上 5,271,408 bytes sha `eb594747…`）。
用戶拍板：頒獎禮舞台要加闊，人物要有位行、有位做動作。**本票唔落地**（落地由統籌做）。

## §0 總覽

| 項 | 舊（v174） | 新（v177） |
|---|---|---|
| FLOOR（舞台頂線） | 290 | **250**（底圖重構，地板深 70→**110px**＝30.6% canvas 高） |
| won／nominated 4 slots | 82／162／242／322（間距 80，罅 17px） | **62／162／262／362（間距 100，罅 37px，兩邊各留 31px）** |
| gallery 3 slots | 122／166／282（罅 44／116，中央 −36 移位） | **82／162／262（罅 80／100，唔再移位）** |
| 講台 vs 人物 | gallery 中央重疊 draw-rect 4px（像素 0px） | **重疊 0px**（講台啱啱落喺 won slot 2／3 之間條罅；gallery 中央右緣 193、右邊左緣 231） |
| reveal 行前腳 | 300 | **260**（FLOOR＋10 唔變） |
| 人仔／canvas／backing | 72／75／96、424×360、636×540、setTransform 1.5 | **全部唔郁** |

改動：`index.html` 8＋／8−（**淨行數 0**，kwan151／tang152 釘行唔使 resync）＋底圖重構 1 檔＋新測試 1 檔＋4 檔舊測試 resync。
全套：pristine `235／12` → 工作版 **`236／12`**（＋1 係新測試，12 項穩定 FAIL 同一批，零回歸）。
實駕：won_932／won_700／gallery_932／nominated_932 **4/4 PASS、0 pageerror**（nominated 係單 case 重跑合併，見 §5）。

## §1 量度＋設計

### 1.1 參考圖量度（PIL，尺寸-only；見 §1.3 授權說明）

參考圖 `~/workspace/user/files/D39EF434-1CF5-4AA1-9C11-DC9F2A8DBDEE-photo-C908F10A-D35C-44B4-BC40-91C709C0FEDD.jpg`，**1290×1031**：

| 量度項 | 數字 |
|---|---|
| 舞台闊（地板橫跨） | x≈30–1260，約 1230px ＝ **95.3% 畫面闊** |
| 地板頂（幕布底→木地板） | y≈715（格仔幕布去到 ~700–715，木地板亮帶 y770–855） |
| 地板深（幕布底→畫面底） | 1031−715＝316px ＝ **30.7% 畫面高**（木地板亮帶本身深 ~140px＝13.6%） |
| 人物（3 隻） | cx **160／612／860**，闊 ~100–132px，高 **~247–258px**（y506–762，腳 ~757–762） |
| 人物高／舞台闊 | 250／1230 ＝ **20.3%** |
| 人物中心距 | 452px（36.8% 舞台闊）、248px（20.2%） |
| 人物邊罅（最細） | 133px（右邊兩隻之間）＝ **10.8% 舞台闊** |
| 人物企位分佈 | **唔係三分法**——左／中／中右（佔舞台闊 10.6%／47.3%／67.5%），**右三分一留空** |

### 1.2 現行數字對照（v174，實測核實）

canvas 邏輯 424×360、backing 636×540、setTransform 1.5 均勻；FLOOR 290（地板深 70px＝19.4%）；won slots 82／162／242／322（間距 80、人仔闊 63px、**邊罅得 17px**）；gallery 122／166／282（罅 44／116，中央 −36）；講台 x194–229；glamour dispH 64→96（v174 寫 96 係燕尾服）；reveal 阿偉 alpha 1.0、winner 0.85、其他 0.7（code 核實，唔郁）。

對照結論：現行最侷促嘅唔係中心距（80px 已經唔細），係**邊罅得 17px**（參考圖最細邊罅係舞台闊嘅 10.8%，換算落 424 闊 canvas ≈ 46px）＋**地板得 70px 深**（參考圖 30.7%）。人物相對比例：現行 72／424＝17.0%，參考圖 20.3%——**今次唔放大人物**：人仔再大，罅又縮返，v174 B1 啱啱定落嘅 72／75／96 比例亦會重開；加闊嘅份額畀晒企位間距＋地板深度。

### 1.3 約束：frame 闊度受 viewport 限死

遊戲直向 390×844，舞台 frame 闊 `min(96vw, 760px)`，canvas 顯示闊跟 frame 走——**加闊唔係加闊 viewport**。喺約束內做到「有位行」嘅方法係三樣：① 平台佔 canvas 比例——地板頂由 290 推上 250，地板深 70→110px（30.6%，對齊參考圖 30.7%）；② 人物分佈——間距 80→100，邊罅 17→37px，兩邊留白由 51／71px 收窄做對稱 31px（闊度由邊緣慳返嚟，唔係由 viewport 攞）；③ 行走區——gallery 右邊空出 293–424＝131px（對照參考圖右三分一留空），reveal 得主行前 28.6→33px。

### 1.4 新幾何（全部數字）

- **FLOOR 250**：底圖重構（見 §2），源圖舞台頂線 y194→y167，×1.5 拉伸後 167×1.5＝250.5→250。
- **won／nominated**：`212 + (i − 1.5) × 100` → **62／162／262／362**。置中由 202 改 212（對稱，兩邊各留 31px）。講台 x194–229 啱啱落喺 slot 2／3 之間：slot 2 右緣 162＋31＝193（留 1px）、slot 3 左緣 262−31＝231（留 2px），draw-rect 重疊 0。
- **gallery**：**[82, 162, 262]**（唔再 −36 移位）。罅 80／100，全部 ≥70px 目標。中央人右緣 162＋31＝193（留 1px）、右邊人左緣 262−31＝231（留 2px），同講台重疊 0。左邊得主 82（51–113），右邊空出 293–424＝131px 行走區。
- **行走路線**：entryPlan 唔郁（from −30／454，0.16px/ms，rank×380）。新 slot 下每人行距 92px（舊 112／132px——舊 slot 貼邊所以行得遠啲，呢個係如實紀錄，唔係退步：四人同時由兩邊行入，cx 橫跨成個舞台，實駕量到 29–34 個不同 cx、跨度 466–475px；reveal 行前 28.6→33px）。walkup beat 繼續用 M4 GIF（2200ms，約兩圈）。
- **唔郁**：人仔 72／75／96、canvas 424×360、backing 636×540、setTransform 1.5、glamour aspect 424/360、光池 99、glyph −96／−39、彩紙底界 364、stagger 60＋i*180、fwd64 向 212 行 22%。
- **後備舞台**（底圖載唔到先用）：平台頂 H-70→**H-110**＝250，正面 250–287（37px），金線 H-76→**H-116**＝244；底部 H-33／椅列 H-39 唔郁。
- **同將來 v174 C1 唔打架**：C1 係 B2 預留暗位改 `max-height` 展開（frame 外嘅嘢）；新幾何冇將平台畫入預留區，平台只係 canvas 入面嘅地板，預留暗位機制原封不動。

### 1.5 尺寸參考授權（寫明）

參考圖係用戶批准嘅**尺寸-only 例外**：「Kairosoft 截圖唔做設計參照」嗰條規矩本身唔變，呢張圖淨係參考佢個尺寸——闊舞台比例、地板深度、人物高佔舞台闊幾多、人物間距。**風格照舊**：冇抄佢嘅畫風、顏色、UI、字體；底圖重構只係將我哋自己現有底圖重採樣（見 §2），冇引入參考圖任何像素／風格元素。

## §2 實作

### 2.1 底圖重構 `assets/story/awards/bg_awards_ballroom.jpg`（424×240，40,380→33,895 bytes）

PIL LANCZOS 重採樣，**唔換風格、唔換內容、唔換尺寸**：
- 幕布帶：源圖 rows 0–193 → rows 0–166（×0.861 壓縮）。
- 地板帶：源圖 rows 194–239 → rows 167–239（×1.587 拉伸）。
- 講台跟住郁：正面由源圖 y196–214 變 y170–199（canvas ×1.5 後 y255–299，腳底 250 之下——同舊幾何一致：講台頂喺腳底之上 ~14px，講台正面喺腳底之下；x 194–229 完全唔郁）。
- 驗證（PIL）：中央帶 y160–164 mean 80–87（幕布紅，<110）、y170–172 mean 217–220（平台面，>180）、講台金色像素 y170–200／x195–231 共 478px。原圖備份存 `qa177/bg_orig_424x240.jpg`（唔入 repo 遊戲區，留證據）。
- 注意：平台頂線喺源圖唔係完全水平（中央 y194、兩側 ~y203，透視斜），重構後斜度由 9px 變 ~14px（中央 y167、兩側 ~y181）——仍然係同一張相嘅透視，唔係新畫嘅嘢；實駕截圖目測幕布底邊斜落兩側，自然。

### 2.2 `index.html`（8＋／8−，淨行數 0）

| 行 | 改動 |
|---|---|
| L46447 | `const FLOOR = 290` → **`250`**＋註解（底圖重構＋167×1.5＝250.5＋地板深 110px） |
| L46448 | `slotCx` 重寫：3 slots → `[82, 162, 262][i]`；其餘 `212 + (i − (n−1)/2) × 100`（舊 `202…× 80`＋`cx -= 36` 刪除） |
| L46202–46203 | 後備舞台註解：H-110＝250／H-116＝244 |
| L46204／46205／46207 | 後備舞台 `H - 70` → **`H - 110`**（側幕／金邊／平台正面） |
| L46208 | 後備舞台金線 `H - 76` → **`H - 116`** |

其餘全部唔郁：`draw()`（`drawImage(bgImg, 0, 0, W, H)` 拉伸不變）、`entryPlan`（`slotCx(i) <= 202` 左右分流閾值——新 slots 162 左／262 右，分流結果同舊一樣）、`fwd64`（向 212 行 22%）、`lightPool`、`drawTrophyGlyph`、sparkle 帶、confetti、`syncCards`／`syncGlamour`／`syncWalkup`、walkup GIF、glamour overlay、CSS（零改動）。

## §3 測試

### 新測試 `tests/test_awards177_static.py`（53 項，全部 PASS）

- 地板：FLOOR 250、舊 290 消失、只定義一次、地板深 110px、行前腳 260、腳底／光池／glyph 跟 FLOOR、後備 H-110／H-116、舊 H-70／H-76 消失、底部 H-33／H-39 唔郁。
- 企位：間距 100／置中 212、gallery `[82, 162, 262]`、舊 80／202／−36 消失、won 罅 ≥70（中心距 100）、gallery 罅 ≥70（80／100）、兩邊企位唔出界（各留 31px）、won 講台落中罅（重疊 0）、gallery 中央／右邊唔掂講台、右邊行走區 131px、玩家 slot 仍然係 1（阿偉 x＝162 唔變）、glamour 燕尾服右緣 49.5%（<56%）。
- 行走：entryPlan 唔郁（0.16／rank*380／from −30／454）、enter 用 walk 幀、fwd64 向 212 行 22%、walkup M4 GIF 2200ms。
- 底圖 PIL：尺寸仲係 424×240、y160–164 幕布紅、y170–172 平台面、講台金色像素在位、檔案 10–200KB。
- v174 五項守衛：A1 金底 chip（#f2c14e／22px）＋`>img`、B1（424×360／636×540／1.5／72／75／96／aspect 424/360）、B2（flex＋visibility＋stagger 60＋i*180）、C2（glamour-hide display:none＋choke point）。
- 紀律：SAVE key／softRev／掌聲 M9／cardsData／彩紙 364 唔郁。

### 反證（pristine worktree `~/workspace/linji-pristine177`，基底 `7801a72`）

- 新測試對 pristine：**14 FAIL**（全部新幾何斷言）／39 PASS（守衛＋v174 項＋純計算斷言），**唔 crash**。
- Resync 檔對 pristine：174：**6 FAIL**；170：**8 FAIL**；160_m1：**1 FAIL**（淨係 y170–172 平台面新斷言）；64_chibi：**2 FAIL**；168／166：**ALL PASS**（冇掂佢哋）。全部係斷言 FAIL，唔係 import／語法 crash。

### Resync 舊測試（新幾何，4 檔；168／166／qa149 唔使郁）

- `test_awards174_static.py`：42 項（舊 41 項，**＋1**——C1 拆做「gallery 用 [82,162,262]」＋「舊 −36 唔再出現」兩項）；FLOOR 250、slotCx 100／212、後備 H-110、C1 新規則、header 註解更新。
- `test_awards170_static.py`：47 項；FLOOR 250、後備 H-110／H-116、舊 H-70／H-76 唔再出現、slotCx 100／212、gallery [82,162,262]、阿偉 x＝162（212−50）註解更新。
- `test_awards64_chibi_static.py`：18 項；FLOOR 250、slotCx 212／100。
- `test_awards160_m1_static.py`：24 項；PIL 舞台頂邊改量 y160–164（幕布）／y170–172（平台面）、講台金色像素範圍改 y170–200、註解更新。
- 全部 resync 檔工作版 ALL PASS。`index.html` 淨行數 0，kwan151／tang152 釘行唔使 resync（全套入面全部 PASS）。
- 相關舊測試工作版：174（42／42）＋170（47／47）＋168（22／22）＋166（32／32）＋160_m1（24／24）＋64_chibi（18／18）＋qa149（36／36）。
- `node --check`：兩段 inline script（1141＋4,315,816 bytes）全部 OK。

### 全套 `qa131/run_suite.sh`

- Pristine 基線（`7801a72`）：**PASS 235 FAIL 12**。
- 工作版：**PASS 236 FAIL 12**（＋1 係新測試 `test_awards177_static.py`）。
- 12 項 FAIL 兩邊同一批（`diff` 零差異）：flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38——全部係已知穩定 FAIL，唔係回歸。
- 結果檔：`qa177/suite_pristine177.txt`、`qa177/suite_work177.txt`。

## §4 實駕 `qa177/drive177.py`（本地鏡像＋Playwright，port 8997，`?softPreview=1`）

**won_932／won_700／gallery_932／nominated_932：4/4 PASS、0 pageerror**（結果 `qa177/drive177.json`，截圖 `qa177/shots177/` 37 張）。

| Case | 腳底 median（每 beat） | 行前腳 max | 企位實測 | enter 行走 |
|---|---|---|---|---|
| won_932 | 250（enter／names／suspense／glamour；reveal 260.2） | 260.2 | 62.5／162／262.5／362.5 | 34 個不同 cx，跨度 468px |
| won_700 | 250（reveal 260.2） | 260.2 | 62.5／162／262.5／362.5 | 34 個不同 cx，跨度 474.5px |
| gallery_932 | 250（pan／names／suspense；reveal 260） | 260 | 82.5／162.5／262.5 | N/A（gallery 冇 enter beat，pan 企定亮相） |
| nominated_932 | 250（enter／names／suspense／comfort；reveal 260） | 260 | 62.5／162／262.5／362.5 | 29 個不同 cx，跨度 466px |

- **腳底＝舞台頂**：顯示值 won_932 385.5＝385.5、won_700 269.5＝269.5、gallery_932 477.5＝477.5（差 0.0）；地板深顯示 103.3px（932，110×0.9387 scale）。
- **講台**：gallery reveal 全部人物 vs 講台 x194–229 重疊 **0px**（中央人 x131–194、右邊人 x231–294、得主行前 cx 84→112 全程 0）；won slot 2／3 同講台各留 1–2px（靜態斷言＋實駕企位吻合）。
- **行走**：enter beat 人物逐格由台側行入（cx 由 −25／449.5 行到企位，唔係淡入企定）；walkup GIF `.on`＋complete；glamour 燕尾服繪製 14–17 次。
- **v174 五項重驗**：A1 金底獎盃 bg `rgb(242,193,78)`、22px、nw 256 complete（glamour＋reveal 兩處）；B1 open 上黑帶 147px（舊 295，v174 數字不變）、canvas 高 346px；B2 names 開場 800ms 內 frameTop 跳幅 0、第 4 張齊 653–679ms（舊 1382ms）；C2 glamour frame 372 vs reveal 640、卡列 `display:none`、canvas 底到 frame 底 26px。
- **視覺核實**（實駕截圖 1x）：won names 四人拉開企、講台企 slot 2／3 之間、地板深咗一截；gallery reveal 三人企位＋講台完整露出、得主行前；glamour 燕尾服企左邊＋海報 panel 右邊並置、金底獎盃清晰。

## §5 實駕教訓（探針問題，唔係遊戲回歸）

1. **B2 frame 跳幅 9px（won_932 第二輪）**：names 採樣尾段（t=2377）frameTop 147→156、frameH 638→620——字幕行數變化（1 行↔2 行）令 caption 高郁，唔係卡列跳位。修法：B2 跳幅改量**開場 800ms 內**（舊 bug 83px 係開場嗰陣；開場內三輪全部跳幅 0）。全程跳幅留返做 info 欄（`frameTopJump`）。
2. **gallery enter 探針誤判**：gallery 根本冇 enter beat（pan 企定亮相），初版探針照驗行走即 FAIL。修法：`enter_walk_real` 只驗 won／nominated，gallery N/A 當 PASS。
3. **nominated `force_nominated` flake（三輪）**：全跑＋兩次重試共三次 8 次重骰全部出 won（probe 層，唔係遊戲錯；v174 NOTES §9.1 同一個 flake，嗰次重跑即過）。同一樹單 case 重跑即 PASS（attempt 1，29 個不同 cx、腳底 250、comfort 250）。`drive177.json` 係合併檔：won_932／won_700／gallery_932 嚟自全跑，nominated_932 嚟自單 case 重跑——如實紀錄，唔扮一次過。

## §6 唔郁／殘留／限制

- **人物唔放大**：人仔維持 72／75／96（人物高／舞台闊 17.0%，參考圖 20.3%）。放大人物會食返啲罅，同今次目標打架；要再大，要連 canvas／frame 一齊諗，唔喺呢票。
- **入場行距短咗**：每人行距 112／132px → 92px（新 slot 離台邊 31px，舊 51／71px）。「有位行」嘅份額喺罅（17→37px）＋地板深（70→110px）＋右邊行走區（131px）＋reveal 行前（28.6→33px），唔係入場行距——NOTES 寫明，唔扮行遠咗。
- **講台留位得 1–2px**：won slot 2 右緣 193 vs 講台 194、slot 3 左緣 231 vs 229；gallery 中央右緣 193、右邊左緣 231。Draw-rect 重疊 0，實駕像素層面同樣 0（gallery 全人物 0px）；但係貼邊貼到 1px——將來人物闊／slot 再郁，呢個就係第一個要重驗嘅位。
- **底圖重構係重採樣，唔係重畫**：幕布 ×0.861 壓縮（吊燈／幕布邊輕微壓扁）、地板 ×1.587 拉伸（木紋加深）。實駕截圖目測無明顯變形；如果將來要再準，要重畫底圖，唔係再拉。
- **v174 C1–C3 未拍板**：本票唔等佢；新幾何冇掂 B2 預留暗位機制（見 §1.4），將來 C1 `max-height` 展開唔使重做舞台。
- 提名卡人像／掌聲 MP3／v149／v171／v172／v173 唔掂（同 v174 §8）。

## §7 證據

- `qa177/drive177.py`（實駕腳本，沿用 drive174 架構：FLOOR／slots／reveal 腳新錨＋enter 行走探針＋B2 開場 800ms 窗口＋gallery enter N/A）、`qa177/drive177.json`（4 case 全結果，nominated 係合併，見 §5.3）、`qa177/shots177/`（37 張逐 beat 截圖）。
- `qa177/bg_orig_424x240.jpg`（重構前底圖原檔，40,380 bytes）。
- `qa177/suite_pristine177.txt`、`qa177/suite_work177.txt`。
- 視覺核實（實駕截圖，1x）：won names／gallery reveal／glamour 三張關鍵畫面見 §4。

## §8 落地紀錄（統籌）

- 落地 2026-11-13：main 落地嗰陣仲係 `7801a72`（v175 未落地），**唔使 rebase**；squash merge `v20a177`（分支 HEAD `e88903d`）→ 遊戲 commit `f09fa1b`，51 檔 ＋18583／−32；`index.html` 淨行數 0，kwan151／tang152 唔使 resync。
- Push：第一次 egress proxy reset 斷線（Broken pipe／remote hung up），重試即得（`7801a72..f09fa1b main -> main`）。重試前 `git fsck` 曾經報一條 `missing blob 03fdbc2d…`（`tests/test_text125_static.py`），重查之後 fsck 乾淨、blob 在位——係斷線 push 嘅短暫殘留，唔係 repo 損壞，落地後 fsck 淨返 pre-existing dangling 物件。
- 線上核實（親自 curl，兩次）：第一次仲係舊版（v172，5,271,408 bytes sha `eb594747…`，Pages 滯後）；等 90 秒後重 curl：**5,271,575 bytes、sha256 `eafb7a72aa3a38d7e1aa7a0c79d5f0148fe3d8949fa86d0cedd0ee036f13a896`**，同 repo `HEAD:index.html` 逐字一致。Live 係 v177。

### 測試 resync（合併態）
- 合併態即分支態：177：53／53、174：42／42、170：47／47、160_m1：24／24、64_chibi：18／18（統籌獨立重跑，全部 PASS）；全套 pristine 235／12 vs 工作版 236／12 零回歸；實駕 drive177.json won_932 28／28、won_700 26／26、gallery_932 21／21、nominated_932 21／21（nominated 係合併檔，見 §5.3）。
