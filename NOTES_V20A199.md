# NOTES v20a199 — 修 v195 設計 review B1＋C1–C3

- 分支 `v20a199`，基底最新 main `b1633e6`（v198 NOTES）。
- index.html 60602 → **60646 行（淨 +44）**：DLG199 插入 +30、fitApply 正規化 +13、WF4 onload +1；兩 bust data URI 換值（行數不變）。
- 狀態：見 §8（rebase 後 `ffe3f70`）＋ §9（補測實駕完成，amend 入同一 commit 再 push）。
- PixelLab 餘額開工前核實 **4,290／5,000**（上次 4,316，期間用咗 26 次）。Fullbody 賽璐璐圖沿用 v195 嘅 media pipeline 路線，唔係 PixelLab——PixelLab documented 端點只出 pixel art，唔合 880×3056 乾淨賽璐璐全身圖規格（同 v195 做法一致）。

## 1. B1：升 tier 阿偉突然高 ~23%（唯一 B 級）——code 修，唔重生圖

根因（probe199 實測，932 viewport、舞台 468×1412／1464）：`.dlg106-char` 按闊度定大小，`dlg108FitPct` 按真闊高比計 pct，落點係「阿偉闊 ≈219px」，渲染高 ≈219/AR。s1 AR 0.343 → 640px，s2／s3 AR 0.278 → ~790px。修前實測：s1 serious painted 652.9px vs s2 783.7px vs s3 722.9px；angry s1 636.8、s2 762.5、s3 762.5。

修法（index.html，DLG108 模組內，`dlg108FitPct` 之前＋`dlg108FitApply` 內）：
- `DLG199_AWEI_REF_AR = 0.345`（＝全庫最大 AR，s1 angry 0.3446 封頂）＋ `dlg199IsAweiId`（awi／awi_s2／awi_s3）＋ `dlg199FitAr`（阿偉一律用 REF 計 fit）＋ `dlg199PctCap(stageW, stageH, maxWfrac)`（天花板 `maxW/(stageH×REF)`）。
- `dlg108FitApply` 雙人步：用 REF AR 計 fit，再加天花板；單人步：阿偉 `pct1 = min(60, cap)`，非阿偉維持 60%。`window.DLG108` 匯出加 `aweiRefAr／isAweiId／fitAr／pctCap`。`dlg108FitPct` 本身零改動。
- 兩招缺一不可——淨用 REF，ok(60)／細搭檔嗰陣仲會超天花板（阿偉×顧明輝 60%→847px，s1 painted 得 655、s2 808）；淨加天花板，fit 落點本身仲跟 tier（s1×何生 640 vs s2×何生 clamp 到 651，差 11px）。
- 附帶修正：WF4 對話圖加 `onload="try{window.__dlg108Fit&&window.__dlg108Fit(this)}catch(_e){}"`（WF4 舞台 `.sp-stage` 嘅 `.dlg106-char` 原本無 `onload __dlg108Fit`；WF4 只有阿偉一個角色）。
- 三處一齊對：對話舞台＋屋企 bust（`#home-awi`）＋頁頭 bust（即 `#home-awi` 本身，同一 DOM 面）。對話舞台經 fitApply；屋企 bust 係 data URI 換圖（C1 嗰 part），渲染尺寸 56×74 唔受 AR 影響。
- 其他角色身高比唔郁：顧明輝／阿偉 painted 比由舊失真 1.108 回復 **1.050**（v109 嘅 1.05），彭少祺 0.85；何生 painted 恒 617px（撞帽 letterbox，不變）。

驗證：
- `tests/test_awei199_logic.js`：**55 項 PASS**（抽 DLG108 模組切片 eval＋手造 fake stage／img）。覆蓋：9 個阿偉 AR × 7 個搭檔 painted 高 spread ≤1px、fit 落點同 tier 無關、淨空 ≥12px；單人阿偉天花板 46.1%（468×1412）／44.5%（468×1464）；非阿偉配對／單人零影響（fitPct 錨點：方小龍＋Vera 390×844 舞台 54–56%、典型配對 60%）；反證舊行為 s1 639.6px vs s2 790.7px vs s3 789.3px（差 ≥100px）；**e79 巧遇分支（isEnc：margin sw*0.04＋.e79-char 選擇器）**：阿偉×Vera 三 tier 617.0–617.0px、pct 唯一 43.7%、淨空 12.1px。
- `tests/test_awei199_static.py`：**FAILURES: 0**。REF＝0.345 且 ≥ 全庫最大 AR 0.3446；fitApply／單人步／匯出字串檢查；DLG109 表原封不動；WF4 onload；C1 bust sha 對 `crop199.json`；C2／C3 新 angry 圖規格＋ sha ≠ v195 舊版；s1 angry＋s2／s3 serious 原封不動。
- 兩檔新測試對 pristine main（`b1633e6`）乾淨 FAIL（logic 1 FAIL、static 14 FAIL），唔 crash。
- 實駕（`qa199/drive199.py`，932／700）：**未跑——沙箱寫入封鎖令 chromium launch 即死 SIGTRAP**（profile 寫唔到，見 §6）。DOM 量度＋截圖證據要等 filter 鬆返先補跑。

## 2. C1：s1／s3 細 bust 要睇第二眼——收緊裁切＋恤衫色對比

修法（`qa199/crop199.py`，v109 嗰套幾何改）：裁切 FRAC 0.30→0.24（裁得貼啲，面大 ~25%）；恤衫色對比只改裁切後下半區 y≥55%：s3 中性亮像素向純白拉 60%、s1 偏藍像素加深 R×0.88／G×0.93／B×1.02；面部零誤觸（面部區兩款 mask 命中率 ≤0.02%）。s2（淺灰西裝）唔郁。角色本身個樣唔郁。

結果（`qa199/bake199_bust.py` 焗入 index.html，240×312 WebP q80，米白底）：
- hero_awi（s1）：box [141,0,399,335]、8,264 bytes、sha `306d05ac9142…`（舊 `eeb868f109c2`）。
- awi_s3：box [145,0,584,571]、7,254 bytes、sha `e545e378aa36…`（舊 `47239ff2f4bf`）。
- 並排對照（`/tmp/bust_compare_4x.png` 舊 s1｜新 s1｜s2｜舊 s3｜新 s3；`/tmp/bust_compare_actual.png` 實際 56×74）目視接受：恤衫 V 更大更易讀，s1 淺藍恤衫 vs s3 白恤衫一眼分到。
- 校準量度：恤衫區（y≥62%、x 35–65%）s1 藍像素 48.2%、中性亮 3.1%；s3 中性亮 38.7%、藍 0.2%。
- `tests/test_bust109_static.py` 已更新：hero_awi／awi_s3 改認 `qa199/crop199.json`（2 鍵），其餘 19 鍵沿用 `qa109b/crop109.json`，加斷言新 sha ≠ 舊值。斷言本身全部 PASS（見 §5：全套嗰陣佢係 8 項環境假 FAIL 之一，crash 喺收尾反證 mkdtemp，唔係斷言）。

## 3. C2＋C3：angry 圖——加強同 serious 區分＋三 tier 統一畫法（以 s2 為準）

- C2：加強兩張 angry 圖（s2／s3）同同 tier serious 嘅區分——眉壓再深半級／嘴角再向下多啲。
- C3：三張 angry 圖統一畫法／統一面部結構，以 s2 嗰套為準（眉心皺紋、去紅印），重畫 s3 angry 面部跟 s2。s1 angry 係舊資產，今次唔郁佢本身；s3 跟 s2 改之後 s1 同 s3 會唔同，呢個係預期結果。
- 出圖：media pipeline（同 v195 路線），成張重生，風格錨 `~/workspace/linji-native-design/style-anchor-awei-anime.jpg`。s2 angry v2（snapshot `d665d21f…:c58rzp`，raw 832×2912 RGB）：淺灰西裝不變，眉壓更深＋眉心直紋更深、眼眯、嘴角更向下、無紅印。s3 angry v2（snapshot `568f506e…:dpffgt`，以新 s2 v2 做面部參照＋舊 s3 angry 做底）：深藍西裝＋白恤衫開領＋單手插袋不變，面部跟 s2 嗰套（眉心皺紋、去紅印、嘴角更向下），側分髮保留。
- 焗入（`qa199/bake199.py`，改編自 `qa195_bake195.py`，白底 flood-fill 切透明，保留米白光邊）：兩張皆 **896×2976、AR 0.3011、邊帶米白 1.0、零遠處米白、畫框 100% 透明、內部差異 <1.0，ALL OK**（`qa199/samples199/bake199_results.json`）。
- 面部對照 strip `/tmp/face_compare199.png`（s1 angry 舊｜s2 新｜s3 新｜s2 serious｜s3 serious）目視接受：C2 兩張新嬲樣明顯嬲過同 tier serious；C3 s2／s3 同一套畫法，s1 舊樣（有紅印）同 s3 新樣明顯唔同。
- 舊版 sha（v195，唔再用）：s2 angry `aa50c70e…`、s3 angry `f863fef6…`。s1 angry `8508c88d…`、s2 serious `0a8b8e82…`、s3 serious `e05c2fe8…` 今票唔郁，static test 釘死。

## 4. 測試 resync（10 檔，全部係行號漂移，唔係回歸）

- `qa199/resync199.py`：difflib 對位 pristine `b1633e6` → 工作版，hunks 淨係 v199 改動（兩 bust data URI 換行、DLG199 插入 +30、fitApply 5 個 replace／insert、WF4 onload +1），**全部釘內容逐字相同，BAD: 0**。總行數 60602→60646。
- 2 個行為斷言更新（預期行為有意改咗）：`test_dlg108_static.py` 單人步檢查 `stage.style.setProperty('--dlg108-char-h', pct1 + '%');`＋`var pct1 = 60;`；`test_dlg109_height_static.py` 單人步 `pctOf(pct1, scaleOf(imgs[0]))`＋`var pct1 = 60;`。
- 8 檔行號 resync（difflib 映射，逐個釘內容核實）：gift185（總行數）、tang171／tang173（總行數＋openLoc DEF 55095→55139／lines[55138]）、rom176（6072／31586→31629／53525→53569／53893→53937／55032→55076／55126→55170）、tang152（lines()[31512]→[31555]、[31656]→[31699]；HELD 25818 唔郁）、kwan151（27217→27260／27250→27293／31023→31066／31031→31074／31032→31075／31074→31117）、text125（27742→27785／27871→27914／33574→33617，1-based；0-based ls 27784／27913／33616）、travel114（COUNT 12 項＋FREE 34 項＋DEF 55095→55139＋WRAPPER 44436→44480）。
- 教訓：第一輪 resync 腳本將 text125／tang152 嘅 0-based 釘當咗 1-based 映射，驗錯上一行（text125 錯一格，tang152／tang171 數值撞啱無影響）。已修正：PINS 一律存 1-based，apply 嗰陣先 −1；修正後 dry run 再核實 `text125_0based L27742 -> L27785 OK`（內容 `const lines = Array.isArray(b.lines)...`）先落手。
- resync 期間沙箱寫入封鎖令 `test_tang152_static.py` 俾截斷成 0 bytes（open 截咗、write 先 EPERM），之後 rm 咗再由 `git show HEAD:` 攞全文、用 `muse.write` 寫返 resync 版；`git diff` 核實淨係 3 處預期改動（v199 註解行＋兩釘）。

## 5. 全套 A/B

- 寫入封鎖下 `qa131/run_suite.sh` 嘅 shell redirect 會整出假 FAIL，改用 `qa199/run_suite_mem.py`（subprocess 捉 output，零寫檔）。
- Run 1（封鎖前，`qa199/suite_work199.txt`）：**261 PASS／22 FAIL**（12 基線＋10 resync）。
- Run 2（resync 後，in-memory runner）：**263 PASS／20 FAIL**（283 檔）。10 項 resync FAIL 全清；12 項基線不變（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38）。
- 新增 8 項 FAIL 全部係**環境假 FAIL，唔係回歸**：bust109／dlg107／dlg119／dlg123／dlg126／dlg127／dlg138／story157_index——全部喺 `tempfile.mkdtemp` 嗰陣 crash（`FileNotFoundError: No usable temporary directory found in ['/tmp', '/var/tmp', '/usr/tmp', ...]`，寫入封鎖所致）。bust109／dlg107／dlg119／dlg123／dlg126／dlg127／dlg138 斷言本身零 FAIL（分別 43／40／59／35／101／161 個 PASS 先 crash）；story157 喺 L99 setup 位 crash（0 PASS）。Run 1 嗰陣呢 8 檔全部 PASS（封鎖前）。
- 相關測試逐個直接覆驗：dlg108／dlg109／gift185／kwan151／rom176／tang152／tang171（22／22）／tang173（21／21）／text125／travel114／bust109（斷言全 PASS）／awei199 logic（55 PASS）／awei199 static（FAILURES: 0）——全部 PASS。
- 結論：**零回歸**（FAIL 清單＝12 基線＋8 環境假 FAIL）。

## 6. 環境：沙箱寫入封鎖（2026-11-13 約 14:57 起，寫 NOTES 嗰陣 15:2x 仍然存在）

- 現象：shell／python 任何檔案內容寫入都 `PermissionError: [Errno 1] Operation not permitted`——連 2-byte flush 都唔得；`echo hi > 檔`一樣 EPERM；`git hash-object -w`／`git checkout`（index.lock）／`git add` 全部唔得；`tempfile.mkdtemp` 話冇可用 temp dir；chromium launch 即死 SIGTRAP（profile 寫唔到）。
- 假象排除：早前一度以為係「單次 write ≥8192 bytes 先擋」——錯。8191 bytes「成功」只係因為 error 喺 GC close 嗰陣俾吞咗，檔案實際 0 bytes；`os.write` 100 bytes 一樣 EPERM；`/dev/shm` 同樣封（syscall 級，唔係路徑級）。`touch`／`rm`／`mkdir`／讀取唔受影響；`muse.write`／`muse.edit`（runtime 通道）唔受影響。
- 時序：14:57 `test_rom176_static.py` 寫入仲成功（11,985 bytes，之後 ALL PASS）；~14:59 起所有 shell 寫入失敗，至今持續。
- Workaround（已用）：測試檔改動一律經 `muse.edit`／`muse.write`；resync 腳本改做 chunked＋temp＋rename 都係唔得（filter 擋所有 shell 寫入），最後放棄腳本寫入、用人手 edit；全套改用 in-memory runner。
- **未做到、要補**：
  1. 實駕 `qa199/drive199.py` 未跑（chromium 起唔到）。B1 舞台逐 px 量度、C1 bust 並排、C2／C3 目視、WF4 現場檢查全部未驗——要等 filter 鬆返先補跑（腳本已備妥，screenshot＋report JSON 已包 try/except，唔會因寫唔到而中斷）。
  2. commit＋push 未做（git 寫入封死）。`git status`：M `index.html`、`assets/story/fullbody/awi_s2_angry.webp`、`awi_s3_angry.webp`、14 個測試檔（見下）；?? `qa199/`、`tests/test_awei199_logic.js`、`tests/test_awei199_static.py`。落地由統籌做；commit 嗰陣要 `git add` 明確加新檔（唔好用 `git add -u`）。
  3. 8 項環境假 FAIL 喺 filter 鬆返之後要重跑確認返 PASS。

## 7. 殘留／唔做（跟任務定義）

- v198 C1（播完 C6F 鎖行唔見「今日已經播過一幕主線」）唔喺呢票。
- 開局 `#start-hero` 舊 s1 圖未郁（已知殘留，另開一票）；唔郁其他角色身高比、地圖「返屋企」掣。
- v195 NOTES §2 已知取捨唔郁；唔郁 `playerTierMax` 寫入／讀取／backfill、tier 判定、內容。
- 新測試檔：`tests/test_awei199_logic.js`、`tests/test_awei199_static.py`；qa 物件：`qa199/`（probe199、drive199、crop199、bake199、bake199_bust、resync199、run_suite_mem、samples199、suite_work199.txt）。
- `qa199/resync199.py` 入面嘅 `write_file`（chunked＋temp＋rename）喺封鎖下仍然唔 work——留返做記錄，唔好以為佢係解法；真正解法係經 runtime file tools。

## 8. 統籌接手：寫入封鎖、反證、rebase 上 v194 main

- 工人交貨嗰陣沙箱寫入封鎖（約 14:57 UTC 起），實駕未跑、commit＋push 未做。統籌接手嗰陣封鎖間歇性鬆緊：`echo 9 bytes > 檔` 得、`git fetch origin` 連續 16 次 EPERM（`fetch-pack: invalid index-pack output`）、`git show > 檔` 0 bytes。解法：工作副本 `.git/objects/info/alternates` 指去常駐 clone（一個 echo 寫入），之後 `git cat-file` 讀到 `a1a6681`；`git add`＋`git commit`（`01ddc60`）喺開窗嗰陣成功。
- 反證（統籌親自重跑，唔信工人舊數）：新 logic test 對住常駐 clone index.html（v194、無 v199）→ `RESULT FAIL (no DLG199)`；新 static test → `FAILURES: 14`，同工人報嘅 pristine `b1633e6` 反證一致。
- Rebase 上最新 main `a1a6681`（v194 NOTES，遊戲 `707ff66`，live 5,349,830 bytes）：`index.html` 自動合併乾淨；5 檔測試衝突（全部係行號 resync，gift185／rom176／tang171／tang173／travel114）——v194 嘅 resync 同 v199 嘅 resync 改咗同一批釘行。解法：`/tmp/map194.py` difflib 對位 `a1a6681`→rebase 後 index.html，57 個釘行內容逐字相同，**BAD: 0**（淨 +44 行，60667→60711；hunks 淨係 v199 改動）；逐檔用 muse.edit 解衝突（唔好信任何一邊嘅數字——例如 travel114 COUNT 59220 嗰個，兩邊數字都錯，正確係 59264；rom176 53590 正確係 53634）。`GIT_EDITOR=true git rebase --continue` 成功，新 HEAD `ffe3f70`。解完 10 檔相關測試（gift185／rom176／tang171 22/22／tang173 21/21／travel114／dlg108／dlg109／bust109 FAILURES: 0／awei199 logic 55 PASS／awei199 static FAILURES: 0）全部 PASS。
- `qa199/samples199/`（432K raw 生成圖＋json）唔入 repo（跟 v147／v195 前例，留喺工作副本）；`qa199/shots/` 空。`alternates` 檔留喺工作副本 `.git`（唔入 repo），push 之後工作副本靠佢讀 v194 物件，落地唔受影響。
- 全套 A/B（統籌親自重跑，`qa131/run_suite.sh`，rebase 後最終樹）：pristine `a1a6681` **271 PASS／12 FAIL** vs 工作版 `ffe3f70` **273 PASS／12 FAIL**，FAIL 清單逐行相同（12 項穩定 pre-existing：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），**零回歸**；+2 PASS 啱啱係兩檔新測試。工人 Run 2 嗰 8 項環境假 FAIL（mkdtemp crash）今次全部清返，證實係環境唔係回歸。

## 9. 補測實駕（統籌親自跑，寫入封鎖鬆返之後）

- `drive199.py` 44/50，6 項 FAIL 全部係**探針 bug，唔係產品問題**（統籌診斷，見 `qa199/diag199.py`）：
  - C1 屋企 bust（932＋700）：drive 先讀 `#home-awi`，唔見就直 call `enterHome(null, false)`——`enterHome` 係 IIFE 內部函數，唔係 global，throw 咗之後屋企永遠唔開，rect 0／natW 0。正確 UI 路徑（v195 review 已證實）：地圖「進度」掣→屋企。另一個坑：「進度」掣實際文案係「進度2」（`#chip-story`，帶計數），exact 文案「進度」撳唔到；返地圖要用 `#home-back-map-tabs`（id），唔用文案（地圖有兩粒同名「返回地圖」掣）。
  - WF4（932＋700）：drive 直接喺 page context call `wf4DlgCharsHtml108(...)`——同樣 IIFE 內部，`ReferenceError`。
  - C2／C3：`drive199.py` 根本冇獨立 check（50 項入面只有表情鏈＋自然尺寸）；工人嘅 `/tmp` 對照圖（`bust_compare_*.png`／`face_compare199.png`）亦已隨 `/tmp` 清空——要統籌自己重新做目視對照。
- 補測 `qa199/drive199_sup.py`：**12/12 PASS，0 pageerror、0 http fail（932＋700）**。C1 三 tier 屋企 bust rect 一致 56×74（932 x358 y282；700 x167 y290）、complete＋natW 240、src 逐 tier 對上三個 bust data URI（`hero_awi`／`awi_s2`／`awi_s3`）。**WF4 嗰個 PASS 係假陽性**——量到嘅係殘留強制播故事（F4《上岸路》）嘅 img，唔係 WF4 場景（嗰陣日數根本冇推進，401→401）；已作廢，由下面專項取代。
- WF4 專項 `qa199/drive199_wf4.py`：**8/8 PASS，0 pageerror、0 http fail（932）**。流程：清場（撳晒 F4《上岸路》強制播 37–38 下）→ tier 設 1（滿足 day02 cond `tierMax:1`；pending 事件本身唔驗 cond，設 1 係防萬一）→ 播種 pending `wf4_ev_day02`（pendingDay=401）→ 過一日（401→402，`pendingMaxAge=2`，tick 唔會清走）→ 晨鏈排水（小休 sheet「返回地圖」→ 台慶請柬「推辭」→ 報紙「關閉」）→ WF4 場景「傳呼台嘅一課」呈現（識別用 beat 原文「Call機響起一串密碼數字」／「520、3344」——標題本身唔渲染）→ pending 清＋seen 入 → img 有 onload `__dlg108Fit`（`awi_base.webp` 獨角）→ 撳「繼續」入 beat 後 fit 有落手（inline height 60%，paintedH 286.8px，stage 480px，零溢出）。診斷要點：晨鏈次序係請柬→報紙→aud91→WF4，唔推辭請柬就永遠等唔到 WF4（第一版專項就係卡喺請柬，15 秒乜都等唔到）；`wf4PresentPending`／`wf4BaseOk`／`todayIsForcedDay` 全部 IIFE 內部，唔可以直接 call；第一版專項誤用標題匹配，WF4 場景出咗都認唔到，仲俾 drain 撳走咗——改用 beat 原文先捉到。
- PIL 目視對照（統籌親自睇，`qa199/shots_sup/c1_bust_compare.png`／`c2_face_compare.png`／`c3_angry_compare.png`，原圖裁切，唔係生成圖）：C1 實際尺寸（56×74）一眼分到——s1 淺藍恤衫＋bomber、s2 淺灰西裝、s3 深藍西裝＋白恤衫；4x 更加分明。C2 同 tier angry vs serious 分明（嬲樣眉心皺紋＋瞇眼＋抿嘴；serious 平嘴正常眉）。C3 s2／s3 angry 同一套畫法（眉心皺紋、去紅印）；s1 舊圖有面紅印、畫法唔同——按任務書 s1 唔郁，s1 同 s3 唔同係預期結果。
- `qa199/shots/` 而家有 `drive199.py` 嘅 12 張 T2 舞台截圖（§8 寫嗰陣係空）；`shots_sup/` 有補測證據（6 張 bust element 截圖＋1 張全頁屋企圖＋WF4 場景／beat 圖＋3 張 PIL 對照圖）。`diag199.py`／`diag199b.py` 係診斷腳本（留檔），diag 截圖已刪。`samples199/` 照舊唔入 repo。
