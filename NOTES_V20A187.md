# NOTES v20a187 —— 修 v181 設計 review B1＋C1–C6（一次過）

- 分支：`v20a187`（工作副本 `~/workspace/linji-work187/`）
- 基底：main `b1b6092`（v181 NOTES；遊戲 `15d97fa`）。開工嗰陣 `git fetch origin` 核實過 main 冇郁，唔使 rebase。
- 任務來源：v181 設計 review（`~/workspace/linji-design-review-v181/REVIEW.md`，155 行，44 張截圖），用戶 2026-11-13 18:37 親自拍板「一次過修」B1＋C1–C6。
- 範圍：淨係修 review 嗰 7 項，唔落地（唔做 squash merge、唔 push main、唔做設計 review）。

## 1. 修法摘要（全部入 `index.html`，淨零行數：60151 行不變，diff 33＋／33－）

### B1 地板過深（B 級）
- `FLOOR` 262 唔郁（人物腳位唔變）。`awards181DrawBase`：地板帶 y200–334（深 134px＝37.2% canvas）→ **y228–310（深 82px＝22.8% canvas 高）**；幕布 `#f2e8d5` y36–228（高 192）、側幕／燈架跟到 y228（燈杆高 188、橫檔到 y228、底檔 y224）；前緣 y310–316；觀眾席 **y316–360（深 44px，光點 6 金＋4 白散開）**。
- 注意：任務書／review 建議寫觀眾席 y310–360（深 50px），實作係 y316–360——310–316 係前緣深木邊，唔係觀眾席。數字上深 44px vs 建議 50px，視覺上觀眾席仍然完整，光點照舊。
- 效果目標（review §4 建議幾何）：地板深／人物高 1.51→~0.92，腳底以下空地板 72→48px（0.81→~0.54 倍）。實測見 §5（0.91–0.92／0.53–0.54，達標）。
- 參考圖本身係 0.64／0.43 倍——review 建議幾何刻意停喺 0.92／0.54（再窄要郁人物／牌，次選放大人物唔建議，頭頂會迫近牌底）。驗收用 review 建議幾何做準，唔係參考圖原值。
- 工人 NOTES 舊句「地板佔畫面下半約四成」係讀錯咗（參考圖實測下半 29%），唔好再信；驗收用 review §4 PIL 數字。

### C1 glamour 白牌＋海報重疊
- `.awd63-glamour-panel` 改 `justify-content:flex-end`、海報 img `max-height:60%→40%`（海報改做下半置中，唔頂住牌嘅高度）。panel 本身仲係全高暗底，牌 z-index 3 照喺上面——修嘅係海報 img 避開牌帶，唔係 panel 縮細。
- 工人 NOTES「貼住，冇重疊」已證實不成立，唔好再信嗰句。

### C2「你」＋「🏆」角標撞埋
- 揀咗卡罅方案（唔搬 🏆 去右上角——會同「你」爭同一個 `::after`／同邊）：`.awd63-cards` gap 8→24px，角標中間留 10px（24−7−7），卡列總闊 376→424px，760 框放到。🏆 仲喺左上角 `left:-7px`，「你」仲喺右上角 `right:-7px`。

### C3 out beat 人物即時消失
- out 分支照畫人物、alpha 跟 step 遞減（`fa = 1 - step*0.25`）；won 只留燕尾服阿偉（跟 glamour 一致），其餘跟 comfort 暗度（player 1／得主 0.85／其他 0.7 再 ×fa）。out 仲係 500ms，唔加 beat。
- 寫法要淨零行數：成個 out block 寫成 4 行，`}` 併入最後一行。
- `tuxedo: true` 由全 play 4 處變 5 處（reveal 行前＋企定＋walkup＋glamour＋out）。

### C4 walkup 穿過左邊提名人
- 揀最簡單穩陣做法——行緊嗰陣 `y: 6`（行前一格，前後層次），行完換燕尾服 y 歸 0。review 話「可接受，唔使即修」，但用戶已拍板一次過修，所以照修。
- 行完歸 0 嗰陣有 6px 落差，但俾換燕尾服遮住，實駕睇唔到跳位。

### C5 glamour frame 下移 124px——評估結論：keep，唔修
- 係 v174 已接受嘅 trade-off（卡列 `display:none` 殺 174px 死位），唔係新 bug。B1 改完之後 frame 高唔郁，下移照舊。
- 實駕量度：glamour frameTop − 之前 frameTop ＝ **124px**，932（123 vs −1）＋700（156 vs 32）兩個 viewport 一致。
- 唔好為修而修、唔好整爛其他 beats。呢項計做「已評估、keep」，唔當未修。

### C6 獎盃 glyph 頂離牌底得 1px
- glyph −112→−110（reveal 行前＋walkup 兩處；對手胸前 −52 唔郁）。牌底 149.4 到 glyph 頂 152，留 2.6 邏輯罅；glyph 底 170 離頭頂 173 仲有 3px。
- 其餘原位註解同步更正：`awards181DrawBase` 上面註解、`.awd181-*` CSS 註解（glyph 頂 150→152）、FLOOR 行註解。

## 2. 保住項核實（冇整爛）
- 6 beats＋walkup＋彩紙＋M9 fanfare／掌聲＋跳過掣＋M6 燕尾服 beat＋comfort beat；三行白牌（黃字 fix 30/30，實駕 36/36 樣本全過）；橫額＋數字條＋幕布＋燈架＋觀眾席光點；冇圓台講台；PixelLab 12 人物＋企位（won／nominated 60／180／300／420、gallery 75／240／405）；F1 空帶已銷帳，冇整返死位。
- Repo 紀律：SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、`?v=`（`v20a10`）冇郁；冇直改 content pack JSON；CSS 全部原位改，冇喺 L802 附近插行（kwan151／tang152 釘行唔會漂移）。

## 3. 新測試（全部 PASS＋反證乾淨）
- `tests/test_awards187_logic.js`（node，43 項）＋ `tests/test_awards187_static.py`（python，43 項）：B1 幾何（mock ctx）、C1／C2 CSS、C3／C4 play 原文、C5 trade-off 保留、C6 glyph −110、守衛（FLOOR 262、企位、beats 全長 13350ms、fanfare、彩紙、SAVE key／softRev／?v=）。
- 反證：對 pristine main `b1b6092` index（`/tmp/pristine187_index.html`，由 `git show b1b6092:index.html` 得出）跑 → 兩檔各 **21 項新斷言 FAIL**（唔 crash），守衛 PASS。
- 注意：logic test 最初 C3 切片用 `id === "out"` 會誤中 `syncConfetti149` 入面嗰句，已改用 `if(id === "out"){` 精確定位（walkup 同理）。
- Resync 咗 9 檔舊測試（斷言咗已取代舊值）：`test_awards181_logic.js`、`test_awards181_static.py`（地板／觀眾席／glyph，黃字 fix 註解 150→152）、`test_awards170_static.py`、`test_awards174_static.py`（glyph −112→−110）、`test_awards177_static.py`、`test_awards160_m4_static.py`、`test_awards160_m6_static.py`（tuxedo 4→5 處）、`test_awards166_static.py`（海報 60%→40%、tuxedo 4→5 處）、`test_awards168_static.py`（海報 60%→40%）。10 檔相關測試逐個直接跑全部 ALL PASS。

## 4. 全套 A/B
- 舊基底（`b1b6092`）：`bash qa131/run_suite.sh . qa187/suite187_work.txt` → **TOTAL PASS 253 FAIL 12**。FAIL 清單同 v181 基線 12 項一模一樣（flash51、giglib36、pacing35、poster59、rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38）；PASS 由 251→253（＋2 檔新測試）。
- 第一次跑嗰陣 `qa187/` 目錄未建立，OUT 檔頭段缺失，已重跑一次攞到完整紀錄。
- **Rebase 後（`cbc3636`，見 §8）：`bash qa131/run_suite.sh . qa187/suite187_rebased.txt` → TOTAL PASS 255 FAIL 12**，FAIL 清單同上面 12 項一模一樣；PASS 253→255（v186 基線 253＋我哋 2 檔新測試）。零回歸。

## 5. 實駕 drive187（`qa187/drive187.py`，port 8974，本地鏡像＋`python3 -m http.server`）
- 改自 `qa181/drive181.py`（真實 UI 路徑：新局 → C1 → morning chain → 請柬 modal → 出席／推辭 → 典禮全程；播種 localStorage key `starVolunteer_map_v19w` slot 1；seed pack hand-built，won 先有 `repGigId63`）。Playwright venv `/home/hatch/pwenv49/bin/python`（冇 PIL，圖像量度用系統 `python3`）；瀏覽器 `/home/hatch/pw-browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell`（headless_shell 截圖有 stale frame 殘影，DOM＋PIL／canvas 量度先係準）。932／700 × won／nominated／gallery。
- 新增量度：EVIDENCE_JS glyphTopY 150→152、glamour img／panel／board DOM 重疊、卡罅＋角標 clearance、frameTop；canvas `toDataURL` 即時 bitmap＋PIL 量 B1（地板帶／人頭頂）、C3 out 對比、C4 walkup_mid（阿偉腳 vs 提名人腳）；out polling（caption 隱藏＋won 要 glamour 已閂，80ms poll）。

### 實駕迭代（detector 問題，唔係遊戲 code 錯）
- **Run 2**：6/6 播完、0 pageerror、0 http fail、黃字 30/30，但取樣漂移 ~1.5–2s（主因：`modal_click` 後死等 1500ms 先 stage poll，t0 滯後；加埋截圖超時 5s），導致 B1 探針撞咗 suspense 暗場、out 探針全部 None、C4／C5 取樣跌出 beat。呢個問題同 v181 review §5 講嘅 stale frame／時鐘慢一致。修咗 drive：t0 改 100ms poll 即刻錨定、絕對時鐘取樣、names／walkup_mid 用 caption 錨定、截圖只留關鍵 beats（timeout 3000ms）。
- **Run 3**：時鐘準晒（real 誤差 ≤~25ms），但 B1 探針有兩個 detector bug：(a) 地板頂讀高 14px（頂部 12px highlight `rgba(255,255,255,0.10)` 令藍色分量 95→111，超出 `is_wood` 藍色容差 ±16）；(b) gallery heads 讀錯（gallery 得 3 slots 75／240／405，探針硬編 4 slots 60／180／300／420，空位誤讀地板邊界）。另外 gallery out 捉唔到——reveal 截圖慢（~1s+）拖過 out 500ms 窗口。修法：`is_wood` 藍容差 ±16→±20、`analyze_b1(im, slots)` slots 做參數、gallery reveal 唔截圖（run 2 嗰張留底）、walkup_mid 改 caption 一出現即探（唔等多 600ms，等多嗰陣已經 wp 0.83、行到 x≈140，掠過嗰刻影唔到）。
- **Gallery out 捉唔到嘅真正原因**（run 3 之後先搵到，唔係時序問題）：gallery out beat 有收尾字幕「掌聲響起——今晚完滿落幕。」（caption 唔隱藏），won／nominated out caption 係 `""`（隱藏）。探針淨係用 `capHidden` 判 out，gallery 永遠判唔到。修咗 `OUT_STATE_JS`：out ＝ capHidden 或者 caption 含「今晚完滿落幕」。針對重跑（`ONLY=gallery`，報告 `drive187_report_gallery.json`）：932_gallery out 216.0、700_gallery out 192.9，兩場都捉到。
- **Run 4（最終全套，報告 `qa187/drive187_report.json`，截圖 `qa187/shots187/` 22 張）**：以下數字全部以 run 4 為準。

### Run 4 驗收數字
- **6/6 播完，0 pageerror，0 http fail**；黃字幾何 **36/36**（subInside／subAboveHeads／boardAboveGlyph 全部 True；36 係因為 won 有 7 個樣本）。
- **B1**：地板 **228.0–310.0、深 82.0**、person_h 89.8（won／nominated）／89.0（gallery）、**floor/person 0.91–0.92**（目標 ~0.92）、**below/person 0.53–0.54**（目標 ~0.54）；heads 173／170／174／172（won／nominated）、173／174／172（gallery）。names_contrast 233.4／233.1 vs 空台 open_contrast 17.7。
- **C1**：glamour overlap **False** 兩個 viewport（overlapX 121／106.6 但 overlapY 0；imgTopAboveBoardBottom True；932 img top 396、700 img top 390）。
- **C2**：cardGaps [24, 24, 24]、minGap 24、badgeClearance 10、rowWidth 424。
- **C3**：out 對比 **won 224.5／224.5、nominated 221.9／221.9、gallery 192.9／214.2** vs 空台 17.7——6 場 out 期間人物確實在場（won 只留燕尾服、其餘全員兩條路都覆蓋埋；gallery capHidden False，收尾字幕照常顯示）。out 樣本之間數值有波動（例如 700_won run 2 係 129.4、run 4 係 224.5），係因為 out 500ms 內 alpha 遞減、取樣瞬間唔同，全部 >> 空台就得。
- **C4**：darkest_x0=**60**（932）／**50**（700），delta **34.0／32.7**（darkest ~57 vs control 90.5）——行到中段 wp≈0.45，阿偉腳區（y 268）明顯暗過提名人腳線（y 262）對照區，掠過左邊提名人（slot 60）嗰刻捉到。
- **C5**：glamour frameTop − 之前 frameTop ＝ **124px**，932（123 vs −1）＋700（156 vs 32）一致 → keep trade-off（見 §1）。
- **C6**：glyphGapPx **3–5px**（932：5／700：3–4；reveal／glamour 兩個樣本一致）。

## 6. 殘留／注意事項（畀統籌／下一票）
- C1：panel 本身仲係全高暗底，只係海報 img 避開咗牌帶；如果日後 panel 本身要縮細，係另一票。
- C3：out gallery／nominated 人物由 slot 位畫起，reveal 行前嗰陣嘅前移唔保留——同 reveal→comfort 既有過渡一致，唔係新問題。
- C4：行完 y 歸 0 嗰陣有 6px 落差，俾換燕尾服遮住；如果日後 walkup 唔換裝，要再睇。
- B1：觀眾席實作 y316–360（深 44px），review 建議 y310–360（深 50px）——310–316 係前緣，見 §1。
- 實駕 drive 支援 `ONLY` 環境變數針對重跑（例如 `ONLY=gallery`、`ONLY=932_gallery`），報告寫 `drive187_report_<only>.json`，唔會覆蓋全套報告。`drive187_report_gallery.json` 係中間針對重跑紀錄，留喺 `qa187/`。
- 進行中其他版本（唔好掂）：v186、v188（獎項改名）、v158、v159——呢票淨係掂 v187 自己嘅嘢。

## 7. Commit 計劃（兩個 commit，淨係 push 分支，唔落地）
1. 遊戲＋測試：`index.html`＋`tests/test_awards187_*`（新）＋9 檔 resync。
2. NOTES＋qa 證據：`NOTES_V20A187.md`＋`qa187/`（drive187.py、drive187_report.json、drive187_report_gallery.json、shots187/、suite187_work.txt、suite187_rebased.txt）。
3. `git push origin v20a187`（淨係去常駐 clone），`git ls-remote` 核實收到。

## 8. Rebase 紀錄（main 喺工作期間郁咗）
- 開工嗰陣 main 係 `b1b6092`；commit 嗰陣 `git fetch origin` 見到 main 已經上咗 `cbc3636`（v186 落地：遊戲 `fc76b9e`＋NOTES）。按任務書要求，兩個 commit 落好之後 rebase 上最新 main：`a803bd4`→`68007cc`、`96a3b43`→`dd8771e`，**零衝突**。
- Rebase 後核實：`index.html` 60151→**60155 行**（v186 加咗 4 行淨值），我哋嘅 diff 對新 main 仍然係 **33＋／33－**；`index.html` ＋／－行內容排序後 sha 同舊基底完全一致（`3f1b93…`），`tests/` diff 亦完全一致（`c24b85…`）——即係遊戲改動本身一字冇變，只係 hunk 位置因 v186 嗰 4 行移咗。
- 10 檔相關測試 rebase 後逐個重跑全部 ALL PASS；全套重跑見 §4（**255／12**，FAIL 清單不變）。
- 實駕 run 4 係 rebase 前跑嘅，但遊戲內容 byte-identical，所以數字照企得住，唔使為咗 rebase 重跑成套 drive。
