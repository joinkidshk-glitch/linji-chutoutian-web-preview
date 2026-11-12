# NOTES — v20a136：結局閘 C17 由 1992 年 1 月搬去 1992 年 12 月

- 分支：`v20a136`（基底 main `673df0d` v135；落地前 rebase 上 `bcac846` v137）
- 範圍：A. C17 閘＋backstop／B. 1992 年終評核／C. 文案（頒獎禮之後、收科嗰晚）／D. 頒獎邀請流程（拎走「稍後」＋推辭有報紙＋G1 reload 修復）／E. 行為確認
- 禁區遵守：冇合併入 main、冇 push main、冇開 PR、冇用 GitHub connector；冇直改 `content/` JSON；冇郁 SAVE key／softRev／產品 `?v=`。

## A. C17 閘（index.html `STORY_GATE_3Y.C17`）

舊閘 `{ needDone: ["C13"], yearEq: 1992, seasonIn: ["冬"]}`——冬天＝12／1／2 月，1992-01-01 已經開，結局 day ~746。
新閘：

```js
C17: { needDone: ["C13"], weekMin: 153, yearEq: 1992, seasonIn: ["冬"],
awardResolved: { ceremonyId: "award_singho_tv", year: 1992},
backstopDay: 1096}
```

- `weekMin: 153`：1992-12-01＝day 1065＝第 153 週（week 153 首日 day 1064＝1992-11-30 係秋，seasonIn 擋住；12 月 1 日先真正開）。
- `awardResolved`：`evalGate3Y` 加檢查，用 `awardsGetFlag(1992, "award_singho_tv")`；終端狀態 `done`／`skipped` 先算通過，`invited`／`pending`／空字串唔計；defensive try/catch（S／awardsFlags 唔存在當未解決，唔 crash）。check token `awardResolved:1992/award_singho_tv`。grep 核實過 `awardResolved`／`backstopDay` 之前冇撞名。
- `backstopDay: 1096`：`Number(ctx.dayIndex) >= 1096`（1993-01-01）嗰陣直接回 ok，**繞過全部條件**（needDone／weekMin／yearEq／seasonIn／awardResolved／同日 pacing 檢查一併繞過）。1992-12-31 係硬邊界。
- 語義核實：1992 年 1 月嗰場台慶係屆別 1991（`awardsEditionYear`：冬季 1–2 月歸上一年），flag `1991/award_singho_tv` 唔會誤觸 1992 屆條件；12 月嗰場先係屆別 1992。
- 進度頁 `prog71GateItems`：加 `awardResolved:` →「等冬台慶有結果（去現場／旁聽／推辭都計）」；`backstopDay:` 唔顯示（兜底，唔係要求）。其他 token 唔識別會靜默跳過，唔漏工程術語出玩家面。
- `storyGate113Scrub` 加護欄：已有 `S.ending410` 嘅舊檔唔清 C17（舊閘合法收科，結局唔復活、紀錄唔改寫）。
- C13 閘唔郁。

## B. 年終評核（`CONSEQ61_REVIEWS`）

加 `1992: { floor: 155, warnLine: 195, boundaryWeek: 156}`（數字**暫定**，之後按實玩再調整；平衡數字由助手負責）。警告週（152–155）同 `conseq61LegacyMark` 自動跟到。核實過 `calib60YearOfWeek(156)`＝1992。

## C. 文案（全部 index.html inline，唔係 content pack）

### 重要修正：walk 語義（實駕捉到，任務原文講法有誤）

任務原文話玩家面字串「1990」→1992，但 `years66Walk` 載入時將 walked 表格嘅年份 +2（源頭寫舊曆值，walk 推 +2 做 1992）。所以 **walked 表入面玩家面年份源頭必須留 1990（顯示先係 1992）；寫 1992 會顯示 1994**。實駕首跑證實：C17 第一句出「1994 年冬末」、頁首「主線 · 1994冬」。已還原 61 個 token（`STORY_HINT_SOFT` 12、`STORY_SPINE_NODES_1990` 34、`STORY_SPINE_NODE_C17_410` 8、`CHOICE47_NODES` 7），只改引號字串內嘅 1992，註解唔郁；`STORY_SPINE_NODES_1990` 剩低 5 個 1992 全部係 DEV 節點頭註解（N12–N16，準確描述遊戲世界年份，留返）。`eraTag` 係 SKIP_KEY（walk 唔掂），但頁首顯示前 +2，所以 eraTag 源頭同樣留 `era_1990_*`。**唔經 walk 嘅字串（閘表、評核、結局總結 fallback、`endingEveOptions410` note）先至直接寫 1992。**MEMORY.md 入面「『1990』舊字串一併改返 1992」嗰句係任務原文講法，未反映呢個修正，紀錄要跟返呢度。

最終文案狀態（源頭寫法；玩家面顯示＝源頭 +2）：
- 提示表：C15／C14／C12／C16／C13／C17 行年份源頭 1990；C17 playerHint／lockedHint 改做「台慶之後，何生喺後台等你——三年，係時候收科。」／「1990 年冬、台慶之後先到呢一晚。未到就照常跑通告；到咗去星河電視台後台。」（顯示 1992 年冬）；C10 nextHint 源頭「1990 年先有新劇情」。
- C17 節點 `STORY_SPINE_NODE_C17_410`：when／eraTag／setting／synopsis／lockedHint／beats／pacing.when／openConditionsNote 年份源頭 1990（顯示 1992）；成幕改做典禮之後：首句「走廊盡頭仲聽到散場嘅人聲。」；紅地氈句→捲起／未散／「俾人請入去、再俾掌聲送出嚟」；何生「今晚之前」→「散場之前」；流程表句→「今晚全部發生晒喇。剩低要對嘅，唔係流程，係你之後點行。」＋「鏡頭掃過嚟嗰陣，你冇四圍望」；紅星句「陸續入座」→「陸續散場」；尾句「司儀喺台上試最後一次咪」→「台前散場嘅人聲漸漸靜落嚟。」；C17_410_a notes「頒獎禮開場」→「頒獎禮散場」；`pacing.weekMin` 140→153（`storyWeekStamp` 用佢顯示「約第N週」，140 錯，對齊閘 153）、`pacing.when`→1990冬（源頭）。
- **動態重建選項（實駕捉到，任務原文冇列）**：`endingEveOptions410`（唔經 walk，直接顯示）嘅 natural 選項 note「頒獎禮開場」→「頒獎禮散場」；全檔已無「頒獎禮開場」。靜態節點 choices 嘅 notes 改咗都唔夠——播放時選項由 `endingEveOptions410` 動態重建。
- 結局總結 fallback（`endingSummaryHtml410`，唔經 walk，源頭直接寫 1992）：→「未收科——去到 1992 年冬、台慶之後嗰晚，先係埋單嗰陣。」
- C13 節點：when／setting／eraTag／lockedHint／beats／comment／pacing.when／openConditionsNote 年份源頭 1990（pacing.weekMin 144 唔郁——C13 有兩個窗口，冇單一正確週數）。
- `STORY_SPINE_NODES_1990` 區塊其餘 1992 節點（C15／C14／C12／C16）同款還原（源頭 1990）。
- CHOICE47：F4 when／setting／synopsis／beats 年份源頭 1990 夏；G4 同款→1990 冬／1990 年年尾（顯示 1992）。
- Pack 核實：`content/story_detail_c1_to_c17.json` C17 `when: "1992收束 / W105-108"`＋`pacing.weekMin: 105` 唔郁（閘表覆寫開閘條件；靜態測試已釘死）。
- 留返未改（有待另票）：C6–C11 提示表／節點嘅 1989 年（閘係 1991，同一類陳舊字串，但任務明確話唔郁）；R_lan_crisis（1990秋）／R_lan_ending（1990冬，flag-gated、冇年份閘可對照）；CMT_hiu／choi_commit（1990秋，`choice47SeasonReached(1990,"秋")` ≥ 語義，文字同 code 一致）；`era_1990_*` gig／eraTag（CONTRA98 ＋2 映射系統內部標籤）；L30905 年份正規化 code；WF4 傳聞 `yearMin:1990`（正確）。

## D. 頒獎邀請流程（A 方案安全所需）

- 拎走「稍後」掣：`presentAwardInvite` 嘅 modal 按鈕只留「出席」＋「推辭」；`onDismiss` 由 `later` 改做 `skip`（mask 撳＝推辭；掣撳會先清 `_modalDismiss`，唔會重複觸發）。`presentPendingAward` 清走 `_awardSnoozed`／`_awardSnoozeDay` 檢查；`awardsDebugForceSeasonWindow` 嘅 `_awardSnoozed=false` 改做清 `S.pendingAwardPack`；全檔已無 `_awardSnooz` 死碼。L38551 嗰個「稍後」係劇情提示 modal，唔關頒獎事，留返。
- 推辭＝典禮照舉行＋第二日報紙講結果（D1）：`skip()` 入面 `commitAwardToLog(pack)` 照舊（flag `skipped`——終端狀態，C17 條件計佢有結果），之後 `enqueueNewspaperFromAward({...pack, skipped:false}, { declined:true})`（publishDay＝day+1；rewards 保持歸零）。
- **Gallery 桶行 inline**：任務首選係加 `award_gallery` 桶＋模板，但禁區話唔准直改 `content/` JSON；nominee 桶映射被否決——4 隻 nominee 模板固定文案全部寫「入圍／提名」，旁聽寫咗就係假結果。所以桶＋模板注入喺 index.html（沿用 WF1「唔直改 pack、注入」先例），stub 計數（win 8／nominee 4）不變。gallery 用 inline 模板 `NEWSPAPER_AWARD_GALLERY_TEMPLATES_136`（4 隻：film／tv／music／ad，fameDelta 1，文案只寫「阿偉坐喺台下睇完整晚」，唔寫入圍／得獎）。
- **Declined 報紙唔用 bucket 模板**：任務字面話 enqueue `{...pack, skipped:false}` 副本；但 win／nominee／gallery 模板分別寫阿偉奪獎／入圍／坐喺台下，推辭咗嘅人三樣都冇，寫咗就係假結果。所以 declined 行專用路徑：用典禮級 press 文案（`pack.press`，stub pressTemplates 係通用側記，唔寫阿偉贏獎／出席），fameDelta 0，templateEventKey `award_declined.<medium>`。D1 意圖（推辭都有報紙講結果）保留。
- G1 修復（reload 遺失請柬）：(b) 為主——`queueAwardInvite`／`promoteAwardQueue` 將 pending pack 持久化入 `S.pendingAwardPack`（S 係 whole-JSON 序列化，`normalizeSaveObj` 原樣保留未知欄位，舊檔唔使遷移；出席／推辭嗰陣清走）；`restorePendingAward136()` 喺 `queueAwardsOnSeasonWindow` 入面統一呼叫：flag `invited`／`pending` 但 session 冇 pack 嗰陣，優先用 persisted pack 還原，否則用 `buildAwardResultPack` 重建。(a) 後備重建嘅限制：tier／分數由 S 計返係確定性，但入圍類別抽選有 `Math.random`，重建版類別組合可能唔同原版——請柬本身唔會唔見，結果以重建版為準。
- C10 延期已核實（唔使改 code）：`softC10WindowActive()` 每年第 49–52 週、C10 未做完嗰陣 TV 典禮讓路；`queueAwardsOnSeasonWindow` 喺嗰陣 return（唔設 flag、不建 pack），窗口一過／C10 做完就排到——只延後、唔取消。注意 `softC10WindowActive` 讀 `S.flags`（`C10`／`done_C10`／`story_C10`），唔係 `S.story.done`。
- TV 典禮排期（schema）：season 冬，`weekMinSoft: 40`；`awardsSeasonMatches` 用 `calendarSeason()`，`awardsWeekOk` 用絕對週 ≥40。
- 唔入 v136（留返頒獎整改包）：D2 安慰場面、頒獎禮做長做實（3.7 秒問題）、燕尾服／VFX／音樂、M1 場地場景圖。唔做強制預覽／seed 存檔驗贏分支。

## E. 行為確認

播完 C17 即刻結局（C17 → `S.ending410` → `ending78Gate()` 鎖死），唔使等 12 月 31 號。實駕證實。

## 測試

### 新測試（全部喺 work copy PASS；對 pristine main 乾淨 FAIL、exit 1、無 crash）
- `tests/test_story_gate136_logic.js`（29 項）：抽真函數 eval（`evalGate3Y`＋`readCtx`＋`done`＋`gate3YEntry`＋`seasonKeyOf`＋`gatePath`＋`nodeId`＋`storyGate113Scrub`，vm 沙盒，`awardsGetFlag` 假旗標表）。覆蓋：1992-01／1992-11／1992-11-30 唔開；1992-12-01＋旗標空／invited／pending 唔開；done／skipped 開；屆別 1991 done 唔誤觸；backstop day 1096 無條件開（C13 未做、季節唔啱都開）、day 1095 唔開；awardsGetFlag 未定義／throw 唔 crash；C13 照開；scrub 已收科唔清／未收科 week<153 清／week≥153 唔郁；反證。
- `tests/test_conseq61_1992_logic.js`（19 項）：抽 `CONSEQ61_REVIEWS`＋`calib60YearOfWeek`＋`conseq61State`＋`conseq61DualOf`＋`conseq61LegacyMark`＋`conseq61SettleEval`。覆蓋：條目數字、警告週 152–155（dual 150 出聲／200 唔出聲／155 週強警告原文「下週就係 1992 年尾評核」＋dual＋floor 155／150 週唔出聲）、邊界 156（dual 154 收場 pendingEnding review／1992／floor 155＋結算行文「1992 年尾評核結果出咗」；155 過關；210 過關）、舊檔 legacy（1993 標記／1992-12-01 唔標記／已收科標記）、1990／1991 不變、反證。
- `tests/test_gate136_static.py`（39 項）：閘／評估器／評核／文案／邀請／G1／gallery／pack 唔郁。已按 walk 語義改寫 C 節：walked 表斷言源頭 1990、無「1992」（會顯示 1994），加 years66Walk 名單斷言（C17 在列）、`endingEveOptions410` note 係散場、全檔無「頒獎禮開場」；唔經 walk 嘅結局總結 fallback 斷言源頭 1992。
- 舊測試更新：`tests/test_weave410_static.py` 兩處（C17 playerHint「台慶之後」；C17 閘新寫法）；`tests/test_years66_static.py`（L36–37 舊字串斷言更新做新文案／新閘）；`tests/test_weave410_logic.js`（harness 加抽三個 awards 函數；START epoch 改 1990-01-01——舊 harness hardcode 1990-03-07 令 week 短 9；C17 期望補 award flag＋「台慶未有結果 → 唔開」）；`tests/test_weave45_logic.js`（同款＋「1993 冬」期望反轉做 true，backstop 無條件開）；`tests/test_wf1_80_logic.js`（fixture 重生成 `tests/fixtures/spine_c6_c17_v136.json`，v79 檔留檔）；`tests/test_text125_static.py`（行號漂移 +35／+38）；`tests/test_travel114_static.py`（openLoc 呼叫點行號漂移，`qa136/resync_travel114.py` 重寫，COUNT 13／FREE 27 不變）。
- 頁內測試更新（index.html）：`newspaperCheck` gallery 斷言反轉（gallery 而家有報紙，fameDelta 1、templateEventKey `award_gallery.film`、文案唔寫入圍／提名／得獎）＋加 declined 斷言（fameDelta 0、`award_declined.ad`、headline+dek 唔含阿偉）；snooze 測試塊改寫做「有請柬就要彈出、掣只有出席＋推辭、無稍後」。

### 全套
- Baseline（pristine 673df0d）：**PASS 193／FAIL 12**（`qa136/suite_baseline136.txt`）。
- Work（rebase 前）：**PASS 196／FAIL 12**（`qa136/suite_work136.txt`）——FAIL 清單同 baseline 一字不差，零回歸。12 個 pre-existing FAIL：`test_flash51_static.py`、`test_giglib36_static.py`、`test_pacing35_static.py`、`test_poster59_static.py`、`test_rumor49_static.py`、`test_slot50_static.py`、`test_soft_tip_111_restore.py`、`test_start53_static.py`、`test_weave43_static.py`、`test_weave44_static.py`、`test_weave49_static.py`、`test_wrap38_static.py`。
- Rebase 後重跑數字見下文「Rebase」一節。

## 實駕（Playwright；`qa136/drive136.py`，本地鏡像＋`?softPreview=1`）

8 個 case 全部 PASS（932：`qa136/drive136_all_932.json`；play_c17 另有 700：`qa136/drive136_playc17_700.json`）：

| # | case | 結果 |
|---|------|------|
| ① | gate_nov（1992-11-22，week 151，C13 done、台慶未解決） | PASS：閘唔開，reasons 含 `weekMin:153`；進度頁 C17 鎖定、見「等冬台慶有結果」、無播呢幕掣 |
| ① | gate_dec_open（1992-12-05，week 153，台慶未解決） | PASS：閘唔開，reasons 僅 `['awardResolved:1992/award_singho_tv']`；進度頁顯示「1992 年冬」（walk 語義證據） |
| ①③ | play_c17（1992-12-05＋台慶 done；430×932＋430×700） | PASS 11/11：閘開、播 C17，第一句「1992 年冬末，星河電視台頒獎禮後台。化妝鏡一排燈泡熱到出煙，走廊盡頭仲聽到散場嘅人聲。」（含 1992＋散場、無 1994）、頁首「主線 · 1992冬」、對話框唔被切、揀「順其自然」→ `S.ending410` 寫入、C17 done、地圖鎖死。截圖 `qa136/shots/c17_play_430x932.png`、`c17_ending_430x932.png`、`c17_locked_430x932.png` |
| ② | backstop（1993-01-05，day 1100，C13 未做、台慶未解決） | PASS：閘無條件開，reasons 空，listOpen 有 C17 |
| ④ | decline（推辭路徑） | PASS 12/12：請柬彈出（台慶頒獎夜請柬，星河台慶・年度頒獎夜 · 冬 1992，席位：旁聽席）＋掣只有出席／推辭（無稍後）＋推辭後 flag `skipped`＋`S.pendingAwardPack` 清走＋報紙已排（`newspaperQueue` 有 `award:1992:award_singho_tv`）＋翌日報紙有台慶結果（唔寫阿偉得獎／奪獎）＋剪報已錄 |
| ⑤ | reload（G1） | PASS 6/6：請柬彈出＋pack 持久化入 S＋存檔還原（day 1070；撳「繼續」載入嗰陣 pending 週日結算即刻行，1070→1071，係遊戲本身行為）＋reload 後請柬重現（persisted pack 還原）＋無稍後 |
| ⑥ | c10_defer | PASS 8/8：12 月 5 日（年內第 49 週）＋C10 未做 → 無請柬、flag 仍空、無 pending pack；1 月 5 日（年內第 2 週）→ 請柬出現、屆別 1992 |
| ⑦ | review（1992 年終評核） | PASS 9/9：seed Dec 20＝week 155 尾日，dual 32 → 過一日結算 week 155 強警告「下週就係 1992 年尾評核…（155）」→ 行 7 日到 Dec 28 結算 week 156：`reviews[1992]={dual:33, floor:155, passed:false}`＋評核場面＋提早收科總結（未紅先收 review1992版）出現。實駕行入咗 E7 強制收場（`S.ending410` 寫入）——係 pump 行完強制收場呈現嘅副作用；本 case 斷言數字同警告行為，唔係以收咗差結局當 PASS |

### 實駕期間捉到嘅 drive／遊戲行為（已處理，唔係產品改動）
- 播種：開新遊戲→跳過教學→返地圖後 evaluate 直接改 S；`saveQ()` 唔係 global，drive 用 evaluate 直接寫 localStorage 做 reload seed（效果一樣）。
- 地圖掣係 `[data-loc="..."]` 按鈕；`#loc-close`「返回地圖」只係 `closeSheet`，唔行晨鏈；頒獎請柬鏈要經「過一日」→確認 modal→「小休」modal→「返回地圖」→`goToMapForBrowse` 先觸發。
- 晨鏈後地圖主掣變「開始今日行程」（「過一日」收喺計劃表入面）；週日結算後入屋企畫面（`enterHome`），要撳「確定本週行程」開週，晨鏈（報紙／請柬）喺開週前彈出。drive 嘅 `advance_day`／pump 已跟呢個流程。
- 推辭後晨鏈可能自動播其他待播劇情（例：1990 春「啟德送芬姐」WF4 送別戲——seed 嘅新遊戲 S.wf4 未做，日子一跳就逾期觸發）；drive seed 加 `S.wf4.fenFarewellDone=true`＋PRE_C17 全做（1992 年尾存檔理應已發生／已做晒），免自動播放鏈擋路。
- 抉擇唔喺 `#modal-btns`，係 `<button class="sp-choice">`。

### 實駕發現、未修（pre-existing，唔入 v136，另開票）
- **週結算 flavor 正常流程唔顯示**：`settleWeek` 生成嘅評核警告／「1992 年尾評核結果出咗」行文只寫入 `S.weekBoundary105.html`＋回傳 summary；`enterHome` 唔再 render summary（註解明言「本函數唔再用佢做展示」），日結 modal（`afterDayModal`／`presentRestSleepDayEnd`）亦唔 render——正常唔 reload 嘅流程，玩家見唔到呢啲行文；只得 reload 續玩嗰陣 `week105Pending()` 先補呈現（modal「回家結算 · 第 N 週」）。1990／1991 警告一樣受影響，唔係 v136 引入。Drive 驗警告／結算行文係經 `S.weekBoundary105.html` 快照＋單元測試直接驗 `conseq61SettleEval` 回傳 lines；數字同收場路徑實駕已驗。
- 巧遇攔截間歇性靜默吞點擊（pre-existing，v126 一樣），要設計決定先修。

## Rebase（落地統籌續，2026-11-12 23:0x–翌日 00:xx）

- 落地前 main 由 `673df0d` 行前到 `bcac846`（v137 地圖 cover 放大＋NOTES）。本分支 rebase 上 `bcac846`（commit `c35f620`），`index.html` 自動合併；衝突只得兩檔行號測試：`tests/test_text125_static.py`（實測重對：currentLine 27606／advance 27719／applyFamilySafe 33320）同 `tests/test_travel114_static.py`（`qa136/resync_travel114.py` 以 `origin/main` 做 OLD 重算：44 個 openLoc( 呼叫點序列逐字一致、內容逐行相同，純漂移，COUNT 13／FREE 27 不變；DEF_LINE 53228／WRAPPER_LINE 43921）。
- Rebase 後重跑：全套 **PASS 197／FAIL 12**（`qa136/suite_work136_rebased.txt`；多咗 1 PASS 係 v137 新測試 `test_ui137_map_static.py`；FAIL 清單同 baseline 一字不差，零回歸）＋ drive 932 **8/8 PASS**（`qa136/drive136_all_932_rebased.json`）＋ play_c17 700 **1/1 PASS**（`qa136/drive136_playc17_700_rebased.json`）。
- v137 改咗 `index.html`（地圖區 129 行）、`tests/test_text125_static.py`、`tests/test_travel114_static.py`（兩檔 v136 都有郁，rebase 嗰陣要對位合併）。

### 落地前連續三輪 rebase（main 當晚連續落地 v141／v144／v143／v134）
- **v141（`4832b85`）**：`index.html` 自動合併；衝突 `test_text125_static.py`（手工重對實量數：currentLine 27666／advance 27779／applyFamilySafe b.text 33380）＋`test_travel114_static.py`（`qa136/resync_travel114.py --apply` 重算：DEF_LINE 53290／WRAPPER_LINE 43983）。重驗：全套 baseline **196／12**、work **199／12**（＋3 係 v136 新測試；FAIL 清單一字不差，零回歸；`qa136/suite_baseline141.txt`／`suite_work136_v141.txt`）。
- **v144（`a1b0920`，巧遇收緊）**：衝突只得 `test_travel114_static.py`（取 main 版＋resync 重算）。重驗：baseline **200／12**、work **201／12**（FAIL 清單一字不差；`qa136/suite_baseline144.txt`／`suite_work136_v144.txt`）。
- **v143（`632e371`，手帳內臟紙面化）**：衝突 `test_travel114_static.py`（取 main 版＋resync：DEF_LINE 53341／WRAPPER_LINE 44026）＋`test_text125_static.py`（取 main 版＋實測重對：currentLine 27709／advance 27822／applyFamilySafe 33423）。重驗：baseline **200／12**、work **203／12**（FAIL 清單一字不差；`qa136/suite_baseline143.txt`／`suite_work136_v143.txt`）＋ drive 932 **8/8 PASS**（`qa136/drive_v143_932.log`）＋ play_c17 700 **1/1 PASS**。
- **v134（`646e16f`，WF4 灰底）**：衝突只得 `test_travel114_static.py`（取 main 版＋resync：DEF_LINE 53369／WRAPPER_LINE 44054；`test_text125_static.py` 唔受影響——v134 插入點 40350 行喺佢三個錨點之後，實測 PASS）。重驗：見「落地前最終重驗」。
- 教訓：`git fetch <path>` 唔會更新 `origin/main`，要用 `git fetch origin`（remote 名）先更新追蹤分支；`git rebase --continue` 喺 dumb terminal 要 `GIT_EDITOR=true`。

### 182／29 假回歸（v141 基底首跑，後證實係環境干擾，唔係 code 回歸）
首跑工作套裝出 **182 PASS／29 FAIL**（多 17 個 static.py FAIL）。逐項排除：17 檔逐檔獨立跑全部 PASS；py-only 全跑 **107／12**（淨 12 個 pre-existing）；js 全跑 92／0 後再跑 17 檔全部 PASS；clean 重跑全套 **199／12**、FAIL 清單同 baseline 一字不差。結論：首跑嗰陣同一個被 SIGTERM kill 咗嘅舊套裝行程重疊（orphan／CPU 爭用），17 個失敗唔可重現，唔係 v136 回歸。證據檔 `qa136/suite_work136_v141.txt`（首跑）vs 重跑同一檔名覆寫後 199／12。

### drive harness 修正（`qa136/drive136.py`，測試工具，唔係遊戲 code）
- 根源：`dismiss_once` 用 `btn.click(timeout=1000)` 撳 `#modal-btns` 首掣；掣一撳 modal 即關、元素 detach，click() 擲錯 → 回 False → `pump_to_map` 誤撳「返回地圖」走人，未開週就返地圖，之後流程卡住。v141 基底全跑 reload＋review 兩 case 因此 FAIL（reload：請柬 pack 在 S 但 modal 唔再彈；review：day 停喺 1085，行唔到 week 156 邊界）。
- 診斷：`qa136/probe_settle.py` 逐步 dump 證實遊戲流程本身正確（撳「回家結算」→入屋企→「確定本週行程」→返地圖）；單獨重跑 reload／review 各自 PASS。修正：click 發出咗就算成功（detach 錯當成功，唔回 False），「返回地圖」後備只喺搵唔到掣嗰陣先行。修正後 v143 基底全跑 **8/8 一次過**。
- 另：runtime 中途重啟過一次，打斷咗 v143 基底套裝重跑（baseline 跑到 89 行）；重跑後無損，數字如上。

## 落地前最終重驗（基底 `646e16f` v134）

- 全套：baseline **201／12**、work **204／12**（＋3 係 v136 新測試；FAIL 清單一字不差，零回歸；`qa136/suite_baseline134.txt`／`qa136/suite_work136_v134.txt`）。
- 實駕：drive 932 **8/8 PASS**（`qa136/drive_v134_932.log`）＋ play_c17 700 **1/1 PASS**。
- Code 抽查（rebase 後最終版）：C17 閘 `{ needDone: ["C13"], weekMin: 153, yearEq: 1992, seasonIn: ["冬"], awardResolved: { ceremonyId: "award_singho_tv", year: 1992 }, backstopDay: 1096 }`；`CONSEQ61_REVIEWS` 1992 `{ floor: 155, warnLine: 195, boundaryWeek: 156 }`；全檔無「頒獎禮開場」（0 宗）、「頒獎禮散場」3 處；`awardSnooz` 死碼 0 宗；`S.pendingAwardPack` 持久化在位；SAVE key `starVolunteer_map_v19w`、softRev s107、產品 `?v=v20a10` 無改動。
- 落地 main commit：（待填）
- 線上核實：（待填）

## 檔案

- 改：`index.html`、`tests/test_text125_static.py`、`tests/test_travel114_static.py`、`tests/test_weave410_logic.js`、`tests/test_weave410_static.py`、`tests/test_weave45_logic.js`、`tests/test_wf1_80_logic.js`、`tests/test_years66_static.py`、`tests/test_conseq61_1992_logic.js`
- 新：`tests/test_story_gate136_logic.js`、`tests/test_gate136_static.py`、`tests/fixtures/spine_c6_c17_v136.json`、`qa136/`（`drive136.py`、`resync_travel114.py`、`gen_fixture136.js`、`suite_baseline136.txt`、`suite_work136.txt`、`drive136_*.json`、`shots/`）
- 清理：debug 腳本 `qa136/dbg_*.py`、`qa136/probe_out.txt` 已刪；`tests/dbg410_tmp.js` 已刪。
