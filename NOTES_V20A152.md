# NOTES_V20A152 — 鄧麗萍只刪感情線，留返排片 NPC

- 分支：`v20a152`（工作副本 `~/workspace/linji-work152/`，由 main `e08a070`＝v148 開出）
- 拍板：用戶 2026-11-13 06:54——只刪感情線，留返佢做排片。
- 紀律：唔直改 content pack JSON；唔改 SAVE key（`starVolunteer_map_v19w`）／softRev（`s107`）／產品 `?v=`（`v20a10`）；**唔落地**（本票只做到 commit，唔 checkout main、唔 squash merge、唔 push main）。
- index.html diff：+68／−275（淨 −207 行）。新測試 1 個（`tests/test_tang152_static.py`，47 項斷言），舊測試更新 5 個。

## 1. 刪咗乜（感情線部分）

### 1.1 `story_detail_romance_tang.json` 停載（live 路徑拎走）
- loader 唔再 `get("story_detail_romance_tang.json")`；Promise.all 解構、賦值、`STORY_WIRE.romance` 初始化改做 `{ veraHiuChoi: null, lanXu: null}`（tang 槽刪除）；`iterNodes` 嘅 `push("romance_tang", …)`、TEXTFIX55／contra98／years66 呼叫入面嘅 `romTang`、error 行、console R 計數、`applyRomanceWf2Overrides81` 嘅 `rom.tang` 全部拎走。
- **檔案本身原封不動留喺 repo**（照有 `R_tang_ending`＋`flag_tang_commit`／`he`／`be`），證明係停載唔係直改；`test_tang152_static.py` 斷言佢照喺度。
- 理據：呢個 pack 淨係載鄧麗萍感情線 5 節點；停載即係成條線 live 去唔到，唔使逐個節點刪。

### 1.2 `R_tang_ending` 節點及 HE／BE 抉擇＋三支旗
- WF2 覆寫表刪 5 個 tang 條目（meet／push1／push2／crisis／ending）；WF5 變體覆寫表刪 `R_tang_ending` 條目（header 註解加 v152 行）；DengLine `HELD` 由 4 縮到 3（`["R_tang_push1","R_tang_push2","R_tang_crisis"]`，L25650）；`PUSH_CHROME` 刪 ending 行；self-check 簽名表刪 ending 行；`push_standing`（HE standing＋1）檢查刪除；BR89 收科回望 try block 成段刪（留 v152 註解）；`CONTRA98_WHEN_FIX` 刪 `R_tang_ending` 行（23→22 節點，winter_finale 計數 12→11）；事務所掣列表刪 `"R_tang_ending"`；debug panel `rCount` 刪 `"tang"`；`relMap`（`textfix55Note` 入面）刪 `["rel_tang","鄧麗萍"]`。
- `flag_tang_commit`／`flag_tang_he`／`flag_tang_be` 程式碼引用全清（`C_tang_ending_he`／`be` 同理）。`grep` 剩低 4 處 `romance_tang`／`romTang` 字眼，全部係 v152 註解。
- 註：`R_tang_ending` 字串而家只出現一次——push mock 載入過濾嘅謂詞（見 §3.2）。

### 1.3 TEXTFIX55 開閘＋收尾條目
- 刪 EXACT 6 條：stub synopsis（「將影響日後感情線能否正式開啟…」）、stub label（「留下聯絡：寫入 flag_tang_met（不開正式閘）」）、ending HE label／note（「跨越商業界線…」）、ending BE label／note（「堅守專業界線…」）。
- 刪 NOTE 4 條：meet data／wait 兩條 notes（「打開同鄧麗萍合作的第一道閘」／「暫緩開閘…」）、stub 兩條 notes（「正式開閘見 R_tang_meet」／「不寫 flag_tang_open」）。
- 玫瑰拒收句輸出改做純公事拒絕：「鄧麗萍：「玫瑰？呢度係排片部，唔係花店。想傾檔期，帶數據嚟。」」（key＝gift JSON 原文「玫瑰？你想綁架我的情緒，還是想拖延談判？」留返先 match 到；舊輸出「你想我心軟，定係想拖住唔傾數？」已清）。
- 腕表第二句新增 EXACT 條目：原文（簡體「别」）「鄧麗萍：「我收下。别以為送完表就可以談感情條款；我們先把場次談清楚。」」→「鄧麗萍：「我收下。錶係錶，檔期係檔期——我哋先把場次談清楚。」」。
- **保留**「可與事業結局並存。」呢條 NOTE（lan／xu／vera／hiu／choi ending notes 共用，刪咗會令其他線顯示書面語）；保留全部 meet／push1／push2／crisis 業務文本條目同 stub 兩句 beats 行、實用禮物 calc 句。
- 實作教訓：TEXTFIX55 係巨型單行 object，插入條目嗰陣要同時保留前後分隔符——第一次插入食咗 `, `、補救又食咗收引號，兩次 `node --check` 失敗先修好。之後已 `node --check` 通過（SYNTAX-OK）。

### 1.4 其他刪除
- `tangFileThreshold` 刪咗死咗嘅 `STORY_WIRE.romance.tang` 讀數分支（只剩 DengLine soft A 鎖定值 2，否則預設 2）。
- L21901 註解更新（stub 唔經 PA 覆寫表，改行 `normaliseTangStub152`）；L41497 註解刪 `flag_tang_commit` 先行例子。

## 2. 留返乜（排片 NPC 部分）

- **DENG 排片部線**：`MOCK_STORY_DENG_LINE_MEET_SOFT_v1.1.json`（meet：帶新片計劃去排片部）＋`MOCK_STORY_DENG_LINE_PUSH_SOFT_v1.json`（push1 票房數據證明賣座、push2、crisis 夜班房票房互通）照載入；DengLine HELD／chrome／self-check／pushGate 照行。
- **生意閘門唔郁**：`flag_tang_open ∧ rel_tang ≥ 2`（`DengLine.pushGate`）、`rel_tang_threshold` 讀數、`resolveThreshold`、`debugUnlockTangPush`、debug panel 顯示、seed `seed_deng_push_ready`（播 `flag_tang_open: true`＋`rel_tang: 2`，開 push1 生意閘）、`gift_prefs.json` tang entry（`relKey: "rel_tang"`、`requireFlagsAny: ["flag_tang_open"]`）。
- **`R_tang_meet_stub` 見面本身**：改做純公事介紹（見 §3.3）；結構層（choice id／effects flags＋stats／flags_written／openConditions／supersededBy）原封不動。
- **實用禮物反應**：名筆、桌上計數機、正裝腕表、咖啡豆等公事反應留返（「實用。我鍾意睇得見、計得到嘅誠意。」）；`sys.tangLocked`＝「院線那邊，還未到送禮的時候。」（公事口吻）留返。
- **角色層**：`tang_laiping` 角色登記／立繪／身高／剪影、`cast_main.json` entry（dev 參考）留返；WF5 meet／push1／push2／crisis 覆寫留返；L27703 `R_tang_meet` 免季節閘列表留返。
- **`flag_tang_crisis_*` 留返**（見 §4.1）。

## 3. 載入機制（每項點處理）

| 目標 | 機制 | 位置 |
|---|---|---|
| `story_detail_romance_tang.json` | **停載**：loader 唔再 fetch，相關引用全清；檔案原封不動 | `refreshCopyPacksFromDisk` 一帶（L31308–31452） |
| push mock `R_tang_ending` beat | **載入過濾**：`DengLine.loadPushMock` 之前 `dengPushMock.beats = beats.filter(b => b.id!== "R_tang_ending")`；原檔照有 ending beat（4 節） | L31442 |
| `R_tang_meet_stub` 開閘語言 | **載入正規化**：新函數 `normaliseTangStub152(pack)`（L31270），喺 TEXTFIX55 之前對 `rom2` 執行（L31414）；只改玩家可見文字層：synopsis→「阿偉到公關公司洽談臨記工作，在會議室遇見鄧麗萍。二人短暫交談，交換電話方便日後排片聯絡。」；`C_tang_meet_keep_contact` label→「留下聯絡：交換電話號碼」／notes→「交換咗聯絡，日後排片可以直接聯絡。」；`C_tang_meet_hold_back` label→「暫時唔留電話」／notes→「今次唔留聯絡，日後有排片需要先再聯絡。」；原檔 `lan_xu.json` 原稿照有舊字 | L31261–31289、L31414 |
| 玫瑰／腕表反應 | **TEXTFIX55 覆寫**：key＝gift JSON 原文，輸出改純公事；`gift_react_copy.json` 原句照喺度 | TEXTFIX55_EXACT |
| 刪旗／刪節點 | 直接刪除 index.html inline 碼（WF2／WF5 覆寫表、HELD、chrome、self-check、BR89、CONTRA98、事務所掣列表等） | 見 §1.2 |

## 4. 邊界問題（等統籌決定，唔好自己估）

### 4.1 `flag_tang_crisis_*` 去留——現狀：留返
任務刪範圍寫明 `tang_crisis*` 旗標，但 crisis 節點本身係生意抉擇（數據 vs 人情爭黃金檔），其旗同 push1／push2 抉擇旗同類（純抉擇留痕），且任務點名嘅 self-check 行只提 ending（L26121／L26135），無提 crisis 行（L26120）。現狀：crisis beat＋旗照行，self-check crisis 行保留。如統籌要清，只需喺 push mock 載入過濾加多一行 strip（同 ending 過濾同一個位）。

### 4.2 Seed 檔——現狀：原封不動
無任何 seed 播 commit／he／be 旗；`seed_deng_push_ready` 播嘅係生意閘（留返所需）。seed meta 第 32 行「…/crisis/ending」係舊 scope 描述，檔案唔直改所以留低咗。如要改描述，等統籌拍板先經覆寫／seed 機制處理。

### 4.3 舊檔相容——現狀：未做遷移清理
舊存檔若已有 `flag_tang_commit`／`he`／`be`，而家無任何讀取方（收科回望已刪），屬死旗留喺 save 入面，未做遷移清理。要唔要清，等統籌決定。

### 4.4 附帶發現：`R_tang_ending` 原 when 係 1992冬
`test_contra98_logic.js` 全域守門曾 FAIL——pack 入面 `R_tang_ending` 原 when 係「1992冬」，經 years66Walk ＋2 變 1994；以前係靠 CONTRA98 嗰行先壓返 1990冬再 walk 到 1992冬。跟住嗰行刪咗，呢個死節點會顯示 1994，但 live 已經去唔到（pack 停載＋mock 過濾）。處理：測試加豁免（同 `R_lan_*` 豁免並列，註明係死數據唔係 live 漏網），index.html 唔郁。

## 5. 驗證

### 5.1 新測試 `tests/test_tang152_static.py`（47 項斷言，全部 PASS）
- 紀律：SAVE key／softRev／?v= 不變。
- 停載：唔再 fetch romance_tang、冇 `romTang`、STORY_WIRE 冇 tang 槽、iterNodes／TEXTFIX／contra98／years66 呼叫冇 romTang。
- 刪旗／刪節點：程式碼再無 `flag_tang_commit`／`he`／`be`、`C_tang_ending_he`／`be` 引用；`"R_tang_ending"` 全檔只剩載入過濾嗰一次；`R_tang_ending:`／`pushSrc("R_tang_ending")`／WF2／WF5／CONTRA98 條目／收科回望「盟友以上／嗰個紅圈」已清；winter_finale 計數 12→11。
- 留線：HELD 3 節（行號寫死 L25650）、PUSH_CHROME／self-check／push 閘門／debugUnlockTangPush／事務所掣列表／WF5 業務覆寫／loadMock 呼叫照舊。
- 機制：`normaliseTangStub152` 在位（L31270）＋喺 TEXTFIX 之前行（L31414）、stub 新 synopsis／label／notes、push mock 過濾在位。
- TEXTFIX：開閘＋收尾條目已清（舊句只剩 normaliser 註解引文各 1 次）、玫瑰／腕表改純公事、共用「可與事業結局並存。」留返、實用禮物句留返、relMap 冇 rel_tang。
- Pack 唔郁：romance_tang.json／push mock／lan_xu stub 原稿／gift_react 玫瑰原句／gift_prefs tang 閘／seed（冇 commit 旗；push-ready 種子留返）逐項對照。
- **反證**：對 pristine main（`e08a070`）index.html 行，31 項刪項斷言乾淨 FAIL、零 crash；留線項全部 PASS（ discriminating 正常）。

### 5.2 舊測試更新（5 個，全部 PASS）
| 測試 | 改動 |
|---|---|
| `tests/test_wf2_81_static.py` | WF2 表在位斷言：`R_tang_ending` 改為不在 |
| `tests/test_wf2_81_logic.js` | 30→25 節點（刪 tang 行、HALF_END 刪 `R_tang_ending`、刪「鄧數字不變」段、merge WIRE 刪 romTang 並將 `R_tang_meet_stub` 改由 rom2 提供以續斷言 stub 唔被掂、applied 30→25） |
| `tests/test_wf5_87_logic.js` | applied 7→6；ending 關鍵句段改為斷言 WF5 表無 `R_tang_ending`；dengAll／年份檢查陣列刪 ending |
| `tests/test_contra98_static.py` | loader 行改無 romTang 版、計數 ≥12→≥11、23→22 節點 |
| `tests/test_contra98_logic.js` | FIX98 齊 23→22；`R_tang_ending` 全域守門豁免（§4.4）；PACK_FILES 留返 romance_tang.json 做數據 fixture（CONTRA98 表仲有 push2／crisis 兩行——測試 fixture 讀檔，唔係 live 載入） |

### 5.3 全套 A/B（`qa131/run_suite.sh`）
- pristine baseline（`e08a070`，全樹抽取 `~/workspace/pristine152-tmp/`，index.html hash 同 `e08a070` 一致）：**TOTAL PASS 211 FAIL 12**。12 項穩定 FAIL：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111／start53／weave43／weave44／weave49／wrap38（全部 static .py，pre-existing）。
  - 註：第一次 sparse 抽取（淨 `index.html content tests qa131/run_suite.sh`）跑出 201／22 係假象——漏咗根目錄 NOTES／assets 等檔案；全樹重跑先係 211／12（同 v156 記錄「基線係 211」吻合）。`/tmp` 係 512M tmpfs，全量抽取會爆滿；`git worktree add` 兩次失敗（`fatal: Could not reset index file to revision 'HEAD'`，同 v146 嗰種間歇性 git 寫入故障同類），最後用 `git archive` 抽去 home disk（623M）先成功。
- 工作版全套：**TOTAL PASS 164 FAIL 60**——數字波動，唔係回歸（v151 教訓：同一 repo 連續跑出 211／12、137／86、200／23；失敗項每次唔同、全部係 .py，逐個直接跑全部 PASS）。對照：
  - 12 項穩定 FAIL 全部保留（baseline 有、工作版一樣有；工作版冇少到任何一項）。
  - 額外 48 項全部係 .py static test，**冇一項係 tang 相關**（tang152／wf2_81／wf5_87／contra98 喺套件入面全部 PASS）。
  - 逐個直接覆驗 60 項 suite-fails：**PASS 46 FAIL 14**——14 項＝12 項穩定 FAIL＋2 項行號漂移（見下），其餘 46 項直接跑全部 PASS，證實係 suite 波動唔係回歸。
- **行號漂移 resync（v152 刪 −207 行引起，唔係邏輯回歸）**：
  - `tests/test_travel114_static.py`：44 個 openLoc( 呼叫點內容逐字一致、純漂移（`qa152/resync_travel114_152.py` difflib 核實）；COUNT／FREE／DEF／WRAPPER 行號已更新（DEF 53562→53355、WRAPPER 44171→43964），而家 PASS。
  - `tests/test_text125_static.py`：currentLine fallback 27800→27564、advance 27913→27677、applyFamilySafe 33516→33309（33518→33311），而家 PASS。
- 最終狀態：6 項 tang 相關測試（tang152／wf2_81 static＋logic／wf5_87 logic／contra98 static＋logic）＋2 項 resync 測試直接跑全部 PASS；12 項穩定 pre-existing FAIL 不變；零新增回歸。

### 5.4 實駕驗證（本地鏡像＋Playwright，`?softPreview=1&softBehaviorGate=1&softSeed=…`，`qa152/drive152.py`）
**OVERALL 3/3 PASS，0 pageerror**（三個 context 各 0 pageerror；截圖 `qa152/shots152/`，記錄 `qa152/drive152.json`）。
- **截圖說明**：`qa152/shots152/` 7 張圖已由 commit 拎走——佢哋全部影到同一個自動觸發嘅魏詠男首次巧遇畫面（`ENC83_DLG_ngai_wingnaam.first`，維港電影後巷，抉擇「拎支汽水俾佢／放低包紙巾／當冇睇到」），係種子狀態下每次返地圖即觸發（同 v138 review 記載「seed 晒冷卻都唔受壓制」嘅巧遇行為一致），唔係逐項測試嘅畫面，留低會誤導；主要證據係 `qa152/drive152.json` 嘅 DOM 文字記錄（對白逐句、旗標、反應句原文）。
- **T1 meet**（`seed_deng_meet_ready`，boot 自動開局＋自動播）：標題「排片室的冷酷算盤」，場景「龍頭院線排片部會議室，桌上堆滿各區戲院的入座率報表與午夜場數據。」；鄧麗萍開口「劇本係紮實，但院線唔係善堂，我要睇嘅係數字——套戲賣唔賣得，先講得落去。」；揀 data 抉擇（「即刻遞上做足功課嘅市場數據同票房預測」）後 `flag_tang_open=true`、`rel_tang=1`、`R_tang_meet` done；全程零禁詞（感情線／開閘／盟友以上／嗰個紅圈／跨越商業界線／應承佢嗰格／commit／he／be）。
- **T2 push**（`seed_deng_push_ready`）：push1「冷門檔期之賭」自動播（揀「攞試映情報，換佢手上嘅冷門檔資料」）→ 事務所行動表出 push2「午夜場後的試探」（揀 WF5 label「將票房紙推返去佢面前，齋講檔期同排片」）→ crisis「黃金檔期之爭」（揀 WF5 label「跟數據行：票房行先」）；`R_tang_push1／push2／crisis` 全部 done，`R_tang_ending` false，`flag_tang_commit` 未見；行動表冇 ending 掣（亦冇「年終的抉擇」）；全頁零禁詞。
  - 註：WF5 覆寫咗 push2／crisis 抉擇 label（mock 原句「只談檔期」→「齋講檔期」；「以票房為先」→「票房行先」），drive 初版用 mock 原句撳唔到，已改返 WF5 label。
  - 註：每次播完有「劇情結算」modal（掣「關閉」），要閂咗先返到地圖，否則之後撳地圖針無效——drive 已處理。
- **T3 送禮**（沿用 push-ready 狀態，`flag_tang_open` true；庫存播種 6 樣各 3 件；逐件推一日＋清 weekGiftGain 避開每日／每週上限）：
  - live `GiftShop.giveGift` 全部 ok:true；`canGive('tang')` ok:true。
  - 咖啡豆 live 行見到專屬句：「鄧麗萍：「咖啡豆……夜更對帳用得著。放那邊，我自己煮。」」（neutral entry，live 可達）。
  - 名筆／計數機／腕表／玫瑰專屬句經 `reactionEntry` 直接驗證（見 §6 點解 live 行唔到）：
    - 筆：「名筆。簽名、批檔期、改數字，都用得著。你至少知道我不是靠感人情書辦事的人。」＋「謝謝。下次如果你要談場次，直接帶報表，比帶花有用。」
    - 計數機：「桌上計數機……你觀察過我辦公桌。入座率、拆帳、場次，我都要即時核。」＋「實用。我鍾意睇得見、計得到嘅誠意。」（TEXTFIX 輸出）
    - 腕表：「正裝腕表。開會不能遲到，檔期也不能含糊——時間就是數字。」＋新句「我收下。錶係錶，檔期係檔期——我哋先把場次談清楚。」（唔見「感情條款」）
    - 玫瑰：新句「玫瑰？呢度係排片部，唔係花店。想傾檔期，帶數據嚟。」＋「花我不收。有話直說，有數直接列。」（唔見「綁架我的情緒」／「心軟」）
  - 全部反應句零禁詞。

## 6. 附帶發現：禮物專屬反應句 live 行唔到（pre-existing，唔係 v152 造成，等統籌決定）
- **現象**：live `giveGift('tang', …)` 嗰陣，名筆／計數機／腕表／玫瑰全部只出通用佔位句「佢接過禮物，點點頭收下。」（TEXTFIX 映射咗嘅 neutral placeholder），唔係佢哋嘅專屬句；淨係咖啡豆（同 memo）出到專屬句。
- **根源**：`content/gift_prefs.json` tang entry 嘅 `likes`／`dislikes` 皆空 → `prefKind('tang', …)` 永遠 `"neutral"` → `reactionEntry` 只查 `tang:<item>:neutral`（pen／calc／watch 只有 `:liked`、rose 只有 `:dislike`），查唔到又唔 fallback（fallback 只喺 pref≠neutral 嗰陣先生效）→ 跌入佔位句。v152 冇郁過 gift_prefs 亦冇郁過 lookup，所以係舊問題。
- **連帶**：玩家面暫時冇 UI 路徑送禮畀鄧麗萍——`MAP_NPC_TO_KEY` 得 vera／hiu／choi 三個（冇 tang），而佢亦唔係任何地點駐場 NPC（全檔只得 `residentNpc:"agent"`）；地點 panel 嘅「送禮：…」掣永遠唔會為佢出現。`openGiftPick` 亦唔係 global（主 script 係 IIFE），外面驅動唔到 pick-list modal。
- **對本票嘅影響**：§1.3 嘅 TEXTFIX 玫瑰／腕表改寫本身正確（§5.4 T3 經 `reactionEntry` 驗證咗輸出），但玩家喺 live 未必見到——要見到，先要將 likes／dislikes 填返（pen／calc／watch 入 likes、rose 入 dislikes），再加 UI 入口。填 likes／dislikes 涉及 content pack JSON，要經覆寫／merge 注入機制（唔直改），加埋 UI 入口已經超出「只刪感情線」範圍。**唔自己估，等統籌決定：係咪喺 v152 補埋，定另開一票。**

## 5. 統籌決定（rebase 上 main 9346a8e＋落地前）

- **Rebase**：基底由 `e08a070`（v148）rebase 上 `9346a8e`（v151 NOTES；中間落地 v156＋v151）。3 處衝突，全部喺 TEXTFIX55／relMap 一帶，用程式合併（`/tmp/merge152.py`，tokenizer 逐條目對位）：EXACT v151 改 1 條＋v152 改 8 條、NOTE v151 改 2 條＋v152 刪 4 條，**重疊 0**；PHRASES 拎走 `["關海媚","當紅花旦"]`（v151）；relMap＝v151 `rel_mei→關海媚`＋v152 刪 `rel_tang`。合併後驗證：`node --check` 主 script（4,300,418 bytes）SYNTAX-OK；v151 緋聞值「關海媚提醒頭條」在位、舊值「嗰位當紅花旦亦提過佢」已無；玫瑰新值、rel_tang 已刪、live `tang_commit`／`R_tang_ending` 零引用。
- **測試 resync**：travel114（`/tmp/resync152_rebase.py` difflib 核實 44 個 openLoc 呼叫點逐字一致、純漂移；DEF 53601→53394、WRAPPER 44205→43998；COUNT／FREE 13／27 不變）；text125（27815→27579、27928→27692、33550→33343）；tang152（25650→25665、31270→31285、31414→31429，全部＋15 跟 v156）。8 項相關測試重跑全部 PASS。
- **實駕重跑（rebase 後樹）**：`qa152/drive152.py` OVERALL 3/3 PASS，0 pageerror——T1 見面公事、flag_open＋rel 1、零禁詞；T2 push1→push2→crisis 逐節播、`R_tang_ending` false、零禁詞；T3 咖啡豆 live 見專屬句，筆／計數機／腕表／玫瑰經 reactionEntry 驗證（新公事拒絕句在位，唔見「綁架我的情緒」／「心軟」／「感情條款」）。
- **決定 1——`flag_tang_crisis_*` 留返**：R_tang_crisis 係生意節點（WF5 覆寫 label「齋講檔期」「票房行先」，實駕 T2 逐節播晒），佢三支旗係留低節點嘅抉擇追蹤旗，同 push1／push2 抉擇旗同類；拎走會整斷留低節點嘅追蹤。任務 brief 嘅刪除清單係按審計旗名寫，未分生意／感情，依實況修正。
- **決定 2——Seed 檔原封不動**：已驗證冇任何種子播 commit／he／be 旗；meta L32 舊 scope 描述（「Mock R_tang_push1/push2/crisis/ending」）留低咗，係 mock seed 入面嘅 dev 註解，唔係玩家面，唔郁。
- **決定 3——舊存檔死旗，唔做遷移**：舊檔若有 commit／he／be 旗，而家零讀取方，屬死旗，唔影響遊戲，唔開遷移清理。
- **決定 4——禮物專屬反應句 live 行唔到（pre-existing），另開一票，唔入 v152**：`gift_prefs.json` tang likes／dislikes 皆空 → `prefKind` 永遠 neutral → pen／calc／watch（`:liked`）同 rose（`:dislike`）查唔到 entry，跌入通用佔位句；連帶玩家面暫時冇 UI 路徑送禮畀鄧麗萍（`MAP_NPC_TO_KEY` 冇 tang、佢唔係任何地點駐場 NPC）。T3 已喺數據層驗證（reactionEntry＋giveGift ok），TEXTFIX 改寫本身正確；要玩家 live 見到，先要填返 likes／dislikes（經覆寫機制，唔直改 JSON）再加 UI 入口——超出「只刪感情線」範圍。
- **追加 resync——`test_kwan151_static.py`**：rebase 後全套初跑工作版 214／13（對照 214／12），多出嘅 1 項係 v151 測試（行號寫死，v152 刪行令錨點移位，內容本身無損）：逐項按內容搵返新行號（A 組 −235／−236、B／C 組 −242），重跑 ALL PASS。最終全套：對照 214／12、工作版 214／12，FAIL 清單逐項相同（12 項穩定 pre-existing），零回歸。
- **第二次 rebase（main 再郁：9346a8e → 8409178，v155＋v161 落地）**：index.html 自動合併零衝突；test_text125／test_travel114／test_kwan151 三份舊測試 resync（方法同上，difflib／內容核實純漂移：travel114 DEF 53632→53425、WRAPPER 44236→44029；text125 27846→27610、27959→27723、33581→33374；kwan151 A 組 −235／−236、B／C 組 −242）；tang152 三錨點 25665→25696、31285→31316、31429→31460。相關測試重跑全部 PASS；實駕重跑 3/3 PASS、0 pageerror。

## 6. 落地紀錄
- main commit `40702c7`（由 `9fde729` squash merge `v20a152`，分支 7 個 commit）；線上核實：5,229,214 bytes、sha256 `e73ddd44…`，同 repo 完全一致。
- 最終全套（main 8409178 對照）：對照 216／12、工作版 217／12（＋1＝新 test_tang152_static.py），FAIL 清單逐項相同（12 項穩定 pre-existing），零回歸。實駕 3/3、0 pageerror。
- 兩次 rebase：9346a8e（v151＋v156）＋8409178（v155＋v161）；衝突合併：TEXTFIX55／relMap 程式合併重疊 0；三份舊測試＋tang152 resync（difflib／內容核實純漂移）。
- 統籌決定：flag_tang_crisis_* 留返、seed 檔唔郁、舊存檔死旗唔遷移；禮物專屬反應句 live 行唔到（pre-existing：tang likes／dislikes 皆空＋冇 UI 入口）另開一票，唔入 v152。
