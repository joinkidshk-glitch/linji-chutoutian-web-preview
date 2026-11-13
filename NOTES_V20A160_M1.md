# NOTES — v20a160 M1 會場場景圖做典禮底圖

- 分支：`v20a160-m1`（工作副本 `~/workspace/linji-work160-m1`，基底 main `e08a070`＝v148）
- 狀態：code＋單元測試＋實駕已完成（見 §6／§7）；唔落地、唔開 PR（落地由統籌做）。
- SAVE key／softRev／`?v=` 一律無郁；無直改 content pack JSON；無新生成（M1 樣本沿用）。
- index.html：58,904 → **58,911 行（＋7 行）**；新檔 1 張圖＋新測試 1 檔＋更新測試 2 檔。

## 1. 落點決定——現有底圖係咩、點換

- 現有典禮舞台底圖係 **v20a62 內嵌像素舞台**：`const AWARDS62_STAGE_PX`（L45000，`data:image/webp;base64`，
  24,872 base64 字元；2048×1152 原圖縮 424×240 WebP q82），canvas backing store **424×240**
 （`<canvas class="awd62-canvas" width="424" height="240">`，CSS 框 `width:min(96vw,760px)`、
  `image-rendering:pixelated`）。`awards62PlayCeremony` 每次播典禮 `new Image()` 載入佢畫做底圖；
  載入失敗跌返 `awards62FallbackStage` 程式格仔舞台（深紫＋紅側幕＋金邊，唔係相）。
- 換法：**成個 data URI 撤走，改行檔案路徑常數**
  `const AWARDS62_STAGE_BG = "assets/story/awards/bg_awards_ballroom.jpg";`，
  loader `im.src = AWARDS62_STAGE_PX;` → `im.src = AWARDS62_STAGE_BG;`。
  其餘典禮 code 一字唔郁（`draw()` 1:1 畫 `bgImg`、`pan` beat 440 闊橫移畫法、fallback、
  canvas 424×240、`imageSmoothingEnabled=false` 全部保留）。
- 點解唔保留 data URI 做後備：① 檔案路徑係全 app 慣例（地點場景圖、海報 master、精靈圖全部行檔案）；
  ② 載入失敗已有設計好嘅程式格仔舞台兜底（v62 註解寫明）；③ 新檔名唔會撞舊快取，唔使 `?v=`。
  移除後 index.html 細咗約 24KB base64。
- 舊 v62 標頭註解（L44997–44999）同步改寫，唔留「像素舞台底圖」舊描述；B 註解（L45761）
  改做「會場實景底圖 AWARDS62_STAGE_BG（v20a160 M1）」。

## 2. 資產位置＋檔名

- 位置：**新目錄 `assets/story/awards/`，檔名 `bg_awards_ballroom.jpg`**——唔跟 `assets/story/locs/bg_*.jpg`。
  理由：會場唔係 15 個地圖地點之一（唔係玩家可以去嘅地方），唔應該入 `locs/`；
  典禮資產（M4 上台 GIF、M6 燕尾服、M5 彩紙、M9 音樂）將來有同一個家，`awards/` 係自然嘅落點。
  檔名望落知係典禮會場（`bg_awards_ballroom`）。
- 檔案：424×240 JPEG q88，39,211 bytes。來源 `~/workspace/linji-work147/samples147/m1_ballroom.png`
  （400×224，pixflux，1 次；參照相係真實香港相——港島香格里拉大禮堂，留檔
  `m1_ref_island_shangrila.webp`；報告見 `~/workspace/linji-work147/samples147/SAMPLES147_REPORT.md` M1 一節）。
  驗收（報告原話）：紅幕舞台＋金色講台＋水晶吊燈＋兩排白椅＋紅地毯，無人、無字、無 logo。

## 3. 裁切／放大做法（系統 python3＋PIL，唔拉變形）

- 原圖 400×224（比例 1.7857）vs 目標 424×240（1.7667）：**兩側各裁 2px → 396×224
  （比例 1.7679），再等比放大（LANCZOS）→ 424×240**。殘差 0.07%，肉眼唔可見。
- 點解裁闊唔裁高：裁高要由 224 裁到 226.4（反方向，唔夠高）；裁闊只係左右各 2px，
  邊緣係均勻深木牆板（逐列量過，左右 4 欄 mean RGB 約 (147,105,80)，幾乎一樣），裁完零可見損失。
- 頂部吊燈原本已裁一半（樣本報告小瑕），**冇再裁主體**：吊燈、紅幕、講台、白椅、紅地毯全部完整入鏡。
- 原圖 alpha 全 255（不透明），直接轉 RGB 存 JPG；q88（跟地點圖 q≈85 慣例）。
- 已知限制：canvas backing store 424×240，CSS 框放大到 760px 闊時 `image-rendering:pixelated`
  會將相片以最近鄰放大 ~1.8 倍——相片邊緣會比原生 424 睇落硬淨／粒狀少少，同像素舞台本身
  嘅 8-bit 風格一致，接受。將來 v149 放大舞台框會再放大呢個效應（見 §5）。

## 4. 邊幾場典禮用新底圖

- **四場典禮＋贏／入圍落選／旁聽三分支，全部共用同一張底圖。**
- 理據（code 實證）：`awards62PlayCeremony` 入面得一個 `bgImg`（單一 `new Image()`＋單一 `im.src`），
  `draw()` 全部 beats／全部分支都畫同一張 `bgImg`；四場典禮（廣告賞／金碟夜／影藝獎／台慶）
  全部行同一個 `awards62PlayCeremony`，code 入面冇任何按場次／按分支分底圖嘅邏輯。
  會場係同一個地方（金禧大酒店大禮堂），一張底圖係正確嘅語義。
- 新測試 pin 死「共享引用點」：`const AWARDS62_STAGE_BG = ` 同 `im.src = AWARDS62_STAGE_BG;`
  全檔各出現一次。
- 實駕 bonus case `gallery_932` 證實旁聽分支都係同一張底圖（見 §7）。

## 5. v149 rebase 風險（v149 未落地，呢票唔預設佢嘅數）

- v149（典禮舞台放大＋M5 彩紙）未落地；佢落地之後舞台幾何可能變：
  ① 如果 v149 改咗 canvas backing store（例如 424×240 → 更大），呢張 424×240 底圖照樣 work
  （`drawImage` 會放大），但會再粒狀啲——嗰陣要考慮由 400×224 原圖重新出大尺寸版（pixflux 上限
  400px 闊，要另外諗辦法，唔係 M1 範圍）。
  ② 如果 v149 改咗 `.awd62-frame` 闊度／`image-rendering`，相片放大倍率會變，同 §3 限制一樣。
  ③ v149 嘅 M5 彩紙 overlay（reveal beat）會疊喺呢張底圖上面——M1 唔使改 code 接佢，純粹視覺疊加。
  ④ v149 唔會郁 `AWARDS62_STAGE_BG` 呢個常數名（除非佢重寫成個舞台），rebase 衝突預計只係行號漂移。
- 落地次序建議：M1 同 v149 邊個先行都得；如果 v149 先行，M1 rebase 嗰陣要重驗 canvas 幾何同埋
  `draw()` 嘅 `bgImg` 畫法有冇變。
- 另外：main 已經郁咗（開工嗰陣 e08a070，期間 v156 上咗 main `9c850f9`；v151 亦已上線）。
  呢個分支 base 保持 e08a070（按任務），落地嗰陣要 rebase。

## 6. 測試

- 新測試 `tests/test_awards160_m1_static.py`：**19/19 PASS**（常數在位＋舊 data URI 全檔消失＋
  共享引用點各一次＋檔案在位／JPEG magic／10–200KB／424×240／比例 ≈424/240＋loader 用新常數＋
  onerror 降級＋draw() 1:1＋pan 440＋fallback 在位＋canvas 424×240＋pixelated＋SAVE key／softRev s107／
  `?v=v20a10` 唔郁＋路徑唔帶 `?v=`）。
- 反證：新測試對 pristine main（`~/workspace/pristine160/`，e08a070）跑——**9 FAIL，乾淨，唔 crash**
  （exit 1；其餘 10 項同 M1 無關嘅斷言照 PASS）。
- 更新咗嘅舊測試（pin 改版，唔係放水）：
  - `tests/test_awards62_static.py`：舊兩項「像素舞台底圖在位（WebP data URI）／base64 ≤150KB」
    改為新常數＋loader pin。更新後 **ALL PASS**。
  - `tests/test_poster59_static.py`：**唔郁**。佢入面 `src.count('data:image/webp') == 21` 嗰個 pin
    喺 pristine 已經 FAIL（實數 42，唔係 21——pin 早已過時）；M1 令實數變 41，一樣 FAIL，
    失敗項集合同 pristine 逐項相同，唔係新回歸。改佢唔會令成檔 PASS（仲有 10 項 master asset
    FAIL），所以留返唔郁，等擁有者決定。
- 全套 A/B（`qa131/run_suite.sh`）：
  - Pristine 基線（`~/workspace/pristine160/`，e08a070，`qa160-m1/suite_baseline160.txt`）：
    **211 PASS／12 FAIL**——注意唔係任務講嘅 210（210 係 v146 數字；v156 NOTES 已更正基線係 211）。
    12 項 FAIL 全部係已知 pre-existing（flash51／giglib36／pacing35／poster59／rumor49／slot50／
    soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38）。
  - 工作版單次全套（`qa160-m1/suite_work160.txt`）：161／63——**唔係回歸，係環境波動**
    （AGENTS.md v151 教訓：同一 repo 連續跑出 211/12、137/86、200/23；失敗項每次唔同、全部係 .py）。
    按 v151 教訓處理：將 work 多出嚟嘅 51 項逐個直接重跑（`qa160-m1/rerun.sh`，
    `qa160-m1/rerun_out.txt`）：第一輪 50/51——唯一 FAIL 係 `test_travel114_static.py`
    （真問題：M1 令 index.html 淨 ＋7 行，佢係行號釘死測試，見下）；修復後第二輪 **51/51 PASS**。
  - **結論：工作版實際係 212 PASS／12 FAIL**（基線 211＋新測試 1 檔；12 項穩定 FAIL 同基線逐項相同），零回歸。
- `test_travel114_static.py` resync（真．行號漂移，唔係 flake）：
  - M1 改動令 index.html 淨 ＋7 行（常數段 1 行 → 6 行，＋5；v62 標頭註解 3 行 → 5 行，＋2；
    B 註解＋loader 原地改，行數不變），改動點約 L44998。
  - 核實（`qa160-m1/resync_travel114.py`，difflib 對位）：3 個 replace 段、44 個 `openLoc(` 呼叫點
    逐字一致、41 個釘行內容逐行相同，純漂移；COUNT 13／FREE 27 不變；DEF 53562→**53569**、
    WRAPPER 44171 不變（佢喺改動點之前）。**RESYNC-OK**。
  - 已套用（＋resync 歷史註解行）；重跑 **RESULT PASS**。

## 7. 實駕（Playwright，`qa160-m1/drive160m1.py`，port 8987）

- 方法：新遊戲 → 播種（贏分支：fame 150＋credit_delta 80＋3 部 1991 電影主角作 q=1.0＋
  2 部跨媒介主角作，base ≈0.90，`debugForceSeasonWindow` 重試到 `bestOutcome==="won"`）
  → 出席 → open beat 取 canvas 像素樣本（吊燈／紅幕／講台／白椅／紅地毯五點，對照舊像素舞台
  深紫 #241736＋黑地板）＋截圖 → 全程計時 → reveal → 結果卡；0 pageerror／0 failed request。
- 第一輪（port 8973）**作廢**：server Popen 靜默撞 port（隔籬 agent 佔咗 8973），browser 食咗
  隔籬嘅舊 index.html——截圖係舊像素舞台（有聚光燈＋金流蘇嗰張），像素檢查 FAIL，之後幾輪
  全部 `ERR_CONNECTION_REFUSED`。教訓：drive 唔可以假設 port 攞到，一定要驗證 serve 緊嘅檔。
  第二輪已修：`start_server()` 起 server 後即驗（served index.html 含 `AWARDS62_STAGE_BG`
  且無 `AWARDS62_STAGE_PX`，否則 fail fast）＋每 case 前 `ensure_server()`＋結果唔好俾 ERROR 蓋過 FAIL。
  第二輪 `gallery_932` 已 PASS（見下），但兩個 won case 撞正兩個 harness bug（見下），第三輪先全過。
- 第二輪教訓（harness bug，唔係 game code）：
  ① `sample_canvas_multi` 插入嗰陣食咗 `def bg_resource(pg):` 嗰行——`bg_resource` 未定義，
  won case 行到一半擲 `NameError`；已補返定義行。
  ② 「新遊戲」click 喺負載重嗰陣等 navigation settle 超時（`waiting for scheduled navigations
  to finish`）——已改 `no_wait_after=True`。
- **第三輪（port 8987，server 已驗證）OVERALL 3/3 PASS，一次過，0 pageerror／0 failed request**
  （`qa160-m1/drive160m1.json`；截圖 `qa160-m1/shots/`）：
  - `won_932`：11/11——pack won（score 0.886，force 1 次）、請柬＋出席、舞台出現、跳過掣可見、
    **像素樣本證實係會場相**（吊燈 lum 211 RGB(231,211,160)／白椅 214／紅地毯 96／meanLum 126；
    舊像素舞台深紫底 meanLum 約 25）、**底圖檔案真係載入咗**（resource transferSize 39,511 bytes＝
    JPG 實際大小）、reveal「得獎！影壇新面孔（臨記組）：《龍城歲月1》」2102ms、總長 7513ms
    （watch 由 enter beat 開始計）、舞台播完消失、結果卡「得獎 · 影壇新面孔（臨記組）」
    （幕前聲望 +1 · 業內信用 +3）。canvas 框 x=12／y=295／w=406／h=233——同 v147 review
    嘅 932 舞台框 top 295 吻合。
  - `won_700`：11/11——同一組樣本（吊燈 211／白椅 214／meanLum 126）、底圖載入 39,511 bytes、
    force 3 次先贏（taste 重抽）、reveal 贏、結果卡、0 pageerror。canvas 框 y=179。
  - `gallery_932`（旁聽分支 bonus）：7/7——同一張底圖（樣本 meanLum 165、吊燈 227、白椅 211、
    紅地毯 200）、6 beats 完整宣佈弧（唱名廖炳星／陸柏言／魏詠男→懸念→揭曉廖炳星憑《離岸的信》得獎→
    散場）、總長 7088ms、結果卡、0 pageerror。
- 目視證據：`won_open_430x932.png`／`won_open_430x700.png`／`gallery_open_430x932.png`——
  紅幕＋金講台＋水晶吊燈＋兩排白椅＋紅地毯全部入鏡，人仔企喺紅地毯上面；`won_reveal_430x932.png`
  係揭曉嗰刻（卡片列＋「得獎者是……」字幕，底圖一樣係會場相）。截圖時序註：負載重嗰陣 evaluate
  慢，open 截圖有時滑入 enter／pan beat（有人仔入鏡），但像素樣本本身係 open beat 攞嘅，
  斷言唔受影響。

## 8. 未解決事項

- v149 rebase 風險（見 §5）：舞台幾何／canvas 尺寸可能變，落地嗰陣要重驗。
- `test_poster59_static.py` 嘅 webp count pin（21 vs 實數 41）早已過時，唔係 M1 造成，留返唔郁。
- 實駕第一輪 port squat 教訓已修（drive 內置 server 驗證），但 port 係共享資源，將來其他票用
  8973／8987 嗰陣都要先驗證。
- 工作副本 `core.sshCommand` 曾經係已死嘅 18080 隧道（開工嗰陣設定），已按 AGENTS.md（v156 教訓）
  改行 `~/workspace/gh_tunnel.py`（同常駐 clone 一致）；push 前已驗證。
- `~/workspace/pristine160/`（e08a070 worktree，623M）係今次基線／反證用嘅臨時副本，用完可刪；
  `~/workspace/linji-work160-m1/qa160-m1/work_fails.txt`／`base_fails.txt`／`rerun_list.txt`／
  `rerun.sh`／`rerun_one.log` 係 A/B 覆驗中間檔，留喺 qa160-m1 供查閱。
