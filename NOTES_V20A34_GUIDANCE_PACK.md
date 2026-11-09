# NOTES V20A34 — 引導包：早期引導修復（試玩報告 P0-1／P0-3／P0-4／P0-5／P1-1）

版本：v20a34（soft 預覽；SAVE key／softRev／?v= 不變；content pack JSON 冇郁）
範圍：跟 `linji-playtest-guidance-report-2026-11-09.md` 嘅修復次序（用戶拍板：先引導包、後節奏包）。
**總原則：只改呈現層——冇改任何數值、門檻、系統邏輯、存檔結構。** 全部新文字嘅數字都嚟自真碼既有計法。

## 1. P0-1 通告卡顯示差額

- 新增 `gigGapBits34／gigGapTotal34／gigGapLine34`：差額計法同詳情頁（`castingNoticeDetailHtml` 嘅「差幾多達標」＋`gigLockReasonLine`）**同一套**——聲望行 `fameFloor(g)` 對 `S.fame`；其餘逐項 `g.req` 對 `S[k]`，標籤用 `STAT_LABEL`（聲望行跟 `gigLockReasonLine` 慣例寫「聲望」）。只列未達項，格式「欠：聲望 13／演技 12／智商 5」。
- 通告板短卡 `gigBoardTeaserHtml`：`boardState==="locked"` 先加一行 `.gt-gap`；齊條件（ready）卡唔加任何字。`gigCardHtml`（拍攝簿／未能試鏡彈窗用）鎖定 rate 行同步加差額行。
- 「最接近」標記有做：`doScout` 計全板鎖定卡入面差額總和（`gigGapTotal34`）最少嗰張（>0 先算），經 `opts.closest` 傳入短卡加 `.gt-closest` 標記。**只標記，冇改 `shown` 排序**（靜態測試釘住）。
- 邊界：若鎖因唔係能力／聲望（選角標籤／信用／逾期債閘），差額列會係空——呢啲卡維持舊樣（只有「暫未能報」標籤），詳情頁本身都冇列呢類差額，唔另作一套。

## 2. P0-3 引導死路修正

死因：C2 底欄 remain 將「未聽聞『電視城廠景生存守則』」同播幕地點「到星河電視台或金龍茶餐廳」並列，玩家誤讀做去電視台聽守則——但打聽行動只有茶餐廳同事務所有。

- 新增 `BehaviorGate.rumorHearHint(rid, full)`：由 `MOCK_ASK` 邊啲行動 `grantsRumorId===rid` **反推**地點＋行動名（唔手寫對照表，日後加新打聽點自動跟）。電視城守則只會得出：茶餐廳「打聽電視城規矩」＋事務所「請教何生入廠守則」。
- `progressToward`（底欄）：傳聞步改「未聽聞「…」（去金龍茶餐廳或何生事務所打聽）」；地點步改「到星河電視台或金龍茶餐廳**播**」，同聽傳聞嘅地點分返開。
- `softLockPlayerLine`（鎖定說明）：傳聞步用 full 版連行動名。
- 無行動派到嘅傳聞回 ""，呼叫方維持舊文案，零回歸。

### 文案核對清單（頭兩週玩家會見到嘅指引，逐條核對「地點真係有嗰個功能」）

| # | 文案出處 | 內容 | 核對結果 |
|---|---|---|---|
| 1 | 底欄 remain（BehaviorGate.progressToward） | 未聽聞守則＋到電視台或茶餐廳 | **死路，已修**（見上） |
| 2 | 事態鎖定說明（softLockPlayerLine） | 未聽聞守則（無講去邊聽） | **已修**（補 full 聽聞提示） |
| 3 | 教學 TUT_MAP／TUT_NPC | 茶餐廳／事務所「打聽」不耗日 | 正確，冇改（兩處都有 MOCK_ASK） |
| 4 | 翻身建議（moneyRecoveryHint 一帶） | 金龍茶餐廳或何生事務所「打聽」 | 正確，冇改 |
| 5 | openLoc 入場 toast（cafe_cha／agency_ho） | 「打聽電視城規矩」／「請教何生入廠守則」→ 解鎖第 2 幕情報 | 正確，冇改（同 MOCK_ASK 行動名一致） |
| 6 | 教學舞台（金龍茶餐廳示範板） | 打聽電視城規矩示範卡 | 正確，冇改（地點本身啱） |
| 7 | TUT_TRAIN／TUT_AUD_LOCK | 到對應地點報名訓練／手帳安排訓練再報名 | 正確，冇改（tv／film／music／ad 類地點有 TRAIN_BY_TYPE 報名；電視台本身有 tv 報名） |
| 8 | STORY_HINT_SOFT 各幕 lockedHint | 「開咗去 X 後台／卡座／後巷」 | 屬場景地點散文（播幕地點描述），唔係功能指引；實際導向靠地圖針，冇改 |
| 9 | NPC 情報對白（如曉晴「去星河電視台打探」） | 打探＝睇通告欄 | 電視台有通告欄，講得通；屬閒聊口吻唔係教學指引，冇改 |
| 10 | 靜態斷言（test_guidance34_static） | MOCK_ASK 入面 grantsRumorId=tvb_rules_gossip 只喺 cafe_cha＋agency_ho；全檔冇「去星河電視台打聽」類字串 | 已釘住，防回歸 |

## 3. P0-4 「過一日」affordance

- 現況：逛逛日（`isMapDay(todayPlanId())`：scout_all／scout_nt／scout_kln／scout_island）地圖提示欄**冇**「開始今日行程」掣（嗰個掣只畀有安排行程嘅日子），玩家要自己去選單搵「提早休息／+1日」。
- 改法：`paintBar` 同一個位、同一款式（`.map-start-today`）加掣 `id="map-end-day"`「逛完・過一日」（title 屬性寫明點用）；條件＝地圖日＋非 `homeEditable`（手帳編輯週程嗰陣唔出，嗰度有自己嘅確定流程）。撳掣行**現有** `confirmEarlyRestFromMenu()`（二次確認→`endBrowseDayGoHome()`：寫 plan=rest＋休息增益＋`tickDay()`），冇寫任何新結算。
- 有安排活動嘅日子唔出呢個掣（出返「開始今日行程」），既有流程零影響（邏輯測試段三覆蓋兩種日子）。
- 取捨：冇加一次性 toast 提示——掣本身常駐喺地圖頂欄、標籤已寫明用途；boot 時機彈 toast 會同教學搶畫面，唔做。

## 4. P0-5 系統出場交代

- (a) 傳聞頁：卡面本身已有「來源：{r.source}」，今次補**兜底**——冇 `source` 欄嘅卡：報紙碎片（`paperFrag`）顯示「報紙花邊」（佢嘅真出處），其餘顯示中性預設「街坊傳聞」，唔亂作地點。冇改任何碎片數據。
- (b) 人情頁：新增純顯示對照表 `DEBT_ORIGIN_LINES34`（唔改債數據結構），開局四筆各加一行「來歷：」——屋企家用 `debt_family_home`、何生春季數 `card_ho_spring`、道具組老張器材數 `card_zhang_spring`、教學人情 `debt_ho_tutorial`。季節卡同 mockDebts 卡兩條渲染路徑都接咗；`renderDebtPane` 以 `typeof` 守衛讀表（跟全檔慣例）。文案跟既有設定：屋企＝應承交家用、唔催；何生＝入行墊支記數簿；老張＝借器材未清；教學＝何生教規矩嘅人情。
- (c) 總說明：傳聞頁頂加一句（碎片嚟自邊、拼合有咩用）；人情頁季節橫額後加一句（邊個欠你／你欠邊個、債會到期、債權留住有用）。兩頁原有嘅係教學 coach（步驟指示）同季節橫額（時節語），唔係頁面用途說明，無重複。

## 5. P1-1 後果白話化

### (a) 壓力——真碼公式查證（逐行對過）

| 影響面 | 真碼位置 | 分支 |
|---|---|---|
| 打工收入 | `resolvePlannedDay` 嘅 `street`／`cafe_gig` 兩段（計法相同） | 壓力 ≥90：`pay×0.2`（下限 $50）；≥70：`pay×0.5`（下限 $80）；<70 唔打折 |
| 試鏡成功率 | `chance(gig)` | ≥70：`p×0.78`；≥90：再 `p×0.7`（兩段累乘＝×0.546） |

- 新增 `stressImpact34(s)`（分支同上表一字不差）＋`stressImpactLine34(s)`（百分數由 impact 值即場計，唔 hardcode 字串數字）。
- `showStressPreviewModal` 喺風險行後加一行「後果講明：…」，以本週**高峰**壓力（`pv.peak`，同風險行同一基準）計：≥90「收入只得返約 20%；試鏡成功率打到約 55%」；≥70「約 50%／約 78%」；52–69 講明未到打折線（70 先開始）；<52 講明 70 以下冇影響。
- 驗法：邏輯測試用真 `chance()` 同一狀態淨改壓力，實測比率 =0.78／0.546，同 helper 對照；靜態測試釘住真碼 `pay*0.2／pay*0.5／p *= 0.78／p *= 0.7` 四個分支原文，防日後改公式唔記得同步。
- 申報：試玩報告講「壓力爆表令收入跌 64%」——真碼 ≥90 係打到兩成（跌 80%），報告嗰次係隨機 pay 區間內嘅個別結果，唔係公式值；本包以真碼為準。

### (b) 雙軌白話解釋

- 新增 `dualTrackExplainHtml34(result)`，喺 StoryPlay `showResult` 嘅雙軌行後接駁：條件＝`result.dual` 有正增益（dStage>0 或 dCredit>0，即「事態結算第一次真係畀咗聲望／信用」）＋未出過（`S.flags.guidanceDualExplained34`，出嗰陣即寫旗＋saveQ）。冇增益唔出、亦唔燒旗。
- 文案刻度跟真門檻：報紙點名 `newspaperNameTier`——聲望 15 起點名（named）、40 起「人氣新人阿偉」（titled）；信用係後段節點／通告嘅隱形門檻（例 1989 暴雨救場要信用夠班）。冇用「60 企穩」呢類無真碼對應嘅數。

## 6. 測試

- 新增 `tests/test_guidance34_logic.js`（61 項，全過）：(a) 真 teaser＋真 canAudition＋同詳情頁同源數字；(b) 真 BehaviorGate＋真 stub 注入，底欄／鎖定說明逐字斷言；(c) 真 paintBar→真確認→真 endBrowseDayGoHome（tickDay 計數 stub，只驗接駁契約——佢係全遊戲共用引擎、本包唔郁）；(d) 真雙頁渲染（教學債行真 markRumorTutorialDone 路徑入帳）；(e) 真 chance() 比率＋真預覽 modal；(f) 解釋只出一次。
- 新增 `tests/test_guidance34_static.py`（39 項，全過）：接線斷言、P0-3 核對釘住、壓力真碼分支原文釘住、紅線（SAVE key）冇郁。
- 既有全套：23 個 logic 檔＋24 個 static 檔＋p03 filter 全部繼續全過；全檔 script `node --check` OK。
- 中途修咗一個自引問題：`renderDebtPane` 直讀新 const 會令舊測試抽函數 sandbox 爆 ReferenceError——改用 `typeof` 守衛（ORIGIN34），跟全檔慣例。
