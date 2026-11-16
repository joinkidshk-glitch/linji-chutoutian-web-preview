# NOTES_V20A243_RW6_GIGS

版本：v20a243（RW-6：新通告覆核）
日期：2026-11-16
Base：main 466827b（v242）

## 目的

語言逐句重寫第 6 批。覆核 `content/gigs_new.json` 241 張新通告（v229 新庫 240＋v232《星夜迷離》），
逐句重寫唔合香港式書面語嘅 synopsis／roleHint 等文字欄位；順手裁定 TEXTFIX55 GIG 五組死碼。
只改文字，零邏輯／數值／旗標／判定／派發規則改動。

## 逐張清單（開工前盤點，見 linji-language-sample/RW6_CHECKLIST.md／.csv）

- 241 張逐張列出：synopsis 合格 141／重寫 79／覆核 21；roleHint 合格 146／重寫 88／覆核 7；兩邊都合格 125 張。
- 全庫計句（按 。！？；＋換行切句）：1,722 句（title 241／blurb 241／synopsis 807／roleHint 242／posterBrief 141／boardNote 2／discoverNote 48）。
- 計劃估算 500–800 句實寫；實寫約 676 句（工人自數）／統籌 zip 法重數 705 句（拆句計法差異）。
- 改動文字欄位共 148 張（工人 147＋統籌補 1 張 posterBrief 主角名）。

## 改動

### 1. content/gigs_new.json（diff 602 行，301+/301−）

- 三份工人草稿全數套用：A 電影 63 張（130 欄位）、B 廣告＋綜藝 66 張（119 欄位）、C 電視劇＋唱片 112 張（44 欄位）。
- 統籌修正 8 項：
  - `gig_1991_rec_102` synopsis 還原 G5 引言句（「」引住對白留廣東話）。
  - `gig_1992_film_118` synopsis「好感」→「雙方交情漸深」。
  - 6 張 posterBrief 主角名按 `leadStarId` 修正（全庫掃描證實只得呢 6 張錯配；synopsis／blurb／discoverNote 零錯配）：
    `gig_1990_rec_109` 陸柏言→顧明輝；`gig_1990_ad_103`／`gig_1992_ad_107` 陸柏言→蘇芷茵；
    `gig_1990_ad_108`／`gig_1992_ad_104` 陸柏言→彭少祺；`gig_1990_ad_107` 廖炳星→陸柏言。
  - 補 6 處殘留「同」作連詞（電影 posterBrief／blurb）。
- 分類／邏輯欄位（title／roleLabel／roleScale／category／type／tier／year／days／pay／req／loc／season／genre／director／leadStarId／trigger／storyKeys／boardNote）對 HEAD 0 改動，`press94RoleClass` 結果不變。

### 2. index.html（淨 −11 行，44,464 → 44,453 行）

刪 TEXTFIX55 GIG 五組（舊通告庫專用；新庫 241 張 0 命中，死碼）：
`TEXTFIX55_GIG_EXACT` 40／`GIG_SUB` 34／`GIG_PHRASES` 19／`POLICY_KW` 17／`ERA_KW` 7，共 117 條。
刪 `textfix55GigField` 入面 4 處引用（EXACT 查表、SUB 循環、PHRASES 循環、POLICY／ERA 兩行 dropSents）。
留一則 v243 刪除註解。`TEXTFIX57_GIG_REQ`（體力→體能）保留。

### 3. 測試（12 檔）

- 刪層後釘死期望值改做直出／守衛（斷言保留）：`test_text55_logic.js`、`test_newspaper214_award_logic.js`、
  `test_newspaper214_award_static.py`、`test_contra98_static.py`。
- 淨 −11 行引發釘行漂移，resync 8 檔（按段重算＋逐行核實內容逐字相同，純漂移；公式加 v243 項）：
  `test_gift185_static.py`、`test_kwan151_static.py`、`test_rom176_static.py`、`test_tang152_static.py`、
  `test_tang171_static.py`、`test_tang173_static.py`、`test_text125_static.py`、`test_travel114_static.py`
  （travel114：FREE 27 處＋COUNT 12 處＋DEF／WRAPPER 各 −11；resync 途中發現 FREE_LINES 一次漏移，
  原因係集合內註解 `{travelFree}` 嘅 `}` 截斷咗段邊界，改用整行 `}` 做邊界重做，之後 PASS）。
- `test_text55_static.py`、`test_terms57_logic.js` 唔郁，PASS。

## 裁定（逐處核實過）

- 「直播」全部 KEEP（22 個欄位，全部 1990–92 電視直播）。
- 「打歌」真違規只得 1 張：`gig_1990_variety_106`（blurb＋synopsis「打歌節目」→「新歌推介節目」）。
- `gig_1992_rec_103` 4 處「《主打歌》」係作品名，假陽性，KEEP。
- 「體力」4 張 roleHint 源頭寫體力、live 經 TEXTFIX57_GIG_REQ 顯示體能；TEXTFIX57 層 KEEP，重寫按 live 寫體能。
- title 一字唔郁（《屋企人》《主打歌》保留）；roleLabel／roleScale／category 唔郁；boardNote 2 張都係「長期合約」；
  storyKeys（33 張）／trigger（47 張）係內部條件。
- TEXTFIX55_EXACT 剩 58 條同通告文字 0 重疊，唔係 RW-6 範圍，留 RW-7。
- 機器預篩漏咗一批粵語詞，工人人手捉出：作連詞用嘅「同」、跟足／聽足、帶住、先至、學嘢／教路／撞正／幫手／成日、周圍搵食、
  系統名入敘述、「於…進行」、discoverNote 碎片句。
- 合併後全庫殘留掃描乾淨：強標記只剩 rec_102 G5 引言句嘅「唔」（有意保留）；synopsis 入面「你」0 處；
  「電視城」30＋處係全庫一致嘅場地名（非公司名），留低唔郁。

## 載入模擬

方法：由已改 index.html 抽出 `textfix55GigRecord`，跑晒 241 張，對照重寫後源頭。
結果 0 diffs——live 文字＝重寫後源頭逐字相同。

## 驗收

- `node --check`／vm.Script 編譯 inline script blocks 通過。
- 全套 suite：**314／10**，同基線一致；10 項 FAIL 全部係已知 pre-existing
  （flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。
- 8 檔 resync 測試逐檔直接跑全部 PASS。
- Read-aloud＋10 句試讀：抽查 5–10 句係逐句重寫，唔係逐詞換；對白無逐詞換普通話。

## 跟進（唔係本票範圍）

- `textfix55GigField` 殘留死行為（5 條舊庫模板 regex、「虛構」剝除、blurb／synopsis 互補、roleLabel 映射）喺新庫 0 命中，留 RW-7。
- `gig_1990_ad_104`／`gig_1991_ad_104` synopsis 入面林曉晴／徐寶珊世界參照句，屬風格寫法，留低唔郁。
- TEXTFIX55_EXACT 剩 58 條，留 RW-7。
- 實機驗證押後（瀏覽器死）：新通告文字實機抽檢。
