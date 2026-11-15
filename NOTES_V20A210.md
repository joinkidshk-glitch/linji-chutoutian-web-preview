# NOTES_V20A210 — 編號統一 C→N（遊戲側）

- 版本：v20a210。Base：main `5a647ee`（v227）。分支：`v210-c-to-n`。
- 範圍：主線章節編號 C1–C19／C6F 全套改做 N（置換表見下）；F4／G4 唔郁；主幹年份 +2 係另一票。
- 攻略側已於 live v91 完成（C18→N18 共 56 處、C19→N19 共 36 處）；呢票只做遊戲側。

## 置換表（已拍板，用戶 2026-11-15 17:43）

C1→N1、C2→N2、C3→N3、C4→N4、C5→N5、C6→N6、C7→N7、C8→N9、C9→N10、C10→N11、
C11→N8、C12→N14、C13→N16、C14→N13、C15→N12、C16→N15、C17→N17、C18→N18、C19→N19、C6F→N6F。

換位對（唔係順序，要單次掃描 dict 查表，絕對唔逐對 re.sub）：C8→N9／C11→N8、
C12→N14／C13→N16／C14→N13／C15→N12／C16→N15。

## 修正方案（CORRECTION.md 為準，原統籌方案 SUMMARY.md 有錯，只作參考）

第一手工人 DRY_RUN 發現原方案三類實質錯誤，停低零寫入，寫咗
`~/workspace/linji-v210/CORRECTION.md`。Parent 核實後拍板按修正方案做，
唔接受快但留低混淆嘅做法；舊存檔一定要遷移。

修正後分類器（`~/workspace/linji-v210/rename.py`，原版備份 `rename_orig.py`）：
- KW 拎走 8 個 review 詞（卡罅、角標、walkup、glamour、燕尾服、glyph、罅、牌底）；KW 加 `Beat`、`合併`。
- mapnote 分支收窄：只喺 `N<數字>＝` 之前先回 mapnote（`P1.5＝C5` 跌入正常分類，經 KW `done` 改做 N5）。
- 留守規則（放喺 quote／冒號／KW rename 規則之前）：`新 C<n>`（有 閘／Beat／章節喺附近就唔留守）、
  `守衛 C<n>`、`（C<n>）`半角括號 test 名、KEEP_WORDS 附近（卡罅、角標、walkup、glamour、燕尾服、glyph、罅、牌底、
  結果卡、字幕框、金碟夜、comfort、對比度、hash 比對、out 分支）、TEXTFIX case 名（`C<n> phrase`／`debt toast`／
  `press headline`）、節頭 `// C<n>：`／`# C<n>：`／`/* ---- C<n>：`（有章節詞就唔留守）、`見 C<n> 段`、
  `[A-BD-Z]\d+/(C\d+/)*` 群組標籤（例如 `# A9/C10:`、`B1/C1/C2`）。
- 窄版章節 rename 規則：`珍姐 C<n>`、`返 C<n>`、`掛 C<n>`、`＋C<n>＋`、`C<n>（<數字>`。
- FILES 加 6 檔：`content/gift_prefs.json`、`content/SANDBOX_BEHAVIOR_GATE_C1_C5_SOFT_STUB_v1.json`、
  `content/MOCK_STORY_DUAL_MEET_THICKEN_SOFT_v1.json`、三個鄧線 MOCK
  （MEET／MEET v1.1／PUSH）。
- 教訓：第一版 `[A-Z]\d+/` 群組規則誤傷真章節列表（index.html `（C7/C11/C8/C9/C10）`、`C18/C19` 被留低），
  已修正做 `[A-BD-Z]` 排除 C；再推廣到 `[A-BD-Z]\d+/(C\d+/)*` 令 `B1/C1/C2` 兩粒一齊留低。

審計（`~/workspace/linji-v210/audit_diff.py`，逐 token 比對新舊分類器）：
最終 DRY_RUN `{'mapnote-dropped': 54, 'leave': 651, 'rename': 4761}`、**LEFTOVER＝0**。
翻查 326 個 flips：366 個 rename→leave 幾乎全部係真 review／ticket／case 標籤
（awards187／190、story198、rom183 等）；含章節詞（閘／Beat／章節／主線／節點／合併／done_）嘅 21 個 flip
逐個核實全部係標籤；22 個舊 LEFTOVER 全部有正確去向（16 leave＋7 rename：
story157 C11→N8、weave48 C7→N7、wf4_203 C6F→N6F、cleanup100 珍姐 C9→N10 ×2、rival C3→N3、
DUAL_MEET 掛 C3→N3；另 mapnote `P1.5＝C5`→N5）。index.html flips 得 6 個，全部正確
（1 個 mapnote→rename＋5 個真標籤留低：glamour trade-off C2、ROM183 C1／C2／C3／C6 節頭）。
6 個新 content 檔 67 個 token 全部 rename、0 leave。
原分類器基線 DRY_RUN：`{'mapnote-dropped': 54, 'leave': 333, 'rename': 4989, 'LEFTOVER': 22}`。

## 實跑

- rename.py 實跑數字同 DRY 一致（4,761／651／LEFTOVER 0）；`node --check` PASS（兩個 inline script 塊，抽出嚟 check）。
- 148 檔改動（未計下面手動修復同測試更新）。

## regex／replace 手動修復（18 行／19 處，全部核數）

`/^C\d+$/`→`/^N\d+$/` ×12、`evalToken` 嘅 `/^(C\d+|R_[\w]+|A_[\w]+)$/`→N、
`/need_done:(C\d+)/`→N、setting strip `(對齊|C\d)`→N、`coversNode` `/^C([1-9]|1[0-7])$/`→N、
`storyActLabel` `/^C(\d+)$/`→N、`.replace(/^C/,"")`→N ×2（L45344／45390）。
注意：CORRECTION.md 只列 14 處，實查仲有 evalToken、need_done、setting strip 3 處。
`tests/test_story165_static.py:69` 已同步做 `/^N\d+$/`，test 名「只取 C*」→「只取 N*」×2
（L9 註解＋L68 test 名）。核實：index.html 再無 `/^C` 章節 regex；
tests 只剩 `test_story191_static.py:106` 反向斷言（正確，唔使郁）。

## 檔名改名

- `content/story_detail_c1_to_c17.json`→`story_detail_n1_to_n17.json`（小寫 c，分類器從來冇掂過佢）
- `content/SOFT_PROGRESS_SEED_C3_C5_DENG_v1.json`→`..._N3_N5_...`
- `content/SANDBOX_BEHAVIOR_GATE_C1_C5_SOFT_STUB_v1.json`→`..._N1_N5_...`
  （連 code 引用 L31945 get()、L32078／L39150 錯誤字串一併改）
- `tests/fixtures/spine_c6_c17_v136.json`→`spine_n6_n17_v136.json`
  （fixture 內容本身已係 N：42 個 N id、0 個 C id）
- `SANDBOX_C1_FUSION_DRAFT_v1.json`（草稿，唔載入）唔郁。
- `*.md` 歷史文件唔郁。
- 已更新嘅引用：index.html 6 處 story_detail、`tests/audit_wf5.js:61`、
  `test_br89_logic.js:50`、`test_cleanup100_logic.js:81`、`test_cleanup100_static.py:115`、
  `test_gate136_static.py:108`、`test_wf1_80_logic.js:4`＋`:50`（spine）。

## 測試更新（分類器掃唔到嘅構造式 id／舊檔名，逐個修，全部逐個跑過 PASS）

- `test_story191_static.py:82`、`test_c17route153_static.py:96`：order71 期望值
  `'C%d'`→`'N%d'`，尾段要寫明換位後播次序
  `['N7','N9','N10','N11','N8','N14','N16','N13','N12','N15','N17']`（唔係 N7–N17 順序號）。
- `test_progress71_logic.js:201／264`、`test_story198_logic.js:327／339`：
  種子 `done['C'+n]` 按對照表改做 `done[C2N210['C'+n]]`（C2N210 map 寫喺檔內；
  唔可以用 `'N'+n` 直代，換位集唔同——例如 done14 係 {N1–N11,N13,N14,N16} 唔係 {N1–N14}）。
- `test_story157_index_static.py:186／187`：`blob(C17)`→`blob(N17)` ×2（變數定義已改 N17，用處漏咗）。
- `test_story157_pack_static.py`：預設路徑改做新檔名；nodes[5:] sha 由
  `fa95df…` 改做 `1a0f1be4…`——79 行改動逐行核實全部只係 C<n>→N<m> 純改名（0 行非純改名）。
- Fixture 改名（內容本身已由分類器改做 N，舊檔名留低係混淆，一併改）：
  `tests/fixtures/story_detail_c1_to_c17.json`→`story_detail_n1_to_n17.json`、
  `tests/fixtures/behavior_gate_c1_c5.json`→`behavior_gate_n1_n5.json`；
  更新 8 個讀者：progress71／story191／story198／verify37／weave410／weave46／weave48／wf5_87_logic
  （wf5_87_logic 嗰個讀嘅係 `content/`，唔係 fixtures）。
- `test_weave45_static.py:68`、`test_v155_static.py:17`：index.html 入面 pack 名斷言改做新名。
- `test_wf5_87_static.py:83–85`：ROOT 路徑改做新名（BASE 係 v86 凍結副本，舊名不變）；
  註明尾段對照喺 v210 之後就算 BASE 喺度都唔會過（要先映射再對照），而 BASE 目錄本身已唔存在，
  呢個測試喺基線已經係穩定 FAIL，唔喺呢票修。
- 唔郁嘅：`_v157_allowed` 歷史豁免（v157 當時個檔就係叫舊名，改咗等於改歷史）；
  4 個 guard 測試嘅 `_v210_allowed` 本來就要舊名新名一齊列（git status 見到 D 舊名＋?? 新名）；
  `tests/fixtures/spine_c6_c17_v79.json`（孤兒 fixture，已還原做原始 C 內容，檔名同內容一致，係凍結歷史）。

## Content guard 測試 v210 豁免（18 條 path）

`tests/test_aud91fix122_static.py`、`test_aud91fix124_static.py`、`test_gigreq110_static.py`、
`test_newspaper214_award_static.py` 全部加 `_v210_allowed`（12 個改動檔＋3 個舊名＋3 個新名），
4 個 guard 測試逐個跑過 PASS。注意：gigreq110 用 `git diff --name-only HEAD`
（只見到刪走嘅舊名，見唔到 untracked 新名），其餘三個用 `git status --porcelain`
（見到 D 舊名＋?? 新名），所以豁免集要舊名新名一齊列。

## 舊存檔遷移（必做，唔遷移會成個章節進度歸零）

核實：`markDone(id)` 做 `st.done[id] = true`——`S.story.done` key 係**裸章節 id**
（`C5`、`C10`、`C6F`），唔係 `done_C*`（CORRECTION.md 呢句寫錯）。
`done_C10`／`story_C10` 只喺 anti-stack `softC10WindowActive`（L47213–47215）讀 `S.flags` 嗰陣做舊格式防禦。
`lastMainDoneId` 只寫唔讀（L24954）。`calib60Missed` key 係節點 id；
`storyGate113Scrub`（讀 `STORY_GATE_3Y` 閘 key）同 `calib60MissedScan`
（讀 `CALIB60_NODE_WINDOWS` key）喺改名後讀 N id。

新函數 `c2n210MigrateSave(o)`（跟 `years66MigrateSave`／`jan67MigrateSave`／
`levels75MigrateSave` 同一 pattern；CORRECTION.md 話「migrat 0 命中」係錯，呢三個函數本身存在）：
- remap `o.story.done` 裸鍵 C→N 全表（含 C6F→N6F；OR 合併、冪等）、`o.story.lastMainDoneId`、
  `o.calib60Missed` 鍵、`o.flags` 嘅 `done_C<n>`→`done_N<m>` 同 `story_C<n>`→`story_N<m>`（防禦性）。
- 呼叫位：normalizeSaveObj 入面、levels75MigrateSave 之後、storyGate113Scrub 之前
  （亦喺 calib60MissedScan 之前）；try/catch 包住，跟鄰近寫法。
- 遷移喺 rename 實跑之後先加（寫死舊→新對照，唔可以俾分類器再改一次）。
- 非章節鍵唔郁（C20、`done_tv_01` 通告旗、R_ 前綴）；空物件／null 唔拋錯。

邏輯測試 `tests/test_story210_migrate_logic.js`（12 項，全 PASS）：
舊存檔播種（done 含 C5／C8／C11／C6F、`done_C10` flag、`calib60Missed` 含 C9、
`lastMainDoneId: "C5"`）經遷移後對照 N key；換位對唔互撞；OR 合併；冪等；
normalizeSaveObj 呼叫次序靜態斷言（levels75 → c2n210 → storyGate113Scrub → calib60MissedScan，
用呼叫式 `(o)` 搵，唔用裸名——L30 註解提到 calib60MissedScan，裸名 indexOf 會搵到註解先）。

## 重數（兩口徑）

| 口徑 | 改前（base 5a647ee） | 改後 |
|---|---|---|
| raw `\bC(1[0-9]\|[1-9])\b` — index | 1,047 | 196 |
| raw — content（15 檔） | 524 | 12 |
| raw — tests | 3,215 | 574 |
| MASTER `C(6F\|1[0-9]\|[1-9])(?![A-Za-z0-9])` — index | 1,322 | 357 |
| MASTER — content（15 檔） | 658 | 49 |
| MASTER — tests | 3,758 | 716 |

改後殘留全部核實，唔係漏改嘅章節 id：
- index.html 357 處：全部係 review／ticket／case 標籤（`v20a197 C2`、`v20a187 C6`、`C1：` 節頭等）；
  live 章節 id 形狀（`"C<n>"`、`C<n>_`、`done_C<n>`、`story_C<n>`、`prevMain: "C`、`needDone: […"C`）全 repo 0 命中。
- content 49 處：base64 圖數據（news_images_v82，20 處）、schema 設計散文／欄位名
  （`parallelWithC10`、`playtestEconomyWeekC2`、`lockedFlagsC1C5`、`scope: "C1-C17"` 範圍寫法、
  `C5 dodge=0；C3 hard 可−1`、`C2 Soft 行為閘` 等，呢啲檔唔喺 rename FILES 入面，係 DEV 文件）、
  `rivalGaoMixC5` 旗名、HINT map 版本標籤（`HINT_C1C5_MAP_v1`、`HINT_C6C10_v1`，歷史版本名）。
  另 `SANDBOX_C1_FUSION_DRAFT_v1.json` 草稿凍結唔郁（14 處，檔名＋內容都係舊 C）。
- tests 574／716 處：review 標籤（test 名入面嘅 `v20a187 C3` 等）、
  新遷移測試故意播種嘅舊 C 存檔、guard 豁免清單、v157 歷史註解、v79 fixture 原始內容。

## Suite

- Suite A（pristine main 5a647ee，worktree `~/workspace/pristine-v210-main`）：**312 PASS／13 FAIL**——同 v227 基線完全一致。
- Suite B（工作副本，第一跑）：307／19——多咗 6 個 FAIL，全部係行號釘漂移（見下），唔係功能回歸。
- 6 個回歸根因：v210 喺 index.html 淨加 40 行（c2n210MigrateSave 函數 ＋36 行＠舊 L36730 之後＋呼叫點 ＋4 行＠舊 L33790；
  difflib 對位核實：除咗呢兩處插入，其餘全部係等行數 replace，純改名，零刪除）。漂移帶：≤舊 L33789 者 ＋0、
  舊 L33790–36729 者 ＋4、＞舊 L36729 者 ＋40。6 個測試全部按呢個映射更新釘行＋補 v20a210 resync 註解：
  gift185（總行數 63134→63174）、tang171／tang173（總行數＋openLoc DEF 57529→57569）、
  rom176（4 釘：55959→55999、56327→56367、57466→57506、57560→57600；6360／31963 唔郁；
  check 名入面舊 L 號係歷史標籤，唔跟住改）、text125（b.text 分支 33952→33956，＋4 帶）、
  travel114（FREE 25 處各 ＋40、COUNT 36071→36075（＋4 帶）＋其餘 10 處各 ＋40、32564 唔郁、
  DEF 57529→57569、WRAPPER 45643→45683）。逐個跑過 PASS。
- Suite B（工作副本，第二跑，釘行修復後）：**313 PASS／13 FAIL**——13 項同基線一模一樣
  （flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／
  weave43／weave44／weave49／wf5_87／wrap38；wf5_87 係 BASE 目錄已刪嘅環境性 FAIL，基線已有），
  ＋1 係新測試 `test_story210_migrate_logic.js` PASS。**零回歸**。
- 相關測試逐個覆驗（story165／story191／wf4_203／cleanup100／rival_rematch／weave48／
  progress71／story198／c17route153／story157 index＋pack／verify37／weave410／weave45／weave46／
  v155／wf5_87_logic／4 個 guard／story210 migrate）：全部 PASS。

## 落地

- main HEAD：見 `git log`（squash merge 原 commit `703941d`，分支 commit `75e0a5a`；
  為補呢節落地數字 amend 過一次，HEAD 已變，index.html 內容不變）。
- push main：`5a647ee..703941d`，GitHub `ls-remote` 核實一致。
- 線上核實：https://joinkidshk-glitch.github.io/linji-chutoutian-web-preview/index.html
  5,590,213 bytes、sha1 `bb66b11f23b4492355262b3569a40b23878a4b6e`，同 main `index.html` 逐 byte 相同
  （`c2n210MigrateSave` ×2 在場；第一次 curl 仲係舊版 v227，隔 4 分鐘後見新版，Pages 傳播正常）。
- 工作副本 `linji-work210`＋分支 `v210-c-to-n`＋pristine worktree 已刪。
- Live drive：未跑——瀏覽器自 2026-11-15 08:48 起已死，等恢復後補跑（同 v225／v226／v227 一樣押後）。
