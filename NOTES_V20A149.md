# NOTES_V20A149 — v149 剔走觀眾席剪影帶（方向 1）

工作副本 `~/workspace/linji-work149/`，分支 `v20a149`，基底 `da90957`（v146 NOTES）。
本票只做一件事：喺原工人 95f82641 已有改動之上，剔走典禮舞台上下兩條觀眾席剪影帶
（用戶 2026-11-13 12:09 方向 1：典禮場景只需要舞台，唔需要台下部分）。
**本票唔落地**（落地由統籌做）；v170 Phase 2（新舞台-only 底圖）另一分支平行進行，冇掂佢嘅檔案。

## §0 範圍

### 剔走咗嘅嘢（index.html 淨 −16 行：CSS −14／JS −2）
1. CSS：`.awd62-aud149` 成條規則（8 個 radial-gradient 橢圓＋深紫漸變）＋
   `.awd62-aud149.bot{transform:scaleY(-1)}`，連同上面兩行註解一併刪除。
2. CSS：`.awd62-stage` 還原——刪 `flex-direction:column`（橫向置中 flex 返原狀）；
   `.awd62-frame` 還原——刪 `flex:none`（同屬觀眾帶佈局）。
3. JS：`stage.innerHTML` 刪 `'<div class="awd62-aud149 top"></div>'` 一行（開頭還原做
   `'<div class="awd62-frame">'`）＋刪 `'<div class="awd62-aud149 bot"></div>'` 一截；
   `.awd62-canvaswrap`＋M5 GIF 兩張 img 原封不動。
4. JS 註解重寫：刪「舞台上下加觀眾席帶」一句，backing 636×360＋M5 疊加描述留返。
5. 驗收：全檔 grep `aud149`、`awd62-aud`（index.html／qa149／tests）**零命中**。
   （註：通告文案入面「觀眾席」等字眼係舊內容，唔關典禮帶事，唔郁。）

### 保留（全部唔郁，測試＋實駕覆驗）
- 其餘 B1：canvas backing 636×360、M5 彩紙 GIF（`assets/fx/awd_confetti_m5.gif`，
  13,889 bytes）、彩紙 46→90 粒、跳過掣移位（top:8px;right:8px）。
- B2：報紙＋結果卡寫明得主＋作品——`awardWinner149(pack)` helper，winner＝
  `winner63 || fellows63[0]`，動態讀，冇寫死；null 跌返舊文案；gallery headline 重寫＋press stub 重寫。
- B3：comfort beat 紫 panel 放海報圖＋winner 卡 🏆 角標。
- B4：700 報紙 modal 底加 padding 76px（`@media (max-height:800px)`，932 唔郁）。

### 測試檔相應改動
- `qa149/test_awards149.js`：B1 舞台斷言改為**反向斷言**（stage 還原橫向置中 flex、
  frame 冇 `flex:none`、檔內零觀眾帶）。反向斷言嘅被禁字串用拆字串寫
  （`'awd62-' + 'aud'`／`'aud' + '149'`），唔好令測試檔本身出現全名，否則 grep 零命中驗收會誤報。
- `qa149/drive149.py`＋`qa149/check_stage_state.js`：`auds` 探針改為
  `[class*="aud"]` 計數（`audClassCount`，應為 0）＋加 `stageBg`（F1 底色證據）；
  gallery case 嘅 `b1_aud_bands_present`／`b1_frame_fills_viewport`／
  `b1_bands_fill_former_black` 三個檢查改為 `b1_no_aud_bands`＋
  `b1_frame_vertically_centred`，另加 `f1` 記錄（frame 上下 gap＋底色）。
- `tests/test_text125_static.py`／`tests/test_travel114_static.py`：行號 resync
  （`qa149/resync149.py` 對位，MISMATCH 0）：CSS 錨點 ＋27→**＋13**，JS 錨點 ＋86→**＋84**，
  全檔淨 ＋97（pristine 58,905 行 → 工作版 59,002 行）。
  text125：currentLine 27813／advance 27926／familySafe 33529–33531。
  travel114：DEF 53659、WRAPPER 44184；COUNT 13／FREE 27 不變。

## §1 測試數字

- 主 script `node --check`（抽 inline script 兩段）：PASS。
- `qa149/test_awards149.js`（工作版）：**36 PASS／0 FAIL**。
- `qa149/test_awards149.js`（pristine `qa149/pristine_index.html`，反證）：2 PASS／34 FAIL——
  34 項全部係 v149 新檢查（B1–B4＋helper＋紀律 M5 引用），乾淨 FAIL 唔 crash。
  註：反向 B1 舞台斷言喺 pristine 係 PASS——pristine 本來就冇觀眾帶，呢項唔係判別證據；
  判別證據係負控制：將觀眾帶插返入臨時副本（`/tmp/idx_with_band.html`，stage 改返
  `flex-direction:column`＋加返 `.awd62-aud149` 規則），跑出 **35 PASS／1 FAIL**，
  唯一 FAIL 就係反向 B1 斷言——證明反向斷言識得捉返條帶。
- `tests/test_text125_static.py`：PASS（RESULT PASS）。
- `tests/test_travel114_static.py`：PASS（RESULT PASS，免費 27＋計數 13＋定義／wrapper／測試區 4）。
- `tests/test_kwan151_static.py`／`tests/test_tang152_static.py`：**呢條分支冇呢兩個檔**
  （v151／v152 先加入，分支基底 `da90957` 早過佢哋；常駐 clone main 有）。
  佢哋唔係本票回歸範圍；rebase 上 main 嗰陣要由統籌處理（見 §4）。
- 全套 A/B（`qa149/run_suite.sh`，pristine worktree `~/workspace/linji-pristine149`＠`da90957`
  對工作版；新輸出 `qa149/suite_baseline149_r2.txt`／`qa149/suite_work149_r2.txt`，
  舊 `suite_baseline149.txt`（211／12）／`suite_work149.txt`（210／12）留返做對照）：
  **pristine 210 PASS／12 FAIL vs 工作版 210 PASS／12 FAIL，FAIL 清單逐項相同，零回歸。**
  12 項 FAIL（兩邊一致）：test_flash51／test_giglib36／test_pacing35／test_poster59／
  test_rumor49／test_slot50／test_soft_tip_111_restore／test_start53／test_weave43／
  test_weave44／test_weave49／test_wrap38（全部 `_static.py`，已知 pre-existing）。
  註：舊基線 211 係 suite 數字波動（同一 repo 連續跑唔同總數）；今次兩邊同一次跑都係 210，
  以逐項對照為準，唔以總數論。

## §2 實駕結果

`qa149/drive149.py all`（本地鏡像＋Playwright；venv `/home/hatch/pwenv49/bin/python`；
port 8983；`?softPreview=1`；ENC79 巧遇播完先開地點板）：**4/7 PASS，0 pageerror，
0 failed request**（全部 7 個 case `pageerrors: []`）。結果檔 `qa149/drive149.json`
（另存 `qa149/drive149_r2.json` 同一份）；截圖 55 張喺 `qa149/shots/`
（另存 `qa149/shots_r2_postremoval/` 同一份）。

- PASS：gallery_932、nominated_932、nominated_700、declined_932——全部檢查 true，
  包括 B1（`b1_no_aud_bands`／`b1_frame_vertically_centred`／backing 636×360／
  M5 彩紙 reveal 可見／跳過掣框內）、B2（報紙 headline＋dek 寫明得主＋作品、
  結果卡 🏆 標記＋metricLine 實內容）、B3（卡片 win 角標、comfort beat 約 2600ms）、
  B4（932 尾句第一眼可見）。
- FAIL（3 個，全部唔係剔走觀眾帶造成——見下面對照）：
  1. gallery_700：唯一 FAIL `b4_tail_first_view`（700 報紙尾句第一眼俾掣遮住：
     尾句「…研究下期。」bottom 657 vs 掣頂 599）。
  2. declined_700：唯一 FAIL `b4_tail_first_view`（同一尾句，bottom 603 vs 掣頂 599）。
  3. gallery_tv_932：唯一 FAIL `b2_tv_paper_names_its_winner`——但晨報本身正確：
     次日報紙 h3 係「星河台慶夜 葉敏芝憑《渡輪燈火》奪獎」，得主＋作品齊；
     fail 原因係 drive 檢查讀 `paper_for_ceremony()`（advance 剪報之後），
     嗰個 helper 對已剪報項目合成空 headline／dek 條目（drive149.py L412–413），
     gal[0] 係空條目所以檢查讀唔到得主。係 drive 腳本次序問題，唔係遊戲／B2 問題。

### 剔走前對照（決定性）
起對照樹 `~/workspace/linji-work149-pre`（已刪）：同一份 v149 code，淨係插返觀眾帶
（stage `flex-direction:column`＋兩條 `.awd62-aud149` 規則＋innerHTML 兩截），
用同一份新檢查重跑三個 fail case（DRIVE149_PORT=8985）：
- gallery_tv_932（剔走前）：FAIL，唯一 FAIL 同樣係 `b2_tv_paper_names_its_winner`——同剔走後逐項相同。
- gallery_700（剔走前）：FAIL，`b1_no_aud_bands`（對照樹有帶，預期內）＋`b4_tail_first_view`——B4 同剔走後相同。
- declined_700（剔走前）：FAIL，唯一 FAIL 同樣係 `b4_tail_first_view`。
**結論：剔走觀眾帶冇令任何實駕檢查由 PASS 變 FAIL。**三個 fail 全部喺剔走前已經存在：
B4 係 700 報紙尾句第一眼位置問題（同一個 seed、同一條尾句，連 pristine probe
`qa149/drive149_pristine_probe.json` 嘅 gallery_700 都係 `b4_tail_first_view: false`，
尾句 bottom 625 vs 掣頂 599；B4 padding 係喺底加，scrollTop 0 嗰陣唔會郁到尾句位置，
所以檢查結果同有冇 padding 無關）；TV B2 係 drive 讀剪報空條目問題。
兩樣都唔喺本票範圍（本票只剔走觀眾帶），留返畀統籌決定開唔開票跟進。
另外第一次 `drive149.py all` 曾經 2.4 秒 exit 120、log 空白——原因係舊 http.server
佔住 port 8983（上一次 run 遺低，pid 59570），kill 咗再跑即正常；唔係 code 問題。

## §3 F1 判斷

**判斷：接受現狀落 v149。** 理由：
- 數字（reveal probe，DOM 量度為主）：932 frame top 304／bottom 628，上下 gap 各 **304px**
  （佔 viewport 約 65%）；700 frame top 188／bottom 512，上下 gap 各 **188px**（約 54%）。
  底色實測 `stageBg: rgb(20, 16, 31)`＝**#14101f**，上下對稱、置中（`b1_frame_vertically_centred` true）。
- 截圖（`qa149/shots/gallery_430x932_beat_reveal.png`／`gallery_430x700_beat_reveal.png`）：
  舞台本身完整置中——紅幕布＋射燈＋彩紙＋三個人物＋獎盃＋字幕＋「跳過」掣齊；
  上下空帶係均勻深紫黑，平坦、無雜訊、無裁切感，視覺上似 letterbox，唔似壞咗／漏嘢。
- 呢個就係用戶方向 1 要嘅樣（典禮只需要舞台，唔要台下部分）；空帶係嗰個方向直接造出嚟嘅，唔係意外。
- 但要講明 trade-off：空帶幾何返到 **v147 B1 嗰個狀態**（當時 review 話「舞台細、上下大片黑帶，
  成個畫面近三分之二係黑」；今次 932 上下各 304px 同當年數字基本一致），分別只係而家係
  平坦 #14101f 唔係純黑。v149 嘅觀眾帶本來就係為咗填呢個空帶而加，剔走佢等於將 v147 B1
  嘅「空帶」部分還原——係用戶拍板方向嘅代價，唔係本票漏咗嘢。
- **v170 唔會自動救返**：v170 嘅新舞台-only 底圖只會填 canvas 入面（frame 內），frame 外
  上下兩截 #14101f 空帶照舊存在。想填外圍要另外決定（例如放大 frame／canvas、
  或者加會場暗景做底），唔喺 v149／v170 現有範圍。建議：接受現狀落 v149，空帶問題
  等 v170 落地、成個典禮視覺換完之後再睇整體先決定，唔好而家為咗空帶再加嘢。

## §4 rebase 提示（留畀統籌）

- 基底 `da90957`（v146 NOTES）；main 而家 `56141a3`（v169 已落地，另有 v171 進行中）。
  落地嗰陣要 rebase（本票冇做）。
- Resync 錨點（相對基底 `da90957`）：CSS **＋13**（唔係舊 v149 數 ＋27）、JS **＋84**
  （唔係 ＋86），全檔淨 **＋97**。text125／travel114 已按呢個數 resync 咗（見 §0）。
- `test_kwan151_static.py`／`test_tang152_static.py`（＋kwan151_textfix.js／tang164／tang167／
  tang169 等）喺 main 先有，呢條分支冇；rebase 嗰陣佢哋 pin 嘅 index.html 行號會受
  CSS −14／JS 後 −16 漂移影響，要逐個重對（尤其係佢哋 pin 喺 761 行 CSS 段之後／46231 行
  JS 段之後嘅錨點）。v149 嘅 `qa149/resync149.py` 只對 text125／travel114 嘅釘行，
  唔包 kwan／tang。
- 剔走觀眾帶同 v170 Phase 2（新舞台-only 底圖）零直接衝突：本票只刪 CSS 兩條規則＋
  innerHTML 兩截，冇郁 FLOOR／slotCx／底圖／`.awd62-canvaswrap`／M5；v170 落地嗰陣
  換底圖＋重定 FLOOR 唔使理本票。但留意：v170 嘅新底圖會填滿 frame，F1 嘅空帶判斷
  到時要重驗（見 §3）。
- 落地前核對：`git log` 應見本票一個 commit（剔走觀眾帶）；`git status` 乾淨；
  線上核實照舊流程（curl bytes＋sha）。
- 環境備註：今次寫入全程正常，零 EPERM；Chromium 實駕期間冇死過。第一次 `drive149.py all`
  曾經 2.4 秒 exit 120、log 空白——原因係舊 http.server 佔住 port 8983（上一次 run 遺低，
  pid 59570），kill 咗再跑即正常；唔係 code 問題，重跑嗰陣先檢查 port。
- 對照樹 `~/workspace/linji-work149-pre`（插返觀眾帶重跑三個 fail case）已經
  `git worktree remove` 刪咗；對照結果寫咗喺 §2，方法可重做（§2 有齊步驟）。

## §5 rebase 紀錄（統籌做，兩輪；§4 嘅基底資料已由本節取代）

### 第一輪：上 main 29d4821（v171）
- 基底 `da90957` → `6d08c7c`（v171 遊戲 commit），rebase 停咗，3 檔衝突：index.html 5 個
  hunk、text125 1 個、travel114 1 個。解決：H1 CSS 保留 v149 B3＋main v166 glamour 規則；
  H2 stage.innerHTML 636×360 canvas＋兩張 M5 GIF＋`glamHtml` 搬入 frame（比例 636/360＝424/240
  一致）；H3 `walkEl`＋`syncConfetti149` 兩樣保留；H5 `syncWalkup`＋`syncConfetti149` 兩樣
  保留；H4 reveal 融合成一行，同時滿足 awards149 逐字檢查（`if(beats[beatIdx].id ===
  "reveal") spawnConfetti();`）＋M9 同行斷言（audio 只限 won）。
- Resync（`qa149/resync_rebase149.py`＋`part2`＋`fixup`＋`fixup2`，difflib 對位，MISMATCH 0）：
  淨 **＋97** 行（CSS ＋13／JS ＋84）。fixup／fixup2 係 reveal 行先拆兩行（＋98）再融返
  一行（＋97）嘅來回修正。text125：currentLine 27639→27652、advance 27752→27765、
  familySafe 33445→33458。travel114：DEF 53690→53787、WRAPPER 44172→44185；40 個釘行
  （awards JS 區域之前 ＋13、之後 ＋97）。kwan151：13 個錨點一律 ＋13。tang152：3 個錨點
  一律 ＋13。tang171：總行數 59171→59268、DEF 53690→53787。
- M1／M9 衝突：`test_awards160_m1_static.py` 斷言 canvas 424×240——v149 B1 刻意改 636×360
  （已拍板規格），更新斷言跟 636×360＋加 v149 頭註；M9 靠融合 reveal 行滿足，唔使改測試。
- 其後 main 由 `6d08c7c` 郁到 `29d4821`（只係 v171 NOTES commit，index.html 0 diff），
  `git rebase origin/main` 乾淨成功，分支 commit `067592d`。

### 第二輪：上 main e8c3a73（v170 落地）
- v170（遊戲 commit `59fdf54`）：舞台-only 底圖（換 `assets/story/awards/bg_awards_ballroom.jpg`）
  ＋FLOOR 194→193＋fallback 舞台幾何（H-52→H-47）；index.html 淨 **＋2** 行（fallback 註解＋
  幾何，插入點 main L46098；FLOOR 原地改）。v170 亦 resync 咗 travel114／tang171／M1／
  chibi64＋新增 test_awards170_static。
- Commit 1（`067592d`）rebase：index.html 自動合併（v170 嘅 FLOOR／fallback 同 v149 嘅
  hunks 唔重疊）；travel114／tang171 衝突——用 `/tmp/resolve_rebase170.py`（已存
  `qa149/resync_rebase149_v170.py`）解決：v170 淨 ＋2 喺 main L46098（＝v149 數 46116），
  v149 釘行 ≥46116 者 ＋2、以下者唔郁；DEF 53788→53790、總行數 59269→59271。驗證：
  `wc -l` 59271、`grep openLoc DEF` 53790。
- Commit 2（`17637f4`）rebase：index.html＋M1 自動合併（reveal 融合行照入）；travel114／
  tang171 再衝突——用 `/tmp/resolve_rebase170_fixup3.py`（已存
  `qa149/resync_rebase149_v170_fixup3.py`）解決：reveal 融合行 −1（插入點 L46602），
  ＞46602 釘行 −1；DEF 53790→53789、總行數 59271→59270。驗證：`wc -l` 59270、
  `grep openLoc DEF` 53789、融合 reveal 行喺 46602。
- **教訓（resolver bug，已修好）**：第一輪 resolver 嘅 `t114_free` 用 `theirs[:27]` 切 FREE 區，
  誤將 27 行全數當數字行——實際 v149 嗰邊只有 23 行數字＋4 行關閉（`}`＋FREE_FLAGS＋DEF＋
  WRAPPER），結果複製多咗 4 行，令 travel114 喺中間 commit `4866b26` 出現 DEF_LINE 重複＋
  stray `}`（syntax error）。已喺 fixup3 嗰陣刪走重複 4 行，`py_compile` 通過；最終樹
  travel114／tang171 全部 PASS。`4866b26` 本身保留咗呢個瑕疵（中間 commit，squash merge
  唔入 main），記喺度等後人唔好重蹈：resync 腳本切 conflict 區嗰陣，要按行內容分
  （數字行 vs 關閉行），唔好靠死數目切片。
- v170 相容：FLOOR＝193 保留（v149 冇郁 FLOOR）；新底圖 asset 保留；`test_awards170_static`
  ALL PASS；M1 自動合併後 ALL PASS（636×360 backing＋v170 底圖並存）。
- 最終淨數：index.html **59270 行**（v170 59173＋v149 ＋97）；CSS ＋13／JS ＋84（相對 v170
  基底）。分支 HEAD `230f0e9`（兩 commit：`4866b26`＋`230f0e9`），工作樹乾淨。

## §6 最終驗證（基底 e8c3a73／v170，分支 `230f0e9`）

- `node --check`（抽兩段 inline script）：PASS。
- `qa149/test_awards149.js`：**36/36**。text125 PASS；travel114 PASS；kwan151 ALL PASS；
  tang152 ALL PASS；tang171 **22/22**；M1 ALL PASS；M9 ALL PASS；awards170 ALL PASS。
- 全套 A/B：pristine `e8c3a73` **231/12** vs 工作版 **231/12**，FAIL 清單逐項相同
  （12 項已知 pre-existing .py：flash51、giglib36、pacing35、poster59、rumor49、slot50、
  soft_tip_111_restore、start53、weave43、weave44、weave49、wrap38），**零回歸**。
  套件：`qa149/suite_baseline149_v170.txt`、`qa149/suite_work149_v170.txt`。
- 實駕 `qa149/drive149.py all`：**3/7 PASS，0 pageerror**（55 張截圖，`qa149/drive149.json`）。
  PASS：gallery_932、nominated_932、nominated_700。FAIL（全部已知／已證實唔係 v149 回歸）：
  - gallery_700：唯一 FAIL `b4_tail_first_view`——pristine probe 已證實 main 都有
    （B4 padding 只能令碌到底嗰陣尾句清出掣，第一眼檢查比規格嚴格）。
  - gallery_tv_932：唯一 FAIL `b2_tv_paper_names_its_winner`——drive 腳本次序問題（advance
    剪報後讀合成空 headline 條目），晨報本身正確「星河台慶夜 葉敏芝憑《渡輪燈火》奪獎」。
  - declined_932／700：各 3 FAIL（`flag_skipped`＋`paper_queued_next_day`＋
    `b4_tail_first_view`）——pristine main `e8c3a73` 對照（declined_932 實測，port 8985）
    同樣 3 fail，連 `after_decline`／`next_day` 狀態都一樣，證實係 main 已有行為
    （v165 推辭播電視直播版典禮：flag 留 "invited"→播完變 "done"，報紙遲一日先入 queue；
    drive 腳本期望舊 "skipped" 語義，要跟進更新，唔喺 v149 範圍）。附帶：v149 B2 令
    declined 報紙由 generic headline 變成「廖炳星憑《離岸的信》奪獎」，
    `b2_declined_paper_names_winner` 喺工作版 PASS、pristine FAIL——v149 改善咗 declined case。
- F1（v170 之後重驗）：gallery_932 frameTop／botGap 各 **304px**、stageBg `rgb(20, 16, 31)`；
  gallery_700 各 **188px**——同 v170 之前數字完全一致；v170 新底圖只填 canvas，frame 外
  空帶唔變。判斷不變：接受現狀（用戶方向 1 嘅代價），等 v170 落地後再睇整體。
- 殘留（唔阻塞落地）：700 B4 第一眼、TV B2 drive 讀空條目、declined drive 腳本要跟 v165
  流程更新——三項留返畀 v149 設計 review 評判／開跟進票。
