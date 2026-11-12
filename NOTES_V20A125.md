# NOTES_V20A125 — StoryPlay 讀埋 `text` 單句 beats（TEXT125）

- 合併：分支 `v125-textbeats`（tip `d48df67`，基底 main `1255f18` v123；合併嗰陣 main 已行前到 `e957022` v124 NOTES，squash 無衝突）→ squash 入 main **`b41d2cd`**，已 push。
- 線上核實：本地 index.html **5,161,148 bytes**／sha256 `8f08858aff911075…`；push 後即刻 curl 線上 200、5,159,938 bytes、sha `e771c824…`（舊版 v119，未部署）——Pages 部署滯後已知毛病，推本 NOTES commit（`4105933`）重觸發後約 3 分鐘再驗，線上 **200、5,161,148 bytes、sha `8f08858aff911075…`，對上**。
- 測試：全套 A/B——pristine main（`1255f18`）**171 PASS／12 FAIL** vs 工作版／合併後樹 **173 PASS／12 FAIL**，零新增回歸；新 PASS 得 2 個新守門（`test_text125_logic.js`、`test_text125_static.py`，含反證）；另 `test_travel114_static.py` 行號 resync（見 §3）。
- 實駕：Playwright 390×844、`?softPreview=1`、本地鏡像（工作副本 `python3 -m http.server 8978`），**12/12 節點 PASS＋C2 對照 PASS、0 pageerror**（見 §2）。
- 回滾：`git revert b41d2cd`（squash 單一 commit；index.html＋2 新測試＋travel114 resync 一併還原）。

## 1. 改咗咩（index.html 淨 +12 行，揀咗修法 (b)）

- **修法揀 (b) 播放器讀埋 `text`，唔揀 (a) 逐句轉 `lines`**。原因：
  - (a) 要改 77 句 literal beats（5 個位：CHOICE47／WF3／COMMIT48／WF4 intro／WF4 送別 builder 入面嘅 `beats.push`），連動態砌出嚟嘅送別 beats 都要逐行改，將來再有 `text` beats 又會再斷。
  - (b) 只係 `currentLine()`／`advance()` 加 `text` fallback（`lines＞line＞text`），一次過修晒全部現行＋將來嘅 `text` beats；節點數據零郁（五表零 `lines:`／`line:` 鍵，static test 釘死），content pack JSON 更加冇掂過（五表本身就喺 index.html 入面，唔係 JSON）。
  - 全庫零 beat 同時有 `lines`／`line`＋`text`，fallback 次序唔會改任何現行 beat 行為；傳聞／情報／獎勵等其他 `text:` 欄位唔經 `currentLine()`，唔受影響。
- **三處改動**（全部有 `TEXT125` 標記，static test 數住恰好 3 個）：
  - `currentLine()`（約 27423 行）：`const lines = … (b.line ? [b.line] : (typeof b.text === "string" && b.text ? [b.text] : []))`。舊版 `text` beats 逐句回 null → `render()` 即跳 `mode=choices`，對白成段唔顯示。
  - `advance()`（約 27526 行）：同一 fallback，`lineCount`／推進同顯示一致（單句 text beats 本來行 beat-by-beat 都啱，但唔對齊會有隱性唔一致）。
  - `applyFamilySafeToNode()`（約 33141 行）：`b.text` 行返同一套替換（抽煙→歇息／食煙→傾偈／買醉→夜歸散心／臨時演員路邊抽煙長句）。現行 5 表入面冇呢啲詞，今日行為不變，防將來漏網。
- **唔郁**：SAVE key（`starVolunteer_map_v19w`）、softRev、產品 `?v=`（static test 釘死）。

## 2. 實駕結果（逐節點，全部逐句核對講者＋行字＝原文 beats 順序）

驅動：`qa125/drive125.py`（節點由 `qa125/extract_nodes125.py` 從工作副本 index.html 原文逐字抽出，`qa125/nodes125.json`＋`nodes125_farewell.json`）；log＋截圖留喺工作副本 `qa125/`（唔入 repo）。

| 節點 | beats | 選項 | 結果 |
|---|---|---|---|
| F4_stay_mind（何生問：走定留） | 4/4 | 3 | PASS |
| G4_family_job（阿媽） | 4/4 | 2 | PASS（揀第一項出「劇情結算」modal，結算唔含 resultBeats 行字） |
| W3_ho_liao | 6/6 | 2 | PASS |
| W3_ho_m27 | 6/6 | 0 | PASS（零選項，出「完成這一節」掣） |
| W3_liao_m27 | 7/7 | 2 | PASS |
| W3_lu_pa（場務姐姐） | 6/6 | 0 | PASS（零選項，出「完成這一節」掣） |
| W3_fong_jump | 9/9 | 2 | PASS |
| W3_fong_hold | 9/9 | 2 | PASS |
| CMT_hiu_commit（曉晴天台） | 4/4 | 2 | PASS |
| CMT_choi_commit（采兒茶餐廳） | 4/4 | 2 | PASS |
| WF4_fen_intro（芬姐茶水帳） | 6/6 | 2 | PASS |
| WF4_fen_farewell（啟德送芬姐，中性變體） | 8/8 | 2 | PASS |
| C2 對照（lines-beats 舊形） | 頭 3 句 | — | PASS（舊形不變） |

- **0 pageerror**。8 個 console.error 404 全部係既有表情候補鏈缺檔（`crew_laolinji_serious`、`ho_sang_surprise`、`liu_bingxing_sad`、`fong_siulung_smile`、`extra_ad_fen_serious` 各 webp＋png，磁碟上本身冇呢啲檔），全部有後備、畫面無破圖，同 TEXT125 無關（v119 實駕同類 404 亦已記錄；`liu_bingxing_shy` v123 已補，今次撞到嘅係 `sad`，另一缺口）。
- **送別 builder 唔係全域**：`wf4FenFarewellNode`／`choice47Play`／`wf3TalkPlay`／節點表全部喺 IIFE 內，`evaluate` 叫唔到（v119 已知同一限制）——送別節點由 builder 原文砌中性變體（fresh 檔：flags 全無、wo＝ex＝false；literal 4＋中性 variant 1＋trailing 3＝8 句，choices 2 個連 resultBeats 照抽），播嘅係同一條 StoryPlay 渲染器。

## 3. `text` beats 全庫普查（static test 釘死數字）

| 表 | beats（玩家可見） | resultBeats（引擎從來唔讀） |
|---|---|---|
| CHOICE47_NODES（F4 4＋G4 4） | 8 | 11 |
| WF3_TALK_NODES（6＋6＋7＋6＋9＋9） | 43 | 24 |
| COMMIT48_NODES（4＋4） | 8 | 8 |
| WF4_FEN_INTRO_NODE | 6 | 4 |
| wf4FenFarewellNode（literal 4＋push 8 行 code） | 運行時 8–11（中性變體 8） | 3 |
| **合計** | **73–76** | **50** |

- **86 句更正（無肖像盤點）**：任務書／v119 報告話 CHOICE47＋WF3 共 86 句「live 句數」要扣返——準確啲講，86 句＝19＋67（beats＋resultBeats）。玩家實機真正唔顯示嘅係 **beats 51 句**（CHOICE47 8＋WF3 43）；resultBeats 35 句（11＋24）引擎從來唔讀（`applyChoice`／`showResult` 只讀 `effects.notes`，sandbox JSON 亦寫明 optional／忽略），唔係「顯示唔到」，係從來唔係對白。連 COMMIT48／WF4 一併計，玩家實機唔顯示嘅 text-beats 總數係 **73–76 句**（今次全部修好）。盤點檔本身唔改，數字更正寫喺呢度。
- **travel114 resync**：TEXT125 令 index.html 淨 +12 行（currentLine +4／advance +1／familySafe +7），`test_travel114_static.py` 寫死嘅行號跟 `qa125/resync_travel114.py`（difflib 對位）重算：44 個 `openLoc(` 呼叫點內容逐字一致、次序一致，COUNT 13／FREE 27 不變（FREE 24421 唔郁；27878→27883 等 +5／+12 兩檔漂移；DEF 52777→52789、WRAPPER 43629→43641）。

## 4. 測試（新守門 2 檔，含反證）

- `tests/test_text125_logic.js`（24 斷言）：由 index.html 抽 `currentLine`／`advance`／`applyFamilySafeToNode` 真身 eval。text 旁白／阿媽／阿偉句顯示、3 句行完轉 choices、lines 多行／line 單句／空 beat 不變、lines＞line＞text 優先次序、空字串 text 唔當一行、familySafe text 同 lines 同一套替換＋唔郁原節點＋關閉原樣回傳。**反證：同一檔對 pristine main 跑，3 項 fallback 斷言 FAIL。**
- `tests/test_text125_static.py`（18 斷言）：fallback 行號（27423／27526／33141，rebase 重對）、五表普查數字、五表零 `lines:`／`line:`、全庫零 beat 並存 lines／line＋text、SAVE／softRev／`?v=` 不變。**反證：抽走任一 fallback／WF3 少一句，checker 必須報錯；對 pristine main 跑 FAIL。**
- 全套：pristine `1255f18` 171／12 → 工作版／合併後樹 173／12；12 FAIL 係既有清單（flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38），兩邊逐字一致。

## 5. 檔案清單（合併內容）

- `index.html`（＋15／−3 行，TEXT125 三處）
- `tests/test_text125_logic.js`、`tests/test_text125_static.py`（新）
- `tests/test_travel114_static.py`（行號 resync，內容逐行一致）
- 工作副本留檔（唔入 repo）：`qa125/`（`run_suite.sh`、`suite_pristine125.txt`、`suite_work125*.txt`、`suite_merge125.txt`、`resync_travel114.py`、`extract_nodes125.py`、`nodes125.json`、`nodes125_farewell.json`、`drive125.py`、`drive125_log.json`、`shots/` 4 張）

## 6. 殘留缺口（唔擋合併）

1. 5 個表情檔缺失（見 §2 404 清單：`crew_laolinji_serious`、`ho_sang_surprise`、`liu_bingxing_sad`、`fong_siulung_smile`、`extra_ad_fen_serious`），補圖嗰陣一併做；`ho_sang_angry`、`liu_bingxing_shy` 已喺 v123 補好。
2. resultBeats 50 句繼續唔播——引擎設計本身唔讀（只出 `effects.notes`），唔係 bug；將來要播 resultBeats 對白要另開一票改 `pickChoice`／`showResult`。
3. 送別變體只驗咗中性變體（8 句）；tea／help／wroteOff／exodused 變體行同一條 `text` fallback，邏輯上已覆蓋，未逐一實駕。
4. 線上核實已補（見頂部：推 NOTES 後約 3 分鐘，線上 byte／sha 對上）。
