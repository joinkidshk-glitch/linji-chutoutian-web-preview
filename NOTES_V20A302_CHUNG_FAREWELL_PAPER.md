# NOTES_V20A302 — Q15 鍾楚凝告別補報紙花邊

基線 main `bd0a37d`（suite 365／9）；分支 `v20a302`；工作目錄 `~/workspace/linji-work302`。

## 1. 已核實錨點（統籌 2026-11-18 親查 live，本票開工前再核實）

- `rumor_chung_*`：index.html 全文 **0 命中**（傳聞系統已刪）。
- 告別 beat `chung_farewell`（舊 L38620）：1992 年秋／冬、天星音樂門口，鍾楚凝決定去加拿大嗰邊睇下、住一排先；「我走，唔想大鑼大鼓。你都唔好同人講，當我去咗一個長啲嘅外景就得喇。」臨走忠告：「唔好學人哋點演，你要諗下嗰個人點解咁做，諗通咗，你點企、點望、點停，都自然係佢，唔係你扮佢。」
- 觸發（舊 L41741）：星好感 tier ≥2＋1992 年＋秋／冬；`grants()` 授 `S.flags.chungAdviceHeld229 = 1`。
- **grants() 時機已核實（ENC79 引擎）**：`pushSeg`（舊 L39969）將 segFx 掛喺 segment 最後一句（有 choices 就掛喺抉擇 step）；`chung_farewell` 無 choices，所以 L40120 嗰個 callback——`s2.beatsDone[beat.id]=dayIndex`＋`beat.grants()`——係 **beat 播完最後一句嗰陣行**，唔係觸發／入隊嗰陣。`beatsDone.chung_farewell` 同 `chungAdviceHeld229` 同一 callback 落，兩者等價。
- `beatsDone` 位置：`S.stars.chung_choning.beatsDone`（經 `enc79StarState`，舊 L39462）。同一紀錄被兩處讀：L39610 出沒盤停出（播完唔再撞到佢）、L13278 結局回望——**兩處唔郁**。
- 現有唯一跟進 `chungAdviceCardHeld229()`（舊 L45216；讀 `S.flags.chungAdviceHeld229`）：下一次文藝片試鏡多一句忠告提示，用一次即清（`chungAdviceSpent229`）。**唔郁呢個機制**（本票只加測試覆驗佢照舊）。
- 告別 beat 對白本身唔郁。

## 2. 報紙架構（已核實，唔重新發明）

- `buildNewspaperEdition(batch, day)`（舊 L34276）：組裝每期晨報；`batch` 空就回 `null`（成期無到期報紙項目就唔出報紙——告別花邊順延至下一期**有報紙**嗰日，見 §4）。
- 短訊列尾加一則花邊：`paperSideItemForDay(day)`（舊 L34152）由 `PAPER_SIDE_ITEMS` 靜態池（39 則，in-file self-test 釘死 39）按 `day % pool.length` 輪替，`source:"side"`、`paperName:"花邊短訊"`。
- `commitMorningPaper(edition, opts)`（舊 L34577）：入剪報庫、清 `S.pendingMorningPaper`、記 `S.newspaperLastPresentedDay`；對每則 `source==="side"` 且有 `sideId` 嘅短訊 call `enc79PaperWhisper(sideId)`。
- **`enc79PaperWhisper` 已核實（舊 L41302）**：純 map 查表（只認 `side_lu_concert`／`side_liao_newfilm`／`side_mak_wrap` 三個），未知 sideId → `sid` undefined → 唔 call `enc79GrantWhisper`，**純 no-op**。所以告別花邊用專屬 sideId 唔會開風聲窗，唔使改 whisper loop。
- 日始流程：`presentDueMorningPaper`（舊 L34632）喺三個位被 call——朝早鏈（舊 L21222：頒獎請柬之後、試鏡消息之前）、瞓覺流程（舊 L6496）、休息流程（舊 L44148）。佢經 `pullDueNewspaperEdition`（舊 L34396）攞 edition：有未 commit 嘅 `S.pendingMorningPaper` 就返用佢（唔 rebuild）；否則由到期隊列建新 edition、存入 `pendingMorningPaper`；present 嗰陣 modal 按鈕／dismiss 一律行 `done()` → `commitMorningPaper`。即係話：**edition 係「出示嗰陣」先組裝（當日 `S.dayIndex`），唔係瞓覺前預製**；commit 一定行一次（`fameApplied===true` 重入嗰陣早退）。
- `buildNewspaperEdition` 唯一真實 call 位係 `pullDueNewspaperEdition`（舊 L34405）；其餘係 in-file self-test。

## 3. 完美做法（設計方向）

- 告別 beat 完成後，下一期晨報短訊列**尾**加一則花邊（細欄，唔係頭版）：鍾楚凝赴加小住。
- **守住佢「唔想大鑼大鼓」**：文案含蓄，用「聽聞」「小住」「外景」口徑，唔寫成高調宣布、唔寫玩家名、唔寫佢同玩家講過咩。報紙文案一律香港式書面語，寫全名「鍾楚凝」。
- 只出一次：新旗 `S.flags.chungFarewellPaper302` 記「已出」。
- 唔改 `paperSideItemForDay` 輪替池本身（靜態花邊照輪）；告別花邊係額外一則，唔係取代當日嗰則。

### 花邊文案（定稿）

- headline：`聽聞鍾楚凝赴加小住，權當一個長外景`
- dek：`有行內人表示，鍾楚凝近日將赴加拿大，小住一段日子，權當一個長一點的外景，歸期未定。`
- `paperName:"花邊短訊"`、`source:"side"`、`sideId:"side_chung_farewell302"`、`fameDelta:0`。

### 高調字眼禁清單（測試斷言用）

headline＋dek 一律唔出現：`宣布`、`轟動`、`離開影壇`、`告別影壇`、`退出影壇`、`引退`、`移民`、`震撼`、`大鑼大鼓`；亦唔出現玩家名 `阿偉`／`陳偉翔`。必須出現：`鍾楚凝`、`聽聞`、`小住`、`外景`。

## 4. 時機掛接點（對住日始流程驗證過，唔係估）

- **注入點：`buildNewspaperEdition` 尾段**（正常花邊 `sideItem`＋`side2` 補位之後、`fameDelta` 匯總之前）。條件：告別已完成＋未出過。完成判定用 `beatsDone.chung_farewell` 為主，`S.flags.chungAdviceHeld229` 做舊檔後備（兩者同一 callback 落，等價；舊檔兩者齊備，OR 唔會誤觸——`chungAdviceHeld229` 全檔只由呢個 beat 嘅 `grants()` 授出）。
- **已出旗唔喺 build 嗰陣記**：build 可以被 self-test／抽出測試叫多次，亦可能建咗 edition 但未 commit（`pendingMorningPaper` 殘留、save/load）；記早咗會漏出。
- **已出旗喺 `commitMorningPaper` 主流程記**（`fameApplied` 早退之後、剪報入庫之後，同 whisper loop 同一段）：掃描 `edition.shorts`，見到 `sideId==="side_chung_farewell302"` 就記 `S.flags.chungFarewellPaper302 = 1`。commit 只行一次有效提交（重入早退唔重複記）；`pullDueNewspaperEdition` 返用 pending edition 唔 rebuild，所以唔會重複注入。
- **舊存檔 defensive**：已有 `chungAdviceHeld229`／`beatsDone.chung_farewell` 但未出過花邊嘅，下一次晨報補出一次，唔 crash、唔重複（OR 判定＋已出旗）。
- **已知順延**：若告別翌日全無到期報紙項目，`buildNewspaperEdition` 回 `null`、成期唔出報紙，花邊順延至下一期有報紙嗰日（「下一期晨報」＝下一期真係出嘅報紙）。若告別完成前已有 pending edition 建好，嗰期唔含花邊，下一期先有。
- **唔郁清單**：`chung_farewell` 對白、`grants()`、`chungAdviceCardHeld229`／`chungAdviceTipForAudition229`／`chungAdviceSpend229`、`paperSideItemForDay`／`PAPER_SIDE_ITEMS`（39 則）、`enc79PaperWhisper`、L13278 結局回望、L39610 出沒盤。

## 5. 實裝

- `index.html`：`buildNewspaperEdition` 注入（try/catch 包住，`typeof S` 守衛，抽出測試安全）；`commitMorningPaper` 記已出旗。行數變化見 §7。
- 新測試 `tests/test_r302_chung_farewell_paper.js`：抽取 `buildNewspaperEdition`／`paperSideItemForDay`／`PAPER_SIDE_ITEMS`／`commitMorningPaper`／`enc79PaperWhisper`／`chungAdviceCardHeld229` 實碼＋stub 跑邏輯斷言，另加靜態斷言（見 §6）。

## 6. 測試結果

- 新測試 `tests/test_r302_chung_farewell_paper.js`：**34 項 ALL PASS**（抽取實碼＋stub 跑邏輯斷言＋靜態斷言）。
  - A1 告別未做唔出；A2 beatsDone → 下一期有一則告別花邊（短訊列尾，頭條仍係殺青則）；A3 當日輪替花邊仍在；B 文案有鍾楚凝／聽聞／小住／外景、無禁清單（宣布／轟動／離開影壇／告別影壇／退出影壇／引退／移民／震撼／大鑼大鼓／阿偉／陳偉翔）；C commit 記旗、第二期唔再出、兩期剪報加埋只得一次；D1 舊檔（得 `chungAdviceHeld229`）補出一次、D2 舊檔（得 `beatsDone`）補出一次；E `enc79PaperWhisper("side_chung_farewell302")` no-op，對照組三個已知 id 照開風聲，含 lu＋liao＋farewell 嗰期 commit 只開兩個風聲；F 忠告機制照舊（持有→true、用過→false、無旗→false）；S1 輪替池仍 39 則、告別對白／結局回望／出沒盤／grants() 唔郁、gigs 302 張。
- Resync：`qa302/resync302.py`——舊 47137→新 47156，difflib 核實 **62 個錨點內容逐字相同、純漂移**（插入區邊界 4 處、rom176 4 釘、travel114 DEF／WRAPPER／COUNT 12／FREE 40）。5 檔釘行測試按段重算（＋14 區無釘行；≥34622 者 ＋19）：gift185（總行數鏈）、tang171／tang173（總行數鏈＋DEF 42346→42365＋guard 行）、rom176（4 釘）、travel114（DEF＋COUNT 4 處＋FREE 24 處；WRAPPER 29103 唔郁）。
- 逐檔覆驗 5 檔 resync 後測試：全部 PASS；新測試 ALL PASS。

## 7. 行數／Suite

- `index.html`：47137 → **47156 行（淨 ＋19）**：build 注入 ＋14（新 L34344–34357）、commit 記旗 ＋5（新 L34637–34641）。其餘改動只有 5 檔釘行測試 resync＋新測試＋NOTES＋resync 腳本，`content/` 唔郁。
- 全套 suite：`bash qa131/run_suite.sh` → **TOTAL PASS 366 FAIL 9**（`~/workspace/suite302.log`）。9 個 FAIL 同基線 pre-existing 完全一致（flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38——基線 stash 覆驗同一批 9 個；新測試由 365→366，＋1 PASS）。
