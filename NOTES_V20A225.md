# NOTES_V20A225 — 對手線強化：高俊傑由「劇情對手」升級做「成日同你鬥嘅對手」

- 基底：main `719975f`（v224「佢」跟進票）；分支 `rival-enhance`；工作副本 `linji-work-rival`。
- **改號**：本票原訂 v223，實裝期間 v221（書面語 P2）＋v223（when-fix）落地，v223 號撞咗，改做 v224；其後「佢」盲點跟進票攞咗 v224（main `719975f`），本票再改做 **v225**。工作副本由 `3e8dfba`（v223）rebase 上 `719975f`，resync 重做（見 §2）。
- 設計稿：`~/workspace/linji-rival-enhance/work/DESIGN.md`（審計＋改動清單＋實裝記錄）。
- 約束：唔改 C3 hard／endure 抉擇本身、唔改 A_ko 三個收尾、唔改決戰門檻 40±6 底數；唔郁攻略（用戶已拍板對手線唔寫入攻略）。

## §1 改動（R1–R6）

### R1 — 手帳對抗狀態行（睇得到）
- 新函數 `rivalryStatusLine()`；`people72Html()` 高俊傑行加 `${rivalryLine}`（`nextLine` 之後）。
- 狀態：`none`（未開決戰，夠分之前講「風聲同報紙愈嚟愈多」）／`open`（講當輪作品＋門檻 40±6＋雙軌即時值）／冷卻（講上次結果＋下一場遊戲日期，`fmtNewspaperDate(nextOpenDay)`）／第 3 輪終態（「三場爭位鬥完，你贏咗 N 場」）。
- 唔顯示 `rivalryScore()` 原始分（佢係開閘進度 0–3，唔係實力分）；render 嗰陣即場重計，唔讀 tick 舊值。

### R2 — 報紙定期快訊（定期出現・報紙）
- 新 `RIVAL_NEWS_SLOTS`（6 則，dayIndex 150／330／510／690／870／1020）＋`rivalryNewsTick()`，掛 `advanceDay()` 喺 `rivalryTick()` 隔籬；帳本 `S.rivalry.newsIdx`。
- 條件：C3 已完成＋到日；每次 tick 最多一則（遲做 C3 唔會一次過補發晒）。
- eventKey `story:C3:rival_news_<n>`（自動接返 `rival:gao` 連載句），source `"story"`，fameDelta 0，**唔傳 rumorEcho**（G1-proof）。
- 作品名虛構：《夜闌燈火》（《長夜燈火》已係 gigs_1989.json 玩家公益客串名，避撞改名）、《望海潮》、《風雨同路》。

### R3 — 試鏡落選後續（定期出現・通告欄迴響）
- 新 `rivalryTookRoleLine(gig, rec)`；`aud91PresentOne()` 落選分支：`presentAudFailSettlement` 嘅 `notesHtml`＋fallback「何生來電」modal 兩邊都加。
- 條件：C3 已完成＋電視劇／電影＋隨機約 1/3 → 手帳閒話一則（`rival_took_<gigId>`，每通告一次）＋文案一句「嗰個位最後畀咗高俊傑。」
- 純 flavor，唔改分數／計分／落選懲罰；決戰通告本身唔計（落選仲可以再報）。

### R4 — 頒獎提名同場對照（定期出現・頒獎）
- `awards62CeremonyBeats()` 夜場 loop：玩家提名格又有高俊傑同場嗰陣，揭曉前加一格 `rival` beat（通用 caption 顯示，唔改卡片／時序；beat 計數測試只數 `nominee`，唔受影響）。
- `renderAwardResultHtml()`：玩家有提名嘅類別入面有高俊傑嗰陣，結果卡加一句同場對照（贏：「你贏咗呢一場」；輸：「獎落 X 手，下年再鬥」）。
- 唔改提名揀選、唔改得主邏輯（`winner63 = fl[0]`）、唔改贏線。

### R5 — 再鬥循環（輸咗唔係完）
- `RIVAL_FACEOFF_GIGS` 加兩則（同形，唔同 title／workTitle／id）：R2 `gig_rival_gao_faceoff_r2`《火線街頭》電影 film_lion；R3 `gig_rival_gao_faceoff_r3`《再見江湖》電視劇 tvb_kowloon。R1 id 唔郁（保舊檔兼容）。三則一律片酬 $1,200、shootBand [1,1]、shootDeadlineDays 14、req {}。
- `RIVAL_CFG` 加 `rematchCooldownDays:90`、`maxRounds:3`。
- `S.rivalry` 加欄：`round`／`gigId`／`nextOpenDay`／`lastResult`／`wins`／`newsIdx`／`workTitle`；`ensureRivalry()` 補齊舊檔＋遷移（第 1／2 輪已結算嘅舊檔轉返 `"none"`＋`nextOpenDay＝settledDay＋90`，等再鬥循環接手；第 3 輪終態唔郁）。
- `rivalryTick()` 狀態機：`none → open` 加冷卻閘（`today >= nextOpenDay`）；開嗰陣第 2／3 輪輪次＋1、換當輪通告、toast 按上次結果換文案；結算邏輯唔變（雙軌、門檻 40±6、贏輸效果）；第 1／2 輪結算後返 `"none"`＋冷卻 90 日，第 3 輪先留 `won`／`lost` 終態。
- `rivalryFaceoffPaper(win, round)`／`rivalryResultRumor(win, round)`：eventKey／傳聞 id 按輪加後綴（R1 唔變保兼容；R2／R3 `_r2`／`_r3`，避開 `newspaperEventSeen` 去重）；標題加「再」。
- `mergeRivalGigs()`：只注入當輪嗰張；唔係 open 就濾走三張；**開緊嗰陣先濾走上一輪殘留通告**（測試捉到嘅 bug，見 §2）。

### R6 — 誠實化修復（審計發現）
- R6a：`rivalryTick()` open 分支嘅 `done_` 後備檢查加排除 `fail_shoot_<gigId>`——`failShootOverdue` 同時寫 `done_` 旗，現行 code 會將逾期掉單當殺青結算。
- R6b：三則決戰通告刪 `applyDeadlineDays:6`——全 repo 無任何 code 執行佢，卡面「仲有 6 日截止」係假話；`shootDeadlineDays:14` 留返（獲聘後真係執行）。

### 刻意保留
- `rivalryFaceoffPaper()` 原有兩則 `rumorEcho` 由語言票（G1）喺 v222 刪走；rebase 嗰陣兩邊改到同一行，解法係留返 main 刪 echo 嗰邊＋rival 動態 `workTitle:work`（第 2／3 輪作品名唔再寫死《霓虹夜影》）。新項目（R2 六則）一律唔傳 rumorEcho。
- 唔改主通告庫（重寫在即）、唔改 C3／A_ko 結局／門檻底數、唔改頒獎得主邏輯、唔用 rumorEcho、唔開新頁、唔郁攻略。

## §2 測試

- `node --check`（抽 2 個 inline script 塊）：PASS。
- 新測試 `tests/test_rival_rematch_logic.js`：19 斷言，全 PASS（再鬥循環三輪、門檻、R6a、舊檔遷移、R2 快訊、R1 狀態行、R3 落選、mergeRivalGigs）。
- 新測試 `tests/test_rival_board_r2.js`：6 斷言，全 PASS（第 2 輪板面見《火線街頭》、舊輪通告已清）。
- **測試捉到嘅真 bug**：`mergeRivalGigs()` 開緊嗰陣唔清上一輪殘留通告——冷卻期內玩家一次都冇開過板，舊嗰張會留喺 GIGS，下一輪開嗰陣兩張決戰通告並存。已修（open 嗰陣先濾走非當輪通告再注入）；測試 `mergeRivalGigs` 一項由 FAIL 轉 PASS 佐證。
- 全套 suite A／B：A（主 clone main `719975f`）**309／13**；B（工作副本）**311／13**（＋2 係兩隻新測試，全過；13 項穩定 pre-existing FAIL 清單一模一樣：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），零回歸。
- 7 檔 tripwire 測試 resync（`qa225/resync225.py` difflib 對位核實純漂移，淨 +272 行：insert 311／delete 39；DEF 57316→57527（＋211）、WRAPPER 45449→45641）：
  - `test_gift185_static.py` 總行數 62860→63132；
  - `test_tang171_static.py`／`test_tang173_static.py` 總行數 62860→63132、DEF 57316→57527；
  - `test_rom176_static.py` 6 錨點（55746→55957、56114→56325、57253→57464、57347→57558；6360／31963 唔郁）；
  - `test_travel114_static.py` 47 錨點（DEF 57527、WRAPPER 45641；COUNT 12／FREE 33 不變）；
  - `test_poster85_static.py` 上限基數 5586915（＋40000 headroom；現行 5,586,915 bytes）；
  - `test_ux68_static.py` 上限 5,630,000 不變（現行 5,586,915 bytes）；
  - `test_gigreq110_logic.js` 池數 469→471（新加兩則決戰通告），跑過 ALL PASS，唔使改。
- **「刪舊」核實**（用戶 2026-11-15 新規則：實裝完成即刪舊設計）：新加 identifier（`RIVAL_NEWS_SLOTS`／`rivalryNewsTick`／`rivalTookRoleLine`／`rivalryStatusLine`／`rivalryGigForRound`／`rematchCooldownDays`／`maxRounds`）全部有呼叫點，零死 code；舊 RIVAL_CFG 頭註解「結算後落 won／lost 終態、唔再重複觸發」一句已改返三輪寫法。殘留：L42282 舊註解「幕前聲量」係 Weave 時期舊註解（唔係玩家面），test_story157 明文容忍舊註解殘留，唔郁，留返語言票決定。
- **rebase 衝突**（`3e8dfba`→`719975f`）：`NOTES_V20A224.md` add/add——留 main 版（「佢」票嗰份；本票 NOTES 另寫呢份）；`index.html` 兩處 content 衝突（`rivalryFaceoffPaper` 勝／負兩則）——留 main 刪 `rumorEcho`＋rival 動態 `workTitle:work`，兩邊改動都保住。其餘測試檔衝突（gift185／rom176／tang171／tang173／travel114）取 main 版再由 resync225 重寫錨點。

## §3 落地

- squash merge：`git merge --squash rival-enhance` → commit `bcb61ab`（`v20a225: 對手線強化——手帳對抗狀態行＋報紙快訊 6 則＋試鏡落選後續＋頒獎提名同場＋再鬥循環 3 輪＋誠實化修復（rebase 上 main 719975f）`）→ `git push origin main`（719975f..bcb61ab）。
- 線上核實：`https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/index.html`，**5,586,915 bytes，sha1 `6fefc891994529d8441f688453d28092d6eca0d1`**，同 `git show HEAD:index.html` 逐 byte 相同。
- NOTES 另一個 commit（呢份）→ push。
- 工作副本 `linji-work-rival`＋pristine `linji-pristine-rival` 已刪。

## §4 殘留／跟進

- 實駕驗證：`qa225/drive225.py`（播種存檔由 C3 行到決戰）——**延期**：瀏覽器已死（Chromium SIGTRAP，自 2026-11-15 08:48 起），等瀏覽器恢復後先跑。drive225 由 drive223 重建，修正三處：P2 快訊 eventKey 係 `rival_news_1`（1-based；drive223 寫 `rival_news_0` 係錯）、P2 標題改查 queue headline、P7 板面檢查以玩家可見文字為準（teaser gid 只作診斷）、P8 改 6 次。
- drive224（07:37）實測：P0–P8 只有 P7-board-r2 FAIL（r2 teaser gid 空；但 P7-rematch-open／P7-old-gig-cleared／P7-r1-round2-line 全部 PASS，game state 無問題；logic test `test_rival_board_r2.js` 亦 ALL PASS）。drive225 重跑嗰陣重點核 P7 係 drive selector 定真問題。
- R6a（掉單唔結算）只由邏輯測試覆蓋（要等 14 日限期＋撞拍攝日告假，live 唔試）。
- L42282 舊註解「幕前聲量」殘留（見 §2，唔郁，等語言票決定）。
