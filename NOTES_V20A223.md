# NOTES_V20A223 — v223 when 顯示值修復票（2026-11-15）

分支 `v20a223`，基底 main `5580f8d`（遊戲 v218）。修 CONTRA98／PA 覆寫表年份錯誤，
全部只改 `index.html` 覆寫表，絕對唔改 `content/` pack source（改 pack 會 double-shift）。
依據：`~/workspace/linji-story-coherence/DECISIONS-2026-11-15.md`「when 欄年份核查結果」一節。
出貨：checkout main → `git merge --squash v20a223` → commit → push main（經 deploy key，唔開 PR）。
唔改 SAVE key、softRev、產品 `?v=`。

## §1 改動清單（9 項：8 項＋統籌補改 1 行；改前→改後＝覆寫表舊曆值 → walk 後顯示值）

| # | 位置 | 改前（表值 → 顯示） | 改後（表值 → 顯示） |
|---|---|---|---|
| (1) | `ROMANCE_LAN_PA_OVERRIDES` R_lan_ending（L22437–22439） | `when "1990冬"` → 1992冬 | `when "1990秋"`＋`eraTag "era_1990_autumn_finale"` → **1992秋**（統籌補改，見 §2 追加決定；頁首由 eraTag 話事，唔跟改會留 1992冬） |
| (2) | `CONTRA98_WHEN_FIX` R_xu_ending（L31838） | `["1990冬","era_1990_winter_finale"]` → 1992冬 | `["1990秋","era_1990_autumn_finale"]` → **1992秋** |
| (3) | `CONTRA98_WHEN_FIX` R_hiu_crisis（L31843） | `["1990秋","era_1990_autumn_anni"]` → 1992秋 | `["1989秋","era_1989_autumn_anni"]` → **1991秋** |
| (4) | `CONTRA98_WHEN_FIX` R_hiu_ending（L31837） | `["1990冬","era_1990_winter_finale"]` → 1992冬 | `["1990秋","era_1990_autumn_finale"]` → **1992秋** |
| (5) | `CONTRA98_WHEN_FIX` R_choi_crisis（L31841） | `["1990冬","era_1990_winter_gossip"]` → 1992冬 | `["1989冬","era_1989_winter_gossip"]` → **1991冬** |
| (6) | `CONTRA98_WHEN_FIX` R_choi_ending（L31838） | `["1990冬","era_1990_winter_finale"]` → 1992冬 | `["1990秋","era_1990_autumn_finale"]` → **1992秋** |
| (7) | `CONTRA98_WHEN_FIX` 新增 R_tang_meet_stub（L31846–31848） | 無表項：pack `when 1991` → **1993**（玩家見唔到，純衞生） | `["1989秋","era_1989_autumn_capital"]` → **1991秋** |
| (8) | commit48 註解兩處（L42660、L42749） | 「1990 年秋起」「1990 秋起」 | 「1992 年秋起」「1992 秋起」；code `choice47SeasonReached(1992, "秋")` 本身啱，**零改動** |

- F4 已一致，唔使郁（核查依據已定）。
- `git diff`：只得上述 9 項（8 項＋統籌補改 1 行），`index.html` 1 檔，+12／−9；零其他行。
- pack 原值（harness 餵真 pack 核實）：R_hiu_crisis `when 1991`、R_choi_crisis `1991冬`、
  R_hiu／R_choi／R_xu_ending `1992`、R_lan_ending `1992`、stub `when 1991`——全部唔郁。

## §2 eraTag 決定＋覆核（本版最大發現：票面前提唔成立，結論反轉）

- 票面前提：「eraTag 唯一讀取方係 L27911 spSoftSeasonChar，輸入 `when + " " + eraTag`，
  when 行先所以 when 嘅季節永遠贏；新 tag 顯示上零影響。」
- **覆核結果：前提錯。** 除咗 L27911（soft-preview 路徑，when 行先）之外，仲有第二個讀取方：
  **`spPlayerMeta` L28002（LIVE 預設路徑，`const soft = String(node.eraTag||node.when||"")`——
  eraTag 優先）**。佢由 eraTag 抽年份（regex `\d{4}`）再由 `years66ShiftYear` 顯示前 +2，
  季節由 `spSoftSeasonChar(soft)` 抽（英文 autumn／winter 都認）。soft flag 係 opt-in
  （`?softBehaviorGate=1`／`?softPreview=1`／localStorage），正常玩家行 LIVE 路徑。
  實播頁首就係呢個函數（`StoryPlay` L28471 播句嗰陣、`pickerPlayerMeta` L28706），
  所以 LIVE 頁首嘅年＋季係由 **eraTag** 話事，唔係 when。
- 其他讀取方已排除：`["eraTag"]`／`['eraTag']` 括號讀取全檔 0 命中；`humanizeEraId`／
  `eraTagLabel`（L33398 起）只喺 `normalizeGigRecord`（通告物件），故事節點唔經過；
  `winter_finale`／`autumn_finale` 精確字串比對全檔 0 命中（無閘 key 住 eraTag 字串）；
  tests 入面 eraTag 只出現喺 spPlayerMeta 相關測試＋通告 fixture。
  `YEARS66_SKIP_KEYS` 含 eraTag（L31674），walk 唔郁佢，核實無誤。
- **結論（同票面 §3 後備指令相反，理由如下，留待統籌覆核）：**
  票面 §3 話「如果發現 spSoftSeasonChar 以外嘅讀取方，(2)(4)(6) 嘅 eraTag 改返唔郁」——
  呢個後備指令建基於「eraTag 顯示上零影響」嘅假設。實情係相反：**eraTag 一對改唔係可有可無，
  係令 LIVE 頁首正確嘅必要條件**。如果 (2)(4)(6) 淨改 when：when 變 1992秋／1991秋／1991冬，
  但 LIVE 頁首照舊出 eraTag 舊值——結局 `主線 · 1992冬`、危機 `主線 · 1992秋／1992冬`，錯晒。
  所以 (2)(4)(6) 照 §2 表一對改，唔執行後備指令嘅 revert。harness §B 實證：
  改晒之後六個目標頁首全部啱（見 §4）。
- 「era_1990_autumn_finale」改前全檔 0 命中，核實無誤；改後出現 4 次（R_lan／R_hiu／R_choi／R_xu_ending），
  顯示上嘅影響正正就係頁首由冬變秋——係修復本身，唔係副作用。

### 統籌追加決定（2026-11-15，覆核 §2 後）

- 統籌親自讀咗 `spPlayerMeta`（L28002 起）＋`StoryPlay` L28471 呼叫點，**確認 §2 結論正確**：
  LIVE 頁首 `const soft = String(node.eraTag||node.when||"")`，eraTag 優先；regex 抽年份再
  `years66ShiftYear` 顯示前 +2，季節由 `spSoftSeasonChar` 抽。票面「eraTag 唯一讀取方係
  L27911」嘅前提錯，(2)(4)(6) eraTag 一對改**唔 revert**，係必要條件。
- 同一邏輯，(1) R_lan_ending 嘅 eraTag 必須跟改：淨改 when 會令 when 1992秋、頁首 1992冬，
  唔符收票標準「6 個節點顯示年份正確」。統籌已補改 PA 覆寫
  `eraTag: "era_1990_winter_finale"` → `"era_1990_autumn_finale"`（一行，見 §1 (1)），
  harness §B 已由 6/7 變 7/7 PASS。呢個唔係擴範圍，係完成 (1) 本身嘅修復。

## §3 PA 覆寫次序覆核（通過）

- `refreshCopyPacksFromDisk`（L31918 起）真實次序：
  `STORY_WIRE.romance.lanXu = rom2` 賦值 → `applyStorySpineOverrides48()`（PA，L24331 附近套用，
  `ROMANCE_LAN_PA_OVERRIDES` 成個節點替換）→ `normaliseTangStub152(rom2)`（只改 synopsis／label／
  notes，唔郁 when；行喺 contra98 之前）→ `contra98FixNodeWhen([main, rom1, rom2, rival])` →
  `years66Walk([main, rom1, rom2, rival, ...])`。
- 所以 PA (1) 寫舊曆值 `1990秋` 正確，walk 之後先係 `1992秋`；唔使改寫做顯示值。
  R_lan_ending 唔喺 CONTRA98 表入面，PA 同 contra98 無衝突。
- stub (7)：`contra98FixNodeWhen` 覆蓋 `[main, rom1, rom2, rival]`，rom2 入面有 stub，
  加表就夠，唔使郁 `normaliseTangStub152`。

## §4 驗收

- **語法**：`node --check`——`index.html` 係 .html，Node 24 直接 check 會報
  `ERR_UNKNOWN_FILE_EXTENSION`；改抽兩個 `<script>` 區塊（L9–30、L6195–62895）合併驗，
  **SYNTAX OK**（v218 教訓跟進）。
- **harness** `qa219/harness_v219.js`（＋log `qa219/harness_v219.log`）：抽 index.html 真函數／真表
  （PA＋contra98＋years66＋normalise＋spPlayerMeta 簇，唔係手抄邏輯），餵真 pack
  （`content/story_detail_romance_*.json`＋主線＋對手線），按真實次序行
  （PA → normalise → contra98 → walk），另由 `git show 5580f8d:index.html`（v218 main 基底；
  原本用 HEAD，commit 之後 HEAD 已經係修復版，對照失效，統籌已改做 pin 死 SHA）抽舊表跑對照。
  **ALL PASS**（統籌補改＋harness 修正後重跑，log 已更新）：
  - A：7 個目標 when 全部啱（1991秋／1991冬／1992秋×4／stub 1991秋）。
  - B：LIVE 頁首 7/7 啱（R_lan_ending 頁首由殘留 1992冬變 1992秋，見 §2 追加決定）。
  - C：舊表對照證實修復實效——舊 when：危機 1992秋／1992冬、結局 1992冬×4、stub **1993**
    （stub 舊頁首 `主線 · 1993秋`，1993 bug 實證）。
  - D：其餘 **76 個**非目標節點 when／eraTag／頁首新舊表 0 差異。
  - E：CONTRA98 只改 5 項＋新增 stub 1 項，其餘表項原封不動。
- **針對性測試（全部 PASS）**：
  - `tests/test_years66_static.py`：23 PASS、FAILURES: 0。
  - `tests/test_weave47_logic.js`：ALL PASS（86 PASS）。
  - `tests/test_weave48_logic.js`：67 過／0 失敗。
  - `tests/test_cleanup100_logic.js`：ALL PASS（30 ok）。
  - `tests/test_wf5_87_logic.js`：PASS 52／FAIL 0（spPlayerMeta／eraTag 相關，順手覆驗）。
- **全套 suite A/B（獨立覆核＋測試跟進，2026-11-15）**：A（main 5580f8d）309／13；B 初跑 300／22——9 檔測試要跟有意改動更新（5 項斷言釘死舊錯值＋38 項純 +3 行漂移，零產品回歸證據）。測試跟進更新 9 檔（contra98 兩檔期望改新值：23 節點、危機 1991、結局 1992秋、冬 11／秋 12；tang152 `winter_finale` 11→8；其餘 6 檔釘行／總行數 +3，用 difflib 對位＋單次掃描 dict 查表，62 個釘行逐字核實；travel114 抽查例子 brief 數字寫錯咗，實測舊 41853→新 41856、舊 62236→新 62239，以 difflib 為準）。B 重跑 **309／13，FAIL 清單同基線 13 項一模一樣，零回歸**。

## §5 殘留

- **已解決**：R_lan_ending LIVE 頁首殘留——統籌已補改 eraTag（見 §2 追加決定），harness §B 7/7 PASS。
- 要 live 實駕先判到：七個目標節點實播頁首目視（harness 已斷言邏輯層，實機畫面未驗）。

## §6 rebase 到 v220 main（a45479e）＋改號受阻（2026-11-15）

- **rebase 成功**：`GIT_EDITOR=true git rebase a45479e`，3 個 commit 原樣落喺新 main 之上——
  `03b36ee`（實作）、`11e7bf4`（測試跟進）、`c7c2981`（NOTES §4）。`git diff 258dfae c7c2981`
  ＝恰好 v220 嗰 4 檔（NOTES_V20A220.md、content/events_zh_HK.json、
  content/story_beats_phase1.json、index.html 1 行），證明 rebase 零內容走樣；
  `git diff a45479e` 仍係本票 15 檔原有改動。
- **rebase 首試中途停過一次（已恢復，唔係內容衝突）**：第一個 pick（bd74628）嗰陣 git 報
  `Your local changes to index.html would be overwritten by merge`，工作樹本身乾淨；
  `git merge-tree --write-tree bd74628 a45479e` exit 0 無衝突，證實內容合併乾淨——
  係 checkout 新 main 嗰陣寫入 index.html 嘅 index stat 未 settled 導致誤判。
  `git update-index --refresh` 之後 `git rebase --continue` 一次成功，無手解任何衝突。
- **改號 v219→v221 受阻，未做**：`git branch -m v20a219 v20a221` 失敗——
  `fatal: a branch named 'v20a221' already exists`。`v20a221` 已有另一票在途：
  工作副本 `~/workspace/linji-work221`（語言審核 v2，index.html＋
  content/story_detail_c1_to_c17.json 有未 commit 改動，NOTES_V20A221.md 未追蹤），
  當時正跑緊 suite。**無用 `-f` 強行改名**，分支維持 `v20a219`，NOTES 檔亦未改名；
  等統籌決定新號碼（或同另一票協調）再改。qa219 目錄名不變。
- **rebase 後重新驗證（基底已變，全部重做）**：
  - harness `qa219/harness_v219.js`：**ALL PASS**、exit 0（控制對照繼續用
    `git show 5580f8d:index.html`，v220 冇郁 CONTRA98 表，對照仍然有效）。
  - 語法：兩個 `<script>` 區塊（L9–30、L6195–62895）`node --check`，**SYNTAX OK**。
  - 針對性測試全 PASS：years66 23 PASS／FAILURES: 0；weave47 ALL PASS；
    weave48 67 過／0 失敗；cleanup100 ALL PASS（30）；wf5_87 PASS 52／FAIL 0。
  - 全套 suite A／B：A＝新 main a45479e（臨時 worktree `linji-pristine-v221rebase`，
    驗完即刪），**309／13**；B＝rebase 後分支，**309／13**。A／B FAIL 清單一模一樣，
    同 v220 基線 13 項（flash51、giglib36、pacing35、poster59、rumor49、slot50、
    soft_tip_111_restore、start53、weave43、weave44、weave49、wf5_87、wrap38）完全一致，
    零回歸。Suite 數字無波動，唔使逐個覆驗。

## §7 第二輪 rebase 到 v221 main（7574287）＋改號 v219→v223（2026-11-15）
- **改號（rebase 前做，commit `b589a8e`）**：`git branch -m v20a219 v20a223`；
  `git mv NOTES_V20A219.md NOTES_V20A223.md`；NOTES 內自指改晒（標題、§1 分支、
  §6 出貨行）。§6「改號 v219→v221 受阻」嗰段歷史原樣保留；
  `qa219/` 目錄名＋harness 檔名唔改。v221／v222 均已被其他票佔用並在途／已落地，
  v223 核實未有人用，`~/workspace/linji-work223` 亦唔存在。
- **rebase**：`GIT_EDITOR=true git rebase 7574287`（v221 書面語改寫 P2），一次成功，
  **零衝突**，5 個 commit 全數 replay，新 HEAD `4d6d922`
 （c4965c4 實作、fce9b57 測試跟進、b300b2a §4、e6624f4 §6、4d6d922 改號）。
- **diff 核實**：`git diff cdedd48 4d6d922` 係 17 檔＝**v221 實際 16 檔**＋NOTES 改名 1 檔。
  留意：任務 brief 寫 v221 得 6 檔係唔齊——`git show 7574287` 核實 v221 實際仲有
  10 檔測試行漂移修復（cleanup100、contra98_static、gate136、story157_index／pack、
  story198_logic／static、text55、weave48_logic／static，全部 ±2–28 行，同 v221
  index.html 309+/309− 行數零變化一致）。本票內容零走樣：`git diff 7574287 4d6d922`
  15 檔同舊 `git diff a45479e cdedd48` 逐行比對，除 blob index 外完全相同，
  檔名單只差 NOTES_V20A219→V20A223。
- **rebase 後重新驗證（基底已變，全部重做）**：
  - harness `qa219/harness_v219.js`：**ALL PASS**、exit 0（24 PASS／0 FAIL；控制對照
    繼續用 `git show 5580f8d:index.html`，v221 冇郁 CONTRA98 表，對照仍然有效；
    rerun 後 log 檔 byte-identical，工作樹乾淨）。
  - 語法：兩個 `<script>` 區塊（L9–30、L6195–62895，行號同上一輪一致，v221 行數
    零變化）`node --check`，**SYNTAX OK**。
  - 針對性測試全 PASS：years66 logic ALL PASS＋static FAILURES: 0；weave47 logic
    ALL PASS＋static ALL PASS；weave48 logic 67 過／0 失敗＋static ALL PASS；
    cleanup100 logic＋static＋enc 全部 ALL PASS；wf5_87 logic PASS 52／FAIL 0。
    （wf5_87_static 係基線 13 項之一：hardcode 咗已刪嘅 `linji-work86` 路徑，
    `FileNotFoundError`，同本票無關。）
  - 全套 suite A／B：A＝新 main 7574287（臨時 worktree `linji-pristine-v223rebase`，
    驗完即刪），**309／13**；B＝rebase 後分支，**309／13**。A／B FAIL 清單一模一樣，
    同基線 13 項（flash51、giglib36、pacing35、poster59、rumor49、slot50、
    soft_tip_111_restore、start53、weave43、weave44、weave49、wf5_87、wrap38）
    完全一致，零回歸。Suite 數字無波動，唔使逐個覆驗。
  - 附註：第一次跑 suite A 唔記得傳 `run_suite.sh <root> <outfile>` 參數（ROOT／OUT
    留空），逐行寫入失敗但計數照出 309／13；已用正確參數重跑一次，數字相同，
    FAIL 清單以重跑為準（`cd ""` 喺呢個 bash 係 no-op exit 0，所以第一次計數本身
    係喺正確目錄跑出嚟嘅，但逐行紀錄已失，唔作準）。
- **未落地**：無 push、無 merge、無刪工作副本；等統籌落地。

## §8 落地核實（2026-11-15）

- **落地**：squash merge `v20a223` → main，commit `91e6365`，已 push（`cb4ea21..91e6365 main -> main`）；`git fsck` 無異常。
- **線上核實**：`curl` https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/index.html ＝ **5,572,129 bytes、sha1 `9dada4c95e0dd548c53ba46da30cc9369d2e3a68`**，同 `git show HEAD:index.html` 完全一致，部署已生效。
- **落地次序說明**：本票以 v223 落地；v222 另一票（`linji-work222`）落地嗰陣仍在途，落地次序將會係 v221 → v223 → v222（編號同落地次序輕微錯位，係平行票競爭所致，內容無影響）。
- **工作副本**：`git worktree remove ~/workspace/linji-work219`＋刪分支 `v20a223`，落地即清（見跟進 commit）。
