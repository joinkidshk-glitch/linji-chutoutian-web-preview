# NOTES_V20A295 — Q8： 「點擊」→「撳」成對拎走，全部用「點擊」

基線 main `de48472`（v294），suite 358／9 → **359／9**（+1 係新測試）。

## 1. 改咗咩（index.html，21 行原位替換，淨行數 0）

### 1.1 核心：TEXTFIX57_PHRASES 拎走第四對
`const TEXTFIX57_PHRASES = [["事態","劇情"],["聲量","聲望"],["周刊","週刊"],["點擊","撳"]];`
→ `[["事態","劇情"],["聲量","聲望"],["周刊","週刊"]]`（L14445）。
其餘三對唔郁；`textfix55Str` 循環（L14500）同 `textfix55Str` 本身唔郁。

### 1.2 點解淨刪一對唔夠：source 硬寫咗 19 處「撳」
親查發現：`點擊` 喺 index.html 得 9 命中，全部係註解／TEXTFIX 區本身——玩家面 source 字串根本冇寫「點擊」，係直接寫「撳」。即係話，淨刪 mapping 嗰對，呢啲字串照樣出「撳」，Q8「全部用點擊」做唔到。所以連同 source 硬寫嗰 19 處非對白「撳」一併改做「點擊」（全部原位單詞替換，行數不變）：

| 位置 | 字串 |
|---|---|
| L14270 醫院 FAQ | 撳入嚟睇 → 點擊入嚟睇 |
| L20429 手帳 | 改完要撳確定才生效 → 改完要點擊確定才生效 |
| L20735 手帳唯讀 | 可撳「壓力估」→ 可點擊「壓力估」 |
| L20927 行程 toast | 要過日請撳「開始今日行程」→ 請點擊 |
| L21137／21139／43536 遮罩提示 ×4 | 撳外面＝回家結算／返回地圖／繼續跑明日行程／開始今日行程 → 點擊外面＝… |
| L22204／22215 自由日 title ×2 | 逛完撳這個掣 → 逛完點擊這個掣 |
| L32039 頒獎 overlay | 撳畫面可以快進 → 點擊畫面可以快進 |
| L45587 通告欄 toast | 請在地圖撳有通告的地點 → 請在地圖點擊 |
| L14274 體檢提示 | 撳「身體檢查」嗰陣會先確認 → 點擊 |
| L18799 訓練跳轉提示 | 撳下面「去訓練／手帳」→ 點擊下面 |
| L20712 手帳提示 | 撳「確定出發」就會落實行程 → 點擊 |
| L42170 對白鎖提示 | 撳「完成對白」才可以繼續 → 點擊 |
| L45200 禮物提示 | 地點選單撳「買禮物」買入 → 點擊 |
| L45622 拍攝簿提示 | 撳下面可直達 → 點擊下面可直達 |

後 6 處匿喺 template literal 入面，普通引號掃描搵唔到，係跑 `test_terms57_static.py` 嗰陣由佢個 tokenizer 捉到——教訓：**唔好淨信引號 grep，要用 tokenizer 掃**。

### 1.3 順帶對齊（同樣原位，唔加行）
- TEXTFIX57_EXACT 教學句值（L14421）：「再撳「確認拼合」。唔識拖都得，撳嚟揀都得。」→「再點擊「確認拼合」。唔識拖都得，點擊嚟揀都得。」呢條係死 entry（key 嗰句舊版教學句只喺 `content/MOCK_TUTORIAL_PHASE2_STEPS_5_6_COPY_SOFT_v1.json` 出現，mock 唔係 runtime load），改佢純粹等表內術語一致。
- L14432 註解：刪「；點擊→撳」（過期說明）。
- L30808 註解：`撳出席唔係即刻播` → `點擊出席唔係即刻播`（static tokenizer 會將呢行註解誤認做字串內容，唔改會令 A4 靜態檢查誤報；註解本身跟新術語亦啱）。

### 1.4 刻意唔郁
- 對白入面嘅「撳」（廣東話對白，合法）：藍若曦「專幫人撳通告牌」「第日你唔使人撳牌嗰陣」＋結局段引述佢嗰句（L13267）。靜態檢查 whitelist 寫明只准呢啲（`撳牌`／`撳通告牌`）。
- CSS／HTML 註解入面嘅「撳」（唔係玩家面文字），除咗 L30808 上面講嗰行。
- 其餘三對 mapping、三個 TEXTFIX57 表、textfix55Str 機制。

## 2. 測試

### 2.1 更新舊測試（跟 source 一齊改）
- `tests/test_terms57_logic.js` A4：舊斷言「點擊→撳」改做三條——「請點擊繼續」原樣通過、混合輸入原樣通過、表入面冇咗「點擊」對。
- `tests/test_terms57_static.py` A4：舊「零點擊」改做「零撳（對白撳牌除外）」＋「UI 字串用點擊」三處 spot check。
- `tests/test_dayend202_logic.js`（12 處）＋`tests/test_dayend202_static.py`（3 處）：「撳外面＝」→「點擊外面＝」。其餘含「撳」嘅測試名／註解係 dev 面文字，唔郁。

### 2.2 新測試 `tests/test_r295_click_not_gam.js`（29 項，ALL PASS）
- 表得返 3 對、冇「點擊」對；其餘三對照常轉換。
- `textfix55Str` 喺 body／lines／title 三種 key 都留低「點擊」。
- 19 處 UI 字串逐個 spot check＋「撳外面」零殘留；對白「撳通告牌」／「撳牌」保留；EXACT 教學句值用「點擊」。

### 2.3 全套 suite
`bash qa131/run_suite.sh` → **TOTAL PASS 359 FAIL 9**。9 項 FAIL 全部係已知 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38），零新增。
針對覆驗（改前後逐個跑）：test_r295_click_not_gam.js ALL PASS、test_terms57_logic.js ALL PASS、test_terms57_static.py（A4 兩條 PASS，零 FAIL）、test_dayend202_logic.js ALL PASS、test_dayend202_static.py 30 PASS 零 FAIL。

## 3. 釘行
index.html 淨行數 0（21 增／21 刪，全原位替換），唔使 resync；suite 一次過 359／9 證明。

## 4. 殘留
- 內容 pack 入面仲有「撳」字：`content/story_detail_romance_lan_xu.json` 有 2 處，全部係藍若曦對白（「專幫人撳通告牌」「第日你唔使人撳牌嗰陣」，同 index.html 嗰兩句同一出處），合法，唔郁；`content/MOCK_TUTORIAL_PHASE2_STEPS_5_6_COPY_SOFT_v1.json` 有 3 處，mock 檔唔係 runtime load。live load 嘅 pack 入面「點擊」命中為 0——即係話，pack 入面冇嘢等緊呢對 mapping 轉換，刪對之後 pack 行為不變。
- 對白「撳」保留，係有意嘅（廣東話對白）。
