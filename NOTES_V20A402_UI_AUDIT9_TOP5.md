# NOTES_V20A402_UI_AUDIT9_TOP5

第九輪 UI 檢視頭五項＋掣量頭項（報告 `~/workspace/linji-ui-audit-2026-11-24h/REPORT.md` §四＋§五，
GPT A 1／B 7／C 210，218 張截圖係 v401；停低條件係 GPT 全部 A，第十輪再檢視）。
基線 v401（main `3f72a41`，suite 426 PASS／9 FAIL）。

## 改動一覽（只做列明修復）

### 1. 卡片頂／底截字家族（避讓版位＋捲動安全區）
- 新函數 `hideMapLabelsUnderModal402()`／`restoreMapLabels402()`：modal 開嗰陣計 `.modal` 卡片 rect
（唔係成個 `#mask`），將相交嘅 `#map-names68.mn68`／`#map-districts97.md97` 加 `mn-hidden402`
（`visibility:hidden!important`，佈局不變，rect 照量到）；`closeModal()` 還原。掛鈎：`modal()` 入面
`maskEl.classList.add("on")` 之後；`closeModal()` 入面清 `scene-paper401` 嗰行之後。目標浮貼標籤
`#tut-target-label399` 唔係 `.mn68`，唔受影響。**後補 fix**：`drawMap()` 尾段（`deCollideLabels363()`
之後、`refreshTutSpotlight398()` 之前）亦叫一次——modal() 嗰陣標籤可能未定位（TUT_MAP 實測：
modal() 嗰陣標籤仲係 0,0，hide 跳過晒；跟住 drawMap 先將「何生事務所」擺去 536.8，撞住卡頂 543.8）。
冇卡開嗰陣 `#modal` rect 係 0，hit 全部 false，等於還原，唔會誤遮。
- `#modal-inner` 加 `padding-bottom:calc(16px + env(safe-area-inset-bottom, 0px))`（`#modal-btns` 係
sibling 唔係 overlay，16px 已夠做安全網）。
- `#app.notebook` padding-bottom `84px`→`calc(119px + env(safe-area-inset-bottom, 0px))`（底欄實高：
home265-row 44px＋#nb-actions 75px＝119px；v197 嗰陣 84px 已過時）。
- `#app #loc-sheet.sheet.act.h` 去 `-webkit-line-clamp:1`（`display:block!important` 覆寫）。
- 實駕：tut step1／step2 nStraddling **2→0**；46 醫院卡 4 個標籤全部 hidden；43d 日期行 scrollTop 0
完全露出（基線藏 11.5px）；33 捲到底尾段完整；11b／11c paddingBottom "119px"，捲到底達 max scroll。

### 2. 「繼續」金掣字邊殘影＋43d 支票「簽約金」掂底線
- 成因已定位：VM 實測 Noto Sans CJK TC 得 Regular 無 Bold，但有 Noto Serif CJK TC Bold；headless
Chromium 用合成粗體（double-strike）渲 `font-weight:700` → 筆畫雙邊殘影。`text-shadow:none` 早已有，
殘影唔係陰影。修法：v401 金掣規則（`button.p,.start button.p,.gig-actions button.p,.nb-actions button.ink`）
加 `font-family:"Noto Serif CJK TC","Noto Serif TC","Songti TC",serif!important; font-synthesis:none!important;`。
實駕：43b zoom 圖「繼續」字邊乾淨（serif、無殘影／黏連）；43d zoom 圖「好」同樣乾淨。
- 支票：`chk101EnsureCss()` 入面 `.chk101` margin `10px 0 4px`→`14px 6px 8px`（留四周紙邊）；
`.ck-memo` top `86.3%`→`84%`。實測：memo「簽約金」距支票底 20.6px（基線 16.6px 且越 memo 格底線約 4px）；
日期行「1990年1月3日（三）· 第1週」scrollTop 0 已完全露出（基線藏 11.5px）。

### 3. 35c P1 大標異常＋P2 圖文錯配（＋v398 fade 張力，見下）
- P1 大標 live 來源已查清：係 stub `pressTemplates` 經 `awardsPickPressNews()` → `buildAwardResultPack()` →
`renderAwardResultHtml()` 嘅 `headline214`；L38334 嗰個同字串 call 係 self-test（declined 路徑），唔係 live 來源。
修 stub＋fallback：`content/STUB_AWARDS_CEREMONY_v1.json` 三個模板——ad「廣告年賞揭盅，新人榜上有名」、
film「影藝獎揭盅，銀幕新人受注目」、tv「台慶頒獎夜，新人榜上有名」；music「金碟夜，樂壇新人輩出」保留。
`index.html` fallback（`awardsCopyLine(press.headline, …)`）→「頒獎夜落幕」，dek fallback→「典禮散場，名單見報。」；
測試輸入字串（declined 路徑）同步改做新 ad 大標。刻意避開「入圍／提名／得獎／奪獎」四字（gallery 路徑測試禁呢啲字）。
實駕：P1 大標「廣告年賞揭盅，新人榜上有名」；P2 捲到底 dual 行完全露出（dualBottom 733 ＜ viewBottom 753）。
- P2：`np214AwardPhoto214()` 得兩個相 key（玩家 `np214_award_awi`／駱家聲 `np214_award_lok`），無彭少祺相，
所以修法係加標記唔係換相。`photoFigure214(p, mark)` 加 mark 參數；`mark214 = (pack.bestOutcome==="nominated" && win149)? "入圍者": ""`，
P2 嗰次 call 傳入；CSS 加 `.paper-sheet.np214-photomark`（黑底白字小籤，左上角）。玩家贏／旁聽嗰陣冇 P2 相，唔出標記。
實駕：P2 相（陳偉翔）左上角有「入圍者」黑籤，圖說「陳偉翔憑《新春團圓》入圍，散場時離開會場。」；P1 相亦有「入圍」小籤（P1 路徑本身已有）。
P1／P2 底掣 label 係「收下這晚」（L35044 原文，唔係截斷）。
- **v398 fade 張力（重要）**：第九輪要求「P1／P2 首屏主欄底 fade 收喺完整段落後，淡出只落空白紙邊」，v402 最初拆走
`#modal-inner:has(.awd-result396)` 嘅 26px mask fade 規則（v398 加嘅）＋將 `.paper-sheet.awd-result396`
padding-bottom 由 24px→32px。suite 證明 v398 test 釘住呢條 rule 存在（v398 原意：「頒獎結果卡捲動區底 26px
淡出——摺位切字行讀做『未完待續』，唔係半隻字俾切走。只限結果卡，晨報唔郁。」）——**已還原原 rule**，padding-bottom
32px 保留。張力：摺位嗰 26px 柔化係 v398 設計嘅「未完待續」提示，唔係 bug；洗字疑慮靠 32px 紙底留白緩解——捲到底
嗰陣 fade 落喺空白紙邊。第十輪再審呢個設計抉擇（若果要改，須同步更新 v398 test，唔好再靜默拆 rule）。

### 4. 地圖頂行＋玩家標籤遮擋（成因已定：clamp 唔識 zone）
- 07c 遮擋物：`.map-here373` 橫條（「目前所在：阿偉屋企」＋像素人圖，`top:6px`），喺約會層嗰陣取代玩家標記；
實測同「廟街禮品」標籤相交 24.2×9.8px。修法：`deCollideLabels363()` 入面，`.map-me363` zone 計完之後，
再將 `.map-here373` rect（＋4px 緩衝）併入同一 `zone391`（無 zone 嗰陣直接用 strip rect）。
- `pushOffMarker391()` 入面 `parseFloat(it.el.style.top)||0` 改為 `it.el.offsetTop`（標籤 inline top 係 `calc()`，
例如 `calc(16% - 52px)`，parseFloat 得 NaN→0，令邊界檢查誤判）。
- `@keyframes settle363` 每幀補返 `translate(-50%,-88%)`（原本 keyframes 嘅 transform 會成個蓋走 `.map-me363`
本身嗰個定位 transform，0.18s 內 marker 低 26.4px）。實測證實動畫唔影響 deCollide 量 zone，動畫已還原保留。
- `.map-well` 嘅 `ResizeObserver` callback 加埋 `deCollideLabels363()`（同 drawMap 次序一致）。
- **真正修復**：`deCollideLabels363()` 尾段 v398 嘅 `clampMapLabels397()` 之後，加返 `pushOffMarker391()`——
clamp 唔識 zone，為咗籤同籤之間嘅 8px 間距會將標籤推返落 tag 區；障礙推撞放最尾，zone 永遠係最後權威。
**關鍵細節：clamp 只改 style.top，唔會更新 items 嘅快取 rect（`it.r`）——推之前要先刷新
`items.forEach(it=>{ it.r = it.el.getBoundingClientRect();})`，否則 push 用舊 rect 以為已經清咗，唔郁。**
`paintBar()` 尾段 v397 嘅 `clampMapLabels397()` 之後亦加 `deCollideLabels363()`（idempotent，收尾一定係 zone 推撞）。
- 試過但撤回嘅錯誤修法：① 將 push 寫返入錨點 `map137aoff`——引發失控累積（label 飛到 193px），已撤回。
② 拆 `settle363` 動畫——證實唔係成因，已還原。
- 實駕：07c strip overlap 0；gift_shop 844 overlap **0**（label 79.6–97.6，tag 109.5–126.3，隔 12px）；
gift_shop h682 overlap 0；05b／07c 計數不變（23／14）；17 個標籤之間零重疊（home 同 gift_shop 狀態都驗過）。
h682 marker 頂部被裁少少（top −2.2 至 −3.6）係 pre-existing，唔係 v402 回歸，唔郁。

### 5. 通告欄／詳情去報表化最後一里＋陣容尾行圖證
- (5a) `.board-head392` 改 flex 橫列（統計剪報標籤靠左、整理紙籤靠右）；`.board-ctl397` margin-top 歸 0。
實測：板頭統計＋整理同一橫列（stats top 126.5–157.3，整理掣靠右）。
- (5b) `.board-menu397` 做側邊索引紙：闊 180px、米紙漸變底、邊框、紙影、微斜 -0.6deg、貼右緣。
紅筆剔號本身 v401 已有（`.board-chip392.on::after` 紅 ✓）。實測：menu rect x184.6／w182.8／h271.9，
米紙漸變底，微斜 -0.6deg（matrix -0.01047），選中 chip「預期日薪」on:true，afterContent "✓"，
afterColor rgb(179,38,30) 紅。
- (5c) 推介卡加劇照式插畫：`gigBoardTeaserHtml()` 入面 `featured392` 嗰陣加 `.gt-still402`（`data-type`＝媒介，
用作品牆同一套 CSS 卡語言 `.work-csscard59` 媒介底色＋角標；大字首字＋媒介／劇種，橫式 62px 高）。海報已刪
（v229，`poster59Path()` 回空字串），所以用 CSS 卡唔係佔位圖；有海報嗰日先換真圖。推介卡揀法：
`readyF392` 入面片酬最高嗰張。實測：推介卡高 164.3px（其他卡 92.3px），「冬」大字＋「電視劇」＋綠色「電視劇」角標。
**註**：推介卡加高 72px，令第 6 張「一屋人」喺 scrollTop 0 嗰陣 visibleH 由基線 46 變 4（更入摺位）；
捲到底全部卡完整露出——按已定驗收（「捲到底完整露出」），可接受。
- 陣容尾行圖證：`402_board_detail_cast.png` 影到「女配角江詩盈」尾行，fullyVisible＝true（實駕驗收用，唔入版）。

### 6. 掣量（背景互動層卸載，唔係前景掣多）
- ③⑤ `setUnderlyingInert()` 入面教學豁免收窄到只限 TUT_MAP（`tutMap = tut && (mask.dataset.tutStep === "TUT_MAP")`；
`ui-hide-under396`／`dayres-scene397` 用 `!tutMap` 而唔係 `!tut`）。`setTutMask()` 改為由 mask class 推導 scene
再叫 `setUnderlyingInert`：`scene402 = m.classList.contains("scene-paper401") || m.classList.contains("day-res") || (m.dataset.tutStep === "TUT_BOARD")`。
成因：43e 落選卡 `presentAudFailSettlement()` 先 `setTutMask(true)` → `modal(..., {scenePaper401:true})` 掛 `dayres-scene397` →
再 `setTutMask(true)` 用 scene=undefined 清走咗 scene 卸載。TUT_MAP 嗰陣背景要留低（聚光目標 pin 要見到）；TUT_BOARD 用
scene 卸載（`dayres-scene397` 收 pin＋掣、留板舞台，因為 `#tut-board-stage` 喺 `#v-map` 入面，`ui-hide-under396` 會連舞台一齊收起）。
- ① 預覽卡非互動：`showTutBoardStage()` 渲染後去 `.gig-teaser[role='button']` 嘅 `role`＋`tabindex`；CSS 再加
`#tut-board-stage.gig-teaser{pointer-events:none!important}` 兜底。
- ② tut_01 只留 1 粒 pin：CSS `#app.tut-stage397 #map-pins.pin:not(.tut-spotlight-target){display:none!important}`。
- ④ 35b 典禮：`#app.awd-stage-on402` CSS 收 `#v-map, #v-home, #v-start,.bar, #menubar,.menu, #loc-sheet, #btn-confirm-plan`；
`awards62PlayCeremony()` 入面 `document.body.appendChild(stage)` 之後加 class，`cleanup()`（唯一拆 stage 嘅地方）入面除 class。
舞台本身掛喺 body，唔受影響，只留跳過掣。
- ⑥ 24_menu：`#app.menu-open402` CSS 收 `#v-map.map-wrap, #chip-story, #loc-sheet, #v-home, #v-start, #menubar, #btn-confirm-plan`
（`#menu` 喺 `#v-map` 入面，唔可以直接 hide `#v-map`；留返 `#map-bar` 等 ☰ 可以關單）。掛鈎三處：`btn-menu.onclick`（toggle 時同步
toggle class）、`menu.onclick`（撳項目即除 class）、`document.body` click listener（撳外面關單嗰陣除 class）；`modal()` 入面亦清 class 做兜底。
- ⑦ 32／08／25b 面板：CSS `.map-wrap.sheet-open #map-pins.pin{display:none!important}`（只收 `.pin` 掣，玩家標記 `.map-me363`／
日卡橫條 `.map-here373` 留低做位置提示——佢哋唔係掣，唔計數）。
- 掣量（COUNT_JS 定義：可見 button／a／input／select／textarea／summary／[role=button]／[tabindex]；修後 vs 基線）：
24_menu **28→6**（−22 ✓）；08_tv **27→11**（−16；面板由基線 4 變 6，係當時狀態多咗「傾談／播劇情」兩粒情境掣，唔係修復失效）；
32_cafe **28→11**（−17 ✓）；25b_date **14→6**（−8）；tut_01 **23→6**（−17；目標 pin 本身唔計入 count，因為計數器嘅可見性規則
唔計被 mask 蓋住嘅 pin；教學流程可推進到 step2／step3，證實目標 pin 可撳）；tut_step2 **29→2**（−27）；
43e **1**（見下）；43f **1**（不變）；33 **3**、33b **15**、36 **3**（不變）；07_map_baseline **23**（不變）；08b 紅字 5.36:1。
- **43e 專項驗證**（`/tmp/probe_43e.py`）：新局、做一次試鏡、將 pending 翻做 ok=false、revealDay 設聽日、再做多一次試鏡推日子——
結算卡「本次未獲聘」出現，count **total 1**（淨係「我知道了」），mask 係 `mask on scene398 scene-paper401 tut-on`（scene 卸載生效），
clash 標籤全部 hidden。**關鍵**：day 2 試鏡後地圖上冇「過一日」掣（`startTodayScheduleFromMap` 係 IIFE 內部函數），要靠再做一次試鏡先推到日子。
- 已核實唔做嘅：兩店重複購買入口唔存在（v396 已改單一購買，行係 div 唔係掣）；約會入口合併唔應做（`addRom159DateActs()` 係揀人先，
約會層 pin 係揀地點先，唔係同功能）；09b 鎖定版多出一掣未重現（locked vs unlocked 完全一樣，截圖 md5 同審計嗰張一樣）；
「未開放（1）」死掣同 45 病倒卡綠字唔喺範圍，唔郁。

### 7. 附帶小項
- 紅印「臨」加深：`assets/ui-physical/notice/seal_extra.png` 紅像素 ×0.85（source red median (196,59,42)→(166,50,35)；
原檔備份喺 `/tmp/seal_extra_orig.png`）。揀 k 嘅方法：PIL 模擬渲染（bilinear＋GaussianBlur 0.4 校準到實測基線：
臨 2.36 vs 實測 2.39）→ k=0.9 預測 3.05、k=0.8 預測 3.31，取 k=0.85 預期約 3.15（同「初」3.03–3.12 一致）。
`seal_junior.png`（初）唔郁。唔改 `?v=20a8`。
- 08b 紅字：只改 `#loc-sheet.sheet.act.cost` 規則，`#C43C2A`→`#A93222`（喺 `#F5E6C0` 上實測 5.36:1，≥4.5:1）；
`--stamp-red` 原值唔郁。

## 測試
- 全套 suite：**TOTAL PASS 426 FAIL 9**（`~/workspace/suite402.txt`；基線 426／9，9 項 FAIL 同基線逐項相同：
flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38——全部 pre-existing，零新 FAIL）。
第一次跑 415／20——11 項新 FAIL 全部同 v402 改動有關，分三類，已全部修好（見下），重跑已消除：
  - (A) 純行號／總行數漂移（7 項）：gift185／rom159／rom176／tang152／tang171／tang173／text125／travel114——
    `qa402/resync402.py`（OLD＝v401 main `3f72a41`，difflib 映射，內容逐字核實純漂移）：
    travel114 FREE 44／COUNT 13／DEF 46334→46522／WRAPPER 32443→32625；rom159 6 釘＋全佳行；rom176 6 釘；
    tang152 兩釘；text125 三錨點；gift185／tang171／tang173 總行數 51561→51771（淨 +210）、
    openLoc DEF 46334→46522、tang173 lines[5393]→[5412]（8 處）。
  - (B) 有意圖行為改動（2 項）：v398——fade rule 拆走後 test 釘住佢，**已還原原 rule**（padding-bottom 32px 保留；
    張力見 §3）；v396——`setUnderlyingInert` 期望字串 `!tut`→`!tutMap`（任務 6③⑤要求，見 test 檔頭 v402 註記）。
  - (C) 函數體增長推過 test 抽取窗（1 項）：s30dedup117 D3——still402 註解縮短 ~90 字元（行數不變），
    `<div class="gt-meta">`／`gt-meta-line` 返入 6000 字元窗；test 本身唔郁。
- 11 項受影響測試逐個重跑全部 PASS（v396 43 checks／v398 38/38／s30dedup117／gift185／rom159／rom176／tang152／
tang171 22/22／tang173 22/22／text125／travel114）。
- 實駕：`~/workspace/linji-drive402/drive402.py`（`--only phone,hosp,tut,awards,board,map,notebook,counts,verify`；
證據 `~/workspace/linji-drive402/`——53 張截圖＋JSON）。逐項數字見上面各節。

## 遺留／下一批
- v398 fade 張力（§3）：第十輪再審「未完待續」淡出 vs 洗字；若果要改，須同步更新 v398 test。
- 09b 鎖定版多出一掣未重現（locked vs unlocked 完全一樣），唔郁。
- h682 marker 頂部被裁少少（pre-existing，唔係 v402 回歸），唔郁。
- 首屏摺位半行／半格係正常捲動提示，驗收係「捲到底完整露出」，唔係首屏零半行（已定，唔再拗）。
