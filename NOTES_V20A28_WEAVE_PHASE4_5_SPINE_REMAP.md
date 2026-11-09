# v20a28 — Weave Phase 4-5：主幹基建（三年版 phase／閘重映射＋openGate ctx 擴充）

性質：soft 預覽基建。SAVE key（starVolunteer_map_v19w）／softRev（s107）／?v=（v20a10）無改；content pack JSON 無改（覆寫只喺 index 做，跟 STORY_LOC_SOFT／STORY_HINT_SOFT 先例）。

## 問題

content pack `story_detail_c1_to_c17.json` 屬五年版節奏：C16 `week_min:100`、C17 `phase:"P5"`＋1992 收束；引擎 phase 晉升（`computePhaseWantFromProgress`）舊條件係 C7→P2、1990＋C10→P3、1991→P4、1992→P5。三年版（1988–1990）入面 P4／P5 永遠唔達，C6–C17 嘅閘亦無雙軌／年份／標籤可用（`BehaviorGate.readCtx` 無 credit／year／dual，tags 唔讀真 castingTags）。

## 改動

### 1. openGate ctx 擴充（BehaviorGate.readCtx）

新增 live 讀取：`liveCredit()`（以 `readDualTracks(S).industryCredit` 派生值為準，S.industryCredit 只係 sync 鏡像）、`liveYearSeason()`（行 Phase 4-1 嘅 `yearSeasonNow()`，真日曆年份，唔經 soft display 改月份）、`liveTags()`（將 `S.castingTags` 嘅 {id,label} 物件陣列正規化成 id＋label 字串清單）。

ctx 新增欄位（原有欄位語義不變）：

| 欄位 | 來源（無明確傳入 ctx 時） | 明確傳入 ctx 時預設 |
| :--- | :--- | :--- |
| `credit` | liveCredit() | 0 |
| `dual` | fame＋credit（可由 ctx.dual 覆寫） | 同左 |
| `year` | liveYearSeason().year | 1988（＝dayIndex 預設 0 嘅年份，方便樣本對照） |
| `tags` | liveTags()（改動前係恆空陣列） | [] |
| `fame`／`season` | 原有 liveFame()／liveSeason() 不變 | 不變 |

### 2. 三年版覆寫表 STORY_GATE_3Y（新表，跟 *_SOFT 命名風格）

`StoryOC.evalNode` 開頭先問 `BehaviorGate.evalGate3Y(node, opts)`：有 entry（C6–C17）就回覆寫評估，唔行 pack 五年版 openConditions／node.phase，亦唔俾 freeplay slot trigger 搶先（掛點喺 soft 分支之前）；無 entry（C1–C5 同其他節點）回 null，完全行返舊邏輯，C1–C5 行為零變化。

評估語義：全部條件 AND；數值門檻用嚴格 `>`（跟主幹 §4）；另鏡像 StoryOC v17z 同日禁（當日已播完任一 C* → 唔入可播，`opts.ignorePacing` 可豁免）。年份窗以外嘅節點用 `yearMin`（過咗年份仍可補做，唔會永久鎖死）；只有 C17 用 `yearEq:1990`（事件閘本質）。

逐節點覆寫閘清單（N↔C 對照跟主幹 §2；前置以 N 次序落返 C id）：

| 節點 | 前置 needDone | 路線 route | 週 weekMin | 聲量 fameGt | 信用 creditGt | 雙軌 dualGt | 標籤 tagAny | 年份 | 季節 seasonIn | 原閘備註 |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| C6（N6） | — | route_tv | 15 | — | — | — | — | — | — | 主幹原閘，全年可選 |
| C7（N7） | C5 | — | — | — | >20 | — | — | ≥1989 | 夏 | 「暴雨外景」情報屬內容層 |
| C11（N8） | — | — | — | — | — | — | — | ≥1989 | 夏／秋 | 「攜帶特定禮物」屬內容層，4-6 對照時處理 |
| C8（N9） | C7 | — | — | >28 | — | — | 喜劇／comedy／動作／action | ≥1989 | 秋 | — |
| C9（N10） | — | — | — | — | — | — | — | ≥1989 | 冬 | 「人情債觸發」屬內容層，4-6 處理 |
| C10（N11） | C9 | — | — | — | — | >70 | — | ≥1989 | 冬 | — |
| C15（N12） | — | — | — | — | — | — | 動作／action | ≥1990 | 春 | — |
| C14（N13） | C10 | — | — | — | >42 | — | — | ≥1990 | 夏 | — |
| C12（N14） | C14 | — | — | >50 | — | — | — | ≥1990 | 秋 | — |
| C16（N15） | C12 | — | — | — | — | >125 | — | ≥1990 | 秋 | — |
| C13（N16） | — | — | — | — | — | — | — | ≥1990 | 冬 | — |
| C17（N17） | C13 | — | — | — | — | — | — | =1990 | 冬 | 事件閘；結局判定／呈現留待 4-10 |

標籤比對：ctx.tags 已正規化（id＋label 都入列），tagAny 用候選清單（中文 label＋英文 id 兩形）任一命中。選角標籤 registry（STUB_CASTING_TAGS_v1.json）係外部 content，4-6 內容對照時若 registry 用其他 id，再喺覆寫表加候選即可，唔使改評估器。

### 3. phase 三年版重映射（computePhaseWantFromProgress）

| Phase | 五年版（舊） | 三年版（新） |
| :--- | :--- | :--- |
| P1 | 開局 | 開局（不變） |
| P1.5 | C5 done | C5 done（不變） |
| P2 | C7 done／1989 年 | C7 done／1989 年（不變） |
| P3 | 1990 年＋C10 done 或 route_indie／route_commercial 旗 | **1990 年到**（唔再要求 C10／路線旗） |
| P4 | 1991 年＋（C11 done 或已 P3） | **1990 秋（9 月起＋季節標籤秋／冬）或 C14 done** |
| P5 | 1992 年 | **1990 冬（12 月＋季節標籤冬）或 C13 done** |

細節：
- 季節 bump 加月份守衛：1–2 月標籤雖係冬，屬上一季冬尾，唔當「1990 冬」，避免 P4／P5 喺 1990 年頭跳級。
- 1991→P4、1992→P5 兩行保留作完結後 freeplay 安全網，唔再係任何節點前置。
- `syncPhaseFromProgress` 只向上 bump：舊檔已高過嘅 phase 唔會俾新表拉低；`recomputePhaseFromProgress`（年跳 debug）先會全量重計。
- 邊啲位真係讀 phase：`evalNode` 嘅 node.phase 相檢（phaseSoft）同 phase_ token、`listOpen` 開局 P1 佇列、事態列顯示。C6–C17 改行覆寫閘後唔再受 node.phase 相檢影響；phase 表主要服務其餘 pack 節點（R／A 線）嘅節奏同顯示。呢個係刻意嘅最小侵入：唔重寫引擎，只換晉升表＋加覆寫閘。

### 4. 驗收樣本 C6

C6 已接通新閘路徑：`StoryOC.evalNode` 真評估——route_tv＋W15 起開；缺 route 唔開；W14 唔開（邏輯測試覆蓋）。
C7–C17 只寫覆寫表＋閘評估，**未接通內容呈現**：唔新增 dialogue／offer 流程，唔保證佢哋喺玩家事態列出現（playerOffer／offers 機制維持原狀）；內容上線係 4-6／4-8 嘅工作。防誤開由閘矩陣測試逐節點證明：逐個抽走關鍵條件（前置／門檻／標籤／年份／季節）都唔開。

## 測試

- 新增 `tests/test_weave45_logic.js`（76 項全過）：行真 StoryOC.evalNode＋真 BehaviorGate——(a) 閘矩陣 C6–C17 每節點齊條件→開、逐個關鍵條件抽走→唔開（含門檻邊界 20/28/42/50/70/125 啱啱唔過）；測試 node 故意帶五年版 pack 欄位（phase P5＋week_min:100）證明覆寫取代 pack 閘；(b) phase 邊界（1989→P2、1990→P3、1990 秋→P4、1990 冬→P5、C14／C13 done 捷徑、1990 年頭唔跳級、舊檔 phase 唔拉低＋唔誤開 C7）；(c) ctx 新欄位（fame／credit 派生／dual／year／season／tags 正規化＋明確傳入優先）；(d) C1–C5 無覆寫＋舊 token 閘行為不變；(e) C6 樣本三態；另同日禁＋ignorePacing 豁免。
- 新增 `tests/test_weave45_static.py`（59 項全過）：覆寫表齊全度同門檻字面值、前置鏈、掛點次序（覆寫喺 soft 分支之前）、ctx 接線、phase 新舊規則、慣例不變。
- 既有 tests/ 全套（34 檔）改後全過，零回歸；全檔 script `node --check` OK。

## 取捨／未做

- C11「攜帶特定禮物」、C9「人情債觸發」係內容層觸發，唔入閘（閘只守時間窗）；4-6 逐節點對照 pack 內容時先處理，避免基建步硬造未有嘅禮物／債務語義。
- C17 只守入場閘（前置 C13＋1990 冬）；結局判定（三軸總帳）同呈現組裝係 4-10，今步唔掂 pack 內置嘅舊 E01–E10 直揀機制住。
- phase P3 改為 1990 年到即達：其餘以 phase 為條件嘅 pack 節點（R／A 線）會跟三年節奏提早鬆綁，屬預期內嘅三年版密度；佢哋各自嘅 openConditions（rel／done 等）仍然把關。
