# NOTES_V20A292_RENAME_LEAD_SONG.md — v20a292 Q4：兩張《主打歌》唱片通告改名

- 基線：main `f796fa7`（v291 已落地，suite 354／9，庫 302 張）。
- 範圍：只改名，唔改 gig id、singer、pay、tier、season、year、cast、req、trigger。

## 1. 新名

| gigId | 舊名 | 新名 | 季節 |
|---|---|---|---|
| `gig_1992_rec_108` | 《主打歌》MV 男主角 | **《只差一步》MV 男主角** | 1992 秋 |
| `gig_1992_rec_111` | 《主打歌》MV：銅鑼灣街頭男主角 | **《銅鑼灣》MV 男主角** | 1992 春 |

兩張都係陸柏言（`luk_baakyin`）新碟主打 MV 男主角、高級、pay [600, 720]、req 演技 85／台風 65／歌藝 55。

## 2. 命名依據（TITLE_AUDIT §4 唱片規律＋R1–R8）

- 歌名是一句話／一個意象，唔係分類（R1／R8）：「主打歌」係功能詞，唔可以做名。
- **《只差一步》**（rec_108，秋）：四字短句。雙關——樂壇封王前夕「只差一步」登頂；情歌內容「差一步講出口」。無高頻字（夜／笑／星），2–5 字，唔含年份數字（R5）。
- **《銅鑼灣》**（rec_111，春）：地名做歌名，對照〈皇后大道東〉；MV 本身就係銅鑼灣街頭雨夜追電車（男主角由街角唱片店出發，追趕電車，雨中相遇）。AUDIT §6 樣本 11 曾提議用《銅鑼灣》取代一張《主打歌》（嗰張係另一張已不存在嘅搖滾／中級／1992 夏 gig）；本票實裝前補做網上撞名抽查。
- **網上撞名抽查（2026-11-18）**：
  - 《只差一步》：無香港歌曲同名。近似唔同名：《差一步》（大壯，國語）、《一步之差》（1935 探戈 Por una Cabeza 譯名）、《差一步就離開》——全部唔係同一個名。
  - 《銅鑼灣》：無香港歌曲同名。搜到嘅只係歌詞入面提及銅鑼灣呢個地名、《香江銅鑼灣》（2026 原創，唔同名）、The Weeknd《Hong Kong》（2026，唔同名）。
  - **棄用**：《一步之遙》撞任然同名國語歌；《並肩行》撞庫內已有《並肩前行》（R3 近似對）。
- 庫內核實：兩新名喺全庫各只出現一次；唔撞主線章標題（R4）；唔撞 RESEARCH 真名表。

## 3. 改動清單

### content/gigs_new.json（7 行）
- rec_108：title →《只差一步》MV 男主角；workTitle → 只差一步；blurb「新碟主打歌音樂錄影帶」→「新碟《只差一步》音樂錄影帶」；synopsis「這首主打歌是他新碟的重點」→「《只差一步》是他新碟的重點」。
- rec_111：title →《銅鑼灣》MV 男主角（舊 title 尾段「：銅鑼灣街頭男主角」刪走，唔係新名會同地點重複兩次）；workTitle → 銅鑼灣；blurb「新碟主打歌音樂錄影帶春季拍攝」→「新碟《銅鑼灣》音樂錄影帶春季拍攝」。
- 其餘欄位全部唔郁。posterBrief／roleLabel／roleHint／discoverNote 本身無舊名，唔郁。

### index.html（2 處）
- BR89 註解（L26330 附近）：「《主打歌》MV（駱）→gig_1992_rec_111《主打歌》MV」→「《銅鑼灣》MV（駱）→gig_1992_rec_111《銅鑼灣》MV」。
- N14_a 即派 reason：『陸柏言新碟《主打歌》MV要個銅鑼灣街頭男主角』→『陸柏言新碟《銅鑼灣》MV要個街頭男主角』（第二個「銅鑼灣」刪走，唔重複）。

### 測試（2 處更新）
- tests/test_gig229_grant.js：label「T1 N14_a 主打歌MV→rec_111」→「T1 N14_a 銅鑼灣MV→rec_111」。
- tests/test_r5_283_logic.js：`['credit_enc83_lok_patron', '主打歌']` → `['credit_enc83_lok_patron', '銅鑼灣']`（creditRedeemLine283 出嘅「可以換：」行跟 gig title）。

### 刻意唔郁
- `gig_1992_rec_109` synopsis「憑這張大碟與主打歌雙線出擊」：「主打歌」係通用詞（指嗰張大碟嘅主打歌），唔係舊名引用；改咗句子唔通。NOTES_V20A243 同類判斷（rec_103 假陽性）一致。
- index.html N8_b reason「坐喺主打歌星隔籬」：通用詞，唔係標題引用。
- 全部 NOTES 檔（V20A243／V20A253／V20A254／V20A278／V20A280）：歷史落地記錄，唔改。
- qa149/pristine_index.html：QA 快照，唔改。

## 4. 新測試

- tests/test_r292_rename_lead_song.js（20 項）：新名、兩名唔同、全庫 workTitle「主打歌」清零、其餘欄位不變、trigger 照舊、新名各只出現一次、blurb／synopsis 跟名、index.html 接駁位。
- tests/test_r292_rename_lead_song_static.py（14 項）：同上 JSON 部分。
- 兩檔 ALL PASS。

## 5. 測試結果

- 新測試兩檔 ALL PASS。
- 受影響現有測試：test_awards63_logic.js ALL PASS（singer 唔變，提名人收集唔受影響）、test_gig229_grant.js ALL PASS、test_r5_283_logic.js ALL PASS。
- 全套 suite：**TOTAL PASS 356 FAIL 9**（`~/workspace/suite_v292.txt`）。基線 354／9，新加 2 個測試檔全部 PASS，9 項 FAIL 全部係已知 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），無新增失敗。
