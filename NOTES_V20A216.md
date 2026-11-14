# v20a216 NOTES：報紙修復票（R0–R5＋實駕跟進＋釘行 resync）

- 基底：v215 NOTES `2b0faf0`（遊戲 `2e4f1c0`＝live v215）。調查報告 `~/workspace/linji-newspaper-v216-inv/ROOTCAUSE.md`；設計權威 `~/workspace/linji-newspaper-sample/`（p1 v11、p2 v7）。
- 用戶回報（2026-11-15 00:58，live v215）：1990-02-10 星期六晨報四處錯。根因全部喺報告 §2–§8，修復建議 §10，口語重寫表 §9。
- 紀律：唔改 SAVE key（`starVolunteer_map_v19w`，10 處）、softRev（`s107`）、產品 `?v=`；新檔案用 `git add <path>` 明確加；唔落地（落地另有人做）。

## 1. 改咗乜（逐項對根因）

### R0 — 殘留填位項目（`press94:"fill"`）
- 三層防禦，喺 `index.html`：
  - `ensureNewspaperQueue()`：每次讀隊列嗰陣清走 `press94==="fill"` 項目（舊存檔遷移）。
  - `enqueueNewspaperItem()`：新遞入嚟嘅填位項直接拒收（return null，唔入隊）。
  - `buildNewspaperEdition()`：合版嗰陣濾走填位項；成批都係填位回 `null`（唔出空報紙）；`pullDueNewspaperEdition()` 守 `if(!edition) return null;`。
- 關鍵約束：靜態測試 `test_newspaper214_wrap_static.py` S02 斷言字串 `press94: "fill"` 唔可以出現喺 `index.html`——code／註解／頁內測試一律用 `press94==="fill"` 寫法，測試入面用 property assignment（`fillRaw216.press94 = "fill";`）。核實：該字串 repo 內 0 命中。
- 已知殘留（唔修得）：v216 之前已經由填位項砌好、存咗喺 `pendingMorningPaper` 嘅晨報，上面冇 marker，分唔出係正紙定填位，可以再顯示一次。隊列 purge 覆蓋主路徑。

### R1 — 頭條排版（`renderMorningPaperHtml`＋CSS）
- 字級降級（`headClass216`，唔計空白字數）：≤10 字 37px、11–16 字 30px、17–18 字 26px（`.np214-headline3`）、>18 字 22px（`.np214-headline4`，新增）。第四級係實駕跟進加嘅：20 字第二版標題喺 26px 下 3 行兼孤行「佈，」，22px 先收返 2 行。
- 全部頭條 class 加 `text-wrap:balance`＋`overflow-wrap:break-word`；書名號「《…》」包 `<span class="np214-nobreak red">`（`white-space:nowrap`，唔准斷開／標點孤兒）。
- 套紅（`.red #b32020`，跟樣本 C4）：書名、星名（`PAPER_TOPIC_STARS`，後備 8 名 literal：陸柏言／麥震東／高俊傑／廖炳星／葉敏芝／魏詠男／程天諾／蘇芷茵）、獎項動詞（奪新人獎／奪獎／奪得／入圍／殺青／煞科／得獎／獲獎／開鏡／封王／稱王／問鼎）。人名唔包陳偉翔——包埋會打爛 polish48 嘅 exact-substring 頭條斷言。
- helpers（`headClass216`／`headRich216`）INLINE 喺 `renderMorningPaperHtml` 入面：polish48 只抽呢個函數＋`newspaperEsc`＋具名 deps，唔可以搬出去。
- 重現標題（15 字）而家 30px、2 行。

### R2 — 第二版真頭條
- 刪硬寫 `<h3 class="np214-headline2">同版短訊</h3>`；第二版頭條＝第一則非 summary 短訊標題（同一套字級邏輯），眉題留「同版短訊」，副題用該則 dek 頭一句；第一則係 summary 就用下一則；得 summary 一則就用頭版標題＋「（續）」。版尾保持「第二版 · 同版短訊」（core_static R11 要）。
- 跟進：lead 嗰則唔喺下面短訊列重複（樣本 v7 式樣，`leadIdx216` 跳過）；佢張相（world 短訊有相）改喺第二版頭條下面出，保住 wrap_logic E05 嘅相斷言。

### R3 — 短正文填版
- `buildNewspaperEdition` 透傳 `workTitle`／`medium`／`roleLabel`（role 由 `S.wrapHistory` 按 gigId 補，guard 咗 extraction-test stub）。
- 第一版資料格（`.np214-factbox`，之前只得頒獎渲染器 emit）：行 作品／媒介／角色，淨係出真數據，格名「《作品》小檔案」或「本期小檔案」。
- 第一版填充字（`.np214-filler`，同頒獎渲染器同一串模糊字）：dek < 80 字＋無相＋唔係世界事件先出。
- 邊欄：第一版有真預告（第一則短訊標題）；第二版用 plain sidebar（無預告）。
- 第二版短訊 ≤2 則嗰陣出 3 段唔同年代詞組嘅填充字（保留 S23 靜態檢查嗰個 exact prefix `(e.shorts||[]).length<=2? \`<p class="np214-filler"`）。
- 冇天氣格（刻意：遊戲冇天氣數據，照舊 CSS 註解）。
- **實駕跟進（第一輪截圖後）**：
  - 浮動資料格（138px）＋浮動填充字將兩欄正文壓成 2–3 字一行窄條。改：無相嗰陣資料格改全闊（`.np214-factbox-wide`，放正文下面）、填充字唔浮動（全闊放資料格下面）；有相嗰陣照舊浮動（樣本式樣，長正文繞得掂）。
  - 全闊格行內出值（一行一筆），慳 ~35px，等版尾第一屏見到。注意：呢條 selector 一定要用 `.np214-factbox.np214-factbox-wide`（5 級）先贏到原本 `display:block`（同級 specificity、後出先贏——第一版寫漏咗，靜默失效，紙高完全唔郁；已加靜態 guard `R3_factbox_wide_inline`）。
  - 邊欄預告由 12 字＋「同版短訊：」改做 6 字＋「同版：」，有預告嗰陣唔出裝飾填充字（免邊欄高過主欄拖長成張紙）。

### R4 — 掣唔疊紙底邊
- 刪 `#mask.paper-on #modal-btns` 嘅 `margin-top:-7px!important`（跌返 base `margin-top: 8px!important`）；保留 -2.2° 斜＋z-index。
- 76px 短屏（`max-height:800px`）padding media query 由 L4580 搬去 34px rule 之後（同 specificity、後出先贏——舊位俾 L4704 靜默 override 咗，死碼）。
- 加 `#mask.paper-on:not(.tut-on).modal{max-height:min(88dvh,88svh,760px)!important;}`（844px 高都唔會令版尾＋「第二版 →」跌出摺疊線；之前 88dvh 只喺 ≤820px 生效）。
- `.paper-sheet.np214-switchrow` 加 `position:sticky; bottom:0; z-index:3; background:#f5eedb; padding-top:6px;`（第一屏見到有第二版）。
- `presentDueMorningPaper` 開頭防禦性清 `story-play-on` flag＋`setStoryPlayLock(false)`（播種 artifact 防禦，無壞）。

### R5 — 口語改書面語（只限晨報短訊模板）
- `PAPER_SIDE_ITEMS` 39 則 h／d 全部按報告 §9 表重寫（原封），＋`NEWS82_EVENTS` E5 第一段：「係真挖角定放風試水溫，圈中人人估緊」→「是真挖角還是放風試水溫，圈中人人猜測」。
- 偏離 §9 表一處（有記低）：3 個標題表話「標題不變」但本身有口語，照佢哋 dek 同一手法修埋：#4「笑到見牙唔見眼」→「笑逐顏開」；#21「經理人話係宣傳安排」→「經理人稱為宣傳安排」；#24「經理人電話繼續響唔停」→「經理人電話響個不停」。重寫後 39 則 h／d 掃 banned 詞 0 命中。
- Lint（`newspaperCheck`＋兩個新測試）：禁 喺／嘅／咗／唔／嗰（「」引號內例外）、「係…定…」句式、估緊、reporting-verb 話（排除 電話／說話／話題／通話／熱話／一句話）、`cut`／`mark`。
- 唔郁：release 推出短訊（乾淨）、頒獎／殺青報紙口語（留返 v214 review 嗰批）。

## 2. 新測試＋反證

- 新增 `tests/test_newspaper216_logic.js`（node，抽真函數跑；38 個斷言：R0／R1／R2／R3／R5＋R4 靜態 CSS）同 `tests/test_newspaper216_static.py`（34 個斷言：CSS 接線、R0／R2／R4／R5 guard、紅字線）。
- `newspaperCheck()`（`index.html` 頁內）加斷言：R0a／b／c、R1 tiers／red／nobreak、R2、R3、R4 DOM 量度（真 `presentDueMorningPaper` 後量 `#modal-btns` margin-top ≥ 0、`.paper-sheet` padding-bottom ≥ 34）、R5 lint。softRev 保持 `s107`。
- 更新咗嘅舊測試（有意改 spec， precedent：v214 S16）：`tests/test_polish48_static.py`（-7px 斷言反轉做斷言佢唔存在）、`tests/test_newspaper214_core_logic.js` c15／c15b（短訊檢查限 P2 切片——邊欄預告＋P2 頭條合理提及第一則短訊）、`tests/test_newspaper214_wrap_logic.js` E05／E09（第一則短訊標題而家出現兩次：P1 邊欄預告＋P2 頭條；dek 一次）。
- **反證（對 pristine main v215，`/tmp/pristine216_index.html`，md5 `216c5ccb0a5c1eb8e3adfdc0bbeeadee`）**：logic test 31 FAIL、static test 29 FAIL；工作副本兩個都 ALL PASS。途中收緊咗兩個原本喺 pristine 上空洞嘅檢查：R1c 30px 改查 P1 切片；R4c 88dvh 改 regex 錨定成條 `#mask.paper-on:not(.tut-on).modal{…max-height:min(88dvh,88svh,760px)` rule（pristine 已有 `#mask.tut-on.modal` 同值 rule＋`#mask.paper-on:not(.tut-on).modal{padding-bottom:20px}` rule）；R2a「同版短訊」計數 3→2 之後發現 pristine 都有 2 個（硬寫 h3＋版尾），加埋 kicker 形式先至非空洞；R3d p2 填充字改數 P2 切片。
- 紅線核實：SAVE key `starVolunteer_map_v19w` 10 處、`"v20a10"` 7 處、`s107` 在位、style braces 平衡（1964／1964）、`rotate(-2.2deg)` 2 處、`press94: "fill"` 字串 0 命中。

## 3. 全套 suite A／B

- A（pristine v215，`qa131/run_suite.sh`）：**307 PASS／13 FAIL**，同任務基線一致。FAIL 清單＝穩定清單：flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38。
- B（工作副本，resync 前）：301／21——多咗 8 個 FAIL，逐個覆驗全部係釘行漂移（見 §4），唔係功能回歸。
- B2（工作副本，resync 後）：**309 PASS／13 FAIL**，FAIL 清單同 A 一模一樣（13 個穩定 FAIL）；多出嚟嘅 2 個 PASS 係兩個新測試檔。
- 注意：第一次 A 跑出 320／0 係假數——`git archive` 經 `/tmp`（512M tmpfs）解壓嗰陣爆滿，pristine 樹截斷咗（503M，tests 全空檔）。刪咗重抽去 `~/workspace/pristine216root`（931M，md5 核實）先至跑出真數 307／13；之後按「唔留大檔」規矩刪埋個 pristine 樹。resync 腳本改咗用 `git show HEAD:index.html` 做基底，唔再靠嗰個樹。
- 相關舊測試逐個覆驗 PASS：polish48 logic／static、newspaper214 core／wrap／award logic＋static、press94 logic／static、weave48 static、wf4_86 static。

## 4. 釘行 resync（v216 淨 +263 行）

- `git diff --numstat index.html`：+322／−59，淨 +263。插入點（difflib opcode）：CSS headline4／factbox-wide（~L4760–4900，+38 行）、renderMorningPaperHtml R1–R3（~L50500–50630）、newspaperCheck R1／R3（~L51030–51120）、R0 隊列閘、R5 原位重寫（淨 0 行）。
- 8 個靜態測試嘅釘行漂移，全部經 difflib 對位核實內容逐字相同（純漂移）：gift185（總行數）、kwan151（13 錨點）、rom176（6 錨點）、tang152（3 錨點）、tang171（總行數＋DEF）、tang173（總行數＋DEF＋L4862）、text125（3 錨點）、travel114（COUNT 12＋FREE 33＋DEF／WRAPPER）。
- 腳本（跟 qa215 模式，單次掃描 dict 查表，唔逐對 re.sub）：`qa216/resync216.py`（建 mapping＋驗純漂移，輸出 `qa216/resync216_map.json`，75 個釘行，BAD none）＋`qa216/apply_resync216.py`（套用，逐項計數，數目唔啱即 exit 1 唔寫檔）。總行數 62492→62755（公式加 ＋v216 +263）、DEF 56964→57227、WRAPPER 45392→45430、L4862 5125→5163。歷史註解／斷言名入面嘅舊 L 號標籤一律唔郁。
- 教訓：`resync216.py` 第一版由工作版測試檔收集釘行，跑第二次嗰陣收集到已 resync 嘅新數，寫咗個第二代 map——已修正：釘行清單改由 `git show HEAD:tests/<file>` 收集，依家重跑會出返同一份原 map。
- resync 後 8 檔逐個 PASS，全套 B2 309／13（見 §3）。

## 5. 實駕驗證（Playwright，`~/workspace/linji-newspaper-v216-inv/verify216.py`）

- 方法：本地鏡像 port 21602，`new_game`＋`seed`，重現調查員嗰份 1990-02-10 晨報（S.dayIndex=40）。三個 case＋三個 viewport（390×844、430×932、390×700）。截圖存 `~/workspace/linji-newspaper-v216-inv/shots-after/`（b390／b430／b390_700，P1＋P2，頂＋底各一）。
- **Case A（R0）**：經真 `__newspaper.enqueue()` 入隊舊填位項目 → 隊列 0、present false、無 modal、0 pageerrors。✓
- **Case B（重現晨報）**：
  - P1 頭條：30px、2 行、《錄音室拍板》紅＋唔斷開（`nobreakRed: true`）。✓
  - P2 頭條：第一則短訊「陸柏言紅磡開唱未公佈，黃牛票價已經高企」，22px、2 行，眉題「同版短訊」；之前 26px 下 3 行兼孤行「佈，」。✓
  - 資料格全闊一行一筆（作品《錄音室拍板》／媒介 唱片）；填充字在位；邊欄「同版：陸柏言紅磡開……」。✓
  - 填版：P1 內容貼到版尾（整體 gap −1.3px，即無空白；主欄／邊欄各自 gap 66.6／75.7px 係聲望行＋note 嘅位，唔係空白）；P2 gap 6.7px。✓
  - R4：捲到底掣紙重疊 0px（三個 viewport）；elementFromPoint 真實遮蓋 0／5（三個 viewport、頂＋底）；「收下這份剪報」margin-top 8px；紙底 padding 34px（844／932）、76px（700）；版尾「維港日報　第一版 · 樂壇速遞」第一屏見到（截圖核實）；「第二版 →」sticky 第一屏見到。✓
  - 紙高：P1 657.7px（原版 650px 左右；之前實駕第一輪 692.9px，修咗全闊格行內出值先落返嚟；430 屏一樣，700 屏 699.7px）。P2 862.2px（之前 908.1px，頭條 3→2 行慳咗）。
  - 0 pageerrors（三個 viewport）。
- **Case C（`window.__newspaper.check()`）**：`ok:false`，fails `['merge_cap', 'press_colloquial', 'seed_win']`——**同 pristine v215 完全一樣**（用完整 pristine 樹重跑核實過），係 pre-existing，唔係 v216 回歸：`merge_cap`（6 則 wrap＋side 則推高 shorts 上限）、`press_colloquial`（頒獎／press 模板口語，v214 review 嗰批，v216 範圍外）、`seed_win`（頒獎 fameDelta）。
- 量度方法修正：行數唔再數 `Range.getClientRects().length`——同一行嘅 inline 片段（紅字 span＋正文）會拆開計，頂部差幾 px；改做 y 值 10px 內聚類。舊方法將 P1 頭條誤報 3 行、P2 誤報 5 行；修正後 P1 2 行、P2 2 行，同截圖一致。
- 抽查：頒獎／殺青報紙——case C 嘅 newspaperCheck 覆蓋 award／gallery／declined／story 路徑，結果同 pristine 一致（上面 3 個 pre-existing fail 之外全過）；實駕 case B 嘅殺青晨報本身就係 wrap 成功報紙。

## 6. 殘留／跟進（唔喺呢票）

1. R0 殘留：v216 之前已砌好存喺 `pendingMorningPaper` 嘅填位晨報可以再顯示一次（無 marker 分唔出），見 §1 R0。
2. `newspaperCheck` 3 個 pre-existing fail（`merge_cap`／`press_colloquial`／`seed_win`），見 §5 case C。
3. 第一版 `.paper-note` 仲印住「公開報紙。圈內耳語仍在手帳『傳聞』。」——「傳聞」已刪，係 v214 review B1 嗰批，唔喺 v216 範圍，冇郁。
4. 第二版紙高 862px（兩格廣告＋3 段填充字），要捲先睇晒；切換掣 sticky，第一屏見到。
5. MEMORY.md 喺呢個 session 期間有外部背景整理（刪／合併咗幾條舊目），同 v216 無關，冇跟進。

## 7. 改動檔清單

- `index.html`（+322／−59，淨 +263 行）
- `tests/test_newspaper216_logic.js`（新增）、`tests/test_newspaper216_static.py`（新增）
- `tests/test_polish48_static.py`、`tests/test_newspaper214_core_logic.js`、`tests/test_newspaper214_wrap_logic.js`（有意改 spec，見 §2）
- `tests/test_gift185_static.py`、`tests/test_kwan151_static.py`、`tests/test_rom176_static.py`、`tests/test_tang152_static.py`、`tests/test_tang171_static.py`、`tests/test_tang173_static.py`、`tests/test_text125_static.py`、`tests/test_travel114_static.py`（釘行 resync，見 §4）
- `qa216/resync216.py`、`qa216/apply_resync216.py`、`qa216/resync216_map.json`（新增）
- 本檔 `NOTES_V20A216.md`
