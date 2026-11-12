# NOTES_V20A117 — S-30 詳情區刪除＋唯一資料搬摘要＋欄卡 meta 拆行

範圍更正版（用戶 2026-11-12 08:01 睇《戲院人潮》話「詳細這部分好像其實都是重複的資料」）。
舊範圍「修復詳細表格 390px 被裁」已停——開工前未改過任何嘢，唔使 revert。
分支 `v117-s30-layout`（基於 main `4d967ed`），工作副本 `~/workspace/linji-work117`。

## 對照驗證（代碼＋實駕，唔係照單全收任務書）

`castingNoticeDetailHtml` 改前摘要區已有：要求格（現／要）、片酬、簽約金、違約金、
通告日數、通告期間、完成期限、報名截止、預計播出、差距提示、情報、var-note 三行。
詳細區（「顯示詳細 ▾」入面）逐項對，實駕展開態原文見 `qa117/drive117_before.json`：

| 詳細區項目 | 結論 |
|---|---|
| 條件（演技：需要 15 等） | 重複——同摘要區要求格同一組數，只係冇現值 |
| 通告日數／片酬／簽約金 | 重複（簽約金連「簽約即付，餘額殺青入帳」都同 var-note 第三行重複） |
| 通告期間 bar／完成期限 bar | 重複（同摘要行同一值） |
| 每週開工 pattern（`weeklyBlock`） | 唯一 → 搬入摘要，**只喺 total>1** |
| 特殊限制（`gigSpecialLimitsHtml`） | 唯一 → 搬入摘要，有先出 |
| 導演（`gigDirectorLabel`） | 唯一 → 搬入摘要，**只出真名** |
| 製作人（`gigProducerLineHtml`） | 唯一 → 搬入摘要，有先出 |
| **劇情簡介（`notice_synopsis_frame`）** | **唯一，任務書對照漏咗** → 搬入摘要（見下） |

**任務書遺漏（已核實，唔係假設）：劇情簡介只喺詳細區出現。**
通告欄 teaser（`gigBoardTeaserHtml`）冇簡介；`gigCardHtml`（有簡介）只喺手帳拍攝簿
（待試鏡／已殺青 list）同「未能試鏡」modal 先出，正常「撳卡 → 詳情」流程入面，
詳細區係簡介唯一家園。照字面成段刪會令成張卡冇晒簡介——故第 5 項救返，
markup 原樣搬入摘要（`.notice_synopsis_frame` CSS 照用），並喺代碼註釋寫明。
角色 hint（`cn-role-note`）跟埋簡介一齊搬。

## 導演 fallback 調查（全庫）

- `gigDirectorLabel` fallback 係「組製未公開」，唔係「副導」——「副導」係數據本身嘅值。
- 實駕普查（`window.GIGS`，live pool **183 張**，0 張缺 director）：
  職銜值（唔係人名）共 **31 張（16.9%）**——「副導」×19、「副導阿標」×4、
  「廣告助導」×3、「特輯副導」×1、「場務阿強」×1、「外景場記」×1、
  「平面攝影師阿忠」×1、「錄音室助導」×1；其餘 **152 張係真名**。
  （對照：內容包 `content/gigs_1988.json` 143 張計 6 張 generic；內嵌池 149 值計 11 張；
  live pool 183 張因為仲有年庫／entry  gigs 併入，副導×19 主要嚟自年庫。）
- 決定：導演欄只出真名，8 個職銜值＋fallback「組製未公開」一律唔出。
  「副導阿標」等雖有花名，但係場務職銜唔係導演名，同樣濾走。
  兩張目標通告都係 generic（《戲院人潮》「副導」、《賀歲特輯》「特輯副導」），
  故兩張改後都唔出導演行——係按規則出嚟嘅結果，唔係 bug。
- 製作人：live pool 94/183 有製作人；兩張目標通告都冇（`producer: null`），故兩張都唔出。
  特殊限制：126/183 有 `limits` 物件，114/183 有 `limits.notes`；兩張目標都係「冬季入門」。
- 每週 pattern：兩張目標都係 total=1，故兩張改後都唔出「每週最多 6 日」——按規則。

## 改動（`index.html`，5,096,097 bytes；−91 行淨）

### 1. 刪走成個詳細區（`castingNoticeDetailHtml`）
- 模板：刪「顯示詳細 ▾」掣＋`.cn-detail` 成塊（條件表、檔期／片酬表、導演行、
  製作人行、期間 bar、期限 bar、簡介框），約 34770–34800 行舊位；唔留空殼、唔留死掣。
- 死 const 一併刪：`condParts`（條件表）、`deadlineBar30v2`（期限 bar）、
  `roleLine`（`gigRoleLineHtml` 唯一調用點，從來冇渲染過——角色職位已由摘要區
  `starsRoleRow30v2` 嘅 `cn-role30v2` 承載；`dir` const 一併刪，導演改由 helper 讀）。
- 刪 `gigRoleLineHtml` 函數（約 34531 行舊位，死咗）＋v19z8「顯示詳細」掣接線
  （`[data-cn-toggle]` forEach block，約 34136 行舊位）。
- 死 CSS 一併清：`.cn-detail-toggle`／`.cn-detail[hidden]`／`.notice_table_frame`／
  `.notice_table_cell`／`.cn-cond-row`／`.notice_period_bar`／`.cn-director-line`／
  `.cn-producer-line`／`.cn-role-line`（＋paper30v2 層同名 override＋兩句過時註釋）。
  保留：`.cn-kv`／`.cn-kv-weekly`／`.cn-wd-sub`／`.cn-limits`／`.notice_synopsis_frame`
  （搬入行照用）／`.notice_director_slot`（舊 legacy chip，唔關今包事）。
  驗證：全檔再無 `cn-detail`／`notice_table_frame`／`cn-cond-row`／`notice_period_bar`／
  `cn-director-line`／`cn-producer-line`／`cn-role-line`／`data-cn-toggle` 實碼
  （淨返 v117 解釋註釋）。

### 2. 唯一資料搬入摘要區（`castingNoticeDetailHtml` 約 34640–34700 行）
順序：預計播出之後、差距／情報／var-note 之前（事實行尾）。
- 特殊限制：`${limitsHtml}` 原樣（`gigSpecialLimitsHtml`，空即隱藏）。
- 導演：`${directorRow117}`，`gigDirectorRealName117(g)`（約 34234–34240 行，
  `GIG_DIRECTOR_GENERIC117` Set：8 職銜值＋「組製未公開」），真名先出 cn-sum-row。
- 製作人：`${producerLine}`，`gigProducerLineHtml`（約 34506 行）改出 cn-sum-row
  （文字一字唔郁：label「製作人」＋名；冇即隱藏）。
- 每週開工：`${weeklyRow117}`，`(total > 1) ? weeklyBlock : ""`——`weeklyBlock` 原樣，
  包括「實際只需通告 N 日」只喺 total<weekly 跟埋出嘅原條件。
- 劇情簡介：`${synopsisFrame117}`，markup 原樣搬（見「任務書遺漏」）。

### 3. 通告欄卡片 meta 拆行（`gigBoardTeaserHtml` 約 34359–34410 行）
- **實駕先確認：實際渲染只得兩段**——「片酬 $520 · 拍攝約 1 日」（單一文字節點，0 子元素）。
  任務書／v115 NOTES 話嘅第三段「獲聘後 N 日內完成」並唔喺 teaser meta 出現
  （嗰句係詳情頁「完成期限」行嘅值）——按實際兩段拆，唔憑空加第三段。
- 舊：`const meta=[pay, days].filter(Boolean).join(" · ");` → `<div class="gt-meta">${meta}</div>`
- 新：`const metaParts=[pay, days].filter(Boolean);` →
  `<div class="gt-meta">${metaParts.map(m=>`<div class="gt-meta-line">${m}</div>`).join("")}</div>`
  ＋ CSS `.gig-teaser .gt-meta-line{ display:block; }`（約 2815 行）。數字／文字一字唔郁。

### 唔郁
v115 文字一句唔郁；數字一概唔變；SAVE key（`starVolunteer_map_v19w`）／softRev（`s107`）／
產品 `?v=`（`v20a10`）唔郁；content pack JSON 唔郁。

## 測試

- 新守門 `tests/test_s30dedup117_static.py`：**33 項全 PASS**。
  斷言：(a) 掣＋`.cn-detail`＋死接線＋死 CSS 已刪 (b) 五個搬入位喺摘要區＋順序啱＋
  導演 generic 集齊 8 值＋fallback／每週 pattern 只喺 total>1／製作人改 cn-sum-row／
  簡介搬入 (c) meta 用 metaParts 逐行、舊 `join(" · ")` 已刪、渲染只讀 metaParts
  (d) v115 文字＋紅線不變。
- **反證**：喺未修版（`git stash` index.html）跑新測試，22 項 FAIL——新測試喺舊版式上
  會 FAIL 成立。
- 同步更新兩個現成測試（寫明點解，唔係放寬）：
  - `tests/test_ui108_static.py` S-33：舊斷言「違約金行喺掣之前（唔使展開先見）」→
    「掣已移除＋違約金行喺摘要區」——全卡即摘要，「唔使展開」已成結構事實。
  - `tests/test_s30text115_static.py` T4：舊斷言詳細區「簽約即付，餘額殺青入帳」不變 →
    該句已隨詳細區刪除（同 var-note 第三行重複），改斷言摘要「獲聘先收三成簽約金，
    餘額殺青先收。」保留同一時點。
- 主 script 抽出 `node --check` 通過。
- 全套 A/B（`qa111/run_suite.py`）：基線 **152 PASS／12 FAIL** →
  工作版 **153 PASS／12 FAIL**（+1 係新守門檔；FAIL 清單逐字相同：
  flash51／giglib36／pacing35／poster59／rumor49／slot50／soft_tip_111_restore／
  start53／weave43／weave44／weave49／wrap38——poster59 係舊資產計數問題，
  同今包無關）。**零新增回歸。**

## 實駕對照（Playwright 390×844，`?softPreview=1`，本地鏡像＋http.server）

工具：`qa117/drive117.py`（改編自 v115 drive；兩地點：星河電視台＋維港電影），
產出 `qa117/drive117_before.json`／`qa117/drive117_after.json`＋`qa117/shots/` 15 張截圖。
**pageerror／console.error：兩版都係 0。**兩版都冇觸發 ENC79 巧遇。
入維港電影嗰陣隨機觸發入場事件鏈「通宵廠凌晨三點」（繼續→睇落去→二揀一
「上保母車瞓陣先」→好），drive 逐個撳走先入到板（棄用槽存檔，log 低咗；
舊版初版 drive 未處理呢條鏈，cinema 一度入唔到板——已修 driver，兩版用同一 driver 重跑）。

### 《賀歲特輯》（`gig_1988_entry_winter_cny_crowd`，星河電視台）
| 項目 | 改前 | 改後 |
|---|---|---|
| 欄卡 meta | 片酬 $520 · 拍攝約 1 日（單行） | 片酬 $520／拍攝約 1 日（兩行，2×`DIV.gt-meta-line`） |
| 摘要 8 行 | 片酬 $520（約酬 $420–$620）／簽約金 約 $156（獲聘後即收）／違約金 $120／通告日數 共 1 天／通告期間 1990年冬季檔／完成期限 獲聘後 10 日內／報名截止 仲有 5 日截止／預計播出 1990 年農曆新年特輯 | **逐字相同** |
| 特殊限制 | 只喺詳細區：冬季入門 | **摘要區有：特殊限制｜冬季入門** |
| 導演 | 詳細區：導演：特輯副導 | **唔出**（generic 值，按規則） |
| 製作人 | 無 | 無（數據本身冇） |
| 每週開工 | 詳細區：每週最多 6 日／逢週一至六／實際只需通告 1 日 | **唔出**（total=1，按規則） |
| 劇情簡介 | 只喺詳細區 | **摘要區有**（全文＋角色行不變） |
| 顯示詳細掣 | 有（摺疊） | **消失** |
| 詳細區 | 有（條件／日數／片酬／簽約金／期間 bar／期限 bar，全部同摘要重複） | **消失** |

### 《戲院人潮》（`gig_1988_entry_winter_cinema_crowd`，維港電影）
同上，數字不同：片酬 $500（約酬 $400–$580）／簽約金 約 $150（獲聘後即收）／
違約金 $120／通告日數 共 1 天／通告期間 1990年冬季檔／完成期限 獲聘後 10 日內／
報名截止 仲有 5 日截止／預計播出「趕賀歲檔：預計 1990 年農曆新年上映」；
導演「副導」改後唔出；特殊限制「冬季入門」搬入摘要；簡介搬入摘要；掣＋詳細區消失。
（預計播出值「趕賀歲檔：…」唔 match v115 regex 故 label 退回「預計播出」——v115 既有行為，今包唔郁。）

### 目測
`after_cny_sheet.png`／`after_cny_sheet_bottom.png`／`after_cinema_sheet_bottom.png`／
`after_cny_board.png`：無掣、無重複行、特殊限制行＋簡介框齊整、欄卡 meta 兩行。
既有瑕疵（唔關今包事）：「難易度 ★★☆☆☆ 角色職位拜年群演」兩段黐埋（舊版已有）；
沈卓衡頭像仍係舊寫實風（v116 換圖進行中）；`#mask.casting-sheet-on` 附近一句歷史註釋
提及「摺疊狀態」（純註釋，零行為影響，留返唔郁）。

## 殘留缺口
- ~~每週 pattern／導演真名／製作人三行喺兩張目標通告全部唔出（兩張都係 1 日＋generic 導演＋
  無製作人）——規則本身啱，但實駕未能親眼見到呢三行喺摘要區出現嘅樣。現成對照：
  《靈幻喜劇迎春夜》`gig_1988_tvb_longmen_spring_high`（星河電視台同板）係多日
  （shootDaysHint 5）＋真名導演黃志鳴＋製作人鄧啟東，三行應該齊出——
  建議合併前／線上核實嗰陣開呢張睇埋。~~ **已補驗（統籌，rebase 後）**：
  `qa117/drive117_spring.py` 實駕《靈幻喜劇迎春夜》，0 pageerror——摘要區親眼見到三行齊出：
  導演 黃志鳴／製作人 鄧啟東／可開工 每週最多 6 日＋逢週一至六＋「實際只需通告 2 日
  （唔係每週做滿）」（total=2＜weekly=6 嗰句跟埋出）；特殊限制「須接受高壓檔期安排」＋
  劇情簡介＋角色行齊全；掣＋詳細區消失。證據 `qa117/drive117_spring.json`＋
  `qa117/shots/spring_spring_sheet.png`／`spring_spring_sheet_bottom.png`
  （bottom 截圖頂行半裁係碌位 artifact，DOM JSON 核實文字無誤）。
  欄卡 meta 亦係兩行「片酬 $3,000」／「拍攝約 2 日」。

## 合併後補記（統籌）
- Rebase：分支由 `4d967ed` rebase 上 main `2d71588`（v114 `cf66865`＋NOTES），乾淨無衝突，
  新 commit `42b37db`。
- **travel114 行號同步（rebase 後新問題，唔係 v117 內容錯）**：全套重跑 154 PASS／13 FAIL，
  唯一新增 FAIL 係 `test_travel114_static.py`（main 上 PASS）。根源：該測試將
  `FREE_LINES`／`COUNT_LINES`／`DEF_LINE`／`WRAPPER_LINE` 寫死做行號，v117 刪詳細區
  淨 −93 行令行號移位（−75 行喺 ~34136 行之前、−93 行喺之後）。修法：逐行經 difflib
  對位舊 main 行內容核實新行號（唔係得個常數偏移），同步測試兩個清單＋兩行常數；
  測試本身嘅覆蓋檢查（零漏網呼叫點）即係反證。結果：該測試 68 PASS／0 FAIL。
  全套重跑：**155 PASS／12 FAIL**（v114 main 154／12＋新守門檔 1；FAIL 清單逐字相同），零回歸。
- 合併：squash 入 main（見 main commit），線上 curl 核實 byte＋sha（見下）。

## 線上核實
- main commit：`ae1d8b1`（squash；分支 `v117-s30-layout` `42dfb0a`）
- 本地 index.html：5,099,862 bytes，sha256 `c6bb45b8…`
- 線上 index.html：5,099,862 bytes，sha256 `c6bb45b8…`（已對上；首查仍係 v114 舊版
  5,101,629／`672e34db…`，Pages 部署停滯，推呢個 NOTES 補記重觸發後對上）
- 導演 generic 集係窮舉已知 8 值：將來年庫加新職銜值（例如「副導阿強」）會漏網而出街——
  可接受，測試釘死咗已知 8 值；要根治先改做職銜關鍵字規則，另開一票。
- 本分支基於 main `4d967ed`；期間 v114 已合併入 main（`cf66865`，出行額度 2 次／日）——
  收尾 rebase 嗰陣留意：drive 一日入兩個地點，v114 下會計 2 次額度（剛好夠用，唔會被擋）。
