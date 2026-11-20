# NOTES_V20A343_CRISIS_YEAR_FIX — crisis 頁首年份修復

- 版本：v343（base main `828e76e` v342，suite 395／9，通告庫 323 張，index.html 47,316 行）
- 來源：drive-342 實駕發現（`~/workspace/linji-drive-342/`，choi-crisis-story-act.png＋probe_years.py），parent 親查 live 核實。

## Bug

R_choi_crisis 頁首顯示「主線 · 1991冬」（期望 1992冬）、R_hiu_crisis 顯示 1991秋（期望 1992秋）。

根因：`CONTRA98_WHEN_FIX`（index.html L14652）載入時經 `contra98FixNodeWhen`（L14672，call site L14855，行喺 `years66Walk` 之前）覆寫節點 when/eraTag——
- L14661 `R_choi_crisis:["1989冬","era_1989_winter_gossip"]`
- L14663 `R_hiu_crisis:["1989秋","era_1989_autumn_anni"]`

→ when 經 walk +2 → 1991冬／1991秋；eraTag 顯示時 `years66ShiftYear` +2 → 1991。v342 改嘅 JSON when（1991→1990）俾表冚住，完全無效。

其餘三節點（R_lan_crisis／R_xu_push2／R_xu_crisis）表值本來就係 1990秋，顯示 1992秋 ✓，唔受影響。

附帶更正：v342 NOTES 沙盒聲稱「R_choi_crisis＝主線 · 1992冬」同 live 不符——沙盒用 soft 路徑（`spPlayerMeta_softSeasonFrom`，讀 walked when）推算，live 頁首行 `spPlayerMeta`（L11189，讀 eraTag 優先）。修復前嘅「1993冬」喺 live 從來冇出現過（表自 v98 已在），係沙盒齋 walk JSON 推算出嚟嘅數字。今票新測試抽 live 真函數 `spPlayerMeta` 行完整載入路徑，唔再齋推算。

## 改動（index.html 兩行，同行改動，行數不變 47,316，零釘行漂移）

- L14661：`R_choi_crisis:["1990冬","era_1990_winter_gossip"]`（＋行內註解）
- L14663：`R_hiu_crisis:["1990秋","era_1990_autumn_anni"]`（＋行內註解）

唔郁：JSON when（v342 已改 1990，留返做雙保險）、其他 CONTRA98 條目、節點內容。L7174 註解「CONTRA98_WHEN_FIX 兩項（crisis 1989秋／ending 1990秋）已由 v223 落地」係 v223 落地歷史紀錄，保留唔改。

## eraTag 存檔相容核實

eraTag 係節點 metadata（pack JSON 載入時由 `contra98FixNodeWhen` 覆寫），**唔入存檔**：存檔只存遊戲狀態（story.done／flags 以節點 id 為鍵），唔存節點 when/eraTag。全檔 grep 核實：eraTag 讀者只有 `spPlayerMeta`（L11215，頁首年份推導）同 `spPlayerMeta_softSeasonFrom`（L11124，只讀季節字元）；gig 側 `eraTagLabel`／`eraTagDisplay`（L15803 起）係通告記錄欄位，同故事節點 eraTag 無關。改表值後所有存檔下次載入自動用新值，唔使遷移。季節（冬／秋）不變，季節閘無影響；`storyWeekStamp` 只讀 when 嘅 `W\d+` 週標，唔讀年份。

## spPlayerMeta 年份推導（核實）

`spPlayerMeta`（L11189）：`soft = node.eraTag || node.when` → 抽 `\d{4}` → 有 eraTag 就 `years66ShiftYear(+2)` → 補季節字元 → 「主線 · YYYY季」。改表後：choi era_1990_winter_gossip → 1992冬；hiu era_1990_autumn_anni → 1992秋。when 經 walk 同步 1992冬／1992秋，soft 路徑一致。

## 測試

- 新 `tests/test_r343_crisis_year_fix.js`：**27 項 ALL PASS**（靜態表值＋完整載入路徑 contra98FixNodeWhen→years66Walk→spPlayerMeta 五節點頁首全 1992＋反證：表值還原 1989 即重現 1991 頁首＋JSON when 未郁）。
- 同步兩檔舊測試：`test_contra98_logic.js`（WANT_YEAR98 剔走 choi／hiu，只剩 stub 1991；註解同步）、`test_hiu266_logic.js`（靜態斷言 1989秋→1990秋＋載入鏈 crisis 頁首 1991秋→1992秋）。
- 全套 suite：見落地紀錄（基線 395／9＋新測試檔 1 項）。

## 落地紀錄

- main 內容 commit `02f62f6`（squash merge 工作分支 `7ef4eb1`），已推 GitHub。
- Suite：396 PASS／9 FAIL（v342 基線 395／9＋新測試檔 1 項；九項 FAIL 同基線逐項一致：flash51／slot50／soft_tip_111_restore／start53／weave43／weave44／weave49／wf5_87／wrap38）。證據：`~/workspace/suite343.txt`。
- Pages byte-identical 已核實：index.html md5 `b67d4f04f54e0872377dceae5f03d114`／4,706,725 bytes／47,316 行（+167 bytes 係兩行行內註解，行數不變）。
- `qa296/derive296.json` 已還原；工作副本已刪。
