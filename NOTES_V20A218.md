# NOTES_V20A218 — v218 Review 修復票（2026-11-15）

分支 `v20a218`，基底 main `e54d9a1`（遊戲 v217）。用戶逐題問完，全部揀「一次過修晒」
（決定記錄 `~/workspace/linji-story-coherence/DECISIONS-2026-11-15.md`「Review 組等拍板」一節）。
出貨：checkout main → `git merge --squash v20a218` → commit → push main（經 deploy key，唔開 PR）。
唔改 SAVE key（`starVolunteer_map_v19w`）、softRev（`s107`）、產品 `?v=`（`v20a10`）。

## §1 批次 A — v217 NOTES §4 遊戲側殘留（5 項，全部完成）

- **A1**：story_detail 3 句 synopsis 顯示 1993——實證顯示係 1992，synopsis 唔使改；
  真正漏 1993 嘅係 `when` 欄，加 6 條 TEXTFIX55_EXACT when 條目＋C15 synopsis 1 條
  （「1991年春，藍家在宴會側廳…問阿偉站哪邊」→「1990年春…問阿偉企邊」）。
  註：TEXTFIX55_EXACT 行先、walk 後行，EXACT value 要寫「顯示年份 −2」。
- **A2**：F4 閘 `F4_stay_mind` season 夏→秋（場面已定 1990 秋，閘跟場面）。
- **A3**：gift_react「怎麼」×8 成句轉廣東話（`content/gift_react_copy.json`，16 行）。
- **A5**：PHASE1 locale `zh-Hant-written`→`zh-Hant-HK`，4 處
  （`content/story_beats_phase1.json`、`content/tutorial_zh_HK.json` 各 1 行＋index.html 2 處）。
- **A6**：D6 對齊 0 改動確認（NOTES 話嘅「113」對唔上任何自然計法，以後唔好再引 113）。
- 第 4 項（NPC 仲叫 Vera）歸 v159，唔喺呢票；第 7 項已修好。

## §2 批次 B — 報紙（v214＋v216，11 項，全部完成）

- **B1**（v214 B1＝v216 B1，同一句一次過清）：聲望行搬出 `.paper-sheet`＋刪 `paper-note`
  「傳聞」句，連兩條 CSS。
- **B3**：stub headline「揭入圍」→「揭曉入圍」（`content/STUB_NEWSPAPER_MORNING_SOFT_v1.json`）。
- **B4**：晨報頭圖＋第二版短訊相加圖說，用現成 `.np214-caption`。
- **C1**：kickDup 比較前剝欄目前綴。
- **C2**：版名按媒介釘死（film 娛樂快報／tv 電視週刊／music 樂壇速遞／ad 消費情報／any 星河娛樂版）。
- **C3**：摺行 dek 列出被摺各則標題。
- **C1b**：第二版填充字按短訊數縮（≤1 則→1 段、2 則→2 段、≥3 則→0 段）。
- **C3b**：短正文單欄 inline style。
- **C4b**：第二版得一則補多一則花邊。
- **B3c**：典禮翌日晨報獎訊做頭條，權重 3。
- **C3c**：推辭版 dek 加電視直播。
- 驗證：Node `/tmp/np218test.cjs` 18/18 PASS＋7 個相關靜態測試 PASS。
- **C2x**（v216 C2，700 矮屏版尾）未 close，要 700px 實駕量度。

## §3 批次 C — 頒獎禮（v213＋v212＋v197 B3，11 項，全部完成）

- **v213 B1**：請柬加預約說明行＋出席 toast＋共用 helper `awards213MapCue213()`＋
  地圖／屋企／日結三處顯示。**B2**：同 helper＋三處顯示。
- **v213 C1**：金碟夜「年終」→「年中」。**C4**：comfort 只喺最後一個入圍格出一次。
- **v213 B4**：唔使改 code（結構核實通過，像素驗收留待 390 實駕）。
- **v212 B1**：`awards208NightCats` 加作品層去重 `usedTitle212`。
- **v212 C1**：`SUSPENSE212` 加第四句「邊個攞走呢個獎……」（4 格晚第 4 格唔再重複第 1 句）。
- **v212 C2＋v197 B3**：`.awd62-stage` `align-items:safe center`→`flex-start`；
  v197 B3 剩低跳幅要 live 重測。
- **v212 C3**：光柱頂加暖加濃＋白牌收窄 60%→52%。
- **v212 C4**：walkup 改行後排，y:-24（先畫，提名人遮住佢；到埗先行返前排換燕尾服捧杯）。
- 驗證：Node `/tmp/c218test.cjs` 15/15 PASS＋9 個相關靜態測試 PASS。

## §4 批次 D — 其他 code

### D-v206（6 項，全部完成）
- **B2**：set32→街市圖、set33→`bg_loc_ad_central.jpg`頂住；覆寫表 48→50 行。
- **B3**：`scenePos146` 加 film_harbour `center 15%`。
- **C2**：set48 睇山景 fx `popularity:1`→`stress:-1`。
- **C3**：set32 旁白刪汽水句。
- **C4**：全池 beat-echo 掃描，14 處 NPC 句重寫；set44「聽晚直播」→「陣間直播」順手修埋。
- **C5**：`NOTES_V20A206.md` 保底 pick 寫法修正。
- 驗證：echo 重掃 0 命中；WF4 相關測試全部 PASS。

### D-v205（5 項完成，1 項等拍板）
- **B1**：`dlg106ExprFor` 加 speakerId 參數——neutral＋`lan_ruoxi` 回 "smile"，限藍若曦一人。
- **B2**：`spDlgPairIds` 喺 D-1 block 之後加一節——單人＋`pcSilent:true`＋cast 有「阿偉」嗰陣
  `pair.unshift("awi")`；R_lan 五節全部 `pcSilent:true`。
- **C1**：抉擇分支加 `choiceCur218`＋`spDlgCharsHtml(choiceCur218, "narration")`，兩人齊暗 0.6；
  抉擇舞台係 96–150px 高 strip，人物約 60% 舞台高，唔遮掣。
- **C2**：R_lan crisis beat 1 加 `emotion:"think"`、push2 beat 1 加 `emotion:"serious"`。
- **C3**：`dlg106Classify` 加 guard——shy 關鍵詞「唔好意思」喺句入面有「押後／超時／重排」嗰陣唔計。
- **C4**（白襪＋波鞋永遠見唔到）唔做，等用戶拍板（接受現狀定人情頁／圖鑑補全身展示位）。
- 驗證：`test_dlg106_logic.js` PASS；`/tmp/d205test.cjs` 9/9 PASS；相關靜態測試全部 PASS。

### D-v189／v213 C5 — 日結板綠線＋支票第一屏見唔到（完成）
- 92dvh 媒體規則由 v197 B4 嗰條 78dvh 之前搬去之後；支票縮細到 70% 闊＋六個 span 字號
  按比例縮 0.7 倍（只限日結板，簽約嗰張維持全闊）；fx102 片縮細
  （video max-width 280→200px、max-height `min(28dvh,170px)`）；
  綠線由 `notes.push` 改 `notes.splice(wrapNoteIdx105, 0,...)`（插喺支票插入位之前）。
- 驗證：結構檢查全部 True；`test_dayend189_static`（加咗 5 項新斷言）ALL PASS＋相關測試全部 PASS。
  最終像素驗收（932／700）要 live 實駕重測。

### D-v189 C1／v197 C1／v197 C5／v173 C1（完成）
- **v189 C1**：`confirmWeekAccel` 開確認 modal 之前加 `mask.classList.remove("day-res")`
  （700 嗰陣確認 modal max-height 由 644px 變返一般 modal 嘅 546px）。
- **v197 C1**：`margin-bottom:-1.5px` 由 `.home-tab.on` 搬去 base `.home-tab` rule（五格統一）。
- **v197 C5**：`.story-play.sp-choices-layout.sp-choice` min-height 44→64px。
- **v173 C1**：鎖住態 rule 加 `color:#3a2e22!important;`（混合後 4.63:1，達 4.5 門檻）。

### D-v165（完成兩項，一項已核實唔使做）
- **C1**：核實已修好，唔使做（舊句「先播到呢幕」／「到星河電視台播」全檔 0 命中；
  `renderProgressPane71` 已改由 `prog71GateItems()` 起逐項條件）。
- **第三條返地圖路 bypass**：`leaveHomeFromNotebook` map 分支加 `story165TryForcedPlay()` 掛點
  （跟 `#loc-close` 同一寫法：用戶已經喺地圖上面、無 modal 開緊先播；`story165ModalOpen` 閘＋
  try/catch `_s165d`；播唔到就照原樣留喺地圖；start-today 分支唔掛；`kickScheduleIfNeeded()`
  截走嗰陣唔掛）。`test_story165_static` ALL PASS。
  可達性（`#home-back-map` 只喺強制日／soft 日先顯示，自由日 `display:none`）留待 live 驗。
- **v197 N1** 唔做（要 live 實駕）：同步邏輯存在（`resetBtn.disabled =!editable`），但撳落去嘅
  防呆依然係靜默 return，零 toast、零反饋；stale window 係咪仲出現取決於 render 時序，靜態判唔到。

## §5 批次 E — 圖

### E-v209 藍若曦 6 張全身圖重焗（完成）
- 腳本 `qa218_bake209.py`（新檔）；原檔備份喺 `~/workspace/linji-work218-bake209-backup/`。
- 機制（v195 口徑）：光邊 CREAM (243,233,210)，闊 r=17；身體＝最大連通 component
  （其餘細 component 全部丟棄）→ 人物縮細 2%（0.98，LANCZOS）→ 置中＋按 bbox 幾何中心平移
  （think dx -30，其餘 dx -14／-15，dy 0；唔可以用像素平均做中心——人物上半身實、下半身疏，
  平均會偏上 ~180px）→ 貼返原尺寸畫布（尺寸不變）→ 重焗光邊（身體膨脹 r=17 減身體，填 CREAM；
  alpha 成層 gaussian σ0.8 羽化；透明區 RGB 填 CREAM 防重採樣洩黑邊）→ WebP q92。
- 覆驗：腳本自帶 verify ALL PASS（6/6）；`tests/test_lan209_outline_static.py` FAILURES: 0。
- 驗證口徑：唔可以用「非米白」計 body component 數——WebP 壓縮令羽化邊緣像素 RGB 偏離
  CREAM >12，碎成幾百個 1–2px 假 component；正確口徑係不透明 component 數。

### E-v206 B1 三張新場景圖（完成）
- 問題：day07／day19／day22／st17 仲係 `bg_wf4_market.jpg`，v218 D 令 set32 都用埋街市圖，
  變成一圖五用。
- 參照相（image-search 搵到，已下載存 `~/workspace/linji-work-news-refs/` 做 DEV 留檔）：
  地鐵站 `ref_mtr_mongkok_night.jpg`（Wikimedia 旺角東站月台夜晚；右下角有 2023.1.11
  時間戳，生成嗰陣唔抄）、公園太極 `ref_park_taichi.jpg`（SCMP 公園太極班＋高廈背景）、
  電車 `ref_tram_upper.jpg`（theodysseyonline 電車上層）。
- 成品（`assets/story/locs/`，全部 720×1280，JPG q90）：
  `bg_wf4_mtr.jpg`（旺角地鐵站夜晚，賣唱後生＋結他＋開咗嘅結他盒有散銀＋紅線列車＋綠磚柱＋
  黃安全線；原圖 1120×2240，裁走頂部 249px 天花板→1120×1991→resize 720×1280）、
  `bg_wf4_park.jpg`（屋邨公園朝早太極班＋磚地廣場＋木櫈＋石牆＋高廈背景）、
  `bg_wf4_tram.jpg`（港島電車上層朝早，由後望前，木長櫈＋鉻扶手杆＋窗外街景＋幾個乘客背影）。
  三張全部目視合格（無可讀文字、內容啱）。
- 接入：`WF4_SCENE_OVERRIDE134` 換三行值（`?v=20a218`），st17 留街市圖頂住；
  表頭註解加 v218 D-B1 行（街市圖淨返 13 個用家：st06／st07／st11／day03／day04／day06／
  day12／st12／st17／day18／day23／day25／set32，已用程式核實）。覆寫表維持 50 行。
- 測試同步：`tests/test_ui134_wf4scene_static.py`（存在清單加 3 檔＋v218 新圖 loop）同
  `tests/test_wf4_203_static.py`（day07 由 v203 loop 移出、day19／day22 由 v206 loop 移出，
  加 v218 loop＋檔案存在檢查）。驗證：兩檔 TOTAL PASS、`test_wf4_193_static.py` TOTAL PASS、
  `test_mask146_static.py` ALL PASS。

## §6 P0 語法錯誤——發現同修復（本版最大發現）

- 批次 C v213 B1 加嗰行 `renderAwardInviteHtml` 預約說明行漏咗 `${...}` 插值嘅收尾 `}`——
  寫成 `})() /* v20a218 C-B1：... */`，應該係 `})()} /*... */`。
- `node --check` 抽出全部 `<script>` 驗證，證實**成個遊戲 JS 唔過 syntax**
  （`SyntaxError: Missing } in template expression`）。上一輪批次 C 只做咗 substring 檢查
  （`/tmp/c218test.cjs` 15/15），冇 eval／syntax check，所以走漏咗。
- **已修**：補返個 `}`；`node --check` 變 SYNTAX OK；`test_awards213_logic.js` ALL PASS。
  呢個錯誤如果落地，遊戲完全 load 唔到。
- 教訓：以後凡係改 JS 嘅批次，驗收一定要加 `node --check` 全檔 syntax 檢查，唔可以只靠 substring 斷言。

## §7 Suite A/B 跟進——22 項額外失敗（全部修好）

- 首次 A/B：A（pristine main `e54d9a1`）309／13（＝v217 基線）；B（工作副本）287／35。
  A 嘅 13 項全部都喺 B 入面；B 多出 22 項，逐個直接跑全部都真係 FAIL，唔係 suite 波動。
- 語法修復順帶修好 4 項：`test_awards192_logic.js`、`test_awards200_logic.js`、
  `test_awards213_logic.js`、`test_terms57_static.py`。
- 其餘 18 項全部係 v218 有意改動、舊測試釘死舊行為——按類更新測試，全部逐個覆驗 PASS：
  - **walkup y:-24**（4 檔）：`test_awards187_logic.js`、`test_awards187_static.py`、
    `test_awards190_logic.js`、`test_awards190_static.py`——舊測試釘死 `y: 6`，改做 `y: -24`
    （只出現一次，行緊嗰支；到埗嗰句無 y）。
  - **awards212 B1**：`test_awards212_logic.js`——期望改做 4 格各唔相同（Set size 4）。
  - **newspaper216 R3d**：`test_newspaper216_logic.js`——1 則→1 段，補 2 則→2 段、3 則→0 段覆蓋。
  - **wf4_203_logic**：day07→`bg_wf4_tram.jpg`、day19→`bg_wf4_park.jpg`、day22→`bg_wf4_mtr.jpg`。
  - **weave47_logic**：F4 閘夏→秋（1992 年 10 月 15 日先開）。
  - **story172_static**：斷言改做要求第三條路掛點＋modal 閘在位（v218 D-v165 已加掛點）。
  - **weave46_static**：TEXTFIX55_EXACT 巨行加 v20a218 申報＋`tfix_block` 豁免
    （呢行係正規化表鍵值，唔係歌手向內容）。
  - **kwan151_static**：13 個 `line()` 錨點 difflib 映射（25956／26297／26300／26301／26302／
    26345／26564 唔郁；27557→27565、27590→27598；31384→31417、31385→31418、31427→31460；
    31376→31408，例外：A1 拆開 TEXTFIX55_EXACT 巨行加 when 條目）。
  - **text125_static**：三個 fallback 釘行 difflib 映射（currentLine 28082→28090、
    advance 28211→28227、applyFamilySafe 33930→33963）。
  - **rom176_static**：6 個錨點（6360 唔郁；31941→31974、55660→55780、56028→56148、
    57167→57287、57261→57381）。
  - **tang152_static**：3 個錨點（26116 唔郁；31866→31899、32012→32045）。
  - **travel114_static**：47 個錨點（COUNT 12／FREE 33 不變；DEF 57230→57350、WRAPPER 45430→45479）。
  - **content JSON 豁免**（3 檔）：`test_aud91fix122_static.py`、`test_aud91fix124_static.py`、
    `test_gigreq110_static.py`——加 `_v218_allowed`（4 檔：STUB_NEWSPAPER_MORNING_SOFT_v1.json、
    tutorial_zh_HK.json、gift_react_copy.json、story_beats_phase1.json；後兩檔已喺 v217 集）。
- 全檔 resync：舊 62,758 行→新 62,894 行，淨 **+136**（插入 235、刪除 99）；
  openLoc DEF 舊 57230→新 57350，位移 **+120**；DEF 之前各 hunk 淨加總和 +120，DEF 之後淨加 +16，
  120+16=136。腳本 `qa218/resync218.py`＋`qa218/resync218_map.json`、
  `qa218/resync218_pins.py`（三檔釘行映射）。
- 附帶修：`test_tang171_static.py` C2 斷言（v173-C1 加咗 `color:#3a2e22!important;` 入 `.h` rule，
  舊字串唔再匹配）＋`test_taxi148_static.py` B1 斷言（v206 B3 加咗 film_harbour `center 15%`
  分支落 `scenePos146` ternary 尾）。

## §8 驗證

- **最終全套 suite A/B（2026-11-15）**：A（pristine）**309／13**，B（工作副本）**309／13**，
  FAIL 清單一模一樣（13 項穩定 pre-existing FAIL：flash51、giglib36、pacing35、poster59、
  rumor49、slot50、soft_tip_111_restore、start53、weave43、weave44、weave49、wf5_87、wrap38），
  **零回歸**。輸出 `/tmp/suite218_A2.txt`、`/tmp/suite218_B2.txt`（ephemeral）。
- **語法**：`node --check` 全檔 script SYNTAX OK（§6 修復後）。
- **相關測試逐個直接覆驗**：§2–§5 嗰啲全部 PASS（見各節）。
- **落地核實**：（待填：線上 bytes／sha、遊戲版本 hash）

## §9 殘留（需 live 實駕先判到／等拍板）

- v213 B4 像素驗收、v213 C5、v197 N1、v165 第三條路可達性、v216 C2（700px）、
  v197 B3 剩低跳幅（flex-start 之後要重測係咪真係唔跳）、v212 C2 px、
  v189 B1 像素重測（932／700，殺青 wrap 板實測綠線＋支票第一屏可見幾多 px）、
  v206 B1 保底 pending 下一朝彈出一步。
- v205 C4 白襪＋波鞋（等用戶拍板：接受現狀定人情頁／圖鑑補全身展示位）。
- v206 C1 day24 信件裁切調位（v218 未做：day24 已喺 v206 C2 改配電視台辦公室圖，v218 無再郁裁切；如要調位另開票）。
- 新發現跟進（唔喺 v218 範圍）：感情線／對手線 `when` 欄有 23 個獨特值
  （`story_detail_romance_vera_hiu_choi.json` 6 個、`story_detail_romance_lan_xu.json` 6 個、
  `story_detail_rival_mentor.json` 11 個）經 walk 顯示 1993／1994——要逐個對攻略故事時間先可以
  定顯示年份，唔好一刀切；L42608 commit48 窗口註解「1990 年秋起」vs「即 N15 秋末」（1992）
  本身唔一致，屬跟進項。
