# NOTES_V20A288 — DUR90 刪組＋v267 小清理＋主線提示年份＋2＋regen-v2 同步

## 落地內容（v288，main 待填）

### A1. DUR90 整組刪除（刪死碼，index.html −90 行）
- 刪：header 註解 L15773–15791、`DUR90_OLD_BAND` L15792–15797、`DUR90_DAILY` L15798–15810、`dur90RoundPay` L15811–15816、`dur90CalibrateGig` L15817–15859（共 87 行）、normalizeGigRecord 內 call site L15923–15924（註解＋`try{ dur90CalibrateGig(o); }`）。行號逐行核實過先刪（brief 話 dur90CalibrateGig 到 L15860，實測係 L15859，L15860 係空行，留返）。
- 註解改寫（唔係成段刪，因為佢哋講緊仲 live 嘅嘢）：
  - v20a229 B1 days→shootDaysHint 註解：只刪「DUR90 校準喺上面已經行完…」嗰句，留返工期映射說明。
  - SHOOT_DAYS／ROLE_SCALE_BAND 兩處註解（原 L19006／L19014）：去咗「DUR90」字眼，留返工期帶說明。
- **代價（安全網移除）**：以後有 shootBand 嘅 gig，片酬唔再有 DUR90 夾帶。現時庫入面 0 張帶 shootBand（python 全量實查，289 張），所以現時係 no-op；將來加帶 shootBand 嘅 gig 要自己校準片酬。
- 測試同步：刪 `tests/test_dur90_static.py`（18 項）、`tests/test_dur90_logic.js`（18 項）；改 8 檔——`test_gig229_tiers.js`（刪 S2／S3／H／H2／H3 共 5 項、CONSTS／return／BOARD_SRC 去 DUR90_DAILY）、`test_gig229_stagger.js`、`test_gig229_pack.js`、`test_gig229_trigger.js`、`test_gig229_years.js`、`test_nat92_logic.js`、`test_awards63_logic.js`、`test_awei195_logic.js`（去期望常數／函數名單入面嘅 DUR90 項）。grep 全 repo DUR90／dur90 零殘留（歷史 NOTES／qa123／qa149／qa166／qa229 快照除外）。
- 8 個改過嘅測試檔逐個直接跑，全部 ALL PASS。

### A2. v267 兩處小清理
- index.html L3443 註解：去咗已刪 `tutorialPhase2FxOn` 嗰句；`@keyframes tutFxFinger`（L3455）仲係 live，唔郁。
- `tests/test_br89_deadflag_lint.js` L54 正則交替表去 `hasIntelFlag`（已刪函數）。lint 照 PASS（「PASS dead-flag lint：冇未註明嘅死旗」）。

### C1. Q4 主線提示年份＋2——已 REVERT（brief 前提錯，唔入 v288）
- 原先做咗：STORY_HINT_SOFT 12 行、22 處年份 source 年＋2（N6／N7／N8／N9／N10／N11／N12／N13／N14／N15／N16／N17），另加新 static test `tests/test_r288_hints_years.js`（35 項）。
- **Suite 第一跑即刻捉到衝突**：`test_sideline282_logic.js` 釘住「1990 年秋末」留返 2 處；`test_gate136_static.py` 斷言提示表行係舊曆 1990、無 1992。兩檔都係 guard 舊狀態。
- **查證結果：brief 前提錯，C1 會 double-shift，必須 revert**。鐵證（runtime 實測，pristine main）：
  - index.html L14767–14768 載入嗰陣 `years66Walk` 行埋 `STORY_HINT_SOFT`（連同 STORY_TITLE_SOFT／STORY_LOC_SOFT／CHOICE47_NODES／COMMIT48_NODES）；
  - `years66ShiftText` 將 1988–1992 全部 +2（`lockedHint`／`nextHint`／`playerHint` 唔喺 YEARS66_SKIP_KEYS 入面）；
  - Node 實測：walk 前 N12 lockedHint「1990 年春才開啟…」→ walk 後「1992 年春才開啟…」；N15「1990 年秋末」→「1992 年秋末」；N10「1989 年冬年尾清貨期」→「1991 年冬年尾清貨期」。
  - 即係話 source 年份本身已經啱，寫「1992 年」入 source 玩家面會見到「1994 年」。MEMORY 硬規則話明唔可以直接手改 source 年份，否則 double-shift；gate136 註解亦寫明呢個機制。
- **已 revert**：22 處全部改返原值（`c1_revert.py`，每處 assert 唯一），hints block 同 HEAD 逐字相同；新 test 已刪。revert 後 sideline282＋gate136 即刻 ALL PASS。
- 教訓：派工前要核實「邊啲表經 years66Walk」——內嵌靜態表（STORY_HINT_SOFT 等）同 JSON pack 一樣，source 年唔郁，顯示年由 runtime +2。


### D1. regen-v2 P7 film_203 season 期望（設計目錄，唔經 merge）
- `~/workspace/linji-gig-redesign/regen-v2/verify-batch-extra-film-tv.js` L60：`gig_1990_film_203` season `'春'`→`'夏'`；同目錄 `batch-extra-film-tv-report.md` L54 同步改「1990 春」→「1990 夏」。live 同設計 copy `gigs_new_v2.json` 都係夏。
- 重跑 `run_batch_verifies.py`：六批全部 exit=0。extra-film-tv 內層 RESULT PASS 43／FAIL 0。Runner summary 顯示 film-works／extra-film-tv／extra-music-ad-variety 各 FAIL=1，係計數 artifact——每份 log 唯一含「FAIL」嗰行都係讀數 0（「硬檢查 FAIL：0 項」／「PASS 43 / FAIL 0」／「PASS 1814 / FAIL 0」），零真失敗。
- 附註：report 其餘三行片名同 verify script 有出入（film_201《賀歲片場》vs《富貴茶餐廳》、film_202《喜劇組片場》vs《笑到最後》、film_203《高空墮樓戲》vs《江湖復仇》），唔喺 D1 範圍，留待設計目錄下次整理。

## B1. HELD（唔入 v288，原因如下，等 parent 決定）
- 原定：10 張玩家主唱唱片 gig 嘅 `singer`／`singerGender` 改 null（跟 v255 前例）。10 張逐張核實過（singer 非 null、singerGender M、roleLabel 含主唱），改完 diff 剛好 20 行，5 張表演角色 gig 無掂過。
- **但改完 `tests/test_awards63_logic.js` 1 項 FAIL**：「男歌手格讀 singer（顧明輝＋駱家聲＋陸柏言）」。因果已證實：改之前 stash 返原 JSON 即刻 ALL PASS，改完即刻 FAIL。
- 根因：`awards63Fellows`（index.html L32590）男歌手格只讀作品類唱片 gig 嘅 `singer`／`singerGender`，唔夠 3 個唔兜底（D-v2 設計）。B1  null 咗之後：
  - 1990 男歌手 distinct：3 個（顧明輝／駱家聲／陸柏言）→ **得返 1 個（顧明輝）**；
  - 1991 男歌手 distinct：3 個 → **2 個**（廖炳星／陸柏言）；
  - 1992 男歌手 distinct：維持 3 個。
  - 駱家聲（lok_gasing）喺作品池入面完全消失（全庫得返一張臨記 gig gig_1991_rec_202 有佢個名）。
- brief 話「頒獎讀 singer 有 null guard（L18457、L18512）」係真，但嗰兩個 guard 只係**顯示層**（null 嗰陣顯示「應徵中」／「主唱：阿偉」），提名人收集層無 guard。D-v2 規則話「唔夠 3 個對手＝庫唔合格」，所以唔可以直接改測試期望了事。
- 決定選項（等 parent）：A. 縮細 B1（例如保留 1990 嗰幾張，等男歌手獎保住 3 個提名人）；B. 接受提名人減少，改測試期望（違反 D-v2 庫合格規則）；C. B1 照做，另開票補提名人來源（例如 fellows 讀埋其他欄位）；D. 擱置 B1。
- B1 已喺工作副本 revert（`git checkout -- content/gigs_new.json`），revert 後 awards63 即刻 ALL PASS。v288 其餘四項照常出。

## 測試／Suite
- 逐個直接跑：A1 八檔、A2 lint、pack、awards204、trigger、years——全部 ALL PASS（B1 revert 後 awards63 亦 ALL PASS）。
- 全套 suite 第一跑：**TOTAL PASS 341 FAIL 18**（基線 351／9）。9 項新 FAIL：`test_sideline282_logic.js`、`test_gate136_static.py`、`test_gift185_static.py`、`test_rom159_static.py`、`test_rom176_static.py`、`test_tang171_static.py`、`test_tang173_static.py`、`test_text125_static.py`、`test_travel114_static.py`。9 項基線 FAIL 全部在列，無多無少。
- **FAIL 分流（全部查清，零真回歸）**：
  - sideline282＋gate136：C1 衝突（見上），C1 revert 後兩檔即刻 ALL PASS。
  - 其餘 7 檔：全部係 A1 −90 行釘行漂移。逐個對 pristine main（`git stash -- index.html` 還原）重跑：gift185／rom176／tang171／tang173／text125／travel114 全部 ALL PASS；rom159 嘅 4 處釘行經內容對位核實係純漂移。
  - resync（v20a288，單次掃描 dict 查表，見 `/tmp/resync288.py`）：gift185 總行數 46310→46220（鏈尾加 ＋v288 −90）；rom159 25207→25117、26041→25951、25956→25866、全佳 25235→25145；rom176 39862→39772、40220→40130、41437→41347、41593→41503；tang171／tang173 總行數＋openLoc DEF 41552→41462（鏈尾加 ＋v288 −90）；text125 16475→16385；travel114 FREE 30 處＋COUNT 11 處各 −90（COUNT 15398／FREE ≤14376 唔郁）、DEF 41552→41462、WRAPPER 28785→28695。全部新位置內容逐字核實（travel114 41 處逐行旗檢查照過）。
  - resync 後 7 檔逐個直接跑全部 ALL PASS（rom159 135 checks 0 FAIL；tang171／173 各 22／22；travel114 RESULT PASS）。
- 全套 suite 第二跑：**TOTAL PASS 349 FAIL 9**（`~/workspace/suite288_run2.log`）。9 項 FAIL 全部係基線 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），零新 FAIL。總檔數 360−2 刪檔＝358，349＋9＝358，對數。

## 出貨
- main commit `d68551d`（squash merge，branch `v20a288` 兩 commits `d47d1c1`＋`2cbd2e8`）；suite 第二跑 TOTAL PASS 349 FAIL 9（基線 FAIL 而已）；Pages 核實 byte-identical（md5 `b8a9361996048a03438ed7cef172f4de`，4,683,219 bytes）。
- 工作副本 `~/workspace/linji-work288` 已刪。
