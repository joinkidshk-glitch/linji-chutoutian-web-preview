# v20a239：RW-4 報紙＋頒獎逐句重寫（語言重寫第四批）

- Base：main `4e30ebd`（v238）。分支 `v239`。
- 範圍：晨報＋故事報紙＋頒獎禮模板＋post-shoot 四檔，逐句重寫做香港式書面語（報紙一律正式書面語；人物原話引述例外，放引號入面）。只改玩家可見文字，唔改邏輯／數值／旗標／獎項判定。
- 改寫實數：**219 處字串**（晨報 81＋故事報紙 52＋頒獎 52＋殺青 34）；舊句 316 → 新句 313（晨報併句 −2、頒獎拆句 ＋2／併句 −3）；保留未改 112 處。
- 報紙全名：陳偉翔 86 處（晨報 32＋故事報紙 47＋頒獎 press 3＋殺青 press 4）；典禮敘述行用「阿偉」30 處（同主線旁白一致，見工作報告 §9 訂正 3）。
- 系統名清零：聲望／幕前聲望／信用／壓力／聲量 0 命中；「人氣」6 處全部喺殺青 metric 顯示字串（舊源頭寫「關注度」，postOpts 載入已映射做「人氣」，玩家見到嘅值不變）。
- TEXTFIX55_EXACT：165 → 145（A 組刪 20）→ **134**（B 組刪 11）；暫留 7 條（S-41 1 條＋NP214 6 條，測試釘死映射本身）；另刪 newsOpts「幕前聲望→聲望」短語 1 條；`newspaperCheck()` 三處「嗌交」錨點改做「爭吵」。
- 載入模擬（抽 index.html 真實 textfix 函數）：新句 0 處被 TEXTFIX55 覆寫；刪 11 條 EXACT key 模擬結果不變。
- 測試改動：3 檔 content-pack guard 加 v239 豁免（頒獎＋殺青兩檔；晨報／故事報紙已喺 v217／v210 豁免入面），只加豁免集，無改斷言期望值。詳見 `~/workspace/linji-language-sample/RW4_WORKLOG.md` §7。
- Suite：**314／10**，FAIL 名單同基線逐項一致（flash51／rumor49／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。
- 獎項對照核實：模板「提名／得獎」字眼跟典禮級判定一致，無錯寫（5 個 null catId 係典禮級觸發）。
- 試讀：A 組 10／10＋B 組 10／10 通過；防逐詞換抽查 5＋5 組全部結構性重寫。

## 重要發現（今批最大事項，另開票跟進）

RW-4 完成咗源頭重寫，但玩家實際見到嘅頒獎新文案好少——覆寫層遮住咗大半：

- `AWARDS188_CATEGORIES`（index.html）優先於 stub，15 個 live catId 全部回 AWARDS188 舊廣東話行；重寫嘅 36 處 stub 類別行係死 fallback。
- `VENUE99_*` 覆寫 inviteDek／press dek／news line 各 3 處（廣告／金碟夜／影藝獎）；live 嘅新頒獎句只有 4 處（台慶 inviteDek、金碟夜 press headline、台慶 press dek、台慶 news line）。
- `AWARDS188_NP_WIN`／`VENUE99_NP_DEK` 覆寫報紙 award 模板 27 處，live 渲染仍有 4 處「聲望」嚟自 overlay。
- 下一票必須重寫 index.html 內嘅 `AWARDS188_CATEGORIES`、`VENUE99_*`、`AWARDS188_NP_WIN`、`PSR_EXTRA_TEMPLATES_35` 同 `buildAwardResultPack` 內嵌 fallback 字面，連 `test_awards192_logic.js` B1／`test_awards188_logic.js` §5 錨點更新。殺青 34 處全部 live（但 `PSR_EXTRA_TEMPLATES_35` 23 張舊廣東話模板同池隨機抽）。

## 檔案

- `content/STUB_NEWSPAPER_MORNING_SOFT_v1.json`（81 處）
- `content/STUB_NEWSPAPER_STORY_SOFT_v1.json`（52 處）
- `content/STUB_AWARDS_CEREMONY_v1.json`（52 處）
- `content/STUB_POST_SHOOT_REWARDS_v1.json`（34 處，含統籌微調 1 處：metrics[3] blurb「街外認人慢熱」）
- `index.html`（TEXTFIX55_EXACT −31、newsOpts −1 短語、newspaperCheck 3 錨點）
- `tests/test_newspaper214_award_static.py`、`tests/test_aud91fix122_static.py`、`tests/test_aud91fix124_static.py`（v239 豁免）
- 工作報告：`~/workspace/linji-language-sample/RW4_WORKLOG.md`（草稿 `RW4A_DRAFT.md`／`RW4B_DRAFT.md`）
