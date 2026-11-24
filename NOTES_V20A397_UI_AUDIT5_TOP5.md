# NOTES_V20A397_UI_AUDIT5_TOP5 — 第五輪 UI 檢視頭五項修正（2026-11-25）

- 底：v396 main `e92a457`；suite 基線 417 PASS／9 FAIL（九項 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。
- 依據：`~/workspace/linji-ui-audit-2026-11-24d/REPORT.md`（GPT A 0／B 2／C 92、Gemini A 0／B 85／C 9；可比 82 屏全部維持原級，0 升 0 跌）。GPT 逐屏原稿 `gpt/*.txt`，專項覆驗 `gpt/priority_*.txt`，Gemini 設計圖 `gemini/design_*.png`＋`gemini/design_notes.md`。
- 實駕：Playwright harness（venv `/home/hatch/pwenv49/bin/python`，Chromium headless shell，本地 CONNECT 中繼 `~/workspace/local_proxy.py` 127.0.0.1:18081，viewport 390×844 dsf 2），driver `qa397/drive397.py`，量度 `qa397/verify/*.json`，截圖 `qa397/shots/`。
- Suite：首輪 406／22（13 項新 FAIL 全係 resync 範圍）；resync 後 **419 PASS／9 FAIL**（同一九項 pre-existing；＋2 係新增 test_v397_static／test_v397_logic）。
- index.html 淨 +338 行（50641→50979）；openLoc DEF 行 45592→45873（＋281）。

## 1. venue99 相疊＋地圖底邊截籤

修前基線（qa397，390×844）：紅棉影業 x240.4–304.4／y221.4–239.4 vs 金禧大酒店 x298–370.1／y221.5–234.1，相交 6.4×12.6＝80.6px²；390×682 相交 6.6×12.6＝83.2px²。上一輪「0 互撞」只計 17 個 `.mn68`，金禧係 `.md97-venue99` div，根本唔喺量度集合入面。
底邊截籤機制（audit 06／05b_h682 截圖親自睇圖確認）：金鐘創意喺地圖底邊只露底部筆畫；何生事務所兩行吊牌「可打聽」第二行被地圖底邊裁切。成因係 labels 由 % 錨點換算 px（`positionMapLabels137`），日卡變高／舞台縮短嗰陣若無重定位，px 位置過時就裁切；viewport resize 有 debounce 重畫（160ms → `scheduleStoryMapRedraw`），但 `paintBar`（日卡渲染）多數路徑唔帶 `drawMap`，所以 hint 變高可以唔觸發重定位。

實裝：
- 金禧錨點 HTML `left:86%;top:24%` → `top:calc(24% + 30px)`（L7157）。
- 新增 `clampMapLabels397()`（`positionMapLabels137` 之後）：量度全部 `.mn68`＋`.md97-venue99`，水平重疊且垂直淨距 ＜8px 就將下面嗰張移夠 8px（貼底改向上移，放喺上面嗰張頂邊之上 8px），任何籤底邊出 `.map-well` 就向上夾返入舞台留 4px；最多三輪，唔改 dataset 錨點原值；地圖隱藏／舞台冇尺寸即刻返。
- `positionMapLabels137` 尾呼叫 clamp；`paintBar` 尾（`paintPageHead363()` 之後）呼叫 clamp，覆蓋 hint 變高唔帶 drawMap 嘅路徑；`.map-well` 上加 `ResizeObserver`（`window.__mapRO397` 守衛防重裝；well 無尺寸嗰陣跳過），舞台尺寸一變即重定位。
- Clamp 數學細節：重疊嗰陣單次 pass 未必一次到位（例如兩籤同 top：need = 8−(−13) = 21，移完淨距得 3px），靠最多三輪迭代收斂到 ≥8px；logic test 斷言最終淨距 ≥8 而唔係單次到位。

修後實測（venue probe）：844／682／seeded844／seeded682 四種情況 overlaps 全部 []；844 紅棉 bottom 238.9、金禧 top 251.3，垂直淨距 12.4px ≥8；金鐘創意底邊 clearance：844 7.7px、682 11.3px、seeded844 10.9px、seeded682 9.5px（stageBottom 615.8／534.8）。截圖 `qa397/shots/venue_844_397.png` 親自睇圖確認紅棉／金禧分行、金鐘完整。

## 2. 35c 殘留：底欄切字＋右欄淡出＋第二版雙焦

結構（`renderAwardResultHtml` 約 L34100，`np214AwardPhoto214` 約 L34040）：P1＝報頭＋主相＋圖說＋單欄正文＋右欄（`np214-sidebar`，直排「影視娛樂」＋快訊）＋小檔案（已搬第二版）；P2＝主標講得主奪獎，dek＝focus 格入圍句（audit 指「逐字重複第一版入圍段」嗰句「入圍名單上有陳偉翔的名字。獎盃未到手，街外已經有人記得他的樣子。」）、lead＝`metricLabel——metricHead`（重複主標）、主相＝同一張陳偉翔相、圖說＝「陳偉翔身穿燕尾服出席〈典禮名〉，憑《作品》入圍。」；相內橫額寫「星河金碟夜」，同圖說嘅「維港街招・年度廣告賞」對唔上。

修前基線（awards probe）：P1 caption bottom 782.1 vs `#modal-inner` bottom 753，截 ~29px（fullyVisible false）；miScrollH 1071 > miH 629；P1 sidebar filler-v 在位；P2 head「彭少祺憑《冬暖》奪獎」、dek／lead／cap 逐字重複已確認；P2 caption 首行 top 726.4 bottom 763.3 vs miBottom 753，一樣半截。

實裝：
- 結果卡專屬報頭收緊約 36px（只限 `.awd-result396`，晨報唔郁）：報頭名 46px→36px、rule-thin margin 6→3、eng margin 5→2、dateline margin 4→2、kicker margin-top 8→4、headline margin-bottom 5→3、dek padding 5→3／margin-bottom 8→6、photowrap margin 8→4px auto。
- 結果卡 sidebar 嘅 filler-v `<p>` 換成非文字印記 `<span class="np214-sb-mark397">❦</span>`（CSS：置中、14px、紅 #b32020）；晨報渲染器（約 L37346–37348）唔郁，filler-v 喺晨報保留。
- `np214AwardPhoto214` 加 `opts.aftermath` 分支：nominated＋aftermath 嗰陣圖說改散場版「陳偉翔憑《rep》入圍，散場時離開會場。」（唔提典禮名，避開相內橫額 mismatch）。
- P2 只限入圍＋有得主 `win149` 嗰陣：dek 改散場鏡頭「散場時分，掌聲未散；憑《rep》入圍的陳偉翔在人群中離開會場。」（`metricDek397`，用 `rep214` 真數據）；lead 改寫「{winLine214}。散場報道的觀察對象，是憑《rep》入圍的陳偉翔。」（`metricLead397`，用 `winLine214`／`rep214` 真數據）；photo2 用 `np214AwardPhoto214(pack, {aftermath:true})`。冇得主嗰陣沿用舊寫法。
- 設計圖 `gemini/design_result35c.png` 係方向參考，圖中阿偉拎獎座係錯（呢次只入圍未得獎）。

修後實測（awards probe）：P1 mastH 97.3→78.8；caption bottom 747.6 ≤ 753，fullyVisible true；miScrollH 1071→1032；fillerV false、sbMark true；P1 底邊捲到底嗰陣最後一段 sidebar 正文底 468.6 < 753（正文喺淡出前收尾）。P2：dek「散場時分，掌聲未散；憑《新春團圓》入圍的陳偉翔在人群中離開會場。」、lead「彭少祺憑《冬暖》奪獎。散場報道的觀察對象，是憑《新春團圓》入圍的陳偉翔。」、cap「陳偉翔憑《新春團圓》入圍，散場時離開會場。」、captionFirst bottom 712.8 ≤ 753 fullyVisible true；P2 head「彭少祺憑《冬暖》奪獎」不變。

## 3. 通告欄峰值：頂欄報表感＋$82 計法唔透明＋鎖定摘要插斷清單

⚠️ 圖釘撞標題唔成立，唔使修：三重獨立量度證實金釘同最長標題字尾橫向相隔逾 100px（peak 最小 126.6px），GPT 將同橫帶誤讀為接觸。

修前基線（board probe，高 stats seed）：headH 96px；sort 3 粒（預期日薪／總片酬／成功率）＋filter 3 粒（全部／電視劇／綜藝）；17 張卡，0 未達標；$82 卡係 `gig_1990_tv_110`「冬日鄰里情」推介，meta「預期 $82／日｜4 日｜86%」；詳情：片酬 $378（約酬 $343–$413）、成功率 約 86%、通告日數 共 4 天；`hasCalc` false（未有計法行）。低 stats seed（演技等全 10、體能 40）基線：共 17 張 · 可接 8 張 · 未達標 9 張；listOrder＝[一哥一姐推介，LOCKED-DETAILS，金曲季選歌舞晚會伴舞，電視城長劇，電視城天台群演，幕後英雄，街市喜宴，錄影廠觀眾群演，茶餐廳一幕]——LOCKED-DETAILS 排第 2，插斷可接清單。

實裝：
- 頂欄縮薄：`.board-head392` padding 6px→4px、margin-bottom 8→6px，`position:sticky;top:0;` 保留（test_v392 釘死）。
- 排序／篩選各收納成一粒下拉掣並排一行（`.board-ctl397` flex row）：「排序：預期日薪 ▾」「媒介：全部 ▾」，撳開先展開選項（in-flow，唔疊內容；選單 `hidden` 預設收起）；wrapper 保留 `board-sort392`／`board-filter392` class（test_v396 釘死呢兩個字串在位）；選項沿用 `data-sort392`／`data-filter392`，現有 `doScout` 尾段 wiring 一併接上；新增 toggle wiring（`data-board-menu397`，一次只開一粒，撳第二次收起）。
- 新增 helper `boardExpCalc397(g)`（放 `board392ExpDaily` 附近；用 `gigPayExact`／`chance`／`effectiveShootDays`，全部 typeof 守門，抽唔到回 null；回傳 `{pay, chance, days, raw, rounded}`；`chance()` 回傳分數（0.863），唔係百分比）。`openCastingNoticeDetail` gate.ok 分支加計法行 `<p class="board-calc397">`，例如「預期日薪 $82／日＝片酬 $378 × 成功率 86.3% ÷ 4 日（未取整 $81.5，四捨五入）」——audit 嘅 378×86%÷4＝81.27 係用已取整 86% 計，真正未取整成功率約 86.3–86.5%（視 seed 而定）。
- 鎖定摘要 `<details class="gig-locked108">` 由 layered 分支嘅推介卡之後、移去可接清單最尾（非 layered 分支本身已喺最尾）。

修後實測：headH 96→60px；可見排序／篩選控制由 6 粒 chips 變 2 粒 toggle（modal 內可見 button 共 3 粒：2 toggle＋「返去地點」；隱藏選單選項仍喺 DOM，唔計可見數）；計法行在位（呢次 seed：86.3% → $81.5 → $82）；低 stats board（`board_low` probe）：LOCKED-DETAILS 由 index 1 移到 index 8／共 9（最尾），8 張可接卡全部行先；sum「共 17 張 · 可接 8 張 · 未達標 9 張」，lockedSummary「未達標／長遠目標（9 張）最接近：台慶晚會歌舞劇助演（差 2）」。

## 4. 40／27／86 家族：bottom-sheet＋大幅黑底＋金掣層級

成因已確認（v396 NOTES）：v396 卸載（`ui-hide-under396`，`display:none`）令任何 modal 背後都係深色 `#app` 殼——漸變頂部.18 無地圖可透，backdrop 讀做平實深色。

修前基線（dayres／dayres2 probes）：rest 卡 maskBgImg `linear-gradient(rgba(0,0,0,0.18) 0px, rgba(0,0,0,0.18) 48px, rgba(0,0,0,0.58) 48px)`；appCls "ui-inert ui-hide-under396 mask-up"，vmapVisible false、pins 0、mapImg w0 h0（地圖完全隱藏，大幅黑底確認）；40 modal got40 true，掣順序 [「開始並結算當日」role p（第一），「返回休息卡」role g（第二）]，modalRect y 615.8 h 218.2 bottom 834（近底部 bottom-sheet）；撳外面（195,120）dismiss 後返去休息卡（day 18，h3「休息（週四）」）。86c（週結卡）：day 21，h3「休息（週日）」，gold「一週完結 → 回家結算」，stamp null，bodyHasHomeSettle true，btns ["回家結算"]。27c（訓練卡）：「演技訓練」，statRows 5–6（數值隨機；一次係演技 +6／台風 +1／現金 −$20／壓力 +12／演技 +1，另一次係演技 +4／台風 +1／現金 −$20／壓力 +12／壓力 −3；第三次係演技 +6／台風 +1／現金 −$20／壓力 +8／台風 +1／壓力 −2），ledger null。

實裝：
- modal 加 `keepScene397` opt（`afterDayModal` 約 L21889、`presentRestSleepDayEnd` 約 L47452、`presentStartScheduleConfirm45` 約 L47406 三處傳入），`modal()`（約 L25053）傳去 `setUnderlyingInert(true,!!opts.keepScene397)`；`setUnderlyingInert(on, scene)`：scene 嗰陣唔加 `ui-hide-under396`，改加 `#app.dayres-scene397` class：地圖／屋企場景影像留低可見，但掣全部 `display:none`（`#map-pins`、`#v-map button`、`#v-home button`、`#menubar`、`.menu`、`#btn-confirm-plan`、`#loc-sheet`）；`closeModal`／`setUnderlyingInert(false)` 清埋兩個 class；教學 tut-on 豁免同 ui-hide-under396 一致。**注意：`.mn68` 籤同地圖唔喺收起清單入面；`#map-pins` 只含可撳 pins（`.mn68` 係佢嘅兄弟元素，唔喺入面），收起 pins 唔會收起籤。**
- 日結漸變放淺：`body.day-res-open #mask.day-res`（約 L2229）由.18／.58 改.10／.42。
- 40 號掣層級：`presentStartScheduleConfirm45` 入面「返回休息卡」改 role "p" 並移去第一位，「開始並結算當日」降做 role "g"；保留 `if(goCancel) btns45.push` 呢行（test_dayend202_static 釘死）＋「返回休息卡」字串，用 push 後 reorder（`btns45.unshift(b45)`）實現。
- 86c 刪重複「回家結算」：**全部 12 處** `一週完結 → 回家結算` 金句改做 `<p class="dayres-stamp397">一週完結</p>` 紅印章（跟 wrap-stamp369 屋企印章樣：2px 紅框 #9E2F2F、letter-spacing.14em、微斜；CSS `.dayres-stamp397` 約 L3300 後）：`presentRestSleepDayEnd` gold 行、`afterDayModal` extra、`flushWeekAccelSummary` extra、`resolvePlannedDay` rest fallback modal＋主 modal、`presentAudFailSettlement` notesHtml、doTalk、doAudition、doGiveGift、約會 modal；另有兩處 call-site（`conseq61ResolveSickDay` 約 L18921、`resolvePlannedDay` 約 L23630）原本向 `flushWeekAccelSummary` 傳 body＋金句——而家函數自己加印章，call-site 嗰句已刪走，免重複兩行。修後 `grep -c '一週完結 → 回家結算'` = 0，`dayres-stamp397` 出現 11 次（10 個模板＋1 個 CSS 定義）。
- 27c 數值改一行手帳記錄：新增 post-process helper `dayResLedger397(html)`（放 `formatResultNotes` 之後，約 L18330）：用 regex 抽 `.res-stat374` 行嘅名／值，砌一行 `演技 +7 ／ 現金 −$20 ／ 壓力 +12`（class `dayres-ledger397`，手寫體 LXGW WenKai），刪走個別 stat 框，敘事行（`.res-note374`）保留；無 stat 行嗰陣唔變；同名行要合併（演技 +6＋+1 → 演技 +7；壓力 +8／−2 → 壓力 +6）；唔識 parse 嘅行原樣留返，唔會靜默刪走。套用喺兩條日結路徑：`afterDayModal` 頂（`resultHtml = dayResLedger397(resultHtml)`）＋`resolvePlannedDay` 嘅 body（`body` 由 const 改 let，構造後 ledger；訓練卡行 `resolvePlannedDay` 自家 modal，唔經 `afterDayModal`，所以兩邊都要加；休息卡經 `formatRestSleepDeltas`，唔受影響）。

修後實測（dayres＋dayres2 probes）：rest 卡 maskBgImg `.10／.42`；appCls `ui-inert mask-up dayres-scene397`（無 ui-hide-under396）；vmapVisible true、mapImg 384×576 可見；pinsVisible 0。40 modal：btns [「返回休息卡」role p（第一），「開始並結算當日」role g]；modalRect y 615.8 h 218.2 bottom 834（仍係 bottom-sheet）；dismiss 後返休息卡（day 18，h3「休息（週四）」）。86c：gold null、stamp「一週完結」、bodyHasHomeSettle false、btns ["回家結算"]。27c：statRows 0、ledger「演技 +4 ／ 台風 +1 ／ 現金 −$20 ／ 壓力 +12」、敘事行「電視台排練結束，阿偉記住鏡頭位置。」保留、h3「演技訓練」。

## 5. 掣量：開局分步＋行程工具合併＋約會入口合併＋排序／篩選收納＋刪選單「過一日」

⚠️ Modal 背景卸載已解決，唔使重做；排序／篩選 6 粒值得保留功能，只減入口數；通告卡逐張可撳、地圖 pin、日期格、劇情選項同唯一確認掣唔應刪。

修前基線（counts probe）：02b＝31、03＝31（教學卡＋手帳全頁；31 項明細：返回地圖＋4 組 tab＋2 sub-tab＋進度＋4 工具＋7 日格＋壓力估＋5 分類＋到處逛逛行＋留話簿＋還原＋確定本週行程＋下一步＋跳過教學）；11d＝29（audit 係 33，seed 差異；同一 seed 前後對比為準）；24_menu＝28（audit 係 32，狀態差異；選單 6 項：過一日／重看教學／設定／存檔／讀檔／新遊戲）；情報站 12 個 act，6 粒約會掣（約林曉晴／周采兒／藍若曦／徐寶珊／葉敏芝／蘇芷茵出街，hint 寫 7／5／6／7／6／6 個地方揀，$4 起）；33b＝22（返回地圖＋4 組 tab＋2 sub-tab＋進度＋7 日格＋5 分類＋留話簿＋開始今日行程；editable false、catTabsVisible 5、dayRows 7、intelVisible true）。

實裝：
- 02b／03／04 開局分步——`setTutMask`（約 L49929）加 toggle `#app.tut-stage397` class，教學期間隱藏手帳次要控制：事業／帳本／人情組 tab（`#hgroup-career`／`#hgroup-status`／`#hgroup-favor`）、衣櫃 sub-tab（`#htab-wardrobe`）、進度 badge（`#prog389-badge`）、壓力估（`#nb-live-stress`）、分類列 `#cat-tabs`、活動列 `#act-list`、留話簿（`#btn-intel381`）；保留返回地圖＋行程＋本週安排＋7 日格＋行程工具（1 粒）＋確定本週行程＋下一步＋跳過教學＝14。教學卡本身只係「讀＋下一步」（TUT_WELCOME／MAP／BOARD／DONE，`content/tutorial_zh_HK.json`），唔使喺卡度揀活動，所以隱藏 `#act-list` 安全；教學完 `setTutMask(false)` 即還原。TUT_WELCOME spotlight 係 `#btn-confirm-plan`（保留，唔受影響）。
- 行程工具收成一粒：`#nb-quick` 入面 4 掣（`#nb-q-rest`／`#nb-q-train`／`#nb-q-clear`／`#nb-q-copy`）＋`#btn-reset-plan` 還原（原喺 `#nb-actions`）一併搬入下拉選單 `#nb-tools397-menu`（預設 hidden），開關掣 `#nb-q-tools397`「行程工具 ▾」一粒（開合切換 ▾／▴＋aria-expanded）；全部 id 同 handler 保留（`wireNotebookQuick` IIFE 按 id 接線，搬 DOM 位置唔影響；`document.getElementById("btn-reset-plan").onclick=resetPlanDraft` 保留；test_book143 釘死呢啲 id 在位）；選單內掣撳完自動收埋（menu 上嘅 delegated click listener，bubble 階段收起，唔影響掣本身 onclick；`#nb-copy-wrap`／`#nb-train71-wrap` 留喺 `#nb-quick` 做選單外兄弟，複製／訓練流程唔變）。死 CSS 已刪：4 條 `#nb-actions #btn-reset-plan` 規則（flex／min-height／:disabled／B1 虛線底線樣），還原喺選單改用紙標籤樣（`#nb-tools397-menu #btn-reset-plan`＋`:disabled` 灰態保留）。**注意：鎖定態嗰陣成個工具組連 `#nb-quick` 一齊隱藏**——buttons197 B2「還原鎖定態唔消失」嘅 :disabled 灰態規則搬咗入選單（選擇器跟新位置），但鎖定／回顧態下掣本身唔可見，呢個係 5(g) 收起編輯工具同一意圖，唔係回歸。
- 情報站約會合併：`addRom159DateActs`（約 L45800）唔再逐個女角加「約X出街」act，改加一粒「約人出街」入口（hint「可約 N 位」，N＝已見面女角數；未見面唔計，v389 規則保留；有任何一位 gate ok 就加 `act-priority` class），入內開新 modal `rom159OpenDateWhoPicker(keys, L)` 列出各人（閘口原因／`rom159DateButtonInfo` hint 做 hint，沿用舊邏輯），揀人後開現成 `rom159OpenDatePicker(rk, L)`；modal 加「返回」掣經 `openLoc(L.id, {forceRestore:true})` 返地點面板（`travel114IsFree` 認 `forceRestore`，免再扣出行額度；onDismiss 同樣返地點面板）。6 位女角全數 spots 指向 `cafe_cha`（金龍茶餐廳，即情報站），meet 節點 R_*_meet；`test_map159_static.py:135` 釘死 `addRom159DateActs(add, L);` 出現 2 次，呼叫點唔郁（L46296／46313）。新加兩個 `forceRestore` 呼叫點已入 travel114 FREE_LINES（42→44，見 resync）。
- 09b：見第 3 項 (b)。
- 刪選單「過一日」：刪 `#menu` 入面 `<button data-m="rest-early">過一日</button>`（約 L7091）＋分隔線 `<div class="menu-sep">`（選單得返系統組，唔再分組；死 CSS `.menu-sep` 規則一併刪）＋menu handler 嘅 `rest-early` 分支；`confirmEarlyRestFromMenu` 函數本身保留（地圖「過一日」掣 L24673 仲用緊）。
- 「未開放」改不可撳紙標：故事選擇器約 L12946 `<button class="sp-play" disabled>…劇情未開放</button>` → `<span class="sp-lock-tag"><span class="sp-lock-ico" aria-hidden="true"></span>劇情未開放</span>`（保留 lock icon＋文字，test_ui128a4 釘死該字串；新增 CSS `.story-picker.sp-lock-tag`；L13019 已係 span，唔郁）。靜態 −1。
- 33b 回顧預設唯讀，收起編輯工具：在 `renderNotebook`（約 L22266）唯讀分支加：隱藏 `#cat-tabs`（5，編輯用分類篩選）、`#btn-intel381` 留話簿（1）、結局鎖定（`ending78Locked()`）嗰陣隱藏 `#home-back-map`「開始今日行程」（1）；插入點喺 hbm 區塊之後（等結局鎖定隱藏贏過 hbm 嘅 forced／soft 顯示邏輯）。預計 22→15。**誠實註記：4 係達唔到嘅目標**——要到 4 必須刪埋日格選擇（7）同組 tab 導覽（4+2），而 GPT 自己嘅保留清單話「每行一個可撳區」唔應刪；15 係可辯護數字，呢度寫明呢個判斷。
- 地點面板若係阻斷式，卸載地圖——**已判定：唔係阻斷式，唔卸載**。實測：情報站 sheet 開住嗰陣 COUNT 係 28（17 pins 仍計入可見掣）；地圖只鎖捲動（`.map-wrap.sheet-open{overflow:hidden}`）＋收起 hint，pins 明確 `pointer-events:auto`（CSS 註解「still tappable」），撳另一粒 pin 可以切換地點；卸載會破壞呢個流程。

修後實測（counts＋counts33b probes）：02b＝14（返回地圖、行程、本週安排、行程工具 ▾、7 日格、確定本週行程、下一步、跳過教學）、03＝14；11d＝25（29→25；11d_tools：quick 只剩 ["nb-q-tools397"]、toolsMenu true、resetVisible false、catTabs 5 項不變）；24_menu＝27（選單得返 5 項：重看教學／設定／存檔／讀檔／新遊戲；menu_btns 印證）；情報站 acts 6 個（5 info＋「約人出街／可約 6 位」；intel_count 28，含 17 pins）；33b＝15（返回地圖＋4 組 tab＋2 sub-tab＋進度＋7 日格；catTabsVisible 0、dayRows 7、intelVisible false、editable false）。

約會端到端（`intel_date` probe）：sheet 開 → 約人出街 → who-picker（h3「約人出街」，6 位女角連 hint 7／5／6／7／6／6，掣「返回」）→ 揀林曉晴 → spot-picker（h3「約林曉晴出街」，7 個地點：星河電視台 $4、獅子山製片 $4、廟街禮品 $20、尖沙咀海傍 $6、淺水灣 $6、啟德機場 $6、金龍茶餐廳 $20；掣「取消」）→ 取消 → 返地點面板，acts 完整（6 個含約人出街）。

**情報站 info act 數目說明**：修後 5 個 info acts（大堂飲茶聽八卦、幫手執漏、打聽電視城規矩、打聽高俊傑搶鏡事、打聽曉晴近況）＋1 約會入口＝6；修前基線 12 個 act＝6 info＋6 約會掣。5(c) 改動只郁 `addRom159DateActs`，info acts 由 `mockAskDefs('cafe_cha')`＋狀態篩選（`enc79HelpAvailable` 幫手執漏、`intel381Available` 情報 act）決定，數目隨狀態浮動，唔係回歸。

**靜態 `<button` 總數：v396 係 110，修後 112（+2）。**帳目：＋2 板下拉掣 toggle（模板）＋1 工具掣＋1 約人 picker 模板行 −1 選單過一日 −1 未開放掣 ＝ +2（`git diff HEAD`：10 行加 `<button`、8 行減）。可見掣數每屏都跌（02b 31→14、11d 29→25、33b 22→15、通告欄 modal 可見掣 6→2、情報站 12→6 acts），靜態數升係因為下拉掣本身係新增嘅靜態／模板掣——唔好齋報 112。

## 測試

- 新增 `tests/test_v397_static.py`（29 個斷言）＋`tests/test_v397_logic.js`（20 個斷言：`boardExpCalc397` 7 項、`dayResLedger397` 8 項、`clampMapLabels397`（fake document stub）5 項）。抽取模式跟 v396（`extractFn` 用 `\n}\n` 搵函數尾；stub 守門：`gigPayExact`／`chance`／`effectiveShootDays` 用替身）。
- 初跑 static 28 過 1 fail、logic 18 過 2 fail，**三處都係測試本身寫錯，code 無錯，已修正**：(1) static「結果卡 sidebar 唔再有 filler-v」fail——我自己加嘅註解入面提到 `.np214-filler-v` 字串；已改斷言查實際元素 `'<p class="np214-filler-v"'`。(2) logic calc 期望計錯數：378×0.863÷4＝**81.5535**（唔係 81.5355）；378×0.865÷4＝**81.7425**（唔係 81.675）。正確算式：378×0.863＝326.214÷4＝81.5535；378×0.865＝326.97÷4＝81.7425。
- 更新釘死舊行為嘅測試（全部係有意圖嘅行為改變）：`test_v396_static.py`（photowrap margin 8px→4px；日結漸變 .18／.58→.10／.42；`setUnderlyingInert` toggle 加 `!scene`；靜態掣數 110→112）、`test_menu72_static.py`（選單刪 rest-early＋分隔線＋handler 分支）、`test_qa101_static.py:54`（new_s 移除過一日）、`test_text108_static.py:92`（S-49 選單項改斷言已刪，地圖金掣保留）、`test_book143_static.py:62`（B1 還原規則跟新選單選擇器）。已核實唔使改：`test_v392_ui_static.py`、`test_dayend202_static.py`、`test_dayend202_logic.js`／`test_dayflow196_logic.js`／`test_flow45_static.py`、`test_book141_static.py:79`、`test_newspaper214_wrap_*`（晨報未郁）、`test_newspaper214_award_*`／`test_awards192／194`、`test_ui128a4`、`test_map159_static.py:135`。
- 直接相關測試逐個重跑全過（v396／v397／menu72／qa101／text108／book143／book141／v392／dayend202／dayflow196＋對應 logic）。

## Resync：`qa397/resync397.py`（總行數 50641→50979，＋v397 +338；其餘釘行按 suite 結果跟進）

注意：今版改動散喺全檔（唔係淨加檔尾），釘行會漂移——resync 用單次掃描 dict 查表（travel114 兩 set）＋逐處 assert 恰好一次，唔好逐對 re.sub（v162 教訓：重疊 pair 會食錨點）。首輪 suite 406／22，13 項新 FAIL 全係 resync 範圍：5 項行為改動（金禧錨點新位 ui108／ui128a1／v155；「還原」搬選單 buttons197 B2／ui128a6 S-20）＋8 項行號漂移（gift185 總行數／tang171 總行數＋DEF／tang173 總行數＋DEF＋lines[5269]／text125 三錨點／tang152 兩釘／rom159 6 釘＋全佳／rom176 6 釘／travel114 FREE＋COUNT＋DEF＋WRAPPER）。resync 後逐個重跑全過，再跑全套：**419 PASS／9 FAIL**（見下）。
- travel114 跟進（首輪後剩 1 項）：rom159 who-picker 新加「返回」掣（45835）＋onDismiss（45836）兩個 `forceRestore` 呼叫點入 FREE_LINES（42→44）；註解行 45810 含 `openLoc(` 字面誤觸呼叫點普查，改寫註解（唔含括號），唔入 FREE_LINES。重複行 7695／7696（衣櫃，後面係 clothing-shop265-list）／48964／48965（禮品店，後面係 gift-shop-list）額外用跟住嗰行核實，冇交叉對錯。
- 註記寫入 .js 檔要用 `//`（v396 教訓：`#` 令 logic 測試 SyntaxError）；逐個重跑嗰陣唔好用 `head -3` 截 FAIL 清單（v396 教訓：rom159／rom176 各漏咗 3 個釘）。今次教訓：`grep -c` 計行唔係計次數（tang173 `lines[5269]` 係 8 次唔係 4 次，resync 腳本第一次跑斷言失敗，已修正重跑）。
- 跑完 suite 還原 `qa296/derive296.json`（suite 會再生，唔入版）。

## 落地

- 常駐 clone 合併前核實 HEAD `e92a457`（v396），v397 空閒。
- 工作副本 `~/workspace/linji-work397`（clone 式，分支 `v397-ui-audit5-top5`），commit：`b866e27`（五項實裝＋新測試）、`095bcdb`（resync）、`4b61e80`（NOTES）。
- 合併：常駐 clone `git fetch <副本路徑> v397-ui-audit5-top5` → `git merge --squash FETCH_HEAD` → commit → push main → curl Pages 核實 byte-identical（https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/）→ 刪工作副本。
- main HEAD（落地後填）：____；Pages 核實（落地後填）：____。
