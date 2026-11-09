# NOTES V20A61 — 後果包 CONSEQ61（早期差結局「未紅先收」＋壓力爆煲強制病倒）

用戶 2026-11-10 拍板：模仿《明星志願》「玩太差提早收場」＋「壓力爆煲強制病倒」，
哲學＝**有警告、有寬限、唔一嘢判死**。全部新狀態收喺 `S.conseq61`（防禦式初始化，舊檔缺欄自動補）。
唔改：SAVE key／softRev／`?v=`／pack JSON／CALIB60 參數／`resolveEnding410`＋`ENDING410_T` 門檻／
感情 commit 條件／STORY_GATE_3Y 觸發條件。E6 仍然只限自願退圈；強制收場係**新結局格 E7**。

主檔 index.html：4,701,779 → **4,727,010 bytes**（+25,231）。

---

## 第一部分：早期差結局「未紅先收」（E7）

### 觸發 A：年終評核（CONSEQ61_REVIEWS）

| 年份 | 地板 floor（dual） | 警告線 warnLine | 邊界週 boundaryWeek |
|---|---|---|---|
| 1988 | **45** | 65 | wk43 |
| 1989 | **100** | 130 | wk95 |

- dual ＝聲望＋信用，同 `resolveEnding410` 計法一致（經 `endingDual410` 攞 `{stageVolume, industryCredit}` 再加）。
- 邊界週推導：真日曆 1988-03-07 開局；`calib60YearOfWeek(w)`＝第 w 週首日年份。
  wk43 首日＝1988 年內、wk44 首日已入 1989 → wk43 週結＝1988 最後一次週結；同理 wk95＝1989 最後週結。
  評核函數內有防禦核對：`calib60YearOfWeek(boundaryWeek)===Y` 先准判，日曆對唔返就唔判。
- **地板推導（v20a60 回放探針實測，校準後曲線）**：
  - 最慢嘅認真弧（Arc A 校準後回放）：wk43 dual **70**、wk95 dual **183**。
  - 穩定弧（Arc C ×0.75）：wk43 dual 103、wk95 dual 193。
  - 全程 hea（數值凍結喺開局 fame5/stage14/acting18）：dual **15**；hea＋輕微漂移（fame12/stage20/acting24/delta+2）：dual **31**。
  - 地板 45：高過 hea 漂移弧（31）約 1.45×，低過慢弧（70）——慢弧有 **1.56× 餘裕**；1989 地板 100：慢弧 183 有 **1.83× 餘裕**。
    即係「近乎冇認真玩」先會中，「慢熱但持續有做嘢」遠遠過關。
- **警告先行**：距邊界週結 1–4 週（dist 1–4）而且 dual 低過 warnLine，先喺**週結算旁白**出何生提點
  （走現有 `pushFlavor` 渠道，冇新造彈窗）；dist≤1 出急版（「下週就係評核…仲差 X」）。
  warnLine（65／130）刻意設喺慢弧評核值（70／183）之下少少：慢弧唔會被無謂警告滋擾，貼線玩家就一定收到聲。
- 評核喺邊界週嘅 `settleWeek` 內即判（`conseq61SettleEval`）：過關出續約行、唔過寫
  `conseq61.pendingEnding={kind:"review", year, dual, floor}`，呈現交返屋企（enterHome）之後出（見下）。
- 已有 `S.ending410` 嘅存檔：評核／寬限全部跳過。

### 觸發 B：破產寬限（CONSEQ61_CFG.graceWeeks = 4）

- 觸發：週結時 `S.money ≤ 0`（真・水底；生活費扣款本身永唔扣負，$0 就係地板）→ 起寬限 4 個週結，
  週結旁白明示倒數；期間保底散工照常可接（冇郁散工系統）。
- 倒數：每個週結 −1，**但有未完拍攝（shootRemain>0）嗰週暫停倒數**（拍緊戲有糧尾，唔好拍到一半收人場），旁白會講明暫停原因。
- 解除：存款返到 ≥ 下週生活費估算（`livingCostEstimate(w+1)`，即現行生活費帶 mid，1988＝$2,400、
  1989/1990 跟 v60 年份＋聲望加級）→ 即刻解除、出「捱過咗」行，**唔留案底、唔扣任何嘢**。
  有錢返但未過線 → 未解除，倒數照行。
- 用盡（weeksLeft 減到 0）：寫 `pendingEnding={kind:"bankrupt"}` 收場。

### 呈現：E7「未紅先收」

- `conseq61PresentForcedEnding()`：喺 `enterHome` 渲染完週結算卡之後（setTimeout 90ms）行，
  冪等（冇 pending／已收科即返回 false）。
- 只用 `resolveEnding410(S)` 攞**快照／感情軸／去留軸**（唔郁佢嘅事業判定同門檻），事業軸覆蓋為：
  - `career: "E7"`、`careerVariant: "review1988" / "review1989" / "bankrupt"`、
    `title: "未紅先收・"＋去留稱號`、`eveKey: "forced_review" / "forced_bankrupt"`、
    另加 `earlyEnd {kind, year, dual, floor, week}`。
  - 結果寫 `S.ending410`（同正常收科同一形狀）＋`saveQ()`，所以剪報頁／手帳總結／重睇掣全部照行。
- 呈現全套行返 ending410 兩頁 modal：事業場景 → 感情＋去留＋個人化插入 → `showEndingSummary410()` 手帳總結頁。
- 事業場景 `endingCareerScene410` 新增 `case "E7"` 三段獨立文案（1988 評核／1989 評核／破產），
  跟 endings-design 界線：有尊嚴、唔懲罰式（何生畀介紹信、講明「唔係輸喺唔夠叻，係輸喺未紅之前先冇咗糧」）。
- 連帶條件化（**非 E7 路徑一字不變**，weave410 既有測試鎖住）：
  - `endingSummaryHtml410` 標題：E7 時用「{year} 年尾評核／寬限期滿・提早收科・手帳總結」，尾段改「呢次收場唔係你揀嘅」版。
  - 剪報卡（renderClippingsPane）日期：E7 時用「{year} 年尾・年終評核」或「寬限期滿・提早收場」，「呢三年」改「呢段日子」。
  - `ENDING410_CAREER_NAMES` 加 `E7: "未紅先收"`；`ENDING410_ADJ_RUMOR` 加 E7 一條。
- 收場後唔鎖檔（同既有結局一致）：可以繼續過日子當另一條時間線，或者開新一局。

### 舊存檔安全

- `normalizeSaveObj` 尾加 `conseq61LegacyMark(o)`：今日曆年份已過評核年份、或已有 `ending410` →
  靜靜寫 `reviews[Y]={passed:true, legacy:true}`，**永不追溯收場**；未到評核年份嘅檔唔標記，評核照常將來判。

---

## 第二部分：壓力爆煲強制病倒（CONSEQ61-2）

### 參數（CONSEQ61_CFG）

| 參數 | 值 | 意思 |
|---|---|---|
| sickWarnStreak | 2 | 連續 2 日收市 ≥80 → 警告層 |
| sickStreak | 2 | 連續 2 日收市 ≥90 → 病倒 |
| 病程長度 | 2–4 日 | `2 + (streak≥3 ? 1:0) + (peak≥99 ? 1:0)`，封頂 4 |
| sickRelief | 35 | 病癒嗰日壓力 −35 |
| sickCooldownDays | 14 | 病癒後 14 日冷卻 |
| sickCreditPerDay | 2 | 拍攝告假一日信用 −2 |
| sickCreditCap | 6 | 一次病程信用扣減封頂 −6 |

- 壓力背景（全弧報告實測）：現行壓力兩段制——1/3 週數＝0、後期恆定 60–75、從未 ≥80；
  來源：拍攝日 +5（殺青）、訓練 +8~14、街頭/咖啡 +5~10、試鏡 +7~11；STRESS_MAX=100、HUD 危險線 90。
  所以 ≥90 連續 2 日係「真・爆煲」先會到，正常遊玩唔會誤觸；≥80 做警告層啱啱喺恆常上限（75）之上。
- 計法：`conseq61DailyTick()` 喺 `advanceDay()` 翻日嗰刻行，用**翻日前嗰日嘅收市壓力**（未經週結 −6/回復扣減）
  更新 streak90/streak80/peak90；病緊唔計、冷卻期內 streak90 強制歸零（唔儲連鎖）。

### 警告層（行現有渠道，冇新 UI 系統）

1. 地圖壓力提示 `updateMapStressTip`：streak80≥2 且當前壓力 ≥80 → 升級做「身體警號：連續多日高壓…再谷落去會病倒」。
2. 週結算旁白：週結收市壓力（stressAtEnd）≥80 且未病 → 「身體警號」一行，講明病倒後果（行程作廢／告假扣信用）。

### 病倒日流程（`conseq61ResolveSickDay`）

接線（全部行返既有日流程，冇平行日曆）：
- `resolvePlannedDay` 開頭守衛（排程執行路徑）；
- `goToMapForBrowse` 入地圖前守衛（劇情進行中唔截，費事打斷播片）；
- `endBrowseDayGoHome` 開頭守衛（唔准扮「提早休息」避病）。
三路都係：病日 → 接管嗰日結算（出日結卡／週加速靜默合併，跟主流程 `_weekAccel` 慣例）＋`tickDay()` 耗日。
同一日有 done 標記防重複結算。

病日內容：
- 今日週計劃格改寫做 `"sick61"`（`planMeta` 新增分支顯示「🤒 病假」），手帳睇得返嗰日點解空咗。
- **拍攝日 → 告假**：`doneDays` 唔加（冇嗰日進度）、`deadlineDay += 1`（順延係必須——否則
  `processOverdueShoots` 會成部戲 fail＋扣違約金，違反「唔好一病永不翻身」）、冇嗰日 delta／糧、
  信用經 `S.industryCreditDelta −2/日`（敘事扣減，唔經 CALIB60 縮放；每病程封頂 −6，扣到上限會喺旁白講明）。
  −2 嘅定法：大約等於一日恆常拍攝信用增益（經 CALIB60 縮放後）嘅兩倍——告假要痛，但一次病最多 −6，
  以 dual 地板 45–100 計只係一段距離，唔會直接推人落評核地板下面。
- **試鏡日（job:）→ 取消預約**：booked 移除、`clearJobFromPlans` 令通告返板，零罰（第日再試過）。
- **其他計劃日 → 作廢**（訓練／街頭／咖啡等全部唔行）；rest／地圖日出休養 flavor。
- 病程**最後一日**：壓力 −35（`apply({stress:-35})`，跟既有週末 −6 回復同一渠道）、寫 cooldownUntil=今日+14、
  清 sick、streak80 歸零。
- **生活費處理**：病假期間冇額外扣款；週結生活費照既有邏輯扣（嗰週病到冇收入，生活費照扣——
  呢個正係破產寬限要接住嘅風險，兩部分係設計上銜接嘅，唔係打架）。同 v58 休息系／武師班冇衝突：
  病日唔會行到 rest 分支，自然唔會誤加／誤扣體能。

---

## 驗證

- **新測試**：
  - `tests/test_conseq61_logic.js`：**82 斷言全 PASS**。覆蓋：邊界週年份鎖（43↔1988／95↔1989）、
    地板推導（hea 15/31 被捉、慢弧 70/183 餘裕 1.56×/1.83×）、警告先行（wk40/42 出聲、邊界週先判）、
    慢弧兩評核點過關、貼線弧（dual 50）有警告但唔誤殺、寬限起／倒數／拍攝暫停／翻水解除／用盡收場、
    舊檔 legacy 標記唔追溯、E7 present 寫檔＋冪等＋總結頁標題、resolveEnding410 判定表冇 E7、
    病倒觸發／長度（2/3/4 日）／冷卻唔連鎖／streak80 警告、告假順延＋信用封頂 −6、病癒 −35、試鏡返板。
  - `tests/test_conseq61_static.py`：PASS。鎖主 блок／參數／全部接線點／E7 呈現接入／判定表冇 E7／SAVE key。
  - **反證**：兩套新測試對 v20a60 index 行 → 都 FAIL（logic exit 1、static exit 1），符合 v20a37 起嘅反證要求。
- **全套 tests**：56/56 檔案 PASS（基線 54＋新 2）；兩個 script block `node --check` OK。
- 測試過程捉到一個真 bug 並已修：`endingDual410` 回 object 而唔係數，`conseq61DualOf` 要照
  `resolveEnding410` 計法加總 stageVolume＋industryCredit（現行實作回 `{fame, credit, dual}`）。

## 已知邊界

- 病日以「開始行程／返地圖／提早休息」三個入口為閘；玩家如果成日留喺地圖內撳耗日行動嘅極端繞道，
  要到下一個入口先結算病日——唔會漏病（sick 窗口按絕對 dayIndex 計，過窗未結算嗰日唔會補扣，只會由當日繼續），
  但呈現時序可以遲一日。
- 評核／寬限只喺週結判（settleWeek），同遊戲既有節奏一致；唔會喺週中突然收場。
- 病倒觸發用「收市壓力」＝當日所有增壓結算後嘅值；當日如果已經休息減壓到 <90，嗰日唔計入 streak（有意：肯唞就唔好病）。
