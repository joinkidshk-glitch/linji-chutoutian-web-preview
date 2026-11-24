# NOTES_V20A396_UI_AUDIT4_TOP5.md — 第四輪 UI 檢視頭五項必修（v396）

- 版本號更正：brief 原寫 v393，但 main 落手嗰陣已經係 v394（`3c77fba`，E0 floor 豁免），v393 已俾結局修復票用咗（`171f9c3`）；其後 v395（`9eaadfd`，mini-game prototype）落地。呢版改號 **v396**，工作副本 `~/workspace/linji-work396`，分支 `v396-ui-audit4-top5`。合併前已 rebase 上最新 main HEAD `9eaadfd`，clean——v395 改動（獨立 `minigame395.js`＋afterDayRes 鉤子＋`?minigame` 入口）同呢版改嘅檔案區域無重疊。
- 依據：`~/workspace/linji-ui-audit-2026-11-24c/REPORT.md` §5（GPT A 0／B 2／C 82，有效 82 屏 A 0／B 2／C 80；Gemini 參考）。
- Suite 基線：v395 **415 PASS／9 FAIL**（九項 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。
- 實駕：Playwright harness（venv `pwenv49`，headless shell，本地 CONNECT 中繼 127.0.0.1:18081，390×844 dsf 2）；driver `qa396/drive396.py`，結果 `qa396/verify/*.json`，截圖 `qa396/shots/`。

## ① 35c 頒獎結果卡：390px 下正文改單欄

- 機制更正（實駕量度，唔係 GPT 兩次都未能確認嘅「兩欄字形互疊／右緣截斷一半」）：欄太窄致逐字斷行＋「第二版 →」掣區遮正文＋何生引文下半截被截。對比度全部合格（最低 5.82:1、內文 11.49:1）都救唔返。
- 修法（`renderAwardResultHtml`，只限結果卡加 `awd-result396` class，晨報唔郁）：① body2 單欄、用足內寬 ② 相片＋圖說綁成一組放導語後，取消正文繞排 ③ 小檔案搬去第二版（抽成共用 `factboxHtml214`，全闊格），同屆提名排喺主文之後，縮短第一版 ④ 「第二版 →」放文章末尾、隨正文捲動；「收下這晚」留喺獨立底欄。
- 實測（`awards35c396.json`，live 流程：請柬→預約→ceremonyDay 翌晚 `playEvening213`→跳過→結果卡；outcome 入圍（街招年賞），1 個類別）：
- 修前：2 欄；導語 16 行、行闊 57／29.5／27.5px（2–3 字／行）；rep 行 3 行、最窄 14px（1 字）；weak 18 行；引文 6 行；sticky switchrow y 691–741，遮引文底部 32.5px；小檔案喺第一版；miScrollH 1042 vs miH 629。
- 修後：**1 欄**；導語 **5 行、行闊 144／274px、最窄 84px**；rep 行 **1 行**（126px）；weak **3 行**；引文 **1 行**（273px，捲到底完全露出）；同屆提名 **2 行**；switchrow **static**（y 1079.7–1129.7，喺文末、唔遮任何正文）；**小檔案喺第二版**（factboxOnP2 true）；miScrollH 1071 vs miH 629（捲到最後一行完整露出，lastP bottom 547.1 ＜ miBottom 753）。
- 截圖：`qa396/shots/35c_top_396.png`（全闊導語＋240px 相片塊＋圖說，收下這晚喺底欄）、`35c_bottom_396.png`（引文一行完整露出，第二版掣喺文末）。
- 設計圖 `gemini/design_result35c.png` 係方向參考，唔係成品：圖中阿偉拎獎座係錯（呢次只入圍未得獎）；正文 AI 亂碼句、「彭少祺」杜撰對白無採用。
- 約束不變：`tests/test_newspaper214_award_static.py`（R05–R08：`np214-body2`／`np214-sidebar`／`np214AwardPhoto214`／`np214-photowrap`／兩版 `data-np214-page`／`np214-factbox`）同 `test_awards186／192_logic.js`（「同屆提名」×1、fellows ×1、各類別標籤 ×1、fellows 行喺兩類別標籤之後）全部保留，直接重跑 PASS。

## ② 通告欄峰值：長標題撞圖釘＋排序透明化

- **「長標題撞圖釘」係已證實嘅非 bug，無為佢改 code**（三重獨立量度）：
1. Live Range 字形 rect（唔係元素盒）：17 張卡最長標題「電視城接待處特約演員」字尾 x=201，圖釘左緣 327.6，**最小間距 126.6px**。
2. Audit 自身 `shots/09b_board_peak.png` 像素量度：標題字最右 ≈199，圖釘左緣 ≈337，間距 **138px**。
3. `shots/09_board.png`（780×1688）：圖釘紅色筆劃 x 673–699，標題字最右 209–401，間距 **272–466px**。
標題隔籬紅色嘢係「推介」標籤（實心深紅塊，標題行一部分），唔係圖釘——已睇 `/tmp/crop09_card2.png` crop 確認。結構上唔可能撞：`.gt-title` padding-right 52px＋卡 padding 14px，對圖釘 36px，任何標題長度都有 ≥30px 間距。
- 實改（功能分層唔郁：第一眼 5 張、推介置頂）：
- (b) Meta 行：排序＝預期日薪且卡可接嗰陣，片酬段改出「預期 $X／日」（`board392ExpDaily`＝片酬×成功率÷日數；全部參照 `typeof` 守門，test sandbox 無 `board392ExpDaily`／`_boardSort392` 都唔爆）。
- (e) Pill：媒介（`gigTypeCoarse`，同篩選同一口徑）行先、genre 行後（唔同先出兩粒）：電視城長劇而家出「電視劇」「劇情」。
- (c) Lead 行：排序＝預期日薪嗰陣，一行換做「不耗日 · 預期日薪＝片酬×成功率÷日數 · 推介置頂。」（唔加行，第一眼仍 5 張）。
- (d) 總數行：篩選生效嗰陣出「顯示 X／總數」，否則原句。
- 實測（`board396.json`，高數值 seed；`lockedboard396.json`，開局數值）：
- 峰值：count **24**（7 掣：3 排序＋3 篩選＋1 返去地點；17 張卡 div；pins 0）；lead 如上、一行；第一眼 **5 張全見＋第 6 張露 15px**；meta「預期 $82／日｜4 日｜86%」（冬日鄰里情 378×≈0.87÷4）、「預期 $81／日｜3 日｜86%」（電視城接待處）；標題／圖釘間距不變（最小 126.6px）。
- 轉總片酬排序：meta 變返「片酬 $378｜4 日｜86%」；電視劇篩選：總數「顯示 11／17 張（可接 11 · 未達標 0）」，n=11，count 18（11 卡＋7 chrome）。
- **前景掣計數 24 vs 25 破案**：24＝17 卡＋3 排序＋3 篩選＋1 返去地點（全可接板，無鎖定 `<summary>`）；25＝24＋1 個鎖定 `<summary>`。鎖定板 live 驗證（開局數值：演技 18／台風 14／歌藝 14／外貌 22／魅力 16／智商 20／體能 75）：共 17 張 · 可接 11 張 · 未達標 6 張，count **25**（7 button＋17 div＋1 summary），summary「未達標／長遠目標（6 張）最接近：今夜歡笑（差 1）」，推介卡變咗一屋人。Audit 嘅 25 係有鎖定通告嗰陣數，唔係漏咗掣。
- 截圖：`board_peak_396.png`（峰值）、`board_filtered_396.png`（篩選後）、`board_locked_396.png`（鎖定板）。

## ③ 40／27／86 家族：視覺殘留＋補驗兩項 live 測試

- 修法（`presentStartScheduleConfirm45`）：開卡後 body 加 `day-res-open`、mask 加 `day-res`（底部貼底＋淺漸變遮罩，同日結卡同一套；`closeModal` 已清兩 class；取消返休息卡嗰條路經 `presentRestSleepDayEnd` 重新加上）。
- 日期標示（新 helper `settledDateObj396`／`fmtShortDate396`／`dayResDateLine396`，近 `fmtDate`）：卡出嗰陣 dayIndex 已經係下一日，`fmtDate()` 係下一日嘅日期——結算日＝displayDateObj() 減一日（Date 減一日，跨月／跨年都啱；有傳入 `dayDone`（tickDay 之前捉嘅結算日全字串）就優先用佢）。三處：`presentRestSleepDayEnd`（標籤「結算」）、`afterDayModal`（「完成日」，用 `opts.dayDone`）、`afterDayRes`（「完成日」，用 `dayDone`）。格式「結算：1月18日（四） · 下一日：1月19日（五）行程」。已核實全部呼叫點都係 tickDay 之後（休息呼叫點先計 `wd` 再 `tickDay` 再出卡；病倒路 L18825 tickDay 之前捉 dayDone；訓練路 L47192 tick 後先 call afterDayModal）。無測試釘 dayLine 舊寫法（「而家」只喺 fixture）；`test_dayend202_static.py` 釘嘅 `<h3>開始今日行程？</h3>`／`返回休息卡`／`if(goCancel) btns45.push`／後果字串全部保留。
- **關鍵發現——日結淺遮罩之前從未生效**：`body.day-res-open #mask.day-res` 嘅漸變一直被 `#mask.on{ background: rgba(0,0,0,.72)!important;}` 蓋住（`!important` 贏 specificity）。實駕量度：日結卡同 40 號卡背景都係 flat `rgba(0,0,0,0.72)`，backgroundImage none——所謂「淺遮罩」得個名。呢版補返 `!important`，漸變先真係生效。呢個先係「遮罩過暗」嘅真正成因。
- 實測（`rest40_396.json`／`dismiss396.json`）：
- 修前：40 modal mask「mask on」（plain.72），modal y 617.1–834；休息卡 dateLine「1990年1月19日（五）· 第3週」（下一日，易誤會）；D1 週結：休息（週日）vs「1990年1月22日（一）· 第4週」。
- 修後：40 modal maskCls「mask on day-res」、bodyCls「day-res-open」、背景 **`linear-gradient(rgba(0,0,0,0.18) 0px, rgba(0,0,0,0.18) 48px, rgba(0,0,0,0.58) 48px)`**（休息卡同款，一齊生效）；modal y 615.8、h 218.2、bottom 834（貼底）；休息卡 dateLine「**結算：1月18日（四） · 下一日：1月19日（五）行程**」；D1「**結算：1月21日（日） · 下一日：1月22日（一）行程**」；D2 訓練卡「**完成日：1月18日（四） · 下一日：1月19日（五）行程**」。
- 撳外面 live 測試（之前只做 code 核實，今次 live 補驗）：D1 週結休息卡撳外面 → day 21 不變、view v-home、mask 關；D2 afterDayModal 訓練卡撳外面 → day 18 不變、view v-map、mask 關；等 1.5s 後 day 仍 18、無自動推進。功能本身之前已經啱，今次 live 證實。
- 截圖：`40_start_day_396.png`（底部 cream 卡＋深色 backdrop，見下註）。
- 殘留（下一輪）：GPT 專項建議嘅文案微調（「連續過週日」→更直白寫法）唔喺 parent 任務文字入面，今版唔做。
- 附註：40 modal 之前已經貼底（修前 y 617.1 vs 修後 615.8），可見差別只係遮罩漸變。另外因為第 5 項將地圖層 `display:none`，modal 背後係深色 `#app` 殼——bottom sheet 配深色 backdrop 係正常做法，漸變頂部.18 無地圖可透，backdrop 讀做平實深色，唔係問題。

## ④ 重截兩張內容錯誤嘅截圖：24_menu、17_ledger（無 code 改動）

- 正確重截：`qa396/shots/retake_24_menu_396.png`、`qa396/shots/retake_17_ledger_396.png`（唔覆蓋 audit `shots/` 原檔）。
- 方法（寫入 NOTES，等下一輪截圖工人跟）：
- 24_menu：`#btn-menu` 開嘅係 `#menu` 下拉面板（`#menu.on`，6 掣：過一日／重看教學／設定／存檔／讀檔／新遊戲），唔係 modal——probe 最初查 mask 係錯嘅，要查 `#menu.on`＋可見掣先影。截圖已目驗（地圖上嘅下拉單）。
- 17_ledger：屋企手帳（`#book389-handle`）→ 帳本 group tab → `#htab-ledger`（帳目 sub-tab）→ `#ledger-list` 可見，記數簿＋統計，存款 $9,000。
- **截圖工人要核實內容先影，唔好再靠檔名假設內容**（今次兩張錯檔都係檔名假設所致）。
- After 驗證（`menuledger396.json`）：menuOn true、menuVisible true、6 掣齊；ledger htab「帳目」、visible true。
- 重截無發現本身畫面有新問題，無擴大範圍。

## ⑤ Modal 開住時卸載背景地圖互動層（掣量頭號）

- **更正——第一版實裝用 `visibility:hidden`，計數完全唔跌**：COUNT_JS 計有非 null `offsetParent`＋rect＞0 嘅元素，`visibility:hidden` 元素兩樣都有。改做 `display:none`（`#app.ui-hide-under396 #v-map／#v-home／#v-start／#loc-sheet／#menubar／.menu／#btn-confirm-plan { display:none!important;}`）。地圖捲動位置由現有 `preserveMapScroll`／`restoreMapScroll`（`modal()`／`closeModal()` 呼叫）保存／還原，DOM 唔拆，關窗即刻返嚟。
- JS（`setUnderlyingInert`，~L21716）：`app.classList.toggle("ui-hide-under396",!!(on &&!tut))`。教學豁免：`tut-on` 係 `showTutCard` 經 `setTutMask` 喺 `modal()` 之前加落 #mask，檢查穩陣；toggle 寫法亦令教學中途開始嗰陣除返個 class。`display:none` 唔可以由子孫 override，所以舊嘅 `.tut-spotlight-target{visibility:visible}` 束帶已刪——JS toggle 係唯一保護。`closeModal()` 每條關窗路都 call `setUnderlyingInert(false)`。
- 晨報 modal 經 `modal(..., {paperSheet:true})` → `setUnderlyingInert(true)` → `#v-home`（手帳）自動收起——覆蓋「晨報收起手帳（−22）」。
- 禮品／買衫單一購買：行由 `<button class="act" data-buy／data-buy265>` 改做 `<div class="act"...>`（無 role=button、無 tabindex——COUNT_JS 計 button／[role=button]／[tabindex]，plain div 跌出計數）；撳行＝揀中（金框 `act-sel396`，同 `.act.act-priority` 同款式；cost 格「揀」→「已揀」）；底部一個「購買」掣（`role:"p"`、`cls:"shop-buy396"`、`stay:true`——`modal()` 支援 stay：call `b.on(btn)` 唔關窗），標籤跟揀中更新做「購買「名」」；無揀中就 toast「請先揀一件禮物／衫」，modal 留開。買流程不變：`confirmChoice236` → `GiftShop.buyItem(shopId, id)`／`buyCostume265(id)` → 重開商店。`openGiftPick`（送禮揀人畫面）唔喺範圍。
- A11y 取捨（記低）：商店行變咗滑鼠／觸控專用，購買／關閉仍可鍵盤操作。鍵盤用戶要逐行買衫／禮品會多一步（揀行→撳購買），換嚟掣量大跌，下一輪如要補鍵盤支援可加 `tabindex`＋Enter 揀中（但會加返計數，要同 audit 計法一齊諗）。
- 實測：
- 通告欄：修前 count **46**（29 button＋17 卡 div；背景 22：17 pins＋5 地圖 chrome；前景 24）；修後 **24**（7 button＋17 div；pins 0）。`modalbg396.json`：board_count 24、appCls「mask-up ui-inert ui-hide-under396」、pinRect 0,0,0,0、visible false、pinAtPoint「mask」。真滑鼠撳 pin 原位（218,198，開 modal 之前捉，因為隱藏咗嘅 pin 無 rect）：modal 留開、h3 通告欄、day 1、無開地點；關窗後 appCls「」、inert false、地圖 count 27（17 pins）、pin 恢復可用。
- 禮品店：修前 **37**（14 買行＋關閉在前景）；修後 **2**（購買＋關閉），14 行全部 DIV。買流程 live：菠蘿油＋奶茶券 $12 → 購買掣標籤「購買「菠蘿油＋奶茶券」」→ reconfirm 確認選擇 → 錢 9000→8988、商店重開、行餘 3→2、庫存有 `gift_pineapple_bun_set`。
- 買衫店：修前 **33**（10 已啟用買行＋關閉在前景；12 行共，2 行鎖定）；修後 **2**，12 行全部 DIV。買流程 live：c1 $120 → 錢 8988→8868、行變「已擁有」。無揀中撳購買 → toast、modal 留開（mask on、h3 廟街禮品檔）。
- 保留：排序／篩選 6 粒（解決咗上一輪「無篩選」問題）；通告卡逐張可撳、地圖 pin、日期格無刪。
- 靜態 `<button` 總數：v392 係 **112**，v396 係 **110**（−2：兩間商店嘅行模板各一個字串，由 button 轉 div；每間得一個模板字串，所以靜態只減 2；實駕掣數禮品 37→2、買衫 33→2 先係真跌幅）。
- 約束不變：costume265（`"confirmChoice236({"`＋`"buyCostume265(id)"`、`"未合要求："`、`"已擁有"`、`"鎖住"`）、reconfirm236（`confirmChoice236({`＋`GiftShop.buyItem(shopId, id)`）、gift185（openGiftShop 唔用 `<span class="gift-pick-name">`）全部保留，直接重跑 PASS。

## 測試

- 新增 `tests/test_v396_static.py`（43 項）＋`tests/test_v396_logic.js`（23 項），全部 PASS。Logic 抽 `board392ExpDaily`（stub gigPayExact／chance／effectiveShootDays）同三個日結日期函數（stub displayDateObj）eval：exp 378×0.87÷4＝82.215→82、一屋人 259×0.66÷3＝56.98→57、跨月（2月1日→1月31日）／跨年（1991-01-01→1990-12-31）結算日都啱。
- 受影響舊測試逐個直接重跑：guidance34、r335、costume265、reconfirm236、newspaper214、awards186／192、dayend202 全部 PASS；gift185 只係釘死總行數 50512→50641（見 resync）。
- Resync：`qa396/resync396.py`（總行數 50512→50641，＋v396 +129；其餘釘行按 suite 結果跟進）。注意：今版改動散喺全檔（唔係淨加檔尾），釘行會漂移——resync 用單次掃描 dict 查表（travel114 兩 set）＋逐處 assert 恰好一次，唔好逐對 re.sub（v162 教訓：重疊 pair 會食錨點）。首輪 suite 401／25，16 項新 FAIL 全係 resync 範圍：8 份 logic 測試抽出嘅函數 call 新 helper（ReferenceError，要一併抽三個 helper 入沙盒）＋8 份 static 釘行漂移（總行數鏈／line_has／line()／lines[]／FREE＋COUNT set）。resync 後逐個重跑全過，再跑全套：**417 PASS／9 FAIL**（見下）。教訓：resync 註記寫入 .js 檔要用 `//`（第一版用 `#` 令 8 份 logic 測試 SyntaxError，已修）；逐個重跑嗰陣唔好用 `head -3` 截 FAIL 清單（rom159／rom176 各漏咗 3 個釘）。
- 全套 suite：**417 PASS／9 FAIL**（`~/workspace/suite396_out2.txt`；基線 v395 415／9，＋2 項新 v396 測試全部 PASS；9 項 FAIL 全部係已知 pre-existing：flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38）。跑完已還原 `qa296/derive296.json`（suite 會再生，唔係 source）。

## 雜項

- 語法檢查：index.html 兩個 `<script>` 塊 `new Function` parse OK。
- `qa396/dbg_*.py`（dbg_pin／dbg_pin2／dbg_pin3／dbg_awd／dbg_40／dbg_locked_board）係 scratch，已刪，唔入版。`qa396/`（driver＋verify JSON＋shots）留喺 repo，同 v395（`qa395/drive395.py`＋shots）一致。
- 40 modal 嘅 dbg 腳本（`dbg_40.py`）行程流程寫錯（無用 drive396 嘅 `run_day_to_card`／`seed_day`），到唔到 40 modal——腳本問題，唔係遊戲問題；已刪，唔好照抄。
- Probe 經驗：`play_out_story` 一定要用 modal-scoped click（document-wide `click_any` 會撳到故事 modal 背後地圖嘅「返回地圖」掣，loop 120 次）；`wait_for_function` 箭頭函數字串喺呢個 Playwright build 唔穩，用 `ev()` 輪詢；一個 process 第二個 probe 經常喺 `new_game` 嘅 S-wait timeout——每個 probe 獨立跑；dismiss probe D2 唔好 reload（單線 http.server 會 stall 第二次 goto），原地 `seed_day` reset。
