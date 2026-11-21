# v359 支線＋感情線複檢最後 5 項修復（文風 4＋部分證實 1）

基線：v358（main `76c0e02`）。Suite：**TOTAL PASS 398 FAIL 9**，同基線一致，九項全係 pre-existing（flash51／slot50／soft_tip_111_restore／start53／weave43_static／weave44_static／weave49_static／wf5_87／wrap38），零新 FAIL。`qa296/derive296.json` 已還原。SAVE key／softRev 冇郁；index.html 行數不變（46,999）。

## 4 項文風取捨（跟核實表修法）

1. **s12 A6 mak_patron_cold**（index.html ENC79 DLG）：冷版收回引薦對白加半句交代「尊重≠肯擔保」。
   - 原文：「不過，嗰啲位，係要企得穩先有得企。你嗰日話你會驚，我記住咗。唔係話你唔好，係呢啲位，等唔到一個驚字。」
   - 新文：「不過，嗰啲位，係要企得穩先有得企。你嗰日話你會驚，我記住咗。唔係話你唔好——我尊重你夠坦白，但引薦要我擔保，你嗰句驚，我擔唔起。呢啲位，等唔到一個驚字。」
2. **s2 B3 A_tsijun_crisis 旁白收尾**（rival_mentor.json beats[4]）：抒情收尾改懸置收尾，保留張力。
   - 原文：「兩人都沒有再出聲，一起望著阿偉。鏡頭裏站著的，始終是他自己。」
   - 新文：「兩人都沒有再出聲，一起望著阿偉，等他自己開口。」
3. **s3 B3 唐素雲「有人走，有人留」起手式三節點同用**（rival_mentor.json）：push1 保留作錨（首次出現），push2／ending 換起手式。
   - A_tong_push2 beats[0]：原文「有人走，有人留。你諗清楚，你係邊種人。」→ 新文「企得穩嘅人，先留得低。你諗清楚，你係邊種人。」
   - A_tong_ending beats[1]：原文「有人走，有人留。你今日企喺呢度，就要幫手睇住呢個地方。」→ 新文「我走之後，呢度就交畀你哋。你今日企喺呢度，就要幫手睇住呢個地方。」
4. **s7 B3 R_choi_ending 旁白套話**（vera_hiu_choi.json beats[5]）：「沒有解決不了的事」改具體講法，扣返交料／拍戲嘅實際難處。
   - 原文：「他欣賞的正是這份認真。只要坦誠相對，沒有解決不了的事。」
   - 新文：「他欣賞的正是這份認真。日後她要交料、他要拍戲，真撞上了，就攤開來談，不必先替對方擔心。」

## 1 項部分證實（s7 A8 R_tang_meet_stub 鄧麗萍具名）

**成立部分（已修，玩家面）**：節點標題＋beats 仍以鄧麗萍具名，改職銜稱呼「排片部負責人」清名：
- lan_xu.json title：「公關公司偶遇鄧麗萍」→「公關公司偶遇排片部負責人」
- lan_xu.json beats speaker ×3：「鄧麗萍」→「排片部負責人」；自報姓名對白「我是鄧麗萍，負責這次活動的客戶對接。」→「我是排片部負責人，負責這次活動的客戶對接。」
- index.html `normaliseTangStub152` 重寫後嘅 synopsis（玩家面）：「在會議室遇見鄧麗萍。」→「在會議室遇見排片部負責人。」

**不成立部分（冇郁）**：JSON 原稿 synopsis「將影響日後感情線能否正式開啟」＋choices notes「正式開閘」等開閘語言，載入時已被 `normaliseTangStub152` 換走，唔係玩家面，照原稿保留（同 tang152 測試「pack 唔郁」斷言一致）。cast 欄位（結構層，唔屬核實表修法範圍）亦冇郁。

## 測試 resync（邏輯斷言不變）

- `tests/test_rom159_static.py`：新增 `_CRISIS359` 層（A_tsijun_crisis beats[4] 1 處）＋`_FIX359` 層（A_tong_push2／A_tong_ending 2 處），跟 _FIX355/_FIX356/_FIX358 先例逐層對位；兩處最終「逐字一致」斷言標籤更新。
- index.html 兩處改動均同行替換、行數不變，冇釘行漂移；tang152 釘行唔使 resync（實測 PASS）。

## 實駕抽查（`~/workspace/linji-drive359/`，截圖喺 shots/）

Playwright 本地 serve 工作副本＋`StoryPlay.start(force)` 真播：
- A_tsijun_crisis：新收尾在位、舊句清零 ✓（截圖確認渲染）
- A_tong_push2／A_tong_ending：新起手式在位、舊句清零 ✓；A_tong_push1 錨句保留 ✓
- R_choi_ending：新句在位、舊套話清零 ✓
- R_tang_meet_stub（session 實播）：標題／speaker／自報姓名／synopsis 全部清名 ✓
- mak_patron_cold：ENC 常數喺 IIFE 內，數據層對 served 原文核實新交代句在位 ✓

## 唔修（照任務範圍）

2 項判斷唔修（s5 A3 已由 v355 處理、s6 A8 死數據）冇郁；其餘複檢項已全部修完，冇順手改其他嘢。支線＋感情線複檢至此全數結案。
