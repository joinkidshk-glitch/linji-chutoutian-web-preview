# v20a157 Rebase Resync 報告（rebase 上 origin/main `60b0a8f`）

- 工作副本：`~/workspace/linji-work157/`，分支 `v20a157`，rebase 後 HEAD `171829a`
- Rebase 前 v157 commit：`d64887c`（基底 `e08a070`）；rebase 基底：`60b0a8f`（v166 NOTES）
- Resync 腳本：`qa131/resync_rebase157.py`（difflib 對位＋單次掃描 dict 查表一次過換；唔逐對 re.sub）
- 日期：2026-11-13

## 1. Rebase diff 核實（splice 內容有冇俾 rebase 沖走）

- `git diff 60b0a8f..HEAD --stat`：38 檔，`index.html` ＋874／−？行、`content/story_detail_c1_to_c17.json`、NOTES、qa131 證據檔、15 張截圖、12 份測試檔。
- 新內容標記（HEAD `index.html` vs rebase 前 `d64887c`，逐個數完全相同）：
  - 「角落嗰張枱」12、「阿媽煲咗湯」3、「收科嗰晚」6、「片場老油條」1（pack 另有 3 處）。
- Splice 實質 0 diff（逐行集合比較，rebase 前 `e08a070..d64887c` vs rebase 後 `60b0a8f..171829a`）：
  - `index.html` 增行集合 472 行完全相同；刪行集合 402 行完全相同。
  - pack 增行集合 389 行完全相同（`git diff … | grep '^+' | sort` 零差異）。
- **結論：splice 內容完整，rebase 無沖走任何嘢。**

## 2. 釘行測試普查（邊啲檔釘死 index.html 行號）

方法：grep 全部 `tests/*.py`／`*.js`（`line(N)`／`lines()[N]`／`ls[N]`／`_LINE ＝ N`／集合字面量／括號數字），再逐檔睇斷言係咪真係讀指定行。

**有 live 釘行：只得 4 檔**（其餘全部用 marker／內容搜尋，唔靠行號）：

| 檔 | 基底 | 釘行數 |
|---|---|---|
| `tests/test_travel114_static.py` | `d64887c`（rebase 衝突取咗 v157 版） | 42（COUNT 13＋FREE 27＋DEF＋WRAPPER） |
| `tests/test_text125_static.py` | `d64887c`（rebase 衝突取咗 v157 版） | 3 |
| `tests/test_kwan151_static.py` | `60b0a8f`（由 main 嚟，splice 令佢漂移） | 13 |
| `tests/test_tang152_static.py` | `60b0a8f`（由 main 嚟，splice 令佢漂移） | 3 |

**查過、確認無 live 釘行嘅檔**（內容／marker 定位，唔使 resync）：
`test_aud91fix122_static.py`、`test_aud91fix124_static.py`、`test_gigreq110_static.py`、`test_gate136_static.py`、`test_weave46_static.py`、`test_weave47_static.py`、`test_weave48_static.py`、`test_weave48_logic.js`、`test_wf1_80_logic.js`、`test_wf5_87_static.py`、`test_story157_index_static.py`、`test_story157_pack_static.py`，以及 main 來源嘅 `test_awards62_*`、`test_awards63_static.py`、`test_br89_static.py`、`test_cleanup100_enc.js`、`test_dlg119_static.py`、`test_enc79／83／84／144_*`、`test_fix65_*`、`test_guidance34_*`、`test_locpanel118_static.py`、`test_terms57_logic.js`、`test_text55_logic.js`、`test_text125_logic.js`、`test_venue99_*`、`test_weave49_*`、`test_wf3_82_logic.js`、`test_wf5_87_logic.js`、`test_awards160_m9_static.py`、`tests/audit_wf5.js`（`lines[0]` 係 beat object、`WIN_LINE`／`VENUE99_LINE` 係值常量，唔係行號）。

## 3. Resync 表（difflib 對位，逐行內容逐字相同＝純漂移）

對位總覽：
- 基底 `d64887c` → HEAD：58,975 行 → 59,023 行；insert ＋247／delete −240／replace 60 段（舊 82 行→新 123 行）；淨 ＋48。
- 基底 `60b0a8f` → HEAD：58,953 行 → 59,023 行；insert ＋66／delete −51／replace 159 段（舊 387 行→新 442 行）；淨 ＋70。

### 3.1 `test_travel114_static.py`（基底 `d64887c`，42 錨點）

| 舊行 | 新行 | 漂移 | 內容（首 80 字） |
|---|---|---|---|
| 24796 | 24612 | −184 | setTimeout 劇情播完刷新 |
| 28291 | 28106 | −185 | leaveStory 劇情播完刷新 |
| 30919 | 30728 | −191 | openLoc("hospital", {travelFree:true})「唔住」 |
| 30920 | 30729 | −191 | onDismiss openLoc hospital travelFree |
| 30932 | 30741 | −191 | openLoc hospital travelFree「好，返去開工」 |
| 30933 | 30742 | −191 | onDismiss openLoc hospital travelFree |
| 30944 | 30753 | −191 | openLoc hospital travelFree「明白」 |
| 30945 | 30754 | −191 | onDismiss openLoc hospital travelFree |
| 31048 | 30857 | −191 | openLoc(atLoc, {travelFree:true}) 故事 seed |
| 32198 | 32061 | −137 | openLoc(locId) ux68GoLoc 手帳「前往」 |
| 35679 | 35542 | −137 | openLoc(target.locId) 訓練建議「去報名」 |
| 37806 | 37669 | −137 | openLoc(L.id) 訓練報名導航 |
| 38800 | 38663 | −137 | openLoc(locId) 進度頁「去現場播劇情」 |
| 39234 | 39097 | −137 | openLoc(best) 地圖釘 goPin |
| 39237 | 39100 | −137 | openLoc(L.id) 地圖釘 goPin 後備 |
| 39268 | 39131 | −137 | openLoc(data-loc) 地圖底欄地點掣 |
| 40773 | 40636 | −137 | openLoc(locId, {wf4Done:true}) wf4Fire |
| 43475 | 43338 | −137 | openLoc(L.id, {travelFree:true}) 人情債流程尾 |
| 43498 | 43361 | −137 | openLoc 人情債「取消」 |
| 43818 | 43681 | −137 | openLoc("agency_ho") 人情債「去事務所」 |
| 44241 | 44104 | −137 | WRAPPER `openLoc: function(id, opts){ openLoc(id, opts); }` |
| 52507 | 52485 | −22 | openLoc(locId, {encDone:true}) 巧遇播完 |
| 52626 | 52604 | −22 | openLoc(locId, {encDone:true}) |
| 53519 | 53497 | −22 | openLoc(locSnap, {travelFree:true}) refreshLocAfterStory |
| 53632 | 53610 | −22 | DEF `function openLoc(id, opts){` |
| 53901 | 53879 | −22 | openLoc(L.id, {travelFree:true})「劇情已完成」toast 後 |
| 53923 | 53901 | −22 | openLoc(L.id, {travelFree:true})「劇情已完成」toast 後 |
| 54058 | 54052 | −6 | openLoc(L.id, {travelFree:true}) 聽完傳聞 reopen |
| 55695 | 55689 | −6 | openLoc(L.id, {forceRestore:true}) |
| 57106 | 57100 | −6 | 傾談結果 modal go |
| 57439 | 57433 | −6 | promptAudition back openLoc travelFree |
| 57557 | 57551 | −6 | 禮物店／送禮 modal 關閉 openLoc travelFree |
| 57558 | 57552 | −6 | onDismiss openLoc travelFree |
| 57593 | 57587 | −6 | 送禮取消 openLoc travelFree |
| 57594 | 57588 | −6 | onDismiss openLoc travelFree |
| 57613 | 57607 | −6 | doGiveGift 失敗後 openLoc travelFree |
| 57628 | 57622 | −6 | 送禮結果 modal go openLoc travelFree |
| 57662 | 57658 | −4 | openLoc("gift_shop") inv72GoShop |
| 57829 | 57825 | −4 | openLoc(loc) people72GoLoc |
| 57972 | 57968 | −4 | openLoc(target) jobs72GoBoard |
| 57993 | 57989 | −4 | openLoc(target) jobs72GoLoc |
| 58443 | 58439 | −4 | openLoc(locId) 開局屋企 modal「去睇劇情」 |

漂移帶：早段 −191／−185／−184（main v152–v166 淨刪行主導）→ 中段 −137 → 尾段 −22／−6／−4。COUNT 13／FREE 27 不變。

### 3.2 `test_text125_static.py`（基底 `d64887c`，3 錨點）

| 舊行 | 新行 | 漂移 | 內容 |
|---|---|---|---|
| 27824 | 27639 | −185 | currentLine `const lines = Array.isArray(b.lines) ? …`（`ls[27823]`→`ls[27638]`，`len(ls) < 27824`→`< 27639`） |
| 27937 | 27752 | −185 | advance 同上（`ls[27936]`→`ls[27751]`，`len < 27937`→`< 27752`） |
| 33582 | 33445 | −137 | applyFamilySafeToNode `if(typeof b.text === "string" && b.text){`（`ls[33581]`→`ls[33444]`，`len < 33584`→`< 33447`，原 ＋2 slack 保留） |

報錯字串「第 27824／27937／33582 行」一併更新做新行號；行尾 `# v157 resync：…` 歷史註解唔郁。

### 3.3 `test_kwan151_static.py`（基底 `60b0a8f`，13 錨點）

| 舊行 | 新行 | 漂移 | 內容 |
|---|---|---|---|
| 25545 | 25569 | ＋24 | `/Ho\s*哥\|陳淑芬\|施南生/` regex（A1，標籤 L25545→L25569） |
| 25882 | 25906 | ＋24 | `["陳淑芬","施南生","Ho哥"]` list（A2） |
| 25885 | 25909 | ＋24 | v1.1 note 註解「雙女主改讀 devAppendix」（A7，header 註解 L25885→L25909 一併更新） |
| 25886 | 25910 | ＋24 | `bad("dual_note")`（A8） |
| 25887 | 25911 | ＋24 | `/* v151 退役：關海媚名禁令已撤 … */`（A6） |
| 25930 | 25954 | ＋24 | `["陳淑芬","施南生","Ho哥","Ho 哥","nextHint"]`（A3） |
| 26149 | 26173 | ＋24 | `["陳淑芬","施南生","Ho哥","Ho 哥"]`（A4） |
| 27090 | 27114 | ＋24 | `"關海媚":"kwan_hoimei"` speaker registry（E1） |
| 27123 | 27147 | ＋24 | `kwan_hoimei: { … display:"關海媚" }`（C1） |
| 30831 | 30897 | ＋66 | `TEXTFIX55_EXACT` C13（B3／B4／B5） |
| 30839 | 30905 | ＋66 | `TEXTFIX55_NOTE_EXACT`（C4／C5） |
| 30840 | 30906 | ＋66 | `TEXTFIX55_PHRASES`（B2） |
| 30882 | 30948 | ＋66 | `relMap` `["rel_mei","關海媚"]`（C3） |

`line(N)` 參數＋ok() 名 `LNNNNN` 標籤＋header 註解跟 live 錨點嗰兩個 L 號一併更新；header 舊歷史數字（`(25744→25761、…)`、L26112／L26160／L26380）留返唔郁（舊例 M4 都係咁處理）。

### 3.4 `test_tang152_static.py`（基底 `60b0a8f`，3 錨點）

| 舊行 | 新行 | 漂移 | 內容 |
|---|---|---|---|
| 25701 | 25725 | ＋24 | `const HELD = ["R_tang_push1","R_tang_push2","R_tang_crisis"];`（`lines()[25700]`→`[25724]`，標籤（L25701）→（L25725）） |
| 31321 | 31387 | ＋66 | `function normaliseTangStub152(pack){`（`lines()[31320]`→`[31386]`，（L31321）→（L31387）） |
| 31465 | 31531 | ＋66 | `try{ normaliseTangStub152(rom2); }`（`lines()[31464]`→`[31530]`，（L31465）→（L31531）） |

注意：ok() 名標籤用**全形括號**`（L…）`，第一版腳本只認半形 `(L…)`，漏咗 3 個標籤，之後補咗全形 pattern 單獨一 pass 修正（腳本已更正，見 `qa131/resync_rebase157.py` 註解）。header 裸數行「HELD 25701／normaliser 31321／loader 31465」成行改寫做新數。

### 3.5 核實方法

- 每條釘行：difflib `SequenceMatcher(autojunk=False)` `equal` 段對位，基底行內容 vs HEAD 行內容逐字相同先叫純漂移；59 條全部 OK，0 條落喺 replace／delete 段。
- 換數方法：單次掃描 dict 查表（`re.sub` callback 一次過），唔逐對 `re.sub`；travel114 只限 COUNT／FREE 集合區＋DEF／WRAPPER 賦值行（註解歷史數字唔郁）；text125 只限 `len(ls) < N`／`ls[N]` pattern；kwan151／tang152 只限 `line(N)`／`lines()[N]`／`LNNNNN` 標籤。
- 四檔各加一行 rebase 歷史註解（寫明漂移量＋核實方法＋腳本路徑）。
- 事故：第一版腳本 travel114 段漏咗 `new = ''.join(out)` 一行，`open(p,'w')` 截斷檔案後先報 `UnboundLocalError`，檔案變 0 bytes；即時 `git checkout -- tests/test_travel114_static.py` 還原（228 行，乾淨），修好腳本後重跑，確認 `git diff` 淨係行號＋註解行。教訓：寫檔前先砌好成個新內容先開檔（腳本其餘三段本來就係咁做）。

## 4. 逐個直接跑（17/17 PASS）

| 測試 | 結果 |
|---|---|
| `tests/test_story157_index_static.py`（新） | PASS（117 PASS 斷言，吻合 NOTES §5.1） |
| `tests/test_story157_pack_static.py`（新） | PASS（124 PASS 斷言，吻合 NOTES §5.1） |
| `tests/test_gate136_static.py` | PASS |
| `tests/test_weave47_static.py` | PASS |
| `tests/test_weave48_static.py` | PASS |
| `tests/test_weave48_logic.js` | PASS |
| `tests/test_wf1_80_logic.js` | PASS |
| `tests/test_text125_static.py` | PASS |
| `tests/test_weave46_static.py` | PASS |
| `tests/test_travel114_static.py` | PASS |
| `tests/test_travel114_logic.js` | PASS |
| `tests/test_aud91fix122_static.py`（守衛窄化） | PASS |
| `tests/test_aud91fix124_static.py`（守衛窄化） | PASS |
| `tests/test_gigreq110_static.py`（守衛窄化） | PASS |
| `tests/test_wf5_87_static.py`（守衛窄化） | PASS |
| `tests/test_kwan151_static.py` | PASS |
| `tests/test_tang152_static.py` | PASS |

## 5. 全套 A/B（`qa131/run_suite.sh`）

| Run | 總數 | 檔數 |
|---|---|---|
| Pristine `60b0a8f`（worktree `~/workspace/linji-pristine166`，跑完已移除；`qa131/suite_rebase_pristine.txt`） | **223 PASS／12 FAIL** | 235 |
| 工作版（resync 後；`qa131/suite_rebase_work.txt`） | **225 PASS／12 FAIL** | 237 |

- 總數差 ＋2＝正好係 2 份新測試（`test_story157_index_static.py`＋`test_story157_pack_static.py`），其餘 PASS 數不變。
- FAIL 清單兩邊 `diff` **零差異**，逐項都係 12 項穩定 pre-existing FAIL：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wrap38。
- 多出嚟嘅 FAIL：**0 項**——無需逐個重跑（重跑條件唔觸發）。
- 附註：MEMORY.md 入面 v166 自己嗰次 run 寫 222／12，今次 pristine 重跑係 223／12——差 1 係套件總數波動（AGENTS.md 已記錄同一 repo 會波動），FAIL 清單逐項相同先係判斷準則；任務書講嘅 main 基線 223／12 今次實跑證實。
- 第二次工作版確認 run：無跑——兩次總數差完全由新測試數解釋，FAIL 清單逐項相同，無大幅波動跡象。

## 6. 結論：零回歸，可 commit

- Rebase diff 核實：splice 增行 472／刪行 402／pack 增行 389，rebase 前後逐行集合完全相同，內容無沖走。
- Resync：4 檔、59 條釘行全部 difflib 對位核實純漂移（內容逐字相同），17 個相關測試逐個直接跑全部 PASS。
- 全套 A/B：工作版 225／12 vs pristine 223／12，FAIL 清單逐項相同，多出 FAIL 0 項。
- Resync commit：`v20a157 rebase resync`（本分支 HEAD，`git log --oneline -1` 可查；8 檔：4 份測試檔＋resync 腳本＋本報告＋2 份全套輸出）。
- 唔落地（落地由統籌做）。分支 HEAD 喺 resync 期間由統籌推前咗一個 NOTES commit（`171829a` → `b38356b`，淨改 `NOTES_V20A157.md` §8 一行，index.html 零郁），resync 不受影響，commit 落喺 `b38356b` 之上。
